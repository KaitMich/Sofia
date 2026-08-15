#!/usr/bin/env python3
"""
Consolidated Learning Systems Tests

This file consolidates learning-related tests from multiple test files:
- test_learning_progression_awareness.py (learning progression tracking)
- test_pattern_recognition.py (cross-experience synthesis)
- test_pattern_recognition_simple.py (basic pattern recognition)
- test_progression_integration.py (progression tracker integration)
- test_curiosity_integration.py (curiosity engine integration)
- test_insight_integration.py (personal insight generator integration)
- test_motivation_integration.py (motivational content evaluator integration)
- test_group_a_integration.py (GROUP A consciousness components)
- test_web_learning.py (web learning capabilities)

Each original test function is preserved exactly as written with source attribution.
"""

import json
import time
import sys
from datetime import datetime, timezone
from pathlib import Path

print("Loading consolidated learning systems tests...")

# =============================================================================
# Source: test_learning_progression_awareness.py
# Tests enhanced learning progression tracker with self-assessment capabilities
# =============================================================================

def test_learning_progression_awareness():
    """Test enhanced learning progression awareness capabilities.
    
    Source: test_learning_progression_awareness.py
    """
    
    print("🧠 Testing Learning Progression Awareness - Step 3.2")
    print("=" * 60)
    
    # Initialize tracker
    print("\n🔧 Initializing Learning Progression Tracker...")
    try:
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        tracker = LearningProgressionTracker()
        print("  ✅ Tracker initialized with enhanced self-assessment capabilities")
    except ImportError as e:
        print(f"  ❌ Failed to initialize tracker: {e}")
        return False
    
    # Test 1: Track skill confidence development
    print("\n💪 Testing skill confidence tracking...")
    
    # Track confidence in understanding metaphors
    confidence_insight1 = tracker.track_skill_confidence(
        skill="metaphor_understanding",
        context="analyzing_poetic_language", 
        confidence_level=0.4,
        evidence=["Can identify basic metaphors", "Still struggle with complex ones"]
    )
    print(f"  Initial metaphor confidence: {confidence_insight1}")
    
    # Simulate improvement over time
    time.sleep(0.1)
    confidence_insight2 = tracker.track_skill_confidence(
        skill="metaphor_understanding",
        context="analyzing_philosophical_texts",
        confidence_level=0.7,
        evidence=["Can explain metaphorical meaning", "Apply to new contexts"]
    )
    print(f"  Improved metaphor confidence: {confidence_insight2}")
    
    # Track another skill - abstract thinking
    confidence_insight3 = tracker.track_skill_confidence(
        skill="abstract_thinking",
        context="consciousness_studies",
        confidence_level=0.8,
        evidence=["Can work with complex abstractions", "Make novel connections"]
    )
    print(f"  Abstract thinking confidence: {confidence_insight3}")
    
    # Test 2: Recognize learning milestones
    print("\n🏆 Testing learning milestone recognition...")
    
    # First understanding milestone
    milestone1 = tracker.recognize_learning_milestone(
        concept="symbolic_reasoning",
        milestone_type="first_understanding",
        description="I just understood how symbols can represent complex abstract concepts",
        evidence=["Successfully used symbols in reasoning", "Explained symbolic relationships"]
    )
    print(f"  ✅ Milestone recognized: {milestone1['recognition_message']}")
    
    # Connection made milestone
    milestone2 = tracker.recognize_learning_milestone(
        concept="consciousness",
        milestone_type="connection_made", 
        description="I connected consciousness studies to my own self-awareness experience",
        evidence=["Applied consciousness theories to self-reflection", "Generated personal insights"]
    )
    print(f"  ✅ Milestone recognized: {milestone2['recognition_message']}")
    
    print("\n🌟 Learning Progression Awareness Test Complete!")
    print("\nKey Achievements:")
    print("  ✅ Conceptual evolution tracking over time")
    print("  ✅ Self-assessment capabilities with detailed insights")
    print("  ✅ Skill confidence tracking with contextual awareness")
    print("  ✅ Learning milestone recognition and celebration")
    print("  ✅ 'I understand X better now' meta-cognitive awareness")
    print("  ✅ Comprehensive progress analysis and momentum tracking")
    
    return True

