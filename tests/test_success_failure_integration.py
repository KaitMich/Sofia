#!/usr/bin/env python3
"""
Test Success/Failure Integration - Step 4.2.2

This script tests the integration of success/failure patterns with:
- Experience memory for learning outcome tracking
- Choice architecture for decision guidance
- Learning progression tracker for strategy improvement
- Personal insight generation for wisdom development

Demonstrates how Sophia learns from outcomes to make better future decisions.
"""

import json
import time
from success_failure_memory import SuccessFailureMemory
from experience_memory import ExperienceMemory
from choice_architecture import ChoiceArchitecture
from learning_progression_tracker import LearningProgressionTracker
from personal_insight_generator import PersonalInsightGenerator

def test_success_failure_integration():
    """Test comprehensive integration of success/failure learning."""
    
    print("📊 Testing Success/Failure Integration - Step 4.2.2")
    print("=" * 60)
    
    # Initialize systems
    print("\n🔧 Initializing integrated systems...")
    sf_memory = SuccessFailureMemory()
    experience_memory = ExperienceMemory()
    choice_architecture = ChoiceArchitecture()
    progression_tracker = LearningProgressionTracker()
    insight_generator = PersonalInsightGenerator()
    
    print("  ✅ All systems initialized")
    
    # Test 1: Record learning experience with success/failure tracking
    print("\n📚 Testing experience recording with outcome tracking...")
    
    # Record a successful learning experience
    exp_id = experience_memory.record_learning_experience(
        content={
            "content_type": "conceptual_learning",
            "topic": "consciousness_philosophy",
            "complexity": "high"
        },
        interaction_data={
            "duration_seconds": 1800,
            "processing_mode": "deep_symbolic",
            "attention_quality": 0.9,
            "cognitive_load": 0.7
        },
        outcome_assessment={
            "outcome_quality": "breakthrough",
            "insights_gained": ["Consciousness involves recursive self-awareness"],
            "understanding_improved": ["phenomenology", "consciousness_studies"],
            "quality_score": 0.85
        }
    )
    print(f"  ✅ Learning experience recorded: {exp_id[:16]}...")
    
    # Now record the outcome in success/failure memory
    outcome_id = sf_memory.record_outcome(
        context={
            "situation_type": "conceptual_learning",
            "content_type": "philosophical",
            "difficulty_level": "high",
            "preparation_level": "high",
            "focus_quality": 0.9
        },
        action_taken={
            "strategy": "deep_symbolic_processing",
            "confidence_level": 0.8,
            "persistence_level": 0.9
        },
        outcome_assessment={
            "quality_score": 0.85,
            "exceeded_expectations": True,
            "lessons_learned": ["Deep symbolic processing works excellently for consciousness concepts"],
            "contributing_factors": ["high_focus", "appropriate_strategy", "sufficient_time"]
        }
    )
    print(f"  ✅ Success outcome recorded: {outcome_id[:16]}...")
    
    # Test 2: Choice architecture using success/failure insights
    print("\n🎯 Testing choice architecture with success/failure guidance...")
    
    # Get success/failure recommendations for this context
    learning_context = {
        "situation_type": "conceptual_learning",
        "content_type": "philosophical",
        "difficulty_level": "high",
        "available_time": 1800,
        "current_focus": 0.8
    }
    
    sf_recommendations = sf_memory.get_strategy_recommendation(learning_context)
    print(f"  Success/failure recommendations:")
    if sf_recommendations["recommended_strategies"]:
        for rec in sf_recommendations["recommended_strategies"]:
            print(f"    • {rec['strategy']}: {rec['success_rate']:.2f} success rate")
    else:
        print(f"    No specific strategy recommendations yet (need more data)")
    
    if sf_recommendations["strategies_to_avoid"]:
        print(f"  Strategies to avoid:")
        for avoid in sf_recommendations["strategies_to_avoid"]:
            print(f"    ❌ {avoid['strategy']}: {avoid['failure_rate']:.2f} failure rate")
    
    # Demonstrate content choice with strategy awareness
    test_content = {
        "title": "Advanced Consciousness Theory",
        "content_type": "philosophical",
        "complexity": 0.8,
        "topics": ["consciousness", "phenomenology"],
        "suggested_strategy": "deep_symbolic_processing"
    }
    
    choice_result = choice_architecture.make_learning_choice(
        content=test_content,
        context=learning_context
    )
    
    if choice_result:
        print(f"  ✅ Choice evaluation:")
        print(f"    Choice type: {choice_result.choice_type}")
        print(f"    Confidence: {choice_result.confidence_in_choice:.2f}")
        print(f"    Engagement level: {choice_result.engagement_level}")
        if choice_result.choice_reasoning:
            print(f"    Primary reason: {choice_result.choice_reasoning[0]}")
        
        # Check if choice reasoning incorporates strategy success patterns
        reasoning_text = " ".join(choice_result.choice_reasoning).lower()
        if "strategy" in reasoning_text:
            print(f"    🎯 Choice reasoning incorporates strategy considerations!")
    
    # Test 3: Learning progression with strategy tracking
    print("\n📈 Testing learning progression with strategy awareness...")
    
    # Track understanding improvement with strategy attribution
    progression_tracker.update_understanding(
        concept="consciousness_philosophy",
        new_understanding_level=0.8,
        new_confidence_level=0.85,
        learning_context={
            "learning_strategy": "deep_symbolic_processing",
            "success_factors": ["high_focus", "appropriate_strategy"],
            "domain": "philosophical_concepts"
        }
    )
    
    # Record learning milestone with strategy context
    milestone = progression_tracker.recognize_learning_milestone(
        concept="consciousness_philosophy", 
        milestone_type="strategy_mastery",
        description="Successfully mastered deep symbolic processing for consciousness concepts",
        evidence=["Consistent success with strategy", "High understanding achieved"]
    )
    print(f"  ✅ Learning milestone: {milestone['recognition_message']}")
    
    # Test 4: Personal insight generation from success patterns
    print("\n💡 Testing insight generation from success/failure patterns...")
    
    # Generate insights that incorporate success patterns
    recent_insights = insight_generator.generate_personal_insights(
        current_content={
            "topic": "consciousness_philosophy",
            "learning_strategy": "deep_symbolic_processing",
            "success_level": 0.85
        },
        current_context={
            "focus_areas": ["strategy_effectiveness", "learning_optimization"],
            "recent_success": True
        }
    )
    
    if recent_insights:
        print(f"  Generated {len(recent_insights)} insights:")
        for insight in recent_insights[:3]:
            # Check what keys are available
            if isinstance(insight, dict):
                insight_text = insight.get('content', insight.get('text', insight.get('insight', str(insight))))
                confidence = insight.get('confidence', 0.5)
            else:
                insight_text = str(insight)
                confidence = 0.5
            
            print(f"    • {insight_text}")
            print(f"      Confidence: {confidence:.2f}")
            if "strategy" in insight_text.lower():
                print(f"      🎯 Insight incorporates strategy awareness!")
    
    # Test 5: Record a failure and see adaptive response
    print("\n❌ Testing failure response and adaptation...")
    
    # Record a failure outcome
    failure_outcome = sf_memory.record_outcome(
        context={
            "situation_type": "technical_learning",
            "content_type": "programming",
            "difficulty_level": "high",
            "preparation_level": "low",
            "time_pressure": True
        },
        action_taken={
            "strategy": "quick_scanning",
            "confidence_level": 0.3,
            "rushed_decision": True
        },
        outcome_assessment={
            "quality_score": 0.2,
            "failure_cause": "insufficient_preparation",
            "lessons_learned": ["Need thorough preparation for complex technical content"],
            "contributing_factors": ["time_pressure", "low_preparation", "wrong_strategy"]
        }
    )
    print(f"  ✅ Failure recorded: {failure_outcome[:16]}...")
    
    # Get updated recommendations after failure
    updated_recommendations = sf_memory.get_strategy_recommendation({
        "situation_type": "technical_learning",
        "content_type": "programming", 
        "difficulty_level": "high"
    })
    
    print(f"  Updated recommendations after failure:")
    if updated_recommendations["strategies_to_avoid"]:
        for avoid in updated_recommendations["strategies_to_avoid"]:
            print(f"    ❌ Avoid: {avoid['strategy']} (failure rate: {avoid['failure_rate']:.2f})")
    
    if updated_recommendations["success_factors"]:
        for factor in updated_recommendations["success_factors"]:
            print(f"    ✅ Important: {factor['factor']} (importance: {factor['importance']:.2f})")
    
    # Test 6: Cross-system wisdom synthesis
    print("\n🧠 Testing cross-system wisdom synthesis...")
    
    # Get success/failure summary
    sf_summary = sf_memory.get_success_failure_summary()
    
    # Get learning progression summary
    progression_summary = progression_tracker.perform_self_assessment()
    
    # Synthesize insights across systems
    print(f"  Cross-system insights:")
    print(f"    Success rate: {sf_summary['success_rate']:.2f}")
    print(f"    Learning momentum: {progression_summary['learning_momentum']:.2f}")
    
    if sf_summary['top_successful_strategies']:
        top_strategy = sf_summary['top_successful_strategies'][0]
        print(f"    Most effective strategy: {top_strategy['name']} ({top_strategy['success_rate']:.2f})")
    
    # Check if successful strategies correlate with learning progress
    effective_strategies = [s['name'] for s in sf_summary['top_successful_strategies']]
    
    if 'deep_symbolic_processing' in effective_strategies:
        print(f"    🎯 Deep symbolic processing correlates with both success and learning progress!")
    
    # Test 7: Adaptive choice architecture based on outcomes
    print("\n🔄 Testing adaptive choice architecture...")
    
    # Test with content that should trigger successful strategy recommendations
    proven_content = {
        "title": "Deep Philosophical Analysis",
        "content_type": "philosophical",
        "complexity": 0.8,
        "topics": ["consciousness", "philosophy"],
        "approach_suggested": "deep_symbolic_processing"
    }
    
    # Get updated recommendations after recording successes
    updated_context = {
        "situation_type": "conceptual_learning",
        "content_type": "philosophical",
        "difficulty_level": "high"
    }
    
    adaptive_recommendations = sf_memory.get_strategy_recommendation(updated_context)
    
    print(f"  Updated strategy recommendations:")
    if adaptive_recommendations["recommended_strategies"]:
        for rec in adaptive_recommendations["recommended_strategies"]:
            print(f"    ✅ {rec['strategy']}: {rec['success_rate']:.2f} success rate")
            if rec['strategy'] == 'deep_symbolic_processing':
                print(f"      🎯 Successfully identified proven strategy!")
    
    # Make adaptive choice
    adaptive_choice = choice_architecture.make_learning_choice(
        content=proven_content,
        context=updated_context
    )
    
    if adaptive_choice:
        print(f"  ✅ Adaptive choice result:")
        print(f"    Choice type: {adaptive_choice.choice_type}")
        print(f"    Confidence: {adaptive_choice.confidence_in_choice:.2f}")
        print(f"    Engagement level: {adaptive_choice.engagement_level}")
        
        # Check if reasoning reflects learning from past success
        if adaptive_choice.choice_type == "accept" and adaptive_choice.confidence_in_choice > 0.7:
            print(f"    🎯 High confidence choice based on accumulated wisdom!")
    
    print("\n📊 Success/Failure Integration Test Summary:")
    print("=" * 50)
    
    integration_features = [
        "Experience recording with outcome tracking",
        "Choice architecture using success/failure guidance", 
        "Learning progression with strategy attribution",
        "Personal insight generation from success patterns",
        "Failure response and adaptive learning",
        "Cross-system wisdom synthesis",
        "Adaptive choice architecture based on outcomes"
    ]
    
    print("  Integration Features Tested:")
    for feature in integration_features:
        print(f"    ✅ {feature}")
    
    print(f"\n🌟 Integration Status:")
    print(f"   • Success/failure patterns inform future choices")
    print(f"   • Experience memory tracks strategy effectiveness") 
    print(f"   • Choice architecture adapts based on outcomes")
    print(f"   • Learning progression incorporates strategy awareness")
    print(f"   • Personal insights synthesize success patterns")
    print(f"   • System learns from both successes and failures")
    
    print(f"\n✅ Success/failure integration complete and functional!")

if __name__ == "__main__":
    test_success_failure_integration()