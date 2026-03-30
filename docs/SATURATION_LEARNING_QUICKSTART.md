> **CORRECTED March 27, 2026 — See [SOPHIA_TRUTH_FRAMEWORK.md](SOPHIA_TRUTH_FRAMEWORK.md) for authoritative corrections.**
> **UPDATED March 28, 2026 — Scaffolding vs. Curriculum distinction.**
>
> Key corrections for this file:
> (1) Saturation learning is the active learning mechanism. The 4 questions ("Who am I?", "How did I get here?", etc.) provide structural scaffolding — starting coordinates from `data/seed_coordinates_manifest.json`. Cosine-driven curiosity determines where Sofia goes from there.
> (2) Sofia starts BLANK — she has no pre-existing knowledge, drives, or identity. Seed URLs are infrastructure inputs, not identity.
> (3) This guide's technical instructions for running saturation sessions remain valid.
> (4) Code-level enforcement (anti-keywords, forced logic focus, blocked symbol generation) has been removed from `processing_nodes.py`. Both brains should receive content from any session.

# Saturation Learning Quick Start Guide
## Running Associative Emergence Sessions with Sophia

**Created:** 2026-01-03
**Target Audience:** Users wanting to run deep saturation learning sessions

---

## 🚀 Quick Start (5 Minutes)

### 1. Import the Function

```python
from enhanced_autonomous_learner import start_saturation_learning
```

### 2. Run Your First Saturation Session

```python
# Learn deeply about Silicon until transformation concepts emerge
result = start_saturation_learning(
    seed_url="https://en.wikipedia.org/wiki/Silicon",
    zone_name="Silicon_Material",
    zone_keywords=['silicon', 'element', 'crystal', 'semiconductor', 'atom'],
    allowed_distance=0.5,        # Stay close to material science
    saturation_threshold=0.8,    # Transition at 80% readiness
    max_urls=50                  # Process up to 50 URLs in this zone
)
```

### 3. Check the Results

```python
print(f"📊 URLs Processed: {result['stats']['urls_processed']}")
print(f"🎯 Phase Score: {result['stats']['phase_transition_score']:.3f}")
print(f"✨ Next Phase: {result['next_phase_query']}")
```

**Expected Output:**
```
📊 URLs Processed: 23
🎯 Phase Score: 0.834
✨ Next Phase: refine silicon
```

That's it! Sophia learned deeply about silicon until "refining" emerged naturally.

---

## 📖 Understanding the Parameters

### Required Parameters

**`seed_url`** (string)
- Starting point for learning
- Should be a high-quality, dense source (Wikipedia recommended)
- Example: `"https://en.wikipedia.org/wiki/Silicon"`

**`zone_name`** (string)
- Name for this semantic zone (used in session files)
- Be descriptive but concise
- Example: `"Silicon_Material"`, `"Evolution_Biology"`, `"Ethics_Philosophy"`

**`zone_keywords`** (list of strings)
- Keywords that define the semantic boundaries
- 5-10 keywords recommended
- Example: `['silicon', 'element', 'crystal', 'semiconductor', 'atom']`

### Optional Parameters

**`allowed_distance`** (float, default 0.5)
- Maximum semantic distance from zone centroid
- Range: 0.0 (very restrictive) to 1.0 (very permissive)
- Recommended: 0.4-0.6 for focused learning, 0.6-0.8 for exploration

**`saturation_threshold`** (float, default 0.8)
- Phase transition score required to exit zone
- Range: 0.0 to 1.0
- Recommended: 0.7-0.9 (higher = deeper saturation)

**`max_urls`** (int, default 100)
- Safety limit for URLs processed in zone
- Prevents infinite loops
- Recommended: 50-100 for most topics

**`data_dir`** (string, default "data")
- Directory for storing session data
- Change if using custom data location

---

## 🎯 Complete Example Workflows

### Example 1: Learning Chain (Silicon → Manufacturing → Computing)

