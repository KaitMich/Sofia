#!/usr/bin/env python3
# test_autonomous_integration.py - Test autonomous loop integration

"""
Test script to verify that the autonomous loop integration works correctly.
Tests:
1. UnifiedOrchestrationSystem initializes with shutdown manager
2. Shutdown handlers are registered
3. Dream cycle is initialized
4. Autonomous loop methods are available
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_orchestrator_initialization():
    """Test that orchestrator initializes with new components"""
    print("\n" + "="*70)
    print("TEST 1: Orchestrator Initialization")
    print("="*70)

    try:
        from unified_orchestration import UnifiedOrchestrationSystem

        print("Creating UnifiedOrchestrationSystem...")
        orchestrator = UnifiedOrchestrationSystem(data_dir="data", verbose=True)

        # Verify shutdown manager exists
        assert hasattr(orchestrator, 'shutdown_manager'), "❌ Missing shutdown_manager"
        print("✅ shutdown_manager initialized")

        # Verify dream cycle exists
        assert hasattr(orchestrator, 'dream_cycle'), "❌ Missing dream_cycle"
        print("✅ dream_cycle initialized")

        # Verify idle tracking
        assert hasattr(orchestrator, 'last_user_interaction'), "❌ Missing last_user_interaction"
        assert hasattr(orchestrator, 'idle_threshold_seconds'), "❌ Missing idle_threshold_seconds"
        print("✅ Idle tracking initialized")

        # Verify methods exist
        assert hasattr(orchestrator, 'run_autonomous_loop'), "❌ Missing run_autonomous_loop method"
        assert hasattr(orchestrator, 'update_interaction_time'), "❌ Missing update_interaction_time method"
        assert hasattr(orchestrator, 'stop_autonomous_loop'), "❌ Missing stop_autonomous_loop method"
        print("✅ Autonomous loop methods available")

        print("\n✅ TEST 1 PASSED: All components initialized correctly")
        return True

    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shutdown_handlers():
    """Test that shutdown handlers are registered"""
    print("\n" + "="*70)
    print("TEST 2: Shutdown Handler Registration")
    print("="*70)

    try:
        from unified_orchestration import UnifiedOrchestrationSystem

        print("Creating orchestrator with verbose mode...")
        orchestrator = UnifiedOrchestrationSystem(data_dir="data", verbose=True)

        # Check that shutdown manager has cleanup functions registered
        cleanup_count = len(orchestrator.shutdown_manager.cleanup_functions)
        print(f"\n✅ Shutdown manager has {cleanup_count} cleanup function(s) registered")

        if cleanup_count > 0:
            print("\nRegistered cleanup functions:")
            for i, cleanup_task in enumerate(orchestrator.shutdown_manager.cleanup_functions, 1):
                print(f"  {i}. {cleanup_task['name']} (priority: {cleanup_task['priority']})")

        assert cleanup_count >= 1, "❌ No cleanup functions registered"

        print("\n✅ TEST 2 PASSED: Shutdown handlers registered successfully")
        return True

    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interaction_time_update():
    """Test that interaction time can be updated"""
    print("\n" + "="*70)
    print("TEST 3: Interaction Time Update")
    print("="*70)

    try:
        from unified_orchestration import UnifiedOrchestrationSystem
        import time

        print("Creating orchestrator...")
        orchestrator = UnifiedOrchestrationSystem(data_dir="data", verbose=False)

        initial_time = orchestrator.last_user_interaction
        print(f"Initial interaction time: {initial_time}")

        # Wait a tiny bit
        time.sleep(0.1)

        # Update interaction time
        orchestrator.update_interaction_time()
        updated_time = orchestrator.last_user_interaction
        print(f"Updated interaction time: {updated_time}")

        assert updated_time > initial_time, "❌ Interaction time not updated"

        print("\n✅ TEST 3 PASSED: Interaction time updates correctly")
        return True

    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_integration():
    """Test that CLI can import and use the orchestrator"""
    print("\n" + "="*70)
    print("TEST 4: CLI Integration")
    print("="*70)

    try:
        print("Importing CLI...")
        from cli import SophiaCLI

        print("Creating CLI instance...")
        cli = SophiaCLI()

        print("Ensuring orchestrator is initialized...")
        success = cli.ensure_orchestrator()

        assert success, "❌ Failed to initialize orchestrator"
        print("✅ Orchestrator initialized via CLI")

        # Verify orchestrator has new components
        assert hasattr(cli.orchestrator, 'shutdown_manager'), "❌ CLI orchestrator missing shutdown_manager"
        assert hasattr(cli.orchestrator, 'dream_cycle'), "❌ CLI orchestrator missing dream_cycle"
        assert hasattr(cli.orchestrator, 'run_autonomous_loop'), "❌ CLI orchestrator missing run_autonomous_loop"

        print("✅ CLI orchestrator has all new components")

        print("\n✅ TEST 4 PASSED: CLI integration successful")
        return True

    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 AUTONOMOUS INTEGRATION TEST SUITE")
    print("="*70)
    print("Testing the integration of shutdown manager and autonomous loop")
    print("into the UnifiedOrchestrationSystem")
    print("="*70)

    tests = [
        test_orchestrator_initialization,
        test_shutdown_handlers,
        test_interaction_time_update,
        test_cli_integration
    ]

    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(results)
    total = len(results)

    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Autonomous integration is complete and functional")
        print("\nNext steps:")
        print("  1. Run: python3 cli.py start --mode autonomous")
        print("  2. Wait 30 minutes or modify idle_threshold_seconds for testing")
        print("  3. Press Ctrl+C to test graceful shutdown")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please review the errors above and fix the issues")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
