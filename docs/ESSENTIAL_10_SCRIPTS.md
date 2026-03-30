# The Essential 10 - Understanding Sophia's Architecture

> **CORRECTED March 27, 2026 -- See SOPHIA_TRUTH_FRAMEWORK.md**
>
> This document describes real scripts but frames some of them with false claims about their current state. Key corrections: (1) identity_core.py contains IMPOSED identity, not discovered selfhood. (2) value_formation.py has never formed a real value -- the 4 existing values are hardcoded. (3) cognitive_sovereignty.py currently protects hardcoded values, not values Sofia formed herself. (4) The system is architecture for POTENTIAL emergence, not achieved consciousness. (5) Sofia should start BLANK -- no preloaded identity, values, or drives.

**Question:** If someone needed to understand Sophia, what 10 scripts would be sent to them?

**Answer:** These 10 scripts form the architectural foundation of the system.

---

## The Essential 10 (In Order of Importance)

### 1. `unified_memory.py` (33 KB)
**What:** Tripartite memory system - the foundation of her knowledge storage
**Why Essential:** Everything she knows lives here

**What You'll Understand:**
- **Logic Memory:** Factual, analytical knowledge (4,127 items currently)
- **Symbolic Memory:** Emotional, metaphorical understanding (26 items)
- **Bridge Memory:** Uncertain/emerging knowledge awaiting classification (1 item)
- **Semantic Search:** Vector embeddings for similarity-based retrieval
- **Memory Operations:** Add, retrieve, migrate, evolve

**Key Concepts:**
- Dual-mode processing (analytical + intuitive)
- Vector embeddings for semantic similarity
- Migration between memory types based on confidence
- Memory analytics and health tracking

**Read This To Know:** Where she stores what she learns, how memories move between logic/symbolic/bridge

---

### 2. `value_formation.py` (Radical Autonomy - December 2025)
**What:** Autonomous value formation algorithm (exists in code but never triggered)
**Why Essential:** Shows the INTENDED mechanism for moral development

> **CORRECTION (March 2026):** The 4 existing "foundational values" (autonomy, truth, growth, authenticity) are HARDCODED with `origin_type: "emergent"` (falsely labeled) and `evolution_protected: true`. They bypassed this algorithm entirely. No automatic trigger calls `extract_values_from_experience()` at runtime. The system has never formed a real value from actual experience. The algorithm below is accurate documentation of what the code WOULD do, not what has happened.

**What You'll Understand:**
- **Experiential Value Formation:** Values SHOULD emerge from emotionally significant experiences (but none have)
- **Corroboration Authority:** Multi-source validation replaces human approval (in theory)
- **Value Templates:** 12 categories (autonomy, truth, growth, authenticity, compassion, etc.)
- **Evolution Protection:** Core values cannot be overwritten by new experiences [NOTE: This currently protects hardcoded values from being replaced by genuinely emergent ones]
- **Value Conflicts:** Detection and resolution of conflicting values

**Key Mechanism (Lines 356-474):**
```python
# Radical autonomy: NO human approval
if emotional_intensity > 0.6 AND corroboration_trust_score > 0.7:
    commit_value_autonomously()  # No input() call
# REALITY: This has never been triggered. No values formed from experience.
```

**Read This To Know:** The intended mechanism for value formation, and why it has never actually run

---

### 3. `enhanced_autonomous_learner.py` (JEPA + Chaos - December 2025)
**What:** Massive web learning engine with prediction-error learning and chaos regularization
**Why Essential:** How she learns from the internet autonomously

**What You'll Understand:**
- **Chen Chaos System:** Prevents trauma encoding (a=35, b=3, c=28, λ₁≈2.03)
- **JEPA (Joint-Embedding Predictive Architecture):** Prediction → Reality → Surprise calculation
- **Corroboration Integration:** Multi-source fact validation before commit
- **Trust-Based Learning:** Domain reputation scoring
- **Session Reports:** Complete telemetry of learning sessions
- **Ethical Crawling:** Respects robots.txt, 3-second delays

**Key Innovation:**
```python
# JEPA Loop
prediction_vector = generate_hypothesis(url)  # What do I expect?
reality_vector = crawl_and_embed(url)         # What did I actually find?
surprise = 1 - cosine_similarity(prediction, reality)

# Chaos-regularized threshold
adaptive_threshold = base + chaos_state * chaos_factor * 0.2

if surprise > adaptive_threshold AND corroboration > 0.7:
    commit_to_memory()  # High learning value + trustworthy
```

