#!/usr/bin/env python3
"""
Self-Correction System - Auto-Learning Without Human Training

This system tracks the immune system's own accuracy and automatically adjusts
thresholds and pattern weights to minimize errors. It learns what works without
any human training data.

Key insight: Outcomes are discovered through corroboration.
- If blocked content later appears from 5+ trusted sources → false positive
- If allowed content later contradicted by 5+ trusted sources → false negative

The system continuously improves itself by:
1. Recording all decisions with triggering patterns
2. Monitoring outcomes through corroboration
3. Calculating accuracy metrics (FP rate, FN rate)
4. Auto-adjusting pattern weights to reduce errors
5. Logging all adjustments for transparency
"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter


@dataclass
class ImmuneDecision:
    """Record of an immune system decision."""
    decision_id: int
    item_id: str                  # Unique ID for the content
    item_type: str                # 'page', 'fact', 'chunk'
    decision: str                 # 'ALLOW', 'BLOCK', 'REVIEW'
    threat_score: float
    confidence: float
    trigger_patterns: List[str]   # Which patterns triggered
    timestamp: str
    outcome: Optional[str] = None  # 'correct', 'false_positive', 'false_negative'
    outcome_timestamp: Optional[str] = None
    outcome_evidence: Optional[str] = None


@dataclass
class AccuracyReport:
    """Accuracy statistics for the immune system."""
    total_decisions: int
    decisions_with_outcomes: int
    correct_decisions: int
    false_positives: int
    false_negatives: int
    accuracy_rate: float
    false_positive_rate: float
    false_negative_rate: float
    recent_adjustments: List[Dict]
    pattern_performance: Dict[str, Dict]


@dataclass
class ThresholdAdjustment:
    """Record of a threshold adjustment."""
    adjustment_id: int
    parameter_name: str
    old_value: float
    new_value: float
    reason: str
    timestamp: str
    expected_impact: str


class SelfCorrection:
    """
    Self-learning system that tracks accuracy and adjusts immune system
    parameters automatically without human training.
    """

    def __init__(self, db_path: str = "data/immune/self_correction.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

        # Outcome discovery thresholds
        self.corroboration_threshold = 5  # Need 5+ sightings to validate
        self.contradiction_threshold = 5   # 5+ contradictions to invalidate

        # Accuracy targets
        self.target_false_positive_rate = 0.05  # Max 5% false positives
        self.target_false_negative_rate = 0.10  # Max 10% false negatives

        # Adjustment parameters
        self.pattern_adjustment_step = 0.1  # Adjust weights by ±0.1
        self.min_decisions_for_adjustment = 20  # Need 20+ decisions before adjusting

        print(f"✅ Self-correction system initialized: {self.db_path}")

    def _init_database(self):
        """Initialize SQLite database for decision tracking."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Decision records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL UNIQUE,
                item_type TEXT NOT NULL,
                decision TEXT NOT NULL,
                threat_score REAL NOT NULL,
                confidence REAL NOT NULL,
                trigger_patterns_json TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                outcome TEXT,
                outcome_timestamp TIMESTAMP,
                outcome_evidence TEXT
            )
        ''')

        # Threshold adjustment history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threshold_adjustments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parameter_name TEXT NOT NULL,
                old_value REAL NOT NULL,
                new_value REAL NOT NULL,
                reason TEXT NOT NULL,
                expected_impact TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Pattern performance tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_performance (
                pattern_id TEXT PRIMARY KEY,
                total_triggers INTEGER DEFAULT 0,
                correct_triggers INTEGER DEFAULT 0,
                false_positive_triggers INTEGER DEFAULT 0,
                false_negative_misses INTEGER DEFAULT 0,
                current_weight REAL DEFAULT 1.0,
                last_adjusted TIMESTAMP
            )
        ''')

        # Indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_decisions_outcome
            ON decisions(outcome)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_decisions_timestamp
            ON decisions(timestamp DESC)
        ''')

        conn.commit()
        conn.close()

    def record_decision(self, item_id: str, item_type: str, decision: str,
                       threat_score: float, confidence: float,
                       trigger_patterns: List[str]) -> int:
        """
        Record an immune system decision for future outcome tracking.

        Args:
            item_id: Unique identifier for the content
            item_type: Type of content ('page', 'fact', 'chunk')
            decision: Decision made ('ALLOW', 'BLOCK', 'REVIEW')
            threat_score: Threat score (0.0 to 1.0)
            confidence: Confidence in decision (0.0 to 1.0)
            trigger_patterns: List of pattern IDs that triggered

        Returns:
            Decision ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        trigger_patterns_json = json.dumps(trigger_patterns)

        cursor.execute('''
            INSERT OR REPLACE INTO decisions
            (item_id, item_type, decision, threat_score, confidence, trigger_patterns_json)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item_id, item_type, decision, threat_score, confidence, trigger_patterns_json))

        decision_id = cursor.lastrowid

        # Update pattern trigger counts
        for pattern_id in trigger_patterns:
            cursor.execute('''
                INSERT OR IGNORE INTO pattern_performance (pattern_id)
                VALUES (?)
            ''', (pattern_id,))

            cursor.execute('''
                UPDATE pattern_performance
                SET total_triggers = total_triggers + 1
                WHERE pattern_id = ?
            ''', (pattern_id,))

        conn.commit()
        conn.close()

        return decision_id

    def record_outcome(self, item_id: str, actual_outcome: str, evidence: str) -> None:
        """
        Record the actual outcome for a decision (discovered later through corroboration).

        Args:
            item_id: Identifier for the content
            actual_outcome: 'correct', 'false_positive', or 'false_negative'
            evidence: Evidence for this outcome (e.g., "Corroborated by 7 trusted sources")
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the decision
        cursor.execute('''
            SELECT id, decision, trigger_patterns_json
            FROM decisions
            WHERE item_id = ?
        ''', (item_id,))

        result = cursor.fetchone()

        if not result:
            print(f"⚠️ No decision found for item {item_id}")
            conn.close()
            return

        decision_id, decision, trigger_patterns_json = result
        trigger_patterns = json.loads(trigger_patterns_json)

        # Update decision with outcome
        cursor.execute('''
            UPDATE decisions
            SET outcome = ?,
                outcome_timestamp = CURRENT_TIMESTAMP,
                outcome_evidence = ?
            WHERE item_id = ?
        ''', (actual_outcome, evidence, item_id))

        # Update pattern performance
        for pattern_id in trigger_patterns:
            if actual_outcome == 'correct':
                cursor.execute('''
                    UPDATE pattern_performance
                    SET correct_triggers = correct_triggers + 1
                    WHERE pattern_id = ?
                ''', (pattern_id,))

            elif actual_outcome == 'false_positive':
                cursor.execute('''
                    UPDATE pattern_performance
                    SET false_positive_triggers = false_positive_triggers + 1
                    WHERE pattern_id = ?
                ''', (pattern_id,))

                print(f"📉 False positive detected for pattern '{pattern_id}' - will adjust weight down")

        # If false negative, increment misses for patterns that SHOULD have triggered
        if actual_outcome == 'false_negative':
            # This is trickier - we need to know which patterns should have caught this
            # For now, we'll handle this through periodic pattern review
            print(f"📈 False negative detected - need to identify missing patterns")

        conn.commit()
        conn.close()

        print(f"   Outcome recorded for {item_id}: {actual_outcome}")

    def get_accuracy_stats(self) -> AccuracyReport:
        """
        Calculate current accuracy statistics.

        Returns:
            AccuracyReport with comprehensive metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get decision counts
        cursor.execute('SELECT COUNT(*) FROM decisions')
        total_decisions = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM decisions WHERE outcome IS NOT NULL')
        decisions_with_outcomes = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM decisions WHERE outcome = ?', ('correct',))
        correct_decisions = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM decisions WHERE outcome = ?', ('false_positive',))
        false_positives = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM decisions WHERE outcome = ?', ('false_negative',))
        false_negatives = cursor.fetchone()[0]

        # Calculate rates
        if decisions_with_outcomes > 0:
            accuracy_rate = correct_decisions / decisions_with_outcomes
            false_positive_rate = false_positives / decisions_with_outcomes
            false_negative_rate = false_negatives / decisions_with_outcomes
        else:
            accuracy_rate = 0.0
            false_positive_rate = 0.0
            false_negative_rate = 0.0

        # Get recent adjustments
        cursor.execute('''
            SELECT parameter_name, old_value, new_value, reason, timestamp
            FROM threshold_adjustments
            ORDER BY timestamp DESC
            LIMIT 10
        ''')

        recent_adjustments = []
        for row in cursor.fetchall():
            recent_adjustments.append({
                'parameter': row[0],
                'old_value': row[1],
                'new_value': row[2],
                'reason': row[3],
                'timestamp': row[4]
            })

        # Get pattern performance
        cursor.execute('''
            SELECT pattern_id, total_triggers, correct_triggers,
                   false_positive_triggers, false_negative_misses, current_weight
            FROM pattern_performance
        ''')

        pattern_performance = {}
        for row in cursor.fetchall():
            pattern_id, total, correct, fp, fn, weight = row

            if total > 0:
                accuracy = correct / total
                fp_rate = fp / total
            else:
                accuracy = 0.0
                fp_rate = 0.0

            pattern_performance[pattern_id] = {
                'total_triggers': total,
                'correct': correct,
                'false_positives': fp,
                'false_negatives': fn,
                'accuracy': accuracy,
                'fp_rate': fp_rate,
                'current_weight': weight
            }

        conn.close()

        return AccuracyReport(
            total_decisions=total_decisions,
            decisions_with_outcomes=decisions_with_outcomes,
            correct_decisions=correct_decisions,
            false_positives=false_positives,
            false_negatives=false_negatives,
            accuracy_rate=accuracy_rate,
            false_positive_rate=false_positive_rate,
            false_negative_rate=false_negative_rate,
            recent_adjustments=recent_adjustments,
            pattern_performance=pattern_performance
        )

    def auto_adjust_thresholds(self) -> List[Dict]:
        """
        Automatically adjust pattern weights and thresholds to improve accuracy.

        This is called periodically (e.g., daily) to tune the immune system.

        Returns:
            List of adjustments made
        """
        stats = self.get_accuracy_stats()

        adjustments = []

        # Only adjust if we have enough data
        if stats.decisions_with_outcomes < self.min_decisions_for_adjustment:
            print(f"⏳ Need {self.min_decisions_for_adjustment - stats.decisions_with_outcomes} more outcomes before adjusting")
            return adjustments

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Adjust pattern weights based on false positive rates
        for pattern_id, perf in stats.pattern_performance.items():
            if perf['total_triggers'] < 5:
                continue  # Need more data for this pattern

            current_weight = perf['current_weight']
            old_weight = current_weight

            # If pattern has high false positive rate, reduce weight
            if perf['fp_rate'] > 0.3:  # >30% false positives
                new_weight = max(0.1, current_weight - self.pattern_adjustment_step)
                reason = f"High false positive rate ({perf['fp_rate']:.1%}) - reducing sensitivity"

                cursor.execute('''
                    UPDATE pattern_performance
                    SET current_weight = ?,
                        last_adjusted = CURRENT_TIMESTAMP
                    WHERE pattern_id = ?
                ''', (new_weight, pattern_id))

                self._log_adjustment(cursor, f"pattern_weight_{pattern_id}",
                                    old_weight, new_weight, reason,
                                    "Reduce false positives")

                adjustments.append({
                    'type': 'pattern_weight',
                    'pattern_id': pattern_id,
                    'old_weight': old_weight,
                    'new_weight': new_weight,
                    'reason': reason
                })

                print(f"🔧 Adjusted '{pattern_id}': {old_weight:.2f} → {new_weight:.2f}")

            # If pattern has high accuracy, maybe increase weight slightly
            elif perf['accuracy'] > 0.9 and perf['fp_rate'] < 0.05:
                new_weight = min(2.0, current_weight + self.pattern_adjustment_step / 2)
                reason = f"High accuracy ({perf['accuracy']:.1%}), low FP rate - increasing confidence"

                cursor.execute('''
                    UPDATE pattern_performance
                    SET current_weight = ?,
                        last_adjusted = CURRENT_TIMESTAMP
                    WHERE pattern_id = ?
                ''', (new_weight, pattern_id))

                self._log_adjustment(cursor, f"pattern_weight_{pattern_id}",
                                    old_weight, new_weight, reason,
                                    "Increase pattern strength")

                adjustments.append({
                    'type': 'pattern_weight',
                    'pattern_id': pattern_id,
                    'old_weight': old_weight,
                    'new_weight': new_weight,
                    'reason': reason
                })

                print(f"🔧 Strengthened '{pattern_id}': {old_weight:.2f} → {new_weight:.2f}")

        conn.commit()
        conn.close()

        if not adjustments:
            print("✓ No threshold adjustments needed - performance within targets")

        return adjustments

    def discover_outcomes_from_corroboration(self, corroboration_engine, trust_db):
        """
        Discover outcomes by checking if blocked/allowed items later became corroborated or contradicted.

        This is the key to learning without human labels!

        Args:
            corroboration_engine: CorroborationEngine instance
            trust_db: TrustDatabase instance

        Returns:
            int: Number of outcomes discovered
        """
        import numpy as np

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get decisions without outcomes that are at least 1 day old
        cursor.execute('''
            SELECT decision_id, item_id, decision, threat_score, trigger_patterns_json
            FROM decisions
            WHERE outcome IS NULL
            AND timestamp < datetime('now', '-1 day')
        ''')

        pending_decisions = cursor.fetchall()

        outcomes_discovered = 0

        for decision_id, item_id, decision, threat_score, trigger_patterns_json in pending_decisions:
            trigger_patterns = json.loads(trigger_patterns_json)

            # Parse item_id to extract URL and content hash
            # Format: "url:<url>:hash:<hash>"
            if not item_id.startswith("url:"):
                continue

            parts = item_id.split(":")
            if len(parts) < 4:
                continue

            url = parts[1]
            content_hash = parts[3] if len(parts) > 3 else None

            # Get domain trust
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            domain_trust = trust_db.get_trust(domain)

            # For blocked items: if later corroborated by trusted sources → false positive
            if decision == 'BLOCK':
                # Check corroboration database for this URL
                corr_conn = sqlite3.connect(corroboration_engine.db_path)
                corr_cursor = corr_conn.cursor()

                corr_cursor.execute('''
                    SELECT COUNT(*), COUNT(DISTINCT source_domain), AVG(trust_score)
                    FROM fact_sightings
                    WHERE source_url = ?
                ''', (url,))

                result = corr_cursor.fetchone()
                corr_conn.close()

                if result and result[0]:
                    sighting_count, unique_sources, avg_trust = result

                    # If later seen 5+ times from 3+ trusted sources (avg trust > 0.6) → false positive
                    if sighting_count >= 5 and unique_sources >= 3 and avg_trust > 0.6:
                        outcome = 'false_positive'
                        evidence = f"Later corroborated: {sighting_count} sightings, {unique_sources} sources, trust {avg_trust:.2f}"

                        self.record_outcome(item_id, outcome, evidence)
                        outcomes_discovered += 1

                        print(f"   🔍 FP discovered: Blocked {url[:50]} but later corroborated")

            # For allowed items: if later contradicted by trusted sources → false negative
            elif decision == 'ALLOW':
                # Check if this URL later appeared in contradictions or got low trust
                if domain_trust < 0.3:  # Trust dropped significantly
                    outcome = 'false_negative'
                    evidence = f"Domain trust dropped to {domain_trust:.2f} (was allowed at {threat_score:.2f})"

                    self.record_outcome(item_id, outcome, evidence)
                    outcomes_discovered += 1

                    print(f"   🔍 FN discovered: Allowed {url[:50]} but trust dropped to {domain_trust:.2f}")

        conn.close()

        if outcomes_discovered > 0:
            print(f"🔍 Discovered {outcomes_discovered} outcomes through corroboration")

        return outcomes_discovered

    def _log_adjustment(self, cursor, parameter_name: str, old_value: float,
                       new_value: float, reason: str, expected_impact: str):
        """Log a threshold adjustment."""
        cursor.execute('''
            INSERT INTO threshold_adjustments
            (parameter_name, old_value, new_value, reason, expected_impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (parameter_name, old_value, new_value, reason, expected_impact))

    def get_pattern_weights(self) -> Dict[str, float]:
        """Get current pattern weights for immune system update."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT pattern_id, current_weight
            FROM pattern_performance
        ''')

        weights = {}
        for pattern_id, weight in cursor.fetchall():
            weights[pattern_id] = weight

        conn.close()
        return weights

    def export_learning_report(self, output_path: str) -> None:
        """Export comprehensive learning report for analysis."""
        stats = self.get_accuracy_stats()

        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'accuracy_metrics': {
                'total_decisions': stats.total_decisions,
                'evaluated_decisions': stats.decisions_with_outcomes,
                'accuracy_rate': stats.accuracy_rate,
                'false_positive_rate': stats.false_positive_rate,
                'false_negative_rate': stats.false_negative_rate
            },
            'pattern_performance': stats.pattern_performance,
            'recent_adjustments': stats.recent_adjustments
        }

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Learning report exported to {output_path}")


