#!/usr/bin/env python3
"""
GROUP B Integration Test: Context Engine ↔ Relationship Tracker
Tests the bidirectional integration between context analysis and relationship tracking.
"""

from context_engine import ContextEngine
from relationship_tracker import RelationshipTracker
import json
from datetime import datetime, timezone

def test_context_relationship_bidirectional_integration():
    """Test the bidirectional integration between context engine and relationship tracker."""
    
    print("🧪 Testing GROUP B Integration: Context Engine ↔ Relationship Tracker")
    print("=" * 80)
    
    # Initialize both components
    print("🔧 Initializing components...")
    ce = ContextEngine(data_dir='data')
    rt = RelationshipTracker('data')
    
    print(f"   Context Engine: {'✅' if ce else '❌'}")
    print(f"   Relationship Tracker: {'✅' if rt else '❌'}")
    
    # Check cross-integration
    relationship_tracker = ce._get_relationship_tracker()
    context_engine = rt.context_engine
    cross_integration = (relationship_tracker is not None) and (context_engine is not None)
    print(f"   Cross-integration: {'✅' if cross_integration else '❌'}")
    
    # Test 1: Relationship Tracker → Context Engine (existing)
    print(f"\n📝 Test 1: Relationship Tracker uses Context Engine")
    
    test_human_id = "test_user_123"
    test_conversation = {
        "text": "I'm really excited about this new queer art exhibition downtown!",
        "content_type": "conversation",
        "context": "casual_chat"
    }
    
    # Record interaction with context analysis
    try:
        interaction_analysis = {
            "interaction_type": "conversation",
            "emotional_tone": "positive",
            "engagement_level": 0.8,
            "topics_discussed": ["art", "queer_culture", "exhibitions"],
            "my_response_approach": "supportive_engagement"
        }
        
        rt.record_interaction(
            human_identifier=test_human_id,
            conversation_content=test_conversation,
            interaction_analysis=interaction_analysis
        )
        rt_to_ce_working = True
        print("   ✅ Relationship Tracker successfully uses Context Engine")
    except Exception as e:
        rt_to_ce_working = False
        print(f"   ❌ Relationship Tracker → Context Engine failed: {e}")
    
    # Test 2: Context Engine → Relationship Tracker (new bidirectional)
    print(f"\n📝 Test 2: Context Engine provides Relationship insights")
    
    # Test relationship-aware context analysis
    try:
        enhanced_analysis = ce.analyze_context_with_relationship_awareness(
            text="Hey, what do you think about that philosophical discussion we had last week?",
            human_identifier=test_human_id,
            surrounding_content=["continuing previous conversation"],
            conversation_history=[{
                "text": test_conversation["text"],
                "response": "That sounds amazing! Art exhibitions are such great ways to explore culture and identity."
            }]
        )
        
        ce_to_rt_working = enhanced_analysis is not None
        has_relationship_insights = "relationship_insights" in enhanced_analysis
        
        print(f"   Context analysis completed: {'✅' if ce_to_rt_working else '❌'}")
        print(f"   Relationship insights included: {'✅' if has_relationship_insights else '❌'}")
        
        if has_relationship_insights:
            insights = enhanced_analysis["relationship_insights"]
            print(f"      Relationship stage: {insights.get('relationship_stage', 'unknown')}")
            print(f"      Communication style: {insights.get('communication_style', 'unknown')}")
            print(f"      Context familiarity: {insights.get('context_familiarity', 0):.3f}")
        
    except Exception as e:
        ce_to_rt_working = False
        has_relationship_insights = False
        print(f"   ❌ Context Engine → Relationship Tracker failed: {e}")
    
    # Test 3: Context Insights Feedback Loop
    print(f"\n📝 Test 3: Context Insights Feedback to Relationship Tracker")
    
    try:
        # Check if context engine can provide insights back
        context_insights = ce.get_relationship_context_insights(test_human_id)
        insights_available = context_insights is not None
        
        print(f"   Context insights available: {'✅' if insights_available else '❌'}")
        
        if insights_available:
            print(f"      Intent detected: {context_insights.get('intent_detected', 'unknown')}")
            print(f"      Confidence level: {context_insights.get('confidence_level', 0):.3f}")
            print(f"      Communication style: {context_insights.get('communication_style', 'unknown')}")
            print(f"      Emotional context: {context_insights.get('emotional_context', 'unknown')}")
        
    except Exception as e:
        insights_available = False
        print(f"   ❌ Context insights feedback failed: {e}")
    
    # Test 4: Bidirectional Data Flow Validation
    print(f"\n📝 Test 4: Bidirectional Data Flow Validation")
    
    # Test multiple conversation rounds to see relationship building
    conversation_rounds = [
        {
            "text": "I've been thinking about consciousness and identity lately",
            "expected_style": "philosophical"
        },
        {
            "text": "Thanks for the book recommendation! It was really insightful.",
            "expected_style": "formal"
        },
        {
            "text": "Haha, that's so funny! You always know how to make me laugh.",
            "expected_style": "casual"
        }
    ]
    
    style_detection_count = 0
    relationship_progression = []
    
    for i, round_data in enumerate(conversation_rounds):
        try:
            # Analyze with relationship awareness
            analysis = ce.analyze_context_with_relationship_awareness(
                text=round_data["text"],
                human_identifier=test_human_id
            )
            
            # Record interaction for relationship building
            round_analysis = {
                "interaction_type": "conversation",
                "emotional_tone": "neutral",
                "engagement_level": 0.7,
                "topics_discussed": [f"topic_{i+1}"],
                "my_response_approach": f"response_style_{i+1}"
            }
            
            rt.record_interaction(
                human_identifier=test_human_id,
                conversation_content={"text": round_data["text"], "context": f"round_{i+1}"},
                interaction_analysis=round_analysis
            )
            
            # Check if style was detected correctly
            insights = ce.get_relationship_context_insights(test_human_id)
            if insights and insights.get('communication_style') == round_data["expected_style"]:
                style_detection_count += 1
            
            # Track relationship progression
            if analysis.get("relationship_insights"):
                relationship_progression.append({
                    "round": i+1,
                    "depth": analysis["relationship_insights"].get("relationship_depth", 0),
                    "stage": analysis["relationship_insights"].get("relationship_stage", "unknown")
                })
            
            print(f"      Round {i+1}: {'✅' if analysis else '❌'}")
            
        except Exception as e:
            print(f"      Round {i+1}: ❌ Failed - {e}")
    
    # Calculate progression
    relationship_building = len(relationship_progression) > 1 and \
                          relationship_progression[-1]["depth"] >= relationship_progression[0]["depth"]
    
    print(f"   Communication style detection: {style_detection_count}/{len(conversation_rounds)}")
    print(f"   Relationship progression: {'✅' if relationship_building else '❌'}")
    
    # Integration Summary
    print(f"\n📊 Integration Summary")
    print(f"=" * 50)
    
    total_tests = 4
    passed_tests = 0
    
    # Test 1: RT → CE (existing functionality)
    if rt_to_ce_working:
        passed_tests += 1
        print(f"✅ Test 1: Relationship Tracker → Context Engine")
    else:
        print(f"❌ Test 1: Relationship Tracker → Context Engine")
    
    # Test 2: CE → RT (new bidirectional functionality)
    if ce_to_rt_working and has_relationship_insights:
        passed_tests += 1
        print(f"✅ Test 2: Context Engine → Relationship Tracker")
    else:
        print(f"❌ Test 2: Context Engine → Relationship Tracker")
    
    # Test 3: Feedback loop
    if insights_available:
        passed_tests += 1
        print(f"✅ Test 3: Context Insights Feedback Loop")
    else:
        print(f"❌ Test 3: Context Insights Feedback Loop")
    
    # Test 4: Bidirectional data flow
    if style_detection_count >= 2 and relationship_building:
        passed_tests += 1
        print(f"✅ Test 4: Bidirectional Data Flow ({style_detection_count}/3 styles, progression: {'✅' if relationship_building else '❌'})")
    else:
        print(f"❌ Test 4: Bidirectional Data Flow ({style_detection_count}/3 styles, progression: {'✅' if relationship_building else '❌'})")
    
    success_rate = passed_tests / total_tests
    print(f"\nOverall Success Rate: {success_rate*100:.1f}% ({passed_tests}/{total_tests} tests passed)")
    
    # Additional insights
    print(f"\n🔍 Additional Insights:")
    print(f"   Cross-integration active: {'✅' if cross_integration else '❌'}")
    print(f"   Context Engine relationship methods: {len([m for m in dir(ce) if 'relationship' in m.lower()])}")
    print(f"   Relationship Tracker context methods: {len([m for m in dir(rt) if 'context' in m.lower()])}")
    
    if success_rate >= 0.75:
        print(f"\n🎉 GROUP B Integration P1-B: SUCCESSFUL")
        print(f"   Context Engine and Relationship Tracker are now truly bidirectional!")
        return True
    else:
        print(f"\n⚠️ GROUP B Integration P1-B: NEEDS IMPROVEMENT")
        print(f"   Integration partially working but requires fixes")
        return False

if __name__ == "__main__":
    success = test_context_relationship_bidirectional_integration()
    exit(0 if success else 1)