# system_orchestrator.py - Unified System Management Hub
"""
Unified System Orchestrator - Consolidates system management functionality from:
- run_system.py: System startup and quick access commands
- unified_orchestration.py: Comprehensive orchestration and utilities
- master_integration_system.py: Integration cycles and data utilization
- system_health_diagnostic.py: Health checking and diagnostics
- system_repair.py: System repair and fixes
- talk_to_ai.py: Interactive AI conversation interface

This replaces multiple orchestration files with a single unified management hub
while keeping main.py as a separate entry point.
"""

import asyncio
import uuid
import json
import sys
import os
import time
import traceback
import threading
import hashlib
import shutil
import re
import argparse
import logging
import importlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable, Set, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, Counter

# Core system imports with graceful fallbacks
try:
    import numpy as np
except ImportError:
    np = None

# ============================================================================
# SYSTEM MODES AND ENUMS
# ============================================================================

class SystemMode(Enum):
    """System operation modes"""
    AUTONOMOUS = "autonomous"
    INTERACTIVE = "interactive" 
    LEARNING = "learning"
    MAINTENANCE = "maintenance"
    TESTING = "testing"
    MIGRATION = "migration"
    INTEGRATION = "integration"
    HEALTH_CHECK = "health_check"
    REPAIR = "repair"

class SystemStatus(Enum):
    """System health status"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"

# ============================================================================
# CONFIGURATION MANAGEMENT (from unified_orchestration.py)
# ============================================================================

class Config:
    """
    Centralized configuration management for the Autonomous Dual-Brain AI System
    Handles environment variables, paths, thresholds, and system settings
    """
    
    # Environment variables with defaults
    DATA_DIR = os.getenv('AUTONOMY_DATA_DIR', './data')
    LOG_LEVEL = os.getenv('AUTONOMY_LOG_LEVEL', 'INFO')
    CACHE_TTL = int(os.getenv('AUTONOMY_CACHE_TTL', '300'))  # 5 minutes
    MAX_SESSIONS = int(os.getenv('AUTONOMY_MAX_SESSIONS', '100'))
    
    # Processing thresholds
    MIGRATION_THRESHOLD = float(os.getenv('MIGRATION_THRESHOLD', '0.8'))
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.6'))
    QUARANTINE_THRESHOLD = float(os.getenv('QUARANTINE_THRESHOLD', '0.8'))
    
    # Model settings
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    MAX_EMBEDDING_CACHE = int(os.getenv('MAX_EMBEDDING_CACHE', '1000'))
    
    # File paths
    UNIFIED_MEMORY_PATH = Path(DATA_DIR) / "unified_memory"
    SYMBOL_SYSTEM_PATH = Path(DATA_DIR) / "symbol_system"
    LOGS_PATH = Path(DATA_DIR) / "logs"
    CACHE_PATH = Path(DATA_DIR) / "cache"
    
    # Feature flags
    ENABLE_ALPHAWALL = os.getenv('ENABLE_ALPHAWALL', 'True').lower() == 'true'
    ENABLE_AUTONOMOUS_LEARNING = os.getenv('ENABLE_AUTONOMOUS_LEARNING', 'True').lower() == 'true'
    ENABLE_MEMORY_EVOLUTION = os.getenv('ENABLE_MEMORY_EVOLUTION', 'True').lower() == 'true'
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all necessary directories exist"""
        for path_attr in ['UNIFIED_MEMORY_PATH', 'SYMBOL_SYSTEM_PATH', 'LOGS_PATH', 'CACHE_PATH']:
            path = getattr(cls, path_attr)
            path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_data_paths(cls) -> Dict[str, Path]:
        """Get all important data paths"""
        return {
            'data_dir': Path(cls.DATA_DIR),
            'memory': cls.UNIFIED_MEMORY_PATH,
            'symbols': cls.SYMBOL_SYSTEM_PATH,
            'logs': cls.LOGS_PATH,
            'cache': cls.CACHE_PATH
        }

