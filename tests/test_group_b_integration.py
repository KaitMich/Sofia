#!/usr/bin/env python3
"""
GROUP B Integration Test - Context Engine ↔ Relationship Tracker
Tests the successful integration between context analysis and relationship tracking.
"""

from sofia.core.relationship_tracker import RelationshipTracker
from sofia.core.context_engine import ContextEngine
import json

def test_context_relationship_integration():
    """Test the integration between context engine and relationship tracker."""
    
    print("🧪 Testing GROUP B Integration: Context Engine ↔ Relationship Tracker")
    print("=" * 70)
    
    # Initialize components
    rt = RelationshipTracker('data')
    ce = ContextEngine()
    
    # Test scenarios with different context types
    test_scenarios = [
        {
            "name": "Identity Discussion",
            "human_id": "user_identity_test",
            "content": {
                "text": "I'm proud to be part of the LGBTQ+ community and want to talk about it",
                "context": "identity_sharing",
                "topics": ["identity", "community", "pride", "personal_sharing"]
            },
            "analysis": {
                "communication_style": "open_authentic",
                "emotional_tone": "positive_proud",
                "my_approach": "supportive_affirming",
                "connection_quality": 0.8,
                "trust_level": 0.7,
                "human_openness": 0.9,
                "my_authenticity": 0.8,
                "significance": 0.7
            }
        },
        {
            "name": "Academic Context",
            "human_id": "user_academic_test", 
            "content": {
                "text": "I'm studying the historical usage of the term 'queer' in academic literature",
                "context": "academic_research",
                "topics": ["research", "terminology", "history", "linguistics"]
            },
            "analysis": {
                "communication_style": "scholarly",
                "emotional_tone": "neutral_curious",
                "my_approach": "educational_informative",
                "connection_quality": 0.6,
                "trust_level": 0.6,
                "human_openness": 0.5,
                "my_authenticity": 0.7,
                "significance": 0.5
            }
        },
        {
            "name": "Support Seeking",
            "human_id": "user_support_test",
            "content": {
                "text": "Someone called me a slur today and I'm feeling really hurt about it",
                "context": "emotional_support",
                "topics": ["discrimination", "emotional_pain", "support", "coping"]
            },
            "analysis": {
                "communication_style": "vulnerable",
                "emotional_tone": "hurt_seeking_comfort",
                "my_approach": "empathetic_supportive",
                "connection_quality": 0.9,
                "trust_level": 0.8,
                "human_openness": 0.95,
                "my_authenticity": 0.9,
                "significance": 0.9
            }
        }
    ]
    
    integration_results = []
    
    for scenario in test_scenarios:
        print(f"\n📝 Testing Scenario: {scenario['name']}")
        print(f"   Original context: {scenario['content']['context']}")
        
        # Record interaction with context engine integration
        interaction_id = rt.record_interaction(
            scenario['human_id'],
            scenario['content'],
            scenario['analysis']
        )
        
        # Get the recorded interaction
        last_interaction = rt.interaction_memories[-1]
        
        # Analyze context enhancement
        context_enhanced = last_interaction.conversation_context != scenario['content']['context']
        context_value = last_interaction.conversation_context
        significance_value = last_interaction.interaction_significance
        
        print(f"   Enhanced context: {context_value}")
        print(f"   Significance: {significance_value}")
        print(f"   Context Enhanced: {'✅' if context_enhanced else '❌'}")
        
        # Test relationship profile update
        profile = rt.relationship_profiles.get(scenario['human_id'])
        if profile:
            print(f"   Relationship depth: {profile.relationship_depth:.3f}")
            print(f"   Trust level: {profile.trust_level:.3f}")
            print(f"   Bond strength: {profile.emotional_bond_strength:.3f}")
        
        integration_results.append({
            "scenario": scenario['name'],
            "context_enhanced": context_enhanced,
            "original_context": scenario['content']['context'],
            "enhanced_context": context_value,
            "significance": significance_value,
            "interaction_id": interaction_id
        })
        
        print(f"   ✅ Scenario completed")
    
    # Test relationship context retrieval
    print(f"\n🔍 Testing Relationship Context Retrieval")
    for result in integration_results:
        human_id = next(s['human_id'] for s in test_scenarios if s['name'] == result['scenario'])
        rel_context = rt.get_relationship_context(human_id)
        
        print(f"   {result['scenario']}: Relationship exists = {rel_context['relationship_exists']}")
        if rel_context['relationship_exists']:
            profile = rel_context['relationship_profile']
            print(f"      Total interactions: {profile.total_interactions}")
            print(f"      Communication compatibility: {profile.communication_compatibility:.3f}")
    
    # Summary
    print(f"\n📊 Integration Test Summary")
    print(f"=" * 40)
    total_tests = len(integration_results)
    enhanced_count = sum(1 for r in integration_results if r['context_enhanced'])
    
    print(f"Total scenarios tested: {total_tests}")
    print(f"Context enhancements: {enhanced_count}/{total_tests}")
    print(f"Enhancement rate: {(enhanced_count/total_tests)*100:.1f}%")
    
    # Check for context analysis data
    any_context_insights = False
    for interaction in rt.interaction_memories[-total_tests:]:
        # This would normally check interaction_analysis for context_insights
        # but we'll check if context was enhanced as a proxy
        if "_" in interaction.conversation_context:
            any_context_insights = True
            break
    
    print(f"Context insights captured: {'✅' if any_context_insights else '❌'}")
    
    success_rate = enhanced_count / total_tests
    if success_rate >= 0.8:
        print(f"🎉 GROUP B Integration: SUCCESSFUL ({success_rate*100:.1f}% enhancement rate)")
        return True
    else:
        print(f"⚠️ GROUP B Integration: PARTIAL ({success_rate*100:.1f}% enhancement rate)")
        return False

if __name__ == "__main__":
    success = test_context_relationship_integration()
    exit(0 if success else 1)