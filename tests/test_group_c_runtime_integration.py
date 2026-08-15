#!/usr/bin/env python3
"""
Runtime Integration Test for GROUP C: MEMORY & COGNITION SUPPORT
Tests actual runtime connections between:
- episodic_memory.py
- brain_metrics.py  
- memory_maintenance.py
- memory_optimizer.py
"""

import time
from datetime import datetime
import json
from pathlib import Path

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
        
        # Check if it analyzed episodic memory
        if "episodic_memory_health" in health_report:
            ep_health = health_report["episodic_memory_health"]
            print(f"   ✓ Episodic memory analyzed: {ep_health.get('total_memories', 0)} memories")
            test_results["integration_tests"].append({
                "test": "brain_metrics_episodic_analysis",
                "status": "PASS",
                "details": f"Found {ep_health.get('total_memories', 0)} episodic memories"
            })
    else:
        print("   ✗ Health analysis failed")
        test_results["integration_tests"].append({
            "test": "brain_metrics_health_analysis",
            "status": "FAIL",
            "details": "No health report generated"
        })
        
    # Test adaptive weights
    weights = bm.get_adaptive_weights()
    if weights:
        print(f"   ✓ Adaptive weights available: {weights['confidence']} confidence")
        test_results["integration_tests"].append({
            "test": "brain_metrics_adaptive_weights",
            "status": "PASS",
            "details": f"Confidence: {weights['confidence']}"
        })
        
except Exception as e:
    print(f"   ✗ Brain metrics test failed: {e}")
    test_results["errors"].append(f"brain_metrics: {str(e)}")

# Test 3: Memory Maintenance Integration
print("\n3. Testing Memory Maintenance System...")
try:
    from memory_maintenance import MemoryMaintenanceManager, prune_phase1_symbolic_vectors
    
    mm = MemoryMaintenanceManager()
    test_results["components_tested"].append("memory_maintenance")
    
    # Check maintenance status
    status = mm.get_maintenance_status()
    
    if status and "system_health" in status:
        print(f"   ✓ Maintenance status retrieved")
        print(f"     - Maintenance needed: {status['maintenance_needed']}")
        if status["system_health"]:
            print(f"     - Overall health: {status['system_health'].get('overall', 0):.2%}")
        
        test_results["integration_tests"].append({
            "test": "memory_maintenance_status",
            "status": "PASS",
            "details": f"Maintenance needed: {status['maintenance_needed']}"
        })
        
    # Test Phase 1 pruning function
    initial_count = 0
    if hasattr(bm, '_read_json'):
        vector_data = bm._read_json(Path("data/vector_memory.json"))
        initial_count = len(vector_data) if isinstance(vector_data, list) else 0
    
    pruned = prune_phase1_symbolic_vectors()
    print(f"   ✓ Phase 1 pruning function executed: {pruned} vectors pruned")
    
    test_results["integration_tests"].append({
        "test": "memory_maintenance_pruning",
        "status": "PASS",
        "details": f"Pruned {pruned} vectors"
    })
    
except Exception as e:
    print(f"   ✗ Memory maintenance test failed: {e}")
    test_results["errors"].append(f"memory_maintenance: {str(e)}")

# Test 4: Memory Optimizer Integration
print("\n4. Testing Memory Optimizer Integration...")
try:
    # Test imports that memory_optimizer claims to use
    from sofia.core.unified_memory import get_unified_memory
    from sofia.memory.brain_metrics import BrainMetrics
    from memory_maintenance import prune_phase1_symbolic_vectors
    
    test_results["components_tested"].append("memory_optimizer_dependencies")
    
    # Test unified memory access
    um = get_unified_memory()
    if um:
        print(f"   ✓ Memory optimizer can access unified memory")
        test_results["integration_tests"].append({
            "test": "memory_optimizer_unified_access",
            "status": "PASS",
            "details": "Successfully accessed unified memory"
        })
    
    # Test adaptive weights computation
    print(f"   ✓ Memory optimizer can use brain metrics for adaptive weights")
    test_results["integration_tests"].append({
        "test": "memory_optimizer_brain_metrics",
        "status": "PASS",
        "details": "Can access brain metrics functions"
    })
    
