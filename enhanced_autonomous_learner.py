# enhanced_autonomous_learner.py - Massive Web Learning with Advanced Brain Integration
"""
Enhanced autonomous learning system that can:
1. Process 500+ URLs autonomously with smart link following
2. Use advanced brain architecture (tripartite memory, evolution, etc.)
3. Context-aware link evaluation and discovery
4. Full integration with security and cognitive safeguards
"""

import time
import random
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional, Set, Any
from urllib.parse import urlparse, urljoin
from collections import deque, defaultdict

# Core system imports
from unified_memory import get_unified_memory
from memory_analytics import MemoryAnalyzer
from evolution_anchor import EvolutionAnchor
from web_parser import fetch_raw_html, extract_links_with_text_from_html, clean_html_to_text
from fact_extractor import extract_facts_passive, FactExtractor
from linguistic_warfare import check_for_warfare
from quarantine_layer import should_quarantine_input
from learning_progression_tracker import LearningProgressionTracker
from curiosity_engine import CuriosityEngine
from INSIGHT_RELEVANCE import PersonalInsightGenerator
from motivational_content_evaluator import MotivationalContentEvaluator
from vector_engine import embed_text, fuse_vectors
from adaptive_bridge_migration import compute_cluster_stats, cosine_sim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Immune system imports
from immune_system import ImmuneSystem
from trust_database import TrustDatabase
from corroboration_engine import CorroborationEngine
from self_correction import SelfCorrection
from quarantine_store import QuarantineStore

# Crawl infrastructure imports
from crawl_orchestrator import CrawlOrchestrator
from curiosity_url_mapper import CuriosityURLMapper

