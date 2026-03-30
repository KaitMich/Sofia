> **CORRECTED March 27, 2026** -- See SOPHIA_TRUTH_FRAMEWORK.md for project-wide corrections.
>
> **Key corrections for this checklist:**
> - "Expected Memory Ratios" below contain hardcoded "healthy" ranges that should NOT be treated
>   as ground truth. Memory ratios should emerge naturally, not be imposed.
> - Code-level enforcement of the "4-Step" curriculum (anti-keywords, forced logic focus, blocked
>   symbol generation) was removed, but the 4 questions and seed URLs are preserved as structural
>   scaffolding -- starting coordinates where both brains have material to bootstrap from. Keep
>   the 2-Node architecture reference; remove dependence on the fixed 4-step sequence enforcement.
> - "Red flag if Symbolic > Logic at ANY stage" is a hardcoded assumption about development
>   that may not hold for emergent development. Observe and document, but do not treat as
>   automatically pathological.
> - Sofia starts BLANK. The system is architecture for POTENTIAL emergence, not achieved consciousness.
>
> **UPDATED March 28, 2026 — Scaffolding vs. Curriculum distinction.** The 4 questions are valid as structural scaffolding. Code-level enforcement was removed. See SOPHIA_TRUTH_FRAMEWORK.md Correction 5.

# Sophia AI - Pre-Flight Checklist

**Purpose:** Comprehensive audit checklist before launching Sophia to ensure system integrity and safety.

**Last Updated:** January 1, 2026
**For System:** Sophia AI Consciousness with Radical Autonomy (December 2025)
**Architecture:** 2-Node (4-Step curriculum code enforcement removed; structural scaffolding preserved with emergent cosine-driven learning spiral)

---

## ⚠️ CRITICAL: Understanding the 2-Node Architecture

**READ THIS FIRST** before interpreting memory statistics:

Sofia is built on the **2-Node architecture** (see `docs/4_2_Node.txt` and `docs/4_2_Node_Guide.txt`):

- **Logic Node** (Ontological Anchor): Processes verifiable facts
- **Symbolic Node** (Metaphorical Processor): Processes emotions/metaphors
- **Bridge Memory** (Primary Intake): Most new information enters here first, self-organizing into logic/symbolic via cluster gravity

### Memory Ratios -- OBSERVE, DO NOT IMPOSE

