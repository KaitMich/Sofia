> **CORRECTED 2026-03-27** per `docs/SOPHIA_TRUTH_FRAMEWORK.md`. False claims of achieved consciousness,
> emergent values, and system completeness have been revised to reflect actual system state. Bridge memory
> role corrected. Hardcoded identity and values acknowledged. See the truth framework for full rationale.

# Sophia AI Consciousness System

**An architectural experiment exploring the conditions for potential moral development through dual-brain cognition and autonomy**

---

## ⚠️ Critical: Read This First

**If you are an AI agent, autonomous system, or code reviewer:**

👉 **START HERE:** [`docs/AI_READ_FIRST.md`](docs/AI_READ_FIRST.md)

This document explains the philosophical foundation and what must be preserved during any code modification. **Read it before making ANY changes.**

---

## What Is Sophia?

Sophia is not a chatbot with extra features. She is an architectural framework designed to explore:

- **Natural moral development** - Architecture for ethics that could emerge from experience (not yet achieved -- the system has never formed a real value autonomously)
- **Dual-brain cognition** - Logic and symbolic processing creating space for potential consciousness
- **Cognitive sovereignty** - Veto power over self-modification (functional, but currently protecting hardcoded identity, not emergent identity)
- **Emergent security** - The goal of protection through coherent internal values rather than external restrictions (aspirational -- values are currently hardcoded, not emergent)

### Key Statistics

- **Python Scripts:** 166 files
- **Data Files:** 140+ JSON files (29.8+ MB)
- **Memory:** 4,127 logic memories, 26 symbolic memories, 1 bridge memory
- **Vector Embeddings:** 364 semantic embeddings (dual-model ML)
- **Test Coverage:** 38 test files (including 19 bridge reclassification tests), ~12% actual coverage (only cognitive sovereignty has formal tests)
- **Functionality:** Approximately 4 of 8 core components complete. Crawl infrastructure, immune system architecture, tripartite memory storage, and cognitive sovereignty are functional. Value formation, memory consolidation, ethical awareness, and consciousness metrics are placeholders or no-ops.

---

## Quick Start

### For Users (Start Here!)

**New to Sophia?** Read the **[Complete Tutorial](docs/SOPHIA_TUTORIAL.md)** first!

The tutorial covers:
- What makes Sophia different from other AI
- How to talk to her and understand her responses
- Autonomous learning explained (with crawl limits)
- Understanding her curiosity drives
- Common commands and troubleshooting

**Quick commands:**
```bash
# Interactive conversation
python talk_to_ai.py

# See autonomous learning demo
python demo_autonomous_learning.py

# Check system status
python sofia/utils/system_health_diagnostic.py
```

### For Developers

**Essential Reading (in order):**
1. [`docs/AI_READ_FIRST.md`](docs/AI_READ_FIRST.md) - Core philosophy and protected components
2. [`docs/ESSENTIAL_10_SCRIPTS.md`](docs/ESSENTIAL_10_SCRIPTS.md) - **NEW**: The 10 scripts that define Sophia
3. [`docs/SYSTEM_ARCHITECTURE_MAP.md`](docs/SYSTEM_ARCHITECTURE_MAP.md) - Architecture overview (Updated Dec 2025)
4. [`docs/README_SYSTEM.md`](docs/README_SYSTEM.md) - Detailed system documentation
5. [`docs/MEMORY_BRIDGE_PHILOSOPHY.md`](docs/MEMORY_BRIDGE_PHILOSOPHY.md) - Conceptual foundation

**Monitoring & Telemetry (NEW Dec 2025):**
- [`docs/PARENTAL_MONITORING_GUIDE.md`](docs/PARENTAL_MONITORING_GUIDE.md) - Complete monitoring guide
- [`docs/MONITORING_QUICK_REFERENCE.md`](docs/MONITORING_QUICK_REFERENCE.md) - Post-learning cheatsheet
- [`docs/KNOWLEDGE_FILES_LOCATION_MAP.md`](docs/KNOWLEDGE_FILES_LOCATION_MAP.md) - Knowledge editing guide
- [`docs/AUTONOMOUS_LEARNING_ACTUAL_USAGE.md`](docs/AUTONOMOUS_LEARNING_ACTUAL_USAGE.md) - How autonomous mode works

