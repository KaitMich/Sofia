#!/usr/bin/env python3
"""
Domain Rate Limiter - Ethical Crawling Politeness (Async-Upgraded)

Enforces per-domain rate limiting with robots.txt Crawl-delay integration.

**ASYNC UPGRADE:** Supports both sync and async operation
- Async methods use asyncio.sleep() for non-blocking waits
- Sync methods maintained for backwards compatibility
- All async methods have _async suffix

Key Features:
- Minimum 3-second delay between requests to same domain (configurable)
- Syncs with robots.txt Crawl-delay directive (uses higher value)
- Random jitter (0.5-1.5 seconds) to avoid patterns
- SQLite persistence for crash recovery
- Per-domain tracking with complete audit trail

Database Schema:
    domain_requests:
        - domain TEXT PRIMARY KEY
        - last_request_time REAL
        - crawl_delay REAL (configured delay, not just robots.txt)
        - total_requests INTEGER
        - last_url TEXT
        - user_agent TEXT

    request_history:
        - id INTEGER PRIMARY KEY AUTOINCREMENT
        - domain TEXT
        - url TEXT
        - timestamp REAL
        - wait_time REAL (seconds waited before request)
        - user_agent TEXT
"""

import sqlite3
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional, Dict
import time
import random
import logging
import asyncio

# Async imports
try:
    import aiosqlite
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    aiosqlite = None

logger = logging.getLogger(__name__)


