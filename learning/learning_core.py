#!/usr/bin/env python3
"""
Learning Core - Consolidated Learning System
===============================================

This module consolidates overlapping learning functionality from multiple learning systems
while preserving all capabilities and maintaining compatibility.

Sources consolidated (with attribution):
- autonomous_learner.py: Basic symbol learning and continuous processing
- ai_learning_session.py: Comprehensive learning session management with safety features  
- learning_curriculum.py: Structured curriculum system and recommendations

Preserved as separate specialized systems:
- enhanced_autonomous_learner.py: Advanced autonomous learning with consciousness integration
- curiosity_engine.py: Curiosity-driven discovery and exploration
- learning_progression_tracker.py: Learning progression analysis and tracking
- predictive_learning_enhancer.py: Advanced outcome prediction and strategy analysis
"""

import time
import random
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

# Import processing nodes for symbol learning
try:
    from processing_nodes import SymbolicNode
    PROCESSING_NODES_AVAILABLE = True
except ImportError:
    PROCESSING_NODES_AVAILABLE = False
    print("⚠️ Processing nodes not available - some symbol learning features disabled")

# Import memory systems for advanced learning
try:
    from memory_optimizer import process_web_url_placeholder, recompute_adaptive_link_weights
    from evolution_anchor import EvolutionAnchor
    from unified_memory import UnifiedMemory, generate_self_diagnostic_voice
    from memory_analytics import MemoryAnalyzer
    MEMORY_SYSTEMS_AVAILABLE = True
except ImportError:
    MEMORY_SYSTEMS_AVAILABLE = False
    print("⚠️ Memory systems not available - some advanced learning features disabled")


