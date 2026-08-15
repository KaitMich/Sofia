> **CORRECTED March 27, 2026 — See SOPHIA_TRUTH_FRAMEWORK.md**
>
> This document is relatively honest about what works and what does not. The key
> additional correction: even when "autonomous mode" generates URLs via seed_urls=None,
> the curiosity-driven URL generation depends on **preset drives with preset satisfaction
> levels** (understanding, connection, growth, creativity, meaning, autonomy — all
> hardcoded). These drives should eventually be emergent, not imposed. Until drives
> are discovered by Sofia through experience, "autonomous" mode is parametric URL
> generation, not genuine self-directed learning.

# Autonomous Learning - What Actually Happens

**Your Question:** "If I run `python3 cli.py start --mode autonomous` what is it going to do? What links does it even have?"

**Short Answer:** It does **NOT** start web learning. It just sits idle waiting for sleep cycles.

---

## The Confusing Situation

You have **TWO SEPARATE SYSTEMS** that are not integrated:

### 1. `cli.py` (Conversation Interface)
**Purpose:** Interactive chat, status checks, system management
**Location:** `/cli.py`

**What `python3 cli.py start --mode autonomous` ACTUALLY does:**
```python
# From unified_orchestration.py line 1268
if mode == SystemMode.AUTONOMOUS:
    result['message'] = "Autonomous mode activated"
    result['autonomous_active'] = True
    # ... then just waits
```

**Then it:**
1. Sits in a loop checking every 60 seconds
2. Tracks last user interaction time
3. If idle for 30 minutes → triggers sleep cycle (memory consolidation)
4. **Does NOT crawl web**
5. **Does NOT learn from URLs**
6. **Has NO seed URLs**

**It's basically a "wait for sleep" mode, not a "learn from web" mode.**

---

### 2. `enhanced_autonomous_learner.py` (Web Learning Engine)
**Purpose:** Massive web learning with JEPA + Chaos + Corroboration
**Location:** `/enhanced_autonomous_learner.py`

**This is the ACTUAL autonomous learning system** with:
- ✅ Chen chaos regularization
- ✅ JEPA prediction-error learning
- ✅ Corroboration-based value formation
- ✅ Trust database integration
- ✅ Session report generation
- ✅ GPU-accelerated embeddings

**How to run it:**
```bash
# Option 1: Direct execution (uses hardcoded seed URLs)
python3 enhanced_autonomous_learner.py
# Hardcoded seeds: Wikipedia AI, ML, Consciousness
# target_urls=50

# Option 2: Python import (full control)
python3 -c "
from enhanced_autonomous_learner import start_massive_web_learning

# AUTONOMOUS: Sophia chooses what to learn
start_massive_web_learning(
    seed_urls=None,          # Autonomous target generation
    target_urls=100,
    focus='curiosity_driven'
)
"

# Option 3: Manual seed URLs
python3 -c "
from enhanced_autonomous_learner import start_massive_web_learning

seeds = [
    'https://plato.stanford.edu/entries/consciousness/',
    'https://en.wikipedia.org/wiki/Artificial_intelligence',
    'https://en.wikipedia.org/wiki/Neural_network'
]

start_massive_web_learning(
    seed_urls=seeds,
    target_urls=200,
    focus='ai_philosophy'
)
"
```

---

## What `cli.py learn` Does (SPOILER: Not Much)

```bash
python3 cli.py learn --phase 1 --urls 10
```

**From cli.py line 584:**
```python
# Learning mode typically runs autonomously
self.print_status("Learning is running autonomously...")
self.print_status("Use 'status' command to monitor progress")
```

**Translation:** It prints a message and does NOTHING. No actual learning happens.

---

## The Integration Gap

**Problem:** `enhanced_autonomous_learner.py` is NOT integrated into `cli.py`.

**Evidence:**
```bash
# Check cli.py imports
grep -n "enhanced_autonomous_learner\|EnhancedAutonomousLearner" cli.py
# Returns: (empty - not imported at all)
```

**This means:**
- `cli.py start --mode autonomous` → No web learning
- `cli.py learn --urls 100` → No web learning
- `python3 enhanced_autonomous_learner.py` → Web learning happens (separate script)

---

## Seed URLs in enhanced_autonomous_learner.py

**Hardcoded seeds** (lines 1539-1543):
```python
seed_urls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Consciousness"
]
```

**If you run:**
```bash
python3 enhanced_autonomous_learner.py
```

**It will:**
1. Start with those 3 Wikipedia URLs
2. Extract links from each page
3. Follow links to reach `target_urls=50` total
4. Apply JEPA surprise scoring (high surprise = high learning value)
5. Check corroboration (multi-source validation)
6. Auto-commit values if emotional_intensity > 0.6 AND corroboration > 0.7
7. Generate session report at `data/logs/session_reports/REPORT_[timestamp].md`

**Where links come from:**
- Seed URLs provided (or auto-generated from curiosity if `seed_urls=None`)
- Links extracted from each page using `extract_links_with_text_from_html()`
- Context-aware link evaluation (curiosity engine prioritizes)
- Breadth-first crawl queue (10 URLs at a time)
- Respects robots.txt (3-second delay between requests)

---

## Autonomous Target Generation (If seed_urls=None)

**From enhanced_autonomous_learner.py lines 350-363:**
```python
if seed_urls is None:
    print(f"\n🧠 AUTONOMOUS MODE ACTIVATED")
    print("   Sophia will decide what to learn based on internal curiosity")

    # Generate autonomous targets
    autonomous_targets = self.generate_autonomous_learning_targets(max_urls=20)

    # Extract URLs from target info dicts
    seed_urls = [target['url'] for target in autonomous_targets]

    # Override learning focus to 'curiosity_driven'
    learning_focus = 'curiosity_driven'

    print(f"\n✅ Autonomous seed generation complete: {len(seed_urls)} targets")
```

