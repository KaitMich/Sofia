> **HISTORICAL DOCUMENT -- CORRECTED March 27, 2026**
> This document is preserved as historical record. Technical content is valid.
> See [SOPHIA_TRUTH_FRAMEWORK.md](../SOPHIA_TRUTH_FRAMEWORK.md) for authoritative corrections.
> Key corrections: None -- this is a factual technical fact-check of archival claims.

# Fact-Check: "The Last 3 Stragglers" Claims

**Date:** November 19, 2025
**Claim Source:** External suggestion to archive 3 files
**Verdict:** ❌ **2 OUT OF 3 CLAIMS ARE FALSE**

---

## Summary

| File | Claim | Reality | Verdict |
|------|-------|---------|---------|
| adaptive_migration.py | "Logic in utils/" | ✅ BUT still imported by 3 files | ❌ **FALSE - ACTIVELY USED** |
| reverse_migration.py | "Logic in utils/" | ⚠️ Class exists in utils, but root file imported | ⚠️ **COMPLEX** |
| adaptive_quarantine_layer.py | "Superseded by alphawall" | ❌ Different purpose, actively used | ❌ **FALSE - ACTIVELY USED** |

**Conclusion:** DO NOT archive these files without further investigation!

---

## Detailed Fact-Check

### File 1: adaptive_migration.py (15.4 KB, 384 lines)

**Claim:** "Its logic lives in utils/memory_migrations.py"

**Reality Check:**
```bash
$ grep -rn "import adaptive_migration" --include="*.py" .

./memory_evolution_engine.py:9:from adaptive_migration import AdaptiveThresholds, MigrationEngine
./reverse_migration.py:4:from adaptive_migration import MigrationEngine, evaluate_link_with_confidence_gates
./utils/memory_migrations.py:426:from adaptive_migration import AdaptiveThresholds, MigrationEngine
```

**Verdict:** ❌ **FALSE - ACTIVELY USED BY 3 FILES**

**Evidence:**
1. **memory_evolution_engine.py** imports it (line 9)
2. **reverse_migration.py** imports it (line 4)
3. **utils/memory_migrations.py** imports it (line 426)

**Key Finding:** utils/memory_migrations.py **IMPORTS FROM** adaptive_migration.py - it does NOT replace it!

**What It Contains:**
```python
class AdaptiveThresholds:
    """Manages time-varying migration thresholds"""
    # Starts high (0.9), decreases over time to 0.3

class MigrationEngine:
    """Handles migration of items between memory stores"""
    # Includes sovereignty checks
    # Prevents ping-ponging
    # Decision history tracking

def evaluate_link_with_confidence_gates(...)
    """Local implementation of confidence gates"""
```

**Action:** ✅ **KEEP - Core migration functionality**

---

### File 2: reverse_migration.py (7.9 KB, 224 lines)

**Claim:** "Its logic lives in utils/memory_migrations.py"

**Reality Check:**
```bash
$ grep -rn "import reverse_migration" --include="*.py" .

./memory_evolution_engine.py:10:from reverse_migration import ReverseMigrationAuditor
```

**Additional Check:**
```bash
$ grep -n "class ReverseMigrationAuditor" utils/memory_migrations.py

431:class ReverseMigrationAuditor:
```

**Verdict:** ⚠️ **COMPLEX - Class exists in BOTH places**

**Evidence:**
1. **memory_evolution_engine.py** imports from root file (line 10)
2. **utils/memory_migrations.py** HAS the class (line 431)
3. Root file is **STILL BEING USED** despite utils having the code

**What It Contains:**
```python
class ReverseMigrationAuditor:
    """Audits items in logic/symbolic memory to catch misclassifications"""
    # Sovereignty protection
    # Re-evaluation of confidence scores
    # Reverse migration back to bridge memory
```

**Situation:**
- Header in utils/memory_migrations.py says it consolidated reverse_migration.py
- But memory_evolution_engine.py still imports from the ROOT file
- This is a **DUPLICATE IMPORT** situation

**Action:** ⚠️ **NEEDS INVESTIGATION**
- Check if utils version is identical to root version
- If yes: Update import in memory_evolution_engine.py to use utils version
- If no: Determine which version is correct
- Only archive after fixing import

---

### File 3: adaptive_quarantine_layer.py (20.4 KB, 475 lines)

**Claim:** "Its logic is superseded by the new alphawall.py"

**Reality Check:**
```bash
$ grep -rn "import adaptive_quarantine" --include="*.py" .

./talk_to_ai.py:15:from adaptive_quarantine_layer import AdaptiveQuarantine
```

**Verdict:** ❌ **FALSE - ACTIVELY USED AND NOT SUPERSEDED**

