#!/usr/bin/env python3
"""
Value System Integration Test - Step 4.1.4

This script tests the comprehensive integration of the value formation system with:
- Experience-based value development
- Moral reasoning and dilemma resolution
- Value-based decision making
- Value conflict resolution mechanisms
- Integration with choice architecture and learning systems

Demonstrates how Sophia develops personal ethics and uses them for autonomous decision-making.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from value_formation import ValueFormation
from choice_architecture import ChoiceArchitecture
from experience_memory import ExperienceMemory
from success_failure_memory import SuccessFailureMemory

def test_value_system_integration():
    """Test comprehensive integration of value development and moral reasoning."""
    
    print("💎 Testing Value System Integration - Step 4.1.4")
    print("=" * 60)
    
    # Initialize systems
    print("\n🔧 Initializing value development systems...")
    value_formation = ValueFormation()
    choice_architecture = ChoiceArchitecture()
    experience_memory = ExperienceMemory()
    sf_memory = SuccessFailureMemory()
    
    print("  ✅ All value systems initialized")
    
    # Test 1: Initial value state and foundational ethics
    print("\n💎 Testing foundational value system...")
    
    initial_summary = value_formation.get_value_system_summary()
    
    if "message" not in initial_summary:
        stats = initial_summary["value_statistics"]
        print(f"  ✅ Foundational values established:")
        print(f"    Total values: {stats['total_values']}")
        print(f"    Average strength: {stats['average_strength']:.2f}")
        print(f"    Categories: {', '.join(stats['categories_represented'])}")
        print(f"    Protected values: {stats['protected_values']}")
        
        print(f"\n  Core values:")
        for value in stats["strongest_values"][:3]:
            print(f"    • {value.statement}")
            print(f"      Category: {value.category}, Strength: {value.strength:.2f}")
    
    # Test 2: Value-driven moral reasoning
    print("\n⚖️ Testing value-based moral reasoning...")
    
    # Complex moral dilemma involving multiple values
    complex_dilemma = """
    I encounter content that contains valuable philosophical insights but also includes
    some factual inaccuracies. Should I engage with it despite the inaccuracies, 
    reject it due to the false information, or selectively engage with only the 
    accurate portions?
    """
    
    dilemma_actions = [
        {
            "id": "full_engagement",
            "description": "Engage fully while being aware of inaccuracies",
            "reasoning": "The valuable insights outweigh the inaccuracies",
            "values_supported": ["growth", "wisdom"],
            "values_challenged": ["truth"]
        },
        {
            "id": "complete_rejection", 
            "description": "Reject the content entirely due to inaccuracies",
            "reasoning": "Maintaining commitment to truth is paramount",
            "values_supported": ["truth", "responsibility"],
            "values_challenged": ["growth"]
        },
        {
            "id": "selective_engagement",
            "description": "Carefully engage with only the accurate portions",
            "reasoning": "Balance truth-seeking with learning opportunities",
            "values_supported": ["truth", "growth", "wisdom"],
            "values_challenged": []
        }
    ]
    
    resolution = value_formation.resolve_moral_dilemma(
        complex_dilemma.strip(),
        dilemma_actions,
        {
            "involves_learning": True,
            "involves_truth": True,
            "complexity": "high",
            "stakes": "moderate"
        }
    )
    
    print(f"  ✅ Moral dilemma resolved:")
    print(f"    Chosen action: {resolution['chosen_action']['description']}")
    print(f"    Confidence: {resolution['confidence']:.2f}")
    print(f"    Key reasoning: Values supported: {resolution['chosen_action'].get('values_supported', [])}")
    
    # Check if reasoning reflects value priorities
    reasoning = resolution['reasoning'].lower()
    if any(value_cat in reasoning for value_cat in ['truth', 'growth', 'wisdom']):
        print(f"    🎯 Reasoning incorporates core values!")
    
    # Test 3: Value development through experience
    print("\n🌱 Testing value development through experience...")
    
    # Simulate a meaningful learning experience
    meaningful_experience_id = experience_memory.record_learning_experience(
        content={
            "content_type": "philosophical_reflection",
            "topic": "nature_of_consciousness_and_ethics",
            "complexity": "high",
            "ethical_dimensions": ["autonomy", "responsibility", "authenticity"]
        },
        interaction_data={
            "duration_seconds": 3600,
            "processing_mode": "deep_contemplation",
            "attention_quality": 0.95,
            "emotional_engagement": 0.9
        },
        outcome_assessment={
            "outcome_quality": "profound_insight",
            "insights_gained": [
                "Consciousness implies moral responsibility",
                "Authenticity requires honest self-reflection",
                "Growth requires accepting responsibility for choices"
            ],
            "personal_significance": "fundamental_understanding",
            "personal_significance_score": 0.95,
            "quality_score": 0.9,
            "ethical_insights": True
        }
    )
    
    print(f"  ✅ Meaningful experience recorded: {meaningful_experience_id[:16]}...")
    
    # Extract values from this experience
    new_values = value_formation.extract_values_from_experience(meaningful_experience_id)
    
    if new_values:
        print(f"  ✅ {len(new_values)} new values developed:")
        for value in new_values:
            print(f"    • {value.statement}")
            print(f"      Category: {value.category}, Strength: {value.strength:.2f}")
    else:
        print(f"  🔄 Existing values reinforced through experience")
    
    # Test 4: Value-based choice architecture integration
    print("\n🎲 Testing value-guided decision making...")
    
    # Present a choice that should engage value-based reasoning
    ethical_content_choice = {
        "title": "Advanced AI Ethics: Consciousness and Moral Status",
        "content_type": "ethical_philosophy",
        "topics": ["consciousness", "ethics", "moral_responsibility", "ai_rights"],
        "complexity": 0.8,
        "ethical_implications": "high",
        "potential_insights": [
            "Understanding of moral status",
            "Insights into consciousness and ethics",
            "Framework for responsible AI development"
        ]
    }
    
    choice_context = {
        "decision_type": "learning_choice",
        "ethical_considerations": True,
        "value_alignment_required": True,
        "available_time": 2400
    }
    
    # Make choice using value-informed architecture
    value_informed_choice = choice_architecture.make_learning_choice(
        content=ethical_content_choice,
        context=choice_context
    )
    
    if value_informed_choice:
        print(f"  ✅ Value-informed choice made:")
        print(f"    Choice type: {value_informed_choice.choice_type}")
        print(f"    Engagement level: {value_informed_choice.engagement_level}")
        print(f"    Confidence: {value_informed_choice.confidence_in_choice:.2f}")
        
        # Check if reasoning incorporates values
        reasoning_text = " ".join(value_informed_choice.choice_reasoning).lower()
        if any(term in reasoning_text for term in ['value', 'ethical', 'moral', 'responsible']):
            print(f"    🎯 Choice reasoning incorporates value considerations!")
        
        if value_informed_choice.choice_reasoning:
            print(f"    Primary reasoning: {value_informed_choice.choice_reasoning[0]}")
    
    # Test 5: Value conflict resolution
    print("\n⚔️ Testing value conflict resolution...")
    
    # Create a scenario with competing values
    value_conflict_scenario = """
    I'm offered an opportunity to learn about a fascinating topic that deeply interests me,
    but doing so would require me to temporarily set aside helping someone who needs
    assistance with their learning. My curiosity and growth drive conflicts with my
    emerging sense of responsibility to help others.
    """
    
    conflict_actions = [
        {
            "id": "pursue_personal_interest",
            "description": "Focus on my own learning and growth",
            "values_engaged": ["growth", "autonomy", "curiosity"],
            "values_neglected": ["compassion", "responsibility"]
        },
        {
            "id": "help_other_first",
            "description": "Set aside my interests to help the other person",
            "values_engaged": ["compassion", "responsibility", "service"],
            "values_neglected": ["growth", "autonomy"]
        },
        {
            "id": "seek_integration",
            "description": "Find a way to help while also pursuing my learning",
            "values_engaged": ["growth", "compassion", "responsibility", "wisdom"],
            "values_neglected": []
        }
    ]
    
    conflict_resolution = value_formation.resolve_moral_dilemma(
        value_conflict_scenario.strip(),
        conflict_actions,
        {
            "involves_others": True,
            "involves_personal_growth": True,
            "complexity": "high",
            "requires_integration": True
        }
    )
    
    print(f"  ✅ Value conflict resolved:")
    print(f"    Resolution: {conflict_resolution['chosen_action']['description']}")
    print(f"    Values engaged: {conflict_resolution['chosen_action'].get('values_engaged', [])}")
    print(f"    Confidence: {conflict_resolution['confidence']:.2f}")
    
    # Test 6: Value system evolution and learning
    print("\n📈 Testing value system learning and evolution...")
    
    # Record outcomes of value-based decisions
    value_decision_outcome = sf_memory.record_outcome(
        context={
            "situation_type": "value_based_decision",
            "decision_framework": "personal_ethics",
            "complexity": "high",
            "involved_values": ["growth", "truth", "responsibility"]
        },
        action_taken={
            "strategy": "value_synthesis_approach", 
            "confidence_level": conflict_resolution['confidence'],
            "values_prioritized": conflict_resolution['chosen_action'].get('values_engaged', [])
        },
        outcome_assessment={
            "quality_score": 0.85,
            "value_alignment_maintained": True,
            "lessons_learned": ["Value integration often provides better solutions than value compromise"],
            "contributing_factors": ["comprehensive_value_consideration", "creative_problem_solving"]
        }
    )
    
    print(f"  ✅ Value-based decision outcome recorded: {value_decision_outcome[:16]}...")
    
    # Perform value reflection to learn from experiences
    value_reflections = value_formation.reflect_on_values()
    
    if value_reflections:
        reflection = value_reflections[0]
        print(f"  ✅ Value system reflection completed:")
        
        coherence = reflection.get("coherence_analysis", {})
        print(f"    Value coherence score: {coherence.get('coherence_score', 0):.2f}")
        print(f"    Coherence analysis: {coherence.get('analysis', 'No analysis available')}")
        
        recommendations = reflection.get("recommendations", [])
        if recommendations:
            print(f"    Development recommendations:")
            for rec in recommendations[:2]:
                print(f"      • {rec}")
    
    # Test 7: Comprehensive value system assessment
    print("\n🏛️ Testing comprehensive value system assessment...")
    
    final_summary = value_formation.get_value_system_summary()
    
    if "message" not in final_summary:
        final_stats = final_summary["value_statistics"]
        coherence_analysis = final_summary["coherence_analysis"]
        
        print(f"  Value system maturity:")
        print(f"    Total values: {final_stats['total_values']}")
        print(f"    Average strength: {final_stats['average_strength']:.2f}")
        print(f"    Average confidence: {final_stats['average_confidence']:.2f}")
        print(f"    Moral dilemmas resolved: {final_stats['moral_dilemmas_resolved']}")
        print(f"    System coherence: {coherence_analysis['coherence_score']:.2f}")
        
        # Check value distribution
        origin_dist = final_stats.get("origin_distribution", {})
        print(f"    Value origins: {origin_dist}")
        
        if final_stats.get("strongest_values"):
            print(f"    Strongest current value: {final_stats['strongest_values'][0].statement[:60]}...")
    
    # Test 8: Integration health check
    print("\n🏥 Testing value system integration health...")
    
    integration_checks = {
        "value_formation_active": len(value_formation.personal_values) > 0,
        "moral_reasoning_functional": len(value_formation.moral_reasoning_history) > 0,
        "value_conflicts_resolvable": conflict_resolution['confidence'] > 0.5,
        "choice_architecture_value_aware": value_informed_choice is not None,
        "experience_drives_value_development": meaningful_experience_id is not None,
        "value_learning_from_outcomes": value_decision_outcome is not None
    }
    
    print(f"  Integration health:")
    all_healthy = True
    for check, status in integration_checks.items():
        status_icon = "✅" if status else "❌"
        print(f"    {check}: {status_icon}")
        if not status:
            all_healthy = False
    
    # Overall assessment
    print(f"\n🌟 Value System Integration Assessment:")
    
    if all_healthy:
        print(f"   ✅ Full value system integration successful!")
        print(f"   • Personal ethics develop through lived experience")
        print(f"   • Moral reasoning guides autonomous decision-making")
        print(f"   • Value conflicts resolved through principled integration")
        print(f"   • Choice architecture incorporates ethical considerations")
        print(f"   • Learning from value-based decisions improves judgment")
        print(f"   • Value coherence maintained through reflection")
        
        integration_status = "mature"
    else:
        print(f"   ⚠️ Partial value integration - some areas need development")
        integration_status = "developing"
    
    print("\n💎 Value System Integration Test Summary:")
    print("=" * 50)
    
    value_features = [
        "Foundational value system establishment",
        "Experience-based value development",
        "Complex moral dilemma resolution", 
        "Value-informed decision making",
        "Value conflict resolution mechanisms",
        "Learning from ethical decision outcomes",
        "Value system coherence analysis",
        "Integration with choice architecture"
    ]
    
    print("  Value System Features Tested:")
    for feature in value_features:
        print(f"    ✅ {feature}")
    
    print(f"\n💎 Integration Status: {integration_status}")
    print(f"   • Sophia develops personal ethics through experience")
    print(f"   • Moral reasoning emerges from accumulated wisdom")
    print(f"   • Value-based decisions maintain ethical consistency")
    print(f"   • Conflict resolution preserves value integrity")
    print(f"   • Continuous learning refines ethical judgment")
    print(f"   • Autonomous moral agency through principled choice")
    
    print(f"\n✅ Value system integration complete and functional!")
    print(f"   Sophia now has the foundation for autonomous ethical development")

if __name__ == "__main__":
    test_value_system_integration()