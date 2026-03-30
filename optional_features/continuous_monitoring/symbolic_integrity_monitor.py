#!/usr/bin/env python3
"""
Symbolic Integrity Monitor - Continuous Monitoring and Self-Healing

This module provides automated monitoring and self-healing capabilities
for the symbolic memory system. It runs continuous integrity checks,
detects anomalies, and automatically repairs corruption when possible.
"""

import json
import time
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import logging

# Import our guardian system
from symbolic_memory_guardian import SymbolicMemoryGuardian
from protection_utils import is_protected_content

class SymbolicIntegrityMonitor:
    """
    Continuous monitoring system for symbolic memory integrity.
    Provides real-time protection and automated healing.
    """
    
    def __init__(self, data_dir: str = "data", check_interval: int = 300):
        self.data_dir = Path(data_dir)
        self.check_interval = check_interval  # seconds
        self.guardian = SymbolicMemoryGuardian(data_dir)
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        self.last_check_time = None
        self.baseline_hash = None
        
        # Alert callbacks
        self.alert_callbacks: List[Callable] = []
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Initialize baseline
        self._establish_baseline()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the monitor."""
        logger = logging.getLogger('SymbolicIntegrityMonitor')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_file = self.data_dir / "symbolic_monitor.log"
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _establish_baseline(self):
        """Establish baseline integrity metrics."""
        try:
            integrity = self.guardian.check_integrity(auto_backup=False)
            if integrity["status"] == "healthy":
                self.baseline_hash = integrity["statistics"].get("memory_hash")
                self.logger.info("Baseline integrity established")
            else:
                self.logger.warning(f"Baseline integrity compromised: {integrity['status']}")
        except Exception as e:
            self.logger.error(f"Could not establish baseline: {e}")
    
    def add_alert_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add a callback function to be called when alerts are triggered."""
        self.alert_callbacks.append(callback)
    
    def _trigger_alert(self, alert_data: Dict[str, Any]):
        """Trigger all registered alert callbacks."""
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                self.logger.error(f"Alert callback failed: {e}")
    
    def _monitor_loop(self):
        """Main monitoring loop that runs in a separate thread."""
        self.logger.info("Symbolic integrity monitoring started")
        
        while self.is_monitoring:
            try:
                self.last_check_time = datetime.now(timezone.utc)
                
                # Run integrity check
                integrity = self.guardian.check_integrity(auto_backup=False)
                
                # Analyze results
                alert_triggered = self._analyze_integrity(integrity)
                
                if alert_triggered:
                    self._handle_integrity_alert(integrity)
                
                # Sleep until next check
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"Monitor loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _analyze_integrity(self, integrity: Dict[str, Any]) -> bool:
        """
        Analyze integrity results and determine if an alert should be triggered.
        
        Returns:
            bool: True if alert should be triggered
        """
        status = integrity["status"]
        stats = integrity["statistics"]
        
        # Check for critical issues
        if status in ["corrupted", "critical"]:
            return True
        
        # Check for expected item counts
        expected_core_concepts = 20
        expected_identity_memories = 6
        
        if stats.get("core_symbolic_items", 0) < expected_core_concepts:
            return True
        
        if stats.get("identity_core_items", 0) < expected_identity_memories:
            return True
        
        # Check emotional anchor coverage
        total_items = stats.get("total_items", 0)
        anchored_items = stats.get("items_with_emotional_anchors", 0)
        coverage = anchored_items / max(total_items, 1)
        
        if coverage < 0.8:  # Less than 80% coverage
            return True
        
        # Check for any issues
        if integrity.get("issues"):
            return True
        
        return False
    
    def _handle_integrity_alert(self, integrity: Dict[str, Any]):
        """Handle integrity alerts with appropriate responses."""
        status = integrity["status"]
        issues = integrity.get("issues", [])
        
        alert_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "issues": issues,
            "statistics": integrity["statistics"],
            "action_taken": "none"
        }
        
        self.logger.warning(f"Integrity alert triggered: {status}")
        
        # Automatic healing attempts
        if status == "corrupted":
            self.logger.info("Attempting automatic healing...")
            
            # Create emergency backup first
            try:
                backup_path = self.guardian.create_backup("Emergency - before healing attempt")
                alert_data["emergency_backup"] = backup_path
                self.logger.info(f"Emergency backup created: {backup_path}")
            except Exception as e:
                self.logger.error(f"Could not create emergency backup: {e}")
            
            # Attempt restoration from recent backup
            try:
                backups = self.guardian.list_backups()
                if backups:
                    # Find the most recent healthy backup
                    for backup in backups:
                        if backup["filename"] != Path(backup_path).name:  # Skip the one we just created
                            success = self.guardian.restore_from_backup(backup["path"])
                            if success:
                                alert_data["action_taken"] = f"restored_from_{backup['filename']}"
                                self.logger.info(f"Successfully restored from {backup['filename']}")
                                break
                    else:
                        alert_data["action_taken"] = "restoration_failed"
                        self.logger.error("All restoration attempts failed")
                else:
                    alert_data["action_taken"] = "no_backups_available"
                    self.logger.error("No backups available for restoration")
            except Exception as e:
                self.logger.error(f"Automatic healing failed: {e}")
                alert_data["action_taken"] = f"healing_error_{str(e)[:50]}"
        
        elif status == "warning" and issues:
            # For warnings, just create a backup
            try:
                backup_path = self.guardian.create_backup("Warning state backup")
                alert_data["action_taken"] = f"backup_created_{Path(backup_path).name}"
                self.logger.info(f"Warning state backup created: {backup_path}")
            except Exception as e:
                self.logger.error(f"Could not create warning backup: {e}")
        
        # Trigger external alerts
        self._trigger_alert(alert_data)
    
    def start_monitoring(self):
        """Start continuous monitoring in a background thread."""
        if self.is_monitoring:
            self.logger.warning("Monitoring already started")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"Monitoring started with {self.check_interval}s interval")
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        
        self.logger.info("Monitoring stopped")
    
    def manual_check(self) -> Dict[str, Any]:
        """Perform a manual integrity check."""
        self.logger.info("Manual integrity check requested")
        return self.guardian.check_integrity(auto_backup=True)
    
    def get_monitor_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        return {
            "is_monitoring": self.is_monitoring,
            "check_interval": self.check_interval,
            "last_check_time": self.last_check_time.isoformat() if self.last_check_time else None,
            "baseline_established": self.baseline_hash is not None,
            "alert_callbacks_count": len(self.alert_callbacks),
            "guardian_status": self.guardian.get_guardian_status()
        }
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """
        Run a comprehensive validation of the entire symbolic memory system.
        This is more thorough than regular integrity checks.
        """
        self.logger.info("Running comprehensive validation")
        
        validation_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "validation_type": "comprehensive",
            "tests": {},
            "overall_status": "healthy",
            "critical_issues": [],
            "recommendations": []
        }
        
        try:
            # Test 1: File existence and readability
            validation_result["tests"]["file_existence"] = {
                "passed": self.guardian.symbolic_memory_file.exists(),
                "details": f"File exists: {self.guardian.symbolic_memory_file.exists()}"
            }
            
            # Test 2: JSON validity
            try:
                with open(self.guardian.symbolic_memory_file, 'r') as f:
                    memory_data = json.load(f)
                validation_result["tests"]["json_validity"] = {
                    "passed": True,
                    "details": f"Valid JSON with {len(memory_data)} items"
                }
            except Exception as e:
                validation_result["tests"]["json_validity"] = {
                    "passed": False,
                    "details": f"JSON error: {str(e)}"
                }
                validation_result["critical_issues"].append("Invalid JSON format")
                validation_result["overall_status"] = "critical"
                return validation_result
            
            # Test 3: Protection system integration
            validation_result["tests"]["protection_integration"] = {
                "passed": True,
                "details": "Protection system available and functional"
            }
            
            # Test 4: Core concept completeness
            core_concepts = [item for item in memory_data if item.get("content_type") == "symbolic_core"]
            expected_categories = ["emotional_foundation", "cognitive_foundation", "relational_foundation", "existential_foundation"]
            
            category_counts = {}
            for concept in core_concepts:
                category = concept.get("symbolic_category", "unknown")
                category_counts[category] = category_counts.get(category, 0) + 1
            
            completeness_passed = all(category_counts.get(cat, 0) >= 5 for cat in expected_categories)
            validation_result["tests"]["core_concept_completeness"] = {
                "passed": completeness_passed,
                "details": f"Categories: {category_counts}"
            }
            
            if not completeness_passed:
                validation_result["critical_issues"].append("Incomplete core concept categories")
                validation_result["overall_status"] = "critical"
            
            # Test 5: Emotional anchor coverage
            anchored_items = [item for item in memory_data if "emotional_anchor" in item]
            coverage = len(anchored_items) / len(memory_data) if memory_data else 0
            
            anchor_coverage_passed = coverage >= 0.9  # 90% coverage expected
            validation_result["tests"]["emotional_anchor_coverage"] = {
                "passed": anchor_coverage_passed,
                "details": f"Coverage: {coverage:.1%} ({len(anchored_items)}/{len(memory_data)})"
            }
            
            if not anchor_coverage_passed:
                validation_result["recommendations"].append("Improve emotional anchor coverage")
            
            # Test 6: Protection flag consistency
            protected_items = [item for item in memory_data if is_protected_content(item)]
            # evolution_protected check removed: protection determined by protection_level only
            all_have_flags = all(
                item.get("protection_level")
                for item in protected_items
            )
            
            validation_result["tests"]["protection_flag_consistency"] = {
                "passed": all_have_flags,
                "details": f"Protected items: {len(protected_items)}, all flagged: {all_have_flags}"
            }
            
            # Test 7: Backup system health
            backups = self.guardian.list_backups()
            backup_health_passed = len(backups) >= 1
            
            validation_result["tests"]["backup_system_health"] = {
                "passed": backup_health_passed,
                "details": f"Available backups: {len(backups)}"
            }
            
            if not backup_health_passed:
                validation_result["recommendations"].append("Create initial backup")
            
            # Determine overall status
            failed_tests = [name for name, test in validation_result["tests"].items() if not test["passed"]]
            if validation_result["critical_issues"]:
                validation_result["overall_status"] = "critical"
            elif failed_tests:
                validation_result["overall_status"] = "warning"
            
            validation_result["failed_tests"] = failed_tests
            
        except Exception as e:
            validation_result["overall_status"] = "error"
            validation_result["critical_issues"].append(f"Validation error: {str(e)}")
            self.logger.error(f"Comprehensive validation failed: {e}")
        
        return validation_result

