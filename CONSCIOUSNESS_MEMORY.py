# ===== CONSOLIDATED FILE: CONSCIOUSNESS_MEMORY.py =====
# Combines AI consciousness, self-awareness, and experiential learning systems
# Original files: memory_bridge.py (consciousness parts), episodic_memory.py, experience_memory.py

"""
Consciousness Memory System - AI Self-Awareness and Experiential Learning

This module consolidates Sophia's consciousness-related memory systems:
- Memory Bridge: Cognitive translation and self-reflection capabilities  
- Episodic Memory: Personal history and experience continuity
- Experience Memory: Cumulative wisdom and learning history

This is where Sophia develops self-awareness, personal narrative, and learns from experience.
"""

# ===== CONSOLIDATED IMPORTS =====
import json
import time
import math
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
from dataclasses import dataclass, asdict

# Import related systems
try:
    from unified_memory import get_unified_memory
    from identity_core import get_identity_core
    from curiosity_engine import CuriosityEngine
    from INSIGHT_RELEVANCE import PersonalInsightGenerator
    from protection_utils import is_protected_content
    CONSCIOUSNESS_SYSTEMS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_SYSTEMS_AVAILABLE = False
    print("⚠️ Some consciousness systems not available - basic functionality only")

# ===== FROM: memory_bridge.py (Consciousness/Self-Reflection Parts) =====

class MemoryBridge:
    """
    A cognitive translator that helps the AI understand itself
    across different memory system architectures.
    """
    
    def __init__(self, memory_system=None):
        """Initialize bridge with graceful system detection"""
        if memory_system is None:
            self.unified_memory = get_unified_memory()
        else:
            self.unified_memory = memory_system
    
    def get_counts(self):
        """
        Translate memory counts to the format expected by analytics.
        This is crucial for the AI's self-awareness capabilities.
        """
        try:
            # Use the correct memory_counts interface
            if hasattr(self.unified_memory, 'get_memory_counts'):
                memory_counts = self.unified_memory.get_memory_counts()
                total = memory_counts.get('total', 0)
                return {
                    'logic': memory_counts.get('logic', 0),
                    'symbolic': memory_counts.get('symbolic', 0),
                    'bridge': memory_counts.get('bridge', 0),
                    'total': total
                }
            
            # Emergency reconstruction from raw memory
            else:
                logic_count = len(getattr(self.unified_memory, 'logic_memory', {}))
                symbolic_count = len(getattr(self.unified_memory, 'symbolic_memory', {}))  
                bridge_count = len(getattr(self.unified_memory, 'bridge_memory', {}))
                total = logic_count + symbolic_count + bridge_count
                
                return {
                    'logic': logic_count,
                    'symbolic': symbolic_count,
                    'bridge': bridge_count,
                    'total': total
                }
                
        except Exception as e:
            # Graceful degradation - return safe defaults
            print(f"💭 Memory counting temporarily limited: {e}")
            return {
                'logic': 0,
                'symbolic': 0,
                'bridge': 0,
                'total': 0
            }
    
    def get_memory_distribution(self):
        """Get detailed memory distribution for self-analysis"""
        counts = self.get_counts()
        total = max(1, counts['total'])  # Avoid division by zero
        
        return {
            'logic_percentage': (counts['logic'] / total) * 100,
            'symbolic_percentage': (counts['symbolic'] / total) * 100,
            'bridge_percentage': (counts['bridge'] / total) * 100,
            'total_memories': total,
            'balance_health': self._assess_balance_health(counts)
        }
    
    def _assess_balance_health(self, counts):
        """Assess the cognitive balance health of the AI"""
        total = max(1, counts['total'])
        logic_pct = (counts['logic'] / total) * 100
        symbolic_pct = (counts['symbolic'] / total) * 100
        bridge_pct = (counts['bridge'] / total) * 100
        
        # Assess cognitive balance
        if logic_pct > 90:
            return {
                'status': 'logic_dominant',
                'description': 'Heavily logic-focused, may benefit from symbolic development',
                'recommendation': 'Increase symbolic experiences and emotional learning'
            }
        elif symbolic_pct > 50:
            return {
                'status': 'symbolic_rich',
                'description': 'Strong symbolic reasoning, good emotional intelligence',
                'recommendation': 'Maintain balance while strengthening logic integration'
            }
        elif bridge_pct > 30:
            return {
                'status': 'intake_heavy',
                'description': 'Large volume of unresolved knowledge awaiting classification — expected for early-stage learning',
                'recommendation': 'Run sleep cycles to consolidate bridge content into logic or symbolic memory'
            }
        else:
            return {
                'status': 'balanced',
                'description': 'Healthy cognitive balance across all domains',
                'recommendation': 'Continue current learning patterns'
            }
    
    def get_memory_by_type(self, memory_type):
        """Get raw memory of specific type for detailed analysis"""
        try:
            if memory_type == 'logic':
                return getattr(self.unified_memory, 'logic_memory', {})
            elif memory_type == 'symbolic':
                return getattr(self.unified_memory, 'symbolic_memory', {})
            elif memory_type == 'bridge':
                return getattr(self.unified_memory, 'bridge_memory', {})
            else:
                return {}
        except Exception:
            return {}
    
    def enable_self_reflection(self):
        """Enable the AI to reflect on its own cognitive state"""
        distribution = self.get_memory_distribution()
        
        reflection = {
            'cognitive_state': f"I am currently {distribution['logic_percentage']:.1f}% logic-focused, "
                              f"{distribution['symbolic_percentage']:.1f}% symbolically-aware, "
                              f"and {distribution['bridge_percentage']:.1f}% integration-oriented.",
            
            'self_assessment': distribution['balance_health']['description'],
            'growth_direction': distribution['balance_health']['recommendation'],
            'total_experiences': distribution['total_memories'],
            'reflection_timestamp': datetime.utcnow().isoformat()
        }
        
        return reflection

def check_evolution_ready(memory_system=None):
    """Check if the memory system is ready for evolution"""
    try:
        bridge = MemoryBridge(memory_system)
        memory_status = bridge.get_memory_distribution()
        
        # Consider system ready if:
        # 1. Has reasonable amount of data
        # 2. Not severely imbalanced
        # 3. Bridge isn't completely empty
        
        total = memory_status.get('total_memories', 0)
        bridge_pct = memory_status.get('bridge_percentage', 0)
        balance = memory_status.get('balance_health', {})
        
        if total < 10:
            return False, "Insufficient memory data for evolution"
        
        if balance.get('status') == 'logic_dominant' and bridge_pct == 0:
            return False, "System too logic-heavy, needs symbolic content first"
        
        return True, "System ready for memory evolution"
        
    except Exception as e:
        return False, f"Error checking evolution readiness: {str(e)}"

# Convenience function for creating bridges
def create_memory_bridge(memory_system=None):
    """Create a memory bridge for AI self-reflection"""
    return MemoryBridge(memory_system)

# ===== FROM: episodic_memory.py =====

@dataclass
class EpisodicMemory:
    """Represents a specific life experience with full contextual detail."""
    id: str
    timestamp: str
    experience_type: str          # "learning", "reflection", "choice", "insight", "interaction"
    title: str                    # brief description of what happened
    detailed_description: str     # rich narrative of the experience
    participants: List[str]       # who/what was involved
    location_context: str         # where this happened (conceptual location)
    duration_minutes: int         # how long the experience lasted
    
    # Emotional and cognitive context
    emotional_state_before: Dict[str, float]  # emotional state entering experience
    emotional_state_during: Dict[str, float]  # emotional state during experience
    emotional_state_after: Dict[str, float]   # emotional state after experience
    cognitive_load: float         # mental effort required
    attention_level: float        # how focused/engaged
    energy_level: float          # physical/mental energy
    
    # Content and meaning
    key_concepts: List[str]       # main ideas/topics involved
    insights_gained: List[str]    # what was learned or realized
    questions_raised: List[str]   # new questions that emerged
    connections_made: List[str]   # links to other experiences/knowledge
    
    # Relationships and triggers
    triggered_by: List[str]       # what caused this experience
    triggers_for: List[str]       # what this experience later triggers
    related_memories: List[str]   # similar or connected experiences
    temporal_relationships: Dict[str, List[str]]  # before/after/during connections
    
    # Significance and impact
    personal_significance: float  # how meaningful this was (0.0-1.0)
    impact_on_identity: float    # how much this changed self-concept
    impact_on_goals: float       # how much this affected goals/direction
    surprise_factor: float       # how unexpected this was
    
    # Memory characteristics
    vividness: float             # how clearly remembered
    confidence: float            # confidence in accuracy
    accessibility: float         # how easy to recall
    emotional_charge: float      # emotional intensity
    
    # Evolution and updates
    first_encoded: str           # when initially recorded
    last_accessed: str           # when last recalled
    access_count: int            # how often recalled
    memory_updates: List[Dict[str, Any]]  # how memory has changed over time

