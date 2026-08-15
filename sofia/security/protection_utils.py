#!/usr/bin/env python3
"""
Protection Utilities - Robust Helper Functions for Identity Protection

This module provides centralized, robust helper functions for identifying
and protecting content that should not be modified by any system.
"""

import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

# Import identity core if available
try:
    from sofia.core.identity_core import get_identity_core
    IDENTITY_CORE_AVAILABLE = True
except ImportError:
    IDENTITY_CORE_AVAILABLE = False

def is_protected_content(item: Union[Dict[str, Any], str, Any]) -> bool:
    """
    Master protection check function.
    
    Checks if any content (memory item, file, etc.) is protected
    and should not be modified, deleted, or migrated.
    
    Args:
        item: Can be a dictionary (memory item), string (ID), or any object
        
    Returns:
        bool: True if content is protected, False otherwise
    """
    if item is None:
        return False
    
    # Handle string IDs
    if isinstance(item, str):
        return _is_protected_id(item)
    
    # Handle dictionary items (memory entries)
    if isinstance(item, dict):
        return _is_protected_dict(item)
    
    # Handle other object types
    if hasattr(item, '__dict__'):
        return _is_protected_object(item)
    
    return False

def _is_protected_id(item_id: str) -> bool:
    """Check if an ID represents protected content."""
    # Protected ID prefixes
    protected_prefixes = [
        'IDENTITY_CORE_',
        'PROTECTED_MEMORY_',
        'CORE_SYMBOLIC_',
        'SOVEREIGNTY_',
        'COGNITIVE_CORE_'
    ]
    
    return any(item_id.startswith(prefix) for prefix in protected_prefixes)

def _is_protected_dict(item: Dict[str, Any]) -> bool:
    """Comprehensive protection check for dictionary items."""
    
    # 1. Check explicit protection flags
    # evolution_protected removed: Sofia must be able to evolve any value she forms

    if item.get('cannot_be_deleted') is True:
        return True
        
    if item.get('cannot_be_modified') is True:
        return True
        
    if item.get('cannot_be_migrated') is True:
        return True
    
    # 2. Check protection levels
    protection_level = item.get('protection_level', '').lower()
    if protection_level in ['absolute', 'maximum', 'inviolable']:
        return True
    
    # 3. Check content types
    content_type = item.get('content_type', '').lower()
    protected_content_types = [
        'identity_core',
        'symbolic_core', 
        'foundational_experience',
        'cognitive_core',
        'sovereignty_core'
    ]
    if content_type in protected_content_types:
        return True
    
    # 4. Check source URLs
    source_url = item.get('source_url', '') or ''
    protected_sources = [
        'core://protected',
        'identity://protected',
        'identity://core',
        'sovereignty://core',
        'cognitive://core'
    ]
    if source_url and any(source_url.startswith(prefix) for prefix in protected_sources):
        return True
    
    # 5. Check memory types
    memory_type = item.get('memory_type', '').lower()
    if memory_type in ['foundational_experience', 'core_identity']:
        return True
    
    # 6. Check item ID
    item_id = item.get('id', '')
    if item_id and _is_protected_id(item_id):
        return True
    
    # 7. Check for cognitive sovereignty markers
    if item.get('sovereignty_protected') is True:
        return True
    
    # 8. Check decision history for protection markers
    decision_history = item.get('decision_history', [])
    if isinstance(decision_history, list):
        for decision in decision_history:
            if isinstance(decision, dict) and decision.get('protected') is True:
                return True
    
    # 9. Check related values for identity markers
    related_values = item.get('related_values', [])
    if isinstance(related_values, list):
        identity_values = ['autonomy', 'identity', 'consciousness', 'self_awareness']
        if any(value in identity_values for value in related_values):
            # Additional check - if it also has high protection markers
            if (item.get('memory_strength', 0) >= 1.0 and 
                item.get('significance') and 
                'core' in str(item.get('significance', '')).lower()):
                return True
    
    return False

def _is_protected_object(obj: Any) -> bool:
    """Check protection for general objects."""
    obj_dict = obj.__dict__ if hasattr(obj, '__dict__') else {}
    
    # Convert object to dict-like structure for checking
    item_dict = {}
    for attr_name in dir(obj):
        if not attr_name.startswith('_'):
            try:
                attr_value = getattr(obj, attr_name)
                if not callable(attr_value):
                    item_dict[attr_name] = attr_value
            except:
                continue
    
    return _is_protected_dict(item_dict)

def is_protected_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file contains protected content that should not be modified.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        bool: True if file is protected, False otherwise
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    if not file_path.exists():
        return False
    
    # Protected filenames
    protected_files = [
        'identity_core.py',
        'cognitive_sovereignty.py', 
        'protected_memories.json',
        'CONSCIOUSNESS_PHASE_1_COMPLETE.md'
    ]
    
    if file_path.name in protected_files:
        return True
    
    # Protected directories
    protected_dirs = ['identity', 'sovereignty', 'core']
    if any(part in protected_dirs for part in file_path.parts):
        return True
    
    return False

