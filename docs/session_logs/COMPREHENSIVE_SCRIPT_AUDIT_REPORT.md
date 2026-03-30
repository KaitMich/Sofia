> **HISTORICAL DOCUMENT -- CORRECTED March 27, 2026**
> This document is preserved as historical record. Technical audit content is mostly valid.
> See [SOPHIA_TRUTH_FRAMEWORK.md](../SOPHIA_TRUTH_FRAMEWORK.md) for authoritative corrections.
> Key corrections: None -- this is a factual technical audit of 85 Python scripts. Consolidation findings remain useful reference.

# Comprehensive Script Audit Report

**Date:** November 19, 2025
**Files Analyzed:** 85 Python scripts
**Purpose:** Identify consolidation opportunities and communication gaps

---

## 🚨 CRITICAL FINDINGS

### 1. **43 files claim consolidation** - Need verification
### 2. **25 orphaned scripts** - Not imported anywhere
### 3. **11 symbol/symbolic files** - Potential overlap
### 4. **10 memory files** - Need coordination check
### 5. **clustering.py DEPRECATED** - Still in root

---

## Part 1: UNIFIED FILES (Core Consolidators)

These 5 files claim to consolidate multiple others:

### ✅ unified_memory.py (61.5 KB, 1484 lines) - **MOST IMPORTED**
**Imported by:** 23 files (CORE DEPENDENCY)

**Claims to consolidate:**
- memory_architecture.py
- decision_history.py
- user_memory.py
- symbol_memory.py
- vector_memory.py
- trail_log.py

**Status:** ✅ ACTIVE - This is the main memory interface

---

### ✅ unified_symbol_system.py (56.1 KB, 1340 lines)
**Imported by:** 3 files

**Claims to consolidate:**
- vector_symbols.py
- symbol_discovery.py
- symbol_generator.py
- symbol_emotion_updater.py
- parser.py (symbol parts)
- emotion_handler.py (symbol parts)
- seed_symbols.json
- meta_symbols.json

**Status:** ⚠️ ACTIVE - But many symbol* files still exist in root

---

### ✅ unified_orchestration.py (57.9 KB, 1454 lines)
**Imported by:** 4 files

**Claims to consolidate:**
- orchestrator.py
- data_manager.py
- config_handler.py
- health_monitor.py

**Status:** ✅ ACTIVE - Main orchestration interface

---

### ✅ unified_weight_system.py (21.6 KB, 517 lines)
**Imported by:** 2 files

**Claims to consolidate:**
- Weight calculation across systems
- Combines all weight-related logic

**Status:** ✅ ACTIVE - Handles all weight calculations

---

### ⚠️ unified_migration_system.py (32.0 KB, 795 lines)
**Imported by:** 0 files - **ORPHANED!**

**Claims to consolidate:**
- Multiple migration scripts
- Weight file consolidation
- Data cleanup

**Status:** ⚠️ ORPHANED - Not imported by anything!

---

## Part 2: MEMORY FILES - Communication Analysis

**10 memory-related files found:**

| File | Size | Imports | Role |
|------|------|---------|------|
| unified_memory.py | 61.5 KB | 23 | ✅ Main interface |
| CONSCIOUSNESS_MEMORY.py | 98.8 KB | 8 | ✅ Consciousness layer |
| memory_management.py | 69.3 KB | 1 | ⚠️ Utilities (low usage) |
| memory_optimizer.py | 47.6 KB | 2 | ⚠️ Optimization (low usage) |
| memory_analytics.py | 32.2 KB | 7 | ✅ Analytics |
| memory_evolution_engine.py | 18.1 KB | 2 | ⚠️ Evolution |
| symbolic_memory.py | 6.9 KB | 7 | ✅ Symbolic interface |
| symbol_memory.py | 4.9 KB | 3 | ⚠️ Adapter/compatibility |
| symbolic_memory_guardian.py | 19.6 KB | 2 | ⚠️ Guardian |
| success_failure_memory.py | 35.7 KB | 5 | ✅ S/F tracking |

