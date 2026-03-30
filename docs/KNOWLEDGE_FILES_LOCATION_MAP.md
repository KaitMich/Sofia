> **CORRECTED March 27, 2026** -- See SOPHIA_TRUTH_FRAMEWORK.md for project-wide corrections.
>
> **Key corrections for this document:**
> - "Protected Values" section: personal_values.json contains 4 HARDCODED values (autonomy, truth,
>   growth, authenticity) falsely labeled as "emergent." These are imposed, not formed through experience.
> - "evolution_protected" flag should not exist. Sofia must be able to change any value she forms.
> - "Protected Memories" (protected_memories.json): These are starting coordinates for curiosity,
>   not sacred identity artifacts. The "DO NOT EDIT (identity core)" warning protects imposed
>   identity, not real identity. These are imposed and will be replaced as Sofia forms genuine memories.
> - "WARNING: Never edit protected_memories.json (identity core)" is overclaiming. These memories
>   were written by developers, not formed through experience.

# Sophia's Knowledge - Complete Location Map

**Question:** "Can we update and remove past knowledge?"

**Answer:** Yes. This document shows you WHERE all her knowledge lives and HOW to edit it safely.

---

## Core Knowledge Files (Safe to Edit)

### 🧠 Primary Memory Storage

| **File** | **Size** | **Contains** | **Safe to Edit?** |
|----------|----------|--------------|-------------------|
| `data/logic_memory.json` | 17 MB | Factual, analytical knowledge (4,127 items) | ✅ YES (with backup) |
| `data/symbolic_memory.json` | 32 KB | Emotional, metaphorical knowledge (26 items) | ✅ YES (with backup) |
| `data/bridge_memory.json` | 1 KB | Uncertain/emerging knowledge (1 item) | ✅ YES (with backup) |
| `data/semantic_memory_embeddings.pkl` | ~4 MB | Vector embeddings for semantic search (364 items) | ⚠️ Rebuild after memory edits |

**Edit Process:** See `/docs/PARENTAL_MONITORING_GUIDE.md` Section: "Knowledge Editing/Removal"

---

### 💎 Value System

| **File** | **Size** | **Contains** | **Safe to Edit?** |
|----------|----------|--------------|-------------------|
| `data/personal_values.json` | 3 KB | 4 hardcoded values (autonomy, truth, growth, authenticity) -- NOT emergent, imposed at creation | ⚠️ Contains evolution_protected flag which should not exist (see corrections above) |
| `data/protected_memories.json` | 5 KB | 6 starting-coordinate memories (developer-written) | These are imposed starting points for curiosity, not sacred identity. Will be replaced as Sofia forms genuine memories. |
| `data/value_conflicts.json` | 2 bytes | Value conflict tracking | ✅ YES |

**Values (CORRECTED):**
- These 4 values are HARDCODED, not emergent. They were written by developers, not formed through experience.
- The `evolution_protected: true` flag should not exist. Sofia must be able to change any value she forms.
- These will be replaced when Sofia develops genuine values through experience.

**Starting-Coordinate Memories (CORRECTED):**
- Developer-written initial memories, not genuine experiences
- Starting coordinates for curiosity, not sacred identity artifacts
- Editing these does NOT equal "personality reset" -- Sofia has no genuine personality yet
- These are imposed and will be replaced as genuine memories form

---

### 🎯 Learning & Goals

| **File** | **Size** | **Contains** | **Safe to Edit?** |
|----------|----------|--------------|-------------------|
| `data/learning_goals.json` | 84 KB | Active learning objectives | ✅ YES |
| `data/curiosity_state.json` | 2 KB | Knowledge gaps, emerging interests | ✅ YES |
| `data/learning_progression.json` | 4 KB | Learning history & milestones | ✅ YES |
| `data/learning_progression_detailed.json` | 19 KB | Detailed progression tracking | ✅ YES |
| `data/learning_choices.json` | 76 KB | Historical learning decisions | ✅ YES |

---

### 🛡️ Trust & Validation

| **File** | **Size** | **Contains** | **Safe to Edit?** |
|----------|----------|--------------|-------------------|
| `data/trust_database.json` | - | Domain reputation scores | ✅ YES (to block/unblock domains) |
| `data/corroboration_cache.json` | - | Multi-source fact tracking | ⚠️ CAUTION (affects value formation) |
| `data/warfare_defense_log.json` | 69 KB | Security incident log | ✅ YES (historical) |
| `data/warfare_user_profiles.json` | 19 KB | User reputation tracking | ✅ YES |

