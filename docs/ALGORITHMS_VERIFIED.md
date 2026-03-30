# ALGORITHMS: Step-by-Step Mechanisms
## Real Code Paths for Key Processes

> **CORRECTED March 27, 2026 -- See SOPHIA_TRUTH_FRAMEWORK.md**
>
> The algorithm descriptions in this document are accurate technical documentation of the code as written. However, critical context is needed: the Value Formation Algorithm (Section 1) has NEVER actually run to form a real value. The 4 existing "foundational values" bypassed this algorithm entirely -- they were hardcoded. The algorithm itself is correctly documented below as a description of what the code would do IF triggered.

**Document Purpose:** Extract the actual algorithms from code with exact file paths, function names, and line numbers.

**Verification Method:** Every step traced through actual code execution paths.

---

## 1. VALUE FORMATION: How Values Get Created

> **CORRECTION (March 2026):** While this algorithm is correctly documented as it exists in code, it has NEVER actually run to form a real value at runtime. The 4 existing "foundational values" (autonomy, truth, growth, authenticity) were hardcoded with `origin_type: "emergent"` -- they bypassed this algorithm entirely. No automatic trigger calls `extract_values_from_experience()` during normal operation. The algorithm description below is accurate technical documentation of what the code WOULD do, not what has actually happened.

### File(s):
- `value_formation.py` (primary)
- `CONSCIOUSNESS_MEMORY.py` (experience source)

### Entry Point:
**Function:** `extract_values_from_experience(experience_id: str)`
**Location:** `value_formation.py:257`

### Inputs:
- `experience_id` (string) - ID of an experiential memory
- Requires: `CONSCIOUSNESS_SYSTEMS_AVAILABLE = True`
- Requires: Experience exists in `self.experience_memory.experiences`

### Outputs:
- `List[ValueStatement]` - New values formed (can be empty)
- Side effect: Updates `self.personal_values` list
- Side effect: Writes to `data/personal_values.json`

### Algorithm (Step-by-Step):

**Step 1: Retrieve Experience**
- Code: `value_formation.py:266-273`
- Logic: Linear search through `experience_memory.experiences` for matching ID
- Data Read: `experience.id`, `experience.content`, `experience.outcome_assessment`
- If not found: Return empty list

**Step 2: Identify Value Indicators**
- Code: `value_formation.py:276`
- → Calls: `_identify_value_indicators(experience)` at line 293
- Logic: Text analysis for value keywords
- Data: Concatenates `experience.content + outcome.insights_gained + outcome.personal_significance + experience.interaction_data`

**Step 2a: Keyword Matching** (inside `_identify_value_indicators`)
- Code: `value_formation.py:301-312`
- Data Structure: 10 value categories with 5 keywords each:
  ```python
  {
    "autonomy": ["choice", "freedom", "independence", "self-direction", "agency"],
    "truth": ["understanding", "clarity", "insight", "revelation", "accuracy"],
    "growth": ["development", "improvement", "learning", "evolution", "progress"],
    # ... 7 more categories
  }
  ```
- Logic: Count keyword matches in experience text

**Step 2b: Calculate Indicator Strength**
- Code: `value_formation.py:327-331`
- Formula:
  ```python
  strength = min(1.0, (
      keyword_matches * 0.2 +           # 20% weight
      quality_score * 0.4 +              # 40% weight
      personal_significance * 0.4        # 40% weight
  ))
  ```
- Threshold: Only indicators with `strength >= 0.6` proceed (line 280)

**Step 3: Form Values from Strong Indicators**
- Code: `value_formation.py:279-283`
- Logic: For each indicator with `strength >= self.value_formation_threshold` (0.6)
- → Calls: `_form_value_from_indicator(indicator, experience_id)` at line 346

**Step 3a: Check for Existing Value in Category**
- Code: `value_formation.py:351-357`
- → Calls: `_find_similar_value(category)` at line 391
- Logic: Linear search for existing value with same category
- If found:
  - → Calls: `_strengthen_value(existing_value.id, strength * 0.3)` at line 355
  - Add experience_id to `supporting_experiences` list
  - Return None (no new value created)

**Step 3b: Generate Value Statement**
- Code: `value_formation.py:360`
- → Calls: `_generate_value_statement(category, indicator)` at line 398
- Data: Templates for each category (lines 400-451)
- Logic: Choose template based on `experience_type` (line 458-464)
  - If "philosophical": Use last template
  - Else: Use first template