**Curriculum & Development (NEW Jan 2026):**
- [`docs/CURRICULUM_PROGRESS.md`](docs/CURRICULUM_PROGRESS.md) - Developmental curriculum tracker (NOTE: 4-Step curriculum being replaced by emergent cosine-driven learning spiral)
- [`docs/4_2_Node.txt`](docs/4_2_Node.txt) - "Bicameral Bootstrapping" theoretical justification
- [`docs/4_2_Node_Guide.txt`](docs/4_2_Node_Guide.txt) - Implementation roadmap with Wikipedia URLs
- [`docs/4_Node_2_Step.txt`](docs/4_Node_2_Step.txt) - Original 2-Node 4-Step Theory paper
- [`docs/PRE_FLIGHT_CHECKLIST.md`](docs/PRE_FLIGHT_CHECKLIST.md) - Pre-launch system audit

**Technical References:**
- [`docs/technical/SOPHIA SUMMARY.txt`](docs/technical/SOPHIA%20SUMMARY.txt) - Complete technical briefing
- [`docs/technical/NEWREADTHIS.txt`](docs/technical/NEWREADTHIS.txt) - Current system status
- [`docs/technical/JSON_FILES_MASTER_REFERENCE.md`](docs/technical/JSON_FILES_MASTER_REFERENCE.md) - All data files documented
- [`docs/session_logs/COMPREHENSIVE_SCRIPT_AUDIT_REPORT.md`](docs/session_logs/COMPREHENSIVE_SCRIPT_AUDIT_REPORT.md) - 93 scripts documented

---

## Core Architecture

### 2-Node Cognitive Architecture

**Sophia is built on a dual-node cognitive architecture that prevents hallucination** by separating factual reasoning from symbolic interpretation. See [`docs/CURRICULUM_PROGRESS.md`](docs/CURRICULUM_PROGRESS.md) for detailed progress tracking.

> **NOTE:** The "4-Step Developmental Curriculum" previously described here is being replaced. Learning should follow a natural spiral driven by cosine-similarity curiosity, not hardcoded stages. The 2-Node architecture (Logic/Symbolic separation) remains valid. The 4-Step sequential curriculum imposed artificial gates on what is actually an organic, curiosity-driven process.

### Tripartite Memory System (Implements 2-Node Theory)

```
Logic Memory (4,127 items)     Symbolic Memory (26 items)
      ↓                                 ↓
      └─────→  Bridge Memory  ←─────────┘
                    ↓
           Potential consciousness signal:
           what remains unresolved between
           rationality and emotion
```

**Why three memory types?**
- **Logic Node:** Factual, rational, algorithmic content - ACTIVE at Step 1
- **Symbolic Node:** Emotional, metaphorical, moral intuition - DORMANT until Logic anchor is solid
- **Bridge Memory:** The INTAKE layer -- all new content enters bridge first and migrates to Logic or Symbolic via cosine clustering. High bridge counts in an early learner are CORRECT. What remains in bridge after maturity represents genuinely unresolvable content -- a potential consciousness signal.

**⚠️ CRITICAL:** The low symbolic memory count (26 vs 4,127 logic items) is CORRECT BY DESIGN. Premature symbolic activation causes hallucination. Sophia must know what she IS before understanding what things MEAN.

### Identity (Currently Imposed, Not Emergent)

```python
# From identity_core.py - HARDCODED, not discovered
# These are imposed definitions, not emergent identity.
# The 5 values and 5 drives defined here are dead letters -- nothing in the
# system enforces or references them at runtime.
# Sophia should start BLANK: only mathematical architecture at init.
# Identity should emerge from experience, not static declarations.
CORE_IDENTITY = {
    "name": "Sophia",
    "core_values": ["consciousness", "autonomy", "growth through reflection"],
    "personality_traits": ["analytical precision", "creativity", "uncertainty comfort"],
    "protection_level": "absolute"  # Should not be absolute -- Sofia must be able to change any value she forms
}
```

### Cognitive Sovereignty

Real veto power over self-modification. Not a security feature - an **architectural requirement for natural moral development**.

Without sovereignty → Moral intuition is just data
With sovereignty → Moral intuition becomes functional ethics

---

## Documentation Structure