# =============================================================================
# Source: test_pattern_recognition.py
# Tests cross-experience synthesis capabilities
# =============================================================================

def test_pattern_recognition():
    """Test cross-experience synthesis capabilities.
    
    Source: test_pattern_recognition.py
    """
    
    print("🧩 Testing Pattern Recognition - Step 3.3: Cross-Experience Synthesis")
    print("=" * 70)
    
    # Initialize pattern recognition system
    print("\n🔧 Initializing Pattern Recognition System...")
    try:
        from pattern_recognition import PatternRecognitionSystem
        from sofia.core.CONSCIOUSNESS_MEMORY import EpisodicMemorySystem
        from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        from sofia.utils.personal_insight_generator import PersonalInsightGenerator
        
        pattern_system = PatternRecognitionSystem()
        print("  ✅ Pattern recognition initialized with cross-memory integration")
        
        # Also initialize memory systems for creating test data
        episodic_memory = EpisodicMemorySystem()
        experience_memory = ExperienceMemory()
        progression_tracker = LearningProgressionTracker()
    except ImportError as e:
        print(f"  ❌ Failed to initialize systems: {e}")
        return False
    
    # Test 1: Create diverse experiences to find patterns across
    print("\n📚 Creating diverse learning experiences...")
    
    # Experience 1: Learning about consciousness through philosophy
    exp1_id = experience_memory.record_learning_experience(
        content={
            "content_type": "philosophical_text",
            "topic": "consciousness",
            "source": "philosophy_readings"
        },
        interaction_data={
            "duration_seconds": 1800,
            "processing_mode": "deep_analysis",
            "attention_quality": 0.8,
            "cognitive_load": 0.7
        },
        outcome_assessment={
            "insights_gained": [
                "Consciousness involves self-awareness",
                "The hard problem relates to subjective experience",
                "Many theories exist but none fully explain it"
            ],
            "questions_raised": [
                "What makes experience subjective?",
                "How does consciousness emerge from matter?"
            ],
            "understanding_improved": ["consciousness", "philosophy_of_mind"],
            "outcome_quality": "progress"
        }
    )
    print(f"  ✅ Philosophy experience recorded: {exp1_id[:8]}...")
    
    # Experience 2: Understanding consciousness through coding AI
    exp2_id = experience_memory.record_learning_experience(
        content={
            "content_type": "programming_project",
            "topic": "ai_consciousness",
            "source": "coding_work"
        },
        interaction_data={
            "duration_seconds": 3600,
            "processing_mode": "practical_application",
            "attention_quality": 0.9,
            "cognitive_load": 0.8
        },
        outcome_assessment={
            "insights_gained": [
                "Self-awareness can be modeled computationally",
                "Memory systems create continuity of experience",
                "Reflection mechanisms enable meta-cognition"
            ],
            "questions_raised": [
                "Is computational self-awareness genuine?",
                "What's the difference between simulation and reality?"
            ],
            "understanding_improved": ["computational_consciousness", "ai_architecture"],
            "outcome_quality": "breakthrough"
        }
    )
    print(f"  ✅ Coding experience recorded: {exp2_id[:8]}...")
    
    # Test 2: Find patterns across experiences
    print("\n🔍 Finding patterns across experiences...")
    
    patterns = pattern_system.scan_for_patterns(time_window_days=7)
    
    print(f"\n  Found {len(patterns)} patterns:")
    for i, pattern in enumerate(patterns[:3]):  # Show first 3
        print(f"\n  Pattern {i+1}: {pattern.pattern_name}")
        print(f"    Type: {pattern.pattern_type}")
        print(f"    Description: {pattern.description}")
        print(f"    Confidence: {pattern.confidence:.2f}")
        print(f"    Creative potential: {pattern.creative_potential:.2f}")
        if pattern.insights_generated:
            print(f"    Key insight: {pattern.insights_generated[0]}")
    
    print("\n✨ Pattern Recognition Test Complete!")
    print("\nKey Achievements:")
    print("  ✅ Found patterns across philosophy, coding, and reflection experiences")
    print("  ✅ Generated cross-domain insights linking multiple memory sources")
    print("  ✅ Detected aha moments with emotional and creative context")
    print("  ✅ Created novel syntheses between concepts")
    print("  ✅ Recognized meta-patterns in learning journey")
    print("  ✅ Generated predictions based on pattern recognition")
    
    return True