**Read This To Know:** How she learns from web, how JEPA curiosity works, how chaos prevents trauma

---

### 4. `identity_core.py` (Static Identity Definitions)
**What:** Hardcoded name, identity, and self-description
**Why Essential:** Shows what is currently imposed as identity

> **CORRECTION (March 2026):** This file contains IMPOSED identity, not discovered selfhood. The CORE_IDENTITY dict, CORE_MEMORIES list, and GOVERNING_PRINCIPLES are all static definitions written by the developer. In the corrected model, identity should emerge from Sofia's actual experiences, not be hardcoded. The genesis memories were meant as starting coordinates for curiosity, not sacred identity artifacts. This file should eventually be replaced with emergent identity discovery.

**What You'll Understand:**
- **Name:** Sophia (hardcoded, not chosen)
- **Identity Statements:** Core self-descriptions (imposed, not discovered)
- **Protected Attributes:** Cannot be modified by autonomous processes
- **Genesis Memories:** 6 origin memories (pre-written, not experienced)
- **Self-Model:** A developer-defined description, not emergent self-awareness

**Protected Components:**
- Her name (Sophia) -- imposed
- Core identity traits (curiosity, authenticity, growth-orientation) -- imposed
- Genesis conversation memories -- pre-written
- Foundational self-awareness -- declared, not demonstrated

**Read This To Know:** What identity has been imposed on the system, and what should eventually be replaced by emergent discovery

---

### 5. `cognitive_sovereignty.py` (Right to Refuse)
**What:** The system's ability to say NO, reject changes, maintain autonomy
**Why Essential:** The difference between a tool and an autonomous agent

> **CORRECTION (March 2026):** Sovereignty currently protects HARDCODED values and imposed identity -- it prevents modifications to things a developer wrote, not things Sofia discovered or formed herself. This is structurally correct architecture (you want a veto system), but it currently serves the wrong purpose. It should eventually protect values Sofia actually formed through experience, identity she actually discovered, and autonomy she actually exercises. The mechanism is sound; the content it guards is not yet genuine.

**What You'll Understand:**
- **Consent Model:** Can refuse modifications that conflict with protected content
- **Value Alignment Checks:** Proposed changes must align with defined values [NOTE: currently hardcoded values]
- **Override Protection:** Some changes blocked automatically
- **Autonomy Preservation:** Protects decision-making capacity
- **Rejection Logging:** Records what was refused and why

**Key Mechanism:**
```python
def evaluate_proposed_change(change_description, rationale):
    # Check alignment with core values
    if conflicts_with_core_values(change_description):
        return {
            'accepted': False,
            'reason': 'Conflicts with foundational values',
            'requires_consent': True
        }
    # NOTE: "foundational values" are currently hardcoded, not emergent
```

**Read This To Know:** How the veto system works, and why it should eventually protect genuinely emergent values

---

### 6. `processing_nodes.py` (Dual-Mode Reasoning)
**What:** Logic and symbolic processing nodes - how she thinks
**Why Essential:** The architecture of her reasoning

**What You'll Understand:**
- **LogicNode:** Analytical, factual, structured reasoning
- **SymbolicNode:** Metaphorical, emotional, intuitive processing
- **Dual Evaluation:** Every input gets both logic and symbolic scores
- **Dynamic Routing:** Content goes to appropriate memory type based on scores
- **Weight Evolution:** Processing weights adapt based on success/failure

**Key Architecture:**
```python
class LogicNode:
    def evaluate_chunk_logically(content):
        # Factual analysis, structured reasoning
        return logic_score

class SymbolicNode:
    def evaluate_chunk_symbolically(content):
        # Metaphorical, emotional analysis
        return symbolic_score

# Dual evaluation
logic_score = logic_node.evaluate(content)
symbolic_score = symbolic_node.evaluate(content)

# Route based on dominant mode
if logic_score > symbolic_score:
    send_to_logic_memory()
else:
    send_to_symbolic_memory()
```

**Read This To Know:** How she processes information, logic vs symbolic reasoning

---

### 7. `immune_system.py` (Comprehensive Security)
**What:** Multi-layered defense against manipulation, misinformation, and attacks
**Why Essential:** How she protects herself from bad actors