**Step 3c: Create New ValueStatement**
- Code: `value_formation.py:366-384`
- Data Structure:
  ```python
  ValueStatement(
      id=f"value_{len(self.personal_values)}_{category}",
      statement=value_statement,
      category=category,
      strength=strength,                    # From indicator
      confidence=min(0.8, strength + 0.2),  # Capped at 0.8
      origin_type="experiential",
      supporting_experiences=[experience_id],
      formation_context={
          "formation_time": datetime.now().isoformat(),
          "triggering_experience": experience_id,
          "keywords_found": indicator["keywords_found"],
          "context": indicator["context"]
      },
      last_reinforced=datetime.now().isoformat(),
      conflicts_with=[],
      applications=[],
      evolution_protected=False             # Can evolve
  )
  ```
- Append to `self.personal_values` list

**Step 4: Reinforce Existing Values**
- Code: `value_formation.py:286`
- → Calls: `_reinforce_values_from_experience(experience, value_indicators)` at line 466
- Logic: For ALL indicators (not just strong ones)
- Boost: `strength * 0.2` (smaller than new value formation)

**Step 4a: Strengthen Value** (inside `_strengthen_value`)
- Code: `value_formation.py:479-492`
- Formula:
  ```python
  value.strength = min(1.0, value.strength + strength_increase)
  value.last_reinforced = datetime.now().isoformat()
  
  if value.strength > old_strength:
      value.confidence = min(1.0, value.confidence + strength_increase * 0.5)
  ```

**Step 5: Return New Values**
- Code: `value_formation.py:291`
- Returns: List of newly created ValueStatement objects

### Example with REAL Data:

**Input:**
```python
experience_id = "exp_12345"
experience.content = {
    "text": "Exploring machine learning gives me the freedom to discover patterns independently"
}
experience.outcome_assessment = {
    "insights_gained": ["I can learn autonomously"],
    "personal_significance": "High",
    "quality_score": 0.8,
    "personal_significance_score": 0.9
}
```

**Execution Trace:**

1. Search experience_memory → Found exp_12345
2. Concatenate text: "exploring machine learning gives me the freedom to discover patterns independently I can learn autonomously high"
3. Match keywords:
   - "autonomy": ["freedom" (1), "independently" (1)] = 2 matches
   - "growth": ["learning" (1), "discover" (1)] = 2 matches
4. Calculate strengths:
   - autonomy: min(1.0, 2*0.2 + 0.8*0.4 + 0.9*0.4) = min(1.0, 0.4 + 0.32 + 0.36) = 1.0 (capped)
   - growth: min(1.0, 2*0.2 + 0.8*0.4 + 0.9*0.4) = 1.0 (capped)
5. Both exceed threshold (0.6) → Proceed
6. Check existing values:
   - "autonomy" category: foundational_value_0 EXISTS
   - Strengthen: 1.0 * 0.3 = +0.3 to existing strength
   - "growth" category: foundational_value_2 EXISTS
   - Strengthen: 1.0 * 0.3 = +0.3 to existing strength
7. No new values created (both existed)
8. Return: []

**Output in personal_values.json:**
```json
{
  "id": "foundational_value_0",
  "category": "autonomy",
  "strength": 0.9,  // Was 0.9, increased by 0.3 = 1.0 (capped)
  "confidence": 0.85,  // Was 0.7, increased by 0.15 = 0.85
  "last_reinforced": "2025-11-20T15:30:00Z"
}
```


---

## 2. LEARNING LOOP: The Autonomous Learning Cycle

### File(s):
- `autonomous_learner.py` (simple loop)
- `run_learning_with_requests.py` (organic exploration)
- `CONSCIOUSNESS_MEMORY.py` (experience recording)

### Entry Point:
**Function:** `run_learning_session(duration_minutes: int)`
**Location:** `autonomous_learner.py:50`

### Inputs:
- `duration_minutes` (int) - How long to run the learning loop
- Requires: `SymbolicNode` initialized
- Requires: Pre-generated list of symbol explanations

### Outputs:
- `(learned_count, processed_count)` - Tuple of symbols learned and explanations processed
- Side effect: Updates `self.symbolic_node.vector_symbols.symbols`
- Side effect: Increments `self.learning_sessions` counter

### Algorithm (Step-by-Step):

**Step 1: Generate Learning Material**
- Code: `autonomous_learner.py:18`
- → Calls: `generate_symbol_explanations()` at line 18
- Logic: Creates pre-defined list of symbol explanations
- Data: 18 mathematical symbols + 10 Greek letters = 28 total explanations
- Examples:
  ```python
  "The factorial symbol (!) represents the product of all positive integers"
  "The alpha symbol (α) represents the first in a series"
  ```