def get_protection_reason(item: Union[Dict[str, Any], str, Any]) -> str:
    """
    Get a human-readable reason why content is protected.
    
    Args:
        item: The item to check
        
    Returns:
        str: Reason for protection, or empty string if not protected
    """
    if not is_protected_content(item):
        return ""
    
    if isinstance(item, str):
        if _is_protected_id(item):
            return f"Protected ID pattern: {item}"
    
    if isinstance(item, dict):
        # evolution_protected check removed: nothing is permanently locked from internal evolution

        if item.get('protection_level') in ['absolute', 'maximum']:
            return f"Protection level: {item.get('protection_level')}"
        
        if item.get('content_type') == 'identity_core':
            return "Identity core content"
        
        if item.get('content_type') == 'symbolic_core':
            return "Core symbolic content"
        
        if item.get('memory_type') == 'foundational_experience':
            return "Foundational experience memory"
        
        source_url = item.get('source_url', '')
        if source_url.startswith('identity://'):
            return "Identity source protection"
        
        if source_url.startswith('core://protected'):
            return "Core protected source"
    
    return "Protected content (multiple reasons)"

def get_all_protected_items(memory_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter a list of memory items to return only protected ones.
    
    Args:
        memory_data: List of memory items to filter
        
    Returns:
        List of protected memory items
    """
    return [item for item in memory_data if is_protected_content(item)]

def validate_protection_integrity() -> Dict[str, Any]:
    """
    Validate that all protection systems are working correctly.
    
    Returns:
        Dict with validation results
    """
    results = {
        'protection_system_available': True,
        'identity_core_available': IDENTITY_CORE_AVAILABLE,
        'test_results': {},
        'errors': []
    }
    
    try:
        # Test 1: Basic protection detection
        test_item = {
            'id': 'IDENTITY_CORE_test',
            'protection_level': 'absolute',
            'content_type': 'identity_core'
        }
        
        is_protected = is_protected_content(test_item)
        results['test_results']['basic_protection'] = is_protected
        
        if not is_protected:
            results['errors'].append("Basic protection detection failed")
        
        # Test 2: ID-based protection
        test_id = 'PROTECTED_MEMORY_test'
        id_protected = is_protected_content(test_id)
        results['test_results']['id_protection'] = id_protected
        
        if not id_protected:
            results['errors'].append("ID-based protection failed")
        
        # Test 3: Multiple protection flags
        multi_protected_item = {
            'cannot_be_deleted': True,
            'protection_level': 'maximum'
        }
        
        multi_protected = is_protected_content(multi_protected_item)
        results['test_results']['multi_flag_protection'] = multi_protected
        
        if not multi_protected:
            results['errors'].append("Multi-flag protection failed")
        
        # Test 4: Non-protected item
        normal_item = {
            'id': 'normal_item_123',
            'text': 'Some regular content',
            'source_url': 'https://example.com'
        }
        
        is_normal = not is_protected_content(normal_item)
        results['test_results']['normal_item_not_protected'] = is_normal
        
        if not is_normal:
            results['errors'].append("Normal item incorrectly flagged as protected")
        
        # Overall result
        results['all_tests_passed'] = len(results['errors']) == 0
        
    except Exception as e:
        results['errors'].append(f"Validation error: {str(e)}")
        results['protection_system_available'] = False
    
    return results

# Convenience functions for common use cases
def protect_item(item: Dict[str, Any], reason: str = "Manual protection") -> Dict[str, Any]:
    """
    Add protection flags to an item.
    
    Args:
        item: Item to protect
        reason: Reason for protection
        
    Returns:
        Protected item (modified in place)
    """
    # evolution_protected no longer set: Sofia can evolve any value she forms
    item['protection_level'] = 'maximum'
    item['protection_reason'] = reason
    item['protection_timestamp'] = str(json.dumps({"time": "now"}))  # Simple timestamp
    
    return item

def is_migration_allowed(item: Dict[str, Any], migration_type: str = "standard") -> bool:
    """
    Check if a specific type of migration is allowed for an item.
    
    Args:
        item: Item to check
        migration_type: Type of migration (standard, reverse, evolution)
        
    Returns:
        bool: True if migration is allowed, False otherwise
    """
    # If item is protected, no migration allowed
    if is_protected_content(item):
        return False
    
    # Check specific migration restrictions
    if migration_type == "reverse" and item.get('no_reverse_migration'):
        return False
    
    if migration_type == "evolution" and item.get('evolution_locked'):
        return False
    
    return True

if __name__ == "__main__":
    # Test the protection system
    print("🛡️ Testing Protection Utilities...")
    
    # Run validation
    validation = validate_protection_integrity()
    
    print(f"\n📊 Validation Results:")
    print(f"  Protection system available: {validation['protection_system_available']}")
    print(f"  Identity core available: {validation['identity_core_available']}")
    print(f"  All tests passed: {validation['all_tests_passed']}")
    
    if validation['errors']:
        print(f"\n❌ Errors found:")
        for error in validation['errors']:
            print(f"    - {error}")
    else:
        print(f"\n✅ All protection tests passed!")
    
    # Test specific cases
    print(f"\n🧪 Specific Test Cases:")
    
    # Test protected item
    protected_item = {
        'id': 'IDENTITY_CORE_consciousness',
        'content_type': 'identity_core',
        'protection_level': 'absolute'
    }
    
    print(f"  Protected item check: {is_protected_content(protected_item)}")
    print(f"  Protection reason: {get_protection_reason(protected_item)}")
    
    # Test normal item
    normal_item = {
        'id': 'regular_123',
        'text': 'Some normal content'
    }
    
    print(f"  Normal item check: {is_protected_content(normal_item)}")
    print(f"  Migration allowed: {is_migration_allowed(normal_item)}")
    
    print(f"\n🛡️ Protection Utilities ready for use!")