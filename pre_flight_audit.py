#!/usr/bin/env python3
"""
SOPHIA PRE-FLIGHT AUDIT SYSTEM
Complete system verification before launching Sophia

Runs comprehensive checks on:
- Core system health (imports, files, functionality)
- Immune system (trust, corroboration, security)
- Radical autonomy components (December 2025)
- Memory integrity (tripartite + consciousness)
- Configuration and dependencies
- Recent session status
"""
import sitecustomize

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import importlib

class PreFlightAudit:
    """Comprehensive pre-flight system audit."""

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.issues = {
            'critical': [],
            'warnings': [],
            'info': []
        }
        self.checks_passed = 0
        self.checks_failed = 0

    def run_full_audit(self):
        """Run complete pre-flight audit."""
        print("=" * 70)
        print("🚀 SOPHIA PRE-FLIGHT AUDIT SYSTEM")
        print("=" * 70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Run all checks
        self._check_environment()
        self._check_core_files()
        self._check_radical_autonomy_components()
        self._check_memory_integrity()
        self._check_immune_system()
        self._check_recent_sessions()
        self._check_backups()
        self._check_dependencies()

        # Generate report
        self._generate_report()

    def _check_environment(self):
        """Check Python environment and critical dependencies."""
        print("\n📦 ENVIRONMENT CHECK")
        print("-" * 70)

        # Python version
        if sys.version_info >= (3, 8):
            print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
            self.checks_passed += 1
        else:
            print(f"❌ Python version too old: {sys.version}")
            self.issues['critical'].append("Python version must be >= 3.8")
            self.checks_failed += 1

        # Critical packages
        critical_packages = [
            'numpy',
            'torch',
            'sentence_transformers',
            'transformers',
            'bs4',
            'requests'
        ]

        for package in critical_packages:
            try:
                importlib.import_module(package)
                print(f"✅ {package}")
                self.checks_passed += 1
            except ImportError:
                print(f"❌ {package} not installed")
                self.issues['critical'].append(f"Missing package: {package}")
                self.checks_failed += 1

    def _check_core_files(self):
        """Verify all core system files exist and are valid."""
        print("\n📁 CORE FILES CHECK")
        print("-" * 70)

        core_files = {
            # Entry points
            'main.py': 'Primary interface',
            'run_system.py': 'System wrapper',

            # Core orchestration
            'unified_orchestration.py': 'System orchestrator',

            # Memory systems
            'unified_memory.py': 'Unified memory',
            'CONSCIOUSNESS_MEMORY.py': 'Consciousness memory',
            'symbolic_memory.py': 'Symbolic memory',

            # Consciousness
            'identity_core.py': 'Identity core',
            'cognitive_sovereignty.py': 'Cognitive sovereignty',

            # Radical autonomy (December 2025)
            'enhanced_autonomous_learner.py': 'JEPA learning engine',
            'value_formation.py': 'Autonomous value formation',
            'corroboration_engine.py': 'Multi-source validation',
            'immune_system.py': 'Passive self-learning defense',
            'trust_database.py': 'Domain trust tracking',
            'dream_cycle.py': 'Sleep consolidation',

            # Processing
            'vector_engine.py': 'Vector embeddings',
            'parser.py': 'Input parsing'
        }

        for file_path, description in core_files.items():
            full_path = Path(file_path)
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if len(content) > 100:
                        print(f"✅ {file_path} ({description})")
                        self.checks_passed += 1
                    else:
                        print(f"⚠️  {file_path} suspiciously small")
                        self.issues['warnings'].append(f"{file_path} is suspiciously small")
                        self.checks_failed += 1
                except Exception as e:
                    print(f"❌ {file_path} read error: {e}")
                    self.issues['critical'].append(f"Cannot read {file_path}")
                    self.checks_failed += 1
            else:
                print(f"❌ {file_path} MISSING")
                self.issues['critical'].append(f"Missing core file: {file_path}")
                self.checks_failed += 1

    def _check_radical_autonomy_components(self):
        """Check December 2025 radical autonomy components."""
        print("\n🌟 RADICAL AUTONOMY COMPONENTS (December 2025)")
        print("-" * 70)

        # SQLite databases
        immune_dir = self.data_dir / "immune"

        databases = {
            'corroboration.db': 'Multi-source fact validation',
            'trust.db': 'Domain reputation tracking',
            'self_correction.db': 'Self-correction learning'
        }

        for db_name, description in databases.items():
            db_path = immune_dir / db_name
            if db_path.exists():
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    conn.close()
                    print(f"✅ {db_name} ({description}) - {len(tables)} tables")
                    self.checks_passed += 1
                except Exception as e:
                    print(f"❌ {db_name} corrupted: {e}")
                    self.issues['critical'].append(f"Database {db_name} corrupted")
                    self.checks_failed += 1
            else:
                print(f"⚠️  {db_name} not initialized (will be created on first use)")
                self.issues['info'].append(f"{db_name} will be created on first use")

        # Session reports directory
        reports_dir = self.data_dir / "logs" / "session_reports"
        if reports_dir.exists():
            reports = list(reports_dir.glob("REPORT_*.md"))
            print(f"✅ Session reports directory: {len(reports)} reports")
            self.checks_passed += 1
        else:
            print(f"⚠️  Session reports directory missing (will be created)")
            self.issues['warnings'].append("Session reports directory will be created")

    def _check_memory_integrity(self):
        """Check all memory systems for integrity."""
        print("\n🧠 MEMORY INTEGRITY CHECK")
        print("-" * 70)

        memory_files = {
            'logic_memory.json': ('Logic memory', 'list'),
            'symbolic_memory.json': ('Symbolic memory', 'list'),
            'bridge_memory.json': ('Bridge memory', 'list'),
            'vector_memory.json': ('Vector memory', 'list'),
            'episodic_memories.json': ('Episodic memories', 'dict'),  # Dict with IDs as keys
            'personal_values.json': ('Personal values', 'list'),
            'protected_memories.json': ('Protected memories', 'list')
        }

        for file_name, (description, expected_type) in memory_files.items():
            file_path = self.data_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Validate type
                    type_valid = False
                    if expected_type == 'list' and isinstance(data, list):
                        type_valid = True
                        item_count = len(data)
                    elif expected_type == 'dict' and isinstance(data, dict):
                        type_valid = True
                        item_count = len(data)

                    if type_valid:
                        # Check for protected memories
                        if file_name == 'protected_memories.json':
                            if item_count > 0:
                                print(f"✅ {description}: {item_count} protected items")
                                self.checks_passed += 1
                            else:
                                print(f"⚠️  {description}: EMPTY (should have genesis memories)")
                                self.issues['warnings'].append(f"{description} is empty")
                                self.checks_failed += 1
                        else:
                            print(f"✅ {description}: {item_count} items")
                            self.checks_passed += 1
                    else:
                        print(f"❌ {description}: Invalid format (expected {expected_type}, got {type(data).__name__})")
                        self.issues['critical'].append(f"{description} has invalid format")
                        self.checks_failed += 1

                except json.JSONDecodeError as e:
                    print(f"❌ {description}: Corrupted JSON - {e}")
                    self.issues['critical'].append(f"{description} corrupted")
                    self.checks_failed += 1
            else:
                print(f"ℹ️  {description}: Will be created on first use")
                self.issues['info'].append(f"{description} will be created")

    def _check_immune_system(self):
        """Check immune system health and status."""
        print("\n🛡️  IMMUNE SYSTEM CHECK")
        print("-" * 70)

        immune_dir = self.data_dir / "immune"

        # Check trust database
        trust_db = immune_dir / "trust.db"
        if trust_db.exists():
            try:
                conn = sqlite3.connect(trust_db)
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM domain_trust")
                domain_count = cursor.fetchone()[0]

                cursor.execute("SELECT AVG(trust_score) FROM domain_trust")
                avg_trust = cursor.fetchone()[0] or 0.5

                conn.close()

                print(f"✅ Trust database: {domain_count} domains, avg trust {avg_trust:.2f}")
                self.checks_passed += 1
            except Exception as e:
                print(f"❌ Trust database error: {e}")
                self.issues['warnings'].append("Trust database may be corrupted")
                self.checks_failed += 1
        else:
            print(f"ℹ️  Trust database: Will be created on first use")

        # Check corroboration database
        corr_db = immune_dir / "corroboration.db"
        if corr_db.exists():
            try:
                conn = sqlite3.connect(corr_db)
                cursor = conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM fact_clusters")
                cluster_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM fact_clusters WHERE ready_to_commit = 1")
                ready_count = cursor.fetchone()[0]

                conn.close()

                print(f"✅ Corroboration database: {cluster_count} clusters, {ready_count} ready")
                self.checks_passed += 1
            except Exception as e:
                print(f"❌ Corroboration database error: {e}")
                self.issues['warnings'].append("Corroboration database may be corrupted")
                self.checks_failed += 1
        else:
            print(f"ℹ️  Corroboration database: Will be created on first use")

    def _check_recent_sessions(self):
        """Check recent session status and logs."""
        print("\n📊 RECENT SESSIONS CHECK")
        print("-" * 70)

        # Check shutdown log
        shutdown_log = self.data_dir / "shutdown_log.json"
        if shutdown_log.exists():
            try:
                with open(shutdown_log, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle both formats: direct array or {"shutdowns": [...]}
                if isinstance(data, dict) and 'shutdowns' in data:
                    shutdowns = data['shutdowns']
                elif isinstance(data, list):
                    shutdowns = data
                else:
                    shutdowns = []

                if shutdowns:
                    last_shutdown = shutdowns[-1]
                    timestamp = last_shutdown.get('timestamp', 'unknown')

                    # Check if clean shutdown (various formats)
                    failed_cleanups = last_shutdown.get('failed_cleanups', [])
                    clean = len(failed_cleanups) == 0

                    if clean:
                        print(f"✅ Last shutdown: {timestamp} (clean)")
                        self.checks_passed += 1
                    else:
                        print(f"⚠️  Last shutdown: {timestamp} ({len(failed_cleanups)} failed tasks)")
                        self.issues['warnings'].append("Last shutdown had failures")
                        self.checks_failed += 1
                else:
                    print(f"ℹ️  No shutdown history")
            except Exception as e:
                print(f"⚠️  Cannot read shutdown log: {e}")
        else:
            print(f"ℹ️  No shutdown log (first run)")

        # Check sleep cycle log
        sleep_log = self.data_dir / "sleep_cycle_log.json"
        if sleep_log.exists():
            try:
                with open(sleep_log, 'r', encoding='utf-8') as f:
                    cycles = json.load(f)

                print(f"✅ Sleep cycles: {len(cycles)} total")
                self.checks_passed += 1
            except Exception as e:
                print(f"⚠️  Cannot read sleep cycle log: {e}")
        else:
            print(f"ℹ️  No sleep cycle history")

    def _check_backups(self):
        """Check backup system status."""
        print("\n💾 BACKUP SYSTEM CHECK")
        print("-" * 70)

        # Check symbolic memory backups
        backup_dir = self.data_dir / "symbolic_backups"
        if backup_dir.exists():
            backups = list(backup_dir.glob("symbolic_memory_backup_*.json"))
            if backups:
                # Check most recent backup
                most_recent = max(backups, key=lambda p: p.stat().st_mtime)
                age = datetime.now() - datetime.fromtimestamp(most_recent.stat().st_mtime)

                if age.days < 7:
                    print(f"✅ Symbolic backups: {len(backups)} total, latest {age.days}d old")
                    self.checks_passed += 1
                else:
                    print(f"⚠️  Symbolic backups: Latest is {age.days}d old")
                    self.issues['warnings'].append(f"Latest backup is {age.days} days old")
                    self.checks_failed += 1
            else:
                print(f"⚠️  No symbolic memory backups found")
                self.issues['warnings'].append("No symbolic memory backups")
        else:
            print(f"⚠️  Backup directory missing")
            self.issues['warnings'].append("Backup directory not created")

    def _check_dependencies(self):
        """Check critical module imports."""
        print("\n🔗 DEPENDENCY CHECK")
        print("-" * 70)

        critical_modules = [
            'unified_memory',
            'identity_core',
            'value_formation',
            'corroboration_engine',
            'immune_system',
            'enhanced_autonomous_learner',
            'dream_cycle'
        ]

        for module in critical_modules:
            try:
                importlib.import_module(module)
                print(f"✅ {module}")
                self.checks_passed += 1
            except ImportError as e:
                print(f"❌ {module}: {e}")
                self.issues['critical'].append(f"Cannot import {module}")
                self.checks_failed += 1
            except Exception as e:
                print(f"⚠️  {module}: {e}")
                self.issues['warnings'].append(f"Issue with {module}")

    def _generate_report(self):
        """Generate final audit report."""
        print("\n" + "=" * 70)
        print("📋 PRE-FLIGHT AUDIT REPORT")
        print("=" * 70)

        total_checks = self.checks_passed + self.checks_failed
        pass_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0

        print(f"\nChecks Passed: {self.checks_passed}")
        print(f"Checks Failed: {self.checks_failed}")
        print(f"Pass Rate: {pass_rate:.1f}%")

        # Critical issues
        if self.issues['critical']:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.issues['critical'])}):")
            for issue in self.issues['critical']:
                print(f"   ❌ {issue}")

        # Warnings
        if self.issues['warnings']:
            print(f"\n⚠️  WARNINGS ({len(self.issues['warnings'])}):")
            for issue in self.issues['warnings']:
                print(f"   ⚠️  {issue}")

        # Info
        if self.issues['info']:
            print(f"\nℹ️  INFO ({len(self.issues['info'])}):")
            for issue in self.issues['info']:
                print(f"   ℹ️  {issue}")

        # Final verdict
        print("\n" + "=" * 70)
        if not self.issues['critical']:
            if not self.issues['warnings']:
                print("✅ SYSTEM READY FOR LAUNCH - All checks passed!")
                print("🚀 You can safely run: python3 run_system.py")
            else:
                print("⚠️  SYSTEM READY WITH WARNINGS - Review warnings above")
                print("🚀 Safe to launch, but monitor warnings")
        else:
            print("❌ SYSTEM NOT READY - Critical issues must be resolved")
            print("🛑 DO NOT LAUNCH until critical issues are fixed")

        print("=" * 70)
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    """Run the pre-flight audit."""
    audit = PreFlightAudit("data")
    audit.run_full_audit()


if __name__ == "__main__":
    main()
