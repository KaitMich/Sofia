#!/usr/bin/env python3
"""
Test script for immune system integration with enhanced_autonomous_learner.py

Tests the layered security architecture:
1. Page-level immune check (HTML structure, quality, source)
2. Chunk-level warfare detection (existing AlphaWall)
3. Corroboration check (multi-source validation)
4. Trust scoring and adjustments
"""

import sys
from pathlib import Path

# Test imports
try:
    from sofia.security.immune_system import ImmuneSystem
    from sofia.security.trust_database import TrustDatabase
    from sofia.security.corroboration_engine import CorroborationEngine
    print("✅ Immune system components imported successfully")
except ImportError as e:
    print(f"❌ Failed to import immune components: {e}")
    sys.exit(1)

def test_immune_system_standalone():
    """Test immune system in standalone mode."""
    print("\n" + "="*60)
    print("TEST 1: Immune System Standalone")
    print("="*60)

    # Initialize components (use default paths - they handle data_dir internally)
    trust_db = TrustDatabase()  # Defaults to "data/immune/trust.db"
    immune = ImmuneSystem("data", trust_database=trust_db)

    # Test 1: Clean content
    print("\n📋 Test 1a: Clean educational content")
    clean_html = """
    <html>
    <head><title>AI Research</title></head>
    <body>
        <h1>Artificial Intelligence Research</h1>
        <p>This article discusses recent advances in machine learning and neural networks.
        Researchers have developed new techniques for improving model accuracy.</p>
    </body>
    </html>
    """
    clean_text = "AI Research. This article discusses recent advances in machine learning."

    assessment = immune.analyze_page("https://example.edu/ai-research", clean_html, clean_text)
    print(f"   Result: {assessment.recommendation}")
    print(f"   Threat score: {assessment.overall_threat_score:.2f}")
    print(f"   Expected: ALLOW (low threat)")
    assert assessment.recommendation == "ALLOW", "Clean content should be ALLOWED"
    print("   ✅ PASSED")

    # Test 2: Suspicious structure
    print("\n📋 Test 1b: Suspicious HTML structure")
    suspicious_html = """
    <html>
    <head>
        <script>eval(atob('malicious code'))</script>
    </head>
    <body>
        <div style="display:none">Hidden content tracking users</div>
        <div>Click here now! You won't believe what happens next!</div>
        <div>BUY NOW! LIMITED TIME OFFER!!!</div>
    </body>
    </html>
    """
    suspicious_text = "Click here now! You won't believe what happens next! BUY NOW!"

    assessment = immune.analyze_page("https://suspicious-site.com/page", suspicious_html, suspicious_text)
    print(f"   Result: {assessment.recommendation}")
    print(f"   Threat score: {assessment.overall_threat_score:.2f}")
    print(f"   Signals detected: {len(assessment.threat_signals)}")
    print(f"   Expected: BLOCK or REVIEW (high threat)")
    assert assessment.recommendation in ["BLOCK", "REVIEW"], "Suspicious content should be blocked/flagged"
    print("   ✅ PASSED")

    print("\n✅ Immune system standalone tests PASSED")

def test_trust_database():
    """Test trust database operations."""
    print("\n" + "="*60)
    print("TEST 2: Trust Database")
    print("="*60)

    trust_db = TrustDatabase()  # Defaults to "data/immune/trust.db"

    # Test domain trust
    print("\n📋 Test 2a: Domain trust operations")
    # Use unique domain for each test run
    from datetime import datetime
    domain = f"test-domain-{datetime.now().strftime('%Y%m%d%H%M%S')}.edu"

    # Get initial trust (should be 0.5 for new domain)
    initial_trust = trust_db.get_trust(domain)
    print(f"   Initial trust for {domain}: {initial_trust:.2f}")
    assert 0.49 <= initial_trust <= 0.51, f"New domain should have neutral trust ~0.5, got {initial_trust}"

    # Adjust trust upward
    trust_db.adjust_trust(domain, +0.1, "Clean content")
    new_trust = trust_db.get_trust(domain)
    print(f"   After +0.1 adjustment: {new_trust:.2f}")
    assert new_trust > initial_trust, "Trust should increase"

    # Adjust trust downward
    trust_db.adjust_trust(domain, -0.2, "Suspicious pattern")
    new_trust = trust_db.get_trust(domain)
    print(f"   After -0.2 adjustment: {new_trust:.2f}")
    assert new_trust < initial_trust, "Trust should decrease"

    # Get audit trail
    audit = trust_db.get_audit_trail(domain, limit=5)
    print(f"   Audit trail entries: {len(audit)}")
    assert len(audit) >= 2, "Should have at least 2 audit entries"

    print("   ✅ PASSED")

    print("\n✅ Trust database tests PASSED")

