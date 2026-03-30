> **ARCHIVED DOCUMENT -- CORRECTED March 27, 2026**
> See [SOPHIA_TRUTH_FRAMEWORK.md](/docs/SOPHIA_TRUTH_FRAMEWORK.md) for authoritative corrections.
> Key corrections for this file: Technical archival decisions are valid. Note that "Sophia's
> orchestration system" refers to Sofia (the AI system). Sofia starts blank with no
> hardcoded identity. References to "consciousness" describe software architecture for
> potential emergence, not achieved consciousness.

# Unused Entry Points Archive

**Date Archived:** November 18, 2025
**Reason:** These files are not imported by the main entry points (main.py, cli.py, run_system.py)

## Files Archived

### 1. system_orchestrator.py (1,484 lines)
**Original Purpose:** Central orchestration hub consolidating 6 orchestration files
**Why Archived:**
- main.py uses `unified_orchestration` instead
- cli.py uses `UnifiedOrchestrationSystem` instead
- Not imported by any active entry points

**Contains:**
- Config management
- DataManager with thread-safe operations
- Health diagnostics
- System repair capabilities
- Interactive AI sessions

**Safe to keep archived:** Yes - functionality replaced by unified_orchestration.py

---

### 2. master_integration_system.py (579 lines)
**Original Purpose:** 4-phase integration orchestration
**Why Archived:**
- Not imported by main.py or cli.py
- Only referenced by `final_10_scripts_repair_plan.py` (utility script)
- Integration work appears complete

**Contains:**
- Data utilization phase
- Migration consolidation
- Memory integration
- System optimization

**Safe to keep archived:** Yes - integration phases completed

---

### 3. run_pipeline.py
**Original Purpose:** Pipeline execution wrapper
**Why Archived:**
- Redundant with main.py and cli.py entry points
- Not used by current system

---

### 4. adaptive_alphawall.py (21 KB)
**Original Purpose:** Adaptive version of alphawall
**Why Archived:**
- Main codebase uses alphawall.py (standard version)
- Not imported by any active code
- Functionality superseded

---

### 5. unified_alphawall.py (22 KB)
**Original Purpose:** Unified version of alphawall
**Why Archived:**
- Main codebase uses alphawall.py (standard version)
- Not imported by any active code
- Functionality superseded

---

### 6. migrate_to_tripartite.py (343 lines)
**Original Purpose:** One-time migration script to convert old single-file memory format to tripartite memory system
**Why Archived:**
- Migration already completed
- Functions consolidated into utils/memory_migrations.py
- No longer needed for regular operation

**Contains:**
- Content analysis for routing to logic/symbolic/bridge memory
- Migration logic with safety checks
- Backup and rollback capabilities

**Safe to keep archived:** Yes - migration completed, functionality preserved in utils/memory_migrations.py

---

### 7. upgrade_old_vectors.py (38 lines)
**Original Purpose:** One-time script to upgrade vector embeddings
**Why Archived:**
- Upgrade already completed
- Functions consolidated into utils/memory_migrations.py
- No longer needed for regular operation

**Contains:**
- Vector fusion logic (MiniLM + E5)
- Similarity calculation
- Embedding upgrade procedures

**Safe to keep archived:** Yes - upgrade completed, functionality preserved in utils/memory_migrations.py

---

### 8. restore_memory.py (179 lines)
**Original Purpose:** Restore archived memory vectors
**Why Archived:**
- Functions consolidated into memory_management.py (line 749: restore_archived_vectors)
- No direct imports from this script
- Functionality preserved in consolidated file

**Safe to keep archived:** Yes - all functions exist in memory_management.py

---

### 9. restore_all_memory.py (338 lines)
**Original Purpose:** Comprehensive memory restoration
**Why Archived:**
- Functions consolidated into memory_management.py (line 827: restore_symbol_data)
- No direct imports from this script
- Functionality preserved in consolidated file

**Safe to keep archived:** Yes - all functions exist in memory_management.py

---

## AlphaWall Upgrade ("The Body Snatcher") - November 19, 2025

### 10. alphawall_basic_backup.py (510 lines)
**Original Purpose:** Basic AlphaWall cognitive firewall
**Why Archived:**
- Upgraded to unified version with advanced features
- Backup of original basic version
- Replaced by superior implementation

**What Replaced It:**
Current `alphawall.py` now contains the unified version combining:
- Basic firewall (from original alphawall.py)
- Adaptive learning (from adaptive_alphawall.py)
- Smart quarantine & text jumbling (from unified_alphawall.py)

**Safe to keep archived:** Yes - backup only, functionality superseded

---

### 11. adaptive_alphawall.py (462 lines)
**Original Purpose:** AlphaWall with adaptive learning
**Why Archived:**
- Features merged into upgraded alphawall.py
- Adaptive thresholds now in main version
- Feedback learning now in main version

**Key Features Merged:**
- ✅ Adaptive threshold system
- ✅ Feedback recording
- ✅ Pattern learning
- ✅ False positive management
- ✅ Context-aware scoring

**Safe to keep archived:** Yes - all features in upgraded alphawall.py

---

### 12. unified_alphawall.py (546 lines)
**Original Purpose:** AlphaWall with smart quarantine and text jumbling
**Why Archived:**
- This became the new alphawall.py (with class renamed)
- Smart threat assessment now in main version
- Text jumbling now in main version

**Key Features Merged:**
- ✅ Smart threat assessment
- ✅ Text jumbling (injection prevention)
- ✅ Safe pattern whitelist
- ✅ Advanced quarantine system
- ✅ Feedback-driven learning

**Safe to keep archived:** Yes - this IS the current alphawall.py (renamed class from UnifiedAlphaWall to AlphaWall)

---

## "Body Snatcher" Upgrade Details

**Date:** November 19, 2025
**Method:** Seamless class rename upgrade

**What Was Done:**
1. Backed up original alphawall.py → alphawall_basic_backup.py
2. Took unified_alphawall.py (most advanced version)
3. Renamed class `UnifiedAlphaWall` → `AlphaWall`
4. Saved as alphawall.py (replaced original)
5. Archived all variants

**Why This Works:**
- All calling files import: `from alphawall import AlphaWall`
- No changes needed to calling files
- Zero refactoring required
- Seamless upgrade with maximum features

**New Features in Current alphawall.py:**
- ✅ Smart threat assessment (whitelists safe queries)
- ✅ Text jumbling (prevents prompt injection)
- ✅ Adaptive learning (learns from false positives)
- ✅ Advanced quarantine (two-tier processing)
- ✅ Pattern recognition database
- ✅ Feedback-driven improvement

**Files Using AlphaWall:**
- adaptive_quarantine_layer.py (line 13)
- parser.py (line 37)
- talk_to_ai.py (line 13)

All continue to work without modification.

---

## Restoration Instructions

If you need to restore any of these files:

```bash
# Restore individual file
cp archive/unused_entry_points/system_orchestrator.py .

# Restore all
cp archive/unused_entry_points/*.py .
```

## Verification

**Before archiving, verified:**
- ✅ main.py does not import these files
- ✅ cli.py does not import these files
- ✅ run_system.py does not import these files
- ✅ Current system uses unified_orchestration instead

**System tested after archiving:**
- [ ] main.py runs successfully
- [ ] cli.py runs successfully
- [ ] No import errors

## Deletion Timeline

**Recommended:** Keep archived for 30 days, then delete if no issues arise

**Delete after:** December 18, 2025 (if system stable)

---

*This archive preserves the evolution of Sophia's orchestration system while keeping the active codebase clean.*