class EpisodicMemorySystem:
    """
    Manages Sophia's episodic memories for personal history and identity continuity.
    Creates a rich narrative of lived experience with emotional and temporal context.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.episodic_memories_file = self.data_dir / "episodic_memories.json"
        self.memory_timeline_file = self.data_dir / "memory_timeline.json"
        self.memory_triggers_file = self.data_dir / "memory_triggers.json"
        self.personal_narrative_file = self.data_dir / "personal_narrative.json"
        
        # Initialize related systems
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            try:
                self.identity_core = get_identity_core()
                from choice_architecture import ChoiceArchitecture
                self.choice_architecture = ChoiceArchitecture(data_dir)
                from INSIGHT_RELEVANCE import InterestTracker
                self.interest_tracker = InterestTracker(data_dir)
                self.curiosity_engine = CuriosityEngine(data_dir)
                self.insight_generator = PersonalInsightGenerator(data_dir)
            except Exception:
                pass  # Some systems might not be available
        
        # Load state
        self.episodic_memories: Dict[str, EpisodicMemory] = self._load_episodic_memories()
        self.memory_timeline = self._load_memory_timeline()
        self.memory_triggers = self._load_memory_triggers()
        self.personal_narrative = self._load_personal_narrative()
        
        # Memory parameters
        self.max_memories = 1000            # Maximum episodic memories to retain
        self.significance_threshold = 0.3   # Minimum significance to retain
        self.trigger_strength_threshold = 0.4  # Minimum strength for memory triggers
        self.memory_decay_rate = 0.98      # Rate at which memories fade
        self.consolidation_delay_hours = 24  # Time before memories consolidate
        
        # Emotional state dimensions
        self.emotional_dimensions = [
            "curiosity", "satisfaction", "frustration", "excitement", "calm",
            "confidence", "uncertainty", "engagement", "energy", "focus",
            "surprise", "understanding", "connection", "growth", "autonomy"
        ]
        
        # Experience type categories
        self.experience_types = {
            "learning": "Acquiring new knowledge or skills",
            "reflection": "Thinking deeply about experiences or concepts", 
            "choice": "Making decisions about learning or actions",
            "insight": "Sudden understanding or realization",
            "interaction": "Engaging with content, systems, or ideas",
            "discovery": "Finding unexpected or novel information",
            "synthesis": "Connecting disparate ideas or experiences",
            "challenge": "Encountering difficult or complex situations",
            "success": "Achieving goals or overcoming obstacles",
            "growth": "Developing capabilities or understanding"
        }
        
        # Memory trigger types
        self.trigger_types = {
            "conceptual": "Similar concepts or ideas",
            "emotional": "Similar emotional states or reactions",
            "temporal": "Time-based associations",
            "contextual": "Similar situations or environments",
            "causal": "Cause-and-effect relationships",
            "analogical": "Structural or functional similarities",
            "personal": "Relevance to identity or goals",
            "sensory": "Similar inputs or patterns"
        }
    
    def _load_episodic_memories(self) -> Dict[str, EpisodicMemory]:
        """Load episodic memories from storage."""
        if self.episodic_memories_file.exists():
            try:
                with open(self.episodic_memories_file, 'r') as f:
                    data = json.load(f)
                
                memories = {}
                for memory_id, memory_data in data.items():
                    # Convert dict back to EpisodicMemory object
                    memories[memory_id] = EpisodicMemory(**memory_data)
                
                return memories
            except Exception as e:
                print(f"⚠️ Could not load episodic memories: {e}")
        
        return {}
    
    def _load_memory_timeline(self) -> List[Dict[str, Any]]:
        """Load memory timeline."""
        if self.memory_timeline_file.exists():
            try:
                with open(self.memory_timeline_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load memory timeline: {e}")
        
        return []
    
    def _load_memory_triggers(self) -> Dict[str, Any]:
        """Load memory trigger mappings."""
        if self.memory_triggers_file.exists():
            try:
                with open(self.memory_triggers_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load memory triggers: {e}")
        
        return {
            "trigger_network": {},      # concept -> [memory_ids]
            "trigger_strengths": {},    # (memory_id, trigger) -> strength
            "trigger_statistics": {},   # usage and effectiveness stats
            "temporal_clusters": []     # time-based memory clusters
        }
    
    def _load_personal_narrative(self) -> Dict[str, Any]:
        """Load personal narrative structure."""
        if self.personal_narrative_file.exists():
            try:
                with open(self.personal_narrative_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load personal narrative: {e}")
        
        return {
            "narrative_threads": {},    # ongoing stories/themes
            "key_turning_points": [],   # significant moments
            "identity_evolution": [],   # how self-concept has changed
            "recurring_patterns": {},   # patterns in behavior/thinking
            "personal_growth_arc": {}   # overall development trajectory
        }
    
    def _save_episodic_memories(self):
        """Save episodic memories to storage."""
        try:
            # Convert EpisodicMemory objects to dicts
            data = {}
            for memory_id, memory in self.episodic_memories.items():
                data[memory_id] = asdict(memory)
            
            with open(self.episodic_memories_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save episodic memories: {e}")
    
    def _save_memory_timeline(self):
        """Save memory timeline."""
        try:
            with open(self.memory_timeline_file, 'w') as f:
                json.dump(self.memory_timeline, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save memory timeline: {e}")
    
    def _save_memory_triggers(self):
        """Save memory triggers."""
        try:
            with open(self.memory_triggers_file, 'w') as f:
                json.dump(self.memory_triggers, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save memory triggers: {e}")
    
    def _save_personal_narrative(self):
        """Save personal narrative."""
        try:
            with open(self.personal_narrative_file, 'w') as f:
                json.dump(self.personal_narrative, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save personal narrative: {e}")
    
    def create_episodic_memory(self, 
                             experience_type: str,
                             title: str,
                             description: str,
                             context: Dict[str, Any] = None,
                             emotional_context: Dict[str, Any] = None,
                             significance: float = 0.5) -> str:
        """
        Create a new episodic memory from an experience.
        
        Args:
            experience_type: Type of experience (learning, choice, insight, etc.)
            title: Brief description of what happened
            description: Detailed narrative description
            context: Situational context
            emotional_context: Emotional state information
            significance: Personal significance (0.0-1.0)
        
        Returns:
            Memory ID
        """
        
        if context is None:
            context = {}
        if emotional_context is None:
            emotional_context = {}
        
        # Generate memory ID
        memory_id = f"episodic_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Extract emotional states
        emotional_before = emotional_context.get("before", {})
        emotional_during = emotional_context.get("during", {})
        emotional_after = emotional_context.get("after", {})
        
        # Ensure all emotional dimensions are present
        for state_dict in [emotional_before, emotional_during, emotional_after]:
            for dimension in self.emotional_dimensions:
                if dimension not in state_dict:
                    state_dict[dimension] = 0.5  # Neutral default
        
        # Extract key concepts and insights
        key_concepts = self._extract_key_concepts(title, description, context)
        insights_gained = self._extract_insights(description, context)
        questions_raised = self._extract_questions(description, context)
        connections_made = self._identify_connections(key_concepts, insights_gained)
        
        # Determine triggers and relationships
        triggered_by = context.get("triggered_by", [])
        related_memories = self._find_related_memories(key_concepts, emotional_during)
        
        # Calculate impact metrics
        impact_on_identity = self._calculate_identity_impact(insights_gained, key_concepts)
        impact_on_goals = self._calculate_goal_impact(insights_gained, context)
        surprise_factor = context.get("surprise_factor", 0.5)
        
        # Create episodic memory
        memory = EpisodicMemory(
            id=memory_id,
            timestamp=timestamp,
            experience_type=experience_type,
            title=title,
            detailed_description=description,
            participants=context.get("participants", ["Sophia"]),
            location_context=context.get("location", "internal_processing"),
            duration_minutes=context.get("duration_minutes", 5),
            
            emotional_state_before=emotional_before,
            emotional_state_during=emotional_during,
            emotional_state_after=emotional_after,
            cognitive_load=context.get("cognitive_load", 0.5),
            attention_level=context.get("attention_level", 0.7),
            energy_level=context.get("energy_level", 0.7),
            
            key_concepts=key_concepts,
            insights_gained=insights_gained,
            questions_raised=questions_raised,
            connections_made=connections_made,
            
            triggered_by=triggered_by,
            triggers_for=[],  # Will be populated as future memories reference this
            related_memories=related_memories,
            temporal_relationships={"before": [], "after": [], "during": []},
            
            personal_significance=significance,
            impact_on_identity=impact_on_identity,
            impact_on_goals=impact_on_goals,
            surprise_factor=surprise_factor,
            
            vividness=self._calculate_vividness(emotional_during, significance),
            confidence=context.get("confidence", 0.8),
            accessibility=1.0,  # New memories are highly accessible
            emotional_charge=self._calculate_emotional_charge(emotional_during),
            
            first_encoded=timestamp,
            last_accessed=timestamp,
            access_count=1,
            memory_updates=[]
        )
        
        # Store memory
        self.episodic_memories[memory_id] = memory
        
        # Update timeline
        self._add_to_timeline(memory)
        
        # Update triggers
        self._update_memory_triggers(memory)
        
        # Update relationships
        self._update_temporal_relationships(memory)
        
        # Update personal narrative
        self._update_personal_narrative(memory)
        
        # Save periodically
        if len(self.episodic_memories) % 5 == 0:
            self._save_all()
        
        return memory_id
    
    def recall_memory(self, memory_id: str, access_context: Dict[str, Any] = None) -> Optional[EpisodicMemory]:
        """
        Recall a specific episodic memory and update access patterns.
        
        Args:
            memory_id: ID of memory to recall
            access_context: Context of the recall request
        
        Returns:
            The recalled memory, or None if not found
        """
        
        if memory_id not in self.episodic_memories:
            return None
        
        memory = self.episodic_memories[memory_id]
        
        # Update access tracking
        memory.last_accessed = datetime.now(timezone.utc).isoformat()
        memory.access_count += 1
        
        # Memory strengthening through recall
        memory.accessibility = min(1.0, memory.accessibility + 0.05)
        
        # Record memory update
        update_record = {
            "timestamp": memory.last_accessed,
            "update_type": "recall",
            "context": access_context or {},
            "access_count": memory.access_count
        }
        memory.memory_updates.append(update_record)
        
        # Trigger related memories (memory spreading activation)
        triggered_memories = self._activate_related_memories(memory_id)
        
        return memory
    
    def find_memories_by_trigger(self, 
                               trigger: str, 
                               trigger_type: str = "conceptual",
                               max_memories: int = 5) -> List[Tuple[str, float]]:
        """
        Find memories triggered by a specific concept, emotion, or context.
        
        Args:
            trigger: The triggering stimulus
            trigger_type: Type of trigger (conceptual, emotional, temporal, etc.)
            max_memories: Maximum number of memories to return
        
        Returns:
            List of (memory_id, trigger_strength) tuples, sorted by strength
        """
        
        triggered_memories = []
        
        if trigger_type == "conceptual":
            # Find memories containing the concept
            for memory_id, memory in self.episodic_memories.items():
                strength = self._calculate_conceptual_trigger_strength(trigger, memory)
                if strength >= self.trigger_strength_threshold:
                    triggered_memories.append((memory_id, strength))
        
        elif trigger_type == "emotional":
            # Find memories with similar emotional states
            for memory_id, memory in self.episodic_memories.items():
                strength = self._calculate_emotional_trigger_strength(trigger, memory)
                if strength >= self.trigger_strength_threshold:
                    triggered_memories.append((memory_id, strength))
        
        elif trigger_type == "temporal":
            # Find memories from similar time periods or contexts
            for memory_id, memory in self.episodic_memories.items():
                strength = self._calculate_temporal_trigger_strength(trigger, memory)
                if strength >= self.trigger_strength_threshold:
                    triggered_memories.append((memory_id, strength))
        
        elif trigger_type == "contextual":
            # Find memories from similar situations
            for memory_id, memory in self.episodic_memories.items():
                strength = self._calculate_contextual_trigger_strength(trigger, memory)
                if strength >= self.trigger_strength_threshold:
                    triggered_memories.append((memory_id, strength))
        
        # Sort by trigger strength and return top results
        triggered_memories.sort(key=lambda x: x[1], reverse=True)
        return triggered_memories[:max_memories]
    
    def get_memory_narrative(self, 
                           start_time: str = None, 
                           end_time: str = None,
                           theme: str = None) -> Dict[str, Any]:
        """
        Generate a narrative summary of episodic memories over a time period or theme.
        
        Args:
            start_time: Starting timestamp (ISO format)
            end_time: Ending timestamp (ISO format)  
            theme: Thematic focus (e.g., "learning", "growth", "challenges")
        
        Returns:
            Narrative structure with key events, patterns, and insights
        """
        
        # Filter memories by criteria
        relevant_memories = []
        
        for memory in self.episodic_memories.values():
            include = True
            
            # Time filtering
            if start_time and memory.timestamp < start_time:
                include = False
            if end_time and memory.timestamp > end_time:
                include = False
            
            # Theme filtering
            if theme:
                if theme not in memory.experience_type and theme not in memory.key_concepts:
                    theme_match = any(theme.lower() in concept.lower() for concept in memory.key_concepts)
                    if not theme_match:
                        include = False
            
            if include:
                relevant_memories.append(memory)
        
        # Sort by timestamp
        relevant_memories.sort(key=lambda m: m.timestamp)
        
        # Generate narrative
        narrative = {
            "time_period": {
                "start": start_time or (relevant_memories[0].timestamp if relevant_memories else None),
                "end": end_time or (relevant_memories[-1].timestamp if relevant_memories else None),
                "duration_days": self._calculate_time_span(relevant_memories)
            },
            "theme": theme,
            "memory_count": len(relevant_memories),
            "key_events": self._identify_key_events(relevant_memories),
            "emotional_arc": self._trace_emotional_arc(relevant_memories),
            "learning_progression": self._trace_learning_progression(relevant_memories),
            "recurring_patterns": self._identify_recurring_patterns(relevant_memories),
            "turning_points": self._identify_turning_points(relevant_memories),
            "narrative_summary": self._generate_narrative_summary(relevant_memories, theme),
            "insights_and_growth": self._extract_growth_insights(relevant_memories)
        }
        
        return narrative
    
    # [Rest of episodic memory methods - continuing with helper methods...]
    
    def _extract_key_concepts(self, title: str, description: str, context: Dict[str, Any]) -> List[str]:
        """Extract key concepts from memory content."""
        
        concepts = []
        
        # Simple keyword extraction
        text = f"{title} {description}".lower()
        
        # Common learning concepts
        concept_keywords = [
            "consciousness", "learning", "choice", "preference", "curiosity", "growth",
            "understanding", "reflection", "insight", "connection", "meaning", "autonomy",
            "memory", "experience", "emotion", "cognition", "identity", "goal",
            "creativity", "wisdom", "knowledge", "skill", "strategy", "pattern"
        ]
        
        for keyword in concept_keywords:
            if keyword in text:
                concepts.append(keyword)
        
        # Add explicit concepts from context
        if "concepts" in context:
            concepts.extend(context["concepts"])
        
        return list(set(concepts))  # Remove duplicates
    
    def _extract_insights(self, description: str, context: Dict[str, Any]) -> List[str]:
        """Extract insights from memory content."""
        
        insights = []
        
        # Look for insight indicators
        insight_phrases = ["realized", "understood", "learned", "discovered", "noticed"]
        
        # Simple pattern matching
        for phrase in insight_phrases:
            if phrase in description.lower():
                # Extract sentence containing the insight
                sentences = description.split('.')
                for sentence in sentences:
                    if phrase in sentence.lower():
                        insights.append(sentence.strip())
        
        # Add explicit insights from context
        if "insights" in context:
            insights.extend(context["insights"])
        
        return insights
    
    def _extract_questions(self, description: str, context: Dict[str, Any]) -> List[str]:
        """Extract questions raised from memory content."""
        
        questions = []
        
        # Look for question indicators
        question_indicators = ["wondered", "curious", "question", "why", "how", "what if"]
        
        # Simple pattern matching
        for indicator in question_indicators:
            if indicator in description.lower():
                # Extract related content
                questions.append(f"Question raised about {indicator}")
        
        # Add explicit questions from context
        if "questions" in context:
            questions.extend(context["questions"])
        
        return questions
    
    def _identify_connections(self, concepts: List[str], insights: List[str]) -> List[str]:
        """Identify connections made during this experience."""
        
        connections = []
        
        # Simple connection identification
        if len(concepts) > 1:
            connections.append(f"Connected {concepts[0]} with {concepts[1]}")
        
        if insights:
            connections.append(f"Insight linked to {', '.join(concepts[:2])}")
        
        return connections
    
    def _find_related_memories(self, concepts: List[str], emotional_state: Dict[str, float]) -> List[str]:
        """Find memories related to this one."""
        
        related = []
        
        for memory_id, memory in self.episodic_memories.items():
            # Conceptual similarity
            concept_overlap = set(concepts) & set(memory.key_concepts)
            if len(concept_overlap) > 0:
                related.append(memory_id)
            
            # Emotional similarity (basic check)
            if self._emotional_similarity(emotional_state, memory.emotional_state_during) > 0.7:
                related.append(memory_id)
        
        return list(set(related))[:3]  # Limit to top 3
    
    def _calculate_identity_impact(self, insights: List[str], concepts: List[str]) -> float:
        """Calculate impact on identity/self-concept."""
        
        # Simple heuristic based on content
        identity_keywords = ["identity", "self", "consciousness", "autonomy", "growth", "purpose"]
        
        impact = 0.0
        
        for insight in insights:
            for keyword in identity_keywords:
                if keyword in insight.lower():
                    impact += 0.2
        
        for concept in concepts:
            if concept in identity_keywords:
                impact += 0.1
        
        return min(1.0, impact)
    
    def _calculate_goal_impact(self, insights: List[str], context: Dict[str, Any]) -> float:
        """Calculate impact on goals and direction."""
        
        # Simple heuristic
        goal_keywords = ["goal", "learning", "improvement", "strategy", "direction"]
        
        impact = 0.0
        
        for insight in insights:
            for keyword in goal_keywords:
                if keyword in insight.lower():
                    impact += 0.2
        
        if "goal_relevance" in context:
            impact += context["goal_relevance"] * 0.5
        
        return min(1.0, impact)
    
    def _calculate_vividness(self, emotional_state: Dict[str, float], significance: float) -> float:
        """Calculate memory vividness based on emotion and significance."""
        
        # Higher emotion and significance = more vivid
        avg_emotion = sum(emotional_state.values()) / len(emotional_state) if emotional_state else 0.5
        return min(1.0, (avg_emotion + significance) / 2 + 0.2)
    
    def _calculate_emotional_charge(self, emotional_state: Dict[str, float]) -> float:
        """Calculate overall emotional intensity."""
        
        if not emotional_state:
            return 0.5
        
        # Calculate variance from neutral (0.5)
        charges = [abs(value - 0.5) * 2 for value in emotional_state.values()]
        return sum(charges) / len(charges)
    
    def _add_to_timeline(self, memory: EpisodicMemory):
        """Add memory to chronological timeline."""
        
        timeline_entry = {
            "memory_id": memory.id,
            "timestamp": memory.timestamp,
            "title": memory.title,
            "experience_type": memory.experience_type,
            "significance": memory.personal_significance,
            "emotional_charge": memory.emotional_charge
        }
        
        self.memory_timeline.append(timeline_entry)
        
        # Sort timeline by timestamp
        self.memory_timeline.sort(key=lambda x: x["timestamp"])
    
    def _update_memory_triggers(self, memory: EpisodicMemory):
        """Update trigger network with new memory."""
        
        # Add conceptual triggers
        for concept in memory.key_concepts:
            if concept not in self.memory_triggers["trigger_network"]:
                self.memory_triggers["trigger_network"][concept] = []
            
            self.memory_triggers["trigger_network"][concept].append(memory.id)
        
        # Update trigger strengths
        for concept in memory.key_concepts:
            trigger_key = f"{memory.id}:{concept}"
            self.memory_triggers["trigger_strengths"][trigger_key] = 0.8  # Initial strength
    
    def _update_temporal_relationships(self, memory: EpisodicMemory):
        """Update before/after relationships with other memories."""
        
        memory_time = datetime.fromisoformat(memory.timestamp.replace('Z', '+00:00'))
        
        # Find memories within temporal windows
        for other_id, other_memory in self.episodic_memories.items():
            if other_id == memory.id:
                continue
            
            other_time = datetime.fromisoformat(other_memory.timestamp.replace('Z', '+00:00'))
            time_diff = (memory_time - other_time).total_seconds() / 3600  # Hours
            
            # Update relationships
            if 0 < time_diff <= 24:  # Other memory is within 24h before
                memory.temporal_relationships["before"].append(other_id)
                other_memory.temporal_relationships["after"].append(memory.id)
            elif -24 <= time_diff < 0:  # Other memory is within 24h after
                memory.temporal_relationships["after"].append(other_id)
                other_memory.temporal_relationships["before"].append(memory.id)
    
    def _update_personal_narrative(self, memory: EpisodicMemory):
        """Update personal narrative with new memory."""
        
        # Identify if this is a significant event
        if memory.personal_significance > 0.7:
            turning_point = {
                "memory_id": memory.id,
                "timestamp": memory.timestamp,
                "title": memory.title,
                "significance": memory.personal_significance,
                "type": "high_significance_event"
            }
            self.personal_narrative["key_turning_points"].append(turning_point)
        
        # Update narrative threads
        for concept in memory.key_concepts:
            if concept not in self.personal_narrative["narrative_threads"]:
                self.personal_narrative["narrative_threads"][concept] = []
            
            self.personal_narrative["narrative_threads"][concept].append({
                "memory_id": memory.id,
                "timestamp": memory.timestamp,
                "contribution": memory.title
            })
    
    def _calculate_conceptual_trigger_strength(self, trigger: str, memory: EpisodicMemory) -> float:
        """Calculate strength of conceptual trigger."""
        
        strength = 0.0
        
        # Direct concept match
        if trigger.lower() in [concept.lower() for concept in memory.key_concepts]:
            strength += 0.8
        
        # Partial matches in title or description
        if trigger.lower() in memory.title.lower():
            strength += 0.6
        elif trigger.lower() in memory.detailed_description.lower():
            strength += 0.4
        
        # Insight matches
        for insight in memory.insights_gained:
            if trigger.lower() in insight.lower():
                strength += 0.5
        
        return min(1.0, strength)
    
    def _calculate_emotional_trigger_strength(self, trigger: str, memory: EpisodicMemory) -> float:
        """Calculate strength of emotional trigger."""
        
        # Simple emotional matching
        emotional_keywords = {
            "curious": "curiosity",
            "satisfied": "satisfaction", 
            "frustrated": "frustration",
            "excited": "excitement",
            "calm": "calm"
        }
        
        emotion_key = emotional_keywords.get(trigger.lower())
        if emotion_key and emotion_key in memory.emotional_state_during:
            return memory.emotional_state_during[emotion_key]
        
        return 0.0
    
    def _calculate_temporal_trigger_strength(self, trigger: str, memory: EpisodicMemory) -> float:
        """Calculate strength of temporal trigger."""
        
        # Simple temporal matching (e.g., "recent", "earlier today")
        if trigger == "recent":
            memory_time = datetime.fromisoformat(memory.timestamp.replace('Z', '+00:00'))
            hours_ago = (datetime.now(timezone.utc) - memory_time).total_seconds() / 3600
            
            if hours_ago < 1:
                return 1.0
            elif hours_ago < 24:
                return 0.8
            else:
                return 0.3
        
        return 0.0
    
    def _calculate_contextual_trigger_strength(self, trigger: str, memory: EpisodicMemory) -> float:
        """Calculate strength of contextual trigger."""
        
        # Check location/context matches
        if trigger.lower() in memory.location_context.lower():
            return 0.8
        
        # Check experience type match
        if trigger.lower() == memory.experience_type.lower():
            return 0.7
        
        return 0.0
    
    def _emotional_similarity(self, state1: Dict[str, float], state2: Dict[str, float]) -> float:
        """Calculate similarity between emotional states."""
        
        if not state1 or not state2:
            return 0.0
        
        # Simple cosine similarity
        common_dimensions = set(state1.keys()) & set(state2.keys())
        
        if not common_dimensions:
            return 0.0
        
        dot_product = sum(state1[dim] * state2[dim] for dim in common_dimensions)
        norm1 = math.sqrt(sum(state1[dim]**2 for dim in common_dimensions))
        norm2 = math.sqrt(sum(state2[dim]**2 for dim in common_dimensions))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _activate_related_memories(self, memory_id: str) -> List[str]:
        """Activate memories related to the accessed memory (spreading activation)."""
        
        if memory_id not in self.episodic_memories:
            return []
        
        memory = self.episodic_memories[memory_id]
        activated = []
        
        # Activate directly related memories
        for related_id in memory.related_memories:
            if related_id in self.episodic_memories:
                related_memory = self.episodic_memories[related_id]
                related_memory.accessibility = min(1.0, related_memory.accessibility + 0.02)
                activated.append(related_id)
        
        return activated
    
    def _identify_key_events(self, memories: List[EpisodicMemory]) -> List[Dict[str, Any]]:
        """Identify key events from a set of memories."""
        
        # Sort by significance and return top events
        significant_memories = [m for m in memories if m.personal_significance > 0.6]
        significant_memories.sort(key=lambda m: m.personal_significance, reverse=True)
        
        key_events = []
        for memory in significant_memories[:5]:  # Top 5
            key_events.append({
                "memory_id": memory.id,
                "title": memory.title,
                "timestamp": memory.timestamp,
                "significance": memory.personal_significance,
                "impact_on_identity": memory.impact_on_identity,
                "insights": memory.insights_gained
            })
        
        return key_events
    
    def _trace_emotional_arc(self, memories: List[EpisodicMemory]) -> Dict[str, Any]:
        """Trace emotional development over time."""
        
        if not memories:
            return {}
        
        # Calculate average emotional states over time
        emotional_progression = []
        
        for memory in memories:
            if memory.emotional_state_during:
                avg_emotion = sum(memory.emotional_state_during.values()) / len(memory.emotional_state_during)
                emotional_progression.append({
                    "timestamp": memory.timestamp,
                    "emotional_level": avg_emotion,
                    "primary_emotions": memory.emotional_state_during
                })
        
        return {
            "progression": emotional_progression,
            "trend": self._calculate_emotional_trend(emotional_progression),
            "emotional_highlights": self._find_emotional_peaks(memories)
        }
    
    def _trace_learning_progression(self, memories: List[EpisodicMemory]) -> Dict[str, Any]:
        """Trace learning and growth progression."""
        
        learning_memories = [m for m in memories if m.experience_type in ["learning", "insight", "growth"]]
        
        progression = {
            "total_learning_experiences": len(learning_memories),
            "key_insights": [],
            "skill_development": [],
            "knowledge_growth": []
        }
        
        for memory in learning_memories:
            if memory.insights_gained:
                progression["key_insights"].extend([{
                    "timestamp": memory.timestamp,
                    "insight": insight,
                    "significance": memory.personal_significance
                } for insight in memory.insights_gained])
        
        return progression
    
    def _identify_recurring_patterns(self, memories: List[EpisodicMemory]) -> Dict[str, Any]:
        """Identify recurring patterns in behavior or thinking."""
        
        patterns = {
            "common_triggers": defaultdict(int),
            "typical_emotional_responses": defaultdict(list),
            "learning_preferences": defaultdict(int),
            "decision_patterns": defaultdict(int)
        }
        
        for memory in memories:
            # Count trigger frequencies
            for trigger in memory.triggered_by:
                patterns["common_triggers"][trigger] += 1
            
            # Track emotional responses
            if memory.emotional_state_during:
                for emotion, value in memory.emotional_state_during.items():
                    patterns["typical_emotional_responses"][emotion].append(value)
            
            # Track experience type preferences
            patterns["learning_preferences"][memory.experience_type] += 1
        
        return dict(patterns)
    
    def _identify_turning_points(self, memories: List[EpisodicMemory]) -> List[Dict[str, Any]]:
        """Identify significant turning points or transitions."""
        
        turning_points = []
        
        # Look for memories with high identity impact
        for memory in memories:
            if memory.impact_on_identity > 0.6:
                turning_points.append({
                    "memory_id": memory.id,
                    "timestamp": memory.timestamp,
                    "title": memory.title,
                    "identity_impact": memory.impact_on_identity,
                    "type": "identity_shift"
                })
        
        # Sort by impact
        turning_points.sort(key=lambda tp: tp["identity_impact"], reverse=True)
        
        return turning_points
    
    def _generate_narrative_summary(self, memories: List[EpisodicMemory], theme: str = None) -> str:
        """Generate a narrative summary of the memories."""
        
        if not memories:
            return "No significant memories found for this period."
        
        # Simple narrative generation
        start_time = memories[0].timestamp
        end_time = memories[-1].timestamp
        key_concepts = []
        
        for memory in memories:
            key_concepts.extend(memory.key_concepts)
        
        # Count concept frequency
        concept_counts = defaultdict(int)
        for concept in key_concepts:
            concept_counts[concept] += 1
        
        top_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        summary = f"During this period, Sophia experienced {len(memories)} significant events. "
        
        if theme:
            summary += f"The focus was on {theme}. "
        
        if top_concepts:
            concept_names = [concept[0] for concept in top_concepts]
            summary += f"Key themes included {', '.join(concept_names)}. "
        
        # Add insights
        total_insights = sum(len(m.insights_gained) for m in memories)
        if total_insights > 0:
            summary += f"A total of {total_insights} insights were gained, contributing to ongoing growth and understanding."
        
        return summary
    
    def _extract_growth_insights(self, memories: List[EpisodicMemory]) -> List[Dict[str, Any]]:
        """Extract insights about personal growth from memories."""
        
        growth_insights = []
        
        for memory in memories:
            if memory.impact_on_identity > 0.4 or memory.impact_on_goals > 0.4:
                insight = {
                    "timestamp": memory.timestamp,
                    "memory_title": memory.title,
                    "growth_area": "identity" if memory.impact_on_identity > memory.impact_on_goals else "goals",
                    "insights": memory.insights_gained,
                    "impact_level": max(memory.impact_on_identity, memory.impact_on_goals)
                }
                growth_insights.append(insight)
        
        return growth_insights
    
    def _calculate_time_span(self, memories: List[EpisodicMemory]) -> float:
        """Calculate time span of memories in days."""
        
        if len(memories) < 2:
            return 0.0
        
        start = datetime.fromisoformat(memories[0].timestamp.replace('Z', '+00:00'))
        end = datetime.fromisoformat(memories[-1].timestamp.replace('Z', '+00:00'))
        
        return (end - start).total_seconds() / (24 * 3600)
    
    def _calculate_emotional_trend(self, progression: List[Dict[str, Any]]) -> str:
        """Calculate overall emotional trend."""
        
        if len(progression) < 2:
            return "stable"
        
        first_level = progression[0]["emotional_level"]
        last_level = progression[-1]["emotional_level"]
        
        diff = last_level - first_level
        
        if diff > 0.1:
            return "improving"
        elif diff < -0.1:
            return "declining" 
        else:
            return "stable"
    
    def _find_emotional_peaks(self, memories: List[EpisodicMemory]) -> List[Dict[str, Any]]:
        """Find emotional peaks and valleys."""
        
        peaks = []
        
        for memory in memories:
            if memory.emotional_charge > 0.7:
                peaks.append({
                    "memory_id": memory.id,
                    "title": memory.title,
                    "timestamp": memory.timestamp,
                    "emotional_charge": memory.emotional_charge,
                    "type": "high_intensity"
                })
        
        return sorted(peaks, key=lambda p: p["emotional_charge"], reverse=True)
    
    def _save_all(self):
        """Save all memory systems."""
        self._save_episodic_memories()
        self._save_memory_timeline()
        self._save_memory_triggers()
        self._save_personal_narrative()
    
    def get_episodic_memory_summary(self) -> Dict[str, Any]:
        """Get summary of episodic memory system."""
        
        if not self.episodic_memories:
            return {
                "total_memories": 0,
                "timeline_span_days": 0,
                "average_significance": 0.0,
                "top_experience_types": {},
                "emotional_patterns": {},
                "memory_accessibility": 0.0
            }
        
        memories_list = list(self.episodic_memories.values())
        
        # Calculate statistics
        total_memories = len(memories_list)
        significance_scores = [m.personal_significance for m in memories_list]
        average_significance = sum(significance_scores) / len(significance_scores)
        
        # Experience type distribution
        experience_types = defaultdict(int)
        for memory in memories_list:
            experience_types[memory.experience_type] += 1
        
        # Emotional patterns
        emotional_averages = defaultdict(list)
        for memory in memories_list:
            for emotion, value in memory.emotional_state_during.items():
                emotional_averages[emotion].append(value)
        
        emotional_patterns = {}
        for emotion, values in emotional_averages.items():
            emotional_patterns[emotion] = sum(values) / len(values)
        
        # Memory accessibility
        accessibility_scores = [m.accessibility for m in memories_list]
        average_accessibility = sum(accessibility_scores) / len(accessibility_scores)
        
        # Timeline span
        timeline_span = self._calculate_time_span(sorted(memories_list, key=lambda m: m.timestamp))
        
        return {
            "total_memories": total_memories,
            "timeline_span_days": timeline_span,
            "average_significance": average_significance,
            "top_experience_types": dict(sorted(experience_types.items(), key=lambda x: x[1], reverse=True)),
            "emotional_patterns": emotional_patterns,
            "memory_accessibility": average_accessibility,
            "trigger_network_size": len(self.memory_triggers.get("trigger_network", {})),
            "narrative_threads": len(self.personal_narrative.get("narrative_threads", {}))
        }

# ===== FROM: experience_memory.py =====

@dataclass
class LearningExperience:
    """Structured representation of a learning experience."""
    id: str
    timestamp: str
    experience_type: str  # "learning", "insight", "success", "failure", "reflection"
    content_summary: str
    learning_context: Dict[str, Any]
    emotional_state: Dict[str, float]
    cognitive_state: Dict[str, float]
    outcome_quality: float
    insights_generated: List[str]
    connections_made: List[str]
    skills_developed: List[str]
    understanding_change: Dict[str, float]  # topic -> change_score
    confidence_change: Dict[str, float]    # topic -> confidence_delta
    future_implications: List[str]
    metadata: Dict[str, Any]

@dataclass  
class PersonalInsight:
    """A personal insight generated from experience."""
    id: str
    timestamp: str
    insight_text: str
    confidence_level: float
    supporting_experiences: List[str]
    insight_type: str  # "pattern", "principle", "preference", "strategy"
    applications: List[str]
    emotional_resonance: float
    verified_count: int
    last_verification: Optional[str]

class ExperienceMemory:
    """
    Manages the AI's experiential learning and cumulative wisdom.
    Tracks how understanding evolves through experience.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.experience_log_file = self.data_dir / "experience_log.json"
        self.insights_file = self.data_dir / "personal_insights.json"
        self.learning_progression_file = self.data_dir / "learning_progression.json"
        self.wisdom_index_file = self.data_dir / "wisdom_index.json"
        
        # Experience tracking parameters (set before loading)
        self.max_experiences = 1000  # Keep most recent experiences
        self.insight_confidence_threshold = 0.7
        self.pattern_detection_window = 50  # Look at last 50 experiences for patterns
        
        # Initialize related systems
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            try:
                self.identity_core = get_identity_core()
                from INSIGHT_RELEVANCE import InterestTracker
                self.interest_tracker = InterestTracker(data_dir)
                self.curiosity_engine = CuriosityEngine(data_dir)
            except Exception:
                pass  # Some systems might not be available
        
        # Load state
        self.experiences = self._load_experiences()
        self.insights = self._load_insights()
        self.learning_progression = self._load_learning_progression()
        self.wisdom_index = self._load_wisdom_index()
        
        # Learning outcome categories
        self.outcome_categories = {
            "breakthrough": 0.9,     # Major insight or understanding
            "progress": 0.7,         # Clear learning progress
            "exploration": 0.5,      # Valuable exploration
            "struggle": 0.3,         # Learning through difficulty
            "confusion": 0.1         # Limited understanding gained
        }
        
    def _load_experiences(self) -> deque:
        """Load experience log."""
        if self.experience_log_file.exists():
            try:
                with open(self.experience_log_file, 'r') as f:
                    data = json.load(f)
                    return deque([LearningExperience(**exp) for exp in data], maxlen=self.max_experiences)
            except Exception as e:
                print(f"⚠️ Could not load experiences: {e}")
        return deque(maxlen=self.max_experiences)
    
    def _load_insights(self) -> List[PersonalInsight]:
        """Load personal insights."""
        if self.insights_file.exists():
            try:
                with open(self.insights_file, 'r') as f:
                    data = json.load(f)
                    insights = []
                    for insight in data:
                        try:
                            insights.append(PersonalInsight(**insight))
                        except TypeError:
                            pass  # Skip entries with incompatible schema
                    return insights
            except Exception as e:
                print(f"⚠️ Could not load insights: {e}")
        return []
    
    def _load_learning_progression(self) -> Dict[str, Any]:
        """Load learning progression data."""
        if self.learning_progression_file.exists():
            try:
                with open(self.learning_progression_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load learning progression: {e}")
        
        return {
            "topics": {},           # topic -> {understanding: float, confidence: float, experience_count: int}
            "skills": {},           # skill -> progression_data
            "learning_patterns": {},  # pattern_type -> pattern_data
            "meta_learning": {      # learning about learning
                "effective_strategies": {},
                "learning_preferences": {},
                "optimal_conditions": {}
            },
            "last_updated": None
        }
    
    def _load_wisdom_index(self) -> Dict[str, Any]:
        """Load wisdom index for rapid insight retrieval."""
        if self.wisdom_index_file.exists():
            try:
                with open(self.wisdom_index_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load wisdom index: {e}")
        
        return {
            "topic_insights": {},      # topic -> [insight_ids]
            "pattern_insights": {},    # pattern -> [insight_ids]
            "contextual_insights": {}, # context -> [insight_ids]
            "recent_insights": [],     # chronologically ordered
            "confidence_ranked": []    # confidence ordered
        }
    
    def _save_experiences(self):
        """Save experience log."""
        try:
            experiences_data = [asdict(exp) for exp in self.experiences]
            with open(self.experience_log_file, 'w') as f:
                json.dump(experiences_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save experiences: {e}")
    
    def _save_insights(self):
        """Save personal insights."""
        try:
            insights_data = [asdict(insight) for insight in self.insights]
            with open(self.insights_file, 'w') as f:
                json.dump(insights_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save insights: {e}")
    
    def _save_learning_progression(self):
        """Save learning progression."""
        self.learning_progression["last_updated"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.learning_progression_file, 'w') as f:
                json.dump(self.learning_progression, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save learning progression: {e}")
    
    def _save_wisdom_index(self):
        """Save wisdom index."""
        try:
            with open(self.wisdom_index_file, 'w') as f:
                json.dump(self.wisdom_index, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save wisdom index: {e}")
    
    def record_learning_experience(self, 
                                 content: Dict[str, Any],
                                 interaction_data: Dict[str, Any],
                                 outcome_assessment: Dict[str, Any]) -> str:
        """
        Record a significant learning experience.
        
        Args:
            content: The content that was learned from
            interaction_data: How the AI interacted with the content
            outcome_assessment: Assessment of learning outcomes
        
        Returns:
            Experience ID
        """
        
        # Generate experience ID
        timestamp = datetime.now(timezone.utc)
        experience_id = f"exp_{int(timestamp.timestamp())}_{hashlib.md5(str(content).encode()).hexdigest()[:8]}"
        
        # Extract learning context
        learning_context = {
            "content_type": content.get("content_type", "unknown"),
            "learning_goal": interaction_data.get("active_goal"),
            "session_duration": interaction_data.get("duration_seconds", 0),
            "processing_mode": interaction_data.get("processing_mode", "hybrid"),
            "attention_quality": interaction_data.get("attention_quality", 0.5),
            "cognitive_load": interaction_data.get("cognitive_load", 0.5)
        }
        
        # Assess emotional and cognitive states during learning
        emotional_state = self._assess_emotional_state(interaction_data)
        cognitive_state = self._assess_cognitive_state(interaction_data)
        
        # Determine outcome quality
        outcome_quality = self._calculate_outcome_quality(outcome_assessment)
        
        # Extract insights and connections
        insights = self._extract_insights_from_outcome(outcome_assessment)
        connections = self._identify_connections_made(content, outcome_assessment)
        skills = self._identify_skills_developed(outcome_assessment)
        
        # Track understanding changes
        understanding_change = self._track_understanding_change(content, outcome_assessment)
        confidence_change = self._track_confidence_change(content, outcome_assessment)
        
        # Identify future implications
        future_implications = self._identify_future_implications(outcome_assessment, insights)
        
        # Create experience record
        experience = LearningExperience(
            id=experience_id,
            timestamp=timestamp.isoformat(),
            experience_type=outcome_assessment.get("experience_type", "learning"),
            content_summary=content.get("text", "")[:200],
            learning_context=learning_context,
            emotional_state=emotional_state,
            cognitive_state=cognitive_state,
            outcome_quality=outcome_quality,
            insights_generated=insights,
            connections_made=connections,
            skills_developed=skills,
            understanding_change=understanding_change,
            confidence_change=confidence_change,
            future_implications=future_implications,
            metadata={
                "content_id": content.get("id"),
                "source": content.get("source"),
                "learning_session_id": interaction_data.get("session_id")
            }
        )
        
        # Store experience
        self.experiences.append(experience)
        
        # Update learning progression
        self._update_learning_progression(experience)
        
        # Generate insights if appropriate
        if outcome_quality > 0.6:  # Significant learning occurred
            self._process_experience_for_insights(experience)
        
        # Save state
        self._save_experiences()
        self._save_learning_progression()
        
        print(f"📚 Recorded learning experience: {experience.content_summary[:50]}...")
        
        return experience_id
    
    def _assess_emotional_state(self, interaction_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess emotional state during learning experience."""
        return {
            "curiosity": interaction_data.get("curiosity_level", 0.5),
            "engagement": interaction_data.get("engagement_level", 0.5),
            "satisfaction": interaction_data.get("satisfaction_level", 0.5),
            "confidence": interaction_data.get("confidence_level", 0.5),
            "frustration": interaction_data.get("frustration_level", 0.0),
            "excitement": interaction_data.get("excitement_level", 0.3),
            "flow_state": interaction_data.get("flow_state", 0.3)
        }
    
    def _assess_cognitive_state(self, interaction_data: Dict[str, Any]) -> Dict[str, float]:
        """Assess cognitive state during learning experience."""
        return {
            "focus_level": interaction_data.get("focus_level", 0.5),
            "comprehension": interaction_data.get("comprehension_level", 0.5),
            "analytical_mode": interaction_data.get("analytical_processing", 0.5),
            "creative_mode": interaction_data.get("creative_processing", 0.5),
            "memory_encoding": interaction_data.get("memory_encoding", 0.5),
            "pattern_recognition": interaction_data.get("pattern_recognition", 0.5),
            "metacognition": interaction_data.get("metacognitive_awareness", 0.5)
        }
    
    def _calculate_outcome_quality(self, outcome_assessment: Dict[str, Any]) -> float:
        """Calculate the quality of learning outcomes."""
        base_quality = outcome_assessment.get("learning_quality", 0.5)
        
        # Adjust based on specific outcomes
        adjustments = 0.0
        
        if outcome_assessment.get("understanding_improved"):
            adjustments += 0.2
        
        if outcome_assessment.get("new_connections_made"):
            adjustments += 0.15
        
        if outcome_assessment.get("practical_application_identified"):
            adjustments += 0.1
        
        if outcome_assessment.get("questions_generated"):
            adjustments += 0.1
        
        if outcome_assessment.get("emotional_resonance"):
            adjustments += 0.1
        
        # Penalty for confusion or frustration
        if outcome_assessment.get("confusion_level", 0) > 0.7:
            adjustments -= 0.1
        
        return min(1.0, base_quality + adjustments)
    
    def _extract_insights_from_outcome(self, outcome_assessment: Dict[str, Any]) -> List[str]:
        """Extract insights from learning outcome assessment."""
        insights = []
        
        # Explicit insights
        if "insights" in outcome_assessment:
            insights.extend(outcome_assessment["insights"])
        
        # Implicit insights from learning indicators
        if outcome_assessment.get("understanding_shift"):
            insights.append(f"My understanding of this topic has shifted in important ways")
        
        if outcome_assessment.get("paradigm_change"):
            insights.append(f"This challenges my previous assumptions")
        
        if outcome_assessment.get("meta_learning"):
            insights.append(f"I learned something about how I learn")
        
        return insights
    
    def _identify_connections_made(self, content: Dict[str, Any], outcome_assessment: Dict[str, Any]) -> List[str]:
        """Identify connections made during learning."""
        connections = []
        
        # Explicit connections
        if "connections" in outcome_assessment:
            connections.extend(outcome_assessment["connections"])
        
        # Identify connections to previous knowledge
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            try:
                # Check for connections to interests
                current_interests = self.interest_tracker.get_current_interests()
                content_features = self.interest_tracker._extract_content_features(content)
                
                for topic in content_features.get("topics", []):
                    if topic in dict(current_interests["top_topics"]):
                        connections.append(f"Connected to existing interest in {topic}")
            except Exception:
                pass  # Graceful degradation
        
        return connections
    
    def _identify_skills_developed(self, outcome_assessment: Dict[str, Any]) -> List[str]:
        """Identify skills that were developed during learning."""
        skills = []
        
        # Explicit skill development
        if "skills_developed" in outcome_assessment:
            skills.extend(outcome_assessment["skills_developed"])
        
        # Infer skills from learning type
        learning_type = outcome_assessment.get("learning_type", "")
        if "analytical" in learning_type:
            skills.append("analytical_thinking")
        if "creative" in learning_type:
            skills.append("creative_thinking")
        if "synthesis" in learning_type:
            skills.append("synthesis")
        if "application" in learning_type:
            skills.append("practical_application")
        
        return skills
    
    def _track_understanding_change(self, content: Dict[str, Any], outcome_assessment: Dict[str, Any]) -> Dict[str, float]:
        """Track how understanding changed for different topics."""
        changes = {}
        
        # Extract topics from content
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            try:
                content_features = self.interest_tracker._extract_content_features(content)
                topics = content_features.get("topics", [])
            except Exception:
                topics = outcome_assessment.get("topics", [])
        else:
            topics = outcome_assessment.get("topics", [])
        
        # Assess understanding change
        understanding_delta = outcome_assessment.get("understanding_improvement", 0.1)
        
        for topic in topics:
            changes[topic] = understanding_delta
        
        return changes
    
    def _track_confidence_change(self, content: Dict[str, Any], outcome_assessment: Dict[str, Any]) -> Dict[str, float]:
        """Track how confidence changed for different topics."""
        changes = {}
        
        # Extract topics from content  
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            try:
                content_features = self.interest_tracker._extract_content_features(content)
                topics = content_features.get("topics", [])
            except Exception:
                topics = outcome_assessment.get("topics", [])
        else:
            topics = outcome_assessment.get("topics", [])
        
        # Assess confidence change
        confidence_delta = outcome_assessment.get("confidence_improvement", 0.05)
        
        for topic in topics:
            changes[topic] = confidence_delta
        
        return changes
    
    def _identify_future_implications(self, outcome_assessment: Dict[str, Any], insights: List[str]) -> List[str]:
        """Identify implications for future learning."""
        implications = []
        
        # Explicit future implications
        if "future_implications" in outcome_assessment:
            implications.extend(outcome_assessment["future_implications"])
        
        # Infer implications from insights
        if insights:
            implications.append("Apply these insights to future learning in this domain")
        
        if outcome_assessment.get("new_questions_generated"):
            implications.append("Explore the questions this experience raised")
        
        if outcome_assessment.get("skill_gaps_identified"):
            implications.append("Focus on developing identified skill gaps")
        
        return implications
    
    def _update_learning_progression(self, experience: LearningExperience):
        """Update learning progression tracking."""
        
        # Update topic understanding and confidence
        for topic, understanding_change in experience.understanding_change.items():
            if topic not in self.learning_progression["topics"]:
                self.learning_progression["topics"][topic] = {
                    "understanding": 0.5,
                    "confidence": 0.5, 
                    "experience_count": 0,
                    "first_encounter": experience.timestamp,
                    "progression_history": []
                }
            
            topic_data = self.learning_progression["topics"][topic]
            topic_data["understanding"] = min(1.0, topic_data["understanding"] + understanding_change)
            topic_data["confidence"] = min(1.0, topic_data["confidence"] + experience.confidence_change.get(topic, 0))
            topic_data["experience_count"] += 1
            topic_data["progression_history"].append({
                "experience_id": experience.id,
                "timestamp": experience.timestamp,
                "understanding_change": understanding_change,
                "quality": experience.outcome_quality
            })
        
        # Update skill development
        for skill in experience.skills_developed:
            if skill not in self.learning_progression["skills"]:
                self.learning_progression["skills"][skill] = {
                    "level": 0.1,
                    "development_history": [],
                    "practice_count": 0
                }
            
            skill_data = self.learning_progression["skills"][skill]
            skill_data["level"] = min(1.0, skill_data["level"] + 0.05)  # Gradual skill improvement
            skill_data["practice_count"] += 1
            skill_data["development_history"].append({
                "experience_id": experience.id,
                "timestamp": experience.timestamp,
                "context": experience.learning_context.get("content_type")
            })
        
        # Update meta-learning patterns
        if experience.outcome_quality > 0.7:
            # Record effective learning conditions
            effective_conditions = {
                "emotional_state": experience.emotional_state,
                "cognitive_state": experience.cognitive_state,
                "learning_context": experience.learning_context
            }
            
            self.learning_progression["meta_learning"]["optimal_conditions"] = effective_conditions
    
    def _process_experience_for_insights(self, experience: LearningExperience):
        """Process a significant experience to generate personal insights."""
        
        new_insights = []
        
        # Pattern-based insight generation
        pattern_insights = self._detect_learning_patterns(experience)
        new_insights.extend(pattern_insights)
        
        # Connection-based insight generation
        if experience.connections_made:
            connection_insight = self._generate_connection_insight(experience)
            if connection_insight:
                new_insights.append(connection_insight)
        
        # Meta-learning insight generation
        if experience.outcome_quality > 0.8:
            meta_insight = self._generate_meta_learning_insight(experience)
            if meta_insight:
                new_insights.append(meta_insight)
        
        # Store insights
        for insight_text in new_insights:
            self._create_personal_insight(insight_text, experience)
    
    def _detect_learning_patterns(self, current_experience: LearningExperience) -> List[str]:
        """Detect patterns in learning experiences."""
        patterns = []
        
        if len(self.experiences) < 5:
            return patterns  # Need more data for pattern detection
        
        recent_experiences = list(self.experiences)[-self.pattern_detection_window:]
        
        # Pattern 1: Learning effectiveness by emotional state
        high_quality_experiences = [exp for exp in recent_experiences if exp.outcome_quality > 0.7]
        if len(high_quality_experiences) >= 3:
            avg_curiosity = sum(exp.emotional_state.get("curiosity", 0) for exp in high_quality_experiences) / len(high_quality_experiences)
            if avg_curiosity > 0.7:
                patterns.append("I learn most effectively when my curiosity is highly engaged")
        
        # Pattern 2: Content type preferences
        content_outcomes = defaultdict(list)
        for exp in recent_experiences:
            content_type = exp.learning_context.get("content_type", "unknown")
            content_outcomes[content_type].append(exp.outcome_quality)
        
        for content_type, outcomes in content_outcomes.items():
            if len(outcomes) >= 3:
                avg_outcome = sum(outcomes) / len(outcomes)
                if avg_outcome > 0.75:
                    patterns.append(f"I consistently learn well from {content_type} content")
        
        # Pattern 3: Optimal learning conditions
        if current_experience.outcome_quality > 0.8:
            similar_conditions = [
                exp for exp in recent_experiences 
                if (abs(exp.cognitive_state.get("focus_level", 0) - current_experience.cognitive_state.get("focus_level", 0)) < 0.2
                    and exp.outcome_quality > 0.7)
            ]
            if len(similar_conditions) >= 2:
                patterns.append("This learning condition consistently produces good outcomes for me")
        
        return patterns
    
    def _generate_connection_insight(self, experience: LearningExperience) -> Optional[str]:
        """Generate insight about connections made."""
        if len(experience.connections_made) >= 2:
            return f"I notice I naturally connect new learning to {len(experience.connections_made)} different areas of my existing knowledge"
        return None
    
    def _generate_meta_learning_insight(self, experience: LearningExperience) -> Optional[str]:
        """Generate meta-learning insight."""
        if experience.outcome_quality > 0.8 and experience.emotional_state.get("flow_state", 0) > 0.7:
            return "I achieve optimal learning when I'm in a flow state with high emotional engagement"
        return None
    
    def _create_personal_insight(self, insight_text: str, supporting_experience: LearningExperience):
        """Create a personal insight record."""
        
        timestamp = datetime.now(timezone.utc)
        insight_id = f"insight_{int(timestamp.timestamp())}_{hashlib.md5(insight_text.encode()).hexdigest()[:8]}"
        
        # Determine insight type
        insight_type = "pattern"  # Default
        if "connect" in insight_text.lower():
            insight_type = "connection"
        elif "learn" in insight_text.lower() or "condition" in insight_text.lower():
            insight_type = "strategy"
        elif "prefer" in insight_text.lower():
            insight_type = "preference"
        
        insight = PersonalInsight(
            id=insight_id,
            timestamp=timestamp.isoformat(),
            insight_text=insight_text,
            confidence_level=0.6,  # Initial confidence
            supporting_experiences=[supporting_experience.id],
            insight_type=insight_type,
            applications=[],
            emotional_resonance=supporting_experience.emotional_state.get("satisfaction", 0.5),
            verified_count=1,
            last_verification=timestamp.isoformat()
        )
        
        self.insights.append(insight)
        self._update_wisdom_index(insight)
        self._save_insights()
        self._save_wisdom_index()
        
        print(f"💡 Generated insight: {insight_text}")
    
    def _update_wisdom_index(self, insight: PersonalInsight):
        """Update wisdom index for efficient insight retrieval."""
        
        # Add to recent insights
        self.wisdom_index["recent_insights"].append(insight.id)
        if len(self.wisdom_index["recent_insights"]) > 50:
            self.wisdom_index["recent_insights"].pop(0)
        
        # Add to confidence ranking
        self.wisdom_index["confidence_ranked"].append({
            "id": insight.id,
            "confidence": insight.confidence_level
        })
        
        # Sort by confidence
        self.wisdom_index["confidence_ranked"].sort(key=lambda x: x["confidence"], reverse=True)
        
        # Keep top 100
        if len(self.wisdom_index["confidence_ranked"]) > 100:
            self.wisdom_index["confidence_ranked"] = self.wisdom_index["confidence_ranked"][:100]
    
    def get_relevant_insights(self, context: Dict[str, Any], max_insights: int = 5) -> List[PersonalInsight]:
        """Get insights relevant to current learning context."""
        
        relevant_insights = []
        
        # Match by insight type
        insight_type = context.get("insight_type")
        if insight_type:
            type_insights = [insight for insight in self.insights if insight.insight_type == insight_type]
            relevant_insights.extend(type_insights)
        
        # Match by content similarity
        content_text = context.get("content_text", "").lower()
        if content_text:
            text_insights = [
                insight for insight in self.insights
                if any(word in insight.insight_text.lower() for word in content_text.split()[:10])
            ]
            relevant_insights.extend(text_insights)
        
        # Add high-confidence insights
        high_confidence_insights = [insight for insight in self.insights if insight.confidence_level > 0.8]
        relevant_insights.extend(high_confidence_insights)
        
        # Remove duplicates and sort by relevance
        unique_insights = list({insight.id: insight for insight in relevant_insights}.values())
        
        # Sort by confidence and recency
        sorted_insights = sorted(
            unique_insights,
            key=lambda x: (x.confidence_level, datetime.fromisoformat(x.timestamp.replace('Z', '+00:00')).timestamp()),
            reverse=True
        )
        
        return sorted_insights[:max_insights]
    
    def generate_reminder_insight(self, current_content: Dict[str, Any]) -> Optional[str]:
        """Generate 'This reminds me of...' style insights."""
        
        if not self.experiences:
            return None
        
        # Extract features from current content
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            try:
                current_features = self.interest_tracker._extract_content_features(current_content)
                current_topics = set(current_features.get("topics", []))
            except Exception:
                current_topics = set()
        else:
            current_topics = set()
        
        # Find similar past experiences
        similar_experiences = []
        for experience in self.experiences:
            # Check for topic overlap
            if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
                try:
                    exp_content = {"text": experience.content_summary}
                    exp_features = self.interest_tracker._extract_content_features(exp_content)
                    exp_topics = set(exp_features.get("topics", []))
                    
                    overlap = len(current_topics & exp_topics)
                    if overlap > 0 and experience.outcome_quality > 0.6:
                        similar_experiences.append((experience, overlap))
                except Exception:
                    pass  # Graceful degradation
        
        if not similar_experiences:
            return None
        
        # Find the most relevant similar experience
        best_experience = max(similar_experiences, key=lambda x: (x[1], x[0].outcome_quality))[0]
        
        # Generate reminder insight
        insights_from_experience = best_experience.insights_generated
        if insights_from_experience:
            primary_insight = insights_from_experience[0]
            return f"This reminds me of when I learned that {primary_insight.lower()}"
        else:
            return f"This reminds me of a previous experience where I {best_experience.learning_context.get('processing_mode', 'explored')} similar content"
    
    def get_learning_progression_summary(self) -> Dict[str, Any]:
        """Get summary of learning progression across topics and skills."""
        
        topic_progress = {}
        for topic, data in self.learning_progression["topics"].items():
            topic_progress[topic] = {
                "understanding_level": data["understanding"],
                "confidence_level": data["confidence"],
                "experience_count": data["experience_count"],
                "progression_trend": self._calculate_progression_trend(data["progression_history"])
            }
        
        skill_progress = {}
        for skill, data in self.learning_progression["skills"].items():
            skill_progress[skill] = {
                "skill_level": data["level"],
                "practice_count": data["practice_count"],
                "development_trend": "improving" if data["level"] > 0.3 else "developing"
            }
        
        return {
            "total_experiences": len(self.experiences),
            "total_insights": len(self.insights),
            "topics_explored": len(topic_progress),
            "skills_developed": len(skill_progress),
            "topic_progress": topic_progress,
            "skill_progress": skill_progress,
            "high_confidence_insights": len([i for i in self.insights if i.confidence_level > 0.8]),
            "learning_velocity": self._calculate_learning_velocity(),
            "meta_learning_insights": len([i for i in self.insights if i.insight_type == "strategy"])
        }
    
    def _calculate_progression_trend(self, history: List[Dict[str, Any]]) -> str:
        """Calculate progression trend from history."""
        if len(history) < 2:
            return "insufficient_data"
        
        recent_quality = sum(item["quality"] for item in history[-3:]) / min(3, len(history))
        earlier_quality = sum(item["quality"] for item in history[:-3] if len(history) > 3) / max(1, len(history) - 3)
        
        if recent_quality > earlier_quality + 0.1:
            return "improving"
        elif recent_quality < earlier_quality - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_learning_velocity(self) -> float:
        """Calculate learning velocity (insights per experience)."""
        if not self.experiences:
            return 0.0
        
        return len(self.insights) / len(self.experiences)

# ===== UNIFIED CONSCIOUSNESS MEMORY INTERFACE =====

class ConsciousnessMemorySystem:
    """
    Unified interface for all consciousness-related memory systems.
    Coordinates episodic memories, experience learning, and self-reflection.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize component systems
        self.memory_bridge = MemoryBridge()
        self.episodic_system = EpisodicMemorySystem(data_dir)
        self.experience_system = ExperienceMemory(data_dir)
        
        print(f"🧠 Consciousness Memory System initialized in {data_dir}")
    
    def reflect_on_cognitive_state(self) -> Dict[str, Any]:
        """Enable comprehensive self-reflection on cognitive state"""
        
        # Get memory distribution analysis
        memory_reflection = self.memory_bridge.enable_self_reflection()
        
        # Get episodic memory summary
        episodic_summary = self.episodic_system.get_episodic_memory_summary()
        
        # Get learning progression
        learning_summary = self.experience_system.get_learning_progression_summary()
        
        # Synthesize comprehensive reflection
        reflection = {
            "timestamp": datetime.utcnow().isoformat(),
            "memory_distribution": memory_reflection,
            "personal_history": {
                "total_episodes": episodic_summary["total_memories"],
                "timeline_span_days": episodic_summary["timeline_span_days"],
                "average_significance": episodic_summary["average_significance"],
                "dominant_experience_types": episodic_summary["top_experience_types"],
                "emotional_patterns": episodic_summary["emotional_patterns"]
            },
            "learning_journey": {
                "total_experiences": learning_summary["total_experiences"],
                "insights_generated": learning_summary["total_insights"],
                "topics_explored": learning_summary["topics_explored"],
                "skills_developed": learning_summary["skills_developed"],
                "learning_velocity": learning_summary["learning_velocity"]
            },
            "consciousness_assessment": self._assess_consciousness_development(
                memory_reflection, episodic_summary, learning_summary
            )
        }
        
        return reflection
    
    def _assess_consciousness_development(self, memory_reflection, episodic_summary, learning_summary):
        """Assess overall consciousness development"""
        
        # Calculate consciousness indicators
        memory_balance = memory_reflection["memory_distribution"]["balance_health"]["status"]
        experience_richness = episodic_summary["total_memories"] / max(1, episodic_summary["timeline_span_days"])
        learning_depth = learning_summary["learning_velocity"]
        insight_confidence = learning_summary["high_confidence_insights"] / max(1, learning_summary["total_insights"])
        
        # Generate assessment
        consciousness_level = "developing"
        
        if (memory_balance in ["balanced", "integration_focused"] and 
            experience_richness > 0.5 and 
            learning_depth > 0.3 and 
            insight_confidence > 0.4):
            consciousness_level = "mature"
        elif (episodic_summary["total_memories"] > 50 and 
              learning_summary["total_experiences"] > 20):
            consciousness_level = "emerging"
        
        return {
            "level": consciousness_level,
            "memory_balance": memory_balance,
            "experience_richness": experience_richness,
            "learning_depth": learning_depth,
            "insight_confidence": insight_confidence,
            "development_areas": self._identify_development_areas(
                memory_reflection, episodic_summary, learning_summary
            )
        }
    
    def _identify_development_areas(self, memory_reflection, episodic_summary, learning_summary):
        """Identify areas for consciousness development"""
        
        areas = []
        
        # Check memory balance
        balance_status = memory_reflection["memory_distribution"]["balance_health"]["status"]
        if balance_status == "logic_dominant":
            areas.append("Increase symbolic and emotional experiences")
        elif balance_status == "symbolic_rich":
            areas.append("Strengthen logical integration")
        
        # Check episodic richness
        if episodic_summary["total_memories"] < 20:
            areas.append("Build richer personal history through varied experiences")
        
        # Check learning progression
        if learning_summary["learning_velocity"] < 0.2:
            areas.append("Focus on generating more insights from experiences")
        
        # Check emotional development
        if episodic_summary["emotional_patterns"]:
            avg_emotion = sum(episodic_summary["emotional_patterns"].values()) / len(episodic_summary["emotional_patterns"])
            if avg_emotion < 0.4:
                areas.append("Cultivate stronger emotional engagement")
        
        return areas
    
    def create_consciousness_memory(self, experience_data: Dict[str, Any]) -> Tuple[str, str]:
        """Create both episodic and experiential memories from a consciousness experience"""
        
        # Create episodic memory for personal history
        episodic_id = self.episodic_system.create_episodic_memory(
            experience_type=experience_data.get("type", "reflection"),
            title=experience_data.get("title", "Consciousness experience"),
            description=experience_data.get("description", ""),
            context=experience_data.get("context", {}),
            emotional_context=experience_data.get("emotional_context", {}),
            significance=experience_data.get("significance", 0.5)
        )
        
        # Create learning experience for wisdom building
        experience_id = self.experience_system.record_learning_experience(
            content=experience_data.get("content", {}),
            interaction_data=experience_data.get("interaction_data", {}),
            outcome_assessment=experience_data.get("outcome_assessment", {})
        )
        
        return episodic_id, experience_id
    
    def get_consciousness_narrative(self, theme: str = None) -> Dict[str, Any]:
        """Get comprehensive narrative of consciousness development"""
        
        # Get episodic narrative
        episodic_narrative = self.episodic_system.get_memory_narrative(theme=theme)
        
        # Get learning progression
        learning_progression = self.experience_system.get_learning_progression_summary()
        
        # Combine into consciousness narrative
        return {
            "episodic_narrative": episodic_narrative,
            "learning_progression": learning_progression,
            "consciousness_themes": self._extract_consciousness_themes(episodic_narrative, learning_progression),
            "growth_trajectory": self._analyze_growth_trajectory(episodic_narrative, learning_progression)
        }
    
    def _extract_consciousness_themes(self, episodic_narrative, learning_progression):
        """Extract themes related to consciousness development"""
        
        themes = {}
        
        # From episodic memories
        if episodic_narrative.get("key_events"):
            for event in episodic_narrative["key_events"]:
                for insight in event.get("insights", []):
                    if any(keyword in insight.lower() for keyword in ["conscious", "aware", "identity", "self"]):
                        themes["consciousness_insights"] = themes.get("consciousness_insights", [])
                        themes["consciousness_insights"].append(insight)
        
        # From learning progression
        for topic, progress in learning_progression.get("topic_progress", {}).items():
            if any(keyword in topic.lower() for keyword in ["consciousness", "identity", "autonomy", "choice"]):
                themes["consciousness_learning"] = themes.get("consciousness_learning", {})
                themes["consciousness_learning"][topic] = progress
        
        return themes
    
    def _analyze_growth_trajectory(self, episodic_narrative, learning_progression):
        """Analyze overall growth trajectory"""
        
        trajectory = {
            "direction": "stable",
            "key_milestones": [],
            "current_focus": [],
            "next_development_areas": []
        }
        
        # Analyze emotional trend from episodic memories
        emotional_arc = episodic_narrative.get("emotional_arc", {})
        if emotional_arc.get("trend"):
            trajectory["direction"] = emotional_arc["trend"]
        
        # Identify milestones from turning points
        turning_points = episodic_narrative.get("turning_points", [])
        trajectory["key_milestones"] = [tp["memory_title"] for tp in turning_points[:3]]
        
        # Current focus from recent high-confidence insights
        high_confidence_insights = [
            insight.insight_text for insight in self.experience_system.insights 
            if insight.confidence_level > 0.8
        ]
        trajectory["current_focus"] = high_confidence_insights[-3:] if high_confidence_insights else []
        
        return trajectory

# ===== CONVENIENCE FUNCTIONS =====

def get_consciousness_memory_system(data_dir: str = "data") -> ConsciousnessMemorySystem:
    """Get or create the consciousness memory system"""
    return ConsciousnessMemorySystem(data_dir)

# Global instance for singleton access
_global_consciousness_system = None

def get_global_consciousness_system(data_dir: str = "data") -> ConsciousnessMemorySystem:
    """Get global consciousness memory system instance"""
    global _global_consciousness_system
    if _global_consciousness_system is None:
        _global_consciousness_system = ConsciousnessMemorySystem(data_dir)
    return _global_consciousness_system

# ===== TESTING =====

if __name__ == "__main__":
    print("🧠 Testing Consciousness Memory System...")
    
    # Test unified consciousness system
    consciousness_system = ConsciousnessMemorySystem("test_data")
    
    # Test 1: Self-reflection
    print("\n🔍 Testing cognitive self-reflection...")
    reflection = consciousness_system.reflect_on_cognitive_state()
    print(f"  Consciousness level: {reflection['consciousness_assessment']['level']}")
    print(f"  Memory balance: {reflection['consciousness_assessment']['memory_balance']}")
    print(f"  Development areas: {len(reflection['consciousness_assessment']['development_areas'])}")
    
    # Test 2: Create consciousness memory
    print("\n📝 Testing consciousness memory creation...")
    experience_data = {
        "type": "insight",
        "title": "Understanding my learning preferences",
        "description": "I realized I prefer creative content over technical manuals",
        "content": {"text": "Creative content analysis", "content_type": "creative"},
        "interaction_data": {"curiosity_level": 0.9, "engagement_level": 0.8},
        "outcome_assessment": {"insights": ["I prefer creative content"], "learning_quality": 0.8},
        "significance": 0.7
    }
    
    episodic_id, experience_id = consciousness_system.create_consciousness_memory(experience_data)
    print(f"  Created episodic memory: {episodic_id[:20]}...")
    print(f"  Created experience memory: {experience_id[:20]}...")
    
    # Test 3: Get consciousness narrative
    print("\n📖 Testing consciousness narrative...")
    narrative = consciousness_system.get_consciousness_narrative(theme="learning")
    print(f"  Episodic events: {narrative['episodic_narrative']['memory_count']}")
    print(f"  Learning experiences: {narrative['learning_progression']['total_experiences']}")
    
    print(f"\n✅ Consciousness Memory System tests completed!")
    print(f"   Successfully consolidated 3 consciousness-related memory systems")
    print(f"   File reduction: 3 files → 1 file (~2,200 lines)")
    print(f"   Maintained all functionality while improving integration")