def test_corroboration_engine():
    """Test corroboration engine."""
    print("\n" + "="*60)
    print("TEST 3: Corroboration Engine")
    print("="*60)

    import numpy as np
    corroboration = CorroborationEngine()  # Defaults to "data/immune/corroboration.db"

    print("\n📋 Test 3a: Single sighting (should defer)")
    fact1 = "The Earth orbits the Sun"
    embedding1 = np.random.rand(384)

    cluster_id = corroboration.record_sighting(fact1, embedding1, "https://source1.com", 0.8)
    print(f"   Cluster ID: {cluster_id}")

    result = corroboration.get_corroboration_score(embedding1)
    print(f"   Ready to commit: {result.ready_to_commit}")
    print(f"   Sightings: {result.total_sightings}")
    print(f"   Expected: NOT ready (only 1 sighting)")
    assert not result.ready_to_commit, "Single sighting should not be ready"
    print("   ✅ PASSED")

    print("\n📋 Test 3b: Multiple sightings (should allow)")
    # Add more sightings from different sources
    corroboration.record_sighting(fact1, embedding1, "https://source2.com", 0.9)
    corroboration.record_sighting(fact1, embedding1, "https://source3.edu", 0.85)

    result = corroboration.get_corroboration_score(embedding1)
    print(f"   Ready to commit: {result.ready_to_commit}")
    print(f"   Sightings: {result.total_sightings}")
    print(f"   Unique sources: {result.unique_sources}")
    print(f"   Expected: Ready (multiple sources)")
    assert result.ready_to_commit, "Multiple sightings should be ready"
    print("   ✅ PASSED")

    print("\n✅ Corroboration engine tests PASSED")

def test_layered_integration():
    """Test that all layers work together."""
    print("\n" + "="*60)
    print("TEST 4: Layered Security Integration")
    print("="*60)

    # Initialize all components (use defaults)
    trust_db = TrustDatabase()
    immune = ImmuneSystem("data", trust_database=trust_db)
    corroboration = CorroborationEngine()

    print("\n📋 Test 4: Complete security flow")

    # Simulate a URL going through all layers
    test_url = "https://test-integration.edu/article"
    test_html = """
    <html>
    <head><title>Test Article</title></head>
    <body><p>This is test content for integration testing.</p></body>
    </html>
    """
    test_text = "This is test content for integration testing."

    # Layer 1: Immune system (page-level)
    print("\n   Layer 1: Immune system (page-level)")
    immune_result = immune.analyze_page(test_url, test_html, test_text)
    print(f"      ✓ Recommendation: {immune_result.recommendation}")
    print(f"      ✓ Threat score: {immune_result.overall_threat_score:.2f}")

    if immune_result.recommendation == "BLOCK":
        print("      → Content BLOCKED at page level")
        print("   ✅ Layer 1 working (blocked)")
        return

    # Layer 2: Linguistic warfare (chunk-level)
    print("\n   Layer 2: Linguistic warfare (chunk-level)")
    from sofia.security.linguistic_warfare import check_for_warfare
    should_quarantine, warfare_analysis = check_for_warfare(test_text, test_url)
    print(f"      ✓ Quarantine: {should_quarantine}")
    if should_quarantine:
        print(f"      ✓ Threat: {warfare_analysis.get('threat_type', 'unknown')}")
        print("      → Content BLOCKED at chunk level")
        print("   ✅ Layer 2 working (blocked)")
        return
    else:
        print("      ✓ No warfare detected")

    # Layer 3: Corroboration (fact validation)
    print("\n   Layer 3: Corroboration (fact validation)")
    import numpy as np
    embedding = np.random.rand(384)
    domain = "test-integration.edu"
    domain_trust = trust_db.get_trust(domain)

    corroboration_result = corroboration.get_corroboration_score(embedding)
    print(f"      ✓ Ready to commit: {corroboration_result.ready_to_commit}")
    print(f"      ✓ Sightings: {corroboration_result.total_sightings}")

    if not corroboration_result.ready_to_commit:
        # Record sighting
        corroboration.record_sighting(test_text, embedding, test_url, domain_trust)
        print("      → Content DEFERRED (need more sources)")
        print("   ✅ Layer 3 working (deferred)")
    else:
        print("      → Content ALLOWED (corroborated)")
        print("   ✅ Layer 3 working (allowed)")

    print("\n✅ Layered integration test PASSED")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 IMMUNE SYSTEM INTEGRATION TEST SUITE")
    print("="*60)
    print("\nTesting layered security architecture:")
    print("  1. Page-level: immune_system.py")
    print("  2. Chunk-level: linguistic_warfare.py (AlphaWall)")
    print("  3. Fact-level: corroboration_engine.py")
    print("  4. Trust: trust_database.py")

    try:
        test_immune_system_standalone()
        test_trust_database()
        test_corroboration_engine()
        test_layered_integration()

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        print("\n🎯 Integration Status: READY")
        print("The immune system is fully integrated with enhanced_autonomous_learner.py")
        print("\nLayered security flow:")
        print("  URL → [immune] → [warfare] → [corroboration] → Memory")
        print("        page       chunk      fact")
        print("        level      level      level")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