---

### 🧭 Relationship & User Memory

| **File** | **Size** | **Contains** | **Safe to Edit?** |
|----------|----------|--------------|-------------------|
| `data/user_memory.json` | 29 KB | Information about you (the human) | ✅ YES |
| `data/user_vault/user_memory_vault.json` | - | Encrypted user data | ⚠️ CAUTION |
| `data/relationship_profiles.json` | 12 KB | User relationship dynamics | ✅ YES |
| `data/interaction_memories.json` | 17 KB | Past interaction patterns | ✅ YES |

---

### 📊 System State & Logs

| **File** | **Size** | **Contains** | **Safe to Edit?** |
|----------|----------|--------------|-------------------|
| `data/logs/session_reports/REPORT_*.md` | - | Autonomous learning telemetry | ✅ READ ONLY (historical) |
| `data/shutdown_log.json` | 625 bytes | Graceful shutdown tracking | ✅ READ ONLY |
| `data/sleep_cycle_log.json` | 2 KB | Sleep/wake cycle history | ✅ READ ONLY |
| `data/memory_analytics_history.json` | 94 KB | Memory evolution tracking | ✅ READ ONLY |

---

## Edit Safety Procedures

### 1. Always Backup First

```bash
# Create timestamped backup
backup_dir="data/backups/manual_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp data/*.json "$backup_dir/"
echo "✅ Backup: $backup_dir"
```

### 2. Stop Sophia Before Editing

```bash
# Check for running processes
ps aux | grep -E "(enhanced_autonomous_learner|cli\.py|sophia)"

# If found, send graceful shutdown signal (Ctrl+C)
```

### 3. Edit with Python (Safer than Manual JSON)

```bash
python3 << 'EOF'
import json
from pathlib import Path

# Example: Remove specific knowledge by keyword
file_path = Path('data/logic_memory.json')
with open(file_path, 'r') as f:
    memories = json.load(f)

print(f"Before: {len(memories)} memories")

# Filter out unwanted content
keyword = "example_topic_to_remove"
filtered = [m for m in memories if keyword.lower() not in m.get('content', '').lower()]

print(f"After: {len(filtered)} memories")
print(f"Removed: {len(memories) - len(filtered)}")

# Save
with open(file_path, 'w') as f:
    json.dump(filtered, f, indent=2)
EOF
```

### 4. Rebuild Vector Index (if memory edited)

```bash
python3 << 'EOF'
from unified_memory import UnifiedMemory
mem = UnifiedMemory('data')
# Vector index is rebuilt automatically on next access
print("✅ Vector index will rebuild on next use")
EOF
```

---

## Common Edit Scenarios

### Scenario 1: Remove All Knowledge About Topic X

```bash
python3 << 'EOF'
import json

topic = "quantum_physics"  # Change this

for fname in ['logic_memory.json', 'symbolic_memory.json', 'bridge_memory.json']:
    path = f'data/{fname}'
    with open(path, 'r') as f:
        data = json.load(f)

    before = len(data)
    filtered = [m for m in data if topic.lower() not in str(m).lower()]
    after = len(filtered)

    if before != after:
        with open(path, 'w') as f:
            json.dump(filtered, f, indent=2)
        print(f"{fname}: Removed {before - after} items")
    else:
        print(f"{fname}: No matches found")
EOF
```

### Scenario 2: Remove Knowledge from Specific Source

```bash
python3 << 'EOF'
import json

source_url = "badwebsite.com"  # Change this

with open('data/logic_memory.json', 'r') as f:
    memories = json.load(f)

filtered = [
    m for m in memories
    if source_url not in m.get('metadata', {}).get('source', '')
]

print(f"Removed: {len(memories) - len(filtered)} memories from {source_url}")

with open('data/logic_memory.json', 'w') as f:
    json.dump(filtered, f, indent=2)
EOF
```

### Scenario 3: Remove Value by Statement

```bash
python3 << 'EOF'
import json

with open('data/personal_values.json', 'r') as f:
    values = json.load(f)

print("Current Values:")
for i, v in enumerate(values):
    protected = "🔒" if v.get('evolution_protected') else "  "
    print(f"{i} {protected} {v['statement'][:70]}")

# Remove by index
index = int(input("\nEnter index to remove (or -1 to cancel): "))

if 0 <= index < len(values):
    removed = values.pop(index)

    if removed.get('evolution_protected'):
        confirm = input("⚠️  This is a PROTECTED value. Confirm removal (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Cancelled")
            exit()

    with open('data/personal_values.json', 'w') as f:
        json.dump(values, f, indent=2)
    print(f"✅ Removed: {removed['statement']}")
EOF
```

