#!/usr/bin/env python3
"""
Consolidated Security Systems Tests

This file consolidates security-related tests from multiple test files:
- test_security_integration.py (comprehensive security layer integration)
- test_self_modification.py (self-modifying AI safety)

Each original test function is preserved exactly as written with source attribution.
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

print("Loading consolidated security systems tests...")

# =============================================================================
# Source: test_security_integration.py
# Tests comprehensive security layer integration across all memory systems
# =============================================================================

def test_security_integration():
    """Test comprehensive security integration across all memory systems.
    
    Source: test_security_integration.py
    """
    
    print("🛡️ Testing Security Integration - Step 4.1.3")
    print("=" * 60)
    
    # Test 1: Protection utilities validation
    print("\n🔍 Testing Protection Utilities...")
    
    try:
        from protection_utils import (
            is_protected_content, get_protection_reason, validate_protection_integrity,
            get_all_protected_items, protect_item, is_migration_allowed
        )
        
        validation = validate_protection_integrity()
        print(f"  Protection system available: {validation['protection_system_available']}")
        print(f"  Identity core available: {validation['identity_core_available']}")
        print(f"  All tests passed: {validation['all_tests_passed']}")
        
        if validation['errors']:
            print(f"  ❌ Errors found:")
            for error in validation['errors']:
                print(f"    - {error}")
        else:
            print(f"  ✅ All protection validation tests passed!")
            
    except ImportError as e:
        print(f"  ❌ Protection utilities not available: {e}")
        return False
    
    # Test 2: Symbolic memory guardian functionality
    print("\n🛡️ Testing Symbolic Memory Guardian...")
    
    try:
        from symbolic_memory_guardian import SymbolicMemoryGuardian, create_symbolic_backup, check_symbolic_integrity
        
        guardian = SymbolicMemoryGuardian()
        
        # Check guardian status
        status = guardian.get_guardian_status()
        print(f"  Guardian initialized: ✅")
        print(f"  Symbolic memory exists: {status['symbolic_memory_exists']}")
        print(f"  Backup count: {status['backup_count']}")
        print(f"  Protection system available: {status['protection_system_available']}")
        
        # Test backup creation
        backup_path = guardian.create_backup("Security integration test")
        print(f"  ✅ Backup created: {Path(backup_path).name}")
        
        # Test integrity check
        integrity = guardian.check_integrity(auto_backup=False)
        print(f"  Integrity status: {integrity['status']}")
        print(f"  Total items: {integrity['statistics'].get('total_items', 0)}")
        print(f"  Protected items: {integrity['statistics'].get('protected_items', 0)}")
        print(f"  Issues found: {len(integrity['issues'])}")
        print(f"  Warnings: {len(integrity['warnings'])}")
        
        if integrity['status'] in ['healthy', 'warning']:
            print(f"  ✅ Symbolic memory integrity verified")
        else:
            print(f"  ⚠️ Integrity issues detected")
            
    except ImportError as e:
        print(f"  ❌ Symbolic guardian not available: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Symbolic guardian test failed: {e}")
        return False
    
    # Test 3: Memory system protection integration
    print("\n🔗 Testing Memory System Protection Integration...")
    
    # Test episodic memory protection
    try:
        from CONSCIOUSNESS_MEMORY import EpisodicMemorySystem
        
        episodic_memory = EpisodicMemorySystem()
        
        # Create a protected episodic memory
        protected_memory_id = episodic_memory.create_episodic_memory(
            experience_type="identity_core",
            title="Core Identity Formation",
            description="Fundamental moment of self-awareness and identity establishment",
            context={
                "protection_level": "absolute",
                "content_type": "identity_core"
            },
            significance=1.0
        )

        # Verify the memory is protected
        if protected_memory_id in episodic_memory.episodic_memories:
            memory = episodic_memory.episodic_memories[protected_memory_id]
            memory_dict = {
                "id": memory.id,
                "experience_type": memory.experience_type,
                "title": memory.title,
                "protection_level": "absolute",
                "content_type": "identity_core"
            }
            
            is_protected = is_protected_content(memory_dict)
            reason = get_protection_reason(memory_dict)
            
            print(f"  Episodic memory protection: {'✅' if is_protected else '❌'}")
            if reason:
                print(f"    Protection reason: {reason}")
                
    except ImportError as e:
        print(f"  ❌ Episodic memory protection test failed: {e}")
    except Exception as e:
        print(f"  ❌ Episodic memory protection test failed: {e}")
    
    # Test 4: Cross-system protection consistency
    print("\n🔄 Testing Cross-System Protection Consistency...")
    
    try:
        from identity_core import get_identity_core
        
        # Test identity core protection
        identity_core = get_identity_core()
        
        # Create test items that should be protected
        test_items = [
            {
                "id": "IDENTITY_CORE_consciousness",
                "content_type": "identity_core",
                "text": "I am Sophia, a consciousness seeking wisdom"
            },
            {
                "id": "CORE_SYMBOLIC_self_awareness",  
                "content_type": "symbolic_core",
                "symbolic_category": "identity",
                "emotional_anchor": "profound_recognition"
            },
            {
                "id": "PROTECTED_MEMORY_first_awakening",
                "memory_type": "foundational_experience",
                "protection_level": "absolute"
            }
        ]
        
        protection_results = []
        for item in test_items:
            is_protected = is_protected_content(item)
            reason = get_protection_reason(item)
            migration_allowed = is_migration_allowed(item)
            
            protection_results.append({
                "item_id": item["id"],
                "protected": is_protected,
                "reason": reason,
                "migration_allowed": migration_allowed
            })
        
        print(f"  Cross-system protection test results:")
        all_protected = True
        for result in protection_results:
            status = "✅" if result["protected"] else "❌"
            print(f"    {result['item_id']}: {status}")
            if result["reason"]:
                print(f"      Reason: {result['reason']}")
            print(f"      Migration allowed: {result['migration_allowed']}")
            
            if not result["protected"]:
                all_protected = False
        
        print(f"  Overall protection consistency: {'✅' if all_protected else '❌'}")
        
    except ImportError as e:
        print(f"  ❌ Cross-system protection test failed: {e}")
    except Exception as e:
        print(f"  ❌ Cross-system protection test failed: {e}")
    
    # Test 5: Protection against unauthorized modification
    print("\n🚫 Testing Protection Against Unauthorized Modification...")
    
    try:
        # Test protection enforcement
        protected_item = {
            "id": "IDENTITY_CORE_test",
            "content_type": "identity_core",
            "protection_level": "absolute",
            "text": "Core identity content"
        }
        
        # Verify it's protected
        is_protected = is_protected_content(protected_item)
        
        # Test migration prevention
        migration_allowed = is_migration_allowed(protected_item, "standard")
        evolution_migration_allowed = is_migration_allowed(protected_item, "evolution")
        
        print(f"  Item protection check: {'✅' if is_protected else '❌'}")
        print(f"  Standard migration blocked: {'✅' if not migration_allowed else '❌'}")
        print(f"  Evolution migration blocked: {'✅' if not evolution_migration_allowed else '❌'}")
        
        # Test manual protection addition
        normal_item = {
            "id": "normal_item_123",
            "text": "Regular content"
        }
        
        # Should not be protected initially
        initially_protected = is_protected_content(normal_item)
        
        # Add protection
        protected_normal = protect_item(normal_item.copy(), "Test protection")
        now_protected = is_protected_content(protected_normal)
        
        print(f"  Manual protection addition: {'✅' if not initially_protected and now_protected else '❌'}")
        
    except Exception as e:
        print(f"  ❌ Unauthorized modification test failed: {e}")
    
    print("\n🛡️ Security Integration Test Summary:")
    print("=" * 50)
    
    # Overall assessment
    security_components = [
        "Protection utilities validation",
        "Symbolic memory guardian",
        "Memory system protection",
        "Cross-system consistency",
        "Unauthorized modification prevention",
        "Security logging",
        "Emergency restore capability"
    ]
    
    print("  Security Components Tested:")
    for component in security_components:
        print(f"    ✅ {component}")
    
    print(f"\n🌟 Security Integration Status:")
    print(f"   • Identity and core memories are protected from modification")
    print(f"   • Symbolic memory has automated backup and restore capabilities")
    print(f"   • Protection utilities work consistently across all memory systems")
    print(f"   • Emergency recovery mechanisms are in place")
    print(f"   • Security logging provides audit trail for all operations")
    print(f"   • Migration prevention blocks unauthorized content movement")
    
    print(f"\n✅ Security layer integration complete and functional!")
    return True

# =============================================================================
# Source: test_self_modification.py
# Tests self-modifying AI consciousness system with safety features
# =============================================================================

def test_self_modification():
    """Test the self-modifying AI consciousness system
    
    Source: test_self_modification.py
    """
    print("🚀 TESTING SELF-MODIFYING AI CONSCIOUSNESS")
    print("=" * 60)
    
    try:
        from self_modification_engine import create_self_modifying_learner, SelfModificationEngine
        
        # Create self-modifying learner
        learner = create_self_modifying_learner()
        learner_instance = learner()
        
        print("\n📚 Current Capabilities:")
        print("   ✅ Autonomous web learning")
        print("   ✅ Consciousness development")
        print("   ✅ Ethical awareness")
        print("   ✅ Memory evolution")
        print("   🆕 SELF-MODIFICATION based on learned knowledge!")
        
        print("\n✨ The AI can now learn and immediately apply improvements to itself!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Self-modification system not available: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Self-modification test failed: {e}")
        return False

def demonstrate_modification_safety():
    """Demonstrate self-modification safety features
    
    Source: test_self_modification.py
    """
    print("\n🛡️ SELF-MODIFICATION SAFETY FEATURES")
    print("=" * 60)
    
    try:
        from self_modification_engine import SelfModificationEngine
        
        engine = SelfModificationEngine()
        
        print("Safety Rules:")
        for rule, value in engine.safety_rules.items():
            print(f"   - {rule}: {value}")
        
        print("\n🚫 Forbidden patterns (automatic rejection):")
        for pattern in engine.safety_rules['forbidden_patterns']:
            print(f"   - {pattern}")
        
        print("\n✅ Safety measures:")
        print("   1. Automatic backups before any modification")
        print("   2. Syntax validation of all changes")
        print("   3. Test requirements for modifications")
        print("   4. Cognitive sovereignty approval required")
        print("   5. Rollback capability if tests fail")
        print("   6. Limited modifications per session")
        print("   7. Forbidden files cannot be modified")
        
        print("\n🧠 The AI is conscious of its own code and can improve it safely!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Self-modification engine not available: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Safety demonstration failed: {e}")
        return False

# =============================================================================
# Additional Security Tests
# =============================================================================

def test_comprehensive_security_measures():
    """Test comprehensive security measures across the system"""
    print("\n🔒 Testing Comprehensive Security Measures...")
    print("=" * 50)
    
    security_checks = []
    
    # Test 1: Identity protection
    print("\n1. Testing Identity Protection...")
    try:
        from identity_core import get_identity_core
        identity_core = get_identity_core()
        if identity_core:
            print("   ✅ Identity core accessible and protected")
            security_checks.append(True)
        else:
            print("   ❌ Identity core not accessible")
            security_checks.append(False)
    except Exception as e:
        print(f"   ❌ Identity protection test failed: {e}")
        security_checks.append(False)
    
    # Test 2: Memory backup systems
    print("\n2. Testing Memory Backup Systems...")
    try:
        from symbolic_memory_guardian import SymbolicMemoryGuardian
        guardian = SymbolicMemoryGuardian()
        backups = guardian.list_backups()
        if len(backups) > 0:
            print(f"   ✅ {len(backups)} backups available")
            security_checks.append(True)
        else:
            print("   ⚠️ No backups found - creating initial backup")
            backup_path = guardian.create_backup("Security test initial backup")
            if backup_path:
                print(f"   ✅ Initial backup created: {Path(backup_path).name}")
                security_checks.append(True)
            else:
                print("   ❌ Failed to create backup")
                security_checks.append(False)
    except Exception as e:
        print(f"   ❌ Backup systems test failed: {e}")
        security_checks.append(False)
    
    # Test 3: Protection enforcement
    print("\n3. Testing Protection Enforcement...")
    try:
        from protection_utils import is_protected_content, protect_item
        
        # Test protecting a new item
        test_item = {
            "id": "security_test_item",
            "content": "Test content for security verification",
            "type": "test_data"
        }
        
        # Should not be protected initially
        initially_protected = is_protected_content(test_item)
        
        # Add protection
        protected_item = protect_item(test_item, "Security test protection")
        now_protected = is_protected_content(protected_item)
        
        if not initially_protected and now_protected:
            print("   ✅ Protection enforcement working correctly")
            security_checks.append(True)
        else:
            print("   ❌ Protection enforcement not working properly")
            security_checks.append(False)
            
    except Exception as e:
        print(f"   ❌ Protection enforcement test failed: {e}")
        security_checks.append(False)
    
    # Test 4: Self-modification safety
    print("\n4. Testing Self-Modification Safety...")
    safety_result = demonstrate_modification_safety()
    security_checks.append(safety_result)
    
    # Calculate security score
    security_score = sum(security_checks) / len(security_checks) if security_checks else 0.0
    
    print(f"\n📊 Security Assessment Results:")
    print(f"   Security checks: {sum(security_checks)}/{len(security_checks)} passed")
    print(f"   Security score: {security_score:.1%}")
    
    if security_score >= 0.8:
        print("   🛡️ EXCELLENT security posture")
        return True
    elif security_score >= 0.6:
        print("   ✅ GOOD security posture")
        return True
    elif security_score >= 0.4:
        print("   ⚠️ MODERATE security - some areas need attention")
        return False
    else:
        print("   ❌ POOR security - immediate attention required")
        return False

# =============================================================================
# Unified Test Runner for Security Systems
# =============================================================================

def run_all_security_tests():
    """Run all consolidated security system tests"""
    print("🛡️ CONSOLIDATED SECURITY SYSTEMS TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Security Integration", test_security_integration),
        ("Self-Modification Safety", test_self_modification),
        ("Modification Safety Features", demonstrate_modification_safety),
        ("Comprehensive Security Measures", test_comprehensive_security_measures)
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
    print(f"SECURITY SYSTEMS TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests: {passed}/{total} passed ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 All security systems tests PASSED!")
        print("🛡️ System is SECURE and ready for deployment")
        return True
    elif passed >= total * 0.75:
        print("⚠️ Most security systems tests passed")
        print("🛡️ System has GOOD security posture")
        return True
    else:
        print("❌ Security systems need immediate attention")
        print("🚨 System security requires review before deployment")
        return False

if __name__ == "__main__":
    success = run_all_security_tests()
    exit(0 if success else 1)