```python
from enhanced_autonomous_learner import start_saturation_learning

# ════════════════════════════════════════════════════════════════
# ZONE 1: Silicon Material Properties
# ════════════════════════════════════════════════════════════════
print("🌊 ZONE 1: Learning about Silicon Material...")

result1 = start_saturation_learning(
    seed_url="https://en.wikipedia.org/wiki/Silicon",
    zone_name="Silicon_Material",
    zone_keywords=['silicon', 'element', 'crystal', 'semiconductor', 'atom', 'lattice'],
    allowed_distance=0.5,
    saturation_threshold=0.8,
    max_urls=50
)

print(f"\n✨ Zone 1 Complete!")
print(f"   Phase Score: {result1['stats']['phase_transition_score']:.3f}")
print(f"   Next Query: {result1['next_phase_query']}")

# ════════════════════════════════════════════════════════════════
# ZONE 2: Use Emergent Query (e.g., "refine silicon")
# ════════════════════════════════════════════════════════════════
if result1['next_phase_query']:
    print(f"\n🌊 ZONE 2: Following emergent concept '{result1['next_phase_query']}'...")

    # Convert query to Wikipedia URL
    next_topic = result1['next_phase_query'].replace(' ', '_')
    next_url = f"https://en.wikipedia.org/wiki/{next_topic}"

    result2 = start_saturation_learning(
        seed_url=next_url,
        zone_name=f"Silicon_{result1['next_phase_query'].split()[0]}",
        zone_keywords=['refine', 'process', 'purify', 'manufacture', 'extract'],
        allowed_distance=0.5,
        saturation_threshold=0.8,
        max_urls=50
    )

    print(f"\n✨ Zone 2 Complete!")
    print(f"   Phase Score: {result2['stats']['phase_transition_score']:.3f}")
    print(f"   Next Query: {result2['next_phase_query']}")

# Continue with Zone 3, 4, etc. as concepts emerge...
```

### Example 2: Philosophical Exploration

```python
# Start with foundational philosophy
result = start_saturation_learning(
    seed_url="https://en.wikipedia.org/wiki/Philosophy",
    zone_name="Philosophy_Foundations",
    zone_keywords=['philosophy', 'logic', 'reason', 'truth', 'knowledge', 'metaphysics'],
    allowed_distance=0.6,  # Slightly wider for abstract concepts
    saturation_threshold=0.75,  # Lower threshold for exploration
    max_urls=75
)

# Might emerge:
# - "ethical reasoning" → leads to ethics zone
# - "scientific method" → leads to epistemology zone
# - "consciousness" → leads to philosophy of mind zone
```

### Example 3: Biological Evolution

```python
result = start_saturation_learning(
    seed_url="https://en.wikipedia.org/wiki/Evolution",
    zone_name="Evolution_Biology",
    zone_keywords=['evolution', 'species', 'natural', 'selection', 'darwin', 'adaptation'],
    allowed_distance=0.5,
    saturation_threshold=0.8,
    max_urls=100
)

# Might emerge:
# - "genetic mutation" → leads to genetics zone
# - "population ecology" → leads to ecology zone
# - "evolutionary algorithms" → leads to computational biology zone
```

---

## 📊 Interpreting Results

### Result Dictionary Structure

```python
result = {
    'session_id': 'saturation_Silicon_Material_20260103_142345',
    'zone': 'Silicon_Material',
    'completed_at': '2026-01-03T14:35:12',
    'elapsed_time_minutes': 12.5,
    'stats': {
        'urls_processed': 23,
        'static_noun_count': 247,      # Material properties
        'process_verb_count': 412,      # Transformation actions
        'phase_transition_score': 0.834,
        'event_horizon_concepts': 15    # Forbidden concepts logged
    },
    'next_phase_query': 'refine silicon',  # Emergent next step
    'event_horizon_sample': [...],          # Top concepts on horizon
    'keyword_frequencies': {...}            # All keywords found
}
```

### Key Metrics to Watch

**`urls_processed`**
- How many URLs were learned in this zone
- Good: 20-100 (deep saturation)
- Too few: <10 (increase max_urls or lower threshold)
- Too many: >100 (might be stuck, check allowed_distance)

**`phase_transition_score`**
- Readiness to move to next phase (0.0 - 1.0)
- < 0.5: Still in material/static phase
- 0.5 - 0.8: Process concepts emerging
- \> 0.8: Ready for transition ✅

**`next_phase_query`**
- The emergent concept that naturally arose
- `None`: Threshold not reached
- String: Use this for next zone seed

