#!/usr/bin/env python3
"""
Quarantine Store - Persistent SQLite store for blocked crawl content.

Holds content that was blocked by the immune system or warfare detector,
preserving full context (threat signals, reasoning, trust state, text preview)
so it can be re-evaluated during sleep cycles as Sofia matures.

Lifecycle:  quarantined  →  re_evaluated  →  absorbed | discarded

Design follows the same SQLite pattern as trust.db, corroboration.db,
and self_correction.db in the immune system family.
"""

import sqlite3
import json
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class QuarantineItem:
    """A single quarantined content item."""
    id: int
    url: str
    parent_url: Optional[str]
    status: str                   # quarantined / re_evaluated / absorbed / discarded
    block_source: str             # immune_blocked / warfare_blocked
    block_category: str           # immune_structure, warfare_meta_injection, etc.
    block_signals_json: str       # serialized signal list
    block_reasoning_json: str     # serialized reasoning list
    block_confidence: Optional[float]
    threat_score: Optional[float]
    domain_trust_at_block: Optional[float]
    text_preview: Optional[str]   # up to 500 chars
    full_text_length: Optional[int]
    session_id: Optional[str]
    quarantined_at: str
    re_evaluated_at: Optional[str]
    resolution: Optional[str]     # reasoned label on discard
    resolution_reason: Optional[str]


