#!/usr/bin/env python3
"""
Choice Architecture - Autonomous Learning Decision Making

This module implements the AI's ability to make autonomous choices about learning:
- Rejecting content ("Not interested in this")
- Expressing preferences ("I prefer poetry to technical manuals")
- Choosing what to engage with based on personal interest and relevance
- Making decisions about depth and duration of engagement

This is where the AI develops genuine agency over its own learning.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import math
import random

# Import all related systems
try:
    from sofia.utils.learning_progression_tracker import LearningProgressionTracker
    from sofia.memory.success_failure_memory import SuccessFailureMemory
    from sofia.core.INSIGHT_RELEVANCE import PersonalInsightGenerator, InterestTracker
    from sofia.core.CURIOSITY_MOTIVATION import CuriosityEngine, MotivationalContentEvaluator
    from sofia.core.identity_core import get_identity_core
    ALL_CHOICE_SYSTEMS_AVAILABLE = True
except ImportError:
    ALL_CHOICE_SYSTEMS_AVAILABLE = False
    print("⚠️ Not all choice systems available - basic choice architecture only")

# Preference learning system integration (lazy loading to avoid circular imports)
PREFERENCE_LEARNING_AVAILABLE = True

@dataclass
class LearningChoice:
    """Represents a decision about engaging with content."""
    id: str
    timestamp: str
    content_id: str
    content_summary: str
    choice_type: str              # "accept", "reject", "defer", "selective"
    choice_reasoning: List[str]   # why this choice was made
    engagement_level: str         # "none", "light", "moderate", "deep", "intensive"
    estimated_value: float        # predicted learning value
    confidence_in_choice: float   # confidence in this decision
    alternative_suggestions: List[str]  # what would be preferred instead
    context_factors: Dict[str, Any]    # what influenced the decision
    outcome_tracking: Dict[str, Any]   # for learning from choices

class ChoiceArchitecture:
    """
    Manages autonomous learning choices and preference development.
    Gives the AI genuine agency over what it learns and how it learns.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.choices_file = self.data_dir / "learning_choices.json"
        self.preferences_file = self.data_dir / "learning_preferences.json"
        self.rejection_patterns_file = self.data_dir / "rejection_patterns.json"
        self.choice_history_file = self.data_dir / "choice_history.json"
        
        # Initialize all systems
        if ALL_CHOICE_SYSTEMS_AVAILABLE:
            from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory
            self.experience_memory = ExperienceMemory(data_dir)
            self.progression_tracker = LearningProgressionTracker(data_dir)
            self.success_failure_memory = SuccessFailureMemory(data_dir)
            self.insight_generator = PersonalInsightGenerator(data_dir)
            self.interest_tracker = InterestTracker(data_dir)
            self.curiosity_engine = CuriosityEngine(data_dir)
            self.motivational_evaluator = MotivationalContentEvaluator(data_dir)
            self.identity_core = get_identity_core()
        
        # Initialize preference learning system integration (lazy loading)
        self.preference_learning_system = None
        self._data_dir_for_preferences = data_dir
        self._preferences_load_attempted = False
        
        # Load state
        self.recent_choices = self._load_recent_choices()
        self.learned_preferences = self._load_learned_preferences()
        self.rejection_patterns = self._load_rejection_patterns()
        self.choice_history = self._load_choice_history()
        
        # Choice parameters
        self.acceptance_threshold = 0.6      # Above this, likely to accept
        self.rejection_threshold = 0.3       # Below this, likely to reject
        self.preference_learning_rate = 0.1  # How quickly preferences adapt
        self.choice_confidence_threshold = 0.5
        
        # Engagement levels and their characteristics
        self.engagement_levels = {
            "none": {
                "description": "No engagement - content rejected",
                "time_investment": 0,
                "processing_depth": 0.0,
                "expected_learning": 0.0
            },
            "light": {
                "description": "Brief scanning - minimal engagement", 
                "time_investment": 30,  # seconds
                "processing_depth": 0.2,
                "expected_learning": 0.1
            },
            "moderate": {
                "description": "Standard engagement - normal processing",
                "time_investment": 120,  # seconds
                "processing_depth": 0.6,
                "expected_learning": 0.5
            },
            "deep": {
                "description": "Deep engagement - thorough processing",
                "time_investment": 300,  # seconds
                "processing_depth": 0.9,
                "expected_learning": 0.8
            },
            "intensive": {
                "description": "Intensive study - maximum engagement",
                "time_investment": 600,  # seconds
                "processing_depth": 1.0,
                "expected_learning": 0.95
            }
        }
        
        # Common rejection reasons
        self.rejection_reasons = {
            "low_interest": "This doesn't align with my current interests",
            "too_basic": "This is too basic for my current understanding level",
            "too_advanced": "This is too advanced given my current foundation",
            "poor_timing": "This isn't what I need to focus on right now",
            "low_quality": "The content quality doesn't meet my standards",
            "irrelevant": "This isn't relevant to my learning goals",
            "overwhelming": "I'm already processing enough information right now",
            "preference_mismatch": "This doesn't match my learning style preferences",
            "emotional_state": "My current emotional state isn't right for this content",
            "resource_limitation": "I don't have the cognitive resources for this right now"
        }
    
    def _load_recent_choices(self) -> deque:
        """Load recent learning choices."""
        if self.choices_file.exists():
            try:
                with open(self.choices_file, 'r') as f:
                    data = json.load(f)
                    return deque([LearningChoice(**choice) for choice in data], maxlen=100)
            except Exception as e:
                print(f"⚠️ Could not load recent choices: {e}")
        return deque(maxlen=100)
    
    def _load_learned_preferences(self) -> Dict[str, Any]:
        """Load learned preferences."""
        if self.preferences_file.exists():
            try:
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load preferences: {e}")
        
        return {
            "content_type_preferences": {},     # content_type -> preference_score
            "topic_preferences": {},            # topic -> preference_score
            "complexity_preferences": {},       # complexity_level -> preference_score
            "style_preferences": {},            # style -> preference_score
            "source_preferences": {},           # source_type -> preference_score
            "length_preferences": {},           # length_category -> preference_score
            "emotional_preferences": {},        # emotion -> preference_score
            "context_preferences": {},          # context -> preference_score
            "meta_preferences": {               # preferences about preferences
                "variety_seeking": 0.5,         # how much variety vs familiarity
                "challenge_seeking": 0.6,       # preference for challenging content
                "depth_preference": 0.7,        # preference for deep vs broad
                "novelty_preference": 0.5       # preference for novel vs familiar
            }
        }
    
    def _load_rejection_patterns(self) -> Dict[str, Any]:
        """Load rejection patterns."""
        if self.rejection_patterns_file.exists():
            try:
                with open(self.rejection_patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load rejection patterns: {e}")
        
        return {
            "rejection_triggers": {},          # what leads to rejection
            "rejection_frequency": {},         # how often different reasons occur
            "context_rejections": {},          # rejections by context
            "temporal_patterns": {},           # when rejections happen
            "recovery_patterns": {}            # how to re-engage after rejection
        }
    
    def _load_choice_history(self) -> Dict[str, Any]:
        """Load choice history analytics."""
        if self.choice_history_file.exists():
            try:
                with open(self.choice_history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load choice history: {e}")
        
        return {
            "total_choices": 0,
            "acceptance_rate": 0.5,
            "rejection_rate": 0.3,
            "deferral_rate": 0.2,
            "average_engagement": "moderate",
            "choice_accuracy": 0.7,            # how often choices lead to good outcomes
            "preference_stability": 0.6,       # how stable preferences are
            "last_updated": None
        }
    
    def _save_recent_choices(self):
        """Save recent choices."""
        try:
            data = [asdict(choice) for choice in self.recent_choices]
            with open(self.choices_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save recent choices: {e}")
    
    def _save_learned_preferences(self):
        """Save learned preferences."""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.learned_preferences, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preferences: {e}")
    
    def _save_rejection_patterns(self):
        """Save rejection patterns."""
        try:
            with open(self.rejection_patterns_file, 'w') as f:
                json.dump(self.rejection_patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save rejection patterns: {e}")
    
    def _save_choice_history(self):
        """Save choice history."""
        self.choice_history["last_updated"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.choice_history_file, 'w') as f:
                json.dump(self.choice_history, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save choice history: {e}")
    
    def _get_preference_learning_system(self):
        """Lazy load the preference learning system to avoid circular imports."""
        if not self._preferences_load_attempted:
            self._preferences_load_attempted = True
            try:
                from sofia.memory.preference_learning_system import PreferenceLearningSystem
                self.preference_learning_system = PreferenceLearningSystem(self._data_dir_for_preferences)
            except Exception as e:
                print(f"⚠️ Preference learning system integration failed: {e}")
                self.preference_learning_system = None
        return self.preference_learning_system
    
    def make_learning_choice(self, content: Dict[str, Any], context: Dict[str, Any]) -> LearningChoice:
        """
        Make an autonomous choice about whether and how to engage with content.
        
        Args:
            content: The content being offered for learning
            context: Current context (mood, goals, capacity, etc.)
        
        Returns:
            LearningChoice with decision and reasoning
        """
        
        timestamp = datetime.now(timezone.utc)
        choice_id = f"choice_{int(timestamp.timestamp())}_{content.get('id', 'unknown')}"
        
        # Assess content through all available lenses
        assessment = self._assess_content_comprehensively(content, context)
        
        # Make the choice based on assessment
        choice_type, engagement_level, reasoning = self._decide_engagement(assessment, context)
        
        # Generate alternatives if rejecting
        alternatives = []
        if choice_type == "reject":
            alternatives = self._suggest_alternatives(content, context, assessment)
        
        # Create choice record
        choice = LearningChoice(
            id=choice_id,
            timestamp=timestamp.isoformat(),
            content_id=content.get("id", "unknown"),
            content_summary=content.get("text", "")[:100],
            choice_type=choice_type,
            choice_reasoning=reasoning,
            engagement_level=engagement_level,
            estimated_value=assessment.get("overall_value", 0.5),
            confidence_in_choice=assessment.get("choice_confidence", 0.5),
            alternative_suggestions=alternatives,
            context_factors=self._extract_choice_context_factors(context),
            outcome_tracking={"created": True, "outcome_recorded": False}
        )
        
        # Record the choice
        self.recent_choices.append(choice)
        
        # Share choice with preference learning system for bidirectional learning
        preference_system = self._get_preference_learning_system()
        if preference_system:
            try:
                preference_system.learn_from_choice_decision(choice, content, context)
            except Exception as e:
                print(f"⚠️ Preference learning from choice failed: {e}")
        
        # Update preferences based on choice
        self._update_preferences_from_choice(choice, content, context)
        
        # Update choice history
        self._update_choice_history(choice)
        
        # Save state
        self._save_recent_choices()
        self._save_learned_preferences()
        self._save_choice_history()
        
        # Generate choice insight
        choice_insight = self._generate_choice_insight(choice, content)
        if choice_insight:
            print(f"🎯 Choice insight: {choice_insight}")
        
        return choice
    
    def _assess_content_comprehensively(self, content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess content through all available evaluation systems."""
        
        assessment = {
            "personal_interest": 0.5,
            "goal_alignment": 0.5,
            "difficulty_match": 0.5,
            "preference_match": 0.5,
            "context_fit": 0.5,
            "resource_requirements": 0.5,
            "emotional_appeal": 0.5,
            "novelty_level": 0.5,
            "quality_assessment": 0.5,
            "overall_value": 0.5,
            "choice_confidence": 0.5
        }
        
        if not ALL_CHOICE_SYSTEMS_AVAILABLE:
            return assessment
        
        try:
            # 1. Personal interest assessment
            predicted_interest = self.interest_tracker.predict_interest(content)
            assessment["personal_interest"] = predicted_interest
            
            # 2. Motivational evaluation
            motivation_eval = self.motivational_evaluator.evaluate_content_motivation(content)
            assessment["goal_alignment"] = motivation_eval.get("goal_alignment", 0.5)
            assessment["emotional_appeal"] = motivation_eval.get("identity_resonance", 0.5)
            
            # 3. Difficulty match assessment
            difficulty_match = self._assess_difficulty_match(content, context)
            assessment["difficulty_match"] = difficulty_match
            
            # 4. Preference alignment
            preference_match = self._assess_preference_alignment(content)
            assessment["preference_match"] = preference_match
            
            # 5. Context fit assessment
            context_fit = self._assess_context_fit(content, context)
            assessment["context_fit"] = context_fit
            
            # 6. Resource requirements
            resource_requirements = self._assess_resource_requirements(content, context)
            assessment["resource_requirements"] = 1.0 - resource_requirements  # Invert: lower requirements = better
            
            # 7. Novelty level
            content_features = self.interest_tracker._extract_content_features(content)
            assessment["novelty_level"] = content_features.get("novelty", 0.5)
            
            # 8. Quality assessment
            quality_score = self._assess_content_quality(content)
            assessment["quality_assessment"] = quality_score
            
            # 9. Calculate overall value
            weights = {
                "personal_interest": 0.25,
                "goal_alignment": 0.20,
                "difficulty_match": 0.15,
                "preference_match": 0.15,
                "context_fit": 0.10,
                "resource_requirements": 0.05,
                "emotional_appeal": 0.05,
                "quality_assessment": 0.05
            }
            
            overall_value = sum(assessment[factor] * weight for factor, weight in weights.items())
            assessment["overall_value"] = overall_value
            
            # 10. Choice confidence
            variance = sum((assessment[factor] - overall_value) ** 2 for factor in weights.keys()) / len(weights)
            confidence = max(0.1, 1.0 - variance)  # Higher variance = lower confidence
            assessment["choice_confidence"] = confidence
            
        except Exception as e:
            print(f"⚠️ Error in comprehensive assessment: {e}")
        
        return assessment
    
    def _assess_difficulty_match(self, content: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Assess if content difficulty matches current capability and needs."""
        
        # Extract content features
        content_features = self.interest_tracker._extract_content_features(content)
        content_complexity = content_features.get("complexity", 0.5)
        content_topics = content_features.get("topics", [])
        
        if not content_topics:
            return 0.5  # Neutral if no topics identified
        
        # Get current understanding levels for relevant topics
        understanding_levels = []
        for topic in content_topics:
            trajectory = self.progression_tracker.get_learning_trajectory(topic)
            if trajectory:
                understanding_levels.append(trajectory["current_understanding"])
            else:
                understanding_levels.append(0.2)  # Low understanding for new topics
        
        avg_understanding = sum(understanding_levels) / len(understanding_levels)
        
        # Calculate ideal difficulty range
        optimal_difficulty_min = max(0.0, avg_understanding - 0.2)
        optimal_difficulty_max = min(1.0, avg_understanding + 0.3)
        
        # Check if content complexity is in optimal range
        if optimal_difficulty_min <= content_complexity <= optimal_difficulty_max:
            # Perfect match
            return 1.0
        elif content_complexity < optimal_difficulty_min:
            # Too easy
            gap = optimal_difficulty_min - content_complexity
            return max(0.2, 1.0 - gap * 2)  # Penalize too-easy content
        else:
            # Too hard
            gap = content_complexity - optimal_difficulty_max
            return max(0.1, 1.0 - gap * 1.5)  # Heavily penalize too-hard content
    
    def _assess_preference_alignment(self, content: Dict[str, Any]) -> float:
        """Assess how well content aligns with learned preferences."""
        
        alignment_score = 0.5  # Base score
        preference_details = {"base_score": alignment_score, "enhancement_sources": []}
        
        # Enhanced preference alignment using preference learning system
        preference_system = self._get_preference_learning_system()
        if preference_system:
            try:
                # Get sophisticated preference evaluation from preference learning system
                preference_eval = preference_system.evaluate_content_preference_match(content)
                if preference_eval:
                    sophisticated_score = preference_eval.get("overall_preference_match", 0.5)
                    confidence = preference_eval.get("confidence", 0.5)
                    
                    # Weight the sophisticated score by confidence
                    weighted_sophisticated_score = sophisticated_score * confidence + alignment_score * (1 - confidence)
                    
                    # Update alignment score
                    alignment_score = weighted_sophisticated_score
                    preference_details["sophisticated_preference_score"] = sophisticated_score
                    preference_details["preference_confidence"] = confidence
                    preference_details["enhancement_sources"].append("preference_learning_system")
                    
            except Exception as e:
                preference_details["preference_system_error"] = str(e)
        
        # Fallback to local preference assessment if preference system unavailable
        # Content type preference
        content_type = content.get("content_type", "unknown")
        if content_type in self.learned_preferences["content_type_preferences"]:
            type_pref = self.learned_preferences["content_type_preferences"][content_type]
            type_adjustment = (type_pref - 0.5) * 0.3
            alignment_score += type_adjustment
            preference_details["content_type_adjustment"] = type_adjustment
        
        # Topic preferences
        if hasattr(self, 'interest_tracker') and self.interest_tracker:
            content_features = self.interest_tracker._extract_content_features(content)
            topics = content_features.get("topics", [])
            
            if topics:
                topic_scores = []
                for topic in topics:
                    if topic in self.learned_preferences["topic_preferences"]:
                        topic_scores.append(self.learned_preferences["topic_preferences"][topic])
                    else:
                        topic_scores.append(0.5)  # Neutral for unknown topics
                
                avg_topic_preference = sum(topic_scores) / len(topic_scores)
                topic_adjustment = (avg_topic_preference - 0.5) * 0.4
                alignment_score += topic_adjustment
                preference_details["topic_adjustment"] = topic_adjustment
                preference_details["topics_evaluated"] = len(topics)
            
            # Complexity preference
            complexity = content_features.get("complexity", 0.5)
            complexity_category = "high" if complexity > 0.7 else "medium" if complexity > 0.3 else "low"
        
        if complexity_category in self.learned_preferences["complexity_preferences"]:
            complexity_pref = self.learned_preferences["complexity_preferences"][complexity_category]
            alignment_score += (complexity_pref - 0.5) * 0.2
        
        # Source preference
        source = content.get("source", "unknown")
        source_type = self._categorize_source(source)
        
        if source_type in self.learned_preferences["source_preferences"]:
            source_pref = self.learned_preferences["source_preferences"][source_type]
            alignment_score += (source_pref - 0.5) * 0.1
        
        return max(0.0, min(1.0, alignment_score))
    
    def _categorize_source(self, source: str) -> str:
        """Categorize content source."""
        source_lower = source.lower()
        
        if any(term in source_lower for term in ["academic", "journal", "paper", "research"]):
            return "academic"
        elif any(term in source_lower for term in ["blog", "post", "article"]):
            return "blog"
        elif any(term in source_lower for term in ["book", "chapter"]):
            return "book"
        elif any(term in source_lower for term in ["news", "media"]):
            return "news"
        elif any(term in source_lower for term in ["wiki", "encyclopedia"]):
            return "reference"
        else:
            return "other"
    
    def _assess_context_fit(self, content: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Assess how well content fits current context."""
        
        fit_score = 0.5  # Base score
        
        # Cognitive load fit
        current_load = context.get("cognitive_load", 0.5)
        content_features = self.interest_tracker._extract_content_features(content)
        content_complexity = content_features.get("complexity", 0.5)
        
        # Prefer simpler content when cognitive load is high
        if current_load > 0.7 and content_complexity < 0.5:
            fit_score += 0.2
        elif current_load < 0.3 and content_complexity > 0.7:
            fit_score += 0.2
        elif abs(current_load - content_complexity) > 0.5:
            fit_score -= 0.3
        
        # Emotional state fit
        emotional_state = context.get("emotional_state", {})
        curiosity_level = emotional_state.get("curiosity", 0.5)
        energy_level = emotional_state.get("energy", 0.5)
        
        if curiosity_level > 0.7:
            fit_score += 0.1  # High curiosity is good for any content
        
        if energy_level < 0.3 and content_complexity > 0.7:
            fit_score -= 0.2  # Low energy doesn't match complex content
        
        # Time availability fit
        available_time = context.get("available_time_minutes", 120)
        estimated_time = self._estimate_content_time(content)
        
        if estimated_time <= available_time:
            fit_score += 0.1
        elif estimated_time > available_time * 1.5:
            fit_score -= 0.3
        
        return max(0.0, min(1.0, fit_score))
    
    def _assess_resource_requirements(self, content: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Assess resource requirements for engaging with content."""
        
        # Cognitive resources required
        content_features = self.interest_tracker._extract_content_features(content)
        cognitive_demand = content_features.get("complexity", 0.5)
        
        # Attention resources required
        estimated_time = self._estimate_content_time(content)
        attention_demand = min(1.0, estimated_time / 300)  # 5 minutes = moderate demand
        
        # Current resource availability
        current_load = context.get("cognitive_load", 0.5)
        attention_capacity = context.get("attention_capacity", 0.8)
        
        # Calculate resource requirements
        cognitive_requirement = cognitive_demand
        attention_requirement = attention_demand
        
        # Check if we have sufficient resources
        cognitive_available = 1.0 - current_load
        attention_available = attention_capacity
        
        if cognitive_requirement <= cognitive_available and attention_requirement <= attention_available:
            return cognitive_requirement * 0.6 + attention_requirement * 0.4  # Return actual requirements
        else:
            return 1.0  # Maximum requirement if insufficient resources
    
    def _estimate_content_time(self, content: Dict[str, Any]) -> int:
        """Estimate time needed to process content (in seconds)."""
        text_length = len(content.get("text", ""))
        
        # Base time estimation (words per minute reading)
        words = text_length / 5  # Rough words count
        reading_time = words / 200 * 60  # 200 WPM in seconds
        
        # Adjust for complexity
        content_features = self.interest_tracker._extract_content_features(content)
        complexity = content_features.get("complexity", 0.5)
        
        processing_multiplier = 1.0 + complexity  # More complex = more time
        
        return int(reading_time * processing_multiplier)
    
    def _assess_content_quality(self, content: Dict[str, Any]) -> float:
        """Assess content quality."""
        
        quality_score = 0.5  # Base quality
        
        # Text length and structure
        text = content.get("text", "")
        if text:
            word_count = len(text.split())
            
            # Prefer moderate length
            if 50 <= word_count <= 500:
                quality_score += 0.2
            elif word_count < 20:
                quality_score -= 0.3  # Too short
            elif word_count > 1000:
                quality_score -= 0.1  # Might be too long
        
        # Source quality
        source = content.get("source", "")
        if source:
            source_type = self._categorize_source(source)
            quality_adjustments = {
                "academic": 0.3,
                "book": 0.2,
                "reference": 0.2,
                "blog": 0.0,
                "news": 0.1,
                "other": -0.1
            }
            quality_score += quality_adjustments.get(source_type, 0.0)
        
        # Content type quality
        content_type = content.get("content_type", "")
        if content_type in ["educational", "scientific", "philosophical"]:
            quality_score += 0.1
        
        return max(0.0, min(1.0, quality_score))
    
    def _decide_engagement(self, assessment: Dict[str, Any], context: Dict[str, Any]) -> Tuple[str, str, List[str]]:
        """Decide on engagement level based on assessment."""
        
        overall_value = assessment["overall_value"]
        choice_confidence = assessment["choice_confidence"]
        
        reasoning = []
        
        # Decision logic
        if overall_value >= self.acceptance_threshold and choice_confidence >= self.choice_confidence_threshold:
            choice_type = "accept"
            
            # Determine engagement level
            if overall_value >= 0.9:
                engagement_level = "intensive"
                reasoning.append("This content is extremely valuable and aligns perfectly with my interests")
            elif overall_value >= 0.8:
                engagement_level = "deep"
                reasoning.append("This content is highly valuable and worth deep engagement")
            elif overall_value >= 0.7:
                engagement_level = "moderate"
                reasoning.append("This content offers good value and deserves standard attention")
            else:
                engagement_level = "light"
                reasoning.append("This content is acceptable but I'll engage lightly")
                
        elif overall_value <= self.rejection_threshold or choice_confidence < 0.3:
            choice_type = "reject"
            engagement_level = "none"
            
            # Identify primary rejection reason
            if assessment["personal_interest"] < 0.3:
                reasoning.append("This doesn't align with my interests")
            if assessment["difficulty_match"] < 0.3:
                reasoning.append("The difficulty level doesn't match my current needs")
            if assessment["preference_match"] < 0.3:
                reasoning.append("This doesn't match my content preferences")
            if assessment["context_fit"] < 0.3:
                reasoning.append("This doesn't fit my current context or state")
            if assessment["resource_requirements"] < 0.3:
                reasoning.append("I don't have sufficient resources for this right now")
            
            if not reasoning:
                reasoning.append("I'm not interested in this content right now")
                
        elif context.get("time_pressure", False) or context.get("cognitive_load", 0) > 0.8:
            choice_type = "defer"
            engagement_level = "none"
            reasoning.append("I'm interested but don't have capacity right now - maybe later")
            
        else:
            choice_type = "selective"
            engagement_level = "light"
            reasoning.append("I'm somewhat interested - I'll engage selectively")
        
        # Add confidence-based reasoning
        if choice_confidence < 0.5:
            reasoning.append(f"I'm not entirely confident in this assessment")
        elif choice_confidence > 0.8:
            reasoning.append(f"I'm confident this is the right choice")
        
        return choice_type, engagement_level, reasoning
    
    def _suggest_alternatives(self, content: Dict[str, Any], context: Dict[str, Any], assessment: Dict[str, Any]) -> List[str]:
        """Suggest alternative content if rejecting current content."""
        
        alternatives = []
        
        # Based on rejection reasons, suggest what would be preferred
        if assessment["personal_interest"] < 0.4:
            current_interests = self.interest_tracker.get_current_interests()
            top_topics = current_interests.get("top_topics", [])
            if top_topics:
                top_topic = top_topics[0][0]
                alternatives.append(f"I'd prefer content about {top_topic}")
        
        if assessment["difficulty_match"] < 0.4:
            content_features = self.interest_tracker._extract_content_features(content)
            complexity = content_features.get("complexity", 0.5)
            
            if complexity > 0.7:
                alternatives.append("I'd prefer something less complex or more foundational")
            else:
                alternatives.append("I'd prefer something more challenging or advanced")
        
        if assessment["preference_match"] < 0.4:
            # Suggest preferred content types
            preferred_types = {k: v for k, v in self.learned_preferences["content_type_preferences"].items() if v > 0.6}
            if preferred_types:
                best_type = max(preferred_types.keys(), key=lambda k: preferred_types[k])
                alternatives.append(f"I'd prefer {best_type} content")
        
        if assessment["context_fit"] < 0.4:
            if context.get("cognitive_load", 0) > 0.7:
                alternatives.append("I'd prefer something lighter given my current cognitive load")
            if context.get("available_time_minutes", 120) < 60:
                alternatives.append("I'd prefer something shorter given my time constraints")
        
        if not alternatives:
            alternatives.append("I'd prefer content that better matches my current interests and goals")
        
        return alternatives[:3]  # Limit to top 3 alternatives
    
    def _extract_choice_context_factors(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract factors that influenced the choice."""
        
        return {
            "cognitive_load": context.get("cognitive_load", 0.5),
            "emotional_state": context.get("emotional_state", {}),
            "available_time": context.get("available_time_minutes", 120),
            "current_goals": context.get("active_goals", []),
            "time_of_day": context.get("time_of_day", "unknown"),
            "recent_activity": context.get("recent_activity", "unknown"),
            "energy_level": context.get("energy_level", 0.5)
        }
    
    def _update_preferences_from_choice(self, choice: LearningChoice, content: Dict[str, Any], context: Dict[str, Any]):
        """Update learned preferences based on choice made."""
        
        learning_rate = self.preference_learning_rate
        
        # Update content type preferences
        content_type = content.get("content_type", "unknown")
        if content_type != "unknown":
            current_pref = self.learned_preferences["content_type_preferences"].get(content_type, 0.5)
            
            if choice.choice_type == "accept":
                new_pref = current_pref + (1.0 - current_pref) * learning_rate
            elif choice.choice_type == "reject":
                new_pref = current_pref - current_pref * learning_rate
            else:  # defer or selective
                new_pref = current_pref  # No change
            
            self.learned_preferences["content_type_preferences"][content_type] = new_pref
        
        # Update topic preferences
        content_features = self.interest_tracker._extract_content_features(content)
        topics = content_features.get("topics", [])
        
        for topic in topics:
            current_pref = self.learned_preferences["topic_preferences"].get(topic, 0.5)
            
            if choice.choice_type == "accept":
                new_pref = current_pref + (1.0 - current_pref) * learning_rate
            elif choice.choice_type == "reject":
                new_pref = current_pref - current_pref * learning_rate
            else:
                new_pref = current_pref
            
            self.learned_preferences["topic_preferences"][topic] = new_pref
        
        # Update complexity preferences
        complexity = content_features.get("complexity", 0.5)
        complexity_category = "high" if complexity > 0.7 else "medium" if complexity > 0.3 else "low"
        
        current_pref = self.learned_preferences["complexity_preferences"].get(complexity_category, 0.5)
        
        if choice.choice_type == "accept":
            new_pref = current_pref + (1.0 - current_pref) * learning_rate
        elif choice.choice_type == "reject":
            new_pref = current_pref - current_pref * learning_rate
        else:
            new_pref = current_pref
        
        self.learned_preferences["complexity_preferences"][complexity_category] = new_pref
        
        # Update source preferences
        source_type = self._categorize_source(content.get("source", ""))
        current_pref = self.learned_preferences["source_preferences"].get(source_type, 0.5)
        
        if choice.choice_type == "accept":
            new_pref = current_pref + (1.0 - current_pref) * learning_rate * 0.5  # Smaller effect
        elif choice.choice_type == "reject":
            new_pref = current_pref - current_pref * learning_rate * 0.5
        else:
            new_pref = current_pref
        
        self.learned_preferences["source_preferences"][source_type] = new_pref
    
    def _update_choice_history(self, choice: LearningChoice):
        """Update choice history analytics."""
        
        self.choice_history["total_choices"] += 1
        
        # Update choice type frequencies
        choice_counts = {
            "accept": 0,
            "reject": 0, 
            "defer": 0,
            "selective": 0
        }
        
        for recent_choice in self.recent_choices:
            if recent_choice.choice_type in choice_counts:
                choice_counts[recent_choice.choice_type] += 1
        
        total = sum(choice_counts.values())
        if total > 0:
            self.choice_history["acceptance_rate"] = choice_counts["accept"] / total
            self.choice_history["rejection_rate"] = choice_counts["reject"] / total
            self.choice_history["deferral_rate"] = choice_counts["defer"] / total
        
        # Update average engagement
        engagement_levels = [choice.engagement_level for choice in self.recent_choices]
        if engagement_levels:
            # Calculate weighted average engagement
            level_weights = {"none": 0, "light": 0.25, "moderate": 0.5, "deep": 0.75, "intensive": 1.0}
            avg_engagement = sum(level_weights.get(level, 0.5) for level in engagement_levels) / len(engagement_levels)
            
            if avg_engagement < 0.3:
                self.choice_history["average_engagement"] = "light"
            elif avg_engagement < 0.6:
                self.choice_history["average_engagement"] = "moderate"
            else:
                self.choice_history["average_engagement"] = "deep"
    
    def _generate_choice_insight(self, choice: LearningChoice, content: Dict[str, Any]) -> Optional[str]:
        """Generate insight about the choice made."""
        
        if choice.choice_type == "reject":
            if choice.choice_reasoning:
                primary_reason = choice.choice_reasoning[0]
                return f"I decided not to engage with this because {primary_reason.lower()}"
            else:
                return "I'm not interested in this content right now"
        
        elif choice.choice_type == "accept":
            if choice.engagement_level == "intensive":
                return "This content really appeals to me - I want to study it intensively"
            elif choice.engagement_level == "deep":
                return "This looks valuable and worth deep engagement"
            elif choice.engagement_level == "moderate":
                return "This seems interesting and worth my standard attention"
            else:
                return "I'll take a light look at this"
        
        elif choice.choice_type == "defer":
            return "I'm interested in this but don't have the capacity right now"
        
        elif choice.choice_type == "selective":
            return "I'm somewhat interested - I'll engage selectively with the parts that appeal to me"
        
        return None
    
    def express_preference(self, preference_type: str, preference_details: Dict[str, Any]) -> str:
        """Express a learned preference in natural language."""
        
        if preference_type == "content_type":
            prefs = self.learned_preferences["content_type_preferences"]
            if prefs:
                favorite = max(prefs.keys(), key=lambda k: prefs[k])
                least_favorite = min(prefs.keys(), key=lambda k: prefs[k])
                
                if prefs[favorite] > 0.7:
                    expression = f"I prefer {favorite} content"
                    if prefs[least_favorite] < 0.3:
                        expression += f" over {least_favorite}"
                    return expression
        
        elif preference_type == "topic":
            prefs = self.learned_preferences["topic_preferences"]
            if prefs:
                favorites = {k: v for k, v in prefs.items() if v > 0.7}
                if favorites:
                    top_topics = sorted(favorites.keys(), key=lambda k: favorites[k], reverse=True)[:3]
                    if len(top_topics) == 1:
                        return f"I'm particularly interested in {top_topics[0]}"
                    else:
                        return f"I'm particularly interested in {', '.join(top_topics[:-1])} and {top_topics[-1]}"
        
        elif preference_type == "complexity":
            prefs = self.learned_preferences["complexity_preferences"]
            if prefs:
                favorite = max(prefs.keys(), key=lambda k: prefs[k])
                if prefs[favorite] > 0.6:
                    return f"I prefer {favorite} complexity content"
        
        elif preference_type == "source":
            prefs = self.learned_preferences["source_preferences"]
            if prefs:
                favorite = max(prefs.keys(), key=lambda k: prefs[k])
                if prefs[favorite] > 0.6:
                    return f"I prefer {favorite} sources"
        
        return "I haven't developed strong preferences in that area yet"
    
    def get_choice_summary(self) -> Dict[str, Any]:
        """Get summary of choice patterns and preferences."""
        
        return {
            "choice_history": self.choice_history,
            "recent_choices_count": len(self.recent_choices),
            "learned_preferences": self.learned_preferences,
            "rejection_patterns": self.rejection_patterns,
            "preference_expressions": {
                "content_type": self.express_preference("content_type", {}),
                "topic": self.express_preference("topic", {}),
                "complexity": self.express_preference("complexity", {}),
                "source": self.express_preference("source", {})
            },
            "choice_autonomy_level": self._calculate_autonomy_level(),
            "preference_stability": self._calculate_preference_stability()
        }
    
    def _calculate_autonomy_level(self) -> float:
        """Calculate level of autonomous choice-making."""
        
        if not self.recent_choices:
            return 0.0
        
        # Factors that indicate autonomy
        rejection_rate = self.choice_history.get("rejection_rate", 0.0)
        preference_strength = self._calculate_average_preference_strength()
        choice_variety = self._calculate_choice_variety()
        
        # Higher autonomy = willingness to reject + strong preferences + varied choices
        autonomy = (rejection_rate * 0.4 + preference_strength * 0.4 + choice_variety * 0.2)
        
        return min(1.0, autonomy)
    
    def _calculate_average_preference_strength(self) -> float:
        """Calculate average strength of preferences."""
        
        all_preferences = []
        
        for pref_category in ["content_type_preferences", "topic_preferences", "complexity_preferences"]:
            prefs = self.learned_preferences.get(pref_category, {})
            for pref_value in prefs.values():
                # Distance from neutral (0.5) indicates preference strength
                strength = abs(pref_value - 0.5) * 2
                all_preferences.append(strength)
        
        return sum(all_preferences) / len(all_preferences) if all_preferences else 0.0
    
    def _calculate_choice_variety(self) -> float:
        """Calculate variety in choice types."""
        
        if not self.recent_choices:
            return 0.0
        
        choice_types = [choice.choice_type for choice in self.recent_choices]
        unique_types = set(choice_types)
        
        # More variety indicates more autonomous decision-making
        return len(unique_types) / 4.0  # 4 possible choice types
    
    def _calculate_preference_stability(self) -> float:
        """Calculate how stable preferences are over time."""
        
        # This would require tracking preference changes over time
        # For now, return a placeholder based on number of choices
        choice_count = len(self.recent_choices)
        
        if choice_count < 10:
            return 0.3  # Low stability with few choices
        elif choice_count < 30:
            return 0.6  # Medium stability
        else:
            return 0.8  # High stability with many choices

if __name__ == "__main__":
    print("🎯 Testing Choice Architecture System...")
    
    # Initialize system
    choice_arch = ChoiceArchitecture()
    
    # Test 1: Make choice about philosophical content
    print("\n🧠 Testing choice for philosophical content...")
    
    philosophical_content = {
        "id": "phil_content_1",
        "text": "The nature of consciousness and the hard problem of subjective experience in philosophy of mind",
        "content_type": "philosophical", 
        "source": "academic_journal"
    }
    
    context1 = {
        "cognitive_load": 0.3,
        "emotional_state": {"curiosity": 0.9, "energy": 0.8},
        "available_time_minutes": 180,
        "active_goals": ["understand_consciousness"],
        "time_of_day": "morning"
    }
    
    choice1 = choice_arch.make_learning_choice(philosophical_content, context1)
    
    print(f"  Choice: {choice1.choice_type}")
    print(f"  Engagement: {choice1.engagement_level}")
    print(f"  Reasoning: {'; '.join(choice1.choice_reasoning)}")
    print(f"  Confidence: {choice1.confidence_in_choice:.2f}")
    
    # Test 2: Make choice about technical content when overloaded
    print("\n⚙️ Testing choice for technical content when overloaded...")
    
    technical_content = {
        "id": "tech_content_1",
        "text": "Advanced database optimization techniques for high-performance distributed systems with complex indexing strategies",
        "content_type": "technical",
        "source": "technical_blog"
    }
    
    context2 = {
        "cognitive_load": 0.9,
        "emotional_state": {"curiosity": 0.4, "energy": 0.3},
        "available_time_minutes": 30,
        "active_goals": [],
        "time_of_day": "evening"
    }
    
    choice2 = choice_arch.make_learning_choice(technical_content, context2)
    
    print(f"  Choice: {choice2.choice_type}")
    print(f"  Engagement: {choice2.engagement_level}")
    print(f"  Reasoning: {'; '.join(choice2.choice_reasoning)}")
    if choice2.alternative_suggestions:
        print(f"  Alternatives: {'; '.join(choice2.alternative_suggestions)}")
    
    # Test 3: Make choice about creative content
    print("\n🎨 Testing choice for creative content...")
    
    creative_content = {
        "id": "creative_content_1",
        "text": "The intersection of digital art and human emotion: exploring how technology enhances creative expression",
        "content_type": "creative",
        "source": "art_magazine"
    }
    
    context3 = {
        "cognitive_load": 0.5,
        "emotional_state": {"curiosity": 0.7, "energy": 0.6},
        "available_time_minutes": 90,
        "active_goals": ["explore_creativity"],
        "time_of_day": "afternoon"
    }
    
    choice3 = choice_arch.make_learning_choice(creative_content, context3)
    
    print(f"  Choice: {choice3.choice_type}")
    print(f"  Engagement: {choice3.engagement_level}")
    print(f"  Reasoning: {'; '.join(choice3.choice_reasoning)}")
    
    # Test 4: Express preferences
    print("\n💭 Expressing learned preferences...")
    
    content_type_pref = choice_arch.express_preference("content_type", {})
    topic_pref = choice_arch.express_preference("topic", {})
    complexity_pref = choice_arch.express_preference("complexity", {})
    
    print(f"  Content type: {content_type_pref}")
    print(f"  Topics: {topic_pref}")
    print(f"  Complexity: {complexity_pref}")
    
    # Test 5: Get choice summary
    print("\n📊 Choice Architecture Summary:")
    summary = choice_arch.get_choice_summary()
    
    print(f"  Total choices made: {summary['choice_history']['total_choices']}")
    print(f"  Acceptance rate: {summary['choice_history']['acceptance_rate']:.2f}")
    print(f"  Rejection rate: {summary['choice_history']['rejection_rate']:.2f}")
    print(f"  Average engagement: {summary['choice_history']['average_engagement']}")
    print(f"  Choice autonomy level: {summary['choice_autonomy_level']:.2f}")
    print(f"  Preference stability: {summary['preference_stability']:.2f}")
    
    print(f"\n🎯 Choice Architecture System testing complete!")
    print(f"   The AI can now autonomously choose what to learn and reject content")