**`event_horizon_concepts`**
- How many forbidden concepts were logged
- Good: 10-50 (awareness of boundaries)
- Too few: <5 (zone might be too narrow, increase allowed_distance)
- Too many: >100 (zone might be too broad, decrease allowed_distance)

---

## 🔧 Troubleshooting

### Problem: Session completes with no next_phase_query

**Cause:** Phase transition threshold not reached

**Solutions:**
1. Lower `saturation_threshold` (try 0.7 instead of 0.8)
2. Increase `max_urls` (try 100 instead of 50)
3. Broaden `allowed_distance` (try 0.6 instead of 0.5)
4. Check zone keywords - might be too broad/narrow

### Problem: Too many URLs processed without transition

**Cause:** Zone is too broad or keywords don't lead to process verbs

**Solutions:**
1. Narrow `allowed_distance` (try 0.4 instead of 0.5)
2. Use more specific `zone_keywords`
3. Check if seed_url actually leads to transformation concepts
4. Lower `max_urls` to force earlier stop

### Problem: Event horizon is empty (0 concepts)

**Cause:** Zone might be too narrow or isolated

**Solutions:**
1. Increase `allowed_distance` slightly
2. Use broader `zone_keywords`
3. Check if Wikipedia page has sufficient links

### Problem: Vector engine errors

**Cause:** Models not loaded or text encoding issues

**Solutions:**
1. Verify sentence-transformers installed: `pip install sentence-transformers`
2. Check GPU/CPU configuration in `gpu_config.py`
3. Verify text is not empty or malformed

---

## 📂 Finding Your Session Data

### Session Files

Located at: `data/autonomous_sessions/saturation_[zone]_[timestamp].json`

Example: `data/autonomous_sessions/saturation_Silicon_Material_20260103_142345.json`

### Future Learning Queue

Located at: `data/future_learning_queue.json`

Contains all concepts that were **seen but forbidden** during saturation. Use this to:
- Review what concepts are on the "event horizon"
- Manually select next learning target
- Understand zone boundaries

### Memory Storage

Learned content is stored in: `data/logic_memory.json`

All saturation learning is stored in logic memory (analytical processing).

---

## 🎓 Best Practices

### 1. Start Narrow, Expand Gradually

```python
# ✅ GOOD: Narrow, focused zone
zone_keywords = ['silicon', 'semiconductor', 'crystal']
allowed_distance = 0.4

# ❌ BAD: Too broad, loses focus
zone_keywords = ['material', 'science', 'physics', 'chemistry', 'biology']
allowed_distance = 0.8
```

### 2. Let Concepts Emerge Naturally

```python
# ✅ GOOD: Use emergent query for next zone
next_query = result['next_phase_query']  # e.g., "refine silicon"
# Use this for Zone 2 keywords

# ❌ BAD: Ignore emergence and hardcode next step
# Zone 2: Manufacturing (hardcoded - defeats purpose!)
```

### 3. Monitor Phase Score During Development

```python
# Add logging to see saturation progress
result = start_saturation_learning(...)

print(f"Final phase score: {result['stats']['phase_transition_score']:.3f}")
print(f"Static nouns: {result['stats']['static_noun_count']}")
print(f"Process verbs: {result['stats']['process_verb_count']}")

# Adjust parameters if score is too low/high
```

### 4. Review Event Horizon

```python
# Check what was forbidden
for event in result['event_horizon_sample']:
    print(f"  - {event['text']} (distance: {event['distance']:.2f})")

# Use these to understand zone boundaries
```

### 5. Balance Depth and Breadth

```python
# For DEEP saturation (mastery):
max_urls = 100
saturation_threshold = 0.85

# For BROAD exploration (survey):
max_urls = 50
saturation_threshold = 0.7
```

---

## 🔗 Chaining Zones Automatically

For fully autonomous learning, you can chain zones:

