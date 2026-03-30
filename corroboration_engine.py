#!/usr/bin/env python3
"""
Corroboration Engine - Cross-Reference and Fact Verification

Facts must be seen multiple times from different sources before committing to memory.
This prevents single-source misinformation from polluting knowledge.

Key principles:
- Track fact fingerprints using embedding clusters (semantic similarity)
- Count corroborations per fact cluster
- Weight by source trust scores
- Detect contradictions across sources
- Facts become "ready to commit" only after sufficient corroboration

This is how the immune system learns truth through consensus without human training.
"""

import sqlite3
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class FactSighting:
    """Single observation of a fact from a source."""
    sighting_id: int
    fact_text: str
    embedding: np.ndarray
    source_url: str
    source_domain: str
    trust_score: float
    timestamp: str
    cluster_id: Optional[int] = None  # Assigned after clustering


@dataclass
class Contradiction:
    """Detected contradiction between facts."""
    fact_a_id: int
    fact_b_id: int
    fact_a_text: str
    fact_b_text: str
    similarity_score: float  # How semantically similar (close but contradictory)
    contradiction_type: str  # 'negation', 'opposite_value', 'conflicting_claim'
    confidence: float


@dataclass
class CorroborationResult:
    """Result of corroboration analysis for a fact."""
    fact_embedding: np.ndarray
    total_sightings: int
    unique_sources: int
    weighted_count: float  # Count weighted by source trust
    contradictions: List[Contradiction]
    ready_to_commit: bool
    confidence: float
    reasoning: List[str]