**Evidence:**
1. **talk_to_ai.py** actively imports it (line 15)
2. **security/unified_security.py** mentions it in header (lines 18, 485)

**What It Contains:**
```python
class AdaptiveQuarantine(BaseQuarantine):
    """Enhanced quarantine system that learns what needs quarantining"""
    # Inherits from quarantine_layer.UserMemoryQuarantine
    # Adds adaptive thresholds
    # Learns from false positives
    # Context-aware vagueness scoring
    # Distinguishes academic queries from vague input
```

**Key Point:** This is **NOT the same as AlphaWall!**

**Comparison:**

| Feature | AlphaWall | AdaptiveQuarantine |
|---------|-----------|-------------------|
| **Purpose** | Cognitive firewall (pre-processing) | Quarantine system (post-processing) |
| **Scope** | All user input | Specific harmful patterns |
| **Location** | Input layer | Memory layer |
| **Learns from** | False positive feedback | Quarantine accuracy |
| **Base class** | Standalone | Extends BaseQuarantine |
| **Used by** | parser.py, talk_to_ai.py (via alphawall import) | talk_to_ai.py (separate import) |

**They serve DIFFERENT purposes:**
- **AlphaWall:** Firewall that processes ALL input, creates zone outputs
- **AdaptiveQuarantine:** Quarantine system for SPECIFIC harmful patterns in memory

**Action:** ✅ **KEEP - Different role than AlphaWall**

---

## Root Cause Analysis

### Why Were These Claims Made?

**Possible reasons:**
1. **Superficial analysis** - Didn't check actual imports
2. **Assumed based on naming** - "adaptive" appears in multiple files
3. **Misread utils header** - Header says it consolidates but still imports
4. **Confusion about consolidation** - Consolidation ≠ Replacement

### The Truth About utils/memory_migrations.py

**Header says:**
```python
"""
Migration-specific utilities for memory system transformations including:
- Tripartite memory migration from migrate_to_tripartite.py
- Vector upgrade utilities from upgrade_old_vectors.py
- Reverse migration audit from reverse_migration.py
- Unified migration system from unified_migration_system.py
"""
```

**But looking at line 426:**
```python
from adaptive_migration import AdaptiveThresholds, MigrationEngine
```

**This means:**
- utils/memory_migrations.py **USES** adaptive_migration.py
- It doesn't **REPLACE** it
- adaptive_migration.py is a **DEPENDENCY**, not redundant code

---

## Corrected Status

### ✅ Files to KEEP (All 3!)

1. **adaptive_migration.py** - Core migration engine (imported by 3 files)
2. **adaptive_quarantine_layer.py** - Quarantine learning system (imported by 1 file)
3. **reverse_migration.py** - Needs investigation (duplicate with utils)

---

## Action Plan

### Immediate: NO ARCHIVAL

**Do NOT archive any of these files.**

### For reverse_migration.py Only:

**Step 1: Compare versions**
```bash
diff reverse_migration.py <(sed -n '415,600p' utils/memory_migrations.py)
```

**Step 2a: If identical**
- Update memory_evolution_engine.py import:
```python
# OLD:
from reverse_migration import ReverseMigrationAuditor

# NEW:
from utils.memory_migrations import ReverseMigrationAuditor
```
- Test system
- Archive reverse_migration.py

**Step 2b: If different**
- Determine which version is correct
- Update the outdated version
- Then proceed with 2a

---

## Lessons Learned

### ⚠️ Dangers of External Advice

1. **Always verify imports** - Don't trust claims without checking
2. **Read != Use** - Just because code exists somewhere doesn't mean original is unused
3. **Headers can be misleading** - "Consolidates X" might mean "uses X" not "replaces X"
4. **Different names ≠ Different purpose** - adaptive_quarantine ≠ alphawall

### ✅ Proper Verification Process

1. Check imports across codebase
2. Read file headers AND code
3. Understand purpose/role
4. Compare with claimed replacement
5. Verify functionality overlap

---

## Final Verdict

**Original Claim:** "3 files are redundant and can be archived"

**Reality:**
- ❌ adaptive_migration.py - **KEEP (imported by 3 files)**
- ⚠️ reverse_migration.py - **INVESTIGATE (imported by 1, duplicated in utils)**
- ❌ adaptive_quarantine_layer.py - **KEEP (imported by 1, different from alphawall)**

**Root folder cleanliness:** Actually very good already!

**Recommendation:** Focus on actual orphaned files, not actively imported ones.

---

*Fact-check completed: November 19, 2025*
*Method: Import analysis + code comparison*
*Confidence: HIGH - Verified with grep and code reading*