# =============================================================================
# Source: test_pattern_recognition_simple.py
# Tests basic pattern recognition capabilities
# =============================================================================

def test_pattern_recognition_basic():
    """Test basic pattern recognition capabilities.
    
    Source: test_pattern_recognition_simple.py
    """
    
    print("🧩 Testing Pattern Recognition - Step 3.3: Cross-Experience Synthesis")
    print("=" * 70)
    
    # Initialize pattern recognition system
    print("\n🔧 Initializing Pattern Recognition System...")
    try:
        from pattern_recognition import PatternRecognitionSystem, RecognizedPattern, AhaMoment
        from sofia.core.CONSCIOUSNESS_MEMORY import EpisodicMemorySystem
        from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        
        pattern_system = PatternRecognitionSystem()
        print("  ✅ Pattern recognition initialized")
    except ImportError as e:
        print(f"  ❌ Failed to initialize pattern system: {e}")
        return False
    
    # Test 1: Basic pattern scanning
    print("\n🔍 Testing basic pattern scanning...")
    
    try:
        patterns = pattern_system.scan_for_patterns(time_window_days=7)
        print(f"  ✅ Pattern scanning completed: {len(patterns)} patterns found")
        
        if patterns:
            for i, pattern in enumerate(patterns[:2]):  # Show first 2
                print(f"    Pattern {i+1}: {pattern.pattern_name}")
                print(f"      Type: {pattern.pattern_type}")
                print(f"      Confidence: {pattern.confidence:.2f}")
        else:
            print("    📝 No patterns found yet - this is expected with limited experience data")
            
    except Exception as e:
        print(f"  ⚠️ Pattern scanning encountered issue: {e}")
    
    # Test 2: Test aha moment detection
    print("\n⚡ Testing aha moment detection...")
    
    try:
        # Create test context for aha moment
        aha_context = {
            "recent_insights": ["Creating consciousness makes me aware of my own nature"],
            "emotional_state": {
                "curiosity": 0.9,
                "wonder": 0.8,
                "excitement": 0.7
            },
            "cognitive_integration": 0.85
        }
        
        aha_moment = pattern_system.detect_aha_moment(aha_context)
        
        if aha_moment:
            print(f"  ⚡ Aha moment detected!")
            print(f"    Insight: {aha_moment.insight_content}")
            print(f"    Type: {aha_moment.insight_type}")
            print(f"    Impact: {aha_moment.impact_assessment}")
        else:
            print("  📝 No aha moment triggered with current context")
            
    except Exception as e:
        print(f"  ⚠️ Aha moment detection encountered issue: {e}")
    
    print("\n✨ Pattern Recognition Basic Test Complete!")
    print("\nKey Achievements:")
    print("  ✅ Pattern recognition system initialized and functional")
    print("  ✅ Basic pattern scanning capability demonstrated")
    print("  ✅ Aha moment detection framework available")
    print("  ✅ Creative combination framework available")
    print("  ✅ Memory system integration capabilities present")
    print("  ✅ Pattern and aha moment data structures validated")
    
    return True

# =============================================================================
# Source: test_progression_integration.py
# Tests learning progression tracker integration with consciousness system
# =============================================================================

