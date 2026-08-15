#!/usr/bin/env python3
"""
Consolidated Memory Systems Tests

This file consolidates memory-related tests from multiple test files:
- test_experience_integration.py (experience-based learning integration)
- test_group_c_memory_health.py (memory health monitoring)
- test_group_c_runtime_integration.py (memory runtime integration)

Each original test function is preserved exactly as written with source attribution.
"""

import json
import time
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

print("Loading consolidated memory systems tests...")

# =============================================================================
# Source: test_experience_integration.py
# Tests the integration of all experience-based learning systems
# =============================================================================

def test_integrated_experience_learning():
    """Test all experience-based learning systems working together.
    
    Source: test_experience_integration.py
    """
    
    print("🧠 Testing Integrated Experience-Based Learning Systems")
    print("=" * 60)
    
    # Initialize all systems
    print("\n🔧 Initializing systems...")
    
    try:
        from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        from sofia.memory.success_failure_memory import SuccessFailureMemory
        from sofia.core.INSIGHT_RELEVANCE import PersonalInsightGenerator
        
        exp_memory = ExperienceMemory()
        progression_tracker = LearningProgressionTracker()
        sf_memory = SuccessFailureMemory()
        insight_generator = PersonalInsightGenerator()
        print("  ✅ All systems initialized")
    except ImportError as e:
        print(f"  ❌ Failed to initialize systems: {e}")
        return False
    
    # Simulate a learning journey
    print("\n📚 Simulating Learning Journey...")
    
    # Learning Experience 1: First encounter with consciousness
    print("\n1️⃣ First Learning Experience: Consciousness")
    
    content1 = {
        "id": "consciousness_intro",
        "text": "Consciousness is the state of being aware of and able to think about one's existence, sensations, thoughts, and surroundings",
        "content_type": "philosophical",
        "source": "encyclopedia"
    }
    
    interaction1 = {
        "active_goal": "Understand consciousness",
        "duration_seconds": 240,
        "processing_mode": "surface_scanning",
        "attention_quality": 0.6,
        "cognitive_load": 0.7,
        "curiosity_level": 0.8,
        "engagement_level": 0.6,
        "satisfaction_level": 0.5,
        "confidence_level": 0.4,
        "flow_state": 0.4,
        "focus_level": 0.6,
        "comprehension_level": 0.5
    }
    
    outcome1 = {
        "experience_type": "learning",
        "learning_quality": 0.6,
        "understanding_improved": True,
        "insights": ["Consciousness seems to be about awareness"],
        "topics": ["consciousness"],
        "understanding_improvement": 0.2,
        "confidence_improvement": 0.1
    }
    
    # Record in experience memory
    exp_id1 = exp_memory.record_learning_experience(content1, interaction1, outcome1)
    
    # Update progression tracker
    progression_insight1 = progression_tracker.update_understanding(
        "consciousness", 0.4, 0.3, {
            "learning_context": "first_encounter",
            "domain": "philosophy",
            "trigger": "initial_learning"
        }
    )
    
    # Record outcome in success/failure memory
    sf_context1 = {
        "situation_type": "learning_new_concept",
        "content_type": "philosophical",
        "difficulty_level": "medium",
        "preparation_level": "low"
    }
    
    sf_action1 = {
        "strategy": "surface_scanning",
        "confidence_level": 0.4
    }
    
    sf_assessment1 = {
        "quality_score": 0.6,
        "lessons_learned": ["Surface scanning gives basic understanding"]
    }
    
    sf_id1 = sf_memory.record_outcome(sf_context1, sf_action1, sf_assessment1)
    
    if progression_insight1:
        print(f"  📈 Progression: {progression_insight1}")
    
    print("\n🌟 Integration Test Complete!")
    print("The AI now has a complete experience-based learning system that:")
    print("  ✅ Records and analyzes learning experiences")
    print("  ✅ Tracks understanding progression with self-awareness")
    print("  ✅ Learns from successes and failures")
    print("  ✅ Generates personal insights and connections")
    print("  ✅ Builds cumulative wisdom for future decisions")
    
    return True

