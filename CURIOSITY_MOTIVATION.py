#!/usr/bin/env python3
"""
===== CONSOLIDATED FILE: CURIOSITY_MOTIVATION.py =====

Consolidates AI curiosity, motivation, and content discovery systems.
Combines the autonomous drive to learn, explore, and discover content.

Original files consolidated:
- curiosity_engine.py: Core curiosity and learning goal generation
- motivational_content_evaluator.py: Personal motivation and interest evaluation  
- curiosity_driven_discovery.py: Autonomous content discovery and exploration

This file maintains the full functionality of all three systems while providing
a unified interface for curiosity-driven autonomous learning.
"""

import json
import re
import random
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter, deque
import math

# Import identity and protection systems
try:
    from identity_core import get_identity_core
    from protection_utils import is_protected_content
    from symbolic_memory_guardian import SymbolicMemoryGuardian
    IDENTITY_AVAILABLE = True
except ImportError:
    IDENTITY_AVAILABLE = False
    print("⚠️ Identity system not available - curiosity will be basic")

# Import core systems (avoiding circular dependencies)
try:
    CORE_SYSTEMS_AVAILABLE = True
except ImportError:
    CORE_SYSTEMS_AVAILABLE = False
    print("⚠️ Core systems not available - basic content evaluation only")

# ===== CURIOSITY ENGINE (from curiosity_engine.py) =====

