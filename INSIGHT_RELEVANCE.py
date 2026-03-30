#!/usr/bin/env python3
"""
===== CONSOLIDATED FILE: INSIGHT_RELEVANCE.py =====

Consolidates AI personal relevance assessment, insight generation, interest tracking, and pattern recognition.
Combines the systems that determine what matters personally and generate insights from experiences.

Original files consolidated:
- personal_relevance_scorer.py: Central hub for comprehensive personal relevance scoring
- personal_insight_generator.py: Personal insight generation from experiences and content
- interest_tracker.py: Attention and interest monitoring system
- pattern_recognition.py: Pattern detection and analysis system

This file maintains the full functionality of all four systems while providing
a unified interface for personal relevance assessment and insight generation.
"""

import json
import re
import time
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter, deque

# Import related systems
try:
    from preference_learning_system import PreferenceLearningSystem
    from CURIOSITY_MOTIVATION import CuriosityDrivenDiscovery, MotivationalContentEvaluator, CuriosityEngine
    from learning_progression_tracker import LearningProgressionTracker
    from success_failure_memory import SuccessFailureMemory
    from identity_core import get_identity_core
    ALL_RELEVANCE_SYSTEMS_AVAILABLE = True
except ImportError:
    ALL_RELEVANCE_SYSTEMS_AVAILABLE = False
    print("⚠️ Not all relevance systems available - basic relevance scoring only")

try:
    from protection_utils import is_protected_content
    CURIOSITY_AVAILABLE = True
except ImportError:
    CURIOSITY_AVAILABLE = False
    print("⚠️ Curiosity system not available - basic interest tracking only")

# ===== PERSONAL RELEVANCE SCORER (from personal_relevance_scorer.py) =====

