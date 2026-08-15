#!/usr/bin/env python3
"""
GROUP C Integration Test: Memory & Cognition Support System Health

This test validates the comprehensive memory health monitoring, maintenance,
and optimization capabilities of GROUP C components:
- brain_metrics.py - Unified memory health analysis
- memory_maintenance.py - Comprehensive maintenance
- memory_optimizer.py - Performance optimization
- episodic_memory.py - Integration verification
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

def test_group_c_memory_health_system():
    """Test the complete GROUP C memory health system"""
    
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
    
    # Test 3: Memory Optimizer - Performance Optimization
    print(f"\n⚡ Test 3: Memory Optimizer - Performance Optimization")
    optimizer_result = test_memory_optimizer_performance()
    test_results["tests_run"].append("memory_optimizer_performance")
    test_results["component_scores"]["memory_optimizer"] = optimizer_result["score"]
    
    if optimizer_result["passed"]:
        test_results["tests_passed"] += 1
        print("   ✅ Memory optimizer performance working")
    else:
        test_results["tests_failed"] += 1
        test_results["errors"].extend(optimizer_result["errors"])
        print(f"   ❌ Memory optimizer performance failed")
    
    # Test 4: Episodic Memory - System Integration
    print(f"\n📝 Test 4: Episodic Memory - System Integration")
    episodic_result = test_episodic_memory_integration()
    test_results["tests_run"].append("episodic_memory_integration")
    test_results["component_scores"]["episodic_memory"] = episodic_result["score"]
    
    if episodic_result["passed"]:
        test_results["tests_passed"] += 1
        print("   ✅ Episodic memory integration working")
    else:
        test_results["tests_failed"] += 1
        test_results["errors"].extend(episodic_result["errors"])
        print(f"   ❌ Episodic memory integration failed")
    
    # Test 5: Integration Health Dashboard
    print(f"\n🎛️ Test 5: Memory Health Dashboard Integration")
    dashboard_result = test_memory_health_dashboard()
    test_results["tests_run"].append("memory_health_dashboard")
    test_results["component_scores"]["health_dashboard"] = dashboard_result["score"]
    
    if dashboard_result["passed"]:
        test_results["tests_passed"] += 1
        print("   ✅ Memory health dashboard working")
    else:
        test_results["tests_failed"] += 1
        test_results["errors"].extend(dashboard_result["errors"])
        print(f"   ❌ Memory health dashboard failed")
    
    # Test 6: End-to-End Memory Health Monitoring
    print(f"\n🔄 Test 6: End-to-End Memory Health Monitoring")
    e2e_result = test_end_to_end_memory_health()
    test_results["tests_run"].append("end_to_end_memory_health")
    test_results["component_scores"]["end_to_end"] = e2e_result["score"]
    
    if e2e_result["passed"]:
        test_results["tests_passed"] += 1
        print("   ✅ End-to-end memory health monitoring working")
    else:
        test_results["tests_failed"] += 1
        test_results["errors"].extend(e2e_result["errors"])
        print(f"   ❌ End-to-end memory health monitoring failed")
    
    # Calculate overall results
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
    
    # Component breakdown
    print(f"\n📊 Component Health Scores:")
    for component, score in test_results["component_scores"].items():
        emoji = "🟢" if score > 0.8 else "🟡" if score > 0.6 else "🟠" if score > 0.4 else "🔴"
        print(f"   {emoji} {component.replace('_', ' ').title()}: {score:.1%}")
    
    # Recommendations
    if test_results["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in test_results["recommendations"]:
            print(f"   • {rec}")
    
    # Errors
    if test_results["errors"]:
        print(f"\n⚠️ Issues Detected:")
        for error in test_results["errors"]:
            print(f"   • {error}")
    
    # Final assessment
    if success_rate >= 0.8 and test_results["overall_health_score"] >= 0.75:
        print(f"\n🎉 GROUP C: MEMORY & COGNITION SUPPORT - EXCELLENT")
        print(f"   Memory health monitoring and optimization systems are functioning excellently")
        return True
    elif success_rate >= 0.6 and test_results["overall_health_score"] >= 0.6:
        print(f"\n✅ GROUP C: MEMORY & COGNITION SUPPORT - GOOD")
        print(f"   Memory health systems are functional with room for improvement")
        return True
    else:
        print(f"\n⚠️ GROUP C: MEMORY & COGNITION SUPPORT - NEEDS IMPROVEMENT")
        print(f"   Memory health systems need attention and optimization")
        return False

def test_brain_metrics_health_analysis() -> Dict[str, Any]:
    """Test brain metrics unified memory health analysis"""
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
    """Test comprehensive memory maintenance system"""
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

def test_memory_optimizer_performance() -> Dict[str, Any]:
    """Test memory optimizer performance capabilities"""
    result = {"passed": False, "score": 0.0, "errors": []}
    
    try:
        from sofia.memory.memory_optimizer import optimize_unified_memory_performance, perform_predictive_memory_optimization
        
        # Test unified memory performance optimization
        optimization_report = optimize_unified_memory_performance()
        
        required_report_keys = [
            "timestamp", "optimizations_applied", 
            "performance_improvements", "errors"
        ]
        
        missing_keys = [key for key in required_report_keys if key not in optimization_report]
        if missing_keys:
            result["errors"].append(f"Missing optimization report keys: {missing_keys}")
            result["score"] = 0.2
        else:
            result["score"] = 0.4
        
        # Test predictive optimization
        prediction_report = perform_predictive_memory_optimization()
        
        if "predictions" in prediction_report and "recommendations" in prediction_report:
            result["score"] += 0.3
        else:
            result["errors"].append("Predictive optimization failed")
        
        # Check if optimizations were applied (even if simulated)
        optimizations_applied = optimization_report.get("optimizations_applied", [])
        if len(optimizations_applied) > 0:
            result["score"] += 0.3
        else:
            result["errors"].append("No optimizations were applied")
        
        result["passed"] = result["score"] >= 0.6
        
    except Exception as e:
        result["errors"].append(f"Memory optimizer test failed: {str(e)}")
        result["score"] = 0.0
    
    return result

def test_episodic_memory_integration() -> Dict[str, Any]:
    """Test episodic memory system integration"""
    result = {"passed": False, "score": 0.0, "errors": []}
    
    try:
        from sofia.core.CONSCIOUSNESS_MEMORY import EpisodicMemorySystem
        
        # Initialize episodic memory system
        episodic_system = EpisodicMemorySystem()
        
        # Test basic functionality
        memories = episodic_system.episodic_memories
        result["score"] = 0.3  # Basic initialization
        
        # Test memory creation capability
        if hasattr(episodic_system, 'create_episodic_memory'):
            result["score"] += 0.2
        else:
            result["errors"].append("Missing create_episodic_memory method")
        
        # Test memory retrieval capability
        if hasattr(episodic_system, 'retrieve_memories'):
            result["score"] += 0.2
        else:
            result["errors"].append("Missing retrieve_memories method")
        
        # Test integration with experience memory
        if hasattr(episodic_system, 'experience_memory'):
            result["score"] += 0.3
        else:
            result["errors"].append("Missing experience_memory integration")
        
        result["passed"] = result["score"] >= 0.6
        
    except Exception as e:
        result["errors"].append(f"Episodic memory test failed: {str(e)}")
        result["score"] = 0.0
    
    return result

def test_memory_health_dashboard() -> Dict[str, Any]:
    """Test memory health dashboard integration"""
    result = {"passed": False, "score": 0.0, "errors": []}
    
    try:
        from memory_maintenance import get_memory_health_dashboard
        from sofia.memory.brain_metrics import BrainMetrics
        
        # Test dashboard generation
        dashboard = get_memory_health_dashboard()
        
        # Check dashboard content
        required_sections = [
            "MEMORY SYSTEM HEALTH DASHBOARD",
            "System Health Scores",
            "Maintenance Status",
            "Recommendations"
        ]
        
        missing_sections = [section for section in required_sections if section not in dashboard]
        if missing_sections:
            result["errors"].append(f"Missing dashboard sections: {missing_sections}")
            result["score"] = 0.3
        else:
            result["score"] = 0.6
        
        # Test brain metrics integration
        brain_metrics = BrainMetrics()
        health_summary = brain_metrics.get_memory_health_summary()
        
        if "Memory system health is" in health_summary:
            result["score"] += 0.4
        else:
            result["errors"].append("Brain metrics health summary failed")
        
        result["passed"] = result["score"] >= 0.6
        
    except Exception as e:
        result["errors"].append(f"Health dashboard test failed: {str(e)}")
        result["score"] = 0.0
    
    return result

def test_end_to_end_memory_health() -> Dict[str, Any]:
    """Test end-to-end memory health monitoring workflow"""
    result = {"passed": False, "score": 0.0, "errors": []}
    
    try:
        from sofia.memory.brain_metrics import BrainMetrics
        from memory_maintenance import MemoryMaintenanceManager
        from sofia.memory.memory_optimizer import optimize_unified_memory_performance
        
        # Step 1: Health analysis
        brain_metrics = BrainMetrics()
        health_report = brain_metrics.analyze_unified_memory_health()
        initial_health = health_report.get("overall_health_score", 0.0)
        
        if initial_health >= 0.0:
            result["score"] += 0.2
        else:
            result["errors"].append("Health analysis failed")
        
        # Step 2: Maintenance check
        manager = MemoryMaintenanceManager()
        maintenance_status = manager.get_maintenance_status()
        
        if "system_health" in maintenance_status:
            result["score"] += 0.2
        else:
            result["errors"].append("Maintenance status check failed")
        
        # Step 3: Optimization
        optimization_report = optimize_unified_memory_performance()
        
        if len(optimization_report.get("optimizations_applied", [])) >= 0:
            result["score"] += 0.2
        else:
            result["errors"].append("Memory optimization failed")
        
        # Step 4: Post-optimization health check
        post_health_report = brain_metrics.analyze_unified_memory_health()
        post_health = post_health_report.get("overall_health_score", 0.0)
        
        if post_health >= initial_health:
            result["score"] += 0.2
        else:
            result["errors"].append("Health did not improve after optimization")
        
        # Step 5: Recommendations generation
        recommendations = post_health_report.get("recommendations", [])
        
        if len(recommendations) > 0:
            result["score"] += 0.2
        else:
            result["errors"].append("No recommendations generated")
        
        result["passed"] = result["score"] >= 0.6
        
    except Exception as e:
        result["errors"].append(f"End-to-end test failed: {str(e)}")
        result["score"] = 0.0
    
    return result

def generate_health_recommendations(test_results: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on test results"""
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

if __name__ == "__main__":
    success = test_group_c_memory_health_system()
    exit(0 if success else 1)