#!/usr/bin/env python3
"""
Predictive Learning Enhancer - Advanced Outcome Prediction

This module enhances the success/failure memory system with sophisticated
predictive learning capabilities:
1. Pattern-based outcome prediction
2. Context similarity analysis
3. Confidence-weighted recommendations
4. Adaptive prediction models
5. Risk assessment for new strategies

This enables Sophia to make better predictions about strategy success.
"""

import json
import math
import statistics
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import hashlib

# Import related systems
try:
    from success_failure_memory import SuccessFailureMemory
    from CONSCIOUSNESS_MEMORY import ExperienceMemory
    from learning_progression_tracker import LearningProgressionTracker
    MEMORY_SYSTEMS_AVAILABLE = True
    
    # Import dataclasses separately to handle import issues
    try:
        from success_failure_memory import StrategyOutcome, StrategyPattern
    except ImportError:
        # Define minimal types if not available
        class StrategyOutcome:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
        
        class StrategyPattern:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
                    
except ImportError:
    MEMORY_SYSTEMS_AVAILABLE = False
    print("⚠️ Memory systems not available - basic predictive learning only")
    
    # Define minimal types for testing
    class StrategyOutcome:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class StrategyPattern:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

class PredictiveLearningEnhancer:
    """
    Enhances success/failure memory with advanced predictive capabilities.
    Uses past outcomes to predict future strategy success with confidence estimates.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.predictions_file = self.data_dir / "predictive_models_enhanced.json"
        self.prediction_accuracy_file = self.data_dir / "prediction_accuracy.json"
        
        # Initialize memory systems
        if MEMORY_SYSTEMS_AVAILABLE:
            self.sf_memory = SuccessFailureMemory(data_dir)
            self.experience_memory = ExperienceMemory(data_dir)
            self.progression_tracker = LearningProgressionTracker(data_dir)
        
        # Load state
        self.predictive_models = self._load_predictive_models()
        self.prediction_accuracy = self._load_prediction_accuracy()
        
        # Prediction parameters
        self.min_samples_for_prediction = 3
        self.context_similarity_threshold = 0.6
        self.confidence_decay_factor = 0.95  # Older predictions lose confidence
        self.prediction_horizon_days = 30    # How far ahead to predict
        
        # Feature weights for prediction
        self.feature_weights = {
            "strategy_history": 0.30,        # Past performance of strategy
            "context_similarity": 0.25,     # How similar current context is
            "recent_trends": 0.20,          # Recent performance trends
            "complexity_match": 0.15,       # Difficulty level alignment
            "preparation_level": 0.10       # Preparation adequacy
        }
    
    def _load_predictive_models(self) -> Dict[str, Any]:
        """Load enhanced predictive models."""
        if self.predictions_file.exists():
            try:
                with open(self.predictions_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load predictive models: {e}")
        
        return {
            "strategy_models": {},           # Per-strategy prediction models
            "context_patterns": {},         # Context-based patterns
            "outcome_correlations": {},     # Factor correlations with outcomes
            "temporal_trends": {},          # Time-based performance trends
            "confidence_calibration": {},   # How accurate our confidence is
            "last_updated": None
        }
    
    def _load_prediction_accuracy(self) -> List[Dict[str, Any]]:
        """Load prediction accuracy tracking."""
        if self.prediction_accuracy_file.exists():
            try:
                with open(self.prediction_accuracy_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load prediction accuracy: {e}")
        return []
    
    def _save_all(self):
        """Save all predictive learning data."""
        try:
            self.predictive_models["last_updated"] = datetime.now(timezone.utc).isoformat()
            with open(self.predictions_file, 'w') as f:
                json.dump(self.predictive_models, f, indent=2)
            
            with open(self.prediction_accuracy_file, 'w') as f:
                json.dump(self.prediction_accuracy, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save predictive learning data: {e}")
    
    def predict_strategy_success(self, 
                                strategy_name: str,
                                context: Dict[str, Any],
                                target_outcome: str = "success") -> Dict[str, Any]:
        """
        Predict the likelihood of strategy success in given context.
        
        Args:
            strategy_name: Strategy to evaluate
            context: Current situation context
            target_outcome: Desired outcome type
            
        Returns:
            Prediction with confidence and reasoning
        """
        
        if not MEMORY_SYSTEMS_AVAILABLE:
            return {
                "predicted_success_rate": 0.5,
                "confidence": 0.1,
                "reasoning": "Memory systems not available",
                "risk_factors": [],
                "recommendations": []
            }
        
        # Gather historical data for this strategy
        strategy_outcomes = [
            outcome for outcome in self.sf_memory.outcome_records
            if outcome.action_taken.get("strategy", "") == strategy_name
        ]
        
        if len(strategy_outcomes) < self.min_samples_for_prediction:
            return {
                "predicted_success_rate": 0.5,
                "confidence": 0.2,
                "reasoning": f"Insufficient data for {strategy_name} (need {self.min_samples_for_prediction}, have {len(strategy_outcomes)})",
                "risk_factors": ["Limited historical data"],
                "recommendations": ["Gather more experience with this strategy"]
            }
        
        # Calculate base success rate
        successful_outcomes = [o for o in strategy_outcomes if o.outcome_quality >= 0.6]
        base_success_rate = len(successful_outcomes) / len(strategy_outcomes)
        
        # Analyze context similarity
        similar_contexts = self._find_similar_contexts(context, strategy_outcomes)
        context_adjusted_rate = self._calculate_context_adjusted_rate(
            similar_contexts, base_success_rate
        )
        
        # Apply trend analysis
        trend_adjusted_rate = self._apply_trend_analysis(
            strategy_outcomes, context_adjusted_rate
        )
        
        # Calculate confidence
        confidence = self._calculate_prediction_confidence(
            strategy_outcomes, similar_contexts, context
        )
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(strategy_name, context, strategy_outcomes)
        
        # Generate recommendations
        recommendations = self._generate_strategy_recommendations(
            strategy_name, context, strategy_outcomes, trend_adjusted_rate
        )
        
        # Generate reasoning
        reasoning = self._generate_prediction_reasoning(
            strategy_name, base_success_rate, context_adjusted_rate, 
            trend_adjusted_rate, similar_contexts
        )
        
        prediction = {
            "predicted_success_rate": trend_adjusted_rate,
            "confidence": confidence,
            "reasoning": reasoning,
            "base_success_rate": base_success_rate,
            "context_adjustment": context_adjusted_rate - base_success_rate,
            "trend_adjustment": trend_adjusted_rate - context_adjusted_rate,
            "sample_size": len(strategy_outcomes),
            "similar_contexts_found": len(similar_contexts),
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "prediction_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Store prediction for accuracy tracking
        self._store_prediction_for_tracking(prediction, strategy_name, context)
        
        return prediction
    
    def _find_similar_contexts(self, current_context: Dict[str, Any], 
                             outcomes: List[StrategyOutcome]) -> List[Tuple[StrategyOutcome, float]]:
        """Find outcomes with similar contexts and their similarity scores."""
        similar_contexts = []
        
        for outcome in outcomes:
            similarity = self._calculate_context_similarity(current_context, outcome.context)
            if similarity >= self.context_similarity_threshold:
                similar_contexts.append((outcome, similarity))
        
        # Sort by similarity
        similar_contexts.sort(key=lambda x: x[1], reverse=True)
        return similar_contexts
    
    def _calculate_context_similarity(self, context1: Dict[str, Any], 
                                    context2: Dict[str, Any]) -> float:
        """Calculate similarity between two contexts."""
        if not context1 or not context2:
            return 0.0
        
        # Key factors for similarity
        important_keys = [
            "situation_type", "content_type", "difficulty_level",
            "complexity", "preparation_level", "time_pressure"
        ]
        
        similarities = []
        
        for key in important_keys:
            if key in context1 and key in context2:
                val1, val2 = context1[key], context2[key]
                
                if isinstance(val1, str) and isinstance(val2, str):
                    # String similarity
                    if val1.lower() == val2.lower():
                        similarities.append(1.0)
                    elif val1.lower() in val2.lower() or val2.lower() in val1.lower():
                        similarities.append(0.7)
                    else:
                        similarities.append(0.0)
                        
                elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    # Numerical similarity
                    diff = abs(val1 - val2)
                    if isinstance(val1, float) or isinstance(val2, float):
                        # Assume 0-1 range for float values
                        similarity = max(0.0, 1.0 - diff)
                    else:
                        # Integer values - normalize by reasonable range
                        similarity = max(0.0, 1.0 - diff / 10.0)
                    similarities.append(similarity)
                
                elif isinstance(val1, bool) and isinstance(val2, bool):
                    similarities.append(1.0 if val1 == val2 else 0.0)
        
        return statistics.mean(similarities) if similarities else 0.0
    
    def _calculate_context_adjusted_rate(self, similar_contexts: List[Tuple[StrategyOutcome, float]], 
                                       base_rate: float) -> float:
        """Adjust success rate based on similar contexts."""
        if not similar_contexts:
            return base_rate
        
        # Weight outcomes by context similarity
        weighted_successes = 0.0
        total_weight = 0.0
        
        for outcome, similarity in similar_contexts:
            weight = similarity
            success = 1.0 if outcome.outcome_quality >= 0.6 else 0.0
            
            weighted_successes += success * weight
            total_weight += weight
        
        if total_weight == 0:
            return base_rate
        
        context_rate = weighted_successes / total_weight
        
        # Blend with base rate based on confidence in context similarity
        confidence_in_context = min(1.0, len(similar_contexts) / 5.0)
        adjusted_rate = (context_rate * confidence_in_context + 
                        base_rate * (1.0 - confidence_in_context))
        
        return adjusted_rate
    
    def _apply_trend_analysis(self, outcomes: List[StrategyOutcome], 
                            current_rate: float) -> float:
        """Apply temporal trend analysis to adjust predictions."""
        if len(outcomes) < 4:
            return current_rate
        
        # Sort by timestamp
        sorted_outcomes = sorted(outcomes, key=lambda x: x.timestamp)
        
        # Calculate recent vs older performance
        cutoff = len(sorted_outcomes) // 2
        older_outcomes = sorted_outcomes[:cutoff]
        recent_outcomes = sorted_outcomes[cutoff:]
        
        older_rate = statistics.mean([
            1.0 if o.outcome_quality >= 0.6 else 0.0 for o in older_outcomes
        ])
        recent_rate = statistics.mean([
            1.0 if o.outcome_quality >= 0.6 else 0.0 for o in recent_outcomes
        ])
        
        # Calculate trend strength
        trend = recent_rate - older_rate
        trend_strength = abs(trend)
        
        # Apply trend with diminishing effect
        trend_adjustment = trend * 0.3 * min(1.0, trend_strength * 2)
        adjusted_rate = current_rate + trend_adjustment
        
        return max(0.0, min(1.0, adjusted_rate))
    
    def _calculate_prediction_confidence(self, outcomes: List[StrategyOutcome],
                                       similar_contexts: List[Tuple[StrategyOutcome, float]],
                                       context: Dict[str, Any]) -> float:
        """Calculate confidence in the prediction."""
        factors = []
        
        # Sample size confidence
        sample_confidence = min(1.0, len(outcomes) / 10.0)
        factors.append(sample_confidence * 0.4)
        
        # Context similarity confidence
        if similar_contexts:
            avg_similarity = statistics.mean([sim for _, sim in similar_contexts])
            context_confidence = avg_similarity
        else:
            context_confidence = 0.0
        factors.append(context_confidence * 0.3)
        
        # Consistency confidence (low variance in outcomes)
        success_levels = [o.outcome_quality for o in outcomes]
        if len(success_levels) > 1:
            variance = statistics.variance(success_levels)
            consistency_confidence = max(0.0, 1.0 - variance * 2)
        else:
            consistency_confidence = 0.5
        factors.append(consistency_confidence * 0.2)
        
        # Recency confidence (more recent data is more reliable)
        if outcomes:
            recent_cutoff = datetime.now(timezone.utc) - timedelta(days=30)
            recent_outcomes = [
                o for o in outcomes 
                if datetime.fromisoformat(o.timestamp.replace('Z', '+00:00')) > recent_cutoff
            ]
            recency_confidence = len(recent_outcomes) / len(outcomes)
        else:
            recency_confidence = 0.0
        factors.append(recency_confidence * 0.1)
        
        total_confidence = sum(factors)
        return max(0.1, min(0.95, total_confidence))
    
    def _identify_risk_factors(self, strategy_name: str, context: Dict[str, Any],
                             outcomes: List[StrategyOutcome]) -> List[str]:
        """Identify potential risk factors for strategy failure."""
        risk_factors = []
        
        # Analyze failure patterns
        failed_outcomes = [o for o in outcomes if o.outcome_quality < 0.4]
        
        if failed_outcomes:
            # Common failure factors
            failure_factors = defaultdict(int)
            for outcome in failed_outcomes:
                for factor in outcome.contributing_factors:
                    failure_factors[factor] += 1
            
            # Check if current context has high-risk factors
            for factor, count in failure_factors.items():
                if count / len(failed_outcomes) >= 0.5:  # Factor in 50%+ of failures
                    # Check if current context might trigger this factor
                    if self._context_suggests_risk_factor(context, factor):
                        risk_factors.append(f"High risk of {factor}")
        
        # Context-specific risks
        if context.get("time_pressure", False):
            risk_factors.append("Time pressure may reduce effectiveness")
        
        if context.get("preparation_level", "medium") == "low":
            risk_factors.append("Low preparation increases failure risk")
        
        if context.get("difficulty_level", "medium") == "high":
            risk_factors.append("High difficulty may challenge strategy")
        
        return risk_factors
    
    def _context_suggests_risk_factor(self, context: Dict[str, Any], risk_factor: str) -> bool:
        """Check if current context suggests a risk factor might occur."""
        risk_indicators = {
            "insufficient_preparation": lambda c: c.get("preparation_level", "medium") == "low",
            "time_pressure": lambda c: c.get("time_pressure", False),
            "complexity_underestimated": lambda c: c.get("difficulty_level", "medium") == "high",
            "attention_scattered": lambda c: c.get("focus_quality", 0.5) < 0.5,
            "wrong_approach": lambda c: c.get("strategy_mismatch", False)
        }
        
        for factor, indicator_func in risk_indicators.items():
            if factor in risk_factor.lower():
                return indicator_func(context)
        
        return False
    
    def _generate_strategy_recommendations(self, strategy_name: str, context: Dict[str, Any],
                                         outcomes: List[StrategyOutcome], 
                                         predicted_rate: float) -> List[str]:
        """Generate recommendations to improve strategy success."""
        recommendations = []
        
        if predicted_rate < 0.5:
            recommendations.append("Consider alternative strategy - low predicted success")
        
        # Analyze successful outcomes for success factors
        successful_outcomes = [o for o in outcomes if o.outcome_quality >= 0.6]
        
        if successful_outcomes:
            # Common success factors
            success_factors = defaultdict(int)
            for outcome in successful_outcomes:
                for factor in outcome.contributing_factors:
                    success_factors[factor] += 1
            
            # Recommend most common success factors
            top_factors = sorted(success_factors.items(), key=lambda x: x[1], reverse=True)
            for factor, count in top_factors[:3]:
                if count / len(successful_outcomes) >= 0.5:
                    recommendations.append(f"Ensure {factor} - key success factor")
        
        # Context-specific recommendations
        if context.get("preparation_level", "medium") == "low":
            recommendations.append("Increase preparation before attempting strategy")
        
        if context.get("difficulty_level", "medium") == "high":
            recommendations.append("Consider breaking into smaller steps")
        
        return recommendations
    
    def _generate_prediction_reasoning(self, strategy_name: str, base_rate: float,
                                     context_rate: float, trend_rate: float,
                                     similar_contexts: List[Tuple[StrategyOutcome, float]]) -> str:
        """Generate human-readable reasoning for the prediction."""
        reasoning_parts = []
        
        reasoning_parts.append(f"{strategy_name} has {base_rate:.1%} historical success rate")
        
        context_adjustment = context_rate - base_rate
        if abs(context_adjustment) > 0.05:
            if context_adjustment > 0:
                reasoning_parts.append(f"Context analysis suggests {context_adjustment:.1%} improvement")
            else:
                reasoning_parts.append(f"Context analysis suggests {abs(context_adjustment):.1%} reduction")
        
        trend_adjustment = trend_rate - context_rate
        if abs(trend_adjustment) > 0.05:
            if trend_adjustment > 0:
                reasoning_parts.append(f"Recent trend shows {trend_adjustment:.1%} improvement")
            else:
                reasoning_parts.append(f"Recent trend shows {abs(trend_adjustment):.1%} decline")
        
        if similar_contexts:
            reasoning_parts.append(f"Based on {len(similar_contexts)} similar situations")
        
        return ". ".join(reasoning_parts)
    
    def _store_prediction_for_tracking(self, prediction: Dict[str, Any], 
                                     strategy_name: str, context: Dict[str, Any]):
        """Store prediction for later accuracy evaluation."""
        tracking_record = {
            "prediction_id": hashlib.md5(
                f"{strategy_name}_{context}_{prediction['prediction_timestamp']}".encode()
            ).hexdigest()[:12],
            "timestamp": prediction["prediction_timestamp"],
            "strategy_name": strategy_name,
            "context": context,
            "predicted_success_rate": prediction["predicted_success_rate"],
            "confidence": prediction["confidence"],
            "actual_outcome": None,  # To be filled when outcome occurs
            "prediction_accuracy": None  # To be calculated later
        }
        
        self.prediction_accuracy.append(tracking_record)
        
        # Keep only recent predictions (last 100)
        if len(self.prediction_accuracy) > 100:
            self.prediction_accuracy = self.prediction_accuracy[-100:]
    
    def update_prediction_accuracy(self, strategy_name: str, context: Dict[str, Any],
                                 actual_success_level: float):
        """Update prediction accuracy when actual outcome is known."""
        # Find matching predictions
        for record in self.prediction_accuracy:
            if (record["strategy_name"] == strategy_name and 
                record["actual_outcome"] is None):
                
                # Check context similarity
                context_sim = self._calculate_context_similarity(record["context"], context)
                if context_sim > 0.7:  # Close enough match
                    # Update with actual outcome
                    record["actual_outcome"] = actual_success_level
                    
                    # Calculate accuracy
                    predicted_success = record["predicted_success_rate"] > 0.5
                    actual_success = actual_success_level > 0.5
                    
                    if predicted_success == actual_success:
                        # Correct prediction
                        accuracy = 1.0 - abs(record["predicted_success_rate"] - actual_success_level)
                    else:
                        # Incorrect prediction
                        accuracy = abs(record["predicted_success_rate"] - actual_success_level)
                    
                    record["prediction_accuracy"] = accuracy
                    break
        
        self._save_all()
    
    def get_prediction_performance(self) -> Dict[str, Any]:
        """Get overall prediction performance metrics."""
        completed_predictions = [
            r for r in self.prediction_accuracy 
            if r["actual_outcome"] is not None
        ]
        
        if not completed_predictions:
            return {
                "total_predictions": len(self.prediction_accuracy),
                "completed_predictions": 0,
                "average_accuracy": 0.0,
                "confidence_calibration": 0.0
            }
        
        # Calculate metrics
        accuracies = [r["prediction_accuracy"] for r in completed_predictions]
        avg_accuracy = statistics.mean(accuracies)
        
        # Confidence calibration (do high-confidence predictions perform better?)
        high_conf_predictions = [r for r in completed_predictions if r["confidence"] > 0.7]
        if high_conf_predictions:
            high_conf_accuracy = statistics.mean([r["prediction_accuracy"] for r in high_conf_predictions])
            low_conf_predictions = [r for r in completed_predictions if r["confidence"] <= 0.7]
            low_conf_accuracy = statistics.mean([r["prediction_accuracy"] for r in low_conf_predictions]) if low_conf_predictions else 0
            confidence_calibration = high_conf_accuracy - low_conf_accuracy
        else:
            confidence_calibration = 0.0
        
        return {
            "total_predictions": len(self.prediction_accuracy),
            "completed_predictions": len(completed_predictions),
            "average_accuracy": avg_accuracy,
            "confidence_calibration": confidence_calibration,
            "high_confidence_predictions": len(high_conf_predictions),
            "prediction_performance": "Good" if avg_accuracy > 0.7 else "Needs improvement"
        }

# Convenience functions
def predict_success(strategy_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Quick function to predict strategy success."""
    enhancer = PredictiveLearningEnhancer()
    return enhancer.predict_strategy_success(strategy_name, context)

