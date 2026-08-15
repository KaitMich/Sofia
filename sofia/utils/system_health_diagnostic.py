#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM HEALTH DIAGNOSTIC

This script identifies what actually needs to be REPAIRED across the entire AI consciousness system.
Goes beyond review to find broken functionality, missing dependencies, and critical issues.
"""

import os
import sys
import importlib
import traceback
import json
from pathlib import Path
from datetime import datetime

class SystemHealthDiagnostic:
    """Comprehensive diagnostic tool to find what needs repair."""
    
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)
        self.critical_issues = []
        self.broken_imports = []
        self.missing_files = []
        self.runtime_failures = []
        self.dependency_issues = []
        self.config_problems = []
        
    def run_full_diagnostic(self):
        """Run complete system health check."""
        print("🏥 COMPREHENSIVE SYSTEM HEALTH DIAGNOSTIC")
        print("=" * 60)
        print("Identifying what actually needs REPAIR...")
        
        # Core system checks
        self._check_critical_imports()
        self._check_core_file_integrity()
        self._check_unified_memory_system()
        self._check_consciousness_systems()
        self._check_data_integrity()
        self._check_configuration_files()
        self._test_core_functionality()
        
        # Generate repair report
        self._generate_repair_report()
        
    def _check_critical_imports(self):
        """Check if critical system imports are working."""
        print("\n🔍 Checking Critical System Imports...")
        
        critical_modules = [
            "unified_memory",
            "creative_engine", 
            "memory_analytics",
            "decision_history",
            "symbolic_memory",
            "CONSCIOUSNESS_MEMORY",
            "learning_progression_tracker",
            "identity_core",
            "emotion_handler",
            "parser",
            "processing_nodes"
        ]
        
        for module in critical_modules:
            try:
                importlib.import_module(module)
                print(f"   ✅ {module}")
            except ImportError as e:
                print(f"   ❌ {module}: {e}")
                self.broken_imports.append({"module": module, "error": str(e)})
            except Exception as e:
                print(f"   ⚠️ {module}: {e}")
                self.critical_issues.append({"type": "import_error", "module": module, "error": str(e)})
    
    def _check_core_file_integrity(self):
        """Check if core system files exist and are readable."""
        print("\n📁 Checking Core File Integrity...")
        
        critical_files = [
            "unified_memory.py",
            "decision_history.py", 
            "creative_engine.py",
            "memory_analytics.py",
            "data/logic_memory.json",
            "data/symbolic_memory.json",
            "data/bridge_memory.json",
            "data/vector_memory.json"
        ]
        
        for file_path in critical_files:
            full_path = self.project_dir / file_path
            if not full_path.exists():
                print(f"   ❌ MISSING: {file_path}")
                self.missing_files.append(file_path)
            elif not full_path.is_file():
                print(f"   ⚠️ NOT A FILE: {file_path}")
                self.critical_issues.append({"type": "file_integrity", "file": file_path, "issue": "not_a_file"})
            else:
                try:
                    if file_path.endswith('.json'):
                        with open(full_path, 'r', encoding='utf-8') as f:
                            json.load(f)
                    elif file_path.endswith('.py'):
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if len(content) < 100:  # Suspiciously small
                                print(f"   ⚠️ SUSPICIOUSLY SMALL: {file_path} ({len(content)} chars)")
                    print(f"   ✅ {file_path}")
                except Exception as e:
                    print(f"   ❌ CORRUPTED: {file_path} - {e}")
                    self.critical_issues.append({"type": "file_corruption", "file": file_path, "error": str(e)})
    
    def _check_unified_memory_system(self):
        """Test unified memory system functionality."""
        print("\n🧠 Testing Unified Memory System...")
        
        try:
            from sofia.core.unified_memory import get_unified_memory
            memory = get_unified_memory()
            
            # Test basic operations
            test_item = {"text": "diagnostic test", "test": True}
            
            # Test storage
            memory.store_decision(test_item, "FOLLOW_LOGIC")
            print("   ✅ Memory storage working")
            
            # Test retrieval  
            counts = memory.get_memory_counts()
            print(f"   ✅ Memory retrieval working: {counts}")
            
            # Test vector operations
            try:
                result = memory.store_vector("test vector storage", confidence=0.8)
                if result.get("status") == "success":
                    print("   ✅ Vector storage working")
                else:
                    print(f"   ⚠️ Vector storage issue: {result}")
            except Exception as e:
                print(f"   ❌ Vector storage failed: {e}")
                self.runtime_failures.append({"system": "unified_memory_vectors", "error": str(e)})
            
        except Exception as e:
            print(f"   ❌ CRITICAL: Unified memory system failed: {e}")
            self.critical_issues.append({"type": "core_system_failure", "system": "unified_memory", "error": str(e)})
    
    def _check_consciousness_systems(self):
        """Test consciousness system components."""
        print("\n🎭 Testing Consciousness Systems...")
        
        consciousness_systems = [
            ("creative_engine", "CreativeEngine"),
            ("symbolic_memory", "SymbolicMemory"), 
            ("CONSCIOUSNESS_MEMORY", "EpisodicMemorySystem"),
            ("CONSCIOUSNESS_MEMORY", "ExperienceMemory"),
            ("identity_core", "get_identity_core")
        ]
        
        for module_name, class_name in consciousness_systems:
            try:
                module = importlib.import_module(module_name)
                
                if class_name == "get_identity_core":
                    # Special case - function not class
                    identity = module.get_identity_core()
                    print(f"   ✅ {module_name}: Identity core accessible")
                else:
                    # Try to instantiate the class
                    cls = getattr(module, class_name)
                    if class_name in ["CreativeEngine", "SymbolicMemory", "ExperienceMemory"]:
                        # These need data_dir parameter
                        instance = cls("temp_test_dir")
                    else:
                        instance = cls()
                    print(f"   ✅ {module_name}: {class_name} instantiable")
                    
            except Exception as e:
                print(f"   ❌ {module_name}: {e}")
                self.runtime_failures.append({"system": module_name, "class": class_name, "error": str(e)})
    
    def _check_data_integrity(self):
        """Check data file integrity and structure."""
        print("\n📊 Checking Data Integrity...")
        
        data_files = [
            ("data/logic_memory.json", "list"),
            ("data/symbolic_memory.json", "list"), 
            ("data/bridge_memory.json", "list"),
            ("data/vector_memory.json", "list"),
            ("data/trail_log.json", "list")
        ]
        
        for file_path, expected_type in data_files:
            full_path = self.project_dir / file_path
            try:
                if full_path.exists():
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if expected_type == "list" and isinstance(data, list):
                        print(f"   ✅ {file_path}: Valid list with {len(data)} items")
                    elif expected_type == "dict" and isinstance(data, dict):
                        print(f"   ✅ {file_path}: Valid dict with {len(data)} keys")
                    else:
                        print(f"   ⚠️ {file_path}: Unexpected format (expected {expected_type}, got {type(data).__name__})")
                        self.config_problems.append({"file": file_path, "issue": "wrong_format", "expected": expected_type, "actual": type(data).__name__})
                else:
                    print(f"   ⚠️ {file_path}: File missing (will be created on first use)")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ {file_path}: Invalid JSON - {e}")
                self.critical_issues.append({"type": "data_corruption", "file": file_path, "error": str(e)})
            except Exception as e:
                print(f"   ❌ {file_path}: Read error - {e}")
                self.critical_issues.append({"type": "data_access", "file": file_path, "error": str(e)})
    
    def _check_configuration_files(self):
        """Check configuration and settings files."""
        print("\n⚙️ Checking Configuration...")
        
        # Check if there are any critical config files
        config_files = [
            "config.json",
            "settings.json", 
            ".env",
            "requirements.txt"
        ]
        
        for config_file in config_files:
            full_path = self.project_dir / config_file
            if full_path.exists():
                print(f"   ✅ {config_file}: Present")
            else:
                print(f"   ℹ️ {config_file}: Not found (may not be required)")
    
    def _test_core_functionality(self):
        """Test core system functionality end-to-end."""
        print("\n🔧 Testing Core Functionality...")
        
        try:
            # Test processing pipeline
            from sofia.core.unified_memory import get_unified_memory
            from sofia.utils import parser as P_Parser
            
            memory = get_unified_memory()
            
            # Test text processing
            test_text = "This is a diagnostic test for the AI consciousness system."
            
            try:
                parsed = P_Parser.parse_text(test_text)
                print("   ✅ Text parsing working")
                
                # Test storage in memory
                if parsed and 'logic_score' in parsed and 'symbolic_score' in parsed:
                    if parsed['logic_score'] > parsed['symbolic_score']:
                        decision = "FOLLOW_LOGIC"
                    elif parsed['symbolic_score'] > parsed['logic_score']:
                        decision = "FOLLOW_SYMBOLIC"
                    else:
                        decision = "FOLLOW_HYBRID"
                    
                    memory.store_decision(parsed, decision)
                    print("   ✅ End-to-end processing pipeline working")
                else:
                    print("   ⚠️ Parser output missing required fields")
                    self.runtime_failures.append({"system": "parser", "error": "missing_required_fields"})
                    
            except Exception as e:
                print(f"   ❌ Text processing failed: {e}")
                self.runtime_failures.append({"system": "text_processing", "error": str(e)})
            
        except Exception as e:
            print(f"   ❌ CRITICAL: Core functionality test failed: {e}")
            self.critical_issues.append({"type": "core_functionality", "error": str(e)})
    
    def _generate_repair_report(self):
        """Generate comprehensive repair report."""
        print("\n" + "=" * 60)
        print("🛠️ SYSTEM REPAIR REPORT")
        print("=" * 60)
        
        total_issues = (len(self.critical_issues) + len(self.broken_imports) + 
                       len(self.missing_files) + len(self.runtime_failures) + 
                       len(self.dependency_issues) + len(self.config_problems))
        
        if total_issues == 0:
            print("🎉 EXCELLENT: No critical issues found! System is healthy.")
            return
        
        print(f"🚨 TOTAL ISSUES FOUND: {total_issues}")
        
        if self.critical_issues:
            print(f"\n❌ CRITICAL ISSUES ({len(self.critical_issues)}):")
            for issue in self.critical_issues:
                print(f"   • {issue['type']}: {issue.get('system', issue.get('file', 'unknown'))} - {issue['error']}")
        
        if self.broken_imports:
            print(f"\n📦 BROKEN IMPORTS ({len(self.broken_imports)}):")
            for issue in self.broken_imports:
                print(f"   • {issue['module']}: {issue['error']}")
        
        if self.missing_files:
            print(f"\n📁 MISSING FILES ({len(self.missing_files)}):")
            for file in self.missing_files:
                print(f"   • {file}")
        
        if self.runtime_failures:
            print(f"\n⚠️ RUNTIME FAILURES ({len(self.runtime_failures)}):")
            for failure in self.runtime_failures:
                print(f"   • {failure['system']}: {failure['error']}")
        
        if self.config_problems:
            print(f"\n⚙️ CONFIGURATION PROBLEMS ({len(self.config_problems)}):")
            for problem in self.config_problems:
                print(f"   • {problem['file']}: {problem['issue']}")
        
        # Prioritized repair recommendations
        print(f"\n🔧 REPAIR PRIORITIES:")
        
        if any("unified_memory" in str(issue) for issue in self.critical_issues):
            print("   🚨 PRIORITY 1: Fix unified memory system - core system failure")
        
        if self.broken_imports:
            print("   🚨 PRIORITY 1: Fix broken imports - system cannot function")
        
        if self.missing_files:
            print("   ⚠️ PRIORITY 2: Restore missing files")
        
        if self.runtime_failures:
            print("   ⚠️ PRIORITY 2: Fix runtime failures")
        
        if self.config_problems:
            print("   ℹ️ PRIORITY 3: Address configuration issues")
        
        print("\n" + "=" * 60)

def main():
    """Run the diagnostic."""
    diagnostic = SystemHealthDiagnostic()
    diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    main()