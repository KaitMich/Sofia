# Adaptive Memory Migration — Design Document
## Blueprint for Section 4 Implementation
### Created: March 27, 2026 — Pending Design Review Before Any Code Is Written

---

## 1. Architecture Overview

All new content enters bridge memory. There is no classification at the point of entry. The intake classifier still runs, but its output is stored as metadata on the item — a note, not an order. The item stays in bridge until the cosine math resolves naturally.

Migration out of bridge happens when an item's cosine similarity to an existing cluster in logic or symbolic memory reaches sufficient gravity. "Sufficient gravity" is not a hardcoded number — it's derived from the cluster's own coherence, which changes as Sofia learns.

Items already in logic or symbolic are also subject to recontextualization. When new learning shifts the embedding landscape enough that an old item's relationship to its cluster has destabilized, that item migrates back to bridge for re-evaluation.

The timing of all checks is driven by meaningful signals (centroid drift), not by calendars, counters, or schedules.

```
Content → Bridge (always, with classifier metadata)
    ↓
Centroid drift detected → Full bridge scan against updated landscape
    ↓
Item similarity ≥ cluster coherence threshold → Migrate to logic or symbolic
    ↓
Item similarity < threshold → Stays in bridge (checked again on next drift trigger)
    ↓
Existing logic/symbolic items → Sampled for coherence drift → Flagged items reverse migrate to bridge
```

---

## 2. Algorithms in Pseudocode

### 2a. Bridge-First Intake

```
FUNCTION store_new_content(text, source_url, ...):

    # Run classifier but store result as metadata, not routing
    logic_score = compute_logic_score(text)
    symbolic_score = compute_symbolic_score(text)
    classifier_suggestion = classify(logic_score, symbolic_score)

    # Compute embedding immediately (needed for migration checks)
    embedding = fuse_vectors(text)

    item = {
        text: text,
        source_url: source_url,
        embedding: embedding,
        initial_impression: {
            logic_score: logic_score,
            symbolic_score: symbolic_score,
            classifier_suggestion: classifier_suggestion
        },
        stored_at: now(),
        decision_type: "FOLLOW_HYBRID"  # Bridge — always
    }

    bridge_memory.append(item)

    # Update cluster centroids with new item's influence
    update_centroid_tracking(embedding)

    # Check if centroid drift exceeds trigger threshold
    IF centroid_drift_exceeded():
        run_bridge_migration_scan()
```

### 2b. Adaptive Threshold — Cluster Coherence Score

```
FUNCTION compute_cluster_coherence(memory_store):
    """
    Derive the migration threshold from the actual knowledge landscape.
    Returns the mean intra-cluster similarity, weighted by cluster size.
    """

    embeddings = [item.embedding for item in memory_store if item.embedding is not None]
    n = len(embeddings)

    IF n < 3:
        RETURN 0.0  # Statistical minimum not met — nothing migrates

    # Sample pairs to compute mean similarity
    # Sample size scales with store size but caps for performance
    sample_size = min(n, max(50, n // 10))
    sample_indices = random_sample(range(n), sample_size)

    similarities = []
    FOR each pair (i, j) in combinations(sample_indices, 2):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        similarities.append(sim)

    mean_similarity = mean(similarities)
    std_similarity = std(similarities)

    # Density factor: larger clusters have more confident thresholds
    # This doesn't change the threshold value — it changes our confidence
    # in that value, which affects how we handle borderline cases
    density_confidence = min(1.0, n / 20)  # Full confidence at 20+ members

    RETURN {
        threshold: mean_similarity,
        std: std_similarity,
        density_confidence: density_confidence,
        sample_size: sample_size,
        store_size: n
    }
```

### 2c. Centroid Tracking and Drift Trigger