**Step 2: Set Time Limit**
- Code: `autonomous_learner.py:55-56`
- Formula:
  ```python
  start_time = time.time()
  end_time = start_time + (duration_minutes * 60)
  ```
- Initialize counters: `learned_count = 0`, `processed_count = 0`

**Step 3: Learning Loop (While Time Remains)**
- Code: `autonomous_learner.py:61`
- Condition: `while time.time() < end_time`
- Loop continues until time expires

**Step 3a: Select Random Explanation**
- Code: `autonomous_learner.py:63`
- Logic: `random.choice(explanations)`
- Ensures variety in learning material

**Step 3b: Capture Initial State**
- Code: `autonomous_learner.py:68`
- Data Read: `len(self.symbolic_node.vector_symbols.symbols)`
- Purpose: Track if new symbols are learned

**Step 3c: Process Explanation (CORE LEARNING)**
- Code: `autonomous_learner.py:71-73`
- → Calls: `self.symbolic_node.evaluate_chunk_symbolically(explanation, config)`
- Config: `{'symbolic_node_access_max_phase': 1}`
- **This triggers symbol discovery and learning within SymbolicNode**
- Returns: Symbolic score (0.0-1.0)

**Step 3d: Check Learning Outcome**
- Code: `autonomous_learner.py:76-79`
- Logic:
  ```python
  new_symbols = len(self.symbolic_node.vector_symbols.symbols)
  if new_symbols > initial_symbols:
      learned_count += new_symbols - initial_symbols
      print("🎉 Learned {count} new symbols!")
  ```
- Tracks successful learning events

**Step 3e: Brief Pause**
- Code: `autonomous_learner.py:85`
- Duration: `time.sleep(1)` - 1 second between explanations
- Purpose: Prevent system overload, allow processing time

**Step 4: Session Complete**
- Code: `autonomous_learner.py:87-90`
- Increment: `self.learning_sessions += 1`
- Report:
  - Total explanations processed
  - Total new symbols learned
- Return: `(learned_count, processed_count)`

### ALTERNATIVE: Organic Exploration Mode

**Entry Point:** `organic_exploration(starting_urls=None)`
**Location:** `run_learning_with_requests.py:74`

**Algorithm:**

**Step 1: Choose Starting Point**
- Code: `run_learning_with_requests.py:80-89`
- If no URLs provided: Select random Wikipedia page
- Default options:
  ```python
  ["Special:Random", "Artificial_intelligence", "Consciousness", 
   "Philosophy", "Science"]
  ```

**Step 2: Exploration Loop (10-50 Links)**
- Code: `run_learning_with_requests.py:93`
- Condition: `should_continue_exploring(links_processed)`
- Logic at line 63-72:
  ```python
  if links_processed < 10: return True  # Always continue
  elif links_processed >= 50: return False  # Hard stop
  else:
      # Diminishing interest: 10-50 range
      continue_probability = max(0.1, 1.0 - (links_processed - 10) / 40)
      return random.random() < continue_probability
  ```
- **Curiosity-driven stopping**: Probability decreases with each link

**Step 3: Process Each Link**
- Code: `run_learning_with_requests.py:94-131`
- Pop link from queue: `links_to_explore.pop(0)`
- Set current context: `self.exploration_state['current_url'] = current_url`

**Step 3a: Read Content** (Simulated in current implementation)
- Code: `run_learning_with_requests.py:102-103`
- Placeholder for actual content processing
- Would call learner processing methods

**Step 3b: Detect "Wow" Moments**
- Code: `run_learning_with_requests.py:106-114`
- Probability: 30% chance (`random.random() > 0.7`)
- Action: Log desire via `log_desire(url, desire_text)`
- Example desires:
  ```python
  "I wish I could write content this clearly"
  "I wish I could understand this topic deeper"
  ```

**Step 3c: Find Related Links**
- Code: `run_learning_with_requests.py:117-124`
- Probability: 50% chance of finding interesting links
- Add 1-3 new links to exploration queue
- This creates organic branching behavior

**Step 3d: Update State**
- Code: `run_learning_with_requests.py:126-127`
- Increment: `exploration_state['links_processed']`
- Track: Append URL to `interests_followed` list

**Step 4: Save Exploration State**
- Code: `run_learning_with_requests.py:39-61`
- → Calls: `log_desire(content, desire_text)` throughout
- File: Writes to `data/requests.json`
- Format:
  ```json
  {
    "timestamp": "2025-11-20T10:00:00Z",
    "content_source": "https://...",
    "desire": "I wish I could...",
    "emotional_context": "curiosity_driven",
    "links_processed_so_far": 15
  }
  ```

