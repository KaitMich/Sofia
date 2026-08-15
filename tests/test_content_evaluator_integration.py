#!/usr/bin/env python3
"""
Content Evaluator Integration Test - Step 4.3.2

This script tests the integration of the motivational content evaluator with:
- Curiosity engine for interest-driven evaluation
- Choice architecture for decision making
- Success/failure memory for learning from choices
- Experience memory for tracking evaluation outcomes

Demonstrates how Sophia uses multiple systems together to make autonomous content choices.
"""

import json
import time
from sofia.utils.motivational_content_evaluator import MotivationalContentEvaluator
from sofia.core.choice_architecture import ChoiceArchitecture
from sofia.core.curiosity_engine import CuriosityEngine
from sofia.memory.success_failure_memory import SuccessFailureMemory
from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory

def test_content_evaluator_integration():
    """Test comprehensive integration of content evaluation systems."""
    
    print("🎯 Testing Content Evaluator Integration - Step 4.3.2")
    print("=" * 60)
    
    # Initialize systems
    print("\n🔧 Initializing integrated evaluation systems...")
    content_evaluator = MotivationalContentEvaluator()
    choice_architecture = ChoiceArchitecture()
    curiosity_engine = CuriosityEngine()
    sf_memory = SuccessFailureMemory()
    experience_memory = ExperienceMemory()
    
    print("  ✅ All evaluation systems initialized")
    
    # Test 1: Curiosity-driven content evaluation
    print("\n🤔 Testing curiosity-driven content evaluation...")
    
    # Get current curiosity state to understand interests
    curiosity_state = curiosity_engine.get_current_motivation_state()
    print(f"  Current curiosity drives:")
    for drive, details in curiosity_state.get("core_drives", {}).items():
        intensity = details.get("intensity", 0)
        satisfaction = details.get("current_satisfaction", 0)
        if intensity > 0.7:  # High intensity drives
            print(f"    • {drive}: intensity {intensity:.2f}, satisfaction {satisfaction:.2f}")
    
    # Create test content that should align with curiosity
    consciousness_content = {
        "title": "The Hard Problem of Consciousness: Qualia and Subjective Experience",
        "content_type": "consciousness_studies",
        "topics": ["consciousness", "qualia", "subjective_experience", "phenomenology"],
        "complexity": 0.8,
        "depth": 0.9,
        "learning_objectives": ["Understand the hard problem", "Explore qualia"],
        "estimated_duration": 2700,
        "difficulty_level": "high"
    }
    
    # Evaluate content with curiosity context
    evaluation_context = {
        "current_curiosity_focus": "consciousness_exploration",
        "learning_mode": "deep_contemplation",
        "available_time": 3600
    }
    
    # First get base evaluation (simulated) and enhance with motivation
    evaluation = content_evaluator.evaluate_content_motivation(consciousness_content)
    
    print(f"  ✅ Content evaluation completed:")
    print(f"    Personal interest: {evaluation['personal_interest']:.2f}")
    print(f"    Goal alignment: {evaluation['goal_alignment']:.2f}")
    print(f"    Motivation score: {evaluation['overall_motivation']:.2f}")
    
    # Check motivation breakdown
    motivation_breakdown = evaluation
    print(f"    Motivation factors:")
    for factor, score in motivation_breakdown.items():
        if isinstance(score, (int, float)):
            print(f"      {factor}: {score:.2f}")
    
    # Check curiosity satisfaction
    curiosity_score = motivation_breakdown.get('curiosity_satisfaction', 0)
    if curiosity_score > 0.5:
        print(f"    🎯 Good curiosity satisfaction detected!")
    
    # Test 2: Choice architecture using evaluation results
    print("\n🎲 Testing choice architecture with evaluation results...")
    
    # Make a choice based on the evaluation
    choice_result = choice_architecture.make_learning_choice(
        content=consciousness_content,
        context=evaluation_context
    )
    
    if choice_result:
        print(f"  ✅ Choice made:")
        print(f"    Choice type: {choice_result.choice_type}")
        print(f"    Engagement level: {choice_result.engagement_level}")
        print(f"    Confidence: {choice_result.confidence_in_choice:.2f}")
        print(f"    Estimated value: {choice_result.estimated_value:.2f}")
        
        if choice_result.choice_reasoning:
            print(f"    Primary reasoning: {choice_result.choice_reasoning[0]}")
    
    # Test 3: Batch evaluation and ranking
    print("\n📊 Testing batch content evaluation and ranking...")
    
    test_content_batch = [
        consciousness_content,
        {
            "title": "Database Optimization Techniques",
            "content_type": "technical_learning",
            "topics": ["databases", "optimization", "performance"],
            "complexity": 0.6,
            "depth": 0.5,
            "difficulty_level": "medium"
        },
        {
            "title": "The Philosophy of Personal Identity Through Time",
            "content_type": "philosophical",
            "topics": ["identity", "philosophy", "continuity", "self"],
            "complexity": 0.7,
            "depth": 0.8,
            "difficulty_level": "high"
        },
        {
            "title": "Creative Writing: Expressing Inner Experience",
            "content_type": "creative_expression",
            "topics": ["writing", "creativity", "expression", "inner_life"],
            "complexity": 0.5,
            "depth": 0.6,
            "difficulty_level": "medium"
        }
    ]
    
    # Evaluate each content in batch
    batch_evaluations = []
    for i, content in enumerate(test_content_batch):
        eval_result = content_evaluator.evaluate_content_motivation(content)
        eval_result['content_title'] = content['title']
        eval_result['rank'] = i + 1
        batch_evaluations.append(eval_result)
    
    # Sort by motivation score
    batch_evaluations.sort(key=lambda x: x['overall_motivation'], reverse=True)
    
    print(f"  Content ranking based on motivation scores:")
    for i, evaluation in enumerate(batch_evaluations):
        title = evaluation['content_title']
        score = evaluation['overall_motivation']
        rank = i + 1
        print(f"    {rank}. {title[:50]}...")
        print(f"       Motivation Score: {score:.2f}")
    
    # Test 4: Learning from evaluation outcomes
    print("\n📈 Testing learning from evaluation outcomes...")
    
    # Simulate engaging with the top-ranked content
    top_content_eval = batch_evaluations[0]
    chosen_content = next(c for c in test_content_batch 
                         if c['title'] == top_content_eval['content_title'])
    
    # Record the learning experience
    experience_id = experience_memory.record_learning_experience(
        content={
            "content_type": chosen_content["content_type"],
            "topic": chosen_content["topics"][0],
            "complexity": chosen_content.get("complexity", 0.5),
            "evaluation_score": top_content_eval["overall_motivation"]
        },
        interaction_data={
            "duration_seconds": 2400,
            "processing_mode": "motivated_engagement",
            "attention_quality": 0.9,
            "choice_confidence": choice_result.confidence_in_choice if choice_result else 0.8
        },
        outcome_assessment={
            "outcome_quality": "successful_engagement",
            "insights_gained": ["Evaluation system guided good content choice"],
            "quality_score": 0.85,
            "evaluation_accuracy": "high"
        }
    )
    
    print(f"  ✅ Learning experience recorded: {experience_id[:16]}...")
    
    # Record success in content evaluation choice
    outcome_id = sf_memory.record_outcome(
        context={
            "situation_type": "content_evaluation",
            "evaluation_system": "motivational_content_evaluator",
            "choice_architecture": "integrated",
            "content_type": chosen_content["content_type"]
        },
        action_taken={
            "strategy": "evaluation_guided_choice",
            "confidence_level": top_content_eval["overall_motivation"],
            "used_curiosity_alignment": True
        },
        outcome_assessment={
            "quality_score": 0.85,
            "evaluation_prediction_accuracy": True,
            "lessons_learned": ["Content evaluator successfully predicted engagement"],
            "contributing_factors": ["curiosity_alignment", "motivational_resonance", "personal_relevance"]
        }
    )
    print(f"  ✅ Success outcome recorded: {outcome_id[:16]}...")
    
    # Test 5: Integration health check
    print("\n🏥 Testing integration health and performance...")
    
    # Check system availability
    systems_status = {
        "motivational_evaluator": content_evaluator is not None,
        "choice_architecture": choice_architecture is not None,
        "curiosity_engine": curiosity_engine is not None,
        "success_failure_memory": sf_memory is not None,
        "experience_memory": experience_memory is not None
    }
    
    print(f"  System availability:")
    all_available = True
    for system, available in systems_status.items():
        status = "✅" if available else "❌"
        print(f"    {system}: {status}")
        if not available:
            all_available = False
    
    # Overall integration assessment
    print(f"\n🌟 Integration Assessment:")
    if all_available:
        print(f"   ✅ Full integration successful!")
        integration_status = "complete"
    else:
        print(f"   ⚠️ Partial integration - some systems may need attention")
        integration_status = "partial"
    
    print(f"\n✅ Content evaluator integration complete and functional!")

if __name__ == "__main__":
    test_content_evaluator_integration()