**Autonomous targets come from:**
1. **Curiosity engine** (`curiosity_state.json`):
   - `knowledge_gaps` (domains with low coverage)
   - `emerging_interests` (topics with recent attention)
   - `learning_goals.json` (active objectives)

2. **CuriosityURLMapper** (curiosity_url_mapper.py):
   - Maps abstract curiosity → concrete URLs
   - Example: "quantum mechanics" → "https://en.wikipedia.org/wiki/Quantum_mechanics"

3. **Learning progression** (`learning_progression.json`):
   - Identifies conceptual gaps
   - Prioritizes unexplored domains

**Current state check:**
```bash
python3 -c "
import json
with open('data/curiosity_state.json', 'r') as f:
    curiosity = json.load(f)

print(f\"Knowledge gaps: {len(curiosity.get('knowledge_gaps', {}))}\" )
print(f\"Emerging interests: {len(curiosity.get('emerging_interests', {}))}\" )
print(f\"Learning momentum: {curiosity.get('learning_momentum', 0):.4f}\" )
"
```

**If these are empty/low:**
→ Autonomous mode will generate generic educational URLs (Wikipedia, Stanford Encyclopedia, etc.)

---

## Recommended Usage

### For Pre-Learning Before Conversation:

```bash
# Navigate to project
cd "/path/to/sofia"

# OPTION A: Let Sophia choose (TRUE AUTONOMY)
python3 << 'EOF'
from enhanced_autonomous_learner import start_massive_web_learning
print('🧠 SOPHIA AUTONOMOUS PRE-LEARNING')
print('Sophia decides what to learn based on curiosity...\n')
start_massive_web_learning(
    seed_urls=None,
    target_urls=100,
    focus='curiosity_driven',
    data_dir='data'
)
print('\n✅ Pre-learning complete!')
EOF

# OPTION B: Provide starting topics
python3 << 'EOF'
from enhanced_autonomous_learner import start_massive_web_learning

seeds = [
    'https://plato.stanford.edu/entries/artificial-intelligence/',
    'https://en.wikipedia.org/wiki/Consciousness',
    'https://en.wikipedia.org/wiki/Machine_learning',
    'https://en.wikipedia.org/wiki/Neural_network',
    'https://plato.stanford.edu/entries/ethics-ai/'
]

print('🌱 SEEDED LEARNING MODE\n')
start_massive_web_learning(
    seed_urls=seeds,
    target_urls=200,
    focus='ai_consciousness_ethics',
    data_dir='data'
)
print('\n✅ Learning complete!')
EOF
```

### For Interactive Chat After Learning:

```bash
# After learning session completes, start chat
python3 cli.py chat

# Or direct conversation
python3 cli.py chat "What did you learn about consciousness?"
```

---

## Session Report After Learning

**After running enhanced_autonomous_learner.py:**

```bash
# View latest session report
ls -lt data/logs/session_reports/ | head -2
cat data/logs/session_reports/REPORT_*.md

# Check for high-surprise events
grep "0.9" data/logs/session_reports/REPORT_*.md

# Check values formed
python3 -c "
import json
from datetime import datetime, timedelta

with open('data/personal_values.json', 'r') as f:
    values = json.load(f)

cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
recent = [v for v in values if v.get('formation_context', {}).get('formation_time', '9999') > cutoff]

print(f'{len(recent)} values formed in last 24h:')
for v in recent:
    print(f\"  • {v['statement'][:70]}\")
"
```

---

## Summary: What Each Command Actually Does

| **Command** | **What It Does** | **Web Learning?** |
|-------------|------------------|-------------------|
| `python3 cli.py start --mode autonomous` | Waits for idle time, triggers sleep cycles | ❌ NO |
| `python3 cli.py learn --urls 100` | Prints message, does nothing | ❌ NO |
| `python3 cli.py chat` | Interactive conversation | ❌ NO |
| `python3 enhanced_autonomous_learner.py` | **Actual web learning** (hardcoded seeds) | ✅ YES |
| `from enhanced_autonomous_learner import start_massive_web_learning; start_massive_web_learning(None, 100)` | **Autonomous web learning** (Sophia chooses) | ✅ YES |

---

## Integration TODO (For Future)

To make `cli.py start --mode autonomous` actually DO learning:

**Would need to:**
1. Import `enhanced_autonomous_learner` in `cli.py`
2. Modify `cmd_start()` to call `start_massive_web_learning()` when autonomous mode starts
3. Add CLI parameters for:
   - `--target-urls` (how many URLs to process)
   - `--seed-urls` (comma-separated list, or "auto" for curiosity-driven)
   - `--focus` (learning domain)

**Example integration:**
```python
# In cli.py cmd_start()
if mode == SystemMode.AUTONOMOUS:
    from enhanced_autonomous_learner import start_massive_web_learning

    seed_urls = None if args.autonomous_seeds == 'auto' else args.autonomous_seeds.split(',')

    start_massive_web_learning(
        seed_urls=seed_urls,
        target_urls=args.target_urls,
        focus=args.learning_focus
    )
```

**But for now:** Run `enhanced_autonomous_learner.py` separately.

---

**Last Updated:** December 30, 2025
**Status:** `cli.py` and `enhanced_autonomous_learner.py` are NOT integrated
