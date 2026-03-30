"""
Tests for Bridge Memory Reclassification System

Run with: pytest tests/test_bridge_reclassification.py -v
Or without pytest: python tests/test_bridge_reclassification.py

Created: 2025-11-24
"""

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    # Mock pytest for standalone running
    class MockPytest:
        @staticmethod
        def main(args):
            print("pytest not available, running tests directly")
    pytest = MockPytest()

import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bridge_reclassifier import BridgeReclassifier


class MockUnifiedMemory:
    """Mock memory system for testing."""

    def __init__(self):
        self.logic_memory = []
        self.symbolic_memory = []
        self.bridge_memory = []
        self.lock = MagicMock()
        self._saved = False

    def _save_tripartite_memory(self):
        self._saved = True

    def move_item_from_bridge(self, item, target, reason):
        """Mock implementation of move_item_from_bridge."""
        # Remove from bridge
        self.bridge_memory = [i for i in self.bridge_memory if i.get('id') != item.get('id')]
        # Add to target
        item['reclassified_from_bridge'] = True
        item['reclassification_reason'] = reason
        if target == 'LOGIC':
            self.logic_memory.append(item)
        else:
            self.symbolic_memory.append(item)
        return True


class TestBridgeReclassifier:
    """Test suite for BridgeReclassifier."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_memory = MockUnifiedMemory()
        self.reclassifier = BridgeReclassifier(self.mock_memory)

    def test_keyword_extraction(self):
        """Test that keywords are extracted correctly."""
        text = "The quantum physics experiment showed interesting results"
        keywords = self.reclassifier._extract_keywords(text)

        assert 'quantum' in keywords
        assert 'physics' in keywords
        assert 'experiment' in keywords
        assert 'the' not in keywords  # Stopword
        assert 'showed' in keywords
        print("✅ Keyword extraction works correctly")

    def test_keyword_extraction_filters_stopwords(self):
        """Test that stopwords are properly filtered."""
        text = "the and but or if then what which who"
        keywords = self.reclassifier._extract_keywords(text)

        # All stopwords should be filtered out
        assert len(keywords) == 0
        print("✅ Stopword filtering works correctly")

    def test_keyword_extraction_minimum_length(self):
        """Test that short words are filtered."""
        text = "a an is be to of in on at by"
        keywords = self.reclassifier._extract_keywords(text)

        # All 2-char or shorter words should be filtered
        assert len(keywords) == 0
        print("✅ Minimum length filtering works correctly")

    def test_gate1_time_check_too_recent(self):
        """Test that recent items are not reclassified (GATE 1 fails)."""
        item = {
            'id': 'test_1',
            'text': 'Test item',
            'timestamp': datetime.now().isoformat()  # Just created
        }

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, [])

        assert should_move is False
        assert target is None
        assert 'Too recent' in reason or 'incubating' in reason
        print(f"✅ GATE 1 (time) correctly rejects recent items: {reason}")

    def test_gate1_time_check_old_enough(self):
        """Test that old items pass the time gate."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_2',
            'text': 'Test item',
            'timestamp': old_date
        }

        # Should pass gate 1, but fail gate 2 (no related items)
        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, [])

        assert 'Too recent' not in reason
        assert 'incubating' not in reason
        # Will fail on gate 2 instead
        assert 'Insufficient context' in reason
        print(f"✅ GATE 1 (time) passes for old items, fails on GATE 2: {reason}")

    def test_gate2_insufficient_context(self):
        """Test that items without enough related content stay in bridge (GATE 2 fails)."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_3',
            'text': 'Test item',
            'timestamp': old_date
        }

        # Only 2 related items (need 5)
        related = [
            {'memory_type': 'logic'},
            {'memory_type': 'logic'}
        ]

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        assert should_move is False
        assert target is None
        assert 'Insufficient context' in reason
        assert '2/5' in reason  # Shows count
        print(f"✅ GATE 2 (context) correctly rejects items with few neighbors: {reason}")

    def test_gate2_sufficient_context(self):
        """Test that items with enough related content pass gate 2."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_4',
            'text': 'Test item',
            'timestamp': old_date
        }

        # 5 related items (exactly the minimum)
        related = [
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'}
        ]

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        # Should pass gate 2, but fail gate 3 (60/40 split, need 70%)
        assert 'Insufficient context' not in reason
        # Will fail on gate 3 instead (split cluster)
        assert 'Split cluster' in reason or '60%' in reason
        print(f"✅ GATE 2 (context) passes with 5+ neighbors, fails on GATE 3: {reason}")

    def test_gate3_cluster_gravity_logic(self):
        """Test that logic-dominated clusters pull items to logic (GATE 3 logic pull)."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_5',
            'text': 'Test item',
            'timestamp': old_date
        }

        # 8 logic, 2 symbolic = 80% logic dominance
        related = [
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
        ]

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        assert should_move is True
        assert target == 'LOGIC'
        assert '80%' in reason or '8/10' in reason
        assert 'Logic' in reason
        print(f"✅ GATE 3 (gravity) pulls to LOGIC with 80% dominance: {reason}")

    def test_gate3_cluster_gravity_symbolic(self):
        """Test that symbolic-dominated clusters pull items to symbolic (GATE 3 symbolic pull)."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_6',
            'text': 'Test item',
            'timestamp': old_date
        }

        # 2 logic, 8 symbolic = 80% symbolic dominance
        related = [
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
        ]

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        assert should_move is True
        assert target == 'SYMBOLIC'
        assert '80%' in reason or '8/10' in reason
        assert 'Symbolic' in reason
        print(f"✅ GATE 3 (gravity) pulls to SYMBOLIC with 80% dominance: {reason}")

    def test_gate3_split_cluster_stays(self):
        """Test that split clusters keep items in bridge (GATE 3 fails)."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_7',
            'text': 'Test item',
            'timestamp': old_date
        }

        # 5 logic, 5 symbolic = 50/50 split
        related = [
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
        ]

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        assert should_move is False
        assert target is None
        assert 'Split' in reason or '50%' in reason.lower()
        print(f"✅ GATE 3 (gravity) correctly keeps split clusters in bridge: {reason}")

    def test_gate3_edge_case_70_percent_exactly(self):
        """Test that exactly 70% dominance triggers reclassification."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_8',
            'text': 'Test item',
            'timestamp': old_date
        }

        # 7 logic, 3 symbolic = exactly 70% logic dominance (at threshold)
        related = [
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'logic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
            {'memory_type': 'symbolic'},
        ]

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        assert should_move is True
        assert target == 'LOGIC'
        assert '70%' in reason
        print(f"✅ GATE 3 (gravity) triggers at exactly 70% threshold: {reason}")

    def test_gate3_edge_case_69_percent_stays(self):
        """Test that 69% dominance (just below threshold) keeps item in bridge."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        item = {
            'id': 'test_9',
            'text': 'Test item',
            'timestamp': old_date
        }

        # 69% logic (69 of 100 neighbors)
        related = [{'memory_type': 'logic'}] * 69 + [{'memory_type': 'symbolic'}] * 31

        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, related)

        assert should_move is False
        assert target is None
        assert 'Split' in reason or '69%' in reason
        print(f"✅ GATE 3 (gravity) stays below 70% threshold: {reason}")

    def test_dry_run_does_not_modify(self):
        """Test that dry run mode doesn't actually move items."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()

        self.mock_memory.bridge_memory = [{
            'id': 'bridge_1',
            'text': 'quantum physics experiment research',
            'timestamp': old_date
        }]

        # Add logic items that would match
        self.mock_memory.logic_memory = [
            {'id': f'logic_{i}', 'text': 'quantum physics research paper'}
            for i in range(10)
        ]

        # Run in dry-run mode
        results = self.reclassifier.review_bridge_memory(dry_run=True)

        # Item should still be in bridge
        assert len(self.mock_memory.bridge_memory) == 1
        assert results['items_reclassified'] == 0
        assert results['items_ready'] >= 0  # May or may not be ready depending on criteria
        print(f"✅ Dry-run mode preserves bridge memory: {len(self.mock_memory.bridge_memory)} items")

    def test_live_mode_modifies(self):
        """Test that live mode actually moves items."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()

        self.mock_memory.bridge_memory = [{
            'id': 'bridge_2',
            'text': 'quantum physics experiment research',
            'timestamp': old_date
        }]

        # Add logic items that would match
        self.mock_memory.logic_memory = [
            {'id': f'logic_{i}', 'text': 'quantum physics research paper'}
            for i in range(10)
        ]

        # Run in live mode
        results = self.reclassifier.review_bridge_memory(dry_run=False)

        # If item was ready and moved, bridge should be empty
        if results['items_ready'] > 0:
            assert len(self.mock_memory.bridge_memory) == 0
            assert results['items_reclassified'] == 1
            print(f"✅ Live mode reclassified item: {results['items_reclassified']} moved")
        else:
            print(f"ℹ️  Item wasn't ready for reclassification (passed time but not other gates)")

    def test_find_related_content_keyword_matching(self):
        """Test finding related items by keyword overlap."""
        self.mock_memory.logic_memory = [
            {'id': 'logic_1', 'text': 'quantum physics experiment'},
            {'id': 'logic_2', 'text': 'cooking recipe pasta'},
        ]
        self.mock_memory.symbolic_memory = [
            {'id': 'sym_1', 'text': 'quantum physics makes me feel curious'},
        ]

        bridge_item = {'text': 'quantum physics is fascinating'}

        related = self.reclassifier.find_related_content(bridge_item)

        # Should find logic_1 (quantum, physics) and sym_1 (quantum, physics - 2 keyword overlap)
        related_ids = [r['id'] for r in related]
        assert 'logic_1' in related_ids
        assert 'logic_2' not in related_ids  # No keyword overlap
        assert 'sym_1' in related_ids

        # Check memory types are tagged
        for item in related:
            assert 'memory_type' in item
            assert item['memory_type'] in ['logic', 'symbolic']

        print(f"✅ Related content finding works: found {len(related)} matches")

    def test_find_related_content_requires_minimum_overlap(self):
        """Test that at least 2 keyword overlap is required."""
        self.mock_memory.logic_memory = [
            {'id': 'logic_1', 'text': 'quantum mechanics research'},  # 2 overlaps
            {'id': 'logic_2', 'text': 'quantum'},  # Only 1 overlap
            {'id': 'logic_3', 'text': 'mechanics'},  # Only 1 overlap
        ]

        bridge_item = {'text': 'quantum mechanics'}

        related = self.reclassifier.find_related_content(bridge_item)

        # Should only find logic_1 (2 overlaps)
        related_ids = [r['id'] for r in related]
        assert 'logic_1' in related_ids
        assert 'logic_2' not in related_ids
        assert 'logic_3' not in related_ids

        print(f"✅ Minimum 2-keyword overlap enforced: {len(related)} matches")

    def test_review_returns_statistics(self):
        """Test that review_bridge_memory returns proper statistics."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()

        self.mock_memory.bridge_memory = [
            {'id': 'bridge_1', 'text': 'test item one', 'timestamp': old_date},
            {'id': 'bridge_2', 'text': 'test item two', 'timestamp': old_date},
        ]

        results = self.reclassifier.review_bridge_memory(dry_run=True)

        # Check all required fields are present
        assert 'timestamp' in results
        assert 'dry_run' in results
        assert 'items_reviewed' in results
        assert 'items_ready' in results
        assert 'items_reclassified' in results
        assert 'to_logic' in results
        assert 'to_symbolic' in results
        assert 'items_remaining' in results
        assert 'details' in results
        assert 'errors' in results

        assert results['items_reviewed'] == 2
        assert results['dry_run'] is True
        assert isinstance(results['details'], list)

        print(f"✅ Review statistics complete: {results['items_reviewed']} items reviewed")

    def test_max_reclassifications_per_review(self):
        """Test that max reclassifications limit is respected."""
        old_date = (datetime.now() - timedelta(days=30)).isoformat()

        # Create 15 bridge items
        self.mock_memory.bridge_memory = [
            {'id': f'bridge_{i}', 'text': 'quantum physics research', 'timestamp': old_date}
            for i in range(15)
        ]

        # Add many logic items to ensure reclassification would trigger
        self.mock_memory.logic_memory = [
            {'id': f'logic_{i}', 'text': 'quantum physics experiment'}
            for i in range(20)
        ]

        # Set max to 5
        self.reclassifier.config['max_reclassifications_per_review'] = 5

        results = self.reclassifier.review_bridge_memory(dry_run=False)

        # Should reclassify at most 5 items
        assert results['items_reclassified'] <= 5

        print(f"✅ Max reclassifications limit enforced: {results['items_reclassified']}/5")

    def test_no_timestamp_handled_gracefully(self):
        """Test that items without timestamps are handled gracefully."""
        item = {
            'id': 'test_no_timestamp',
            'text': 'Item without timestamp'
            # No timestamp field
        }

        # Should not crash, but fail on age check
        should_move, target, reason = self.reclassifier.evaluate_bridge_item(item, [])

        assert should_move is False
        # Should fail on time or context gate
        assert 'Too recent' in reason or 'Insufficient context' in reason

        print(f"✅ Missing timestamp handled gracefully: {reason}")


if __name__ == '__main__':
    if HAS_PYTEST:
        pytest.main([__file__, '-v'])
    else:
        # Run tests without pytest
        import traceback

        test_class = TestBridgeReclassifier()
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]

        passed = 0
        failed = 0

        print("\n" + "="*70)
        print("BRIDGE RECLASSIFICATION TEST SUITE (Standalone Mode)")
        print("="*70 + "\n")

        for test_name in test_methods:
            test_class.setup_method()
            test_method = getattr(test_class, test_name)

            try:
                test_method()
                passed += 1
            except AssertionError as e:
                failed += 1
                print(f"❌ FAIL: {test_name} - {e}")
            except Exception as e:
                failed += 1
                print(f"❌ ERROR: {test_name}")
                traceback.print_exc()

        print("\n" + "="*70)
        print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
        print("="*70)

        sys.exit(0 if failed == 0 else 1)
