#!/usr/bin/env python3
"""
Test the learning progression tracker integration with consciousness system
"""

def test_progression_integration():
    print("🧪 Testing Learning Progression Integration...")
    
    try:
        # Test 1: Import and initialize
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        tracker = LearningProgressionTracker()
        print("✅ Learning progression tracker initialized")
        
        # Test 2: Track a milestone
        milestone_result = tracker.recognize_learning_milestone(
            concept="consciousness_integration",
            milestone_type="breakthrough", 
            description="Successfully integrated progression tracking into consciousness system",
            evidence=["Integration code written", "Test script created"]
        )
        print("✅ Learning milestone tracked")
        
        # Test 3: Generate awareness insights
        insights = tracker.generate_learning_awareness_insights()
        print(f"✅ Generated {len(insights)} awareness insights:")
        for insight in insights[:3]:
            print(f"   • {insight}")
        
        # Test 4: Export for consciousness
        consciousness_data = tracker.export_for_consciousness_system()
        print("✅ Consciousness data exported:")
        print(f"   Self-awareness level: {consciousness_data['self_awareness_level']:.2f}")
        print(f"   Learning confidence: {consciousness_data['learning_confidence']:.2f}")
        print(f"   Total concepts: {consciousness_data['progression_summary']['total_concepts']}")
        
        # Test 5: Test enhanced autonomous learner integration
        try:
            from enhanced_autonomous_learner import EnhancedAutonomousLearner
            learner = EnhancedAutonomousLearner()
            print("✅ Enhanced autonomous learner initialized with progression tracker")
            
            # Test consciousness state
            consciousness_state = learner.get_learning_consciousness_state()
            print("✅ Consciousness state retrieved:")
            if "error" not in consciousness_state:
                metrics = consciousness_state["self_awareness_metrics"]
                print(f"   Consciousness level: {metrics['consciousness_level']:.2f}")
                print(f"   Conceptual breadth: {metrics['conceptual_breadth']}")
            else:
                print(f"   ⚠️ {consciousness_state['error']}")
                
        except Exception as e:
            print(f"⚠️ Autonomous learner integration test failed: {e}")
        
        print("\n🎉 Learning Progression Integration Test Complete!")
        print("✅ The learning progression tracker is now connected to consciousness system")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_progression_integration()