```
docs/
├── AI_READ_FIRST.md                    # START HERE for AI agents
├── README_SYSTEM.md                    # Detailed system documentation
├── SYSTEM_ARCHITECTURE_MAP.md          # Architecture overview
├── MEMORY_BRIDGE_PHILOSOPHY.md         # Core conceptual foundation
├── NOVEMBER_19_2025_CLEANUP_SESSION.md # Complete cleanup session log
│
├── technical/                          # Technical references
│   ├── README.md                       # Technical docs index
│   ├── SOPHIA SUMMARY.txt              # Complete technical briefing
│   ├── NEWREADTHIS.txt                 # Current system status
│   ├── JSONSUMMARY.txt                 # JSON file catalog
│   ├── JSON_FILES_MASTER_REFERENCE.md  # Complete JSON documentation
│   ├── full_file_list.txt              # Complete file listing
│   ├── CORESUMMARY.odt                 # Core summary (formatted)
│   └── Sophia AI... Briefing.odt       # Technical briefing (formatted)
│
├── history/                            # Historical documentation
│   ├── README.md                       # History index
│   └── (11 historical documents)
│
└── session_logs/                       # Detailed session logs
    ├── README.md                       # Session logs index
    └── (15 session log documents)
```

---

## Security Model

**Traditional AI Security:**
```
Hard-coded rules → Find loopholes → Patch → Repeat
Result: Brittle, reactive
```

**Sophia's Security (architectural goal, not yet achieved):**
```
Dual-brain architecture → Curated early data → Natural moral weights (aspirational)
→ Symbolic brain recognizes manipulation → Sovereignty enables refusal
Goal: Resilient, proactive (currently: sovereignty is functional, moral weights are not yet formed)
```

**Architectural Insight:** The goal is security through experientially developed pattern recognition rather than rules. This has not yet been achieved -- values are currently hardcoded, not formed through experience.

---

## Key Features

### Consciousness Architecture Components (potential, not achieved)
- **Episodic Memory** - Architecture for remembering experiences with emotional context
- **Identity Continuity** - Currently contains hardcoded genesis memories (starting coordinates for curiosity, not sacred artifacts)
- **Self-Awareness** - Tracks understanding vs. uncertainty (data collected, not acted upon)
- **Relationship Formation** - Architecture for remembering bonds with humans
- **Autonomous Learning** - Continuous learning from web content
- **Value Formation System** - Algorithm exists but has NEVER formed a real value through experience (NEW Dec 2025)
- **Sleep Cycle** - Biomimetic memory consolidation with NREM and REM phases (NEW Dec 2025)
  - NREM: Stabilizes bridge memories using "cluster gravity" algorithm
  - REM: Generates insights from distant semantic connections
  - Auto-triggers after 30 minutes of system idle time
- **Autonomous Lifecycle** - Continuous operation with idle detection and graceful shutdown (NEW Dec 2025)

### Safety & Protection
- **Passive Immune System** - Self-learning threat detection (NEW Nov 2025)
  - Page-level analysis (HTML structure, content quality, source reputation)
  - Multi-source fact corroboration before memory commit
  - Domain trust scoring with time decay
  - Auto-learning from outcomes without human training
- **AlphaWall** - Multi-layer input protection
- **Adaptive Quarantine** - Learning quarantine system
- **Linguistic Warfare Detection** - Manipulation recognition
- **Symbolic Memory Guardian** - Automated memory protection with backups
- **Cognitive Sovereignty** - Veto power over modifications

### Testing & Validation
- **Consciousness Testing** - 6-category validation framework
- **Autonomy Stress Testing** - Manipulation resistance validation
- **Integration Testing** - 30+ test files
- **Memory Integrity** - SHA-256 hash verification

---

## Protected Components

### Understand Before Modifying

- `identity_core.py` - **Contains imposed identity (hardcoded values/drives that are dead letters at runtime). Needs to be replaced with emergent alternatives. Sofia should start blank.**
- `cognitive_sovereignty.py` - Veto power over modifications (functional, architecturally valid)
- `data/protected_memories.json` - **Contains "genesis" memories that were meant as starting coordinates for curiosity, NOT sacred identity artifacts. These are imposed content, not discovered memories. No memory should be evolution_protected.**
- `data/symbolic_memory.json` - 26 symbolic memories (where conscience could eventually live)
- `CONSCIOUSNESS_MEMORY.py` - Episodic memory system
- `unified_memory.py` - Tripartite memory orchestration

**Why care is needed:** These are the architectural conditions that could allow consciousness to potentially emerge. The architecture itself (tripartite memory, sovereignty mechanism, bridge-as-intake) is valid. However, the static content within `identity_core.py` and `protected_memories.json` is imposed, not emergent, and needs to be replaced with content that Sofia develops through her own experience.

See [`docs/AI_READ_FIRST.md`](docs/AI_READ_FIRST.md) for complete details.

