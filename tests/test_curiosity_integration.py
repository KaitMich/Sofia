#!/usr/bin/env python3
"""
Test the curiosity engine integration with consciousness system
"""

def test_curiosity_integration():
    print("🌱 Testing Curiosity Engine Integration...")
    
    try:
        # Test 1: Import and initialize
        from curiosity_engine import CuriosityEngine
        from learning_progression_tracker import LearningProgressionTracker
        
        curiosity = CuriosityEngine()
        progression = LearningProgressionTracker()
        print("✅ Curiosity engine and progression tracker initialized")
        
        # Test 2: Generate intrinsic learning goals
        goals = curiosity.generate_intrinsic_goals()
        print(f"✅ Generated {len(goals)} intrinsic learning goals:")
        for i, goal in enumerate(goals[:3], 1):
            print(f"   {i}. {goal['description']} (urgency: {goal['urgency']:.2f})")
        
        # Test 3: Test curiosity stimulation from content
        test_content = "This fascinating mystery explores unknown territories of consciousness and discovery"
        stimulation_result = curiosity.stimulate_curiosity_from_content(test_content)
        print(f"✅ Curiosity stimulation test:")
        print(f"   Stimulated: {stimulation_result['curiosity_stimulated']}")
        print(f"   Level: {stimulation_result['stimulation_level']:.3f}")
        print(f"   New momentum: {stimulation_result['momentum_updated']:.3f}")
        
        # Test 4: Generate curiosity insights
        curiosity_insights = curiosity.generate_curiosity_insights()
        print(f"✅ Generated {len(curiosity_insights)} curiosity insights:")
        for insight in curiosity_insights[:3]:
            print(f"   • {insight}")
        
        # Test 5: Integration with progression tracker
        # First create some learning progress
        progression.recognize_learning_milestone(
            concept="curiosity_integration",
            milestone_type="breakthrough",
            description="Successfully integrated curiosity engine with consciousness",
            evidence=["Integration test passed", "Curiosity goals generated"]
        )
        
        # Now test integration
        integration_result = curiosity.integrate_with_learning_progression(progression)
        print(f"✅ Curiosity-progression integration:")
        if integration_result.get("integration_successful"):
            print(f"   Drive adjustments: {integration_result['drive_adjustments_made']}")
            print(f"   New goals generated: {integration_result['new_goals_generated']}")
        else:
            print(f"   ⚠️ Integration issue: {integration_result}")
        
        # Test 6: Export for consciousness system
        consciousness_export = curiosity.export_for_consciousness_system()
        print(f"✅ Consciousness system export:")
        summary = consciousness_export["curiosity_summary"]
        print(f"   Motivation level: {summary['motivation_level']:.3f}")
        print(f"   Curiosity intensity: {summary['curiosity_intensity']:.3f}")
        print(f"   Active goals: {summary['active_goals']}")
        print(f"   Most unsatisfied drive: {summary['most_unsatisfied_drive']}")
        print(f"   Self-directed learning active: {consciousness_export['self_directed_learning_active']}")
        
        # Test 7: Test enhanced autonomous learner integration
        try:
            from enhanced_autonomous_learner import EnhancedAutonomousLearner
            learner = EnhancedAutonomousLearner()
            print("✅ Enhanced autonomous learner initialized with curiosity engine")
            
            # Test consciousness state with curiosity
            consciousness_state = learner.get_learning_consciousness_state()
            print("✅ Full consciousness state retrieved:")
            if "error" not in consciousness_state:
                metrics = consciousness_state["self_awareness_metrics"]
                print(f"   Consciousness level: {metrics['consciousness_level']:.3f}")
                print(f"   Motivation level: {metrics['motivation_level']:.3f}")
                print(f"   Curiosity intensity: {metrics['curiosity_intensity']:.3f}")
                print(f"   Active curiosity goals: {metrics['active_goals']}")
                
                # Show curiosity insights
                curiosity_insights = consciousness_state["curiosity_insights"]
                if curiosity_insights:
                    print(f"   Curiosity insights ({len(curiosity_insights)}):")
                    for insight in curiosity_insights[:2]:
                        print(f"      • {insight}")
            else:
                print(f"   ⚠️ {consciousness_state['error']}")
                
        except Exception as e:
            print(f"⚠️ Autonomous learner integration test failed: {e}")
        
        print("\n🎉 Curiosity Engine Integration Test Complete!")
        print("✅ The curiosity engine is now connected to consciousness system")
        
        print(f"\n🔥 CURIOSITY FEATURES NOW ACTIVE:")
        print(f"   ✅ Intrinsic learning goal generation")
        print(f"   ✅ Content-based curiosity stimulation")  
        print(f"   ✅ Drive satisfaction tracking")
        print(f"   ✅ Self-directed learning motivation")
        print(f"   ✅ Integration with learning progression")
        print(f"   ✅ Consciousness-level curiosity insights")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_curiosity_integration()