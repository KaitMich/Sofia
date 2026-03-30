"""
Bridge Memory Reclassification System

Purpose: Move items OUT of bridge memory when accumulated context
provides enough evidence to classify them as Logic or Symbolic.

Design Philosophy:
- Bridge is TEMPORARY staging, not permanent storage
- Items escape via "cluster gravity" - when surrounded by clear neighbors
- Three gates must pass: TIME (7 days), CONTEXT (5+ items), GRAVITY (70%)

Created: 2025-11-24
Author: Claude Code
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BridgeReclassifier:
    """
    Handles periodic review and reclassification of bridge memory items.

    Algorithm: Cluster Gravity
    - Instead of recalculating an item's own ratio, we look at WHERE
      related items live (Logic vs Symbolic memory)
    - If 70%+ of related items are in one memory type, the bridge item
      gets "pulled" into that memory
    """

    # Configuration
    MIN_AGE_DAYS = 7           # Gate 1: Must be in bridge at least this long
    MIN_RELATED_ITEMS = 5      # Gate 2: Must have this many related neighbors
    DOMINANCE_THRESHOLD = 0.70 # Gate 3: Cluster must be 70%+ one type

    def __init__(self, unified_memory, config_path: str = "data/bridge_reclassification_config.json"):
        """
        Initialize with reference to unified memory system.

        Args:
            unified_memory: Instance of UnifiedMemory class
            config_path: Path to configuration file (optional)
        """
        self.memory = unified_memory
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.log_path = Path(self.config.get('log_file', 'data/bridge_reclassification_log.json'))

    def _load_config(self) -> Dict:
        """Load configuration or return defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load config: {e}, using defaults")

        return {
            "enabled": True,
            "min_age_days": self.MIN_AGE_DAYS,
            "min_related_items": self.MIN_RELATED_ITEMS,
            "dominance_threshold": self.DOMINANCE_THRESHOLD,
            "max_reclassifications_per_review": 10,
            "log_file": "data/bridge_reclassification_log.json"
        }

    def find_related_content(self, bridge_item: Dict) -> List[Dict]:
        """
        Find items in Logic and Symbolic memory related to this bridge item.

        Strategy: Keyword overlap (simple but effective)
        - Extract significant words from bridge item
        - Find items in Logic/Symbolic with 2+ matching keywords
        - Tag each result with its source memory type

        Args:
            bridge_item: The bridge memory item to find relations for

        Returns:
            List of related items, each tagged with 'memory_type': 'logic'|'symbolic'
        """
        related = []

        # Extract keywords from bridge item (simple approach)
        bridge_text = bridge_item.get('text', '').lower()
        bridge_keywords = self._extract_keywords(bridge_text)

        if len(bridge_keywords) < 2:
            return []  # Not enough keywords to match

        # Search Logic memory
        for item in self.memory.logic_memory:
            item_text = item.get('text', '').lower()
            item_keywords = self._extract_keywords(item_text)
            overlap = len(bridge_keywords & item_keywords)
            if overlap >= 2:
                related.append({
                    **item,
                    'memory_type': 'logic',
                    'keyword_overlap': overlap
                })

        # Search Symbolic memory
        for item in self.memory.symbolic_memory:
            item_text = item.get('text', '').lower()
            item_keywords = self._extract_keywords(item_text)
            overlap = len(bridge_keywords & item_keywords)
            if overlap >= 2:
                related.append({
                    **item,
                    'memory_type': 'symbolic',
                    'keyword_overlap': overlap
                })

        return related

    def _extract_keywords(self, text: str) -> set:
        """
        Extract significant keywords from text.
        Filters out common stopwords, keeps meaningful terms.
        """
        # Common words to ignore
        stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'this', 'that', 'these', 'those', 'what',
            'which', 'who', 'whom', 'i', 'me', 'my', 'myself', 'we',
            'our', 'ours', 'you', 'your', 'he', 'him', 'his', 'she',
            'her', 'it', 'its', 'they', 'them', 'their', 'about'
        }

        # Simple tokenization
        words = text.lower().split()
        # Remove punctuation and filter
        keywords = set()
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if clean and len(clean) > 2 and clean not in stopwords:
                keywords.add(clean)

        return keywords

    def evaluate_bridge_item(self, item: Dict, related_items: List[Dict]) -> Tuple[bool, Optional[str], str]:
        """
        Evaluate whether a bridge item should be reclassified using Cluster Gravity.

        Three gates must pass:
        1. TIME: Item must be in bridge >= MIN_AGE_DAYS
        2. CONTEXT: Must have >= MIN_RELATED_ITEMS neighbors
        3. GRAVITY: Cluster must be >= DOMINANCE_THRESHOLD one type

        Args:
            item: The bridge memory item
            related_items: List of related items from find_related_content()

        Returns:
            Tuple of (should_reclassify, target_memory, reason)
            target_memory is 'LOGIC', 'SYMBOLIC', or None
        """
        # GATE 1: TIME CHECK
        item_timestamp = item.get('timestamp')
        if item_timestamp:
            try:
                item_date = datetime.fromisoformat(item_timestamp.replace('Z', '+00:00'))
                age_days = (datetime.now(item_date.tzinfo) - item_date).days
            except:
                age_days = 0
        else:
            age_days = 0

        min_age = self.config.get('min_age_days', self.MIN_AGE_DAYS)
        if age_days < min_age:
            return False, None, f"Too recent ({age_days}/{min_age} days - incubating)"

        # GATE 2: CONTEXT CHECK
        min_related = self.config.get('min_related_items', self.MIN_RELATED_ITEMS)
        if len(related_items) < min_related:
            return False, None, f"Insufficient context ({len(related_items)}/{min_related} related items)"

        # GATE 3: CLUSTER GRAVITY CHECK
        logic_neighbors = sum(1 for r in related_items if r.get('memory_type') == 'logic')
        symbolic_neighbors = sum(1 for r in related_items if r.get('memory_type') == 'symbolic')
        total = logic_neighbors + symbolic_neighbors

        if total == 0:
            return False, None, "No valid neighbors found"

        logic_dominance = logic_neighbors / total
        symbolic_dominance = symbolic_neighbors / total

        threshold = self.config.get('dominance_threshold', self.DOMINANCE_THRESHOLD)

        if logic_dominance >= threshold:
            return True, "LOGIC", f"Cluster gravity: {logic_dominance:.0%} Logic neighbors ({logic_neighbors}/{total})"
        elif symbolic_dominance >= threshold:
            return True, "SYMBOLIC", f"Cluster gravity: {symbolic_dominance:.0%} Symbolic neighbors ({symbolic_neighbors}/{total})"

        return False, None, f"Split cluster ({logic_dominance:.0%} Logic / {symbolic_dominance:.0%} Symbolic)"

    def review_bridge_memory(self, dry_run: bool = True) -> Dict:
        """
        Main entry point: Review all bridge items and reclassify eligible ones.

        Args:
            dry_run: If True, only report what would happen without making changes

        Returns:
            Dict with review statistics and details
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': dry_run,
            'items_reviewed': 0,
            'items_ready': 0,
            'items_reclassified': 0,
            'to_logic': 0,
            'to_symbolic': 0,
            'items_remaining': 0,
            'details': [],
            'errors': []
        }

        bridge_items = list(self.memory.bridge_memory)  # Copy to avoid modification during iteration
        results['items_reviewed'] = len(bridge_items)

        max_reclassify = self.config.get('max_reclassifications_per_review', 10)
        reclassified_count = 0

        for item in bridge_items:
            if reclassified_count >= max_reclassify:
                break

            try:
                # Find related content
                related = self.find_related_content(item)

                # Evaluate for reclassification
                should_move, target, reason = self.evaluate_bridge_item(item, related)

                detail = {
                    'id': item.get('id', 'unknown'),
                    'text_preview': item.get('text', '')[:50] + '...',
                    'related_count': len(related),
                    'should_reclassify': should_move,
                    'target': target,
                    'reason': reason
                }

                if should_move:
                    results['items_ready'] += 1

                    if not dry_run:
                        # Actually move the item
                        success = self.memory.move_item_from_bridge(item, target, reason)
                        if success:
                            results['items_reclassified'] += 1
                            reclassified_count += 1
                            if target == 'LOGIC':
                                results['to_logic'] += 1
                            else:
                                results['to_symbolic'] += 1
                            detail['reclassified'] = True
                        else:
                            detail['reclassified'] = False
                            detail['error'] = "Move operation failed"
                            results['errors'].append(f"Failed to move {item.get('id')}")
                    else:
                        detail['reclassified'] = False
                        detail['would_reclassify'] = True

                results['details'].append(detail)

            except Exception as e:
                results['errors'].append(f"Error processing {item.get('id', 'unknown')}: {str(e)}")

        # Count remaining
        results['items_remaining'] = len(self.memory.bridge_memory)

        # Log results
        self._log_review(results)

        return results

    def _log_review(self, results: Dict):
        """Append review results to log file."""
        try:
            # Load existing log
            if self.log_path.exists():
                with open(self.log_path, 'r') as f:
                    log = json.load(f)
            else:
                log = {'reviews': []}

            # Append new review
            log['reviews'].append(results)

            # Trim if too long
            max_entries = self.config.get('max_log_entries', 1000)
            if len(log['reviews']) > max_entries:
                log['reviews'] = log['reviews'][-max_entries:]

            # Save
            with open(self.log_path, 'w') as f:
                json.dump(log, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log review: {e}")


# Convenience function for external use
def run_bridge_review(dry_run: bool = True) -> Dict:
    """
    Run a bridge memory review.

    Args:
        dry_run: If True, only report what would happen

    Returns:
        Review results dictionary
    """
    from unified_memory import get_unified_memory

    memory = get_unified_memory()
    reclassifier = BridgeReclassifier(memory)
    return reclassifier.review_bridge_memory(dry_run=dry_run)