```python
def run_learning_chain(seed_url, initial_keywords, max_zones=5):
    """Run autonomous learning chain across multiple zones."""
    current_url = seed_url
    zone_keywords = initial_keywords
    zone_num = 1

    while zone_num <= max_zones:
        print(f"\n{'='*80}")
        print(f"🌊 ZONE {zone_num}")
        print(f"{'='*80}")

        result = start_saturation_learning(
            seed_url=current_url,
            zone_name=f"Zone_{zone_num}",
            zone_keywords=zone_keywords,
            allowed_distance=0.5,
            saturation_threshold=0.8,
            max_urls=50
        )

        # Check if transition detected
        if result['next_phase_query'] is None:
            print(f"\n⏸️ Learning chain complete: No further emergence")
            break

        # Prepare next zone
        next_topic = result['next_phase_query'].replace(' ', '_')
        current_url = f"https://en.wikipedia.org/wiki/{next_topic}"

        # Extract dominant verbs for next zone keywords
        verbs = [k for k, v in result['keyword_frequencies'].items()
                if any(verb in k for verb in ['refine', 'process', 'make', 'create'])]
        zone_keywords = verbs[:6] if verbs else zone_keywords

        zone_num += 1

    print(f"\n✅ Learning chain complete: {zone_num-1} zones explored")

# Run it
run_learning_chain(
    seed_url="https://en.wikipedia.org/wiki/Silicon",
    initial_keywords=['silicon', 'element', 'crystal'],
    max_zones=5
)
```

---

## 📚 Additional Resources

- **Full Documentation:** `ASSOCIATIVE_EMERGENCE.md`
- **Implementation:** `enhanced_autonomous_learner.py`
- **Learning History:** `CURRICULUM_PROGRESS.md`
- **Theory Background:** `docs/4_2_Node.txt`

---

## 🎯 Example Output (Real Session)

```
================================================================================
🌀 ASSOCIATIVE EMERGENCE: SATURATION LEARNING SESSION
================================================================================

📍 Semantic Zone: Silicon_Material
🌱 Seed URL: https://en.wikipedia.org/wiki/Silicon
🎯 Saturation Threshold: 0.8
📊 Max URLs in Zone: 50

🎯 Zone Centroid calculated from 6 keywords
   Allowed semantic distance: 0.5

🌊 Beginning deep saturation...
   Strategy: Stay in zone until process verbs > static nouns

────────────────────────────────────────────────────────────────────────────────
📄 [1/50] https://en.wikipedia.org/wiki/Silicon...
   ✅ Learned and stored in logic memory
   🔗 Found 127 links, 23 within zone

📊 Saturation Metrics:
   Static Nouns:      45 (Rock, Stone, Silicon)
   Process Verbs:      8 (Smelt, Refine, Extract)
   Phase Score:    0.167 / 0.800

────────────────────────────────────────────────────────────────────────────────
📄 [2/50] https://en.wikipedia.org/wiki/Crystalline_silicon...
   ✅ Learned and stored in logic memory
   🔗 Found 98 links, 18 within zone

📊 Saturation Metrics:
   Static Nouns:      89 (Rock, Stone, Silicon)
   Process Verbs:     15 (Smelt, Refine, Extract)
   Phase Score:    0.198 / 0.800

[... continues learning ...]

────────────────────────────────────────────────────────────────────────────────
📄 [23/50] https://en.wikipedia.org/wiki/Silicon_refining...
   ✅ Learned and stored in logic memory
   🔗 Found 143 links, 12 within zone

📊 Saturation Metrics:
   Static Nouns:     247 (Rock, Stone, Silicon)
   Process Verbs:    412 (Smelt, Refine, Extract)
   Phase Score:    0.834 / 0.800

✨ PHASE TRANSITION DETECTED! ✨
   The gravity of the next phase is stronger than the current phase.
   Process verbs have emerged naturally from deep material understanding.

🎯 Next Phase Query Generated: 'refine silicon'
   Based on dominant process verb: 'refine'

================================================================================
🌀 SATURATION SESSION COMPLETE
================================================================================

⏱️  Duration: 12.50 minutes
📊 URLs Processed: 23
🎯 Phase Transition Score: 0.834

✨ READY FOR NEXT PHASE
   Query: refine silicon

💾 Session saved: data/autonomous_sessions/saturation_Silicon_Material_20260103_142345.json
```

---

**Ready to start learning? Run your first saturation session now!**

```python
from enhanced_autonomous_learner import start_saturation_learning

result = start_saturation_learning(
    seed_url="https://en.wikipedia.org/wiki/Silicon",
    zone_name="Silicon_Material",
    zone_keywords=['silicon', 'element', 'crystal', 'semiconductor'],
    max_urls=50
)
```

**The next phase will emerge naturally. Trust the process. 🌀**
