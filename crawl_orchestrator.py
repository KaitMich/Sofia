#!/usr/bin/env python3
"""
Crawl Orchestrator - Ethical Crawling Integration Layer

Coordinates robots.txt compliance, rate limiting, and URL queue management.

Key Responsibilities:
- Pre-flight checks (robots.txt + rate limits)
- URL queue management with priority
- Post-crawl recording (success/failure/blocked)
- Domain-aware load distribution
- Complete audit trail integration
- **ASYNC SUPPORT** - Concurrent crawling with semaphore + per-domain locking

Usage (Sync):
    orchestrator = CrawlOrchestrator()
    can_crawl, reason = orchestrator.can_crawl(url)
    if can_crawl:
        url_id = orchestrator.prepare_crawl(url)
        # ... do actual HTTP request ...
        orchestrator.record_success(url_id)

Usage (Async - 10-50x faster):
    orchestrator = CrawlOrchestrator()
    urls = ["https://example.com/1", "https://example.com/2", ...]
    results = await orchestrator.crawl_batch_async(urls, max_concurrent=5)
"""

from pathlib import Path
from typing import Optional, Dict, List, Tuple
import logging
from urllib.parse import urlparse
from dataclasses import dataclass

# Async support
try:
    import asyncio
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    asyncio = None

from robots_txt_manager import RobotsTxtManager
from domain_rate_limiter import DomainRateLimiter
from persistent_url_queue import PersistentURLQueue

logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    """Result of a single crawl attempt."""
    url: str
    url_id: Optional[int]
    success: bool
    error: Optional[str] = None
    blocked_reason: Optional[str] = None  # 'robots' or 'immune'
    wait_time: float = 0.0  # Time waited for rate limiting