class DomainRateLimiter:
    """
    Enforces ethical per-domain rate limiting with robots.txt integration.

    Supports both sync and async operation:
    - Sync methods: wait_if_needed(), record_request(), etc.
    - Async methods: wait_if_needed_async(), record_request_async(), etc.
    """

    DEFAULT_MIN_DELAY = 3.0  # seconds
    JITTER_MIN = 0.5  # seconds
    JITTER_MAX = 1.5  # seconds
    USER_AGENT = "SophiaAutonomousLearner/1.0"

    def __init__(self, data_dir: str = "data", min_delay: float = None):
        """
        Initialize rate limiter.

        Args:
            data_dir: Base directory for data storage
            min_delay: Minimum delay between requests in seconds (default: 3.0)
        """
        self.data_dir = Path(data_dir)
        self.min_delay = min_delay if min_delay is not None else self.DEFAULT_MIN_DELAY
        self.db_path = self.data_dir / "crawl" / "rate_limiter.db"

        # Create data directory if needed
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        logger.info(f"Rate limiter initialized (min_delay: {self.min_delay}s)")

    def _init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Domain tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domain_requests (
                domain TEXT PRIMARY KEY,
                last_request_time REAL NOT NULL,
                crawl_delay REAL NOT NULL,
                total_requests INTEGER NOT NULL DEFAULT 0,
                last_url TEXT,
                user_agent TEXT NOT NULL
            )
        ''')

        # Request history for analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS request_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                url TEXT NOT NULL,
                timestamp REAL NOT NULL,
                wait_time REAL NOT NULL,
                user_agent TEXT NOT NULL
            )
        ''')

        # Create indices
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_history_domain
            ON request_history(domain)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_history_timestamp
            ON request_history(timestamp)
        ''')

        conn.commit()
        conn.close()

        logger.info(f"Rate limiter database initialized at {self.db_path}")

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    # ═══════════════════════════════════════════════════════════════
    # SYNC METHODS (Original - Backwards Compatible)
    # ═══════════════════════════════════════════════════════════════

    def _get_domain_state(self, domain: str) -> Optional[Dict]:
        """
        Get current state for domain (SYNC).

        Returns:
            Dict with last_request_time, crawl_delay, total_requests or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT last_request_time, crawl_delay, total_requests, last_url
            FROM domain_requests
            WHERE domain = ?
        ''', (domain,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'last_request_time': row[0],
                'crawl_delay': row[1],
                'total_requests': row[2],
                'last_url': row[3]
            }
        return None

    def _update_domain_state(self, domain: str, url: str, crawl_delay: Optional[float] = None):
        """Update domain state after request (SYNC)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        current_time = time.time()

        # Get existing state to check if we need to update crawl_delay
        state = self._get_domain_state(domain)

        if state:
            # Update existing
            if crawl_delay is not None:
                # Explicit crawl_delay update
                cursor.execute('''
                    UPDATE domain_requests
                    SET last_request_time = ?,
                        crawl_delay = ?,
                        total_requests = total_requests + 1,
                        last_url = ?
                    WHERE domain = ?
                ''', (current_time, crawl_delay, url, domain))
            else:
                # Just update request time, keep existing crawl_delay
                cursor.execute('''
                    UPDATE domain_requests
                    SET last_request_time = ?,
                        total_requests = total_requests + 1,
                        last_url = ?
                    WHERE domain = ?
                ''', (current_time, url, domain))
        else:
            # Insert new
            effective_delay = crawl_delay if crawl_delay is not None else self.min_delay
            cursor.execute('''
                INSERT INTO domain_requests
                (domain, last_request_time, crawl_delay, total_requests, last_url, user_agent)
                VALUES (?, ?, ?, 1, ?, ?)
            ''', (domain, current_time, effective_delay, url, self.USER_AGENT))

        conn.commit()
        conn.close()

    def set_crawl_delay(self, domain: str, delay: float):
        """
        Explicitly set crawl delay for a domain (SYNC).

        This is typically called when robots.txt Crawl-delay is discovered.

        Args:
            domain: Domain (with scheme, e.g., "https://example.com")
            delay: Crawl delay in seconds
        """
        # Use the higher of min_delay and specified delay
        effective_delay = max(self.min_delay, delay)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if domain exists
        state = self._get_domain_state(domain)

        if state:
            # Update existing
            cursor.execute('''
                UPDATE domain_requests
                SET crawl_delay = ?
                WHERE domain = ?
            ''', (effective_delay, domain))
        else:
            # Insert new (with current time so it doesn't block immediately)
            cursor.execute('''
                INSERT INTO domain_requests
                (domain, last_request_time, crawl_delay, total_requests, user_agent)
                VALUES (?, ?, ?, 0, ?)
            ''', (domain, time.time(), effective_delay, self.USER_AGENT))

        conn.commit()
        conn.close()

        logger.info(f"Set crawl delay for {domain}: {effective_delay}s")

    def get_wait_time(self, url: str, include_jitter: bool = True) -> float:
        """
        Calculate how long to wait before crawling this URL (SYNC).

        Args:
            url: URL to check
            include_jitter: Whether to add random jitter (default: True)

        Returns:
            Seconds to wait (0 if can proceed immediately)
        """
        domain = self._get_domain(url)
        state = self._get_domain_state(domain)

        if not state:
            # First request to this domain - no wait needed
            return 0.0

        # Calculate time since last request
        time_since_last = time.time() - state['last_request_time']
        crawl_delay = state['crawl_delay']

        # Calculate required wait
        base_wait = max(0.0, crawl_delay - time_since_last)

        if include_jitter and base_wait == 0:
            # Add jitter only if we're not already waiting
            # This prevents predictable crawl patterns
            jitter = random.uniform(self.JITTER_MIN, self.JITTER_MAX)
            return jitter
        else:
            return base_wait

    def wait_if_needed(self, url: str) -> float:
        """
        Wait if necessary to respect rate limits, then return (SYNC).

        Args:
            url: URL about to be crawled

        Returns:
            Actual time waited in seconds
        """
        wait_time = self.get_wait_time(url, include_jitter=True)

        if wait_time > 0:
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s before {url}")
            time.sleep(wait_time)

        return wait_time

    def record_request(self, url: str, robots_crawl_delay: Optional[float] = None):
        """
        Record that a request was made to this URL (SYNC).

        Should be called AFTER the request completes.

        Args:
            url: URL that was crawled
            robots_crawl_delay: If robots.txt specifies Crawl-delay, pass it here
        """
        domain = self._get_domain(url)

        # If robots.txt specifies crawl delay, update it
        if robots_crawl_delay is not None:
            effective_delay = max(self.min_delay, robots_crawl_delay)
            self._update_domain_state(domain, url, crawl_delay=effective_delay)
        else:
            self._update_domain_state(domain, url)

        # Record in history
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Calculate wait time that would have been required
        state = self._get_domain_state(domain)
        wait_time = 0.0
        if state and state['total_requests'] > 1:
            # Not first request, calculate what we waited
            # This is approximate since jitter was applied
            wait_time = max(0.0, state['crawl_delay'] - (time.time() - state['last_request_time']))

        cursor.execute('''
            INSERT INTO request_history
            (domain, url, timestamp, wait_time, user_agent)
            VALUES (?, ?, ?, ?, ?)
        ''', (domain, url, time.time(), wait_time, self.USER_AGENT))

        conn.commit()
        conn.close()

    # ═══════════════════════════════════════════════════════════════
    # ASYNC METHODS (New - High Performance)
    # ═══════════════════════════════════════════════════════════════

    async def _get_domain_state_async(self, domain: str) -> Optional[Dict]:
        """
        Get current state for domain (ASYNC).

        Returns:
            Dict with last_request_time, crawl_delay, total_requests or None
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.execute('''
                SELECT last_request_time, crawl_delay, total_requests, last_url
                FROM domain_requests
                WHERE domain = ?
            ''', (domain,)) as cursor:
                row = await cursor.fetchone()

        if row:
            return {
                'last_request_time': row[0],
                'crawl_delay': row[1],
                'total_requests': row[2],
                'last_url': row[3]
            }
        return None

    async def _update_domain_state_async(self, domain: str, url: str, crawl_delay: Optional[float] = None):
        """Update domain state after request (ASYNC)."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        current_time = time.time()

        # Get existing state
        state = await self._get_domain_state_async(domain)

        async with aiosqlite.connect(self.db_path) as conn:
            if state:
                # Update existing
                if crawl_delay is not None:
                    await conn.execute('''
                        UPDATE domain_requests
                        SET last_request_time = ?,
                            crawl_delay = ?,
                            total_requests = total_requests + 1,
                            last_url = ?
                        WHERE domain = ?
                    ''', (current_time, crawl_delay, url, domain))
                else:
                    await conn.execute('''
                        UPDATE domain_requests
                        SET last_request_time = ?,
                            total_requests = total_requests + 1,
                            last_url = ?
                        WHERE domain = ?
                    ''', (current_time, url, domain))
            else:
                # Insert new
                effective_delay = crawl_delay if crawl_delay is not None else self.min_delay
                await conn.execute('''
                    INSERT INTO domain_requests
                    (domain, last_request_time, crawl_delay, total_requests, last_url, user_agent)
                    VALUES (?, ?, ?, 1, ?, ?)
                ''', (domain, current_time, effective_delay, url, self.USER_AGENT))

            await conn.commit()

    async def set_crawl_delay_async(self, domain: str, delay: float):
        """
        Explicitly set crawl delay for a domain (ASYNC).

        Args:
            domain: Domain (with scheme)
            delay: Crawl delay in seconds
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        effective_delay = max(self.min_delay, delay)
        state = await self._get_domain_state_async(domain)

        async with aiosqlite.connect(self.db_path) as conn:
            if state:
                await conn.execute('''
                    UPDATE domain_requests
                    SET crawl_delay = ?
                    WHERE domain = ?
                ''', (effective_delay, domain))
            else:
                await conn.execute('''
                    INSERT INTO domain_requests
                    (domain, last_request_time, crawl_delay, total_requests, user_agent)
                    VALUES (?, ?, ?, 0, ?)
                ''', (domain, time.time(), effective_delay, self.USER_AGENT))

            await conn.commit()

        logger.info(f"Set crawl delay for {domain}: {effective_delay}s (async)")

    async def get_wait_time_async(self, url: str, include_jitter: bool = True) -> float:
        """
        Calculate how long to wait before crawling this URL (ASYNC).

        Args:
            url: URL to check
            include_jitter: Whether to add random jitter

        Returns:
            Seconds to wait (0 if can proceed immediately)
        """
        domain = self._get_domain(url)
        state = await self._get_domain_state_async(domain)

        if not state:
            return 0.0

        time_since_last = time.time() - state['last_request_time']
        crawl_delay = state['crawl_delay']
        base_wait = max(0.0, crawl_delay - time_since_last)

        if include_jitter and base_wait == 0:
            jitter = random.uniform(self.JITTER_MIN, self.JITTER_MAX)
            return jitter
        else:
            return base_wait

    async def wait_if_needed_async(self, url: str) -> float:
        """
        Wait if necessary to respect rate limits, then return (ASYNC).

        Args:
            url: URL about to be crawled

        Returns:
            Actual time waited in seconds
        """
        wait_time = await self.get_wait_time_async(url, include_jitter=True)

        if wait_time > 0:
            logger.debug(f"Rate limiting (async): waiting {wait_time:.2f}s before {url}")
            await asyncio.sleep(wait_time)

        return wait_time

    async def can_request_now_async(self, url: str) -> bool:
        """
        Check if we can request this URL now without waiting (ASYNC).

        Args:
            url: URL to check

        Returns:
            True if can request immediately, False if rate limited
        """
        wait_time = await self.get_wait_time_async(url, include_jitter=False)
        return wait_time == 0.0

    async def record_request_async(self, url: str, robots_crawl_delay: Optional[float] = None):
        """
        Record that a request was made to this URL (ASYNC).

        Should be called AFTER the request completes.

        Args:
            url: URL that was crawled
            robots_crawl_delay: If robots.txt specifies Crawl-delay, pass it here
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        domain = self._get_domain(url)

        # Update domain state
        if robots_crawl_delay is not None:
            effective_delay = max(self.min_delay, robots_crawl_delay)
            await self._update_domain_state_async(domain, url, crawl_delay=effective_delay)
        else:
            await self._update_domain_state_async(domain, url)

        # Record in history
        state = await self._get_domain_state_async(domain)
        wait_time = 0.0
        if state and state['total_requests'] > 1:
            wait_time = max(0.0, state['crawl_delay'] - (time.time() - state['last_request_time']))

        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute('''
                INSERT INTO request_history
                (domain, url, timestamp, wait_time, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (domain, url, time.time(), wait_time, self.USER_AGENT))
            await conn.commit()

    # ═══════════════════════════════════════════════════════════════
    # UTILITY METHODS (Sync - Backwards Compatible)
    # ═══════════════════════════════════════════════════════════════

    def get_stats(self) -> Dict:
        """Get rate limiter statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total domains tracked
        cursor.execute('SELECT COUNT(*) FROM domain_requests')
        total_domains = cursor.fetchone()[0]

        # Total requests
        cursor.execute('SELECT SUM(total_requests) FROM domain_requests')
        total_requests_row = cursor.fetchone()
        total_requests = total_requests_row[0] if total_requests_row[0] else 0

        # Average crawl delay
        cursor.execute('SELECT AVG(crawl_delay) FROM domain_requests')
        avg_delay_row = cursor.fetchone()
        avg_crawl_delay = avg_delay_row[0] if avg_delay_row[0] else self.min_delay

        # Most crawled domain
        cursor.execute('''
            SELECT domain, total_requests
            FROM domain_requests
            ORDER BY total_requests DESC
            LIMIT 1
        ''')
        most_crawled = cursor.fetchone()

        # Average wait time (last 1000 requests)
        cursor.execute('''
            SELECT AVG(wait_time)
            FROM (
                SELECT wait_time FROM request_history
                ORDER BY timestamp DESC
                LIMIT 1000
            )
        ''')
        avg_wait_row = cursor.fetchone()
        avg_wait_time = avg_wait_row[0] if avg_wait_row[0] else 0.0

        conn.close()

        return {
            'total_domains': total_domains,
            'total_requests': total_requests,
            'avg_crawl_delay': avg_crawl_delay,
            'min_delay_setting': self.min_delay,
            'most_crawled_domain': most_crawled[0] if most_crawled else None,
            'most_crawled_count': most_crawled[1] if most_crawled else 0,
            'avg_wait_time_recent': avg_wait_time,
            'async_available': ASYNC_AVAILABLE
        }

    def get_domain_stats(self, url: str) -> Dict:
        """Get statistics for a specific domain."""
        domain = self._get_domain(url)
        state = self._get_domain_state(domain)

        if not state:
            return {
                'domain': domain,
                'tracked': False,
                'message': 'Domain not yet tracked'
            }

        # Get request history
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                MIN(timestamp) as first_request,
                MAX(timestamp) as last_request,
                COUNT(*) as total_history
            FROM request_history
            WHERE domain = ?
        ''', (domain,))

        history = cursor.fetchone()
        conn.close()

        time_since_last = time.time() - state['last_request_time']
        can_crawl_now = time_since_last >= state['crawl_delay']

        return {
            'domain': domain,
            'tracked': True,
            'crawl_delay': state['crawl_delay'],
            'total_requests': state['total_requests'],
            'last_url': state['last_url'],
            'time_since_last_request': time_since_last,
            'can_crawl_now': can_crawl_now,
            'wait_time_needed': max(0.0, state['crawl_delay'] - time_since_last),
            'first_request': history[0] if history[0] else None,
            'last_request': history[1] if history[1] else None
        }

    def clear_domain(self, domain: str):
        """Clear rate limiting state for a specific domain."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM domain_requests WHERE domain = ?', (domain,))
        deleted = cursor.rowcount

        conn.commit()
        conn.close()

        if deleted > 0:
            logger.info(f"Cleared rate limiter state for {domain}")
        return deleted > 0

    def clear_all(self):
        """Clear all rate limiting state."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM domain_requests')
        cursor.execute('DELETE FROM request_history')

        conn.commit()
        conn.close()

        logger.info("Cleared all rate limiter state")


if __name__ == "__main__":
    # Demo usage
    import logging
    logging.basicConfig(level=logging.INFO)

    limiter = DomainRateLimiter(min_delay=2.0)

    # Test sync mode
    print("=" * 60)
    print("SYNC MODE TEST")
    print("=" * 60)

    test_url = "https://example.com/page1"
    print(f"\nTesting: {test_url}\n")

    # First request - should be immediate
    wait1 = limiter.get_wait_time(test_url)
    print(f"First request - wait time: {wait1:.2f}s")

    limiter.record_request(test_url, robots_crawl_delay=5.0)

    # Second request - should require waiting
    wait2 = limiter.get_wait_time(test_url)
    print(f"Second request (immediately after) - wait time: {wait2:.2f}s")

    stats = limiter.get_stats()
    print(f"\nStats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test async mode if available
    if ASYNC_AVAILABLE:
        print("\n" + "=" * 60)
        print("ASYNC MODE TEST")
        print("=" * 60)

        async def test_async():
            test_urls = [
                "https://example.com/page1",
                "https://example.com/page2",
                "https://another.com/page"
            ]

            print(f"\nTesting {len(test_urls)} URLs with async rate limiting...\n")

            for url in test_urls:
                wait_time = await limiter.wait_if_needed_async(url)
                print(f"{url}: waited {wait_time:.2f}s")
                await limiter.record_request_async(url)

        asyncio.run(test_async())
    else:
        print("\n⚠️  Async mode not available (install aiosqlite)")
