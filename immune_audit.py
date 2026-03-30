#!/usr/bin/env python3
"""
Immune Audit System - Transparency Layer for All Immune Decisions

Provides complete auditability of the immune system with:
- Decision export with full reasoning chains
- Trust evolution tracking across time
- Pattern weight evolution history
- Statistical analysis and reporting
- Human-readable summaries

This ensures the immune system is never a "black box" - every decision can be
traced, explained, and reviewed.
"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import csv


@dataclass
class DecisionAuditEntry:
    """Complete audit entry for a single immune decision."""
    decision_id: int
    timestamp: str
    item_id: str
    item_type: str
    decision: str
    threat_score: float
    confidence: float
    trigger_patterns: List[str]
    reasoning: List[str]
    outcome: Optional[str]
    outcome_evidence: Optional[str]
    domain: str
    domain_trust_at_decision: float

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TrustEvolutionEntry:
    """Trust score change over time for a domain."""
    domain: str
    timestamp: str
    old_score: float
    new_score: float
    delta: float
    reason: str
    event_type: str


@dataclass
class PatternPerformanceReport:
    """Performance metrics for a specific pattern."""
    pattern_id: str
    total_triggers: int
    correct_triggers: int
    false_positive_triggers: int
    false_negative_triggers: int
    current_weight: float
    accuracy_rate: float
    false_positive_rate: float

    def to_dict(self) -> Dict:
        return asdict(self)


class ImmuneAudit:
    """
    Transparency layer that provides complete auditability of immune system decisions.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.immune_dir = self.data_dir / "immune"

        # Database paths
        self.trust_db_path = self.immune_dir / "trust.db"
        self.correction_db_path = self.immune_dir / "self_correction.db"
        self.corroboration_db_path = self.immune_dir / "corroboration.db"

        print(f"✅ Immune audit system initialized")

    def get_recent_decisions(self, limit: int = 50, include_reasoning: bool = True) -> List[DecisionAuditEntry]:
        """
        Get recent immune decisions with full context.

        Args:
            limit: Number of recent decisions to retrieve
            include_reasoning: Include full reasoning chains

        Returns:
            List of DecisionAuditEntry objects
        """
        if not self.correction_db_path.exists():
            return []

        conn = sqlite3.connect(self.correction_db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                decision_id, timestamp, item_id, item_type, decision,
                threat_score, confidence, trigger_patterns_json,
                outcome, outcome_evidence
            FROM decisions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        entries = []
        for row in cursor.fetchall():
            decision_id, timestamp, item_id, item_type, decision, threat_score, \
                confidence, trigger_patterns_json, outcome, outcome_evidence = row

            trigger_patterns = json.loads(trigger_patterns_json) if trigger_patterns_json else []

            # Extract domain from item_id
            domain = "unknown"
            if item_id.startswith("url:"):
                from urllib.parse import urlparse
                parts = item_id.split(":")
                if len(parts) >= 2:
                    try:
                        domain = urlparse(parts[1]).netloc
                    except:
                        pass

            # Get domain trust at time of decision (approximate with current trust)
            domain_trust = self._get_domain_trust(domain)

            # Build reasoning based on patterns
            reasoning = []
            if include_reasoning:
                for pattern in trigger_patterns:
                    reasoning.append(f"Pattern '{pattern}' triggered")
                if threat_score > 0.7:
                    reasoning.append(f"High threat score: {threat_score:.2f}")
                elif threat_score > 0.4:
                    reasoning.append(f"Moderate threat score: {threat_score:.2f}")

            entry = DecisionAuditEntry(
                decision_id=decision_id,
                timestamp=timestamp,
                item_id=item_id,
                item_type=item_type,
                decision=decision,
                threat_score=threat_score,
                confidence=confidence,
                trigger_patterns=trigger_patterns,
                reasoning=reasoning,
                outcome=outcome,
                outcome_evidence=outcome_evidence,
                domain=domain,
                domain_trust_at_decision=domain_trust
            )
            entries.append(entry)

        conn.close()
        return entries

    def get_trust_evolution(self, domain: str, limit: int = 100) -> List[TrustEvolutionEntry]:
        """
        Get trust score evolution for a specific domain.

        Args:
            domain: Domain to query
            limit: Maximum number of events to retrieve

        Returns:
            List of TrustEvolutionEntry objects in chronological order
        """
        if not self.trust_db_path.exists():
            return []

        conn = sqlite3.connect(self.trust_db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT timestamp, old_score, new_score, delta, reason, event_type
            FROM trust_events
            WHERE domain = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (domain, limit))

        entries = []
        for row in cursor.fetchall():
            timestamp, old_score, new_score, delta, reason, event_type = row

            entry = TrustEvolutionEntry(
                domain=domain,
                timestamp=timestamp,
                old_score=old_score,
                new_score=new_score,
                delta=delta,
                reason=reason,
                event_type=event_type
            )
            entries.append(entry)

        conn.close()
        return list(reversed(entries))  # Return chronologically

    def get_pattern_performance(self) -> List[PatternPerformanceReport]:
        """
        Get performance metrics for all patterns.

        Returns:
            List of PatternPerformanceReport objects
        """
        if not self.correction_db_path.exists():
            return []

        conn = sqlite3.connect(self.correction_db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                pattern_id, total_triggers, correct_triggers,
                false_positive_triggers, current_weight
            FROM pattern_performance
            ORDER BY total_triggers DESC
        ''')

        reports = []
        for row in cursor.fetchall():
            pattern_id, total_triggers, correct_triggers, fp_triggers, current_weight = row

            # Calculate rates
            accuracy_rate = correct_triggers / total_triggers if total_triggers > 0 else 0.0
            fp_rate = fp_triggers / total_triggers if total_triggers > 0 else 0.0
            fn_triggers = total_triggers - correct_triggers - fp_triggers

            report = PatternPerformanceReport(
                pattern_id=pattern_id,
                total_triggers=total_triggers,
                correct_triggers=correct_triggers,
                false_positive_triggers=fp_triggers,
                false_negative_triggers=fn_triggers,
                current_weight=current_weight,
                accuracy_rate=accuracy_rate,
                false_positive_rate=fp_rate
            )
            reports.append(report)

        conn.close()
        return reports

    def get_system_health_report(self) -> Dict:
        """
        Get comprehensive health report for the immune system.

        Returns:
            Dictionary with health metrics and status
        """
        health = {
            'timestamp': datetime.utcnow().isoformat(),
            'decisions': {},
            'trust': {},
            'corroboration': {},
            'self_correction': {},
            'overall_status': 'HEALTHY'
        }

        # Decision metrics
        if self.correction_db_path.exists():
            conn = sqlite3.connect(self.correction_db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM decisions')
            total_decisions = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM decisions WHERE outcome IS NOT NULL')
            evaluated_decisions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM decisions WHERE outcome = 'false_positive'")
            false_positives = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM decisions WHERE outcome = 'false_negative'")
            false_negatives = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM decisions WHERE outcome = 'correct'")
            correct_decisions = cursor.fetchone()[0]

            health['decisions'] = {
                'total': total_decisions,
                'evaluated': evaluated_decisions,
                'correct': correct_decisions,
                'false_positives': false_positives,
                'false_negatives': false_negatives,
                'fp_rate': false_positives / evaluated_decisions if evaluated_decisions > 0 else 0.0,
                'fn_rate': false_negatives / evaluated_decisions if evaluated_decisions > 0 else 0.0,
                'accuracy': correct_decisions / evaluated_decisions if evaluated_decisions > 0 else 0.0
            }

            conn.close()

        # Trust metrics
        if self.trust_db_path.exists():
            conn = sqlite3.connect(self.trust_db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM domain_trust')
            total_domains = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM domain_trust WHERE trust_score >= 0.7')
            trusted_domains = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM domain_trust WHERE trust_score <= 0.3')
            untrusted_domains = cursor.fetchone()[0]

            cursor.execute('SELECT AVG(trust_score) FROM domain_trust')
            avg_trust = cursor.fetchone()[0] or 0.5

            health['trust'] = {
                'total_domains': total_domains,
                'trusted_domains': trusted_domains,
                'untrusted_domains': untrusted_domains,
                'average_trust': avg_trust
            }

            conn.close()

        # Corroboration metrics
        if self.corroboration_db_path.exists():
            conn = sqlite3.connect(self.corroboration_db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM fact_clusters')
            total_clusters = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM fact_clusters WHERE ready_to_commit = 1')
            corroborated_clusters = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM fact_sightings')
            total_sightings = cursor.fetchone()[0]

            health['corroboration'] = {
                'total_fact_clusters': total_clusters,
                'corroborated_facts': corroborated_clusters,
                'total_sightings': total_sightings,
                'pending_verification': total_clusters - corroborated_clusters
            }

            conn.close()

        # Determine overall status
        if health['decisions'].get('fp_rate', 0) > 0.1:
            health['overall_status'] = 'WARNING: High false positive rate'
        elif health['decisions'].get('fn_rate', 0) > 0.15:
            health['overall_status'] = 'WARNING: High false negative rate'
        elif health['decisions'].get('evaluated', 0) < 20:
            health['overall_status'] = 'LEARNING: Insufficient data for full evaluation'

        return health

    def export_full_audit(self, output_path: str, format: str = 'json') -> None:
        """
        Export complete audit trail to file.

        Args:
            output_path: Path to output file
            format: 'json' or 'csv'
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Gather all audit data
        audit_data = {
            'generated_at': datetime.utcnow().isoformat(),
            'system_health': self.get_system_health_report(),
            'recent_decisions': [e.to_dict() for e in self.get_recent_decisions(limit=1000)],
            'pattern_performance': [p.to_dict() for p in self.get_pattern_performance()],
            'trust_summary': self._get_trust_summary()
        }

        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(audit_data, f, indent=2)
            print(f"📊 Full audit exported to {output_path} (JSON)")

        elif format == 'csv':
            # Export decisions to CSV
            csv_path = output_path.with_suffix('.csv')
            with open(csv_path, 'w', newline='') as f:
                if audit_data['recent_decisions']:
                    writer = csv.DictWriter(f, fieldnames=audit_data['recent_decisions'][0].keys())
                    writer.writeheader()
                    writer.writerows(audit_data['recent_decisions'])
            print(f"📊 Full audit exported to {csv_path} (CSV)")

    def print_recent_decisions_summary(self, limit: int = 20):
        """Print human-readable summary of recent decisions."""
        decisions = self.get_recent_decisions(limit=limit, include_reasoning=True)

        if not decisions:
            print("No decisions recorded yet")
            return

        print(f"\n{'='*70}")
        print(f"RECENT IMMUNE DECISIONS (Last {limit})")
        print(f"{'='*70}\n")

        for i, dec in enumerate(decisions, 1):
            # Format timestamp
            try:
                dt = datetime.fromisoformat(dec.timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                time_str = dec.timestamp

            # Outcome badge
            outcome_badge = ""
            if dec.outcome == 'correct':
                outcome_badge = "✅"
            elif dec.outcome == 'false_positive':
                outcome_badge = "❌ FP"
            elif dec.outcome == 'false_negative':
                outcome_badge = "❌ FN"
            else:
                outcome_badge = "⏳ pending"

            print(f"{i}. [{time_str}] {dec.decision} {outcome_badge}")
            print(f"   Domain: {dec.domain} (trust: {dec.domain_trust_at_decision:.2f})")
            print(f"   Threat: {dec.threat_score:.2f} | Confidence: {dec.confidence:.2f}")

            if dec.trigger_patterns:
                print(f"   Patterns: {', '.join(dec.trigger_patterns[:3])}")

            if dec.outcome_evidence:
                print(f"   Evidence: {dec.outcome_evidence[:80]}...")

            print()

    def print_pattern_performance_summary(self):
        """Print human-readable summary of pattern performance."""
        patterns = self.get_pattern_performance()

        if not patterns:
            print("No pattern performance data available")
            return

        print(f"\n{'='*70}")
        print(f"PATTERN PERFORMANCE SUMMARY")
        print(f"{'='*70}\n")

        for pattern in patterns:
            if pattern.total_triggers == 0:
                continue

            # Status indicator
            if pattern.accuracy_rate >= 0.9:
                status = "✅ EXCELLENT"
            elif pattern.accuracy_rate >= 0.7:
                status = "✓ GOOD"
            elif pattern.accuracy_rate >= 0.5:
                status = "⚠️ NEEDS TUNING"
            else:
                status = "❌ POOR"

            print(f"{pattern.pattern_id} {status}")
            print(f"  Triggers: {pattern.total_triggers} | Weight: {pattern.current_weight:.2f}")
            print(f"  Accuracy: {pattern.accuracy_rate:.1%} | FP Rate: {pattern.false_positive_rate:.1%}")
            print()

    def print_trust_summary(self, top_n: int = 10):
        """Print summary of most/least trusted domains."""
        trust_data = self._get_trust_summary()

        if not trust_data['domains']:
            print("No trust data available")
            return

        print(f"\n{'='*70}")
        print(f"TRUST SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total domains: {trust_data['total_domains']}")
        print(f"Average trust: {trust_data['average_trust']:.2f}")
        print(f"Trusted (≥0.7): {trust_data['trusted_count']}")
        print(f"Untrusted (≤0.3): {trust_data['untrusted_count']}")

        print(f"\nMost Trusted Domains:")
        for domain, trust in trust_data['most_trusted'][:top_n]:
            print(f"  ✅ {domain}: {trust:.2f}")

        print(f"\nLeast Trusted Domains:")
        for domain, trust in trust_data['least_trusted'][:top_n]:
            print(f"  ⚠️ {domain}: {trust:.2f}")

    def _get_domain_trust(self, domain: str) -> float:
        """Get current trust score for domain."""
        if not self.trust_db_path.exists():
            return 0.5

        conn = sqlite3.connect(self.trust_db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT trust_score FROM domain_trust WHERE domain = ?', (domain,))
        result = cursor.fetchone()

        conn.close()
        return result[0] if result else 0.5

    def _get_trust_summary(self) -> Dict:
        """Get summary statistics for trust scores."""
        if not self.trust_db_path.exists():
            return {
                'total_domains': 0,
                'average_trust': 0.5,
                'trusted_count': 0,
                'untrusted_count': 0,
                'most_trusted': [],
                'least_trusted': [],
                'domains': []
            }

        conn = sqlite3.connect(self.trust_db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*), AVG(trust_score) FROM domain_trust')
        total, avg = cursor.fetchone()

        cursor.execute('SELECT COUNT(*) FROM domain_trust WHERE trust_score >= 0.7')
        trusted_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM domain_trust WHERE trust_score <= 0.3')
        untrusted_count = cursor.fetchone()[0]

        cursor.execute('SELECT domain, trust_score FROM domain_trust ORDER BY trust_score DESC LIMIT 20')
        most_trusted = cursor.fetchall()

        cursor.execute('SELECT domain, trust_score FROM domain_trust ORDER BY trust_score ASC LIMIT 20')
        least_trusted = cursor.fetchall()

        cursor.execute('SELECT domain, trust_score FROM domain_trust')
        all_domains = cursor.fetchall()

        conn.close()

        return {
            'total_domains': total or 0,
            'average_trust': avg or 0.5,
            'trusted_count': trusted_count,
            'untrusted_count': untrusted_count,
            'most_trusted': most_trusted,
            'least_trusted': least_trusted,
            'domains': all_domains
        }


# Testing and CLI usage
if __name__ == "__main__":
    print("🧪 Testing Immune Audit System...")

    audit = ImmuneAudit("data")

    # Test 1: Recent decisions
    print("\n1️⃣ Recent Decisions Summary:")
    audit.print_recent_decisions_summary(limit=10)

    # Test 2: Pattern performance
    print("\n2️⃣ Pattern Performance:")
    audit.print_pattern_performance_summary()

    # Test 3: Trust summary
    print("\n3️⃣ Trust Summary:")
    audit.print_trust_summary(top_n=5)

    # Test 4: System health
    print("\n4️⃣ System Health Report:")
    health = audit.get_system_health_report()
    print(json.dumps(health, indent=2))

    # Test 5: Export audit
    print("\n5️⃣ Exporting Full Audit:")
    audit.export_full_audit("data/immune/audit_export.json", format='json')

    print("\n✅ Audit system tests complete!")