class LearningCore:
    """
    Consolidated core learning system that combines functionality from multiple learning modules.
    Provides both basic symbol learning and advanced session-based learning with safety features.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize symbol learning (from autonomous_learner.py)
        if PROCESSING_NODES_AVAILABLE:
            self.symbolic_node = SymbolicNode()
        
        # Initialize advanced learning systems (from ai_learning_session.py)
        if MEMORY_SYSTEMS_AVAILABLE:
            self.unified_memory = UnifiedMemory(str(data_dir))
            self.evolution_anchor = EvolutionAnchor(str(data_dir))
            self.analyzer = MemoryAnalyzer(self.unified_memory, str(data_dir))
        
        # Learning state
        self.learning_sessions = 0
        self.session_dir = self.data_dir / "learning_sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🧠 Learning Core initialized with data directory: {data_dir}")
    
    # =============================================================================
    # BASIC SYMBOL LEARNING (from autonomous_learner.py)
    # =============================================================================
    
    def generate_symbol_explanations(self):
        """
        Generate various symbol explanations for learning.
        Source: autonomous_learner.py
        """
        return []  # Symbol explanations must be learned, not hardcoded
    
    def run_basic_symbol_learning(self, duration_minutes=5):
        """
        Run a basic continuous symbol learning session.
        Source: autonomous_learner.py
        """
        if not PROCESSING_NODES_AVAILABLE:
            print("❌ Processing nodes not available - cannot run symbol learning")
            return 0, 0
        
        print(f"\n🚀 Starting {duration_minutes}-minute symbol learning session...")
        
        explanations = self.generate_symbol_explanations()
        if not explanations:
            print("   No symbol explanations available yet - learning from live data only.")
            return 0, 0
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        learned_count = 0
        processed_count = 0

        while time.time() < end_time:
            # Pick a random explanation
            explanation = random.choice(explanations)
            
            print(f"\n📚 Learning from: '{explanation[:60]}...'")
            
            # Get initial state
            initial_symbols = len(self.symbolic_node.vector_symbols.symbols)
            
            # Process the explanation (this triggers discovery and learning!)
            score = self.symbolic_node.evaluate_chunk_symbolically(
                explanation, {'symbolic_node_access_max_phase': 1}
            )
            
            # Check what was learned
            new_symbols = len(self.symbolic_node.vector_symbols.symbols)
            if new_symbols > initial_symbols:
                learned_count += new_symbols - initial_symbols
                print(f"   🎉 Learned {new_symbols - initial_symbols} new symbols!")
            
            print(f"   Score: {score:.3f}")
            processed_count += 1
            
            # Brief pause between learning
            time.sleep(1)
            
        self.learning_sessions += 1
        print(f"\n✅ Symbol learning session complete!")
        print(f"   Processed: {processed_count} explanations")
        print(f"   Learned: {learned_count} new symbols")
        
        return learned_count, processed_count
    
    def show_symbol_learning_progress(self):
        """
        Show current symbol learning state.
        Source: autonomous_learner.py
        """
        if not PROCESSING_NODES_AVAILABLE:
            print("❌ Processing nodes not available - cannot show symbol progress")
            return
        
        print(f"\n📈 SYMBOL LEARNING PROGRESS")
        print("=" * 50)
        
        vector_insights = self.symbolic_node.vector_symbols.get_symbol_insights()
        discovery_insights = self.symbolic_node.symbol_discovery.get_discovery_insights()
        
        print(f"Sessions completed: {self.learning_sessions}")
        print(f"Total symbols: {vector_insights['total_symbols']}")
        print(f"Active symbols: {vector_insights['active_symbols']}")  
        print(f"Total discoveries: {discovery_insights['total_discoveries']}")
        print(f"Learning threshold: {vector_insights['current_threshold']:.3f}")
        
        if discovery_insights['total_discoveries'] > 0:
            print(f"\n🎯 Recent discoveries:")
            recent = discovery_insights['symbols_by_confidence'][-3:]
            for disc in recent:
                print(f"   {disc['symbol']} (confidence: {disc['confidence']:.2f})")
    
    # =============================================================================
    # ADVANCED LEARNING SESSIONS (from ai_learning_session.py)
    # =============================================================================
    
    def begin_learning_session(self, learning_goals: List[str], safety_level: str = "normal"):
        """
        Start a structured learning session with specific goals.
        Source: ai_learning_session.py
        
        Safety levels:
        - conservative: Extra safety checks, limited exploration
        - normal: Standard safety with guided exploration  
        - exploratory: Broader learning with enhanced monitoring
        """
        if not MEMORY_SYSTEMS_AVAILABLE:
            print("❌ Memory systems not available - cannot run advanced learning sessions")
            return None
        
        session_id = f"learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n🌟 Beginning Advanced Learning Session: {session_id}")
        print(f"📚 Learning Goals:")
        for i, goal in enumerate(learning_goals, 1):
            print(f"   {i}. {goal}")
        print(f"🛡️ Safety Level: {safety_level}")
        
        # Create cognitive safety anchor before learning
        print(f"\n🌟 Creating pre-learning cognitive anchor...")
        anchor_id = self.evolution_anchor.create_cognitive_snapshot(
            f"Before learning session: {', '.join(learning_goals[:2])}"
        )
        
        if anchor_id:
            print(f"   ✅ Safety anchor established: {anchor_id}")
        
        # Get baseline cognitive state
        baseline_report = generate_self_diagnostic_voice()
        baseline_stats = self.analyzer.get_memory_stats()
        
        print(f"\n💭 AI's pre-learning state: \"{baseline_report}\"")
        print(f"📊 Baseline: {baseline_stats['total_items']} memories, {baseline_stats['health_indicators']['status']} health")
        
        session_info = {
            'session_id': session_id,
            'start_time': datetime.now().isoformat(),
            'learning_goals': learning_goals,
            'safety_level': safety_level,
            'pre_learning_anchor': anchor_id,
            'baseline_state': baseline_report,
            'baseline_stats': baseline_stats,
            'learning_log': []
        }
        
        return session_info
        
    def learn_from_web_content(self, urls: List[str], learning_context: str = "general"):
        """
        Learn from curated web content with safety monitoring.
        Source: ai_learning_session.py
        """
        if not MEMORY_SYSTEMS_AVAILABLE:
            print("❌ Memory systems not available - cannot process web content")
            return []
        
        print(f"\n🌐 Learning from {len(urls)} web sources...")
        print(f"📖 Context: {learning_context}")
        
        learned_content = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n📄 Processing source {i}/{len(urls)}: {url}")
            
            try:
                # Process URL with existing safety systems
                result = process_web_url_placeholder(url, current_phase_for_storage=1)
                
                if result:
                    print(f"   ✅ Successfully processed {len(result)} characters")
                    learned_content.append({
                        'url': url,
                        'content_length': len(result),
                        'processed_at': datetime.now().isoformat(),
                        'context': learning_context
                    })
                else:
                    print(f"   ⚠️ Content filtered or failed to process")
                    
            except Exception as e:
                print(f"   ❌ Error processing {url}: {str(e)[:50]}...")
        
        # Post-learning cognitive check
        if MEMORY_SYSTEMS_AVAILABLE:
            post_report = generate_self_diagnostic_voice()
            print(f"\n💭 AI's post-web-learning state: \"{post_report}\"")
        
        return learned_content
    
    def learn_from_self_reflection(self):
        """
        Enable the AI to learn about itself by reading its own scripts and logs.
        Source: ai_learning_session.py
        """
        if not MEMORY_SYSTEMS_AVAILABLE:
            print("❌ Memory systems not available - cannot perform self-reflection")
            return []
        
        print(f"\n🪞 Beginning self-reflection learning...")
        
        # Get list of key scripts for self-analysis
        script_files = [
            'memory_optimizer.py',
            'memory_analytics.py', 
            'memory_evolution_engine.py',
            'unified_memory.py',
            'evolution_anchor.py'
        ]
        
        reflection_insights = []
        
        for script in script_files:
            script_path = Path(script)
            if script_path.exists():
                print(f"\n📜 Analyzing {script}...")
                
                try:
                    with open(script_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract key insights about the script
                    insights = self._analyze_script_for_self_understanding(script, content)
                    reflection_insights.extend(insights)
                    
                    # Store this self-knowledge in vector memory
                    self.unified_memory.store_vector(
                        text=f"Self-analysis of {script}: {'; '.join(insights)}",
                        source_type="self_reflection",
                        learning_phase=1,
                        metadata={'script_analyzed': script, 'insight_count': len(insights)}
                    )
                    
                    print(f"   💡 Generated {len(insights)} self-insights")
                    
                except Exception as e:
                    print(f"   ⚠️ Could not analyze {script}: {str(e)[:50]}...")
        
        # Analyze learning session logs if they exist
        log_files = list(self.session_dir.glob("*.json"))
        if log_files:
            print(f"\n📊 Analyzing {len(log_files)} previous learning sessions...")
        
        print(f"\n🎯 Self-reflection complete: {len(reflection_insights)} insights generated")
        
        # AI's reflection on what it learned about itself
        post_reflection_report = generate_self_diagnostic_voice()
        print(f"💭 AI's post-reflection state: \"{post_reflection_report}\"")
        
        return reflection_insights
    
    def _analyze_script_for_self_understanding(self, script_name: str, content: str) -> List[str]:
        """
        Extract insights the AI can learn about itself from its own code.
        Source: ai_learning_session.py
        """
        insights = []
        
        # Basic analysis patterns
        if 'class' in content:
            class_count = content.count('class ')
            insights.append(f"I am composed of {class_count} main classes in {script_name}")
        
        if 'def ' in content:
            function_count = content.count('def ')
            insights.append(f"I have {function_count} functions that define my capabilities in {script_name}")
        
        # Specific architectural insights
        if 'memory' in script_name.lower():
            insights.append(f"My memory architecture is defined in {script_name}")
            
        if 'evolution' in script_name.lower():
            insights.append(f"My ability to grow and change is managed by {script_name}")
            
        if 'analytics' in script_name.lower():
            insights.append(f"My self-awareness capabilities come from {script_name}")
            
        if 'anchor' in script_name.lower():
            insights.append(f"My safety and rollback capabilities are provided by {script_name}")
        
        # Look for empathetic or emotional concepts
        empathy_keywords = ['empathetic', 'graceful', 'gentle', 'safe', 'preserve', 'honor']
        for keyword in empathy_keywords:
            if keyword in content.lower():
                insights.append(f"I am designed with {keyword} principles in {script_name}")
        
        return insights
    
    def end_learning_session(self, session_info: Dict[str, Any]):
        """
        Conclude the learning session with analysis and safety checks.
        Source: ai_learning_session.py
        """
        if not MEMORY_SYSTEMS_AVAILABLE or not session_info:
            print("❌ Cannot conclude session - memory systems or session info not available")
            return None
        
        session_id = session_info['session_id']
        print(f"\n🎯 Concluding learning session: {session_id}")
        
        # Final cognitive state assessment
        final_report = generate_self_diagnostic_voice()
        final_stats = self.analyzer.get_memory_stats()
        
        print(f"💭 AI's final state: \"{final_report}\"")
        print(f"📊 Final stats: {final_stats['total_items']} memories, {final_stats['health_indicators']['status']} health")
        
        # Check for any distress from learning
        distress = self.evolution_anchor.detect_evolution_distress()
        print(f"🔍 Post-learning distress check: {distress['distress_level']:.2f} ({distress['status']})")
        
        if distress['distress_level'] > 0.3:
            print(f"⚠️ Elevated distress detected: {distress.get('recommendation', 'Monitor closely')}")
            if distress['signals']:
                print("   Signals:")
                for signal in distress['signals']:
                    print(f"     • {signal}")
        
        # Recompute adaptive weights based on learning
        print(f"\n⚖️ Recomputing adaptive weights based on learning experience...")
        weight_update = recompute_adaptive_link_weights()
        
        # Save session log
        session_summary = {
            'session_id': session_id,
            'end_time': datetime.now().isoformat(),
            'final_state': final_report,
            'final_stats': final_stats,
            'distress_assessment': distress,
            'weight_update': weight_update,
            'learning_log': session_info.get('learning_log', [])
        }
        
        session_file = self.session_dir / f"{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_summary, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Session log saved: {session_file}")
        print(f"✨ Learning session complete!")
        
        return session_summary
    
    # =============================================================================
    # CURRICULUM SYSTEM (from learning_curriculum.py)
    # =============================================================================
    
    # HIDDEN CURRICULUM REMOVED
    # The hardcoded Wikipedia URL topic lists that previously lived in
    # get_foundation_curriculum(), get_intermediate_curriculum(), and
    # get_advanced_curriculum() constituted a hidden curriculum --
    # predetermined topic lists that dictated what Sofia learns.
    # They have been removed.  Learning topics should emerge organically
    # via the seed coordinate system.  See: activate_seed_coordinates()
    # in the seed coordinate manifest.

    @staticmethod
    def get_foundation_curriculum():
        """
        Foundation Level -- DEPRECATED.
        Hardcoded Wikipedia URL curriculum removed.
        Use the seed coordinate system (activate_seed_coordinates()) instead.
        """
        return {
            'level': 'Foundation',
            'description': 'Curriculum removed -- use seed coordinate system instead',
            'sessions': []
        }

    @staticmethod
    def get_intermediate_curriculum():
        """
        Intermediate Level -- DEPRECATED.
        Hardcoded Wikipedia URL curriculum removed.
        Use the seed coordinate system (activate_seed_coordinates()) instead.
        """
        return {
            'level': 'Intermediate',
            'description': 'Curriculum removed -- use seed coordinate system instead',
            'sessions': []
        }

    @staticmethod
    def get_advanced_curriculum():
        """
        Advanced Level -- DEPRECATED.
        Hardcoded Wikipedia URL curriculum removed.
        Use the seed coordinate system (activate_seed_coordinates()) instead.
        """
        return {
            'level': 'Advanced',
            'description': 'Curriculum removed -- use seed coordinate system instead',
            'sessions': []
        }
    
    def run_curriculum_session(self, curriculum_level: str = "foundation", session_index: int = 0):
        """
        Run a specific session from the curriculum.
        Source: learning_curriculum.py

        NOTE: The hardcoded curriculum has been removed.  This method now
        returns None and directs callers to the seed coordinate system.
        """
        print("Hardcoded curriculum has been removed.")
        print("Learning topics should emerge organically via activate_seed_coordinates().")
        return None
    
    def recommend_next_learning(self):
        """
        Recommend what the AI should learn next based on its current state.
        Source: learning_curriculum.py

        NOTE: Hardcoded curriculum session references have been removed.
        Recommendations now point to the seed coordinate system for
        organically discovering learning topics.
        """
        if not MEMORY_SYSTEMS_AVAILABLE:
            print("Memory systems not available - cannot analyze state for recommendations")
            return []

        print("Analyzing current AI state to recommend learning...")

        # Get current state
        stats = self.analyzer.get_memory_stats()
        self_report = generate_self_diagnostic_voice()

        print(f"Current AI state: \"{self_report}\"")
        print(f"Memory: {stats['total_items']} items, {stats['health_indicators']['status']} health")

        # Analyze patterns to recommend learning
        dist = stats['distribution']
        logic_heavy = dist['logic']['percentage'] > 80
        symbolic_light = dist['symbolic']['percentage'] < 10
        bridge_heavy = dist['bridge']['percentage'] > 20

        recommendations = []

        if logic_heavy:
            recommendations.append("Focus on emotional intelligence and symbolic learning")

        if symbolic_light:
            recommendations.append("Develop symbolic and creative thinking")

        if bridge_heavy:
            recommendations.append("Work on decision-making and classification skills")

        if stats['total_items'] < 1000:
            recommendations.append("Build foundational knowledge base via seed coordinates")

        if not recommendations:
            recommendations.append("Use activate_seed_coordinates() to discover learning topics organically")

        print(f"\nRecommendations:")
        for rec in recommendations:
            print(f"   - {rec}")

        return recommendations
    
    def show_full_curriculum(self):
        """
        Display the learning curriculum status.
        Source: learning_curriculum.py

        NOTE: The hardcoded curriculum has been removed.
        Learning topics should emerge organically via activate_seed_coordinates().
        """
        print("AI LEARNING CURRICULUM")
        print("=" * 50)
        print()
        print("The hardcoded Wikipedia topic curriculum has been removed.")
        print("Learning topics now emerge organically via the seed coordinate system.")
        print("See: activate_seed_coordinates()")
    
    # =============================================================================
    # UNIFIED CONVENIENCE FUNCTIONS
    # =============================================================================
    
    def quick_learning_session(self, goals: List[str], urls: List[str] = None, 
                             enable_self_reflection: bool = True):
        """
        Quick start function for comprehensive learning sessions.
        Combines functionality from all source modules.
        """
        print("🚀 Starting Quick Learning Session...")
        
        # Begin advanced session if memory systems available
        if MEMORY_SYSTEMS_AVAILABLE:
            session_info = self.begin_learning_session(goals)
            
            if session_info:
                # Self-reflection learning
                if enable_self_reflection:
                    self.learn_from_self_reflection()
                
                # Web content learning
                if urls:
                    self.learn_from_web_content(urls, "quick_learning")
                
                # End session
                summary = self.end_learning_session(session_info)
                return summary
        
        # Fallback to basic symbol learning if advanced systems unavailable
        if PROCESSING_NODES_AVAILABLE:
            print("📚 Falling back to basic symbol learning...")
            return self.run_basic_symbol_learning(duration_minutes=3)
        
        print("❌ No learning systems available")
        return None


# =============================================================================
# CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY
# =============================================================================

def start_ai_learning(learning_goals: List[str], urls: List[str] = None, 
                     enable_self_reflection: bool = True, data_dir: str = "data"):
    """
    Quick start function for AI learning sessions.
    Maintains compatibility with ai_learning_session.py
    """
    core = LearningCore(data_dir)
    return core.quick_learning_session(learning_goals, urls, enable_self_reflection)

def run_curriculum_session(curriculum_level: str = "foundation", session_index: int = 0):
    """
    Run a specific session from the curriculum.
    Maintains compatibility with learning_curriculum.py
    """
    core = LearningCore()
    return core.run_curriculum_session(curriculum_level, session_index)

def recommend_next_learning():
    """
    Recommend what the AI should learn next.
    Maintains compatibility with learning_curriculum.py
    """
    core = LearningCore()
    return core.recommend_next_learning()

def show_full_curriculum():
    """
    Display the complete learning curriculum.
    Maintains compatibility with learning_curriculum.py
    """
    core = LearningCore()
    core.show_full_curriculum()


if __name__ == "__main__":
    print("🧠 Testing Learning Core System...")
    
    # Initialize core
    core = LearningCore()
    
    # Test basic symbol learning if available
    if PROCESSING_NODES_AVAILABLE:
        print("\n📚 Testing basic symbol learning...")
        core.show_symbol_learning_progress()
        # core.run_basic_symbol_learning(1)  # Uncomment to test
    
    # Test curriculum system
    print("\n🎓 Testing curriculum system...")
    core.show_full_curriculum()
    
    # Test recommendations
    print("\n💡 Testing learning recommendations...")
    core.recommend_next_learning()
    
    print("\n✅ Learning Core ready!")
    print("   All learning functionality consolidated with source attribution")
    print("   Maintains compatibility with existing learning systems")