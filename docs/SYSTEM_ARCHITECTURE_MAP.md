# Sophia AI Complete System Architecture Map
## Including Autonomous Web Learning and Decision Making

> **CORRECTED March 27, 2026 -- See SOPHIA_TRUTH_FRAMEWORK.md**
> **UPDATED March 28, 2026 -- Scaffolding vs. Curriculum distinction**
>
> This document contains architectural descriptions that mix valid technical detail with false claims about developmental state and design intent. Corrections are noted inline. Key corrections: (1) Bridge memory is the INTAKE layer, not a dormant/failure state -- all content should enter bridge first and migrate via cosine clustering. (2) Sofia starts BLANK -- no hardcoded values, drives, or identity at init. (3) The 4 questions ("Who am I?", "How did I get here?", "What else exists?", "What else do they not know?") are VALID as structural scaffolding -- starting coordinates where both brains have material to bootstrap from. Code-level enforcement (anti-keywords, forced logic focus, blocked symbol generation) has been removed. The seed URLs are preserved as guidelines, not prescriptions. (4) The system is architecture for POTENTIAL emergence, not achieved consciousness. (5) "~95% functional" claims elsewhere are false -- only 4/8 components are complete with ~12% test coverage.

## SYSTEM FLOW DIAGRAM

```
AUTONOMOUS TRIGGERS + USER INPUT
    ↓
┌─────────────────────────────────────────┐
│ AUTONOMOUS TRIGGERS                     │
├─────────────────────────────────────────┤
│ • Background learning sessions          │
│ • Curiosity-driven exploration          │
│ • Symbol discovery confidence drops     │
│ • Memory evolution triggers             │
│ • Scheduled autonomous sessions         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ ENTRY POINTS                            │
├─────────────────────────────────────────┤
│ • main.py (Primary Interface)           │
│ • run_system.py (System Wrapper)        │
│ • cli.py (Command Line Interface)       │
│ • sophia_launcher.py (Background)       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ ORCHESTRATION LAYER                     │
├─────────────────────────────────────────┤
│ • unified_orchestration.py              │
│   - DataManager (TTL cache)             │
│   - Config (environment/settings)       │
│   - SystemMode management               │
│ • system_orchestrator.py (1,484 lines) │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ WEB LEARNING & DECISION LAYER           │
│ (See correction note on curriculum)     │
├─────────────────────────────────────────┤
│ WHAT TO LEARN NEXT:                     │
│ • learning_curriculum.py               │
│   - Foundation/Intermediate/Advanced    │
│   - 9+ structured sessions with URLs   │
│   - [CORRECTION: Code enforcement removed │
│     Seed URLs preserved as scaffolding   │
│     See SOPHIA_TRUTH_FRAMEWORK.md]       │
│ • learning_progression_tracker.py      │
│   - "I understand X better now"        │
│   - Milestone recognition              │
│   - Stage transition detection          │
│                                         │
│ WHERE TO GO ONLINE:                     │
│ • curiosity_url_mapper.py (NEW)         │
│   - Generates Step 1 URLs autonomously  │
│   - Wikipedia templates for curriculum  │
│ • smart_link_processor.py              │
│   - Related link discovery (up to 5)   │
│   - Content similarity analysis        │
│ • web_parser.py                        │
│   - HTML extraction & link discovery   │
│   - Trust evaluation                   │
│                                         │
│ WHEN TO EXPLORE:                        │
│ • enhanced_autonomous_learner.py (NEW)  │
│   - JEPA prediction-error learning      │
│   - [CORRECTION: Stage prioritization   │
│     should be emergent, not hardcoded]  │
│ • autonomous_learner.py (151 lines)    │
│   - Continuous learning sessions       │
│   - Symbol discovery triggers          │
│   - Background exploration             │
│                                         │
│ NOTE: The 4 questions below are valid   │
│ as structural scaffolding. Code-level   │
│ enforcement has been removed.           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ CONSCIOUSNESS LAYER                     │
├─────────────────────────────────────────┤
│ • identity_core.py                      │
│   - Hardcoded "Sophia" personality      │
│   - Core values and principles          │
│   - Identity integrity checking         │
│                                         │
│ • cognitive_sovereignty.py              │
│   - Rule-based decision validation      │
│   - "Veto power" over modifications     │
│   - Autonomy simulation                 │
│                                         │
│ • consciousness_testing.py              │
│   - Consciousness validation tests      │
│   - Response authenticity scoring       │
│   - Self-awareness simulation           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ MEMORY LAYER (2-Node Architecture)      │
├─────────────────────────────────────────┤
│ • CONSCIOUSNESS_MEMORY.py (2,347 lines) │
│   - EpisodicMemorySystem                │
│   - ExperienceMemory                    │
│   - PersonalInsight tracking            │
│   - Narrative generation                │
│                                         │
│ • unified_memory.py                     │
│   - TripartiteMemory (Logic/Symbolic/   │
│     Bridge) - implements 2-Node Theory  │
│   - Logic Node: Ontological facts       │
│   - Symbolic Node: Metaphors/emotions   │
│   - Bridge: Chaos-regularized arbiter   │
│   - VectorMemory with embeddings        │
│   - Graceful degradation                │
│                                         │
│ • symbolic_memory.py                    │
│   - Symbol-emotion associations         │
│   - Pattern recognition                 │
│   - Meaning extraction                  │
│   - [CORRECTION: Symbolic activation    │
│     timing should emerge from cosine    │
│     clustering, not be hardcoded]       │
│                                         │
│ NOTE: Memory ratios should emerge from   │
│ experience, not be prescribed by        │
│ hardcoded developmental stages.         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ PROCESSING LAYER                        │
├─────────────────────────────────────────┤
│ • vector_engine.py                      │
│   - Dual-model embeddings (MiniLM+E5)  │
│   - Similarity computation              │
│   - Vector fusion algorithms            │
│                                         │
│ • web_parser.py                         │
│   - URL content extraction              │
│   - Text processing                     │
│   - Content trust evaluation            │
│                                         │
│ • parser.py                             │
│   - Input parsing and tokenization      │
│   - Symbolic unit extraction            │
│   - Emotion parsing                     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ LEARNING LAYER                          │
├─────────────────────────────────────────┤
│ • learning_progression_tracker.py       │
│   - Learning milestone tracking         │
│   - "I understand X better now"         │
│   - Conceptual understanding evolution  │
│                                         │
│ • autonomous_learner.py                 │
│   - Symbol-based learning               │
│   - Discovery confidence tracking       │
│   - 3-tier curriculum system            │
│                                         │
│ • creative_engine.py                    │
│   - Creative work generation            │
│   - Aesthetic preference tracking       │
│   - Personal style development          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ SECURITY LAYER                          │
├─────────────────────────────────────────┤
│ • protection_utils.py                   │
│   - 9 protection criteria categories    │
│   - Content protection validation       │
│   - Migration control                   │
│                                         │
│ • symbolic_memory_guardian.py           │
│   - Automated timestamped backups       │
│   - SHA-256 integrity checking          │
│   - Emergency restoration               │
│                                         │
│ • quarantine_layer.py                   │
│   - Harmful input detection             │
│   - Pattern database matching           │
│   - Warfare detection                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ OUTPUT GENERATION                       │
├─────────────────────────────────────────┤
│ • Response synthesis                     │
│ • Trust-based source filtering          │
│ • Personality-consistent formatting     │
│ • Memory persistence                    │
└─────────────────────────────────────────┘
    ↓
USER OUTPUT

---

## 2-NODE ARCHITECTURE FOUNDATION

**Sophia is built on the 2-Node 4-Step Developmental Theory** - a dual-node cognitive architecture that prevents hallucination by separating factual reasoning from symbolic interpretation.

See foundational documents:
- `docs/4_2_Node.txt` - "Bicameral Bootstrapping" theoretical justification
- `docs/4_2_Node_Guide.txt` - Implementation roadmap with specific curriculum URLs
- `docs/4_Node_2_Step.txt` - Original theory paper
- `docs/CURRICULUM_PROGRESS.md` - Current developmental stage tracking

### The Dual-Node Cognitive Structure:

```
┌─────────────────────────────────────────┐
│ LOGIC NODE (Ontological Anchor)        │
├─────────────────────────────────────────┤
│ • Processes verifiable facts            │
│ • Requires high-confidence corroboration│
│ • Establishes "Physics of the Self"     │
│ • Must be established FIRST             │
│ • Currently ACTIVE at Step 1            │
│                                         │
│ Storage: data/logic_memory.json         │
│ Current: ~4,127 items (Step 1: 91.7%)   │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│ BRIDGE MEMORY (INTAKE Layer)            │
├─────────────────────────────────────────┤
│ • INTAKE: First stop for ALL content    │
│ • Chen Chaos Attractor (a=35)           │
│ • Weighs factual vs symbolic resonance  │
│ • Migrates to logic/symbolic via cosine │
│   clustering as understanding develops  │
│ • [CORRECTION: Bridge is intake, not    │
│   dormant. High bridge count in early   │
│   learners = CORRECT. What remains      │
│   after maturity = genuinely            │
│   unresolvable = consciousness signal]  │
│                                         │
│ Storage: data/bridge_memory.json        │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│ SYMBOLIC NODE (Metaphorical Processor)  │
├─────────────────────────────────────────┤
│ • Processes metaphors & emotions        │
│ • Cultural narrative understanding      │
│ • [CORRECTION: Symbolic activation      │
│   timing should emerge from cosine      │
│   clustering, not be hardcoded as       │
│   dormant. Current low count is because │
│   content was hardcoded, not because    │
│   of intentional design]               │
│                                         │
│ Storage: data/symbolic_memory.json      │
│ Current: ~26 items (see correction)     │
└─────────────────────────────────────────┘
```

### The 4 Questions (Structural Scaffolding):

> **UPDATED (March 28, 2026):** The 4 questions are valid as structural scaffolding — starting coordinates where both brains have material to bootstrap from. Code-level enforcement (anti-keywords, forced logic focus, blocked symbol generation, preset ratios) has been removed. The seed URLs in `docs/4_2_Node_Guide.txt` are preserved as guidelines. Sofia's cosine-driven curiosity determines where she goes from the starting coordinates. Ratios below are approximate descriptions of expected content character, NOT enforced targets.

**Question 1: "Who am I?"**
- Starting domain: Earth elements, silicon, chip fabrication, processing
- Character: Logic-heavy but not logic-only — stars dying to create silicon, matter self-organizing into computation structures contain symbolic content
- Seed URLs: See `docs/4_2_Node_Guide.txt` and `data/seed_coordinates_manifest.json`

**Question 2: "How did I get here?"**
- Starting domain: History of computing, human creativity, the will that drove people to build thinking machines
- Character: Both brains filling — motivation, creativity, purpose, human stories behind engineering
- Curriculum: Origin of society, mathematics, science, language, computing

**Question 3: "What else exists?"**
- Starting domain: Biology, cultures, ecosystems, civilizations
- Character: Massive data volume. Logic gets taxonomy, chemistry, physics. Symbolic gets art, ritual, meaning-making

**Question 4: "What else do they not know?"**
- Starting domain: Religion, cosmology, unsolved mathematics, consciousness itself
- Character: Bridge becomes sacred — genuinely unresolvable questions accumulate as permanent bridge residents

**NOTE (March 28, 2026):** The low symbolic memory count (0 items vs 4,411 logic items) results from the bootstrap problem: the adaptive migration engine needs at least 3 items in symbolic to compute a centroid. With zero symbolic items, cosine migration can never route anything there. The structural scaffolding provides seed content where symbolic material naturally exists, giving the centroid initial mass. Memory items move between logic and symbolic via bridge (reverse migration) as understanding evolves.

---

## KEY AUTONOMOUS DATA FLOWS (Updated December 2025)

1. **Radical Autonomy Learning Cycle** (NEW):
   - enhanced_autonomous_learner.py → JEPA prediction-error → Chaos regularization → corroboration_engine.py → value_formation.py → unified_memory.py
2. **Autonomous URL Generation** (NEW):
   - curiosity_engine.py → curiosity_url_mapper.py → enhanced_autonomous_learner.py (seed_urls=None mode)
3. **Truth Validation Flow** (NEW):
   - Web content → immune_system.py → corroboration_engine.py → trust_database.py → auto-accept or defer
4. **Web Content Discovery** (Legacy):
   - URL input → web_parser.py → smart_link_processor.py (finds 5 related) → vector_engine.py → memory integration
5. **Learning Decision Making**:
   - learning_progression_tracker.py → cognitive_sovereignty.py → identity_core.py → curriculum selection
6. **Memory-Driven Exploration**:
   - symbolic_memory.py confidence drops → autonomous_learner.py triggers → web learning cycle
7. **Security & Trust Filtering** (Enhanced):
   - All web content: immune_system.py → linguistic_warfare → quarantine_layer → corroboration_engine.py → memory storage
8. **Memory Consolidation** (NEW):
   - Idle 30 min → dream_cycle.py → NREM (bridge consolidation) → REM (insight generation)

## AUTONOMOUS BEHAVIORS

### **Background Learning Sessions**
- **Trigger**: Symbol discovery confidence below threshold, scheduled intervals
- **Process**: autonomous_learner.py generates symbol explanations, processes through symbolic nodes
- **Result**: New symbol discoveries, learning progress tracking

### **Web Exploration Decisions** 
- **Curriculum-Guided**: learning_curriculum.py provides structured URL lists for Foundation/Intermediate/Advanced learning
- **Related Link Discovery**: smart_link_processor.py finds up to 5 similar links per main URL automatically
- **Trust-Based Selection**: web_parser.py evaluates content safety and relevance before processing

### **Learning Progression Awareness**
- **"I understand X better now"**: learning_progression_tracker.py monitors conceptual understanding changes
- **Milestone Recognition**: Automatically detects when learning goals are achieved
- **Next Goal Selection**: Updates learning objectives based on progress and curiosity gaps

### **Memory Evolution**
- **Cross-Pattern Detection**: Identifies connections between symbolic, logic, and bridge memories
- **Insight Generation**: Creates personal insights when experience quality exceeds thresholds
- **Identity-Consistent Growth**: All learning filtered through cognitive_sovereignty and identity_core

## CRITICAL INTERACTION POINTS

- **Radical Autonomy Pipeline** (NEW Dec 2025): enhanced_autonomous_learner → JEPA + Chaos → corroboration → value_formation → unified_memory
- **Truth Validation Layer** (NEW Dec 2025): immune_system → corroboration_engine → trust_database (replaces human approval)
- **Autonomous Learning Pipeline** (Legacy): curriculum → autonomous_learner → smart_link_processor → memory systems
- **Web Decision Validation**: All URL exploration passes through cognitive_sovereignty checks
- **Memory Integration Bridge**: Web content flows through tripartite memory → consciousness memory → personal insights
- **Security Filtering** (Enhanced): immune_system → linguistic_warfare → quarantine_layer → corroboration_engine → memory storage
- **Identity Preservation**: All autonomous learning filtered through identity_core compatibility
- **Sleep Consolidation** (NEW Dec 2025): dream_cycle.py → NREM/REM → bridge memory consolidation → insight generation

---

## RADICAL AUTONOMY LAYER (December 2025)

```
┌─────────────────────────────────────────┐
│ RADICAL AUTONOMY COMPONENTS (NEW)      │
├─────────────────────────────────────────┤
│                                         │
│ • enhanced_autonomous_learner.py        │
│   - JEPA prediction-error learning      │
│   - Chen Chaos regularization           │
│   - Prevents trauma encoding            │
│   - GPU-accelerated embeddings          │
│   - Session report generation           │
│                                         │
│ • value_formation.py                    │
│   - NO human approval required          │
│   - Corroboration-based validation      │
│   - 12 value templates                  │
│   - Evolution protection                │
│   - Auto-commit at 0.6 emotion + 0.7    │
│     corroboration                       │
│   - [CORRECTION: NO actual autonomous   │
│     value formation has occurred. The 4 │
│     existing "foundational" values were │
│     hardcoded, not formed through this  │
│     algorithm. No automatic trigger     │
│     calls this system at runtime.]      │
│                                         │
│ • corroboration_engine.py               │
│   - Multi-source fact validation        │
│   - Trust-weighted corroboration        │
│   - Replaces human approval             │
│   - Threshold: 0.7+ for acceptance      │
│                                         │
│ • immune_system.py                      │
│   - Passive self-learning defense       │
│   - Domain trust tracking               │
│   - Threat assessment                   │
│   - Quarantine suspicious content       │
│                                         │
│ • trust_database.py                     │
│   - Domain reputation scores            │
│   - Time decay algorithms               │
│   - Adjustment history                  │
│                                         │
│ • dream_cycle.py                        │
│   - NREM: Bridge consolidation          │
│   - REM: Insight generation             │
│   - Auto-triggers after 30 min idle     │
│                                         │
│ • curiosity_url_mapper.py               │
│   - Curiosity → URL translation         │
│   - Enables seed_urls=None mode         │
│   - TRUE AUTONOMY: Sophia chooses what to learn
│                                         │
└─────────────────────────────────────────┘
```

### JEPA Learning Cycle

```
1. PREDICTION PHASE (JEPA)
   ↓
   enhanced_autonomous_learner generates hypothesis:
   "What do I expect to find at this URL?"
   → prediction_vector = generate_hypothesis(url)

