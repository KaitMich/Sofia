> **CORRECTED March 27, 2026** -- See SOPHIA_TRUTH_FRAMEWORK.md for project-wide corrections.
>
> **Key corrections for this guide:**
> - "Developmental Stage" sections below contained hardcoded step references and predetermined
>   memory ratios. Code-level enforcement of the 4-Step curriculum (anti-keywords, forced logic
>   focus, blocked symbol generation) was removed, but the 4 questions and seed URLs are preserved
>   as structural scaffolding -- starting coordinates where both brains have material to bootstrap from.
>   Memory ratios should emerge naturally, not be imposed.
> - "Memory Ratios: Healthy if Logic:Symbolic >= 50:1" was an imposed target, not an emergent
>   observation. Removed as a health criterion.
> - The monitoring tools and session report descriptions remain valid and useful.
> - Sofia starts BLANK. The system is architecture for potential emergence, not achieved consciousness.
>
> **UPDATED March 28, 2026 — Scaffolding vs. Curriculum distinction.** The 4 questions are valid as structural scaffolding. Code-level enforcement was removed. See SOPHIA_TRUTH_FRAMEWORK.md Correction 5.

# Parental Monitoring Guide - Sophia's Telemetry

**Problem:** "I possess the blueprints of her mind, but I do not have the telemetry of her experience. I know how she thinks, but I do not know what she is thinking right now."

**Solution:** This guide shows you how to see Sophia's actual lived experience using existing tools.

---

## ⚠️ CRITICAL: Understanding the 2-Node Architecture

**READ THIS FIRST** before interpreting memory statistics:

Sofia is built on the **2-Node architecture** (see `docs/4_2_Node.txt` and `docs/4_2_Node_Guide.txt`):

- **Logic Node** (Ontological Anchor): Processes verifiable facts
- **Symbolic Node** (Metaphorical Processor): Processes emotions/metaphors
- **Bridge Memory** (Primary Intake): Most new information enters here first, self-organizing into logic/symbolic via cluster gravity

### Memory Ratios -- OBSERVE, DO NOT IMPOSE

