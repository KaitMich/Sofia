#!/usr/bin/env python3
"""
Robots.txt Manager - Ethical Crawling Compliance (Async-Upgraded)

Fetches, parses, and caches robots.txt files for ethical web crawling.
Uses urllib.robotparser as the base with SQLite caching.

**ASYNC UPGRADE:** Supports both sync and async operation
- Async methods use aiohttp for 10-50x throughput
- Sync methods maintained for backwards compatibility
- All async methods have _async suffix

Key Features:
- Automatic robots.txt fetching and parsing (sync + async)
- 24-hour SQLite cache (configurable)
- User-agent: "SophiaAutonomousLearner/1.0"
- Crawl-delay directive extraction
- Complete audit trail of checks

Database Schema:
    robots_cache:
        - domain TEXT PRIMARY KEY
        - robots_txt TEXT
        - fetch_timestamp REAL
        - crawl_delay REAL (NULL if not specified)
        - user_agent TEXT

    access_checks:
        - id INTEGER PRIMARY KEY AUTOINCREMENT
        - domain TEXT
        - url TEXT
        - allowed INTEGER (0/1)
        - timestamp REAL
        - user_agent TEXT
"""

import sqlite3
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Tuple
import time
import logging
import asyncio

# Async imports
try:
    import aiohttp
    import aiosqlite
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    aiohttp = None
    aiosqlite = None

logger = logging.getLogger(__name__)