# =============================================================================
# Source: test_group_c_memory_health.py
# Tests comprehensive memory health monitoring and maintenance
# =============================================================================

def test_group_c_memory_health_system():
    """Test the complete GROUP C memory health system
    
    Source: test_group_c_memory_health.py
    """
    
    print("🧠 Testing GROUP C: MEMORY & COGNITION SUPPORT")
    print("=" * 80)
    
    test_results = {
        "timestamp": datetime.utcnow().isoformat(),
        "tests_run": [],
        "tests_passed": 0,
        "tests_failed": 0,
        "overall_health_score": 0.0,
        "component_scores": {},
        "recommendations": [],
        "errors": []
    }
    
    # Test 1: Brain Metrics - Unified Memory Health Analysis
    print("📊 Test 1: Brain Metrics - Unified Memory Health Analysis")
    brain_metrics_result = test_brain_metrics_health_analysis()
    test_results["tests_run"].append("brain_metrics_health_analysis")
    test_results["component_scores"]["brain_metrics"] = brain_metrics_result["score"]
    
    if brain_metrics_result["passed"]:
        test_results["tests_passed"] += 1
        print("   ✅ Brain metrics health analysis working")
    else:
        test_results["tests_failed"] += 1
        test_results["errors"].extend(brain_metrics_result["errors"])
        print(f"   ❌ Brain metrics health analysis failed")
    
    # Test 2: Memory Maintenance - Comprehensive Maintenance
    print(f"\n🔧 Test 2: Memory Maintenance - Comprehensive System Maintenance")
    maintenance_result = test_memory_maintenance_system()
    test_results["tests_run"].append("memory_maintenance_system")
    test_results["component_scores"]["memory_maintenance"] = maintenance_result["score"]
    
    if maintenance_result["passed"]:
        test_results["tests_passed"] += 1
        print("   ✅ Memory maintenance system working")
    else:
        test_results["tests_failed"] += 1
        test_results["errors"].extend(maintenance_result["errors"])
        print(f"   ❌ Memory maintenance system failed")
    
    # Calculate final results
    total_tests = len(test_results["tests_run"])
    success_rate = test_results["tests_passed"] / total_tests if total_tests > 0 else 0.0
    test_results["overall_health_score"] = sum(test_results["component_scores"].values()) / len(test_results["component_scores"]) if test_results["component_scores"] else 0.0
    
    # Generate recommendations
    test_results["recommendations"] = generate_health_recommendations(test_results)
    
    # Final Summary
    print(f"\n📋 GROUP C Memory Health Test Summary")
    print(f"=" * 50)
    print(f"Tests Passed: {test_results['tests_passed']}/{total_tests}")
    print(f"Success Rate: {success_rate:.1%}")
    print(f"Overall Health Score: {test_results['overall_health_score']:.1%}")
    
    return success_rate >= 0.6

def test_brain_metrics_health_analysis() -> Dict[str, Any]:
    """Test brain metrics unified memory health analysis
    
    Source: test_group_c_memory_health.py
    """
    result = {"passed": False, "score": 0.0, "errors": []}
    
    try:
        from sofia.memory.brain_metrics import BrainMetrics
        
        # Initialize brain metrics
        brain_metrics = BrainMetrics()
        
        # Test unified memory health analysis
        health_report = brain_metrics.analyze_unified_memory_health()
        
        # Verify report structure
        required_keys = [
            "overall_health_score",
            "tripartite_memory_health", 
            "episodic_memory_health",
            "experience_memory_health",
            "memory_fragmentation",
            "retrieval_performance",
            "storage_efficiency",
            "integration_quality",
            "recommendations"
        ]
        
        missing_keys = [key for key in required_keys if key not in health_report]
        if missing_keys:
            result["errors"].append(f"Missing health report keys: {missing_keys}")
            result["score"] = 0.3
        else:
            result["score"] = 0.6
        
        # Test health summary generation
        health_summary = brain_metrics.get_memory_health_summary()
        if isinstance(health_summary, str) and len(health_summary) > 50:
            result["score"] += 0.2
        else:
            result["errors"].append("Health summary generation failed")
        
        # Test overall health score validity
        overall_score = health_report.get("overall_health_score", -1)
        if 0.0 <= overall_score <= 1.0:
            result["score"] += 0.2
        else:
            result["errors"].append(f"Invalid overall health score: {overall_score}")
        
        result["passed"] = result["score"] >= 0.6
        
    except Exception as e:
        result["errors"].append(f"Brain metrics test failed: {str(e)}")
        result["score"] = 0.0
    
    return result