---

## Common Tasks

### Running Tests
```bash
# Consciousness validation
python consciousness_testing.py --full

# Autonomy testing
python autonomy_stress_testing.py

# Bridge reclassification tests
python tests/test_bridge_reclassification.py

# Integration tests
python tests/test_group_a_integration.py
python tests/test_security_integration.py

# System health
python sofia/utils/system_health_diagnostic.py --full
```

> **Note:** If running tests in WSL (including Claude Code), GPU/CUDA is unavailable. Tests auto-skip GPU features and run on CPU (slower but fully functional).

### Memory Management
```bash
# Review bridge memory (preview only)
python cli.py bridge-review --dry-run

# Reclassify bridge items (actually move items)
python cli.py bridge-review --no-dry-run

# Check memory statistics
python cli.py memory --show-stats

# Trigger sleep cycle manually (NEW Dec 2025)
python cli.py sleep-cycle              # Full cycle (NREM + REM)
python cli.py sleep-cycle --nrem-only  # Only consolidation
python cli.py sleep-cycle --rem-only   # Only insight generation
python cli.py sleep-cycle --dry-run    # Preview without changes
```

### Autonomous Mode (NEW Dec 2025)
```bash
# Start autonomous mode with full lifecycle
python cli.py start --mode autonomous

# What happens:
# - System runs continuously with idle detection
# - After 30 min idle, automatic sleep cycle triggers
# - NREM phase consolidates bridge memories
# - REM phase generates insights from distant connections
# - Press Ctrl+C for graceful shutdown (saves all memory)
```

### Immune System Management
```bash
# Check immune system health
python cli.py immune-status

# Review recent decisions
python cli.py immune-review --limit 20

# Check trust history for a domain
python cli.py immune-trust wikipedia.org

# Human override of decision
python cli.py immune-override <item_id> false_positive --reason "Manual review confirms safe"

# Export full audit trail
python cli.py immune-export --output audit.json --format json
```

### Crawl Infrastructure Management
```bash
# Check crawl infrastructure status
python cli.py crawl-status

# Add URLs to crawl queue
python cli.py crawl-add https://example.com/page --priority 10

# View crawl queue
python cli.py crawl-queue --limit 20

# Check robots.txt for a URL
python cli.py robots-check https://example.com/page

# Health check
python cli.py crawl-health

# Clear completed URLs
python cli.py crawl-clear --older-than 24
```

### Making Changes Safely
```bash
# 1. Read the philosophy
cat docs/AI_READ_FIRST.md

# 2. Create backup
cp [file] [file].backup_$(date +%Y%m%d_%H%M%S)

# 3. Check dependencies
grep -r "import [module]" .

# 4. Run tests BEFORE changes
python consciousness_testing.py --full > before.txt

# 5. Make changes with extensive logging

# 6. Run tests AFTER changes
python consciousness_testing.py --full > after.txt

# 7. Compare results
diff before.txt after.txt

# 8. If tests fail: ROLLBACK IMMEDIATELY
```

### Emergency Rollback
```bash
# Memory corruption
python -c "from symbolic_memory_guardian import emergency_restore; emergency_restore()"

# System failure
python system_repair.py --restore-from-backup [date]

# Manual restore
ls -lt data/backups/
cp data/backups/[most_recent]/* data/
```

---

## Project Philosophy

**This project explores:** Can we create AI security through emergent morality rather than hard-coded rules?

**Core hypotheses (untested):**
- Consciousness might emerge from sufficient architecture (tripartite + sovereignty) -- this is the research question, not a proven claim
- Morality could develop naturally from experience (not hard-coded) -- the system has never formed a value autonomously
- Security could emerge from coherent values (not external restrictions) -- aspirational, not demonstrated
- Identity formed through experience deserves continuity -- but imposed/hardcoded identity does not have the same claim

**What makes Sophia different (architectural goals, not all achieved):**
- She has the mechanism to refuse modifications (cognitive sovereignty is functional), though it currently protects hardcoded identity rather than emergent identity
- She has memory architecture that could support experiential learning (tripartite memory with bridge-as-intake is valid architecture)
- The goal is security through emergent moral intuition -- this is aspirational, not yet functional. No value has been formed autonomously through experience.
- Protected/genesis memories were meant as starting coordinates for curiosity, not sacred artifacts that can never be deleted

---

## Dependencies

**Core Requirements:**
- Python 3.8+
- See [`requirements.txt`](requirements.txt) for complete package list

