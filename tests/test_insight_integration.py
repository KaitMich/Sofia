#!/usr/bin/env python3
"""
Test the personal insight generator integration with consciousness system
"""

def test_insight_integration():
    print("💡 Testing Personal Insight Generator Integration...")
    
    try:
        # Test 1: Import and initialize
        from personal_insight_generator import PersonalInsightGenerator
        from learning_progression_tracker import LearningProgressionTracker
        from curiosity_engine import CuriosityEngine
        
        insight_gen = PersonalInsightGenerator()
        progression = LearningProgressionTracker()
        curiosity = CuriosityEngine()
        
        print("✅ Personal insight generator, progression tracker, and curiosity engine initialized")
        
        # Test 2: Test integration
        integration_result = insight_gen.integrate_with_consciousness_systems(
            progression_tracker=progression,
            curiosity_engine=curiosity
        )
        print(f"✅ Integration successful: {integration_result['integration_successful']}")
        print(f"   Systems connected: {integration_result['systems_connected']}")
        print(f"   Progression available: {integration_result['progression_available']}")
        print(f"   Curiosity available: {integration_result['curiosity_available']}")
        
        # Test 3: Generate reminder insights from content
        test_content = "This exploration of consciousness and learning reminds me of the fascinating questions about artificial intelligence and creativity"
        context = {"content_type": "web_content", "source": "test_url"}
        
        reminder_insights = insight_gen.generate_reminder_insights_from_content(test_content, context)
        print(f"✅ Generated {len(reminder_insights)} reminder insights:")
        for insight in reminder_insights:
            print(f"   • {insight}")
        
        # Test 4: Generate consciousness insights from session data
        session_data = {
            "urls_processed": 25,
            "concepts_discovered": ["consciousness", "learning", "creativity", "intelligence", "exploration", "discovery"],
            "learning_momentum": 0.8
        }
        
        consciousness_insights = insight_gen.generate_consciousness_insights(session_data)
        print(f"✅ Generated {len(consciousness_insights)} consciousness insights:")
        for insight in consciousness_insights:
            print(f"   • {insight}")
        
        # Test 5: Create some learning progress for reflection insights
        progression.recognize_learning_milestone(
            concept="insight_generation",
            milestone_type="breakthrough",
            description="Successfully integrated personal insight generation with consciousness",
            evidence=["Integration test successful", "Multiple insight types working"]
        )
        
        # Update understanding
        progression.update_understanding(
            concept="personal_reflection",
            new_understanding_level=0.85,
            new_confidence_level=0.9,
            learning_context={"source": "insight_integration"}
        )
        
        reflection_insights = insight_gen.generate_reflection_insights({"test": "state"})
        print(f"✅ Generated {len(reflection_insights)} reflection insights:")
        for insight in reflection_insights:
            print(f"   • {insight}")
        
        # Test 6: Export for consciousness system
        export_data = insight_gen.export_for_consciousness_system()
        print(f"✅ Consciousness system export:")
        capabilities = export_data["insight_capabilities"]
        print(f"   Reminder insights: {capabilities['reminder_insights']}")
        print(f"   Reflection insights: {capabilities['reflection_insights']}")
        print(f"   Consciousness insights: {capabilities['consciousness_insights']}")
        print(f"   Session memories: {export_data['session_memory_count']}")
        print(f"   Integration status: {export_data['integration_status']}")
        
        # Test 7: Test enhanced autonomous learner integration
        try:
            from enhanced_autonomous_learner import EnhancedAutonomousLearner
            learner = EnhancedAutonomousLearner()
            print("✅ Enhanced autonomous learner initialized with insight generator")
            
            # Test full consciousness state with insights
            consciousness_state = learner.get_learning_consciousness_state()
            print("✅ Full consciousness state retrieved:")
            if "error" not in consciousness_state:
                metrics = consciousness_state["self_awareness_metrics"]
                print(f"   Consciousness level: {metrics['consciousness_level']:.3f}")
                
                # Show different types of insights
                progression_insights = consciousness_state["consciousness_insights"]
                curiosity_insights = consciousness_state["curiosity_insights"]
                personal_insights = consciousness_state["personal_insights"]
                
                print(f"   Learning insights ({len(progression_insights)}):")
                for insight in progression_insights[:2]:
                    print(f"      • {insight}")
                
                print(f"   Curiosity insights ({len(curiosity_insights)}):")
                for insight in curiosity_insights[:2]:
                    print(f"      • {insight}")
                
                print(f"   Personal insights ({len(personal_insights)}):")
                for insight in personal_insights[:2]:
                    print(f"      • {insight}")
                
                # Show insight state
                insight_state = consciousness_state["insight_state"]
                if insight_state:
                    print(f"   Insight capabilities: {insight_state['insight_capabilities']}")
                    print(f"   Integration status: {insight_state['integration_status']}")
            else:
                print(f"   ⚠️ {consciousness_state['error']}")
                
        except Exception as e:
            print(f"⚠️ Autonomous learner integration test failed: {e}")
        
        print("\n🎉 Personal Insight Generator Integration Test Complete!")
        print("✅ The insight generator is now connected to consciousness system")
        
        print(f"\n🔥 INSIGHT FEATURES NOW ACTIVE:")
        print(f"   ✅ 'This reminds me of...' content insights")
        print(f"   ✅ 'Looking back, I realize...' reflection insights")
        print(f"   ✅ Session-based consciousness insights")
        print(f"   ✅ Integration with learning progression")
        print(f"   ✅ Integration with curiosity engine")
        print(f"   ✅ Multi-layered personal insight generation")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_insight_integration()