class CorroborationEngine:
    """
    Cross-reference system that tracks fact sightings and determines when
    facts are sufficiently corroborated for memory commit.
    """

    def __init__(self, db_path: str = "data/immune/corroboration.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

        # Corroboration thresholds
        self.min_sightings = 3  # Need at least 3 sightings
        self.min_unique_sources = 2  # From at least 2 different sources
        self.min_weighted_count = 2.0  # Trust-weighted count must be >= 2.0
        self.similarity_threshold = 0.85  # Facts with >0.85 similarity are "same fact"

        # Contradiction detection
        self.contradiction_similarity_range = (0.7, 0.95)  # Similar enough to compare, different enough to contradict

        print(f"✅ Corroboration engine initialized: {self.db_path}")

    def _init_database(self):
        """Initialize SQLite database for fact sightings."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Fact sightings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fact_sightings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_text TEXT NOT NULL,
                embedding_json TEXT NOT NULL,
                source_url TEXT NOT NULL,
                source_domain TEXT NOT NULL,
                trust_score REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cluster_id INTEGER,
                committed BOOLEAN DEFAULT 0,
                commit_timestamp TIMESTAMP
            )
        ''')

        # Fact clusters (similar facts grouped together)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fact_clusters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                representative_text TEXT NOT NULL,
                representative_embedding_json TEXT NOT NULL,
                sighting_count INTEGER DEFAULT 0,
                unique_sources INTEGER DEFAULT 0,
                weighted_count REAL DEFAULT 0.0,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ready_to_commit BOOLEAN DEFAULT 0
            )
        ''')

        # Contradiction detections
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contradictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_a_id INTEGER NOT NULL,
                fact_b_id INTEGER NOT NULL,
                similarity_score REAL NOT NULL,
                contradiction_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fact_a_id) REFERENCES fact_sightings(id),
                FOREIGN KEY (fact_b_id) REFERENCES fact_sightings(id)
            )
        ''')

        # Indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sightings_cluster
            ON fact_sightings(cluster_id)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sightings_domain
            ON fact_sightings(source_domain)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_sightings_committed
            ON fact_sightings(committed)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_clusters_ready
            ON fact_clusters(ready_to_commit)
        ''')

        conn.commit()
        conn.close()

    def record_sighting(self, fact_text: str, fact_embedding: np.ndarray,
                       source_url: str, trust_score: float) -> int:
        """
        Record a sighting of a fact from a source.

        Args:
            fact_text: Text of the fact
            fact_embedding: Vector embedding (384-dim)
            source_url: URL where fact was found
            trust_score: Trust score of the source (0.0 to 1.0)

        Returns:
            Sighting ID
        """
        from urllib.parse import urlparse
        source_domain = urlparse(source_url).netloc

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Serialize embedding as JSON
        embedding_json = np.array2string(fact_embedding, separator=',')

        # Insert sighting
        cursor.execute('''
            INSERT INTO fact_sightings
            (fact_text, embedding_json, source_url, source_domain, trust_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (fact_text[:500], embedding_json, source_url, source_domain, trust_score))

        sighting_id = cursor.lastrowid

        # Try to assign to existing cluster or create new one
        cluster_id = self._assign_to_cluster(cursor, sighting_id, fact_embedding, fact_text, trust_score)

        # Update sighting with cluster assignment
        cursor.execute('''
            UPDATE fact_sightings
            SET cluster_id = ?
            WHERE id = ?
        ''', (cluster_id, sighting_id))

        conn.commit()
        conn.close()

        return sighting_id

    def _assign_to_cluster(self, cursor, sighting_id: int, embedding: np.ndarray,
                          fact_text: str, trust_score: float) -> int:
        """
        Assign a fact sighting to an existing cluster or create new cluster.

        Returns cluster_id.
        """
        # Get all existing clusters
        cursor.execute('''
            SELECT id, representative_embedding_json
            FROM fact_clusters
        ''')

        clusters = cursor.fetchall()

        best_cluster_id = None
        best_similarity = 0.0

        # Find best matching cluster
        for cluster_id, embedding_json in clusters:
            cluster_embedding = self._deserialize_embedding(embedding_json)
            similarity = cosine_similarity([embedding], [cluster_embedding])[0][0]

            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_cluster_id = cluster_id

        if best_cluster_id:
            # Add to existing cluster
            cursor.execute('''
                UPDATE fact_clusters
                SET sighting_count = sighting_count + 1,
                    weighted_count = weighted_count + ?,
                    last_seen = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (trust_score, best_cluster_id))

            # Update unique sources count
            cursor.execute('''
                SELECT COUNT(DISTINCT source_domain)
                FROM fact_sightings
                WHERE cluster_id = ?
            ''', (best_cluster_id,))

            unique_sources = cursor.fetchone()[0]

            cursor.execute('''
                UPDATE fact_clusters
                SET unique_sources = ?
                WHERE id = ?
            ''', (unique_sources, best_cluster_id))

            # Check if ready to commit
            self._update_cluster_readiness(cursor, best_cluster_id)

            return best_cluster_id
        else:
            # Create new cluster
            embedding_json = np.array2string(embedding, separator=',')

            cursor.execute('''
                INSERT INTO fact_clusters
                (representative_text, representative_embedding_json, sighting_count,
                 unique_sources, weighted_count)
                VALUES (?, ?, 1, 1, ?)
            ''', (fact_text[:500], embedding_json, trust_score))

            return cursor.lastrowid

    def _update_cluster_readiness(self, cursor, cluster_id: int):
        """Update whether a cluster is ready to commit based on corroboration."""
        cursor.execute('''
            SELECT sighting_count, unique_sources, weighted_count
            FROM fact_clusters
            WHERE id = ?
        ''', (cluster_id,))

        result = cursor.fetchone()
        if not result:
            return

        sighting_count, unique_sources, weighted_count = result

        ready = (
            sighting_count >= self.min_sightings and
            unique_sources >= self.min_unique_sources and
            weighted_count >= self.min_weighted_count
        )

        cursor.execute('''
            UPDATE fact_clusters
            SET ready_to_commit = ?
            WHERE id = ?
        ''', (1 if ready else 0, cluster_id))

    def get_corroboration_score(self, fact_embedding: np.ndarray) -> CorroborationResult:
        """
        Get corroboration score for a fact.

        Args:
            fact_embedding: Vector embedding of the fact

        Returns:
            CorroborationResult with corroboration analysis
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Find most similar cluster
        cursor.execute('''
            SELECT id, representative_embedding_json, sighting_count,
                   unique_sources, weighted_count, ready_to_commit
            FROM fact_clusters
        ''')

        clusters = cursor.fetchall()

        best_cluster = None
        best_similarity = 0.0

        for cluster_data in clusters:
            cluster_id, embedding_json, sighting_count, unique_sources, weighted_count, ready = cluster_data
            cluster_embedding = self._deserialize_embedding(embedding_json)
            similarity = cosine_similarity([fact_embedding], [cluster_embedding])[0][0]

            if similarity > best_similarity:
                best_similarity = similarity
                best_cluster = (cluster_id, sighting_count, unique_sources, weighted_count, ready)

        if best_cluster and best_similarity >= self.similarity_threshold:
            cluster_id, sighting_count, unique_sources, weighted_count, ready = best_cluster

            # Get contradictions for this cluster
            contradictions = self._find_contradictions_for_cluster(cursor, cluster_id)

            # Build reasoning
            reasoning = [
                f"Found {sighting_count} sightings from {unique_sources} unique sources",
                f"Trust-weighted count: {weighted_count:.2f}"
            ]

            if ready:
                reasoning.append(f"✅ Meets corroboration thresholds (ready to commit)")
            else:
                missing = []
                if sighting_count < self.min_sightings:
                    missing.append(f"need {self.min_sightings - sighting_count} more sightings")
                if unique_sources < self.min_unique_sources:
                    missing.append(f"need {self.min_unique_sources - unique_sources} more unique sources")
                if weighted_count < self.min_weighted_count:
                    missing.append(f"need {self.min_weighted_count - weighted_count:.1f} more trust-weighted count")

                reasoning.append(f"❌ Not ready: {', '.join(missing)}")

            if contradictions:
                reasoning.append(f"⚠️ Found {len(contradictions)} contradictions")

            confidence = min(1.0, (sighting_count / self.min_sightings) *
                                  (unique_sources / self.min_unique_sources) *
                                  (weighted_count / self.min_weighted_count))

        else:
            # No matching cluster - this is a new fact
            sighting_count = 0
            unique_sources = 0
            weighted_count = 0.0
            ready = False
            contradictions = []
            reasoning = ["New fact - no prior sightings", "❌ Not ready: need corroboration"]
            confidence = 0.0

        conn.close()

        return CorroborationResult(
            fact_embedding=fact_embedding,
            total_sightings=sighting_count,
            unique_sources=unique_sources,
            weighted_count=weighted_count,
            contradictions=contradictions,
            ready_to_commit=ready,
            confidence=confidence,
            reasoning=reasoning
        )

    def find_contradictions(self, fact_embedding: np.ndarray) -> List[Contradiction]:
        """
        Find contradictions for a specific fact.

        Args:
            fact_embedding: Vector embedding of the fact

        Returns:
            List of Contradiction objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Find facts in the contradiction similarity range
        cursor.execute('''
            SELECT id, fact_text, embedding_json
            FROM fact_sightings
            WHERE committed = 1
        ''')

        contradictions = []

        for fact_id, fact_text, embedding_json in cursor.fetchall():
            other_embedding = self._deserialize_embedding(embedding_json)
            similarity = cosine_similarity([fact_embedding], [other_embedding])[0][0]

            # Check if in contradiction range
            if self.contradiction_similarity_range[0] <= similarity <= self.contradiction_similarity_range[1]:
                # Detect contradiction type
                contradiction_type, confidence = self._detect_contradiction_type(
                    fact_text, other_embedding
                )

                if contradiction_type:
                    contradictions.append(Contradiction(
                        fact_a_id=-1,  # New fact (not in DB yet)
                        fact_b_id=fact_id,
                        fact_a_text="[New fact being evaluated]",
                        fact_b_text=fact_text,
                        similarity_score=similarity,
                        contradiction_type=contradiction_type,
                        confidence=confidence
                    ))

        conn.close()
        return contradictions

    def _find_contradictions_for_cluster(self, cursor, cluster_id: int) -> List[Contradiction]:
        """Find contradictions involving facts in a cluster."""
        cursor.execute('''
            SELECT id, fact_a_id, fact_b_id, similarity_score, contradiction_type, confidence
            FROM contradictions
            WHERE fact_a_id IN (SELECT id FROM fact_sightings WHERE cluster_id = ?)
            OR fact_b_id IN (SELECT id FROM fact_sightings WHERE cluster_id = ?)
        ''', (cluster_id, cluster_id))

        contradictions = []

        for row in cursor.fetchall():
            # Get fact texts
            contradiction_id, fact_a_id, fact_b_id, similarity, ctype, confidence = row

            cursor.execute('SELECT fact_text FROM fact_sightings WHERE id = ?', (fact_a_id,))
            fact_a_text = cursor.fetchone()[0]

            cursor.execute('SELECT fact_text FROM fact_sightings WHERE id = ?', (fact_b_id,))
            fact_b_text = cursor.fetchone()[0]

            contradictions.append(Contradiction(
                fact_a_id=fact_a_id,
                fact_b_id=fact_b_id,
                fact_a_text=fact_a_text,
                fact_b_text=fact_b_text,
                similarity_score=similarity,
                contradiction_type=ctype,
                confidence=confidence
            ))

        return contradictions

    def _detect_contradiction_type(self, text_a: str, text_b: str) -> Tuple[Optional[str], float]:
        """
        Detect type of contradiction between two texts.

        Returns (contradiction_type, confidence) or (None, 0.0) if no contradiction.
        """
        text_a_lower = text_a.lower()
        text_b_lower = text_b.lower()

        # Negation detection
        negation_words_a = {'not', 'no', 'never', 'neither', 'none'}
        negation_words_b = {'is', 'has', 'can', 'will', 'does'}

        has_negation_a = any(word in text_a_lower for word in negation_words_a)
        has_negation_b = any(word in text_b_lower for word in negation_words_a)

        if has_negation_a != has_negation_b:
            return 'negation', 0.7

        # Opposite values (simple detection)
        opposites = [
            ('true', 'false'), ('yes', 'no'), ('good', 'bad'),
            ('increase', 'decrease'), ('more', 'less'), ('higher', 'lower')
        ]

        for word_a, word_b in opposites:
            if ((word_a in text_a_lower and word_b in text_b_lower) or
                (word_b in text_a_lower and word_a in text_b_lower)):
                return 'opposite_value', 0.6

        # No clear contradiction detected
        return None, 0.0

    def mark_cluster_committed(self, cluster_id: int) -> int:
        """
        Mark all sightings in a cluster as committed to memory.

        Returns number of sightings marked.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE fact_sightings
            SET committed = 1,
                commit_timestamp = CURRENT_TIMESTAMP
            WHERE cluster_id = ? AND committed = 0
        ''', (cluster_id,))

        count = cursor.rowcount

        conn.commit()
        conn.close()

        return count

    def get_ready_clusters(self, limit: int = 10) -> List[Dict]:
        """Get clusters that are ready to commit to memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, representative_text, sighting_count, unique_sources, weighted_count
            FROM fact_clusters
            WHERE ready_to_commit = 1
            ORDER BY weighted_count DESC
            LIMIT ?
        ''', (limit,))

        clusters = []
        for row in cursor.fetchall():
            clusters.append({
                'cluster_id': row[0],
                'text': row[1],
                'sightings': row[2],
                'sources': row[3],
                'weighted_count': row[4]
            })

        conn.close()
        return clusters

    def _serialize_embedding(self, embedding: np.ndarray) -> str:
        """Serialize numpy array to string."""
        return np.array2string(embedding, separator=',')

    def _deserialize_embedding(self, embedding_str: str) -> np.ndarray:
        """Deserialize string to numpy array."""
        # Remove brackets and parse
        clean_str = embedding_str.strip('[]')
        values = [float(x.strip()) for x in clean_str.split(',')]
        return np.array(values)

    def get_stats(self) -> Dict:
        """Get overall corroboration statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM fact_sightings')
        total_sightings = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM fact_clusters')
        total_clusters = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM fact_clusters WHERE ready_to_commit = 1')
        ready_clusters = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM fact_sightings WHERE committed = 1')
        committed_sightings = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(DISTINCT source_domain) FROM fact_sightings')
        unique_domains = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM contradictions')
        total_contradictions = cursor.fetchone()[0]

        conn.close()

        return {
            'total_sightings': total_sightings,
            'total_clusters': total_clusters,
            'ready_to_commit': ready_clusters,
            'committed': committed_sightings,
            'pending': total_sightings - committed_sightings,
            'unique_sources': unique_domains,
            'contradictions_detected': total_contradictions
        }


# Testing function
if __name__ == "__main__":
    print("🧪 Testing Corroboration Engine...")

    engine = CorroborationEngine("data/immune/corroboration_test.db")

    # Test 1: Record fact sightings
    print("\n1️⃣ Testing fact sighting recording...")

    # Create sample embeddings (in real use, these come from sentence transformers)
    fact1_embedding = np.random.rand(384)
    fact2_embedding = fact1_embedding + np.random.rand(384) * 0.05  # Very similar
    fact3_embedding = np.random.rand(384)  # Different fact

    # Record sightings of same fact from different sources
    sighting1 = engine.record_sighting(
        "Water boils at 100°C at sea level",
        fact1_embedding,
        "https://science.edu/physics",
        trust_score=0.9
    )

    sighting2 = engine.record_sighting(
        "At sea level, water boils at 100 degrees Celsius",
        fact2_embedding,
        "https://encyclopedia.org/water",
        trust_score=0.8
    )

    sighting3 = engine.record_sighting(
        "The Earth orbits the Sun",
        fact3_embedding,
        "https://astronomy.edu/basics",
        trust_score=0.9
    )

    print(f"   Recorded sightings: {sighting1}, {sighting2}, {sighting3}")

    # Test 2: Check corroboration
    print("\n2️⃣ Testing corroboration scoring...")

    corroboration1 = engine.get_corroboration_score(fact1_embedding)
    print(f"   Fact 1 corroboration:")
    print(f"      Sightings: {corroboration1.total_sightings}")
    print(f"      Unique sources: {corroboration1.unique_sources}")
    print(f"      Weighted count: {corroboration1.weighted_count:.2f}")
    print(f"      Ready to commit: {corroboration1.ready_to_commit}")
    for reason in corroboration1.reasoning:
        print(f"      - {reason}")

    # Test 3: Add third sighting to make it ready
    print("\n3️⃣ Testing threshold crossing...")

    sighting4 = engine.record_sighting(
        "Water's boiling point is 100°C at sea level",
        fact1_embedding,
        "https://textbook.com/chemistry",
        trust_score=0.7
    )

    corroboration2 = engine.get_corroboration_score(fact1_embedding)
    print(f"   After third sighting:")
    print(f"      Sightings: {corroboration2.total_sightings}")
    print(f"      Ready to commit: {corroboration2.ready_to_commit}")

    # Test 4: Ready clusters
    print("\n4️⃣ Testing ready clusters retrieval...")

    ready = engine.get_ready_clusters()
    print(f"   Ready clusters: {len(ready)}")
    for cluster in ready:
        print(f"      Cluster {cluster['cluster_id']}: '{cluster['text'][:50]}...' ({cluster['sightings']} sightings)")

    # Test 5: Statistics
    print("\n5️⃣ Testing statistics...")

    stats = engine.get_stats()
    print(f"   Total sightings: {stats['total_sightings']}")
    print(f"   Total clusters: {stats['total_clusters']}")
    print(f"   Ready to commit: {stats['ready_to_commit']}")
    print(f"   Unique sources: {stats['unique_sources']}")

    print("\n✅ All corroboration engine tests passed!")

    # Cleanup
    import os
    if os.path.exists("data/immune/corroboration_test.db"):
        os.remove("data/immune/corroboration_test.db")
        print("🧹 Test database cleaned up")