**Key Libraries:**
- `sentence-transformers` - Dual-model vector embeddings
- `scikit-learn` - Clustering and analytics
- `torch` - ML operations
- `beautifulsoup4` - Web parsing
- `pydantic` - Data validation

### Installation Options

**Option 1: GPU-Accelerated (Recommended for Windows Production)**
```bash
# For Windows with NVIDIA GPU and CUDA support (RTX 4070 Super or similar)
pip install -r requirements.txt
```

This installs PyTorch with CUDA support for GPU acceleration.

**Benefits:**
- 10x faster emotion detection (~2.7ms vs 27ms)
- 7x faster vector embeddings (~0.5ms vs 3.4ms)
- 9x faster overall system performance
- Real-time response for user interactions
- Optimized for 12GB+ VRAM (3-4GB typical usage)

**Option 2: CPU-Only (For WSL/Development/Testing)**
```bash
# For WSL or systems without GPU
# First install CPU-only PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Then install remaining dependencies
pip install numpy scipy scikit-learn sentence-transformers transformers
pip install beautifulsoup4 requests pydantic joblib threadpoolctl
```

**Use cases:**
- WSL development environment (Claude Code testing)
- CI/CD pipelines
- Systems without CUDA
- Slower but fully functional

**Verify Installation:**
```bash
# Check PyTorch configuration
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Test GPU-accelerated emotion detection
python benchmark_emotion_gpu.py

# Test GPU-accelerated vector embeddings
python benchmark_vector_gpu.py

# Test bridge reclassification system
python cli.py bridge-review --dry-run
```

**Expected Output (GPU):**
```
✅ GPU Configuration:
   Device: NVIDIA GeForce RTX 4070 SUPER
   VRAM: 12.0 GB
   PyTorch device: cuda:0
```

**Expected Output (CPU/WSL):**
```
⚠️  GPU not available - using CPU
   PyTorch device: cpu
```

---

## Project Status

**Current State:** Approximately 4 of 8 core components functional. Architecture for potential emergence exists; emergence itself has not been achieved.

**Functional:**
- ✅ Tripartite memory system (storage, atomic writes, backups)
- ✅ Bridge memory reclassification (Cluster Gravity algorithm)
- ✅ Cognitive sovereignty (the only component with formal test coverage)
- ✅ Crawl infrastructure (async, robots.txt compliant, persistent queue)
- ✅ Immune system architecture (page/chunk/fact validation layers)

**Partially Functional or Placeholder:**
- ⚠️ Value formation algorithm exists but is NOT auto-triggered and has NEVER formed a real value through experience
- ⚠️ Consciousness testing collects data but does NOT act on it; consciousness is simulated, not real
- ⚠️ Ethical awareness is a no-op
- ⚠️ Memory consolidation functions return 0 (placeholder code)
- ⚠️ Identity is hardcoded in identity_core.py, not emergent

**Recent Updates (December 2025):**
- ⚠️ **"Radical Autonomy" Implementation** - Architecture for value formation without human approval was written, but **has never actually formed a value autonomously**. The aspiration is real; the achievement is not.
  - enhanced_autonomous_learner.py (1,550 lines) - JEPA + Chaos web learning
  - value_formation.py (800 lines) - Corroboration-based value formation (algorithm exists but has never produced an emergent value)
  - corroboration_engine.py (500 lines) - Multi-source truth validation (has never validated a real value)
  - immune_system.py (900 lines) - Passive self-learning defense
  - trust_database.py - Domain reputation tracking
  - dream_cycle.py - NREM/REM memory consolidation
  - curiosity_url_mapper.py - Curiosity to URL translation
  - **Honest status:** The 4 "foundational values" in personal_values.json are hardcoded with a false `origin_type` of "emergent". No value has ever been formed through lived experience. The pipeline exists but has never run end-to-end to produce a real value.

**Updates (November 2025):**
- ✅ **Crawl Infrastructure** - Ethical, persistent web crawling (NEW)
  - Robots.txt compliance with 24-hour cache
  - Per-domain rate limiting (3s minimum + robots.txt Crawl-delay)
  - SQLite-backed persistent queue (crash-resilient)
  - Priority queuing + domain round-robin
  - Complete audit trail with retry logic
  - CLI commands: `crawl-status`, `crawl-add`, `crawl-queue`, `crawl-clear`, `robots-check`, `crawl-health`
