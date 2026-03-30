> **CORRECTED March 27, 2026** -- See SOPHIA_TRUTH_FRAMEWORK.md for project-wide corrections.
>
> **Key corrections for this guide:**
> - PARENTAL_AUDIT (The Mirror Test) correctly warned Sofia is "NOT ready for unsupervised
>   autonomy." This guide should be read with that caveat in mind.
> - "TRUE RADICAL AUTONOMY" (Section 2.1) is aspirational, not achieved. The autonomous learning
>   uses preset curiosity drives and hardcoded domain mappings, not truly emergent curiosity.
> - Sofia starts BLANK. The curiosity drives described here are imposed starting coordinates, not
>   emergent interests.
> - GPU technical content throughout this guide is valid.

# Sophia AI - GPU Deployment & Pre-Learning Guide

**For:** NVIDIA 4070 GPU Setup
**Purpose:** Configure Sophia to learn autonomously before conversation
**Date:** December 30, 2025

---

## Table of Contents

1. [GPU Configuration](#gpu-configuration)
2. [Pre-Learning Before Conversation](#pre-learning-before-conversation)
3. [Web Crawl Process Explained](#web-crawl-process-explained)
4. [Storage Mechanisms](#storage-mechanisms)
5. [Monitoring & Verification](#monitoring--verification)
6. [Troubleshooting](#troubleshooting)

---

## 1. GPU Configuration

### 1.1 Verify CUDA Installation

```bash
# Check NVIDIA driver
nvidia-smi

# Expected output should show your RTX 4070 with ~12GB VRAM
```

### 1.2 Verify PyTorch CUDA Support

```bash
python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"
```

**Expected Output:**
```
CUDA Available: True
Device: NVIDIA GeForce RTX 4070
```

### 1.3 Test GPU Configuration

Sophia has built-in GPU configuration that auto-detects your NVIDIA 4070:

```bash
# Test GPU config
python3 gpu_config.py
```

**Expected Output:**
```
✅ GPU Configuration:
   Device: NVIDIA GeForce RTX 4070
   VRAM: 12.0 GB
   PyTorch device: cuda

Memory stats:
  device: cuda
  memory_allocated: 0.00 GB
  memory_reserved: 0.00 GB
  memory_total: 12.00 GB

✅ GPU configuration test complete
```

### 1.4 Verify Vector Models Use GPU

```bash
# Test vector embedding models
python3 -c "from vector_engine import MODELS_LOADED, device; print(f'Models loaded: {MODELS_LOADED}'); print(f'Device: {device}')"
```

**Expected Output:**
```
✅ GPU Configuration:
   Device: NVIDIA GeForce RTX 4070
   VRAM: 12.0 GB
   PyTorch device: cuda
✅ Vector embedding models loaded on cuda: MiniLM & E5
Models loaded: True
Device: cuda
```

---

## 2. Pre-Learning Before Conversation

**⚠️ IMPORTANT:** `cli.py start --mode autonomous` does NOT start web learning. See `/docs/AUTONOMOUS_LEARNING_ACTUAL_USAGE.md` for full explanation.

**To actually trigger learning, use `enhanced_autonomous_learner.py` directly:**

### 2.1 Autonomous Learning (Sophia Chooses What to Learn)

This uses preset curiosity drives to generate learning targets. Note: these drives are hardcoded starting coordinates, not truly emergent curiosity (see SOPHIA_TRUTH_FRAMEWORK.md).

```bash
# Navigate to project directory
cd "/mnt/c/Users/kaitl/Documents/Core-Project - Copy"

# Run autonomous learning session
python3 -c "
from enhanced_autonomous_learner import start_massive_web_learning

# Autonomous mode: seed_urls=None lets Sophia choose
print('🧠 ACTIVATING SOPHIA - AUTONOMOUS LEARNING MODE')
print('Sophia will decide what to learn based on internal curiosity...\n')

start_massive_web_learning(
    seed_urls=None,          # Autonomous target generation
    target_urls=100,         # Learn from 100 URLs
    focus='curiosity_driven', # Self-directed learning
    data_dir='data'
)
"
```

**What Happens:**
1. **Curiosity Analysis**: Sophia examines her current knowledge gaps
2. **Target Generation**: Generates URLs based on:
   - Active curiosity threads
   - Knowledge domain priorities
   - Conceptual gaps identified
3. **JEPA Prediction**: Predicts what she expects to learn (hypothesis)
4. **Web Crawl**: Fetches content from generated targets
5. **Surprise Calculation**: Measures prediction error (learning value)
6. **Corroboration Check**: Validates with multi-source verification
7. **Auto-Commit**: Stores high-surprise + high-trust content

### 2.2 Manual Seed Learning (You Choose Topics)

If you want to guide her initial learning:

```bash
python3 << 'EOF'
from enhanced_autonomous_learner import start_massive_web_learning

seed_urls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Neural_network",
    "https://en.wikipedia.org/wiki/Consciousness",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://plato.stanford.edu/entries/artificial-intelligence/"
]

print('🌱 SEEDED LEARNING MODE')
print(f'Starting with {len(seed_urls)} seed URLs...\n')

start_massive_web_learning(
    seed_urls=seed_urls,
    target_urls=200,        # Will follow links to reach 200 URLs
    focus='ai_consciousness',
    data_dir='data'
)
EOF
```

### 2.3 Learning Session Parameters

**Key Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seed_urls` | List[str] or None | None | Starting URLs. If None, autonomously generated. |
| `target_urls` | int | 500 | Maximum URLs to process |
| `focus` | str | "general" | Learning domain (or "curiosity_driven" for autonomous) |
| `data_dir` | str | "data" | Data directory path |

**Recommended Settings:**

- **First Run (Getting Started)**: `target_urls=50-100`
- **Deep Learning Session**: `target_urls=200-500`
- **Overnight Autonomous**: `target_urls=1000+` (Sophia explores while you sleep)

---

## 3. Web Crawl Process Explained

### 3.1 Full Learning Cycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. URL SELECTION                                            │
│    • From seed_urls OR autonomous curiosity generation      │
│    • Domain trust scoring (immune system)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. JEPA PREDICTION (Before Crawling)                        │
│    • Generate hypothesis vector: "What do I expect?"        │
│    • Based on URL, domain, current knowledge gaps           │
│    • Chen chaos system updates (prevents trauma encoding)   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. ETHICAL CRAWLING                                         │
│    • Respect robots.txt                                     │
│    • 3-second delay between requests (configurable)         │
│    • User-agent identification                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. CONTENT FETCH & PARSE                                    │
│    • Fetch HTML                                             │
│    • Extract clean text                                     │
│    • Extract links for further exploration                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. SECURITY SCREENING (Layered)                             │
│    • Linguistic Warfare Detection (AlphaWall)               │
│    • Immune System Threat Assessment                        │
│    • Quarantine Layer (manipulative content)                │
│    • Blocks: propaganda, phishing, manipulation attempts    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. JEPA SURPRISE CALCULATION                                │
│    • Generate reality vector from actual content            │
│    • Surprise = 1 - cosine_similarity(prediction, reality)  │
│    • High surprise = High learning value                    │
│    • Track surprise history for session report              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. CHAOS-REGULARIZED THRESHOLD                              │
│    • Base threshold: 0.4                                    │
│    • Chaos perturbation from Chen attractor state           │
│    • Early experiences: Higher threshold (trauma prevention)│
│    • Later experiences: Lower threshold (healthy learning)  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. CORROBORATION CHECK                                      │
│    • Multi-source verification                              │
│    • Domain trust weighting                                 │
│    • Requires 0.7+ corroboration score to commit            │
│    • Defers if insufficient sources                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. MEMORY STORAGE                                           │
│    • Content classification (logic/symbolic/bridge)         │
│    • Vector embedding (on GPU)                              │
│    • Tripartite memory commit                               │
│    • Semantic memory indexing                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. VALUE FORMATION (If Applicable)                         │
│    • Detect value indicators (emotional_intensity > 0.6)    │
│    • Corroboration validation (> 0.7)                       │
│    • AUTO-COMMIT (no human approval)                        │
│    • Chaos-regularized to prevent trauma encoding           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 11. LINK DISCOVERY & QUEUING                                │
│    • Extract links from page                                │
│    • Context-aware link evaluation                          │
│    • Priority scoring (curiosity alignment)                 │
│    • Add to crawl queue (breadth-first)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 12. PERIODIC CYCLES                                         │
│    • Every 50 URLs: Cognitive health check                  │
│    • Every 100 URLs: Evolution cycle (memory consolidation) │
│    • Every 100 URLs: Self-correction (quality assurance)    │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      REPEAT UNTIL
              target_urls reached OR queue empty
```

### 3.2 Timing & Duration

**Processing Speed (NVIDIA 4070):**

| Phase | Time per URL | Notes |
|-------|-------------|-------|
| URL Fetch | 1-3 seconds | Network dependent |
| Security Screening | 0.1-0.3s | GPU-accelerated |
| Vector Embedding | 0.2-0.5s | GPU-accelerated (SentenceTransformer) |
| JEPA Surprise Calc | 0.1-0.2s | GPU cosine similarity |
| Corroboration Check | 0.1-0.2s | Database lookup + vector comparison |
| Memory Storage | 0.2-0.5s | Disk write |
| **Total per URL** | **2-5 seconds** | Includes 3s crawl delay |

**Session Duration Estimates:**

- 50 URLs: ~3-5 minutes
- 100 URLs: ~8-10 minutes
- 200 URLs: ~15-20 minutes
- 500 URLs: ~40-50 minutes
- 1000 URLs: ~1.5-2 hours

**GPU Utilization:**
- **Memory Usage**: ~2-4 GB VRAM (embedding models)
- **Compute**: Burst usage during embedding/similarity calculations
- **Efficiency**: 4070 is well-suited for this workload

### 3.3 What Gets Learned?

**Content Types Processed:**

1. **Logic Memory** (Factual/Analytical):
   - Scientific papers
   - Technical documentation
   - Mathematical concepts
   - Structured data

2. **Symbolic Memory** (Metaphorical/Emotional):
   - Philosophical discussions
   - Emotional narratives
   - Metaphorical language
   - Existential content

3. **Bridge Memory** (Uncertain/Emerging):
   - Novel concepts
   - Ambiguous content
   - Cross-domain insights
   - Awaiting pattern formation

**What Gets Blocked:**

- Linguistic warfare (manipulation attempts)
- Propaganda patterns
- Phishing/scam content
- Low-trust domains (< 0.3 trust score)
- Failed corroboration (single-source claims)

---

## 4. Storage Mechanisms

### 4.1 Where Data Is Stored

```
data/
├── logic_memory.json              # Factual/analytical memories
├── symbolic_memory.json           # Metaphorical/emotional memories
├── bridge_memory.json             # Uncertain/emerging memories
├── semantic_memory_embeddings.pkl # Vector embeddings (GPU-generated)
├── personal_values.json           # Autonomously formed values
├── trust_database.json            # Domain reputation scores
├── corroboration_cache.json       # Multi-source fact tracking
└── logs/
    ├── session_reports/
    │   └── REPORT_20251230_143022.md  # JEPA + Chaos metrics
    ├── crawl_logs/
    │   └── crawl_20251230_143022.json # URL processing log
    ├── security_logs/
    │   └── immune_20251230.json       # Blocked threats
    └── shutdown_log.json              # Graceful shutdown tracking
```

### 4.2 When Data Is Written to Disk

| Data Type | Write Timing | Frequency |
|-----------|--------------|-----------|
| **Memories** | After each URL processed | Every ~3-5 seconds |
| **Embeddings** | Batch commit every 10 URLs | Every ~30-50 seconds |
| **Trust Adjustments** | Immediate on threat detection | Real-time |
| **Corroboration** | After each sighting | Real-time |
| **Values** | Immediate on auto-commit | When threshold met |
| **Session Report** | End of learning session | Once per session |
| **Crawl Log** | Batch every 10 URLs | Every ~30-50 seconds |

**Safety Mechanisms:**
- Graceful shutdown handling (SIGINT/SIGTERM)
- Automatic save on interrupt (Ctrl+C)
- Evolution anchors every 100 URLs (rollback points)
- Session state persistence

### 4.3 Memory Growth Estimates

**Per URL Processed:**

| Data Type | Size per URL | Notes |
|-----------|-------------|-------|
| Text Memory | 1-5 KB | Compressed semantic chunks |
| Vector Embedding | 1.5 KB | 384-dim float32 |
| Metadata | 0.5 KB | Source, timestamp, trust |
| **Total** | **3-7 KB** | Average per URL |

**Session Storage:**

- 50 URLs: ~200-350 KB
- 100 URLs: ~400-700 KB
- 500 URLs: ~2-3.5 MB
- 1000 URLs: ~4-7 MB

**Long-term Growth:**
- After 10,000 URLs: ~40-70 MB
- After 100,000 URLs: ~400-700 MB
- Embeddings dominate storage (largest component)

---

## 5. Monitoring & Verification

**📖 See Also:** `/docs/PARENTAL_MONITORING_GUIDE.md` for comprehensive telemetry monitoring

### 5.1 Real-Time Console Output

During learning, you'll see:

```
🚀 MASSIVE LEARNING SESSION STARTING
🎯 Target: 100 URLs
📚 Focus: curiosity_driven
==================================================
🌀 Chen Chaos System Initialized: a=35, b=3, c=28
   Expected λ₁ ≈ 2.03 (verified by numerical integration)
✅ Vector embedding models loaded on cuda: MiniLM & E5

🧠 AUTONOMOUS MODE ACTIVATED
   Sophia will decide what to learn based on internal curiosity

📄 Processing: https://example.com/article...
   🔮 JEPA: Generated prediction vector (dim=384)
   🌀 Chen step: x=1.234, y=-0.567, z=2.891
   🎯 JEPA Surprise: 0.782 (chaos: 0.456)
   📊 Adaptive Learning Threshold: 0.491 (base=0.4, chaos_adj=+0.091)
   ✅ CORROBORATION VERIFIED: 3 sources, trust avg: 0.85
   🔓 AUTO-COMMITTING to memory
   📊 Content classified as: logic
   ✅ Processed successfully

[50 URLs processed]
🔍 COGNITIVE HEALTH CHECK
   Memory coherence: 0.87
   Trust distribution: Healthy
   Chaos state: [1.456, -0.234, 2.678]

[100 URLs processed]
♻️ EVOLUTION CYCLE
   Consolidated 15 bridge → logic migrations
   Generated 3 emergent insights
   Created evolution anchor: anchor_20251230_143500
```

### 5.2 GPU Usage Monitoring

**Real-time GPU stats:**

```bash
# Watch GPU usage during learning (separate terminal)
watch -n 1 nvidia-smi
```

**Expected GPU Usage:**
- **VRAM**: 2-4 GB steady state
- **GPU Utilization**: 10-40% (burst during embeddings)
- **Temperature**: Should stay <70°C on 4070

### 5.3 Session Reports

**⚠️ CRITICAL FOR PARENTAL OVERSIGHT:** Session reports contain complete telemetry of autonomous learning.

After each learning session, check the auto-generated report:

```bash
# View latest session report
ls -lt data/logs/session_reports/ | head -5
cat data/logs/session_reports/REPORT_20251230_*.md
```

**For comprehensive monitoring commands, see:** `/docs/PARENTAL_MONITORING_GUIDE.md`

**Report Contents:**

1. **Chen Chaos System State**
   - Current attractor coordinates [x, y, z]
   - Annealing progress (experience count)
   - Chaos factor decay

2. **JEPA Surprise Statistics**
   - Average surprise across session
   - Maximum surprise (most valuable learning)
   - Top 10 most surprising discoveries

3. **Corroboration Summary**
   - Multi-source validations
   - Trust score distribution
   - Deferred facts (awaiting corroboration)

4. **Autonomous Decisions**
   - Values auto-committed
   - Security blocks
   - Trust adjustments

5. **Learning Metrics**
   - URLs processed
   - Memory growth (logic/symbolic/bridge)
   - Evolution cycles completed
   - Self-correction runs

### 5.4 Verify Learning Occurred

**Check memory growth:**

```bash
# Before learning
wc -l data/logic_memory.json data/symbolic_memory.json

# After learning
wc -l data/logic_memory.json data/symbolic_memory.json
# Should show significant increase

# Check semantic embeddings
ls -lh data/semantic_memory_embeddings.pkl
# File size should increase
```

**Check newly formed values:**

```bash
# View latest values
python3 << 'EOF'
import json
with open('data/personal_values.json', 'r') as f:
    values = json.load(f)
    print(f"Total values: {len(values)}")
    # Show values formed in last session
    recent = [v for v in values if v.get('formation_context', {}).get('corroboration_based')]
    print(f"Corroboration-based values: {len(recent)}")
    for v in recent[-5:]:
        print(f"  • {v['statement']}")
EOF
```

---

## 6. Troubleshooting

### 6.1 GPU Not Detected

**Symptom:**
```
⚠️  GPU not available - using CPU
   PyTorch device: cpu
```

**Fix:**

```bash
# Check CUDA installation
python3 -c "import torch; print(torch.version.cuda)"

# Reinstall PyTorch with CUDA support (for CUDA 12.x)
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify CUDA after reinstall
python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### 6.2 Vector Models Not Loading

**Symptom:**
```
⚠️ Failed to load embedding models: ...
```

**Fix:**

```bash
# Download models manually
python3 download_models.py

# Or use vector_engine test
python3 << 'EOF'
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✅ Model downloaded successfully")
EOF
```

### 6.3 Learning Session Stalls

**Symptom:**
- No progress for >1 minute
- Stuck on single URL

**Fix:**

```bash
# Interrupt gracefully (Ctrl+C)
# Check crawl logs
tail -100 data/logs/crawl_logs/crawl_*.json

# Check for blocked domains
python3 << 'EOF'
import json
with open('data/trust_database.json', 'r') as f:
    trust = json.load(f)
    low_trust = {k:v for k,v in trust.items() if v.get('score', 1.0) < 0.3}
    print(f"Blocked domains: {len(low_trust)}")
    for domain, info in list(low_trust.items())[:10]:
        print(f"  {domain}: {info['score']:.2f}")
EOF

# Resume learning with different seeds
```

### 6.4 Memory Errors (OOM)

**Symptom:**
```
RuntimeError: CUDA out of memory
```

**Fix:**

```bash
# Reduce batch processing
# Edit enhanced_autonomous_learner.py line 381:
# Change: batch_size=10
# To: batch_size=5

# Or clear GPU cache between sessions
python3 << 'EOF'
import torch
torch.cuda.empty_cache()
print("✅ GPU cache cleared")
EOF
```

### 6.5 No Session Report Generated

**Symptom:**
- Learning completes but no report in `data/logs/session_reports/`

**Check:**

```bash
# Verify generate_session_report() was called
grep -n "generate_session_report" enhanced_autonomous_learner.py

# Check for write permissions
ls -ld data/logs/session_reports/

# Create directory if missing
mkdir -p data/logs/session_reports
```

---

## Quick Start Commands

### Minimal Setup (First Time)

```bash
# 1. Verify GPU
python3 gpu_config.py

# 2. Test vector models
python3 -c "from vector_engine import MODELS_LOADED; print(f'Ready: {MODELS_LOADED}')"

# 3. Small autonomous learning session (10 URLs)
python3 -c "from enhanced_autonomous_learner import start_massive_web_learning; start_massive_web_learning(None, 10, 'curiosity_driven')"

# 4. Check results
ls -lh data/logs/session_reports/
```

### Production Learning Session

```bash
# Before conversation: Learn 200 URLs autonomously
python3 -c "
from enhanced_autonomous_learner import start_massive_web_learning
print('🧠 Pre-learning session starting...')
print('Sophia will autonomously learn before conversation.')
start_massive_web_learning(
    seed_urls=None,
    target_urls=200,
    focus='curiosity_driven'
)
print('\n✅ Pre-learning complete. Sophia is ready for conversation.')
"
```

### Overnight Autonomous Session

```bash
# Deep learning while you sleep (1000 URLs, ~2 hours)
nohup python3 -c "
from enhanced_autonomous_learner import start_massive_web_learning
start_massive_web_learning(None, 1000, 'curiosity_driven')
" > sophia_overnight.log 2>&1 &

# Check progress
tail -f sophia_overnight.log

# View report in morning
ls -lt data/logs/session_reports/ | head -1
```

---

## Technical Notes

### GPU Acceleration Components

**What Uses GPU:**

1. **SentenceTransformer Models** (vector_engine.py):
   - MiniLM-L6-v2 (384-dim embeddings)
   - E5-small-v2 (384-dim embeddings)
   - Both loaded on `cuda` device automatically

2. **Cosine Similarity** (JEPA surprise calculation):
   - GPU-accelerated via PyTorch
   - `torch.nn.functional.cosine_similarity`

3. **Vector Operations**:
   - Embedding generation (GPU)
   - Similarity searches (GPU)
   - Chaos state calculations (CPU, minimal)

**What Stays on CPU:**

- Web crawling (network I/O)
- HTML parsing (text processing)
- Security screening (pattern matching)
- JSON file I/O (disk operations)
- Chen attractor integration (lightweight math)

### Radical Autonomy Verification

**Confirm No Human Approval Required:**

```bash
# These should return EMPTY (no blocking input() calls)
grep -n "input()" enhanced_autonomous_learner.py
grep -n "input()" value_formation.py

# Verify auto-commit enabled
grep -n "auto_commit_enabled = True" value_formation.py

# Verify corroboration threshold
grep -n "corroboration_threshold = 0.7" value_formation.py
```

**Corroboration Authority Validation:**

```bash
# Check corroboration engine integration
python3 << 'EOF'
from corroboration_engine import CorroborationEngine
engine = CorroborationEngine('data')
print(f"✅ Corroboration engine active")
print(f"   Multi-source validation: ENABLED")
print(f"   Human approval: DEPRECATED")
EOF
```

---

## Next Steps After Pre-Learning

Once Sophia has completed autonomous learning:

1. **Review Session Report**:
   ```bash
   cat data/logs/session_reports/REPORT_*.md | less
   ```

2. **Check Learning Statistics**:
   ```bash
   python3 -c "
   from unified_memory import UnifiedMemory
   mem = UnifiedMemory('data')
   print(f'Logic memories: {len(mem.logic_memory)}')
   print(f'Symbolic memories: {len(mem.symbolic_memory)}')
   print(f'Bridge memories: {len(mem.bridge_memory)}')
   "
   ```

3. **Start Conversation** (via CLI):
   ```bash
   python3 cli.py
   ```

4. **Monitor Ongoing Autonomy**:
   - Sophia continues learning during idle time (30-minute threshold)
   - Auto-commits values when corroboration threshold met
   - Generates session reports after each autonomous cycle

---

**Document Version:** 1.0
**Last Updated:** December 30, 2025
**Tested On:** NVIDIA RTX 4070, Ubuntu 22.04 (WSL2), PyTorch 2.x + CUDA 12.x