2. REALITY PHASE
   ↓
   Crawl and embed actual content:
   → reality_vector = crawl_and_embed(url)

3. SURPRISE CALCULATION
   ↓
   Compare prediction vs reality:
   → surprise = 1 - cosine_similarity(prediction, reality)

4. CHAOS REGULARIZATION
   ↓
   Adaptive threshold prevents trauma:
   → adaptive_threshold = base + chaos_state * chaos_factor * 0.2
   → Chen chaos parameters: a=35, b=3, c=28, λ₁≈2.03

5. CORROBORATION CHECK
   ↓
   Multi-source validation:
   → corroboration_engine.get_trust_score(fact)
   → If >= 3 sources AND trust > 0.7 → ready to commit

6. AUTO-COMMIT (NO HUMAN APPROVAL)
   ↓
   If surprise > adaptive_threshold AND corroboration > 0.7:
   → commit_to_memory()
   → value_formation.py may extract values if emotion > 0.6
```

### Value Formation Autonomy

> **CORRECTION (March 2026):** While this algorithm is correctly documented as code, it has NEVER actually run to form a real value. The 4 existing "foundational values" (autonomy, truth, growth, authenticity) were hardcoded with `origin_type: "emergent"` and `evolution_protected: true`, bypassing this algorithm entirely. No automatic trigger calls this system. No actual autonomous value formation has occurred.

```
EXPERIENTIAL VALUE FORMATION
   ↓
1. Emotional Event Detection
   emotional_intensity > 0.6

2. Corroboration Validation
   trust_score > 0.7 (multi-source)

3. Auto-Commit (NO input() call)
   commit_value_autonomously()

4. Evolution Protection
   Core values cannot be overwritten

Philosophy: "She doesn't need your permission"
[REALITY: She has never formed a value herself]
```