# ============================================================================
# DATA MANAGEMENT LAYER (from unified_orchestration.py)
# ============================================================================

class DataManager:
    """
    Singleton data manager that provides:
    - Centralized access to all data files
    - In-memory caching with TTL
    - Thread-safe operations
    - Schema validation
    - Transaction support with rollback
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.config = Config()
        self.data_dir = Path(self.config.DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Thread-safe cache with TTL
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_lock = threading.RLock()
        
        # Transaction support
        self._transactions = {}
        
        # Change notifications
        self._change_callbacks = defaultdict(list)
        
        print(f"📊 DataManager initialized with data directory: {self.data_dir}")
    
    def get_json_data(self, filename: str, default_value=None, use_cache: bool = True) -> Any:
        """Get JSON data with caching and error handling"""
        file_path = self.data_dir / filename
        
        # Check cache first
        if use_cache:
            with self._cache_lock:
                cache_key = str(file_path)
                if cache_key in self._cache:
                    cache_time = self._cache_timestamps.get(cache_key, 0)
                    if time.time() - cache_time < self.config.CACHE_TTL:
                        return self._cache[cache_key]
        
        # Load from file
        try:
            if file_path.exists() and file_path.stat().st_size > 0:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Update cache
                if use_cache:
                    with self._cache_lock:
                        self._cache[str(file_path)] = data
                        self._cache_timestamps[str(file_path)] = time.time()
                
                return data
            else:
                return default_value if default_value is not None else {}
                
        except (json.JSONDecodeError, OSError) as e:
            print(f"⚠️ Error loading {filename}: {e}")
            return default_value if default_value is not None else {}
    
    def save_json_data(self, filename: str, data: Any, atomic: bool = True) -> bool:
        """Save JSON data with atomic write and cache update"""
        file_path = self.data_dir / filename
        
        try:
            if atomic:
                # Atomic write using temporary file
                temp_path = file_path.with_suffix('.tmp')
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Atomic rename
                temp_path.replace(file_path)
            else:
                # Direct write
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Update cache
            with self._cache_lock:
                self._cache[str(file_path)] = data
                self._cache_timestamps[str(file_path)] = time.time()
            
            # Notify change callbacks
            self._notify_change_callbacks(filename, data)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
            return False
    
    def _notify_change_callbacks(self, filename: str, data: Any):
        """Notify registered callbacks about data changes"""
        callbacks = self._change_callbacks.get(filename, [])
        for callback in callbacks:
            try:
                callback(filename, data)
            except Exception as e:
                print(f"⚠️ Error in change callback: {e}")
    
    def register_change_callback(self, filename: str, callback: Callable):
        """Register a callback for when a file changes"""
        self._change_callbacks[filename].append(callback)
    
    def clear_cache(self, filename: str = None):
        """Clear cache for specific file or all files"""
        with self._cache_lock:
            if filename:
                file_path = str(self.data_dir / filename)
                self._cache.pop(file_path, None)
                self._cache_timestamps.pop(file_path, None)
            else:
                self._cache.clear()
                self._cache_timestamps.clear()
    
    def get_file_stats(self) -> Dict[str, Dict]:
        """Get statistics about all data files"""
        stats = {}
        
        for file_path in self.data_dir.glob("*.json"):
            try:
                file_stat = file_path.stat()
                stats[file_path.name] = {
                    'size_bytes': file_stat.st_size,
                    'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                    'cached': str(file_path) in self._cache
                }
            except Exception as e:
                stats[file_path.name] = {'error': str(e)}
        
        return stats

# ============================================================================
# SAFE MODULE LOADING (from unified_orchestration.py)
# ============================================================================

class SafeModuleLoader:
    """Safe module loading with fallback handling"""
    
    def __init__(self):
        self.core_modules = {}
        self.optional_modules = {}
        self.failed_imports = []
    
    def safe_import(self, module_name: str, is_core: bool = True, fallback=None):
        """Safely import modules with fallback handling"""
        try:
            module = importlib.import_module(module_name)
            if is_core:
                self.core_modules[module_name] = module
            else:
                self.optional_modules[module_name] = module
            return module
        except ImportError as e:
            self.failed_imports.append((module_name, str(e)))
            if is_core:
                print(f"⚠️ Core module {module_name} not available: {e}")
                self.core_modules[module_name] = fallback
            else:
                print(f"📝 Optional module {module_name} not available: {e}")
                self.optional_modules[module_name] = fallback
            return fallback
        except Exception as e:
            print(f"❌ Error importing {module_name}: {e}")
            self.failed_imports.append((module_name, str(e)))
            return fallback
    
    def get_import_status(self) -> Dict[str, Any]:
        """Get status of all import attempts"""
        total_attempts = len(self.core_modules) + len(self.optional_modules) + len(self.failed_imports)
        success_count = len(self.core_modules) + len(self.optional_modules)
        
        return {
            'core_modules': list(self.core_modules.keys()),
            'optional_modules': list(self.optional_modules.keys()),
            'failed_imports': self.failed_imports,
            'success_rate': success_count / total_attempts if total_attempts > 0 else 0
        }

# ============================================================================
# SYSTEM HEALTH DIAGNOSTIC (from system_health_diagnostic.py)
# ============================================================================

class SystemHealthDiagnostic:
    """Comprehensive diagnostic tool to find what needs repair"""
    
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)
        self.critical_issues = []
        self.broken_imports = []
        self.missing_files = []
        self.runtime_failures = []
        self.dependency_issues = []
        self.config_problems = []
        
    def run_full_diagnostic(self) -> Dict[str, Any]:
        """Run complete system health check"""
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
        return self._generate_repair_report()
        
    def _check_critical_imports(self):
        """Check if critical system imports are working"""
        print("\n🔍 Checking Critical System Imports...")
        
        critical_modules = [
            "unified_memory",
            "creative_engine", 
            "memory_analytics",
            "decision_history",
            "symbolic_memory",
            "experience_memory",
            "episodic_memory",
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
        """Check if core system files exist and are readable"""
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
                        with open(full_path, 'r') as f:
                            json.load(f)
                    elif file_path.endswith('.py'):
                        with open(full_path, 'r') as f:
                            content = f.read()
                            if len(content) < 100:  # Suspiciously small
                                print(f"   ⚠️ SUSPICIOUSLY SMALL: {file_path} ({len(content)} chars)")
                    print(f"   ✅ {file_path}")
                except Exception as e:
                    print(f"   ❌ CORRUPTED: {file_path} - {e}")
                    self.critical_issues.append({"type": "file_corruption", "file": file_path, "error": str(e)})
    
    def _check_unified_memory_system(self):
        """Test unified memory system functionality"""
        print("\n🧠 Testing Unified Memory System...")
        
        try:
            unified_memory = importlib.import_module('unified_memory')
            memory = unified_memory.get_unified_memory()
            
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
        """Test consciousness system components"""
        print("\n🎭 Testing Consciousness Systems...")
        
        consciousness_systems = [
            ("creative_engine", "CreativeEngine"),
            ("symbolic_memory", "SymbolicMemory"), 
            ("episodic_memory", "EpisodicMemorySystem"),
            ("experience_memory", "ExperienceMemory"),
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
        """Check data file integrity and structure"""
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
                    with open(full_path, 'r') as f:
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
        """Check configuration and settings files"""
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
        """Test core system functionality end-to-end"""
        print("\n🔧 Testing Core Functionality...")
        
        try:
            # Test processing pipeline
            unified_memory = importlib.import_module('unified_memory')
            parser = importlib.import_module('parser')
            
            memory = unified_memory.get_unified_memory()
            
            # Test text processing
            test_text = "This is a diagnostic test for the AI consciousness system."
            
            try:
                parsed = parser.parse_text(test_text)
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
    
    def _generate_repair_report(self) -> Dict[str, Any]:
        """Generate comprehensive repair report"""
        print("\n" + "=" * 60)
        print("🛠️ SYSTEM REPAIR REPORT")
        print("=" * 60)
        
        total_issues = (len(self.critical_issues) + len(self.broken_imports) + 
                       len(self.missing_files) + len(self.runtime_failures) + 
                       len(self.dependency_issues) + len(self.config_problems))
        
        if total_issues == 0:
            print("🎉 EXCELLENT: No critical issues found! System is healthy.")
            return {"status": SystemStatus.HEALTHY, "issues": 0, "details": {}}
        
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
        
        # Determine status
        if self.critical_issues or any("unified_memory" in str(issue) for issue in self.broken_imports):
            status = SystemStatus.CRITICAL
        elif self.broken_imports or self.missing_files:
            status = SystemStatus.WARNING
        else:
            status = SystemStatus.HEALTHY
        
        print("\n" + "=" * 60)
        
        return {
            "status": status,
            "issues": total_issues,
            "details": {
                "critical_issues": self.critical_issues,
                "broken_imports": self.broken_imports,
                "missing_files": self.missing_files,
                "runtime_failures": self.runtime_failures,
                "config_problems": self.config_problems
            }
        }

# ============================================================================
# SYSTEM REPAIR (from system_repair.py)
# ============================================================================

class SystemRepair:
    """System repair utilities"""
    
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)
        
    def repair_parser_interface(self) -> bool:
        """Add missing parse_text function to parser.py for backward compatibility"""
        parser_file = self.project_dir / "parser.py"
        
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
    
    def test_repairs(self) -> bool:
        """Test that the repairs worked"""
        print("\n🧪 Testing repairs...")
        
        # Test symbolic_memory import
        try:
            symbolic_memory = importlib.import_module('symbolic_memory')
            print("✅ symbolic_memory import working")
            
            # Test SymbolicMemory class
            sym_mem = symbolic_memory.SymbolicMemory("test_temp")
            print("✅ SymbolicMemory instantiation working")
        except Exception as e:
            print(f"❌ symbolic_memory test failed: {e}")
            return False
        
        # Test parser.parse_text
        try:
            parser = importlib.import_module('parser')
            
            if hasattr(parser, 'parse_text'):
                result = parser.parse_text("test text")
                print("✅ parser.parse_text working")
            else:
                print("❌ parser.parse_text still missing")
                return False
        except Exception as e:
            print(f"❌ parser.parse_text test failed: {e}")
            return False
        
        # Test unified memory integration
        try:
            unified_memory = importlib.import_module('unified_memory')
            memory = unified_memory.get_unified_memory()
            
            # Test basic operation
            test_item = {"text": "repair test", "repair": True}
            memory.store_decision(test_item, "FOLLOW_LOGIC")
            
            counts = memory.get_memory_counts()
            print(f"✅ Unified memory integration working: {counts['total']} total items")
            
        except Exception as e:
            print(f"❌ Unified memory test failed: {e}")
            return False
        
        return True
    
    def run_repairs(self, diagnostic_result: Dict[str, Any]) -> bool:
        """Run system repairs based on diagnostic results"""
        print("🛠️ SYSTEM REPAIR SCRIPT")
        print("=" * 40)
        
        if diagnostic_result["status"] == SystemStatus.HEALTHY:
            print("✅ No repairs needed - system is healthy!")
            return True
        
        print("\n1️⃣ Repairing parser interface...")
        if not self.repair_parser_interface():
            print("❌ Failed to repair parser interface")
            return False
        
        print("\n2️⃣ Testing repairs...")
        if not self.test_repairs():
            print("❌ Repair verification failed")
            return False
        
        print("\n🎉 SYSTEM REPAIRS COMPLETED SUCCESSFULLY!")
        return True

# ============================================================================
# INTERACTIVE AI INTERFACE (from talk_to_ai.py)
# ============================================================================

class InteractiveAI:
    """Interactive AI conversation interface"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.module_loader = SafeModuleLoader()
        self.conversation_history = []
        self.verbose_mode = False
        
        # Load required components safely
        self._load_components()
        
    def _load_components(self):
        """Load AI components with safe imports"""
        print("🔧 Loading AI components...")
        
        # Core components
        self.alphawall = self.module_loader.safe_import('alphawall', is_core=False)
        self.quarantine = self.module_loader.safe_import('adaptive_quarantine_layer', is_core=False)
        self.warfare_detector = self.module_loader.safe_import('linguistic_warfare', is_core=False)
        self.processing_nodes = self.module_loader.safe_import('processing_nodes', is_core=False)
        self.unified_memory = self.module_loader.safe_import('unified_memory', is_core=False)
        
        print(f"🔧 Component loading completed")
    
    def process_and_respond(self, user_input: str) -> str:
        """Complete pipeline: process input and generate response"""
        try:
            # Basic response generation for now
            # This would integrate with the full processing pipeline
            
            # Simple content-based responses
            if user_input.lower() in ['hello', 'hi', 'hey']:
                return "Hello! I'm here to help you explore ideas through both logical analysis and symbolic understanding. What would you like to discuss?"
            
            if any(word in user_input.lower() for word in ['what', 'how', 'why', 'explain']):
                return f"That's an interesting question about '{user_input}'. Let me think about this from both logical and symbolic perspectives."
            
            return "I'm processing your message and considering multiple perspectives. What specific aspect would you like to explore further?"
            
        except Exception as e:
            return f"I apologize, there was an error processing your input: {str(e)}"
    
    def run_interactive_session(self):
        """Run interactive conversation session"""
        print("\n" + "="*60)
        print("🧠 AI SYSTEM - Interactive Mode")
        print("="*60)
        
        print("\nCommands:")
        print("  'exit' or 'quit' - End session")
        print("  'verbose' - Toggle verbose output")
        print("  'help' - Show available commands")
        
        print("-"*60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🗣️  You: ").strip()
                
                # Check for commands
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Thank you for the conversation. Goodbye!")
                    break
                    
                elif user_input.lower() == 'verbose':
                    self.verbose_mode = not self.verbose_mode
                    print(f"🔧 Verbose mode: {'ON' if self.verbose_mode else 'OFF'}")
                    continue
                    
                elif user_input.lower() == 'help':
                    print("\n📋 Available Commands:")
                    print("  exit/quit  - End conversation")
                    print("  verbose    - Toggle detailed output")
                    print("  help       - Show this help")
                    continue
                    
                elif not user_input:
                    continue
                
                # Process input and generate response
                print("-"*60)
                response = self.process_and_respond(user_input)
                
                # Display response
                print(f"\n🤖 AI: {response}")
                
                # Add to conversation history
                self.conversation_history.append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'input': user_input,
                    'response': response
                })
                
                # Keep history manageable
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Type 'exit' to quit properly.")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                if self.verbose_mode:
                    traceback.print_exc()

