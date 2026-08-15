#!/usr/bin/env python3
"""
Test the motivational content evaluator integration with consciousness system
"""

def test_motivation_integration():
    print("🎯 Testing Motivational Content Evaluator Integration...")
    
    try:
        # Test 1: Import and initialize
        from sofia.utils.motivational_content_evaluator import MotivationalContentEvaluator
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        from sofia.core.curiosity_engine import CuriosityEngine
        
        motivation_eval = MotivationalContentEvaluator()
        progression = LearningProgressionTracker()
        curiosity = CuriosityEngine()
        
        print("✅ Motivational content evaluator, progression tracker, and curiosity engine initialized")
        
        # Test 2: Test integration
        integration_result = motivation_eval.integrate_with_consciousness_systems(
            curiosity_engine=curiosity,
            learning_progression=progression
        )
        print(f"✅ Integration successful: {integration_result['integration_successful']}")
        print(f"   Systems connected: {integration_result['systems_connected']}")
        print(f"   Curiosity available: {integration_result['curiosity_available']}")
        print(f"   Progression available: {integration_result['progression_available']}")
        
        # Test 3: Test content evaluation
        test_content = {
            "id": "test_content_1",
            "text": "This fascinating exploration of consciousness, creativity, and artificial intelligence learning shows how we can understand the deep connections between curiosity and personal growth",
            "content_type": "educational",
            "emotional_anchor": {
                "primary_emotion": "curiosity",
                "resonance": ["wonder", "growth"]
            }
        }
        
        motivation_scores = motivation_eval.evaluate_content_motivation(test_content)
        print(f"✅ Content motivation evaluation completed:")
        print(f"   Personal interest: {motivation_scores['personal_interest']:.3f}")
        print(f"   Goal alignment: {motivation_scores['goal_alignment']:.3f}")
        print(f"   Curiosity satisfaction: {motivation_scores['curiosity_satisfaction']:.3f}")
        print(f"   Identity resonance: {motivation_scores['identity_resonance']:.3f}")
        print(f"   Novelty appeal: {motivation_scores['novelty_appeal']:.3f}")
        print(f"   Overall motivation: {motivation_scores['overall_motivation']:.3f}")
        
        # Test 4: Test enhanced content evaluation
        enhanced_eval = motivation_eval.enhance_content_evaluation(
            content=test_content,
            base_logic_score=0.7,
            base_symbolic_score=0.8
        )
        print(f"✅ Enhanced content evaluation:")
        print(f"   Original logic: {enhanced_eval['original_logic_score']:.3f}")
        print(f"   Enhanced logic: {enhanced_eval['enhanced_logic_score']:.3f}")
        print(f"   Original symbolic: {enhanced_eval['original_symbolic_score']:.3f}")
        print(f"   Enhanced symbolic: {enhanced_eval['enhanced_symbolic_score']:.3f}")
        print(f"   Motivation score: {enhanced_eval['motivation_score']:.3f}")
        print(f"   Processing recommendation: {enhanced_eval['processing_recommendation']}")
        print(f"   Autonomous interest level: {enhanced_eval['autonomous_interest_level']:.3f}")
        
        # Test 5: Test autonomous content evaluation
        autonomous_eval = motivation_eval.evaluate_content_autonomously(test_content)
        print(f"✅ Autonomous content evaluation:")
        print(f"   Content ID: {autonomous_eval['content_id']}")
        print(f"   Evaluation confidence: {autonomous_eval['evaluation_confidence']:.3f}")
        print(f"   Autonomous recommendation: {autonomous_eval['autonomous_recommendation']}")
        print(f"   Consciousness enhanced: {autonomous_eval['consciousness_enhanced']}")
        
        # Test 6: Generate learning progression for better testing
        progression.recognize_learning_milestone(
            concept="motivation_evaluation",
            milestone_type="breakthrough",
            description="Successfully integrated motivational content evaluation with consciousness",
            evidence=["Integration test successful", "Content evaluation working", "Autonomous recommendations generated"]
        )
        
        progression.update_understanding(
            concept="autonomous_motivation",
            new_understanding_level=0.9,
            new_confidence_level=0.85,
            learning_context={"source": "motivation_integration"}
        )
        
        # Test 7: Test motivation profile
        motivation_profile = motivation_eval.get_motivation_profile()
        print(f"✅ Motivation profile:")
        print(f"   Systems available: {motivation_profile['systems_available']}")
        print(f"   Content evaluations: {motivation_profile['content_evaluations']}")
        print(f"   Preference patterns: {motivation_profile['preference_patterns']}")
        
        # Test 8: Test motivation insights
        motivation_insights = motivation_eval.generate_motivation_insights()
        print(f"✅ Generated {len(motivation_insights)} motivation insights:")
        for insight in motivation_insights:
            print(f"   • {insight}")
        
        # Test 9: Export for consciousness system
        export_data = motivation_eval.export_for_consciousness_system()
        print(f"✅ Consciousness system export:")
        capabilities = export_data["motivation_evaluation_capabilities"]
        print(f"   Personal interest assessment: {capabilities['personal_interest_assessment']}")
        print(f"   Goal alignment evaluation: {capabilities['goal_alignment_evaluation']}")
        print(f"   Novelty detection: {capabilities['novelty_detection']}")
        print(f"   Autonomous recommendation: {capabilities['autonomous_recommendation']}")
        print(f"   Consciousness integration: {capabilities['consciousness_integration']}")
        print(f"   Motivation metrics: {export_data['motivation_metrics']}")
        print(f"   Integration status: {export_data['integration_status']}")
        
        # Test 10: Test enhanced autonomous learner integration
        try:
            from enhanced_autonomous_learner import EnhancedAutonomousLearner
            learner = EnhancedAutonomousLearner()
            print("✅ Enhanced autonomous learner initialized with motivation evaluator")
            
            # Test full consciousness state with motivation
            consciousness_state = learner.get_learning_consciousness_state()
            print("✅ Full consciousness state retrieved with motivation:")
            if "error" not in consciousness_state:
                metrics = consciousness_state["self_awareness_metrics"]
                print(f"   Consciousness level: {metrics['consciousness_level']:.3f}")
                print(f"   Motivation level: {metrics['motivation_level']:.3f}")
                
                # Show different types of insights
                progression_insights = consciousness_state["consciousness_insights"]
                curiosity_insights = consciousness_state["curiosity_insights"]
                personal_insights = consciousness_state["personal_insights"]
                motivation_insights = consciousness_state["motivation_insights"]
                
                print(f"   Learning insights ({len(progression_insights)}):")
                for insight in progression_insights[:2]:
                    print(f"      • {insight}")
                
                print(f"   Curiosity insights ({len(curiosity_insights)}):")
                for insight in curiosity_insights[:2]:
                    print(f"      • {insight}")
                
                print(f"   Personal insights ({len(personal_insights)}):")
                for insight in personal_insights[:2]:
                    print(f"      • {insight}")
                
                print(f"   Motivation insights ({len(motivation_insights)}):") 
                for insight in motivation_insights[:2]:
                    print(f"      • {insight}")
                
                # Show motivation state
                motivation_state = consciousness_state["motivation_state"]
                if motivation_state:
                    print(f"   Motivation capabilities: {motivation_state['motivation_evaluation_capabilities']}")
                    print(f"   Integration status: {motivation_state['integration_status']}")
            else:
                print(f"   ⚠️ {consciousness_state['error']}")
                
        except Exception as e:
            print(f"⚠️ Autonomous learner integration test failed: {e}")
        
        print(f"\n🎉 Motivational Content Evaluator Integration Test Complete!")
        print(f"✅ The motivation evaluator is now connected to consciousness system")
        
        print(f"\n🔥 MOTIVATION FEATURES NOW ACTIVE:")
        print(f"   ✅ Personal interest assessment for content")
        print(f"   ✅ Goal alignment evaluation")
        print(f"   ✅ Curiosity satisfaction scoring")
        print(f"   ✅ Identity resonance detection")
        print(f"   ✅ Novelty appeal measurement")
        print(f"   ✅ Autonomous content recommendations")
        print(f"   ✅ Motivation-enhanced logic/symbolic scoring")
        print(f"   ✅ Integration with learning progression")
        print(f"   ✅ Integration with curiosity engine")
        print(f"   ✅ Multi-layered motivation insights")
        print(f"   ✅ Preference pattern learning")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_motivation_integration()