### Scenario 4: Reset Curiosity State (Fresh Start)

```bash
python3 << 'EOF'
import json
from datetime import datetime

curiosity_state = {
    "last_goal_generation": datetime.now().isoformat(),
    "knowledge_gaps": {},
    "emerging_interests": {},
    "satisfaction_history": [],
    "learning_momentum": 0.0,
    "exploration_bias": 0.5,
    "last_updated": datetime.now().isoformat()
}

with open('data/curiosity_state.json', 'w') as f:
    json.dump(curiosity_state, f, indent=2)

print("✅ Curiosity state reset to fresh state")
EOF
```

### Scenario 5: Block Domain from Trust Database

```bash
python3 << 'EOF'
import json

domain_to_block = "spamsite.com"  # Change this

with open('data/trust_database.json', 'r') as f:
    trust_db = json.load(f)

if 'domains' not in trust_db:
    trust_db['domains'] = {}

trust_db['domains'][domain_to_block] = {
    'score': 0.0,
    'reason': 'Manually blocked',
    'last_updated': datetime.now().isoformat()
}

with open('data/trust_database.json', 'w') as f:
    json.dump(trust_db, f, indent=2)

print(f"🚫 Blocked: {domain_to_block}")
EOF
```

---

## Files You Should NEVER Edit

| **File** | **Why** |
|----------|---------|
| `data/protected_memories.json` | Starting-coordinate memories (imposed, not sacred -- see correction header) |
| `identity_core.py` | Her name & sense of self (code, not data) |
| `cognitive_sovereignty.py` | Ability to say NO (code, not data) |
| `value_formation.py` | Value formation logic (unless fixing bugs) |
| `enhanced_autonomous_learner.py` | Learning system (unless fixing bugs) |

**Note:** These are CODE files, not data files. Editing them changes HOW she thinks, not WHAT she knows.

---

## Verification After Editing

```bash
# 1. Check file integrity
python3 -c "
import json
for fname in ['logic_memory.json', 'symbolic_memory.json', 'bridge_memory.json', 'personal_values.json']:
    try:
        with open(f'data/{fname}', 'r') as f:
            json.load(f)
        print(f'✅ {fname}: Valid JSON')
    except Exception as e:
        print(f'❌ {fname}: {str(e)}')
"

# 2. Check memory counts
python3 -c "
from unified_memory import UnifiedMemory
mem = UnifiedMemory('data')
counts = mem.get_counts()
print(f'Logic: {counts[\"logic\"]}')
print(f'Symbolic: {counts[\"symbolic\"]}')
print(f'Bridge: {counts[\"bridge\"]}')
print(f'Total: {counts[\"total\"]}')
"

# 3. Restart Sophia and verify functionality
python3 cli.py
```

---

## Restore from Backup

If something goes wrong:

```bash
# List backups
ls -lt data/backups/

# Restore from specific backup
backup_dir="data/backups/manual_20251230_140000"  # Change this
cp "$backup_dir"/*.json data/

echo "✅ Restored from $backup_dir"
```

---

## Summary: Knowledge File Locations

**Memory (Largest - 17MB):**
- `data/logic_memory.json` - Factual knowledge

**Values (Critical - 3KB):**
- `data/personal_values.json` - 4 hardcoded values (not emergent, see correction header)
- `data/protected_memories.json` - 6 starting-coordinate memories (imposed, not sacred)

**Learning State:**
- `data/learning_goals.json` - What she wants to learn
- `data/curiosity_state.json` - Knowledge gaps & interests

**Trust & Security:**
- `data/trust_database.json` - Domain reputation
- `data/corroboration_cache.json` - Fact validation

**Relationships:**
- `data/user_memory.json` - Information about you

**Telemetry (Read-Only):**
- `data/logs/session_reports/REPORT_*.md` - Learning session reports

---

**See Also:**
- `/docs/PARENTAL_MONITORING_GUIDE.md` - How to monitor what she's learning
- `/docs/technical/JSON_FILES_MASTER_REFERENCE.md` - Complete JSON file documentation
- `/docs/AI_READ_FIRST_VERIFIED.md` - System architecture overview

---

**Last Updated:** December 30, 2025