class CrawlOrchestrator:
    """
    Coordinates all crawling infrastructure for ethical, reliable crawling.

    Supports both sync and async operations.
    Sync methods: can_crawl(), prepare_crawl(), record_success(), etc.
    Async methods: crawl_batch_async(), process_queue_async(), etc.
    """

    def __init__(self, data_dir: str = "data", min_delay: float = 3.0):
        """
        Initialize crawl orchestrator.

        Args:
            data_dir: Base directory for data storage
            min_delay: Minimum delay between requests to same domain (seconds)
        """
        self.data_dir = Path(data_dir)

        # Initialize components
        self.robots_manager = RobotsTxtManager(data_dir=str(self.data_dir))
        self.rate_limiter = DomainRateLimiter(data_dir=str(self.data_dir), min_delay=min_delay)
        self.url_queue = PersistentURLQueue(data_dir=str(self.data_dir))

        # Track recently crawled domains for round-robin distribution
        self._recent_domains: List[str] = []
        self._recent_domains_limit = 10

        # Per-domain locks for async crawling (prevents hitting same domain simultaneously)
        self._domain_locks: Dict[str, asyncio.Lock] = {} if ASYNC_AVAILABLE else {}

        logger.info(f"Crawl orchestrator initialized (min_delay: {min_delay}s, async_available: {ASYNC_AVAILABLE})")

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    # ========================================================================
    # SYNC METHODS (Original - Preserved for Backwards Compatibility)
    # ========================================================================

    def can_crawl(self, url: str, check_robots: bool = True,
                  check_rate_limit: bool = True) -> Tuple[bool, str]:
        """
        Pre-flight check: Can we crawl this URL right now? (SYNC)

        Args:
            url: URL to check
            check_robots: Whether to check robots.txt (default: True)
            check_rate_limit: Whether to check rate limits (default: True)

        Returns:
            (can_crawl, reason)
            - (True, "OK") if allowed
            - (False, reason) if blocked
        """
        # Check robots.txt
        if check_robots:
            if not self.robots_manager.is_allowed(url):
                return False, "Blocked by robots.txt"

        # Check rate limit
        if check_rate_limit:
            wait_time = self.rate_limiter.get_wait_time(url, include_jitter=False)
            if wait_time > 0:
                return False, f"Rate limited (wait {wait_time:.1f}s)"

        return True, "OK"

    def prepare_crawl(self, url: str, wait_if_needed: bool = True) -> Optional[int]:
        """
        Prepare to crawl a URL (SYNC).

        1. Checks robots.txt
        2. Waits for rate limit if needed
        3. Syncs crawl delay from robots.txt to rate limiter
        4. Marks URL as in_progress in queue (if queued)

        Args:
            url: URL to prepare
            wait_if_needed: Whether to wait for rate limits (default: True)

        Returns:
            URL queue ID if successful, None if blocked
        """
        # Check robots.txt
        if not self.robots_manager.is_allowed(url):
            logger.info(f"Blocked by robots.txt: {url}")
            return None

        # Get robots.txt crawl delay and sync with rate limiter
        robots_delay = self.robots_manager.get_crawl_delay(url)
        if robots_delay:
            domain = self._get_domain(url)
            self.rate_limiter.set_crawl_delay(domain, robots_delay)
            logger.debug(f"Synced robots.txt crawl delay for {domain}: {robots_delay}s")

        # Wait for rate limit if needed
        if wait_if_needed:
            wait_time = self.rate_limiter.wait_if_needed(url)
            if wait_time > 0:
                logger.debug(f"Waited {wait_time:.2f}s for rate limit: {url}")

        # Check if URL is in queue, get its ID
        url_info = self.url_queue.get_url_info(url)
        if url_info:
            return url_info['id']

        # Not in queue - add it now
        self.url_queue.add(url, priority=0, depth=0)
        url_info = self.url_queue.get_url_info(url)
        return url_info['id'] if url_info else None

    def record_success(self, url_id: int, url: str):
        """
        Record successful crawl (SYNC).

        Args:
            url_id: URL queue ID
            url: URL that was crawled
        """
        # Mark in queue
        self.url_queue.mark_completed(url_id)

        # Record in rate limiter
        robots_delay = self.robots_manager.get_crawl_delay(url)
        self.rate_limiter.record_request(url, robots_crawl_delay=robots_delay)

        # Track domain for round-robin
        domain = self._get_domain(url)
        if domain in self._recent_domains:
            self._recent_domains.remove(domain)
        self._recent_domains.insert(0, domain)
        if len(self._recent_domains) > self._recent_domains_limit:
            self._recent_domains.pop()

        logger.debug(f"Recorded success: {url}")

    def record_failure(self, url_id: int, url: str, error: str):
        """
        Record failed crawl (SYNC).

        Args:
            url_id: URL queue ID
            url: URL that failed
            error: Error message
        """
        # Mark in queue (will retry if under limit)
        self.url_queue.mark_failed(url_id, error)

        # Still record in rate limiter to avoid hammering failed URLs
        robots_delay = self.robots_manager.get_crawl_delay(url)
        self.rate_limiter.record_request(url, robots_crawl_delay=robots_delay)

        logger.warning(f"Recorded failure: {url} - {error}")

    def record_blocked(self, url_id: int, url: str, reason: str = 'robots'):
        """
        Record blocked crawl (robots.txt or immune system) (SYNC).

        Args:
            url_id: URL queue ID
            url: URL that was blocked
            reason: 'robots' or 'immune'
        """
        self.url_queue.mark_blocked(url_id, reason)

        logger.info(f"Recorded blocked ({reason}): {url}")

    def get_next_url(self, domain_round_robin: bool = True) -> Optional[Dict]:
        """
        Get next URL to crawl from queue (SYNC).

        Optionally distributes load across domains using round-robin.

        Args:
            domain_round_robin: Use domain round-robin (default: True)

        Returns:
            Dict with id, url, priority, depth, domain or None if queue empty
        """
        if domain_round_robin and self._recent_domains:
            # Try to get URL from domain NOT recently crawled
            next_item = self.url_queue.get_next(exclude_domains=self._recent_domains)
            if next_item:
                return next_item

        # Fallback: get any next URL
        return self.url_queue.get_next()

    def add_url(self, url: str, priority: int = 0, depth: int = 0,
                source_url: Optional[str] = None) -> bool:
        """
        Add URL to crawl queue (SYNC).

        Args:
            url: URL to add
            priority: Priority (higher = crawled sooner)
            depth: Link depth from seed
            source_url: URL where this was discovered

        Returns:
            True if added, False if already exists
        """
        return self.url_queue.add(url, priority, depth, source_url)

    def add_batch(self, urls: List[Tuple[str, int, int]]) -> int:
        """
        Add multiple URLs to queue in batch (SYNC).

        Args:
            urls: List of (url, priority, depth) tuples

        Returns:
            Number of URLs successfully added
        """
        return self.url_queue.add_batch(urls)

    def get_stats(self) -> Dict:
        """
        Get comprehensive crawling statistics (SYNC).

        Returns:
            Dict with stats from all components
        """
        queue_stats = self.url_queue.get_stats()
        rate_stats = self.rate_limiter.get_stats()
        robots_stats = self.robots_manager.get_cache_stats()

        return {
            'queue': queue_stats,
            'rate_limiter': rate_stats,
            'robots_cache': robots_stats,
            'recent_domains': self._recent_domains[:5]  # Top 5 most recent
        }

    def get_url_info(self, url: str) -> Dict:
        """
        Get comprehensive info about a URL (SYNC).

        Returns:
            Dict with queue info, robots.txt status, rate limit status
        """
        queue_info = self.url_queue.get_url_info(url)
        robots_allowed = self.robots_manager.is_allowed(url)
        crawl_delay = self.robots_manager.get_crawl_delay(url)
        rate_limit_info = self.rate_limiter.get_domain_stats(url)

        return {
            'url': url,
            'in_queue': queue_info is not None,
            'queue_info': queue_info,
            'robots_allowed': robots_allowed,
            'robots_crawl_delay': crawl_delay,
            'rate_limit_info': rate_limit_info
        }

    def pause_crawling(self):
        """
        Pause crawling (resets all in_progress URLs to pending) (SYNC).

        Use for graceful shutdown.
        """
        paused = self.url_queue.pause_all()
        logger.info(f"Paused crawling ({paused} URLs reset to pending)")
        return paused

    def clear_completed(self, older_than_hours: Optional[int] = 24) -> int:
        """
        Clear completed URLs from queue (SYNC).

        Args:
            older_than_hours: Only clear items older than this (default: 24)

        Returns:
            Number of URLs cleared
        """
        return self.url_queue.clear_completed(older_than_hours)

    def health_check(self) -> Dict:
        """
        Comprehensive health check (SYNC).

        Returns:
            Dict with health status and any issues
        """
        issues = []
        stats = self.get_stats()

        # Check for stuck in_progress URLs
        if stats['queue']['in_progress'] > 0:
            issues.append(f"{stats['queue']['in_progress']} URLs stuck in_progress (may indicate crash)")

        # Check for high failure rate
        total_completed = stats['queue']['completed'] + stats['queue']['failed']
        if total_completed > 0:
            failure_rate = stats['queue']['failed'] / total_completed
            if failure_rate > 0.3:
                issues.append(f"High failure rate: {failure_rate*100:.1f}%")

        # Check for robots.txt blocks
        if stats['queue']['blocked_robots'] > 10:
            issues.append(f"{stats['queue']['blocked_robots']} URLs blocked by robots.txt")

        # Check robots cache health
        if stats['robots_cache']['cache_hit_rate'] < 50:
            issues.append(f"Low robots.txt cache hit rate: {stats['robots_cache']['cache_hit_rate']:.1f}%")

        return {
            'status': 'healthy' if not issues else 'issues_detected',
            'issues': issues,
            'stats': stats
        }

    # ========================================================================
    # ASYNC METHODS (New - For Concurrent Crawling)
    # ========================================================================

    async def _get_domain_lock(self, domain: str) -> asyncio.Lock:
        """
        Get or create async lock for a domain.

        Prevents hitting same domain simultaneously from multiple coroutines.

        Args:
            domain: Domain URL

        Returns:
            asyncio.Lock for this domain
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        if domain not in self._domain_locks:
            self._domain_locks[domain] = asyncio.Lock()
        return self._domain_locks[domain]

    async def can_crawl_async(self, url: str, check_robots: bool = True,
                             check_rate_limit: bool = True) -> Tuple[bool, str]:
        """
        Pre-flight check: Can we crawl this URL right now? (ASYNC)

        Args:
            url: URL to check
            check_robots: Whether to check robots.txt (default: True)
            check_rate_limit: Whether to check rate limits (default: True)

        Returns:
            (can_crawl, reason)
            - (True, "OK") if allowed
            - (False, reason) if blocked
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        # Check robots.txt
        if check_robots:
            if not await self.robots_manager.is_allowed_async(url):
                return False, "Blocked by robots.txt"

        # Check rate limit
        if check_rate_limit:
            wait_time = await self.rate_limiter.get_wait_time_async(url, include_jitter=False)
            if wait_time > 0:
                return False, f"Rate limited (wait {wait_time:.1f}s)"

        return True, "OK"

    async def prepare_crawl_async(self, url: str, wait_if_needed: bool = True) -> Optional[int]:
        """
        Prepare to crawl a URL (ASYNC).

        1. Checks robots.txt
        2. Waits for rate limit if needed (non-blocking)
        3. Syncs crawl delay from robots.txt to rate limiter
        4. Marks URL as in_progress in queue (if queued)

        Args:
            url: URL to prepare
            wait_if_needed: Whether to wait for rate limits (default: True)

        Returns:
            URL queue ID if successful, None if blocked
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        # Check robots.txt
        if not await self.robots_manager.is_allowed_async(url):
            logger.info(f"Blocked by robots.txt (async): {url}")
            return None

        # Get robots.txt crawl delay and sync with rate limiter
        robots_delay = await self.robots_manager.get_crawl_delay_async(url)
        if robots_delay:
            domain = self._get_domain(url)
            await self.rate_limiter.set_crawl_delay_async(domain, robots_delay)
            logger.debug(f"Synced robots.txt crawl delay for {domain}: {robots_delay}s (async)")

        # Wait for rate limit if needed
        if wait_if_needed:
            wait_time = await self.rate_limiter.wait_if_needed_async(url)
            if wait_time > 0:
                logger.debug(f"Waited {wait_time:.2f}s for rate limit (async): {url}")

        # Check if URL is in queue, get its ID
        url_info = self.url_queue.get_url_info(url)
        if url_info:
            return url_info['id']

        # Not in queue - add it now
        await self.url_queue.add_url_async(url, priority=0, depth=0)
        url_info = self.url_queue.get_url_info(url)
        return url_info['id'] if url_info else None

    async def record_success_async(self, url_id: int, url: str):
        """
        Record successful crawl (ASYNC).

        Args:
            url_id: URL queue ID
            url: URL that was crawled
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        # Mark in queue
        await self.url_queue.mark_completed_async(url_id)

        # Record in rate limiter
        robots_delay = await self.robots_manager.get_crawl_delay_async(url)
        await self.rate_limiter.record_request_async(url, robots_crawl_delay=robots_delay)

        # Track domain for round-robin
        domain = self._get_domain(url)
        if domain in self._recent_domains:
            self._recent_domains.remove(domain)
        self._recent_domains.insert(0, domain)
        if len(self._recent_domains) > self._recent_domains_limit:
            self._recent_domains.pop()

        logger.debug(f"Recorded success (async): {url}")

    async def record_failure_async(self, url_id: int, url: str, error: str):
        """
        Record failed crawl (ASYNC).

        Args:
            url_id: URL queue ID
            url: URL that failed
            error: Error message
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        # Mark in queue (will retry if under limit)
        await self.url_queue.mark_failed_async(url_id, error)

        # Still record in rate limiter to avoid hammering failed URLs
        robots_delay = await self.robots_manager.get_crawl_delay_async(url)
        await self.rate_limiter.record_request_async(url, robots_crawl_delay=robots_delay)

        logger.warning(f"Recorded failure (async): {url} - {error}")

    async def record_blocked_async(self, url_id: int, url: str, reason: str = 'robots'):
        """
        Record blocked crawl (robots.txt or immune system) (ASYNC).

        Args:
            url_id: URL queue ID
            url: URL that was blocked
            reason: 'robots' or 'immune'
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        await self.url_queue.mark_blocked_async(url_id, reason)

        logger.info(f"Recorded blocked ({reason}) (async): {url}")

    async def crawl_batch_async(self, urls: List[str], max_concurrent: int = 5,
                                fetch_callback=None) -> List[CrawlResult]:
        """
        Crawl multiple URLs concurrently with rate limiting and robots.txt compliance.

        **THIS IS THE 10-50X MULTIPLIER METHOD.**

        Key features:
        - Global concurrency limit via asyncio.Semaphore
        - Per-domain locking to prevent hitting same domain twice simultaneously
        - Automatic robots.txt checking and rate limiting
        - Returns results as they complete

        Args:
            urls: List of URLs to crawl
            max_concurrent: Maximum concurrent requests (default: 5)
            fetch_callback: Optional async function(url) -> (success, content_or_error)
                           If None, only performs pre-flight checks (no actual fetch)

        Returns:
            List of CrawlResult objects
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available. Install with: pip install asyncio")

        logger.info(f"Starting batch crawl: {len(urls)} URLs, max_concurrent={max_concurrent}")

        # Global concurrency limiter
        semaphore = asyncio.Semaphore(max_concurrent)

        async def crawl_one(url: str) -> CrawlResult:
            """Crawl a single URL with all safety checks."""
            async with semaphore:  # Global concurrency limit
                domain = self._get_domain(url)

                # Per-domain lock (never hit same domain simultaneously)
                async with await self._get_domain_lock(domain):
                    # Pre-flight check
                    can_crawl, reason = await self.can_crawl_async(url)

                    if not can_crawl:
                        # Blocked by robots.txt or rate limit
                        if "robots" in reason.lower():
                            # Add to queue and mark blocked
                            await self.url_queue.add_url_async(url, priority=0, depth=0)
                            url_info = self.url_queue.get_url_info(url)
                            url_id = url_info['id'] if url_info else None
                            if url_id:
                                await self.record_blocked_async(url_id, url, reason='robots')

                            return CrawlResult(
                                url=url,
                                url_id=url_id,
                                success=False,
                                blocked_reason='robots'
                            )
                        else:
                            # Rate limited - wait and retry
                            logger.debug(f"Rate limited, waiting: {url}")

                    # Prepare crawl (handles rate limiting + robots.txt sync)
                    url_id = await self.prepare_crawl_async(url, wait_if_needed=True)

                    if url_id is None:
                        # Blocked by robots.txt
                        return CrawlResult(
                            url=url,
                            url_id=None,
                            success=False,
                            blocked_reason='robots'
                        )

                    # Actual fetch (if callback provided)
                    if fetch_callback:
                        try:
                            success, result = await fetch_callback(url)

                            if success:
                                await self.record_success_async(url_id, url)
                                return CrawlResult(
                                    url=url,
                                    url_id=url_id,
                                    success=True
                                )
                            else:
                                # Fetch failed
                                error = str(result) if result else "Unknown error"
                                await self.record_failure_async(url_id, url, error)
                                return CrawlResult(
                                    url=url,
                                    url_id=url_id,
                                    success=False,
                                    error=error
                                )

                        except Exception as e:
                            # Exception during fetch
                            error = str(e)
                            await self.record_failure_async(url_id, url, error)
                            return CrawlResult(
                                url=url,
                                url_id=url_id,
                                success=False,
                                error=error
                            )
                    else:
                        # No callback - just mark as prepared
                        await self.record_success_async(url_id, url)
                        return CrawlResult(
                            url=url,
                            url_id=url_id,
                            success=True
                        )

        # Launch all crawls concurrently
        tasks = [crawl_one(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to failed CrawlResults
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append(CrawlResult(
                    url=urls[i],
                    url_id=None,
                    success=False,
                    error=str(result)
                ))
            else:
                final_results.append(result)

        # Summary
        success_count = sum(1 for r in final_results if r.success)
        blocked_count = sum(1 for r in final_results if r.blocked_reason)
        failed_count = sum(1 for r in final_results if not r.success and not r.blocked_reason)

        logger.info(f"Batch crawl complete: {success_count} success, {blocked_count} blocked, {failed_count} failed")

        return final_results

    async def process_queue_async(self, max_concurrent: int = 5, max_urls: int = 100,
                                  fetch_callback=None) -> Dict:
        """
        Process URLs from queue concurrently.

        Args:
            max_concurrent: Maximum concurrent requests (default: 5)
            max_urls: Maximum URLs to process (default: 100)
            fetch_callback: Optional async function(url) -> (success, content_or_error)

        Returns:
            Dict with processing stats
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("asyncio not available")

        logger.info(f"Processing queue: max_concurrent={max_concurrent}, max_urls={max_urls}")

        # Get pending count
        pending_count = await self.url_queue.get_pending_count_async()
        logger.info(f"Pending URLs: {pending_count}")

        # Determine how many to process
        to_process = min(pending_count, max_urls)

        if to_process == 0:
            logger.info("No URLs to process")
            return {
                'processed': 0,
                'successful': 0,
                'failed': 0,
                'blocked': 0
            }

        # Pull URLs from queue (sync method is fine here - not the bottleneck)
        urls_to_crawl = []
        for _ in range(to_process):
            next_item = await self.url_queue.get_next_async()
            if next_item:
                urls_to_crawl.append(next_item['url'])
            else:
                break

        # Crawl them concurrently
        results = await self.crawl_batch_async(urls_to_crawl, max_concurrent, fetch_callback)

        # Stats
        stats = {
            'processed': len(results),
            'successful': sum(1 for r in results if r.success),
            'failed': sum(1 for r in results if not r.success and not r.blocked_reason),
            'blocked': sum(1 for r in results if r.blocked_reason)
        }

        logger.info(f"Queue processing complete: {stats}")
        return stats