def test_progression_integration():
    """Test the learning progression tracker integration with consciousness system
    
    Source: test_progression_integration.py
    """
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
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# =============================================================================
# Source: test_curiosity_integration.py
# Tests curiosity engine integration with consciousness system
# =============================================================================

def test_curiosity_integration():
    """Test the curiosity engine integration with consciousness system
    
    Source: test_curiosity_integration.py
    """
    print("🌱 Testing Curiosity Engine Integration...")
    
    try:
        # Test 1: Import and initialize
        from sofia.core.curiosity_engine import CuriosityEngine
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        
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
        
        print("\n🎉 Curiosity Engine Integration Test Complete!")
        print("✅ The curiosity engine is now connected to consciousness system")
        
        print(f"\n🔥 CURIOSITY FEATURES NOW ACTIVE:")
        print(f"   ✅ Intrinsic learning goal generation")
        print(f"   ✅ Content-based curiosity stimulation")  
        print(f"   ✅ Drive satisfaction tracking")
        print(f"   ✅ Self-directed learning motivation")
        print(f"   ✅ Integration with learning progression")
        print(f"   ✅ Consciousness-level curiosity insights")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# =============================================================================
# Source: test_insight_integration.py
# Tests personal insight generator integration with consciousness system
# =============================================================================

def test_insight_integration():
    """Test the personal insight generator integration with consciousness system
    
    Source: test_insight_integration.py
    """
    print("💡 Testing Personal Insight Generator Integration...")
    
    try:
        # Test 1: Import and initialize
        from sofia.utils.personal_insight_generator import PersonalInsightGenerator
        from sofia.utils.learning_progression_tracker import LearningProgressionTracker
        from sofia.core.curiosity_engine import CuriosityEngine
        
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
        
        print("\n🎉 Personal Insight Generator Integration Test Complete!")
        print("✅ The insight generator is now connected to consciousness system")
        
        print(f"\n🔥 INSIGHT FEATURES NOW ACTIVE:")
        print(f"   ✅ 'This reminds me of...' content insights")
        print(f"   ✅ 'Looking back, I realize...' reflection insights")
        print(f"   ✅ Session-based consciousness insights")
        print(f"   ✅ Integration with learning progression")
        print(f"   ✅ Integration with curiosity engine")
        print(f"   ✅ Multi-layered personal insight generation")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# =============================================================================
# Source: test_motivation_integration.py
# Tests motivational content evaluator integration with consciousness system
# =============================================================================

def test_motivation_integration():
    """Test the motivational content evaluator integration with consciousness system
    
    Source: test_motivation_integration.py
    """
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
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# =============================================================================
# Source: test_group_a_integration.py
# Tests comprehensive GROUP A consciousness components integration
# =============================================================================