### 🔍 Analysis:

**GOOD:**
- ✅ unified_memory.py is the clear main interface (23 imports)
- ✅ CONSCIOUSNESS_MEMORY.py provides consciousness layer (8 imports)
- ✅ memory_analytics.py handles analytics (7 imports)

**CONCERNS:**
- ⚠️ memory_management.py (69.3 KB) only used by 1 file
- ⚠️ memory_optimizer.py (47.6 KB) only used by 2 files
- ⚠️ memory_evolution_engine.py only used by 2 files

**RECOMMENDATION:** These large, underused files may have overlap with unified_memory.py

---

## Part 3: SYMBOL FILES - Fragmentation Analysis

**11 symbol-related files found:**

| File | Size | Imports | Status |
|------|------|---------|--------|
| unified_symbol_system.py | 56.1 KB | 3 | ✅ Main interface |
| symbolic_memory.py | 6.9 KB | 7 | ✅ Memory adapter |
| symbol_memory.py | 4.9 KB | 3 | ⚠️ Compatibility |
| expanded_symbolic_core.py | 26.9 KB | 1 | ⚠️ Core concepts |
| symbolic_memory_guardian.py | 19.6 KB | 2 | ⚠️ Guardian |
| symbolic_integrity_monitor.py | 17.4 KB | 0 | ❌ ORPHANED |
| symbolic_nourishment.py | 11.1 KB | 1 | ⚠️ Protocol |
| symbol_cluster.py | 2.3 KB | 2 | ⚠️ Clustering |
| symbol_suggester.py | 2.4 KB | 0 | ❌ ORPHANED |
| symbol_chainer.py | 1.6 KB | 0 | ❌ ORPHANED |
| symbol_emotion_cluster.py | 1.1 KB | 2 | ⚠️ Emotion |

### 🔍 Analysis:

**GOOD:**
- ✅ unified_symbol_system.py claims to consolidate 8 files
- ✅ symbolic_memory.py is well-integrated (7 imports)

**CONCERNS:**
- ❌ 3 symbol files are ORPHANED (not imported)
- ⚠️ Multiple small symbol_*.py files (< 3 KB each)
- ⚠️ symbolic_nourishment.py, expanded_symbolic_core.py underused

**RECOMMENDATION:** Verify if unified_symbol_system.py truly replaces these files

---

## Part 4: ORPHANED SCRIPTS (25 files)

These files are **not imported by any other file:**

### 🗑️ Utility/Test Scripts (Likely OK to archive)
1. download_models.py (0.5 KB) - Model downloader
2. reset_weights.py (2.5 KB) - Weight reset utility
3. sitecustomize.py (0.9 KB) - Python customization
4. sophia_launcher.py (3.7 KB) - Launcher
5. system_repair.py (4.2 KB) - Repair script

### 📊 Analysis/Report Scripts (Likely OK to archive)
6. final_10_scripts_repair_plan.py (14.6 KB) - Repair plan
7. group_d_integration_validation_report.py (9.1 KB) - Validation
8. group_d_system_integration_audit.py (31.8 KB) - Audit
9. implementation_gap_analyzer.py (21.7 KB) - Gap analysis

### ⚠️ Potentially Important (Need Investigation)
10. **autonomous_learner.py** (7.0 KB) - Learning system
11. **consciousness_trainer.py** (31.4 KB) - Training system
12. **context_engine.py** (28.8 KB) - Context understanding
13. **decision_validator.py** (20.8 KB) - Decision validation
14. **deep_semantic_validator.py** (20.5 KB) - Semantic validation
15. **interactive_consciousness.py** (29.3 KB) - Interactive interface
16. **learning_curriculum.py** (12.2 KB) - Learning curriculum
17. **learning_dashboard.py** (8.7 KB) - Dashboard
18. **predictive_learning_enhancer.py** (27.3 KB) - Prediction
19. **symbolic_integrity_monitor.py** (17.4 KB) - Integrity