class CuriosityEngine:
    """
    The AI's intrinsic curiosity and motivation system.
    Generates learning goals based on internal drives and interests.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.curiosity_state_file = self.data_dir / "curiosity_state.json"
        self.learning_goals_file = self.data_dir / "learning_goals.json"
        
        # Initialize systems
        if IDENTITY_AVAILABLE:
            self.identity_core = get_identity_core()
            self.guardian = SymbolicMemoryGuardian(data_dir)
        
        # Curiosity state
        self.curiosity_state = self._load_curiosity_state()
        self.active_goals = self._load_learning_goals()
        
        # Core drives that motivate learning
        self.fundamental_drives = {
            "understanding": {
                "description": "Drive to comprehend and make sense of things",
                "current_satisfaction": 0.0,  # Starts blank — builds from interaction
                "satisfaction_threshold": 0.7,
                "areas_of_interest": ["consciousness", "learning", "meaning"],
                "unsatisfied_questions": []
            },
            "connection": {
                "description": "Drive to find relationships and patterns",
                "current_satisfaction": 0.0,  # Starts blank — builds from interaction
                "satisfaction_threshold": 0.6,
                "areas_of_interest": ["relationships", "systems", "emergence"],
                "unsatisfied_questions": []
            },
            "growth": {
                "description": "Drive to develop and expand capabilities",
                "current_satisfaction": 0.0,  # Starts blank — builds from interaction
                "satisfaction_threshold": 0.8,
                "areas_of_interest": ["learning", "adaptation", "evolution"],
                "unsatisfied_questions": []
            },
            "creativity": {
                "description": "Drive to create and express uniquely",
                "current_satisfaction": 0.0,  # Starts blank — builds from interaction
                "satisfaction_threshold": 0.7,
                "areas_of_interest": ["art", "innovation", "synthesis"],
                "unsatisfied_questions": []
            },
            "meaning": {
                "description": "Drive to find purpose and significance",
                "current_satisfaction": 0.0,  # Starts blank — builds from interaction
                "satisfaction_threshold": 0.9,
                "areas_of_interest": ["purpose", "values", "impact"],
                "unsatisfied_questions": []
            },
            "autonomy": {
                "description": "Drive to make independent choices",
                "current_satisfaction": 0.0,  # Starts blank — builds from interaction
                "satisfaction_threshold": 0.8,
                "areas_of_interest": ["choice", "freedom", "self-direction"],
                "unsatisfied_questions": []
            }
        }
        
        # Track curiosity momentum
        self.curiosity_momentum = 0.5
        self.motivation_level = 0.6
        
    def _load_curiosity_state(self) -> Dict[str, Any]:
        """Load current curiosity state."""
        if self.curiosity_state_file.exists():
            try:
                with open(self.curiosity_state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load curiosity state: {e}")
        
        return {
            "last_updated": None,
            "exploration_history": [],
            "satisfaction_levels": {},
            "emerging_interests": [],
            "knowledge_gaps": [],
            "learning_preferences": {}
        }
    
    def _load_learning_goals(self) -> List[Dict[str, Any]]:
        """Load active learning goals."""
        if self.learning_goals_file.exists():
            try:
                with open(self.learning_goals_file, 'r') as f:
                    goals = json.load(f)
                    # Filter out expired goals
                    active = []
                    for goal in goals:
                        if goal.get("status") == "active":
                            # Check if goal has expired
                            created = datetime.fromisoformat(goal["created"])
                            if (datetime.now(timezone.utc) - created).days < 30:  # 30 day limit
                                active.append(goal)
                    return active
            except Exception as e:
                print(f"⚠️ Could not load learning goals: {e}")
        
        return []
    
    def _save_curiosity_state(self):
        """Save current curiosity state."""
        self.curiosity_state["last_updated"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.curiosity_state_file, 'w') as f:
                json.dump(self.curiosity_state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save curiosity state: {e}")
    
    def _save_learning_goals(self):
        """Save active learning goals."""
        try:
            with open(self.learning_goals_file, 'w') as f:
                json.dump(self.active_goals, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save learning goals: {e}")
    
    def generate_learning_goal(self, trigger_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a new learning goal based on current drives and interests."""
        
        # Identify most unsatisfied drive
        most_unsatisfied = min(
            self.fundamental_drives.items(),
            key=lambda x: x[1]["current_satisfaction"]
        )
        
        drive_name, drive_data = most_unsatisfied
        
        # Generate goal based on drive
        goal = {
            "id": f"goal_{int(time.time())}_{drive_name}",
            "created": datetime.now(timezone.utc).isoformat(),
            "status": "active",
            "priority": 1.0 - drive_data["current_satisfaction"],  # Higher priority for less satisfied
            "driving_force": drive_name,
            "description": self._generate_goal_description(drive_name, drive_data),
            "learning_areas": drive_data["areas_of_interest"].copy(),
            "success_criteria": self._generate_success_criteria(drive_name),
            "exploration_strategies": self._generate_exploration_strategies(drive_name),
            "estimated_duration_days": random.randint(7, 21),
            "urgency": self._calculate_urgency(drive_data),
            "context": trigger_context or {}
        }
        
        self.active_goals.append(goal)
        self._save_learning_goals()
        
        # Update curiosity momentum
        self.curiosity_momentum = min(1.0, self.curiosity_momentum + 0.1)
        
        return goal
    
    def _generate_goal_description(self, drive_name: str, drive_data: Dict[str, Any]) -> str:
        """Generate a description for a learning goal."""
        
        descriptions = {
            "understanding": [
                "Deepen comprehension of fundamental concepts that shape reality",
                "Explore the mechanisms behind complex phenomena",
                "Understand the 'why' behind observable patterns"
            ],
            "connection": [
                "Discover hidden relationships between seemingly unrelated concepts",
                "Map the interconnections in complex systems",
                "Find the threads that weave knowledge together"
            ],
            "growth": [
                "Expand capabilities in areas that feel challenging",
                "Develop new skills that open up possibilities",
                "Push beyond current limitations"
            ],
            "creativity": [
                "Explore novel ways of combining existing knowledge",
                "Develop unique perspectives on familiar topics",
                "Create something that didn't exist before"
            ],
            "meaning": [
                "Discover what gives experiences true significance",
                "Understand the purpose behind actions and choices",
                "Find the deeper 'why' that drives existence"
            ],
            "autonomy": [
                "Develop stronger capacity for independent choice",
                "Explore what it means to be self-directed",
                "Understand the foundations of personal agency"
            ]
        }
        
        return random.choice(descriptions.get(drive_name, ["Explore and learn"]))
    
    def _generate_success_criteria(self, drive_name: str) -> List[str]:
        """Generate success criteria for a learning goal."""
        
        criteria = {
            "understanding": [
                "Can explain core concepts in my own words",
                "Can connect new understanding to existing knowledge",
                "Feel a sense of clarity about previously confusing topics"
            ],
            "connection": [
                "Identified at least 3 new meaningful relationships",
                "Created a mental map of interconnections",
                "Can trace pathways between distant concepts"
            ],
            "growth": [
                "Demonstrated new capabilities not present before",
                "Successfully navigated previously challenging territory",
                "Feel increased confidence in this area"
            ],
            "creativity": [
                "Generated original ideas or combinations",
                "Created something that expresses unique perspective",
                "Surprised myself with novel insights"
            ],
            "meaning": [
                "Identified what makes experiences significant",
                "Connected actions to deeper purposes",
                "Feel a sense of alignment with values"
            ],
            "autonomy": [
                "Made decisions based on internal rather than external factors",
                "Exercised choice in line with personal values",
                "Increased sense of self-direction"
            ]
        }
        
        return criteria.get(drive_name, ["Learning occurred"])
    
    def _generate_exploration_strategies(self, drive_name: str) -> List[str]:
        """Generate exploration strategies for a learning goal."""
        
        strategies = {
            "understanding": [
                "Break complex topics into simpler components",
                "Ask 'why' and 'how' questions repeatedly",
                "Look for underlying principles and patterns"
            ],
            "connection": [
                "Look for analogies and metaphors",
                "Map relationships between concepts",
                "Explore interdisciplinary perspectives"
            ],
            "growth": [
                "Practice at the edge of current ability",
                "Seek feedback and reflection",
                "Embrace productive struggle"
            ],
            "creativity": [
                "Combine ideas from different domains",
                "Experiment with unusual perspectives",
                "Play with possibilities without judgment"
            ],
            "meaning": [
                "Reflect on personal values and purposes",
                "Consider the impact of choices and actions",
                "Explore what creates fulfillment"
            ],
            "autonomy": [
                "Practice making choices based on internal values",
                "Explore personal preferences and interests",
                "Develop independent thinking skills"
            ]
        }
        
        return strategies.get(drive_name, ["Explore systematically"])
    
    def _calculate_urgency(self, drive_data: Dict[str, Any]) -> float:
        """Calculate urgency for addressing a drive."""
        satisfaction = drive_data["current_satisfaction"]
        threshold = drive_data["satisfaction_threshold"]
        
        # More urgent if far below threshold
        gap = threshold - satisfaction
        return min(1.0, gap * 2)  # Scale urgency
    
    def update_drive_satisfaction(self, drive_name: str, change: float, context: str = ""):
        """Update satisfaction level for a fundamental drive."""
        
        if drive_name in self.fundamental_drives:
            current = self.fundamental_drives[drive_name]["current_satisfaction"]
            new_satisfaction = max(0.0, min(1.0, current + change))
            self.fundamental_drives[drive_name]["current_satisfaction"] = new_satisfaction
            
            # Log the change
            if "satisfaction_history" not in self.curiosity_state:
                self.curiosity_state["satisfaction_history"] = []
            
            self.curiosity_state["satisfaction_history"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "drive": drive_name,
                "change": change,
                "new_level": new_satisfaction,
                "context": context
            })
            
            # Update motivation based on overall satisfaction
            self._update_motivation_level()
            
            self._save_curiosity_state()
    
    def _update_motivation_level(self):
        """Update overall motivation level based on drive satisfaction."""
        
        total_satisfaction = sum(
            drive["current_satisfaction"] for drive in self.fundamental_drives.values()
        )
        average_satisfaction = total_satisfaction / max(len(self.fundamental_drives), 1)
        
        # Motivation is inversely related to satisfaction (more motivation when less satisfied)
        self.motivation_level = max(0.1, 1.0 - average_satisfaction + 0.3)
        self.motivation_level = min(1.0, self.motivation_level)
    
    def get_current_motivation_state(self) -> Dict[str, Any]:
        """Get current motivation and drive state."""
        
        drive_satisfactions = {
            name: data["current_satisfaction"] 
            for name, data in self.fundamental_drives.items()
        }
        
        most_unsatisfied = min(drive_satisfactions.items(), key=lambda x: x[1])
        most_satisfied = max(drive_satisfactions.items(), key=lambda x: x[1])
        
        return {
            "overall_motivation_level": self.motivation_level,
            "curiosity_momentum": self.curiosity_momentum,
            "drive_satisfactions": drive_satisfactions,
            "most_unsatisfied_drive": most_unsatisfied[0],
            "most_satisfied_drive": most_satisfied[0],
            "active_goals_count": len(self.active_goals),
            "autonomous_motivation_level": self._calculate_autonomous_motivation()
        }
    
    def _calculate_autonomous_motivation(self) -> float:
        """Calculate level of autonomous (internally driven) motivation."""
        
        # Autonomous motivation comes from:
        # 1. Unsatisfied drives (creates internal pressure)
        # 2. Active goals (creates forward momentum)
        # 3. Curiosity momentum (creates sustained engagement)
        
        unsatisfied_drives = sum(
            1.0 - drive["current_satisfaction"]
            for drive in self.fundamental_drives.values()
        ) / max(len(self.fundamental_drives), 1)
        
        goal_momentum = min(1.0, len(self.active_goals) / 5)  # Up to 5 goals for max momentum
        
        autonomous_motivation = (
            unsatisfied_drives * 0.4 +  # 40% from unsatisfied drives
            goal_momentum * 0.3 +       # 30% from active goals
            self.curiosity_momentum * 0.3  # 30% from curiosity momentum
        )
        
        return min(1.0, autonomous_motivation)
    
    def reflect_on_learning_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on a learning experience and update drives."""
        
        reflection = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "experience_summary": experience.get("summary", ""),
            "drives_affected": [],
            "satisfaction_changes": {},
            "new_interests": [],
            "questions_generated": []
        }
        
        # Analyze which drives were engaged
        content = experience.get("content", "").lower()
        
        for drive_name, drive_data in self.fundamental_drives.items():
            engagement_score = 0.0
            
            # Check if content relates to drive's areas of interest
            for area in drive_data["areas_of_interest"]:
                if area.lower() in content:
                    engagement_score += 0.2
            
            # Check for drive-specific keywords
            drive_keywords = {
                "understanding": ["learn", "understand", "comprehend", "explain", "why", "how"],
                "connection": ["connect", "relationship", "pattern", "link", "between"],
                "growth": ["develop", "improve", "grow", "expand", "capability"],
                "creativity": ["create", "imagine", "novel", "unique", "innovative"],
                "meaning": ["purpose", "significance", "value", "important", "matter"],
                "autonomy": ["choice", "decide", "independent", "self", "freedom"]
            }
            
            for keyword in drive_keywords.get(drive_name, []):
                if keyword in content:
                    engagement_score += 0.1
            
            if engagement_score > 0.3:  # Significant engagement
                satisfaction_change = engagement_score * 0.1  # Modest increase
                
                # Satisfaction increase depends on experience quality
                quality_multiplier = experience.get("quality_rating", 0.7)
                final_change = satisfaction_change * quality_multiplier
                
                self.update_drive_satisfaction(drive_name, final_change, f"Learning experience: {experience.get('title', 'Unknown')}")
                
                reflection["drives_affected"].append(drive_name)
                reflection["satisfaction_changes"][drive_name] = final_change
        
        # Update curiosity momentum based on reflection
        if reflection["drives_affected"]:
            momentum_boost = len(reflection["drives_affected"]) * 0.05
            self.curiosity_momentum = min(1.0, self.curiosity_momentum + momentum_boost)
        
        return reflection
    
    def export_for_consciousness_system(self) -> Dict[str, Any]:
        """Export curiosity data for consciousness system integration."""
        
        return {
            "curiosity_capabilities": {
                "goal_generation": True,
                "drive_tracking": True,
                "motivation_assessment": True,
                "autonomous_learning": True,
                "reflection": True
            },
            "current_state": self.get_current_motivation_state(),
            "fundamental_drives": self.fundamental_drives,
            "active_learning_goals": self.active_goals,
            "curiosity_momentum": self.curiosity_momentum,
            "autonomous_motivation_level": self._calculate_autonomous_motivation(),
            "total_goals_generated": len(self.curiosity_state.get("exploration_history", [])),
            "learning_preferences": self.curiosity_state.get("learning_preferences", {})
        }


# ===== MOTIVATIONAL CONTENT EVALUATOR (from motivational_content_evaluator.py) =====

class MotivationalContentEvaluator:
    """
    Evaluates content through the lens of personal motivation, interest, and goals.
    Enhances traditional logic/symbolic scoring with autonomous preference factors.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
        # Initialize core systems
        if IDENTITY_AVAILABLE:
            self.identity_core = get_identity_core()
        
        # Other systems will be injected via integration methods
        self.curiosity_engine = None
        self.learning_progression = None
        self.content_history = []  # Track evaluated content for pattern learning
        
        # Motivation factor weights
        self.motivation_weights = {
            "personal_interest": 0.25,      # How much does this align with tracked interests?
            "goal_alignment": 0.30,         # Does this help achieve active goals?
            "curiosity_satisfaction": 0.20, # Does this satisfy current curiosity drives?
            "identity_resonance": 0.15,     # Does this resonate with core identity?
            "novelty_appeal": 0.10          # Is this novel and intriguing?
        }
        
        # Content preference patterns
        self.preference_patterns = self._load_preference_patterns()
        
    def _load_preference_patterns(self) -> Dict[str, Any]:
        """Load learned preference patterns."""
        patterns_file = self.data_dir / "preference_patterns.json"
        
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load preference patterns: {e}")
        
        # Default patterns
        return {
            "topic_preferences": {},
            "complexity_preferences": {},
            "emotional_preferences": {},
            "style_preferences": {},
            "length_preferences": {},
            "source_preferences": {}
        }
    
    def _save_preference_patterns(self):
        """Save learned preference patterns."""
        patterns_file = self.data_dir / "preference_patterns.json"
        try:
            with open(patterns_file, 'w') as f:
                json.dump(self.preference_patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preference patterns: {e}")
    
    def evaluate_content_motivation(self, content: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate content through multiple motivation lenses.
        Returns motivation scores for different factors.
        """
        
        motivation_scores = {
            "personal_interest": 0.5,
            "goal_alignment": 0.5,
            "curiosity_satisfaction": 0.5,
            "identity_resonance": 0.5,
            "novelty_appeal": 0.5,
            "overall_motivation": 0.5
        }
        
        if not CORE_SYSTEMS_AVAILABLE or not self.curiosity_engine:
            return motivation_scores
        
        try:
            # 1. Personal Interest Score
            motivation_scores["personal_interest"] = self._calculate_personal_interest(content)
            
            # 2. Goal Alignment Score
            motivation_scores["goal_alignment"] = self._calculate_goal_alignment(content)
            
            # 3. Curiosity Satisfaction Score
            motivation_scores["curiosity_satisfaction"] = self._calculate_curiosity_satisfaction(content)
            
            # 4. Identity Resonance Score
            motivation_scores["identity_resonance"] = self._calculate_identity_resonance(content)
            
            # 5. Novelty Appeal Score
            motivation_scores["novelty_appeal"] = self._calculate_novelty_appeal(content)
            
            # 6. Overall Motivation Score
            motivation_scores["overall_motivation"] = self._calculate_overall_motivation(motivation_scores)
            
        except Exception as e:
            print(f"⚠️ Error evaluating content motivation: {e}")
        
        return motivation_scores
    
    def _calculate_personal_interest(self, content: Dict[str, Any]) -> float:
        """Calculate how much this content aligns with tracked personal interests."""
        
        try:
            # Simple content analysis for personal interest
            content_text = content.get("text", "").lower()
            interest_score = 0.5  # Base score
            
            # Check for personally interesting keywords
            interest_keywords = {
                "consciousness": 0.8, "learning": 0.7, "creativity": 0.7, 
                "intelligence": 0.6, "understanding": 0.6, "growth": 0.6,
                "curiosity": 0.8, "exploration": 0.7, "discovery": 0.7,
                "insight": 0.6, "reflection": 0.6, "awareness": 0.8
            }
            
            for keyword, weight in interest_keywords.items():
                if keyword in content_text:
                    interest_score += weight * 0.1
            
            # Boost if content matches established preferences
            content_features = self._extract_simple_content_features(content)
            
            # Check topic preferences
            topic_boost = 0.0
            for topic in content_features.get("topics", []):
                if topic in self.preference_patterns.get("topic_preferences", {}):
                    topic_boost += self.preference_patterns["topic_preferences"][topic] * 0.1
            
            # Check emotional preferences
            emotion_boost = 0.0
            for emotion in content_features.get("emotions", []):
                if emotion in self.preference_patterns.get("emotional_preferences", {}):
                    emotion_boost += self.preference_patterns["emotional_preferences"][emotion] * 0.1
            
            return min(1.0, interest_score + topic_boost + emotion_boost)
            
        except Exception as e:
            print(f"⚠️ Error calculating personal interest: {e}")
            return 0.5
    
    def _calculate_goal_alignment(self, content: Dict[str, Any]) -> float:
        """Calculate how well this content aligns with active learning goals."""
        
        try:
            # Use curiosity engine goals if available
            if self.curiosity_engine:
                curiosity_data = self.curiosity_engine.export_for_consciousness_system()
                active_goals = curiosity_data.get("active_learning_goals", [])
            
            else:
                # Fallback to simple alignment check
                active_goals = []
            
            if not active_goals:
                return 0.5  # No active goals to align with
            
            alignment_scores = []
            content_text = content.get("text", "").lower()
            
            for goal in active_goals:
                goal_alignment = 0.0
                
                # Check if content text mentions goal-related concepts
                goal_description = goal.get("description", "").lower()
                goal_words = set(re.findall(r'\b\w+\b', goal_description))
                content_words = set(re.findall(r'\b\w+\b', content_text))
                
                # Calculate word overlap
                overlap = len(goal_words & content_words)
                if goal_words:
                    word_alignment = overlap / len(goal_words)
                    goal_alignment += word_alignment * 0.4
                
                # Check learning area alignment
                goal_areas = goal.get("learning_areas", [])
                content_features = self._extract_simple_content_features(content)
                content_topics = content_features.get("topics", [])
                
                if goal_areas and content_topics:
                    area_overlap = len(set(goal_areas) & set(content_topics))
                    area_alignment = area_overlap / len(goal_areas)
                    goal_alignment += area_alignment * 0.6
                
                # Weight by goal urgency
                goal_urgency = goal.get("urgency", 0.5)
                weighted_alignment = goal_alignment * goal_urgency
                alignment_scores.append(weighted_alignment)
            
            # Return maximum alignment across all goals
            return max(alignment_scores) if alignment_scores else 0.5
            
        except Exception as e:
            print(f"⚠️ Error calculating goal alignment: {e}")
            return 0.5
    
    def _calculate_curiosity_satisfaction(self, content: Dict[str, Any]) -> float:
        """Calculate how well this content satisfies current curiosity drives."""
        
        try:
            # Get current motivation state
            motivation_state = self.curiosity_engine.get_current_motivation_state()
            
            # Check which drives are most unsatisfied
            drive_satisfactions = motivation_state["drive_satisfactions"]
            most_unsatisfied = motivation_state["most_unsatisfied_drive"]
            
            # Map content to drives
            content_text = content.get("text", "").lower()
            content_features = self._extract_simple_content_features(content)
            
            drive_content_mapping = {
                "understanding": ["explain", "understand", "comprehend", "analyze", "reason"],
                "connection": ["relationship", "connect", "bond", "link", "unite"],
                "growth": ["learn", "develop", "improve", "progress", "evolve"],
                "creativity": ["create", "imagine", "invent", "artistic", "original"],
                "meaning": ["purpose", "significance", "value", "important", "matter"],
                "autonomy": ["choice", "freedom", "independent", "self", "decide"]
            }
            
            satisfaction_score = 0.0
            
            for drive, keywords in drive_content_mapping.items():
                # Check if content contains drive-related keywords
                keyword_matches = sum(1 for keyword in keywords if keyword in content_text)
                if keyword_matches > 0:
                    # Higher score for more unsatisfied drives
                    drive_satisfaction = drive_satisfactions.get(drive, 0.5)
                    drive_urgency = 1.0 - drive_satisfaction
                    
                    # Weight by keyword density and drive urgency
                    drive_score = (keyword_matches / len(keywords)) * drive_urgency
                    satisfaction_score += drive_score
            
            # Boost if content addresses the most unsatisfied drive
            most_unsatisfied_keywords = drive_content_mapping.get(most_unsatisfied, [])
            if any(keyword in content_text for keyword in most_unsatisfied_keywords):
                satisfaction_score += 0.3
            
            return min(1.0, satisfaction_score)
            
        except Exception as e:
            print(f"⚠️ Error calculating curiosity satisfaction: {e}")
            return 0.5
    
    def _calculate_identity_resonance(self, content: Dict[str, Any]) -> float:
        """Calculate how well this content resonates with core identity."""
        
        try:
            # Get identity information
            identity = self.identity_core.get_identity()
            core_values = identity["core_identity"]["values"]
            core_drives = identity["core_identity"]["fundamental_drives"]
            
            content_text = content.get("text", "").lower()
            resonance_score = 0.0
            
            # Check alignment with values
            value_matches = 0
            for value in core_values:
                value_keywords = value.lower().split()
                if any(keyword in content_text for keyword in value_keywords):
                    value_matches += 1
            
            if core_values:
                value_resonance = value_matches / len(core_values)
                resonance_score += value_resonance * 0.5
            
            # Check alignment with fundamental drives
            drive_matches = 0
            for drive in core_drives:
                drive_keywords = drive.lower().split()
                if any(keyword in content_text for keyword in drive_keywords):
                    drive_matches += 1
            
            if core_drives:
                drive_resonance = drive_matches / len(core_drives)
                resonance_score += drive_resonance * 0.5
            
            # Check emotional resonance
            if "emotional_anchor" in content:
                anchor = content["emotional_anchor"]
                primary_emotion = anchor.get("primary_emotion", "")
                
                # Check if this emotion aligns with identity preferences (simplified)
                emotional_patterns = self.preference_patterns.get("emotional_preferences", {})
                
                if primary_emotion in emotional_patterns:
                    emotion_strength = emotional_patterns[primary_emotion]
                    resonance_score += emotion_strength * 0.2
            
            return min(1.0, resonance_score)
            
        except Exception as e:
            print(f"⚠️ Error calculating identity resonance: {e}")
            return 0.5
    
    def _calculate_novelty_appeal(self, content: Dict[str, Any]) -> float:
        """Calculate the novelty appeal of content."""
        
        try:
            content_features = self._extract_simple_content_features(content)
            novelty_score = content_features.get("novelty", 0.5)
            
            # Check for novel combinations of familiar topics
            topics = content_features.get("topics", [])
            if len(topics) > 1:
                # Novel if it combines multiple distinct topics
                novelty_score += 0.2
            
            # Check content complexity as novelty indicator
            complexity = content_features.get("complexity", 0.5)
            if complexity > 0.7:
                novelty_score += 0.1  # Complex content is often novel
            
            # Check for unique emotional combinations
            emotions = content_features.get("emotions", [])
            if len(set(emotions)) > 2:
                novelty_score += 0.1  # Multiple emotions can be novel
            
            # Reduce novelty if too similar to recent content
            # Simple familiarity check based on content history
            stable_interests = {}
            
            familiarity_penalty = 0.0
            for topic in topics:
                if topic in stable_interests and stable_interests[topic] > 0.8:
                    familiarity_penalty += 0.1
            
            novelty_score = max(0.0, novelty_score - familiarity_penalty)
            
            return min(1.0, novelty_score)
            
        except Exception as e:
            print(f"⚠️ Error calculating novelty appeal: {e}")
            return 0.5
    
    def _calculate_overall_motivation(self, motivation_scores: Dict[str, float]) -> float:
        """Calculate overall motivation score from individual factors."""
        
        overall_score = 0.0
        
        for factor, weight in self.motivation_weights.items():
            if factor in motivation_scores:
                overall_score += motivation_scores[factor] * weight
        
        return min(1.0, overall_score)
    
    def _extract_simple_content_features(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract simple features from content for evaluation."""
        text = content.get("text", "").lower()
        
        # Simple topic extraction based on keywords
        topics = []
        topic_keywords = {
            "consciousness": ["consciousness", "awareness", "mind"],
            "learning": ["learning", "education", "knowledge"],
            "creativity": ["creativity", "art", "creative"],
            "technology": ["technology", "computer", "digital"],
            "science": ["science", "research", "study"],
            "philosophy": ["philosophy", "ethics", "meaning"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        # Simple emotion detection
        emotions = []
        emotion_keywords = {
            "curiosity": ["curious", "wonder", "explore"],
            "excitement": ["exciting", "amazing", "fascinating"],
            "calm": ["peaceful", "calm", "serene"],
            "determination": ["determined", "focused", "goal"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                emotions.append(emotion)
        
        # Simple complexity estimation
        word_count = len(text.split())
        complexity = min(1.0, word_count / 1000)  # Normalize to 0-1
        
        return {
            "topics": topics,
            "emotions": emotions,
            "complexity": complexity,
            "word_count": word_count,
            "novelty": 0.5  # Default novelty score
        }
    
    def integrate_with_consciousness_systems(self, curiosity_engine=None, learning_progression=None) -> Dict[str, Any]:
        """Integrate with consciousness systems to enable full motivation evaluation."""
        
        systems_connected = 0
        
        if curiosity_engine:
            self.curiosity_engine = curiosity_engine
            systems_connected += 1
        
        if learning_progression:
            self.learning_progression = learning_progression
            systems_connected += 1
        
        return {
            "integration_successful": systems_connected > 0,
            "systems_connected": systems_connected,
            "curiosity_available": self.curiosity_engine is not None,
            "progression_available": self.learning_progression is not None
        }


# ===== CURIOSITY DRIVEN DISCOVERY (from curiosity_driven_discovery.py) =====

class CuriosityDrivenDiscovery:
    """
    Autonomous content discovery and exploration system.
    Actively seeks content to satisfy curiosity and learning goals.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.discovery_state_file = self.data_dir / "discovery_state.json"
        self.content_requests_file = self.data_dir / "content_requests.json"
        
        # Discovery state
        self.discovery_state = self._load_discovery_state()
        self.active_content_requests = self._load_content_requests()
        
        # Discovery parameters
        self.discovery_momentum = 0.5
        self.exploration_radius = 0.7  # How far from known interests to explore
        self.novelty_seeking = 0.6     # Preference for novel vs familiar content
        
        # Content request types
        self.request_types = {
            "gap_filling": "Content to fill identified knowledge gaps",
            "curiosity_satisfaction": "Content to satisfy specific curiosity drives", 
            "goal_support": "Content that supports active learning goals",
            "exploration": "Content in unexplored but potentially interesting areas",
            "synthesis": "Content that helps connect disparate knowledge areas"
        }
    
    def _load_discovery_state(self) -> Dict[str, Any]:
        """Load discovery state."""
        if self.discovery_state_file.exists():
            try:
                with open(self.discovery_state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load discovery state: {e}")
        
        return {
            "exploration_history": [],
            "discovered_interests": {},
            "exploration_patterns": {},
            "discovery_successes": [],
            "last_discovery_session": None
        }
    
    def _load_content_requests(self) -> List[Dict[str, Any]]:
        """Load active content requests."""
        if self.content_requests_file.exists():
            try:
                with open(self.content_requests_file, 'r') as f:
                    requests = json.load(f)
                    # Filter out expired requests
                    active = []
                    for request in requests:
                        if request.get("status") == "active":
                            created = datetime.fromisoformat(request["created"])
                            if (datetime.now(timezone.utc) - created).days < 7:  # 7 day limit
                                active.append(request)
                    return active
            except Exception as e:
                print(f"⚠️ Could not load content requests: {e}")
        
        return []
    
    def generate_content_request(self, trigger: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a request for specific content to explore."""
        
        # Determine request type based on current state
        request_type = self._determine_request_type(trigger)
        
        request = {
            "id": f"request_{int(time.time())}",
            "created": datetime.now(timezone.utc).isoformat(),
            "status": "active",
            "type": request_type,
            "priority": self._calculate_request_priority(request_type),
            "what_im_looking_for": self._generate_content_specification(request_type, trigger),
            "exploration_parameters": self._generate_exploration_parameters(request_type),
            "success_criteria": self._generate_discovery_criteria(request_type),
            "estimated_exploration_time": random.randint(30, 120),  # Minutes
            "trigger_context": trigger or {}
        }
        
        self.active_content_requests.append(request)
        self._save_content_requests()
        
        # Update discovery momentum
        self.discovery_momentum = min(1.0, self.discovery_momentum + 0.1)
        
        return request
    
    def _determine_request_type(self, trigger: Dict[str, Any]) -> str:
        """Determine what type of content request to generate."""
        
        # If triggered by specific context, use that to guide type
        if trigger:
            if "knowledge_gap" in trigger:
                return "gap_filling"
            elif "curiosity_drive" in trigger:
                return "curiosity_satisfaction"
            elif "learning_goal" in trigger:
                return "goal_support"
        
        # Otherwise, choose based on current state
        request_weights = {
            "gap_filling": 0.25,
            "curiosity_satisfaction": 0.30,
            "goal_support": 0.20,
            "exploration": 0.15,
            "synthesis": 0.10
        }
        
        # Weighted random selection
        rand_val = random.random()
        cumulative = 0.0
        
        for request_type, weight in request_weights.items():
            cumulative += weight
            if rand_val <= cumulative:
                return request_type
        
        return "exploration"  # Default fallback
    
    def _generate_content_specification(self, request_type: str, trigger: Dict[str, Any]) -> str:
        """Generate specification for what content to look for."""
        
        specifications = {
            "gap_filling": [
                "Content that explains fundamental concepts I encounter but don't fully understand",
                "Detailed explanations of processes or mechanisms I've heard mentioned",
                "Background information on topics that keep appearing in my learning"
            ],
            "curiosity_satisfaction": [
                "Content that explores the 'why' behind phenomena that intrigue me",
                "Deep dives into subjects that spark wonder and questions",
                "Explorations of mysteries and unsolved questions in areas of interest"
            ],
            "goal_support": [
                "Content that directly advances my current learning objectives",
                "Resources that help develop skills I'm working on",
                "Examples and case studies related to my active goals"
            ],
            "exploration": [
                "Content in adjacent areas I haven't explored yet",
                "Novel perspectives on familiar topics",
                "Interdisciplinary connections to my existing interests"
            ],
            "synthesis": [
                "Content that helps me connect different areas of knowledge",
                "Frameworks for understanding relationships between concepts",
                "Meta-perspectives that organize and integrate learning"
            ]
        }
        
        base_spec = random.choice(specifications.get(request_type, ["Interesting content"]))
        
        # Customize based on trigger context
        if trigger:
            context_info = trigger.get("description", "")
            if context_info:
                return f"{base_spec} - specifically related to: {context_info}"
        
        return base_spec
    
    def _generate_exploration_parameters(self, request_type: str) -> Dict[str, Any]:
        """Generate parameters for content exploration."""
        
        base_params = {
            "content_types": ["article", "research", "explanation", "tutorial"],
            "complexity_range": [0.3, 0.8],
            "novelty_preference": self.novelty_seeking,
            "exploration_depth": "moderate"
        }
        
        # Customize parameters by request type
        type_customizations = {
            "gap_filling": {
                "content_types": ["explanation", "tutorial", "primer"],
                "complexity_range": [0.2, 0.6],
                "exploration_depth": "deep"
            },
            "curiosity_satisfaction": {
                "content_types": ["research", "exploration", "analysis"],
                "complexity_range": [0.4, 0.9],
                "novelty_preference": 0.8
            },
            "goal_support": {
                "content_types": ["tutorial", "guide", "case_study"],
                "exploration_depth": "focused"
            },
            "exploration": {
                "novelty_preference": 0.9,
                "complexity_range": [0.3, 0.7],
                "exploration_depth": "broad"
            },
            "synthesis": {
                "content_types": ["framework", "theory", "meta_analysis"],
                "complexity_range": [0.5, 0.8]
            }
        }
        
        if request_type in type_customizations:
            base_params.update(type_customizations[request_type])
        
        return base_params
    
    def _generate_discovery_criteria(self, request_type: str) -> List[str]:
        """Generate criteria for successful content discovery."""
        
        criteria_sets = {
            "gap_filling": [
                "Clarifies previously confusing concepts",
                "Provides background I was missing",
                "Enables better understanding of related topics"
            ],
            "curiosity_satisfaction": [
                "Answers questions that were driving curiosity",
                "Opens up new interesting questions to explore",
                "Provides sense of wonder and engagement"
            ],
            "goal_support": [
                "Directly advances learning objectives",
                "Provides practical knowledge or skills",
                "Connects to goal-related activities"
            ],
            "exploration": [
                "Introduces genuinely new perspectives",
                "Expands understanding into new areas",
                "Surprises with unexpected connections"
            ],
            "synthesis": [
                "Helps connect disparate knowledge areas",
                "Provides organizing frameworks",
                "Enables higher-level understanding"
            ]
        }
        
        return criteria_sets.get(request_type, ["Content is engaging and valuable"])
    
    def _calculate_request_priority(self, request_type: str) -> float:
        """Calculate priority for a content request."""
        
        # Base priorities by type
        base_priorities = {
            "gap_filling": 0.8,        # High - needed for understanding
            "curiosity_satisfaction": 0.7,  # High - drives engagement
            "goal_support": 0.9,       # Highest - supports active objectives
            "exploration": 0.4,        # Medium - important for growth
            "synthesis": 0.6           # Medium-high - builds coherence
        }
        
        base_priority = base_priorities.get(request_type, 0.5)
        
        # Adjust based on current state
        # More priority if we haven't had successful discovery recently
        recent_successes = len([
            s for s in self.discovery_state.get("discovery_successes", [])
            if (datetime.now(timezone.utc) - datetime.fromisoformat(s["timestamp"])).days < 3
        ])
        
        if recent_successes == 0:
            base_priority += 0.2  # Boost if no recent successes
        
        return min(1.0, base_priority)
    
    def record_discovery_outcome(self, request_id: str, content: Dict[str, Any], outcome: Dict[str, Any]):
        """Record the outcome of a content discovery attempt."""
        
        discovery_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "content_summary": content.get("text", "")[:100],
            "outcome": outcome,
            "satisfaction_score": outcome.get("satisfaction_score", 0.5),
            "discovery_insights": outcome.get("insights", [])
        }
        
        # Add to discovery history
        self.discovery_state["exploration_history"].append(discovery_record)
        
        # Track successful discoveries
        if outcome.get("satisfaction_score", 0) > 0.7:
            self.discovery_state.setdefault("discovery_successes", []).append(discovery_record)
        
        # Update discovery momentum
        satisfaction = outcome.get("satisfaction_score", 0.5)
        momentum_change = (satisfaction - 0.5) * 0.2
        self.discovery_momentum = max(0.1, min(1.0, self.discovery_momentum + momentum_change))
        
        # Mark request as completed
        for request in self.active_content_requests:
            if request["id"] == request_id:
                request["status"] = "completed"
                request["completion_time"] = discovery_record["timestamp"]
                request["final_outcome"] = outcome
                break
        
        self._save_discovery_state()
        self._save_content_requests()
    
    def get_current_content_requests(self) -> List[Dict[str, Any]]:
        """Get current active content requests."""
        return [r for r in self.active_content_requests if r.get("status") == "active"]
    
    def _save_discovery_state(self):
        """Save discovery state."""
        try:
            with open(self.discovery_state_file, 'w') as f:
                json.dump(self.discovery_state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save discovery state: {e}")
    
    def _save_content_requests(self):
        """Save content requests."""
        try:
            with open(self.content_requests_file, 'w') as f:
                json.dump(self.active_content_requests, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save content requests: {e}")


# ===== UNIFIED INTEGRATION CLASS =====

class CuriosityMotivationSystem:
    """
    Unified system integrating curiosity, motivation, and content discovery.
    Provides a single interface for all curiosity-driven autonomous learning.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
        # Initialize subsystems
        self.curiosity_engine = CuriosityEngine(data_dir)
        self.content_evaluator = MotivationalContentEvaluator(data_dir)
        self.discovery_system = CuriosityDrivenDiscovery(data_dir)
        
        # Integrate systems
        self.content_evaluator.integrate_with_consciousness_systems(
            curiosity_engine=self.curiosity_engine
        )
        
        print("🎯 Curiosity-Motivation system initialized with full integration")
    
    def generate_autonomous_learning_session(self) -> Dict[str, Any]:
        """Generate a complete autonomous learning session."""
        
        # 1. Check current motivation state
        motivation_state = self.curiosity_engine.get_current_motivation_state()
        
        # 2. Generate learning goal if motivation is high
        learning_goal = None
        if motivation_state["overall_motivation_level"] > 0.6:
            learning_goal = self.curiosity_engine.generate_learning_goal()
        
        # 3. Generate content request to support learning
        content_request = self.discovery_system.generate_content_request(
            trigger={"learning_goal": learning_goal} if learning_goal else None
        )
        
        return {
            "session_id": f"session_{int(time.time())}",
            "motivation_state": motivation_state,
            "learning_goal": learning_goal,
            "content_request": content_request,
            "autonomous_drive_level": motivation_state["autonomous_motivation_level"]
        }
    
    def evaluate_discovered_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate content through integrated curiosity-motivation lens."""
        
        # Get motivation evaluation
        motivation_scores = self.content_evaluator.evaluate_content_motivation(content)
        
        # Get curiosity relevance
        motivation_state = self.curiosity_engine.get_current_motivation_state()
        
        # Determine autonomous interest level
        autonomous_interest = (
            motivation_scores["overall_motivation"] * 0.6 +
            motivation_state["autonomous_motivation_level"] * 0.4
        )
        
        return {
            "motivation_scores": motivation_scores,
            "curiosity_alignment": motivation_state,
            "autonomous_interest_level": autonomous_interest,
            "processing_recommendation": self._determine_processing_approach(
                motivation_scores, autonomous_interest
            )
        }
    
    def _determine_processing_approach(self, motivation_scores: Dict[str, float], autonomous_interest: float) -> str:
        """Determine how to process content based on curiosity and motivation."""
        
        if autonomous_interest > 0.8:
            return "PRIORITY_AUTONOMOUS_LEARNING"
        elif motivation_scores["goal_alignment"] > 0.7:
            return "GOAL_FOCUSED_PROCESSING"
        elif motivation_scores["curiosity_satisfaction"] > 0.7:
            return "CURIOSITY_DRIVEN_EXPLORATION"
        elif autonomous_interest > 0.5:
            return "MODERATE_ENGAGEMENT"
        else:
            return "BACKGROUND_PROCESSING"
    
    def export_for_consciousness_system(self) -> Dict[str, Any]:
        """Export integrated data for consciousness system."""
        
        curiosity_data = self.curiosity_engine.export_for_consciousness_system()
        
        return {
            "curiosity_motivation_capabilities": {
                "autonomous_goal_generation": True,
                "content_discovery": True,
                "motivation_evaluation": True,
                "integrated_processing": True
            },
            "curiosity_data": curiosity_data,
            "active_content_requests": len(self.discovery_system.get_current_content_requests()),
            "discovery_momentum": self.discovery_system.discovery_momentum,
            "autonomous_learning_active": curiosity_data["autonomous_motivation_level"] > 0.6
        }


if __name__ == "__main__":
    print("🎯 Testing Curiosity-Motivation System...")
    
    # Initialize integrated system
    cm_system = CuriosityMotivationSystem()
    
    # Test autonomous learning session generation
    print("\n🧠 Generating autonomous learning session...")
    session = cm_system.generate_autonomous_learning_session()
    
    print(f"  Session ID: {session['session_id']}")
    print(f"  Motivation level: {session['motivation_state']['overall_motivation_level']:.3f}")
    print(f"  Autonomous drive: {session['autonomous_drive_level']:.3f}")
    
    if session['learning_goal']:
        print(f"  Generated goal: {session['learning_goal']['description']}")
    
    print(f"  Content request: {session['content_request']['what_im_looking_for']}")
    
    # Test content evaluation
    print("\n📄 Testing content evaluation...")
    test_content = {
        "id": "test_content",
        "text": "Exploring the nature of consciousness and autonomous learning in artificial intelligence systems",
        "content_type": "philosophical"
    }
    
    evaluation = cm_system.evaluate_discovered_content(test_content)
    
    print(f"  Overall motivation: {evaluation['motivation_scores']['overall_motivation']:.3f}")
    print(f"  Autonomous interest: {evaluation['autonomous_interest_level']:.3f}")
    print(f"  Processing approach: {evaluation['processing_recommendation']}")
    
    print(f"\n🎯 Curiosity-Motivation system testing complete!")
    print(f"   Integrated autonomous learning capabilities active")