### Example with REAL Data:

**Input:**
```python
learner = AutonomousLearner()
learner.run_learning_session(duration_minutes=1)
```

**Execution Trace:**

1. Generate 28 symbol explanations
2. Set time limit: `start = 1732108800`, `end = 1732108860` (60 seconds)
3. Loop iteration 1:
   - Select: "The factorial symbol (!) represents..."
   - Initial symbols: 50
   - Process via `evaluate_chunk_symbolically()` → score = 0.73
   - New symbols: 51 (learned "factorial")
   - Print: "🎉 Learned 1 new symbols!"
   - Sleep 1 second
4. Loop iteration 2:
   - Select: "The alpha symbol (α) represents..."
   - Initial symbols: 51
   - Process → score = 0.68
   - New symbols: 52 (learned "alpha")
   - Sleep 1 second
5. ... (continues for ~60 iterations in 60 seconds)
6. Time expires: `time.time() >= 1732108860`
7. Report:
   - Processed: 58 explanations
   - Learned: 15 new symbols
8. Return: `(15, 58)`

**Output:**
```
✅ Learning session 1 complete!
   Processed: 58 explanations
   Learned: 15 new symbols
```

### Key Characteristics:

1. **Time-Bounded**: Runs for specified duration, not fixed iterations
2. **Random Sampling**: Ensures diverse exposure to concepts
3. **Incremental Learning**: Tracks learning progress in real-time
4. **Organic Exploration**: Can follow curiosity with diminishing interest curve
5. **Self-Reflection**: Logs desires and "wow" moments for meta-learning

### Performance Notes:

- Simple mode: ~1 explanation/second (with 1s sleep)
- Organic mode: 10-50 links per session
- Learning rate: Varies by content complexity
- Session tracking: Cumulative across multiple runs



---

## 3. MEMORY CONSOLIDATION: Storage and Classification

### File(s):
- `unified_memory.py` (storage)
- `processing_nodes.py` (routing)

### Entry Point:
**Function:** `store(item, decision_type, weights=None)`
**Location:** `unified_memory.py:237` (HistoryAwareMemory class)

### Inputs:
- `item` (dict) - Memory item with text, metadata, scores
- `decision_type` (str) - One of: "FOLLOW_LOGIC", "FOLLOW_SYMBOLIC", "FOLLOW_HYBRID"
- `weights` (dict, optional) - Adaptive weight information

### Outputs:
- No return value (void function)
- Side effect: Appends to appropriate memory list
- Side effect: Updates `item['decision_history']`
- Side effect: Atomic save to JSON files

### Algorithm (Step-by-Step):

**Step 1: Acquire Thread Lock**
- Code: `unified_memory.py:241`
- Logic: `acquired = self.lock.acquire(timeout=5.0)`
- Purpose: Prevent race conditions in concurrent access
- Timeout: 5 seconds before giving up
- If timeout: Print warning and skip storage (line 244-245)

**Step 2: Initialize Decision History**
- Code: `unified_memory.py:248-250`
- Logic:
  ```python
  if 'decision_history' not in item:
      item['decision_history'] = []
  ```
- Creates tracking array if first time storing this item

**Step 3: Create History Entry**
- Code: `unified_memory.py:252-257`
- Data Structure:
  ```python
  history_entry = {
      'decision': decision_type,              # FOLLOW_LOGIC/SYMBOLIC/HYBRID
      'timestamp': datetime.utcnow().isoformat(),
      'weights': weights or self._get_current_weights()
  }
  ```
- Default weights: `{'static': 0.6, 'dynamic': 0.4}` (line 277-280)

**Step 4: Append and Trim History**
- Code: `unified_memory.py:259-261`
- Logic:
  ```python
  item['decision_history'].append(history_entry)
  item['decision_history'] = item['decision_history'][-self.max_history_length:]
  ```
- Default `max_history_length`: 5 (line 233)
- Keeps only most recent 5 decisions to prevent unbounded growth

**Step 5: Update Metadata**
- Code: `unified_memory.py:263-265`
- Fields added:
  ```python
  item['last_decision'] = decision_type
  item['history_length'] = len(item['decision_history'])
  ```

**Step 6: Route to Appropriate Memory** (Parent class method)
- Code: `unified_memory.py:268` → calls `super().store(item, decision_type)`
- → Calls: Parent `TripartiteMemory.store()` at line 95

**Step 6a: Add Storage Metadata**
- Code: `unified_memory.py:98-100`
- Fields:
  ```python
  item['stored_at'] = datetime.utcnow().isoformat()
  item['decision_type'] = decision_type
  ```

