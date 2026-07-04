#!/usr/bin/env python3
"""
Trust Database - Per-Domain Trust Scoring with Time Decay

SQLite-backed persistent trust scoring system that:
- Tracks trust scores per domain (0.0 to 1.0)
- Starts all domains at 0.5 (neutral)
- Adjusts based on passive observations
- Implements time decay (scores drift toward neutral over time)
- Maintains complete audit trail of all adjustments
- Never actively probes domains

Trust philosophy:
- New domain = neutral (0.5) until proven otherwise
- Trust increases with positive observations
- Trust decreases with negative observations
- Old trust decays to force re-evaluation
- All changes logged with timestamp and reason
"""

import sqlite3
import json
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse


@dataclass
class TrustEvent:
    """Single trust adjustment event."""
    domain: str
    timestamp: str
    old_score: float
    new_score: float
    delta: float
    reason: str
    event_type: str  # 'adjustment', 'decay', 'init', 'override'

    def to_dict(self) -> Dict:
        """Convert to dictionary for export."""
        return asdict(self)


@dataclass
class DomainTrustProfile:
    """Complete trust profile for a domain."""
    domain: str
    current_trust: float
    first_seen: str
    last_updated: str
    last_decayed: str
    adjustment_count: int
    positive_adjustments: int
    negative_adjustments: int
    decay_count: int
    notes: str

    def to_dict(self) -> Dict:
        """Convert to dictionary for export."""
        return asdict(self)


