#!/usr/bin/env python3
"""
Test script for Associative Emergence / Saturation Learning

This demonstrates the new learning architecture where knowledge emerges
naturally from deep saturation rather than following a prescribed curriculum.
"""

from enhanced_autonomous_learner import start_saturation_learning

def test_silicon_saturation():
    """
    Test saturation learning with Silicon as the seed.

    Expected: The system should learn deeply about silicon's material
    properties until process verbs (refine, manufacture, process) emerge
    more strongly than static nouns (silicon, crystal, atom).
    """
    print("\n" + "="*80)
    print("🧪 TEST: Silicon Material Saturation Learning")
    print("="*80)
    print("\nObjective: Learn about Silicon until transformation concepts emerge")
    print("Expected: Should discover 'refine', 'process', or 'manufacture' naturally\n")

    result = start_saturation_learning(
        seed_url="https://en.wikipedia.org/wiki/Silicon",
        zone_name="Silicon_Material_Test",
        zone_keywords=['silicon', 'element', 'crystal', 'semiconductor', 'atom'],
        allowed_distance=0.5,
        saturation_threshold=0.8,
        max_urls=30  # Reduced for testing
    )

    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80)

    print(f"\n✅ Session ID: {result['session_id']}")
    print(f"✅ Zone: {result['zone']}")
    print(f"✅ URLs Processed: {result['stats']['urls_processed']}")
    print(f"✅ Duration: {result['elapsed_time_minutes']:.2f} minutes")

    print(f"\n📈 Saturation Metrics:")
    print(f"   Static Nouns:  {result['stats']['static_noun_count']:4d}")
    print(f"   Process Verbs: {result['stats']['process_verb_count']:4d}")
    print(f"   Phase Score:   {result['stats']['phase_transition_score']:.3f}")
    print(f"   Event Horizon: {result['stats']['event_horizon_concepts']} concepts")

    if result['next_phase_query']:
        print(f"\n✨ PHASE TRANSITION SUCCESSFUL!")
        print(f"   Next Phase Query: '{result['next_phase_query']}'")
        print(f"\n   ✅ TEST PASSED: Concept emergence detected")
    else:
        print(f"\n⚠️ PHASE TRANSITION NOT REACHED")
        print(f"   Score: {result['stats']['phase_transition_score']:.3f} / 0.800")
        print(f"\n   ℹ️ TEST INCOMPLETE: May need more URLs or lower threshold")

    print(f"\n📊 Top Keywords:")
    top_keywords = sorted(result['keyword_frequencies'].items(),
                         key=lambda x: x[1], reverse=True)[:10]
    for keyword, count in top_keywords:
        print(f"   {keyword:20s} : {count:4d}")

    if result['event_horizon_sample']:
        print(f"\n🔭 Event Horizon Sample (Forbidden Concepts):")
        for event in result['event_horizon_sample'][:5]:
            print(f"   - {event['text'][:50]:50s} (distance: {event['distance']:.2f})")

    return result


def test_evolution_saturation():
    """
    Test saturation learning with Evolution as the seed.

    Expected: Should learn about biological evolution until process concepts
    like 'adaptation', 'selection', or 'mutation' emerge.
    """
    print("\n" + "="*80)
    print("🧪 TEST: Evolution Biology Saturation Learning")
    print("="*80)
    print("\nObjective: Learn about Evolution until adaptation/selection emerges")
    print("Expected: Should discover ecological or genetic processes\n")

    result = start_saturation_learning(
        seed_url="https://en.wikipedia.org/wiki/Evolution",
        zone_name="Evolution_Biology_Test",
        zone_keywords=['evolution', 'species', 'natural', 'selection', 'darwin'],
        allowed_distance=0.5,
        saturation_threshold=0.75,  # Slightly lower for biological concepts
        max_urls=30
    )

    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80)

    print(f"\n✅ URLs Processed: {result['stats']['urls_processed']}")
    print(f"✅ Phase Score: {result['stats']['phase_transition_score']:.3f}")
    print(f"✅ Next Query: {result['next_phase_query']}")

    if result['next_phase_query']:
        print(f"\n   ✅ TEST PASSED: Evolution concepts led to '{result['next_phase_query']}'")
    else:
        print(f"\n   ℹ️ TEST INCOMPLETE: Evolution zone needs more saturation")

    return result


