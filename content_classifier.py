# content_classifier.py - Grounded logic/symbolic/bridge classification
"""
Replaces the hardcoded keyword lists that previously decided what counted as
"logical" or "symbolic" content (Talk pages read as symbolic because editor
chatter is conversational; category pages classified on coin-flip noise).

Two signal sources, in strict order of preference:

1. EMERGENT CENTROIDS - once the logic and symbolic stores each hold at
   least `min_items_for_centroids` embedded items, a chunk is classified by
   cosine similarity to each store's centroid. Fully emergent: the meaning
   of "logical" and "symbolic" is whatever Sofia's own clusters have become.
   No content words are hardcoded anywhere.

2. BOOTSTRAP MEASUREMENTS - before centroids exist (a young learner), the
   only signals used are measurements, not content lists:
     - emotion intensity from the trained emotion models (emotion_handler)
     - numeric/structural density (counts of numbers, units, dates - regex
       math, not topic keywords)
   These are deliberately weak: most early content lands in bridge with a
   recorded impression, which is CORRECT for an early learner - migration
   resolves placement as clusters form.

Every result carries its measured scores so downstream storage can persist
them (migration's overlap consensus reads logic_score/symbolic_score) and
logs can show the evidence instead of an unexplained label.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import json
import re

import numpy as np


@dataclass
class ClassificationResult:
    label: str                    # 'logical' | 'symbolic' | 'bridge'
    logic_score: float            # 0..1
    symbolic_score: float         # 0..1
    confidence: float             # 0..1
    basis: str                    # 'centroids' | 'bootstrap' | 'none'
    evidence: Dict = field(default_factory=dict)


class GroundedClassifier:
    """Classifies chunks against Sofia's own emergent clusters when possible."""

    def __init__(self, data_dir: str = "data", min_items_for_centroids: int = 20,
                 margin: float = 0.05):
        self.data_dir = Path(data_dir)
        self.min_items = min_items_for_centroids
        self.margin = margin
        # (logic_count, symbolic_count) -> (logic_centroid, symbolic_centroid)
        self._centroid_cache = None
        self._centroid_cache_key = None

    # ------------------------------------------------------------------
    # Centroid signal (emergent)
    # ------------------------------------------------------------------

    def _load_store_embeddings(self, filename: str) -> List[np.ndarray]:
        path = self.data_dir / filename
        try:
            items = json.load(open(path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        vecs = []
        for item in items:
            emb = item.get("embedding")
            if emb:
                vecs.append(np.asarray(emb, dtype=np.float32))
        return vecs

    def _get_centroids(self):
        """Unit-norm centroids of the logic and symbolic stores, or None."""
        logic_vecs = self._load_store_embeddings("logic_memory.json")
        symbolic_vecs = self._load_store_embeddings("symbolic_memory.json")
        key = (len(logic_vecs), len(symbolic_vecs))
        if self._centroid_cache_key == key:
            return self._centroid_cache

        if len(logic_vecs) < self.min_items or len(symbolic_vecs) < self.min_items:
            self._centroid_cache, self._centroid_cache_key = None, key
            return None

        def unit_centroid(vecs):
            m = np.mean(np.stack(vecs), axis=0)
            n = np.linalg.norm(m)
            return m / n if n > 0 else None

        lc, sc = unit_centroid(logic_vecs), unit_centroid(symbolic_vecs)
        self._centroid_cache = (lc, sc) if lc is not None and sc is not None else None
        self._centroid_cache_key = key
        return self._centroid_cache

    # ------------------------------------------------------------------
    # Bootstrap signals (measurements only)
    # ------------------------------------------------------------------

    @staticmethod
    def _structural_density(text: str) -> float:
        """Share of tokens that are numbers/measurements — math, not topics."""
        tokens = text.split()
        if not tokens:
            return 0.0
        numeric = len(re.findall(r'(?<!\w)[-+]?\d[\d.,%]*(?!\w)', text))
        return min(1.0, numeric / max(len(tokens), 1) * 5)

    @staticmethod
    def _emotion_intensity(text: str) -> float:
        """Emotion intensity from the hartmann model: top_non_neutral * (1 - neutral).

        The models always emit a top class, so a raw peak score reads dry
        statistics as 'amusement 0.98'. Weighting by (1 - neutral) uses the
        model's own neutrality judgment to separate calm facts (neutral 0.94
        -> intensity ~0.05) from genuine emotion (neutral 0.23 -> ~0.76).
        """
        try:
            from emotion_handler import predict_emotions
            hartmann = dict(predict_emotions(text[:800]).get("hartmann_emotions", []))
            if not hartmann:
                return 0.0
            neutral = hartmann.get("neutral", 0.5)
            non_neutral = max((s for label, s in hartmann.items() if label != "neutral"),
                              default=0.0)
            return float(non_neutral * (1.0 - neutral))
        except Exception:
            return 0.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(self, text: str, embedding: Optional[np.ndarray] = None) -> ClassificationResult:
        if not text or not text.strip():
            return ClassificationResult("bridge", 0.0, 0.0, 0.0, "none")

        centroids = self._get_centroids()

        if centroids is not None:
            if embedding is None:
                try:
                    from vector_engine import fuse_vectors
                    vec, _ = fuse_vectors(text[:1000])
                    embedding = np.asarray(vec, dtype=np.float32) if vec is not None else None
                except Exception:
                    embedding = None
            if embedding is not None:
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    unit = embedding / norm
                    logic_c, symbolic_c = centroids
                    logic_sim = float(unit @ logic_c)
                    symbolic_sim = float(unit @ symbolic_c)
                    # map cosine [-1,1] -> [0,1] for storage compatibility
                    logic_score = (logic_sim + 1) / 2
                    symbolic_score = (symbolic_sim + 1) / 2
                    gap = abs(logic_sim - symbolic_sim)
                    evidence = {"logic_sim": round(logic_sim, 4),
                                "symbolic_sim": round(symbolic_sim, 4),
                                "gap": round(gap, 4)}
                    if gap < self.margin:
                        return ClassificationResult("bridge", logic_score, symbolic_score,
                                                    round(gap / self.margin, 3), "centroids", evidence)
                    label = "logical" if logic_sim > symbolic_sim else "symbolic"
                    confidence = min(1.0, gap / (self.margin * 4))
                    return ClassificationResult(label, logic_score, symbolic_score,
                                                round(confidence, 3), "centroids", evidence)

        # Bootstrap: weak measured lean, mostly defers to bridge
        structure = self._structural_density(text)
        emotion = self._emotion_intensity(text)
        evidence = {"structural_density": round(structure, 3),
                    "emotion_intensity": round(emotion, 3)}
        logic_score = round(structure, 3)
        symbolic_score = round(emotion, 3)

        if emotion >= 0.6 and emotion > structure * 2:
            return ClassificationResult("symbolic", logic_score, symbolic_score,
                                        0.3, "bootstrap", evidence)
        if structure >= 0.4 and structure > emotion * 2:
            return ClassificationResult("logical", logic_score, symbolic_score,
                                        0.3, "bootstrap", evidence)
        return ClassificationResult("bridge", logic_score, symbolic_score, 0.2,
                                    "bootstrap", evidence)


_classifier_instances: Dict[str, GroundedClassifier] = {}


def get_classifier(data_dir: str = "data") -> GroundedClassifier:
    key = str(Path(data_dir).resolve())
    if key not in _classifier_instances:
        _classifier_instances[key] = GroundedClassifier(data_dir)
    return _classifier_instances[key]