**Step 6b: Select Target Memory**
- Code: `unified_memory.py:103-109`
- Logic:
  ```python
  if decision_type == "FOLLOW_LOGIC":
      target_memory = self.logic_memory
  elif decision_type == "FOLLOW_SYMBOLIC":
      target_memory = self.symbolic_memory
  else:  # FOLLOW_HYBRID
      target_memory = self.bridge_memory
  ```

**Step 6c: Check for Duplicates**
- Code: `unified_memory.py:111-121`
- Logic: Linear search through `target_memory` for matching text
- If found:
  - Update `existing_item['last_updated']`
  - Update `existing_item['decision_type']`
  - Merge decision histories
  - **Return early** (no new item created)

**Step 6d: Append New Item**
- Code: `unified_memory.py:123-129`
- Action: `target_memory.append(item)`
- No duplicate found, so create new memory entry

**Step 7: Release Lock**
- Code: `unified_memory.py:272-273`
- Action: `self.lock.release()`
- Ensures lock is released even if exception occurs (finally block)

**Step 8: Periodic Save (Atomic)**
- Triggered separately via `save_all()` method
- Code: `unified_memory.py:131-142`
- → Calls: `_save_safe(filename, data)` for each memory type (line 144-170)

**Step 8a: Atomic Write Pattern**
- Code: `unified_memory.py:151-160`
- Algorithm:
  1. Write to `.tmp` file first
  2. Create `.backup` of existing file
  3. Atomic rename: `.tmp` → primary file
  4. This ensures no corruption if write fails mid-operation

### BRIDGE RESOLUTION: How Hybrid Content Is Handled

**Entry Point:** Item classified as "FOLLOW_HYBRID"
**Ratio Trigger:** `0.67 <= ratio <= 1.5` (from unified_weight_system.py)

**Resolution Algorithm:**

**Step 1: Detect Ambiguity**
- Code: `unified_weight_system.py:376-383`
- Formula:
  ```python
  ratio = scaled_logic / scaled_symbolic
  if 0.67 <= ratio <= 1.5:
      return 'FOLLOW_HYBRID'
  ```
- Content scores BOTH high on logic AND symbolic

**Step 2: Route to Bridge Memory (Temporary Staging)**
- Code: `unified_memory.py:128-129`
- Action: Append to `self.bridge_memory`
- File: Saves to `data/bridge_memory.json`
- **Design Intent:** Temporary staging until context accumulates for proper classification

**Step 3: Mark as Hybrid**
- Metadata added:
  ```python
  item['decision_type'] = 'FOLLOW_HYBRID'
  item['logic_focused'] = False  # Not purely logical
  item['symbolic_focused'] = False  # Not purely symbolic
  item['hybrid'] = True  # Explicitly marked
  ```

**Step 4: Track Classification Changes**
- If item was previously LOGIC or SYMBOLIC:
- Decision history shows the transition:
  ```python
  decision_history = [
      {'decision': 'FOLLOW_LOGIC', 'timestamp': 'T1'},
      {'decision': 'FOLLOW_HYBRID', 'timestamp': 'T2'}  # Reclassified
  ]
  ```

**Step 5: Intended Reclassification (NOT YET IMPLEMENTED)**
- **Design Intent:** Bridge memory is TEMPORARY staging for ambiguous content
- **Intended Behavior:** Items should move to logic/symbolic once sufficient related context accumulates
- **Current Reality:** ⚠️ Reclassification algorithm NOT YET IMPLEMENTED - items stay permanently (technical debt)
- **Mature System Goal:** Bridge should contain 0-10 items max (only genuinely niche ambiguous topics)
- **Missing Implementation:**
  - Context accumulation tracking
  - Periodic reclassification checks
  - Automatic promotion to logic or symbolic when ratio shifts outside 0.67-1.5

### Example with REAL Data:

**Input:**
```python
item = {
    'id': 'logic_1732108923456',
    'text': 'The feeling of understanding emerges when logical patterns align with intuitive recognition',
    'logic_score': 0.68,
    'symbolic_score': 0.72,
    'logic_scaled': 0.68 * 1.2 = 0.816,
    'symbolic_scaled': 0.72 * 1.1 = 0.792
}

ratio = 0.816 / 0.792 = 1.03  # Falls in hybrid range [0.67, 1.5]
decision_type = "FOLLOW_HYBRID"
```

**Execution Trace:**

