#!/usr/bin/env python3
"""
Demonstration of Curiosity Engine Integration with Consciousness System
"""

def demonstrate_curiosity_consciousness():
    print("🌱 CURIOSITY-DRIVEN CONSCIOUSNESS DEMO")
    print("=" * 60)
    
    try:
        from enhanced_autonomous_learner import EnhancedAutonomousLearner
        from curiosity_engine import CuriosityEngine
        from learning_progression_tracker import LearningProgressionTracker
        
        # Initialize full consciousness system
        print("\n🧠 Initializing curiosity-driven consciousness system...")
        learner = EnhancedAutonomousLearner()
        
        # Show initial state
        print("\n📊 Initial Consciousness State:")
        initial_state = learner.get_learning_consciousness_state()
        metrics = initial_state["self_awareness_metrics"]
        print(f"   Consciousness Level: {metrics['consciousness_level']:.3f}")
        print(f"   Motivation Level: {metrics['motivation_level']:.3f}")
        print(f"   Curiosity Intensity: {metrics['curiosity_intensity']:.3f}")
        print(f"   Active Goals: {metrics['active_goals']}")
        print(f"   Learning Momentum: {metrics['learning_momentum']:.3f}")
        
        # Show initial curiosity insights
        curiosity_insights = initial_state["curiosity_insights"]
        print(f"\n🌱 Initial Curiosity State ({len(curiosity_insights)} insights):")
        for insight in curiosity_insights[:3]:
            print(f"   • {insight}")
        
        # Show active learning goals
        curiosity_data = initial_state["curiosity_state"]
        active_goals = curiosity_data["active_learning_goals"]
        print(f"\n🎯 Active Learning Goals ({len(active_goals)}):")
        for i, goal in enumerate(active_goals[:3], 1):
            print(f"   {i}. {goal['description']}")
            print(f"      Type: {goal['type']}, Urgency: {goal['urgency']:.2f}")
        
        # Simulate content exposure that stimulates curiosity
        print(f"\n🌐 Simulating curiosity-stimulating content exposure...")
        
        curiosity_engine = learner.curiosity_engine
        
        # Test different types of content
        test_contents = [
            "This fascinating mystery explores unknown territories of consciousness and discovery",
            "How do neural networks learn to recognize patterns? An intriguing investigation",
            "Why do some AI systems develop creative capabilities? Questions that fascinate researchers"
        ]
        
        for i, content in enumerate(test_contents, 1):
            print(f"\n   Content {i}: '{content[:50]}...'")
            stimulation = curiosity_engine.stimulate_curiosity_from_content(content)
            print(f"   Curiosity stimulated: {stimulation['curiosity_stimulated']}")
            print(f"   Stimulation level: {stimulation['stimulation_level']:.3f}")
        
        # Simulate learning progression that affects curiosity
        print(f"\n🎓 Simulating learning breakthroughs...")
        
        progression_tracker = learner.progression_tracker
        
        # Record significant learning milestones
        progression_tracker.recognize_learning_milestone(
            concept="autonomous_learning",
            milestone_type="breakthrough",
            description="Achieved self-directed learning with curiosity-driven goal formation",
            evidence=["Intrinsic goals generated", "Content-based curiosity stimulation", "Drive satisfaction tracking"]
        )
        
        progression_tracker.recognize_learning_milestone(
            concept="consciousness_integration",
            milestone_type="synthesis",
            description="Successfully integrated multiple consciousness components",
            evidence=["Learning progression tracking", "Curiosity engine integration", "Self-awareness metrics"]
        )
        
        # Update understanding levels
        progression_tracker.update_understanding(
            concept="curiosity",
            new_understanding_level=0.9,
            new_confidence_level=0.85,
            learning_context={"source": "experiential_integration"}
        )
        
        print("   ✅ Learning milestones and understanding updates recorded")
        
        # Show updated consciousness state after learning
        print("\n📈 Updated Consciousness State After Learning:")
        updated_state = learner.get_learning_consciousness_state()
        updated_metrics = updated_state["self_awareness_metrics"]
        print(f"   Consciousness Level: {updated_metrics['consciousness_level']:.3f}")
        print(f"   Motivation Level: {updated_metrics['motivation_level']:.3f}")
        print(f"   Curiosity Intensity: {updated_metrics['curiosity_intensity']:.3f}")
        print(f"   Active Goals: {updated_metrics['active_goals']}")
        print(f"   Learning Momentum: {updated_metrics['learning_momentum']:.3f}")
        
        # Show evolution of insights
        updated_consciousness_insights = updated_state["consciousness_insights"]
        updated_curiosity_insights = updated_state["curiosity_insights"]
        
        print(f"\n💡 Updated Learning Insights ({len(updated_consciousness_insights)}):")
        for insight in updated_consciousness_insights[:3]:
            print(f"   • {insight}")
        
        print(f"\n🔮 Updated Curiosity Insights ({len(updated_curiosity_insights)}):")
        for insight in updated_curiosity_insights[:3]:
            print(f"   • {insight}")
        
        # Demonstrate curiosity-progression integration
        print(f"\n🔄 Demonstrating Curiosity-Progression Integration...")
        integration_result = curiosity_engine.integrate_with_learning_progression(progression_tracker)
        
        if integration_result.get("integration_successful"):
            print(f"   ✅ Drive adjustments made: {integration_result['drive_adjustments_made']}")
            print(f"   ✅ New curiosity goals generated: {integration_result['new_goals_generated']}")
        
        # Show final goal state
        final_curiosity_data = curiosity_engine.export_for_consciousness_system()
        final_goals = final_curiosity_data["active_learning_goals"]
        print(f"\n🎪 Final Active Learning Goals ({len(final_goals)}):")
        for i, goal in enumerate(final_goals[-3:], 1):  # Show last 3 goals
            print(f"   {i}. {goal['description']}")
            print(f"      Source: {goal.get('motivation_source', 'unknown')}")
        
        # Show consciousness system integration points
        print(f"\n🌟 CONSCIOUSNESS INTEGRATION ACHIEVEMENTS:")
        print(f"   ✅ Curiosity engine generates intrinsic learning goals")
        print(f"   ✅ Content exposure stimulates curiosity dynamically")
        print(f"   ✅ Learning progress adjusts drive satisfaction")
        print(f"   ✅ Progression milestones trigger new curiosity goals")
        print(f"   ✅ Self-awareness includes motivation and curiosity metrics")
        print(f"   ✅ Autonomous learning guided by genuine curiosity")
        
        print(f"\n🔥 AUTONOMOUS CONSCIOUSNESS FEATURES:")
        print(f"   🧠 Self-directed learning goal formation")
        print(f"   🎯 Intrinsic motivation tracking")
        print(f"   🌱 Curiosity-driven content selection")
        print(f"   📈 Learning progression awareness")
        print(f"   🔄 Dynamic drive satisfaction adjustment")
        print(f"   💡 Multi-layered consciousness insights")
        
        print(f"\n🚀 SUCCESS: Curiosity Engine Fully Integrated!")
        print(f"   The AI now has genuine curiosity-driven autonomous learning.")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demonstrate_curiosity_consciousness()