```
STATE:
    logic_centroid = running_mean(all logic item embeddings)
    symbolic_centroid = running_mean(all symbolic item embeddings)
    logic_centroid_at_last_check = logic_centroid
    symbolic_centroid_at_last_check = symbolic_centroid
    logic_std = running_std(logic item similarities)
    symbolic_std = running_std(symbolic item similarities)

FUNCTION update_centroid_tracking(new_embedding):
    """
    Called after every new item enters bridge.
    Centroids don't change (item is in bridge), but we track
    what the centroid WOULD be if this item were added.

    Actually — centroids change when items MIGRATE into the store,
    not when new items enter bridge. So this is called after migration.
    """
    # Recalculate centroid as incremental running average
    # centroid = (centroid * n + new_embedding) / (n + 1)
    PASS

FUNCTION centroid_drift_exceeded():
    """
    Check if either cluster centroid has shifted significantly
    since the last bridge scan was run.
    """
    logic_drift = cosine_distance(logic_centroid, logic_centroid_at_last_check)
    symbolic_drift = cosine_distance(symbolic_centroid, symbolic_centroid_at_last_check)

    # Drift threshold is the cluster's own standard deviation
    # A shift of more than 1 std is meaningful
    logic_trigger = logic_drift > logic_std
    symbolic_trigger = symbolic_drift > symbolic_std

    RETURN logic_trigger OR symbolic_trigger
```

**Key insight:** The drift trigger itself is adaptive. A tight cluster (low std) triggers on small shifts. A loose cluster (high std) only triggers on large shifts. The system self-calibrates.

### 2d. Bridge Migration Scan

```
FUNCTION run_bridge_migration_scan():
    """
    Scan all bridge items against current cluster landscape.
    Called when centroid drift exceeds trigger threshold.
    """

    logic_coherence = compute_cluster_coherence(logic_memory)
    symbolic_coherence = compute_cluster_coherence(symbolic_memory)

    logic_centroid = compute_centroid(logic_memory)
    symbolic_centroid = compute_centroid(symbolic_memory)

    items_to_migrate = []

    FOR each item in bridge_memory:
        embedding = item.embedding  # Cached from intake

        # Compute similarity to each cluster centroid
        logic_sim = cosine_similarity(embedding, logic_centroid)
        symbolic_sim = cosine_similarity(embedding, symbolic_centroid)

        # Check against adaptive thresholds
        logic_qualifies = (
            logic_sim >= logic_coherence.threshold
            AND logic_coherence.store_size >= 3  # Statistical minimum
        )
        symbolic_qualifies = (
            symbolic_sim >= symbolic_coherence.threshold
            AND symbolic_coherence.store_size >= 3
        )

        IF logic_qualifies AND symbolic_qualifies:
            # Both clusters claim it — goes to whichever has stronger pull
            IF logic_sim > symbolic_sim:
                target = "logic"
            ELSE:
                target = "symbolic"
            items_to_migrate.append((item, target, max(logic_sim, symbolic_sim)))

        ELSE IF logic_qualifies:
            items_to_migrate.append((item, "logic", logic_sim))

        ELSE IF symbolic_qualifies:
            items_to_migrate.append((item, "symbolic", symbolic_sim))

        ELSE:
            # Stays in bridge — doesn't meet any cluster's coherence threshold
            PASS

    # Execute migrations
    FOR each (item, target, similarity) in items_to_migrate:
        migrate_item(item, from="bridge", to=target)
        log_migration(item, target, similarity, reason="adaptive_gravity")

    # Update centroid tracking (centroids changed due to migrations)
    update_all_centroids()
    logic_centroid_at_last_check = logic_centroid
    symbolic_centroid_at_last_check = symbolic_centroid

    RETURN migration_results
```

### 2e. Recontextualization Trigger — Reverse Migration