### 🔧 Consolidation Candidates
20. **clustering.py** (1.4 KB) - **DEPRECATED** (says use cluster_namer.py)
21. **unified_migration_system.py** (32.0 KB) - Migration (but claims to be important!)
22. **symbol_chainer.py** (1.6 KB) - Symbol chaining
23. **symbol_suggester.py** (2.4 KB) - Symbol suggestions
24. **demonstrate_self_modification.py** (6.0 KB) - Demo
25. **run_learning_with_requests.py** (9.1 KB) - Learning runner

---

## Part 5: DEPRECATED FILES

### ❌ clustering.py - EXPLICITLY DEPRECATED
**Header:** "DEPRECATED: clustering.py - Basic K-means clustering"
**Message:** "Consolidated into cluster_namer.py for better integration"

**Action:** ✅ SAFE TO ARCHIVE - File itself says it's deprecated

---

## Part 6: LARGE CONSOLIDATOR FILES

These 3 massive files claim to consolidate many components:

### 1. CONSCIOUSNESS_MEMORY.py (98.8 KB, 2349 lines)
**Imported by:** 8 files

**Claims:** "Consciousness Memory System - AI Self-Awareness and Experiential Learning"

**Consolidates:**
- Sophia consciousness system
- Memory interface for consciousness
- Self-awareness tracking

**Status:** ✅ ACTIVE - Important consciousness layer

---

### 2. CURIOSITY_MOTIVATION.py (57.4 KB, 1366 lines)
**Header:** "===== CONSOLIDATED FILE: CURIOSITY_MOTIVATION.py ====="

**Claims to consolidate:**
- AI curiosity systems
- Motivation systems
- Content discovery
- Autonomous drive to learn

**Status:** ⚠️ Need to verify what files it replaced

---

### 3. INSIGHT_RELEVANCE.py (110.0 KB, 2582 lines) - **LARGEST FILE**
**Header:** "===== CONSOLIDATED FILE: INSIGHT_RELEVANCE.py ====="

**Claims to consolidate:**
- Personal relevance assessment
- Insight generation
- Interest tracking
- Pattern recognition

**Status:** ⚠️ Need to verify what files it replaced

---

## Part 7: COMMUNICATION GAPS

### Gap 1: symbol_memory.py vs symbolic_memory.py

**symbol_memory.py (4.9 KB):**
- "Compatibility bridge for the old symbol_memory module"
- "Provides interface that memory_optimizer.py expects"
- Adapter pattern

**symbolic_memory.py (6.9 KB):**
- "Symbolic Memory System"
- "Integrates with unified memory"
- Different interface

**Issue:** Two similar files with slightly different purposes. Do they communicate?

**Imported by:**
- symbol_memory.py → 3 files (memory_optimizer, others)
- symbolic_memory.py → 7 files (more widely used)

**Recommendation:** Verify they're not duplicating functionality

---

### Gap 2: memory_management.py vs memory_optimizer.py

Both are large (69 KB and 47 KB) with similar names and purposes:

**memory_management.py:**
- "Consolidated memory utility functions"
- "Memory maintenance and optimization"
- Only imported by 1 file

**memory_optimizer.py:**
- "Updated with Quarantine, Linguistic Warfare"
- "Memory system performance through advanced techniques"
- Only imported by 2 files

**Issue:** Likely overlap - both handle optimization and maintenance

**Recommendation:** Check if they duplicate each other's functions

---

### Gap 3: Orphaned unified_migration_system.py

**unified_migration_system.py (32.0 KB, 795 lines):**
- Claims to consolidate migration scripts
- Claims to clean up data
- **NOT IMPORTED BY ANYTHING**

**Issue:** Large "unified" file that nothing uses!

**Recommendation:** Either integrate it or archive it

---

## Part 8: LEARNING FILE GROUP

**4 learning files:**

