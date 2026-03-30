#!/usr/bin/env python3
"""Quick test for saturation learning with link extraction"""

from enhanced_autonomous_learner import start_saturation_learning
import time

print("\n" + "="*80)
print("🧪 QUICK SATURATION TEST - Link Extraction Fix")
print("="*80)

start_time = time.time()

try:
    result = start_saturation_learning(
        seed_url="https://en.wikipedia.org/wiki/Silicon",
        zone_name="Silicon_Quick_Test",
        zone_keywords=['silicon', 'element', 'semiconductor'],
        allowed_distance=0.6,
        saturation_threshold=0.75,
        max_urls=3  # Only 3 URLs for quick test
    )

    elapsed = time.time() - start_time

    print("\n" + "="*80)
    print("✅ TEST COMPLETE")
    print("="*80)
    print(f"Time: {elapsed:.1f} seconds")
    print(f"URLs Processed: {result['stats']['urls_processed']}")
    print(f"Phase Score: {result['stats']['phase_transition_score']:.3f}")
    print(f"Next Phase: {result.get('next_phase_query', 'None')}")

except Exception as e:
    elapsed = time.time() - start_time
    print(f"\n❌ TEST FAILED after {elapsed:.1f} seconds")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
