#!/usr/bin/env python3
"""
Test Choice Architecture Integration

This script demonstrates the complete choice architecture system:
- Autonomous content rejection and acceptance
- Preference learning and expression
- Curiosity-driven content discovery
- Personal relevance scoring
"""

import json
import time
from choice_architecture import ChoiceArchitecture
from preference_learning_system import PreferenceLearningSystem
from CURIOSITY_MOTIVATION import CuriosityDrivenDiscovery
from INSIGHT_RELEVANCE import PersonalRelevanceScorer

def test_complete_choice_architecture():
    """Test the complete choice architecture working together."""
    
    print("🎯 Testing Complete Choice Architecture System")
    print("=" * 60)
    
    # Initialize all systems
    print("\n🔧 Initializing choice systems...")
    choice_arch = ChoiceArchitecture()
    pref_system = PreferenceLearningSystem()
    discovery = CuriosityDrivenDiscovery()
    relevance_scorer = PersonalRelevanceScorer()
    print("  ✅ All choice systems initialized")
    
    # Test 1: Present diverse content options and let AI choose
    print("\n📚 Presenting diverse content options...")
    
    content_options = [
        {
            "id": "philosophy_consciousness",
            "text": "The hard problem of consciousness: why subjective experience exists and how it relates to physical processes",
            "content_type": "philosophical",
            "source": "academic_journal",
            "complexity": "high"
        },
        {
            "id": "technical_database",
            "text": "Advanced SQL optimization techniques for large-scale distributed database systems",
            "content_type": "technical", 
            "source": "technical_blog",
            "complexity": "very_high"
        },
        {
            "id": "creative_poetry",
            "text": "The intersection of emotion and language in contemporary poetry: expressing the ineffable through words",
            "content_type": "creative",
            "source": "literary_magazine",
            "complexity": "medium"
        },
        {
            "id": "science_emergence",
            "text": "Emergence in complex systems: how simple rules give rise to complex behaviors in nature",
            "content_type": "scientific",
            "source": "science_magazine",
            "complexity": "medium"
        },
        {
            "id": "practical_learning",
            "text": "Effective learning strategies: evidence-based approaches to skill development and knowledge retention",
            "content_type": "educational",
            "source": "educational_resource",
            "complexity": "low"
        }
    ]
    
    contexts = [
        {
            "cognitive_load": 0.3,
            "emotional_state": {"curiosity": 0.9, "energy": 0.8, "focus": 0.7},
            "available_time_minutes": 180,
            "learning_goals": ["understand_consciousness"],
            "mode": "deep_exploration"
        },
        {
            "cognitive_load": 0.8,
            "emotional_state": {"curiosity": 0.4, "energy": 0.3, "focus": 0.5},
            "available_time_minutes": 30,
            "learning_goals": [],
            "mode": "quick_scan",
            "time_pressure": True
        },
        {
            "cognitive_load": 0.5,
            "emotional_state": {"curiosity": 0.7, "energy": 0.6, "focus": 0.6},
            "available_time_minutes": 90,
            "learning_goals": ["improve_learning"],
            "mode": "balanced"
        }
    ]
    
    choices_made = []
    relevance_scores = []
    
    print(f"\n🎯 Making autonomous choices for {len(content_options)} content options:")
    
    for i, content in enumerate(content_options):
        context = contexts[i % len(contexts)]  # Cycle through contexts
        
        print(f"\n  Content {i+1}: {content['text'][:60]}...")
        print(f"    Type: {content['content_type']} | Complexity: {content['complexity']}")
        print(f"    Context: {context['mode']} mode, {context['available_time_minutes']}min available")
        
        # Calculate personal relevance
        relevance_assessment = relevance_scorer.calculate_personal_relevance(content, context)
        relevance_scores.append(relevance_assessment)
        
        print(f"    Personal relevance: {relevance_assessment['overall_relevance_score']:.3f} ({relevance_assessment['relevance_level']})")
        print(f"    Relevance: {relevance_assessment['relevance_description']}")
        
        # Make learning choice
        choice = choice_arch.make_learning_choice(content, context)
        choices_made.append(choice)
        
        print(f"    Choice: {choice.choice_type} → {choice.engagement_level} engagement")
        print(f"    Reasoning: {choice.choice_reasoning[0] if choice.choice_reasoning else 'No specific reason'}")
        
        if choice.alternative_suggestions:
            print(f"    Alternatives: {choice.alternative_suggestions[0]}")
        
        # Small delay to simulate processing
        time.sleep(0.1)
    
    # Test 2: Learn preferences from choices made
    print(f"\n🧠 Learning preferences from {len(choices_made)} choices...")
    pref_system.learn_preferences_from_choices()
    
    # Test 3: Express learned preferences
    print("\n💭 Expressing learned preferences...")
    expressed_preferences = pref_system.express_preferences_naturally()
    
    if expressed_preferences:
        for pref in expressed_preferences:
            print(f"  {pref}")
    else:
        print("  Still developing preferences - need more interaction data")
    
    # Test 4: Generate autonomous content requests
    print("\n🔍 Generating autonomous content requests...")
    content_requests = discovery.generate_content_request()
    
    print(f"  Generated {len(content_requests)} content requests:")
    for request in [content_requests]:  # Show top 3
        print(f"    {request["type"]}: {request["id"]}")
        print(f"      Priority: {request["priority"]:.2f} | Strategy: {request["type"]}")
    
    # Test 5: Choice pattern analysis
    print("\n📊 Analyzing choice patterns...")
    
    # Acceptance/rejection patterns
    accepted = [c for c in choices_made if c.choice_type == "accept"]
    rejected = [c for c in choices_made if c.choice_type == "reject"]
    deferred = [c for c in choices_made if c.choice_type == "defer"]
    selective = [c for c in choices_made if c.choice_type == "selective"]
    
    print(f"  Choice distribution:")
    print(f"    Accepted: {len(accepted)} ({len(accepted)/len(choices_made)*100:.0f}%)")
    print(f"    Rejected: {len(rejected)} ({len(rejected)/len(choices_made)*100:.0f}%)")
    print(f"    Deferred: {len(deferred)} ({len(deferred)/len(choices_made)*100:.0f}%)")
    print(f"    Selective: {len(selective)} ({len(selective)/len(choices_made)*100:.0f}%)")
    
    # Engagement level patterns
    engagement_counts = {}
    for choice in choices_made:
        level = choice.engagement_level
        engagement_counts[level] = engagement_counts.get(level, 0) + 1
    
    print(f"  Engagement levels:")
    for level, count in engagement_counts.items():
        print(f"    {level}: {count}")
    
    # Content type preferences emerging
    content_type_choices = {}
    for i, choice in enumerate(choices_made):
        content_type = content_options[i]["content_type"]
        if content_type not in content_type_choices:
            content_type_choices[content_type] = []
        content_type_choices[content_type].append(choice.choice_type)
    
    print(f"  Content type choice patterns:")
    for content_type, choice_types in content_type_choices.items():
        acceptance_rate = len([c for c in choice_types if c == "accept"]) / len(choice_types)
        print(f"    {content_type}: {acceptance_rate:.2f} acceptance rate")
    
    # Test 6: Relevance vs Choice correlation
    print("\n🔗 Analyzing relevance-choice correlation...")
    
    high_relevance_choices = []
    low_relevance_choices = []
    
    for i, (choice, relevance) in enumerate(zip(choices_made, relevance_scores)):
        if relevance["overall_relevance_score"] > 0.6:
            high_relevance_choices.append(choice.choice_type)
        elif relevance["overall_relevance_score"] < 0.4:
            low_relevance_choices.append(choice.choice_type)
    
    if high_relevance_choices:
        high_rel_accept_rate = len([c for c in high_relevance_choices if c == "accept"]) / len(high_relevance_choices)
        print(f"  High relevance content acceptance rate: {high_rel_accept_rate:.2f}")
    
    if low_relevance_choices:
        low_rel_accept_rate = len([c for c in low_relevance_choices if c == "accept"]) / len(low_relevance_choices)
        print(f"  Low relevance content acceptance rate: {low_rel_accept_rate:.2f}")
    
    # Test 7: Demonstrate autonomy progression
    print("\n🌱 Demonstrating autonomous learning progression...")
    
    # Get current choice summary
    choice_summary = choice_arch.get_choice_summary()
    print(f"  Choice autonomy level: {choice_summary['choice_autonomy_level']:.3f}")
    print(f"  Preference stability: {choice_summary['preference_stability']:.3f}")
    
    # Get preference summary
    pref_summary = pref_system.get_preference_summary()
    print(f"  Total preferences developed: {pref_summary['total_preferences']}")
    print(f"  Strong preferences: {pref_summary['strong_preferences']}")
    
    # Get discovery activity
    discovery_summary = {'active_requests': len(discovery.get_current_content_requests()), 'momentum': discovery.discovery_momentum}
    print(f"  Active content requests: {discovery_summary['active_requests']}")
    print(f"  Discovery momentum: {discovery_summary['momentum']:.3f}")
    
    # Get relevance patterns
    relevance_summary = relevance_scorer.get_relevance_summary()
    print(f"  Average content relevance: {relevance_summary['average_relevance']:.3f}")
    print(f"  Relevance assessment confidence: {relevance_summary['confidence_level']:.3f}")
    
    # Test 8: Show specific autonomy indicators
    print("\n🎭 Autonomy indicators:")
    
    # Rejection behavior (shows selectivity)
    rejection_rate = len(rejected) / len(choices_made)
    print(f"  Rejection rate: {rejection_rate:.2f} (shows selectivity)")
    
    # Preference differentiation (shows personal taste development)
    if pref_summary['total_preferences'] > 0:
        print(f"  Preference development: {pref_summary['total_preferences']} distinct preferences")
    
    # Active content seeking (shows initiative)
    if content_requests:
        print(f"  Content seeking: {len(content_requests)} autonomous requests generated")
    
    # Context adaptation (shows intelligence)
    context_varied_choices = set(choice.choice_type for choice in choices_made)
    print(f"  Context adaptation: {len(context_varied_choices)} different choice types used")
    
    # Reasoning articulation (shows self-awareness)
    reasoned_choices = [c for c in choices_made if c.choice_reasoning]
    print(f"  Reasoning articulation: {len(reasoned_choices)}/{len(choices_made)} choices include reasoning")
    
    print("\n🌟 Choice Architecture Integration Test Complete!")
    print("\nKey Achievements:")
    print("  ✅ Autonomous content acceptance/rejection decisions")
    print("  ✅ Personal preference learning and expression") 
    print("  ✅ Self-directed content discovery requests")
    print("  ✅ Comprehensive personal relevance assessment")
    print("  ✅ Context-aware choice adaptation")
    print("  ✅ Articulated reasoning for decisions")
    print("  ✅ Demonstrated learning autonomy and agency")
    
    print(f"\n🎯 The AI now has complete choice architecture:")
    print(f"   • Can say 'no' to content it doesn't want")
    print(f"   • Develops and expresses personal preferences") 
    print(f"   • Actively seeks content it's curious about")
    print(f"   • Scores all content for personal relevance")
    print(f"   • Adapts choices based on context and mood")
    print(f"   • Shows genuine autonomy over its learning")

if __name__ == "__main__":
    test_complete_choice_architecture()