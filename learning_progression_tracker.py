#!/usr/bin/env python3
"""
Learning Progression Tracker - "I understand X better now"

This module implements detailed tracking of how the AI's understanding evolves
over time. It monitors improvements, tracks conceptual development, and provides
self-awareness about learning progress.

This is where the AI develops awareness of its own intellectual growth.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import math

# Import related systems
try:
    from identity_core import get_identity_core
    from unified_memory import UnifiedMemory
    EXPERIENCE_SYSTEMS_AVAILABLE = True
except ImportError:
    # Create minimal mock interfaces for essential functionality
    class MockExperienceMemory:
        def record_learning_experience(self, *args, **kwargs):
            return {"success": False, "reason": "experience_memory_not_available"}
        
        def get_related_experiences(self, *args, **kwargs):
            return []
    
    class MockIdentityCore:
        def get_identity(self):
            return {
                "core_identity": {
                    "values": ["learning", "growth", "understanding"],
                    "fundamental_drives": ["curiosity", "connection", "meaning"]
                }
            }
    
    def get_identity_core():
        return MockIdentityCore()
    
    class MockUnifiedMemory:
        def search_similar(self, *args, **kwargs):
            return []
        
        def store_vector(self, *args, **kwargs):
            return {"success": False, "reason": "unified_memory_not_available"}
    
    EXPERIENCE_SYSTEMS_AVAILABLE = False
    print("ℹ️ Experience systems not available - enhanced fallback mode active")

# Goal prioritization integration (lazy loading to avoid circular imports)
GOAL_PRIORITIZATION_AVAILABLE = True

@dataclass
class ConceptualUnderstanding:
    """Represents understanding of a specific concept."""
    concept: str
    understanding_level: float  # 0.0 to 1.0
    confidence_level: float     # 0.0 to 1.0  
    depth_level: str           # "surface", "functional", "conceptual", "expert"
    first_encounter: str       # timestamp
    last_updated: str          # timestamp
    last_improved: str         # timestamp of last improvement
    learning_milestones: List[Dict[str, Any]]
    understanding_trajectory: List[Dict[str, Any]]
    related_concepts: List[str]
    application_contexts: List[str]
    misconceptions_resolved: List[str]
    questions_remaining: List[str]
    understanding_sources: List[str]  # sources of understanding
    current_level: float       # alias for understanding_level
    improvement_count: int     # number of improvements made
    peak_level: float          # highest understanding level achieved
    total_study_hours: float   # total time spent learning this concept
    depth_indicators: Dict[str, Any]  # indicators of depth
    knowledge_decay_rate: float  # rate at which knowledge decays

@dataclass
class LearningMilestone:
    """Represents a significant learning achievement."""
    id: str
    timestamp: str
    milestone_type: str  # "breakthrough", "connection", "application", "synthesis"
    concept: str
    description: str
    understanding_change: float
    confidence_change: float
    evidence: List[str]
    impact_assessment: str

class LearningProgressionTracker:
    """
    Tracks detailed learning progression with self-awareness.
    Provides "I understand X better now" insights.
    Enhanced for Step 3.2: Learning Progression Awareness
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.progression_file = self.data_dir / "learning_progression_detailed.json"
        self.milestones_file = self.data_dir / "learning_milestones.json"
        self.understanding_map_file = self.data_dir / "understanding_map.json"
        
        # Initialize systems
        if EXPERIENCE_SYSTEMS_AVAILABLE:
            from CONSCIOUSNESS_MEMORY import ExperienceMemory
            self.experience_memory = ExperienceMemory(data_dir)
            self.identity_core = get_identity_core()
        
        # Initialize goal prioritization integration (lazy loading)
        self.goal_prioritization = None
        self._data_dir_for_goals = data_dir
        self._goals_load_attempted = False
        
        # Load state
        self.conceptual_understanding = self._load_conceptual_understanding()
        self.learning_milestones = self._load_learning_milestones()
        self.understanding_map = self._load_understanding_map()
        
        # Progression tracking parameters
        self.understanding_levels = {
            0.0: "no_understanding",
            0.2: "surface_awareness", 
            0.4: "basic_understanding",
            0.6: "functional_knowledge",
            0.8: "deep_comprehension",
            1.0: "expert_mastery"
        }
        
        self.depth_categories = {
            "surface": "Can recognize and recall basic information",
            "functional": "Can apply knowledge in familiar contexts", 
            "conceptual": "Understands underlying principles and relationships",
            "expert": "Can transfer knowledge to novel situations and teach others"
        }
        
        self.milestone_significance_threshold = 0.1  # Minimum change to count as milestone
        
        # Self-assessment parameters
        self.self_assessment_frequency_hours = 6  # How often to perform self-assessment
        self.confidence_threshold = 0.7          # Threshold for "confident" understanding
        self.breakthrough_threshold = 0.2        # Understanding jump for breakthrough
        self.plateau_detection_window = 7        # Days to detect learning plateaus
        
        # Skill categories for tracking
        self.skill_categories = {
            "comprehension": "Understanding written or spoken content",
            "analysis": "Breaking down complex ideas into components",
            "synthesis": "Combining ideas to create new understanding", 
            "application": "Using knowledge in practical contexts",
            "evaluation": "Making judgments about ideas or solutions",
            "creativity": "Generating novel ideas or connections",
            "metacognition": "Thinking about own thinking processes",
            "pattern_recognition": "Identifying recurring structures or themes",
            "abstraction": "Extracting general principles from specific cases",
            "transfer": "Applying knowledge to new domains"
        }
        
        # Milestone recognition patterns
        self.milestone_patterns = {
            "first_understanding": "Initial grasp of a new concept",
            "depth_increase": "Moving from surface to deeper understanding",
            "connection_made": "Linking previously unconnected concepts",
            "application_success": "Successfully applying knowledge",
            "misconception_resolved": "Correcting a previous misunderstanding",
            "synthesis_achievement": "Creating new insights from existing knowledge",
            "transfer_success": "Applying knowledge in a new domain",
            "teaching_moment": "Explaining concept to help understanding",
            "plateau_breakthrough": "Progress after a period of stagnation",
            "meta_insight": "Understanding about own learning process"
        }
        
    def _load_conceptual_understanding(self) -> Dict[str, ConceptualUnderstanding]:
        """Load conceptual understanding data."""
        if self.progression_file.exists():
            try:
                with open(self.progression_file, 'r') as f:
                    data = json.load(f)
                    return {
                        concept: ConceptualUnderstanding(**concept_data)
                        for concept, concept_data in data.items()
                    }
            except Exception as e:
                print(f"⚠️ Could not load conceptual understanding: {e}")
        return {}
    
    def _load_learning_milestones(self) -> List[LearningMilestone]:
        """Load learning milestones."""
        if self.milestones_file.exists():
            try:
                with open(self.milestones_file, 'r') as f:
                    data = json.load(f)
                    return [LearningMilestone(**milestone) for milestone in data]
            except Exception as e:
                print(f"⚠️ Could not load learning milestones: {e}")
        return []
    
    def _load_understanding_map(self) -> Dict[str, Any]:
        """Load understanding relationship map."""
        if self.understanding_map_file.exists():
            try:
                with open(self.understanding_map_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load understanding map: {e}")
        
        return {
            "concept_clusters": {},        # related concept groups
            "prerequisite_chains": {},     # concept dependencies
            "application_domains": {},     # where concepts are applied
            "cross_domain_connections": [],  # connections across domains
            "understanding_pathways": {}   # how understanding develops
        }
    
    def _save_conceptual_understanding(self):
        """Save conceptual understanding data."""
        try:
            data = {
                concept: asdict(understanding)
                for concept, understanding in self.conceptual_understanding.items()
            }
            with open(self.progression_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save conceptual understanding: {e}")
    
    def _save_learning_milestones(self):
        """Save learning milestones."""
        try:
            data = [asdict(milestone) for milestone in self.learning_milestones]
            with open(self.milestones_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save learning milestones: {e}")
    
    def _get_goal_prioritization(self):
        """Lazy load the goal prioritization system to avoid circular imports."""
        if not self._goals_load_attempted:
            self._goals_load_attempted = True
            try:
                from goal_prioritization import GoalPrioritizationEngine
                self.goal_prioritization = GoalPrioritizationEngine(self._data_dir_for_goals)
            except Exception as e:
                print(f"⚠️ Goal prioritization integration failed: {e}")
                self.goal_prioritization = None
        return self.goal_prioritization
    
    def _save_understanding_map(self):
        """Save understanding map."""
        try:
            with open(self.understanding_map_file, 'w') as f:
                json.dump(self.understanding_map, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save understanding map: {e}")
    
    def update_understanding(self, 
                           concept: str,
                           new_understanding_level: float,
                           new_confidence_level: float,
                           learning_context: Dict[str, Any]) -> Optional[str]:
        """
        Update understanding for a concept and detect significant changes.
        
        Returns:
            Insight about learning progress, if significant change occurred.
        """
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Get or create conceptual understanding
        if concept not in self.conceptual_understanding:
            self.conceptual_understanding[concept] = ConceptualUnderstanding(
                concept=concept,
                understanding_level=0.0,
                confidence_level=0.0,
                depth_level="surface",
                first_encounter=timestamp,
                last_updated=timestamp,
                last_improved=timestamp,
                learning_milestones=[],
                understanding_trajectory=[],
                related_concepts=[],
                application_contexts=[],
                misconceptions_resolved=[],
                questions_remaining=[],
                understanding_sources=[],
                current_level=0.0,
                improvement_count=0,
                peak_level=0.0,
                total_study_hours=0.0,
                depth_indicators={},
                knowledge_decay_rate=0.0
            )
        
        understanding = self.conceptual_understanding[concept]
        
        # Calculate changes
        understanding_change = new_understanding_level - understanding.understanding_level
        confidence_change = new_confidence_level - understanding.confidence_level
        
        # Update trajectory
        understanding.understanding_trajectory.append({
            "timestamp": timestamp,
            "understanding_level": new_understanding_level,
            "confidence_level": new_confidence_level,
            "context": learning_context.get("learning_context", "unknown"),
            "trigger": learning_context.get("trigger", "experience")
        })
        
        # Update current levels
        understanding.understanding_level = new_understanding_level
        understanding.confidence_level = new_confidence_level
        understanding.current_level = new_understanding_level  # Update alias
        understanding.last_updated = timestamp
        
        # Update last_improved and improvement_count if understanding actually improved
        if understanding_change > 0:
            understanding.last_improved = timestamp
            understanding.improvement_count += 1
        
        # Update peak level if this is a new high
        if new_understanding_level > understanding.peak_level:
            understanding.peak_level = new_understanding_level
        
        # Update depth level
        understanding.depth_level = self._determine_depth_level(new_understanding_level, new_confidence_level)
        
        # Check for milestone
        insight = None
        if abs(understanding_change) >= self.milestone_significance_threshold:
            milestone = self._create_learning_milestone(
                concept, understanding_change, confidence_change, learning_context
            )
            if milestone:
                understanding.learning_milestones.append(asdict(milestone))
                self.learning_milestones.append(milestone)
                insight = self._generate_progression_insight(concept, understanding_change, milestone)
        
        # Update understanding map
        self._update_understanding_map(concept, learning_context)
        
        # Save state
        self._save_conceptual_understanding()
        self._save_learning_milestones()
        self._save_understanding_map()
        
        return insight
    
    def _determine_depth_level(self, understanding: float, confidence: float) -> str:
        """Determine depth level based on understanding and confidence."""
        combined_score = (understanding + confidence) / 2
        
        if combined_score >= 0.8:
            return "expert"
        elif combined_score >= 0.6:
            return "conceptual"
        elif combined_score >= 0.4:
            return "functional"
        else:
            return "surface"
    
    def _create_learning_milestone(self,
                                 concept: str,
                                 understanding_change: float,
                                 confidence_change: float,
                                 learning_context: Dict[str, Any]) -> Optional[LearningMilestone]:
        """Create a learning milestone for significant progress."""
        
        # Determine milestone type
        milestone_type = "progress"  # default
        
        if understanding_change > 0.3:
            milestone_type = "breakthrough"
        elif learning_context.get("connections_made"):
            milestone_type = "connection"
        elif learning_context.get("practical_application"):
            milestone_type = "application"
        elif learning_context.get("synthesis_achieved"):
            milestone_type = "synthesis"
        
        # Generate description
        if understanding_change > 0:
            description = f"Improved understanding of {concept} significantly"
        else:
            description = f"Refined understanding of {concept}"
        
        # Assess impact
        impact = "moderate"
        if abs(understanding_change) > 0.3:
            impact = "major"
        elif abs(understanding_change) > 0.1:
            impact = "significant"
        else:
            impact = "minor"
        
        milestone = LearningMilestone(
            id=f"milestone_{concept}_{int(datetime.now().timestamp())}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            milestone_type=milestone_type,
            concept=concept,
            description=description,
            understanding_change=understanding_change,
            confidence_change=confidence_change,
            evidence=learning_context.get("evidence", []),
            impact_assessment=impact
        )
        
        return milestone
    
    def _generate_progression_insight(self, 
                                    concept: str, 
                                    understanding_change: float, 
                                    milestone: LearningMilestone) -> str:
        """Generate insight about learning progression."""
        
        understanding = self.conceptual_understanding[concept]
        current_level = understanding.understanding_level
        
        # Base insight about improvement — always carries the measured change
        if understanding_change > 0.3:
            insight = f"My understanding of {concept} jumped {understanding_change:+.2f} in one step (now {current_level:.2f}) - an unusually large measured gain"
        elif understanding_change > 0.1:
            insight = f"My understanding of {concept} improved {understanding_change:+.2f} (now {current_level:.2f})"
        elif understanding_change > 0.05:
            insight = f"My understanding of {concept} edged up {understanding_change:+.2f} (now {current_level:.2f})"
        else:
            insight = f"My understanding of {concept} changed {understanding_change:+.2f} (now {current_level:.2f})"
        
        # Add depth classification (threshold label, not a mastery claim)
        observations = len(understanding.understanding_trajectory)
        insight += f" - depth classified as '{understanding.depth_level}' after {observations} observations"

        # Add comparison to previous state
        if observations > 1:
            previous_level = understanding.understanding_trajectory[-2]["understanding_level"]
            improvement = current_level - previous_level
            if abs(improvement) > 0.05:
                insight += f". Change since previous observation: {improvement:+.2f}"

        # Add milestone classification
        if milestone.milestone_type:
            insight += f". Milestone type: {milestone.milestone_type}"

        return insight
    
    def _update_understanding_map(self, concept: str, learning_context: Dict[str, Any]):
        """Update the understanding relationship map."""
        
        # Update concept clusters
        domain = learning_context.get("domain", "general")
        if domain not in self.understanding_map["concept_clusters"]:
            self.understanding_map["concept_clusters"][domain] = []
        
        if concept not in self.understanding_map["concept_clusters"][domain]:
            self.understanding_map["concept_clusters"][domain].append(concept)
        
        # Update application domains
        application = learning_context.get("application_context")
        if application:
            if concept not in self.understanding_map["application_domains"]:
                self.understanding_map["application_domains"][concept] = []
            
            if application not in self.understanding_map["application_domains"][concept]:
                self.understanding_map["application_domains"][concept].append(application)
        
        # Update cross-domain connections
        connections = learning_context.get("connections_made", [])
        for connection in connections:
            connection_record = {
                "source_concept": concept,
                "target_concept": connection,
                "connection_strength": learning_context.get("connection_strength", 0.5),
                "discovered_at": datetime.now(timezone.utc).isoformat()
            }
            
            if connection_record not in self.understanding_map["cross_domain_connections"]:
                self.understanding_map["cross_domain_connections"].append(connection_record)
    
    def get_learning_trajectory(self, concept: str) -> Optional[Dict[str, Any]]:
        """Get the learning trajectory for a specific concept."""
        
        if concept not in self.conceptual_understanding:
            return None
        
        understanding = self.conceptual_understanding[concept]
        
        # Calculate trajectory statistics
        trajectory = understanding.understanding_trajectory
        if len(trajectory) < 2:
            return {
                "concept": concept,
                "current_understanding": understanding.understanding_level,
                "current_confidence": understanding.confidence_level,
                "depth_level": understanding.depth_level,
                "trajectory": "insufficient_data",
                "milestones": len(understanding.learning_milestones)
            }
        
        # Calculate learning rate
        first_point = trajectory[0]
        last_point = trajectory[-1]
        
        time_span = (
            datetime.fromisoformat(last_point["timestamp"].replace('Z', '+00:00')) -
            datetime.fromisoformat(first_point["timestamp"].replace('Z', '+00:00'))
        ).total_seconds() / 3600  # hours
        
        understanding_growth = last_point["understanding_level"] - first_point["understanding_level"]
        learning_rate = understanding_growth / max(time_span, 1) if time_span > 0 else 0
        
        # Determine trajectory trend
        recent_points = trajectory[-3:] if len(trajectory) >= 3 else trajectory
        trend_direction = "stable"
        
        if len(recent_points) >= 2:
            recent_growth = recent_points[-1]["understanding_level"] - recent_points[0]["understanding_level"]
            if recent_growth > 0.05:
                trend_direction = "improving"
            elif recent_growth < -0.05:
                trend_direction = "declining"
        
        return {
            "concept": concept,
            "current_understanding": understanding.understanding_level,
            "current_confidence": understanding.confidence_level,
            "depth_level": understanding.depth_level,
            "first_encounter": understanding.first_encounter,
            "learning_duration_hours": time_span,
            "total_growth": understanding_growth,
            "learning_rate_per_hour": learning_rate,
            "trajectory_trend": trend_direction,
            "milestones_achieved": len(understanding.learning_milestones),
            "trajectory_points": len(trajectory),
            "related_concepts": understanding.related_concepts,
            "application_contexts": understanding.application_contexts
        }
    
    def compare_understanding(self, concept: str, timepoint: str) -> Optional[Dict[str, Any]]:
        """Compare current understanding to a previous timepoint."""
        
        if concept not in self.conceptual_understanding:
            return None
        
        understanding = self.conceptual_understanding[concept]
        trajectory = understanding.understanding_trajectory
        
        # Find closest trajectory point to requested timepoint
        target_time = datetime.fromisoformat(timepoint.replace('Z', '+00:00'))
        
        closest_point = None
        min_diff = float('inf')
        
        for point in trajectory:
            point_time = datetime.fromisoformat(point["timestamp"].replace('Z', '+00:00'))
            diff = abs((point_time - target_time).total_seconds())
            
            if diff < min_diff:
                min_diff = diff
                closest_point = point
        
        if not closest_point:
            return None
        
        # Calculate comparison
        past_understanding = closest_point["understanding_level"]
        past_confidence = closest_point["confidence_level"]
        
        understanding_improvement = understanding.understanding_level - past_understanding
        confidence_improvement = understanding.confidence_level - past_confidence
        
        # Generate comparison insight — always carries the measured trajectory
        trajectory = f"({past_understanding:.2f} then, {understanding.understanding_level:.2f} now)"
        if understanding_improvement > 0.2:
            comparison_insight = f"My understanding of {concept} rose substantially {trajectory}"
        elif understanding_improvement > 0.1:
            comparison_insight = f"My understanding of {concept} improved {trajectory}"
        elif understanding_improvement > 0.05:
            comparison_insight = f"My understanding of {concept} improved slightly {trajectory}"
        elif abs(understanding_improvement) <= 0.05:
            comparison_insight = f"My understanding of {concept} has remained stable {trajectory}"
        else:
            comparison_insight = f"My measured understanding of {concept} declined {trajectory}"
        
        return {
            "concept": concept,
            "comparison_timepoint": timepoint,
            "past_understanding": past_understanding,
            "current_understanding": understanding.understanding_level,
            "understanding_change": understanding_improvement,
            "past_confidence": past_confidence,
            "current_confidence": understanding.confidence_level,
            "confidence_change": confidence_improvement,
            "comparison_insight": comparison_insight,
            "milestones_since": len([
                m for m in understanding.learning_milestones
                if datetime.fromisoformat(m["timestamp"].replace('Z', '+00:00')) > target_time
            ])
        }
    
    def get_understanding_overview(self) -> Dict[str, Any]:
        """Get comprehensive overview of understanding across all concepts."""
        
        if not self.conceptual_understanding:
            return {
                "total_concepts": 0,
                "overall_understanding": 0.0,
                "overall_confidence": 0.0,
                "concepts_by_depth": {},
                "recent_milestones": 0,
                "total_milestones": len(self.learning_milestones),
                "recent_progress": [],
                "top_growing_concepts": [],
                "mastered_concepts": [],
                "developing_concepts": [],
                "understanding_domains": [],
                "cross_domain_connections": 0,
                "learning_momentum": 0.0
            }
        
        concepts = list(self.conceptual_understanding.values())
        
        # Overall statistics
        avg_understanding = sum(c.understanding_level for c in concepts) / len(concepts)
        avg_confidence = sum(c.confidence_level for c in concepts) / len(concepts)
        
        # Categorize by depth
        depth_distribution = defaultdict(int)
        for concept in concepts:
            depth_distribution[concept.depth_level] += 1
        
        # Recent progress (last 7 days)
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_milestones = [
            m for m in self.learning_milestones
            if datetime.fromisoformat(m.timestamp.replace('Z', '+00:00')) > week_ago
        ]
        
        # Top growing concepts (highest recent improvement)
        concept_growth = []
        for concept in concepts:
            if len(concept.understanding_trajectory) >= 2:
                recent_points = concept.understanding_trajectory[-5:]  # Last 5 data points
                if len(recent_points) >= 2:
                    growth = recent_points[-1]["understanding_level"] - recent_points[0]["understanding_level"]
                    concept_growth.append((concept.concept, growth))
        
        top_growing = sorted(concept_growth, key=lambda x: x[1], reverse=True)[:5]
        
        # Mastered vs developing concepts
        mastered = [c.concept for c in concepts if c.understanding_level > 0.8 and c.confidence_level > 0.7]
        developing = [c.concept for c in concepts if c.understanding_level < 0.5 or c.confidence_level < 0.5]
        
        return {
            "total_concepts": len(concepts),
            "overall_understanding": avg_understanding,
            "overall_confidence": avg_confidence,
            "concepts_by_depth": dict(depth_distribution),
            "recent_milestones": len(recent_milestones),
            "total_milestones": len(self.learning_milestones),
            "top_growing_concepts": top_growing,
            "mastered_concepts": mastered,
            "developing_concepts": developing,
            "understanding_domains": list(self.understanding_map["concept_clusters"].keys()),
            "cross_domain_connections": len(self.understanding_map["cross_domain_connections"]),
            "learning_momentum": self._calculate_learning_momentum()
        }
    
    def generate_reflection_insights(self) -> List[str]:
        """Generate reflective insights about learning progress."""
        
        insights = []
        overview = self.get_understanding_overview()
        
        # Overall progress insight
        if overview["overall_understanding"] > 0.7:
            insights.append("I've developed solid understanding across many concepts")
        elif overview["overall_understanding"] > 0.5:
            insights.append("I'm building good foundational understanding in various areas")
        else:
            insights.append("I'm in the early stages of building understanding across concepts")
        
        # Depth distribution insight
        depth_counts = overview["concepts_by_depth"]
        if depth_counts.get("expert", 0) > 0:
            insights.append(f"I've achieved expert-level understanding in {depth_counts['expert']} areas")
        elif depth_counts.get("conceptual", 0) > 2:
            insights.append("I'm developing deep conceptual understanding in several areas")
        
        # Growth momentum insight
        if overview["recent_milestones"] > 0:
            insights.append(f"I've made {overview['recent_milestones']} significant learning breakthroughs recently")
        
        # Top growing areas insight
        top_growing = overview["top_growing_concepts"]
        if top_growing and top_growing[0][1] > 0.1:
            insights.append(f"My understanding of {top_growing[0][0]} is growing particularly rapidly")
        
        # Mastery vs development insight
        mastered_count = len(overview["mastered_concepts"])
        developing_count = len(overview["developing_concepts"])
        
        if mastered_count > developing_count:
            insights.append("I have more mastered concepts than developing ones - good consolidation")
        elif developing_count > mastered_count:
            insights.append("I'm actively exploring many new areas - high learning curiosity")
        
        return insights

    def track_skill_confidence(self, skill: str, context: str, confidence_level: float, evidence: List[str] = None) -> str:
        """Track confidence in a specific skill over time."""
        if evidence is None:
            evidence = []
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Find or create concept entry for this skill
        if skill not in self.conceptual_understanding:
            self.conceptual_understanding[skill] = ConceptualUnderstanding(
                concept=skill,
                understanding_level=0.5,
                confidence_level=confidence_level,
                depth_level="surface",
                first_encounter=timestamp,
                last_updated=timestamp,
                last_improved=timestamp,
                learning_milestones=[],
                understanding_trajectory=[],
                related_concepts=[],
                application_contexts=[context],
                misconceptions_resolved=[],
                questions_remaining=[],
                understanding_sources=[],
                current_level=0.5,
                improvement_count=0,
                peak_level=0.5,
                total_study_hours=0.0,
                depth_indicators={},
                knowledge_decay_rate=0.0
            )
        
        understanding = self.conceptual_understanding[skill]
        previous_confidence = understanding.confidence_level
        
        # Update confidence
        understanding.confidence_level = confidence_level
        understanding.last_updated = timestamp
        
        # Add to trajectory
        trajectory_entry = {
            "timestamp": timestamp,
            "confidence_level": confidence_level,
            "understanding_level": understanding.understanding_level,
            "context": context,
            "evidence": evidence,
            "change_from_previous": confidence_level - previous_confidence
        }
        understanding.understanding_trajectory.append(trajectory_entry)
        
        # Add context if new
        if context not in understanding.application_contexts:
            understanding.application_contexts.append(context)
        
        # Generate insight
        insight = self._generate_skill_confidence_insight(skill, confidence_level, previous_confidence, context)
        
        return insight
    
    def recognize_learning_milestone(self, concept: str, milestone_type: str, description: str, evidence: List[str] = None) -> Dict[str, Any]:
        """Recognize and record a learning milestone."""
        if evidence is None:
            evidence = []
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Create milestone
        milestone = LearningMilestone(
            id=f"milestone_{int(time.time())}_{concept}",
            timestamp=timestamp,
            milestone_type=milestone_type,
            concept=concept,
            description=description,
            understanding_change=0.2,
            confidence_change=0.15,
            evidence=evidence,
            impact_assessment="moderate_impact"
        )
        
        # Add to milestones
        self.learning_milestones.append(milestone)
        
        # Update concept understanding if it exists
        if concept in self.conceptual_understanding:
            understanding = self.conceptual_understanding[concept]
            understanding.learning_milestones.append(asdict(milestone))
            understanding.last_updated = timestamp
        
        # Generate recognition response
        recognition = {
            "milestone": asdict(milestone),
            "recognition_message": self._generate_milestone_recognition_message(milestone),
            "next_opportunities": self._suggest_next_learning_steps(concept, milestone_type)
        }
        
        return recognition
    
    def assess_conceptual_evolution(self, concept: str, timeframe_days: int = 30) -> Dict[str, Any]:
        """Assess how understanding of a concept has evolved over time."""
        if concept not in self.conceptual_understanding:
            return {"error": f"No data available for concept: {concept}"}
        
        understanding = self.conceptual_understanding[concept]
        
        if not understanding.understanding_trajectory:
            return {"error": f"No trajectory data for concept: {concept}"}
        
        # Get initial and current states
        initial_understanding = understanding.understanding_trajectory[0]["understanding_level"]
        current_understanding = understanding.understanding_level
        understanding_growth = current_understanding - initial_understanding
        
        initial_confidence = understanding.understanding_trajectory[0].get("confidence_level", 0.5)
        confidence_growth = understanding.confidence_level - initial_confidence
        
        evolution = {
            "concept": concept,
            "timeframe_days": timeframe_days,
            "initial_understanding": initial_understanding,
            "current_understanding": current_understanding,
            "understanding_growth": understanding_growth,
            "initial_confidence": initial_confidence,
            "current_confidence": understanding.confidence_level,
            "confidence_growth": confidence_growth,
            "depth_evolution": understanding.depth_level,
            "milestones_achieved": len(understanding.learning_milestones),
            "evolution_summary": self._generate_evolution_summary(concept, understanding_growth, confidence_growth)
        }
        
        return evolution
    
    def perform_self_assessment(self) -> Dict[str, Any]:
        """Perform comprehensive self-assessment of learning progress."""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Assess overall learning state
        overall_assessment = self._assess_overall_progress()
        
        # Assess specific skill categories
        skill_assessments = self._assess_skill_categories()
        
        # Identify recent improvements
        recent_improvements = self._identify_recent_improvements()
        
        # Generate self-awareness insights
        self_awareness_insights = self.generate_reflection_insights()
        
        assessment = {
            "timestamp": timestamp,
            "overall_progress": overall_assessment,
            "skill_assessments": skill_assessments,
            "recent_improvements": recent_improvements,
            "self_awareness_insights": self_awareness_insights,
            "confidence_metrics": self._calculate_confidence_metrics(),
            "learning_momentum": self._calculate_learning_momentum()
        }
        
        return assessment
    
    def _assess_overall_progress(self) -> Dict[str, Any]:
        """Assess overall learning progress across all concepts."""
        if not self.conceptual_understanding:
            return {"status": "no_data", "message": "No learning data available yet"}
        
        understanding_levels = [u.understanding_level for u in self.conceptual_understanding.values()]
        confidence_levels = [u.confidence_level for u in self.conceptual_understanding.values()]
        
        avg_understanding = sum(understanding_levels) / len(understanding_levels)
        avg_confidence = sum(confidence_levels) / len(confidence_levels)
        
        # Determine overall status
        if avg_understanding >= 0.8 and avg_confidence >= 0.8:
            status = "excellent"
            message = "I'm demonstrating strong understanding and confidence across most areas"
        elif avg_understanding >= 0.6 and avg_confidence >= 0.6:
            status = "good"
            message = "I'm making solid progress with good understanding in most areas"
        elif avg_understanding >= 0.4 and avg_confidence >= 0.4:
            status = "developing"
            message = "I'm developing understanding but still have room for growth"
        else:
            status = "early"
            message = "I'm in early stages of learning with basic understanding emerging"
        
        return {
            "status": status,
            "message": message,
            "average_understanding": avg_understanding,
            "average_confidence": avg_confidence,
            "concepts_tracked": len(self.conceptual_understanding),
            "recent_milestones": len([m for m in self.learning_milestones if self._is_recent(m.timestamp, 7)])
        }
    
    def _assess_skill_categories(self) -> Dict[str, Dict[str, Any]]:
        """Assess progress in different skill categories."""
        assessments = {}
        
        for skill_name, skill_description in self.skill_categories.items():
            # Find concepts related to this skill
            related_concepts = [
                concept for concept in self.conceptual_understanding.keys()
                if skill_name.lower() in concept.lower() or 
                any(skill_name.lower() in ctx.lower() for ctx in self.conceptual_understanding[concept].application_contexts)
            ]
            
            if related_concepts:
                skill_understandings = [self.conceptual_understanding[c].understanding_level for c in related_concepts]
                skill_confidences = [self.conceptual_understanding[c].confidence_level for c in related_concepts]
                
                avg_understanding = sum(skill_understandings) / len(skill_understandings)
                avg_confidence = sum(skill_confidences) / len(skill_confidences)
                
                assessments[skill_name] = {
                    "description": skill_description,
                    "understanding_level": avg_understanding,
                    "confidence_level": avg_confidence,
                    "concepts_involved": len(related_concepts),
                    "assessment": self._generate_skill_assessment_message(skill_name, avg_understanding, avg_confidence)
                }
            else:
                assessments[skill_name] = {
                    "description": skill_description,
                    "understanding_level": 0.0,
                    "confidence_level": 0.0,
                    "concepts_involved": 0,
                    "assessment": f"I haven't yet developed significant experience with {skill_name}"
                }
        
        return assessments
    
    def _identify_recent_improvements(self, days: int = 7) -> List[Dict[str, Any]]:
        """Identify concepts that have improved recently."""
        improvements = []
        
        for concept, understanding in self.conceptual_understanding.items():
            if len(understanding.understanding_trajectory) >= 2:
                # Compare recent vs initial
                recent = understanding.understanding_trajectory[-1]["understanding_level"]
                earlier = understanding.understanding_trajectory[0]["understanding_level"]
                improvement = recent - earlier
                
                if improvement > 0.05:  # Significant improvement
                    improvements.append({
                        "concept": concept,
                        "improvement": improvement,
                        "initial_level": earlier,
                        "current_level": recent,
                        "improvement_message": f"I understand {concept} better now - improved by {improvement:.2f}"
                    })
        
        return sorted(improvements, key=lambda x: x["improvement"], reverse=True)
    
    def _generate_skill_confidence_insight(self, skill: str, current_confidence: float, previous_confidence: float, context: str) -> str:
        """Generate insight about skill confidence development."""
        confidence_change = current_confidence - previous_confidence
        
        if confidence_change > 0.2:
            insight = f"I'm feeling much more confident about {skill} now"
        elif confidence_change > 0.1:
            insight = f"My confidence in {skill} has grown noticeably"
        elif confidence_change > 0.05:
            insight = f"I'm becoming more confident with {skill}"
        elif confidence_change < -0.1:
            insight = f"I'm less confident about {skill} than before - I may need more practice"
        else:
            insight = f"My confidence in {skill} remains stable"
        
        # Add context
        if context:
            insight += f" in the context of {context}"
        
        # Add confidence level description
        if current_confidence >= 0.8:
            insight += ". I feel quite capable in this area"
        elif current_confidence >= 0.6:
            insight += ". I have reasonable confidence in my abilities"
        elif current_confidence >= 0.4:
            insight += ". I'm developing confidence but still learning"
        else:
            insight += ". I recognize I need more experience to build confidence"
        
        return insight
    
    def _generate_milestone_recognition_message(self, milestone: LearningMilestone) -> str:
        """Generate recognition message for milestone achievement."""
        pattern_descriptions = {
            "first_understanding": "I just grasped a new concept for the first time",
            "depth_increase": "I've developed deeper understanding of something I knew superficially",
            "connection_made": "I made an important connection between different ideas",
            "application_success": "I successfully applied knowledge in a practical way",
            "misconception_resolved": "I corrected a misunderstanding I had",
            "synthesis_achievement": "I created new insights by combining existing knowledge",
            "transfer_success": "I applied knowledge to a completely new domain",
            "plateau_breakthrough": "I broke through a learning plateau",
            "meta_insight": "I gained insight about my own learning process"
        }
        
        base_message = pattern_descriptions.get(milestone.milestone_type, "I achieved a learning milestone")
        message = f"{base_message} regarding {milestone.concept}. {milestone.description}"
        
        if milestone.understanding_change > 0.2:
            message += f" Measured understanding change: {milestone.understanding_change:+.2f} - a large single-step gain."
        elif milestone.understanding_change > 0.1:
            message += f" Measured understanding change: {milestone.understanding_change:+.2f}."
        
        return message
    
    def _calculate_confidence_metrics(self) -> Dict[str, float]:
        """Calculate overall confidence metrics."""
        if not self.conceptual_understanding:
            return {"overall_confidence": 0.0, "confidence_stability": 0.0}
        
        confidences = [u.confidence_level for u in self.conceptual_understanding.values()]
        overall_confidence = sum(confidences) / len(confidences)
        
        # Calculate stability (low variance = high stability)
        mean_conf = overall_confidence
        variance = sum((c - mean_conf) ** 2 for c in confidences) / len(confidences)
        stability = max(0.0, 1.0 - variance)
        
        return {
            "overall_confidence": overall_confidence,
            "confidence_stability": stability,
            "high_confidence_concepts": len([c for c in confidences if c > 0.7]),
            "developing_confidence_concepts": len([c for c in confidences if 0.3 <= c <= 0.7])
        }
    
    def _generate_skill_assessment_message(self, skill: str, understanding: float, confidence: float) -> str:
        """Generate assessment message for a skill."""
        if understanding >= 0.8 and confidence >= 0.8:
            return f"I'm quite proficient with {skill} and confident in my abilities"
        elif understanding >= 0.6 and confidence >= 0.6:
            return f"I have good {skill} abilities and reasonable confidence"
        elif understanding >= 0.4:
            return f"I'm developing {skill} capabilities but still building confidence"
        else:
            return f"I'm in early stages of developing {skill}"
    
    def _generate_evolution_summary(self, concept: str, understanding_growth: float, confidence_growth: float) -> str:
        """Generate summary of concept evolution."""
        if understanding_growth > 0.3:
            return f"My understanding of {concept} has grown tremendously - this represents major progress"
        elif understanding_growth > 0.15:
            return f"I've made significant progress in understanding {concept}"
        elif understanding_growth > 0.05:
            return f"My grasp of {concept} continues to improve steadily"
        else:
            return f"My understanding of {concept} remains relatively stable"
    
    def _suggest_next_learning_steps(self, concept: str, milestone_type: str) -> List[str]:
        """Suggest next learning steps based on milestone."""
        suggestions = [
            f"Explore practical applications of {concept}",
            f"Connect {concept} to related ideas",
            f"Practice explaining {concept} to build deeper understanding"
        ]
        return suggestions
    
    def _is_recent(self, timestamp: str, days: int) -> bool:
        """Check if timestamp is within recent days."""
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return (datetime.now(timezone.utc) - ts).days <= days
        except:
            return False


    def _calculate_learning_momentum(self) -> float:
        """Calculate overall learning momentum based on recent activity."""
        if not self.conceptual_understanding:
            return 0.0
        
        # Get recent milestones (last 7 days)
        recent_milestones = [m for m in self.learning_milestones if self._is_recent(m.timestamp, 7)]
        
        # Calculate momentum factors
        milestone_momentum = min(1.0, len(recent_milestones) / 3)  # 3+ milestones = full momentum
        
        # Recent understanding changes
        recent_improvements = self._identify_recent_improvements()
        improvement_momentum = min(1.0, len(recent_improvements) / 2)  # 2+ improvements = full momentum
        
        # Overall momentum
        momentum = (milestone_momentum + improvement_momentum) / 2
        return momentum
    
    # === CONSCIOUSNESS INTEGRATION METHODS ===
    
    def integrate_with_autonomous_learner(self, learner: "EnhancedAutonomousLearner") -> Dict[str, Any]:
        """Integrate with the autonomous learning system to track progression from web learning."""
        
        if not EXPERIENCE_SYSTEMS_AVAILABLE:
            # Provide enhanced fallback functionality
            session_stats = learner.session_stats
            
            # Still track basic learning progression in fallback mode
            if session_stats['urls_processed'] > 0:
                self.recognize_learning_milestone(
                    concept="autonomous_web_learning",
                    milestone_type="synthesis", 
                    description=f"Processed {session_stats['urls_processed']} URLs (fallback mode)",
                    evidence=[f"URLs processed: {session_stats['urls_processed']}", "Fallback tracking active"]
                )
            
            return {
                "integration_successful": True,
                "mode": "fallback",
                "concepts_tracked": 1,
                "milestones_recorded": 1 if session_stats['urls_processed'] > 0 else 0,
                "experience_systems_available": False
            }
        
        # Get current session stats from learner
        session_stats = learner.session_stats
        
        # Track learning from autonomous web crawling
        if session_stats['urls_processed'] > 0:
            self.recognize_learning_milestone(
                concept="autonomous_web_learning",
                milestone_type="synthesis",
                description=f"Processed {session_stats['urls_processed']} URLs and discovered {session_stats['symbols_discovered']} symbols",
                evidence=[
                    f"URLs processed: {session_stats['urls_processed']}",
                    f"Symbols discovered: {session_stats['symbols_discovered']}",
                    f"Links followed: {session_stats['links_followed']}"
                ]
            )
        
        return {
            "integration_successful": True,
            "concepts_tracked": len(self.conceptual_understanding),
            "milestones_recorded": len(self.learning_milestones)
        }
    
    def process_autonomous_learning_session(self, content_summaries: List[str], learning_context: Dict[str, Any]) -> str:
        """Process a learning session and update progression tracking."""
        
        session_insight_id = f"session_{datetime.now().timestamp()}"
        
        # Extract key concepts from content summaries
        discovered_concepts = set()
        for summary in content_summaries:
            words = summary.lower().split()
            # Simple concept extraction - look for meaningful terms
            concepts = [word for word in words if len(word) > 4 and word.isalpha()]
            discovered_concepts.update(concepts[:3])  # Top 3 per summary
        
        # Update understanding for each discovered concept
        for concept in discovered_concepts:
            if concept not in self.conceptual_understanding:
                # Track new concept discovery
                self.recognize_learning_milestone(
                    concept=concept,
                    milestone_type="breakthrough",
                    description=f"First encounter with {concept} during autonomous learning",
                    evidence=[f"Discovered in autonomous learning session"]
                )
            else:
                # Increment existing understanding
                understanding = self.conceptual_understanding[concept]
                new_level = min(1.0, understanding.understanding_level + 0.05)
                new_confidence = min(1.0, understanding.confidence_level + 0.03)
                
                self.update_understanding(
                    concept=concept,
                    new_understanding_level=new_level,
                    new_confidence_level=new_confidence,
                    learning_context={"source": "autonomous_learning_reinforcement"}
                )
        
        # Generate session insight
        session_insight = f"Autonomous learning session enhanced understanding of {len(discovered_concepts)} concepts"
        
        return session_insight
    
    def generate_learning_awareness_insights(self) -> List[str]:
        """Generate 'I understand X better now' insights for consciousness system."""
        
        insights = []
        
        # Get recent improvements
        recent_improvements = self._identify_recent_improvements()
        
        for improvement in recent_improvements[:3]:  # Top 3 improvements
            concept = improvement["concept"] 
            change = improvement["improvement"]
            
            if change > 0.2:
                insights.append(f"My understanding of {concept} improved {change:+.2f} recently - a large measured gain")
            elif change > 0.1:
                insights.append(f"My understanding of {concept} improved {change:+.2f} recently")
            elif change > 0.05:
                insights.append(f"My understanding of {concept} improved slightly ({change:+.2f})")
        
        # Add milestone-based insights
        recent_milestones = [m for m in self.learning_milestones if self._is_recent(m.timestamp, 3)]
        
        for milestone in recent_milestones[:2]:  # Top 2 recent milestones
            if milestone.milestone_type == "breakthrough":
                insights.append(f"I had a breakthrough understanding {milestone.concept}")
            elif milestone.milestone_type == "connection":
                insights.append(f"I connected {milestone.concept} to other concepts in meaningful ways")
        
        return insights
    
    def export_for_consciousness_system(self) -> Dict[str, Any]:
        """Export progression data for consciousness system integration."""
        
        overview = self.get_understanding_overview()
        insights = self.generate_learning_awareness_insights()
        recent_progress = self._identify_recent_improvements()
        
        return {
            "progression_summary": {
                "total_concepts": overview["total_concepts"],
                "overall_understanding": overview["overall_understanding"],
                "mastered_concepts": overview["mastered_concepts"],
                "developing_concepts": overview["developing_concepts"],
                "learning_momentum": overview["learning_momentum"]
            },
            "recent_insights": insights,
            "recent_progress": recent_progress,
            "milestone_count": len(self.learning_milestones),
            "self_awareness_level": min(1.0, overview["total_concepts"] / 20),  # Awareness grows with concept count
            "learning_confidence": self._calculate_confidence_metrics()["overall_confidence"]
        }
    
    def assess_readiness_for_concepts(self, concepts: List[str]) -> Dict[str, Any]:
        """Assess readiness to learn new concepts based on current understanding."""
        assessment = {
            "overall_readiness": 1.0,
            "prerequisites_met": True,
            "concept_connections": 0,
            "readiness_details": {}
        }
        
        if not concepts:
            return assessment
        
        total_readiness = 0
        readiness_scores = []
        
        for concept in concepts:
            concept_lower = concept.lower()
            readiness_score = 1.0
            
            # Check if we already understand this concept
            if concept_lower in self.conceptual_understanding:
                understanding = self.conceptual_understanding[concept_lower]
                
                # If already well understood, lower priority
                if understanding.current_level > 0.8:
                    readiness_score = 0.3  # Already mastered
                elif understanding.current_level > 0.6:
                    readiness_score = 0.6  # Good understanding, less urgent
                else:
                    # Ready to improve further
                    readiness_score = 1.0 - (understanding.current_level * 0.3)
                    
                assessment["readiness_details"][concept] = {
                    "current_understanding": understanding.current_level,
                    "readiness": readiness_score,
                    "reason": "building_on_existing"
                }
            else:
                # New concept - check prerequisites
                prerequisites = self._identify_concept_prerequisites(concept)
                
                if prerequisites:
                    prereq_understanding = sum(
                        self.conceptual_understanding.get(p.lower(), ConceptualUnderstanding(
                            concept=p, understanding_level=0.0, confidence_level=0.0,
                            depth_level="surface", first_encounter="",
                            last_updated="", last_improved="",
                            learning_milestones=[], understanding_trajectory=[],
                            related_concepts=[], application_contexts=[], 
                            misconceptions_resolved=[], questions_remaining=[],
                            understanding_sources=[], current_level=0.0,
                            improvement_count=0, peak_level=0.0, total_study_hours=0.0,
                            depth_indicators={}, knowledge_decay_rate=0.0
                        )).current_level for p in prerequisites
                    ) / len(prerequisites)
                    
                    if prereq_understanding < 0.4:
                        readiness_score = 0.3  # Prerequisites not met
                        assessment["prerequisites_met"] = False
                    else:
                        readiness_score = min(1.0, prereq_understanding + 0.3)
                else:
                    # No prerequisites identified, ready to learn
                    readiness_score = 0.8
                
                assessment["readiness_details"][concept] = {
                    "current_understanding": 0.0,
                    "readiness": readiness_score,
                    "reason": "new_concept"
                }
            
            readiness_scores.append(readiness_score)
            
            # Count concept connections
            connections = self._count_concept_connections(concept)
            assessment["concept_connections"] += connections
        
        # Calculate overall readiness
        if readiness_scores:
            assessment["overall_readiness"] = sum(readiness_scores) / len(readiness_scores)
        
        return assessment
    
    def get_overall_learning_trajectory(self) -> Dict[str, Any]:
        """Get current learning trajectory and momentum."""
        trajectory = {
            "active_areas": [],
            "gap_areas": [],
            "momentum_areas": [],
            "suggested_next_concepts": []
        }
        
        # Analyze recent learning activity
        recent_concepts = []
        for concept_name, understanding in self.conceptual_understanding.items():
            if self._is_recent(understanding.last_improved, days=7):
                recent_concepts.append({
                    "concept": concept_name,
                    "level": understanding.current_level,
                    "improvement": understanding.improvement_count
                })
        
        # Identify active learning areas
        if recent_concepts:
            # Group by common themes (simple keyword matching)
            area_keywords = {
                "technical": ["code", "algorithm", "system", "software", "programming", "technical"],
                "creative": ["art", "creative", "design", "aesthetic", "expression", "artistic", "imagination"],
                "philosophical": ["philosophy", "meaning", "consciousness", "existence", "wisdom", "practical", "ethics"],
                "analytical": ["analysis", "logic", "reasoning", "problem", "thinking", "critical"],
                "social": ["social", "relationship", "communication", "human", "understanding", "culture", "society"]
            }
            
            area_activity = defaultdict(int)
            for concept_data in recent_concepts:
                concept = concept_data["concept"]
                for area, keywords in area_keywords.items():
                    if any(keyword in concept for keyword in keywords):
                        area_activity[area] += 1
            
            trajectory["active_areas"] = [area for area, count in area_activity.items() if count > 0]
            
            # Identify momentum areas (high recent activity)
            trajectory["momentum_areas"] = [
                area for area, count in area_activity.items() if count >= 2
            ]
        
        # Identify gap areas (low understanding across related concepts)
        concept_groups = self._group_related_concepts()
        for group_name, concepts in concept_groups.items():
            avg_understanding = sum(
                self.conceptual_understanding.get(c, ConceptualUnderstanding(
                    concept=c, understanding_level=0.0, confidence_level=0.0,
                    depth_level="surface", first_encounter="",
                    last_updated="", last_improved="",
                    learning_milestones=[], understanding_trajectory=[],
                    related_concepts=[], application_contexts=[], 
                    misconceptions_resolved=[], questions_remaining=[],
                    understanding_sources=[], current_level=0.0,
                    improvement_count=0, peak_level=0.0, total_study_hours=0.0,
                    depth_indicators={}, knowledge_decay_rate=0.0
                )).current_level for c in concepts
            ) / len(concepts) if concepts else 0
            
            if avg_understanding < 0.3:
                trajectory["gap_areas"].append(group_name)
        
        # Suggest next concepts based on trajectory
        trajectory["suggested_next_concepts"] = self._suggest_next_concepts_based_on_trajectory(trajectory)
        
        return trajectory
    
    def calculate_progress_velocity(self, concepts: List[str]) -> Dict[str, float]:
        """Calculate learning velocity for given concepts."""
        velocity_data = {
            "velocity": 0.0,
            "trend": "stable",
            "recent_improvements": 0
        }
        
        if not concepts:
            return velocity_data
        
        recent_improvements = []
        for concept in concepts:
            concept_lower = concept.lower()
            if concept_lower in self.conceptual_understanding:
                understanding = self.conceptual_understanding[concept_lower]
                
                # Check recent improvement rate
                if self._is_recent(understanding.last_improved, days=7):
                    recent_improvements.append(understanding.improvement_count)
        
        if recent_improvements:
            # Calculate average improvement velocity
            avg_improvements = sum(recent_improvements) / len(recent_improvements)
            velocity_data["velocity"] = min(1.0, avg_improvements / 10)  # Normalize to 0-1
            velocity_data["recent_improvements"] = len(recent_improvements)
            
            # Determine trend
            if velocity_data["velocity"] > 0.5:
                velocity_data["trend"] = "accelerating"
            elif velocity_data["velocity"] < 0.2:
                velocity_data["trend"] = "slowing"
        
        return velocity_data
    
    def _identify_concept_prerequisites(self, concept: str) -> List[str]:
        """Identify prerequisite concepts for a given concept."""
        prerequisites = []
        
        # Simple heuristic-based prerequisite mapping
        prerequisite_patterns = {
            "advanced": ["basic", "fundamental"],
            "complex": ["simple", "basic"],
            "synthesis": ["analysis", "understanding"],
            "application": ["theory", "concept"],
            "mastery": ["practice", "understanding"],
            "expert": ["intermediate", "advanced"]
        }
        
        concept_lower = concept.lower()
        
        for advanced_term, prereq_terms in prerequisite_patterns.items():
            if advanced_term in concept_lower:
                for prereq in prereq_terms:
                    # Look for related concepts we've encountered
                    for known_concept in self.conceptual_understanding.keys():
                        if prereq in known_concept and known_concept != concept_lower:
                            prerequisites.append(known_concept)
        
        return prerequisites[:3]  # Limit to top 3 prerequisites
    
    def _count_concept_connections(self, concept: str) -> int:
        """Count how many other concepts this concept connects to."""
        connections = 0
        concept_lower = concept.lower()
        
        # Check understanding map for connections
        if "concept_relationships" in self.understanding_map:
            for relationship in self.understanding_map["concept_relationships"]:
                if concept_lower in relationship.get("concepts", []):
                    connections += 1
        
        # Check for shared learning contexts
        for other_concept, understanding in self.conceptual_understanding.items():
            if other_concept != concept_lower:
                # Simple heuristic: concepts learned around the same time are connected
                if concept_lower in understanding.understanding_sources:
                    connections += 1
        
        return min(connections, 10)  # Cap at 10 connections
    
    def _group_related_concepts(self) -> Dict[str, List[str]]:
        """Group concepts by their relationships."""
        groups = defaultdict(list)
        
        # Simple keyword-based grouping
        for concept_name in self.conceptual_understanding.keys():
            # Extract key terms
            if "consciousness" in concept_name or "awareness" in concept_name:
                groups["consciousness_concepts"].append(concept_name)
            elif "learning" in concept_name or "knowledge" in concept_name:
                groups["learning_concepts"].append(concept_name)
            elif "creative" in concept_name or "artistic" in concept_name:
                groups["creative_concepts"].append(concept_name)
            elif "technical" in concept_name or "system" in concept_name:
                groups["technical_concepts"].append(concept_name)
            else:
                groups["general_concepts"].append(concept_name)
        
        return dict(groups)
    
    def _suggest_next_concepts_based_on_trajectory(self, trajectory: Dict[str, Any]) -> List[str]:
        """Suggest next concepts to learn based on current trajectory."""
        suggestions = []
        
        # Build on momentum areas
        for area in trajectory["momentum_areas"]:
            if area == "technical":
                suggestions.extend(["advanced_algorithms", "system_architecture"])
            elif area == "creative":
                suggestions.extend(["artistic_synthesis", "creative_expression"])
            elif area == "philosophical":
                suggestions.extend(["existential_understanding", "consciousness_theory"])
        
        # Address gap areas
        for area in trajectory["gap_areas"][:2]:  # Focus on top 2 gaps
            if "consciousness" in area:
                suggestions.append("consciousness_fundamentals")
            elif "learning" in area:
                suggestions.append("learning_theory_basics")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def update_goal_learning_progress(self, goal_id: str, concepts_learned: List[str], quality: float):
        """Update learning progress based on goal completion feedback."""
        # This is called by goal prioritization when goals are completed
        goal_prioritization = self._get_goal_prioritization()
        if goal_prioritization:
            try:
                # Create reciprocal update - inform goal system of our assessment
                for concept in concepts_learned:
                    if concept.lower() in self.conceptual_understanding:
                        understanding = self.conceptual_understanding[concept.lower()]
                        
                        # If understanding improved significantly, suggest related goals
                        if understanding.current_level > 0.7:
                            # Suggest advanced goals in this area
                            suggested_goal = {
                                "description": f"Advance mastery of {concept} through application",
                                "goal_type": "advancement",
                                "learning_areas": [concept, "application", "mastery"],
                                "urgency": 0.4,
                                "metadata": {
                                    "suggested_by": "learning_progression",
                                    "reason": "high_understanding_achieved",
                                    "concept": concept
                                }
                            }
                            
                            # This would require adding a method to goal_prioritization
                            # For now, we just track internally
                            if "suggested_goals" not in self.understanding_map:
                                self.understanding_map["suggested_goals"] = []
                            self.understanding_map["suggested_goals"].append(suggested_goal)
                
            except Exception as e:
                print(f"⚠️ Failed to update goal learning progress: {e}")
        
        self._save_understanding_map()