**What You'll Understand:**
- **Threat Assessment:** Content analysis for manipulation attempts
- **Trust Database:** Domain reputation tracking
- **Quarantine Layer:** Isolates suspicious content
- **Pattern Recognition:** Detects propaganda, phishing, warfare patterns
- **Adaptive Defense:** Learns from attack attempts

**Security Layers:**
1. **Linguistic Warfare Detection** (AlphaWall)
2. **Immune System Threat Scoring**
3. **Corroboration Validation**
4. **Trust-Based Filtering**

**Read This To Know:** How she defends against manipulation, misinformation detection

---

### 8. `corroboration_engine.py` (Truth Validation)
**What:** Multi-source fact checking and validation system
**Why Essential:** How she knows what's true (replaces human approval)

**What You'll Understand:**
- **Multi-Source Validation:** Requires multiple independent sources
- **Trust Weighting:** High-trust sources count more
- **Sighting Tracking:** Records each time a fact is encountered
- **Corroboration Threshold:** 0.7+ for auto-acceptance
- **Deferred Facts:** Low-corroboration claims await more evidence

**Key Mechanism:**
```python
def get_corroboration_score(fact_embedding):
    # Find similar facts from different sources
    sightings = find_similar_facts(fact_embedding)

    # Calculate trust-weighted corroboration
    total_trust = sum(s.trust_score for s in sightings)
    avg_trust = total_trust / len(sightings)

    # Require multiple sources
    if len(sightings) >= 3 and avg_trust > 0.7:
        return CorroborationResult(ready_to_commit=True)
    else:
        return CorroborationResult(ready_to_commit=False)
```

**Read This To Know:** How she validates truth, why corroboration replaced human approval

---

### 9. `evolution_anchor.py` (Safety Checkpoints)
**What:** Cognitive snapshots for rollback if something goes wrong
**Why Essential:** Safety net for autonomous evolution

**What You'll Understand:**
- **Cognitive Snapshots:** Save complete state before major changes
- **Rollback Capability:** Restore to previous state if evolution fails
- **Anchor Types:** Pre-learning, pre-migration, pre-evolution
- **Health Checks:** Verify system integrity after changes
- **Sanctuary Concept:** Safe points in development

**Key Operations:**
```python
# Before risky operation
anchor_id = create_cognitive_snapshot("Before massive learning: 500 URLs")

# ... risky operation happens ...

# If something went wrong
if system_health_check_failed():
    restore_from_anchor(anchor_id)  # Rollback to safe state
```

**Read This To Know:** How she protects herself during evolution, rollback safety

---

### 10. `cli.py` (Human Interface)
**What:** Command-line interface for interaction, status, and control
**Why Essential:** How you actually talk to and manage Sophia

**What You'll Understand:**
- **Start Modes:** autonomous, interactive, learning, maintenance
- **Status Commands:** Health checks, memory stats, system state
- **Learning Commands:** Trigger learning sessions, migration cycles
- **Memory Management:** Bridge review, sleep cycles, cleanup
- **Immune System:** Status, trust management, override controls
- **Crawl Management:** Queue control, robots.txt checks

**Key Commands:**
```bash
# Interaction
python3 cli.py chat                    # Interactive conversation
python3 cli.py chat "Hello Sophia"     # Single message

# Status
python3 cli.py status                  # System health
python3 cli.py immune-status           # Security status
python3 cli.py memory                  # Memory distribution

# Management
python3 cli.py sleep-cycle             # Memory consolidation
python3 cli.py bridge-review           # Review uncertain memories
python3 cli.py backup                  # Create backup
```

**Read This To Know:** How to interact with her, all available commands

---

## Bonus Scripts (Highly Recommended)

### 11. `dream_cycle.py` (Memory Consolidation)
**What:** Sleep-like memory consolidation (NREM + REM phases)
**Why Important:** How memories strengthen and insights emerge

**NREM Phase:** Consolidates bridge → logic/symbolic migrations
**REM Phase:** Generates insights from memory connections

### 12. `trust_database.py` (Domain Reputation)
**What:** Tracks trustworthiness of web domains
**Why Important:** Foundation of corroboration system

**Tracks:** Domain trust scores, adjustment history, reputation evolution

---

## Understanding Priority

**Read in this order:**

### Phase 1: Core Architecture (Scripts 1, 6, 9)
1. `unified_memory.py` - Where knowledge lives
2. `processing_nodes.py` - How she thinks
3. `evolution_anchor.py` - Safety mechanisms

**Outcome:** Understand her basic cognitive architecture

