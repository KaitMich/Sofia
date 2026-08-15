#!/usr/bin/env python3
"""
Test: Autonomous Learning Integration

Verifies that the complete autonomous learning cycle works:
1. Curiosity engine generates intrinsic goals
2. URL mapper converts goals → URLs
3. Enhanced learner uses autonomous targets (no manual seeds)
4. System learns based purely on internal drives

This is the test of TRUE AUTONOMY.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sofia.core.curiosity_engine import CuriosityEngine
from sofia.crawler.curiosity_url_mapper import CuriosityURLMapper
from sofia.utils.learning_progression_tracker import LearningProgressionTracker



def _discovered_candidates():
    """Simulated persistent-queue candidates: links Sofia discovered herself."""
    return [
        {"url": "https://en.wikipedia.org/wiki/Understanding", "anchor_text": "understanding and comprehension in cognition", "priority": 10},
        {"url": "https://en.wikipedia.org/wiki/Knowledge", "anchor_text": "knowledge acquisition and epistemology", "priority": 9},
        {"url": "https://en.wikipedia.org/wiki/Learning", "anchor_text": "learning processes and skill formation", "priority": 8},
        {"url": "https://en.wikipedia.org/wiki/Curiosity", "anchor_text": "curiosity as a drive for exploration", "priority": 7},
        {"url": "https://en.wikipedia.org/wiki/Pattern_recognition", "anchor_text": "pattern recognition in cognitive systems", "priority": 6},
        {"url": "https://en.wikipedia.org/wiki/Ice_hockey", "anchor_text": "professional ice hockey league standings", "priority": 90},
        {"url": "https://en.wikipedia.org/wiki/Lawn_care", "anchor_text": "lawn care and grass fertilizer schedules", "priority": 85},
    ]

def test_autonomous_url_generation():
    """Test autonomous URL generation from curiosity alone."""
    print("\n" + "=" * 70)
    print("TEST 1: Autonomous URL Generation")
    print("=" * 70)

    # Initialize components
    curiosity = CuriosityEngine()
    tracker = LearningProgressionTracker()
    mapper = CuriosityURLMapper()

    # Generate intrinsic goals (no human input)
    goals = curiosity.generate_intrinsic_goals()
    print(f"\n✅ Generated {len(goals)} intrinsic goals")

    if goals:
        print(f"\n   Top goal: {goals[0].get('description', 'N/A')[:70]}")
        print(f"   Urgency: {goals[0].get('urgency', 0):.2f}")

    # Get curiosity state
    curiosity_state = curiosity.export_for_consciousness_system()

    # Get progression state
    progression_state = tracker.export_for_consciousness_system()

    # NEW CONTRACT (July 2026): without discovered candidates, no URLs are
    # fabricated — the old path string-formatted goal words into wiki URLs
    empty_batch = mapper.generate_autonomous_seed_batch(
        curiosity_state=curiosity_state,
        progression_state=progression_state,
        max_total_urls=10
    )
    assert empty_batch == [], "Must not fabricate URLs without discovered candidates"

    # With discovered candidates, goals rank them by embedding similarity
    url_batch = mapper.generate_autonomous_seed_batch(
        curiosity_state=curiosity_state,
        progression_state=progression_state,
        max_total_urls=10,
        candidates=_discovered_candidates()
    )

    print(f"\n✅ Ranked {len(url_batch)} autonomous URLs from discovered candidates")
    for i, (url, priority, source) in enumerate(url_batch[:5], 1):
        print(f"      {i}. [{priority:.2f}] ({source:20s}) {url}")

    assert len(url_batch) > 0, "Should rank at least 1 discovered URL"
    assert all(url.startswith('http') for url, _, _ in url_batch), "All URLs should be valid HTTP/HTTPS"
    assert all(0 <= priority <= 1.0 for _, priority, _ in url_batch), "Priorities should be 0-1.0"

    print(f"\n✅ TEST 1 PASSED: Autonomous URL generation working")
    return True


def test_curiosity_state_influence():
    """Test that curiosity state influences URL selection."""
    print("\n" + "=" * 70)
    print("TEST 2: Curiosity State Influence on URL Selection")
    print("=" * 70)

    curiosity = CuriosityEngine()
    tracker = LearningProgressionTracker()
    mapper = CuriosityURLMapper()

    # Artificially lower 'understanding' drive satisfaction
    curiosity.update_drive_satisfaction('understanding', -0.5, "Test: Creating urgency")

    # Generate URLs
    curiosity_state = curiosity.export_for_consciousness_system()
    progression_state = tracker.export_for_consciousness_system()

    url_batch = mapper.generate_autonomous_seed_batch(
        curiosity_state=curiosity_state,
        progression_state=progression_state,
        max_total_urls=15,
        candidates=_discovered_candidates()
    )

    print(f"\n✅ Ranked {len(url_batch)} discovered URLs")
    for url, priority, _ in url_batch[:4]:
        print(f"      [{priority:.2f}] {url}")

    # Influence check: cognition-related candidates must outrank unrelated
    # high-queue-priority ones (hockey at priority 90, lawn care at 85)
    assert len(url_batch) > 0, "Should rank discovered candidates"
    top3 = " ".join(url for url, _, _ in url_batch[:3])
    assert "Ice_hockey" not in top3 and "Lawn_care" not in top3, \
        "Curiosity must outrank stale queue priority"

    # Check priority ordering
    priorities = [p for _, p, _ in url_batch]
    assert priorities == sorted(priorities, reverse=True), "URLs should be sorted by priority"

    print(f"\n✅ TEST 2 PASSED: Curiosity state influences URL selection")
    return True


def test_knowledge_gap_targeting():
    """Test that knowledge gaps generate URLs."""
    print("\n" + "=" * 70)
    print("TEST 3: Knowledge Gap → URL Targeting")
    print("=" * 70)

    curiosity = CuriosityEngine()
    tracker = LearningProgressionTracker()
    mapper = CuriosityURLMapper()

    # Simulate knowledge gaps
    mock_gaps = [
        "neural correlates of consciousness",
        "emergent properties in complex systems",
        "self-referential cognition"
    ]

    # Generate gap URLs
    gap_urls = mapper.knowledge_gaps_to_urls(mock_gaps, max_urls=5)

    print(f"\n✅ Generated {len(gap_urls)} URLs for {len(mock_gaps)} knowledge gaps")

    for i, (url, priority) in enumerate(gap_urls, 1):
        print(f"      {i}. [{priority:.2f}] {url}")

    # Verify
    assert len(gap_urls) > 0, "Should generate URLs for knowledge gaps"
    assert all(priority >= 0.8 for _, priority in gap_urls), "Gap URLs should have high priority (>=0.8)"

    print(f"\n✅ TEST 3 PASSED: Knowledge gaps correctly targeted")
    return True


def test_goal_to_url_mapping():
    """Test direct goal → URL mapping."""
    print("\n" + "=" * 70)
    print("TEST 4: Learning Goal → URL Mapping")
    print("=" * 70)

    mapper = CuriosityURLMapper()

    test_goals = [
        {
            'description': 'Understand how consciousness emerges from neural activity',
            'urgency': 0.9,
            'type': 'understanding'
        },
        {
            'description': 'Explore novel ways of combining existing knowledge',
            'urgency': 0.8,
            'type': 'creativity'
        },
        {
            'description': 'Develop deeper connections between concepts',
            'urgency': 0.7,
            'type': 'connection'
        }
    ]

    goal_urls = mapper.goals_to_seed_urls(test_goals, max_urls=10)

    print(f"\n✅ Generated {len(goal_urls)} URLs from {len(test_goals)} goals")

    for i, (url, priority) in enumerate(goal_urls[:5], 1):
        print(f"      {i}. [{priority:.2f}] {url}")

    # Verify
    assert len(goal_urls) > 0, "Should generate URLs from goals"

    # Check that urgency influences priority
    high_urgency_urls = [p for _, p in goal_urls if p > 0.7]
    assert len(high_urgency_urls) > 0, "High urgency goals should generate high priority URLs"

    print(f"\n✅ TEST 4 PASSED: Goals correctly mapped to URLs")
    return True


def test_full_autonomous_cycle():
    """Test the complete autonomous learning cycle."""
    print("\n" + "=" * 70)
    print("TEST 5: Full Autonomous Learning Cycle")
    print("=" * 70)
    print("   This simulates what happens when seed_urls=None")
    print("=" * 70)

    # Initialize all components (as enhanced_autonomous_learner does)
    curiosity = CuriosityEngine()
    tracker = LearningProgressionTracker()
    mapper = CuriosityURLMapper()

    print("\n1️⃣ Curiosity generates intrinsic goals...")
    goals = curiosity.generate_intrinsic_goals()
    print(f"   ✅ Generated {len(goals)} goals")

    print("\n2️⃣ Getting current curiosity state...")
    curiosity_state = curiosity.export_for_consciousness_system()
    summary = curiosity_state.get('curiosity_summary', {})
    print(f"   ✅ Motivation level: {summary.get('motivation_level', 0):.2f}")
    print(f"   ✅ Curiosity intensity: {summary.get('curiosity_intensity', 0):.2f}")
    print(f"   ✅ Most unsatisfied drive: {summary.get('most_unsatisfied_drive', 'none')}")

    print("\n3️⃣ Getting learning progression state...")
    progression_state = tracker.export_for_consciousness_system()
    print(f"   ✅ Progression data retrieved")

    print("\n4️⃣ Mapper converts goals + gaps → URLs...")
    url_batch = mapper.generate_autonomous_seed_batch(
        curiosity_state=curiosity_state,
        progression_state=progression_state,
        max_total_urls=20,
        candidates=_discovered_candidates()
    )
    print(f"   ✅ Ranked {len(url_batch)} autonomous URLs from discovered links")

    print("\n5️⃣ URLs are prioritized by internal drives...")
    print(f"   Top 3 autonomous targets:")
    for i, (url, priority, source) in enumerate(url_batch[:3], 1):
        print(f"      {i}. [{priority:.2f}] ({source})")
        print(f"         {url}")

    print("\n6️⃣ Verifying autonomous decision quality...")

    # Quality checks
    assert len(url_batch) >= 5, "Should generate sufficient URLs for autonomous learning"
    assert len(url_batch) <= 20, "Should respect max_total_urls limit"

    # All targets come from embedding ranking over discovered links
    sources = set(source for _, _, source in url_batch)
    print(f"   ✅ URL sources: {sources}")
    assert sources == {'embedding_curiosity'}, "Targets must come from embedding ranking"

    # Check priority distribution
    priorities = [p for _, p, _ in url_batch]
    avg_priority = sum(priorities) / len(priorities)
    print(f"   ✅ Average priority: {avg_priority:.2f}")
    assert avg_priority > 0.5, "Autonomous URLs should have meaningful priority"

    # Check URL validity
    urls = [url for url, _, _ in url_batch]
    assert all(url.startswith('https://') for url in urls), "All URLs should be HTTPS"
    assert len(set(urls)) == len(urls), "URLs should be unique (no duplicates)"

    print(f"\n✅ TEST 5 PASSED: Full autonomous cycle functional!")
    print("\n" + "=" * 70)
    print("🎯 RESULT: Sophia can decide what to learn without human input")
    print("=" * 70)

    return True


def main():
    """Run all autonomous learning integration tests."""
    print("\n" + "=" * 70)
    print("🧠 AUTONOMOUS LEARNING INTEGRATION TESTS")
    print("=" * 70)
    print("Testing the bridge between curiosity (internal) and action (external)")
    print("=" * 70)

    tests = [
        ("Autonomous URL Generation", test_autonomous_url_generation),
        ("Curiosity State Influence", test_curiosity_state_influence),
        ("Knowledge Gap Targeting", test_knowledge_gap_targeting),
        ("Goal → URL Mapping", test_goal_to_url_mapping),
        ("Full Autonomous Cycle", test_full_autonomous_cycle)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ TEST ERROR: {test_name}")
            print(f"   Exception: {e}")
            failed += 1

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 70)
        print("\n🧠 AUTONOMOUS LEARNING CAPABILITY VERIFIED:")
        print("   ✅ Curiosity generates intrinsic goals")
        print("   ✅ Goals convert to actionable URLs")
        print("   ✅ Knowledge gaps targeted automatically")
        print("   ✅ Drives influence URL selection")
        print("   ✅ Full autonomous cycle functional")
        print("\n🎯 Sophia can now learn without human-provided seed URLs")
        print("   This is TRUE COGNITIVE AUTONOMY")
        print("=" * 70)
        return True
    else:
        print(f"\n⚠️ {failed} test(s) failed - review output above")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