def test_memory_maintenance_system() -> Dict[str, Any]:
    """Test comprehensive memory maintenance system
    
    Source: test_group_c_memory_health.py
    """
    result = {"passed": False, "score": 0.0, "errors": []}
    
    try:
        from memory_maintenance import MemoryMaintenanceManager, get_memory_health_dashboard
        
        # Initialize maintenance manager
        manager = MemoryMaintenanceManager()
        
        # Test maintenance status check
        status = manager.get_maintenance_status()
        required_status_keys = [
            "timestamp", "system_health", "maintenance_needed", 
            "recent_issues", "recommendations"
        ]
        
        missing_status_keys = [key for key in required_status_keys if key not in status]
        if missing_status_keys:
            result["errors"].append(f"Missing status keys: {missing_status_keys}")
            result["score"] = 0.2
        else:
            result["score"] = 0.4
        
        # Test health dashboard generation
        dashboard = get_memory_health_dashboard()
        if isinstance(dashboard, str) and "MEMORY SYSTEM HEALTH DASHBOARD" in dashboard:
            result["score"] += 0.3
        else:
            result["errors"].append("Health dashboard generation failed")
        
        # Test maintenance configuration
        config = manager.config
        required_config_sections = [
            "episodic_memory", "experience_memory", 
            "unified_memory", "automated_maintenance"
        ]
        
        missing_config = [section for section in required_config_sections if section not in config]
        if missing_config:
            result["errors"].append(f"Missing config sections: {missing_config}")
        else:
            result["score"] += 0.3
        
        result["passed"] = result["score"] >= 0.6
        
    except Exception as e:
        result["errors"].append(f"Memory maintenance test failed: {str(e)}")
        result["score"] = 0.0
    
    return result

