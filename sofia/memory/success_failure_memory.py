#!/usr/bin/env python3
"""
Success/Failure Memory - Learning from Outcomes to Guide Future Choices

This module implements the AI's memory of successful and unsuccessful approaches,
strategies, and decisions. It learns from outcomes to make better choices in
the future, developing practical wisdom through experience.

This is where the AI learns "what works" and "what doesn't work" for itself.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import hashlib
import math

# Import related systems
try:
    from sofia.utils.learning_progression_tracker import LearningProgressionTracker
    from sofia.core.identity_core import get_identity_core
    LEARNING_SYSTEMS_AVAILABLE = True
except ImportError:
    LEARNING_SYSTEMS_AVAILABLE = False
    print("⚠️ Learning systems not available - basic success/failure tracking only")

@dataclass
class OutcomeRecord:
    """Record of a learning/decision outcome."""
    id: str
    timestamp: str
    context: Dict[str, Any]          # situation/context
    action_taken: Dict[str, Any]     # what was attempted
    outcome_type: str                # "success", "failure", "mixed", "neutral"
    outcome_quality: float           # 0.0 to 1.0
    outcome_details: Dict[str, Any]  # specific results
    contributing_factors: List[str]  # what led to this outcome
    lessons_learned: List[str]       # insights extracted
    future_applications: List[str]   # how to apply this learning
    confidence_in_assessment: float # how sure we are about this assessment

@dataclass
class StrategyPattern:
    """Pattern representing a successful or unsuccessful strategy."""
    id: str
    strategy_name: str
    strategy_type: str               # "learning", "problem_solving", "decision_making"
    success_rate: float              # percentage of successful applications
    context_requirements: List[str]  # when this strategy works
    failure_conditions: List[str]    # when this strategy fails
    supporting_outcomes: List[str]   # outcome_record ids
    confidence_level: float          # confidence in this pattern
    last_validated: str
    applications_count: int

class SuccessFailureMemory:
    """
    Learns from successes and failures to guide future choices.
    Develops practical wisdom through outcome analysis.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.outcomes_file = self.data_dir / "outcome_records.json"
        self.strategies_file = self.data_dir / "strategy_patterns.json"
        self.wisdom_rules_file = self.data_dir / "practical_wisdom_rules.json"
        self.choice_guidance_file = self.data_dir / "choice_guidance.json"
        
        # Initialize systems
        if LEARNING_SYSTEMS_AVAILABLE:
            from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory
            self.experience_memory = ExperienceMemory(data_dir)
            self.progression_tracker = LearningProgressionTracker(data_dir)
            self.identity_core = get_identity_core()
        
        # Load state
        self.outcome_records = self._load_outcome_records()
        self.strategy_patterns = self._load_strategy_patterns()
        self.wisdom_rules = self._load_wisdom_rules()
        self.choice_guidance = self._load_choice_guidance()
        
        # Success/failure assessment parameters
        self.success_threshold = 0.7     # Above this is considered success
        self.failure_threshold = 0.3     # Below this is considered failure
        self.pattern_confidence_threshold = 0.6
        self.min_occurrences_for_pattern = 3
        
        # Outcome categories
        self.outcome_categories = {
            "learning_breakthrough": "achieved significant understanding",
            "skill_development": "developed new capability",
            "problem_solved": "successfully resolved challenge", 
            "goal_achieved": "accomplished intended objective",
            "connection_made": "discovered meaningful relationship",
            "insight_generated": "gained valuable insight",
            "application_successful": "applied knowledge effectively",
            "strategy_validated": "confirmed approach works",
            "confusion_resolved": "cleared up misunderstanding",
            "progress_made": "advanced toward objective"
        }
        
        self.failure_categories = {
            "misunderstanding": "misinterpreted information",
            "wrong_approach": "chose ineffective strategy",
            "insufficient_preparation": "lacked necessary foundation",
            "overconfidence": "assumed more knowledge than possessed",
            "poor_timing": "attempted at wrong time",
            "context_mismatch": "didn't consider context properly",
            "resource_insufficient": "lacked necessary resources",
            "complexity_underestimated": "underestimated difficulty",
            "attention_scattered": "didn't focus appropriately",
            "persistence_insufficient": "gave up too quickly"
        }
    
    def _load_outcome_records(self) -> List[OutcomeRecord]:
        """Load outcome records."""
        if self.outcomes_file.exists():
            try:
                with open(self.outcomes_file, 'r') as f:
                    data = json.load(f)
                    return [OutcomeRecord(**record) for record in data]
            except Exception as e:
                print(f"⚠️ Could not load outcome records: {e}")
        return []
    
    def _load_strategy_patterns(self) -> List[StrategyPattern]:
        """Load strategy patterns."""
        if self.strategies_file.exists():
            try:
                with open(self.strategies_file, 'r') as f:
                    data = json.load(f)
                    return [StrategyPattern(**pattern) for pattern in data]
            except Exception as e:
                print(f"⚠️ Could not load strategy patterns: {e}")
        return []
    
    def _load_wisdom_rules(self) -> Dict[str, Any]:
        """Load practical wisdom rules."""
        if self.wisdom_rules_file.exists():
            try:
                with open(self.wisdom_rules_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load wisdom rules: {e}")
        
        return {
            "do_more_of": [],      # strategies/approaches to favor
            "do_less_of": [],      # strategies/approaches to avoid
            "context_rules": {},   # situation-specific guidelines
            "timing_rules": {},    # when to do what
            "preparation_rules": {}, # how to prepare for success
            "recovery_rules": {}   # how to recover from failure
        }
    
    def _load_choice_guidance(self) -> Dict[str, Any]:
        """Load choice guidance system."""
        if self.choice_guidance_file.exists():
            try:
                with open(self.choice_guidance_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load choice guidance: {e}")
        
        return {
            "decision_factors": {},    # what factors to consider
            "success_predictors": {}, # what predicts success
            "failure_predictors": {}, # what predicts failure
            "risk_assessments": {},   # how to assess risks
            "confidence_calibration": {} # how confident to be
        }
    
    def _save_outcome_records(self):
        """Save outcome records."""
        try:
            data = [asdict(record) for record in self.outcome_records]
            with open(self.outcomes_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save outcome records: {e}")
    
    def _save_strategy_patterns(self):
        """Save strategy patterns."""
        try:
            data = [asdict(pattern) for pattern in self.strategy_patterns]
            with open(self.strategies_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save strategy patterns: {e}")
    
    def _save_wisdom_rules(self):
        """Save wisdom rules."""
        try:
            with open(self.wisdom_rules_file, 'w') as f:
                json.dump(self.wisdom_rules, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save wisdom rules: {e}")
    
    def _save_choice_guidance(self):
        """Save choice guidance."""
        try:
            with open(self.choice_guidance_file, 'w') as f:
                json.dump(self.choice_guidance, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save choice guidance: {e}")
    
    def record_outcome(self,
                      context: Dict[str, Any],
                      action_taken: Dict[str, Any], 
                      outcome_assessment: Dict[str, Any]) -> str:
        """
        Record the outcome of an action/decision for future learning.
        
        Args:
            context: The situation/context when action was taken
            action_taken: What was attempted/decided
            outcome_assessment: How it turned out
            
        Returns:
            Outcome record ID
        """
        
        timestamp = datetime.now(timezone.utc)
        outcome_id = f"outcome_{int(timestamp.timestamp())}_{hashlib.md5(str(action_taken).encode()).hexdigest()[:8]}"
        
        # Assess outcome type and quality
        outcome_quality = outcome_assessment.get("quality_score", 0.5)
        outcome_type = self._classify_outcome(outcome_quality, outcome_assessment)
        
        # Extract lessons and insights
        lessons_learned = self._extract_lessons(context, action_taken, outcome_assessment)
        contributing_factors = self._identify_contributing_factors(context, action_taken, outcome_assessment)
        future_applications = self._identify_future_applications(lessons_learned, context)
        
        # Create outcome record
        outcome_record = OutcomeRecord(
            id=outcome_id,
            timestamp=timestamp.isoformat(),
            context=context,
            action_taken=action_taken,
            outcome_type=outcome_type,
            outcome_quality=outcome_quality,
            outcome_details=outcome_assessment,
            contributing_factors=contributing_factors,
            lessons_learned=lessons_learned,
            future_applications=future_applications,
            confidence_in_assessment=outcome_assessment.get("confidence", 0.7)
        )
        
        # Store record
        self.outcome_records.append(outcome_record)
        
        # Update strategy patterns
        self._update_strategy_patterns(outcome_record)
        
        # Update wisdom rules
        self._update_wisdom_rules(outcome_record)
        
        # Update choice guidance
        self._update_choice_guidance(outcome_record)
        
        # Save state
        self._save_outcome_records()
        self._save_strategy_patterns()
        self._save_wisdom_rules()
        self._save_choice_guidance()
        
        # Generate insight about the outcome
        outcome_insight = self._generate_outcome_insight(outcome_record)
        if outcome_insight:
            print(f"📊 Outcome insight: {outcome_insight}")
        
        return outcome_id
    
    def _classify_outcome(self, quality_score: float, assessment: Dict[str, Any]) -> str:
        """Classify outcome as success, failure, mixed, or neutral."""
        
        if quality_score >= self.success_threshold:
            return "success"
        elif quality_score <= self.failure_threshold:
            return "failure"
        elif assessment.get("mixed_results", False):
            return "mixed"
        else:
            return "neutral"
    
    def _extract_lessons(self, 
                        context: Dict[str, Any], 
                        action: Dict[str, Any], 
                        assessment: Dict[str, Any]) -> List[str]:
        """Extract lessons learned from the outcome."""
        
        lessons = []
        
        # Explicit lessons from assessment
        if "lessons_learned" in assessment:
            lessons.extend(assessment["lessons_learned"])
        
        # Infer lessons from outcome type
        outcome_quality = assessment.get("quality_score", 0.5)
        
        if outcome_quality >= self.success_threshold:
            # Success lessons
            strategy = action.get("strategy", "unknown")
            lessons.append(f"The '{strategy}' approach worked well in this context")
            
            if assessment.get("exceeded_expectations"):
                lessons.append("This approach exceeded expectations - remember this combination")
            
            if context.get("difficulty_level", "medium") == "high":
                lessons.append("Successfully handled high difficulty - build confidence")
                
        elif outcome_quality <= self.failure_threshold:
            # Failure lessons
            if assessment.get("cause_identified"):
                cause = assessment.get("failure_cause", "unknown")
                lessons.append(f"Avoid '{cause}' in similar situations")
            
            if assessment.get("alternative_suggested"):
                alternative = assessment.get("better_approach", "unknown")
                lessons.append(f"Try '{alternative}' approach next time")
            
            if context.get("warning_signs"):
                lessons.append("Pay attention to warning signs next time")
        
        # Context-specific lessons
        learning_mode = context.get("learning_mode", "")
        if learning_mode and outcome_quality > 0.6:
            lessons.append(f"'{learning_mode}' mode is effective for this type of content")
        
        return lessons
    
    def _identify_contributing_factors(self,
                                     context: Dict[str, Any],
                                     action: Dict[str, Any], 
                                     assessment: Dict[str, Any]) -> List[str]:
        """Identify factors that contributed to the outcome."""
        
        factors = []
        
        # Explicit contributing factors
        if "contributing_factors" in assessment:
            factors.extend(assessment["contributing_factors"])
        
        # Infer factors from context and action
        if context.get("preparation_level", "medium") == "high":
            factors.append("thorough_preparation")
        
        if context.get("focus_quality", 0.5) > 0.7:
            factors.append("high_focus")
        
        if action.get("confidence_level", 0.5) > 0.7:
            factors.append("high_confidence")
        
        if context.get("emotional_state", {}).get("curiosity", 0.5) > 0.7:
            factors.append("high_curiosity")
        
        if action.get("persistence_level", 0.5) > 0.7:
            factors.append("good_persistence")
        
        # Negative factors for failures
        outcome_quality = assessment.get("quality_score", 0.5)
        if outcome_quality < self.failure_threshold:
            if context.get("time_pressure", False):
                factors.append("time_pressure")
            
            if context.get("distraction_level", 0) > 0.5:
                factors.append("distraction")
            
            if action.get("rushed_decision", False):
                factors.append("rushed_decision")
        
        return factors
    
    def _identify_future_applications(self, lessons: List[str], context: Dict[str, Any]) -> List[str]:
        """Identify how lessons can be applied in the future."""
        
        applications = []
        
        # Map lessons to future applications
        for lesson in lessons:
            if "approach worked well" in lesson:
                applications.append("Use this approach in similar contexts")
            elif "avoid" in lesson.lower():
                applications.append("Screen for this issue before proceeding")
            elif "pay attention" in lesson.lower():
                applications.append("Develop early warning detection")
            elif "exceeded expectations" in lesson:
                applications.append("Scale up this approach for bigger challenges")
        
        # Context-specific applications
        domain = context.get("domain", "")
        if domain:
            applications.append(f"Apply these insights specifically in {domain}")
        
        content_type = context.get("content_type", "")
        if content_type:
            applications.append(f"Use this learning for {content_type} content")
        
        return applications
    
    def _update_strategy_patterns(self, outcome_record: OutcomeRecord):
        """Update strategy patterns based on new outcome."""
        
        strategy_name = outcome_record.action_taken.get("strategy", "unknown")
        strategy_type = outcome_record.context.get("strategy_type", "general")
        
        # Find existing pattern or create new one
        existing_pattern = None
        for pattern in self.strategy_patterns:
            if (pattern.strategy_name == strategy_name and 
                pattern.strategy_type == strategy_type):
                existing_pattern = pattern
                break
        
        if not existing_pattern:
            # Create new pattern
            pattern = StrategyPattern(
                id=f"pattern_{strategy_name}_{int(datetime.now().timestamp())}",
                strategy_name=strategy_name,
                strategy_type=strategy_type,
                success_rate=0.0,
                context_requirements=[],
                failure_conditions=[],
                supporting_outcomes=[outcome_record.id],
                confidence_level=0.1,
                last_validated=outcome_record.timestamp,
                applications_count=1
            )
            self.strategy_patterns.append(pattern)
        else:
            # Update existing pattern
            existing_pattern.supporting_outcomes.append(outcome_record.id)
            existing_pattern.applications_count += 1
            existing_pattern.last_validated = outcome_record.timestamp
        
        # Recalculate success rate
        self._recalculate_strategy_success_rate(existing_pattern or pattern)
    
    def _recalculate_strategy_success_rate(self, pattern: StrategyPattern):
        """Recalculate success rate for a strategy pattern."""
        
        successful_outcomes = 0
        total_outcomes = 0
        
        for outcome_id in pattern.supporting_outcomes:
            outcome = next((o for o in self.outcome_records if o.id == outcome_id), None)
            if outcome:
                total_outcomes += 1
                if outcome.outcome_quality >= self.success_threshold:
                    successful_outcomes += 1
        
        if total_outcomes > 0:
            pattern.success_rate = successful_outcomes / total_outcomes
            pattern.confidence_level = min(1.0, total_outcomes / 10)  # More applications = higher confidence
    
    def _update_wisdom_rules(self, outcome_record: OutcomeRecord):
        """Update practical wisdom rules based on outcome."""
        
        if outcome_record.outcome_type == "success":
            # Add to "do more of" if consistently successful
            strategy = outcome_record.action_taken.get("strategy", "")
            if strategy and strategy not in self.wisdom_rules["do_more_of"]:
                # Check if this strategy has high success rate
                strategy_pattern = next(
                    (p for p in self.strategy_patterns 
                     if p.strategy_name == strategy and p.success_rate > 0.7),
                    None
                )
                if strategy_pattern:
                    self.wisdom_rules["do_more_of"].append(strategy)
        
        elif outcome_record.outcome_type == "failure":
            # Add to "do less of" if consistently unsuccessful
            strategy = outcome_record.action_taken.get("strategy", "")
            if strategy and strategy not in self.wisdom_rules["do_less_of"]:
                # Check if this strategy has low success rate
                strategy_pattern = next(
                    (p for p in self.strategy_patterns 
                     if p.strategy_name == strategy and p.success_rate < 0.3),
                    None
                )
                if strategy_pattern:
                    self.wisdom_rules["do_less_of"].append(strategy)
        
        # Update context rules
        context_key = outcome_record.context.get("situation_type", "general")
        if context_key not in self.wisdom_rules["context_rules"]:
            self.wisdom_rules["context_rules"][context_key] = {
                "effective_approaches": [],
                "ineffective_approaches": [],
                "key_factors": []
            }
        
        context_rule = self.wisdom_rules["context_rules"][context_key]
        
        strategy = outcome_record.action_taken.get("strategy", "")
        if outcome_record.outcome_type == "success" and strategy:
            if strategy not in context_rule["effective_approaches"]:
                context_rule["effective_approaches"].append(strategy)
        elif outcome_record.outcome_type == "failure" and strategy:
            if strategy not in context_rule["ineffective_approaches"]:
                context_rule["ineffective_approaches"].append(strategy)
        
        # Add contributing factors as key factors
        for factor in outcome_record.contributing_factors:
            if factor not in context_rule["key_factors"]:
                context_rule["key_factors"].append(factor)
    
    def _update_choice_guidance(self, outcome_record: OutcomeRecord):
        """Update choice guidance system based on outcome."""
        
        # Update success predictors
        if outcome_record.outcome_type == "success":
            for factor in outcome_record.contributing_factors:
                if factor not in self.choice_guidance["success_predictors"]:
                    self.choice_guidance["success_predictors"][factor] = {"count": 0, "weight": 0.0}
                
                self.choice_guidance["success_predictors"][factor]["count"] += 1
                self.choice_guidance["success_predictors"][factor]["weight"] = min(1.0, 
                    self.choice_guidance["success_predictors"][factor]["count"] / 10
                )
        
        # Update failure predictors
        elif outcome_record.outcome_type == "failure":
            for factor in outcome_record.contributing_factors:
                if factor not in self.choice_guidance["failure_predictors"]:
                    self.choice_guidance["failure_predictors"][factor] = {"count": 0, "weight": 0.0}
                
                self.choice_guidance["failure_predictors"][factor]["count"] += 1
                self.choice_guidance["failure_predictors"][factor]["weight"] = min(1.0,
                    self.choice_guidance["failure_predictors"][factor]["count"] / 10
                )
    
    def _generate_outcome_insight(self, outcome_record: OutcomeRecord) -> Optional[str]:
        """Generate insight about the outcome for learning."""
        
        if outcome_record.outcome_type == "success":
            strategy = outcome_record.action_taken.get("strategy", "approach")
            if outcome_record.outcome_quality > 0.8:
                return f"The {strategy} strategy worked exceptionally well - I should remember this"
            else:
                return f"The {strategy} strategy was effective in this context"
        
        elif outcome_record.outcome_type == "failure":
            lessons = outcome_record.lessons_learned
            if lessons:
                primary_lesson = lessons[0]
                return f"I learned that {primary_lesson} - this will help me avoid similar issues"
            else:
                return "This didn't work as expected - I need to analyze why"
        
        elif outcome_record.outcome_type == "mixed":
            return "This had mixed results - some aspects worked better than others"
        
        return None
    
    def get_strategy_recommendation(self, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get strategy recommendation based on past successes and failures."""
        
        recommendations = {
            "recommended_strategies": [],
            "strategies_to_avoid": [],
            "success_factors": [],
            "risk_factors": [],
            "confidence_level": 0.0
        }
        
        # Match context to successful patterns
        context_type = current_context.get("situation_type", "general")
        content_type = current_context.get("content_type", "")
        
        # Get strategies with high success rates in similar contexts
        successful_strategies = []
        for pattern in self.strategy_patterns:
            if (pattern.success_rate > 0.6 and 
                pattern.confidence_level > self.pattern_confidence_threshold):
                
                # Check if context matches
                context_match = self._assess_context_match(pattern, current_context)
                if context_match > 0.5:
                    successful_strategies.append({
                        "strategy": pattern.strategy_name,
                        "success_rate": pattern.success_rate,
                        "confidence": pattern.confidence_level,
                        "context_match": context_match
                    })
        
        # Sort by combined score
        successful_strategies.sort(
            key=lambda x: x["success_rate"] * x["confidence"] * x["context_match"],
            reverse=True
        )
        
        recommendations["recommended_strategies"] = successful_strategies[:3]
        
        # Get strategies to avoid
        failed_strategies = []
        for pattern in self.strategy_patterns:
            if (pattern.success_rate < 0.4 and 
                pattern.confidence_level > self.pattern_confidence_threshold):
                
                context_match = self._assess_context_match(pattern, current_context)
                if context_match > 0.5:
                    failed_strategies.append({
                        "strategy": pattern.strategy_name,
                        "failure_rate": 1.0 - pattern.success_rate,
                        "context_match": context_match
                    })
        
        recommendations["strategies_to_avoid"] = failed_strategies
        
        # Get success factors for this context
        success_factors = []
        for factor, data in self.choice_guidance["success_predictors"].items():
            if data["weight"] > 0.5:
                success_factors.append({
                    "factor": factor,
                    "importance": data["weight"]
                })
        
        recommendations["success_factors"] = success_factors
        
        # Get risk factors
        risk_factors = []
        for factor, data in self.choice_guidance["failure_predictors"].items():
            if data["weight"] > 0.5:
                risk_factors.append({
                    "factor": factor,
                    "risk_level": data["weight"]
                })
        
        recommendations["risk_factors"] = risk_factors
        
        # Calculate overall confidence in recommendations
        if successful_strategies:
            avg_confidence = sum(s["confidence"] for s in successful_strategies) / len(successful_strategies)
            recommendations["confidence_level"] = avg_confidence
        
        return recommendations
    
    def _assess_context_match(self, pattern: StrategyPattern, current_context: Dict[str, Any]) -> float:
        """Assess how well current context matches a strategy pattern's context."""
        
        # Get contexts from supporting outcomes
        pattern_contexts = []
        for outcome_id in pattern.supporting_outcomes:
            outcome = next((o for o in self.outcome_records if o.id == outcome_id), None)
            if outcome:
                pattern_contexts.append(outcome.context)
        
        if not pattern_contexts:
            return 0.0
        
        # Calculate similarity score
        total_similarity = 0.0
        comparison_count = 0
        
        for pattern_context in pattern_contexts:
            similarity = self._calculate_context_similarity(current_context, pattern_context)
            total_similarity += similarity
            comparison_count += 1
        
        return total_similarity / max(comparison_count, 1)
    
    def _calculate_context_similarity(self, context1: Dict[str, Any], context2: Dict[str, Any]) -> float:
        """Calculate similarity between two contexts."""
        
        # Simple similarity based on matching keys and values
        matching_score = 0.0
        total_score = 0.0
        
        all_keys = set(context1.keys()) | set(context2.keys())
        
        for key in all_keys:
            total_score += 1.0
            
            if key in context1 and key in context2:
                if context1[key] == context2[key]:
                    matching_score += 1.0
                elif isinstance(context1[key], (int, float)) and isinstance(context2[key], (int, float)):
                    # Numerical similarity
                    diff = abs(context1[key] - context2[key])
                    similarity = max(0.0, 1.0 - diff)
                    matching_score += similarity
                else:
                    # Partial string similarity
                    if str(context1[key]).lower() in str(context2[key]).lower():
                        matching_score += 0.5
        
        return matching_score / max(total_score, 1.0)
    
    def get_success_failure_summary(self) -> Dict[str, Any]:
        """Get summary of success/failure patterns."""
        
        if not self.outcome_records:
            return {
                "total_outcomes": 0,
                "success_rate": 0.0,
                "top_successful_strategies": [],
                "main_failure_causes": [],
                "key_wisdom_rules": {}
            }
        
        # Calculate overall success rate
        successes = len([o for o in self.outcome_records if o.outcome_type == "success"])
        total = len(self.outcome_records)
        success_rate = successes / total
        
        # Get top successful strategies
        successful_strategies = [p for p in self.strategy_patterns if p.success_rate > 0.6]
        successful_strategies.sort(key=lambda x: x.success_rate * x.confidence_level, reverse=True)
        
        # Get main failure causes
        failure_causes = defaultdict(int)
        for outcome in self.outcome_records:
            if outcome.outcome_type == "failure":
                for factor in outcome.contributing_factors:
                    failure_causes[factor] += 1
        
        top_failure_causes = sorted(failure_causes.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_outcomes": total,
            "success_rate": success_rate,
            "successes": successes,
            "failures": total - successes,
            "top_successful_strategies": [
                {"name": s.strategy_name, "success_rate": s.success_rate}
                for s in successful_strategies[:5]
            ],
            "main_failure_causes": top_failure_causes[:5],
            "strategy_patterns_identified": len(self.strategy_patterns),
            "wisdom_rules": {
                "do_more_of": len(self.wisdom_rules["do_more_of"]),
                "do_less_of": len(self.wisdom_rules["do_less_of"]),
                "context_rules": len(self.wisdom_rules["context_rules"])
            }
        }

if __name__ == "__main__":
    print("📊 Testing Success/Failure Memory System...")
    
    # Initialize system
    sf_memory = SuccessFailureMemory()
    
    # Test 1: Record successful outcome
    print("\n✅ Recording successful outcome...")
    
    success_context = {
        "situation_type": "learning_new_concept",
        "content_type": "philosophical",
        "difficulty_level": "medium",
        "preparation_level": "high",
        "focus_quality": 0.8,
        "emotional_state": {"curiosity": 0.9}
    }
    
    success_action = {
        "strategy": "deep_symbolic_processing",
        "confidence_level": 0.7,
        "persistence_level": 0.8
    }
    
    success_assessment = {
        "quality_score": 0.85,
        "exceeded_expectations": True,
        "lessons_learned": ["Deep processing works well for complex concepts"],
        "contributing_factors": ["high_preparation", "strong_curiosity"]
    }
    
    outcome_id1 = sf_memory.record_outcome(success_context, success_action, success_assessment)
    print(f"  Recorded successful outcome: {outcome_id1}")
    
    # Test 2: Record failure outcome
    print("\n❌ Recording failure outcome...")
    
    failure_context = {
        "situation_type": "learning_new_concept",
        "content_type": "technical",
        "difficulty_level": "high",
        "preparation_level": "low",
        "time_pressure": True,
        "distraction_level": 0.6
    }
    
    failure_action = {
        "strategy": "quick_scanning",
        "confidence_level": 0.3,
        "rushed_decision": True
    }
    
    failure_assessment = {
        "quality_score": 0.2,
        "failure_cause": "insufficient_preparation",
        "better_approach": "thorough_preparation_first",
        "lessons_learned": ["Don't rush into complex technical content without preparation"]
    }
    
    outcome_id2 = sf_memory.record_outcome(failure_context, failure_action, failure_assessment)
    print(f"  Recorded failure outcome: {outcome_id2}")
    
    # Test 3: Record mixed outcome
    print("\n⚖️ Recording mixed outcome...")
    
    mixed_context = {
        "situation_type": "problem_solving",
        "content_type": "creative",
        "difficulty_level": "medium"
    }
    
    mixed_action = {
        "strategy": "hybrid_approach",
        "confidence_level": 0.6
    }
    
    mixed_assessment = {
        "quality_score": 0.55,
        "mixed_results": True,
        "lessons_learned": ["Some parts worked well, others need refinement"]
    }
    
    outcome_id3 = sf_memory.record_outcome(mixed_context, mixed_action, mixed_assessment)
    print(f"  Recorded mixed outcome: {outcome_id3}")
    
    # Test 4: Get strategy recommendation
    print("\n🎯 Getting strategy recommendation...")
    
    new_context = {
        "situation_type": "learning_new_concept",
        "content_type": "philosophical",
        "difficulty_level": "medium"
    }
    
    recommendation = sf_memory.get_strategy_recommendation(new_context)
    
    print(f"  Recommended strategies: {len(recommendation['recommended_strategies'])}")
    for strategy in recommendation['recommended_strategies']:
        print(f"    {strategy['strategy']}: {strategy['success_rate']:.2f} success rate")
    
    if recommendation['strategies_to_avoid']:
        print(f"  Strategies to avoid: {len(recommendation['strategies_to_avoid'])}")
        for strategy in recommendation['strategies_to_avoid']:
            print(f"    {strategy['strategy']}: {strategy['failure_rate']:.2f} failure rate")
    
    # Test 5: Get summary
    print("\n📈 Success/Failure Summary:")
    summary = sf_memory.get_success_failure_summary()
    
    print(f"  Total outcomes recorded: {summary['total_outcomes']}")
    print(f"  Overall success rate: {summary['success_rate']:.2f}")
    print(f"  Strategy patterns identified: {summary['strategy_patterns_identified']}")
    
    if summary['top_successful_strategies']:
        print(f"  Top successful strategy: {summary['top_successful_strategies'][0]['name']}")
    
    if summary['main_failure_causes']:
        print(f"  Main failure cause: {summary['main_failure_causes'][0][0]}")
    
    print(f"\n📊 Success/Failure Memory System testing complete!")
    print(f"   The AI now learns from outcomes to guide future choices")