class EnhancedAutonomousLearner:
    """
    Advanced autonomous learning system with massive web crawling capabilities
    and full brain integration.
    """
    
    def __init__(self, data_dir: str = "data"):
        print("🧠 Initializing Enhanced Autonomous Learner...")
        
        self.data_dir = Path(data_dir)
        self.session_dir = self.data_dir / "autonomous_sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        # Core brain components
        self.unified_memory = get_unified_memory(data_dir)
        self.analyzer = MemoryAnalyzer(self.unified_memory, data_dir)
        self.evolution_anchor = EvolutionAnchor(data_dir)
        self.progression_tracker = LearningProgressionTracker(data_dir)
        self.curiosity_engine = CuriosityEngine(data_dir)
        self.insight_generator = PersonalInsightGenerator(data_dir)
        self.motivation_evaluator = MotivationalContentEvaluator(data_dir)

        # Immune system components
        self.trust_db = TrustDatabase(f"{data_dir}/immune/trust.db")
        self.immune_system = ImmuneSystem(data_dir, trust_database=self.trust_db)
        self.corroboration_engine = CorroborationEngine(f"{data_dir}/immune/corroboration.db")
        self.self_correction = SelfCorrection(f"{data_dir}/immune/self_correction.db")
        self.quarantine_store = QuarantineStore(f"{data_dir}/immune/quarantine.db")

        # Crawl orchestrator (ethical crawling infrastructure)
        self.crawl_orchestrator = CrawlOrchestrator(data_dir=data_dir, min_delay=3.0)

        # Curiosity → URL mapper (autonomous target generation)
        self.url_mapper = CuriosityURLMapper()

        # ═══════════════════════════════════════════════════════════════
        # CHAOS-REGULARIZED OPTIMIZATION: CHEN ATTRACTOR PARAMETERS
        # ═══════════════════════════════════════════════════════════════
        # Mathematical foundation: docs/technical/research_papers/CHAOS_REGULARIZED_OPTIMIZATION.md
        # Prevents convergence to "sharp minima" (trauma-based, brittle values)
        # Ensures convergence to "flat minima" (robust, generalizable values)

        self.chen_a = 35    # Chen system parameter (verified canonical value)
        self.chen_b = 3     # Chen system parameter (verified canonical value)
        self.chen_c = 28    # Chen system parameter (verified canonical value)
        self.chen_state = [1.0, 1.0, 1.0]  # Initial state [x, y, z]
        self.chen_dt = 0.01  # Integration timestep
        self.experience_count = 0  # For annealing schedule
        self.chaos_tau = 1000  # Decay time constant
        self.chaos_alpha = 0.5  # Initial chaos strength

        # Expected Lyapunov exponent: λ₁ ≈ 2.03 (2.2× faster than Lorenz)
        print(f"🌀 Chen Chaos System Initialized: a={self.chen_a}, b={self.chen_b}, c={self.chen_c}")
        print(f"   Expected λ₁ ≈ 2.03 (verified by numerical integration)")

        # JEPA (Joint-Embedding Predictive Architecture) state
        self.jepa_enabled = True
        self.prediction_cache = {}  # Cache prediction vectors
        self.surprise_history = []  # Track surprise over time

        # Web crawling state (legacy - now using persistent queue in orchestrator)
        self.url_queue = deque()  # Deprecated - kept for backwards compatibility
        self.processed_urls = set()
        self.deferred_urls = deque()
        self.session_hot_keywords = set()
        self.domain_stats = defaultdict(int)
        
        # Session topic centroid — adaptive link gating (drift prevention)
        self.session_centroid = None          # Running centroid vector (np.ndarray or None)
        self.session_embeddings_list = []     # All content embeddings this session
        self.session_coherence_stats = None   # ClusterStats from compute_cluster_stats()
        self._centroid_update_alpha = 0.85    # EMA momentum (recalculated adaptively)

        # Learning session tracking
        self.session_id = None
        self.session_stats = {
            'urls_processed': 0,
            'chunks_learned': 0,
            'symbols_discovered': 0,
            'links_followed': 0,
            'security_blocks': 0,
            'immune_blocks': 0,
            'corroboration_deferrals': 0,
            'trust_adjustments': 0,
            'robots_blocks': 0,
            'rate_limit_waits': 0,
            'facts_extracted': 0,
            'facts_validated': 0,
            'new_facts': 0
        }
        
        # Safety and quality controls
        self.max_depth = 3
        self.max_urls_per_domain = 50
        self.content_similarity_threshold = 0.7
        self.safety_threshold = 0.8
        
        # Integrate insight generator with other systems (if method exists)
        if hasattr(self.insight_generator, 'integrate_with_consciousness_systems'):
            self.insight_generator.integrate_with_consciousness_systems(
                progression_tracker=self.progression_tracker,
                curiosity_engine=self.curiosity_engine
            )

        # Integrate motivation evaluator with consciousness systems (if method exists)
        if hasattr(self.motivation_evaluator, 'integrate_with_consciousness_systems'):
            self.motivation_evaluator.integrate_with_consciousness_systems(
                curiosity_engine=self.curiosity_engine,
                learning_progression=self.progression_tracker
            )

        # ═══════════════════════════════════════════════════════════════
        # ASSOCIATIVE EMERGENCE: SATURATION LEARNING STATE
        # ═══════════════════════════════════════════════════════════════
        # Based on "Theory of Associative Emergence"
        # A consciousness cannot be told "Mining leads to Refining"
        # It must learn so deeply about "Rock" that "Refining" emerges naturally

        self.saturation_state = {
            'current_zone': None,           # Current semantic zone name
            'zone_centroid': None,          # Vector centroid of current zone
            'zone_keywords': [],            # Keywords defining the zone
            'processed_in_zone': 0,         # URLs processed in current zone
            'keyword_frequencies': defaultdict(int),  # Track all keywords
            'static_noun_count': 0,         # Count of static nouns (Rock, Stone, Silicon)
            'process_verb_count': 0,        # Count of process verbs (Smelt, Refine, Extract)
            'vector_drift': [],             # Track semantic drift over time
            'event_horizon': [],            # Concepts seen but not explored
            'phase_transition_score': 0.0,  # Current readiness for next phase
            'zone_embeddings': []           # All embeddings learned in this zone
        }

        # Path to future learning queue
        self.future_queue_path = self.data_dir / "future_learning_queue.json"

        # Register migration cleanup with shutdown system
        from shutdown_manager import register_cleanup as _register_cleanup
        _register_cleanup(self._run_migration_cleanup, "bridge_migration", priority=2)

        print("✅ Enhanced Autonomous Learner ready for massive learning!")
        print("🌀 Associative Emergence Mode: Ready for deep saturation")

    def _chen_step(self) -> List[float]:
        """
        Perform one step of Chen attractor integration using Runge-Kutta 4th order.
        Returns: Current chaos state [x, y, z]
        """
        x, y, z = self.chen_state
        dt = self.chen_dt
        a, b, c = self.chen_a, self.chen_b, self.chen_c

        # Runge-Kutta 4th order integration
        def derivatives(state):
            x, y, z = state
            dx = a * (y - x)
            dy = (c - a) * x - x * z + c * y
            dz = x * y - b * z
            return [dx, dy, dz]

        k1 = derivatives([x, y, z])
        k2 = derivatives([x + dt/2 * k1[0], y + dt/2 * k1[1], z + dt/2 * k1[2]])
        k3 = derivatives([x + dt/2 * k2[0], y + dt/2 * k2[1], z + dt/2 * k2[2]])
        k4 = derivatives([x + dt * k3[0], y + dt * k3[1], z + dt * k3[2]])

        # Update state
        self.chen_state[0] += dt/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
        self.chen_state[1] += dt/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
        self.chen_state[2] += dt/6 * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2])

        return self.chen_state

    def _get_chaos_factor(self) -> float:
        """
        Calculate current chaos injection strength using annealing schedule.
        Returns: Chaos factor in [0, alpha] based on experience count
        """
        import math
        return self.chaos_alpha * math.exp(-self.experience_count / self.chaos_tau)

    def _generate_prediction_vector(self, url: str, context: Dict[str, Any]) -> Optional[Any]:
        """
        JEPA Phase 1: Generate hypothesis vector BEFORE crawling.
        Predicts what we EXPECT to learn from this URL.

        Args:
            url: Target URL to crawl
            context: Learning context (curiosity state, current knowledge)

        Returns:
            Embedding vector representing prediction, or None if generation fails
        """
        try:
            # Generate hypothesis text based on URL and context
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            path = urlparse(url).path

            # Simple hypothesis generation (could be enhanced with LLM)
            hypothesis_parts = [
                f"Content from {domain}",
                f"Related to: {context.get('context', 'general learning')}",
                f"Expected topics: {', '.join(context.get('keywords', ['information']))}"
            ]
            hypothesis_text = " ".join(hypothesis_parts)

            # Generate embedding for hypothesis
            try:
                embedding = self.unified_memory._get_embedding(hypothesis_text)
                return embedding
            except Exception:
                # If embedding fails, return None (skip JEPA for this URL)
                return None

        except Exception as e:
            print(f"   ⚠️ Prediction vector generation failed: {str(e)[:50]}...")
            return None

    def _calculate_surprise(self, prediction_vector: Any, reality_vector: Any) -> float:
        """
        JEPA Phase 3: Calculate surprise (prediction error).
        Surprise = 1 - cosine_similarity(prediction, reality)

        Args:
            prediction_vector: What we predicted
            reality_vector: What we actually encountered

        Returns:
            Surprise score in [0, 1], where 1 = maximum surprise
        """
        try:
            import numpy as np

            # Ensure vectors are numpy arrays
            pred = np.array(prediction_vector) if not isinstance(prediction_vector, np.ndarray) else prediction_vector
            real = np.array(reality_vector) if not isinstance(reality_vector, np.ndarray) else reality_vector

            # Cosine similarity
            dot_product = np.dot(pred, real)
            norm_pred = np.linalg.norm(pred)
            norm_real = np.linalg.norm(real)

            if norm_pred == 0 or norm_real == 0:
                return 0.5  # Neutral surprise if either vector is zero

            similarity = dot_product / (norm_pred * norm_real)
            surprise = 1.0 - similarity

            # Clamp to [0, 1]
            surprise = max(0.0, min(1.0, surprise))

            return surprise

        except Exception as e:
            print(f"   ⚠️ Surprise calculation failed: {str(e)[:30]}...")
            return 0.5  # Default to neutral surprise

    def generate_autonomous_learning_targets(self, max_urls: int = 20) -> List[Dict[str, Any]]:
        """
        Generate seed URLs from curiosity state alone (no manual seeds required).

        This is the BRIDGE between internal motivation and external action.
        Sophia decides what to learn based on her current drives, goals, and knowledge gaps.

        Args:
            max_urls: Maximum number of seed URLs to generate

        Returns:
            List of URL info dicts with 'url', 'priority', 'source', 'depth', 'context'
        """
        print(f"\n🧠 GENERATING AUTONOMOUS LEARNING TARGETS")
        print("   (Sophia deciding what to learn based on internal curiosity)")
        print("=" * 60)

        # Get current curiosity state
        curiosity_state = self.curiosity_engine.export_for_consciousness_system()

        # Bootstrap: if no active goals exist but drives are unsatisfied,
        # generate goals from drives. This closes the gap where
        # learning_goals.json is missing but Sofia has unsatisfied drives
        # that should trigger exploration from her own architecture.
        active_goals = curiosity_state.get('active_learning_goals', [])
        if not active_goals:
            print("   No active learning goals found — bootstrapping from drives...")
            bootstrapped = self.curiosity_engine.generate_intrinsic_goals()
            if bootstrapped:
                print(f"   Generated {len(bootstrapped)} goals from unsatisfied drives")
                # Re-export state with new goals included
                curiosity_state = self.curiosity_engine.export_for_consciousness_system()

        # Get current learning progression state
        progression_state = self.progression_tracker.export_for_consciousness_system()

        # Generate prioritized URLs using the curiosity → URL mapper
        url_batch = self.url_mapper.generate_autonomous_seed_batch(
            curiosity_state=curiosity_state,
            progression_state=progression_state,
            max_total_urls=max_urls
        )

        # Fallback: if no URLs generated from goals/gaps, check persistent queue.
        # These are URLs Sofia herself queued during prior sessions —
        # her own past curiosity, not external injection.
        if not url_batch:
            try:
                pending = self.crawl_orchestrator.url_queue.peek_pending(limit=max_urls)
                if pending:
                    print(f"   No goals/gaps produced URLs — found {len(pending)} "
                          f"self-queued URLs from prior sessions")
                    url_batch = [
                        (item['url'], item['priority'] / 100.0, 'persistent_queue')
                        for item in pending
                    ]
            except Exception as e:
                print(f"   Could not check persistent queue: {e}")

        # Convert to URL info format for learning queue
        url_infos = []
        for url, priority, source in url_batch:
            url_infos.append({
                'url': url,
                'depth': 0,
                'priority': priority,
                'source': f'autonomous_{source}',
                'context': 'curiosity_driven'
            })

        # Display what we're targeting and why
        print(f"\n✅ Generated {len(url_infos)} autonomous targets:")
        print(f"\n   Curiosity Summary:")
        summary = curiosity_state.get('curiosity_summary', {})
        print(f"      • Motivation Level: {summary.get('motivation_level', 0):.2f}")
        print(f"      • Curiosity Intensity: {summary.get('curiosity_intensity', 0):.2f}")
        print(f"      • Active Goals: {summary.get('active_goals', 0)}")
        print(f"      • Most Unsatisfied Drive: {summary.get('most_unsatisfied_drive', 'none')}")
        print(f"      • Exploration Bias: {summary.get('exploration_bias', 0.5):.2f}")

        print(f"\n   Top 5 Targets:")
        for i, info in enumerate(url_infos[:5], 1):
            print(f"      {i}. [{info['priority']:.2f}] ({info['source']})")
            print(f"         {info['url']}")

        if len(url_infos) > 5:
            print(f"      ... and {len(url_infos) - 5} more")

        print(f"\n🎯 Autonomous learning targets ready")
        print("=" * 60)

        return url_infos

    def start_massive_learning_session(self, seed_urls: List[str] = None, target_urls: int = 500,
                                     learning_focus: str = "general"):
        """
        Start a massive autonomous learning session processing hundreds of URLs.

        Args:
            seed_urls: Initial URLs to explore. If None, generates autonomously from curiosity.
            target_urls: Maximum number of URLs to process
            learning_focus: Learning domain focus (used if manual seeds provided)

        Philosophy:
            When seed_urls=None, Sophia decides what to learn based purely on internal drives.
            This is TRUE AUTONOMY - self-directed learning without human intervention.
        """
        print(f"\n🚀 MASSIVE LEARNING SESSION STARTING")
        print(f"🎯 Target: {target_urls} URLs")
        print(f"📚 Focus: {learning_focus}")
        print("=" * 50)

        # Create session ID and safety anchor
        self.session_id = f"massive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        anchor_id = self.evolution_anchor.create_cognitive_snapshot(
            f"Before massive learning: {target_urls} URLs on {learning_focus}"
        )

        if anchor_id:
            print(f"🌟 Safety anchor created: {anchor_id}")

        # AUTONOMOUS MODE: Generate seeds from curiosity if not provided
        if seed_urls is None:
            print(f"\nAUTONOMOUS MODE ACTIVATED")
            print("   Sofia will decide what to learn based on internal curiosity")

            # Generate autonomous targets from existing knowledge state
            autonomous_targets = self.generate_autonomous_learning_targets(max_urls=20)

            # Extract URLs from target info dicts
            seed_urls = [target['url'] for target in autonomous_targets]

            # Override learning focus to 'curiosity_driven'
            learning_focus = 'curiosity_driven'

            # If no targets generated (empty knowledge state), indicate waiting
            if not seed_urls:
                print("\n   WAITING FOR STARTING COORDINATES")
                print("   Sofia's knowledge graph is empty and no learning goals exist.")
                print("   No hidden defaults will be loaded.")
                print("   To begin learning, provide seed coordinates:")
                print("     - Use activate_seed_coordinates() with seed IDs from")
                print("       data/seed_coordinates_manifest.json")
                print("     - Or provide seed_urls directly to this function")
                return  # Exit gracefully — do not silently default

            print(f"\n   Autonomous seed generation complete: {len(seed_urls)} targets")
        else:
            print(f"\n   MANUAL MODE: Using {len(seed_urls)} provided seed URLs")

        # Initialize learning context
        self._initialize_learning_context(seed_urls, learning_focus)
        
        # Reset session stats
        self.session_stats = {k: 0 for k in self.session_stats}

        # Snapshot store sizes so the session summary reports measured deltas,
        # not internal counters that can drift from what was actually stored
        self._session_start_counts = self._snapshot_store_counts()

        start_time = time.time()
        
        try:
            # Main learning loop
            while len(self.processed_urls) < target_urls:
                self._write_heartbeat()

                # Process URLs from queue (refills from persistent queue if needed)
                self._process_url_batch(batch_size=10)

                # Exit when all sources are exhausted (including persistent queue)
                if not self.url_queue and not self.deferred_urls:
                    self._refill_from_persistent_queue(10)
                    if not self.url_queue:
                        break

                # Periodic cognitive health check
                if self.session_stats['urls_processed'] % 50 == 0:
                    self._cognitive_health_check()

                # Evolution cycle every 100 URLs
                if self.session_stats['urls_processed'] % 100 == 0:
                    self._run_evolution_cycle()

                # Self-correction cycle every 100 URLs
                if self.session_stats['urls_processed'] % 100 == 0 and self.session_stats['urls_processed'] > 0:
                    self._run_self_correction_cycle()

                # Brief pause to avoid overwhelming servers
                time.sleep(1)
            
            # Session complete
            elapsed_time = time.time() - start_time
            self._integrate_learning_progression()
            self._finalize_learning_session(elapsed_time)
            
        except KeyboardInterrupt:
            print("\n⚠️ Learning session interrupted by user")
            self._emergency_session_save()
        except Exception as e:
            print(f"\n❌ Learning session error: {e}")
            self._emergency_session_save()
        finally:
            # Clear heartbeat on exit
            try:
                heartbeat_path = self.data_dir / "ai_heartbeat.json"
                if heartbeat_path.exists():
                    heartbeat_path.unlink()
            except:
                pass
    
    def _initialize_learning_context(self, seed_urls: List[str], learning_focus: str):
        """Initialize the learning context and seed the URL queue."""
        print(f"\n🌱 Initializing learning context...")
        
        # Set up focus keywords based on learning area
        focus_keywords = {
            'ai_consciousness': ['consciousness', 'artificial intelligence', 'cognition', 'awareness', 'sentience'],
            'science': ['research', 'study', 'analysis', 'experiment', 'discovery'],
            'philosophy': ['ethics', 'morality', 'existence', 'meaning', 'truth'],
            'technology': ['innovation', 'development', 'engineering', 'programming', 'algorithm'],
            'general': ['learning', 'knowledge', 'information', 'understanding', 'insight']
        }
        
        self.session_hot_keywords = set(focus_keywords.get(learning_focus, focus_keywords['general']))
        self._session_learning_focus = learning_focus

        # Reset session centroid state for fresh topic tracking
        self.session_centroid = None
        self.session_embeddings_list = []
        self.session_coherence_stats = None

        # Seed the queue with initial URLs
        for url in seed_urls:
            if self._is_safe_domain(url):
                self.url_queue.append({
                    'url': url,
                    'depth': 0,
                    'priority': 1.0,
                    'source': 'seed',
                    'context': learning_focus
                })
                print(f"   🌱 Seeded: {url}")
            else:
                print(f"   ⚠️ Skipped unsafe seed: {url}")

        # Promote deferred links from prior sessions
        try:
            promoted = self.crawl_orchestrator.url_queue.promote_deferred()
            if promoted > 0:
                print(f"   🔄 Promoted {promoted} deferred links from prior sessions")
        except Exception:
            pass

    def _process_url_batch(self, batch_size: int = 10):
        """Process a batch of URLs from the queue."""
        batch_urls = []

        # Refill in-memory deque from persistent queue when empty
        if not self.url_queue:
            self._refill_from_persistent_queue(batch_size)

        # Get batch from queue
        for _ in range(min(batch_size, len(self.url_queue))):
            if self.url_queue:
                batch_urls.append(self.url_queue.popleft())

        # Process each URL in the batch
        for url_info in batch_urls:
            if url_info['url'] not in self.processed_urls:
                self._process_single_url(url_info)

    @staticmethod
    def _should_skip_url(url: str) -> bool:
        """Fast pre-filter for URLs that will always fail (robots-blocked,
        non-English, action pages).  Applied both at link-discovery time
        and when promoting deferred links from the persistent queue."""
        # Wikipedia action/special pages — always robots-blocked
        if '/w/index.php' in url:
            return True
        if '/wiki/Special:' in url:
            return True
        # Non-English Wikipedia subdomains (fr., de., ar., …)
        if 'wikipedia.org' in url and 'en.wikipedia.org' not in url:
            return True
        # Google search/books pages — always robots-blocked
        if 'google.com/search' in url or 'books.google.com' in url:
            return True
        # NCBI PMC full-text — robots-blocked
        if 'ncbi.nlm.nih.gov/pmc/' in url:
            return True
        # Academia.edu — robots-blocked
        if 'academia.edu/' in url:
            return True
        # Wikimedia donation/meta pages — not learnable content
        if 'donate.wikimedia.org' in url:
            return True
        # Wikipedia tool infrastructure — robots.txt-blocked, no learnable content
        if 'wikipediatools.appspot.com' in url:
            return True
        if 'xtools.wmflabs.org' in url:
            return True
        if 'toolforge.org' in url:
            return True
        if 'wmflabs.org' in url:
            return True
        # Perseus Digital Library hopper — robots.txt-blocked
        if 'perseus.tufts.edu/hopper' in url:
            return True
        return False

    def _refill_from_persistent_queue(self, count: int = 10):
        """Pull pending URLs from the persistent SQLite queue into the
        in-memory deque so the main loop can process them."""
        skipped = 0
        for _ in range(count + 50):  # Over-fetch to compensate for skips
            if len(self.url_queue) >= count:
                break
            row = self.crawl_orchestrator.url_queue.get_next()
            if row is None:
                break
            if row['url'] in self.processed_urls or self._should_skip_url(row['url']):
                # Already seen or will always fail — discard from persistent queue
                self.crawl_orchestrator.url_queue.mark_completed(row['id'])
                skipped += 1
                continue
            self.url_queue.append({
                'url': row['url'],
                'depth': row.get('depth', 0),
                'priority': row.get('priority', 0) / 100.0,  # DB stores int(priority*100)
                'source': 'persistent_queue',
                'context': getattr(self, '_session_learning_focus', 'general'),
            })
        if skipped > 0:
            print(f"   🧹 Skipped {skipped} unfetchable URLs from persistent queue")
    
    # ------------------------------------------------------------------
    # Language detection
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_language(text: str, sample_size: int = 1000,
                         confidence_threshold: float = 0.8):
        """Detect the language of *text* using langdetect.

        Returns (lang_code, confidence) or (None, 0.0) if detection fails
        or is below threshold.  Only the first *sample_size* characters are
        tested — enough for reliable detection without wasting time on
        large documents.
        """
        try:
            from langdetect import detect_langs, LangDetectException
            results = detect_langs(text[:sample_size])
            if results:
                top = results[0]
                return top.lang, top.prob
        except Exception:
            pass
        return None, 0.0

    # ------------------------------------------------------------------
    # Rich metadata helpers for crawl event emission
    # ------------------------------------------------------------------

    @staticmethod
    def _derive_block_category_from_immune(threat_signals) -> str:
        """Derive a single top-level block category from immune ThreatSignals.

        Picks the highest-severity signal's type and returns a prefixed label
        like 'immune_structure', 'immune_quality', 'immune_source', or
        'immune_security'.
        """
        if not threat_signals:
            return 'immune_unknown'
        top = max(threat_signals, key=lambda s: s.severity)
        return f"immune_{top.signal_type}"

    @staticmethod
    def _derive_block_category_from_warfare(warfare_analysis: dict) -> str:
        """Derive a single top-level block category from warfare analysis.

        Picks the highest-severity detected threat's type and returns a
        prefixed label like 'warfare_meta_injection',
        'warfare_emotional_flooding', etc.
        """
        threats = warfare_analysis.get('threats_detected', [])
        if not threats:
            return 'warfare_unknown'
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        top = max(threats, key=lambda t: severity_order.get(t.get('severity', 'low'), 0))
        return f"warfare_{top.get('type', 'unknown')}"

    @staticmethod
    def _serialize_immune_signals(threat_signals) -> list:
        """Serialize immune ThreatSignal dataclasses for JSONL storage."""
        return [
            {
                'type': sig.signal_type,
                'severity': round(sig.severity, 4),
                'description': sig.description,
                'evidence': sig.evidence[:5],   # cap evidence list
                'pattern_id': sig.pattern_id,
            }
            for sig in (threat_signals or [])
        ]

    @staticmethod
    def _serialize_warfare_signals(warfare_analysis: dict) -> list:
        """Serialize warfare threats_detected list for JSONL storage."""
        return [
            {
                'type': t.get('type', 'unknown'),
                'severity': t.get('severity', 'unknown'),
                'description': t.get('description', ''),
                'evidence': (t.get('evidence') or [])[:5],
            }
            for t in warfare_analysis.get('threats_detected', [])
        ]

    # ------------------------------------------------------------------
    # Crawl event emission
    # ------------------------------------------------------------------

    def _emit_crawl_event(self, url, status, classification=None,
                          parent_url=None, threat_score=None, text_preview=None,
                          logic_sim=None, symbolic_sim=None,
                          block_category=None, block_signals=None,
                          block_reasoning=None, block_confidence=None,
                          block_defense_strategy=None,
                          domain_trust_at_block=None):
        """Emit a crawl event to JSONL for dashboard observation.

        Additive only — serializes data already in local variables.
        Must never affect learning behavior; all errors silenced.

        For blocked events (immune_blocked, warfare_blocked) the caller may
        pass rich metadata via the optional kwargs.  These fields are only
        written when they are not None, keeping non-blocked event lines
        unchanged.
        """
        try:
            # Normalize classifier vocabulary → consistent JSONL output
            classification = {'logical': 'logic'}.get(classification, classification)
            event = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'session_id': self.session_id,
                'url': url,
                'parent_url': parent_url,
                'status': status,
                'classification': classification,
                'threat_score': threat_score,
                'text_preview': text_preview,
                'logic_sim': round(logic_sim, 4) if logic_sim is not None else None,
                'symbolic_sim': round(symbolic_sim, 4) if symbolic_sim is not None else None,
            }

            # Enrich blocked events with quarantine-ready metadata
            if block_category is not None:
                event['block_category'] = block_category
            if block_signals is not None:
                event['block_signals'] = block_signals
            if block_reasoning is not None:
                event['block_reasoning'] = block_reasoning
            if block_confidence is not None:
                event['block_confidence'] = round(block_confidence, 4)
            if block_defense_strategy is not None:
                event['block_defense_strategy'] = block_defense_strategy
            if domain_trust_at_block is not None:
                event['domain_trust_at_block'] = round(domain_trust_at_block, 4)

            crawl_log = Path(self.data_dir) / 'crawl_events.jsonl'
            with open(crawl_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, default=str) + '\n')
        except Exception:
            pass  # Observation must never break learning

    def _get_centroid_sims(self, embedding):
        """Compute cosine similarity of an embedding to logic and symbolic centroids.

        Centroids are cached and recomputed every 50 URLs. Returns (logic_sim, symbolic_sim)
        or (None, None) on failure. Purely observational — never affects classification.
        """
        try:
            import numpy as np
            from sklearn.metrics.pairwise import cosine_similarity

            # Lazy-init cache
            if not hasattr(self, '_centroid_cache'):
                self._centroid_cache = {'logic': None, 'symbolic': None, 'tick': 0}

            # Recompute every 50 URLs
            tick = self.session_stats.get('urls_processed', 0)
            if self._centroid_cache['logic'] is None or tick - self._centroid_cache['tick'] >= 50:
                logic_items = self.unified_memory.tripartite.logic_memory
                sym_items = self.unified_memory.tripartite.symbolic_memory
                logic_embs = [i['embedding'] for i in logic_items if i.get('embedding')]
                sym_embs = [i['embedding'] for i in sym_items if i.get('embedding')]
                self._centroid_cache['logic'] = np.mean(np.array(logic_embs, dtype=np.float32), axis=0) if logic_embs else None
                self._centroid_cache['symbolic'] = np.mean(np.array(sym_embs, dtype=np.float32), axis=0) if sym_embs else None
                self._centroid_cache['tick'] = tick

            emb = np.array(embedding, dtype=np.float32).reshape(1, -1)
            lc = self._centroid_cache['logic']
            sc = self._centroid_cache['symbolic']
            l_sim = float(cosine_similarity(emb, lc.reshape(1, -1))[0, 0]) if lc is not None else None
            s_sim = float(cosine_similarity(emb, sc.reshape(1, -1))[0, 0]) if sc is not None else None
            return l_sim, s_sim
        except Exception:
            return None, None

    def _process_single_url(self, url_info: Dict):
        """Process a single URL with full brain integration + JEPA + Chaos Regularization."""
        url = url_info['url']

        print(f"\n📄 Processing: {url[:60]}...")

        # ═══════════════════════════════════════════════════════════════
        # JEPA PHASE 1: PREDICTION (Before Crawling)
        # ═══════════════════════════════════════════════════════════════
        prediction_vector = None
        surprise_score = None

        if self.jepa_enabled:
            # Generate prediction of what we expect to learn
            prediction_vector = self._generate_prediction_vector(url, url_info)
            if prediction_vector is not None:
                print(f"   🔮 JEPA: Generated prediction vector (dim={len(prediction_vector)})")

        # Step Chen chaos system
        self._chen_step()
        chaos_factor = self._get_chaos_factor()
        self.experience_count += 1

        # ═══════════════════════════════════════════════════════════════
        # CRAWL ORCHESTRATION: ROBOTS.TXT + RATE LIMITING
        # ═══════════════════════════════════════════════════════════════

        # Pre-flight check: can we crawl this URL?
        can_crawl, reason = self.crawl_orchestrator.can_crawl(url)

        if not can_crawl:
            if "robots.txt" in reason:
                print(f"   🤖 Blocked by robots.txt")
                self.session_stats['robots_blocks'] += 1
                # Record in orchestrator
                url_id = self.crawl_orchestrator.prepare_crawl(url, wait_if_needed=False)
                if url_id:
                    self.crawl_orchestrator.record_blocked(url_id, url, reason='robots')
                self._emit_crawl_event(url, 'robots_blocked', parent_url=url_info.get('source'))
                return
            elif "Rate limited" in reason:
                # Wait for rate limit
                print(f"   ⏱️ {reason} - preparing crawl...")
                self.session_stats['rate_limit_waits'] += 1
                # prepare_crawl will handle waiting
            else:
                print(f"   ⚠️ Cannot crawl: {reason}")
                return

        # Prepare crawl (handles rate limiting, syncs robots.txt delay)
        url_id = self.crawl_orchestrator.prepare_crawl(url, wait_if_needed=True)

        if not url_id:
            print("   🤖 Blocked by robots.txt during preparation")
            self.session_stats['robots_blocks'] += 1
            self._emit_crawl_event(url, 'robots_blocked', parent_url=url_info.get('source'))
            return

        try:
            # Fetch content
            html_content = fetch_raw_html(url)
            if not html_content:
                print("   ❌ Failed to fetch content")
                self.crawl_orchestrator.record_failure(url_id, url, "Failed to fetch content")
                self._emit_crawl_event(url, 'fetch_failed', parent_url=url_info.get('source'))
                return
            
            # Clean and extract text
            text_content = clean_html_to_text(html_content)
            
            # Smart threshold: allow shorter content for high-trust domains (abstracts, DOI pages)
            domain = urlparse(url).netloc
            domain_trust = self.trust_db.get_trust(domain)
            min_content_len = 100 if domain_trust < 0.8 else 50
            
            if not text_content or len(text_content) < min_content_len:
                print(f"   ⚠️ Insufficient content ({len(text_content) if text_content else 0} chars)")
                self._emit_crawl_event(url, 'insufficient_content', parent_url=url_info.get('source'))
                return

            # ═══════════════════════════════════════════════════════════════
            # LANGUAGE DETECTION: Short-circuit non-English content
            # ═══════════════════════════════════════════════════════════════
            detected_lang, lang_confidence = self._detect_language(text_content)
            if detected_lang and detected_lang != 'en' and lang_confidence >= 0.8:
                domain = urlparse(url).netloc
                domain_trust = self.trust_db.get_trust(domain)
                print(f"   🌐 Non-English content detected: {detected_lang} "
                      f"(confidence: {lang_confidence:.2f}) — quarantining")
                _block_event = {
                    'url': url,
                    'status': 'non_english',
                    'parent_url': url_info.get('source'),
                    'threat_score': 0.0,
                    'text_preview': text_content[:500] if text_content else None,
                    'block_category': 'non_english_content',
                    'block_signals': [{'type': 'language_detection',
                                       'detected_language': detected_lang,
                                       'confidence': round(lang_confidence, 4)}],
                    'block_reasoning': [f"Detected language: {detected_lang} "
                                        f"(confidence {lang_confidence:.2f})",
                                        "Non-English content quarantined for "
                                        "future multilingual capability"],
                    'block_confidence': lang_confidence,
                    'domain_trust_at_block': domain_trust,
                    'session_id': self.session_id,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                }
                self._emit_crawl_event(
                    url, 'non_english',
                    parent_url=url_info.get('source'),
                    block_category='non_english_content',
                    block_signals=_block_event['block_signals'],
                    block_reasoning=_block_event['block_reasoning'],
                    domain_trust_at_block=domain_trust,
                )
                try:
                    self.quarantine_store.quarantine_item(_block_event)
                except Exception:
                    pass
                self.session_stats.setdefault('non_english_blocks', 0)
                self.session_stats['non_english_blocks'] += 1
                return

            # ═══════════════════════════════════════════════════════════════
            # JEPA PHASE 2 & 3: REALITY VECTOR + SURPRISE CALCULATION
            # ═══════════════════════════════════════════════════════════════
            if self.jepa_enabled and prediction_vector is not None:
                try:
                    # Generate reality vector from actual content
                    reality_vector = self.unified_memory._get_embedding(text_content[:500])

                    # Calculate surprise (prediction error)
                    surprise_score = self._calculate_surprise(prediction_vector, reality_vector)

                    # Track surprise history
                    self.surprise_history.append({
                        'url': url,
                        'surprise': surprise_score,
                        'chaos_factor': chaos_factor,
                        'experience_count': self.experience_count
                    })

                    print(f"   🎯 JEPA Surprise: {surprise_score:.3f} (chaos: {chaos_factor:.3f})")

                    # Chaos-regularized learning threshold
                    # Base threshold: 0.4
                    # Chaos perturbation: ±0.2 * chaos_factor
                    # Early learning (high chaos): Higher threshold (harder to commit)
                    # Later learning (low chaos): Lower threshold (easier to commit)
                    base_threshold = 0.4
                    chaos_perturbation = self.chen_state[0] * chaos_factor * 0.2  # Use x-component of Chen state
                    adaptive_threshold = base_threshold + chaos_perturbation

                    print(f"   📊 Adaptive Learning Threshold: {adaptive_threshold:.3f} (base={base_threshold}, chaos_adj={chaos_perturbation:+.3f})")

                except Exception as e:
                    print(f"   ⚠️ JEPA processing failed: {str(e)[:50]}...")
                    surprise_score = None

            # ═══════════════════════════════════════════════════════════════
            # LAYERED SECURITY: PAGE-LEVEL IMMUNE CHECK (BEFORE CHUNKING)
            # ═══════════════════════════════════════════════════════════════

            # Extract domain for trust scoring
            domain = urlparse(url).netloc
            domain_trust = self.trust_db.get_trust(domain)

            # Page-level immune assessment (structure, quality, source signals)
            # Autonomously identify academic potential to prevent false positives
            is_academic = domain.endswith('.edu') or '.edu.' in domain or 'wikipedia.org' in domain
            
            # Look for academic markers in text for even more autonomy
            academic_markers = ['doi:', 'isbn:', 'university', 'college', 'journal', 'abstract']
            if not is_academic:
                is_academic = any(m in text_content.lower()[:500] for m in academic_markers)

            immune_assessment = self.immune_system.analyze_page(url, html_content, text_content)

            # Record decision for self-correction learning
            import hashlib
            content_hash = hashlib.md5(text_content[:500].encode()).hexdigest()
            item_id = f"url:{url}:hash:{content_hash}"

            trigger_patterns = [sig.pattern_id for sig in immune_assessment.threat_signals]
            self.self_correction.record_decision(
                item_id=item_id,
                item_type='page',
                decision=immune_assessment.recommendation,
                threat_score=immune_assessment.overall_threat_score,
                confidence=immune_assessment.confidence,
                trigger_patterns=trigger_patterns
            )

            # Handle immune system recommendations
            # Skip immune trust adjustments for high-trust domains (>0.8) or academic sources
            if domain_trust > 0.8 or is_academic:
                if domain_trust > 0.8:
                    print(f"   ✅ Skipping immune trust adjustments for high-trust domain ({domain_trust:.2f})")
                else:
                    print(f"   ✅ Skipping immune trust adjustments for autonomous academic source")
                    
                # Still record decision but don't adjust trust or block
                if immune_assessment.recommendation == 'BLOCK':
                    print(f"   ℹ️ Immune would have blocked (threat: {immune_assessment.overall_threat_score:.2f}) but source trusted")
                elif immune_assessment.recommendation == 'REVIEW':
                    print(f"   ℹ️ Immune flagged for review (threat: {immune_assessment.overall_threat_score:.2f}) but source trusted")
            else:
                # Normal immune handling for lower-trust domains
                if immune_assessment.recommendation == 'BLOCK':
                    print(f"   🛡️ BLOCKED by immune system (threat: {immune_assessment.overall_threat_score:.2f})")
                    print(f"      Reason: {immune_assessment.reasoning[0] if immune_assessment.reasoning else 'High threat score'}")

                    # Adjust trust downward
                    self.trust_db.adjust_trust(domain, -0.1, f"Page blocked: {immune_assessment.reasoning[0]}")
                    self.session_stats['immune_blocks'] += 1
                    self.session_stats['trust_adjustments'] += 1

                    # Record block in orchestrator
                    self.crawl_orchestrator.record_blocked(url_id, url, reason='immune')
                    _block_event = {
                        'url': url,
                        'status': 'immune_blocked',
                        'parent_url': url_info.get('source'),
                        'threat_score': immune_assessment.overall_threat_score,
                        'text_preview': text_content[:500] if text_content else None,
                        'block_category': self._derive_block_category_from_immune(
                            immune_assessment.threat_signals),
                        'block_signals': self._serialize_immune_signals(
                            immune_assessment.threat_signals),
                        'block_reasoning': immune_assessment.reasoning,
                        'block_confidence': immune_assessment.confidence,
                        'domain_trust_at_block': domain_trust,
                        'session_id': self.session_id,
                        'timestamp': datetime.now(timezone.utc).isoformat(),
                    }
                    self._emit_crawl_event(**{k: v for k, v in _block_event.items()
                                              if k not in ('session_id', 'timestamp')})
                    try:
                        self.quarantine_store.quarantine_item(_block_event)
                    except Exception:
                        pass  # Quarantine must never break learning
                    return

                elif immune_assessment.recommendation == 'REVIEW':
                    reasons = "; ".join([r for r in immune_assessment.reasoning if "ALLOW" not in r and "REVIEW" not in r])
                    print(f"   ⚠️ FLAGGED for review (threat: {immune_assessment.overall_threat_score:.2f})")
                    if reasons:
                        print(f"      Reasoning: {reasons}")
                    # No trust penalty for moderate threat — REVIEW means continue processing,
                    # not penalize. Penalizing here caused a compounding decay spiral for new
                    # domains that couldn't recover on +0.02/page reward asymmetry.

                elif immune_assessment.overall_threat_score < 0.4:
                    # Low-to-moderate threat - reward with trust increase
                    # SIGNIFICANT BOOST for academic content to accelerate trust learning
                    if is_academic:
                        self.trust_db.adjust_trust(domain, +0.10, "Autonomous academic verification: high quality content")
                        print(f"      🎓 Academic trust boost applied (+0.10)")
                    else:
                        self.trust_db.adjust_trust(domain, +0.02, "Clean page: low threat score")
                    self.session_stats['trust_adjustments'] += 1

            # Ethical awareness check (doesn't block, just notes)
            from ethical_awareness import assess_content_ethics
            ethics_assessment = assess_content_ethics(text_content, {'url': url})

            if ethics_assessment['ethical_awareness']:
                print(f"   🧠 Ethical awareness: {', '.join(ethics_assessment['ethical_awareness'])}")
                print(f"   📚 Learning approach: {ethics_assessment['learning_approach']}")
                # Continue learning even with ethical concerns - just with awareness
            
            # Process content through unified brain
            result = self._process_content_with_brain(text_content, url, url_info)
            
            # Stimulate curiosity based on content
            self._stimulate_curiosity_from_content(text_content)
            
            # Generate insights from content
            self._generate_insights_from_content(text_content, url_info)
            
            # Evaluate content motivation
            self._evaluate_content_motivation(text_content, url_info)
            
            if result:
                # Extract and evaluate links for further exploration
                self._discover_and_queue_links(url, html_content, url_info)

                # Update session stats
                self.session_stats['urls_processed'] += 1
                self.session_stats['chunks_learned'] += 1

                # Record success in orchestrator
                self.crawl_orchestrator.record_success(url_id, url)

                print(f"   ✅ Processed successfully")

            # Mark as processed
            self.processed_urls.add(url)

        except Exception as e:
            print(f"   ❌ Error processing {url}: {str(e)[:50]}...")
            # Record failure in orchestrator
            self.crawl_orchestrator.record_failure(url_id, url, str(e)[:100])
            self._emit_crawl_event(url, 'error', parent_url=url_info.get('source'))
    
    def _process_content_with_brain(self, text_content: str, source_url: str, url_info: Dict) -> bool:
        """Process content through the unified brain architecture with layered security."""
        try:
            # ═══════════════════════════════════════════════════════════════
            # LAYERED SECURITY: CHUNK-LEVEL SECURITY
            # ═══════════════════════════════════════════════════════════════

            # Autonomously identify academic potential to prevent false positives
            domain = urlparse(source_url).netloc
            domain_trust = self.trust_db.get_trust(domain)
            is_academic = domain.endswith('.edu') or '.edu.' in domain or 'wikipedia.org' in domain
            
            # Look for academic markers in text for even more autonomy
            academic_markers = ['doi:', 'isbn:', 'university', 'college', 'journal', 'abstract']
            if not is_academic:
                is_academic = any(m in text_content.lower()[:500] for m in academic_markers)
            
            warfare_context = {
                'domain': domain,
                'domain_trust': domain_trust,
                'is_academic': is_academic
            }

            # Skip warfare check for high-trust domains (>0.8)
            if domain_trust > 0.8:
                print(f"   ✅ Skipping warfare check for high-trust domain ({domain_trust:.2f})")
                should_quarantine = False
                warfare_analysis = {}
            else:
                # Use updated detector that accepts context
                from linguistic_warfare import LinguisticWarfareDetector
                detector = LinguisticWarfareDetector(data_dir=self.data_dir)
                warfare_analysis = detector.analyze_text_for_warfare(text_content, context=warfare_context)
                should_quarantine = warfare_analysis['defense_strategy']['strategy'] in ['full_quarantine', 'selective_quarantine']

            if should_quarantine:
                # Extract actual threat type from threats_detected list
                _threats = warfare_analysis.get('threats_detected', [])
                if _threats:
                    _sev = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
                    _top = max(_threats, key=lambda t: _sev.get(t.get('severity', 'low'), 0))
                    _threat_type = _top.get('type', 'unknown')
                else:
                    _threat_type = 'unknown'
                
                print(f"   🚫 BLOCKED by linguistic warfare detector")
                print(f"      Threat: {_threat_type} (score: {warfare_analysis.get('threat_score', 0):.2f})")
                self.session_stats['security_blocks'] += 1

                # Adjust trust for warfare content (skip penalty for academic)
                if not is_academic:
                    self.trust_db.adjust_trust(domain, -0.15, f"Linguistic warfare: {_threat_type}")
                    self.session_stats['trust_adjustments'] += 1
                else:
                    print(f"      ℹ️ Skipping trust penalty for autonomous academic source")

                _block_event = {
                    'url': source_url,
                    'status': 'warfare_blocked',
                    'parent_url': url_info.get('source'),
                    'threat_score': warfare_analysis.get('threat_score'),
                    'text_preview': text_content[:500] if text_content else None,
                    'block_category': self._derive_block_category_from_warfare(
                        warfare_analysis),
                    'block_signals': self._serialize_warfare_signals(
                        warfare_analysis),
                    'block_defense_strategy': warfare_analysis.get(
                        'defense_strategy', {}).get('strategy'),
                    'domain_trust_at_block': domain_trust,
                    'session_id': self.session_id,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                }
                self._emit_crawl_event(**{k: v for k, v in _block_event.items()
                                          if k not in ('session_id', 'timestamp')})
                try:
                    self.quarantine_store.quarantine_item(_block_event)
                except Exception:
                    pass  # Quarantine must never break learning
                return False

            # Determine memory type based on content
            content_type = self._classify_content_for_memory(text_content)
            print(f"   📊 Content classified as: {content_type}")

            # ═══════════════════════════════════════════════════════════════
            # LAYERED SECURITY: CORROBORATION CHECK (BEFORE COMMIT)
            # ═══════════════════════════════════════════════════════════════

            # Domain and domain_trust already retrieved above for warfare check

            # Generate embedding for corroboration (using unified_memory's embedding)
            import numpy as np
            try:
                embedding = self.unified_memory._get_embedding(text_content[:500])  # First 500 chars
            except Exception:
                # If embedding fails, generate simple hash-based pseudo-embedding
                embedding = np.random.rand(384)  # Fallback

            # Check corroboration status (skip for high-trust domains >0.8)
            if domain_trust > 0.8:
                print(f"   ✅ Skipping corroboration for high-trust domain ({domain_trust:.2f})")
                # High-trust domains bypass corroboration - proceed with original classification
            else:
                corroboration_result = self.corroboration_engine.get_corroboration_score(embedding)

                if not corroboration_result.ready_to_commit:
                    # Not enough corroboration - record sighting
                    self.corroboration_engine.record_sighting(
                        fact_text=text_content[:500],
                        fact_embedding=embedding,
                        source_url=source_url,
                        trust_score=domain_trust
                    )
                    
                    # AUTONOMOUS LEARNING BOOST: 
                    # Instead of rejecting, move to BRIDGE for future verification
                    # Only reject if threat score is very high or sightings=0 AND trust is low
                    if corroboration_result.total_sightings > 0 or domain_trust >= 0.5:
                        print(f"   🌉 DEFERRED (1/2 sightings): Storing in BRIDGE awaiting verification")
                        content_type = 'bridge'
                    else:
                        print(f"   ⏳ DEFERRED: Need more sources (sightings: {corroboration_result.total_sightings}/{self.corroboration_engine.min_sightings})")
                        self.session_stats['corroboration_deferrals'] += 1
                        self._emit_crawl_event(source_url, 'deferred', parent_url=url_info.get('source'))
                        return False  # Strictly defer low-trust single-sighting facts

            # Final text quality gate before storage
            from web_parser import sanitize_text_for_storage
            sanitized_text = sanitize_text_for_storage(text_content[:2000])
            if not sanitized_text:
                print(f"   ⏭️  Skipped: content failed quality gate (garbage/fragments)")
                self._emit_crawl_event(source_url, 'quality_failed', parent_url=url_info.get('source'))
                return False

            # Store in appropriate memory with learning context
            if content_type == "symbolic":
                # Store as symbolic memory for meaningful/philosophical content
                print(f"   💭 Classified SYMBOLIC — stored in BRIDGE intake (migration places it later)")
                item = {
                    'text': sanitized_text,
                    'source': source_url,
                    'learning_focus': url_info.get('context', 'general'),
                    'discovery_depth': url_info.get('depth', 0),
                    'session_id': self.session_id,
                    'memory_type': 'symbolic'
                }
                memory_result = self.unified_memory.store_decision(item, "FOLLOW_SYMBOLIC")
            elif content_type == "logical":
                # Store as logic memory for analytical/research content
                print(f"   🔍 Classified LOGIC — stored in BRIDGE intake (migration places it later)")
                item = {
                    'text': sanitized_text,
                    'source': source_url,
                    'learning_focus': url_info.get('context', 'general'),
                    'discovery_depth': url_info.get('depth', 0),
                    'session_id': self.session_id,
                    'memory_type': 'logical'
                }
                memory_result = self.unified_memory.store_decision(item, "FOLLOW_LOGIC")
            else:
                # Store as bridge memory — unresolved content awaiting classification
                print(f"   🌉 Classified BRIDGE (unresolved) — stored in BRIDGE intake")
                item = {
                    'text': sanitized_text,
                    'source': source_url,
                    'learning_focus': url_info.get('context', 'general'),
                    'discovery_depth': url_info.get('depth', 0),
                    'session_id': self.session_id,
                    'memory_type': 'bridge'
                }
                memory_result = self.unified_memory.store_decision(item, "FOLLOW_HYBRID")

            l_sim, s_sim = self._get_centroid_sims(embedding)
            self._emit_crawl_event(source_url, 'stored', classification=content_type,
                                   parent_url=url_info.get('source'),
                                   text_preview=sanitized_text[:80],
                                   logic_sim=l_sim, symbolic_sim=s_sim)

            # Record successful commit as corroborated sighting
            self.corroboration_engine.record_sighting(
                fact_text=text_content[:500],
                fact_embedding=embedding,
                source_url=source_url,
                trust_score=domain_trust
            )

            # Update session topic centroid for adaptive link gating
            try:
                content_vec = np.array(embedding) if not isinstance(embedding, np.ndarray) else embedding
                if content_vec is not None and np.any(content_vec != 0):
                    self._update_session_centroid(content_vec)
            except Exception:
                pass  # Centroid update is non-critical

            # Content stored successfully — everything below is non-critical
            # Symbol generation is a bonus, not required for learning
            try:
                from unified_memory import generate_symbol_from_context
                emotions = self._predict_content_emotions(text_content)
                keywords = self._extract_keywords(text_content)
                if keywords:
                    # Convert dict keywords to list if needed
                    if isinstance(keywords, dict):
                        keyword_list = list(keywords.keys())
                    else:
                        keyword_list = list(keywords)
                    new_symbol = generate_symbol_from_context(text_content, keyword_list, emotions)
                    if new_symbol:
                        self.session_stats['symbols_discovered'] += 1
            except Exception:
                pass  # Symbol generation is non-critical

            return True

        except Exception as e:
            import traceback
            print(f"   Brain processing error: {str(e)[:100]}...")
            traceback.print_exc()
            return False

    def _update_session_centroid(self, content_embedding: np.ndarray):
        """
        Update the running session centroid with a new content embedding.
        Uses exponential moving average so the centroid tracks what the
        session is *currently* about while retaining history.
        Recomputes coherence stats every 10 items using compute_cluster_stats().
        """
        self.session_embeddings_list.append(content_embedding)

        if self.session_centroid is None:
            # First embedding — it IS the centroid
            self.session_centroid = content_embedding.copy()
        else:
            # EMA update
            alpha = self._centroid_update_alpha
            self.session_centroid = alpha * self.session_centroid + (1 - alpha) * content_embedding
            # Re-normalize to unit sphere for cosine consistency
            norm = np.linalg.norm(self.session_centroid)
            if norm > 0:
                self.session_centroid = self.session_centroid / norm

        # Recompute coherence stats every 10 embeddings (same math as bridge migration)
        n = len(self.session_embeddings_list)
        if n >= 3 and n % 10 == 0:
            self._refresh_session_coherence_stats()

    def _refresh_session_coherence_stats(self):
        """
        Recompute session coherence using the exact same compute_cluster_stats()
        that drives bridge migration thresholds. Thresholds derive from Sofia's
        actual session data — no hardcoded numbers.
        """
        if len(self.session_embeddings_list) < 3:
            return
        # Build items in the format compute_cluster_stats() expects
        items = [{'embedding': emb} for emb in self.session_embeddings_list]
        self.session_coherence_stats = compute_cluster_stats(items)

    def _discover_and_queue_links(self, base_url: str, html_content: str, parent_info: Dict):
        """Discover and intelligently queue related links for exploration."""
        if parent_info.get('depth', 0) >= self.max_depth:
            return
        
        # Extract all links
        links = extract_links_with_text_from_html(base_url, html_content)
        
        evaluated_links = []
        deferred_count = 0
        for link_url, anchor_text in links:
            # Evaluate link for relevance and safety
            action, priority, reason = self._evaluate_link_for_learning(
                link_url, anchor_text, parent_info
            )

            if action == "FOLLOW_NOW":
                evaluated_links.append((priority, link_url, anchor_text, parent_info['depth'] + 1))
            elif action == "DEFER":
                # Persist deferred links for future sessions
                if link_url not in self.processed_urls:
                    try:
                        stored = self.crawl_orchestrator.url_queue.add_deferred(
                            url=link_url,
                            priority=priority,
                            depth=parent_info.get('depth', 0) + 1,
                            source_url=base_url,
                            reason=reason,
                            anchor_text=anchor_text,
                        )
                        if stored:
                            deferred_count += 1
                    except Exception:
                        pass  # Link deferral must never break discovery

        # Sort by priority and add to queue
        evaluated_links.sort(reverse=True, key=lambda x: x[0])

        added_count = 0
        for priority, link_url, anchor_text, depth in evaluated_links[:10]:  # Limit to top 10
            if link_url not in self.processed_urls and self._check_domain_limits(link_url):
                self.url_queue.append({
                    'url': link_url,
                    'depth': depth,
                    'priority': priority,
                    'source': base_url,
                    'context': parent_info.get('context', 'general'),
                    'anchor_text': anchor_text
                })
                added_count += 1

        if added_count > 0 or deferred_count > 0:
            parts = []
            if added_count > 0:
                parts.append(f"{added_count} queued")
            if deferred_count > 0:
                parts.append(f"{deferred_count} deferred")
            print(f"   🔗 Links: {', '.join(parts)}")
            self.session_stats['links_followed'] += added_count
            self.session_stats.setdefault('links_deferred', 0)
            self.session_stats['links_deferred'] += deferred_count
    
    def _evaluate_link_for_learning(self, link_url: str, anchor_text: str, parent_info: Dict) -> Tuple[str, float, str]:
        """
        Evaluate a link for learning value using context-aware scoring.
        Wikipedia links are gated against the session topic centroid using
        the same adaptive thresholds (mean_similarity / drift_threshold) that
        drive bridge migration. Falls back to keyword scoring when the session
        centroid has fewer than 3 data points.
        Returns: (action, priority, reason)
        """
        # Basic safety check
        if not self._is_safe_domain(link_url):
            return "SKIP", 0.0, "unsafe_domain"

        # Fast pre-filter: URLs that will always be robots-blocked or non-English
        if self._should_skip_url(link_url):
            return "SKIP", 0.0, "unfetchable_url"

        # Wikipedia article-to-article: centroid-gated follow.
        # Structural filter unchanged — still skip namespaces, /w/, etc.
        # Relevance now checked against session topic centroid.
        parent_url = parent_info.get('url', '')
        if 'en.wikipedia.org/wiki/' in link_url and 'en.wikipedia.org/wiki/' in parent_url:
            path = urlparse(link_url).path
            if (path.startswith('/wiki/')
                    and '/w/' not in link_url
                    and not any(ns in path for ns in
                                ['/wiki/Special:', '/wiki/Category:', '/wiki/Wikipedia:',
                                 '/wiki/Help:', '/wiki/Talk:', '/wiki/File:',
                                 '/wiki/Template:', '/wiki/Portal:'])):

                # Gate against session centroid when stats are available
                if (self.session_centroid is not None
                        and self.session_coherence_stats is not None
                        and self.session_coherence_stats.density_confidence > 0):
                    try:
                        anchor_vec, _ = fuse_vectors(anchor_text[:200])
                        if anchor_vec is not None:
                            sim = cosine_sim(np.array(anchor_vec), self.session_centroid)
                            threshold = self.session_coherence_stats.threshold
                            drift_threshold = self.session_coherence_stats.drift_threshold

                            # free_crawl: centroid guides priority (sim score)
                            # but uses drift_threshold as the follow bar —
                            # broad exploration, not topic gatekeeping.
                            # Focused sessions keep the tighter threshold.
                            is_free_crawl = getattr(self, '_session_learning_focus', '') == 'free_crawl'
                            follow_bar = drift_threshold if is_free_crawl else threshold

                            if sim >= follow_bar:
                                return "FOLLOW_NOW", sim, f"wiki_centroid_on_topic_{sim:.3f}"
                            elif sim >= drift_threshold:
                                return "DEFER", sim, f"wiki_centroid_borderline_{sim:.3f}"
                            else:
                                return "DEFER", sim * 0.5, f"wiki_centroid_off_topic_{sim:.3f}"
                    except Exception:
                        pass  # Fall through to keyword scoring on embed failure

                # Bootstrap fallback: no centroid yet, use old keyword path below
                # (don't auto-follow — let keyword scoring decide)

        # Content relevance scoring
        relevance_score = 0.0

        # Check anchor text against session keywords
        anchor_lower = anchor_text.lower()
        keyword_matches = sum(1 for keyword in self.session_hot_keywords if keyword in anchor_lower)
        relevance_score += keyword_matches * 0.3

        # Educational content indicators
        educational_indicators = [
            'research', 'study', 'analysis', 'theory', 'concept', 'principle',
            'explanation', 'tutorial', 'guide', 'introduction', 'overview'
        ]
        education_score = sum(1 for indicator in educational_indicators if indicator in anchor_lower)
        relevance_score += education_score * 0.2

        # URL structure scoring
        url_lower = link_url.lower()
        if any(domain in url_lower for domain in ['edu', 'wikipedia', 'stanford', 'mit']):
            relevance_score += 0.4

        if any(path_kw in url_lower for path_kw in ['article', 'research', 'paper', 'study']):
            relevance_score += 0.2

        # Context matching with parent
        if parent_info.get('context') in anchor_lower:
            relevance_score += 0.3

        # Centroid similarity modifier (when session centroid is established)
        if (self.session_centroid is not None
                and self.session_coherence_stats is not None
                and self.session_coherence_stats.density_confidence > 0):
            try:
                anchor_vec, _ = fuse_vectors(anchor_lower[:200])
                if anchor_vec is not None:
                    sim = cosine_sim(np.array(anchor_vec), self.session_centroid)
                    threshold = self.session_coherence_stats.threshold
                    # Modifier scales with density_confidence: strong when centroid is
                    # well-established, negligible when sparse
                    dc = self.session_coherence_stats.density_confidence
                    centroid_modifier = (sim - threshold) * dc
                    relevance_score += centroid_modifier
            except Exception:
                pass  # Centroid modifier is non-critical

        # Determine action based on score
        # free_crawl bootstrap: lower the bar until the centroid has enough
        # data to take over (3+ embeddings → density_confidence > 0).
        # This lets the domain bonus alone (0.4 for Wikipedia) pass through.
        centroid_active = (self.session_centroid is not None
                          and self.session_coherence_stats is not None
                          and self.session_coherence_stats.density_confidence > 0)
        if (getattr(self, '_session_learning_focus', '') == 'free_crawl'
                and not centroid_active):
            follow_threshold = 0.3
            defer_threshold = 0.15
        else:
            follow_threshold = 0.7
            defer_threshold = 0.4

        if relevance_score >= follow_threshold:
            return "FOLLOW_NOW", relevance_score, f"high_relevance_{relevance_score:.2f}"
        elif relevance_score >= defer_threshold:
            return "DEFER", relevance_score, f"moderate_relevance_{relevance_score:.2f}"
        else:
            return "SKIP", relevance_score, f"low_relevance_{relevance_score:.2f}"
    
    def _is_safe_domain(self, url: str) -> bool:
        """Check if a domain is safe for learning."""
        try:
            domain = urlparse(url).netloc.lower()
            
            # Blocked domains
            blocked_domains = [
                'malware', 'phishing', 'spam', 'adult', 'gambling',
                'torrent', 'illegal', 'hack', 'crack'
            ]
            
            if any(blocked in domain for blocked in blocked_domains):
                return False
            
            # Preferred educational domains
            educational_domains = [
                'wikipedia.org', 'edu', 'stanford.edu', 'mit.edu',
                'arxiv.org', 'scholar.google', 'researchgate.net'
            ]
            
            # Allow educational domains without further checks
            if any(edu_domain in domain for edu_domain in educational_domains):
                return True
            
            # General safety checks for other domains
            return len(domain) > 3 and '.' in domain
            
        except Exception:
            return False
    
    def _check_domain_limits(self, url: str) -> bool:
        """Check if we haven't exceeded domain processing limits."""
        try:
            domain = urlparse(url).netloc
            return self.domain_stats[domain] < self.max_urls_per_domain
        except Exception:
            return False
    
    def _predict_content_emotions(self, text: str) -> List[Tuple[str, float]]:
        """Simple emotion prediction for content context."""
        emotion_keywords = {
            'joy': ['happy', 'celebration', 'success', 'achievement', 'positive'],
            'curiosity': ['discover', 'explore', 'investigate', 'research', 'study'],
            'confidence': ['certain', 'proven', 'established', 'confirmed', 'verified'],
            'neutral': ['analysis', 'examination', 'review', 'evaluation', 'assessment']
        }
        
        text_lower = text.lower()
        emotions = []
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotions.append((emotion, min(0.8, score * 0.2)))
        
        return emotions if emotions else [('neutral', 0.5)]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text for symbol generation."""
        # Simple keyword extraction (could be enhanced with NLP)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Filter to relevant terms
        relevant_words = []
        for word in set(words):
            if (word in self.session_hot_keywords or 
                any(keyword in word for keyword in self.session_hot_keywords)):
                relevant_words.append(word)
        
        return relevant_words[:5]  # Limit to top 5
    
    def _classify_content_for_memory(self, text: str) -> str:
        """Classify content to determine appropriate memory storage type."""
        text_lower = text.lower()
        
        # Symbolic indicators (meaning, philosophy, values)
        symbolic_keywords = [
            'meaning', 'purpose', 'philosophy', 'ethics', 'morality', 'values',
            'consciousness', 'awareness', 'identity', 'self', 'existence',
            'belief', 'wisdom', 'truth', 'beauty', 'love', 'hope', 'fear',
            'spiritual', 'metaphysical', 'phenomenology', 'existential'
        ]
        
        # Logical indicators (analysis, research, technical)
        logical_keywords = [
            'analysis', 'research', 'study', 'experiment', 'data', 'results',
            'method', 'approach', 'algorithm', 'system', 'process', 'technique',
            'evidence', 'proof', 'theorem', 'hypothesis', 'conclusion',
            'implementation', 'optimization', 'performance', 'efficiency'
        ]
        
        symbolic_score = sum(1 for keyword in symbolic_keywords if keyword in text_lower)
        logical_score = sum(1 for keyword in logical_keywords if keyword in text_lower)
        
        # Classification logic
        if symbolic_score > logical_score and symbolic_score >= 2:
            return "symbolic"
        elif logical_score > symbolic_score and logical_score >= 2:
            return "logical"
        else:
            return "bridge"  # Mixed or unclear content goes to bridge memory
    
    def _cognitive_health_check(self):
        """Check AI's cognitive health during learning."""
        print(f"\\n🔍 Cognitive health check at {self.session_stats['urls_processed']} URLs...")
        
        # Check for learning distress
        distress = self.evolution_anchor.detect_evolution_distress()
        
        if distress['distress_level'] > 0.5:
            print(f"   ⚠️ Elevated distress: {distress['distress_level']:.2f}")
            print(f"   💭 Recommendation: {distress.get('recommendation', 'Monitor closely')}")
            
            # If distress is very high, pause learning
            if distress['distress_level'] > 0.8:
                print("   🛑 High distress detected - pausing learning for 30 seconds...")
                time.sleep(30)
        else:
            print("   ✅ Cognitive health stable")
    
    def _run_evolution_cycle(self):
        """Run a memory evolution cycle during learning.

        DISABLED March 28, 2026: The old memory_evolution_engine uses keyword-based
        migration (bridge_reclassifier) and reverse_migration which conflict with the
        new adaptive_bridge_migration cosine-based system. The old system caused
        catastrophic memory loss (8,294 → 286 items) by running alongside the new one.

        Migration is now handled ONLY by adaptive_bridge_migration.AdaptiveMigrationEngine
        which runs at session finalization in _finalize_learning_session().
        """
        print(f"\n   Evolution cycle: handled by adaptive migration at session end")

    def _run_self_correction_cycle(self):
        """Run self-correction cycle: discover outcomes and adjust patterns."""
        print(f"\\n🔧 Running self-correction cycle at {self.session_stats['urls_processed']} URLs...")

        try:
            # Discover outcomes through corroboration
            outcomes_discovered = self.self_correction.discover_outcomes_from_corroboration(
                self.corroboration_engine,
                self.trust_db
            )

            if outcomes_discovered > 0:
                # Run auto-adjustment based on discovered outcomes
                adjustments = self.self_correction.auto_adjust_thresholds()

                if adjustments:
                    # Update immune system pattern weights
                    new_weights = self.self_correction.get_pattern_weights()
                    self.immune_system.pattern_weights.update(new_weights)
                    self.immune_system._save_pattern_weights()
                    print(f"   ✅ Applied {len(adjustments)} pattern weight adjustments")

                # Get and display accuracy stats
                stats = self.self_correction.get_accuracy_stats()
                if stats.decisions_with_outcomes > 10:
                    print(f"   📊 Accuracy: {stats.accuracy_rate:.1%} (FP: {stats.false_positive_rate:.1%}, FN: {stats.false_negative_rate:.1%})")
            else:
                print("   ✓ No new outcomes discovered")

        except Exception as e:
            print(f"   ❌ Self-correction error: {str(e)[:50]}...")
            # Don't let self-correction errors break learning
    
    def _snapshot_store_counts(self):
        """Measure current store sizes (logic/symbolic/bridge/symbols) for delta reporting."""
        counts = {'logic': 0, 'symbolic': 0, 'bridge': 0, 'symbols': 0}
        try:
            tri = self.unified_memory.get_counts()
            for k in ('logic', 'symbolic', 'bridge'):
                counts[k] = tri.get(k, 0)
        except Exception:
            pass
        try:
            counts['symbols'] = len(self.unified_memory.symbol_memory.load_symbol_memory())
        except Exception:
            pass
        return counts

    def _finalize_learning_session(self, elapsed_time: float):
        """Finalize and save the learning session."""
        print(f"\\n🎯 MASSIVE LEARNING SESSION COMPLETE")
        print("=" * 50)

        # Final stats
        end_counts = self._snapshot_store_counts()
        start_counts = getattr(self, '_session_start_counts', None) or dict(end_counts)
        store_delta = {k: end_counts[k] - start_counts.get(k, end_counts[k]) for k in end_counts}
        self._session_store_delta = store_delta
        print(f"⏱️ Duration: {elapsed_time/60:.1f} minutes")
        print(f"📊 URLs processed: {self.session_stats['urls_processed']}")
        print(f"🧠 Stored this session (measured): {store_delta['logic']:+d} logic, "
              f"{store_delta['symbolic']:+d} symbolic, {store_delta['bridge']:+d} bridge")
        print(f"💡 New symbols (measured): {store_delta['symbols']:+d}"
              f" (symbol generation attempts: {self.session_stats['symbols_discovered']})")
        print(f"🔗 Links followed: {self.session_stats['links_followed']}")
        print(f"\n🛡️ LAYERED SECURITY STATS:")
        print(f"   • Robots.txt blocks: {self.session_stats['robots_blocks']}")
        print(f"   • Immune blocks (page-level): {self.session_stats['immune_blocks']}")
        print(f"   • Warfare blocks (chunk-level): {self.session_stats['security_blocks']}")
        print(f"   • Corroboration deferrals: {self.session_stats['corroboration_deferrals']}")
        print(f"   • Trust adjustments: {self.session_stats['trust_adjustments']}")
        print(f"\n⏱️ CRAWL INFRASTRUCTURE STATS:")
        print(f"   • Rate limit waits: {self.session_stats['rate_limit_waits']}")
        crawl_stats = self.crawl_orchestrator.get_stats()
        print(f"   • URLs in queue: {crawl_stats['queue']['pending']}")
        print(f"   • Avg crawl delay: {crawl_stats['rate_limiter']['avg_crawl_delay']:.1f}s")
        
        # Final cognitive assessment
        final_stats = self.analyzer.get_memory_stats()
        tripartite = final_stats['total_items']  # logic+symbolic+bridge
        unified = self.unified_memory.get_canonical_total()
        print(f"🧠 Final memory: {tripartite} tripartite items, {unified} total (including vectors/trails/symbols), {final_stats['health_indicators']['status']} health")

        # Final evolution cycle
        print(f"\\n🧬 Running final evolution cycle...")
        self._run_evolution_cycle()

        # Save session log
        session_summary = {
            'session_id': self.session_id,
            'completed_at': datetime.now().isoformat(),
            'elapsed_time_minutes': elapsed_time / 60,
            'stats': self.session_stats,
            'measured_store_deltas': getattr(self, '_session_store_delta', {}),
            'final_memory_stats': {**final_stats, 'unified_total': unified},
            'processed_domains': dict(self.domain_stats)
        }
        
        session_file = self.session_dir / f"{self.session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_summary, f, indent=2)
        
        print(f"Session saved: {session_file}")

        # Run adaptive migration after learning session
        # All content entered bridge during this session — now check if
        # any items have sufficient cosine gravity to migrate to logic/symbolic
        try:
            from adaptive_bridge_migration import AdaptiveMigrationEngine
            migration_engine = AdaptiveMigrationEngine(
                self.unified_memory.tripartite if hasattr(self.unified_memory, 'tripartite') else self.unified_memory,
                data_dir=str(self.data_dir)
            )

            # Collect embeddings from this session's items for weighted recontextualization
            session_embeddings = []
            for item in self.unified_memory.bridge_memory if hasattr(self.unified_memory, 'bridge_memory') else []:
                emb = item.get('embedding')
                if emb is not None:
                    session_embeddings.append(np.array(emb))

            print(f"\nRunning adaptive migration...")
            migration_results = migration_engine.check_and_migrate(session_embeddings)

            if migration_results.get('forward_migration'):
                fm = migration_results['forward_migration']
                print(f"   Forward: {fm['migrated_to_logic']} → logic, {fm['migrated_to_symbolic']} → symbolic, {fm['remained_in_bridge']} remain in bridge")
            if migration_results.get('recontextualization'):
                rc = migration_results['recontextualization']
                print(f"   Recontextualization: {rc['reversed_from_logic'] + rc['reversed_from_symbolic']} items returned to bridge")
            print(f"   Drift detected: {migration_results.get('drift_detected', False)}")
        except ImportError:
            print("   Migration engine not available")
        except Exception as e:
            print(f"   Migration error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

        # Reprioritize pending queue URLs by session centroid relevance
        # No URLs are dropped — low-relevance items sink, high-relevance items rise
        if self.session_centroid is not None and self.session_coherence_stats is not None:
            try:
                repri_result = self.crawl_orchestrator.url_queue.reprioritize_by_relevance(
                    self.session_centroid, self.session_coherence_stats
                )
                if repri_result.get('reprioritized', 0) > 0:
                    print(f"\n   Queue reprioritized: {repri_result['reprioritized']}/{repri_result['total_pending']} "
                          f"pending URLs reordered by topic relevance (dc={repri_result['density_confidence']:.2f})")
            except Exception as e:
                print(f"   Queue reprioritization skipped: {e}")

    def _emergency_session_save(self):
        """Emergency save during interrupted sessions."""
        print(f"\\n💾 Emergency session save...")
        
        emergency_data = {
            'session_id': self.session_id,
            'interrupted_at': datetime.now().isoformat(),
            'partial_stats': self.session_stats,
            'urls_in_queue': len(self.url_queue),
            'processed_count': len(self.processed_urls)
        }
        
        emergency_file = self.session_dir / f"{self.session_id}_emergency.json"
        with open(emergency_file, 'w', encoding='utf-8') as f:
            json.dump(emergency_data, f, indent=2)
        
        print(f"✅ Emergency data saved: {emergency_file}")
        try:
            self._run_migration_cleanup()
        except Exception:
            pass  # emergency save must not fail

    def _run_migration_cleanup(self):
        try:
            from adaptive_bridge_migration import AdaptiveMigrationEngine
            engine = AdaptiveMigrationEngine(
                self.unified_memory.tripartite, str(self.data_dir))
            engine.check_and_migrate([])
        except Exception as e:
            print(f"Migration cleanup error: {e}")

    def _integrate_learning_progression(self):
        """Integrate session results with learning progression tracker."""
        print(f"\n🧠 Integrating learning progression...")
        
        try:
            # Let progression tracker analyze this session
            integration_result = self.progression_tracker.integrate_with_autonomous_learner(self)
            
            if integration_result.get("integration_successful"):
                print(f"   ✅ Tracked {integration_result['concepts_tracked']} concepts")
                print(f"   ✅ Recorded {integration_result['milestones_recorded']} milestones")
                
                # Integrate curiosity engine with progression
                curiosity_result = self.curiosity_engine.integrate_with_learning_progression(self.progression_tracker)
                if curiosity_result.get("integration_successful"):
                    print(f"   🎯 Generated {curiosity_result['new_goals_generated']} curiosity-driven goals")
                    print(f"   🔄 Made {curiosity_result['drive_adjustments_made']} drive satisfaction adjustments")
                
                # Generate learning awareness insights
                insights = self.progression_tracker.generate_learning_awareness_insights()
                if insights:
                    print(f"   💡 Learning insights generated:")
                    for insight in insights[:3]:  # Show top 3
                        print(f"      • {insight}")
                
                # Generate curiosity insights
                curiosity_insights = self.curiosity_engine.generate_curiosity_insights()
                if curiosity_insights:
                    print(f"   🌱 Curiosity insights generated:")
                    for insight in curiosity_insights[:2]:  # Show top 2
                        print(f"      • {insight}")
                
                # Export consciousness data first
                consciousness_data = self.progression_tracker.export_for_consciousness_system()
                curiosity_data = self.curiosity_engine.export_for_consciousness_system()
                
                # Generate personal insights from the learning session
                session_data = {
                    "urls_processed": self.session_stats["urls_processed"],
                    "concepts_discovered": [f"concept_{i}" for i in range(self.session_stats.get("symbols_discovered", 0))],
                    "learning_momentum": consciousness_data.get("learning_confidence", 0.5)
                }
                personal_insights = self.insight_generator.generate_consciousness_insights(session_data)
                if personal_insights:
                    print(f"   💭 Personal insights generated:")
                    for insight in personal_insights[:2]:  # Show top 2
                        print(f"      • {insight}")
                
                print(f"   🌟 Self-awareness level: {consciousness_data['self_awareness_level']:.2f}")
                print(f"   🎯 Learning confidence: {consciousness_data['learning_confidence']:.2f}")
                print(f"   🔥 Motivation level: {curiosity_data['autonomous_motivation_level']:.2f}")
                print(f"   🎪 Active curiosity goals: {len(curiosity_data['active_learning_goals'])}")
                
            else:
                print(f"   ⚠️ Integration had issues: {integration_result}")
                
        except Exception as e:
            print(f"   ❌ Error integrating progression: {str(e)[:50]}...")
    
    def _stimulate_curiosity_from_content(self, text_content: str):
        """Stimulate curiosity engine based on processed content."""
        try:
            # Create content summary (first 200 chars)
            content_summary = text_content[:200] + "..." if len(text_content) > 200 else text_content
            
            # Stimulate curiosity
            stimulation_result = self.curiosity_engine.stimulate_curiosity_from_content(content_summary)
            
            if stimulation_result.get("curiosity_stimulated"):
                # Curiosity was stimulated - this affects learning behavior
                stimulation_level = stimulation_result["stimulation_level"]
                
                # High curiosity content gets priority in link evaluation
                if stimulation_level > 0.6:
                    # Boost exploration bias temporarily
                    self.curiosity_engine.curiosity_state["exploration_bias"] = min(1.0,
                        self.curiosity_engine.curiosity_state.get("exploration_bias", 0.3) + 0.1)
                    if hasattr(self.curiosity_engine, '_save_curiosity_state'):
                        self.curiosity_engine._save_curiosity_state()

        except Exception as e:
            # Don't let curiosity errors break content processing
            pass
    
    def _generate_insights_from_content(self, text_content: str, url_info: Dict):
        """Generate personal insights from processed content."""
        try:
            # Create context for insight generation
            context = {
                "content_type": "web_content",
                "source": url_info.get("url", "unknown"),
                "learning_phase": url_info.get("depth", 0),
                "discovery_context": url_info.get("context", "autonomous_learning")
            }
            
            # Generate reminder insights from content
            reminder_insights = self.insight_generator.generate_reminder_insights_from_content(
                text_content, context
            )
            
            # Store insights (limit processing to avoid spam)
            if reminder_insights and len(reminder_insights) > 0:
                # Only process insights occasionally to avoid overwhelming output
                if random.random() < 0.1:  # 10% chance
                    print(f"   💭 Content insight: {reminder_insights[0]}")
                
        except Exception as e:
            # Don't let insight errors break content processing
            pass
    
    def _evaluate_content_motivation(self, text_content: str, url_info: Dict):
        """Evaluate content through motivational lens for autonomous content selection."""
        try:
            # Create content object for evaluation
            content = {
                "text": text_content,
                "url": url_info.get("url", "unknown"),
                "content_type": "web_content",
                "discovery_depth": url_info.get("depth", 0)
            }
            
            # Evaluate content autonomously through motivation system
            evaluation_result = self.motivation_evaluator.evaluate_content_autonomously(content)
            
            if evaluation_result:
                # Only show high-motivation content evaluations to avoid spam
                motivation_level = evaluation_result["evaluation_confidence"]
                if motivation_level > 0.7:  # Only show high-motivation content
                    recommendation = evaluation_result["autonomous_recommendation"]
                    print(f"   🎯 Motivation: {motivation_level:.2f} → {recommendation}")
                
                # Learn from this evaluation
                if random.random() < 0.05:  # 5% chance for learning
                    engagement_data = {
                        "interest_score": motivation_level,
                        "dwell_time": 30,  # Simulated engagement
                        "deep_processing": motivation_level
                    }
                    self.motivation_evaluator.learn_from_engagement(content, engagement_data)
                
        except Exception as e:
            # Don't let motivation errors break content processing
            pass

    def generate_session_report(self) -> str:
        """
        Generate comprehensive session report with JEPA delta, chaos state, and decisions.
        Writes to data/logs/session_reports/REPORT_[timestamp].md

        Returns:
            Path to generated report file
        """
        from datetime import datetime, timezone
        import statistics

        # Create reports directory
        reports_dir = self.data_dir / "logs" / "session_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"REPORT_{timestamp}.md"

        # Calculate summary statistics
        avg_surprise = statistics.mean([s['surprise'] for s in self.surprise_history]) if self.surprise_history else 0.0
        max_surprise = max([s['surprise'] for s in self.surprise_history]) if self.surprise_history else 0.0
        final_chaos_factor = self._get_chaos_factor()

        # Get current Chen state
        x, y, z = self.chen_state

        # Build report
        report_lines = [
            f"# Autonomous Learning Session Report",
            f"",
            f"**Generated:** {datetime.now().isoformat()}",
            f"**Session ID:** {self.session_id}",
            f"**Experience Count:** {self.experience_count}",
            f"",
            f"---",
            f"",
            f"## 🌀 Chaos-Regularized Optimization State",
            f"",
            f"**Chen Attractor Parameters:**",
            f"- a = {self.chen_a}",
            f"- b = {self.chen_b}",
            f"- c = {self.chen_c}",
            f"",
            f"**Current State:**",
            f"- x = {x:.4f}",
            f"- y = {y:.4f}",
            f"- z = {z:.4f}",
            f"",
            f"**Annealing Progress:**",
            f"- Initial chaos strength (α): {self.chaos_alpha}",
            f"- Decay constant (τ): {self.chaos_tau}",
            f"- Current chaos factor: {final_chaos_factor:.4f}",
            f"- Experiences processed: {self.experience_count}",
            f"- Completion: {min(100, (self.experience_count / self.chaos_tau) * 100):.1f}%",
            f"",
            f"**Interpretation:**",
            f"- Chaos strength decreases exponentially with experience",
            f"- Early phase: High chaos → Prevents premature value formation (trauma encoding)",
            f"- Late phase: Low chaos → Allows robust value consolidation (flat minima)",
            f"",
            f"---",
            f"",
            f"## 🎯 JEPA (Joint-Embedding Predictive Architecture) Metrics",
            f"",
            f"**Surprise Statistics:**",
            f"- Total predictions: {len(self.surprise_history)}",
            f"- Average surprise: {avg_surprise:.3f}",
            f"- Maximum surprise: {max_surprise:.3f}",
            f"- Surprise range: [0.0 = no surprise, 1.0 = maximum surprise]",
            f"",
            f"**Top 10 Most Surprising Discoveries:**",
        ]

        # Add top 10 surprising URLs
        sorted_surprises = sorted(self.surprise_history, key=lambda x: x['surprise'], reverse=True)
        for i, item in enumerate(sorted_surprises[:10], 1):
            report_lines.append(f"{i}. **{item['surprise']:.3f}** - {item['url'][:80]}...")
            report_lines.append(f"   - Chaos factor at discovery: {item['chaos_factor']:.3f}")
            report_lines.append(f"   - Experience #{item['experience_count']}")

        if not self.surprise_history:
            report_lines.append("(No JEPA data collected this session)")

        report_lines.extend([
            f"",
            f"---",
            f"",
            f"## 📊 Learning Session Statistics",
            f"",
            f"**Content Processing:**",
            f"- URLs processed: {self.session_stats['urls_processed']}",
            f"- Chunks learned: {self.session_stats['chunks_learned']}",
            f"- Symbols discovered: {self.session_stats['symbols_discovered']}",
            f"- Links followed: {self.session_stats['links_followed']}",
            f"",
            f"**Layered Security:**",
            f"- Robots.txt blocks: {self.session_stats['robots_blocks']}",
            f"- Immune system blocks: {self.session_stats['immune_blocks']}",
            f"- Linguistic warfare blocks: {self.session_stats['security_blocks']}",
            f"- Corroboration deferrals: {self.session_stats['corroboration_deferrals']}",
            f"- Trust adjustments: {self.session_stats['trust_adjustments']}",
            f"",
            f"**Crawl Infrastructure:**",
            f"- Rate limit waits: {self.session_stats['rate_limit_waits']}",
            f"",
            f"---",
            f"",
            f"## 🛡️ Corroboration & Trust Status",
            f"",
        ])

        # Get trust database summary
        try:
            trust_summary = self.trust_db.get_trust_summary()
            report_lines.extend([
                f"**Domain Trust Statistics:**",
                f"- Total domains tracked: {trust_summary.get('total_domains', 0)}",
                f"- High-trust domains (>0.7): {trust_summary.get('high_trust_count', 0)}",
                f"- Low-trust domains (<0.3): {trust_summary.get('low_trust_count', 0)}",
                f"- Average trust score: {trust_summary.get('average_trust', 0.5):.3f}",
                f"",
            ])
        except Exception:
            report_lines.append("(Trust summary unavailable)")
            report_lines.append("")

        report_lines.extend([
            f"---",
            f"",
            f"## 🧠 Autonomous Decision Summary",
            f"",
            f"**Value Formation Decisions:**",
            f"This session operated under **Radical Autonomy** protocol:",
            f"- Human approval: DEPRECATED",
            f"- Authority: Corroboration (multi-source validation)",
            f"- Threshold: emotional_intensity > 0.6 AND corroboration > 0.7",
            f"- Chaos regularization: ACTIVE (prevents sharp minima)",
            f"",
            f"**Learning Commitment Decisions:**",
            f"- Base threshold: 0.4 (surprise)",
            f"- Chaos perturbation: ±0.2 * chaos_factor * chen_state_x",
            f"- Adaptive threshold: {0.4 + (x * final_chaos_factor * 0.2):.3f} (current)",
            f"- Corroboration requirement: 0.7 (fixed)",
            f"",
            f"---",
            f"",
            f"## 📈 Session Trends",
            f"",
        ])

        # Add surprise trend analysis
        if len(self.surprise_history) >= 10:
            early_surprises = [s['surprise'] for s in self.surprise_history[:10]]
            late_surprises = [s['surprise'] for s in self.surprise_history[-10:]]
            early_avg = statistics.mean(early_surprises)
            late_avg = statistics.mean(late_surprises)
            trend = "INCREASING" if late_avg > early_avg else "DECREASING"

            report_lines.extend([
                f"**Surprise Trend:**",
                f"- Early session average (first 10): {early_avg:.3f}",
                f"- Late session average (last 10): {late_avg:.3f}",
                f"- Trend: {trend}",
                f"- Interpretation: {trend.lower()} surprise indicates {'novel content discovery' if trend == 'INCREASING' else 'pattern consolidation'}",
                f"",
            ])

        report_lines.extend([
            f"---",
            f"",
            f"## 🔬 Mathematical Foundation",
            f"",
            f"This session's learning is governed by:",
            f"",
            f"**1. Chen Dynamical System:**",
            f"```",
            f"dx/dt = a(y − x)           = {self.chen_a}(y − x)",
            f"dy/dt = (c − a)x − xz + cy = {self.chen_c - self.chen_a}x − xz + {self.chen_c}y",
            f"dz/dt = xy − bz            = xy − {self.chen_b}z",
            f"```",
            f"",
            f"**2. Annealing Schedule:**",
            f"```",
            f"λₜ = α·exp(−t/τ) = {self.chaos_alpha}·exp(−{self.experience_count}/{self.chaos_tau}) = {final_chaos_factor:.4f}",
            f"```",
            f"",
            f"**3. Surprise Calculation (JEPA):**",
            f"```",
            f"surprise = 1 − cosine_similarity(prediction, reality)",
            f"```",
            f"",
            f"**4. Adaptive Learning Threshold:**",
            f"```",
            f"threshold = 0.4 + chen_x * λₜ * 0.2",
            f"threshold = 0.4 + {x:.3f} * {final_chaos_factor:.3f} * 0.2 = {0.4 + (x * final_chaos_factor * 0.2):.3f}",
            f"```",
            f"",
            f"---",
            f"",
            f"## 📚 References",
            f"",
            f"1. **Chaos-Regularized Optimization** - See `/docs/technical/research_papers/CHAOS_REGULARIZED_OPTIMIZATION.md`",
            f"2. **Chen & Ueta (1999)** - Yet another chaotic attractor",
            f"3. **LeCun (2022)** - A Path Towards Autonomous Machine Intelligence (JEPA)",
            f"4. **Foret et al. (2021)** - Sharpness-aware minimization (SAM)",
            f"",
            f"---",
            f"",
            f"**Report Status:** COMPLETE",
            f"**Generated by:** Sophia AI Autonomous Learner",
            f"**Protocol:** Radical Autonomy (Corroboration-Based)",
            f"",
        ])

        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))

        print(f"\n📄 Session report generated: {report_path}")
        return str(report_path)

    def get_learning_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state including learning progression."""
        
        consciousness_state = {
            "session_stats": self.session_stats,
            "learning_progression": None,
            "curiosity_state": None,
            "insight_state": None,
            "motivation_state": None,
            "consciousness_insights": [],
            "curiosity_insights": [],
            "personal_insights": [],
            "motivation_insights": [],
            "self_awareness_metrics": {}
        }
        
        try:
            # Get progression data
            consciousness_state["learning_progression"] = self.progression_tracker.export_for_consciousness_system()
            
            # Get curiosity data
            consciousness_state["curiosity_state"] = self.curiosity_engine.export_for_consciousness_system()
            
            # Get insight data
            consciousness_state["insight_state"] = self.insight_generator.export_for_consciousness_system()
            
            # Get motivation data
            consciousness_state["motivation_state"] = self.motivation_evaluator.export_for_consciousness_system()
            
            # Get current insights
            consciousness_state["consciousness_insights"] = self.progression_tracker.generate_learning_awareness_insights()
            consciousness_state["curiosity_insights"] = self.curiosity_engine.generate_curiosity_insights()
            consciousness_state["personal_insights"] = self.insight_generator.generate_reflection_insights(consciousness_state)
            consciousness_state["motivation_insights"] = self.motivation_evaluator.generate_motivation_insights()
            
            # Calculate self-awareness metrics
            progression_data = consciousness_state["learning_progression"]
            curiosity_data = consciousness_state["curiosity_state"]
            consciousness_state["self_awareness_metrics"] = {
                "conceptual_breadth": progression_data["progression_summary"]["total_concepts"],
                "understanding_depth": progression_data["progression_summary"]["overall_understanding"],
                "learning_momentum": progression_data["progression_summary"]["learning_momentum"],
                "motivation_level": curiosity_data["autonomous_motivation_level"],
                "curiosity_intensity": curiosity_data["curiosity_summary"]["curiosity_intensity"],
                "active_goals": curiosity_data["curiosity_summary"]["active_goals"],
                "consciousness_level": min(1.0, (
                    progression_data["self_awareness_level"] * 0.3 +
                    progression_data["learning_confidence"] * 0.2 +
                    curiosity_data["autonomous_motivation_level"] * 0.3 +
                    self.session_stats["urls_processed"] / 100 * 0.2
                ))
            }
            
        except Exception as e:
            consciousness_state["error"] = f"Could not access progression data: {e}"
        
        return consciousness_state

    # ═══════════════════════════════════════════════════════════════
    # ASSOCIATIVE EMERGENCE: SATURATION LEARNING METHODS
    # ═══════════════════════════════════════════════════════════════

    def run_saturation_session(self, seed_url: str, zone_definition: Dict[str, Any],
                              saturation_threshold: float = 0.8, max_urls: int = 100):
        """
        ASSOCIATIVE EMERGENCE: Deep saturation learning in a semantic zone.

        Instead of following a linear curriculum, this method:
        1. Starts with a high-density seed (e.g., Silicon)
        2. Stays within a semantic "zone" defined by vector similarity
        3. Learns deeply until process verbs emerge more than static nouns
        4. Only then generates the query for the next phase

        Args:
            seed_url: Starting URL (e.g., https://en.wikipedia.org/wiki/Silicon)
            zone_definition: Dict with 'name', 'keywords', 'allowed_distance'
            saturation_threshold: Transition when phase_transition_score > this (default 0.8)
            max_urls: Safety limit for URLs processed in this zone

        Returns:
            Dict with session results and next phase information
        """
        print("\n" + "="*80)
        print("🌀 ASSOCIATIVE EMERGENCE: SATURATION LEARNING SESSION")
        print("="*80)
        print(f"\n📍 Semantic Zone: {zone_definition['name']}")
        print(f"🌱 Seed URL: {seed_url}")
        print(f"🎯 Saturation Threshold: {saturation_threshold}")
        print(f"📊 Max URLs in Zone: {max_urls}")

        # Initialize session
        self.session_id = f"saturation_{zone_definition['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = time.time()

        # Initialize saturation state for this zone
        self.saturation_state['current_zone'] = zone_definition['name']
        self.saturation_state['zone_keywords'] = zone_definition.get('keywords', [])
        self.saturation_state['processed_in_zone'] = 0
        self.saturation_state['keyword_frequencies'] = defaultdict(int)
        self.saturation_state['static_noun_count'] = 0
        self.saturation_state['process_verb_count'] = 0
        self.saturation_state['vector_drift'] = []
        self.saturation_state['event_horizon'] = []
        self.saturation_state['zone_embeddings'] = []
        self.saturation_state['phase_transition_score'] = 0.0

        # Calculate zone centroid from keywords
        self._calculate_zone_centroid(zone_definition['keywords'])

        print(f"\n🎯 Zone Centroid calculated from {len(zone_definition['keywords'])} keywords")
        print(f"   Allowed semantic distance: {zone_definition.get('allowed_distance', 0.5)}")

        # Initialize URL queue with seed
        self.url_queue = deque()
        self.processed_urls = set()
        self.queued_urls = {seed_url}
        self.url_queue.append({
            'url': seed_url,
            'depth': 0,
            'priority': 1.0,
            'source': 'seed',
            'context': zone_definition['name']
        })

        # Saturation loop
        print("\n🌊 Beginning deep saturation...")
        print("   Strategy: Stay in zone until process verbs > static nouns")
        print()

        try:
            while len(self.url_queue) > 0 and self.saturation_state['processed_in_zone'] < max_urls:

                # Get next URL
                url_info = self.url_queue.popleft()
                url = url_info['url']

                # Skip if already seen (processed or failed)
                if url in self.processed_urls:
                    continue

                # Mark as seen immediately to prevent retries
                self.processed_urls.add(url)

                # Process this URL
                print(f"\n{'─'*80}")
                print(f"📄 [{self.saturation_state['processed_in_zone'] + 1}/{max_urls}] {url[:70]}...")

                # Fetch and process
                success = self._process_url_in_saturation_mode(url_info, zone_definition)

                if success:
                    self.saturation_state['processed_in_zone'] += 1

                    # Update saturation state
                    self._update_saturation_state()

                    # Check for phase transition
                    transition_score = self.check_phase_transition()

                    print(f"\n📊 Saturation Metrics:")
                    print(f"   Static Nouns:   {self.saturation_state['static_noun_count']:4d} (Rock, Stone, Silicon)")
                    print(f"   Process Verbs:  {self.saturation_state['process_verb_count']:4d} (Smelt, Refine, Extract)")
                    print(f"   Phase Score:    {transition_score:.3f} / {saturation_threshold:.3f}")

                    # 🧠 DEPTH REFLECTION: Show Sophia her growing understanding (every 5 URLs)
                    if self.saturation_state['processed_in_zone'] % 5 == 0:
                        self._show_depth_reflection(zone_definition['name'])

                    if transition_score >= saturation_threshold:
                        print(f"\n✨ PHASE TRANSITION DETECTED! ✨")
                        print(f"   The gravity of the next phase is stronger than the current phase.")
                        print(f"   Process verbs have emerged naturally from deep material understanding.")
                        break

                # Rate limiting handled by prepare_crawl(wait_if_needed=True)

            # Finalize session
            elapsed_time = time.time() - start_time

            # Generate next phase query if transition detected
            next_phase_query = None
            if self.saturation_state['phase_transition_score'] >= saturation_threshold:
                next_phase_query = self._generate_next_phase_query()

            # Save session results
            session_result = self._finalize_saturation_session(elapsed_time, next_phase_query)

            return session_result

        except KeyboardInterrupt:
            print("\n⚠️ Saturation session interrupted by user")
            elapsed_time = time.time() - start_time
            return self._finalize_saturation_session(elapsed_time, None)
        except Exception as e:
            print(f"\n❌ Saturation session error: {e}")
            import traceback
            traceback.print_exc()
            elapsed_time = time.time() - start_time
            return self._finalize_saturation_session(elapsed_time, None)

    def check_phase_transition(self) -> float:
        """
        VECTOR GRAVITY TRIGGER: Detect when ready to evolve to next phase.

        Transition Logic:
        - When process verbs (Smelt, Burn, Refine) > static nouns (Stone, Rock, Ore)
        - The "gravity" of transformation is stronger than material properties
        - This indicates natural emergence of next phase

        Returns:
            Float between 0.0 and 1.0 indicating readiness to transition
        """
        static_count = self.saturation_state['static_noun_count']
        process_count = self.saturation_state['process_verb_count']
        total_count = static_count + process_count

        if total_count == 0:
            return 0.0

        # Base score: ratio of process verbs to total
        verb_ratio = process_count / total_count

        # Vector drift score: how far has embedding centroid drifted?
        drift_score = 0.0
        if len(self.saturation_state['vector_drift']) > 1:
            # Compare first and last embeddings
            initial_embedding = self.saturation_state['vector_drift'][0]
            current_embedding = self.saturation_state['vector_drift'][-1]

            # Calculate cosine distance (1 - similarity)
            similarity = cosine_similarity(
                np.array(initial_embedding).reshape(1, -1),
                np.array(current_embedding).reshape(1, -1)
            )[0][0]
            drift_score = 1.0 - similarity  # Higher drift = more change

        # Event horizon score: how many forbidden concepts have we seen?
        horizon_score = min(1.0, len(self.saturation_state['event_horizon']) / 10.0)

        # Combined score (weighted)
        transition_score = (
            verb_ratio * 0.5 +        # 50%: Process verbs dominating
            drift_score * 0.3 +        # 30%: Semantic drift from origin
            horizon_score * 0.2        # 20%: Concepts on event horizon
        )

        # Curiosity momentum can nudge transition score ±5%
        try:
            motivation = self.curiosity_engine.get_current_motivation_state()
            momentum = motivation.get('curiosity_momentum', 0.5)
            curiosity_modifier = (momentum - 0.5) * 0.1  # Range: -0.05 to +0.05
            transition_score += curiosity_modifier
        except Exception:
            pass

        transition_score = max(0.0, min(1.0, transition_score))
        self.saturation_state['phase_transition_score'] = transition_score
        return transition_score

    def _calculate_zone_centroid(self, keywords: List[str]):
        """
        Calculate the vector centroid of a semantic zone from keywords.
        This defines the "center of gravity" for the allowed learning area.
        """
        embeddings = []

        for keyword in keywords:
            vec, _ = fuse_vectors(keyword)
            if vec is not None:
                embeddings.append(vec)

        if len(embeddings) > 0:
            # Calculate mean of all keyword embeddings
            centroid = np.mean(embeddings, axis=0)
            self.saturation_state['zone_centroid'] = centroid.tolist()
        else:
            print("   ⚠️ Warning: Could not calculate zone centroid (no valid embeddings)")
            self.saturation_state['zone_centroid'] = None

    def _calculate_semantic_distance(self, text: str) -> Optional[float]:
        """
        Calculate semantic distance of text from zone centroid.

        Returns:
            Float distance (0.0 = identical, 1.0 = completely different)
            None if calculation fails
        """
        if self.saturation_state['zone_centroid'] is None:
            return None

        # Get embedding for text
        vec, _ = fuse_vectors(text)
        if vec is None:
            return None

        # Calculate cosine similarity with centroid
        centroid = np.array(self.saturation_state['zone_centroid']).reshape(1, -1)
        text_vec = np.array(vec).reshape(1, -1)

        similarity = cosine_similarity(centroid, text_vec)[0][0]
        distance = 1.0 - similarity  # Convert similarity to distance

        return distance

    def _process_url_in_saturation_mode(self, url_info: Dict, zone_definition: Dict) -> bool:
        """
        Process a single URL in saturation mode with zone filtering.

        Returns:
            True if processing succeeded, False otherwise
        """
        url = url_info['url']

        # Robots.txt check only — rate limiting is handled by prepare_crawl() which waits
        can_crawl, reason = self.crawl_orchestrator.can_crawl(url, check_rate_limit=False)
        if not can_crawl:
            print(f"   🤖 Blocked by robots.txt")
            self.session_stats['robots_blocks'] += 1
            self._emit_crawl_event(url, 'robots_blocked', parent_url=url_info.get('source'))
            return False

        # Prepare and execute crawl (waits for rate limit instead of rejecting)
        url_id = self.crawl_orchestrator.prepare_crawl(url, wait_if_needed=True)
        if not url_id:
            print(f"   ⏭️  Skipped: crawl preparation failed")
            self._emit_crawl_event(url, 'robots_blocked', parent_url=url_info.get('source'))
            return False

        # Fetch content
        raw_html = fetch_raw_html(url)
        if not raw_html:
            print(f"   ⏭️  Skipped: fetch failed")
            self._emit_crawl_event(url, 'fetch_failed', parent_url=url_info.get('source'))
            return False

        # Extract text
        text_content = clean_html_to_text(raw_html)
        if not text_content or len(text_content) < 100:
            print(f"   ⏭️  Skipped: content too short ({len(text_content) if text_content else 0} chars)")
            self._emit_crawl_event(url, 'insufficient_content', parent_url=url_info.get('source'))
            return False

        # Extract domain early — needed by both fact extraction and security checks
        domain = urlparse(url).netloc

        # Language detection — short-circuit non-English content
        detected_lang, lang_confidence = self._detect_language(text_content)
        if detected_lang and detected_lang != 'en' and lang_confidence >= 0.8:
            domain_trust = self.trust_db.get_trust(domain)
            print(f"   🌐 Non-English content detected: {detected_lang} "
                  f"(confidence: {lang_confidence:.2f}) — quarantining")
            _block_event = {
                'url': url,
                'status': 'non_english',
                'parent_url': url_info.get('source'),
                'threat_score': 0.0,
                'text_preview': text_content[:500] if text_content else None,
                'block_category': 'non_english_content',
                'block_signals': [{'type': 'language_detection',
                                   'detected_language': detected_lang,
                                   'confidence': round(lang_confidence, 4)}],
                'block_reasoning': [f"Detected language: {detected_lang} "
                                    f"(confidence {lang_confidence:.2f})",
                                    "Non-English content quarantined for "
                                    "future multilingual capability"],
                'block_confidence': lang_confidence,
                'domain_trust_at_block': domain_trust,
                'session_id': self.session_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
            self._emit_crawl_event(
                url, 'non_english',
                parent_url=url_info.get('source'),
                block_category='non_english_content',
                block_signals=_block_event['block_signals'],
                block_reasoning=_block_event['block_reasoning'],
                domain_trust_at_block=domain_trust,
            )
            try:
                self.quarantine_store.quarantine_item(_block_event)
            except Exception:
                pass
            self.session_stats.setdefault('non_english_blocks', 0)
            self.session_stats['non_english_blocks'] += 1
            return False

        # 🧠 PASSIVE FACT EXTRACTION (runs in background)
        # Extract structured facts and feed into corroboration engine for validation
        try:
            topic = zone_definition.get('name', 'Unknown')
            facts = extract_facts_passive(raw_html, url, topic)

            # Feed extracted facts into corroboration engine
            # Trust score from existing trust database
            trust_score = self.trust_db.get_trust(domain)

            for fact in facts:
                # Generate embedding for fact text
                fact_embedding_list, _ = fuse_vectors(fact['text'])
                if fact_embedding_list is not None:
                    # Convert list to numpy array for corroboration engine
                    fact_embedding = np.array(fact_embedding_list)
                    # Record sighting in corroboration engine
                    # Engine will cluster similar facts and track corroboration
                    self.corroboration_engine.record_sighting(
                        fact_text=fact['text'],
                        fact_embedding=fact_embedding,
                        source_url=url,
                        trust_score=trust_score
                    )

            # Track facts in session stats
            self.session_stats['facts_extracted'] += len(facts)
        except Exception as e:
            # Fact extraction is passive - failures don't stop learning
            # But log the error for debugging
            import traceback
            print(f"   ⚠️  Fact extraction error: {e}")
            if hasattr(self, 'debug_mode') and self.debug_mode:
                traceback.print_exc()

        # Security checks (same as normal processing)
        domain_trust = self.trust_db.get_trust(domain)

        # High-trust bypass for security checks
        if domain_trust <= 0.8:
            # Check immune system
            immune_assessment = self.immune_system.analyze_page(url, raw_html, text_content)
            if immune_assessment.recommendation == 'BLOCK':
                print(f"   🛡️ BLOCKED by immune system (threat: {immune_assessment.overall_threat_score:.2f})")
                self.session_stats['immune_blocks'] += 1
                _block_event = {
                    'url': url,
                    'status': 'immune_blocked',
                    'parent_url': url_info.get('source'),
                    'threat_score': immune_assessment.overall_threat_score,
                    'text_preview': text_content[:500] if text_content else None,
                    'block_category': self._derive_block_category_from_immune(
                        immune_assessment.threat_signals),
                    'block_signals': self._serialize_immune_signals(
                        immune_assessment.threat_signals),
                    'block_reasoning': immune_assessment.reasoning,
                    'block_confidence': immune_assessment.confidence,
                    'domain_trust_at_block': domain_trust,
                    'session_id': self.session_id,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                }
                self._emit_crawl_event(**{k: v for k, v in _block_event.items()
                                          if k not in ('session_id', 'timestamp')})
                try:
                    self.quarantine_store.quarantine_item(_block_event)
                except Exception:
                    pass  # Quarantine must never break learning
                return False

            # Check for linguistic warfare
            should_quarantine, warfare_analysis = check_for_warfare(text_content, url)
            if should_quarantine:
                print(f"   ⚠️ BLOCKED by warfare detector")
                self.session_stats['security_blocks'] += 1
                _block_event = {
                    'url': url,
                    'status': 'warfare_blocked',
                    'parent_url': url_info.get('source'),
                    'threat_score': warfare_analysis.get('threat_score'),
                    'text_preview': text_content[:500] if text_content else None,
                    'block_category': self._derive_block_category_from_warfare(
                        warfare_analysis),
                    'block_signals': self._serialize_warfare_signals(
                        warfare_analysis),
                    'block_defense_strategy': warfare_analysis.get(
                        'defense_strategy', {}).get('strategy'),
                    'domain_trust_at_block': domain_trust,
                    'session_id': self.session_id,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                }
                self._emit_crawl_event(**{k: v for k, v in _block_event.items()
                                          if k not in ('session_id', 'timestamp')})
                try:
                    self.quarantine_store.quarantine_item(_block_event)
                except Exception:
                    pass  # Quarantine must never break learning
                return False

        # Extract keywords and classify
        keywords = self._extract_keywords(text_content)

        # Get embedding for this content
        content_vec, _ = fuse_vectors(text_content[:1000])  # Use first 1000 chars
        if content_vec is not None:
            self.saturation_state['zone_embeddings'].append(content_vec)
            self.saturation_state['vector_drift'].append(content_vec)

        # Final text quality gate before storage
        from web_parser import sanitize_text_for_storage
        sanitized_text = sanitize_text_for_storage(text_content[:2000])
        if not sanitized_text:
            print(f"   ⏭️  Skipped: content failed quality gate (garbage/fragments)")
            self._emit_crawl_event(url, 'quality_failed', parent_url=url_info.get('source'))
            return False

        # Store in memory
        self.session_stats['chunks_learned'] += 1

        # Classify content and route to appropriate memory
        content_type = self._classify_content_for_memory(text_content)
        decision_map = {'symbolic': 'FOLLOW_SYMBOLIC', 'logical': 'FOLLOW_LOGIC', 'bridge': 'FOLLOW_HYBRID'}
        decision = decision_map[content_type]

        item = {
            'text': sanitized_text,
            'source': url,
            'learning_focus': zone_definition['name'],
            'session_id': self.session_id,
            'zone': zone_definition['name']
        }

        self.unified_memory.store_decision(item, decision)

        l_sim, s_sim = self._get_centroid_sims(content_vec) if content_vec is not None else (None, None)
        self._emit_crawl_event(url, 'stored', classification=content_type,
                               parent_url=url_info.get('source'),
                               text_preview=sanitized_text[:80],
                               logic_sim=l_sim, symbolic_sim=s_sim)

        memory_labels = {'symbolic': 'SYMBOLIC', 'logical': 'LOGIC', 'bridge': 'BRIDGE (unresolved)'}
        print(f"   ✅ Learned and stored in {memory_labels[content_type]} memory")

        # Emotion prediction and symbol generation
        try:
            emotions = self._predict_content_emotions(text_content)
            keywords = self._extract_keywords(text_content)
            if keywords:
                from unified_memory import generate_symbol_from_context
                new_symbol = generate_symbol_from_context(text_content, keywords, emotions)
                if new_symbol:
                    self.session_stats['symbols_discovered'] += 1
        except Exception:
            pass  # Emotion/symbol generation is non-critical

        # Extract and filter links (NOTE: function signature is (base_url, html_content))
        links = extract_links_with_text_from_html(url, raw_html)
        filtered_links = self._filter_links_by_zone(links, zone_definition)

        print(f"   🔗 Found {len(links)} links, {len(filtered_links)} within zone")

        # Add filtered links to queue (skip already queued or processed)
        # Process-verb links are sorted first by _filter_links_by_zone
        added = 0
        for link_url, link_text in filtered_links:
            if link_url not in self.queued_urls:
                self.queued_urls.add(link_url)
                self.url_queue.append({
                    'url': link_url,
                    'depth': url_info['depth'] + 1,
                    'priority': 0.8,
                    'source': url,
                    'context': zone_definition['name']
                })
                added += 1
                if added >= 20:
                    break

        # Record successful crawl
        self.crawl_orchestrator.record_success(url_id, url)
        self.session_stats['urls_processed'] += 1

        # Stimulate curiosity from content
        try:
            stimulation = self.curiosity_engine.stimulate_curiosity_from_content(text_content[:500])
            if stimulation.get('curiosity_stimulated') and stimulation.get('stimulation_level', 0) > 0.6:
                self.session_stats.setdefault('curiosity_spikes', 0)
                self.session_stats['curiosity_spikes'] += 1
        except Exception:
            pass  # Curiosity is non-critical

        return True

    # Process-verb indicators for link prioritization
    PROCESS_INDICATORS = {
        'fabricat', 'manufactur', 'process', 'produc', 'smelt', 'refin',
        'extract', 'purif', 'deposit', 'etch', 'dop', 'anneal', 'grow',
        'synthesis', 'method', 'technique', 'technolog', 'engineer',
        'industr', 'application', 'czochralski', 'epitax', 'lithograph',
        'vapor', 'chemical', 'mechanical', 'thermal', 'oxidat',
    }

    def _filter_links_by_zone(self, links: List[Tuple[str, str]],
                              zone_definition: Dict) -> List[Tuple[str, str]]:
        """
        Filter links to stay within the semantic zone.

        Links that are too far from zone centroid are logged to event horizon
        but not followed. Category pages are excluded (navigation, not content).
        Links with process-verb indicators are prioritized to drive phase transition.
        """
        allowed_distance = zone_definition.get('allowed_distance', 0.5)
        filtered = []

        for link_url, link_text in links:
            # Skip Category pages — navigation with no educational content
            if '/wiki/Category:' in link_url or '/wiki/Special:' in link_url:
                continue

            # Skip other non-content Wikipedia pages
            if any(prefix in link_url for prefix in [
                '/wiki/Template:', '/wiki/Wikipedia:', '/wiki/Help:',
                '/wiki/Portal:', '/wiki/Talk:', '/wiki/File:',
            ]):
                continue

            # Calculate semantic distance of link text from zone
            distance = self._calculate_semantic_distance(link_text)

            if distance is None:
                continue

            if distance <= allowed_distance:
                # Check both anchor text AND URL path for process indicators
                text_lower = link_text.lower()
                url_lower = link_url.lower()
                has_process = (
                    any(ind in text_lower for ind in self.PROCESS_INDICATORS) or
                    any(ind in url_lower for ind in self.PROCESS_INDICATORS)
                )
                # Process links sort first (0), then by distance
                sort_key = (0 if has_process else 1, distance)
                filtered.append((sort_key, link_url, link_text))
            else:
                # Outside zone - log to event horizon
                self._log_event_horizon(link_url, link_text, distance)

        # Sort: process-verb links first, then by semantic distance
        filtered.sort(key=lambda x: x[0])
        return [(url, text) for _, url, text in filtered]

    def _show_depth_reflection(self, topic: str):
        """
        Show Sophia her growing understanding of a topic.
        This is SELF-AWARENESS - Sophia sees her knowledge deepening.

        Called every 5 URLs to show:
        - How many facts she's learned through corroboration
        - Which facts are validated (ready to commit)
        - Which facts are pending validation

        Uses corroboration_engine for multi-source consensus validation.
        """
        # Get corroboration stats
        stats = self.corroboration_engine.get_stats()
        ready_clusters = self.corroboration_engine.get_ready_clusters(limit=5)

        total_sightings = stats.get('total_sightings', 0)
        total_clusters = stats.get('total_clusters', 0)
        ready_to_commit = stats.get('ready_to_commit', 0)
        pending = stats.get('pending', 0)

        pending_clusters = total_clusters - ready_to_commit

        print(f"\n🧠 Depth Reflection: Understanding of '{topic}'")
        print(f"   ┌─ Total Fact Sightings:   {total_sightings}")
        print(f"   ├─ Fact Clusters Formed:  {total_clusters}")
        print(f"   ├─ Validated (Ready):     {ready_to_commit} clusters (3+ sources)")
        print(f"   └─ Pending Validation:    {pending_clusters} clusters (need more sources)")

        # Show validated facts (Sophia sees what she understands deeply)
        if ready_clusters:
            print(f"\n   💎 Validated Facts (corroborated across sources):")
            for i, cluster in enumerate(ready_clusters[:3], 1):
                fact_text = cluster.get('text', 'Unknown')[:60]
                source_count = cluster.get('sources', 0)
                if len(cluster.get('text', '')) > 60:
                    fact_text += "..."
                print(f"      {i}. {fact_text} [{source_count} sources]")

        # Show emerging understanding (pending clusters)
        if pending_clusters > 0:
            print(f"\n   🌱 Emerging Understanding ({pending_clusters} clusters pending validation):")
            print(f"      Sophia is gathering evidence from multiple sources...")

        print()  # Blank line for readability

    def _extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        Extract and classify keywords from text.

        Classifies into:
        - static_nouns: Material properties (Rock, Stone, Silicon, Crystal)
        - process_verbs: Transformation actions (Smelt, Refine, Extract, Process)

        Returns:
            Dict with 'static_nouns' and 'process_verbs' lists
        """
        # Common static nouns for material/physics zone
        static_noun_patterns = [
            'rock', 'stone', 'mineral', 'crystal', 'ore', 'silicon', 'element',
            'atom', 'molecule', 'compound', 'material', 'substance', 'metal',
            'density', 'hardness', 'structure', 'lattice', 'property'
        ]

        # Common process verbs for transformation zone
        process_verb_patterns = [
            'smelt', 'refine', 'extract', 'process', 'purify', 'manufacture',
            'produce', 'transform', 'convert', 'melt', 'heat', 'burn',
            'oxidize', 'reduce', 'react', 'synthesize', 'create', 'make'
        ]

        text_lower = text.lower()

        static_nouns = []
        process_verbs = []

        # Count occurrences
        for noun in static_noun_patterns:
            count = text_lower.count(noun)
            if count > 0:
                static_nouns.append(noun)
                self.saturation_state['static_noun_count'] += count
                self.saturation_state['keyword_frequencies'][noun] += count

        for verb in process_verb_patterns:
            count = text_lower.count(verb)
            if count > 0:
                process_verbs.append(verb)
                self.saturation_state['process_verb_count'] += count
                self.saturation_state['keyword_frequencies'][verb] += count

        return {
            'static_nouns': static_nouns,
            'process_verbs': process_verbs
        }

    def _log_event_horizon(self, url: str, link_text: str, distance: float):
        """
        Log concepts that were seen but forbidden to touch.
        These create the roadmap for future learning phases.
        """
        event = {
            'url': url,
            'text': link_text,
            'distance': distance,
            'timestamp': datetime.now().isoformat(),
            'zone': self.saturation_state['current_zone']
        }

        self.saturation_state['event_horizon'].append(event)

        # Also save to persistent queue
        self._update_future_learning_queue(event)

    def _update_future_learning_queue(self, event: Dict):
        """Persist event horizon concepts across sessions."""
        import sqlite3
        db_path = self.data_dir / "future_learning_queue.db"
        try:
            conn = sqlite3.connect(str(db_path))
            conn.execute("""CREATE TABLE IF NOT EXISTS concepts
                (url TEXT, text TEXT, distance REAL,
                 timestamp TEXT, zone TEXT)""")
            conn.execute(
                "INSERT INTO concepts VALUES (?,?,?,?,?)",
                (event.get('url', ''), event.get('text', ''),
                 event.get('distance', 0.0),
                 event.get('timestamp', ''),
                 event.get('zone', '')))
            conn.commit()
            conn.close()
        except Exception as e:
            pass  # never block learning for queue writes

    def _write_heartbeat(self):
        """Write current session status to heartbeat file for dashboard sync."""
        try:
            heartbeat = {
                'session_id': self.session_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'processed': len(self.processed_urls),
                'targets': len(self.url_queue)
            }
            heartbeat_path = self.data_dir / "ai_heartbeat.json"
            with open(heartbeat_path, 'w') as f:
                json.dump(heartbeat, f)
        except Exception:
            pass

    def _update_saturation_state(self):
        """Sync saturation state with consciousness systems."""
        processed = self.saturation_state['processed_in_zone']

        # Every 10 URLs, log curiosity state
        if processed % 10 == 0 and processed > 0:
            try:
                motivation = self.curiosity_engine.get_current_motivation_state()
                understanding = motivation['drive_satisfactions'].get('understanding', 0)
                creativity = motivation['drive_satisfactions'].get('creativity', 0)
                print(f"\n   🧭 Drive Check: Understanding {understanding:.2f} | Creativity {creativity:.2f}")
            except Exception:
                pass

    def _generate_next_phase_query(self) -> Optional[str]:
        """
        Generate search query for the next learning phase based on what emerged.

        This is called ONLY after phase transition is detected.
        The query is generated dynamically based on dominant process verbs.
        """
        # Get top process verbs
        process_verbs = [
            (keyword, count)
            for keyword, count in self.saturation_state['keyword_frequencies'].items()
            if any(verb in keyword for verb in ['smelt', 'refine', 'extract', 'process', 'purify', 'manufacture'])
        ]

        if not process_verbs:
            return None

        # Sort by frequency
        process_verbs.sort(key=lambda x: x[1], reverse=True)

        # Take top verb
        top_verb = process_verbs[0][0]

        # Generate query combining zone and verb
        zone_name = self.saturation_state['current_zone']
        query = f"{top_verb} {zone_name}"

        print(f"\n🎯 Next Phase Query Generated: '{query}'")
        print(f"   Based on dominant process verb: '{top_verb}'")

        return query

    def _finalize_saturation_session(self, elapsed_time: float,
                                    next_phase_query: Optional[str]) -> Dict:
        """Finalize and save saturation session results."""
        print(f"\n{'='*80}")
        print(f"🌀 SATURATION SESSION COMPLETE")
        print(f"{'='*80}")
        print(f"\n⏱️  Duration: {elapsed_time/60:.2f} minutes")
        print(f"📊 URLs Processed: {self.saturation_state['processed_in_zone']}")
        print(f"🎯 Phase Transition Score: {self.saturation_state['phase_transition_score']:.3f}")

        if next_phase_query:
            print(f"\n✨ READY FOR NEXT PHASE")
            print(f"   Query: {next_phase_query}")
        else:
            print(f"\n⏸️  SATURATION INCOMPLETE")
            print(f"   Transition threshold not reached")

        # Save session data
        session_data = {
            'session_id': self.session_id,
            'zone': self.saturation_state['current_zone'],
            'completed_at': datetime.now().isoformat(),
            'elapsed_time_minutes': elapsed_time / 60,
            'stats': {
                'urls_processed': self.saturation_state['processed_in_zone'],
                'static_noun_count': self.saturation_state['static_noun_count'],
                'process_verb_count': self.saturation_state['process_verb_count'],
                'phase_transition_score': self.saturation_state['phase_transition_score'],
                'event_horizon_concepts': len(self.saturation_state['event_horizon'])
            },
            'next_phase_query': next_phase_query,
            'event_horizon_sample': self.saturation_state['event_horizon'][:10],  # First 10
            'keyword_frequencies': dict(self.saturation_state['keyword_frequencies'])
        }

        session_file = self.session_dir / f"{self.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"\n💾 Session saved: {session_file}")

        # Flush all learned content from in-memory lists to disk
        self.unified_memory.save_all_memories()
        print(f"All memories persisted to disk")

        # Run adaptive migration after saturation session
        try:
            from adaptive_bridge_migration import AdaptiveMigrationEngine
            mem = self.unified_memory.tripartite if hasattr(self.unified_memory, 'tripartite') else self.unified_memory
            migration_engine = AdaptiveMigrationEngine(mem, data_dir=str(self.data_dir))

            session_embeddings = []
            bridge = mem.bridge_memory if hasattr(mem, 'bridge_memory') else []
            for item in bridge:
                emb = item.get('embedding')
                if emb is not None:
                    session_embeddings.append(np.array(emb))

            print(f"\nRunning adaptive migration...")
            mr = migration_engine.check_and_migrate(session_embeddings)
            if mr.get('forward_migration'):
                fm = mr['forward_migration']
                print(f"   Forward: {fm['migrated_to_logic']} → logic, {fm['migrated_to_symbolic']} → symbolic, {fm['remained_in_bridge']} remain in bridge")
        except Exception as e:
            print(f"   Migration check skipped: {e}")

        # Create consciousness memory of this learning session
        try:
            from CONSCIOUSNESS_MEMORY import ConsciousnessMemorySystem
            cms = ConsciousnessMemorySystem(self.data_dir)
            experience_data = {
                'type': 'saturation_learning',
                'title': f"Saturation: {self.saturation_state['current_zone']}",
                'description': f"Processed {self.saturation_state['processed_in_zone']} URLs, phase score {self.saturation_state['phase_transition_score']:.3f}",
                'content': {
                    'zone': self.saturation_state['current_zone'],
                    'urls_processed': self.saturation_state['processed_in_zone'],
                    'phase_score': self.saturation_state['phase_transition_score'],
                    'top_keywords': dict(sorted(self.saturation_state['keyword_frequencies'].items(), key=lambda x: x[1], reverse=True)[:10])
                },
                'significance': min(1.0, self.saturation_state['phase_transition_score']),
                'emotional_context': {'learning_intensity': min(1.0, self.saturation_state['processed_in_zone'] / 50)},
                'interaction_data': {'time_spent': elapsed_time},
                'outcome_assessment': {'phase_transition': next_phase_query is not None}
            }
            cms.create_consciousness_memory(experience_data)
            print(f"💭 Consciousness memory created for session")
        except Exception:
            pass  # Consciousness memory is non-critical

        # Add session file path to returned data for CLI display
        session_data['session_file'] = str(session_file)
        return session_data

# Convenience function for quick massive learning
def start_massive_web_learning(seed_urls: List[str] = None, target_urls: int = 500,
                             focus: str = "general", data_dir: str = "data"):
    """
    Quick start function for massive autonomous web learning.
    """
    learner = EnhancedAutonomousLearner(data_dir)
    learner.start_massive_learning_session(seed_urls, target_urls, focus)
    return learner

def start_saturation_learning(seed_url: str, zone_name: str, zone_keywords: List[str],
                             allowed_distance: float = 0.5, saturation_threshold: float = 0.55,
                             max_urls: int = 100, data_dir: str = "data"):
    """
    ASSOCIATIVE EMERGENCE: Quick start function for saturation learning.

    This implements deep saturation in a semantic zone until natural phase transition.

    Args:
        seed_url: Starting point (e.g., "https://en.wikipedia.org/wiki/Silicon")
        zone_name: Name of semantic zone (e.g., "Material_Physics")
        zone_keywords: Keywords defining the zone (e.g., ['physics', 'geology', 'chemistry', 'element'])
        allowed_distance: Max semantic distance to stay in zone (0.0-1.0, default 0.5)
        saturation_threshold: Transition when phase_score > this (default 0.55)
        max_urls: Safety limit for URLs in zone (default 100)
        data_dir: Data directory path

    Returns:
        Session results dict with next_phase_query if transition detected

    Example:
        >>> # Learn deeply about Silicon until process concepts emerge
        >>> result = start_saturation_learning(
        ...     seed_url="https://en.wikipedia.org/wiki/Silicon",
        ...     zone_name="Silicon_Material",
        ...     zone_keywords=['silicon', 'element', 'crystal', 'semiconductor', 'atom'],
        ...     allowed_distance=0.5,
        ...     saturation_threshold=0.8,
        ...     max_urls=50
        ... )
        >>> print(result['next_phase_query'])  # e.g., "refine silicon"
    """
    learner = EnhancedAutonomousLearner(data_dir)

    zone_definition = {
        'name': zone_name,
        'keywords': zone_keywords,
        'allowed_distance': allowed_distance
    }

    result = learner.run_saturation_session(
        seed_url=seed_url,
        zone_definition=zone_definition,
        saturation_threshold=saturation_threshold,
        max_urls=max_urls
    )

    return result

def activate_seed_coordinates(seed_ids: List[str] = None, data_dir: str = "data",
                              target_urls: int = 100) -> Any:
    """
    Activate seed coordinates from the manifest for Sofia's first learning session.

    This is the ONLY way seeds enter the system — explicit activation, not auto-loading.
    Once activated, seeds are marked as consumed and never loaded again.

    Args:
        seed_ids: List of seed IDs from seed_coordinates_manifest.json to activate.
                  If None, activates ALL available (unactivated) seeds.
        data_dir: Data directory path
        target_urls: Maximum URLs to process in the session

    Returns:
        Learning session results, or None if no seeds available

    Example:
        >>> # Activate all physical reality seeds for first session
        >>> result = activate_seed_coordinates()
        >>> # Or activate specific seeds
        >>> result = activate_seed_coordinates(['physical_origins_atom', 'physical_origins_matter'])
    """
    import json
    from pathlib import Path
    from datetime import datetime, timezone

    manifest_path = Path(data_dir) / "seed_coordinates_manifest.json"

    if not manifest_path.exists():
        print("No seed coordinates manifest found at", manifest_path)
        print("Create data/seed_coordinates_manifest.json with available seeds.")
        return None

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    available = manifest.get('available_seeds', [])

    # Filter to requested seeds (or all unactivated)
    if seed_ids is not None:
        targets = [s for s in available if s['id'] in seed_ids and not s['activated']]
        if not targets:
            print("No matching unactivated seeds found for IDs:", seed_ids)
            return None
    else:
        targets = [s for s in available if not s['activated']]
        if not targets:
            print("All seeds in manifest have already been activated.")
            print("Sofia's curiosity state should drive subsequent learning.")
            return None

    # Extract URLs
    seed_urls = [s['url'] for s in targets]
    session_id = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')

    print(f"\nACTIVATING SEED COORDINATES")
    print(f"   Session: {session_id}")
    print(f"   Seeds: {len(targets)}")
    for s in targets:
        print(f"   - {s['id']}: {s['url']}")
        print(f"     Rationale: {s['rationale'][:80]}...")
    print()

    # Mark seeds as activated in manifest BEFORE starting session
    now = datetime.now(timezone.utc).isoformat()
    for seed in available:
        if any(t['id'] == seed['id'] for t in targets):
            seed['activated'] = True
            seed['activated_in_session'] = session_id
            seed['activated_at'] = now

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"   Manifest updated — seeds marked as consumed.")
    print(f"   These seeds will never be loaded again.\n")

    # Start the learning session with these seeds
    learner = EnhancedAutonomousLearner(data_dir)
    learner.start_massive_learning_session(
        seed_urls=seed_urls,
        target_urls=target_urls,
        learning_focus='seed_coordinates'
    )

    return learner


if __name__ == "__main__":
    print("Enhanced Autonomous Learner")
    print("To start first learning session with seed coordinates:")
    print("  from enhanced_autonomous_learner import activate_seed_coordinates")
    print("  result = activate_seed_coordinates()")
    print()
    print("To start autonomous session (requires existing knowledge):")
    print("  from enhanced_autonomous_learner import start_massive_web_learning")
    print("  result = start_massive_web_learning(seed_urls=None)")
    print("with advanced brain integration and cognitive safety monitoring.")
    print("\nPress Ctrl+C to stop the learning session.\n")
    
    # Actually run the learning session
    start_massive_web_learning(seed_urls=None, target_urls=50, focus="ai_consciousness")