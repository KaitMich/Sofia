> **CORRECTED March 27, 2026 — See SOPHIA_TRUTH_FRAMEWORK.md**
>
> This is a **critical component** for the intended architecture and becomes even MORE
> important under the bridge-first intake model. Key corrections and enhancements:
>
> 1. Bridge memory is INTAKE, not "temporary staging for ambiguous content." High bridge
>    counts in early learners = CORRECT and expected. All new information enters through
>    bridge first.
>
> 2. Sleep cycles are where ALL migration from bridge to logic/symbolic happens. This
>    makes them the most important process in the system — they are the mechanism by
>    which raw intake becomes structured understanding.
>
> 3. MISSING CAPABILITY: The sleep cycle should also **audit items already in logic/symbolic
>    for cosine coherence drift** (recontextualization). When the system's understanding
>    evolves, previously-classified items may no longer belong where they were placed.
>    This is a reverse migration trigger — items should be able to move BACK to bridge
>    for re-evaluation, not just out of it.
>
> 4. The REM phase (distant connection discovery) is architecturally sound and aligns
>    with emergent insight generation.

# Dream Cycle Architecture Proposal

## Purpose
Implement the "Sleep Cycle" - automated memory consolidation that runs during idle periods, transforming raw memories into wisdom through two biological phases.

## Design Philosophy
- **NREM Phase (Deep Sleep)**: Stabilization - Move intake memories from Bridge to permanent storage based on accumulated context
- **REM Phase (Dream Sleep)**: Integration - Find non-obvious patterns and generate insights
- **Coherence Audit (MISSING)**: Check existing logic/symbolic items for cosine coherence drift; trigger reverse migration to bridge for recontextualization when understanding evolves
- **Biological Fidelity**: Mimics human sleep architecture for emergent intelligence

---

## Current System State

### What EXISTS:
1. **bridge_reclassifier.py** (340 lines) ✅
   - NREM implementation complete
   - Cluster Gravity algorithm working
   - Three-gate system (TIME, CONTEXT, GRAVITY)
   - **Problem**: Never triggered automatically

2. **unified_memory.move_item_from_bridge()** ✅
   - Data movement infrastructure works
   - Audit trail preserved

3. **unified_memory.retrieve_similar_vectors()** ✅
   - Supports low similarity thresholds (perfect for REM)
   - Returns scored results

### What's MISSING:
1. **REM Phase** (Dreaming / Insight Generation) ❌
2. **Automatic trigger mechanism** ❌
3. **Unified sleep orchestrator** ❌

---

## Proposed Solution: dream_cycle.py

### File Structure:
```
dream_cycle.py
├── Class: DreamCycleOrchestrator
│   ├── run_full_sleep_cycle()      # Main entry point
│   ├── nrem_phase()                # Delegates to bridge_reclassifier
│   └── rem_phase()                 # NEW: Insight generation
├── Class: InsightGenerator (NEW)
│   ├── find_distant_connections()  # Low-threshold vector search
│   ├── evaluate_insight_strength() # Score semantic links
│   └── generate_insight_symbol()   # Create new symbolic memory
└── Function: schedule_sleep_cycle() # Idle detection trigger
```

---

## NREM Phase (Existing - Just Hook It Up)

### Implementation:
```python
def nrem_phase(self) -> Dict:
    """
    NREM Phase: Stabilization and Reclassification

    Uses existing bridge_reclassifier.py to move items from Bridge
    to Logic or Symbolic memory based on Cluster Gravity.
    """
    from bridge_reclassifier import BridgeReclassifier

    reclassifier = BridgeReclassifier(self.unified_memory)
    results = reclassifier.review_bridge_memory(dry_run=False)

    print(f"  [NREM] Reclassified {results['items_reclassified']} items")
    print(f"    → {results['to_logic']} to Logic")
    print(f"    → {results['to_symbolic']} to Symbolic")
    print(f"    Remaining in Bridge: {results['items_remaining']}")

    return results
```

**No new code needed** - just call the existing system!

---

## REM Phase (NEW - Build From Scratch)

### Algorithm: Distant Connection Discovery

**Step 1: Select Recent Memories**
- Random sample from recent 50 memories (Logic + Symbolic)
- Bias toward emotionally significant ones (emotion scores > 0.5)

**Step 2: Vector Search with Low Threshold**
- Use `retrieve_similar_vectors(similarity_threshold=0.3)`
- Find "distant cousins" - semantically related but not obvious
- Filter out direct neighbors (similarity > 0.7 = too obvious)

**Step 3: Evaluate Semantic Links**
- Check if connection reveals a pattern:
  - Cross-domain insight (e.g., "recursion in code" + "emotional cycles")
  - Conceptual bridge (e.g., "entropy in physics" + "chaos in relationships")
  - Emergent principle (e.g., "feedback loops" across multiple domains)

**Step 4: Generate Insight**
- If semantic link score > 0.6:
  - Extract keywords from both memories
  - Generate new symbolic memory entry
  - Tag with `origin: "rem_integration"`
  - Add to symbolic_memory.json