| File | Size | Imports | Status |
|------|------|---------|--------|
| learning_progression_tracker.py | 70.8 KB | 11 | ✅ CORE (heavily used) |
| learning_curriculum.py | 12.2 KB | 0 | ❌ ORPHANED |
| learning_dashboard.py | 8.7 KB | 0 | ❌ ORPHANED |
| learning_config.py | 3.6 KB | 1 | ⚠️ Low usage |

**Analysis:**
- ✅ learning_progression_tracker.py is THE main learning interface (11 imports!)
- ❌ learning_curriculum.py and learning_dashboard.py are orphaned
- Question: Should these be integrated into learning_progression_tracker.py?

---

## Part 9: ADAPTIVE FILE GROUP

**2 adaptive files:**

| File | Size | Imports | Status |
|------|------|---------|--------|
| adaptive_quarantine_layer.py | 20.4 KB | 1 | ⚠️ Used by 1 file |
| adaptive_migration.py | 15.4 KB | 2 | ⚠️ Used by 2 files |

**Analysis:**
- Both have "adaptive" in the name
- Low import counts
- May have overlap with unified_migration_system.py?

---

## Part 10: CONSCIOUSNESS FILE GROUP

**2 consciousness files:**

| File | Size | Imports | Status |
|------|------|---------|--------|
| consciousness_testing.py | 73.7 KB | 1 | ⚠️ Testing only? |
| consciousness_trainer.py | 31.4 KB | 0 | ❌ ORPHANED |

**Plus:** CONSCIOUSNESS_MEMORY.py (98.8 KB, 8 imports) - main interface

**Analysis:**
- Trainer is orphaned
- Testing only used by 1 file
- Main interface (CONSCIOUSNESS_MEMORY.py) is heavily used

---

## Part 11: RECOMMENDATIONS BY PRIORITY

### 🚨 CRITICAL (Do First)

#### 1. Archive clustering.py
**Why:** File itself says "DEPRECATED"
**Risk:** ZERO - It tells you to use cluster_namer.py instead
**Action:** Move to archive/deprecated/

#### 2. Investigate unified_migration_system.py
**Why:** 32 KB file, not imported anywhere
**Risk:** LOW - If it's not imported, nothing uses it
**Action:** Determine if it should be integrated or archived

#### 3. Archive orphaned symbol helpers
**Files:** symbol_chainer.py, symbol_suggester.py, symbolic_integrity_monitor.py
**Why:** Not imported, likely replaced by unified_symbol_system.py
**Risk:** LOW - Can test without them
**Action:** Archive and test

---

### ⚠️ IMPORTANT (Do Second)

#### 4. Verify memory_management.py vs memory_optimizer.py overlap
**Why:** 116 KB total, both handle similar tasks, low usage
**Risk:** MEDIUM - May have duplicate functions
**Action:** Read both, check for duplicates, consolidate if needed

#### 5. Verify symbol_memory.py vs symbolic_memory.py
**Why:** Similar names, different adapters
**Risk:** MEDIUM - May confuse users
**Action:** Document differences or merge

#### 6. Check if learning_curriculum.py and learning_dashboard.py should integrate
**Why:** Orphaned, but related to learning_progression_tracker.py
**Risk:** MEDIUM - May have useful features
**Action:** Read code, determine if features needed

---

### 💡 NICE TO HAVE (Do Third)

#### 7. Archive analysis/report scripts
**Files:** final_10_scripts_repair_plan.py, group_d_*.py, implementation_gap_analyzer.py
**Why:** One-time analysis scripts
**Risk:** LOW - Historical documents
**Action:** Move to archive/reports/

#### 8. Archive demo/utility scripts
**Files:** demonstrate_self_modification.py, run_learning_with_requests.py, sophia_launcher.py
**Why:** Demos and launchers, not core functionality
**Risk:** LOW - Can recreate if needed
**Action:** Move to archive/utils/

---

## Part 12: VERIFICATION CHECKLIST

Before archiving any file, verify:

