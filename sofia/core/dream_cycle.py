# dream_cycle.py - Sleep Cycle System for Memory Consolidation
"""
Dream Cycle System - Memory Consolidation During Idle Periods

Implements biological sleep architecture:
- NREM Phase (Deep Sleep): Stabilization via bridge reclassification
- REM Phase (Dream Sleep): Integration via distant connection discovery

This system transforms raw memories into wisdom through two distinct phases,
mimicking the human sleep cycle.

Created: 2025-12-30
Author: Claude Code
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import logging

# Import existing systems
from sofia.memory.bridge_reclassifier import BridgeReclassifier
from sofia.core.unified_memory import get_unified_memory
from sofia.core.value_formation import ValueFormation
from sofia.security.quarantine_store import QuarantineStore
from sofia.security.trust_database import TrustDatabase
from sofia.security.self_correction import SelfCorrection

logger = logging.getLogger(__name__)


class DreamCycleOrchestrator:
    """
    Orchestrates the sleep cycle for memory consolidation.

    Phases:
    1. NREM (Deep Sleep): Stabilize bridge memories into permanent storage
    2. REM (Dream Sleep): Generate insights from distant connections
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.unified_memory = get_unified_memory(data_dir=str(data_dir))

        # Initialize subsystems
        self.bridge_reclassifier = BridgeReclassifier(self.unified_memory)

        # Quarantine re-evaluation (immune system components)
        self.quarantine_store = QuarantineStore(f"{data_dir}/immune/quarantine.db")
        self.trust_db = TrustDatabase(f"{data_dir}/immune/trust.db")
        self.self_correction = SelfCorrection(f"{data_dir}/immune/self_correction.db")

        # Initialize value formation for insight assessment
        try:
            self.value_formation = ValueFormation(data_dir=str(data_dir))
        except Exception as e:
            logger.warning(f"Value formation system unavailable: {e}")
            self.value_formation = None

        # Configuration
        self.config = self._load_config()
        self.log_path = self.data_dir / "sleep_cycle_log.json"
        self.insights_path = self.data_dir / "insights_generated.json"

    def _load_config(self) -> Dict:
        """Load configuration or return defaults."""
        config_path = self.data_dir / "dream_cycle_config.json"

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load config: {e}, using defaults")

        return {
            "rem_similarity_threshold": 0.35,
            "rem_max_insights_per_cycle": 3,
            "rem_memory_lookback_hours": 24,
            "rem_sweet_spot_min": 0.3,
            "rem_sweet_spot_max": 0.65,
            "insight_strength_threshold": 0.6,
            "enable_value_integration": True
        }

    def run_sleep_cycle(self) -> Dict[str, Any]:
        """
        Run a complete sleep cycle (NREM + REM phases).

        Returns:
            Dict with results from both phases
        """
        cycle_start = datetime.utcnow()

        print("\n💤 Sleep Cycle Beginning...")
        print(f"   Time: {cycle_start.strftime('%Y-%m-%d %H:%M:%S UTC')}")

        results = {
            'cycle_start': cycle_start.isoformat(),
            'cycle_end': None,
            'duration_seconds': 0,
            'nrem_results': {},
            'rem_results': {},
            'total_consolidations': 0,
            'total_insights': 0,
            'values_affected': 0
        }

        # Phase 1: NREM (Deep Sleep) - Stabilization
        print("\n🌙 Phase 1: NREM (Deep Sleep) - Stabilization")
        nrem_results = self.nrem_phase()
        results['nrem_results'] = nrem_results
        results['total_consolidations'] = nrem_results.get('items_reclassified', 0)

        # Phase 2: REM (Dream Sleep) - Integration
        print("\n✨ Phase 2: REM (Dream Sleep) - Integration")
        rem_results = self.rem_phase()
        results['rem_results'] = rem_results
        results['total_insights'] = rem_results.get('insights_generated', 0)
        results['values_affected'] = rem_results.get('values_affected', 0)

        # Finalize
        cycle_end = datetime.utcnow()
        results['cycle_end'] = cycle_end.isoformat()
        results['duration_seconds'] = (cycle_end - cycle_start).total_seconds()

        # Quarantine summary
        q_review = nrem_results.get('quarantine_review', {})
        results['quarantine_absorbed'] = q_review.get('absorbed', 0)
        results['quarantine_discarded'] = q_review.get('discarded', 0)

        print(f"\n💤 Sleep Cycle Complete")
        print(f"   Duration: {results['duration_seconds']:.1f}s")
        print(f"   Memories stabilized: {results['total_consolidations']}")
        print(f"   Insights generated: {results['total_insights']}")
        print(f"   Values affected: {results['values_affected']}")
        q_total = results['quarantine_absorbed'] + results['quarantine_discarded']
        if q_total > 0:
            print(f"   Quarantine resolved: {q_total} "
                  f"({results['quarantine_absorbed']} absorbed, "
                  f"{results['quarantine_discarded']} discarded)")

        # Log cycle
        self._log_sleep_cycle(results)

        return results

    def nrem_phase(self) -> Dict[str, Any]:
        """
        NREM Phase: Deep Sleep - Memory Stabilization

        Reclassifies bridge memories into permanent Logic or Symbolic storage
        using the existing BridgeReclassifier system.

        Returns:
            Dict with reclassification results
        """
        print("  [NREM] Reviewing bridge memory for stabilization...")

        # Delegate to existing bridge reclassifier
        results = self.bridge_reclassifier.review_bridge_memory(dry_run=False)

        # Log results
        items_reclassified = results.get('items_reclassified', 0)
        to_logic = results.get('to_logic', 0)
        to_symbolic = results.get('to_symbolic', 0)
        remaining = results.get('items_remaining', 0)

        if items_reclassified > 0:
            print(f"  [NREM] ✅ Stabilized {items_reclassified} memories:")
            print(f"    → {to_logic} consolidated to Logic Memory")
            print(f"    → {to_symbolic} consolidated to Symbolic Memory")
        else:
            print(f"  [NREM] No memories ready for stabilization")

        print(f"  [NREM] Bridge memory status: {remaining} items remaining")

        # ── Quarantine Re-evaluation ──
        print("  [NREM] Reviewing quarantined content...")
        try:
            q_results = self.quarantine_store.review_quarantine(
                self.trust_db, self.self_correction
            )
            q_reviewed = q_results.get('items_reviewed', 0)
            q_absorbed = q_results.get('absorbed', 0)
            q_discarded = q_results.get('discarded', 0)
            q_kept = q_results.get('kept_quarantined', 0)

            if q_reviewed > 0:
                print(f"  [NREM] 🔍 Quarantine review: {q_reviewed} items evaluated")
                if q_absorbed > 0:
                    print(f"    → {q_absorbed} absorbed (safe for re-processing)")
                if q_discarded > 0:
                    print(f"    → {q_discarded} discarded (with reasoned labels)")
                if q_kept > 0:
                    print(f"    → {q_kept} kept quarantined (re-check next cycle)")
            else:
                print(f"  [NREM] No quarantined items pending review")

            results['quarantine_review'] = q_results
        except Exception as e:
            logger.warning(f"Quarantine review failed: {e}")
            print(f"  [NREM] ⚠️ Quarantine review skipped: {e}")
            results['quarantine_review'] = {'error': str(e)}

        return results

    def rem_phase(self) -> Dict[str, Any]:
        """
        REM Phase: Dream Sleep - Pattern Integration

        Finds distant connections between memories and generates insights
        when non-obvious patterns emerge.

        Returns:
            Dict with insight generation results
        """
        results = {
            'memories_sampled': 0,
            'distant_connections_found': 0,
            'insights_generated': 0,
            'insights_created': [],
            'values_affected': 0,
            'patterns_discovered': []
        }

        print("  [REM] Searching for distant connections in memory...")

        # Step 1: Get recent emotional memories (last 24 hours)
        recent_memories = self._get_recent_emotional_memories()

        if not recent_memories:
            print("  [REM] No recent emotional memories to process")
            return results

        # Select 1 random memory as seed
        seed_memory = random.choice(recent_memories)
        results['memories_sampled'] = 1

        seed_preview = seed_memory.get('text', '')[:60] + '...'
        print(f"  [REM] Seed memory: \"{seed_preview}\"")

        # Step 2: Find distant connections
        distant_connections = self._find_distant_connections(seed_memory)
        results['distant_connections_found'] = len(distant_connections)

        print(f"  [REM] Found {len(distant_connections)} distant neighbors")

        if not distant_connections:
            print("  [REM] No distant connections found")
            return results

        # Step 3: Generate insights from connections
        max_insights = self.config.get('rem_max_insights_per_cycle', 3)
        insights_generated = 0

        for similarity_score, distant_memory in distant_connections:
            if insights_generated >= max_insights:
                break

            # Evaluate insight potential
            insight = self._evaluate_insight_potential(
                seed_memory,
                distant_memory,
                similarity_score
            )

            if insight and insight.get('strength', 0) >= self.config.get('insight_strength_threshold', 0.6):
                # Generate and store insight
                success = self._generate_insight_symbol(insight)

                if success:
                    insights_generated += 1
                    results['insights_created'].append(insight['title'])
                    results['patterns_discovered'].append(insight.get('pattern', 'unknown'))

                    print(f"  [REM] ✨ Insight {insights_generated}: {insight['title']}")
                    print(f"         Pattern: {insight.get('pattern', 'N/A')}")
                    print(f"         Strength: {insight.get('strength', 0):.2f}")

                    # Step 4: Value Integration (NEW REQUIREMENT)
                    if self.config.get('enable_value_integration', True):
                        values_affected = self._integrate_insight_with_values(insight)
                        results['values_affected'] += values_affected

                        if values_affected > 0:
                            print(f"         Values affected: {values_affected}")

        results['insights_generated'] = insights_generated

        if insights_generated == 0:
            print("  [REM] No significant patterns discovered this cycle")

        return results

    def _get_recent_emotional_memories(self) -> List[Dict]:
        """
        Get memories from the last N hours that have emotional significance.

        Returns:
            List of memory items with emotions
        """
        lookback_hours = self.config.get('rem_memory_lookback_hours', 24)
        cutoff_time = datetime.utcnow() - timedelta(hours=lookback_hours)

        recent_emotional = []

        # Search across all memory types
        all_memories = (
            self.unified_memory.tripartite.logic_memory +
            self.unified_memory.tripartite.symbolic_memory +
            self.unified_memory.tripartite.bridge_memory
        )

        for memory in all_memories:
            # Check timestamp
            timestamp_str = memory.get('timestamp')
            if timestamp_str:
                try:
                    memory_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if memory_time.replace(tzinfo=None) < cutoff_time:
                        continue
                except:
                    continue

            # Check for emotions
            emotions = memory.get('emotions', {})
            if emotions and len(emotions) > 0:
                # Calculate emotional intensity
                max_emotion = max(emotions.values()) if emotions else 0
                if max_emotion > 0.5:  # Significant emotion
                    recent_emotional.append(memory)

        return recent_emotional

    def _find_distant_connections(self, seed_memory: Dict) -> List[Tuple[float, Dict]]:
        """
        Find distant (non-obvious) connections to a seed memory.

        Uses low similarity threshold to find memories in the "sweet spot"
        of being related but not obviously so.

        Args:
            seed_memory: The memory to find connections for

        Returns:
            List of (similarity_score, memory) tuples
        """
        seed_text = seed_memory.get('text', '')

        if not seed_text:
            return []

        # Use low threshold to cast a wide net
        threshold = self.config.get('rem_similarity_threshold', 0.35)

        all_similar = self.unified_memory.retrieve_similar_vectors(
            query_text=seed_text,
            top_n=20,
            similarity_threshold=threshold
        )

        # Filter to "sweet spot" - related but not obvious
        sweet_spot_min = self.config.get('rem_sweet_spot_min', 0.3)
        sweet_spot_max = self.config.get('rem_sweet_spot_max', 0.65)

        distant_connections = [
            (score, memory) for score, memory in all_similar
            if sweet_spot_min <= score <= sweet_spot_max
        ]

        # Filter out the seed memory itself
        seed_id = seed_memory.get('id')
        if seed_id:
            distant_connections = [
                (score, memory) for score, memory in distant_connections
                if memory.get('id') != seed_id
            ]

        return distant_connections

    def _evaluate_insight_potential(self, memory_a: Dict, memory_b: Dict,
                                    similarity_score: float) -> Optional[Dict]:
        """
        Evaluate whether two memories can form a meaningful insight.

        Args:
            memory_a: First memory
            memory_b: Second memory (distant connection)
            similarity_score: Vector similarity between them

        Returns:
            Dict with insight details if strong enough, None otherwise
        """
        # Extract key information
        text_a = memory_a.get('text', '')
        text_b = memory_b.get('text', '')

        keywords_a = memory_a.get('keywords', [])
        keywords_b = memory_b.get('keywords', [])

        # Check for cross-domain pattern
        # If memories are from different decision types, that's interesting
        type_a = memory_a.get('decision_type', 'unknown')
        type_b = memory_b.get('decision_type', 'unknown')

        is_cross_domain = type_a != type_b

        # Extract emotions
        emotions_a = memory_a.get('emotions', {})
        emotions_b = memory_b.get('emotions', {})

        # Find common themes
        keywords_set_a = set(keywords_a)
        keywords_set_b = set(keywords_b)
        common_keywords = keywords_set_a & keywords_set_b
        unique_a = keywords_set_a - keywords_set_b
        unique_b = keywords_set_b - keywords_set_a

        # Calculate insight strength
        strength = similarity_score

        # Boost if cross-domain
        if is_cross_domain:
            strength += 0.15

        # Boost if has common keywords (pattern indicator)
        if len(common_keywords) >= 2:
            strength += 0.1

        # Create pattern description
        if is_cross_domain and common_keywords:
            pattern_keywords = list(common_keywords)[:2]
            pattern = f"Cross-domain pattern: {' + '.join(pattern_keywords)} appears in both {type_a} and {type_b}"
        elif common_keywords:
            pattern = f"Recurring theme: {', '.join(list(common_keywords)[:3])}"
        else:
            pattern = f"Distant semantic connection (similarity: {similarity_score:.2f})"

        # Generate insight title
        # Pick key concepts from each memory
        concept_a = keywords_a[0] if keywords_a else "Concept A"
        concept_b = keywords_b[0] if keywords_b else "Concept B"

        title = f"Dream Insight: {concept_a.title()} + {concept_b.title()}"

        insight = {
            'title': title,
            'pattern': pattern,
            'strength': strength,
            'memory_a_id': memory_a.get('id'),
            'memory_b_id': memory_b.get('id'),
            'memory_a_preview': text_a[:100],
            'memory_b_preview': text_b[:100],
            'common_keywords': list(common_keywords),
            'cross_domain': is_cross_domain,
            'similarity_score': similarity_score,
            'timestamp': datetime.utcnow().isoformat()
        }

        return insight

    def _generate_insight_symbol(self, insight: Dict) -> bool:
        """
        Create a new symbolic memory entry for the insight.

        Args:
            insight: Insight details from evaluation

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current phase for context
            current_phase = 1
            if self.unified_memory.tripartite.logic_memory:
                current_phase = self.unified_memory.tripartite.logic_memory[0].get('processing_phase', 1)

            # Create symbolic memory item
            insight_item = {
                'id': f"insight_{int(datetime.utcnow().timestamp() * 1000)}",
                'text': f"{insight['title']}: {insight['pattern']}. "
                        f"Connects: \"{insight['memory_a_preview']}\" "
                        f"with \"{insight['memory_b_preview']}\"",
                'source_url': None,
                'logic_score': 0.3,  # Insights are primarily symbolic
                'symbolic_score': 0.8,
                'confidence': insight['strength'],
                'processing_phase': current_phase,
                'storage_phase': current_phase,
                'is_shallow': False,
                'is_highly_relevant': True,
                'timestamp': insight['timestamp'],
                'content_type': 'dream_insight',
                'emotions': {'curiosity': 0.7, 'wonder': 0.6},  # Insights evoke curiosity
                'symbols_found': 0,
                'symbols_list': [],
                'keywords': insight.get('common_keywords', []),
                'decision_type': 'FOLLOW_SYMBOLIC',
                'origin': 'rem_integration',
                'insight_metadata': {
                    'strength': insight['strength'],
                    'pattern': insight['pattern'],
                    'cross_domain': insight.get('cross_domain', False),
                    'connected_memories': [
                        insight.get('memory_a_id'),
                        insight.get('memory_b_id')
                    ]
                }
            }

            # Store to symbolic memory
            self.unified_memory.tripartite.symbolic_memory.append(insight_item)
            self.unified_memory.tripartite.save_all()

            # Log to insights file
            self._log_insight(insight)

            return True

        except Exception as e:
            logger.error(f"Failed to generate insight symbol: {e}")
            return False

    def _integrate_insight_with_values(self, insight: Dict) -> int:
        """
        Integrate insight with value formation system.

        Treats the insight as a high-significance "Growth" experience
        and triggers value formation to assess it.

        Args:
            insight: The generated insight

        Returns:
            Number of values affected
        """
        if not self.value_formation:
            return 0

        try:
            # Create an experience proxy for the insight
            experience_proxy = type('obj', (object,), {
                'id': f"insight_exp_{int(datetime.utcnow().timestamp() * 1000)}",
                'content': {
                    'text': f"{insight['title']}: {insight['pattern']}",
                    'content_type': 'dream_insight',
                    'source_url': None
                },
                'outcome_assessment': {
                    # High quality for insights
                    'quality_score': insight.get('strength', 0.8),

                    # Map to "Growth" significance (insights are learning moments)
                    'personal_significance_score': 0.9,

                    # Extract insights from pattern
                    'insights_gained': [insight['pattern']] + insight.get('common_keywords', []),

                    # Emphasize growth aspect
                    'personal_significance': f"Dream insight revealing pattern: {insight['pattern']}"
                },
                'interaction_data': {
                    'decision_type': 'FOLLOW_SYMBOLIC',
                    'cross_domain': insight.get('cross_domain', False),
                    'origin': 'rem_integration'
                }
            })()

            # Identify value indicators
            indicators = self.value_formation._identify_value_indicators(experience_proxy)

            values_affected = 0

            # Form or reinforce values
            for indicator in indicators:
                if indicator["strength"] >= self.value_formation.value_formation_threshold:
                    new_value = self.value_formation._form_value_from_indicator(
                        indicator,
                        experience_proxy.id
                    )
                    if new_value:
                        values_affected += 1

            # Always reinforce existing values with this experience
            self.value_formation._reinforce_values_from_experience(experience_proxy, indicators)

            return values_affected

        except Exception as e:
            logger.error(f"Failed to integrate insight with values: {e}")
            return 0

    def _log_sleep_cycle(self, results: Dict):
        """Log sleep cycle results to file."""
        try:
            # Load existing log
            if self.log_path.exists():
                with open(self.log_path, 'r') as f:
                    log = json.load(f)
            else:
                log = {'cycles': []}

            # Append new cycle
            log['cycles'].append(results)

            # Trim if too long (keep last 100 cycles)
            if len(log['cycles']) > 100:
                log['cycles'] = log['cycles'][-100:]

            # Save
            with open(self.log_path, 'w') as f:
                json.dump(log, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log sleep cycle: {e}")

    def _log_insight(self, insight: Dict):
        """Log generated insight to insights file."""
        try:
            # Load existing insights
            if self.insights_path.exists():
                with open(self.insights_path, 'r') as f:
                    insights_log = json.load(f)
            else:
                insights_log = {'insights': []}

            # Append new insight
            insights_log['insights'].append(insight)

            # Save
            with open(self.insights_path, 'w') as f:
                json.dump(insights_log, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log insight: {e}")


# Convenience function for external use
def run_sleep_cycle(data_dir: str = "data") -> Dict:
    """
    Run a complete sleep cycle.

    Args:
        data_dir: Data directory path

    Returns:
        Results dictionary from the sleep cycle
    """
    orchestrator = DreamCycleOrchestrator(data_dir=data_dir)
    return orchestrator.run_sleep_cycle()


if __name__ == "__main__":
    # Allow manual testing
    print("Dream Cycle System - Manual Test Mode")
    results = run_sleep_cycle()
    print("\nResults:")
    print(json.dumps(results, indent=2, default=str))
