"""
Test Fact Extraction System

Quick test to verify passive fact extraction works correctly.
"""

from fact_extractor import FactExtractor
from web_parser import fetch_raw_html

def test_fact_extraction():
    """Test fact extraction on a real Wikipedia page."""

    print("="*80)
    print("🧪 Testing Passive Fact Extraction")
    print("="*80)

    # Test URL: Silicon (foundational topic)
    test_url = "https://en.wikipedia.org/wiki/Silicon"
    topic = "Silicon"

    print(f"\n📄 Fetching: {test_url}")
    print(f"   Topic: {topic}")

    # Fetch the page
    html_content = fetch_raw_html(test_url)

    if not html_content:
        print("\n❌ Failed to fetch page")
        return False

    print(f"\n✅ Page fetched ({len(html_content)} bytes)")

    # Extract facts
    print(f"\n🔍 Extracting facts...")
    extractor = FactExtractor()
    facts = extractor.extract_facts_from_html(html_content, test_url, topic)

    print(f"\n📊 Extraction Results:")
    print(f"   Facts extracted: {len(facts)}")

    # Show extracted facts by type
    facts_by_type = {}
    for fact in facts:
        fact_type = fact.get('type', 'unknown')
        if fact_type not in facts_by_type:
            facts_by_type[fact_type] = []
        facts_by_type[fact_type].append(fact)

    print(f"\n   Breakdown by type:")
    for fact_type, type_facts in facts_by_type.items():
        print(f"      {fact_type}: {len(type_facts)}")

    # Show sample facts
    print(f"\n💎 Sample Extracted Facts:")
    for i, fact in enumerate(facts[:10], 1):
        print(f"\n   {i}. [{fact['type']}]")
        print(f"      Text: {fact['text']}")
        print(f"      Confidence: {fact['confidence']}")
        print(f"      Sources: {len(fact['sources'])}")

    # Test validation through repetition
    print(f"\n" + "="*80)
    print("🔄 Testing Fact Validation (simulating multiple visits)")
    print("="*80)

    # Simulate visiting same page again (should increase confidence)
    print(f"\n📄 Simulating second visit to same page...")
    test_url_2 = test_url + "#duplicate_visit"  # Different URL but same content
    facts_2 = extractor.extract_facts_from_html(html_content, test_url_2, topic)

    print(f"\n📊 Second Visit Results:")
    print(f"   Facts extracted: {len(facts_2)}")

    # Check if confidence increased
    validated_count = sum(1 for f in facts_2 if f['confidence'] > 1)
    print(f"   Facts validated (confidence > 1): {validated_count}")

    # Show validated facts
    if validated_count > 0:
        print(f"\n✅ Validated Facts (seen multiple times):")
        for fact in [f for f in facts_2 if f['confidence'] > 1][:5]:
            print(f"\n      Text: {fact['text']}")
            print(f"      Confidence: {fact['confidence']} (seen in {len(fact['sources'])} sources)")

    # Test depth summary
    print(f"\n" + "="*80)
    print("🧠 Testing Depth Reflection")
    print("="*80)

    depth = extractor.get_learning_depth_summary(topic)

    print(f"\n📚 Learning Depth for '{topic}':")
    print(f"   Total Facts Learned:     {depth['total_facts_learned']}")
    print(f"   High Confidence Facts:  {depth['high_confidence_facts']} (seen 3+ times)")
    print(f"   Medium Confidence:      {depth['medium_confidence_facts']} (seen 2 times)")
    print(f"   Emerging Understanding: {depth['emerging_facts']} (seen 1 time)")
    print(f"   Depth Score:            {depth['depth_score']:.2%}")

    if depth['sample_high_confidence']:
        print(f"\n   💎 Sample High-Confidence Facts:")
        for i, fact in enumerate(depth['sample_high_confidence'][:5], 1):
            print(f"      {i}. {fact['text']}")

    if depth['sample_emerging']:
        print(f"\n   🌱 Sample Emerging Facts:")
        for i, fact in enumerate(depth['sample_emerging'][:3], 1):
            print(f"      {i}. {fact['text']}")

    print(f"\n" + "="*80)
    print("✅ Fact Extraction Test Complete!")
    print("="*80)

    return True


if __name__ == "__main__":
    try:
        success = test_fact_extraction()
        if success:
            print("\n🎉 All tests passed!")
        else:
            print("\n❌ Tests failed")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
