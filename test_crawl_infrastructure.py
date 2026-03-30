#!/usr/bin/env python3
"""
Test Suite: Crawl Infrastructure - Ethical Crawling Components

Tests for:
- robots_txt_manager.py - Robots.txt compliance
- domain_rate_limiter.py - Rate limiting
- persistent_url_queue.py - Persistent queue
- crawl_orchestrator.py - Integration layer

Run with: python test_crawl_infrastructure.py
"""

import os
import time
import tempfile
import shutil
from pathlib import Path

# Import components to test
from robots_txt_manager import RobotsTxtManager
from domain_rate_limiter import DomainRateLimiter
from persistent_url_queue import PersistentURLQueue
from crawl_orchestrator import CrawlOrchestrator


class TestCrawlInfrastructure:
    """Test suite for crawl infrastructure components"""

    def __init__(self):
        self.temp_dir = None
        self.passed_tests = 0
        self.failed_tests = 0

    def setup(self):
        """Create temporary directory for tests"""
        self.temp_dir = tempfile.mkdtemp(prefix="crawl_test_")
        print(f"\n🧪 Test directory: {self.temp_dir}")

    def teardown(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up test directory")

    def assert_true(self, condition, message):
        """Assert condition is True"""
        if condition:
            print(f"   ✅ {message}")
            self.passed_tests += 1
        else:
            print(f"   ❌ FAILED: {message}")
            self.failed_tests += 1

    def assert_equal(self, actual, expected, message):
        """Assert actual equals expected"""
        if actual == expected:
            print(f"   ✅ {message}")
            self.passed_tests += 1
        else:
            print(f"   ❌ FAILED: {message}")
            print(f"      Expected: {expected}")
            print(f"      Actual:   {actual}")
            self.failed_tests += 1

    # ═══════════════════════════════════════════════════════════════
    # ROBOTS.TXT MANAGER TESTS
    # ═══════════════════════════════════════════════════════════════

    def test_robots_txt_manager_init(self):
        """Test robots.txt manager initialization"""
        print("\n📝 Test: Robots.txt Manager Initialization")

        manager = RobotsTxtManager(data_dir=self.temp_dir)

        # Check database created
        db_path = Path(self.temp_dir) / "crawl" / "robots_cache.db"
        self.assert_true(db_path.exists(), "Database file created")

        # Check initial stats
        stats = manager.get_cache_stats()
        self.assert_equal(stats['total_cached_domains'], 0, "Initial cache is empty")

    def test_robots_txt_check_wikipedia(self):
        """Test robots.txt check for Wikipedia (real URL)"""
        print("\n📝 Test: Robots.txt Check - Wikipedia")

        manager = RobotsTxtManager(data_dir=self.temp_dir)

        test_url = "https://en.wikipedia.org/wiki/Python"

        # Check if allowed (Wikipedia generally allows crawlers)
        allowed = manager.is_allowed(test_url)
        self.assert_true(allowed, "Wikipedia URL is allowed")

        # Check cache populated
        stats = manager.get_cache_stats()
        self.assert_equal(stats['total_cached_domains'], 1, "Domain cached after check")
        self.assert_equal(stats['total_checks'], 1, "Check recorded")

        # Second check should use cache
        allowed2 = manager.is_allowed(test_url)
        stats2 = manager.get_cache_stats()
        self.assert_true(stats2['cache_hit_rate'] > 0, "Cache hit on second check")

    def test_robots_txt_crawl_delay(self):
        """Test extracting Crawl-delay from robots.txt"""
        print("\n📝 Test: Robots.txt Crawl-delay Extraction")

        manager = RobotsTxtManager(data_dir=self.temp_dir)

        # Wikipedia doesn't typically set crawl-delay, but test the mechanism
        test_url = "https://en.wikipedia.org/wiki/Test"
        crawl_delay = manager.get_crawl_delay(test_url)

        # Crawl delay might be None or a number
        print(f"      Wikipedia crawl delay: {crawl_delay}")
        self.assert_true(crawl_delay is None or crawl_delay > 0, "Crawl delay is valid")

    # ═══════════════════════════════════════════════════════════════
    # RATE LIMITER TESTS
    # ═══════════════════════════════════════════════════════════════

    def test_rate_limiter_init(self):
        """Test rate limiter initialization"""
        print("\n📝 Test: Rate Limiter Initialization")

        limiter = DomainRateLimiter(data_dir=self.temp_dir, min_delay=2.0)

        # Check database created
        db_path = Path(self.temp_dir) / "crawl" / "rate_limiter.db"
        self.assert_true(db_path.exists(), "Database file created")

        # Check initial stats
        stats = limiter.get_stats()
        self.assert_equal(stats['total_domains'], 0, "No domains tracked initially")
        self.assert_equal(stats['total_requests'], 0, "No requests tracked initially")

    def test_rate_limiter_first_request(self):
        """Test first request to domain (no wait needed)"""
        print("\n📝 Test: Rate Limiter - First Request")

        limiter = DomainRateLimiter(data_dir=self.temp_dir, min_delay=2.0)

        test_url = "https://example.com/page1"

        # First request should not require waiting
        wait_time = limiter.get_wait_time(test_url, include_jitter=False)
        self.assert_equal(wait_time, 0.0, "First request requires no wait")

        # Record the request
        limiter.record_request(test_url)

        stats = limiter.get_stats()
        self.assert_equal(stats['total_domains'], 1, "Domain tracked after first request")

    def test_rate_limiter_second_request(self):
        """Test second request to same domain (wait required)"""
        print("\n📝 Test: Rate Limiter - Second Request Requires Wait")

        limiter = DomainRateLimiter(data_dir=self.temp_dir, min_delay=2.0)

        test_url = "https://example.com/page1"

        # First request
        limiter.record_request(test_url)

        # Immediate second request should require waiting
        wait_time = limiter.get_wait_time(test_url, include_jitter=False)
        self.assert_true(wait_time > 0, "Second request requires wait")
        self.assert_true(wait_time <= 2.0, "Wait time doesn't exceed min_delay")

    def test_rate_limiter_crawl_delay_sync(self):
        """Test syncing crawl delay from robots.txt"""
        print("\n📝 Test: Rate Limiter - Robots.txt Crawl Delay Sync")

        limiter = DomainRateLimiter(data_dir=self.temp_dir, min_delay=2.0)

        domain = "https://example.com"

        # Set crawl delay from robots.txt
        limiter.set_crawl_delay(domain, 5.0)

        # Check domain stats
        test_url = "https://example.com/page"
        stats = limiter.get_domain_stats(test_url)

        self.assert_equal(stats['crawl_delay'], 5.0, "Crawl delay synced from robots.txt")

    # ═══════════════════════════════════════════════════════════════
    # PERSISTENT URL QUEUE TESTS
    # ═══════════════════════════════════════════════════════════════

    def test_url_queue_init(self):
        """Test URL queue initialization"""
        print("\n📝 Test: URL Queue Initialization")

        queue = PersistentURLQueue(data_dir=self.temp_dir)

        # Check database created
        db_path = Path(self.temp_dir) / "crawl" / "url_queue.db"
        self.assert_true(db_path.exists(), "Database file created")

        # Check initial stats
        stats = queue.get_stats()
        self.assert_equal(stats['total_urls'], 0, "Queue initially empty")

    def test_url_queue_add(self):
        """Test adding URLs to queue"""
        print("\n📝 Test: URL Queue - Add URLs")

        queue = PersistentURLQueue(data_dir=self.temp_dir)

        # Add URLs
        url1 = "https://example.com/page1"
        url2 = "https://example.com/page2"

        added1 = queue.add(url1, priority=10, depth=0)
        added2 = queue.add(url2, priority=5, depth=1)

        self.assert_true(added1, "First URL added successfully")
        self.assert_true(added2, "Second URL added successfully")

        # Try adding duplicate
        added_dup = queue.add(url1, priority=10, depth=0)
        self.assert_true(not added_dup, "Duplicate URL rejected")

        # Check stats
        stats = queue.get_stats()
        self.assert_equal(stats['total_urls'], 2, "Two URLs in queue")
        self.assert_equal(stats['pending'], 2, "Both URLs pending")

    def test_url_queue_priority(self):
        """Test URL queue priority ordering"""
        print("\n📝 Test: URL Queue - Priority Ordering")

        queue = PersistentURLQueue(data_dir=self.temp_dir)

        # Add URLs with different priorities
        queue.add("https://example.com/low", priority=1, depth=0)
        queue.add("https://example.com/high", priority=10, depth=0)
        queue.add("https://example.com/medium", priority=5, depth=0)

        # Get next URL (should be highest priority)
        next_item = queue.get_next()

        self.assert_equal(next_item['priority'], 10, "Highest priority URL returned first")
        self.assert_true("high" in next_item['url'], "Correct URL returned")

    def test_url_queue_mark_completed(self):
        """Test marking URL as completed"""
        print("\n📝 Test: URL Queue - Mark Completed")

        queue = PersistentURLQueue(data_dir=self.temp_dir)

        url = "https://example.com/page"
        queue.add(url, priority=0, depth=0)

        # Get and complete
        item = queue.get_next()
        queue.mark_completed(item['id'])

        stats = queue.get_stats()
        self.assert_equal(stats['completed'], 1, "URL marked as completed")
        self.assert_equal(stats['pending'], 0, "No pending URLs")

    def test_url_queue_crash_recovery(self):
        """Test crash recovery (in_progress → pending)"""
        print("\n📝 Test: URL Queue - Crash Recovery")

        queue = PersistentURLQueue(data_dir=self.temp_dir)

        # Add URL and get it (marks as in_progress)
        queue.add("https://example.com/page", priority=0, depth=0)
        item = queue.get_next()

        # Simulate crash by creating new queue instance
        queue2 = PersistentURLQueue(data_dir=self.temp_dir)

        stats = queue2.get_stats()
        self.assert_equal(stats['pending'], 1, "In-progress URL recovered to pending")
        self.assert_equal(stats['in_progress'], 0, "No in-progress URLs after recovery")

    # ═══════════════════════════════════════════════════════════════
    # CRAWL ORCHESTRATOR TESTS
    # ═══════════════════════════════════════════════════════════════

    def test_orchestrator_init(self):
        """Test crawl orchestrator initialization"""
        print("\n📝 Test: Crawl Orchestrator Initialization")

        orchestrator = CrawlOrchestrator(data_dir=self.temp_dir, min_delay=2.0)

        # Check all components initialized
        self.assert_true(orchestrator.robots_manager is not None, "Robots manager initialized")
        self.assert_true(orchestrator.rate_limiter is not None, "Rate limiter initialized")
        self.assert_true(orchestrator.url_queue is not None, "URL queue initialized")

    def test_orchestrator_can_crawl(self):
        """Test orchestrator pre-flight check"""
        print("\n📝 Test: Orchestrator - Pre-flight Check")

        orchestrator = CrawlOrchestrator(data_dir=self.temp_dir, min_delay=0.5)

        # Wikipedia should be allowed
        test_url = "https://en.wikipedia.org/wiki/Python"
        can_crawl, reason = orchestrator.can_crawl(test_url)

        self.assert_true(can_crawl, f"Wikipedia allows crawling: {reason}")

    def test_orchestrator_add_url(self):
        """Test adding URL through orchestrator"""
        print("\n📝 Test: Orchestrator - Add URL")

        orchestrator = CrawlOrchestrator(data_dir=self.temp_dir)

        url = "https://example.com/page"
        added = orchestrator.add_url(url, priority=5, depth=0)

        self.assert_true(added, "URL added successfully")

        # Check in queue
        stats = orchestrator.get_stats()
        self.assert_equal(stats['queue']['total_urls'], 1, "URL in queue")

    def test_orchestrator_prepare_and_record(self):
        """Test orchestrator prepare + record flow"""
        print("\n📝 Test: Orchestrator - Prepare and Record Success")

        orchestrator = CrawlOrchestrator(data_dir=self.temp_dir, min_delay=0.5)

        url = "https://en.wikipedia.org/wiki/Test"

        # Prepare crawl
        url_id = orchestrator.prepare_crawl(url, wait_if_needed=True)
        self.assert_true(url_id is not None, "Prepare crawl successful")

        # Record success
        orchestrator.record_success(url_id, url)

        stats = orchestrator.get_stats()
        self.assert_equal(stats['queue']['completed'], 1, "URL marked completed")

    def test_orchestrator_health_check(self):
        """Test orchestrator health check"""
        print("\n📝 Test: Orchestrator - Health Check")

        orchestrator = CrawlOrchestrator(data_dir=self.temp_dir)

        health = orchestrator.health_check()

        self.assert_true(health['status'] in ['healthy', 'issues_detected'], "Health status valid")
        self.assert_true('stats' in health, "Health check includes stats")

    # ═══════════════════════════════════════════════════════════════
    # RUN ALL TESTS
    # ═══════════════════════════════════════════════════════════════

    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "=" * 70)
        print("🧪 CRAWL INFRASTRUCTURE TEST SUITE")
        print("=" * 70)

        self.setup()

        try:
            # Robots.txt manager tests
            print("\n" + "─" * 70)
            print("🤖 ROBOTS.TXT MANAGER TESTS")
            print("─" * 70)
            self.test_robots_txt_manager_init()
            self.test_robots_txt_check_wikipedia()
            self.test_robots_txt_crawl_delay()

            # Rate limiter tests
            print("\n" + "─" * 70)
            print("⏱️  RATE LIMITER TESTS")
            print("─" * 70)
            self.test_rate_limiter_init()
            self.test_rate_limiter_first_request()
            self.test_rate_limiter_second_request()
            self.test_rate_limiter_crawl_delay_sync()

            # URL queue tests
            print("\n" + "─" * 70)
            print("📊 PERSISTENT URL QUEUE TESTS")
            print("─" * 70)
            self.test_url_queue_init()
            self.test_url_queue_add()
            self.test_url_queue_priority()
            self.test_url_queue_mark_completed()
            self.test_url_queue_crash_recovery()

            # Orchestrator tests
            print("\n" + "─" * 70)
            print("🎭 CRAWL ORCHESTRATOR TESTS")
            print("─" * 70)
            self.test_orchestrator_init()
            self.test_orchestrator_can_crawl()
            self.test_orchestrator_add_url()
            self.test_orchestrator_prepare_and_record()
            self.test_orchestrator_health_check()

        finally:
            self.teardown()

        # Summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Total:  {self.passed_tests + self.failed_tests}")

        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED!")
            return 0
        else:
            print(f"\n⚠️  {self.failed_tests} TEST(S) FAILED")
            return 1


if __name__ == "__main__":
    tester = TestCrawlInfrastructure()
    exit_code = tester.run_all_tests()
    exit(exit_code)
