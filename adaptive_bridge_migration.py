#!/usr/bin/env python3
"""
Adaptive Bridge Migration — The Core Migration Engine

Implements the adaptive memory migration system described in
docs/ADAPTIVE_MIGRATION_DESIGN.md

Architecture:
- All content enters bridge (bridge-first intake)
- Migration happens when cosine math resolves, not on a schedule
- Thresholds are adaptive (derived from cluster coherence)
- Timing is signal-driven (centroid drift triggers scans)
- Items can reverse-migrate when new learning recontextualizes old knowledge

No hardcoded thresholds. Every number that determines behavior is derived
from Sofia's actual knowledge state.
"""

import json
import random
import itertools
import numpy as np
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine


# ---------------------------------------------------------------------------
# Embedding helpers
# ---------------------------------------------------------------------------

def get_or_compute_embedding(item: Dict, force_recompute: bool = False) -> Optional[np.ndarray]:
    """Get cached embedding or compute and cache it on the item."""
    if not force_recompute and item.get('embedding') is not None:
        return np.array(item['embedding'])

    text = item.get('text', '')
    if not text or len(text.strip()) < 5:
        return None

    try:
        from vector_engine import fuse_vectors
        vec, _ = fuse_vectors(text[:1000])  # Cap at 1000 chars for consistency
        if vec is not None:
            item['embedding'] = vec  # Cache on the item (list of floats)
            return np.array(vec)
    except Exception:
        pass
    return None


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors. Returns 0.0 on error."""
    try:
        if a is None or b is None:
            return 0.0
        return float(sklearn_cosine(a.reshape(1, -1), b.reshape(1, -1))[0][0])
    except Exception:
        return 0.0


# ---------------------------------------------------------------------------
# Cluster Analysis
# ---------------------------------------------------------------------------

class ClusterStats:
    """Statistics about a memory cluster (logic or symbolic store)."""
    def __init__(self, centroid: Optional[np.ndarray], mean_similarity: float,
                 std_similarity: float, size: int, density_confidence: float):
        self.centroid = centroid
        self.mean_similarity = mean_similarity  # Adaptive threshold
        self.std_similarity = std_similarity
        self.size = size
        self.density_confidence = density_confidence  # 0-1, higher = more data

    @property
    def threshold(self) -> float:
        return self.mean_similarity

    @property
    def drift_threshold(self) -> float:
        """Items below this have significantly drifted from cluster."""
        return self.mean_similarity - self.std_similarity


def compute_cluster_stats(items: List[Dict], max_sample: int = 200) -> ClusterStats:
    """
    Compute cluster statistics from a memory store.

    Returns adaptive threshold derived from the actual knowledge landscape:
    - threshold = mean intra-cluster similarity (items must be as similar
      to the cluster as members are to each other)
    - std = spread of similarities (used for drift detection)
    - density_confidence = how confident we are in these stats
    """
    # Gather embeddings
    embeddings = []
    for item in items:
        emb = get_or_compute_embedding(item)
        if emb is not None:
            embeddings.append(emb)

    n = len(embeddings)

    if n < 3:
        # Statistical minimum not met
        return ClusterStats(
            centroid=None, mean_similarity=0.0, std_similarity=0.0,
            size=n, density_confidence=0.0
        )

    # Compute centroid
    centroid = np.mean(embeddings, axis=0)

    # Sample pairs for mean similarity
    sample_size = min(n, max_sample)
    if sample_size < n:
        sample_indices = random.sample(range(n), sample_size)
        sample_embs = [embeddings[i] for i in sample_indices]
    else:
        sample_embs = embeddings

    similarities = []
    pairs = list(itertools.combinations(range(len(sample_embs)), 2))
    # Cap pairs for performance
    if len(pairs) > 5000:
        pairs = random.sample(pairs, 5000)

    for i, j in pairs:
        sim = cosine_sim(sample_embs[i], sample_embs[j])
        similarities.append(sim)

    mean_sim = float(np.mean(similarities)) if similarities else 0.0
    std_sim = float(np.std(similarities)) if similarities else 0.0
    density_confidence = min(1.0, n / 20.0)

    return ClusterStats(
        centroid=centroid,
        mean_similarity=mean_sim,
        std_similarity=std_sim,
        size=n,
        density_confidence=density_confidence
    )


# ---------------------------------------------------------------------------
# Migration Engine
# ---------------------------------------------------------------------------

class AdaptiveMigrationEngine:
    """
    The core adaptive migration engine.

    Handles:
    - Bridge → Logic/Symbolic migration (forward)
    - Logic/Symbolic → Bridge reverse migration (recontextualization)
    - Centroid tracking and drift detection
    - Migration logging
    """

    STATISTICAL_MINIMUM = 3  # Math constant: need ≥3 points for meaningful mean

    def __init__(self, unified_memory, data_dir: str = "data"):
        self.memory = unified_memory
        self.data_dir = Path(data_dir)
        self.log_path = self.data_dir / "migration_log.json"

        # Centroid tracking state
        self._logic_stats: Optional[ClusterStats] = None
        self._symbolic_stats: Optional[ClusterStats] = None
        self._logic_centroid_at_last_scan: Optional[np.ndarray] = None
        self._symbolic_centroid_at_last_scan: Optional[np.ndarray] = None
        self._stats_dirty = True

        # Bootstrap centroid cache (computed once, reused until symbolic has mass)
        self._bootstrap_centroid: Optional[np.ndarray] = None
        self._bootstrap_centroid_computed = False

    def refresh_cluster_stats(self):
        """Recompute cluster statistics for both stores."""
        self._logic_stats = compute_cluster_stats(self.memory.logic_memory)
        self._symbolic_stats = compute_cluster_stats(self.memory.symbolic_memory)
        self._stats_dirty = False

    @property
    def logic_stats(self) -> ClusterStats:
        if self._logic_stats is None or self._stats_dirty:
            self.refresh_cluster_stats()
        return self._logic_stats

    @property
    def symbolic_stats(self) -> ClusterStats:
        if self._symbolic_stats is None or self._stats_dirty:
            self.refresh_cluster_stats()
        return self._symbolic_stats

    # -------------------------------------------------------------------
    # Centroid drift detection
    # -------------------------------------------------------------------

    def centroid_drift_exceeded(self) -> bool:
        """
        Check if either cluster centroid has shifted significantly since
        the last bridge scan. Drift threshold = cluster's own std.
        """
        current_logic = self.logic_stats
        current_symbolic = self.symbolic_stats

        if self._logic_centroid_at_last_scan is None:
            # First check — always trigger
            return True

        logic_drifted = False
        symbolic_drifted = False

        if current_logic.centroid is not None and self._logic_centroid_at_last_scan is not None:
            drift = 1.0 - cosine_sim(current_logic.centroid, self._logic_centroid_at_last_scan)
            if current_logic.std_similarity > 0 and drift > current_logic.std_similarity:
                logic_drifted = True

        if current_symbolic.centroid is not None and self._symbolic_centroid_at_last_scan is not None:
            drift = 1.0 - cosine_sim(current_symbolic.centroid, self._symbolic_centroid_at_last_scan)
            if current_symbolic.std_similarity > 0 and drift > current_symbolic.std_similarity:
                symbolic_drifted = True

        return logic_drifted or symbolic_drifted

    def _snapshot_centroids(self):
        """Save current centroids as the baseline for drift detection."""
        if self.logic_stats.centroid is not None:
            self._logic_centroid_at_last_scan = self.logic_stats.centroid.copy()
        if self.symbolic_stats.centroid is not None:
            self._symbolic_centroid_at_last_scan = self.symbolic_stats.centroid.copy()

    # -------------------------------------------------------------------
    # Bootstrap: cold-start for empty clusters
    # -------------------------------------------------------------------

    def _compute_bootstrap_centroid(self) -> Optional[np.ndarray]:
        """
        Compute a reference centroid for symbolic from the seed symbol vocabulary.

        Used ONLY during cold start (symbolic cluster < STATISTICAL_MINIMUM).
        Once real items populate symbolic memory, this is never called again.

        The centroid is derived from Sofia's own seed symbol keywords — the
        same vocabulary she was initialized with. This is not new content;
        it is a vector computed from content that already exists in the system.
        """
        # Return cached result if already computed
        if self._bootstrap_centroid_computed:
            return self._bootstrap_centroid

        self._bootstrap_centroid_computed = True

        try:
            from vector_engine import embed_text

            # Try both possible locations for seed_symbols.json
            symbols_path = self.data_dir.parent / "seed_symbols.json"
            if not symbols_path.exists():
                symbols_path = self.data_dir / "seed_symbols.json"
            if not symbols_path.exists():
                print("[bootstrap] seed_symbols.json not found — cannot compute bootstrap centroid")
                return None

            with open(symbols_path, 'r', encoding='utf-8') as f:
                seed_symbols = json.load(f)

            embeddings = []
            for sym, info in seed_symbols.items():
                if not isinstance(info, dict):
                    continue
                keywords = info.get('keywords', [])
                archetypes = info.get('archetypes', [])
                core = info.get('core_meanings', [])

                # Build text from keywords + archetypes (short, meaningful)
                parts = keywords + archetypes
                # Include short core_meanings only (skip raw Wikipedia chunks)
                for m in core:
                    if isinstance(m, str) and 10 < len(m) < 100:
                        parts.append(m)

                text = ' '.join(parts)
                if not text.strip():
                    continue

                vec = embed_text(text[:500])
                if vec is not None:
                    embeddings.append(np.array(vec))

            if len(embeddings) >= 3:
                self._bootstrap_centroid = np.mean(embeddings, axis=0)
                print(f"[bootstrap] Computed symbolic reference centroid from {len(embeddings)} seed symbol embeddings")
                return self._bootstrap_centroid
            else:
                print(f"[bootstrap] Only {len(embeddings)} seed symbols embeddable — insufficient for centroid")
                return None

        except Exception as e:
            print(f"[bootstrap] Error computing bootstrap centroid: {e}")
            return None

    # -------------------------------------------------------------------
    # Forward migration: Bridge → Logic/Symbolic
    # -------------------------------------------------------------------

    def run_bridge_migration_scan(self) -> Dict[str, Any]:
        """
        Scan all bridge items against current cluster landscape.
        Migrate items whose cosine similarity to a cluster centroid
        meets or exceeds that cluster's adaptive coherence threshold.

        Bootstrap mode: When symbolic memory has fewer than STATISTICAL_MINIMUM
        items, uses a reference centroid computed from the seed symbol vocabulary
        and comparative routing (symbolic_sim > logic_sim) to seed the first
        items into symbolic. Capped at STATISTICAL_MINIMUM items per scan.
        Once symbolic has enough real items, bootstrap is inert and normal
        centroid-based migration takes over.
        """
        self.refresh_cluster_stats()
        logic_stats = self.logic_stats
        symbolic_stats = self.symbolic_stats

        # Detect bootstrap condition
        bootstrapping = symbolic_stats.size < self.STATISTICAL_MINIMUM
        bootstrap_centroid = None
        if bootstrapping:
            bootstrap_centroid = self._compute_bootstrap_centroid()

        # Pre-scan: compute derived similarity floor for bootstrap.
        # The floor is the mean similarity of all embeddable bridge items to
        # the bootstrap centroid. Items must have above-average symbolic
        # affinity to qualify — not just be far from logic.
        bootstrap_floor = 0.0
        if bootstrapping and bootstrap_centroid is not None:
            bridge_sims = []
            for item in self.memory.bridge_memory:
                emb = get_or_compute_embedding(item)
                if emb is not None:
                    bridge_sims.append(cosine_sim(emb, bootstrap_centroid))
            if bridge_sims:
                bootstrap_floor = float(np.mean(bridge_sims) + np.std(bridge_sims))
                print(f"[bootstrap] Derived similarity floor from {len(bridge_sims)} bridge items: {bootstrap_floor:.4f} (mean+1σ)")

        results = {
            'scanned': 0,
            'migrated_to_logic': 0,
            'migrated_to_symbolic': 0,
            'remained_in_bridge': 0,
            'bootstrap_mode': bootstrapping,
            'bootstrap_centroid_source': 'seed_symbols' if (bootstrapping and bootstrap_centroid is not None) else None,
            'bootstrap_similarity_floor': round(bootstrap_floor, 4) if bootstrapping else None,
            'details': [],
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        items_to_migrate = []

        for item in list(self.memory.bridge_memory):
            results['scanned'] += 1
            embedding = get_or_compute_embedding(item)
            if embedding is None:
                results['remained_in_bridge'] += 1
                continue

            # Compute similarity to each cluster centroid
            logic_sim = 0.0
            symbolic_sim = 0.0

            if logic_stats.centroid is not None and logic_stats.size >= self.STATISTICAL_MINIMUM:
                logic_sim = cosine_sim(embedding, logic_stats.centroid)

            if symbolic_stats.centroid is not None and symbolic_stats.size >= self.STATISTICAL_MINIMUM:
                # Normal path: real symbolic centroid
                symbolic_sim = cosine_sim(embedding, symbolic_stats.centroid)
            elif bootstrapping and bootstrap_centroid is not None:
                # Bootstrap path: reference centroid from seed symbol vocabulary
                symbolic_sim = cosine_sim(embedding, bootstrap_centroid)

            # Determine qualification
            logic_qualifies = (logic_sim >= logic_stats.threshold
                               and logic_stats.size >= self.STATISTICAL_MINIMUM)

            if symbolic_stats.size >= self.STATISTICAL_MINIMUM:
                # Normal symbolic qualification: meets cluster coherence threshold
                symbolic_qualifies = (symbolic_sim >= symbolic_stats.threshold
                                      and symbolic_stats.size >= self.STATISTICAL_MINIMUM)
            elif bootstrapping and bootstrap_centroid is not None:
                # Bootstrap symbolic qualification:
                # 1. Item is closer to symbolic reference than to logic centroid
                # 2. Item's symbolic similarity exceeds the derived mean floor
                #    (above-average affinity, not just distant from logic)
                symbolic_qualifies = (symbolic_sim > logic_sim
                                      and symbolic_sim >= bootstrap_floor)
            else:
                symbolic_qualifies = False

            # Route based on qualification
            if logic_qualifies and symbolic_qualifies:
                # Both claim it — stronger pull wins
                if logic_sim >= symbolic_sim:
                    items_to_migrate.append((item, 'logic', logic_sim))
                else:
                    items_to_migrate.append((item, 'symbolic', symbolic_sim))
            elif logic_qualifies:
                items_to_migrate.append((item, 'logic', logic_sim))
            elif symbolic_qualifies:
                items_to_migrate.append((item, 'symbolic', symbolic_sim))
            else:
                results['remained_in_bridge'] += 1

        # Cap bootstrap migrations to STATISTICAL_MINIMUM items per scan.
        # Once we seed 3 items, bootstrap is done — next scan uses real centroid.
        if bootstrapping:
            symbolic_candidates = [(i, item, target, sim)
                                   for i, (item, target, sim) in enumerate(items_to_migrate)
                                   if target == 'symbolic']
            if len(symbolic_candidates) > self.STATISTICAL_MINIMUM:
                # Keep only top N by similarity
                symbolic_candidates.sort(key=lambda x: x[3], reverse=True)
                demoted = set(x[0] for x in symbolic_candidates[self.STATISTICAL_MINIMUM:])
                items_to_migrate = [
                    (item, target, sim)
                    for i, (item, target, sim) in enumerate(items_to_migrate)
                    if i not in demoted
                ]
                results['remained_in_bridge'] += len(demoted)

        # Execute migrations
        for item, target, similarity in items_to_migrate:
            reason = 'bootstrap_seed' if (bootstrapping and target == 'symbolic') else 'adaptive_gravity'
            self._migrate_item(item, from_store='bridge', to_store=target,
                             similarity=similarity, reason=reason)
            if target == 'logic':
                results['migrated_to_logic'] += 1
            else:
                results['migrated_to_symbolic'] += 1
            results['details'].append({
                'item_id': item.get('id', 'unknown'),
                'text_preview': item.get('text', '')[:80],
                'target': target,
                'similarity': round(similarity, 4),
                'reason': reason
            })

        # Snapshot centroids for drift tracking
        self._stats_dirty = True
        self.refresh_cluster_stats()
        self._snapshot_centroids()

        # Log results
        self._log_scan_results('forward_migration', results)

        return results

    # -------------------------------------------------------------------
    # Reverse migration: Logic/Symbolic → Bridge (recontextualization)
    # -------------------------------------------------------------------

    def run_recontextualization_check(self, session_embeddings: List[np.ndarray] = None) -> Dict[str, Any]:
        """
        Check if existing logic/symbolic items have been recontextualized
        by recent learning. Uses weighted sampling biased toward domains
        relevant to what was just learned.

        Args:
            session_embeddings: Embeddings of items learned this session.
                               Used to weight sampling toward relevant items.
                               If None, uses random sampling only.
        """
        self.refresh_cluster_stats()
        logic_stats = self.logic_stats
        symbolic_stats = self.symbolic_stats

        results = {
            'checked': 0,
            'reversed_from_logic': 0,
            'reversed_from_symbolic': 0,
            'details': [],
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        # Build candidate list with relevance scoring
        all_candidates = []

        for item in self.memory.logic_memory:
            emb = get_or_compute_embedding(item)
            if emb is not None:
                all_candidates.append(('logic', item, emb))

        for item in self.memory.symbolic_memory:
            emb = get_or_compute_embedding(item)
            if emb is not None:
                all_candidates.append(('symbolic', item, emb))

        if not all_candidates:
            return results

        # Score by relevance to this session
        if session_embeddings and len(session_embeddings) > 0:
            session_centroid = np.mean(session_embeddings, axis=0)
            scored = []
            for store, item, emb in all_candidates:
                relevance = cosine_sim(emb, session_centroid)
                scored.append((store, item, emb, relevance))
            scored.sort(key=lambda x: x[3], reverse=True)
        else:
            # No session context — random ordering
            random.shuffle(all_candidates)
            scored = [(s, i, e, 0.0) for s, i, e in all_candidates]

        # Select items to check: top 10% relevant + 2% random
        n = len(scored)
        relevant_count = max(10, n // 10)
        random_count = max(5, n // 50)

        items_to_check = scored[:relevant_count]
        remaining = scored[relevant_count:]
        if remaining:
            random_picks = random.sample(remaining, min(random_count, len(remaining)))
            items_to_check.extend(random_picks)

        items_to_reverse = []

        for store, item, emb, relevance in items_to_check:
            results['checked'] += 1

            if store == 'logic':
                stats = logic_stats
            else:
                stats = symbolic_stats

            if stats.centroid is None or stats.size < self.STATISTICAL_MINIMUM:
                continue

            current_sim = cosine_sim(emb, stats.centroid)

            # Drift threshold: mean - 1 std (adaptive, derived from cluster)
            if current_sim < stats.drift_threshold:
                items_to_reverse.append((store, item, current_sim))

        # Execute reverse migrations
        for store, item, similarity in items_to_reverse:
            self._migrate_item(item, from_store=store, to_store='bridge',
                             similarity=similarity, reason='recontextualization')
            if store == 'logic':
                results['reversed_from_logic'] += 1
            else:
                results['reversed_from_symbolic'] += 1
            results['details'].append({
                'item_id': item.get('id', 'unknown'),
                'text_preview': item.get('text', '')[:80],
                'from_store': store,
                'similarity': round(similarity, 4),
                'reason': 'recontextualization'
            })

        if items_to_reverse:
            self._stats_dirty = True

        self._log_scan_results('recontextualization', results)
        return results

    # -------------------------------------------------------------------
    # Item migration mechanics
    # -------------------------------------------------------------------

    def _migrate_item(self, item: Dict, from_store: str, to_store: str,
                      similarity: float, reason: str):
        """Move an item between stores with full logging metadata."""
        # Add migration metadata
        if 'migration_history' not in item:
            item['migration_history'] = []
        item['migration_history'].append({
            'from': from_store,
            'to': to_store,
            'similarity': round(similarity, 4),
            'reason': reason,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })

        # Remove from source
        if from_store == 'bridge':
            self.memory.bridge_memory = [i for i in self.memory.bridge_memory if i is not item]
        elif from_store == 'logic':
            self.memory.logic_memory = [i for i in self.memory.logic_memory if i is not item]
        elif from_store == 'symbolic':
            self.memory.symbolic_memory = [i for i in self.memory.symbolic_memory if i is not item]

        # Update decision type
        if to_store == 'logic':
            item['decision_type'] = 'FOLLOW_LOGIC'
            self.memory.logic_memory.append(item)
        elif to_store == 'symbolic':
            item['decision_type'] = 'FOLLOW_SYMBOLIC'
            self.memory.symbolic_memory.append(item)
        elif to_store == 'bridge':
            item['decision_type'] = 'FOLLOW_HYBRID'
            self.memory.bridge_memory.append(item)

    # -------------------------------------------------------------------
    # Combined check: called after new items enter bridge
    # -------------------------------------------------------------------

    def check_and_migrate(self, session_embeddings: List[np.ndarray] = None) -> Dict[str, Any]:
        """
        Full migration cycle: check centroid drift, run forward migration
        if triggered, then run recontextualization check.

        This is the main entry point called after learning.
        """
        results = {
            'drift_detected': False,
            'forward_migration': None,
            'recontextualization': None
        }

        # Check if centroids have drifted enough to warrant a scan
        self._stats_dirty = True  # Force fresh stats
        drift = self.centroid_drift_exceeded()
        results['drift_detected'] = drift

        if drift:
            # Run forward migration (bridge → logic/symbolic)
            results['forward_migration'] = self.run_bridge_migration_scan()

            # Run recontextualization (logic/symbolic → bridge)
            results['recontextualization'] = self.run_recontextualization_check(session_embeddings)

            # Save memory after migrations
            self.memory.save_all()
        else:
            # Even without drift, always run a forward scan after learning sessions
            # (new items in bridge might match existing clusters without moving centroids)
            results['forward_migration'] = self.run_bridge_migration_scan()
            self.memory.save_all()

        return results

    # -------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------

    def _log_scan_results(self, scan_type: str, results: Dict):
        """Append scan results to migration log."""
        try:
            log = []
            if self.log_path.exists():
                with open(self.log_path, 'r') as f:
                    log = json.load(f)

            log.append({
                'type': scan_type,
                'results': results,
                'logic_stats': {
                    'size': self.logic_stats.size,
                    'threshold': round(self.logic_stats.threshold, 4),
                    'std': round(self.logic_stats.std_similarity, 4)
                } if self.logic_stats.centroid is not None else None,
                'symbolic_stats': {
                    'size': self.symbolic_stats.size,
                    'threshold': round(self.symbolic_stats.threshold, 4),
                    'std': round(self.symbolic_stats.std_similarity, 4)
                } if self.symbolic_stats.centroid is not None else None
            })

            # Keep last 500 entries
            if len(log) > 500:
                log = log[-500:]

            with open(self.log_path, 'w') as f:
                json.dump(log, f, indent=2)
        except Exception as e:
            print(f"Migration log error: {e}")

    # -------------------------------------------------------------------
    # Diagnostics
    # -------------------------------------------------------------------

    def get_migration_status(self) -> Dict[str, Any]:
        """Get current migration system status for display."""
        self.refresh_cluster_stats()
        return {
            'logic': {
                'size': self.logic_stats.size,
                'threshold': round(self.logic_stats.threshold, 4),
                'std': round(self.logic_stats.std_similarity, 4),
                'drift_threshold': round(self.logic_stats.drift_threshold, 4),
                'density_confidence': round(self.logic_stats.density_confidence, 2)
            },
            'symbolic': {
                'size': self.symbolic_stats.size,
                'threshold': round(self.symbolic_stats.threshold, 4),
                'std': round(self.symbolic_stats.std_similarity, 4),
                'drift_threshold': round(self.symbolic_stats.drift_threshold, 4),
                'density_confidence': round(self.symbolic_stats.density_confidence, 2)
            },
            'bridge_items': len(self.memory.bridge_memory),
            'drift_exceeded': self.centroid_drift_exceeded()
        }