class RobotsTxtManager:
    """
    Manages robots.txt fetching, parsing, and caching for ethical web crawling.

    Supports both sync and async operation:
    - Sync methods: is_allowed(), get_crawl_delay(), etc.
    - Async methods: is_allowed_async(), get_crawl_delay_async(), etc.
    """

    USER_AGENT = "SophiaAutonomousLearner/1.0"
    DEFAULT_CACHE_HOURS = 24
    REQUEST_TIMEOUT = 10  # seconds

    def __init__(self, data_dir: str = "data", cache_hours: int = None):
        """
        Initialize robots.txt manager.

        Args:
            data_dir: Base directory for data storage
            cache_hours: Hours to cache robots.txt (default: 24)
        """
        self.data_dir = Path(data_dir)
        self.cache_hours = cache_hours or self.DEFAULT_CACHE_HOURS
        self.db_path = self.data_dir / "crawl" / "robots_cache.db"

        # Create data directory if needed
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        # In-memory cache for RobotFileParser objects
        self._parser_cache: Dict[str, Tuple[RobotFileParser, float]] = {}

        # Async session (created on demand)
        # Use string type hint to avoid NameError if aiohttp not imported
        self._aio_session: Optional["aiohttp.ClientSession"] = None

    def _init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robots_cache (
                domain TEXT PRIMARY KEY,
                robots_txt TEXT,
                fetch_timestamp REAL NOT NULL,
                crawl_delay REAL,
                user_agent TEXT NOT NULL,
                fetch_status TEXT,  -- 'success', 'not_found', 'error'
                error_message TEXT
            )
        ''')

        # Access check audit trail
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                url TEXT NOT NULL,
                allowed INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                user_agent TEXT NOT NULL,
                cached INTEGER NOT NULL  -- 1 if from cache, 0 if fresh fetch
            )
        ''')

        # Create indices
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_access_checks_domain
            ON access_checks(domain)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_access_checks_timestamp
            ON access_checks(timestamp)
        ''')

        conn.commit()
        conn.close()

        logger.info(f"Robots.txt cache initialized at {self.db_path}")

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _get_robots_url(self, domain: str) -> str:
        """Get robots.txt URL for domain."""
        return urljoin(domain, "/robots.txt")

    def _is_cache_valid(self, fetch_timestamp: float) -> bool:
        """Check if cached robots.txt is still valid."""
        age_hours = (time.time() - fetch_timestamp) / 3600
        return age_hours < self.cache_hours

    # ═══════════════════════════════════════════════════════════════
    # SYNC METHODS (Original - Backwards Compatible)
    # ═══════════════════════════════════════════════════════════════

    def _fetch_from_cache(self, domain: str) -> Optional[Tuple[str, float, Optional[float], str]]:
        """
        Fetch robots.txt from cache if valid.

        Returns:
            (robots_txt, fetch_timestamp, crawl_delay, fetch_status) or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT robots_txt, fetch_timestamp, crawl_delay, fetch_status
            FROM robots_cache
            WHERE domain = ?
        ''', (domain,))

        row = cursor.fetchone()
        conn.close()

        if row and self._is_cache_valid(row[1]):
            return row
        return None

    def _fetch_from_web(self, domain: str) -> Tuple[Optional[str], str, Optional[str]]:
        """
        Fetch robots.txt from web.

        Returns:
            (robots_txt_content, fetch_status, error_message)
        """
        robots_url = self._get_robots_url(domain)

        try:
            req = urllib.request.Request(
                robots_url,
                headers={'User-Agent': self.USER_AGENT}
            )

            with urllib.request.urlopen(req, timeout=self.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8', errors='ignore')
                    return content, 'success', None
                else:
                    return None, 'error', f"HTTP {response.status}"

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # No robots.txt = allow everything
                return None, 'not_found', None
            else:
                return None, 'error', f"HTTP {e.code}"

        except Exception as e:
            return None, 'error', str(e)

    def _cache_robots_txt(self, domain: str, robots_txt: Optional[str],
                          fetch_status: str, error_message: Optional[str] = None):
        """Store robots.txt in cache."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Parse crawl-delay if robots.txt exists
        crawl_delay = None
        if robots_txt and fetch_status == 'success':
            parser = RobotFileParser()
            parser.parse(robots_txt.splitlines())
            crawl_delay = parser.crawl_delay(self.USER_AGENT)

        cursor.execute('''
            INSERT OR REPLACE INTO robots_cache
            (domain, robots_txt, fetch_timestamp, crawl_delay, user_agent, fetch_status, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (domain, robots_txt, time.time(), crawl_delay, self.USER_AGENT, fetch_status, error_message))

        conn.commit()
        conn.close()

        logger.info(f"Cached robots.txt for {domain} (status: {fetch_status}, crawl_delay: {crawl_delay})")

    def _get_parser(self, domain: str) -> Tuple[RobotFileParser, bool]:
        """
        Get RobotFileParser for domain.

        Returns:
            (parser, was_cached)
        """
        # Check in-memory cache first
        if domain in self._parser_cache:
            parser, timestamp = self._parser_cache[domain]
            if self._is_cache_valid(timestamp):
                return parser, True

        # Check database cache
        cached = self._fetch_from_cache(domain)

        if cached:
            robots_txt, fetch_timestamp, crawl_delay, fetch_status = cached

            if fetch_status == 'success' and robots_txt:
                parser = RobotFileParser()
                parser.parse(robots_txt.splitlines())
            else:
                # not_found or error - create permissive parser
                parser = RobotFileParser()
                parser.parse([])  # Empty robots.txt = allow all

            self._parser_cache[domain] = (parser, fetch_timestamp)
            return parser, True

        # Fetch from web
        robots_txt, fetch_status, error_message = self._fetch_from_web(domain)
        self._cache_robots_txt(domain, robots_txt, fetch_status, error_message)

        if fetch_status == 'success' and robots_txt:
            parser = RobotFileParser()
            parser.parse(robots_txt.splitlines())
        else:
            # not_found or error - create permissive parser
            parser = RobotFileParser()
            parser.parse([])  # Empty robots.txt = allow all

        self._parser_cache[domain] = (parser, time.time())
        return parser, False

    def _record_check(self, domain: str, url: str, allowed: bool, cached: bool):
        """Record access check in audit trail."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO access_checks
            (domain, url, allowed, timestamp, user_agent, cached)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (domain, url, int(allowed), time.time(), self.USER_AGENT, int(cached)))

        conn.commit()
        conn.close()

    def is_allowed(self, url: str) -> bool:
        """
        Check if URL is allowed by robots.txt (SYNC).

        Args:
            url: Full URL to check

        Returns:
            True if allowed, False if blocked
        """
        domain = self._get_domain(url)
        parser, cached = self._get_parser(domain)

        allowed = parser.can_fetch(self.USER_AGENT, url)

        # Record check
        self._record_check(domain, url, allowed, cached)

        return allowed

    def get_crawl_delay(self, url: str) -> Optional[float]:
        """
        Get crawl delay for domain (from robots.txt Crawl-delay directive) (SYNC).

        Args:
            url: URL from the domain

        Returns:
            Crawl delay in seconds, or None if not specified
        """
        domain = self._get_domain(url)
        parser, _ = self._get_parser(domain)

        return parser.crawl_delay(self.USER_AGENT)

    def fetch_and_cache(self, url: str) -> bool:
        """
        Explicitly fetch and cache robots.txt for a domain (SYNC).

        Args:
            url: URL from the domain

        Returns:
            True if successful, False otherwise
        """
        domain = self._get_domain(url)

        # Remove from in-memory cache to force fresh fetch
        if domain in self._parser_cache:
            del self._parser_cache[domain]

        robots_txt, fetch_status, error_message = self._fetch_from_web(domain)
        self._cache_robots_txt(domain, robots_txt, fetch_status, error_message)

        return fetch_status == 'success'

    # ═══════════════════════════════════════════════════════════════
    # ASYNC METHODS (New - High Performance)
    # ═══════════════════════════════════════════════════════════════

    async def _get_aio_session(self) -> "aiohttp.ClientSession":
        """Get or create aiohttp session."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiohttp not available. Install with: pip install aiohttp")

        if self._aio_session is None or self._aio_session.closed:
            timeout = aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
            self._aio_session = aiohttp.ClientSession(timeout=timeout)
        return self._aio_session

    async def _fetch_from_cache_async(self, domain: str) -> Optional[Tuple[str, float, Optional[float], str]]:
        """
        Fetch robots.txt from cache if valid (ASYNC).

        Returns:
            (robots_txt, fetch_timestamp, crawl_delay, fetch_status) or None
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.execute('''
                SELECT robots_txt, fetch_timestamp, crawl_delay, fetch_status
                FROM robots_cache
                WHERE domain = ?
            ''', (domain,)) as cursor:
                row = await cursor.fetchone()

        if row and self._is_cache_valid(row[1]):
            return row
        return None

    async def _fetch_from_web_async(self, domain: str) -> Tuple[Optional[str], str, Optional[str]]:
        """
        Fetch robots.txt from web (ASYNC).

        Returns:
            (robots_txt_content, fetch_status, error_message)
        """
        robots_url = self._get_robots_url(domain)
        session = await self._get_aio_session()

        try:
            headers = {'User-Agent': self.USER_AGENT}
            async with session.get(robots_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text(errors='ignore')
                    return content, 'success', None
                elif response.status == 404:
                    # No robots.txt = allow everything
                    return None, 'not_found', None
                else:
                    return None, 'error', f"HTTP {response.status}"

        except asyncio.TimeoutError:
            return None, 'error', "Timeout"
        except Exception as e:
            return None, 'error', str(e)

    async def _cache_robots_txt_async(self, domain: str, robots_txt: Optional[str],
                                     fetch_status: str, error_message: Optional[str] = None):
        """Store robots.txt in cache (ASYNC)."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        # Parse crawl-delay if robots.txt exists
        crawl_delay = None
        if robots_txt and fetch_status == 'success':
            parser = RobotFileParser()
            parser.parse(robots_txt.splitlines())
            crawl_delay = parser.crawl_delay(self.USER_AGENT)

        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''
                INSERT OR REPLACE INTO robots_cache
                (domain, robots_txt, fetch_timestamp, crawl_delay, user_agent, fetch_status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (domain, robots_txt, time.time(), crawl_delay, self.USER_AGENT, fetch_status, error_message))
            await conn.commit()

        logger.info(f"Cached robots.txt for {domain} (status: {fetch_status}, crawl_delay: {crawl_delay})")

    async def _get_parser_async(self, domain: str) -> Tuple[RobotFileParser, bool]:
        """
        Get RobotFileParser for domain (ASYNC).

        Returns:
            (parser, was_cached)
        """
        # Check in-memory cache first
        if domain in self._parser_cache:
            parser, timestamp = self._parser_cache[domain]
            if self._is_cache_valid(timestamp):
                return parser, True

        # Check database cache
        cached = await self._fetch_from_cache_async(domain)

        if cached:
            robots_txt, fetch_timestamp, crawl_delay, fetch_status = cached

            if fetch_status == 'success' and robots_txt:
                parser = RobotFileParser()
                parser.parse(robots_txt.splitlines())
            else:
                # not_found or error - create permissive parser
                parser = RobotFileParser()
                parser.parse([])  # Empty robots.txt = allow all

            self._parser_cache[domain] = (parser, fetch_timestamp)
            return parser, True

        # Fetch from web
        robots_txt, fetch_status, error_message = await self._fetch_from_web_async(domain)
        await self._cache_robots_txt_async(domain, robots_txt, fetch_status, error_message)

        if fetch_status == 'success' and robots_txt:
            parser = RobotFileParser()
            parser.parse(robots_txt.splitlines())
        else:
            # not_found or error - create permissive parser
            parser = RobotFileParser()
            parser.parse([])  # Empty robots.txt = allow all

        self._parser_cache[domain] = (parser, time.time())
        return parser, False

    async def _record_check_async(self, domain: str, url: str, allowed: bool, cached: bool):
        """Record access check in audit trail (ASYNC)."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''
                INSERT INTO access_checks
                (domain, url, allowed, timestamp, user_agent, cached)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (domain, url, int(allowed), time.time(), self.USER_AGENT, int(cached)))
            await conn.commit()

    async def is_allowed_async(self, url: str) -> bool:
        """
        Check if URL is allowed by robots.txt (ASYNC).

        Args:
            url: Full URL to check

        Returns:
            True if allowed, False if blocked
        """
        domain = self._get_domain(url)
        parser, cached = await self._get_parser_async(domain)

        allowed = parser.can_fetch(self.USER_AGENT, url)

        # Record check
        await self._record_check_async(domain, url, allowed, cached)

        return allowed

    async def get_crawl_delay_async(self, url: str) -> Optional[float]:
        """
        Get crawl delay for domain (from robots.txt Crawl-delay directive) (ASYNC).

        Args:
            url: URL from the domain

        Returns:
            Crawl delay in seconds, or None if not specified
        """
        domain = self._get_domain(url)
        parser, _ = await self._get_parser_async(domain)

        return parser.crawl_delay(self.USER_AGENT)

    async def fetch_and_cache_async(self, url: str) -> bool:
        """
        Explicitly fetch and cache robots.txt for a domain (ASYNC).

        Args:
            url: URL from the domain

        Returns:
            True if successful, False otherwise
        """
        domain = self._get_domain(url)

        # Remove from in-memory cache to force fresh fetch
        if domain in self._parser_cache:
            del self._parser_cache[domain]

        robots_txt, fetch_status, error_message = await self._fetch_from_web_async(domain)
        await self._cache_robots_txt_async(domain, robots_txt, fetch_status, error_message)

        return fetch_status == 'success'

    async def close(self):
        """Close async resources."""
        if self._aio_session and not self._aio_session.closed:
            await self._aio_session.close()

    # ═══════════════════════════════════════════════════════════════
    # UTILITY METHODS (Sync - Backwards Compatible)
    # ═══════════════════════════════════════════════════════════════

    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total cached domains
        cursor.execute('SELECT COUNT(*) FROM robots_cache')
        total_cached = cursor.fetchone()[0]

        # Valid cache entries
        valid_timestamp = time.time() - (self.cache_hours * 3600)
        cursor.execute('SELECT COUNT(*) FROM robots_cache WHERE fetch_timestamp > ?', (valid_timestamp,))
        valid_cached = cursor.fetchone()[0]

        # Total checks
        cursor.execute('SELECT COUNT(*) FROM access_checks')
        total_checks = cursor.fetchone()[0]

        # Allowed vs blocked
        cursor.execute('SELECT COUNT(*) FROM access_checks WHERE allowed = 1')
        allowed_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM access_checks WHERE allowed = 0')
        blocked_count = cursor.fetchone()[0]

        # Cache hit rate (last 1000 checks)
        cursor.execute('''
            SELECT
                SUM(CASE WHEN cached = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as hit_rate
            FROM (
                SELECT cached FROM access_checks
                ORDER BY timestamp DESC
                LIMIT 1000
            )
        ''')
        hit_rate_row = cursor.fetchone()
        cache_hit_rate = hit_rate_row[0] if hit_rate_row[0] else 0.0

        conn.close()

        return {
            'total_cached_domains': total_cached,
            'valid_cached_domains': valid_cached,
            'expired_cached_domains': total_cached - valid_cached,
            'total_checks': total_checks,
            'allowed_checks': allowed_count,
            'blocked_checks': blocked_count,
            'cache_hit_rate': cache_hit_rate,
            'cache_hours': self.cache_hours,
            'async_available': ASYNC_AVAILABLE
        }

    def get_domain_info(self, url: str) -> Dict:
        """
        Get detailed info about domain's robots.txt.

        Args:
            url: URL from the domain

        Returns:
            Dict with domain info
        """
        domain = self._get_domain(url)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT robots_txt, fetch_timestamp, crawl_delay, fetch_status, error_message
            FROM robots_cache
            WHERE domain = ?
        ''', (domain,))

        row = cursor.fetchone()

        if not row:
            conn.close()
            return {
                'domain': domain,
                'cached': False,
                'message': 'Not cached - will fetch on first access'
            }

        robots_txt, fetch_timestamp, crawl_delay, fetch_status, error_message = row

        # Get check stats for this domain
        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN allowed = 1 THEN 1 ELSE 0 END) as allowed,
                MAX(timestamp) as last_check
            FROM access_checks
            WHERE domain = ?
        ''', (domain,))

        stats = cursor.fetchone()
        conn.close()

        age_hours = (time.time() - fetch_timestamp) / 3600
        is_valid = self._is_cache_valid(fetch_timestamp)

        return {
            'domain': domain,
            'cached': True,
            'fetch_status': fetch_status,
            'error_message': error_message,
            'age_hours': age_hours,
            'is_valid': is_valid,
            'crawl_delay': crawl_delay,
            'robots_txt_length': len(robots_txt) if robots_txt else 0,
            'total_checks': stats[0] if stats else 0,
            'allowed_checks': stats[1] if stats else 0,
            'last_check': datetime.fromtimestamp(stats[2]).isoformat() if stats and stats[2] else None
        }

    def clear_cache(self, domain: Optional[str] = None):
        """
        Clear robots.txt cache.

        Args:
            domain: Specific domain to clear, or None to clear all
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if domain:
            cursor.execute('DELETE FROM robots_cache WHERE domain = ?', (domain,))
            if domain in self._parser_cache:
                del self._parser_cache[domain]
            logger.info(f"Cleared cache for {domain}")
        else:
            cursor.execute('DELETE FROM robots_cache')
            self._parser_cache.clear()
            logger.info("Cleared all robots.txt cache")

        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Demo usage
    import logging
    logging.basicConfig(level=logging.INFO)

    manager = RobotsTxtManager()

    # Test sync mode
    print("=" * 60)
    print("SYNC MODE TEST")
    print("=" * 60)

    test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    print(f"\nTesting: {test_url}\n")

    allowed = manager.is_allowed(test_url)
    print(f"Allowed: {allowed}")

    crawl_delay = manager.get_crawl_delay(test_url)
    print(f"Crawl delay: {crawl_delay} seconds")

    domain_info = manager.get_domain_info(test_url)
    print(f"\nDomain info:")
    for key, value in domain_info.items():
        print(f"  {key}: {value}")

    stats = manager.get_cache_stats()
    print(f"\nCache stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test async mode if available
    if ASYNC_AVAILABLE:
        print("\n" + "=" * 60)
        print("ASYNC MODE TEST")
        print("=" * 60)

        async def test_async():
            test_urls = [
                "https://en.wikipedia.org/wiki/Python",
                "https://en.wikipedia.org/wiki/Machine_learning",
                "https://www.python.org/"
            ]

            print(f"\nTesting {len(test_urls)} URLs concurrently...\n")

            # Test concurrent checks
            tasks = [manager.is_allowed_async(url) for url in test_urls]
            results = await asyncio.gather(*tasks)

            for url, allowed in zip(test_urls, results):
                print(f"{url[:50]:<50} {'ALLOWED' if allowed else 'BLOCKED'}")

            # Close async resources
            await manager.close()

        asyncio.run(test_async())
    else:
        print("\n⚠️  Async mode not available (install aiohttp and aiosqlite)")