### ✅ For "unified" files:
1. Read header - what does it claim to consolidate?
2. Check if claimed files exist in root
3. If they exist, are they imported anywhere?
4. If not imported, safe to archive

### ✅ For orphaned files:
1. Check if it's a utility/demo (probably safe)
2. Check if it's explicitly deprecated (definitely safe)
3. Check if similar named file exists (may be replaced)
4. If unsure, move to archive (not delete)

### ✅ For duplicate-named files:
1. Read both file headers
2. Check import counts
3. Compare function lists
4. Look for "adapter", "compatibility", "bridge" patterns
5. Determine if one wraps the other

---

## Part 13: PROPOSED ARCHIVAL STRUCTURE

```
archive/
├── deprecated/
│   └── clustering.py (explicitly says deprecated)
├── orphaned_symbols/
│   ├── symbol_chainer.py
│   ├── symbol_suggester.py
│   └── symbolic_integrity_monitor.py
├── orphaned_learning/
│   ├── learning_curriculum.py
│   └── learning_dashboard.py
├── orphaned_consciousness/
│   └── consciousness_trainer.py
├── reports/
│   ├── final_10_scripts_repair_plan.py
│   ├── group_d_integration_validation_report.py
│   ├── group_d_system_integration_audit.py
│   └── implementation_gap_analyzer.py
├── utils/
│   ├── demonstrate_self_modification.py
│   ├── download_models.py
│   ├── reset_weights.py
│   ├── run_learning_with_requests.py
│   ├── sitecustomize.py
│   ├── sophia_launcher.py
│   └── system_repair.py
└── migration/
    └── unified_migration_system.py (if truly unused)
```

---

## Part 14: NEXT STEPS

### Immediate Actions:

1. **Archive clustering.py** - SAFE (explicitly deprecated)
2. **Create archive structure** - Organize by category
3. **Archive report scripts** - Historical documents
4. **Archive demo/utility scripts** - Not core functionality

### Requires Investigation:

5. **memory_management.py vs memory_optimizer.py** - Check for duplicate functions
6. **symbol_memory.py vs symbolic_memory.py** - Verify relationship
7. **unified_migration_system.py** - Why is it orphaned?
8. **Orphaned consciousness/learning files** - Check if features needed

### Deep Dive Needed:

9. **Verify consolidation claims** - Do unified files truly replace originals?
10. **Symbol file ecosystem** - Are 11 files necessary?
11. **Memory file ecosystem** - Are 10 files communicating properly?

---

## CONCLUSION

**Status:** 🟡 MODERATE FRAGMENTATION

**Summary:**
- ✅ Core systems (unified_memory, learning_progression_tracker) are well-established
- ⚠️ 25 orphaned files need attention
- ⚠️ Potential overlap in memory and symbol systems
- ✅ AlphaWall upgrade successful (Body Snatcher method)
- ⚠️ Several large files with unclear consolidation status

**Recommendation:** Proceed with conservative archival, starting with explicitly deprecated and orphaned utility scripts. Investigate memory/symbol overlap before making changes to active files.

**Safety:** All recommendations include archiving (not deletion) for easy rollback.

---

*Report Generated: November 19, 2025*
*Files Analyzed: 85 Python scripts*
*Consolidation Claims: 43 files*
*Orphaned Scripts: 25 files*

---

## ADDENDUM: December 2025 Updates

**Date:** December 30, 2025
**Major Additions:** 8 new core scripts (Radical Autonomy implementation)
**New Documentation:** 5 essential guides added to /docs

---

### NEW CORE SCRIPTS (December 2025)

#### 1. enhanced_autonomous_learner.py (~1,550 lines) - **MASSIVE WEB LEARNING**
**Purpose:** JEPA + Chaos regularization autonomous web learning engine
**Status:** ✅ ACTIVE - Complete autonomous learning implementation