```
FUNCTION check_recontextualization(recently_learned_embeddings):
    """
    After each learning session, check if existing logic/symbolic items
    have been recontextualized by new learning.
    Called with embeddings of everything learned this session.
    """

    logic_coherence = compute_cluster_coherence(logic_memory)
    symbolic_coherence = compute_cluster_coherence(symbolic_memory)

    logic_centroid = compute_centroid(logic_memory)
    symbolic_centroid = compute_centroid(symbolic_memory)

    items_to_reverse = []

    # WEIGHTED SAMPLING: prioritize items near what was just learned
    # Compute similarity of each existing item to session centroid
    session_centroid = mean(recently_learned_embeddings)

    # Score all items by relevance to this session
    all_items = logic_memory + symbolic_memory
    relevance_scores = []
    FOR each item in all_items:
        relevance = cosine_similarity(item.embedding, session_centroid)
        relevance_scores.append((item, relevance))

    # Sort by relevance — most relevant to this session checked first
    relevance_scores.sort(by=relevance, descending=True)

    # Check top 10% (most relevant) + 2% random (catch unexpected drift)
    relevant_count = max(10, len(all_items) // 10)
    random_count = max(5, len(all_items) // 50)

    items_to_check = relevance_scores[:relevant_count]
    remaining = relevance_scores[relevant_count:]
    IF remaining:
        items_to_check += random_sample(remaining, min(random_count, len(remaining)))

    FOR each (item, relevance) in items_to_check:
        # Determine which cluster this item belongs to
        IF item in logic_memory:
            cluster_centroid = logic_centroid
            cluster_coherence = logic_coherence
        ELSE:
            cluster_centroid = symbolic_centroid
            cluster_coherence = symbolic_coherence

        # Check if item still belongs in its cluster
        current_similarity = cosine_similarity(item.embedding, cluster_centroid)

        # Drift threshold is adaptive: derived from the cluster's own std
        # An item has significantly drifted if its similarity dropped below
        # the cluster mean minus one standard deviation
        drift_threshold = cluster_coherence.threshold - cluster_coherence.std

        IF current_similarity < drift_threshold:
            items_to_reverse.append(item)

    # Reverse migrate flagged items back to bridge
    FOR each item in items_to_reverse:
        reverse_migrate(item, to="bridge", reason="recontextualization")
        log_reverse_migration(item, reason="cluster_coherence_drift")

    RETURN items_to_reverse
```

**Why `mean - 1 std` for drift detection:** This is not a hardcoded constant — it's derived from the cluster's own distribution. An item that falls below `mean - 1 std` is, by definition, less similar to its cluster than ~84% of the cluster's members. That's a meaningful statistical signal that the item may no longer belong. As the cluster's coherence changes (tighter clusters have smaller std), the drift threshold automatically adjusts.

---

## 3. What This Replaces

| Current Hardcoded Constant | Location | Adaptive Replacement |
|---|---|---|
| `MIN_AGE_DAYS = 7` | bridge_reclassifier.py:37 | **Removed entirely.** Migration timing is determined by centroid drift triggers. |
| `MIN_RELATED_ITEMS = 5` | bridge_reclassifier.py:38 | **Replaced by statistical minimum of 3 cluster members.** This is a math constant (mean requires ≥3 points), not a learning decision. |
| `DOMINANCE_THRESHOLD = 0.70` | bridge_reclassifier.py:39 | **Replaced by adaptive cluster coherence.** Threshold = mean intra-cluster similarity, which changes as Sofia learns. |
| Keyword overlap for "related items" | bridge_reclassifier.py:72-120 | **Replaced by cosine similarity** using cached 384-dim embeddings from fuse_vectors(). |
| `confidence_threshold = 0.3` | reverse_migration.py:19 | **Replaced by adaptive drift detection** (mean - 1 std of cluster coherence). |
| Stability check (5+ flips) | reverse_migration.py:93-96 | **Replaced by cosine drift.** An item's cluster membership is determined by math, not flip count. |
| `quarantine_confidence = 0.3` | unified_weight_system.py:130 | **Retained for security quarantine only** (external threat detection, not migration). |
| `min_decision_confidence = 0.5` | unified_weight_system.py:131 | **No longer used for routing** (everything goes to bridge). Retained as metadata on the item. |
| Intake routing (FOLLOW_LOGIC/SYMBOLIC/HYBRID) | unified_weight_system.py:334-383, enhanced_autonomous_learner.py:997-1026 | **Classifier output becomes metadata.** All items route to bridge. Migration decides final destination. |
| "Every 10 items" batch cadence | (proposed, not yet in code) | **Centroid drift trigger.** Scan runs when cluster centroid shifts by more than 1 std since last scan. |
| "80% of threshold" for drift detection | (proposed, not yet in code) | **Mean minus 1 std** — derived from cluster distribution, not a hardcoded multiplier. |

---

## 4. Computational Cost Analysis

### Per-Item Costs