class TrustDatabase:
    """
    Persistent trust scoring database with full audit trail.

    Trust scores range from 0.0 (completely untrusted) to 1.0 (highly trusted).
    Default starting score is 0.5 (neutral).
    """

    def __init__(self, db_path: str = "data/immune/trust.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Trust parameters must be initialized BEFORE _init_database()
        # because _init_database() calls _force_reseed_high_trust which needs these.
        self.max_single_adjustment = 0.2
        self.min_trust = 0.0
        self.max_trust = 1.0
        self.decay_half_life_days = 90
        self.neutral_trust = 0.5

        self._init_database()

    def _init_database(self):
        """Initialize SQLite database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Domain trust table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domain_trust (
                domain TEXT PRIMARY KEY,
                trust_score REAL NOT NULL DEFAULT 0.5,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_decayed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                adjustment_count INTEGER DEFAULT 0,
                positive_adjustments INTEGER DEFAULT 0,
                negative_adjustments INTEGER DEFAULT 0,
                decay_count INTEGER DEFAULT 0,
                notes TEXT DEFAULT ''
            )
        ''')

        # Trust event audit log (immutable history)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trust_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                old_score REAL NOT NULL,
                new_score REAL NOT NULL,
                delta REAL NOT NULL,
                reason TEXT NOT NULL,
                event_type TEXT NOT NULL,
                FOREIGN KEY (domain) REFERENCES domain_trust(domain)
            )
        ''')

        # Indexes for performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_domain_trust
            ON domain_trust(trust_score DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_trust_events_domain
            ON trust_events(domain, timestamp DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_trust_events_timestamp
            ON trust_events(timestamp DESC)
        ''')

        # FORCE RESEED HIGH-TRUST DOMAINS on startup
        self._force_reseed_high_trust(cursor)

        conn.commit()
        conn.close()

        print(f"✅ Trust database initialized: {self.db_path}")

    def _force_reseed_high_trust(self, cursor):
        """Forcefully update trust scores for high-trust domains if they are below the threshold."""
        high_trust_domains = {
            'wikipedia.org': 0.95,
            'wikimedia.org': 0.95,
            'cambridge.org': 0.90,
            'oxford.edu': 0.95,
            'harvard.edu': 0.95,
            'mit.edu': 0.95,
            'stanford.edu': 0.95,
            'utm.edu': 0.90,
            'plato.stanford.edu': 0.95,  # SEP
            'iep.utm.edu': 0.95,        # IEP
            'nature.com': 0.90,
            'science.org': 0.90,
            'arxiv.org': 0.90,
            'github.com': 0.85,
            'stack-overflow.com': 0.85,
            'python.org': 0.90,
            'openai.com': 0.85,
            'anthropic.com': 0.85,
            'google.com': 0.90,
            'microsoft.com': 0.90,
            'apple.com': 0.90
        }

        for domain, target_score in high_trust_domains.items():
            # Check current score
            cursor.execute('SELECT trust_score FROM domain_trust WHERE domain = ?', (domain,))
            row = cursor.fetchone()
            
            if row:
                current_score = row[0]
                if current_score < target_score:
                    # Update existing low-trust score
                    cursor.execute('''
                        UPDATE domain_trust 
                        SET trust_score = ?, notes = 'Startup high-trust re-seed'
                        WHERE domain = ?
                    ''', (target_score, domain))
                    self._log_event(cursor, domain, current_score, target_score, target_score - current_score, 
                                   "Forced re-seed of high-trust domain", 'override')
            else:
                # Initialize fresh
                self._init_domain(cursor, domain)

    def get_trust(self, domain: str) -> float:
        """
        Get current trust score for a domain.

        If domain not seen before, returns neutral (0.5) and creates entry.

        Args:
            domain: Domain name (e.g., 'example.com')

        Returns:
            Trust score (0.0 to 1.0)
        """
        # Normalize domain
        domain = self._normalize_domain(domain)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT trust_score FROM domain_trust
            WHERE domain = ?
        ''', (domain,))

        result = cursor.fetchone()

        if result:
            trust_score = result[0]
        else:
            # First time seeing this domain — initialize with TLD/seed priors
            # and return what was actually seeded (previously returned neutral
            # on first sight even when the seed said otherwise)
            self._init_domain(cursor, domain)
            conn.commit()
            cursor.execute('SELECT trust_score FROM domain_trust WHERE domain = ?', (domain,))
            seeded = cursor.fetchone()
            trust_score = seeded[0] if seeded else self.neutral_trust

        conn.close()
        return trust_score

    def adjust_trust(self, domain: str, delta: float, reason: str) -> None:
        """
        Adjust trust score for a domain and log the change.

        Args:
            domain: Domain name
            delta: Amount to adjust (-1.0 to +1.0)
            reason: Human-readable reason for adjustment
        """
        # Normalize domain
        domain = self._normalize_domain(domain)

        # Clamp delta to max adjustment
        delta = max(-self.max_single_adjustment, min(self.max_single_adjustment, delta))

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get or create domain entry
        cursor.execute('''
            SELECT trust_score FROM domain_trust
            WHERE domain = ?
        ''', (domain,))

        result = cursor.fetchone()

        if result:
            old_score = result[0]
        else:
            old_score = self.neutral_trust
            self._init_domain(cursor, domain)

        # Calculate new score (clamped)
        new_score = max(self.min_trust, min(self.max_trust, old_score + delta))

        # Update domain trust
        cursor.execute('''
            UPDATE domain_trust
            SET trust_score = ?,
                last_updated = CURRENT_TIMESTAMP,
                adjustment_count = adjustment_count + 1,
                positive_adjustments = positive_adjustments + ?,
                negative_adjustments = negative_adjustments + ?
            WHERE domain = ?
        ''', (
            new_score,
            1 if delta > 0 else 0,
            1 if delta < 0 else 0,
            domain
        ))

        # Log event
        self._log_event(cursor, domain, old_score, new_score, delta, reason, 'adjustment')

        conn.commit()
        conn.close()

        print(f"   Trust adjusted for {domain}: {old_score:.2f} → {new_score:.2f} ({reason})")

    def get_audit_trail(self, domain: str, limit: int = 100) -> List[TrustEvent]:
        """
        Get audit trail for a domain (chronological order, newest first).

        Args:
            domain: Domain name
            limit: Maximum number of events to return

        Returns:
            List of TrustEvent objects
        """
        domain = self._normalize_domain(domain)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT domain, timestamp, old_score, new_score, delta, reason, event_type
            FROM trust_events
            WHERE domain = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (domain, limit))

        events = []
        for row in cursor.fetchall():
            events.append(TrustEvent(
                domain=row[0],
                timestamp=row[1],
                old_score=row[2],
                new_score=row[3],
                delta=row[4],
                reason=row[5],
                event_type=row[6]
            ))

        conn.close()
        return events

    def get_domain_profile(self, domain: str) -> Optional[DomainTrustProfile]:
        """
        Get complete trust profile for a domain.

        Args:
            domain: Domain name

        Returns:
            DomainTrustProfile or None if domain not found
        """
        domain = self._normalize_domain(domain)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT domain, trust_score, first_seen, last_updated, last_decayed,
                   adjustment_count, positive_adjustments, negative_adjustments,
                   decay_count, notes
            FROM domain_trust
            WHERE domain = ?
        ''', (domain,))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        return DomainTrustProfile(
            domain=result[0],
            current_trust=result[1],
            first_seen=result[2],
            last_updated=result[3],
            last_decayed=result[4],
            adjustment_count=result[5],
            positive_adjustments=result[6],
            negative_adjustments=result[7],
            decay_count=result[8],
            notes=result[9]
        )

    def decay_old_scores(self, days: int = 30) -> int:
        """
        Apply time decay to trust scores that haven't been updated recently.

        Trust scores drift toward neutral (0.5) over time to force re-evaluation.
        Uses exponential decay: trust(t) = neutral + (trust(0) - neutral) * 0.5^(t/half_life)

        Args:
            days: Apply decay to scores not updated in this many days

        Returns:
            Number of domains decayed
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Find domains that need decay
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        cursor.execute('''
            SELECT domain, trust_score, last_updated
            FROM domain_trust
            WHERE datetime(last_updated) < datetime(?)
            AND trust_score != ?
        ''', (cutoff_date.isoformat(), self.neutral_trust))

        domains_to_decay = cursor.fetchall()

        decayed_count = 0

        for domain, old_score, last_updated in domains_to_decay:
            # Calculate days since last update
            last_update_time = datetime.fromisoformat(last_updated)
            days_elapsed = (datetime.utcnow() - last_update_time).days

            # Calculate decay factor
            decay_factor = 0.5 ** (days_elapsed / self.decay_half_life_days)

            # Calculate new score (exponential decay toward neutral)
            new_score = self.neutral_trust + (old_score - self.neutral_trust) * decay_factor

            # Only update if change is significant (>0.01)
            if abs(new_score - old_score) > 0.01:
                delta = new_score - old_score

                cursor.execute('''
                    UPDATE domain_trust
                    SET trust_score = ?,
                        last_decayed = CURRENT_TIMESTAMP,
                        decay_count = decay_count + 1
                    WHERE domain = ?
                ''', (new_score, domain))

                self._log_event(
                    cursor, domain, old_score, new_score, delta,
                    f"Time decay after {days_elapsed} days of inactivity",
                    'decay'
                )

                decayed_count += 1

        conn.commit()
        conn.close()

        if decayed_count > 0:
            print(f"🕐 Decayed {decayed_count} domain trust scores")

        return decayed_count

    def get_most_trusted(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Get most trusted domains."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT domain, trust_score
            FROM domain_trust
            WHERE trust_score > ?
            ORDER BY trust_score DESC
            LIMIT ?
        ''', (self.neutral_trust, limit))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_least_trusted(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Get least trusted domains."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT domain, trust_score
            FROM domain_trust
            WHERE trust_score < ?
            ORDER BY trust_score ASC
            LIMIT ?
        ''', (self.neutral_trust, limit))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_stats(self) -> Dict:
        """Get overall database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM domain_trust')
        total_domains = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM trust_events')
        total_events = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(trust_score) FROM domain_trust')
        avg_trust = cursor.fetchone()[0] or 0.5

        cursor.execute('SELECT COUNT(*) FROM domain_trust WHERE trust_score > ?', (self.neutral_trust,))
        trusted_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM domain_trust WHERE trust_score < ?', (self.neutral_trust,))
        untrusted_count = cursor.fetchone()[0]

        conn.close()

        return {
            'total_domains': total_domains,
            'total_events': total_events,
            'average_trust': avg_trust,
            'trusted_domains': trusted_count,
            'untrusted_domains': untrusted_count,
            'neutral_domains': total_domains - trusted_count - untrusted_count
        }

    def override_trust(self, domain: str, new_score: float, reason: str) -> None:
        """
        Human override of trust score (logged separately).

        Args:
            domain: Domain name
            new_score: New trust score (0.0 to 1.0)
            reason: Reason for override
        """
        domain = self._normalize_domain(domain)
        new_score = max(self.min_trust, min(self.max_trust, new_score))

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get current score
        cursor.execute('SELECT trust_score FROM domain_trust WHERE domain = ?', (domain,))
        result = cursor.fetchone()

        if result:
            old_score = result[0]
        else:
            old_score = self.neutral_trust
            self._init_domain(cursor, domain)

        delta = new_score - old_score

        # Update trust
        cursor.execute('''
            UPDATE domain_trust
            SET trust_score = ?,
                last_updated = CURRENT_TIMESTAMP,
                notes = ?
            WHERE domain = ?
        ''', (new_score, reason, domain))

        # Log as override event
        self._log_event(cursor, domain, old_score, new_score, delta, reason, 'override')

        conn.commit()
        conn.close()

        print(f"⚠️ Trust override for {domain}: {old_score:.2f} → {new_score:.2f} (human: {reason})")

    def _init_domain(self, cursor, domain: str):
        """Initialize a new domain with specialized trust seeds."""
        initial = self.neutral_trust
        reason = "Initial domain observation"

        # High-trust TLD seeds
        if domain.endswith('.edu') or '.edu.' in domain:
            initial = 0.75
            reason = "Initial domain observation (academic .edu seed)"
        elif domain.endswith('.gov') or '.gov.' in domain:
            initial = 0.80
            reason = "Initial domain observation (government .gov seed)"
        elif domain.endswith('.org') or '.org.' in domain:
            initial = 0.65  # Slightly higher than neutral
            reason = "Initial domain observation (organization .org seed)"

        # Specific high-trust domain seeds
        high_trust_domains = {
            'wikipedia.org': 0.95,
            'wikimedia.org': 0.95,
            'cambridge.org': 0.90,
            'oxford.edu': 0.95,
            'harvard.edu': 0.95,
            'mit.edu': 0.95,
            'stanford.edu': 0.95,
            'utm.edu': 0.90,
            'plato.stanford.edu': 0.95,  # SEP
            'iep.utm.edu': 0.95,        # IEP
            'nature.com': 0.90,
            'science.org': 0.90,
            'arxiv.org': 0.90,
            'github.com': 0.85,
            'stack-overflow.com': 0.85,
            'python.org': 0.90,
            'openai.com': 0.85,
            'anthropic.com': 0.85,
            'google.com': 0.90,
            'microsoft.com': 0.90,
            'apple.com': 0.90
        }

        # Check for exact matches and parent domain matches
        for ht_domain, trust in high_trust_domains.items():
            if domain == ht_domain or domain.endswith('.' + ht_domain):
                initial = trust
                reason = f"Initial domain observation (high-trust seed: {ht_domain})"
                break

        cursor.execute('''
            INSERT OR IGNORE INTO domain_trust (domain, trust_score)
            VALUES (?, ?)
        ''', (domain, initial))

        self._log_event(cursor, domain, initial, initial, 0.0, reason, 'init')

    def _log_event(self, cursor, domain: str, old_score: float, new_score: float,
                   delta: float, reason: str, event_type: str):
        """Log a trust event to the audit trail."""
        cursor.execute('''
            INSERT INTO trust_events (domain, old_score, new_score, delta, reason, event_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (domain, old_score, new_score, delta, reason, event_type))

    def _normalize_domain(self, domain_or_url: str) -> str:
        """
        Normalize domain name from URL or domain string.

        Args:
            domain_or_url: Either 'example.com' or 'https://example.com/path'

        Returns:
            Normalized domain (e.g., 'example.com')
        """
        # If it looks like a URL, parse it
        if '://' in domain_or_url:
            domain = urlparse(domain_or_url).netloc.lower()
        else:
            domain = domain_or_url.lower().strip()

        # www.example.com and example.com are the same publisher — without
        # this, seeded trust for example.com never matches www lookups and
        # the two rows accumulate divergent trust histories
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain


# Testing function
if __name__ == "__main__":
    print("🧪 Testing Trust Database...")

    # Use test database
    test_db = TrustDatabase("data/immune/trust_test.db")

    # Test 1: Get trust for new domain
    print("\n1️⃣ Testing new domain trust...")
    trust1 = test_db.get_trust("example.com")
    print(f"   New domain trust: {trust1:.2f}")
    assert trust1 == 0.5, "New domain should start at neutral (0.5)"

    # Test 2: Adjust trust
    print("\n2️⃣ Testing trust adjustment...")
    test_db.adjust_trust("example.com", 0.1, "Good content observed")
    trust2 = test_db.get_trust("example.com")
    print(f"   After positive adjustment: {trust2:.2f}")
    assert trust2 == 0.6, "Trust should increase to 0.6"

    test_db.adjust_trust("example.com", -0.15, "Suspicious ad patterns")
    trust3 = test_db.get_trust("example.com")
    print(f"   After negative adjustment: {trust3:.2f}")
    assert trust3 == 0.45, "Trust should decrease to 0.45"

    # Test 3: Audit trail
    print("\n3️⃣ Testing audit trail...")
    trail = test_db.get_audit_trail("example.com")
    print(f"   Events logged: {len(trail)}")
    for event in trail:
        print(f"      {event.timestamp[:19]}: {event.old_score:.2f} → {event.new_score:.2f} ({event.reason})")
    assert len(trail) >= 3, "Should have at least 3 events (init + 2 adjustments)"

    # Test 4: Domain profile
    print("\n4️⃣ Testing domain profile...")
    profile = test_db.get_domain_profile("example.com")
    print(f"   Current trust: {profile.current_trust:.2f}")
    print(f"   Adjustments: {profile.adjustment_count} total ({profile.positive_adjustments} positive, {profile.negative_adjustments} negative)")
    assert profile.adjustment_count == 2, "Should have 2 adjustments"

    # Test 5: Time decay
    print("\n5️⃣ Testing time decay...")
    test_db.adjust_trust("old-domain.com", 0.3, "Initial positive observation")
    trust_before_decay = test_db.get_trust("old-domain.com")

    # Manually set last_updated to 60 days ago for testing
    import sqlite3
    conn = sqlite3.connect(test_db.db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE domain_trust
        SET last_updated = datetime('now', '-60 days')
        WHERE domain = 'old-domain.com'
    ''')
    conn.commit()
    conn.close()

    decayed = test_db.decay_old_scores(days=30)
    trust_after_decay = test_db.get_trust("old-domain.com")

    print(f"   Trust before decay: {trust_before_decay:.2f}")
    print(f"   Trust after decay: {trust_after_decay:.2f}")
    print(f"   Domains decayed: {decayed}")
    assert trust_after_decay < trust_before_decay, "Trust should decay toward neutral"
    assert trust_after_decay > 0.5, "Trust should move toward neutral (0.5)"

    # Test 6: Statistics
    print("\n6️⃣ Testing database statistics...")
    stats = test_db.get_stats()
    print(f"   Total domains: {stats['total_domains']}")
    print(f"   Total events: {stats['total_events']}")
    print(f"   Average trust: {stats['average_trust']:.2f}")
    print(f"   Trusted: {stats['trusted_domains']}, Untrusted: {stats['untrusted_domains']}, Neutral: {stats['neutral_domains']}")

    # Test 7: Most/Least trusted
    print("\n7️⃣ Testing trust rankings...")
    test_db.adjust_trust("trusted-site.com", 0.4, "Excellent content")
    test_db.adjust_trust("untrusted-site.com", -0.4, "Suspicious patterns")

    most_trusted = test_db.get_most_trusted(3)
    least_trusted = test_db.get_least_trusted(3)

    print("   Most trusted:")
    for domain, trust in most_trusted:
        print(f"      {domain}: {trust:.2f}")

    print("   Least trusted:")
    for domain, trust in least_trusted:
        print(f"      {domain}: {trust:.2f}")

    # Test 8: Human override
    print("\n8️⃣ Testing human override...")
    test_db.override_trust("example.com", 0.9, "Manually verified as trustworthy")
    trust_after_override = test_db.get_trust("example.com")
    print(f"   Trust after override: {trust_after_override:.2f}")
    assert trust_after_override == 0.9, "Override should set exact trust value"

    # Check override logged correctly
    trail_after_override = test_db.get_audit_trail("example.com", limit=1)
    assert trail_after_override[0].event_type == 'override', "Should log as override event"

    print("\n✅ All trust database tests passed!")

    # Cleanup test database
    import os
    if os.path.exists("data/immune/trust_test.db"):
        os.remove("data/immune/trust_test.db")
        print("🧹 Test database cleaned up")