def update_accuracy(strategy_name: str, context: Dict[str, Any], actual_result: float):
    """Quick function to update prediction accuracy."""
    enhancer = PredictiveLearningEnhancer()
    enhancer.update_prediction_accuracy(strategy_name, context, actual_result)

if __name__ == "__main__":
    print("🔮 Testing Predictive Learning Enhancer...")
    
    # Initialize enhancer
    enhancer = PredictiveLearningEnhancer()
    
    # Test prediction
    print("\n🎯 Testing strategy success prediction...")
    
    test_context = {
        "situation_type": "conceptual_learning",
        "content_type": "philosophical",
        "difficulty_level": "high",
        "preparation_level": "high"
    }
    
    prediction = enhancer.predict_strategy_success(
        "deep_symbolic_processing",
        test_context
    )
    
    print(f"  Strategy: deep_symbolic_processing")
    print(f"  Predicted success rate: {prediction['predicted_success_rate']:.2%}")
    print(f"  Confidence: {prediction['confidence']:.2f}")
    print(f"  Reasoning: {prediction['reasoning']}")
    
    if prediction['risk_factors']:
        print(f"  Risk factors:")
        for risk in prediction['risk_factors']:
            print(f"    ⚠️ {risk}")
    
    if prediction['recommendations']:
        print(f"  Recommendations:")
        for rec in prediction['recommendations']:
            print(f"    💡 {rec}")
    
    # Test prediction performance
    print("\n📊 Prediction performance metrics:")
    performance = enhancer.get_prediction_performance()
    
    for key, value in performance.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")
    
    print("\n🔮 Predictive Learning Enhancer ready!")
    print("   Sophia can now predict strategy success with confidence estimates")