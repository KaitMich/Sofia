#!/usr/bin/env python3
"""
Persistent URL Queue - Crash-Resilient Crawling

SQLite-backed priority queue with crash recovery and retry logic.

Key Features:
- SQLite persistence (survives crashes and restarts)
- Priority queue (higher priority = crawled first)
- Depth tracking (for bounded crawling)
- Status tracking (pending/in_progress/completed/failed/blocked)
- Automatic retry with exponential backoff
- Crash recovery (detect interrupted crawls)
- Domain-aware ordering (distributes load across domains)
- Complete audit trail
- **ASYNC SUPPORT** - Non-blocking DB operations using aiosqlite

Database Schema:
    url_queue:
        - id INTEGER PRIMARY KEY
        - url TEXT UNIQUE
        - domain TEXT
        - priority INTEGER (higher = more important)
        - depth INTEGER (link depth from seed)
        - status TEXT (pending/in_progress/completed/failed/blocked_robots/blocked_immune)
        - added_timestamp REAL
        - started_timestamp REAL (when crawl started)
        - completed_timestamp REAL (when crawl finished)
        - error_count INTEGER (retry counter)
        - last_error TEXT
        - source_url TEXT (where we found this URL)
        - metadata TEXT (JSON for extra info)

Status Values:
    - pending: Not yet crawled
    - in_progress: Currently being crawled
    - completed: Successfully crawled
    - failed: Failed after max retries
    - blocked_robots: Blocked by robots.txt
    - blocked_immune: Blocked by immune system
"""

import sqlite3
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import time
import json
import logging

# Async support (graceful degradation if not installed)
try:
    import aiosqlite
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    aiosqlite = None

logger = logging.getLogger(__name__)


# ============================================================================
# URL CRAWLABILITY FILTER
# Enforced at every enqueue point so unfetchable/no-content URLs never enter
# the queue, regardless of which caller discovered them.
# ============================================================================

# MediaWiki non-article namespaces — navigation/meta pages, not knowledge content
_WIKI_META_NAMESPACES = (
    'category', 'talk', 'wikipedia', 'special', 'file', 'image', 'template',
    'portal', 'help', 'draft', 'user', 'module', 'mediawiki', 'book',
    'timedtext', 'gadget', 'gadget_definition',
)

# File extensions the text pipeline cannot parse
_UNPARSEABLE_EXTENSIONS = (
    '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',
    '.zip', '.gz', '.tar', '.bz2', '.7z', '.rar',
    '.mp3', '.mp4', '.avi', '.mov', '.webm', '.ogg', '.wav',
    '.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.csv',
    '.css', '.js', '.woff', '.woff2', '.ttf',
)

# Pure redirect/resolver hosts — never serve content themselves
_RESOLVER_HOSTS = ('doi.org', 'dx.doi.org')

# Path fragments of CGI viewers/apps that never yield article text
_UNFETCHABLE_PATH_FRAGMENTS = ('/cgi-bin/', 'jmol.php', 'action=edit', 'action=history')


def is_crawlable_url(url: str) -> Tuple[bool, str]:
    """Cheap static check: can this URL possibly yield storable text content?

    Returns (True, '') or (False, reason). Operational filtering only —
    judges fetchability and content format, never subject matter.
    """
    try:
        parsed = urlparse(url)
    except (ValueError, AttributeError):
        return False, 'unparseable url'

    if parsed.scheme not in ('http', 'https'):
        return False, f'scheme {parsed.scheme or "none"}'

    host = (parsed.netloc or '').lower()
    path = (parsed.path or '').lower()

    if host in _RESOLVER_HOSTS:
        return False, 'redirect resolver host'

    for fragment in _UNFETCHABLE_PATH_FRAGMENTS:
        if fragment in path or fragment in (parsed.query or '').lower():
            return False, f'unfetchable path ({fragment})'

    for ext in _UNPARSEABLE_EXTENSIONS:
        if path.endswith(ext):
            return False, f'unparseable extension ({ext})'

    # MediaWiki namespace pages: /wiki/Category:X, /wiki/Talk:X, /wiki/User_talk:X ...
    if '/wiki/' in path:
        page = path.split('/wiki/', 1)[1]
        if ':' in page:
            namespace = page.split(':', 1)[0].replace('%20', '_')
            base_namespace = namespace[:-5] if namespace.endswith('_talk') else namespace
            if base_namespace in _WIKI_META_NAMESPACES or namespace == 'talk':
                return False, f'wiki meta namespace ({namespace})'
        if '(disambiguation)' in page or '%28disambiguation%29' in page:
            return False, 'disambiguation page'

    return True, ''