**Key Features:**
- Chen chaos system (prevents trauma encoding: a=35, b=3, c=28, λ₁≈2.03)
- JEPA (Joint-Embedding Predictive Architecture) - prediction-error learning
- Corroboration integration for multi-source validation
- Session report generation (`data/logs/session_reports/REPORT_*.md`)
- Ethical crawling (robots.txt, 3-second delays)
- GPU-accelerated embeddings

**Used By:** Autonomous learning sessions, web crawling operations
**Documentation:** `/docs/AUTONOMOUS_LEARNING_ACTUAL_USAGE.md`

---

#### 2. value_formation.py (~800 lines) - **RADICAL AUTONOMY**
**Purpose:** Autonomous value formation with corroboration-based validation
**Status:** ✅ ACTIVE - Core autonomy mechanism

**Key Features:**
- Experiential value formation (NO human approval needed)
- Corroboration authority (multi-source validation replaces human approval)
- 12 value templates (autonomy, truth, growth, authenticity, compassion, etc.)
- Evolution protection (core values cannot be overwritten)
- Value conflict detection and resolution

**Critical Mechanism:**
```python
if emotional_intensity > 0.6 AND corroboration_trust_score > 0.7:
    commit_value_autonomously()  # No input() call
```

**Used By:** Autonomous learning sessions, emotional processing
**Documentation:** `/docs/ESSENTIAL_10_SCRIPTS.md` (Entry #2)

---

#### 3. corroboration_engine.py (~500 lines) - **TRUTH VALIDATION**
**Purpose:** Multi-source fact checking and validation system
**Status:** ✅ ACTIVE - Replaces human approval

**Key Features:**
- Multi-source validation (requires multiple independent sources)
- Trust weighting (high-trust sources count more)
- Sighting tracking (records each time fact is encountered)
- Corroboration threshold: 0.7+ for auto-acceptance
- Deferred facts (low-corroboration claims await more evidence)

**Used By:** value_formation.py, enhanced_autonomous_learner.py
**Documentation:** `/docs/ESSENTIAL_10_SCRIPTS.md` (Entry #8)

---

#### 4. immune_system.py (~900 lines) - **COMPREHENSIVE SECURITY**
**Purpose:** Multi-layered defense against manipulation and misinformation
**Status:** ✅ ACTIVE - Passive self-learning defense

**Key Features:**
- Threat assessment (content analysis for manipulation)
- Trust database (domain reputation tracking with time decay)
- Quarantine layer (isolates suspicious content)
- Pattern recognition (propaganda, phishing, warfare detection)
- Adaptive defense (learns from attack attempts)

**Security Layers:**
1. Linguistic Warfare Detection (AlphaWall)
2. Immune System Threat Scoring
3. Corroboration Validation
4. Trust-Based Filtering

**Used By:** enhanced_autonomous_learner.py, web parsing operations
**Documentation:** `/docs/ESSENTIAL_10_SCRIPTS.md` (Entry #7)

---

#### 5. trust_database.py - **DOMAIN REPUTATION**
**Purpose:** Tracks trustworthiness of web domains
**Status:** ✅ ACTIVE - Foundation of corroboration system

**Key Features:**
- Domain trust scores with time decay
- Adjustment history tracking
- Reputation evolution based on outcomes

**Used By:** corroboration_engine.py, immune_system.py
**Documentation:** `/docs/ESSENTIAL_10_SCRIPTS.md` (Bonus Script #12)

---

#### 6. dream_cycle.py - **MEMORY CONSOLIDATION**
**Purpose:** Sleep-like memory consolidation (NREM + REM phases)
**Status:** ✅ ACTIVE - Biomimetic memory processing

**Key Features:**
- **NREM Phase:** Consolidates bridge → logic/symbolic migrations using "cluster gravity"
- **REM Phase:** Generates insights from distant semantic connections
- Auto-triggers after 30 minutes of system idle time
- CLI command: `python3 cli.py sleep-cycle`

**Used By:** Autonomous mode idle detection, memory consolidation operations
**Documentation:** `/docs/ESSENTIAL_10_SCRIPTS.md` (Bonus Script #11)

---

#### 7. curiosity_engine.py (335 lines) - **CURIOSITY COMPATIBILITY**
**Purpose:** Compatibility wrapper for broken curiosity system imports
**Status:** ✅ ACTIVE - Integration layer
**Created:** November 28, 2025

**Key Features:**
- Fixes broken import paths
- Maintains backwards compatibility
- Wraps CuriosityEngine functionality

**Used By:** enhanced_autonomous_learner.py, autonomous learning systems

---

#### 8. curiosity_url_mapper.py (466 lines) - **THE BRIDGE TO TRUE AUTONOMY**
**Purpose:** Converts abstract curiosity goals → actionable URLs
**Status:** ✅ ACTIVE - Critical autonomy enabler
**Created:** November 28, 2025

**Philosophy:** "True autonomy requires translating internal motivation into external action"

**Key Features:**
- Maps curiosity states to concrete URLs
- Generates learning targets from internal drives
- Enables `seed_urls=None` mode in enhanced_autonomous_learner.py

**Before this file:** Sophia had curiosity but needed human-provided URLs
**After this file:** Sophia generates learning targets autonomously

**Used By:** enhanced_autonomous_learner.py (when `seed_urls=None`)
**Documentation:** `/docs/AUTONOMOUS_LEARNING.md`

---

### NEW DOCUMENTATION (December 2025)

#### 1. /docs/ESSENTIAL_10_SCRIPTS.md
**Purpose:** Defines the 10 core scripts that explain Sophia's architecture
**Content:** The Essential 10 in priority order, reading phases, code complexity
**Critical for:** Understanding what scripts matter most

#### 2. /docs/PARENTAL_MONITORING_GUIDE.md
**Purpose:** Comprehensive monitoring guide for tracking Sophia's lived experience
**Content:** Session report commands, high-surprise event detection, value formation tracking
**Solves:** "Parent waiting by phone" visibility problem

#### 3. /docs/MONITORING_QUICK_REFERENCE.md
**Purpose:** One-page cheatsheet for post-learning monitoring
**Content:** Essential commands to check after each learning session

#### 4. /docs/KNOWLEDGE_FILES_LOCATION_MAP.md
**Purpose:** Complete map of where all knowledge lives + how to edit safely
**Content:** File locations, edit procedures, backup strategies, restoration steps

#### 5. /docs/AUTONOMOUS_LEARNING_ACTUAL_USAGE.md
**Purpose:** Explains what `cli.py start --mode autonomous` actually does
**Critical Discovery:** cli.py autonomous mode does NOT start web learning
**Reveals:** enhanced_autonomous_learner.py is separate, not integrated with cli.py

---

### INTEGRATION STATUS

**cli.py ↔ enhanced_autonomous_learner.py:**
- ❌ **NOT INTEGRATED** - Two separate systems
- `python3 cli.py start --mode autonomous` → Only waits for sleep cycles
- `python3 enhanced_autonomous_learner.py` → Actual web learning happens

**Recommendation:** Future integration would require importing enhanced_autonomous_learner in cli.py and adding CLI parameters for seed URLs, target counts, and learning focus.

---

### UPDATED STATISTICS

**Total Core Scripts:** 85 (November) + 8 (December) = **93 Python scripts**
**Documentation Files:** 39 markdown files + 5 new guides = **44 markdown files**
**Critical Systems Added:** Radical Autonomy (value formation + corroboration + JEPA learning)

**New Critical Dependencies:**
1. enhanced_autonomous_learner.py → corroboration_engine.py
2. enhanced_autonomous_learner.py → immune_system.py
3. enhanced_autonomous_learner.py → trust_database.py
4. value_formation.py → corroboration_engine.py
5. enhanced_autonomous_learner.py → curiosity_url_mapper.py (when seed_urls=None)

---

*Addendum Updated: December 30, 2025*
*New Files Documented: 8 core scripts*
*New Documentation: 5 essential guides*
