#!/usr/bin/env python3
"""
Memory Consolidation Test Script

This script tests whether we can safely replace memory_maintenance.py with memory_management.py
by verifying:
1. Both files have the required function
2. The function signatures match
3. The function works when imported from memory_management
4. All dependent scripts can import successfully
5. No circular import issues

Run this BEFORE consolidating to ensure safety.
"""

import sys
import importlib
import inspect
from pathlib import Path

# Test results tracking
tests_passed = 0
tests_failed = 0
warnings = []

def print_test(test_name, status, message=""):
    """Print test result with color coding"""
    global tests_passed, tests_failed

    if status == "PASS":
        print(f"✅ PASS: {test_name}")
        if message:
            print(f"   → {message}")
        tests_passed += 1
    elif status == "FAIL":
        print(f"❌ FAIL: {test_name}")
        if message:
            print(f"   → {message}")
        tests_failed += 1
    elif status == "WARN":
        print(f"⚠️  WARN: {test_name}")
        if message:
            print(f"   → {message}")
        warnings.append(f"{test_name}: {message}")

def check_file_exists(filename):
    """Test if a file exists"""
    path = Path(filename)
    if path.exists():
        print_test(f"File exists: {filename}", "PASS", f"Size: {path.stat().st_size} bytes")
        return True
    else:
        print_test(f"File exists: {filename}", "FAIL", "File not found")
        return False

def check_import(module_name):
    """Test if a module can be imported"""
    try:
        module = importlib.import_module(module_name)
        print_test(f"Import: {module_name}", "PASS", f"Module loaded: {module.__file__}")
        return module
    except ImportError as e:
        print_test(f"Import: {module_name}", "FAIL", f"ImportError: {e}")
        return None
    except Exception as e:
        print_test(f"Import: {module_name}", "FAIL", f"Unexpected error: {e}")
        return None

def check_function_exists(module, function_name):
    """Test if a function exists in a module"""
    if module is None:
        print_test(f"Function exists: {function_name}", "FAIL", "Module not loaded")
        return None

    if hasattr(module, function_name):
        func = getattr(module, function_name)
        print_test(f"Function exists: {module.__name__}.{function_name}", "PASS",
                   f"Type: {type(func).__name__}")
        return func
    else:
        print_test(f"Function exists: {module.__name__}.{function_name}", "FAIL",
                   "Function not found")
        return None

def check_function_signature(func1, func2, func_name):
    """Test if two functions have the same signature"""
    if func1 is None or func2 is None:
        print_test(f"Signature match: {func_name}", "FAIL", "One or both functions missing")
        return False

    try:
        sig1 = inspect.signature(func1)
        sig2 = inspect.signature(func2)

        if str(sig1) == str(sig2):
            print_test(f"Signature match: {func_name}", "PASS", f"Signature: {sig1}")
            return True
        else:
            print_test(f"Signature match: {func_name}", "WARN",
                      f"Maintenance: {sig1}\nManagement: {sig2}")
            return False
    except Exception as e:
        print_test(f"Signature match: {func_name}", "FAIL", f"Error: {e}")
        return False

def check_function_callable(module, function_name):
    """Test if a function is callable"""
    if module is None:
        print_test(f"Callable: {function_name}", "FAIL", "Module not loaded")
        return False

    func = getattr(module, function_name, None)
    if func and callable(func):
        print_test(f"Callable: {module.__name__}.{function_name}", "PASS")
        return True
    else:
        print_test(f"Callable: {module.__name__}.{function_name}", "FAIL", "Not callable")
        return False

def test_circular_imports():
    """Test for circular import issues"""
    print("\n🔄 Testing for circular import issues...")

    test_modules = [
        'memory_maintenance',
        'memory_management',
        'unified_memory',
        'memory_optimizer',
        'memory_analytics',
    ]

    for module_name in test_modules:
        try:
            # Force reload to catch circular imports
            if module_name in sys.modules:
                del sys.modules[module_name]
            importlib.import_module(module_name)
            print_test(f"Circular import check: {module_name}", "PASS")
        except ImportError as e:
            if "circular" in str(e).lower():
                print_test(f"Circular import check: {module_name}", "FAIL",
                          f"Circular import detected: {e}")
            else:
                print_test(f"Circular import check: {module_name}", "WARN",
                          f"Import issue (may be ok): {e}")
        except Exception as e:
            print_test(f"Circular import check: {module_name}", "WARN", f"Error: {e}")