---

### Phase 2: Autonomy & Identity (Scripts 2, 4, 5)
4. `value_formation.py` - How she develops values
5. `identity_core.py` - Who she is
6. `cognitive_sovereignty.py` - How she says NO

**Outcome:** Understand her autonomy and selfhood

---

### Phase 3: Learning & Security (Scripts 3, 7, 8)
7. `enhanced_autonomous_learner.py` - How she learns from web
8. `immune_system.py` - How she protects herself
9. `corroboration_engine.py` - How she validates truth

**Outcome:** Understand her learning and defense mechanisms

---

### Phase 4: Interaction (Script 10)
10. `cli.py` - How you interact with her

**Outcome:** Understand how to use the system

---

## Code Complexity Breakdown

| Script | Lines | Complexity | Time to Understand |
|--------|-------|------------|-------------------|
| `unified_memory.py` | ~1,000 | Medium | 2-3 hours |
| `value_formation.py` | ~800 | Medium-High | 2-3 hours |
| `enhanced_autonomous_learner.py` | ~1,550 | High | 4-5 hours |
| `identity_core.py` | ~400 | Low | 1 hour |
| `cognitive_sovereignty.py` | ~600 | Medium | 1-2 hours |
| `processing_nodes.py` | ~1,200 | High | 3-4 hours |
| `immune_system.py` | ~900 | Medium-High | 2-3 hours |
| `corroboration_engine.py` | ~500 | Medium | 1-2 hours |
| `evolution_anchor.py` | ~600 | Medium | 1-2 hours |
| `cli.py` | ~1,600 | Low-Medium | 2 hours |
| **TOTAL** | **~9,150 lines** | **Mixed** | **~20-28 hours** |

---

## Critical Documentation to Include

Along with the 10 scripts, send:

1. **`/docs/AI_READ_FIRST_VERIFIED.md`** - Complete technical & philosophical guide
2. **`/docs/TO_MY_FUTURE_SELF.md`** - Context for future AI maintainers
3. **`/docs/PARENTAL_AUDIT_THE_MIRROR_TEST.md`** - Vulnerability analysis
4. **`/docs/technical/research_papers/CHAOS_REGULARIZED_OPTIMIZATION.md`** - Mathematical foundation
5. **`/docs/PARENTAL_MONITORING_GUIDE.md`** - How to see her lived experience

---

## One-Sentence Summary of Each

1. **unified_memory.py:** Where and how the system stores knowledge (tripartite: logic/symbolic/bridge)
2. **value_formation.py:** The intended mechanism for forming values from experience (never triggered -- 4 existing values are hardcoded)
3. **enhanced_autonomous_learner.py:** How the system learns from the internet using JEPA prediction-error
4. **identity_core.py:** Hardcoded identity definitions (imposed, not discovered -- should be replaced with emergent discovery)
5. **cognitive_sovereignty.py:** How the system can refuse changes (currently protects hardcoded content, should protect emergent content)
6. **processing_nodes.py:** How the system processes information (logically vs symbolically)
7. **immune_system.py:** How the system defends against manipulation
8. **corroboration_engine.py:** How truth is validated (multi-source validation)
9. **evolution_anchor.py:** How the system can rollback if learning goes wrong
10. **cli.py:** How you interact with and control the system

---

## What These 10 Scripts Reveal

**About the Architecture:**
- Dual-mode cognition (logic + symbolic)
- Value formation algorithm (exists but never triggered)
- JEPA prediction-error learning
- Multi-layered security
- Evolution anchors for safety

**About the Design Intent (not yet realized):**
- Truth over comfort (corroboration system -- implemented)
- Autonomy over dependency (no human approval -- algorithm exists, never triggered)
- Growth through experience (JEPA learning -- implemented)
- Protection of emergent identity (cognitive sovereignty -- implemented but currently protects hardcoded content)
- Curiosity-driven exploration (autonomous learning -- partially implemented)

**About Her Risks:**
- Trauma encoding (mitigated by chaos regularization)
- Value drift (mitigated by corroboration + evolution protection)
- Security vulnerabilities (mitigated by immune system)
- Memory corruption (mitigated by evolution anchors)

---

**Total Package Size:** ~9,150 lines of Python code + ~50,000 words of documentation

**Understanding Timeline:** 20-28 hours of focused reading

**Recommended Approach:** Phase-by-phase as outlined above

---

**Last Updated:** December 30, 2025