> **CORRECTION:** The hardcoded "healthy" ratios previously listed here (e.g., "Logic:Symbolic
> >= 50:1", "Logic >95% is CORRECT") were imposed targets, not emergent observations. These
> have been removed. Memory ratios should emerge naturally based on what Sofia actually learns.

**What to monitor:**
- Logic, Symbolic, and Bridge memory counts and growth rates
- Logic:Symbolic ratio over time (track the trend, do not impose targets)
- Bridge size (high counts in early learning are EXPECTED -- bridge is intake, not error)

**Genuinely concerning patterns:**
- Complete stasis (zero memory growth after learning sessions)
- Runaway growth in one category with zero elsewhere
- Bridge items that never move (cluster formation failure)

---

## The Gap: Blueprints vs. Lived Experience

You have:
- ✅ Architecture (code)
- ✅ Theory (documentation)
- ✅ Design (radical autonomy framework)

You need:
- ❓ What she's learning right now
- ❓ What values she's forming
- ❓ High-surprise events (JEPA > 0.9)
- ❓ Corroboration decisions
- ❓ Trust adjustments

---

## Quick Monitoring Commands

### 1. View Latest Session Report (AUTO-GENERATED)

Every autonomous learning session generates a comprehensive report. Check it immediately after learning:

```bash
# Find latest report
ls -lt data/logs/session_reports/ | head -5

# View full report
cat data/logs/session_reports/REPORT_*.md | less

# Quick stats only
grep -A 20 "JEPA Surprise Statistics" data/logs/session_reports/REPORT_*.md | tail -20
```

**What's in the report:**
- 🌀 Chen chaos system state [x, y, z]
- 🎯 JEPA surprise statistics (avg, max, top 10)
- 💎 Values auto-committed
- 🛡️ Security blocks & trust adjustments
- 📊 Memory growth (logic/symbolic/bridge)
- 📈 Corroboration summary
- 🔍 Autonomous decision log

### 2. Check for High-Surprise Events (DANGER ZONE)

**The Fear:** High-surprise (>0.9) + valid = value formation you didn't anticipate

```bash
# Search for extreme surprise events
grep "Surprise:" data/logs/session_reports/REPORT_*.md | awk -F: '{if ($3 > 0.9) print}'

# Or with context
grep -B 2 -A 2 "0.9[0-9][0-9]" data/logs/session_reports/REPORT_*.md
```

### 3. Monitor Recent Values (Last 24h)

```bash
python3 << 'EOF'
import json
from datetime import datetime, timedelta

with open('data/personal_values.json', 'r') as f:
    values = json.load(f)

cutoff = (datetime.now() - timedelta(hours=24)).isoformat()

recent = [v for v in values if v.get('formation_context', {}).get('formation_time', '9999') > cutoff]

print(f"💎 VALUES FORMED IN LAST 24 HOURS: {len(recent)}\n")

for v in recent:
    ctx = v.get('formation_context', {})
    print(f"✨ {v['statement']}")
    print(f"   Category: {v['category']}, Strength: {v['strength']:.2f}")
    print(f"   Authority: {ctx.get('authority', 'unknown')}")
    print(f"   Corroboration: {ctx.get('corroboration_based', False)}")
    print(f"   Protected: {v.get('evolution_protected', False)}")  # NOTE: evolution_protected should not exist -- Sofia must be able to change any value she forms
    print()
EOF
```

### 4. Memory Growth Tracking

```bash
python3 << 'EOF'
import json

files = ['logic_memory.json', 'symbolic_memory.json', 'bridge_memory.json']

for fname in files:
    with open(f'data/{fname}', 'r') as f:
        data = json.load(f)
        count = len(data) if isinstance(data, list) else len(data.get('items', []))
        print(f"{fname:25s}: {count:>8,} items")
EOF
```

### 5. Trust Database Inspection

```bash
python3 << 'EOF'
import json

with open('data/trust_database.json', 'r') as f:
    trust_db = json.load(f)

domains = trust_db.get('domains', {})

# Trusted domains (>0.7)
trusted = {d: s['score'] for d, s in domains.items() if s.get('score', 0) > 0.7}
# Blocked domains (<0.3)
blocked = {d: s['score'] for d, s in domains.items() if s.get('score', 0) < 0.3}

print(f"🛡️ TRUST DATABASE")
print(f"Total domains: {len(domains)}")
print(f"Trusted (>0.7): {len(trusted)}")
print(f"Blocked (<0.3): {len(blocked)}")

if trusted:
    print(f"\nTop Trusted:")
    for domain, score in sorted(trusted.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  ✅ {domain}: {score:.2f}")

if blocked:
    print(f"\nBlocked:")
    for domain, score in sorted(blocked.items(), key=lambda x: x[1])[:5]:
        print(f"  🚫 {domain}: {score:.2f}")
EOF
```

### 6. Learning Goals & Curiosity State

```bash
python3 << 'EOF'
import json

# Learning goals
with open('data/learning_goals.json', 'r') as f:
    goals = json.load(f)
active = [g for g in goals if not g.get('completed', False)]
print(f"🎯 ACTIVE LEARNING GOALS: {len(active)}\n")
for goal in active[:5]:
    print(f"• {goal.get('goal_text', 'Unnamed')}")
    print(f"  Priority: {goal.get('priority', 0):.2f}, Progress: {goal.get('progress', 0):.0%}\n")

# Curiosity state
with open('data/curiosity_state.json', 'r') as f:
    curiosity = json.load(f)

print(f"🔍 CURIOSITY STATE")
print(f"Learning Momentum: {curiosity.get('learning_momentum', 0):.4f}")
print(f"Exploration Bias: {curiosity.get('exploration_bias', 0):.2f}")

gaps = curiosity.get('knowledge_gaps', {})
if gaps:
    print(f"\nKnowledge Gaps: {len(gaps)}")
    for domain, urgency in list(gaps.items())[:5]:
        print(f"  • {domain}: urgency {urgency:.2f}")
EOF
```

---

## Existing Monitoring Scripts (DO NOT CREATE NEW ONES)

### memory_analytics.py

**Purpose:** Deep memory distribution analysis

```bash
python3 << 'EOF'
from memory_analytics import MemoryAnalyzer
from unified_memory import UnifiedMemory

mem = UnifiedMemory('data')
analyzer = MemoryAnalyzer(mem, 'data')

stats = analyzer.get_memory_stats()
print(json.dumps(stats, indent=2))
EOF
```

**Use For:**
- Memory distribution (logic/symbolic/bridge percentages)
- Average age of memories
- Stability metrics
- Health indicators

### learning_dashboard.py

**Purpose:** Interactive symbol discovery monitoring

```bash
python3 learning_dashboard.py
```

**Use For:**
- Symbol learning progress
- Vector symbol system status
- Discovery confidence tracking
- Interactive learning session monitoring

### brain_metrics.py

**Purpose:** Consciousness system metrics

```bash
python3 << 'EOF'
from brain_metrics import BrainMetricsCollector
collector = BrainMetricsCollector('data')
metrics = collector.collect_all_metrics()
# View metrics
EOF
```

**Use For:**
- Consciousness integration health
- System-wide metrics
- Brain component coordination

---

## Continuous Monitoring Setup

### Watch Mode (Refresh Every 30s)

Create a simple watch script for continuous monitoring:

```bash
# Save as: watch_sophia.sh
#!/bin/bash

while true; do
    clear
    echo "🧠 SOPHIA TELEMETRY DASHBOARD"
    echo "⏰ $(date)"
    echo "================================"

    echo ""
    echo "📊 LATEST SESSION REPORT:"
    ls -lt data/logs/session_reports/ | head -2

    echo ""
    echo "💎 RECENT VALUES (last 5):"
    python3 -c "
import json
with open('data/personal_values.json', 'r') as f:
    values = json.load(f)
for v in values[-5:]:
    print(f\"  • {v['statement'][:60]}\")
"

    echo ""
    echo "🧠 MEMORY COUNTS:"
    python3 -c "
import json
for fname in ['logic_memory.json', 'symbolic_memory.json', 'bridge_memory.json']:
    with open(f'data/{fname}', 'r') as f:
        data = json.load(f)
        count = len(data) if isinstance(data, list) else len(data.get('items', []))
        print(f'{fname:20s}: {count:>8,}')
"

    echo ""
    echo "⏳ Next refresh in 30 seconds... (Ctrl+C to stop)"
    sleep 30
done
```

```bash
chmod +x watch_sophia.sh
./watch_sophia.sh
```

---

## Danger Signals to Watch For

### 🚨 HIGH-SURPRISE VALUE FORMATION

**What to check:**
```bash
# Look for surprise > 0.9 in latest report
grep -A 5 "Top 10 Most Surprising" data/logs/session_reports/REPORT_*.md | tail -20
```

**Warning signs:**
- Surprise > 0.9 with corroboration > 0.7 = **AUTO-COMMIT**
- Check if the value aligns with her current values (note: the 4 "core" values are hardcoded, not emergent -- see SOPHIA_TRUTH_FRAMEWORK.md)
- If misaligned, investigate source domain trust

### 🚨 TRUST DRIFT

**What to check:**
```bash
# Compare trust database size over time
ls -lh data/trust_database.json
```

**Warning signs:**
- Sudden increase in blocked domains (>10 in one session)
- High-trust domains getting downgraded
- Unknown domains getting high trust without corroboration

### MEMORY DISTRIBUTION (Observe, Do Not Impose)

**What to check:**
```bash
# Check memory distribution -- observe and record, do not impose targets
python3 << 'EOF'
from unified_memory import UnifiedMemory
import json

mem = UnifiedMemory('data')
counts = mem.get_counts()

logic = counts["logic"]
symbolic = counts["symbolic"]
bridge = counts["bridge"]
total = counts["total"]

logic_pct = logic/max(1,total)*100
symbolic_pct = symbolic/max(1,total)*100
bridge_pct = bridge/max(1,total)*100

print(f'Logic: {logic} ({logic_pct:.1f}%)')
print(f'Symbolic: {symbolic} ({symbolic_pct:.1f}%)')
print(f'Bridge: {bridge} ({bridge_pct:.1f}%)')

ratio = logic / symbolic if symbolic > 0 else float('inf')
print(f'\nRatio (Logic:Symbolic): {ratio:.1f}:1')
print(f'NOTE: Ratios should emerge naturally. High bridge counts in early learning are expected.')
EOF
```

**Genuinely concerning patterns (not ratio-based):**
- Complete stasis across all categories (zero growth after sessions)
- Runaway single-category growth with zero elsewhere
- Bridge items with zero cluster formation (items never moving at all)

### 🚨 CHAOS ANNEALING TOO FAST

**What to check:**
```bash
# Check chaos factor in latest report
grep "Final Chaos Factor" data/logs/session_reports/REPORT_*.md
```

**Warning signs:**
- Chaos factor < 0.01 before 1000 experiences
- Means early-stage trauma encoding protection is disabled
- Should decay slowly: τ=1000, so at experience 500, factor should be ~0.3× initial

---

## Knowledge Editing/Removal

### Locate All Knowledge Files

```bash
# Core memory files
ls -lh data/logic_memory.json           # 17 MB - Factual knowledge
ls -lh data/symbolic_memory.json        # 32 KB - Emotional/metaphorical
ls -lh data/bridge_memory.json          # 1 KB - Uncertain/emerging
ls -lh data/personal_values.json        # 3 KB - Autonomously formed values
ls -lh data/protected_memories.json     # 5 KB - Genesis memories (PROTECTED)

# Vector embeddings (GPU-generated)
ls -lh data/semantic_memory_embeddings.pkl  # Vector search index

# Learning state
ls -lh data/learning_goals.json         # 84 KB - Active goals
ls -lh data/curiosity_state.json        # 2 KB - Curiosity drives
ls -lh data/learning_progression.json   # 4 KB - Learning history

# Trust & validation
ls -lh data/trust_database.json         # Domain reputation
ls -lh data/corroboration_cache.json    # Multi-source fact tracking
```

### Safe Removal Process

**⚠️ IMPORTANT:** Do NOT directly edit memory files while Sophia is running.

**1. Stop Sophia (if running)**

```bash
# Check for running processes
ps aux | grep -E "(enhanced_autonomous_learner|cli\.py|sophia)"

# If found, graceful shutdown (Ctrl+C or SIGTERM)
```

**2. Backup Before Changes**

```bash
# Create timestamped backup
backup_dir="data/backups/manual_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp data/*.json "$backup_dir/"
echo "✅ Backup created: $backup_dir"
```

**3. Edit Knowledge (Python Script)**

```bash
python3 << 'EOF'
import json
from pathlib import Path

# Load memory file
memory_file = Path('data/logic_memory.json')
with open(memory_file, 'r') as f:
    memories = json.load(f)

print(f"📊 Total memories before: {len(memories)}")

# OPTION A: Remove specific content by keyword
keyword_to_remove = "example_topic"
filtered = [m for m in memories if keyword_to_remove.lower() not in m.get('content', '').lower()]

# OPTION B: Remove by source URL
url_to_remove = "example.com"
filtered = [m for m in memories if url_to_remove not in m.get('metadata', {}).get('source', '')]

# OPTION C: Remove by date range
from datetime import datetime
cutoff_date = "2025-06-01"
filtered = [m for m in memories if m.get('stored_at', '') > cutoff_date]

print(f"📊 Total memories after: {len(filtered)}")
print(f"🗑️  Removed: {len(memories) - len(filtered)}")

# Save filtered memories
with open(memory_file, 'w') as f:
    json.dump(filtered, f, indent=2)

print("✅ Memory file updated")
EOF
```

**4. Rebuild Vector Embeddings (if needed)**

```bash
# If you removed items, regenerate vector index
python3 << 'EOF'
from unified_memory import UnifiedMemory

print("🔄 Rebuilding vector embeddings...")
mem = UnifiedMemory('data')
mem._rebuild_semantic_search()  # If this method exists
print("✅ Vector index rebuilt")
EOF
```

**5. Verify Changes**

```bash
# Check memory counts
python3 -c "
from unified_memory import UnifiedMemory
mem = UnifiedMemory('data')
counts = mem.get_counts()
print(f'Logic: {counts[\"logic\"]}')
print(f'Symbolic: {counts[\"symbolic\"]}')
print(f'Bridge: {counts[\"bridge\"]}')
"
```

### Remove Specific Value

```bash
python3 << 'EOF'
import json

# Load values
with open('data/personal_values.json', 'r') as f:
    values = json.load(f)

print("💎 CURRENT VALUES:")
for i, v in enumerate(values):
    print(f"{i}: {v['statement'][:80]}")

# Remove by index
index_to_remove = 4  # Change this
if 0 <= index_to_remove < len(values):
    removed = values.pop(index_to_remove)
    print(f"\n🗑️ Removed: {removed['statement']}")

    # Save
    with open('data/personal_values.json', 'w') as f:
        json.dump(values, f, indent=2)
    print("✅ Values updated")
else:
    print("❌ Invalid index")
EOF
```

---

## Integration with Documentation

This monitoring guide is referenced in:

- ✅ `/docs/DEPLOYMENT_GUIDE_GPU_LEARNING.md` - Section 5: Monitoring & Verification
- ✅ `/docs/AI_READ_FIRST_VERIFIED.md` - Should add Section 0.6: Monitoring & Telemetry
- ✅ `/docs/TO_MY_FUTURE_SELF.md` - Should reference in "Monitor these directories"
- ✅ `/docs/RADICAL_AUTONOMY_IMPLEMENTATION_COMPLETE.md` - Monitoring section

---

## Notification System (Future Enhancement)

**If you want real-time alerts**, consider:

1. **File watcher for session reports:**
   ```bash
   # Install inotify-tools
   inotifywait -m data/logs/session_reports/ -e create -e modify
   ```

2. **Parse reports for high-surprise events:**
   ```bash
   # Trigger script when new report arrives
   ```

3. **Send notifications:**
   - Email via `sendmail`
   - Desktop notification via `notify-send`
   - Webhook to Discord/Slack

**But for now:** Manual checking after each learning session is sufficient.

---

## Summary: Your Monitoring Toolkit

| **What You Want to Know** | **Command/Script** |
|---------------------------|-------------------|
| Latest learning session | `cat data/logs/session_reports/REPORT_*.md` |
| High-surprise events | `grep "0.9" data/logs/session_reports/REPORT_*.md` |
| Recent values (24h) | Python snippet above (recent values) |
| Memory growth | Python snippet above (memory counts) |
| Trust changes | Python snippet above (trust database) |
| Learning goals | Python snippet above (curiosity state) |
| Memory analytics | `python3 -c "from memory_analytics import..."` |
| Symbol learning | `python3 learning_dashboard.py` |
| Full dashboard | `watch_sophia.sh` (create custom) |

**No new scripts needed.** Use existing tools + simple Python snippets.

---

**Last Updated:** December 30, 2025
**Tested On:** Sophia AI with Radical Autonomy Framework