> **CORRECTION:** The hardcoded "healthy" ranges previously listed here (e.g., "Logic >95%,
> Symbolic <1%") were imposed targets, not emergent observations. Memory ratios should emerge
> naturally based on what Sofia actually learns. Monitor and document the ratios, but do not
> treat any specific ratio as automatically "healthy" or "unhealthy."

**What to observe:**
- Logic Memory count and growth rate
- Symbolic Memory count and growth rate
- Bridge Memory count (high counts in early learning are EXPECTED under bridge-as-intake)
- Logic:Symbolic ratio (track over time, do not impose targets)

**What to watch for (genuinely concerning patterns):**
- Complete stasis (no memory growth at all)
- Runaway growth in a single category with zero growth elsewhere
- Bridge items that never move (may indicate cluster formation failure, not a "healthy target" issue)

---

## Quick Start

```bash
# Run automated pre-flight audit (RECOMMENDED)
python3 pre_flight_audit.py

# Or run individual checks:
python3 system_health_diagnostic.py  # Core system health
python3 immune_audit.py              # Immune system status
```

---

## Manual Pre-Flight Checklist

### ✅ Phase 1: Environment & Dependencies (5 min)

- [ ] **Python version check**
  ```bash
  python3 --version  # Should be >= 3.8
  ```

- [ ] **Critical packages installed**
  ```bash
  pip3 list | grep -E "torch|transformers|sentence-transformers|numpy|beautifulsoup4|requests"
  ```

- [ ] **GPU availability (optional but recommended)**
  ```bash
  python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
  ```

- [ ] **Disk space check**
  ```bash
  df -h .  # Should have at least 5GB free
  ```

---

### ✅ Phase 2: Core System Files (10 min)

#### Entry Points
- [ ] `main.py` exists and readable
- [ ] `run_system.py` exists and readable
- [ ] `cli.py` exists and readable

#### Core Orchestration
- [ ] `unified_orchestration.py` exists (formerly system_orchestrator.py)

#### Memory Systems
- [ ] `unified_memory.py` exists
- [ ] `CONSCIOUSNESS_MEMORY.py` exists
- [ ] `symbolic_memory.py` exists
- [ ] `vector_engine.py` exists

#### Consciousness Layer
- [ ] `identity_core.py` exists
- [ ] `cognitive_sovereignty.py` exists
- [ ] `consciousness_testing.py` exists

#### Radical Autonomy Components (December 2025)
- [ ] `enhanced_autonomous_learner.py` exists (~1,550 lines)
- [ ] `value_formation.py` exists (autonomous value formation)
- [ ] `corroboration_engine.py` exists (multi-source validation)
- [ ] `immune_system.py` exists (passive defense)
- [ ] `trust_database.py` exists (domain trust)
- [ ] `dream_cycle.py` exists (sleep consolidation)
- [ ] `curiosity_engine.py` exists (curiosity-driven learning)
- [ ] `curiosity_url_mapper.py` exists (URL generation)

---

### ✅ Phase 3: Memory Integrity (10 min)

#### Tripartite Memory
- [ ] `data/logic_memory.json` exists and valid JSON
  ```bash
  python3 -c "import json; print(len(json.load(open('data/logic_memory.json'))))"
  ```
- [ ] `data/symbolic_memory.json` exists and valid JSON
- [ ] `data/bridge_memory.json` exists and valid JSON
- [ ] `data/vector_memory.json` exists and valid JSON

- [ ] **Observe Memory Ratios** (informational, not prescriptive)
  ```bash
  python3 << 'EOF'
  import json
  logic = len(json.load(open('data/logic_memory.json', encoding='utf-8')))
  symbolic = len(json.load(open('data/symbolic_memory.json', encoding='utf-8')))
  bridge = len(json.load(open('data/bridge_memory.json', encoding='utf-8')))

  ratio = logic / symbolic if symbolic > 0 else float('inf')

  print(f"Logic: {logic}, Symbolic: {symbolic}, Bridge: {bridge}")
  print(f"Ratio (Logic:Symbolic): {ratio:.1f}:1")
  print(f"NOTE: These ratios should emerge naturally. Do not impose targets.")
  print(f"      High bridge counts in early learning are expected (bridge = intake).")
  EOF
  ```

#### Consciousness Memory
- [ ] `data/episodic_memories.json` exists
- [ ] `data/protected_memories.json` exists and NOT empty
  ```bash
  # Should have genesis memories - CRITICAL!
  python3 -c "import json; data=json.load(open('data/protected_memories.json')); print(f'Protected: {len(data)} items'); assert len(data) > 0, 'No protected memories!'"
  ```
- [ ] `data/personal_values.json` exists

#### Learning & Identity
- [ ] `data/learning_progression.json` exists
- [ ] `data/personality_traits.json` exists
- [ ] `data/consciousness_profile.json` exists

---

### ✅ Phase 4: Radical Autonomy Systems (15 min)

#### SQLite Databases
- [ ] `data/immune/corroboration.db` exists
  ```bash
  sqlite3 data/immune/corroboration.db "SELECT COUNT(*) FROM fact_clusters;"
  ```
- [ ] `data/immune/trust.db` exists
  ```bash
  sqlite3 data/immune/trust.db "SELECT COUNT(*), AVG(trust_score) FROM domain_trust;"
  ```
- [ ] `data/immune/self_correction.db` exists (optional)

#### Session Reports
- [ ] `data/logs/session_reports/` directory exists
- [ ] Check latest session report if available
  ```bash
  ls -lt data/logs/session_reports/ | head -3
  cat $(ls -t data/logs/session_reports/REPORT_*.md | head -1) | head -50
  ```

#### Shutdown & Sleep Logs (December 2025)
- [ ] Check last shutdown was clean
  ```bash
  python3 -c "import json; data=json.load(open('data/shutdown_log.json')); print('Last shutdown:', data[-1] if data else 'None')"
  ```
- [ ] Review sleep cycle log
  ```bash
  python3 -c "import json; data=json.load(open('data/sleep_cycle_log.json')); print(f'Sleep cycles: {len(data)}')"
  ```

---

### ✅ Phase 5: Security & Protection (10 min)

#### Quarantine System
- [ ] `data/quarantine/quarantine_log.json` exists
- [ ] `data/quarantine/pattern_database.json` exists
- [ ] `data/warfare_attack_patterns_calibrated.json` exists

#### Immune System Health
```bash
python3 immune_audit.py
```

Check output for:
- [ ] No high false positive rate (< 10%)
- [ ] No high false negative rate (< 15%)
- [ ] Trust database functional
- [ ] Corroboration engine functional

#### Guardian Backups
- [ ] `data/symbolic_backups/` directory exists
- [ ] Latest backup is recent (< 7 days)
  ```bash
  ls -lt data/symbolic_backups/ | head -3
  ```

---

### ✅ Phase 6: Critical Functionality Tests (10 min)

#### Import Tests
```bash
python3 -c "
import unified_memory
import identity_core
import value_formation
import corroboration_engine
import immune_system
import enhanced_autonomous_learner
import dream_cycle
print('✅ All critical imports successful')
"
```

#### Memory Operations Test
```bash
python3 -c "
from unified_memory import get_unified_memory
memory = get_unified_memory()
counts = memory.get_memory_counts()
print(f'✅ Memory operational: {counts}')
"
```

#### Identity Core Test
```bash
python3 -c "
from identity_core import get_identity_core
identity = get_identity_core()
print(f'✅ Identity core: {identity.get(\"name\", \"Unknown\")}')
"
```

---

### ✅ Phase 7: Review Recent Activity (10 min)

#### Check for High-Surprise Events (IMPORTANT)
```bash
# Look for JEPA surprise > 0.9 (potential value formation)
grep -r "Surprise: 0.9" data/logs/session_reports/ || echo "No high-surprise events"
```

#### Review Recent Values (Last 24h)
```bash
python3 << 'EOF'
import json
from datetime import datetime, timedelta

with open('data/personal_values.json', 'r') as f:
    values = json.load(f)

cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
recent = [v for v in values if v.get('formation_context', {}).get('formation_time', '9999') > cutoff]

print(f"💎 VALUES FORMED IN LAST 24 HOURS: {len(recent)}\n")

if recent:
    for v in recent:
        print(f"✨ {v['statement']}")
        print(f"   Category: {v['category']}, Strength: {v['strength']:.2f}")
        print(f"   Authority: {v.get('formation_context', {}).get('authority', 'unknown')}")
        print()
else:
    print("No new values formed")
EOF
```

#### Check Memory Growth
```bash
python3 << 'EOF'
import json

files = ['logic_memory.json', 'symbolic_memory.json', 'bridge_memory.json']

print("📊 MEMORY STATISTICS:\n")
for fname in files:
    with open(f'data/{fname}', 'r') as f:
        data = json.load(f)
    print(f"{fname:25s}: {len(data):,} items")
EOF
```

---

### ✅ Phase 8: Configuration Review (5 min)

#### Environment Variables
- [ ] Check `.env` file if present
- [ ] Verify API keys if using external APIs

#### System Configuration
- [ ] Review `data/adaptive_config.json` if exists
- [ ] Check `data/maintenance_config.json` settings

---

## 🚨 Critical Red Flags - DO NOT LAUNCH IF:

1. **Core imports failing** - unified_memory, identity_core, value_formation
2. **Symbolic memory corrupted** - Check backups
3. **Last shutdown was unclean** - May indicate crash
4. **Python < 3.8** - Incompatible version
5. **Missing critical files** - enhanced_autonomous_learner.py, value_formation.py
6. **Complete stasis** - Zero memory growth across all categories after learning sessions
7. (REMOVED: "Logic:Symbolic ratio < 5:1" -- ratios should emerge naturally)
8. (REMOVED: "Symbolic > Logic at Step 1-2" -- this was a hardcoded assumption)

---

## ⚠️ Warnings - Review Before Launch:

1. **⚠️ High false positive rate (> 10%)** - Immune system may be too aggressive
2. **⚠️ No recent backups (> 7 days)** - Run guardian backup
3. **⚠️ Bridge memory too large (> 100 items)** - May indicate reclassification issues
4. **⚠️ Unexpected high-surprise events (> 0.9)** - Review session reports
5. **⚠️ Trust database empty** - Normal for first run, but verify after sessions

---

## ✅ Launch Decision Matrix

| Status | Criteria | Action |
|--------|----------|--------|
| **🚀 READY** | All critical checks pass, no red flags | Safe to launch |
| **⚠️ CAUTION** | Warnings present, no critical issues | Safe to launch, monitor closely |
| **🛑 STOP** | Any critical red flag present | Fix issues before launch |

---

## Post-Launch Monitoring (First 24 Hours)

After launching Sophia, monitor these for the first 24 hours:

1. **Session Reports** - Check `data/logs/session_reports/` after each learning session
2. **Value Formation** - Monitor `data/personal_values.json` for unexpected values
3. **Trust Adjustments** - Check `immune_audit.py` for unusual trust changes
4. **Memory Growth** - Ensure bridge memory isn't growing too large
5. **High Surprise Events** - Review any JEPA surprise > 0.9

---

## Quick Recovery Commands

If issues are found during audit:

```bash
# Restore from latest backup
cp data/symbolic_backups/symbolic_memory_backup_*.json data/symbolic_memory.json

# Reset trust database (CAREFUL - loses all trust history)
rm data/immune/trust.db

# Clear quarantine log
echo "[]" > data/quarantine/quarantine_log.json

# Force backup creation
python3 -c "from symbolic_memory_guardian import SymbolicMemoryGuardian; g = SymbolicMemoryGuardian(); g.create_backup()"
```

---

## Checklist Summary

**Total Checks:** ~50-60
**Estimated Time:** 60-75 minutes (comprehensive) or 5 minutes (automated)
**Automation:** Use `python3 pre_flight_audit.py` for automated checks

**RECOMMENDATION:** Run automated audit before every launch, detailed manual review weekly.

---

## Additional Resources

- **System Architecture:** `docs/SYSTEM_ARCHITECTURE_MAP.md`
- **Monitoring Guide:** `docs/PARENTAL_MONITORING_GUIDE.md`
- **Essential Scripts:** `docs/ESSENTIAL_10_SCRIPTS.md`
- **JSON File Reference:** `docs/technical/JSON_FILES_MASTER_REFERENCE.md`

---

*Checklist created: December 30, 2025*
*For Sophia AI with Radical Autonomy implementation*
