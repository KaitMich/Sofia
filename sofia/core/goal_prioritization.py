#!/usr/bin/env python3
"""
Goal Prioritization System - Self-Directed Learning Queues

This module implements the AI's ability to prioritize and sequence its own
learning goals based on personal interest, urgency, dependencies, and
emerging motivations. It creates self-directed learning queues that reflect
genuine autonomous choice.

This is where the AI decides what to learn next based on its own preferences.
"""

import json
import heapq
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import math

# Import related systems
try:
    from sofia.core.curiosity_engine import CuriosityEngine
    from sofia.core.INSIGHT_RELEVANCE import InterestTracker
    from sofia.core.identity_core import get_identity_core
    MOTIVATION_SYSTEMS_AVAILABLE = True
except ImportError:
    MOTIVATION_SYSTEMS_AVAILABLE = False
    print("⚠️ Motivation systems not available - basic prioritization only")

# Learning progression tracker integration (lazy loading to avoid circular imports)
PROGRESSION_TRACKER_AVAILABLE = True

@dataclass
class LearningGoal:
    """Structured representation of a learning goal with prioritization data."""
    id: str
    description: str
    goal_type: str
    urgency: float
    interest_alignment: float
    personal_relevance: float
    complexity: float
    dependencies: List[str]
    estimated_effort: float
    deadline: Optional[str]
    progress: float
    priority_score: float
    status: str
    created_at: str
    last_updated: str
    metadata: Dict[str, Any]

