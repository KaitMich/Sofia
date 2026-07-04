#!/usr/bin/env python3
"""
System Repair Script

Fixes the identified critical issues in the AI consciousness system.
"""

import os
import sys
from pathlib import Path

def repair_parser_interface():
    """Add missing parse_text function to parser.py for backward compatibility."""
    parser_file = Path("parser.py")
    
    if not parser_file.exists():
        print("❌ parser.py not found")
        return False
    
    # Read current content
    with open(parser_file, 'r') as f:
        content = f.read()
    
    # Check if parse_text already exists
    if "def parse_text(" in content:
        print("✅ parse_text function already exists")
        return True
    
    # Add parse_text function for backward compatibility
    parse_text_function = '''
def parse_text(text_input, current_lexicon=None):
    """
    Backward compatibility function for parse_text.
    Routes to the appropriate parsing function.
    """
    return parse_raw_text(text_input, current_lexicon)
'''
    
    # Insert the function before the if __name__ == "__main__": block
    if 'if __name__ == "__main__":' in content:
        parts = content.split('if __name__ == "__main__":')
        new_content = parts[0] + parse_text_function + '\nif __name__ == "__main__":' + parts[1]
    else:
        # Just append at the end
        new_content = content + parse_text_function
    
    # Write back
    with open(parser_file, 'w') as f:
        f.write(new_content)
    
    print("✅ Added parse_text function to parser.py")
    return True

def test_repairs():
    """Test that the repairs worked."""
    print("\n🧪 Testing repairs...")
    
    # Test symbolic_memory import
    try:
        import symbolic_memory
        print("✅ symbolic_memory import working")
        
        # Test SymbolicMemory class
        sym_mem = symbolic_memory.SymbolicMemory("test_temp")
        print("✅ SymbolicMemory instantiation working")
    except Exception as e:
        print(f"❌ symbolic_memory test failed: {e}")
        return False
    
    # Test parser.parse_text
    try:
        import parser as P_Parser
        
        if hasattr(P_Parser, 'parse_text'):
            result = P_Parser.parse_text("test text")
            print("✅ parser.parse_text working")
        else:
            print("❌ parser.parse_text still missing")
            return False
    except Exception as e:
        print(f"❌ parser.parse_text test failed: {e}")
        return False
    
    # Test unified memory integration
    try:
        from unified_memory import get_unified_memory
        memory = get_unified_memory()
        
        # Test basic operation
        test_item = {"text": "repair test", "repair": True}
        memory.store_decision(test_item, "FOLLOW_LOGIC")
        
        counts = memory.get_memory_counts()
        print(f"✅ Unified memory integration working: {counts['total']} total items")
        
    except Exception as e:
        print(f"❌ Unified memory test failed: {e}")
        return False
    
    return True

def run_final_diagnostic():
    """Run the diagnostic again to confirm fixes."""
    print("\n🔍 Running final diagnostic...")
    
    try:
        from system_health_diagnostic import SystemHealthDiagnostic
        diagnostic = SystemHealthDiagnostic()
        diagnostic.run_full_diagnostic()
    except Exception as e:
        print(f"❌ Could not run diagnostic: {e}")

def main():
    """Main repair function."""
    print("🛠️ SYSTEM REPAIR SCRIPT")
    print("=" * 40)
    
    print("\n1️⃣ Repairing parser interface...")
    if not repair_parser_interface():
        print("❌ Failed to repair parser interface")
        return False
    
    print("\n2️⃣ symbolic_memory.py already created ✅")
    
    print("\n3️⃣ Testing repairs...")
    if not test_repairs():
        print("❌ Repair verification failed")
        return False
    
    print("\n🎉 SYSTEM REPAIRS COMPLETED SUCCESSFULLY!")
    print("\nRepaired issues:")
    print("   ✅ Created missing symbolic_memory.py")
    print("   ✅ Added missing parse_text function to parser.py")
    print("   ✅ Verified unified memory integration")
    
    # Run final diagnostic
    run_final_diagnostic()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)