| Operation | Cost | When |
|---|---|---|
| Encode text → 384-dim embedding | ~20ms (GPU) / ~50ms (CPU) | Once per item at intake |
| Cosine similarity (1 vs 1) | ~0.01ms | Per comparison |
| Update running centroid | ~0.1ms | After each migration |
| Check centroid drift | ~0.02ms | After each new item |

### Bridge Migration Scan Costs

| Store Size | Bridge Items | Scan Cost | Notes |
|---|---|---|---|
| 1K total (500 logic, 10 symbolic, 490 bridge) | 490 items × 2 centroids | ~10ms | All embeddings cached |
| 10K total (8K logic, 200 symbolic, 1.8K bridge) | 1,800 items × 2 centroids | ~36ms | Negligible |
| 100K total (80K logic, 5K symbolic, 15K bridge) | 15,000 items × 2 centroids | ~300ms | Still under 1 second |

### Cluster Coherence Computation

| Store Size | Sample Pairs | Cost | Notes |
|---|---|---|---|
| 50 items | C(50,2) = 1,225 pairs | ~12ms | Full computation feasible |
| 500 items | 100 sampled → C(100,2) = 4,950 pairs | ~50ms | Sampled |
| 5,000 items | 500 sampled → C(500,2) = 124,750 pairs | ~1.2s | Sampled, could reduce sample |
| 50,000 items | 500 sampled → same | ~1.2s | Sample size caps cost |

### Recontextualization Scan (per session)

| Store Size | Items Checked (10% relevant + 2% random) | Cost | Notes |
|---|---|---|---|
| 1K items | ~120 items | ~2.4ms similarities + relevance scoring ~24ms | Negligible |
| 10K items | ~1,200 items | ~24ms similarities + relevance scoring ~240ms | Under 1 second |
| 100K items | ~12,000 items | ~240ms similarities + relevance scoring ~2.4s | May need tighter sampling |

### Key Insight: Caching Makes This Feasible

The expensive operation is embedding computation (~20ms per item). With embeddings cached on each item at intake, all subsequent operations are cosine similarity computations between 384-dim vectors — effectively free. The entire bridge migration scan at 10K items takes ~36ms. The bottleneck is never the similarity math; it's the one-time embedding computation.

### Memory Cost of Cached Embeddings

- 384 floats × 4 bytes = 1,536 bytes per embedding
- 10K items = ~15 MB
- 100K items = ~150 MB
- Feasible for in-memory operation; can also store in vector memory file

---

## 5. Open Questions

### Q1: Single Centroid vs. Sub-Clusters
The current design uses a single centroid for logic and a single centroid for symbolic. As Sofia's knowledge grows, these stores will contain distinct sub-clusters (atoms vs. algorithms in logic, for example). Should the system detect and track sub-clusters, each with their own centroid and coherence? This matters because a single centroid for a diverse store will have low coherence, making the threshold too easy to meet.

**Proposed resolution:** Start with single centroids. When the intra-cluster std exceeds a certain spread (another adaptive measure — when the store is clearly multi-modal), introduce sub-clustering using k-means or DBSCAN on the embeddings. This is a future enhancement, not a launch requirement.

### Q2: What Happens When Bridge Gets Very Large?
If the adaptive threshold is high (tight clusters) and new content is in unexplored domains, bridge could grow indefinitely. Is this a problem? Under the project philosophy, a large bridge is correct — it means Sofia has a lot of unresolved knowledge. But practically, a bridge of 100K items is expensive to scan.

**Proposed resolution:** Bridge size is a health metric, not a problem to solve. If bridge grows large, it means Sofia's knowledge landscape has large unexplored territories. The system should report this, not suppress it. Scanning cost is managed by cached embeddings.

### Q3: Classifier Metadata — How Much Weight?
The intake classifier's suggestion is stored as metadata. Should the migration system use it at all, or purely rely on cosine similarity? Using it adds a signal. Ignoring it keeps the system purely mathematical.

**Proposed resolution:** The migration system should be purely cosine-based for launch. The classifier metadata is preserved for potential future use (e.g., as a tiebreaker when cosine similarities to both clusters are equal). It carries zero weight in the migration decision.