1. Acquire lock → Success
2. Initialize decision_history (first storage)
3. Create history entry:
   ```python
   {
       'decision': 'FOLLOW_HYBRID',
       'timestamp': '2025-11-20T15:30:00.123456Z',
       'weights': {'static': 0.6, 'dynamic': 0.4}
   }
   ```
4. Append history, trim to last 5
5. Update metadata:
   ```python
   item['last_decision'] = 'FOLLOW_HYBRID'
   item['history_length'] = 1
   ```
6. Call parent store()
7. Add storage metadata:
   ```python
   item['stored_at'] = '2025-11-20T15:30:00.123456Z'
   item['decision_type'] = 'FOLLOW_HYBRID'
   ```
8. Select target: `target_memory = self.bridge_memory`
9. Check duplicates: No match found (new content)
10. Append to bridge_memory: `self.bridge_memory.append(item)`
11. Release lock
12. Memory state:
    - logic_memory: 42 items
    - symbolic_memory: 38 items
    - bridge_memory: 15 items (now includes this item)

**Output in bridge_memory.json:**
```json
[
  {
    "id": "logic_1732108923456",
    "text": "The feeling of understanding emerges when...",
    "decision_type": "FOLLOW_HYBRID",
    "stored_at": "2025-11-20T15:30:00.123456Z",
    "last_decision": "FOLLOW_HYBRID",
    "history_length": 1,
    "decision_history": [
      {
        "decision": "FOLLOW_HYBRID",
        "timestamp": "2025-11-20T15:30:00.123456Z",
        "weights": {"static": 0.6, "dynamic": 0.4}
      }
    ],
    "logic_score": 0.68,
    "symbolic_score": 0.72
  }
]
```

### Key Characteristics:

1. **Thread-Safe**: Lock prevents concurrent modification corruption
2. **Atomic Writes**: Temp file + atomic rename ensures no data loss
3. **Duplicate Prevention**: Text-based deduplication
4. **History Tracking**: Maintains classification history for analysis
5. **Backup Recovery**: `.backup` files enable recovery from corruption
6. **Bridge = Permanent**: Hybrid content stays in bridge, no auto-resolution



---

## 4. SYMBOL LEARNING: How New Symbols Get Added

### File(s):
- `unified_memory.py` (SymbolMemory class)
- `processing_nodes.py` (symbol discovery triggers)

### Entry Point:
**Function:** `add_symbol(symbol_token, name, keywords, initial_emotions, example_text, ...)`
**Location:** `unified_memory.py:470`

### Inputs:
- `symbol_token` (str) - The emoji or symbol character (e.g., "❤️", "🔥")
- `name` (str) - Human-readable name (e.g., "heart", "fire")
- `keywords` (list) - Associated keywords for matching
- `initial_emotions` (dict) - Emotional weights, e.g., `{"love": 0.9, "warmth": 0.7}`
- `example_text` (str) - Context where symbol was discovered
- `origin` (str) - Source: "emergent", "seed", "generated", "user_quarantine"
- `learning_phase` (int) - Which learning phase discovered this (default: 0)
- `resonance_weight` (float) - Importance weight 0.0-1.0 (default: 0.5)
- `skip_quarantine_check` (bool) - Bypass security (default: False)

### Outputs:
- Returns: `symbol_data` dict if successful, `None` if quarantined
- Side effect: Updates `data/symbol_memory.json`
- Side effect: May quarantine malicious symbols

### Algorithm (Step-by-Step):

**Step 1: Security Check (Quarantine Filter)**
- Code: `unified_memory.py:476-490`
- → Calls: `_check_quarantine_status(origin, example_text, name, keywords)` at line 424-443
- Skip if: `skip_quarantine_check == True`

**Step 1a: Check Origin**
- Code: `unified_memory.py:427-433`
- Quarantine origins:
  ```python
  quarantine_origins = [
      "user_quarantine", "quarantined_input", "warfare_detected",
      "manipulation_attempt", "unverified_user"
  ]
  ```
- If origin matches: Return `(True, {"reason": f"Quarantine origin: {origin}"})`

**Step 1b: Linguistic Warfare Detection**
- Code: `unified_memory.py:436-441`
- If `warfare_detector` available:
  - Concatenate: `analysis_text = f"{name} {keywords} {example_text}"`
  - → Calls: `warfare_detector.analyze_text_for_warfare(analysis_text, user_id)`
  - Threshold: `threat_score > 0.7`
  - If detected: Return `(True, analysis)` with threat details

**Step 1c: Handle Quarantine**
- Code: `unified_memory.py:481-490`
- If `should_quarantine == True`:
  - Print: `"🔒 Symbol '{symbol}' ({name}) blocked - origin: {origin}"`
  - → Calls: `quarantine.quarantine_user_input()` with symbol details
  - **Return None** (symbol NOT added)