# ============================================================================
# MAIN UNIFIED SYSTEM ORCHESTRATOR
# ============================================================================

class UnifiedSystemOrchestrator:
    """
    Main unified system orchestrator that consolidates all system management functionality
    """
    
    def __init__(self, data_dir: str = "data"):
        self.config = Config()
        self.config.ensure_directories()
        
        # Initialize core subsystems
        self.data_manager = DataManager()
        self.module_loader = SafeModuleLoader()
        self.health_diagnostic = SystemHealthDiagnostic()
        self.system_repair = SystemRepair()
        self.interactive_ai = InteractiveAI(data_dir)
        
        # System state
        self.current_mode = None
        self.startup_time = datetime.utcnow()
        self.session_history = []
        
        print(f"🌟 Unified System Orchestrator initialized")
    
    def start_system(self, mode: SystemMode, **kwargs) -> Dict[str, Any]:
        """Start the system in specified mode"""
        try:
            self.current_mode = mode
            result = {
                'mode': mode.value,
                'status': 'started',
                'timestamp': datetime.utcnow().isoformat(),
                'kwargs': kwargs
            }
            
            print(f"🚀 Starting system in {mode.value} mode...")
            
            if mode == SystemMode.AUTONOMOUS:
                # Load unified orchestration system
                unified_orchestration = self.module_loader.safe_import('unified_orchestration', is_core=False)
                if unified_orchestration:
                    orchestrator = unified_orchestration.get_unified_orchestration_system(self.config.DATA_DIR)
                    result['message'] = "Autonomous mode activated with unified orchestration"
                    result['autonomous_active'] = True
                else:
                    result['message'] = "Autonomous mode activated (simplified)"
                    result['autonomous_active'] = True
                
            elif mode == SystemMode.INTERACTIVE:
                result['message'] = "Interactive mode activated"
                result['interactive_active'] = True
                
            elif mode == SystemMode.LEARNING:
                result['message'] = "Learning mode activated"
                result['learning_active'] = True
                
            elif mode == SystemMode.HEALTH_CHECK:
                result = self.run_health_check()
                
            elif mode == SystemMode.REPAIR:
                result = self.run_system_repair()
                
            elif mode == SystemMode.MAINTENANCE:
                result['message'] = "Maintenance mode activated"
                
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'mode': mode.value if mode else 'unknown'
            }
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run comprehensive system health check"""
        print("🏥 Running system health diagnostic...")
        
        try:
            diagnostic_result = self.health_diagnostic.run_full_diagnostic()
            
            return {
                'status': 'completed',
                'mode': 'health_check',
                'timestamp': datetime.utcnow().isoformat(),
                'health_status': diagnostic_result['status'].value,
                'issues_found': diagnostic_result['issues'],
                'details': diagnostic_result['details'],
                'message': f"Health check completed - Status: {diagnostic_result['status'].value}"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'mode': 'health_check',
                'error': str(e),
                'message': "Health check failed"
            }
    
    def run_system_repair(self) -> Dict[str, Any]:
        """Run system repair based on health diagnostic"""
        print("🛠️ Running system repair...")
        
        try:
            # First run diagnostic
            diagnostic_result = self.health_diagnostic.run_full_diagnostic()
            
            # Then run repairs
            repair_success = self.system_repair.run_repairs(diagnostic_result)
            
            return {
                'status': 'completed' if repair_success else 'failed',
                'mode': 'repair',
                'timestamp': datetime.utcnow().isoformat(),
                'repair_success': repair_success,
                'issues_before': diagnostic_result['issues'],
                'message': "System repair completed successfully" if repair_success else "System repair failed"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'mode': 'repair',
                'error': str(e),
                'message': "System repair encountered an error"
            }
    
    def run_interactive_session(self):
        """Run interactive AI conversation session"""
        self.interactive_ai.run_interactive_session()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            # Get import status
            import_status = self.module_loader.get_import_status()
            
            # Get file statistics
            file_stats = self.data_manager.get_file_stats()
            
            # Calculate uptime
            uptime_seconds = (datetime.utcnow() - self.startup_time).total_seconds()
            uptime_hours = uptime_seconds / 3600
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'system_health': 'operational',
                'health': 'healthy',
                'current_mode': self.current_mode.value if self.current_mode else 'none',
                'uptime_hours': uptime_hours,
                'import_status': import_status,
                'file_statistics': file_stats,
                'session_count': len(self.session_history),
                'config': {
                    'data_dir': str(self.config.DATA_DIR),
                    'cache_ttl': self.config.CACHE_TTL,
                    'confidence_threshold': self.config.CONFIDENCE_THRESHOLD
                },
                'data_dir': str(self.config.DATA_DIR)
            }
            
        except Exception as e:
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'system_health': 'error',
                'error': str(e)
            }
    
    def execute_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute system commands"""
        try:
            result = {
                'command': command,
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'executed'
            }
            
            if command == 'status':
                result.update(self.get_system_status())
                
            elif command == 'health':
                health_result = self.run_health_check()
                result.update(health_result)
                
            elif command == 'repair':
                repair_result = self.run_system_repair()
                result.update(repair_result)
                
            elif command == 'interactive':
                result['message'] = "Starting interactive session..."
                result['action'] = 'start_interactive'
                
            elif command == 'chat':
                result['message'] = "Starting chat session..."
                result['action'] = 'start_chat'
                
            else:
                result['status'] = 'unknown_command'
                result['message'] = f"Unknown command: {command}"
                
            return result
            
        except Exception as e:
            return {
                'command': command,
                'status': 'error',
                'error': str(e)
            }
    
    def stop_system(self) -> Dict[str, Any]:
        """Stop the system gracefully"""
        try:
            return {
                'status': 'stopped',
                'timestamp': datetime.utcnow().isoformat(),
                'uptime_hours': (datetime.utcnow() - self.startup_time).total_seconds() / 3600,
                'message': "System stopped gracefully"
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

# Global instance for ease of use
_global_orchestrator = None

def get_system_orchestrator(data_dir: str = "data") -> UnifiedSystemOrchestrator:
    """Get or create the global system orchestrator"""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = UnifiedSystemOrchestrator(data_dir)
    return _global_orchestrator

# Convenience functions for common operations
def run_health_check(data_dir: str = "data") -> Dict[str, Any]:
    """Run system health check"""
    orchestrator = get_system_orchestrator(data_dir)
    return orchestrator.run_health_check()

def run_system_repair(data_dir: str = "data") -> Dict[str, Any]:
    """Run system repair"""
    orchestrator = get_system_orchestrator(data_dir)
    return orchestrator.run_system_repair()

def start_interactive_session(data_dir: str = "data"):
    """Start interactive AI session"""
    orchestrator = get_system_orchestrator(data_dir)
    orchestrator.run_interactive_session()

def get_system_status(data_dir: str = "data") -> Dict[str, Any]:
    """Get system status"""
    orchestrator = get_system_orchestrator(data_dir)
    return orchestrator.get_system_status()

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Unified System Orchestrator')
    parser.add_argument('command', nargs='?', default='status', 
                       choices=['start', 'stop', 'status', 'health', 'repair', 'interactive', 'chat'],
                       help='Command to execute')
    parser.add_argument('--mode', choices=[mode.value for mode in SystemMode], 
                       default='interactive', help='System mode for start command')
    parser.add_argument('--data-dir', default='data', help='Data directory path')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = get_system_orchestrator(args.data_dir)
    
    # Execute command
    if args.command == 'start':
        mode = SystemMode(args.mode)
        result = orchestrator.start_system(mode)
        print(json.dumps(result, indent=2))
        
        # If interactive mode, start the session
        if mode == SystemMode.INTERACTIVE:
            orchestrator.run_interactive_session()
            
    elif args.command == 'stop':
        result = orchestrator.stop_system()
        print(json.dumps(result, indent=2))
        
    elif args.command == 'status':
        status = orchestrator.get_system_status()
        print(json.dumps(status, indent=2))
        
    elif args.command == 'health':
        health_result = orchestrator.run_health_check()
        print(json.dumps(health_result, indent=2))
        
    elif args.command == 'repair':
        repair_result = orchestrator.run_system_repair()
        print(json.dumps(repair_result, indent=2))
        
    elif args.command == 'interactive':
        orchestrator.run_interactive_session()
        
    elif args.command == 'chat':
        orchestrator.run_interactive_session()

if __name__ == "__main__":
    main()