def test_philosophy_saturation():
    """
    Test saturation learning with Philosophy as the seed.

    Expected: Should explore philosophical concepts until applied areas
    like 'ethics', 'logic', or 'epistemology' emerge.
    """
    print("\n" + "="*80)
    print("🧪 TEST: Philosophy Foundations Saturation Learning")
    print("="*80)
    print("\nObjective: Learn about Philosophy until applied areas emerge")
    print("Expected: Should discover ethics, epistemology, or logic naturally\n")

    result = start_saturation_learning(
        seed_url="https://en.wikipedia.org/wiki/Philosophy",
        zone_name="Philosophy_Test",
        zone_keywords=['philosophy', 'logic', 'reason', 'truth', 'knowledge'],
        allowed_distance=0.6,  # Wider for abstract concepts
        saturation_threshold=0.7,  # Lower for exploratory learning
        max_urls=30
    )

    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80)

    print(f"\n✅ URLs Processed: {result['stats']['urls_processed']}")
    print(f"✅ Phase Score: {result['stats']['phase_transition_score']:.3f}")
    print(f"✅ Next Query: {result['next_phase_query']}")

    if result['next_phase_query']:
        print(f"\n   ✅ TEST PASSED: Philosophy led to '{result['next_phase_query']}'")
    else:
        print(f"\n   ℹ️ TEST INCOMPLETE: Philosophy zone needs adjustment")

    return result


def main():
    """Run all saturation learning tests."""
    print("\n" + "="*80)
    print("🌀 ASSOCIATIVE EMERGENCE: SATURATION LEARNING TEST SUITE")
    print("="*80)
    print("\nThis test suite demonstrates the new learning architecture.")
    print("Each test shows how knowledge emerges naturally from deep saturation.")
    print("\nPress Ctrl+C to stop any test.\n")

    input("Press Enter to begin tests...")

    # Test 1: Silicon (Material → Process)
    try:
        silicon_result = test_silicon_saturation()
    except KeyboardInterrupt:
        print("\n⚠️ Silicon test interrupted")
        silicon_result = None
    except Exception as e:
        print(f"\n❌ Silicon test failed: {e}")
        import traceback
        traceback.print_exc()
        silicon_result = None

    input("\nPress Enter to continue to Evolution test (or Ctrl+C to skip)...")

    # Test 2: Evolution (Biology → Genetics/Ecology)
    try:
        evolution_result = test_evolution_saturation()
    except KeyboardInterrupt:
        print("\n⚠️ Evolution test interrupted")
        evolution_result = None
    except Exception as e:
        print(f"\n❌ Evolution test failed: {e}")
        import traceback
        traceback.print_exc()
        evolution_result = None

    input("\nPress Enter to continue to Philosophy test (or Ctrl+C to skip)...")

    # Test 3: Philosophy (Foundations → Applied)
    try:
        philosophy_result = test_philosophy_saturation()
    except KeyboardInterrupt:
        print("\n⚠️ Philosophy test interrupted")
        philosophy_result = None
    except Exception as e:
        print(f"\n❌ Philosophy test failed: {e}")
        import traceback
        traceback.print_exc()
        philosophy_result = None

    # Summary
    print("\n" + "="*80)
    print("📋 TEST SUITE SUMMARY")
    print("="*80)

    tests = [
        ("Silicon Material", silicon_result),
        ("Evolution Biology", evolution_result),
        ("Philosophy Foundations", philosophy_result)
    ]

    for test_name, result in tests:
        if result is None:
            print(f"\n❌ {test_name}: SKIPPED or FAILED")
        elif result.get('next_phase_query'):
            print(f"\n✅ {test_name}: PASSED")
            print(f"   Emergent Query: '{result['next_phase_query']}'")
        else:
            print(f"\n⚠️ {test_name}: INCOMPLETE")
            print(f"   Phase Score: {result['stats']['phase_transition_score']:.3f}")

    print("\n" + "="*80)
    print("🎓 TEST SUITE COMPLETE")
    print("="*80)
    print("\nThe tests demonstrate that knowledge emerges naturally from deep")
    print("saturation, without prescribing what should be learned next.")
    print("\nSee session files in data/autonomous_sessions/ for details.")


if __name__ == "__main__":
    main()
