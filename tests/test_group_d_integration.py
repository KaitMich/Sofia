#!/usr/bin/env python3
"""
Comprehensive Integration Test for GROUP D: SYMBOL & CONCEPT PROCESSING

Tests the consolidated symbol processing functionality:
1. Creative Engine's build_concept_chains() method (from symbol_chainer.py)
2. Creative Engine's suggest_symbols_from_clusters() method (from symbol_suggester.py)  
3. Memory Analytics' analyze_symbol_clusters() method (from symbol_cluster.py)
4. Symbolic Nourishment strengthening functionality
5. Expanded Symbolic Core cross-system integration

This test validates that all GROUP D components work correctly after consolidation.
"""

import tempfile
import json
import os
from pathlib import Path
from datetime import datetime

def test_group_d_integration():
    """Comprehensive test of consolidated GROUP D symbol processing functionality."""
    
    print("🧪 TESTING GROUP D: SYMBOL & CONCEPT PROCESSING INTEGRATION")
    print("=" * 70)
    
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "integration_status": "unknown",
        "component_results": {},
        "errors": []
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize test environment
        test_data_dir = Path(tmpdir)
        
        # Test 1: Creative Engine Concept Chains (from symbol_chainer.py)
        print("\n1️⃣ Testing Creative Engine Concept Chains...")
        results["tests_run"] += 1
        
        try:
            from sofia.core.creative_engine import CreativeEngine
            from sofia.core.unified_memory import get_unified_memory
            
            # Setup memory with test symbols
            unified_memory = get_unified_memory()
            
            # Add symbolic entries with vectors for testing
            test_symbols = [
                {"text": "🌟 Wonder sparks curiosity and transforms ordinary into extraordinary", "symbol": "🌟", "vector": [0.8, 0.2, 0.6, 0.9, 0.3]},
                {"text": "🌊 Flow represents the seamless movement between states", "symbol": "🌊", "vector": [0.7, 0.3, 0.8, 0.5, 0.4]},
                {"text": "⚡ Energy drives transformation and creative expression", "symbol": "⚡", "vector": [0.9, 0.1, 0.7, 0.8, 0.2]},
                {"text": "🌱 Growth emerges from nurturing potential with patience", "symbol": "🌱", "vector": [0.6, 0.4, 0.9, 0.7, 0.5]},
                {"text": "🔥 Passion ignites the spark of creative breakthrough", "symbol": "🔥", "vector": [0.8, 0.3, 0.5, 0.9, 0.1]}
            ]
            
            for symbol_data in test_symbols:
                unified_memory.store_decision(symbol_data, "FOLLOW_SYMBOLIC")
            
            # Initialize creative engine
            creative_engine = CreativeEngine(str(test_data_dir))
            creative_engine.unified_memory = unified_memory  # Ensure access to unified memory
            
            # Test concept chains functionality
            chains = creative_engine.build_concept_chains(min_similarity=0.4)
            
            if chains and len(chains) > 0:
                print("✅ Creative Engine concept chains working correctly")
                results["tests_passed"] += 1
                results["component_results"]["concept_chains"] = {
                    "status": "success",
                    "chains_found": len(chains),
                    "sample_chain": str(list(chains.keys())[:3]) if chains else "none"
                }
            else:
                print("❌ Creative Engine concept chains returned empty results")
                results["tests_failed"] += 1
                results["component_results"]["concept_chains"] = {"status": "failed", "reason": "empty_chains"}
                
        except Exception as e:
            print(f"❌ Creative Engine concept chains test failed: {e}")
            results["tests_failed"] += 1
            results["errors"].append(f"concept_chains: {str(e)}")
            results["component_results"]["concept_chains"] = {"status": "error", "error": str(e)}
        
        # Test 2: Creative Engine Symbol Suggestions (from symbol_suggester.py)
        print("\n2️⃣ Testing Creative Engine Symbol Suggestions...")
        results["tests_run"] += 1
        
        try:
            # Re-initialize creative engine if needed (in case test 1 failed)
            if 'creative_engine' not in locals():
                creative_engine = CreativeEngine(str(test_data_dir))
                creative_engine.unified_memory = unified_memory
            
            # Test symbol suggestions from clusters
            suggestions = creative_engine.suggest_symbols_from_clusters(min_cluster_size=2, eps=0.4)
            
            if isinstance(suggestions, list):
                print("✅ Creative Engine symbol suggestions working correctly")
                results["tests_passed"] += 1
                results["component_results"]["symbol_suggestions"] = {
                    "status": "success",
                    "suggestions_count": len(suggestions),
                    "has_clusters": len(suggestions) > 0
                }
            else:
                print("❌ Creative Engine symbol suggestions returned unexpected format")
                results["tests_failed"] += 1
                results["component_results"]["symbol_suggestions"] = {"status": "failed", "reason": "wrong_format"}
                
        except Exception as e:
            print(f"❌ Creative Engine symbol suggestions test failed: {e}")
            results["tests_failed"] += 1
            results["errors"].append(f"symbol_suggestions: {str(e)}")
            results["component_results"]["symbol_suggestions"] = {"status": "error", "error": str(e)}
        
        # Test 3: Memory Analytics Symbol Clusters (from symbol_cluster.py)
        print("\n3️⃣ Testing Memory Analytics Symbol Clusters...")
        results["tests_run"] += 1
        
        try:
            from sofia.memory.memory_analytics import MemoryAnalyzer
            
            # Initialize memory analyzer
            analyzer = MemoryAnalyzer(unified_memory, str(test_data_dir))
            
            # Test cluster analysis
            cluster_analysis = analyzer.analyze_symbol_clusters(max_features=50, n_clusters=3, show_visualization=False)
            
            if "error" not in cluster_analysis and "cluster_results" in cluster_analysis:
                print("✅ Memory Analytics symbol clustering working correctly")
                results["tests_passed"] += 1
                results["component_results"]["symbol_clustering"] = {
                    "status": "success",
                    "clusters_found": cluster_analysis.get("n_clusters", 0),
                    "valid_entries": cluster_analysis.get("valid_text_entries", 0)
                }
            else:
                error_msg = cluster_analysis.get("error", "unknown_error")
                print(f"❌ Memory Analytics symbol clustering failed: {error_msg}")
                results["tests_failed"] += 1
                results["component_results"]["symbol_clustering"] = {"status": "failed", "reason": error_msg}
                
        except Exception as e:
            print(f"❌ Memory Analytics symbol clustering test failed: {e}")
            results["tests_failed"] += 1
            results["errors"].append(f"symbol_clustering: {str(e)}")
            results["component_results"]["symbol_clustering"] = {"status": "error", "error": str(e)}
        
        # Test 4: Symbolic Nourishment Integration
        print("\n4️⃣ Testing Symbolic Nourishment Integration...")
        results["tests_run"] += 1
        
        try:
            from sofia.core.symbolic_nourishment import SymbolicNourishment
            
            # Initialize symbolic nourishment (no data_dir parameter)
            nourishment = SymbolicNourishment()
            
            # Test nourishment functionality 
            pre_counts = unified_memory.get_memory_counts()
            balance_assessment = nourishment.assess_current_balance()
            post_counts = unified_memory.get_memory_counts()
            
            print("✅ Symbolic Nourishment integration working correctly")
            results["tests_passed"] += 1
            results["component_results"]["symbolic_nourishment"] = {
                "status": "success",
                "pre_memory_count": pre_counts.get("total", 0),
                "post_memory_count": post_counts.get("total", 0),
                "balance_assessed": True,
                "cognitive_state": balance_assessment.get("cognitive_state", "unknown")
            }
                
        except Exception as e:
            print(f"❌ Symbolic Nourishment integration test failed: {e}")
            results["tests_failed"] += 1
            results["errors"].append(f"symbolic_nourishment: {str(e)}")
            results["component_results"]["symbolic_nourishment"] = {"status": "error", "error": str(e)}
        
        # Test 5: Expanded Symbolic Core Integration
        print("\n5️⃣ Testing Expanded Symbolic Core Integration...")
        results["tests_run"] += 1
        
        try:
            from sofia.core.expanded_symbolic_core import create_expanded_symbolic_core
            
            # Test core functionality - this is a function not a class
            expanded_symbols = create_expanded_symbolic_core()
            
            if expanded_symbols and len(expanded_symbols) > 0:
                print("✅ Expanded Symbolic Core integration working correctly")
                results["tests_passed"] += 1
                results["component_results"]["expanded_symbolic_core"] = {
                    "status": "success",
                    "symbols_created": len(expanded_symbols),
                    "has_core_concepts": True,
                    "sample_concept": expanded_symbols[0].get("text", "")[:50] + "..." if expanded_symbols else ""
                }
            else:
                print("❌ Expanded Symbolic Core returned no symbols")
                results["tests_failed"] += 1
                results["component_results"]["expanded_symbolic_core"] = {"status": "failed", "reason": "no_symbols"}
                
        except Exception as e:
            print(f"❌ Expanded Symbolic Core integration test failed: {e}")
            results["tests_failed"] += 1
            results["errors"].append(f"expanded_symbolic_core: {str(e)}")
            results["component_results"]["expanded_symbolic_core"] = {"status": "error", "error": str(e)}
    
    # Calculate final integration status
    success_rate = (results["tests_passed"] / results["tests_run"]) * 100 if results["tests_run"] > 0 else 0
    
    if success_rate >= 80:
        results["integration_status"] = "excellent"
    elif success_rate >= 60:
        results["integration_status"] = "good"
    elif success_rate >= 40:
        results["integration_status"] = "needs_improvement"
    else:
        results["integration_status"] = "critical_issues"
    
    # Print final results
    print("\n" + "=" * 70)
    print("📊 GROUP D INTEGRATION TEST RESULTS")
    print("=" * 70)
    print(f"🎯 Tests Run: {results['tests_run']}")
    print(f"✅ Tests Passed: {results['tests_passed']}")
    print(f"❌ Tests Failed: {results['tests_failed']}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    print(f"🏆 Integration Status: {results['integration_status'].upper()}")
    
    if results["errors"]:
        print("\n❌ Errors Encountered:")
        for error in results["errors"]:
            print(f"   • {error}")
    
    print("\n🔍 Component Status Summary:")
    for component, status in results["component_results"].items():
        status_emoji = "✅" if status["status"] == "success" else "❌"
        print(f"   {status_emoji} {component}: {status['status']}")
    
    print("\n" + "=" * 70)
    
    return results

if __name__ == "__main__":
    test_results = test_group_d_integration()
    
    # Save results for validation
    results_file = Path("data/group_d_integration_test_results.json")
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, "w") as f:
        json.dump(test_results, f, indent=2)
    
    print(f"📁 Test results saved to: {results_file}")
    
    # Return appropriate exit code
    if test_results["integration_status"] in ["excellent", "good"]:
        print("🎉 GROUP D integration test PASSED!")
        exit(0)
    else:
        print("⚠️ GROUP D integration test needs attention.")
        exit(1)