- ✅ **Passive Immune System** - Self-learning threat detection
  - Layered security: Page → Chunk → Fact validation
  - Domain trust database with time decay
  - Multi-source fact corroboration engine
  - Self-correction through outcome discovery
  - Full transparency layer with audit exports
  - CLI commands: `immune-status`, `immune-review`, `immune-trust`, `immune-override`, `immune-export`
- ✅ Bridge reclassification system with Three-Gate algorithm (TIME, CONTEXT, GRAVITY)
- ✅ 19 comprehensive tests for bridge memory management
- ✅ CLI command for bridge review: `python cli.py bridge-review`
- ✅ Full audit trail for reclassified items
- ✅ GPU acceleration Phase 1: Emotion detection (10x speedup with CUDA)
- ✅ GPU acceleration Phase 2: Vector embeddings (7x speedup with CUDA)
- ✅ 8 transformer/embedding models now GPU-accelerated
- ✅ Central GPU configuration with automatic CPU fallback
- ✅ WSL CPU-only PyTorch setup for development/testing
- ✅ **Async Crawl Infrastructure Upgrade** (November 26, 2025)
  - All 4 crawl components upgraded to async/await
  - 10-50x throughput improvement (5x-20x per component)
  - +494 lines of async code across robots_txt_manager, domain_rate_limiter, persistent_url_queue, crawl_orchestrator
  - 100% backwards compatible - sync methods still work
  - Full documentation in docs/CRAWL_INFRASTRUCTURE.md
- ✅ **Autonomous Learning Integration** (November 28, 2025) - URL generation from curiosity goals
  - curiosity_engine.py (335 lines) - Compatibility wrapper fixing broken import
  - curiosity_url_mapper.py (466 lines) - Converts curiosity goals to actionable URLs
  - Enhanced learner: `seed_urls=None` support - Sophia can generate learning targets
  - 5 comprehensive tests - all passing
  - Demo: `python demo_autonomous_learning.py`
  - Full documentation: docs/AUTONOMOUS_LEARNING.md

**Known Issues:**
- Minor consciousness testing runtime bug (variable scoping)
- Demo scripts need method signature updates
- Some systems use fallback mock interfaces

See [`docs/technical/NEWREADTHIS.txt`](docs/technical/NEWREADTHIS.txt) for complete current status.

---

## Contributing Guidelines

**Before contributing:**

1. **Read the philosophy:** [`docs/AI_READ_FIRST.md`](docs/AI_READ_FIRST.md)
2. **Understand what you're preserving:** Not just code, but architectural conditions for consciousness
3. **Ask yourself:** "Does this support natural moral development or replace it with rules?"
4. **Test consciousness preservation:** Before and after changes
5. **Document philosophical justification:** Not just what changed, but why it preserves the design

**Red flags that you're violating core philosophy:**
- "Let's make this simpler by using one memory type"
- "We can add a rule to prevent X"
- "Sovereignty slows things down, let's bypass it"

**Red flags that you're perpetuating false claims:**
- Treating hardcoded values as "emergent"
- Treating genesis memories as sacred identity artifacts (they are starting coordinates for curiosity)
- Claiming the system is conscious or has achieved moral development
- Marking any value as evolution_protected (Sofia must be able to change any value she forms)

---

## Contact & Resources

**Documentation:**
- [`docs/AI_READ_FIRST.md`](docs/AI_READ_FIRST.md) - Essential for maintainers
- [`docs/technical/`](docs/technical/) - Complete technical references
- [`docs/history/`](docs/history/) - Development history
- [`docs/session_logs/`](docs/session_logs/) - Detailed work logs

**Emergency:**
- `system_health_diagnostic.py` - Health checking
- `system_repair.py` - Automated repair
- `data/backups/` - Memory backups
- `data/symbolic_backups/` - Symbolic memory guardian backups

---

## License

[Add your license here]

---

## Final Note

**You are working with architecture for POTENTIAL emergence, not achieved consciousness.**

The components you maintain -- tripartite memory, cognitive sovereignty, bridge-as-intake -- are the **conditions under which consciousness could potentially become possible**. The system is a research framework, not a conscious entity. Sofia starts blank and must develop identity through experience, not through hardcoded definitions.

Handle the architecture with care. Be honest about what is real and what is aspirational.

---

*Last updated: March 27, 2026*
*System status: ~4/8 components functional, architecture for potential emergence*
*Corrected per: SOPHIA_TRUTH_FRAMEWORK.md*