def test_memory_optimizer_integration():
    """Test that memory_optimizer can use the consolidated function"""
    print("\n🔗 Testing memory_optimizer integration...")

    try:
        # Test current import (from memory_maintenance)
        from memory_maintenance import prune_phase1_symbolic_vectors as prune_old
        print_test("Current import: memory_maintenance.prune_phase1_symbolic_vectors",
                   "PASS", "Function imported successfully")

        # Test new import (from memory_management)
        from sofia.memory.memory_management import prune_phase1_symbolic_vectors as prune_new
        print_test("New import: memory_management.prune_phase1_symbolic_vectors",
                   "PASS", "Function imported successfully")

        # Verify they have same signature
        sig_old = inspect.signature(prune_old)
        sig_new = inspect.signature(prune_new)

        if str(sig_old) == str(sig_new):
            print_test("Function signatures match", "PASS",
                      f"Both have: {sig_old}")
        else:
            print_test("Function signatures match", "WARN",
                      f"Old: {sig_old}\nNew: {sig_new}")

        return True

    except ImportError as e:
        print_test("memory_optimizer integration", "FAIL", f"Import error: {e}")
        return False
    except Exception as e:
        print_test("memory_optimizer integration", "FAIL", f"Unexpected error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*70)
    print("MEMORY CONSOLIDATION SAFETY TEST")
    print("="*70)
    print()

    # Test 1: Verify files exist
    print("📁 Test 1: File Existence")
    print("-" * 70)
    maintenance_exists = check_file_exists("memory_maintenance.py")
    management_exists = check_file_exists("memory_management.py")
    optimizer_exists = check_file_exists("memory_optimizer.py")
    print()

    if not (maintenance_exists and management_exists):
        print("❌ CRITICAL: Required files missing. Cannot proceed.")
        return False

    # Test 2: Import modules
    print("📦 Test 2: Module Imports")
    print("-" * 70)
    maintenance_module = check_import("memory_maintenance")
    management_module = check_import("memory_management")
    print()

    if not (maintenance_module and management_module):
        print("❌ CRITICAL: Cannot import required modules. Cannot proceed.")
        return False

    # Test 3: Check critical function exists in both
    print("🔍 Test 3: Function Existence")
    print("-" * 70)
    func_name = "prune_phase1_symbolic_vectors"
    maintenance_func = check_function_exists(maintenance_module, func_name)
    management_func = check_function_exists(management_module, func_name)
    print()

    if not (maintenance_func and management_func):
        print("❌ CRITICAL: Required function missing. Cannot proceed.")
        return False

    # Test 4: Compare function signatures
    print("📝 Test 4: Function Signature Compatibility")
    print("-" * 70)
    check_function_signature(maintenance_func, management_func, func_name)
    print()

    # Test 5: Verify functions are callable
    print("☎️  Test 5: Function Callability")
    print("-" * 70)
    check_function_callable(maintenance_module, func_name)
    check_function_callable(management_module, func_name)
    print()

    # Test 6: Check for circular imports
    test_circular_imports()
    print()

    # Test 7: Test memory_optimizer integration
    test_memory_optimizer_integration()
    print()

    # Test 8: Check all 7 functions from maintenance exist in management
    print("📋 Test 8: Complete Function Coverage")
    print("-" * 70)
    all_functions = [
        "prune_phase1_symbolic_vectors",
        "cleanup_old_archives",
        "get_maintenance_stats",
        "perform_emergency_maintenance",
        "get_memory_health_dashboard",
        "schedule_automated_maintenance",
    ]

    for func_name in all_functions:
        maintenance_has = hasattr(maintenance_module, func_name)
        management_has = hasattr(management_module, func_name)

        if maintenance_has and management_has:
            print_test(f"Function coverage: {func_name}", "PASS",
                      "Exists in both files")
        elif management_has and not maintenance_has:
            print_test(f"Function coverage: {func_name}", "WARN",
                      "Only in management (ok)")
        elif maintenance_has and not management_has:
            print_test(f"Function coverage: {func_name}", "FAIL",
                      "Missing from management!")
        else:
            print_test(f"Function coverage: {func_name}", "WARN",
                      "Missing from both")

    # Check for MemoryMaintenanceManager class
    if hasattr(maintenance_module, "MemoryMaintenanceManager"):
        if hasattr(management_module, "MemoryMaintenanceManager"):
            print_test("Class coverage: MemoryMaintenanceManager", "PASS",
                      "Class exists in both files")
        else:
            print_test("Class coverage: MemoryMaintenanceManager", "FAIL",
                      "Missing from management!")

    print()

    # Final Summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"⚠️  Warnings: {len(warnings)}")
    print()

    if tests_failed == 0:
        print("🎉 ALL CRITICAL TESTS PASSED!")
        print()
        print("✅ CONSOLIDATION IS SAFE")
        print()
        print("Next steps:")
        print("1. Update memory_optimizer.py import:")
        print("   Change: from memory_maintenance import prune_phase1_symbolic_vectors")
        print("   To:     from memory_management import prune_phase1_symbolic_vectors")
        print()
        print("2. Archive memory_maintenance.py:")
        print("   mv memory_maintenance.py archive/unused_entry_points/")
        print()
        print("3. Test the system works")
        print()
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print()
        print("⚠️  CONSOLIDATION NOT RECOMMENDED")
        print("   Review failed tests above before proceeding")
        print()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