class QuarantineStore:
    """
    Persistent quarantine store for blocked crawl content.

    Items enter as 'quarantined' and remain until the sleep cycle
    re-evaluates them.  Re-evaluation produces one of:
      - absorbed   (content is safe — re-crawl or commit)
      - discarded  (content confirmed bad — with a reasoned label)
      - keep_quarantined (not yet decidable — try again next cycle)
    """

    # ------------------------------------------------------------------
    # Standard discard categories — structured labels for self-knowledge
    # ------------------------------------------------------------------
    DISCARD_STALE_UNRECOVERED = 'stale_unrecovered'
    DISCARD_CONFIRMED_DANGEROUS = 'confirmed_dangerous'
    DISCARD_LOW_QUALITY = 'low_quality'
    DISCARD_NON_ENGLISH = 'non_english_unreadable'
    DISCARD_DUPLICATE = 'duplicate_content'
    DISCARD_CORRUPTED = 'corrupted_data'

    def __init__(self, db_path: str = "data/immune/quarantine.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _init_database(self):
        """Create tables if they don't exist."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quarantine_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                parent_url TEXT,
                status TEXT NOT NULL DEFAULT 'quarantined',
                block_source TEXT NOT NULL,
                block_category TEXT NOT NULL,
                block_signals_json TEXT NOT NULL DEFAULT '[]',
                block_reasoning_json TEXT NOT NULL DEFAULT '[]',
                block_confidence REAL,
                threat_score REAL,
                domain_trust_at_block REAL,
                text_preview TEXT,
                full_text_length INTEGER,
                session_id TEXT,
                quarantined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                re_evaluated_at TIMESTAMP,
                resolution TEXT,
                resolution_reason TEXT,
                discard_category TEXT
            )
        ''')

        # Migration: add discard_category if table already existed without it
        try:
            cursor.execute('SELECT discard_category FROM quarantine_items LIMIT 0')
        except sqlite3.OperationalError:
            cursor.execute('ALTER TABLE quarantine_items ADD COLUMN discard_category TEXT')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quarantine_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quarantine_item_id INTEGER NOT NULL,
                reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                domain_trust_at_review REAL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                FOREIGN KEY (quarantine_item_id)
                    REFERENCES quarantine_items(id)
            )
        ''')

        # Indexes for common queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_quarantine_status
            ON quarantine_items(status)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_quarantine_url
            ON quarantine_items(url)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_quarantine_block_source
            ON quarantine_items(block_source)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_quarantine_category
            ON quarantine_items(block_category)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_reviews_item
            ON quarantine_reviews(quarantine_item_id)
        ''')

        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Write path — called at block time
    # ------------------------------------------------------------------

    def quarantine_item(self, event: Dict) -> int:
        """
        Ingest a blocked crawl event into quarantine.

        Accepts the enriched event dict that _emit_crawl_event() builds,
        so callers can pass the same data to both JSONL and here.

        Returns the quarantine item id.
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Serialize list/dict fields to JSON strings
        signals = event.get('block_signals') or []
        reasoning = event.get('block_reasoning') or []
        text_preview = event.get('text_preview')

        cursor.execute('''
            INSERT INTO quarantine_items
                (url, parent_url, status, block_source, block_category,
                 block_signals_json, block_reasoning_json,
                 block_confidence, threat_score, domain_trust_at_block,
                 text_preview, full_text_length, session_id, quarantined_at)
            VALUES (?, ?, 'quarantined', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.get('url', ''),
            event.get('parent_url'),
            event.get('status', 'unknown'),         # immune_blocked / warfare_blocked
            event.get('block_category', 'unknown'),
            json.dumps(signals, default=str),
            json.dumps(reasoning, default=str),
            event.get('block_confidence'),
            event.get('threat_score'),
            event.get('domain_trust_at_block'),
            text_preview,
            len(text_preview) if text_preview else None,
            event.get('session_id'),
            event.get('timestamp') or datetime.utcnow().isoformat(),
        ))

        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id

    # ------------------------------------------------------------------
    # Read path — called by sleep cycle re-evaluation
    # ------------------------------------------------------------------

    def get_pending_items(self, limit: int = 100) -> List[Dict]:
        """
        Return quarantined items that are due for re-evaluation.

        Returns oldest-first so the sleep cycle processes the most stale
        items first.
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM quarantine_items
            WHERE status = 'quarantined'
            ORDER BY quarantined_at ASC
            LIMIT ?
        ''', (limit,))

        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items

    def get_item(self, item_id: int) -> Optional[Dict]:
        """Fetch a single quarantine item by id."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM quarantine_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_reviews(self, item_id: int) -> List[Dict]:
        """Fetch all reviews for a quarantine item."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM quarantine_reviews
            WHERE quarantine_item_id = ?
            ORDER BY reviewed_at ASC
        ''', (item_id,))

        reviews = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reviews

    # ------------------------------------------------------------------
    # Resolution path — called during sleep cycle re-evaluation
    # ------------------------------------------------------------------

    def record_review(self, item_id: int, decision: str, reason: str,
                      domain_trust_at_review: Optional[float] = None,
                      discard_category: Optional[str] = None) -> None:
        """
        Record a re-evaluation review for a quarantine item.

        decision:         'keep_quarantined' | 'absorb' | 'discard'
        reason:           human-readable explanation of why
        discard_category: structured label from DISCARD_* constants
                          (required when decision == 'discard')
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Insert the review audit record
        cursor.execute('''
            INSERT INTO quarantine_reviews
                (quarantine_item_id, domain_trust_at_review, decision, reason)
            VALUES (?, ?, ?, ?)
        ''', (item_id, domain_trust_at_review, decision, reason))

        # Update item status if the decision resolves it
        now = datetime.utcnow().isoformat()

        if decision == 'absorb':
            cursor.execute('''
                UPDATE quarantine_items
                SET status = 'absorbed',
                    re_evaluated_at = ?,
                    resolution = 'absorbed',
                    resolution_reason = ?
                WHERE id = ?
            ''', (now, reason, item_id))

        elif decision == 'discard':
            cursor.execute('''
                UPDATE quarantine_items
                SET status = 'discarded',
                    re_evaluated_at = ?,
                    resolution = 'discarded',
                    resolution_reason = ?,
                    discard_category = ?
                WHERE id = ?
            ''', (now, reason, discard_category, item_id))

        elif decision == 'keep_quarantined':
            # Mark that we reviewed it but it stays quarantined
            cursor.execute('''
                UPDATE quarantine_items
                SET re_evaluated_at = ?
                WHERE id = ?
            ''', (now, item_id))

        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Re-evaluation — called during NREM sleep cycle
    # ------------------------------------------------------------------

    # Configurable thresholds
    TRUST_RECOVERY_DELTA = 0.15   # Trust must improve by this much to absorb
    PATTERN_FP_RATE_THRESHOLD = 0.3  # Pattern FP rate above this → absorb
    STALE_AGE_DAYS = 90           # Auto-discard after this many days with no trust recovery

    def review_quarantine(self, trust_db, self_correction,
                          limit: int = 50) -> Dict:
        """
        Re-evaluate pending quarantined items during the NREM sleep cycle.

        For each item, checks:
        1. Trust: Has domain trust improved since block?
        2. Pattern: Has self_correction found the blocking pattern unreliable?
        3. Language: Non-English items stay quarantined (future capability).
        4. Age: Items stale > STALE_AGE_DAYS with no trust recovery → discard.

        Args:
            trust_db: TrustDatabase instance for current domain trust lookups
            self_correction: SelfCorrection instance for pattern performance
            limit: Max items to review per cycle

        Returns:
            Dict with review summary
        """
        from urllib.parse import urlparse

        pending = self.get_pending_items(limit=limit)

        # Pre-fetch pattern performance once
        try:
            accuracy_stats = self_correction.get_accuracy_stats()
            pattern_perf = accuracy_stats.pattern_performance
        except Exception:
            pattern_perf = {}

        results = {
            'items_reviewed': 0,
            'absorbed': 0,
            'discarded': 0,
            'kept_quarantined': 0,
            'details': [],
        }

        for item in pending:
            item_id = item['id']
            url = item['url']
            domain = urlparse(url).netloc
            block_category = item.get('block_category', '')
            trust_at_block = item.get('domain_trust_at_block')
            quarantined_at = item.get('quarantined_at', '')

            results['items_reviewed'] += 1

            # ── Current trust ──
            try:
                current_trust = trust_db.get_trust(domain)
            except Exception:
                current_trust = None

            trust_recovered = (
                current_trust is not None
                and trust_at_block is not None
                and (current_trust - trust_at_block) >= self.TRUST_RECOVERY_DELTA
            )

            # ── Pattern reliability ──
            pattern_unreliable = False
            try:
                signals = json.loads(item.get('block_signals_json', '[]'))
                for sig in signals:
                    pid = sig.get('pattern_id', '')
                    if pid and pid in pattern_perf:
                        perf = pattern_perf[pid]
                        if perf.get('fp_rate', 0) > self.PATTERN_FP_RATE_THRESHOLD:
                            pattern_unreliable = True
                            break
            except Exception:
                pass

            # ── Language check ──
            is_non_english = block_category == 'non_english_content'

            # ── Age check ──
            try:
                q_time = datetime.fromisoformat(quarantined_at)
                age_days = (datetime.utcnow() - q_time).days
            except Exception:
                age_days = 0

            stale = age_days > self.STALE_AGE_DAYS

            # ── Decision ──
            decision = 'keep_quarantined'
            reason = ''
            discard_cat = None

            if is_non_english:
                decision = 'keep_quarantined'
                reason = (f"Non-English content ({block_category}) — "
                          f"awaiting multilingual capability")

            elif trust_recovered and pattern_unreliable:
                decision = 'absorb'
                reason = (f"Domain trust recovered ({trust_at_block:.2f} → "
                          f"{current_trust:.2f}) and blocking pattern has "
                          f"high false-positive rate")

            elif trust_recovered:
                decision = 'absorb'
                reason = (f"Domain trust recovered significantly "
                          f"({trust_at_block:.2f} → {current_trust:.2f})")

            elif pattern_unreliable:
                decision = 'absorb'
                reason = ("Blocking pattern identified as unreliable "
                          f"(FP rate > {self.PATTERN_FP_RATE_THRESHOLD:.0%})")

            elif stale and not trust_recovered:
                decision = 'discard'
                # Pick the right discard category based on what blocked it
                if block_category == 'non_english_content':
                    discard_cat = self.DISCARD_NON_ENGLISH
                    reason = (f"Non-English content — unreadable after "
                              f"{age_days} days, no multilingual capability yet")
                elif item.get('block_source') == 'warfare_blocked':
                    discard_cat = self.DISCARD_CONFIRMED_DANGEROUS
                    reason = (f"Warfare pattern confirmed — {age_days} days "
                              f"quarantined, no trust recovery, original threat "
                              f"score {item.get('threat_score', '?')}")
                elif block_category in ('immune_quality', 'immune_source'):
                    discard_cat = self.DISCARD_LOW_QUALITY
                    reason = (f"Low quality / untrusted source — {age_days} days "
                              f"with no trust recovery (was {trust_at_block})")
                else:
                    discard_cat = self.DISCARD_STALE_UNRECOVERED
                    reason = (f"Stale quarantine — {age_days} days with no "
                              f"trust recovery (threshold: {self.STALE_AGE_DAYS} days)")

            # ── Record ──
            self.record_review(
                item_id, decision, reason,
                domain_trust_at_review=current_trust,
                discard_category=discard_cat,
            )

            if decision == 'absorb':
                results['absorbed'] += 1
            elif decision == 'discard':
                results['discarded'] += 1
            else:
                results['kept_quarantined'] += 1

            results['details'].append({
                'id': item_id,
                'url': url[:80],
                'decision': decision,
                'reason': reason,
                'discard_category': discard_cat,
            })

        return results

    # ------------------------------------------------------------------
    # Statistics — for dashboards and audits
    # ------------------------------------------------------------------

    def get_statistics(self) -> Dict:
        """Return summary statistics about the quarantine store."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute('SELECT status, COUNT(*) FROM quarantine_items GROUP BY status')
        status_counts = dict(cursor.fetchall())

        cursor.execute('SELECT block_source, COUNT(*) FROM quarantine_items GROUP BY block_source')
        source_counts = dict(cursor.fetchall())

        cursor.execute('SELECT block_category, COUNT(*) FROM quarantine_items GROUP BY block_category')
        category_counts = dict(cursor.fetchall())

        cursor.execute('SELECT COUNT(*) FROM quarantine_reviews')
        total_reviews = cursor.fetchone()[0]

        conn.close()

        return {
            'by_status': status_counts,
            'by_source': source_counts,
            'by_category': category_counts,
            'total_reviews': total_reviews,
            'total_items': sum(status_counts.values()),
            'pending': status_counts.get('quarantined', 0),
        }

    def get_discard_statistics(self) -> Dict:
        """
        Return discard statistics grouped by category — Sofia's
        self-knowledge about what she's filtering and why.

        Example output:
        {
            'total_discarded': 12,
            'by_category': {
                'stale_unrecovered': 5,
                'confirmed_dangerous': 3,
                'low_quality': 2,
                'non_english_unreadable': 2,
            },
            'by_block_source': {
                'immune_blocked': 7,
                'warfare_blocked': 3,
                'non_english': 2,
            },
            'recent_discards': [
                {'url': '...', 'discard_category': '...', 'reason': '...', 'at': '...'},
            ]
        }
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM quarantine_items WHERE status = 'discarded'
        ''')
        total = cursor.fetchone()[0]

        cursor.execute('''
            SELECT discard_category, COUNT(*) as cnt
            FROM quarantine_items
            WHERE status = 'discarded' AND discard_category IS NOT NULL
            GROUP BY discard_category
            ORDER BY cnt DESC
        ''')
        by_category = dict(cursor.fetchall())

        cursor.execute('''
            SELECT block_source, COUNT(*) as cnt
            FROM quarantine_items
            WHERE status = 'discarded'
            GROUP BY block_source
            ORDER BY cnt DESC
        ''')
        by_source = dict(cursor.fetchall())

        cursor.execute('''
            SELECT url, discard_category, resolution_reason, re_evaluated_at
            FROM quarantine_items
            WHERE status = 'discarded'
            ORDER BY re_evaluated_at DESC
            LIMIT 10
        ''')
        recent = [
            {
                'url': row['url'][:80],
                'discard_category': row['discard_category'],
                'reason': row['resolution_reason'],
                'at': row['re_evaluated_at'],
            }
            for row in cursor.fetchall()
        ]

        conn.close()

        return {
            'total_discarded': total,
            'by_category': by_category,
            'by_block_source': by_source,
            'recent_discards': recent,
        }