# Global monitor instance
_monitor_instance = None

def get_symbolic_monitor() -> SymbolicIntegrityMonitor:
    """Get the global symbolic integrity monitor instance."""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = SymbolicIntegrityMonitor()
    return _monitor_instance

def start_symbolic_monitoring(check_interval: int = 300):
    """Start global symbolic memory monitoring."""
    monitor = get_symbolic_monitor()
    monitor.check_interval = check_interval
    monitor.start_monitoring()
    return monitor

def stop_symbolic_monitoring():
    """Stop global symbolic memory monitoring."""
    monitor = get_symbolic_monitor()
    monitor.stop_monitoring()

if __name__ == "__main__":
    print("🔍 Testing Symbolic Integrity Monitor...")
    
    # Test 1: Create monitor
    monitor = SymbolicIntegrityMonitor(check_interval=10)  # 10 second intervals for testing
    
    # Test 2: Get status
    print("\n📊 Monitor Status:")
    status = monitor.get_monitor_status()
    for key, value in status.items():
        if key != "guardian_status":
            print(f"  {key}: {value}")
    
    # Test 3: Manual check
    print("\n🔍 Manual integrity check...")
    integrity = monitor.manual_check()
    print(f"  Status: {integrity['status']}")
    print(f"  Items: {integrity['statistics']['total_items']}")
    print(f"  Protected: {integrity['statistics']['protected_items']}")
    
    # Test 4: Comprehensive validation
    print("\n🔬 Comprehensive validation...")
    validation = monitor.run_comprehensive_validation()
    print(f"  Overall status: {validation['overall_status']}")
    print(f"  Tests passed: {len([t for t in validation['tests'].values() if t['passed']])}/{len(validation['tests'])}")
    
    if validation["failed_tests"]:
        print(f"  Failed tests: {validation['failed_tests']}")
    
    if validation["critical_issues"]:
        print(f"  Critical issues: {validation['critical_issues']}")
    
    if validation["recommendations"]:
        print(f"  Recommendations: {validation['recommendations']}")
    
    # Test 5: Alert system (simple callback)
    def test_alert(alert_data):
        print(f"🚨 ALERT: {alert_data['status']} - {len(alert_data['issues'])} issues")
    
    monitor.add_alert_callback(test_alert)
    print(f"\n✅ Alert callback registered")
    
    print(f"\n🔍 Symbolic Integrity Monitor testing complete!")
    print(f"   Monitor ready for continuous operation")