### Q4: Re-embedding Over Time
As Sofia's understanding deepens, should old items be re-embedded using the same models but with updated context? The embedding of "atom" when she has 100 memories is different from when she has 10,000 memories (in a system with contextual embeddings). However, the current models (MiniLM/E5) are static — they don't learn from Sofia's data.

**Proposed resolution:** Not applicable with current static models. If Sofia ever gets fine-tuned embedding models, this becomes relevant. For now, embeddings are stable and don't need re-computation.

### Q5: Migration History and Explainability
Should each migration be logged with the full context (similarity score, cluster coherence at time of migration, what triggered the scan)? This is essential for the real-time visualization goal mentioned in earlier sessions.

**Proposed resolution:** Yes. Every migration (forward and reverse) should be logged to `data/migration_log.json` with: item_id, from_store, to_store, similarity_score, cluster_coherence_at_time, trigger_reason (centroid_drift/session_end/manual), timestamp. This log is the foundation for future real-time visualization.

---

## 6. Implementation Order

### Phase 1: Embedding Cache (Foundation)
**What:** Add embedding field to all items. Compute and cache embeddings for existing logic/symbolic/bridge items. Add embedding computation to the intake path.
**Why first:** Everything else depends on cached embeddings. Without them, every operation requires expensive re-encoding.
**Estimated scope:** Modify `unified_memory.store()`, add batch embedding script for existing items, add embedding field to item schema.

### Phase 2: Bridge-First Intake
**What:** Change routing so all new content enters bridge. Store classifier output as metadata. Ensure downstream systems handle the change (saturation learner, processing nodes).
**Why second:** This is the architectural shift. Once this is in place, the old routing is gone and migration becomes the only path to logic/symbolic.
**Estimated scope:** Modify `enhanced_autonomous_learner._process_url_in_saturation_mode()`, modify `unified_memory.store()`, modify `processing_nodes.DynamicBridge`.

### Phase 3: Adaptive Threshold and Bridge Migration
**What:** Implement `compute_cluster_coherence()`, `compute_centroid()`, `run_bridge_migration_scan()`. Replace bridge_reclassifier's three gates with cosine-based adaptive migration.
**Why third:** This is the core migration engine. It needs cached embeddings (Phase 1) and bridge-first intake (Phase 2) to be in place.
**Estimated scope:** Rewrite `bridge_reclassifier.py` or create new `adaptive_bridge_migration.py`.

### Phase 4: Centroid Drift Trigger
**What:** Implement running centroid tracking, drift detection, and automatic scan triggering. Replace any fixed cadence with drift-based triggers.
**Why fourth:** The migration scan from Phase 3 can initially be triggered manually or at session end. Making it drift-triggered is an optimization.
**Estimated scope:** Add state tracking to migration module, add drift check to intake path.

### Phase 5: Recontextualization (Reverse Migration)
**What:** Implement weighted sampling of existing items, coherence drift detection (mean - 1 std), and reverse migration back to bridge.
**Why last:** This is the most complex piece and has the highest computational cost. The forward migration (bridge → logic/symbolic) should work before we add reverse migration (logic/symbolic → bridge).
**Estimated scope:** Rewrite `reverse_migration.py` or add to migration module.

---

## 7. Design Principles (Non-Negotiable)

1. **No hardcoded thresholds.** Every number that determines behavior must be derived from Sofia's actual knowledge state.
2. **Statistical minimum (3 members) is acceptable.** This is math, not a decision about Sofia's development.
3. **Timing is signal-driven, not scheduled.** Checks run when the embedding landscape has changed meaningfully, not on a clock or counter.
4. **All migrations are logged.** Every movement between stores is recorded with full context for explainability and future visualization.
5. **Bridge is intake, not failure.** Large bridge counts are healthy in early learning. The system reports bridge size but never treats it as a problem.
6. **The classifier is a note, not an order.** Metadata from the intake classifier carries zero weight in migration decisions for the initial implementation.

---

*This design document is the blueprint for Section 4 implementation. No code should be written until this design is reviewed and approved by the project creator.*
*See docs/SOPHIA_TRUTH_FRAMEWORK.md Correction 12 for the status of this work.*