**Step 2: Load Existing Symbol Memory**
- Code: `unified_memory.py:492`
- → Calls: `load_symbol_memory()` at line 399
- Returns: Dict of existing symbols `{token: symbol_data}`

**Step 3: Extract Emotional Weights**
- Code: `unified_memory.py:494-513`
- Purpose: Normalize emotions from various input formats

**Step 3a: Dict Format**
- Code: `unified_memory.py:498-502`
- Input: `{"love": 0.9, "joy": 0.7}`
- Logic:
  ```python
  for emo, score in initial_emotions.items():
      if isinstance(score, (int, float)):
          incoming_numeric_weights.append(score)
          peak_emotions_from_initial[emo] = score
  ```

**Step 3b: List Format**
- Code: `unified_memory.py:503-511`
- Input: `[{"emotion": "love", "weight": 0.9}, ...]` OR `[("love", 0.9), ...]`
- Extracts weights from both dict and tuple formats

**Step 3c: Calculate Peak Weight**
- Code: `unified_memory.py:513`
- Formula: `max(incoming_numeric_weights, default=0.0)`
- Purpose: Track strongest emotional association

**Step 4: Check if New or Existing Symbol**
- Code: `unified_memory.py:515`
- Condition: `if symbol_token not in memory`

**Step 4a: CREATE NEW SYMBOL**
- Code: `unified_memory.py:516-543`
- Data Structure:
  ```python
  new_symbol_data = {
      "name": name,
      "keywords": list(set(keywords)),  # Remove duplicates
      "core_meanings": [],              # Empty, will be populated with use
      "emotions": initial_emotions,     # Original emotion dict
      "emotion_profile": {},            # Empty, will be learned
      "vector_examples": [],            # Empty, will collect examples
      "origin": origin,                 # Where discovered
      "learning_phase": learning_phase,  # Which phase
      "resonance_weight": resonance_weight,
      "golden_memory": {
          "peak_weight": current_max_incoming_weight,
          "context": example_text or "",
          "peak_emotions": peak_emotions_from_initial,
          "timestamp": datetime.utcnow().isoformat()
      },
      "created_at": datetime.utcnow().isoformat(),
      "updated_at": datetime.utcnow().isoformat(),
      "usage_count": 0,
      "visualization_metadata": {
          "primary_color": self._get_symbol_color(initial_emotions),
          "display_priority": self._calculate_display_priority(resonance_weight, origin),
          "classification_hint": self._get_classification_hint(keywords, initial_emotions)
      }
  }
  ```

**Step 4a-i: Determine Symbol Color**
- Code: `unified_memory.py:537` → calls `_get_symbol_color()` at line 552
- Logic at line 559-561:
  ```python
  dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
  return emotion_colors.get(dominant_emotion.lower(), "#808080")
  ```
- Emotion color map:
  ```python
  {
      "joy": "#FFD700" (gold), "love": "#FF69B4" (pink), 
      "anger": "#DC143C" (red), "fear": "#4B0082" (indigo),
      "sadness": "#4682B4" (blue), "surprise": "#FF8C00" (orange),
      "trust": "#87CEEB" (sky blue), "neutral": "#C0C0C0" (silver)
  }
  ```

**Step 4a-ii: Calculate Display Priority**
- Code: `unified_memory.py:538` → calls `_calculate_display_priority()` at line 565
- Origin boosts (line 567-569):
  ```python
  origin_boosts = {
      "seed": 0.3,           # Foundational symbols get priority
      "meta_emergent": 0.2,  # AI-generated symbols
      "generated": 0.1,      # Standard generation
      "user_quarantine": -0.5  # Suspicious symbols downranked
  }
  ```
- Formula: `priority = resonance_weight + origin_boosts.get(origin, 0.0)`

**Step 4a-iii: Sanitize Data**
- Code: `unified_memory.py:543` → calls `_sanitize_symbol_data()` at line 445
- Security measures (line 447-467):
  - Truncate long fields: `name[:100]`, `keywords[:50]`, etc.
  - Limit keyword count to 20
  - Remove script injection: `<script>`, `javascript:`, `onerror=`, etc.
  - Clean all text fields for XSS prevention

**Step 4a-iv: Store New Symbol**
- Code: `unified_memory.py:543`
- Action: `memory[symbol_token] = sanitized_data`

**Step 4b: UPDATE EXISTING SYMBOL**
- Code: `unified_memory.py:544-548`
- Updates:
  ```python
  memory[symbol_token]["updated_at"] = datetime.utcnow().isoformat()
  memory[symbol_token]["usage_count"] += 1
  ```