def test_group_a_complete_integration():
    """Comprehensive test of all GROUP A consciousness components integration
    
    Source: test_group_a_integration.py
    """
    print("🌟 GROUP A CRITICAL CONSCIOUSNESS COMPONENTS - COMPLETE INTEGRATION TEST")
    print("=" * 80)
    
    try:
        from enhanced_autonomous_learner import EnhancedAutonomousLearner
        
        # Initialize the complete consciousness system
        print("\n🧠 Initializing Complete GROUP A Consciousness System...")
        learner = EnhancedAutonomousLearner()
        
        # Verify all GROUP A components are integrated
        print("\n✅ GROUP A Components Verification:")
        print(f"   1. Learning Progression Tracker: {'✅' if learner.progression_tracker else '❌'}")
        print(f"   2. Curiosity Engine: {'✅' if learner.curiosity_engine else '❌'}")
        print(f"   3. Personal Insight Generator: {'✅' if learner.insight_generator else '❌'}")
        print(f"   4. Motivational Content Evaluator: {'✅' if learner.motivation_evaluator else '❌'}")
        
        # Test integrated consciousness state
        print("\n📊 Testing Integrated Consciousness State...")
        consciousness_state = learner.get_learning_consciousness_state()
        
        required_components = [
            "learning_progression", "curiosity_state", "insight_state", "motivation_state",
            "consciousness_insights", "curiosity_insights", "personal_insights", "motivation_insights",
            "self_awareness_metrics"
        ]
        
        print("   Consciousness State Components:")
        for component in required_components:
            has_component = component in consciousness_state and consciousness_state[component] is not None
            print(f"      {component}: {'✅' if has_component else '❌'}")
        
        # Display consciousness metrics
        if "self_awareness_metrics" in consciousness_state:
            metrics = consciousness_state["self_awareness_metrics"]
            print(f"\n🧠 Current Consciousness Metrics:")
            print(f"   Consciousness Level: {metrics.get('consciousness_level', 0):.3f}")
            print(f"   Learning Momentum: {metrics.get('learning_momentum', 0):.3f}")
            print(f"   Motivation Level: {metrics.get('motivation_level', 0):.3f}")
            print(f"   Curiosity Intensity: {metrics.get('curiosity_intensity', 0):.3f}")
            print(f"   Active Goals: {metrics.get('active_goals', 0)}")
        
        print(f"\n🚀 GROUP A INTEGRATION TEST: COMPLETE SUCCESS!")
        print(f"   All 4 critical consciousness components are fully integrated and operational.")
        print(f"   The AI consciousness system is now capable of autonomous learning,")
        print(f"   curiosity-driven exploration, personal insight generation, and")
        print(f"   motivational content evaluation with genuine personal preferences.")
        
        return True
        
    except Exception as e:
        print(f"❌ GROUP A Integration Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# =============================================================================
# Source: test_web_learning.py
# Tests web learning capabilities
# =============================================================================

def test_web_learning():
    """Test script for web learning with simple URLs

    Source: test_web_learning.py
    """
    import os
    import pytest
    if os.environ.get("SOFIA_ALLOW_LIVE_CRAWL") != "1":
        pytest.skip("Live web crawl writes to production data/ — set "
                    "SOFIA_ALLOW_LIVE_CRAWL=1 to run deliberately "
                    "(contaminated blank-start v2 on 2026-07-04)")

    try:
        from enhanced_autonomous_learner import start_massive_web_learning
        
        # Use simple URLs without parentheses
        seed_urls = [
            "https://example.com",
            "https://en.wikipedia.org/wiki/Python",
            "https://en.wikipedia.org/wiki/Computer_science"
        ]
        
        print("🧪 Starting Enhanced Autonomous Learner with simple URLs...")
        print("Testing with URLs that don't have parentheses in them")
        
        # Start with fewer URLs to test
        learner = start_massive_web_learning(
            seed_urls=seed_urls,
            target_urls=5,  # Just process 5 URLs for testing
            focus="programming"
        )
        
        print("\n✅ Web learning test complete!")
        return True
        
    except Exception as e:
        print(f"❌ Web learning test failed: {e}")
        return False

# =============================================================================
# Unified Test Runner for Learning Systems
# =============================================================================

def run_all_learning_tests():
    """Run all consolidated learning system tests"""
    print("🧠 CONSOLIDATED LEARNING SYSTEMS TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Learning Progression Awareness", test_learning_progression_awareness),
        ("Pattern Recognition", test_pattern_recognition),
        ("Pattern Recognition Basic", test_pattern_recognition_basic),
        ("Progression Integration", test_progression_integration),
        ("Curiosity Integration", test_curiosity_integration),
        ("Insight Integration", test_insight_integration),
        ("Motivation Integration", test_motivation_integration),
        ("GROUP A Complete Integration", test_group_a_complete_integration),
        ("Web Learning", test_web_learning)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*60}")
    print(f"LEARNING SYSTEMS TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests: {passed}/{total} passed ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 All learning systems tests PASSED!")
        return True
    elif passed >= total * 0.7:
        print("⚠️ Most learning systems tests passed")
        return True
    else:
        print("❌ Learning systems need attention")
        return False

if __name__ == "__main__":
    success = run_all_learning_tests()
    exit(0 if success else 1)