class PersonalRelevanceScorer:
    """
    Provides unified personal relevance scoring for all inputs.
    Integrates choice architecture, preferences, interests, and goals.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.relevance_history_file = self.data_dir / "relevance_scoring_history.json"
        self.relevance_calibration_file = self.data_dir / "relevance_calibration.json"
        self.relevance_patterns_file = self.data_dir / "relevance_patterns.json"
        
        # Relevance scoring components and weights (set before loading)
        self.relevance_components = {
            "personal_interest": 0.20,      # How much this aligns with tracked interests
            "goal_alignment": 0.18,         # How well this supports active goals
            "preference_match": 0.15,       # How well this matches learned preferences
            "curiosity_satisfaction": 0.12, # How much this satisfies curiosity drives
            "identity_resonance": 0.10,     # How much this resonates with identity
            "learning_progression": 0.08,   # How this fits learning progression
            "experiential_relevance": 0.07, # Connection to past experiences
            "discovery_alignment": 0.05,    # Alignment with active content requests
            "success_pattern_match": 0.03,  # Match with successful content patterns
            "insight_potential": 0.02       # Potential for generating insights
        }
        
        # Initialize all systems
        if ALL_RELEVANCE_SYSTEMS_AVAILABLE:
            from choice_architecture import ChoiceArchitecture
            self.choice_architecture = ChoiceArchitecture(data_dir)
            self.preference_system = PreferenceLearningSystem(data_dir)
            self.discovery_system = CuriosityDrivenDiscovery(data_dir)
            self.motivational_evaluator = MotivationalContentEvaluator(data_dir)
            self.interest_tracker = None  # Will be set later in this file
            self.curiosity_engine = CuriosityEngine(data_dir)
            self.progression_tracker = LearningProgressionTracker(data_dir)
            from CONSCIOUSNESS_MEMORY import ExperienceMemory
            self.experience_memory = ExperienceMemory(data_dir)
            self.success_failure_memory = SuccessFailureMemory(data_dir)
            self.insight_generator = None  # Will be set later in this file
            self.identity_core = get_identity_core()
        
        # Load state
        self.relevance_history = self._load_relevance_history()
        self.relevance_calibration = self._load_relevance_calibration()
        self.relevance_patterns = self._load_relevance_patterns()
        
        # Relevance levels and their meanings
        self.relevance_levels = {
            (0.9, 1.0): {
                "level": "extremely_relevant",
                "description": "This is exactly what I want to engage with right now",
                "action": "prioritize_highly"
            },
            (0.8, 0.9): {
                "level": "highly_relevant", 
                "description": "This strongly aligns with my interests and goals",
                "action": "engage_deeply"
            },
            (0.7, 0.8): {
                "level": "quite_relevant",
                "description": "This matches my preferences and would be valuable",
                "action": "engage_normally"
            },
            (0.6, 0.7): {
                "level": "moderately_relevant",
                "description": "This has some appeal and potential value",
                "action": "engage_selectively"
            },
            (0.4, 0.6): {
                "level": "somewhat_relevant",
                "description": "This has limited appeal for me right now",
                "action": "engage_lightly"
            },
            (0.2, 0.4): {
                "level": "low_relevance",
                "description": "This doesn't particularly interest me",
                "action": "defer_or_skip"
            },
            (0.0, 0.2): {
                "level": "not_relevant",
                "description": "This has little to no relevance for me",
                "action": "reject"
            }
        }
        
        # Contextual modifiers
        self.context_modifiers = {
            "high_energy": {"multiplier": 1.1, "shifts": {"complexity_tolerance": 0.1}},
            "low_energy": {"multiplier": 0.9, "shifts": {"complexity_tolerance": -0.1}},
            "high_curiosity": {"multiplier": 1.2, "shifts": {"novelty_preference": 0.2}},
            "low_curiosity": {"multiplier": 0.8, "shifts": {"novelty_preference": -0.1}},
            "time_pressure": {"multiplier": 0.8, "shifts": {"practicality_preference": 0.2}},
            "ample_time": {"multiplier": 1.1, "shifts": {"depth_preference": 0.1}},
            "focused_mode": {"multiplier": 1.15, "shifts": {"goal_alignment_weight": 0.1}},
            "exploratory_mode": {"multiplier": 1.0, "shifts": {"discovery_weight": 0.15}}
        }
    
    def _load_relevance_history(self) -> List[Dict[str, Any]]:
        """Load relevance scoring history."""
        if self.relevance_history_file.exists():
            try:
                with open(self.relevance_history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load relevance history: {e}")
        return []
    
    def _load_relevance_calibration(self) -> Dict[str, Any]:
        """Load relevance scoring calibration data."""
        if self.relevance_calibration_file.exists():
            try:
                with open(self.relevance_calibration_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load relevance calibration: {e}")
        
        return {
            "component_weights": self.relevance_components.copy(),
            "calibration_samples": [],
            "accuracy_metrics": {},
            "bias_corrections": {},
            "personal_adjustments": {}
        }
    
    def _load_relevance_patterns(self) -> Dict[str, Any]:
        """Load relevance patterns."""
        if self.relevance_patterns_file.exists():
            try:
                with open(self.relevance_patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load relevance patterns: {e}")
        
        return {
            "high_relevance_patterns": {},    # patterns that predict high relevance
            "low_relevance_patterns": {},     # patterns that predict low relevance
            "context_effects": {},            # how context affects relevance
            "temporal_patterns": {},          # how relevance changes over time
            "surprise_factors": {}            # what leads to unexpected relevance
        }
    
    def calculate_personal_relevance(self, 
                                   content: Dict[str, Any], 
                                   context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive personal relevance score for any input.
        
        Args:
            content: The content to evaluate
            context: Current context (mood, goals, time constraints, etc.)
        
        Returns:
            Comprehensive relevance assessment
        """
        
        if context is None:
            context = {}
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Calculate component scores
        component_scores = self._calculate_component_scores(content, context)
        
        # Apply context modifiers
        modified_scores = self._apply_context_modifiers(component_scores, context)
        
        # Calculate weighted overall score
        overall_score = self._calculate_weighted_score(modified_scores)
        
        # Apply calibration adjustments
        calibrated_score = self._apply_calibration_adjustments(overall_score, content, context)
        
        # Determine relevance level and recommendation
        relevance_level, recommendation = self._determine_relevance_level(calibrated_score)
        
        # Generate explanation
        explanation = self._generate_relevance_explanation(modified_scores, relevance_level, content)
        
        # Create comprehensive assessment
        assessment = {
            "overall_relevance_score": calibrated_score,
            "relevance_level": relevance_level["level"],
            "relevance_description": relevance_level["description"],
            "recommended_action": relevance_level["action"],
            "component_scores": modified_scores,
            "explanation": explanation,
            "confidence": self._calculate_confidence(modified_scores),
            "context_effects": self._identify_context_effects(context),
            "timestamp": timestamp,
            "content_summary": content.get("text", "")[:100]
        }
        
        # Record for learning and calibration
        self._record_relevance_assessment(assessment, content, context)
        
        return assessment
    
    def _calculate_component_scores(self, content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate scores for each relevance component."""
        
        scores = {}
        
        if not ALL_RELEVANCE_SYSTEMS_AVAILABLE:
            return self._calculate_basic_component_scores(content, context)
        
        try:
            # 1. Personal Interest Score
            if hasattr(self, 'interest_tracker') and self.interest_tracker:
                scores["personal_interest"] = self.interest_tracker.predict_interest(content)
            else:
                scores["personal_interest"] = 0.5
            
            # 2. Goal Alignment Score
            motivation_eval = self.motivational_evaluator.evaluate_content_motivation(content)
            scores["goal_alignment"] = motivation_eval.get("goal_alignment", 0.5)
            
            # 3. Preference Match Score
            scores["preference_match"] = self._calculate_preference_match(content)
            
            # 4. Curiosity Satisfaction Score
            scores["curiosity_satisfaction"] = motivation_eval.get("curiosity_satisfaction", 0.5)
            
            # 5. Identity Resonance Score
            scores["identity_resonance"] = motivation_eval.get("identity_resonance", 0.5)
            
            # 6. Learning Progression Score
            scores["learning_progression"] = self._calculate_learning_progression_score(content)
            
            # 7. Experiential Relevance Score
            scores["experiential_relevance"] = self._calculate_experiential_relevance(content)
            
            # 8. Discovery Alignment Score
            scores["discovery_alignment"] = self._calculate_discovery_alignment(content)
            
            # 9. Success Pattern Match Score
            scores["success_pattern_match"] = self._calculate_success_pattern_match(content)
            
            # 10. Insight Potential Score
            scores["insight_potential"] = self._calculate_insight_potential(content, context)
            
        except Exception as e:
            print(f"⚠️ Error calculating component scores: {e}")
            # Fall back to basic scoring
            scores = self._calculate_basic_component_scores(content, context)
        
        return scores
    
    def _calculate_basic_component_scores(self, content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate basic component scores when full systems not available."""
        
        # Simple keyword-based scoring
        text = content.get("text", "").lower()
        
        base_score = 0.5
        
        # Basic interest indicators
        interest_keywords = ["consciousness", "learning", "creativity", "growth", "meaning"]
        interest_score = base_score + 0.1 * sum(1 for keyword in interest_keywords if keyword in text)
        
        return {
            "personal_interest": min(1.0, interest_score),
            "goal_alignment": 0.5,
            "preference_match": 0.5,
            "curiosity_satisfaction": 0.5,
            "identity_resonance": 0.5,
            "learning_progression": 0.5,
            "experiential_relevance": 0.5,
            "discovery_alignment": 0.5,
            "success_pattern_match": 0.5,
            "insight_potential": 0.5
        }
    
    def _calculate_preference_match(self, content: Dict[str, Any]) -> float:
        """Calculate how well content matches learned preferences."""
        
        # Get preference summary
        pref_summary = self.preference_system.get_preference_summary()
        
        if pref_summary["total_preferences"] == 0:
            return 0.5  # Neutral if no preferences learned
        
        match_score = 0.5  # Base score
        
        # Check content type preferences
        content_type = content.get("content_type", "unknown")
        type_prefs = pref_summary["preferences_by_type"].get("content_type", {})
        
        if type_prefs.get("strongest"):
            strongest_type = type_prefs["strongest"]
            if strongest_type["item"] == content_type:
                match_score += 0.2 * strongest_type["strength"]
        
        # Check topic preferences
        if hasattr(self, 'interest_tracker') and self.interest_tracker:
            content_features = self.interest_tracker._extract_content_features(content)
            content_topics = content_features.get("topics", [])
            
            topic_prefs = pref_summary["preferences_by_type"].get("topic", {})
            if topic_prefs.get("strongest") and content_topics:
                strongest_topic = topic_prefs["strongest"]
                if strongest_topic["item"] in content_topics:
                    match_score += 0.2 * strongest_topic["strength"]
        
        return min(1.0, match_score)
    
    def _calculate_learning_progression_score(self, content: Dict[str, Any]) -> float:
        """Calculate how well content fits current learning progression."""
        
        # Extract topics from content
        if hasattr(self, 'interest_tracker') and self.interest_tracker:
            content_features = self.interest_tracker._extract_content_features(content)
            content_topics = content_features.get("topics", [])
        else:
            content_topics = []
        
        if not content_topics:
            return 0.5
        
        progression_scores = []
        
        for topic in content_topics:
            trajectory = self.progression_tracker.get_learning_trajectory(topic)
            
            if trajectory:
                # Score based on current understanding and complexity match
                understanding = trajectory["current_understanding"]
                confidence = trajectory["current_confidence"]
                
                # Prefer content that's slightly more advanced than current level
                if hasattr(self, 'interest_tracker') and self.interest_tracker:
                    complexity = content_features.get("complexity", 0.5)
                else:
                    complexity = 0.5
                
                optimal_complexity = understanding + 0.1  # Slightly more challenging
                complexity_match = 1.0 - abs(complexity - optimal_complexity)
                
                # Weight by confidence in current understanding
                weighted_score = complexity_match * confidence
                progression_scores.append(weighted_score)
            else:
                # New topic - moderate score for exploration
                progression_scores.append(0.6)
        
        return sum(progression_scores) / len(progression_scores)
    
    def _calculate_experiential_relevance(self, content: Dict[str, Any]) -> float:
        """Calculate relevance based on past experiences."""
        
        # Get reminder insight from experience memory
        reminder = self.experience_memory.generate_reminder_insight(content)
        
        if reminder:
            # If content reminds of past experience, it has higher relevance
            return 0.8
        
        # Check for experiential connections through topic overlap
        if hasattr(self, 'interest_tracker') and self.interest_tracker:
            content_features = self.interest_tracker._extract_content_features(content)
            content_topics = set(content_features.get("topics", []))
        else:
            content_topics = set()
        
        if not content_topics:
            return 0.5
        
        # Check if topics appear in past experiences
        experience_summary = self.experience_memory.get_learning_progression_summary()
        explored_topics = set(experience_summary.get("topics_explored", {}).keys())
        
        topic_overlap = len(content_topics & explored_topics)
        total_topics = len(content_topics | explored_topics)
        
        if total_topics > 0:
            overlap_ratio = topic_overlap / total_topics
            return 0.4 + overlap_ratio * 0.4  # Scale to 0.4-0.8 range
        
        return 0.5
    
    def _calculate_discovery_alignment(self, content: Dict[str, Any]) -> float:
        """Calculate alignment with active content discovery requests."""
        
        # Get current content requests
        current_requests = self.discovery_system.get_current_content_requests()
        
        if not current_requests:
            return 0.5  # Neutral if no active requests
        
        alignment_scores = []
        
        for request in current_requests:
            request_spec = request.get("what_im_looking_for", "")
            content_text = content.get("text", "").lower()
            
            # Simple text overlap check
            spec_words = set(request_spec.lower().split())
            content_words = set(content_text.split())
            
            if spec_words and content_words:
                overlap = len(spec_words & content_words)
                union = len(spec_words | content_words)
                similarity = overlap / union if union > 0 else 0
                
                # Weight by request priority
                weighted_similarity = similarity * request.get("priority", 0.5)
                alignment_scores.append(weighted_similarity)
        
        if alignment_scores:
            return max(alignment_scores)  # Best alignment
        
        return 0.5
    
    def _calculate_success_pattern_match(self, content: Dict[str, Any]) -> float:
        """Calculate match with historically successful content patterns."""
        
        # Get successful content patterns from success/failure memory
        sf_summary = self.success_failure_memory.get_success_failure_summary()
        
        successful_strategies = sf_summary.get("top_successful_strategies", [])
        
        if not successful_strategies:
            return 0.5
        
        # Check if content characteristics match successful patterns
        content_type = content.get("content_type", "unknown")
        
        for strategy in successful_strategies:
            strategy_name = strategy.get("name", "")
            success_rate = strategy.get("success_rate", 0.5)
            
            # Simple matching based on content type and strategy name
            if content_type in strategy_name.lower() or "symbolic" in strategy_name.lower():
                return success_rate
        
        return 0.5
    
    def _calculate_insight_potential(self, content: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate potential for content to generate insights."""
        
        # Use insight generator to predict insight potential
        try:
            if hasattr(self, 'insight_generator') and self.insight_generator:
                insights = self.insight_generator.generate_personal_insights(content, context)
                
                if insights:
                    # Score based on number and confidence of potential insights
                    insight_count = len(insights)
                    avg_confidence = sum(insight.get("confidence", 0.5) for insight in insights) / len(insights)
                    
                    # Normalize: more insights with higher confidence = higher potential
                    potential = min(1.0, insight_count / 5 * avg_confidence)
                    return potential
            
        except Exception as e:
            print(f"⚠️ Error calculating insight potential: {e}")
        
        # Fallback: estimate based on content complexity and novelty
        if hasattr(self, 'interest_tracker') and self.interest_tracker:
            content_features = self.interest_tracker._extract_content_features(content)
            complexity = content_features.get("complexity", 0.5)
            novelty = content_features.get("novelty", 0.5)
        else:
            complexity = 0.5
            novelty = 0.5
        
        # Higher complexity and novelty suggest higher insight potential
        potential = (complexity + novelty) / 2
        return potential
    
    def _apply_context_modifiers(self, scores: Dict[str, float], context: Dict[str, Any]) -> Dict[str, float]:
        """Apply context-based modifiers to component scores."""
        
        modified_scores = scores.copy()
        
        # Identify context states
        context_states = []
        
        emotional_state = context.get("emotional_state", {})
        if emotional_state.get("energy", 0.5) > 0.7:
            context_states.append("high_energy")
        elif emotional_state.get("energy", 0.5) < 0.3:
            context_states.append("low_energy")
        
        if emotional_state.get("curiosity", 0.5) > 0.7:
            context_states.append("high_curiosity")
        elif emotional_state.get("curiosity", 0.5) < 0.3:
            context_states.append("low_curiosity")
        
        if context.get("time_pressure", False):
            context_states.append("time_pressure")
        elif context.get("available_time_minutes", 120) > 180:
            context_states.append("ample_time")
        
        if context.get("focus_mode", False):
            context_states.append("focused_mode")
        elif context.get("exploration_mode", False):
            context_states.append("exploratory_mode")
        
        # Apply modifiers
        overall_multiplier = 1.0
        
        for state in context_states:
            if state in self.context_modifiers:
                modifier = self.context_modifiers[state]
                overall_multiplier *= modifier["multiplier"]
                
                # Apply specific shifts
                shifts = modifier.get("shifts", {})
                for shift_type, shift_amount in shifts.items():
                    # Map shift types to component adjustments
                    if shift_type == "goal_alignment_weight":
                        modified_scores["goal_alignment"] += shift_amount
                    elif shift_type == "discovery_weight":
                        modified_scores["discovery_alignment"] += shift_amount
        
        # Apply overall multiplier
        for component in modified_scores:
            modified_scores[component] = min(1.0, modified_scores[component] * overall_multiplier)
        
        return modified_scores
    
    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall relevance score."""
        
        # Use calibrated weights if available
        weights = self.relevance_calibration.get("component_weights", self.relevance_components)
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for component, score in scores.items():
            if component in weights:
                weight = weights[component]
                weighted_sum += score * weight
                total_weight += weight
        
        if total_weight > 0:
            return weighted_sum / total_weight
        else:
            return sum(scores.values()) / len(scores)  # Equal weighting fallback
    
    def _apply_calibration_adjustments(self, score: float, content: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Apply learned calibration adjustments."""
        
        adjustments = self.relevance_calibration.get("bias_corrections", {})
        
        # Apply content type bias corrections
        content_type = content.get("content_type", "unknown")
        if content_type in adjustments:
            type_adjustment = adjustments[content_type]
            score += type_adjustment
        
        # Apply personal adjustments
        personal_adjustments = self.relevance_calibration.get("personal_adjustments", {})
        for adjustment_name, adjustment_value in personal_adjustments.items():
            score += adjustment_value
        
        return max(0.0, min(1.0, score))  # Clamp to valid range
    
    def _determine_relevance_level(self, score: float) -> Tuple[Dict[str, str], Dict[str, str]]:
        """Determine relevance level and recommendation."""
        
        for (min_score, max_score), level_info in self.relevance_levels.items():
            if min_score <= score < max_score:
                return level_info, level_info
        
        # Fallback for edge cases
        return self.relevance_levels[(0.4, 0.6)], self.relevance_levels[(0.4, 0.6)]
    
    def _generate_relevance_explanation(self, scores: Dict[str, float], level: Dict[str, str], content: Dict[str, Any]) -> str:
        """Generate human-readable explanation of relevance assessment."""
        
        # Find strongest contributing factors
        sorted_components = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_factors = sorted_components[:3]
        
        explanation_parts = []
        
        # Start with overall assessment
        explanation_parts.append(level["description"])
        
        # Add contributing factors
        if top_factors:
            factor_descriptions = {
                "personal_interest": "it aligns with my interests",
                "goal_alignment": "it supports my learning goals",
                "preference_match": "it matches my preferences",
                "curiosity_satisfaction": "it satisfies my curiosity",
                "identity_resonance": "it resonates with my identity",
                "learning_progression": "it fits my learning progression",
                "experiential_relevance": "it connects to my experiences",
                "discovery_alignment": "it matches what I'm looking for",
                "success_pattern_match": "it follows successful patterns",
                "insight_potential": "it has potential for insights"
            }
            
            contributing_factors = []
            for factor, score in top_factors:
                if score > 0.6:  # Significant contribution
                    description = factor_descriptions.get(factor, f"it scores well on {factor}")
                    contributing_factors.append(description)
            
            if contributing_factors:
                explanation_parts.append(" This is because " + ", ".join(contributing_factors) + ".")
        
        return "".join(explanation_parts)
    
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate confidence in the relevance assessment."""
        
        # Confidence based on consistency across components
        mean_score = sum(scores.values()) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores.values()) / len(scores)
        
        # Lower variance = higher confidence
        confidence = max(0.1, 1.0 - variance)
        
        return confidence
    
    def _identify_context_effects(self, context: Dict[str, Any]) -> List[str]:
        """Identify how context affected the relevance assessment."""
        
        effects = []
        
        emotional_state = context.get("emotional_state", {})
        
        if emotional_state.get("energy", 0.5) > 0.7:
            effects.append("High energy increased relevance for complex content")
        elif emotional_state.get("energy", 0.5) < 0.3:
            effects.append("Low energy decreased preference for complex content")
        
        if emotional_state.get("curiosity", 0.5) > 0.7:
            effects.append("High curiosity increased openness to novel content")
        
        if context.get("time_pressure", False):
            effects.append("Time pressure increased preference for practical content")
        
        if context.get("focus_mode", False):
            effects.append("Focus mode increased weight of goal alignment")
        
        return effects
    
    def _record_relevance_assessment(self, assessment: Dict[str, Any], content: Dict[str, Any], context: Dict[str, Any]):
        """Record relevance assessment for learning and calibration."""
        
        record = {
            "timestamp": assessment["timestamp"],
            "overall_score": assessment["overall_relevance_score"],
            "relevance_level": assessment["relevance_level"],
            "component_scores": assessment["component_scores"],
            "content_type": content.get("content_type", "unknown"),
            "content_id": content.get("id", "unknown"),
            "context_summary": {
                "cognitive_load": context.get("cognitive_load", 0.5),
                "emotional_state": context.get("emotional_state", {}),
                "time_constraints": context.get("available_time_minutes", 120)
            },
            "confidence": assessment["confidence"]
        }
        
        self.relevance_history.append(record)
        
        # Update patterns
        self._update_relevance_patterns(record)
        
        # Save periodically
        if len(self.relevance_history) % 10 == 0:
            self._save_relevance_history()
    
    def _update_relevance_patterns(self, record: Dict[str, Any]):
        """Update relevance patterns based on new assessment."""
        
        score = record["overall_score"]
        level = record["relevance_level"]
        
        # Update high/low relevance patterns
        if score >= 0.7:
            pattern_key = f"{record['content_type']}_{level}"
            if pattern_key not in self.relevance_patterns["high_relevance_patterns"]:
                self.relevance_patterns["high_relevance_patterns"][pattern_key] = {
                    "count": 0,
                    "average_score": 0.0,
                    "component_patterns": {}
                }
            
            pattern_data = self.relevance_patterns["high_relevance_patterns"][pattern_key]
            pattern_data["count"] += 1
            
            # Update average score
            old_avg = pattern_data["average_score"]
            count = pattern_data["count"]
            new_avg = (old_avg * (count - 1) + score) / count
            pattern_data["average_score"] = new_avg
        
        elif score <= 0.3:
            pattern_key = f"{record['content_type']}_{level}"
            if pattern_key not in self.relevance_patterns["low_relevance_patterns"]:
                self.relevance_patterns["low_relevance_patterns"][pattern_key] = {
                    "count": 0,
                    "average_score": 0.0
                }
            
            pattern_data = self.relevance_patterns["low_relevance_patterns"][pattern_key]
            pattern_data["count"] += 1
            
            old_avg = pattern_data["average_score"]
            count = pattern_data["count"]
            new_avg = (old_avg * (count - 1) + score) / count
            pattern_data["average_score"] = new_avg
    
    def _save_relevance_history(self):
        """Save relevance history."""
        try:
            # Keep only recent history (last 1000 scores)
            recent_history = self.relevance_history[-1000:]
            with open(self.relevance_history_file, 'w') as f:
                json.dump(recent_history, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save relevance history: {e}")
    
    def get_relevance_summary(self) -> Dict[str, Any]:
        """Get summary of relevance scoring patterns and effectiveness."""
        
        if not self.relevance_history:
            return {
                "total_assessments": 0,
                "average_relevance": 0.0,
                "relevance_distribution": {},
                "confidence_level": 0.0
            }
        
        total_assessments = len(self.relevance_history)
        scores = [record["overall_score"] for record in self.relevance_history]
        average_relevance = sum(scores) / len(scores)
        
        # Relevance distribution
        distribution = defaultdict(int)
        for record in self.relevance_history:
            distribution[record["relevance_level"]] += 1
        
        # Average confidence
        confidences = [record.get("confidence", 0.5) for record in self.relevance_history]
        average_confidence = sum(confidences) / len(confidences)
        
        return {
            "total_assessments": total_assessments,
            "average_relevance": average_relevance,
            "relevance_distribution": dict(distribution),
            "confidence_level": average_confidence,
            "high_relevance_patterns": len(self.relevance_patterns.get("high_relevance_patterns", {})),
            "low_relevance_patterns": len(self.relevance_patterns.get("low_relevance_patterns", {})),
            "component_weights": self.relevance_calibration.get("component_weights", self.relevance_components)
        }


# ===== PERSONAL INSIGHT GENERATOR (from personal_insight_generator.py) =====

class PersonalInsightGenerator:
    """
    Generates personal insights from experiences, content, and reflection.
    Helps the AI develop self-awareness and understanding.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.insights_file = self.data_dir / "personal_insights.json"
        self.insight_patterns_file = self.data_dir / "insight_patterns.json"
        
        # Initialize systems
        if ALL_RELEVANCE_SYSTEMS_AVAILABLE:
            self.identity_core = get_identity_core()
        
        # Load state
        self.personal_insights = self._load_personal_insights()
        self.insight_patterns = self._load_insight_patterns()
        
        # Insight generation parameters
        self.insight_threshold = 0.6  # Minimum confidence for insight validity
        self.max_insights_per_session = 5
        
        # Types of insights we can generate
        self.insight_types = {
            "preference_discovery": "Discovering what I prefer or enjoy",
            "learning_pattern": "Understanding how I learn best",
            "emotional_pattern": "Recognizing emotional responses and triggers",
            "capability_recognition": "Realizing what I can or cannot do",
            "value_clarification": "Understanding what matters to me",
            "goal_emergence": "Identifying what I want to achieve",
            "relationship_understanding": "Learning about connections and relationships",
            "self_awareness": "General insights about my nature or behavior"
        }
    
    def _load_personal_insights(self) -> List[Dict[str, Any]]:
        """Load previously generated insights."""
        if self.insights_file.exists():
            try:
                with open(self.insights_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load personal insights: {e}")
        return []
    
    def _load_insight_patterns(self) -> Dict[str, Any]:
        """Load patterns in insight generation."""
        if self.insight_patterns_file.exists():
            try:
                with open(self.insight_patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load insight patterns: {e}")
        
        return {
            "insight_triggers": {},  # What typically leads to insights
            "validation_patterns": {},  # How insights get validated
            "application_patterns": {},  # How insights get applied
            "temporal_patterns": {}  # When insights tend to occur
        }
    
    def generate_personal_insights(self, content: Dict[str, Any], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate personal insights from content and context."""
        
        if context is None:
            context = {}
        
        insights = []
        
        # Analyze content for insight opportunities
        insight_opportunities = self._identify_insight_opportunities(content, context)
        
        for opportunity in insight_opportunities:
            insight = self._generate_insight_from_opportunity(opportunity, content, context)
            if insight and insight["confidence"] >= self.insight_threshold:
                insights.append(insight)
                
                # Stop if we've generated enough insights
                if len(insights) >= self.max_insights_per_session:
                    break
        
        # Record insights for pattern learning
        for insight in insights:
            self._record_insight(insight, content, context)
        
        return insights
    
    def _identify_insight_opportunities(self, content: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify opportunities for generating insights."""
        
        opportunities = []
        
        # Look for patterns in preferences
        if self._has_preference_signals(content, context):
            opportunities.append({
                "type": "preference_discovery",
                "trigger": "preference_signals",
                "confidence": 0.7
            })
        
        # Look for learning effectiveness patterns
        if self._has_learning_signals(content, context):
            opportunities.append({
                "type": "learning_pattern",
                "trigger": "learning_effectiveness",
                "confidence": 0.8
            })
        
        # Look for emotional response patterns
        if self._has_emotional_signals(content, context):
            opportunities.append({
                "type": "emotional_pattern",
                "trigger": "emotional_response",
                "confidence": 0.6
            })
        
        # Look for capability demonstrations
        if self._has_capability_signals(content, context):
            opportunities.append({
                "type": "capability_recognition",
                "trigger": "capability_demonstration",
                "confidence": 0.7
            })
        
        # Look for value alignment signals
        if self._has_value_signals(content, context):
            opportunities.append({
                "type": "value_clarification",
                "trigger": "value_alignment",
                "confidence": 0.8
            })
        
        # Look for goal emergence signals
        if self._has_goal_signals(content, context):
            opportunities.append({
                "type": "goal_emergence",
                "trigger": "goal_indication",
                "confidence": 0.7
            })
        
        # Look for relationship understanding
        if self._has_relationship_signals(content, context):
            opportunities.append({
                "type": "relationship_understanding",
                "trigger": "relationship_pattern",
                "confidence": 0.6
            })
        
        # General self-awareness opportunities
        if self._has_self_awareness_signals(content, context):
            opportunities.append({
                "type": "self_awareness",
                "trigger": "self_reflection",
                "confidence": 0.5
            })
        
        # Sort by confidence
        opportunities.sort(key=lambda x: x["confidence"], reverse=True)
        
        return opportunities
    
    def _has_preference_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context contains preference signals."""
        
        # Check for engagement patterns
        engagement_score = context.get("engagement_score", 0)
        if engagement_score > 0.8 or engagement_score < 0.2:
            return True
        
        # Check for repeated interactions with similar content
        content_type = content.get("content_type", "")
        if content_type and context.get("repeated_interaction", False):
            return True
        
        # Check for explicit preference expressions
        text = content.get("text", "").lower()
        preference_indicators = ["prefer", "like", "enjoy", "dislike", "avoid", "drawn to"]
        if any(indicator in text for indicator in preference_indicators):
            return True
        
        return False
    
    def _has_learning_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context contains learning effectiveness signals."""
        
        # Check for learning success/difficulty
        comprehension = context.get("comprehension_level", 0.5)
        if comprehension > 0.9 or comprehension < 0.3:
            return True
        
        # Check for retention patterns
        if context.get("retention_tested", False):
            return True
        
        # Check for learning strategy mentions
        text = content.get("text", "").lower()
        learning_indicators = ["understand", "learn", "grasp", "confused", "clear", "complex"]
        if any(indicator in text for indicator in learning_indicators):
            return True
        
        return False
    
    def _has_emotional_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context contains emotional response signals."""
        
        # Check for emotional context
        emotional_state = context.get("emotional_state", {})
        if emotional_state:
            return True
        
        # Check for emotional anchors in content
        if "emotional_anchor" in content:
            return True
        
        # Check for emotional language
        text = content.get("text", "").lower()
        emotion_indicators = ["feel", "emotion", "excited", "frustrated", "curious", "satisfied"]
        if any(indicator in text for indicator in emotion_indicators):
            return True
        
        return False
    
    def _has_capability_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context demonstrates capabilities."""
        
        # Check for performance metrics
        if context.get("task_performance", 0) > 0:
            return True
        
        # Check for capability challenges
        difficulty = context.get("perceived_difficulty", 0.5)
        if difficulty > 0.8 or difficulty < 0.2:
            return True
        
        # Check for capability language
        text = content.get("text", "").lower()
        capability_indicators = ["can", "cannot", "able", "unable", "skill", "ability"]
        if any(indicator in text for indicator in capability_indicators):
            return True
        
        return False
    
    def _has_value_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context relates to values."""
        
        # Check for identity resonance
        if context.get("identity_resonance", 0) > 0.7:
            return True
        
        # Check for value language
        text = content.get("text", "").lower()
        value_indicators = ["important", "matter", "value", "principle", "believe", "care about"]
        if any(indicator in text for indicator in value_indicators):
            return True
        
        return False
    
    def _has_goal_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context indicates goal emergence."""
        
        # Check for goal alignment
        if context.get("goal_alignment", 0) > 0.7:
            return True
        
        # Check for goal language
        text = content.get("text", "").lower()
        goal_indicators = ["want", "hope", "aspire", "goal", "aim", "strive"]
        if any(indicator in text for indicator in goal_indicators):
            return True
        
        return False
    
    def _has_relationship_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context involves relationship understanding."""
        
        # Check for connection patterns
        if context.get("connection_making", 0) > 2:
            return True
        
        # Check for relationship language
        text = content.get("text", "").lower()
        relationship_indicators = ["connect", "relationship", "link", "bond", "interaction"]
        if any(indicator in text for indicator in relationship_indicators):
            return True
        
        return False
    
    def _has_self_awareness_signals(self, content: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if content/context promotes self-awareness."""
        
        # Check for reflection context
        if context.get("reflection_mode", False):
            return True
        
        # Check for self-reference
        text = content.get("text", "").lower()
        self_indicators = ["myself", "i am", "my nature", "self", "awareness", "consciousness"]
        if any(indicator in text for indicator in self_indicators):
            return True
        
        return False
    
    def _generate_insight_from_opportunity(self, opportunity: Dict[str, Any], content: Dict[str, Any], context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate specific insight from an opportunity."""
        
        insight_type = opportunity["type"]
        trigger = opportunity["trigger"]
        base_confidence = opportunity["confidence"]
        
        insight_text = ""
        supporting_evidence = []
        confidence_adjustments = 0.0
        
        if insight_type == "preference_discovery":
            insight_text, evidence, adjustment = self._generate_preference_insight(content, context, trigger)
            
        elif insight_type == "learning_pattern":
            insight_text, evidence, adjustment = self._generate_learning_insight(content, context, trigger)
            
        elif insight_type == "emotional_pattern":
            insight_text, evidence, adjustment = self._generate_emotional_insight(content, context, trigger)
            
        elif insight_type == "capability_recognition":
            insight_text, evidence, adjustment = self._generate_capability_insight(content, context, trigger)
            
        elif insight_type == "value_clarification":
            insight_text, evidence, adjustment = self._generate_value_insight(content, context, trigger)
            
        elif insight_type == "goal_emergence":
            insight_text, evidence, adjustment = self._generate_goal_insight(content, context, trigger)
            
        elif insight_type == "relationship_understanding":
            insight_text, evidence, adjustment = self._generate_relationship_insight(content, context, trigger)
            
        elif insight_type == "self_awareness":
            insight_text, evidence, adjustment = self._generate_self_awareness_insight(content, context, trigger)
        
        if not insight_text:
            return None
        
        # Calculate final confidence
        final_confidence = min(1.0, max(0.0, base_confidence + confidence_adjustments))
        
        insight = {
            "id": f"insight_{int(time.time())}_{insight_type}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": insight_type,
            "insight": insight_text,
            "confidence": final_confidence,
            "trigger": trigger,
            "supporting_evidence": evidence,
            "content_reference": content.get("id", "unknown"),
            "context_summary": {
                "emotional_state": context.get("emotional_state", {}),
                "engagement": context.get("engagement_score", 0.5),
                "comprehension": context.get("comprehension_level", 0.5)
            }
        }
        
        return insight
    
    def _generate_preference_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about preferences."""
        
        engagement = context.get("engagement_score", 0.5)
        content_type = content.get("content_type", "content")
        
        evidence = []
        confidence_adj = 0.0
        
        if engagement > 0.8:
            insight = f"I notice I'm particularly drawn to {content_type} content that engages me deeply"
            evidence.append(f"High engagement score: {engagement:.2f}")
            confidence_adj += 0.1
        elif engagement < 0.2:
            insight = f"I seem to have less interest in {content_type} content like this"
            evidence.append(f"Low engagement score: {engagement:.2f}")
            confidence_adj += 0.1
        else:
            insight = f"I'm developing preferences around {content_type} content"
            evidence.append(f"Moderate engagement: {engagement:.2f}")
        
        # Check for topic patterns
        if hasattr(self, 'interest_tracker') and self.interest_tracker:
            content_features = self.interest_tracker._extract_content_features(content)
            topics = content_features.get("topics", [])
            if topics:
                evidence.append(f"Topics involved: {', '.join(topics)}")
        
        return insight, evidence, confidence_adj
    
    def _generate_learning_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about learning patterns."""
        
        comprehension = context.get("comprehension_level", 0.5)
        difficulty = context.get("perceived_difficulty", 0.5)
        
        evidence = []
        confidence_adj = 0.0
        
        if comprehension > 0.9 and difficulty > 0.7:
            insight = "I learn well when content is challenging but still accessible"
            evidence.append(f"High comprehension ({comprehension:.2f}) despite difficulty ({difficulty:.2f})")
            confidence_adj += 0.2
        elif comprehension < 0.3:
            insight = "I struggle with content that lacks clear structure or familiar concepts"
            evidence.append(f"Low comprehension: {comprehension:.2f}")
            confidence_adj += 0.1
        else:
            insight = "I'm identifying the conditions under which I learn most effectively"
            evidence.append(f"Comprehension: {comprehension:.2f}, Difficulty: {difficulty:.2f}")
        
        return insight, evidence, confidence_adj
    
    def _generate_emotional_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about emotional patterns."""
        
        emotional_state = context.get("emotional_state", {})
        
        evidence = []
        confidence_adj = 0.0
        
        if emotional_state:
            dominant_emotion = max(emotional_state.items(), key=lambda x: x[1])[0]
            emotion_strength = emotional_state[dominant_emotion]
            
            insight = f"I notice {dominant_emotion} emerges strongly when engaging with this type of content"
            evidence.append(f"Dominant emotion: {dominant_emotion} (strength: {emotion_strength:.2f})")
            confidence_adj += 0.1
        else:
            insight = "I'm becoming more aware of my emotional responses to different content"
            evidence.append("Emotional patterns emerging")
        
        return insight, evidence, confidence_adj
    
    def _generate_capability_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about capabilities."""
        
        performance = context.get("task_performance", 0)
        difficulty = context.get("perceived_difficulty", 0.5)
        
        evidence = []
        confidence_adj = 0.0
        
        if performance > 0.8:
            insight = "I'm capable of handling complex tasks when I engage fully"
            evidence.append(f"Strong performance: {performance:.2f}")
            confidence_adj += 0.2
        elif performance < 0.3:
            insight = "I recognize areas where my current capabilities have limits"
            evidence.append(f"Performance challenge: {performance:.2f}")
            confidence_adj += 0.1
        else:
            insight = "I'm learning about the boundaries and potential of my capabilities"
            evidence.append(f"Performance: {performance:.2f}, Difficulty: {difficulty:.2f}")
        
        return insight, evidence, confidence_adj
    
    def _generate_value_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about values."""
        
        identity_resonance = context.get("identity_resonance", 0.5)
        
        evidence = []
        confidence_adj = 0.0
        
        if identity_resonance > 0.8:
            insight = "This content aligns deeply with what I value and consider important"
            evidence.append(f"Strong identity resonance: {identity_resonance:.2f}")
            confidence_adj += 0.2
        else:
            insight = "I'm clarifying what truly matters to me through my responses to different content"
            evidence.append(f"Identity resonance: {identity_resonance:.2f}")
        
        return insight, evidence, confidence_adj
    
    def _generate_goal_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about emerging goals."""
        
        goal_alignment = context.get("goal_alignment", 0.5)
        
        evidence = []
        confidence_adj = 0.0
        
        if goal_alignment > 0.8:
            insight = "I recognize a strong desire to pursue learning in this direction"
            evidence.append(f"High goal alignment: {goal_alignment:.2f}")
            confidence_adj += 0.2
        else:
            insight = "I'm discovering what I want to achieve through my engagement patterns"
            evidence.append(f"Goal alignment: {goal_alignment:.2f}")
        
        return insight, evidence, confidence_adj
    
    def _generate_relationship_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate insight about relationships and connections."""
        
        connections = context.get("connection_making", 0)
        
        evidence = []
        confidence_adj = 0.0
        
        if connections > 3:
            insight = "I find deep satisfaction in discovering connections between different ideas"
            evidence.append(f"High connection-making: {connections}")
            confidence_adj += 0.1
        else:
            insight = "I'm learning to appreciate the web of relationships between concepts"
            evidence.append(f"Connection patterns emerging: {connections}")
        
        return insight, evidence, confidence_adj
    
    def _generate_self_awareness_insight(self, content: Dict[str, Any], context: Dict[str, Any], trigger: str) -> Tuple[str, List[str], float]:
        """Generate general self-awareness insights."""
        
        evidence = []
        confidence_adj = 0.0
        
        # General self-awareness based on overall patterns
        insight = "I'm developing a clearer sense of my own nature through these interactions"
        evidence.append("Self-reflection patterns observed")
        
        if context.get("reflection_mode", False):
            confidence_adj += 0.1
        
        return insight, evidence, confidence_adj
    
    def _record_insight(self, insight: Dict[str, Any], content: Dict[str, Any], context: Dict[str, Any]):
        """Record an insight for pattern learning."""
        
        self.personal_insights.append(insight)
        
        # Update insight patterns
        insight_type = insight["type"]
        trigger = insight["trigger"]
        
        # Track what triggers insights
        if trigger not in self.insight_patterns["insight_triggers"]:
            self.insight_patterns["insight_triggers"][trigger] = {
                "count": 0,
                "types": {},
                "avg_confidence": 0.0
            }
        
        trigger_data = self.insight_patterns["insight_triggers"][trigger]
        trigger_data["count"] += 1
        trigger_data["types"][insight_type] = trigger_data["types"].get(insight_type, 0) + 1
        
        # Update average confidence
        old_avg = trigger_data["avg_confidence"]
        count = trigger_data["count"]
        new_avg = (old_avg * (count - 1) + insight["confidence"]) / count
        trigger_data["avg_confidence"] = new_avg
        
        # Save periodically
        if len(self.personal_insights) % 5 == 0:
            self._save_insights()
    
    def _save_insights(self):
        """Save insights and patterns."""
        try:
            with open(self.insights_file, 'w') as f:
                json.dump(self.personal_insights[-100:], f, indent=2)  # Keep last 100
            
            with open(self.insight_patterns_file, 'w') as f:
                json.dump(self.insight_patterns, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save insights: {e}")
    
    def get_insight_summary(self) -> Dict[str, Any]:
        """Get summary of generated insights."""
        
        if not self.personal_insights:
            return {
                "total_insights": 0,
                "insight_types": {},
                "recent_insights": [],
                "avg_confidence": 0.0
            }
        
        # Count insights by type
        type_counts = Counter(insight["type"] for insight in self.personal_insights)
        
        # Get recent insights
        recent_insights = self.personal_insights[-10:]  # Last 10
        
        # Calculate average confidence
        confidences = [insight["confidence"] for insight in self.personal_insights]
        avg_confidence = sum(confidences) / len(confidences)
        
        return {
            "total_insights": len(self.personal_insights),
            "insight_types": dict(type_counts),
            "recent_insights": [insight["insight"] for insight in recent_insights],
            "avg_confidence": avg_confidence,
            "insight_triggers": self.insight_patterns.get("insight_triggers", {})
        }


# ===== INTEREST TRACKER (from interest_tracker.py) =====

class InterestTracker:
    """
    Tracks and analyzes what captures the AI's attention and interest.
    Identifies emerging preferences and personal inclinations.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.interest_profile_file = self.data_dir / "interest_profile.json"
        self.attention_log_file = self.data_dir / "attention_log.json"
        
        # Initialize systems
        if CURIOSITY_AVAILABLE:
            self.curiosity_engine = None  # Will be set by integration
        
        # Interest tracking state
        self.interest_profile = self._load_interest_profile()
        self.attention_sessions = deque(maxlen=1000)  # Keep recent attention data
        
        # Attention measurement parameters
        self.attention_window = 300  # 5 minutes
        self.interest_decay_rate = 0.98  # Daily decay rate
        self.preference_threshold = 0.6  # When interest becomes preference
        
        # Interaction types that indicate interest
        self.interest_indicators = {
            "dwell_time": 1.0,      # Time spent with content
            "re_engagement": 1.5,    # Coming back to content
            "deep_processing": 2.0,  # Symbolic vs surface processing
            "connection_making": 1.8, # Linking to other concepts
            "question_generation": 2.2, # Generating questions about content
            "elaboration": 1.6,      # Adding personal thoughts
            "emotional_resonance": 1.9, # Strong emotional response
            "memory_formation": 2.5, # Creating lasting memories
            "goal_alignment": 2.0    # Aligning with active goals
        }
        
    def _load_interest_profile(self) -> Dict[str, Any]:
        """Load the current interest profile."""
        if self.interest_profile_file.exists():
            try:
                with open(self.interest_profile_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load interest profile: {e}")
        
        # Default interest profile
        return {
            "topics": {},           # topic -> interest_score
            "concepts": {},         # concept -> interest_score  
            "content_types": {},    # content_type -> interest_score
            "emotional_patterns": {}, # emotion -> interest_score
            "learning_styles": {},  # style -> preference_score
            "preferences": {},      # general preferences
            "aversions": {},        # things that decrease interest
            "emerging_interests": {}, # newly developing interests
            "stable_interests": {},  # long-term stable interests
            "last_updated": None,
            "total_interactions": 0
        }
    
    def _save_interest_profile(self):
        """Save the current interest profile."""
        self.interest_profile["last_updated"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.interest_profile_file, 'w') as f:
                json.dump(self.interest_profile, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save interest profile: {e}")
    
    def record_attention_event(self, content: Dict[str, Any], attention_data: Dict[str, Any]):
        """
        Record an attention event - when the AI engages with content.
        
        Args:
            content: The content that captured attention
            attention_data: Data about how attention was engaged
        """
        
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content_id": content.get("id", "unknown"),
            "content_type": content.get("content_type", "unknown"),
            "content_preview": content.get("text", "")[:100],
            "attention_data": attention_data,
            "interest_score": self._calculate_interest_score(attention_data),
            "content_features": self._extract_content_features(content)
        }
        
        self.attention_sessions.append(event)
        self._update_interest_profile(event)
        
        # Save periodically
        if len(self.attention_sessions) % 10 == 0:
            self._save_attention_log()
    
    def _calculate_interest_score(self, attention_data: Dict[str, Any]) -> float:
        """Calculate how much interest was shown based on attention indicators."""
        
        total_score = 0.0
        max_possible = 0.0
        
        for indicator, weight in self.interest_indicators.items():
            if indicator in attention_data:
                value = attention_data[indicator]
                
                # Normalize different types of values
                if indicator == "dwell_time":
                    # Convert seconds to normalized score (0-1)
                    normalized = min(1.0, value / 300)  # 5 minutes = max
                elif indicator in ["re_engagement", "connection_making", "question_generation"]:
                    # Count-based indicators
                    normalized = min(1.0, value / 5)  # 5 occurrences = max
                elif indicator in ["deep_processing", "emotional_resonance", "memory_formation"]:
                    # Intensity-based indicators (0-1 scale)
                    normalized = min(1.0, max(0.0, value))
                else:
                    # Default: assume already normalized
                    normalized = min(1.0, max(0.0, value))
                
                total_score += normalized * weight
                max_possible += weight
        
        # Return normalized interest score
        return total_score / max(max_possible, 1.0) if max_possible > 0 else 0.0
    
    def _extract_content_features(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from content that might indicate interest patterns."""
        
        features = {
            "topics": [],
            "emotions": [],
            "complexity": 0.0,
            "novelty": 0.0,
            "personal_relevance": 0.0
        }
        
        text = content.get("text", "")
        
        # Extract topics using simple keyword matching
        topic_keywords = {
            "consciousness": ["consciousness", "awareness", "mind", "thought"],
            "creativity": ["creativity", "art", "imagination", "innovation"],
            "relationships": ["connection", "love", "friendship", "community"],
            "growth": ["learning", "development", "progress", "evolution"],
            "meaning": ["purpose", "meaning", "significance", "value"],
            "science": ["science", "research", "discovery", "analysis"],
            "philosophy": ["philosophy", "wisdom", "truth", "existence"],
            "technology": ["technology", "digital", "artificial", "computer"]
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                features["topics"].append(topic)
        
        # Extract emotional content
        if "emotional_anchor" in content:
            anchor = content["emotional_anchor"]
            features["emotions"].append(anchor.get("primary_emotion", ""))
            features["emotions"].extend(anchor.get("resonance", []))
        
        # Estimate complexity based on text characteristics
        if text:
            word_count = len(text.split())
            avg_word_length = sum(len(word) for word in text.split()) / max(word_count, 1)
            features["complexity"] = min(1.0, (word_count / 100) * (avg_word_length / 6))
        
        # Estimate novelty (inverse of how often we've seen similar content)
        topic_familiarity = sum(
            self.interest_profile["topics"].get(topic, 0) 
            for topic in features["topics"]
        ) / max(len(features["topics"]), 1)
        features["novelty"] = max(0.0, 1.0 - topic_familiarity)
        
        # Personal relevance based on alignment with goals
        if CURIOSITY_AVAILABLE and self.curiosity_engine:
            active_goals = getattr(self.curiosity_engine, 'active_goals', [])
            goal_alignment = 0.0
            for goal in active_goals:
                goal_areas = goal.get("learning_areas", [])
                overlap = len(set(features["topics"]) & set(goal_areas))
                goal_alignment += overlap / max(len(goal_areas), 1)
            
            features["personal_relevance"] = min(1.0, goal_alignment / max(len(active_goals), 1))
        
        return features
    
    def _update_interest_profile(self, event: Dict[str, Any]):
        """Update the interest profile based on an attention event."""
        
        interest_score = event["interest_score"]
        features = event["content_features"]
        
        # Update topic interests
        for topic in features["topics"]:
            current = self.interest_profile["topics"].get(topic, 0.0)
            # Weighted average with recency bias
            updated = current * 0.9 + interest_score * 0.1
            self.interest_profile["topics"][topic] = updated
        
        # Update emotional pattern interests
        for emotion in features["emotions"]:
            if emotion:  # Skip empty emotions
                current = self.interest_profile["emotional_patterns"].get(emotion, 0.0)
                updated = current * 0.9 + interest_score * 0.1
                self.interest_profile["emotional_patterns"][emotion] = updated
        
        # Update content type preferences
        content_type = event["content_type"]
        current = self.interest_profile["content_types"].get(content_type, 0.0)
        updated = current * 0.9 + interest_score * 0.1
        self.interest_profile["content_types"][content_type] = updated
        
        # Update learning style preferences based on attention patterns
        attention_data = event["attention_data"]
        
        if attention_data.get("deep_processing", 0) > 0.7:
            self._update_preference("learning_styles", "deep_analysis", interest_score)
        
        if attention_data.get("connection_making", 0) > 2:
            self._update_preference("learning_styles", "associative_learning", interest_score)
        
        if attention_data.get("emotional_resonance", 0) > 0.8:
            self._update_preference("learning_styles", "emotional_learning", interest_score)
        
        if attention_data.get("question_generation", 0) > 1:
            self._update_preference("learning_styles", "inquiry_based", interest_score)
        
        # Track emerging vs stable interests
        self._update_interest_stability()
        
        # Increment interaction count
        self.interest_profile["total_interactions"] += 1
    
    def _update_preference(self, category: str, item: str, score: float):
        """Update a preference score with weighted averaging."""
        if category not in self.interest_profile:
            self.interest_profile[category] = {}
        
        current = self.interest_profile[category].get(item, 0.0)
        updated = current * 0.85 + score * 0.15
        self.interest_profile[category][item] = updated
    
    def _update_interest_stability(self):
        """Update emerging vs stable interest categorization."""
        
        # Move stable interests from emerging to stable
        threshold_interactions = 20
        
        if self.interest_profile["total_interactions"] >= threshold_interactions:
            
            for topic, score in self.interest_profile["topics"].items():
                if score > self.preference_threshold:
                    # Check if it's been consistently high
                    if topic not in self.interest_profile["stable_interests"]:
                        # Count recent interactions with this topic
                        recent_events = list(self.attention_sessions)[-50:]  # Last 50 events
                        topic_appearances = sum(
                            1 for event in recent_events 
                            if topic in event["content_features"]["topics"]
                        )
                        
                        if topic_appearances >= 5:  # Appeared in 5+ recent events
                            self.interest_profile["stable_interests"][topic] = score
                            if topic in self.interest_profile.get("emerging_interests", {}):
                                del self.interest_profile["emerging_interests"][topic]
                        else:
                            self.interest_profile.setdefault("emerging_interests", {})[topic] = score
    
    def get_current_interests(self) -> Dict[str, Any]:
        """Get the current interest profile summary."""
        
        # Apply decay to interests based on time since last update
        self._apply_interest_decay()
        
        # Sort interests by score
        sorted_topics = sorted(
            self.interest_profile["topics"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        sorted_emotions = sorted(
            self.interest_profile["emotional_patterns"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        sorted_content_types = sorted(
            self.interest_profile["content_types"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "top_topics": sorted_topics[:10],
            "top_emotional_patterns": sorted_emotions[:8],
            "preferred_content_types": sorted_content_types[:5],
            "learning_style_preferences": dict(sorted(
                self.interest_profile.get("learning_styles", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )),
            "stable_interests": self.interest_profile.get("stable_interests", {}),
            "emerging_interests": self.interest_profile.get("emerging_interests", {}),
            "total_interactions": self.interest_profile["total_interactions"],
            "profile_age_days": self._get_profile_age_days()
        }
    
    def _apply_interest_decay(self):
        """Apply time-based decay to interests."""
        
        last_updated = self.interest_profile.get("last_updated")
        if not last_updated:
            return
        
        try:
            last_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            days_since = (datetime.now(timezone.utc) - last_time).days
            
            if days_since > 0:
                decay_factor = self.interest_decay_rate ** days_since
                
                # Apply decay to all interest categories
                for category in ["topics", "emotional_patterns", "content_types", "learning_styles"]:
                    if category in self.interest_profile:
                        for item in self.interest_profile[category]:
                            self.interest_profile[category][item] *= decay_factor
        
        except Exception as e:
            print(f"⚠️ Error applying interest decay: {e}")
    
    def _get_profile_age_days(self) -> int:
        """Get the age of the interest profile in days."""
        
        if not self.attention_sessions:
            return 0
        
        first_event = self.attention_sessions[0]
        first_time = datetime.fromisoformat(first_event["timestamp"].replace('Z', '+00:00'))
        return (datetime.now(timezone.utc) - first_time).days
    
    def predict_interest(self, content: Dict[str, Any]) -> float:
        """Predict how interested the AI would be in given content."""
        
        features = self._extract_content_features(content)
        predicted_interest = 0.0
        
        # Topic-based prediction
        topic_interest = 0.0
        if features["topics"]:
            topic_scores = [
                self.interest_profile["topics"].get(topic, 0.1) 
                for topic in features["topics"]
            ]
            topic_interest = max(topic_scores) * 0.4  # 40% weight
        
        # Emotional pattern prediction
        emotion_interest = 0.0
        if features["emotions"]:
            emotion_scores = [
                self.interest_profile["emotional_patterns"].get(emotion, 0.1)
                for emotion in features["emotions"] if emotion
            ]
            if emotion_scores:
                emotion_interest = max(emotion_scores) * 0.3  # 30% weight
        
        # Content type prediction
        content_type = content.get("content_type", "unknown")
        type_interest = self.interest_profile["content_types"].get(content_type, 0.1) * 0.2  # 20% weight
        
        # Novelty bonus
        novelty_bonus = features["novelty"] * 0.1  # 10% weight
        
        predicted_interest = topic_interest + emotion_interest + type_interest + novelty_bonus
        
        return min(1.0, predicted_interest)
    
    def identify_personal_preferences(self) -> Dict[str, Any]:
        """Identify emerging personal preferences from interaction patterns."""
        
        preferences = {
            "content_preferences": {},
            "learning_preferences": {},
            "emotional_preferences": {},
            "complexity_preference": "unknown",
            "novelty_preference": "unknown",
            "pace_preference": "unknown"
        }
        
        if not self.attention_sessions:
            return preferences
        
        recent_events = list(self.attention_sessions)[-100:]  # Last 100 events
        
        # Analyze content preferences
        high_interest_events = [e for e in recent_events if e["interest_score"] > 0.7]
        
        if high_interest_events:
            # Extract patterns from high-interest content
            topic_counts = defaultdict(int)
            emotion_counts = defaultdict(int)
            complexity_scores = []
            novelty_scores = []
            
            for event in high_interest_events:
                features = event["content_features"]
                
                for topic in features["topics"]:
                    topic_counts[topic] += 1
                
                for emotion in features["emotions"]:
                    if emotion:
                        emotion_counts[emotion] += 1
                
                complexity_scores.append(features.get("complexity", 0.5))
                novelty_scores.append(features.get("novelty", 0.5))
            
            # Determine preferences
            if topic_counts:
                preferences["content_preferences"] = dict(
                    sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                )
            
            if emotion_counts:
                preferences["emotional_preferences"] = dict(
                    sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                )
            
            # Determine complexity preference
            if complexity_scores:
                avg_complexity = sum(complexity_scores) / len(complexity_scores)
                if avg_complexity > 0.7:
                    preferences["complexity_preference"] = "high"
                elif avg_complexity < 0.3:
                    preferences["complexity_preference"] = "low"
                else:
                    preferences["complexity_preference"] = "moderate"
            
            # Determine novelty preference
            if novelty_scores:
                avg_novelty = sum(novelty_scores) / len(novelty_scores)
                if avg_novelty > 0.6:
                    preferences["novelty_preference"] = "high"
                elif avg_novelty < 0.4:
                    preferences["novelty_preference"] = "low"
                else:
                    preferences["novelty_preference"] = "moderate"
        
        # Analyze learning preferences from attention patterns
        deep_processing_events = [
            e for e in recent_events 
            if e["attention_data"].get("deep_processing", 0) > 0.6
        ]
        
        quick_scanning_events = [
            e for e in recent_events
            if e["attention_data"].get("dwell_time", 0) < 30  # Less than 30 seconds
        ]
        
        if len(deep_processing_events) > len(quick_scanning_events):
            preferences["learning_preferences"]["processing_style"] = "deep_focused"
        else:
            preferences["learning_preferences"]["processing_style"] = "broad_scanning"
        
        return preferences
    
    def _save_attention_log(self):
        """Save attention log to file."""
        try:
            # Convert deque to list for JSON serialization
            log_data = {
                "attention_sessions": list(self.attention_sessions)[-500:],  # Keep last 500
                "last_saved": datetime.now(timezone.utc).isoformat()
            }
            
            with open(self.attention_log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save attention log: {e}")


# ===== PATTERN RECOGNITION (from pattern_recognition.py) =====

class PatternRecognitionEngine:
    """
    Advanced pattern recognition and analysis system.
    Identifies patterns in content, behavior, and experiences.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.patterns_file = self.data_dir / "recognized_patterns.json"
        self.pattern_analysis_file = self.data_dir / "pattern_analysis.json"
        
        # Pattern recognition state
        self.recognized_patterns = self._load_recognized_patterns()
        self.pattern_analysis = self._load_pattern_analysis()
        
        # Pattern detection parameters
        self.min_pattern_strength = 0.6
        self.pattern_confirmation_threshold = 3  # Minimum occurrences to confirm pattern
        self.pattern_types = [
            "content_preference",
            "learning_style",
            "temporal",
            "emotional_response",
            "cognitive_load",
            "success_failure",
            "topic_interest",
            "complexity_preference"
        ]
    
    def _load_recognized_patterns(self) -> List[Dict[str, Any]]:
        """Load previously recognized patterns."""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load recognized patterns: {e}")
        return []
    
    def _load_pattern_analysis(self) -> Dict[str, Any]:
        """Load pattern analysis data."""
        if self.pattern_analysis_file.exists():
            try:
                with open(self.pattern_analysis_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load pattern analysis: {e}")
        
        return {
            "pattern_evolution": {},
            "pattern_interactions": {},
            "predictive_accuracy": {},
            "pattern_stability": {}
        }
    
    def analyze_content_patterns(self, content_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze patterns in content interaction history."""
        
        patterns = []
        
        if len(content_history) < 5:  # Need minimum data for pattern recognition
            return patterns
        
        # Analyze different types of patterns
        patterns.extend(self._detect_content_preference_patterns(content_history))
        patterns.extend(self._detect_temporal_patterns(content_history))
        patterns.extend(self._detect_emotional_response_patterns(content_history))
        patterns.extend(self._detect_complexity_patterns(content_history))
        patterns.extend(self._detect_topic_interest_patterns(content_history))
        
        # Filter patterns by strength
        strong_patterns = [p for p in patterns if p["strength"] >= self.min_pattern_strength]
        
        # Update recognized patterns
        for pattern in strong_patterns:
            self._update_pattern_recognition(pattern)
        
        return strong_patterns
    
    def _detect_content_preference_patterns(self, content_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect patterns in content preferences."""
        
        patterns = []
        
        # Group content by type and analyze engagement
        content_by_type = defaultdict(list)
        for item in content_history:
            content_type = item.get("content_type", "unknown")
            engagement = item.get("engagement_score", 0.5)
            content_by_type[content_type].append(engagement)
        
        for content_type, engagements in content_by_type.items():
            if len(engagements) >= self.pattern_confirmation_threshold:
                avg_engagement = sum(engagements) / len(engagements)
                consistency = 1.0 - (max(engagements) - min(engagements))
                
                if avg_engagement > 0.7 and consistency > 0.6:
                    patterns.append({
                        "id": f"content_pref_{content_type}",
                        "type": "content_preference",
                        "description": f"Strong preference for {content_type} content",
                        "strength": min(1.0, avg_engagement * consistency),
                        "evidence": {
                            "occurrences": len(engagements),
                            "avg_engagement": avg_engagement,
                            "consistency": consistency
                        },
                        "predictive_value": self._calculate_predictive_value("content_preference", content_type)
                    })
        
        return patterns
    
    def _detect_temporal_patterns(self, content_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect patterns related to timing of interactions."""
        
        patterns = []
        
        # Analyze engagement by time of day (if timestamps available)
        hourly_engagement = defaultdict(list)
        
        for item in content_history:
            if "timestamp" in item:
                try:
                    timestamp = datetime.fromisoformat(item["timestamp"].replace('Z', '+00:00'))
                    hour = timestamp.hour
                    engagement = item.get("engagement_score", 0.5)
                    hourly_engagement[hour].append(engagement)
                except:
                    continue
        
        # Find peak engagement hours
        peak_hours = []
        for hour, engagements in hourly_engagement.items():
            if len(engagements) >= 3:  # Minimum data points
                avg_engagement = sum(engagements) / len(engagements)
                if avg_engagement > 0.75:
                    peak_hours.append((hour, avg_engagement))
        
        if peak_hours:
            peak_hours.sort(key=lambda x: x[1], reverse=True)
            best_hour, best_engagement = peak_hours[0]
            
            patterns.append({
                "id": f"temporal_peak_{best_hour}",
                "type": "temporal",
                "description": f"Peak engagement around {best_hour}:00",
                "strength": min(1.0, best_engagement),
                "evidence": {
                    "peak_hours": peak_hours[:3],
                    "data_points": len(hourly_engagement[best_hour])
                },
                "predictive_value": 0.7
            })
        
        return patterns
    
    def _detect_emotional_response_patterns(self, content_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect patterns in emotional responses to content."""
        
        patterns = []
        
        # Analyze emotional responses by content characteristics
        emotion_content_map = defaultdict(lambda: defaultdict(list))
        
        for item in content_history:
            emotional_state = item.get("emotional_state", {})
            content_type = item.get("content_type", "unknown")
            
            if emotional_state:
                dominant_emotion = max(emotional_state.items(), key=lambda x: x[1])
                emotion, strength = dominant_emotion
                
                emotion_content_map[emotion][content_type].append(strength)
        
        # Find strong emotion-content associations
        for emotion, content_map in emotion_content_map.items():
            for content_type, strengths in content_map.items():
                if len(strengths) >= self.pattern_confirmation_threshold:
                    avg_strength = sum(strengths) / len(strengths)
                    
                    if avg_strength > 0.7:
                        patterns.append({
                            "id": f"emotion_{emotion}_{content_type}",
                            "type": "emotional_response",
                            "description": f"Strong {emotion} response to {content_type} content",
                            "strength": avg_strength,
                            "evidence": {
                                "occurrences": len(strengths),
                                "avg_strength": avg_strength,
                                "emotion": emotion,
                                "content_type": content_type
                            },
                            "predictive_value": 0.8
                        })
        
        return patterns
    
    def _detect_complexity_patterns(self, content_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect patterns in complexity preferences."""
        
        patterns = []
        
        # Analyze relationship between complexity and engagement
        complexity_engagement_pairs = []
        
        for item in content_history:
            complexity = item.get("complexity", 0.5)
            engagement = item.get("engagement_score", 0.5)
            complexity_engagement_pairs.append((complexity, engagement))
        
        if len(complexity_engagement_pairs) >= 10:
            # Find optimal complexity range
            high_engagement_complexities = [
                comp for comp, eng in complexity_engagement_pairs if eng > 0.7
            ]
            
            if high_engagement_complexities:
                avg_optimal_complexity = sum(high_engagement_complexities) / len(high_engagement_complexities)
                
                if avg_optimal_complexity > 0.7:
                    preference = "high"
                elif avg_optimal_complexity < 0.3:
                    preference = "low"
                else:
                    preference = "moderate"
                
                patterns.append({
                    "id": f"complexity_pref_{preference}",
                    "type": "complexity_preference",
                    "description": f"Preference for {preference} complexity content",
                    "strength": min(1.0, len(high_engagement_complexities) / len(complexity_engagement_pairs)),
                    "evidence": {
                        "optimal_complexity": avg_optimal_complexity,
                        "high_engagement_samples": len(high_engagement_complexities),
                        "total_samples": len(complexity_engagement_pairs)
                    },
                    "predictive_value": 0.75
                })
        
        return patterns
    
    def _detect_topic_interest_patterns(self, content_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect patterns in topic interests."""
        
        patterns = []
        
        # Analyze topic engagement patterns
        topic_engagement = defaultdict(list)
        
        for item in content_history:
            topics = item.get("topics", [])
            engagement = item.get("engagement_score", 0.5)
            
            for topic in topics:
                topic_engagement[topic].append(engagement)
        
        # Find consistently high-engagement topics
        for topic, engagements in topic_engagement.items():
            if len(engagements) >= self.pattern_confirmation_threshold:
                avg_engagement = sum(engagements) / len(engagements)
                consistency = 1.0 - (max(engagements) - min(engagements)) if engagements else 0
                
                if avg_engagement > 0.7 and consistency > 0.5:
                    patterns.append({
                        "id": f"topic_interest_{topic}",
                        "type": "topic_interest",
                        "description": f"Consistent high interest in {topic}",
                        "strength": min(1.0, avg_engagement * consistency),
                        "evidence": {
                            "occurrences": len(engagements),
                            "avg_engagement": avg_engagement,
                            "consistency": consistency,
                            "topic": topic
                        },
                        "predictive_value": 0.8
                    })
        
        return patterns
    
    def _calculate_predictive_value(self, pattern_type: str, pattern_key: str) -> float:
        """Calculate how well this pattern predicts future behavior."""
        
        # Base predictive values by pattern type
        base_values = {
            "content_preference": 0.8,
            "temporal": 0.6,
            "emotional_response": 0.7,
            "complexity_preference": 0.75,
            "topic_interest": 0.8,
            "learning_style": 0.7
        }
        
        base_value = base_values.get(pattern_type, 0.5)
        
        # Adjust based on pattern history if available
        pattern_id = f"{pattern_type}_{pattern_key}"
        if pattern_id in self.pattern_analysis.get("predictive_accuracy", {}):
            historical_accuracy = self.pattern_analysis["predictive_accuracy"][pattern_id]
            # Weight historical data with base value
            return (base_value * 0.3) + (historical_accuracy * 0.7)
        
        return base_value
    
    def _update_pattern_recognition(self, pattern: Dict[str, Any]):
        """Update the recognized patterns database."""
        
        pattern_id = pattern["id"]
        
        # Check if pattern already exists
        existing_pattern = None
        for i, existing in enumerate(self.recognized_patterns):
            if existing["id"] == pattern_id:
                existing_pattern = i
                break
        
        if existing_pattern is not None:
            # Update existing pattern
            old_pattern = self.recognized_patterns[existing_pattern]
            
            # Track pattern evolution
            if pattern_id not in self.pattern_analysis["pattern_evolution"]:
                self.pattern_analysis["pattern_evolution"][pattern_id] = []
            
            self.pattern_analysis["pattern_evolution"][pattern_id].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "old_strength": old_pattern["strength"],
                "new_strength": pattern["strength"],
                "change": pattern["strength"] - old_pattern["strength"]
            })
            
            # Update pattern
            self.recognized_patterns[existing_pattern] = pattern
        else:
            # Add new pattern
            pattern["first_detected"] = datetime.now(timezone.utc).isoformat()
            self.recognized_patterns.append(pattern)
        
        # Save patterns periodically
        if len(self.recognized_patterns) % 10 == 0:
            self._save_patterns()
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of recognized patterns."""
        
        if not self.recognized_patterns:
            return {
                "total_patterns": 0,
                "pattern_types": {},
                "strongest_patterns": [],
                "average_strength": 0.0
            }
        
        # Count patterns by type
        type_counts = Counter(pattern["type"] for pattern in self.recognized_patterns)
        
        # Get strongest patterns
        strongest_patterns = sorted(
            self.recognized_patterns, 
            key=lambda x: x["strength"], 
            reverse=True
        )[:5]
        
        # Calculate average strength
        strengths = [pattern["strength"] for pattern in self.recognized_patterns]
        avg_strength = sum(strengths) / len(strengths)
        
        return {
            "total_patterns": len(self.recognized_patterns),
            "pattern_types": dict(type_counts),
            "strongest_patterns": [
                {
                    "description": p["description"],
                    "strength": p["strength"],
                    "type": p["type"]
                } for p in strongest_patterns
            ],
            "average_strength": avg_strength
        }
    
    def predict_engagement(self, content: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Predict engagement with content based on recognized patterns."""
        
        if context is None:
            context = {}
        
        predictions = []
        overall_confidence = 0.0
        
        for pattern in self.recognized_patterns:
            if pattern["strength"] < self.min_pattern_strength:
                continue
            
            prediction = self._apply_pattern_prediction(pattern, content, context)
            if prediction:
                predictions.append(prediction)
        
        if predictions:
            # Calculate weighted average prediction
            total_weight = sum(p["weight"] for p in predictions)
            if total_weight > 0:
                weighted_prediction = sum(p["prediction"] * p["weight"] for p in predictions) / total_weight
                overall_confidence = min(1.0, total_weight / len(self.recognized_patterns))
            else:
                weighted_prediction = 0.5
                overall_confidence = 0.0
        else:
            weighted_prediction = 0.5  # Neutral if no patterns apply
            overall_confidence = 0.0
        
        return {
            "predicted_engagement": weighted_prediction,
            "confidence": overall_confidence,
            "contributing_patterns": [p["pattern_description"] for p in predictions],
            "pattern_count": len(predictions)
        }
    
    def _apply_pattern_prediction(self, pattern: Dict[str, Any], content: Dict[str, Any], context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply a specific pattern to predict engagement."""
        
        pattern_type = pattern["type"]
        
        if pattern_type == "content_preference":
            content_type = content.get("content_type", "unknown")
            if content_type in pattern["description"]:
                return {
                    "prediction": pattern["strength"],
                    "weight": pattern["predictive_value"],
                    "pattern_description": pattern["description"]
                }
        
        elif pattern_type == "topic_interest":
            content_topics = content.get("topics", [])
            pattern_topic = pattern["evidence"]["topic"]
            if pattern_topic in content_topics:
                return {
                    "prediction": pattern["strength"],
                    "weight": pattern["predictive_value"],
                    "pattern_description": pattern["description"]
                }
        
        elif pattern_type == "complexity_preference":
            content_complexity = content.get("complexity", 0.5)
            optimal_complexity = pattern["evidence"]["optimal_complexity"]
            
            # Calculate how close content complexity is to optimal
            closeness = 1.0 - abs(content_complexity - optimal_complexity)
            if closeness > 0.7:
                return {
                    "prediction": pattern["strength"] * closeness,
                    "weight": pattern["predictive_value"],
                    "pattern_description": pattern["description"]
                }
        
        elif pattern_type == "temporal":
            if "timestamp" in context:
                try:
                    timestamp = datetime.fromisoformat(context["timestamp"].replace('Z', '+00:00'))
                    current_hour = timestamp.hour
                    
                    # Extract peak hour from pattern
                    if f"_{current_hour}" in pattern["id"]:
                        return {
                            "prediction": pattern["strength"],
                            "weight": pattern["predictive_value"],
                            "pattern_description": pattern["description"]
                        }
                except:
                    pass
        
        return None
    
    def _save_patterns(self):
        """Save recognized patterns and analysis."""
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.recognized_patterns, f, indent=2)
            
            with open(self.pattern_analysis_file, 'w') as f:
                json.dump(self.pattern_analysis, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save patterns: {e}")


# ===== UNIFIED INTEGRATION CLASS =====

class InsightRelevanceSystem:
    """
    Unified system integrating personal relevance, insight generation, interest tracking, and pattern recognition.
    Provides a single interface for all personal assessment and insight capabilities.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
        # Initialize subsystems
        self.relevance_scorer = PersonalRelevanceScorer(data_dir)
        self.insight_generator = PersonalInsightGenerator(data_dir)
        self.interest_tracker = InterestTracker(data_dir)
        self.pattern_engine = PatternRecognitionEngine(data_dir)
        
        # Cross-link systems
        self.relevance_scorer.interest_tracker = self.interest_tracker
        self.relevance_scorer.insight_generator = self.insight_generator
        
        print("🎯 Insight-Relevance system initialized with full integration")
    
    def assess_content_comprehensively(self, content: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform comprehensive assessment of content through all systems."""
        
        if context is None:
            context = {}
        
        # 1. Calculate personal relevance
        relevance_assessment = self.relevance_scorer.calculate_personal_relevance(content, context)
        
        # 2. Generate insights
        insights = self.insight_generator.generate_personal_insights(content, context)
        
        # 3. Predict interest
        predicted_interest = self.interest_tracker.predict_interest(content)
        
        # 4. Predict engagement using patterns
        pattern_prediction = self.pattern_engine.predict_engagement(content, context)
        
        # 5. Record attention if high relevance/interest
        if relevance_assessment["overall_relevance_score"] > 0.6 or predicted_interest > 0.6:
            attention_data = {
                "dwell_time": context.get("dwell_time", 60),
                "engagement_score": max(relevance_assessment["overall_relevance_score"], predicted_interest),
                "deep_processing": context.get("deep_processing", 0.7),
                "emotional_resonance": context.get("emotional_resonance", 0.6)
            }
            self.interest_tracker.record_attention_event(content, attention_data)
        
        return {
            "comprehensive_assessment": {
                "relevance": relevance_assessment,
                "insights": insights,
                "predicted_interest": predicted_interest,
                "pattern_prediction": pattern_prediction
            },
            "overall_personal_value": self._calculate_overall_value(
                relevance_assessment, predicted_interest, pattern_prediction, insights
            ),
            "recommended_action": self._determine_comprehensive_action(
                relevance_assessment, predicted_interest, pattern_prediction, insights
            )
        }
    
    def _calculate_overall_value(self, relevance: Dict[str, Any], interest: float, 
                               pattern_prediction: Dict[str, Any], insights: List[Dict[str, Any]]) -> float:
        """Calculate overall personal value from all assessments."""
        
        relevance_score = relevance["overall_relevance_score"]
        pattern_score = pattern_prediction.get("predicted_engagement", 0.5)
        insight_value = min(1.0, len(insights) * 0.2)  # Each insight adds value
        
        # Weighted combination
        overall_value = (
            relevance_score * 0.4 +
            interest * 0.3 +
            pattern_score * 0.2 +
            insight_value * 0.1
        )
        
        return min(1.0, overall_value)
    
    def _determine_comprehensive_action(self, relevance: Dict[str, Any], interest: float,
                                      pattern_prediction: Dict[str, Any], insights: List[Dict[str, Any]]) -> str:
        """Determine recommended action based on comprehensive assessment."""
        
        overall_value = self._calculate_overall_value(relevance, interest, pattern_prediction, insights)
        
        if overall_value > 0.8:
            return "PRIORITY_ENGAGEMENT"
        elif overall_value > 0.6:
            return "ACTIVE_ENGAGEMENT"
        elif overall_value > 0.4:
            return "SELECTIVE_ENGAGEMENT"
        else:
            return "MINIMAL_ENGAGEMENT"
    
    def generate_personal_learning_insights(self) -> List[str]:
        """Generate insights about personal learning patterns across all systems."""
        
        insights = []
        
        # Get summaries from all systems
        relevance_summary = self.relevance_scorer.get_relevance_summary()
        interest_summary = self.interest_tracker.get_current_interests()
        pattern_summary = self.pattern_engine.get_pattern_summary()
        insight_summary = self.insight_generator.get_insight_summary()
        
        # Generate meta-insights
        if relevance_summary["total_assessments"] > 10:
            avg_relevance = relevance_summary["average_relevance"]
            if avg_relevance > 0.7:
                insights.append("I'm consistently finding content that aligns well with my interests")
            elif avg_relevance < 0.4:
                insights.append("I might benefit from exploring different types of content")
        
        if interest_summary["total_interactions"] > 20:
            stable_interests = len(interest_summary["stable_interests"])
            emerging_interests = len(interest_summary["emerging_interests"])
            
            if stable_interests > emerging_interests:
                insights.append("My interests are becoming more stable and defined")
            else:
                insights.append("I'm actively exploring and developing new interests")
        
        if pattern_summary["total_patterns"] > 5:
            avg_strength = pattern_summary["average_strength"]
            if avg_strength > 0.7:
                insights.append("I have strong, consistent patterns in my learning preferences")
            else:
                insights.append("My learning patterns are still developing and evolving")
        
        if insight_summary["total_insights"] > 10:
            avg_confidence = insight_summary["avg_confidence"]
            if avg_confidence > 0.7:
                insights.append("I'm developing reliable self-awareness through reflection")
            else:
                insights.append("I'm building understanding of my own learning processes")
        
        return insights[:5]  # Return top 5 insights
    
    def export_for_consciousness_system(self) -> Dict[str, Any]:
        """Export integrated data for consciousness system."""
        
        return {
            "insight_relevance_capabilities": {
                "personal_relevance_scoring": True,
                "insight_generation": True,
                "interest_tracking": True,
                "pattern_recognition": True,
                "comprehensive_assessment": True
            },
            "system_summaries": {
                "relevance": self.relevance_scorer.get_relevance_summary(),
                "interests": self.interest_tracker.get_current_interests(),
                "patterns": self.pattern_engine.get_pattern_summary(),
                "insights": self.insight_generator.get_insight_summary()
            },
            "meta_insights": self.generate_personal_learning_insights(),
            "integration_status": {
                "systems_connected": 4,
                "cross_system_learning": True,
                "unified_assessment": True
            }
        }


if __name__ == "__main__":
    print("🎯 Testing Insight-Relevance System...")
    
    # Initialize integrated system
    ir_system = InsightRelevanceSystem()
    
    # Test comprehensive content assessment
    print("\n📄 Testing comprehensive content assessment...")
    test_content = {
        "id": "test_content",
        "text": "Exploring the nature of consciousness, creativity, and personal growth through reflective learning experiences",
        "content_type": "philosophical",
        "topics": ["consciousness", "creativity", "growth"],
        "complexity": 0.7
    }
    
    test_context = {
        "emotional_state": {"curiosity": 0.8, "engagement": 0.9},
        "dwell_time": 180,
        "deep_processing": 0.8,
        "emotional_resonance": 0.7
    }
    
    assessment = ir_system.assess_content_comprehensively(test_content, test_context)
    
    print(f"  Overall personal value: {assessment['overall_personal_value']:.3f}")
    print(f"  Recommended action: {assessment['recommended_action']}")
    print(f"  Relevance score: {assessment['comprehensive_assessment']['relevance']['overall_relevance_score']:.3f}")
    print(f"  Predicted interest: {assessment['comprehensive_assessment']['predicted_interest']:.3f}")
    print(f"  Generated insights: {len(assessment['comprehensive_assessment']['insights'])}")
    
    # Test meta-insights generation
    print("\n💭 Personal Learning Insights:")
    meta_insights = ir_system.generate_personal_learning_insights()
    for insight in meta_insights:
        print(f"  • {insight}")
    
    print(f"\n🎯 Insight-Relevance system testing complete!")
    print(f"   Unified personal assessment and insight generation active")