# Error-text markers meaning a retry can never succeed
_PERMANENT_ERROR_MARKERS = (
    '404', '403', '401', '410', '451',
    'getaddrinfo failed', 'nameresolutionerror', 'name or service not known',
    'certificate verify failed', 'unsupported url', 'invalid url',
    'blocked by robots',
)


def is_permanent_error(error: str) -> bool:
    """Classify an error message: permanent (don't retry) vs transient (retry)."""
    lowered = (error or '').lower()
    return any(marker in lowered for marker in _PERMANENT_ERROR_MARKERS)


class PersistentURLQueue:
    """
    SQLite-backed priority queue for reliable URL crawling.

    Supports both sync and async operations.
    Sync methods: add(), get_next(), mark_completed(), etc.
    Async methods: add_url_async(), get_next_async(), update_status_async(), etc.
    """

    MAX_RETRIES = 3
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_BLOCKED_ROBOTS = 'blocked_robots'
    STATUS_BLOCKED_IMMUNE = 'blocked_immune'
    STATUS_DEFERRED = 'deferred'

    def __init__(self, data_dir: str = "data"):
        """
        Initialize persistent URL queue.

        Args:
            data_dir: Base directory for data storage
        """
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "crawl" / "url_queue.db"

        # Create data directory if needed
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        # Recover any interrupted crawls
        self._recover_interrupted()

        logger.info(f"URL queue initialized at {self.db_path} (async_available: {ASYNC_AVAILABLE})")

    def _init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main queue table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                domain TEXT NOT NULL,
                priority INTEGER NOT NULL DEFAULT 0,
                depth INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'pending',
                added_timestamp REAL NOT NULL,
                started_timestamp REAL,
                completed_timestamp REAL,
                error_count INTEGER NOT NULL DEFAULT 0,
                last_error TEXT,
                source_url TEXT,
                metadata TEXT
            )
        ''')

        # Create indices for efficient querying
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_queue_status_priority
            ON url_queue(status, priority DESC, added_timestamp)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_queue_domain
            ON url_queue(domain)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_queue_url
            ON url_queue(url)
        ''')

        conn.commit()
        conn.close()

        logger.info(f"URL queue database initialized at {self.db_path}")

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _recover_interrupted(self):
        """
        Recover URLs that were 'in_progress' when system crashed.

        These are reset to 'pending' so they can be retried.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE url_queue
            SET status = ?, error_count = error_count + 1
            WHERE status = ?
        ''', (self.STATUS_PENDING, self.STATUS_IN_PROGRESS))

        recovered = cursor.rowcount
        conn.commit()
        conn.close()

        if recovered > 0:
            logger.warning(f"Recovered {recovered} interrupted URLs (reset to pending)")

        return recovered

    def peek_pending(self, limit: int = 20) -> List[Dict]:
        """
        Peek at top pending URLs without changing their status.

        Returns URL info dicts sorted by priority DESC, oldest first.
        Does NOT mark them as in_progress — purely read-only.

        Args:
            limit: Maximum number of URLs to return

        Returns:
            List of dicts with url, priority, depth, domain keys
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT url, priority, depth, domain
            FROM url_queue
            WHERE status = ?
            ORDER BY priority DESC, added_timestamp ASC
            LIMIT ?
        ''', (self.STATUS_PENDING, limit))

        rows = cursor.fetchall()
        conn.close()

        return [
            {'url': row[0], 'priority': row[1], 'depth': row[2], 'domain': row[3]}
            for row in rows
        ]

    def peek_candidates(self, limit: int = 150) -> List[Dict]:
        """Read-only sample of pending+deferred URLs with anchor text.

        Feeds embedding-based curiosity targeting: these are links Sofia
        herself discovered in prior sessions, with the anchor text they
        were discovered under (when recorded at defer time).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT url, priority, depth, domain, metadata
            FROM url_queue
            WHERE status IN (?, ?)
            ORDER BY priority DESC, added_timestamp ASC
            LIMIT ?
        ''', (self.STATUS_PENDING, self.STATUS_DEFERRED, limit))
        rows = cursor.fetchall()
        conn.close()

        candidates = []
        for url, priority, depth, domain, metadata in rows:
            anchor = None
            if metadata:
                try:
                    anchor = json.loads(metadata).get('anchor_text')
                except (ValueError, AttributeError):
                    pass
            candidates.append({'url': url, 'priority': priority, 'depth': depth,
                               'domain': domain, 'anchor_text': anchor})
        return candidates

    # ========================================================================
    # SYNC METHODS (Original - Preserved for Backwards Compatibility)
    # ========================================================================

    def add(self, url: str, priority: int = 0, depth: int = 0,
            source_url: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """
        Add URL to queue (SYNC).

        Args:
            url: URL to add
            priority: Priority (higher = crawled sooner)
            depth: Link depth from seed
            source_url: URL where this was discovered
            metadata: Optional metadata dict

        Returns:
            True if added, False if already exists
        """
        crawlable, filter_reason = is_crawlable_url(url)
        if not crawlable:
            logger.debug(f"Filtered at enqueue ({filter_reason}): {url}")
            return False

        domain = self._get_domain(url)
        metadata_json = json.dumps(metadata) if metadata else None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO url_queue
                (url, domain, priority, depth, status, added_timestamp, source_url, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (url, domain, priority, depth, self.STATUS_PENDING,
                  time.time(), source_url, metadata_json))

            conn.commit()
            logger.debug(f"Added to queue: {url} (priority: {priority}, depth: {depth})")
            return True

        except sqlite3.IntegrityError:
            # URL already exists
            logger.debug(f"URL already in queue: {url}")
            return False

        finally:
            conn.close()

    def add_batch(self, urls: List[Tuple[str, int, int]]) -> int:
        """
        Add multiple URLs in batch (SYNC).

        Args:
            urls: List of (url, priority, depth) tuples

        Returns:
            Number of URLs successfully added
        """
        added_count = 0

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for url, priority, depth in urls:
            if not is_crawlable_url(url)[0]:
                continue
            domain = self._get_domain(url)

            try:
                cursor.execute('''
                    INSERT INTO url_queue
                    (url, domain, priority, depth, status, added_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (url, domain, priority, depth, self.STATUS_PENDING, time.time()))

                added_count += 1

            except sqlite3.IntegrityError:
                # URL already exists - skip
                continue

        conn.commit()
        conn.close()

        logger.info(f"Batch added {added_count}/{len(urls)} URLs to queue")
        return added_count

    def add_deferred(self, url: str, priority: float = 0, depth: int = 0,
                     source_url: Optional[str] = None,
                     reason: Optional[str] = None, **kwargs) -> bool:
        """
        Store a deferred link — not processed this session but eligible later.

        Deferred links sit with status='deferred' until promote_deferred()
        flips them to 'pending' at the start of a future session.

        Args:
            url: The deferred URL
            priority: Relevance score (0.4-0.7 from link evaluator)
            depth: Link depth from seed
            source_url: Parent URL where link was found
            reason: Why it was deferred (e.g. "moderate_relevance_0.55")

        Returns:
            True if stored, False if URL already exists in queue
        """
        if not is_crawlable_url(url)[0]:
            return False

        domain = self._get_domain(url)
        meta = {}
        if reason:
            meta['defer_reason'] = reason
        if kwargs.get('anchor_text'):
            meta['anchor_text'] = kwargs['anchor_text']
        metadata_json = json.dumps(meta) if meta else None

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO url_queue
                (url, domain, priority, depth, status, added_timestamp,
                 source_url, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (url, domain, int(priority * 100), depth,
                  self.STATUS_DEFERRED, time.time(),
                  source_url, metadata_json))

            conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        finally:
            conn.close()

    def promote_deferred(self) -> int:
        """
        Promote all deferred URLs to pending so they become crawl-eligible.

        Called at session start — deferred links from prior sessions
        become available when the queue needs them.  They retain their
        original (lower) priority so FOLLOW_NOW links still go first.

        Returns:
            Number of URLs promoted
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE url_queue
            SET status = ?
            WHERE status = ?
        ''', (self.STATUS_PENDING, self.STATUS_DEFERRED))

        promoted = cursor.rowcount
        conn.commit()
        conn.close()

        if promoted > 0:
            logger.info(f"Promoted {promoted} deferred URLs to pending")

        return promoted

    def get_next(self, exclude_domains: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Get next URL to crawl (highest priority, oldest first) (SYNC).

        Optionally exclude domains to enable domain-round-robin crawling.

        Args:
            exclude_domains: List of domains to skip (for load distribution)

        Returns:
            Dict with url, id, priority, depth, domain, or None if queue empty
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query with optional domain exclusion
        if exclude_domains:
            placeholders = ','.join('?' * len(exclude_domains))
            query = f'''
                SELECT id, url, priority, depth, domain
                FROM url_queue
                WHERE status = ? AND domain NOT IN ({placeholders})
                ORDER BY priority DESC, added_timestamp ASC
                LIMIT 1
            '''
            params = [self.STATUS_PENDING] + exclude_domains
        else:
            query = '''
                SELECT id, url, priority, depth, domain
                FROM url_queue
                WHERE status = ?
                ORDER BY priority DESC, added_timestamp ASC
                LIMIT 1
            '''
            params = [self.STATUS_PENDING]

        cursor.execute(query, params)
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        url_id, url, priority, depth, domain = row

        # Mark as in_progress
        cursor.execute('''
            UPDATE url_queue
            SET status = ?, started_timestamp = ?
            WHERE id = ?
        ''', (self.STATUS_IN_PROGRESS, time.time(), url_id))

        conn.commit()
        conn.close()

        return {
            'id': url_id,
            'url': url,
            'priority': priority,
            'depth': depth,
            'domain': domain
        }

    def mark_completed(self, url_id: int):
        """Mark URL as successfully crawled (SYNC)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE url_queue
            SET status = ?, completed_timestamp = ?
            WHERE id = ?
        ''', (self.STATUS_COMPLETED, time.time(), url_id))

        conn.commit()
        conn.close()

        logger.debug(f"Marked URL {url_id} as completed")

    def mark_failed(self, url_id: int, error: str):
        """
        Mark URL as failed (SYNC).

        If under retry limit, resets to pending.
        If over limit, marks as permanently failed.

        Args:
            url_id: URL ID
            error: Error message
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current error count
        cursor.execute('SELECT error_count FROM url_queue WHERE id = ?', (url_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return

        error_count = row[0] + 1

        # Permanent errors (404, DNS failure, ...) can never succeed on retry
        if error_count < self.MAX_RETRIES and not is_permanent_error(error):
            # Retry - reset to pending
            cursor.execute('''
                UPDATE url_queue
                SET status = ?, error_count = ?, last_error = ?, started_timestamp = NULL
                WHERE id = ?
            ''', (self.STATUS_PENDING, error_count, error, url_id))

            logger.warning(f"URL {url_id} failed (attempt {error_count}/{self.MAX_RETRIES}), will retry: {error}")
        else:
            # Permanently failed
            cursor.execute('''
                UPDATE url_queue
                SET status = ?, error_count = ?, last_error = ?, completed_timestamp = ?
                WHERE id = ?
            ''', (self.STATUS_FAILED, error_count, error, time.time(), url_id))

            logger.error(f"URL {url_id} permanently failed after {error_count} attempts: {error}")

        conn.commit()
        conn.close()

    def prune_unfetchable(self) -> Dict[str, int]:
        """Apply is_crawlable_url() to pending/deferred URLs, marking filtered
        ones as failed. One-time hygiene after filter changes; safe to re-run."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, url FROM url_queue WHERE status IN (?, ?)',
                       (self.STATUS_PENDING, self.STATUS_DEFERRED))
        rows = cursor.fetchall()

        pruned_by_reason: Dict[str, int] = {}
        pruned_ids = []
        for url_id, url in rows:
            crawlable, reason = is_crawlable_url(url)
            if not crawlable:
                pruned_ids.append((url_id, f'filtered: {reason}'))
                bucket = reason.split('(')[0].strip()
                pruned_by_reason[bucket] = pruned_by_reason.get(bucket, 0) + 1

        cursor.executemany('''
            UPDATE url_queue SET status = ?, last_error = ?, completed_timestamp = ?
            WHERE id = ?
        ''', [(self.STATUS_FAILED, err, time.time(), uid) for uid, err in pruned_ids])
        conn.commit()
        conn.close()

        logger.info(f"Pruned {len(pruned_ids)}/{len(rows)} unfetchable URLs from queue")
        return {'checked': len(rows), 'pruned': len(pruned_ids), 'by_reason': pruned_by_reason}

    def mark_blocked(self, url_id: int, reason: str = 'robots'):
        """
        Mark URL as blocked (robots.txt or immune system) (SYNC).

        Args:
            url_id: URL ID
            reason: 'robots' or 'immune'
        """
        status = self.STATUS_BLOCKED_ROBOTS if reason == 'robots' else self.STATUS_BLOCKED_IMMUNE

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE url_queue
            SET status = ?, completed_timestamp = ?, last_error = ?
            WHERE id = ?
        ''', (status, time.time(), f"Blocked by {reason}", url_id))

        conn.commit()
        conn.close()

        logger.info(f"URL {url_id} blocked by {reason}")

    def get_stats(self) -> Dict:
        """Get queue statistics (SYNC)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total URLs
        cursor.execute('SELECT COUNT(*) FROM url_queue')
        total = cursor.fetchone()[0]

        # Count by status
        cursor.execute('''
            SELECT status, COUNT(*)
            FROM url_queue
            GROUP BY status
        ''')
        status_counts = dict(cursor.fetchall())

        # Average depth
        cursor.execute('SELECT AVG(depth) FROM url_queue WHERE status = ?', (self.STATUS_PENDING,))
        avg_depth_row = cursor.fetchone()
        avg_depth = avg_depth_row[0] if avg_depth_row[0] else 0.0

        # Domain distribution (top 10)
        cursor.execute('''
            SELECT domain, COUNT(*) as count
            FROM url_queue
            WHERE status = ?
            GROUP BY domain
            ORDER BY count DESC
            LIMIT 10
        ''', (self.STATUS_PENDING,))
        domain_dist = cursor.fetchall()

        conn.close()

        return {
            'total_urls': total,
            'pending': status_counts.get(self.STATUS_PENDING, 0),
            'in_progress': status_counts.get(self.STATUS_IN_PROGRESS, 0),
            'completed': status_counts.get(self.STATUS_COMPLETED, 0),
            'failed': status_counts.get(self.STATUS_FAILED, 0),
            'blocked_robots': status_counts.get(self.STATUS_BLOCKED_ROBOTS, 0),
            'blocked_immune': status_counts.get(self.STATUS_BLOCKED_IMMUNE, 0),
            'avg_depth_pending': avg_depth,
            'top_domains': domain_dist,
            'async_available': ASYNC_AVAILABLE
        }

    def get_url_info(self, url: str) -> Optional[Dict]:
        """Get detailed info about a URL (SYNC)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, url, domain, priority, depth, status,
                   added_timestamp, started_timestamp, completed_timestamp,
                   error_count, last_error, source_url, metadata
            FROM url_queue
            WHERE url = ?
        ''', (url,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        metadata = json.loads(row[12]) if row[12] else None

        return {
            'id': row[0],
            'url': row[1],
            'domain': row[2],
            'priority': row[3],
            'depth': row[4],
            'status': row[5],
            'added_timestamp': row[6],
            'started_timestamp': row[7],
            'completed_timestamp': row[8],
            'error_count': row[9],
            'last_error': row[10],
            'source_url': row[11],
            'metadata': metadata
        }

    def clear_completed(self, older_than_hours: Optional[int] = None) -> int:
        """
        Clear completed/failed URLs from queue (SYNC).

        Args:
            older_than_hours: Only clear items older than this (None = all)

        Returns:
            Number of URLs cleared
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if older_than_hours:
            cutoff_time = time.time() - (older_than_hours * 3600)
            cursor.execute('''
                DELETE FROM url_queue
                WHERE status IN (?, ?) AND completed_timestamp < ?
            ''', (self.STATUS_COMPLETED, self.STATUS_FAILED, cutoff_time))
        else:
            cursor.execute('''
                DELETE FROM url_queue
                WHERE status IN (?, ?)
            ''', (self.STATUS_COMPLETED, self.STATUS_FAILED))

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        logger.info(f"Cleared {deleted} completed/failed URLs from queue")
        return deleted

    def clear_all(self):
        """Clear entire queue (use with caution) (SYNC)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM url_queue')
        deleted = cursor.rowcount

        conn.commit()
        conn.close()

        logger.warning(f"Cleared entire queue ({deleted} URLs)")
        return deleted

    def pause_all(self):
        """Reset all in_progress URLs to pending (for graceful shutdown) (SYNC)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE url_queue
            SET status = ?, started_timestamp = NULL
            WHERE status = ?
        ''', (self.STATUS_PENDING, self.STATUS_IN_PROGRESS))

        paused = cursor.rowcount
        conn.commit()
        conn.close()

        logger.info(f"Paused {paused} in-progress URLs")
        return paused

    def reprioritize_by_relevance(self, session_centroid, session_coherence_stats,
                                   batch_size: int = 500,
                                   max_urls: int = 5000) -> Dict:
        """
        Reprioritize pending URLs by cosine similarity to the session centroid.

        Blends the original priority with centroid relevance, weighted by
        density_confidence — when the centroid is well-established it dominates,
        when sparse the original priority is preserved.

        Only processes URLs that have anchor_text in their metadata — URLs
        without it would fall back to URL-path embedding which is low value
        and not worth the compute. Capped at max_urls (top N by original
        priority) to avoid hour-long embedding runs on large queues.

        No URLs are dropped — low-relevance items sink in priority but remain
        reachable. This mirrors bridge-first: triage, never discard.

        Args:
            session_centroid: np.ndarray — current session centroid vector
            session_coherence_stats: ClusterStats — session coherence metrics
            batch_size: Process this many pending URLs per DB transaction
            max_urls: Maximum number of URLs to reprioritize (top N by priority)

        Returns:
            Dict with reprioritization stats
        """
        import numpy as np
        try:
            from vector_engine import fuse_vectors
            from adaptive_bridge_migration import cosine_sim
        except ImportError:
            return {'reprioritized': 0, 'error': 'missing_imports'}

        if session_centroid is None or session_coherence_stats is None:
            return {'reprioritized': 0, 'skipped': 'no_centroid'}

        dc = session_coherence_stats.density_confidence
        if dc <= 0:
            return {'reprioritized': 0, 'skipped': 'zero_confidence'}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Count total pending for stats
        cursor.execute(
            'SELECT COUNT(*) FROM url_queue WHERE status = ?',
            (self.STATUS_PENDING,))
        total_pending = cursor.fetchone()[0]

        # Only fetch URLs that have anchor_text in metadata, capped at max_urls,
        # ordered by priority so the most promising URLs get reprioritized first.
        cursor.execute('''
            SELECT id, url, priority, metadata FROM url_queue
            WHERE status = ?
              AND metadata IS NOT NULL
              AND metadata LIKE '%"anchor_text"%'
            ORDER BY priority DESC
            LIMIT ?
        ''', (self.STATUS_PENDING, max_urls))

        rows = cursor.fetchall()
        reprioritized = 0
        failed_embed = 0
        skipped_no_anchor = 0

        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            updates = []

            for url_id, url, original_priority, metadata_json in batch:
                # Extract anchor text from metadata
                anchor_text = None
                if metadata_json:
                    try:
                        meta = json.loads(metadata_json)
                        anchor_text = meta.get('anchor_text')
                    except (json.JSONDecodeError, TypeError):
                        pass

                if not anchor_text:
                    skipped_no_anchor += 1
                    continue

                try:
                    vec, _ = fuse_vectors(anchor_text[:200])
                except Exception:
                    vec = None

                if vec is None:
                    failed_embed += 1
                    continue

                relevance = cosine_sim(np.array(vec), session_centroid)

                # Blend: relevance * dc + original * (1 - dc)
                # Normalize original_priority to 0-1 range (stored as int, typically 0-100)
                orig_normalized = min(1.0, max(0.0, original_priority / 100.0))
                blended = relevance * dc + orig_normalized * (1 - dc)
                new_priority = int(blended * 100)

                updates.append((new_priority, url_id))

            if updates:
                cursor.executemany('''
                    UPDATE url_queue SET priority = ? WHERE id = ?
                ''', updates)
                reprioritized += len(updates)

            conn.commit()

        conn.close()
        logger.info(f"Reprioritized {reprioritized}/{total_pending} pending URLs "
                    f"(failed embed: {failed_embed}, skipped no anchor: {skipped_no_anchor})")
        return {
            'reprioritized': reprioritized,
            'total_pending': total_pending,
            'candidates_fetched': len(rows),
            'failed_embed': failed_embed,
            'skipped_no_anchor': skipped_no_anchor,
            'density_confidence': dc
        }

    # ========================================================================
    # ASYNC METHODS (New - For Non-Blocking Event Loop Operation)
    # ========================================================================

    async def add_url_async(self, url: str, priority: int = 0, depth: int = 0,
                           source_url: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """
        Add URL to queue (ASYNC).

        Args:
            url: URL to add
            priority: Priority (higher = crawled sooner)
            depth: Link depth from seed
            source_url: URL where this was discovered
            metadata: Optional metadata dict

        Returns:
            True if added, False if already exists
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        if not is_crawlable_url(url)[0]:
            return False

        domain = self._get_domain(url)
        metadata_json = json.dumps(metadata) if metadata else None

        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO url_queue
                    (url, domain, priority, depth, status, added_timestamp, source_url, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (url, domain, priority, depth, self.STATUS_PENDING,
                      time.time(), source_url, metadata_json))

                await db.commit()
                logger.debug(f"Added to queue (async): {url} (priority: {priority}, depth: {depth})")
                return True

            except aiosqlite.IntegrityError:
                # URL already exists
                logger.debug(f"URL already in queue (async): {url}")
                return False

    async def get_next_async(self, exclude_domains: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Get next URL to crawl (highest priority, oldest first) (ASYNC).

        Optionally exclude domains to enable domain-round-robin crawling.

        Args:
            exclude_domains: List of domains to skip (for load distribution)

        Returns:
            Dict with url, id, priority, depth, domain, or None if queue empty
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as db:
            # Build query with optional domain exclusion
            if exclude_domains:
                placeholders = ','.join('?' * len(exclude_domains))
                query = f'''
                    SELECT id, url, priority, depth, domain
                    FROM url_queue
                    WHERE status = ? AND domain NOT IN ({placeholders})
                    ORDER BY priority DESC, added_timestamp ASC
                    LIMIT 1
                '''
                params = [self.STATUS_PENDING] + exclude_domains
            else:
                query = '''
                    SELECT id, url, priority, depth, domain
                    FROM url_queue
                    WHERE status = ?
                    ORDER BY priority DESC, added_timestamp ASC
                    LIMIT 1
                '''
                params = [self.STATUS_PENDING]

            async with db.execute(query, params) as cursor:
                row = await cursor.fetchone()

            if not row:
                return None

            url_id, url, priority, depth, domain = row

            # Mark as in_progress
            await db.execute('''
                UPDATE url_queue
                SET status = ?, started_timestamp = ?
                WHERE id = ?
            ''', (self.STATUS_IN_PROGRESS, time.time(), url_id))

            await db.commit()

            return {
                'id': url_id,
                'url': url,
                'priority': priority,
                'depth': depth,
                'domain': domain
            }

    async def update_status_async(self, url_id: int, status: str):
        """
        Update URL status (ASYNC).

        Args:
            url_id: URL ID
            status: New status value
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE url_queue
                SET status = ?, completed_timestamp = ?
                WHERE id = ?
            ''', (status, time.time(), url_id))

            await db.commit()

        logger.debug(f"Updated URL {url_id} status to {status} (async)")

    async def mark_completed_async(self, url_id: int):
        """Mark URL as successfully crawled (ASYNC)."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE url_queue
                SET status = ?, completed_timestamp = ?
                WHERE id = ?
            ''', (self.STATUS_COMPLETED, time.time(), url_id))

            await db.commit()

        logger.debug(f"Marked URL {url_id} as completed (async)")

    async def mark_failed_async(self, url_id: int, error: str):
        """
        Mark URL as failed (ASYNC).

        If under retry limit, resets to pending.
        If over limit, marks as permanently failed.

        Args:
            url_id: URL ID
            error: Error message
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as db:
            # Get current error count
            async with db.execute('SELECT error_count FROM url_queue WHERE id = ?', (url_id,)) as cursor:
                row = await cursor.fetchone()

            if not row:
                return

            error_count = row[0] + 1

            if error_count < self.MAX_RETRIES and not is_permanent_error(error):
                # Retry - reset to pending
                await db.execute('''
                    UPDATE url_queue
                    SET status = ?, error_count = ?, last_error = ?, started_timestamp = NULL
                    WHERE id = ?
                ''', (self.STATUS_PENDING, error_count, error, url_id))

                logger.warning(f"URL {url_id} failed (attempt {error_count}/{self.MAX_RETRIES}), will retry (async): {error}")
            else:
                # Permanently failed
                await db.execute('''
                    UPDATE url_queue
                    SET status = ?, error_count = ?, last_error = ?, completed_timestamp = ?
                    WHERE id = ?
                ''', (self.STATUS_FAILED, error_count, error, time.time(), url_id))

                logger.error(f"URL {url_id} permanently failed after {error_count} attempts (async): {error}")

            await db.commit()

    async def mark_blocked_async(self, url_id: int, reason: str = 'robots'):
        """
        Mark URL as blocked (robots.txt or immune system) (ASYNC).

        Args:
            url_id: URL ID
            reason: 'robots' or 'immune'
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        status = self.STATUS_BLOCKED_ROBOTS if reason == 'robots' else self.STATUS_BLOCKED_IMMUNE

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE url_queue
                SET status = ?, completed_timestamp = ?, last_error = ?
                WHERE id = ?
            ''', (status, time.time(), f"Blocked by {reason}", url_id))

            await db.commit()

        logger.info(f"URL {url_id} blocked by {reason} (async)")

    async def get_pending_count_async(self) -> int:
        """Get count of pending URLs (ASYNC)."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT COUNT(*) FROM url_queue WHERE status = ?',
                (self.STATUS_PENDING,)
            ) as cursor:
                row = await cursor.fetchone()

        return row[0] if row else 0

    async def get_stats_async(self) -> Dict:
        """Get queue statistics (ASYNC)."""
        if not ASYNC_AVAILABLE:
            raise RuntimeError("aiosqlite not available. Install with: pip install aiosqlite")

        async with aiosqlite.connect(self.db_path) as db:
            # Total URLs
            async with db.execute('SELECT COUNT(*) FROM url_queue') as cursor:
                total = (await cursor.fetchone())[0]

            # Count by status
            async with db.execute('''
                SELECT status, COUNT(*)
                FROM url_queue
                GROUP BY status
            ''') as cursor:
                status_counts = dict(await cursor.fetchall())

            # Average depth
            async with db.execute(
                'SELECT AVG(depth) FROM url_queue WHERE status = ?',
                (self.STATUS_PENDING,)
            ) as cursor:
                avg_depth_row = await cursor.fetchone()
                avg_depth = avg_depth_row[0] if avg_depth_row[0] else 0.0

            # Domain distribution (top 10)
            async with db.execute('''
                SELECT domain, COUNT(*) as count
                FROM url_queue
                WHERE status = ?
                GROUP BY domain
                ORDER BY count DESC
                LIMIT 10
            ''', (self.STATUS_PENDING,)) as cursor:
                domain_dist = await cursor.fetchall()

        return {
            'total_urls': total,
            'pending': status_counts.get(self.STATUS_PENDING, 0),
            'in_progress': status_counts.get(self.STATUS_IN_PROGRESS, 0),
            'completed': status_counts.get(self.STATUS_COMPLETED, 0),
            'failed': status_counts.get(self.STATUS_FAILED, 0),
            'blocked_robots': status_counts.get(self.STATUS_BLOCKED_ROBOTS, 0),
            'blocked_immune': status_counts.get(self.STATUS_BLOCKED_IMMUNE, 0),
            'avg_depth_pending': avg_depth,
            'top_domains': domain_dist,
            'async_available': ASYNC_AVAILABLE
        }


if __name__ == "__main__":
    # Demo usage (sync and async)
    import asyncio
    logging.basicConfig(level=logging.INFO)

    queue = PersistentURLQueue()

    print("Testing URL queue (SYNC)...\n")

    # Add some test URLs (sync)
    test_urls = [
        ("https://en.wikipedia.org/wiki/Python", 10, 0),
        ("https://en.wikipedia.org/wiki/Machine_learning", 5, 1),
        ("https://www.python.org/", 8, 0),
    ]

    for url, priority, depth in test_urls:
        queue.add(url, priority, depth)

    # Get stats (sync)
    stats = queue.get_stats()
    print("Queue stats (sync):")
    for key, value in stats.items():
        if key != 'top_domains':
            print(f"  {key}: {value}")

    # Get next URL (sync)
    next_item = queue.get_next()
    if next_item:
        print(f"\nNext URL to crawl: {next_item['url']} (priority: {next_item['priority']})")
        queue.mark_completed(next_item['id'])
        print(f"Marked as completed")

    # Test async methods
    async def test_async():
        print("\n\nTesting URL queue (ASYNC)...\n")

        if not ASYNC_AVAILABLE:
            print("⚠️  aiosqlite not available - skipping async tests")
            print("   Install with: pip install aiosqlite")
            return

        # Add URLs concurrently (async)
        async_urls = [
            ("https://en.wikipedia.org/wiki/Asyncio", 10, 0),
            ("https://docs.python.org/3/library/asyncio.html", 9, 0),
        ]

        tasks = [
            queue.add_url_async(url, priority, depth)
            for url, priority, depth in async_urls
        ]
        results = await asyncio.gather(*tasks)
        print(f"Added {sum(results)} URLs concurrently")

        # Get stats (async)
        stats = await queue.get_stats_async()
        print(f"\nQueue stats (async):")
        print(f"  Pending: {stats['pending']}")
        print(f"  Total: {stats['total_urls']}")

        # Get next URL (async)
        next_item = await queue.get_next_async()
        if next_item:
            print(f"\nNext URL: {next_item['url']}")
            await queue.mark_completed_async(next_item['id'])
            print("Marked as completed (async)")

    asyncio.run(test_async())

    # Final stats
    final_stats = queue.get_stats()
    print(f"\nFinal stats:")
    print(f"  Pending: {final_stats['pending']}")
    print(f"  Completed: {final_stats['completed']}")