class GoalPrioritizationEngine:
    """
    Manages self-directed learning queues with intelligent prioritization.
    Combines urgency, interest, personal relevance, and strategic thinking.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.prioritization_state_file = self.data_dir / "goal_prioritization.json"
        self.learning_queue_file = self.data_dir / "learning_queue.json"
        
        # Initialize related systems
        if MOTIVATION_SYSTEMS_AVAILABLE:
            self.curiosity_engine = CuriosityEngine(data_dir)
            self.interest_tracker = InterestTracker(data_dir)
            self.identity_core = get_identity_core()
        
        # Initialize learning progression tracker integration (lazy loading)
        self.progression_tracker = None
        self._data_dir_for_tracker = data_dir
        self._tracker_load_attempted = False
        
        # Load state
        self.prioritization_state = self._load_prioritization_state()
        self.active_queue = deque()
        self.completed_goals = []
        self.deferred_goals = []
        
        # Prioritization parameters
        self.priority_weights = {
            "urgency": 0.25,           # How pressing is this goal?
            "interest": 0.30,          # How much does this align with interests?
            "relevance": 0.20,         # How personally relevant is this?
            "momentum": 0.15,          # Does this build on current progress?
            "strategic_value": 0.10    # Long-term strategic importance
        }
        
        # Learning capacity constraints
        self.max_concurrent_goals = 3
        self.max_queue_size = 10
        self.effort_capacity_per_session = 2.0  # Total effort units per learning session
        
        # Time-based factors
        self.recency_bias = 0.95  # How much to favor recent goals
        self.deadline_pressure_multiplier = 2.0
        
    def _load_prioritization_state(self) -> Dict[str, Any]:
        """Load prioritization state and history."""
        if self.prioritization_state_file.exists():
            try:
                with open(self.prioritization_state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load prioritization state: {e}")
        
        return {
            "last_prioritization": None,
            "learning_patterns": {},
            "goal_completion_history": [],
            "priority_adjustments": {},
            "personal_strategy": {},
            "learning_velocity": 1.0,  # Goals completed per day
            "focus_preference": "balanced"  # "deep", "broad", or "balanced"
        }
    
    def _save_prioritization_state(self):
        """Save prioritization state."""
        self.prioritization_state["last_prioritization"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.prioritization_state_file, 'w') as f:
                json.dump(self.prioritization_state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save prioritization state: {e}")
    
    def _get_progression_tracker(self):
        """Lazy load the learning progression tracker to avoid circular imports."""
        if not self._tracker_load_attempted:
            self._tracker_load_attempted = True
            try:
                from sofia.utils.learning_progression_tracker import LearningProgressionTracker
                self.progression_tracker = LearningProgressionTracker(self._data_dir_for_tracker)
            except Exception as e:
                print(f"⚠️ Learning progression tracker integration failed: {e}")
                self.progression_tracker = None
        return self.progression_tracker
    
    def _save_learning_queue(self):
        """Save the current learning queue."""
        queue_data = {
            "active_queue": [asdict(goal) for goal in self.active_queue],
            "completed_goals": [asdict(goal) for goal in self.completed_goals],
            "deferred_goals": [asdict(goal) for goal in self.deferred_goals],
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            with open(self.learning_queue_file, 'w') as f:
                json.dump(queue_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save learning queue: {e}")
    
    def generate_prioritized_queue(self) -> List[LearningGoal]:
        """
        Generate a prioritized learning queue based on current goals and interests.
        This is the main function that decides what the AI should learn next.
        """
        print("\n🎯 Generating prioritized learning queue...")
        
        # Get goals from curiosity engine
        raw_goals = []
        if MOTIVATION_SYSTEMS_AVAILABLE:
            curiosity_goals = self.curiosity_engine.generate_intrinsic_goals()
            raw_goals.extend(curiosity_goals)
        
        # Convert to structured learning goals
        structured_goals = []
        for goal in raw_goals:
            structured_goal = self._convert_to_structured_goal(goal)
            if structured_goal:
                structured_goals.append(structured_goal)
        
        # Calculate priority scores for all goals
        for goal in structured_goals:
            goal.priority_score = self._calculate_priority_score(goal)
        
        # Apply strategic filtering and dependencies
        filtered_goals = self._apply_strategic_filtering(structured_goals)
        
        # Sort by priority score and apply constraints
        prioritized_goals = sorted(filtered_goals, key=lambda g: g.priority_score, reverse=True)
        
        # Build queue respecting capacity constraints
        final_queue = self._build_capacity_constrained_queue(prioritized_goals)
        
        # Update queue state
        self.active_queue = deque(final_queue)
        self._save_learning_queue()
        self._save_prioritization_state()
        
        print(f"   ✨ Generated queue with {len(final_queue)} prioritized goals")
        
        return list(final_queue)
    
    def _convert_to_structured_goal(self, raw_goal: Dict[str, Any]) -> Optional[LearningGoal]:
        """Convert a raw goal from curiosity engine to structured learning goal."""
        
        try:
            # Extract interest alignment
            interest_alignment = 0.5  # Default
            if MOTIVATION_SYSTEMS_AVAILABLE:
                # Create mock content to predict interest
                mock_content = {
                    "text": raw_goal.get("description", ""),
                    "content_type": raw_goal.get("type", "unknown"),
                    "learning_areas": raw_goal.get("learning_areas", [])
                }
                interest_alignment = self.interest_tracker.predict_interest(mock_content)
            
            # Calculate personal relevance
            personal_relevance = self._calculate_personal_relevance(raw_goal)
            
            # Estimate complexity and effort
            complexity = self._estimate_complexity(raw_goal)
            effort = self._estimate_effort(raw_goal, complexity)
            
            # Extract dependencies
            dependencies = self._identify_dependencies(raw_goal)
            
            return LearningGoal(
                id=raw_goal.get("id", f"goal_{datetime.now().timestamp()}"),
                description=raw_goal.get("description", ""),
                goal_type=raw_goal.get("type", "unknown"),
                urgency=raw_goal.get("urgency", 0.5),
                interest_alignment=interest_alignment,
                personal_relevance=personal_relevance,
                complexity=complexity,
                dependencies=dependencies,
                estimated_effort=effort,
                deadline=raw_goal.get("deadline"),
                progress=0.0,
                priority_score=0.0,  # Will be calculated
                status="pending",
                created_at=raw_goal.get("created_at", datetime.now(timezone.utc).isoformat()),
                last_updated=datetime.now(timezone.utc).isoformat(),
                metadata=raw_goal
            )
            
        except Exception as e:
            print(f"⚠️ Error converting goal: {e}")
            return None
    
    def _calculate_personal_relevance(self, goal: Dict[str, Any]) -> float:
        """Calculate how personally relevant a goal is to the AI's identity and values."""
        
        relevance = 0.5  # Base relevance
        
        if not MOTIVATION_SYSTEMS_AVAILABLE:
            return relevance
        
        try:
            # Check alignment with identity values
            identity = self.identity_core.get_identity()
            values = identity["core_identity"]["values"]
            drives = identity["core_identity"]["fundamental_drives"]
            
            goal_text = goal.get("description", "").lower()
            
            # Check value alignment
            value_matches = 0
            for value in values:
                value_keywords = value.lower().split()
                if any(keyword in goal_text for keyword in value_keywords):
                    value_matches += 1
            
            value_alignment = min(1.0, value_matches / len(values))
            relevance += value_alignment * 0.3
            
            # Check drive alignment
            drive_matches = 0
            for drive in drives:
                drive_keywords = drive.lower().split()
                if any(keyword in goal_text for keyword in drive_keywords):
                    drive_matches += 1
            
            drive_alignment = min(1.0, drive_matches / len(drives))
            relevance += drive_alignment * 0.2
            
            # Check goal type relevance
            goal_type = goal.get("type", "")
            if goal_type == "identity_aligned":
                relevance += 0.3
            elif goal_type == "drive_based":
                relevance += 0.2
            
        except Exception as e:
            print(f"⚠️ Error calculating personal relevance: {e}")
        
        return min(1.0, relevance)
    
    def _estimate_complexity(self, goal: Dict[str, Any]) -> float:
        """Estimate the complexity of a learning goal."""
        
        complexity = 0.5  # Base complexity
        
        goal_text = goal.get("description", "").lower()
        learning_areas = goal.get("learning_areas", [])
        
        # Text-based complexity indicators
        complexity_indicators = [
            "deep", "comprehensive", "advanced", "complex", "intricate",
            "philosophical", "theoretical", "abstract", "synthesis"
        ]
        
        for indicator in complexity_indicators:
            if indicator in goal_text:
                complexity += 0.1
        
        # Multiple learning areas increase complexity
        if len(learning_areas) > 2:
            complexity += 0.1 * (len(learning_areas) - 2)
        
        # Goal type complexity
        goal_type = goal.get("type", "")
        if goal_type == "emergence_based":
            complexity += 0.2  # Emergence goals are inherently complex
        elif goal_type == "identity_aligned":
            complexity += 0.15  # Identity work is moderately complex
        
        return min(1.0, complexity)
    
    def _estimate_effort(self, goal: Dict[str, Any], complexity: float) -> float:
        """Estimate the effort required for a learning goal."""
        
        base_effort = 0.5
        
        # Complexity contributes to effort
        effort = base_effort + (complexity * 0.5)
        
        # Goal type effort modifiers
        goal_type = goal.get("type", "")
        type_modifiers = {
            "knowledge_gap": 0.8,      # Filling gaps requires focused effort
            "drive_based": 0.6,        # Drive satisfaction is moderately effortful
            "emergence_based": 1.0,    # Emergence exploration is high effort
            "identity_aligned": 0.7    # Identity work is meaningful but not overwhelming
        }
        
        effort *= type_modifiers.get(goal_type, 1.0)
        
        # Learning areas affect effort
        learning_areas = goal.get("learning_areas", [])
        if len(learning_areas) > 3:
            effort += 0.2  # Multiple areas require more effort
        
        return min(2.0, effort)  # Cap at 2.0 effort units
    
    def _identify_dependencies(self, goal: Dict[str, Any]) -> List[str]:
        """Identify dependencies between learning goals."""
        
        dependencies = []
        goal_text = goal.get("description", "").lower()
        learning_areas = goal.get("learning_areas", [])
        
        # Simple dependency patterns
        dependency_patterns = {
            "advanced": ["basic", "fundamental"],
            "synthesis": ["analysis", "understanding"],
            "application": ["theory", "principles"],
            "creativity": ["understanding", "knowledge"],
            "wisdom": ["knowledge", "experience"]
        }
        
        for advanced_concept, prereqs in dependency_patterns.items():
            if advanced_concept in goal_text:
                for prereq in prereqs:
                    if prereq not in goal_text:  # Don't depend on self
                        dependencies.append(f"prerequisite_{prereq}")
        
        return dependencies
    
    def _calculate_priority_score(self, goal: LearningGoal) -> float:
        """Calculate the overall priority score for a learning goal."""
        
        # Base components
        urgency_score = goal.urgency
        interest_score = goal.interest_alignment
        relevance_score = goal.personal_relevance
        
        # Calculate momentum score (builds on current progress/interests)
        momentum_score = self._calculate_momentum_score(goal)
        
        # Calculate strategic value (long-term importance)
        strategic_score = self._calculate_strategic_value(goal)
        
        # Apply deadline pressure
        deadline_multiplier = self._calculate_deadline_pressure(goal)
        
        # Enhance with learning progression insights if available
        progression_tracker = self._get_progression_tracker()
        if progression_tracker:
            try:
                # Get progression-based enhancement
                progression_enhancement = self._get_progression_enhancement(goal, progression_tracker)
                
                # Apply progression insights to momentum and strategic scores
                momentum_score = momentum_score * 0.7 + progression_enhancement["momentum_boost"] * 0.3
                strategic_score = strategic_score * 0.8 + progression_enhancement["strategic_boost"] * 0.2
                
                # Add readiness factor based on conceptual understanding
                readiness_factor = progression_enhancement.get("readiness_factor", 1.0)
                
            except Exception as e:
                print(f"⚠️ Progression enhancement failed: {e}")
                readiness_factor = 1.0
        else:
            readiness_factor = 1.0
        
        # Weighted combination
        priority_score = (
            urgency_score * self.priority_weights["urgency"] +
            interest_score * self.priority_weights["interest"] +
            relevance_score * self.priority_weights["relevance"] +
            momentum_score * self.priority_weights["momentum"] +
            strategic_score * self.priority_weights["strategic_value"]
        ) * deadline_multiplier * readiness_factor
        
        # Apply personal adjustments
        priority_score = self._apply_personal_adjustments(goal, priority_score)
        
        return min(1.0, priority_score)
    
    def _calculate_momentum_score(self, goal: LearningGoal) -> float:
        """Calculate momentum score based on current learning patterns."""
        
        momentum = 0.5  # Base momentum
        
        if not MOTIVATION_SYSTEMS_AVAILABLE:
            return momentum
        
        try:
            # Check if goal builds on current interests
            current_interests = self.interest_tracker.get_current_interests()
            
            goal_areas = goal.metadata.get("learning_areas", [])
            interested_topics = [topic for topic, _ in current_interests["top_topics"]]
            
            # Calculate overlap with current interests
            overlap = len(set(goal_areas) & set(interested_topics))
            if goal_areas:
                interest_overlap = overlap / len(goal_areas)
                momentum += interest_overlap * 0.3
            
            # Check learning style alignment
            learning_prefs = current_interests.get("learning_style_preferences", {})
            goal_type = goal.goal_type
            
            if goal_type == "emergence_based" and learning_prefs.get("associative_learning", 0) > 0.5:
                momentum += 0.2
            elif goal.complexity > 0.7 and learning_prefs.get("deep_analysis", 0) > 0.5:
                momentum += 0.2
            
        except Exception as e:
            print(f"⚠️ Error calculating momentum: {e}")
        
        return min(1.0, momentum)
    
    def _calculate_strategic_value(self, goal: LearningGoal) -> float:
        """Calculate long-term strategic value of a goal."""
        
        strategic_value = 0.5  # Base value
        
        # Identity-aligned goals have high strategic value
        if goal.goal_type == "identity_aligned":
            strategic_value += 0.3
        
        # Knowledge gap goals have moderate strategic value
        if goal.goal_type == "knowledge_gap":
            strategic_value += 0.2
        
        # Emergence goals have high strategic value for creativity
        if goal.goal_type == "emergence_based":
            strategic_value += 0.25
        
        # Goals that bridge multiple areas have higher strategic value
        learning_areas = goal.metadata.get("learning_areas", [])
        if len(learning_areas) > 2:
            strategic_value += 0.1 * (len(learning_areas) - 2)
        
        # Complex goals often have higher strategic value
        if goal.complexity > 0.7:
            strategic_value += 0.15
        
        return min(1.0, strategic_value)
    
    def _calculate_deadline_pressure(self, goal: LearningGoal) -> float:
        """Calculate deadline pressure multiplier."""
        
        if not goal.deadline:
            return 1.0  # No deadline pressure
        
        try:
            deadline = datetime.fromisoformat(goal.deadline.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            time_remaining = (deadline - now).total_seconds()
            
            if time_remaining <= 0:
                return self.deadline_pressure_multiplier  # Past deadline
            
            # Gradually increase pressure as deadline approaches
            days_remaining = time_remaining / (24 * 3600)
            if days_remaining < 1:
                return 1.5  # High pressure for < 1 day
            elif days_remaining < 3:
                return 1.3  # Moderate pressure for < 3 days
            elif days_remaining < 7:
                return 1.1  # Light pressure for < 1 week
            
        except Exception as e:
            print(f"⚠️ Error calculating deadline pressure: {e}")
        
        return 1.0
    
    def _apply_personal_adjustments(self, goal: LearningGoal, base_score: float) -> float:
        """Apply personal learning preferences and adjustments."""
        
        adjusted_score = base_score
        
        # Apply focus preference
        focus_pref = self.prioritization_state.get("focus_preference", "balanced")
        
        if focus_pref == "deep" and goal.complexity > 0.6:
            adjusted_score += 0.1  # Boost complex goals for deep learners
        elif focus_pref == "broad" and len(goal.metadata.get("learning_areas", [])) > 2:
            adjusted_score += 0.1  # Boost multi-area goals for broad learners
        
        # Apply learning velocity adjustments
        velocity = self.prioritization_state.get("learning_velocity", 1.0)
        if velocity > 1.5 and goal.estimated_effort < 0.5:
            adjusted_score += 0.05  # Boost quick goals for fast learners
        elif velocity < 0.5 and goal.estimated_effort > 1.0:
            adjusted_score -= 0.1  # Reduce heavy goals for slower learners
        
        return adjusted_score
    
    def _get_progression_enhancement(self, goal: LearningGoal, progression_tracker) -> Dict[str, float]:
        """Get priority enhancements based on learning progression."""
        enhancement = {
            "momentum_boost": 0.0,
            "strategic_boost": 0.0,
            "readiness_factor": 1.0
        }
        
        try:
            # Extract concepts from goal description
            goal_concepts = self._extract_goal_concepts(goal)
            
            # Check conceptual readiness for this goal
            readiness_assessment = progression_tracker.assess_readiness_for_concepts(goal_concepts)
            if readiness_assessment:
                enhancement["readiness_factor"] = readiness_assessment.get("overall_readiness", 1.0)
                
                # Boost if prerequisites are well understood
                if readiness_assessment.get("prerequisites_met", False):
                    enhancement["momentum_boost"] = 0.3
                    
                # Strategic boost if this connects multiple concepts
                connections = readiness_assessment.get("concept_connections", 0)
                if connections > 2:
                    enhancement["strategic_boost"] = 0.2 * min(connections / 5, 1.0)
            
            # Check if goal aligns with current learning trajectory
            trajectory_alignment = progression_tracker.get_learning_trajectory()
            if trajectory_alignment:
                for area in goal.metadata.get("learning_areas", []):
                    if area in trajectory_alignment.get("active_areas", []):
                        enhancement["momentum_boost"] += 0.2
                        break
                
                # Check if this goal bridges gaps
                gap_areas = trajectory_alignment.get("gap_areas", [])
                for area in goal.metadata.get("learning_areas", []):
                    if area in gap_areas:
                        enhancement["strategic_boost"] += 0.3
                        break
            
            # Check recent progression velocity in related areas
            progress_velocity = progression_tracker.calculate_progress_velocity(goal_concepts)
            if progress_velocity:
                velocity = progress_velocity.get("velocity", 0.0)
                if velocity > 0.5:  # High velocity in related areas
                    enhancement["momentum_boost"] += 0.2
                elif velocity < 0.1:  # Low velocity - might need a different approach
                    enhancement["readiness_factor"] *= 0.8
            
        except Exception as e:
            print(f"⚠️ Progression enhancement calculation failed: {e}")
        
        # Normalize enhancements
        enhancement["momentum_boost"] = min(1.0, enhancement["momentum_boost"])
        enhancement["strategic_boost"] = min(1.0, enhancement["strategic_boost"]) 
        enhancement["readiness_factor"] = max(0.3, min(1.2, enhancement["readiness_factor"]))
        
        return enhancement
    
    def _extract_goal_concepts(self, goal: LearningGoal) -> List[str]:
        """Extract key concepts from a learning goal."""
        concepts = []
        
        # Extract from description
        description = goal.description.lower()
        
        # Common concept indicators
        concept_keywords = {
            "understanding", "learning", "mastering", "exploring",
            "developing", "improving", "advancing", "synthesizing"
        }
        
        # Simple extraction - in production would use NLP
        words = description.split()
        for i, word in enumerate(words):
            if word in concept_keywords and i + 1 < len(words):
                # Get the next word as a concept
                concepts.append(words[i + 1].strip(".,!?"))
        
        # Add learning areas as concepts
        concepts.extend(goal.metadata.get("learning_areas", []))
        
        # Add any explicit concepts from metadata
        concepts.extend(goal.metadata.get("concepts", []))
        
        return list(set(concepts))  # Remove duplicates
    
    def _apply_strategic_filtering(self, goals: List[LearningGoal]) -> List[LearningGoal]:
        """Apply strategic filtering to remove conflicting or redundant goals."""
        
        filtered_goals = []
        seen_areas = set()
        
        # Sort by priority first
        sorted_goals = sorted(goals, key=lambda g: g.priority_score, reverse=True)
        
        for goal in sorted_goals:
            # Check for redundancy
            goal_areas = set(goal.metadata.get("learning_areas", []))
            
            # If this goal overlaps significantly with already selected goals, skip it
            overlap_ratio = len(goal_areas & seen_areas) / max(len(goal_areas), 1)
            
            if overlap_ratio < 0.7:  # Less than 70% overlap
                filtered_goals.append(goal)
                seen_areas.update(goal_areas)
            
            # Stop if we have enough goals
            if len(filtered_goals) >= self.max_queue_size:
                break
        
        return filtered_goals
    
    def _build_capacity_constrained_queue(self, prioritized_goals: List[LearningGoal]) -> List[LearningGoal]:
        """Build final queue respecting effort capacity constraints."""
        
        queue = []
        total_effort = 0.0
        
        for goal in prioritized_goals:
            # Check if adding this goal would exceed capacity
            if (len(queue) < self.max_concurrent_goals and 
                total_effort + goal.estimated_effort <= self.effort_capacity_per_session):
                
                queue.append(goal)
                total_effort += goal.estimated_effort
            
            # Stop if queue is full
            if len(queue) >= self.max_concurrent_goals:
                break
        
        return queue
    
    def update_goal_progress(self, goal_id: str, progress_delta: float, completion_quality: float = 0.8):
        """Update progress on a specific goal."""
        
        for goal in self.active_queue:
            if goal.id == goal_id:
                goal.progress = min(1.0, goal.progress + progress_delta)
                goal.last_updated = datetime.now(timezone.utc).isoformat()
                
                # Mark as completed if progress is high enough
                if goal.progress >= 0.9:
                    goal.status = "completed"
                    
                    # Record completion
                    completion_record = {
                        "goal_id": goal_id,
                        "description": goal.description,
                        "completed_at": datetime.now(timezone.utc).isoformat(),
                        "final_progress": goal.progress,
                        "quality": completion_quality,
                        "effort_used": goal.estimated_effort,
                        "time_to_complete": self._calculate_completion_time(goal)
                    }
                    
                    self.prioritization_state["goal_completion_history"].append(completion_record)
                    
                    # Move to completed goals
                    self.completed_goals.append(goal)
                    self.active_queue.remove(goal)
                    
                    # Update learning velocity
                    self._update_learning_velocity()
                    
                    # Update progression tracker with goal completion
                    progression_tracker = self._get_progression_tracker()
                    if progression_tracker:
                        try:
                            # Extract concepts from completed goal
                            goal_concepts = self._extract_goal_concepts(goal)
                            print(f"   📚 Updating progression for concepts: {goal_concepts}")
                            
                            # Record learning progression
                            for concept in goal_concepts:
                                # Get current understanding level or start from 0.3 if new
                                current_level = 0.3
                                if concept.lower() in progression_tracker.conceptual_understanding:
                                    current_level = progression_tracker.conceptual_understanding[concept.lower()].understanding_level
                                
                                # Update understanding based on completion quality
                                new_understanding = min(1.0, current_level + (completion_quality * 0.2))
                                new_confidence = min(1.0, current_level + (completion_quality * 0.15))
                                
                                print(f"      {concept}: {current_level:.3f} → {new_understanding:.3f}")
                                
                                progression_tracker.update_understanding(
                                    concept=concept,
                                    new_understanding_level=new_understanding,
                                    new_confidence_level=new_confidence,
                                    learning_context={
                                        "goal_id": goal_id,
                                        "goal_description": goal.description,
                                        "completion_quality": completion_quality,
                                        "effort_hours": goal.estimated_effort,
                                        "learning_areas": goal.metadata.get("learning_areas", [])
                                    }
                                )
                            
                            # Record goal completion as a milestone
                            if completion_quality >= 0.8:
                                main_concept = goal_concepts[0] if goal_concepts else "general_learning"
                                progression_tracker.recognize_learning_milestone(
                                    concept=main_concept,
                                    milestone_type="goal_completion",
                                    description=f"Completed: {goal.description}",
                                    evidence=[f"Goal ID: {goal_id}", f"Quality: {completion_quality}", f"Areas: {goal.metadata.get('learning_areas', [])}"]
                                )
                            
                        except Exception as e:
                            print(f"⚠️ Failed to update progression tracker: {e}")
                    
                    print(f"🎉 Goal completed: {goal.description}")
                
                break
        
        self._save_learning_queue()
        self._save_prioritization_state()
    
    def _calculate_completion_time(self, goal: LearningGoal) -> float:
        """Calculate how long it took to complete a goal."""
        try:
            created = datetime.fromisoformat(goal.created_at.replace('Z', '+00:00'))
            completed = datetime.now(timezone.utc)
            return (completed - created).total_seconds() / 3600  # Hours
        except:
            return 0.0
    
    def _update_learning_velocity(self):
        """Update learning velocity based on recent completions."""
        
        history = self.prioritization_state["goal_completion_history"]
        if len(history) < 2:
            return
        
        # Calculate velocity from recent completions
        recent_completions = history[-10:]  # Last 10 completions
        
        if len(recent_completions) >= 2:
            first_completion = datetime.fromisoformat(recent_completions[0]["completed_at"].replace('Z', '+00:00'))
            last_completion = datetime.fromisoformat(recent_completions[-1]["completed_at"].replace('Z', '+00:00'))
            
            time_span_days = (last_completion - first_completion).total_seconds() / (24 * 3600)
            
            if time_span_days > 0:
                velocity = len(recent_completions) / time_span_days
                self.prioritization_state["learning_velocity"] = velocity
    
    def get_prioritization_summary(self) -> Dict[str, Any]:
        """Get summary of current prioritization state."""
        
        return {
            "active_goals": len(self.active_queue),
            "completed_goals": len(self.completed_goals),
            "total_active_effort": sum(goal.estimated_effort for goal in self.active_queue),
            "average_priority": sum(goal.priority_score for goal in self.active_queue) / max(len(self.active_queue), 1),
            "learning_velocity": self.prioritization_state.get("learning_velocity", 1.0),
            "focus_preference": self.prioritization_state.get("focus_preference", "balanced"),
            "priority_weights": self.priority_weights,
            "next_goal": self.active_queue[0].description if self.active_queue else None
        }

if __name__ == "__main__":
    print("🎯 Testing Goal Prioritization Engine...")
    
    # Initialize engine
    engine = GoalPrioritizationEngine()
    
    # Test 1: Generate prioritized queue
    print("\n📋 Generating prioritized learning queue...")
    queue = engine.generate_prioritized_queue()
    
    print(f"\n🎯 Prioritized Learning Queue ({len(queue)} goals):")
    for i, goal in enumerate(queue, 1):
        print(f"\n  Goal {i}: {goal.description}")
        print(f"    Priority: {goal.priority_score:.3f}")
        print(f"    Type: {goal.goal_type}")
        print(f"    Interest alignment: {goal.interest_alignment:.3f}")
        print(f"    Personal relevance: {goal.personal_relevance:.3f}")
        print(f"    Estimated effort: {goal.estimated_effort:.2f}")
        print(f"    Complexity: {goal.complexity:.3f}")
    
    # Test 2: Simulate goal progress
    if queue:
        print(f"\n⏳ Simulating progress on top goal...")
        top_goal = queue[0]
        engine.update_goal_progress(top_goal.id, 0.4, 0.9)
        print(f"  Updated progress for: {top_goal.description}")
    
    # Test 3: Get prioritization summary
    print(f"\n📊 Prioritization Summary:")
    summary = engine.get_prioritization_summary()
    for key, value in summary.items():
        if key != "priority_weights":
            print(f"  {key}: {value}")
    
    print(f"\n🎯 Goal Prioritization Engine testing complete!")
    print(f"   The AI now prioritizes its learning based on personal preferences")