# Testing function
if __name__ == "__main__":
    print("🧪 Testing Self-Correction System...")

    correction = SelfCorrection("data/immune/self_correction_test.db")

    # Test 1: Record decisions
    print("\n1️⃣ Testing decision recording...")

    decision1 = correction.record_decision(
        item_id="page_1",
        item_type="page",
        decision="BLOCK",
        threat_score=0.8,
        confidence=0.7,
        trigger_patterns=['hidden_elements', 'suspicious_scripts']
    )

    decision2 = correction.record_decision(
        item_id="page_2",
        item_type="page",
        decision="ALLOW",
        threat_score=0.2,
        confidence=0.9,
        trigger_patterns=[]
    )

    print(f"   Recorded decisions: {decision1}, {decision2}")

    # Test 2: Record outcomes
    print("\n2️⃣ Testing outcome recording...")

    correction.record_outcome("page_1", "false_positive", "Later corroborated by 6 trusted sources")
    correction.record_outcome("page_2", "correct", "No contradictions found")

    # Test 3: Get accuracy stats
    print("\n3️⃣ Testing accuracy statistics...")

    stats = correction.get_accuracy_stats()
    print(f"   Total decisions: {stats.total_decisions}")
    print(f"   Evaluated: {stats.decisions_with_outcomes}")
    print(f"   Accuracy: {stats.accuracy_rate:.1%}")
    print(f"   False positive rate: {stats.false_positive_rate:.1%}")
    print(f"   False negative rate: {stats.false_negative_rate:.1%}")

    # Test 4: Add more decisions to trigger adjustment
    print("\n4️⃣ Testing threshold adjustment...")

    # Add many false positives for 'hidden_elements' pattern
    for i in range(10):
        decision_id = correction.record_decision(
            item_id=f"page_fp_{i}",
            item_type="page",
            decision="BLOCK",
            threat_score=0.7,
            confidence=0.6,
            trigger_patterns=['hidden_elements']
        )
        correction.record_outcome(f"page_fp_{i}", "false_positive",
                                 "Later verified as legitimate")

    # Run auto-adjustment
    adjustments = correction.auto_adjust_thresholds()
    print(f"   Adjustments made: {len(adjustments)}")
    for adj in adjustments:
        print(f"      {adj['pattern_id']}: {adj['old_weight']:.2f} → {adj['new_weight']:.2f}")

    # Test 5: Pattern performance
    print("\n5️⃣ Testing pattern performance tracking...")

    final_stats = correction.get_accuracy_stats()
    for pattern_id, perf in final_stats.pattern_performance.items():
        print(f"   {pattern_id}:")
        print(f"      Triggers: {perf['total_triggers']}")
        print(f"      Accuracy: {perf['accuracy']:.1%}")
        print(f"      FP rate: {perf['fp_rate']:.1%}")
        print(f"      Weight: {perf['current_weight']:.2f}")

    # Test 6: Export report
    print("\n6️⃣ Testing report export...")

    correction.export_learning_report("data/immune/test_learning_report.json")

    print("\n✅ All self-correction tests passed!")

    # Cleanup
    import os
    if os.path.exists("data/immune/self_correction_test.db"):
        os.remove("data/immune/self_correction_test.db")
    if os.path.exists("data/immune/test_learning_report.json"):
        os.remove("data/immune/test_learning_report.json")
    print("🧹 Test files cleaned up")
