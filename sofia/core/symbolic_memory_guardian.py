#!/usr/bin/env python3
"""
Symbolic Memory Guardian - Backup, Restore, and Integrity System

This module provides comprehensive protection for symbolic memory through:
1. Automated backup systems with versioning
2. Integrity monitoring and validation
3. Emergency restoration capabilities
4. Corruption detection and repair

This is a critical safety system for preserving the AI's emotional and symbolic understanding.
"""

import json
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

# Import protection utilities
try:
    from sofia.security.protection_utils import is_protected_content, get_protection_reason
    PROTECTION_AVAILABLE = True
except ImportError:
    PROTECTION_AVAILABLE = False

class SymbolicMemoryGuardian:
    """
    Guardian system for symbolic memory protection, backup, and restoration.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.symbolic_memory_file = self.data_dir / "symbolic_memory.json"
        self.backup_dir = self.data_dir / "symbolic_backups"
        self.integrity_log_file = self.data_dir / "symbolic_integrity.json"
        
        # Create directories
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Integrity tracking
        self.integrity_history = self._load_integrity_history()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the guardian system."""
        logger = logging.getLogger('SymbolicMemoryGuardian')
        logger.setLevel(logging.INFO)
        
        # Create file handler if it doesn't exist
        if not logger.handlers:
            log_file = self.data_dir / "symbolic_guardian.log"
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_integrity_history(self) -> List[Dict[str, Any]]:
        """Load integrity check history."""
        if self.integrity_log_file.exists():
            try:
                with open(self.integrity_log_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load integrity history: {e}")
        return []
    
    def _save_integrity_history(self):
        """Save integrity check history."""
        try:
            with open(self.integrity_log_file, 'w') as f:
                json.dump(self.integrity_history[-100:], f, indent=2)  # Keep last 100 entries
        except Exception as e:
            self.logger.error(f"Could not save integrity history: {e}")
    
    def calculate_memory_hash(self, memory_data: List[Dict[str, Any]]) -> str:
        """Calculate a hash of the symbolic memory for integrity checking."""
        # Create a deterministic string representation
        memory_str = json.dumps(memory_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(memory_str.encode()).hexdigest()
    
    def create_backup(self, reason: str = "Manual backup") -> str:
        """
        Create a timestamped backup of symbolic memory.
        
        Returns:
            str: Backup file path
        """
        if not self.symbolic_memory_file.exists():
            raise FileNotFoundError("Symbolic memory file not found")
        
        # Load current memory
        with open(self.symbolic_memory_file, 'r') as f:
            memory_data = json.load(f)
        
        # Create backup filename with timestamp
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        backup_filename = f"symbolic_memory_backup_{timestamp}.json"
        backup_path = self.backup_dir / backup_filename
        
        # Create backup metadata
        backup_metadata = {
            "backup_time": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "item_count": len(memory_data),
            "memory_hash": self.calculate_memory_hash(memory_data),
            "protected_items": 0,
            "categories": {}
        }
        
        # Analyze backup content
        if PROTECTION_AVAILABLE:
            for item in memory_data:
                if is_protected_content(item):
                    backup_metadata["protected_items"] += 1
                
                category = item.get("symbolic_category", "unknown")
                backup_metadata["categories"][category] = backup_metadata["categories"].get(category, 0) + 1
        
        # Create backup structure
        backup_data = {
            "metadata": backup_metadata,
            "symbolic_memory": memory_data
        }
        
        # Save backup
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        self.logger.info(f"Backup created: {backup_filename} ({len(memory_data)} items)")
        
        # Clean old backups (keep last 20)
        self._cleanup_old_backups()
        
        return str(backup_path)
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups with metadata."""
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob("symbolic_memory_backup_*.json")):
            try:
                with open(backup_file, 'r') as f:
                    backup_data = json.load(f)
                
                metadata = backup_data.get("metadata", {})
                backups.append({
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "backup_time": metadata.get("backup_time"),
                    "reason": metadata.get("reason", "Unknown"),
                    "item_count": metadata.get("item_count", 0),
                    "protected_items": metadata.get("protected_items", 0),
                    "memory_hash": metadata.get("memory_hash", ""),
                    "file_size": backup_file.stat().st_size
                })
            except Exception as e:
                self.logger.warning(f"Could not read backup {backup_file.name}: {e}")
        
        return sorted(backups, key=lambda x: x["backup_time"], reverse=True)
    
    def restore_from_backup(self, backup_path: str, verify_integrity: bool = True) -> bool:
        """
        Restore symbolic memory from a backup.
        
        Args:
            backup_path: Path to the backup file
            verify_integrity: Whether to verify backup integrity before restoring
            
        Returns:
            bool: True if restoration was successful
        """
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            self.logger.error(f"Backup file not found: {backup_path}")
            return False
        
        try:
            # Load backup
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            metadata = backup_data.get("metadata", {})
            memory_data = backup_data.get("symbolic_memory", [])
            
            # Verify integrity if requested
            if verify_integrity:
                expected_hash = metadata.get("memory_hash")
                if expected_hash:
                    actual_hash = self.calculate_memory_hash(memory_data)
                    if actual_hash != expected_hash:
                        self.logger.error(f"Backup integrity check failed for {backup_path.name}")
                        return False
                    else:
                        self.logger.info("Backup integrity verified")
            
            # Create current backup before restoring
            current_backup = self.create_backup(f"Pre-restore backup before restoring {backup_path.name}")
            self.logger.info(f"Created pre-restore backup: {current_backup}")
            
            # Restore memory
            with open(self.symbolic_memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            self.logger.info(f"Restored symbolic memory from {backup_path.name} ({len(memory_data)} items)")
            
            # Log restoration
            restoration_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "restore",
                "source_backup": backup_path.name,
                "items_restored": len(memory_data),
                "pre_restore_backup": Path(current_backup).name,
                "integrity_verified": verify_integrity
            }
            
            self.integrity_history.append(restoration_record)
            self._save_integrity_history()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore from backup {backup_path.name}: {e}")
            return False
    
    def check_integrity(self, auto_backup: bool = True) -> Dict[str, Any]:
        """
        Comprehensive integrity check of symbolic memory.
        
        Args:
            auto_backup: Whether to create a backup if integrity issues are found
            
        Returns:
            Dict with integrity check results
        """
        integrity_result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "healthy",
            "issues": [],
            "warnings": [],
            "statistics": {},
            "recommendations": []
        }
        
        try:
            # Load current memory
            if not self.symbolic_memory_file.exists():
                integrity_result["status"] = "critical"
                integrity_result["issues"].append("Symbolic memory file missing")
                return integrity_result
            
            with open(self.symbolic_memory_file, 'r') as f:
                memory_data = json.load(f)
            
            # Basic statistics
            stats = {
                "total_items": len(memory_data),
                "protected_items": 0,
                "core_symbolic_items": 0,
                "identity_core_items": 0,
                "items_with_emotional_anchors": 0,
                "categories": {},
                "protection_levels": {}
            }
            
            # Analyze each item
            duplicates = {}
            missing_fields = []
            
            for i, item in enumerate(memory_data):
                item_id = item.get("id", f"item_{i}")
                
                # Check for protection
                if PROTECTION_AVAILABLE and is_protected_content(item):
                    stats["protected_items"] += 1
                
                # Count by content type
                content_type = item.get("content_type", "unknown")
                if content_type == "symbolic_core":
                    stats["core_symbolic_items"] += 1
                elif content_type == "identity_core":
                    stats["identity_core_items"] += 1
                
                # Check for emotional anchors
                if "emotional_anchor" in item:
                    stats["items_with_emotional_anchors"] += 1
                
                # Count categories
                category = item.get("symbolic_category", item.get("memory_type", "unknown"))
                stats["categories"][category] = stats["categories"].get(category, 0) + 1
                
                # Count protection levels
                protection_level = item.get("protection_level", "none")
                stats["protection_levels"][protection_level] = stats["protection_levels"].get(protection_level, 0) + 1
                
                # Check for duplicates
                if item_id in duplicates:
                    integrity_result["issues"].append(f"Duplicate ID found: {item_id}")
                    duplicates[item_id] += 1
                else:
                    duplicates[item_id] = 1
                
                # Check for required fields
                required_fields = ["id", "text"]
                if content_type == "symbolic_core":
                    required_fields.extend(["emotional_anchor", "symbolic_category"])
                
                for field in required_fields:
                    if field not in item or not item[field]:
                        missing_fields.append(f"Item {item_id} missing {field}")
            
            integrity_result["statistics"] = stats
            
            # Add missing field issues
            if missing_fields:
                integrity_result["issues"].extend(missing_fields[:10])  # Limit to first 10
                if len(missing_fields) > 10:
                    integrity_result["issues"].append(f"... and {len(missing_fields) - 10} more missing field issues")
            
            # Check expected protected items
            expected_core_concepts = 20
            if stats["core_symbolic_items"] < expected_core_concepts:
                integrity_result["warnings"].append(
                    f"Expected {expected_core_concepts} core symbolic concepts, found {stats['core_symbolic_items']}"
                )
            
            # Check emotional anchor coverage
            anchor_coverage = stats["items_with_emotional_anchors"] / max(stats["total_items"], 1)
            if anchor_coverage < 0.8:  # Expect 80%+ coverage
                integrity_result["warnings"].append(
                    f"Low emotional anchor coverage: {anchor_coverage:.1%} (expected >80%)"
                )
            
            # Determine overall status
            if integrity_result["issues"]:
                integrity_result["status"] = "corrupted" if len(integrity_result["issues"]) > 5 else "damaged"
                if auto_backup:
                    backup_path = self.create_backup("Integrity check - issues found")
                    integrity_result["backup_created"] = backup_path
            elif integrity_result["warnings"]:
                integrity_result["status"] = "warning"
            
            # Generate recommendations
            if integrity_result["issues"]:
                integrity_result["recommendations"].append("Consider restoring from a recent backup")
            if stats["protected_items"] < 20:
                integrity_result["recommendations"].append("Verify all protected symbolic concepts are present")
            if anchor_coverage < 0.5:
                integrity_result["recommendations"].append("Add emotional anchors to symbolic memories")
            
        except Exception as e:
            integrity_result["status"] = "critical"
            integrity_result["issues"].append(f"Integrity check failed: {str(e)}")
            self.logger.error(f"Integrity check error: {e}")
        
        # Log integrity check
        self.integrity_history.append(integrity_result)
        self._save_integrity_history()
        
        return integrity_result
    
    def emergency_restore(self) -> bool:
        """
        Emergency restoration from the most recent backup.
        Use when symbolic memory is corrupted or missing.
        
        Returns:
            bool: True if emergency restore was successful
        """
        self.logger.warning("EMERGENCY RESTORE INITIATED")
        
        try:
            # Find most recent backup
            backups = self.list_backups()
            if not backups:
                self.logger.error("No backups available for emergency restore")
                return False
            
            latest_backup = backups[0]
            self.logger.info(f"Using latest backup: {latest_backup['filename']}")
            
            # Attempt restore
            success = self.restore_from_backup(latest_backup["path"], verify_integrity=True)
            
            if success:
                self.logger.info("Emergency restore completed successfully")
            else:
                self.logger.error("Emergency restore failed")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Emergency restore failed: {e}")
            return False
    
    def _cleanup_old_backups(self, keep_count: int = 20):
        """Remove old backups, keeping the most recent ones."""
        backup_files = sorted(
            self.backup_dir.glob("symbolic_memory_backup_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for old_backup in backup_files[keep_count:]:
            try:
                old_backup.unlink()
                self.logger.info(f"Cleaned up old backup: {old_backup.name}")
            except Exception as e:
                self.logger.warning(f"Could not remove old backup {old_backup.name}: {e}")
    
    def get_guardian_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the guardian system."""
        backups = self.list_backups()
        recent_integrity = self.integrity_history[-1] if self.integrity_history else None
        
        return {
            "symbolic_memory_exists": self.symbolic_memory_file.exists(),
            "backup_count": len(backups),
            "latest_backup": backups[0] if backups else None,
            "recent_integrity_check": recent_integrity,
            "guardian_log_size": (self.data_dir / "symbolic_guardian.log").stat().st_size if (self.data_dir / "symbolic_guardian.log").exists() else 0,
            "protection_system_available": PROTECTION_AVAILABLE
        }

# Convenience functions
def create_symbolic_backup(reason: str = "Manual backup") -> str:
    """Quick function to create a symbolic memory backup."""
    guardian = SymbolicMemoryGuardian()
    return guardian.create_backup(reason)

def check_symbolic_integrity() -> Dict[str, Any]:
    """Quick function to check symbolic memory integrity."""
    guardian = SymbolicMemoryGuardian()
    return guardian.check_integrity()

def emergency_restore_symbolic() -> bool:
    """Quick function for emergency symbolic memory restoration."""
    guardian = SymbolicMemoryGuardian()
    return guardian.emergency_restore()

if __name__ == "__main__":
    print("🛡️ Testing Symbolic Memory Guardian...")
    
    # Initialize guardian
    guardian = SymbolicMemoryGuardian()
    
    # Test 1: Check status
    print("\n📊 Guardian Status:")
    status = guardian.get_guardian_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test 2: Create backup
    print("\n💾 Creating test backup...")
    try:
        backup_path = guardian.create_backup("Guardian system test")
        print(f"✅ Backup created: {Path(backup_path).name}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")
    
    # Test 3: List backups
    print("\n📋 Available backups:")
    backups = guardian.list_backups()
    for backup in backups[:3]:  # Show first 3
        print(f"  • {backup['filename']} - {backup['item_count']} items ({backup['reason']})")
    
    # Test 4: Integrity check
    print("\n🔍 Running integrity check...")
    integrity = guardian.check_integrity(auto_backup=False)
    print(f"  Status: {integrity['status']}")
    print(f"  Items: {integrity['statistics'].get('total_items', 0)}")
    print(f"  Protected: {integrity['statistics'].get('protected_items', 0)}")
    print(f"  Issues: {len(integrity['issues'])}")
    print(f"  Warnings: {len(integrity['warnings'])}")
    
    if integrity['issues']:
        print("  Issues found:")
        for issue in integrity['issues'][:3]:
            print(f"    • {issue}")
    
    if integrity['warnings']:
        print("  Warnings:")
        for warning in integrity['warnings']:
            print(f"    • {warning}")
    
    print("\n🛡️ Symbolic Memory Guardian testing complete!")