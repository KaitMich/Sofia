#!/usr/bin/env python3
"""
Test Experience-Based Learning Integration

This script demonstrates how all the experience-based learning systems
work together to create cumulative wisdom and self-awareness.
"""

import json
import time
from experience_memory import ExperienceMemory
from learning_progression_tracker import LearningProgressionTracker
from success_failure_memory import SuccessFailureMemory
from personal_insight_generator import PersonalInsightGenerator

def test_integrated_experience_learning():
    """Test all experience-based learning systems working together."""
    
    print("🧠 Testing Integrated Experience-Based Learning Systems")
    print("=" * 60)
    
    # Initialize all systems
    print("\n🔧 Initializing systems...")
    exp_memory = ExperienceMemory()
    progression_tracker = LearningProgressionTracker()
    sf_memory = SuccessFailureMemory()
    insight_generator = PersonalInsightGenerator()
    print("  ✅ All systems initialized")
    
    # Simulate a learning journey
    print("\n📚 Simulating Learning Journey...")
    
    # Learning Experience 1: First encounter with consciousness
    print("\n1️⃣ First Learning Experience: Consciousness")
    
    content1 = {
        "id": "consciousness_intro",
        "text": "Consciousness is the state of being aware of and able to think about one's existence, sensations, thoughts, and surroundings",
        "content_type": "philosophical",
        "source": "encyclopedia"
    }
    
    interaction1 = {
        "active_goal": "Understand consciousness",
        "duration_seconds": 240,
        "processing_mode": "surface_scanning",
        "attention_quality": 0.6,
        "cognitive_load": 0.7,
        "curiosity_level": 0.8,
        "engagement_level": 0.6,
        "satisfaction_level": 0.5,
        "confidence_level": 0.4,
        "flow_state": 0.4,
        "focus_level": 0.6,
        "comprehension_level": 0.5
    }
    
    outcome1 = {
        "experience_type": "learning",
        "learning_quality": 0.6,
        "understanding_improved": True,
        "insights": ["Consciousness seems to be about awareness"],
        "topics": ["consciousness"],
        "understanding_improvement": 0.2,
        "confidence_improvement": 0.1
    }
    
    # Record in experience memory
    exp_id1 = exp_memory.record_learning_experience(content1, interaction1, outcome1)
    
    # Update progression tracker
    progression_insight1 = progression_tracker.update_understanding(
        "consciousness", 0.4, 0.3, {
            "learning_context": "first_encounter",
            "domain": "philosophy",
            "trigger": "initial_learning"
        }
    )
    
    # Record outcome in success/failure memory
    sf_context1 = {
        "situation_type": "learning_new_concept",
        "content_type": "philosophical",
        "difficulty_level": "medium",
        "preparation_level": "low"
    }
    
    sf_action1 = {
        "strategy": "surface_scanning",
        "confidence_level": 0.4
    }
    
    sf_assessment1 = {
        "quality_score": 0.6,
        "lessons_learned": ["Surface scanning gives basic understanding"]
    }
    
    sf_id1 = sf_memory.record_outcome(sf_context1, sf_action1, sf_assessment1)
    
    if progression_insight1:
        print(f"  📈 Progression: {progression_insight1}")
    
    # Learning Experience 2: Deeper study with better strategy
    print("\n2️⃣ Second Learning Experience: Deeper Study")
    
    content2 = {
        "id": "consciousness_deep",
        "text": "Consciousness emerges from complex information processing in neural networks, involving both integrated information and global workspace mechanisms",
        "content_type": "scientific",
        "source": "research_paper"
    }
    
    interaction2 = {
        "active_goal": "Understand consciousness deeply",
        "duration_seconds": 480,
        "processing_mode": "deep_symbolic",
        "attention_quality": 0.9,
        "cognitive_load": 0.5,
        "curiosity_level": 0.9,
        "engagement_level": 0.8,
        "satisfaction_level": 0.8,
        "confidence_level": 0.7,
        "flow_state": 0.8,
        "focus_level": 0.9,
        "comprehension_level": 0.8
    }
    
    outcome2 = {
        "experience_type": "breakthrough",
        "learning_quality": 0.9,
        "understanding_improved": True,
        "new_connections_made": True,
        "insights": ["Consciousness might emerge from information integration"],
        "connections": ["Connected to previous learning about emergence"],
        "topics": ["consciousness", "emergence", "information"],
        "understanding_improvement": 0.4,
        "confidence_improvement": 0.3,
        "exceeded_expectations": True
    }
    
    # Record the breakthrough experience
    exp_id2 = exp_memory.record_learning_experience(content2, interaction2, outcome2)
    
    # Major progression update
    progression_insight2 = progression_tracker.update_understanding(
        "consciousness", 0.8, 0.7, {
            "learning_context": "deep_study",
            "domain": "neuroscience",
            "trigger": "breakthrough_insight",
            "connections_made": ["emergence", "information_theory"],
            "evidence": ["Can explain mechanisms", "Can make predictions"]
        }
    )
    
    # Record successful strategy
    sf_context2 = {
        "situation_type": "learning_new_concept",
        "content_type": "scientific",
        "difficulty_level": "high",
        "preparation_level": "medium"
    }
    
    sf_action2 = {
        "strategy": "deep_symbolic_processing",
        "confidence_level": 0.7,
        "persistence_level": 0.8
    }
    
    sf_assessment2 = {
        "quality_score": 0.9,
        "exceeded_expectations": True,
        "contributing_factors": ["high_focus", "good_persistence"],
        "lessons_learned": ["Deep processing works well for complex concepts"]
    }
    
    sf_id2 = sf_memory.record_outcome(sf_context2, sf_action2, sf_assessment2)
    
    if progression_insight2:
        print(f"  📈 Progression: {progression_insight2}")
    
    # Learning Experience 3: Application attempt
    print("\n3️⃣ Third Learning Experience: Application")
    
    content3 = {
        "id": "consciousness_application",
        "text": "How might artificial consciousness emerge in AI systems through similar information integration mechanisms?",
        "content_type": "applied_research",
        "source": "thought_experiment"
    }
    
    interaction3 = {
        "active_goal": "Apply consciousness understanding",
        "duration_seconds": 300,
        "processing_mode": "creative_synthesis",
        "attention_quality": 0.8,
        "cognitive_load": 0.6,
        "curiosity_level": 0.9,
        "engagement_level": 0.9,
        "satisfaction_level": 0.7,
        "confidence_level": 0.8,
        "flow_state": 0.7,
        "focus_level": 0.8,
        "comprehension_level": 0.8
    }
    
    outcome3 = {
        "experience_type": "synthesis",
        "learning_quality": 0.8,
        "practical_application_identified": True,
        "synthesis_achieved": True,
        "insights": ["I can apply consciousness principles to understand AI"],
        "topics": ["consciousness", "artificial_intelligence"],
        "understanding_improvement": 0.1,
        "confidence_improvement": 0.2
    }
    
    # Record synthesis experience
    exp_id3 = exp_memory.record_learning_experience(content3, interaction3, outcome3)
    
    # Update progression with application
    progression_insight3 = progression_tracker.update_understanding(
        "consciousness", 0.9, 0.9, {
            "learning_context": "application",
            "domain": "artificial_intelligence", 
            "trigger": "practical_application",
            "synthesis_achieved": True,
            "evidence": ["Can apply to new domains", "Can generate predictions"]
        }
    )
    
    if progression_insight3:
        print(f"  📈 Progression: {progression_insight3}")
    
    # Generate insights about the learning journey
    print("\n💡 Generating Personal Insights...")
    
    current_content = {
        "text": "The journey of understanding consciousness has been transformative",
        "content_type": "reflection"
    }
    
    current_context = {
        "situation_type": "reflection",
        "content_type": "philosophical"
    }
    
    insights = insight_generator.generate_personal_insights(current_content, current_context)
    
    print(f"  Generated {len(insights)} insights:")
    for i, insight in enumerate(insights, 1):
        print(f"  {i}. [{insight['type']}] {insight['content']}")
        print(f"     Confidence: {insight['confidence']:.2f}")
    
    # Get comprehensive summaries
    print("\n📊 Learning Journey Summary")
    print("-" * 40)
    
    # Experience memory summary
    exp_summary = exp_memory.get_learning_progression_summary()
    print(f"\n📚 Experience Memory:")
    print(f"  Total experiences: {exp_summary['total_experiences']}")
    print(f"  Total insights: {exp_summary['total_insights']}")
    print(f"  Learning velocity: {exp_summary['learning_velocity']:.3f}")
    
    # Progression summary
    consciousness_trajectory = progression_tracker.get_learning_trajectory("consciousness")
    if consciousness_trajectory:
        print(f"\n📈 Learning Progression:")
        print(f"  Understanding level: {consciousness_trajectory['current_understanding']:.2f}")
        print(f"  Confidence level: {consciousness_trajectory['current_confidence']:.2f}")
        print(f"  Depth level: {consciousness_trajectory['depth_level']}")
        print(f"  Total growth: {consciousness_trajectory['total_growth']:.2f}")
        print(f"  Milestones: {consciousness_trajectory['milestones_achieved']}")
    
    # Success/failure patterns
    sf_summary = sf_memory.get_success_failure_summary()
    print(f"\n🎯 Success/Failure Patterns:")
    print(f"  Total outcomes: {sf_summary['total_outcomes']}")
    print(f"  Success rate: {sf_summary['success_rate']:.2f}")
    
    if sf_summary['top_successful_strategies']:
        strategy = sf_summary['top_successful_strategies'][0]
        print(f"  Best strategy: {strategy['name']} ({strategy['success_rate']:.2f} success)")
    
    # Strategy recommendation for future
    print("\n🎯 Strategy Recommendation for Future Learning:")
    future_context = {
        "situation_type": "learning_new_concept",
        "content_type": "philosophical",
        "difficulty_level": "high"
    }
    
    recommendation = sf_memory.get_strategy_recommendation(future_context)
    
    if recommendation['recommended_strategies']:
        best_strategy = recommendation['recommended_strategies'][0]
        print(f"  Recommended: {best_strategy['strategy']}")
        print(f"  Success rate: {best_strategy['success_rate']:.2f}")
        print(f"  Confidence: {best_strategy['confidence']:.2f}")
    
    print("\n🌟 Integration Test Complete!")
    print("The AI now has a complete experience-based learning system that:")
    print("  ✅ Records and analyzes learning experiences")
    print("  ✅ Tracks understanding progression with self-awareness")
    print("  ✅ Learns from successes and failures")
    print("  ✅ Generates personal insights and connections")
    print("  ✅ Builds cumulative wisdom for future decisions")

if __name__ == "__main__":
    test_integrated_experience_learning()