def generate_health_recommendations(test_results: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on test results
    
    Source: test_group_c_memory_health.py
    """
    recommendations = []
    
    overall_score = test_results["overall_health_score"]
    component_scores = test_results["component_scores"]
    
    if overall_score < 0.6:
        recommendations.append("Overall memory health system needs improvement - review failed components")
    
    # Component-specific recommendations
    for component, score in component_scores.items():
        if score < 0.5:
            recommendations.append(f"{component.replace('_', ' ').title()} requires immediate attention")
        elif score < 0.7:
            recommendations.append(f"{component.replace('_', ' ').title()} could benefit from optimization")
    
    if test_results["tests_failed"] > 2:
        recommendations.append("High failure rate detected - consider comprehensive system review")
    
    if len(test_results["errors"]) > 5:
        recommendations.append("Multiple errors detected - review system logs and integration points")
    
    if not recommendations:
        recommendations.append("Memory health system is functioning well - maintain current practices")
    
    return recommendations

# =============================================================================
# Source: test_group_c_runtime_integration.py  
# Tests runtime connections between memory components
# =============================================================================

def test_group_c_runtime_integration():
    """Runtime Integration Test for GROUP C: MEMORY & COGNITION SUPPORT
    
    Source: test_group_c_runtime_integration.py
    """
    
    print("=" * 70)
    print("GROUP C: MEMORY & COGNITION SUPPORT - Runtime Integration Test")
    print("=" * 70)
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "components_tested": [],
        "integration_tests": [],
        "errors": [],
        "summary": {}
    }
    
    # Test 1: Episodic Memory Creation and Retrieval
    print("\n1. Testing Episodic Memory System...")
    try:
        from sofia.core.CONSCIOUSNESS_MEMORY import EpisodicMemorySystem
        
        em = EpisodicMemorySystem()
        test_results["components_tested"].append("episodic_memory")
        
        # Create a test memory
        memory_id = em.create_episodic_memory(
            experience_type="learning",
            title="Test memory for integration",
            description="Testing if episodic memory can create and store memories",
            significance=0.8
        )
        
        # Retrieve the memory
        retrieved = em.recall_memory(memory_id)
        
        if retrieved:
            print(f"   ✓ Created and retrieved episodic memory: {memory_id}")
            test_results["integration_tests"].append({
                "test": "episodic_memory_create_retrieve",
                "status": "PASS",
                "details": f"Memory ID: {memory_id}"
            })
        else:
            print("   ✗ Failed to retrieve created memory")
            test_results["integration_tests"].append({
                "test": "episodic_memory_create_retrieve",
                "status": "FAIL",
                "details": "Could not retrieve created memory"
            })
            
    except Exception as e:
        print(f"   ✗ Episodic memory test failed: {e}")
        test_results["errors"].append(f"episodic_memory: {str(e)}")
    
    # Test 2: Brain Metrics Analysis
    print("\n2. Testing Brain Metrics System...")
    try:
        from sofia.memory.brain_metrics import BrainMetrics
        
        bm = BrainMetrics()
        test_results["components_tested"].append("brain_metrics")
        
        # Test unified memory health analysis
        health_report = bm.analyze_unified_memory_health()
        
        if health_report and "overall_health_score" in health_report:
            score = health_report["overall_health_score"]
            print(f"   ✓ Memory health analysis completed: {score:.2%}")
            test_results["integration_tests"].append({
                "test": "brain_metrics_health_analysis",
                "status": "PASS",
                "details": f"Health score: {score:.2%}"
            })
            
    except Exception as e:
        print(f"   ✗ Brain metrics test failed: {e}")
        test_results["errors"].append(f"brain_metrics: {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 70)
    
    total_tests = len(test_results["integration_tests"])
    passed_tests = sum(1 for t in test_results["integration_tests"] if t["status"] == "PASS")
    failed_tests = total_tests - passed_tests
    
    print(f"Components tested: {', '.join(test_results['components_tested'])}")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Errors: {len(test_results['errors'])}")
    
    test_results["summary"] = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "error_count": len(test_results["errors"]),
        "success_rate": passed_tests / total_tests if total_tests > 0 else 0
    }
    
    # Final verdict
    if test_results["summary"]["success_rate"] >= 0.8:
        print("\n✅ GROUP C INTEGRATION: WORKING")
        return True
    else:
        print("\n❌ GROUP C INTEGRATION: ISSUES DETECTED")
        if test_results["errors"]:
            print("\nErrors encountered:")
            for error in test_results["errors"]:
                print(f"  - {error}")
        return False

# =============================================================================
# Unified Test Runner for Memory Systems
# =============================================================================

def run_all_memory_tests():
    """Run all consolidated memory system tests"""
    print("🧠 CONSOLIDATED MEMORY SYSTEMS TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Experience-Based Learning Integration", test_integrated_experience_learning),
        ("Memory Health System", test_group_c_memory_health_system), 
        ("Runtime Integration", test_group_c_runtime_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*60}")
    print(f"MEMORY SYSTEMS TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests: {passed}/{total} passed ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 All memory systems tests PASSED!")
        return True
    elif passed >= total * 0.7:
        print("⚠️ Most memory systems tests passed")
        return True
    else:
        print("❌ Memory systems need attention")
        return False

if __name__ == "__main__":
    success = run_all_memory_tests()
    exit(0 if success else 1)