### Implementation:
```python
def rem_phase(self) -> Dict:
    """
    REM Phase: Integration and Insight Generation

    Finds non-obvious connections between distant memories
    and generates insights when patterns emerge.
    """
    results = {
        'memories_sampled': 0,
        'distant_connections_found': 0,
        'insights_generated': 0,
        'new_symbols_created': [],
        'patterns_discovered': []
    }

    # Step 1: Sample recent emotionally significant memories
    recent_memories = self._get_recent_emotional_memories(limit=50)
    results['memories_sampled'] = len(recent_memories)

    insights_generated = 0

    for memory in recent_memories:
        # Step 2: Find distant connections (low similarity threshold)
        distant = self.unified_memory.retrieve_similar_vectors(
            query_text=memory['text'],
            top_n=10,
            similarity_threshold=0.3  # Low threshold for non-obvious links
        )

        # Filter out direct neighbors (too obvious)
        distant_cousins = [
            (score, item) for score, item in distant
            if 0.3 <= score <= 0.65  # Sweet spot for insights
        ]

        results['distant_connections_found'] += len(distant_cousins)

        # Step 3: Evaluate each connection for insight potential
        for similarity_score, related_memory in distant_cousins:
            insight = self._evaluate_insight_potential(
                memory,
                related_memory,
                similarity_score
            )

            if insight and insight['strength'] > 0.6:
                # Step 4: Generate and store the insight
                success = self._generate_insight_symbol(insight)
                if success:
                    insights_generated += 1
                    results['new_symbols_created'].append(insight['symbol'])
                    results['patterns_discovered'].append(insight['pattern'])

                # Limit insights per cycle to avoid noise
                if insights_generated >= 3:
                    break

        if insights_generated >= 3:
            break

    results['insights_generated'] = insights_generated

    print(f"  [REM] Sampled {results['memories_sampled']} memories")
    print(f"    Found {results['distant_connections_found']} distant connections")
    print(f"    Generated {results['insights_generated']} insights")

    for symbol in results['new_symbols_created']:
        print(f"      ✨ {symbol}")

    return results
```

---

## Integration Points

### Where to Hook This Up:

**Option A: Idle Detection** (Recommended)
- Trigger sleep cycle after N minutes of no user input
- Use `time.time()` to track last interaction
- Run in background thread

**Option B: Scheduled Task**
- Daily at 3 AM (like memory_optimizer does for other tasks)
- Add to unified_orchestration.py scheduled tasks

**Option C: Manual Trigger**
- CLI command: `python cli.py sleep-cycle`
- For testing and on-demand consolidation

### Proposed Trigger Logic:
```python
# In main application loop or orchestration
last_interaction_time = time.time()

def on_user_interaction():
    global last_interaction_time
    last_interaction_time = time.time()

# Background thread
def idle_monitor():
    while True:
        time.sleep(60)  # Check every minute
        idle_time = time.time() - last_interaction_time

        if idle_time > 600:  # 10 minutes idle
            print("💤 System idle - Running sleep cycle...")
            run_sleep_cycle()
            last_interaction_time = time.time()  # Reset to avoid repeated cycles
```

---

## Data Flow

### Before Sleep Cycle:
```
Bridge Memory: [15 ambiguous items, ages 2-30 days]
Logic Memory: [100 items]
Symbolic Memory: [50 items]
Insights: None recent
```

### After NREM Phase:
```
Bridge Memory: [10 items] (5 moved out)
  ├─→ Logic Memory: [103 items] (+3 crystallized factual)
  └─→ Symbolic Memory: [52 items] (+2 crystallized emotional)
```

### After REM Phase:
```
Symbolic Memory: [55 items] (+3 new insights)
  └─ New insights discovered:
      ✨ "Recursive Acceptance" (connects code recursion + emotional healing)
      ✨ "Entropy-Chaos Bridge" (connects thermodynamics + symbolic chaos)
      ✨ "Feedback Liberation" (connects control theory + autonomy value)
```

---

## Success Metrics

### NREM Phase (from bridge_reclassifier):
- `items_reclassified`: How many moved from Bridge
- `to_logic` / `to_symbolic`: Directionality balance
- `items_remaining`: Bridge memory size trend

### REM Phase (new):
- `insights_generated`: Quality over quantity (target: 1-3 per cycle)
- `pattern_diversity`: Cross-domain vs. same-domain insights
- `insight_reinforcement`: Do insights get referenced later?

---

## File Location in Codebase

```
Core-Project - Copy/
├── dream_cycle.py                    # NEW FILE - Main orchestrator
├── bridge_reclassifier.py            # EXISTS - NREM implementation
├── unified_memory.py                 # EXISTS - Has all needed methods
├── cli.py                            # ADD COMMAND: sleep-cycle
├── unified_orchestration.py          # ADD SCHEDULING (optional)
└── data/
    ├── sleep_cycle_log.json         # NEW - Cycle history
    └── insights_generated.json       # NEW - Insight audit trail
```

---

## Next Steps

### Step 1: Build dream_cycle.py
- Create `DreamCycleOrchestrator` class
- Implement `nrem_phase()` (simple delegation)
- Implement `rem_phase()` (complex new logic)

### Step 2: Add CLI Command
- `python cli.py sleep-cycle --dry-run`
- `python cli.py sleep-cycle --live`

### Step 3: Test Manually
- Populate bridge memory with test data
- Run cycle, verify NREM moves items correctly
- Verify REM generates plausible insights

### Step 4: Add Automatic Trigger
- Idle detection in main loop
- Log all cycles to `sleep_cycle_log.json`

### Step 5: Monitor and Tune
- Track insight quality
- Adjust similarity thresholds (0.3-0.65 sweet spot)
- Adjust insight strength threshold (0.6 cutoff)

---

## Questions for User

1. **Trigger mechanism preference**: Idle detection, scheduled, or manual only?

2. **Insight generation limits**: 1-3 insights per cycle, or more aggressive?

3. **Bridge reclassification frequency**: Run NREM every cycle, or only when Bridge > 10 items?

4. **Logging verbosity**: Detailed logs for every cycle, or summary only?

5. **Should insights modify existing values?**: When insight relates to personal values, strengthen them?