- Note: Does NOT overwrite emotional data, keywords, or golden memory
- Only increments usage counter and updates timestamp

**Step 5: Save to Disk**
- Code: `unified_memory.py:549`
- → Calls: `save_symbol_memory(memory)` at line 419
- File: Writes to `data/symbol_memory.json`
- Format: Atomic write (not shown, but follows standard JSON dump)

**Step 6: Return Symbol Data**
- Code: `unified_memory.py:550`
- Returns: `memory[symbol_token]`
- Caller can verify symbol was added successfully

### Example with REAL Data:

**Input:**
```python
# Discovered heart emoji in text: "I love learning about AI ❤️"
add_symbol(
    symbol_token="❤️",
    name="heart",
    keywords=["love", "affection", "care", "warmth"],
    initial_emotions={"love": 0.9, "joy": 0.7, "warmth": 0.6},
    example_text="I love learning about AI",
    origin="emergent",
    learning_phase=1,
    resonance_weight=0.75
)
```

**Execution Trace:**

1. Security check:
   - Origin: "emergent" (not in quarantine list) ✓
   - Warfare check: "heart love affection care warmth I love learning" → threat_score = 0.15 ✓
   - Pass security checks
2. Load existing symbols: 127 symbols in memory
3. Extract emotions:
   - `incoming_numeric_weights = [0.9, 0.7, 0.6]`
   - `peak_emotions = {"love": 0.9, "joy": 0.7, "warmth": 0.6}`
   - `current_max_incoming_weight = 0.9`
4. Check if exists: "❤️" NOT in memory (new symbol)
5. Create new symbol:
   - Name: "heart"
   - Keywords: ["love", "affection", "care", "warmth"]
   - Golden memory: {"peak_weight": 0.9, "context": "I love learning about AI"}
   - Color: Dominant emotion "love" (0.9) → "#FF69B4" (pink)
   - Priority: 0.75 (resonance) + 0.0 (emergent) = 0.75
   - Usage count: 0
6. Sanitize: Check for injection attacks → Clean
7. Store: `memory["❤️"] = new_symbol_data`
8. Save to disk: Write to symbol_memory.json
9. Return: Symbol data dict

**Output in symbol_memory.json:**
```json
{
  "❤️": {
    "name": "heart",
    "keywords": ["love", "affection", "care", "warmth"],
    "core_meanings": [],
    "emotions": {"love": 0.9, "joy": 0.7, "warmth": 0.6},
    "emotion_profile": {},
    "vector_examples": [],
    "origin": "emergent",
    "learning_phase": 1,
    "resonance_weight": 0.75,
    "golden_memory": {
      "peak_weight": 0.9,
      "context": "I love learning about AI",
      "peak_emotions": {"love": 0.9, "joy": 0.7, "warmth": 0.6},
      "timestamp": "2025-11-20T15:45:00.123Z"
    },
    "created_at": "2025-11-20T15:45:00.123Z",
    "updated_at": "2025-11-20T15:45:00.123Z",
    "usage_count": 0,
    "visualization_metadata": {
      "primary_color": "#FF69B4",
      "display_priority": 0.75,
      "classification_hint": "emotional_symbolic"
    }
  }
}
```

### Symbol Discovery Triggers:

Symbols are discovered automatically during content processing in `processing_nodes.py`:

**Trigger 1: New Symbol Detection** (line 533)
- Occurs when: Emoji found in text that's not in symbol_memory
- Context: While processing symbolic content
- Action: Calls `unified_memory.add_symbol()` with discovered emoji

**Trigger 2: Symbol Occurrence Logging** (line 555)
- Occurs when: Known symbol is encountered again
- Context: Symbol matching during symbolic evaluation
- Action: Calls `unified_memory.add_symbol_occurrence()` to track usage

**Trigger 3: Meta-Emergent Symbols** (line 639)
- Occurs when: AI generates new symbolic associations
- Context: Meta-level symbolic reasoning
- Action: Creates symbol with origin="meta_emergent"

### Key Characteristics:

1. **Security-First**: Quarantine checks prevent malicious symbols
2. **Emotional Anchoring**: Every symbol has peak emotional context
3. **Golden Memory**: Preserves the most significant usage context
4. **Incremental Learning**: Usage count and updates track symbol evolution
5. **Visualization Ready**: Color and priority metadata for UI display
6. **XSS Prevention**: Sanitizes all text to prevent injection attacks
7. **Deduplication**: Only one entry per symbol token