if __name__ == "__main__":
    # Demo usage (sync and async)
    import asyncio
    logging.basicConfig(level=logging.INFO)

    orchestrator = CrawlOrchestrator()

    print("=" * 60)
    print("Testing Crawl Orchestrator (SYNC)\n")
    print("=" * 60)

    # Add some URLs to queue
    test_urls = [
        ("https://en.wikipedia.org/wiki/Python", 10, 0),
        ("https://en.wikipedia.org/wiki/Machine_learning", 8, 1),
        ("https://www.python.org/", 5, 0),
    ]

    print("\nAdding URLs to queue...")
    for url, priority, depth in test_urls:
        orchestrator.add_url(url, priority, depth)

    # Get next URL
    print("\nGetting next URL to crawl...")
    next_item = orchestrator.get_next_url()

    if next_item:
        url = next_item['url']
        url_id = next_item['id']

        print(f"Next URL: {url}")

        # Pre-flight check
        can_crawl, reason = orchestrator.can_crawl(url)
        print(f"Can crawl: {can_crawl} ({reason})")

        if can_crawl:
            # Prepare crawl
            print("Preparing crawl...")
            prepared_id = orchestrator.prepare_crawl(url)

            if prepared_id:
                print(f"Ready to crawl (ID: {prepared_id})")

                # Simulate successful crawl
                orchestrator.record_success(prepared_id, url)
                print("Recorded success")

    # Get stats
    print("\nCrawl Statistics:")
    stats = orchestrator.get_stats()
    print(f"  Queue - Pending: {stats['queue']['pending']}, Completed: {stats['queue']['completed']}")
    print(f"  Rate Limiter - Domains: {stats['rate_limiter']['total_domains']}")
    print(f"  Robots Cache - Cached: {stats['robots_cache']['total_cached_domains']}")

    # Health check
    print("\nHealth Check:")
    health = orchestrator.health_check()
    print(f"  Status: {health['status']}")
    if health['issues']:
        for issue in health['issues']:
            print(f"  - {issue}")

    # Test async batch crawling
    async def test_async():
        print("\n" + "=" * 60)
        print("Testing Crawl Orchestrator (ASYNC - 10-50x FASTER)\n")
        print("=" * 60)

        if not ASYNC_AVAILABLE:
            print("⚠️  asyncio not available - skipping async tests")
            return

        # Test URLs
        async_urls = [
            "https://en.wikipedia.org/wiki/Asyncio",
            "https://en.wikipedia.org/wiki/Concurrent_computing",
            "https://docs.python.org/3/library/asyncio.html",
        ]

        print(f"\nCrawling {len(async_urls)} URLs concurrently (max_concurrent=2)...")

        # Mock fetch callback (for demo - no actual HTTP request)
        async def mock_fetch(url):
            await asyncio.sleep(0.1)  # Simulate network delay
            return True, None  # Success

        results = await orchestrator.crawl_batch_async(
            async_urls,
            max_concurrent=2,
            fetch_callback=mock_fetch
        )

        print(f"\nResults:")
        for result in results:
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            if result.blocked_reason:
                status = f"🚫 BLOCKED ({result.blocked_reason})"
            print(f"  {status}: {result.url}")

        # Final stats
        stats = await orchestrator.url_queue.get_stats_async()
        print(f"\nFinal queue stats:")
        print(f"  Pending: {stats['pending']}")
        print(f"  Completed: {stats['completed']}")

    asyncio.run(test_async())

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