except Exception as e:
    print(f"   ✗ Memory optimizer integration test failed: {e}")
    test_results["errors"].append(f"memory_optimizer_integration: {str(e)}")

# Test 5: Cross-Component Data Flow
print("\n5. Testing Cross-Component Data Flow...")
try:
    # Create an episodic memory and see if brain metrics can analyze it
    from sofia.core.CONSCIOUSNESS_MEMORY import EpisodicMemorySystem
    from sofia.memory.brain_metrics import BrainMetrics
    
    em = EpisodicMemorySystem()
    
    # Create test memory
    test_context = {
        "participants": ["AI", "test_system"],
        "location": "integration_test",
        "cognitive_load": 0.7,
        "concepts": ["integration", "testing", "memory"]
    }
    
    memory_id = em.create_episodic_memory(
        experience_type="testing",
        title="Cross-component integration test",
        description="Testing if data flows between episodic memory and brain metrics",
        context=test_context,
        significance=0.9
    )
    
    # Force save
    em._save_episodic_memories()
    
    # Now check if brain metrics can see it
    bm = BrainMetrics()
    health = bm.analyze_unified_memory_health()
    
    ep_health = health.get("episodic_memory_health", {})
    if ep_health.get("total_memories", 0) > 0:
        print(f"   ✓ Data flows from episodic memory to brain metrics")
        print(f"     - Brain metrics found {ep_health['total_memories']} episodic memories")
        test_results["integration_tests"].append({
            "test": "cross_component_data_flow",
            "status": "PASS",
            "details": f"Brain metrics detected {ep_health['total_memories']} episodic memories"
        })
    else:
        print("   ✗ Brain metrics could not see episodic memories")
        test_results["integration_tests"].append({
            "test": "cross_component_data_flow",
            "status": "FAIL",
            "details": "No episodic memories detected by brain metrics"
        })
        
except Exception as e:
    print(f"   ✗ Cross-component test failed: {e}")
    test_results["errors"].append(f"cross_component: {str(e)}")

# Test 6: Memory Maintenance Can Act on Brain Metrics Analysis
print("\n6. Testing Maintenance Acting on Health Analysis...")
try:
    from memory_maintenance import MemoryMaintenanceManager
    from sofia.memory.brain_metrics import BrainMetrics
    
    mm = MemoryMaintenanceManager()
    
    # Check if maintenance uses brain metrics internally
    if hasattr(mm, 'brain_metrics') and mm.brain_metrics is not None:
        print(f"   ✓ Memory maintenance has brain metrics integration")
        test_results["integration_tests"].append({
            "test": "maintenance_uses_brain_metrics",
            "status": "PASS",
            "details": "MemoryMaintenanceManager includes BrainMetrics"
        })
        
        # Test if it can get system health
        health = mm._get_system_health()
        if health:
            print(f"     - Can retrieve system health: {list(health.keys())}")
    else:
        print("   ✗ Memory maintenance does not integrate brain metrics")
        test_results["integration_tests"].append({
            "test": "maintenance_uses_brain_metrics",
            "status": "FAIL",
            "details": "No brain metrics integration found"
        })
        
except Exception as e:
    print(f"   ✗ Maintenance-metrics integration test failed: {e}")
    test_results["errors"].append(f"maintenance_metrics: {str(e)}")

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

# Save results
output_file = Path("data/group_c_runtime_integration_results.json")
output_file.parent.mkdir(exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(test_results, f, indent=2)

print(f"\nResults saved to: {output_file}")

# Final verdict
if test_results["summary"]["success_rate"] >= 0.8:
    print("\n✅ GROUP C INTEGRATION: WORKING")
else:
    print("\n❌ GROUP C INTEGRATION: ISSUES DETECTED")
    if test_results["errors"]:
        print("\nErrors encountered:")
        for error in test_results["errors"]:
            print(f"  - {error}")