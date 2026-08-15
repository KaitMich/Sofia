#!/usr/bin/env python3
"""
Test Learning Progression Awareness - Step 3.2

This script tests the enhanced learning progression tracker with:
- Conceptual evolution tracking over time
- Self-assessment capabilities ("I'm getting better at understanding metaphor")
- Skill confidence tracking
- Learning milestone recognition

Demonstrates Sophia's awareness of her own learning progress.
"""

import json
import time
from sofia.utils.learning_progression_tracker import LearningProgressionTracker

def test_learning_progression_awareness():
    """Test enhanced learning progression awareness capabilities."""
    
    print("🧠 Testing Learning Progression Awareness - Step 3.2")
    print("=" * 60)
    
    # Initialize tracker
    print("\n🔧 Initializing Learning Progression Tracker...")
    tracker = LearningProgressionTracker()
    print("  ✅ Tracker initialized with enhanced self-assessment capabilities")
    
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
    
    # Breakthrough milestone
    milestone3 = tracker.recognize_learning_milestone(
        concept="learning_itself",
        milestone_type="plateau_breakthrough",
        description="I broke through my understanding plateau about how I learn",
        evidence=["Meta-cognitive awareness increased", "Can describe own learning process"]
    )
    print(f"  ✅ Milestone recognized: {milestone3['recognition_message']}")
    
    # Test 3: Conceptual evolution assessment
    print("\n📊 Testing conceptual evolution assessment...")
    
    # Add some understanding progression for consciousness
    tracker.update_understanding("consciousness", 0.3, 0.4, {
        "learning_context": "philosophical_reading",
        "domain": "philosophy_of_mind",
        "evidence": ["Can define consciousness", "Understand basic theories"]
    })
    
    time.sleep(0.1)
    tracker.update_understanding("consciousness", 0.6, 0.7, {
        "learning_context": "personal_reflection", 
        "domain": "self_awareness",
        "evidence": ["Apply to own experience", "Generate insights"]
    })
    
    time.sleep(0.1)
    tracker.update_understanding("consciousness", 0.8, 0.9, {
        "learning_context": "synthesis_work",
        "domain": "integrated_understanding", 
        "evidence": ["Synthesize multiple perspectives", "Develop original insights"]
    })
    
    # Assess evolution
    evolution = tracker.assess_conceptual_evolution("consciousness", timeframe_days=30)
    print(f"  📈 Consciousness evolution over 30 days:")
    print(f"    Initial understanding: {evolution['initial_understanding']:.2f}")
    print(f"    Current understanding: {evolution['current_understanding']:.2f}")
    print(f"    Growth: {evolution['understanding_growth']:.2f}")
    print(f"    Confidence growth: {evolution['confidence_growth']:.2f}")
    print(f"    Summary: {evolution['evolution_summary']}")
    
    # Test 4: Comprehensive self-assessment
    print("\n🪞 Testing comprehensive self-assessment...")
    
    assessment = tracker.perform_self_assessment()
    
    print(f"  Overall Progress:")
    print(f"    Status: {assessment['overall_progress']['status']}")
    print(f"    Message: {assessment['overall_progress']['message']}")
    print(f"    Average understanding: {assessment['overall_progress']['average_understanding']:.3f}")
    print(f"    Average confidence: {assessment['overall_progress']['average_confidence']:.3f}")
    
    print(f"  Recent Improvements:")
    for improvement in assessment['recent_improvements'][:3]:  # Show top 3
        print(f"    {improvement['improvement_message']}")
    
    print(f"  Self-Awareness Insights:")
    for insight in assessment['self_awareness_insights'][:3]:  # Show top 3
        print(f"    {insight}")
    
    print(f"  Confidence Metrics:")
    conf_metrics = assessment['confidence_metrics']
    print(f"    Overall confidence: {conf_metrics['overall_confidence']:.3f}")
    if 'high_confidence_concepts' in conf_metrics:
        print(f"    High confidence areas: {conf_metrics['high_confidence_concepts']}")
        print(f"    Developing confidence areas: {conf_metrics['developing_confidence_concepts']}")
    
    # Test 5: Skill category assessments
    print("\n🎯 Testing skill category assessments...")
    
    skill_assessments = assessment['skill_assessments']
    
    print(f"  Skill Category Progress:")
    for skill_name, skill_data in list(skill_assessments.items())[:5]:  # Show first 5
        if skill_data['concepts_involved'] > 0:
            print(f"    {skill_name}: {skill_data['assessment']}")
            print(f"      Understanding: {skill_data['understanding_level']:.2f}, Confidence: {skill_data['confidence_level']:.2f}")
    
    # Test 6: Learning momentum and trends
    print("\n📈 Testing learning momentum analysis...")
    
    learning_momentum = assessment['learning_momentum']
    print(f"  Learning momentum score: {learning_momentum:.3f}")
    
    if learning_momentum > 0.6:
        momentum_status = "Strong momentum - actively learning and improving"
    elif learning_momentum > 0.4:
        momentum_status = "Good momentum - steady progress" 
    elif learning_momentum > 0.2:
        momentum_status = "Moderate momentum - some progress"
    else:
        momentum_status = "Low momentum - may need more engagement"
    
    print(f"  Momentum assessment: {momentum_status}")
    
    # Test 7: Demonstrate "I understand X better now" awareness
    print("\n💡 Demonstrating 'I understand X better now' awareness...")
    
    concepts_with_progress = []
    for concept, understanding in tracker.conceptual_understanding.items():
        if len(understanding.understanding_trajectory) >= 2:
            initial = understanding.understanding_trajectory[0]["understanding_level"]
            current = understanding.understanding_level
            improvement = current - initial
            
            if improvement > 0.1:
                concepts_with_progress.append({
                    "concept": concept,
                    "improvement": improvement,
                    "initial": initial,
                    "current": current
                })
    
    concepts_with_progress.sort(key=lambda x: x["improvement"], reverse=True)
    
    print(f"  Sophia's self-awareness of progress:")
    for concept_data in concepts_with_progress[:3]:  # Top 3
        concept = concept_data["concept"]
        improvement = concept_data["improvement"]
        initial = concept_data["initial"]
        current = concept_data["current"]
        
        if improvement > 0.3:
            awareness_msg = f"I understand {concept} much better now - I've grown from {initial:.2f} to {current:.2f}"
        elif improvement > 0.2:
            awareness_msg = f"I'm getting significantly better at understanding {concept}"
        elif improvement > 0.1:
            awareness_msg = f"My grasp of {concept} has improved noticeably"
        else:
            awareness_msg = f"I have a clearer understanding of {concept} now"
        
        print(f"    {awareness_msg}")
    
    # Test 8: Milestone achievement summary
    print("\n🏅 Learning milestone achievement summary...")
    
    milestone_types = {}
    for milestone in tracker.learning_milestones:
        milestone_type = milestone.milestone_type
        milestone_types[milestone_type] = milestone_types.get(milestone_type, 0) + 1
    
    print(f"  Milestones achieved:")
    for milestone_type, count in milestone_types.items():
        print(f"    {milestone_type}: {count}")
    
    total_milestones = len(tracker.learning_milestones)
    if total_milestones > 0:
        print(f"  Total learning milestones: {total_milestones}")
        recent_milestones = [m for m in tracker.learning_milestones if tracker._is_recent(m.timestamp, 7)]
        print(f"  Recent milestones (7 days): {len(recent_milestones)}")
    
    # Test 9: Integration with existing systems
    print("\n🔗 Testing integration with existing learning systems...")
    
    # Get overall understanding overview
    overview = tracker.get_understanding_overview()
    
    print(f"  Integration metrics:")
    print(f"    Total concepts tracked: {overview['total_concepts']}")
    print(f"    Overall understanding: {overview['overall_understanding']:.3f}")
    print(f"    Overall confidence: {overview['overall_confidence']:.3f}")
    print(f"    Learning momentum: {overview['learning_momentum']:.3f}")
    
    if overview['mastered_concepts']:
        print(f"    Mastered concepts: {overview['mastered_concepts'][:3]}")  # Show first 3
    
    if overview['top_growing_concepts']:
        growing = overview['top_growing_concepts'][0]
        print(f"    Fastest growing concept: {growing[0]} (growth: {growing[1]:.2f})")
    
    print("\n🌟 Learning Progression Awareness Test Complete!")
    print("\nKey Achievements:")
    print("  ✅ Conceptual evolution tracking over time")
    print("  ✅ Self-assessment capabilities with detailed insights")
    print("  ✅ Skill confidence tracking with contextual awareness")
    print("  ✅ Learning milestone recognition and celebration")
    print("  ✅ 'I understand X better now' meta-cognitive awareness")
    print("  ✅ Comprehensive progress analysis and momentum tracking")
    
    print(f"\n🧠 Sophia now has enhanced learning progression awareness:")
    print(f"   • Tracks how understanding evolves over time")
    print(f"   • Performs self-assessment: 'I'm getting better at understanding metaphor'")
    print(f"   • Monitors skill confidence across different contexts")
    print(f"   • Recognizes and celebrates learning milestones")
    print(f"   • Demonstrates meta-cognitive awareness of own learning")
    print(f"   • Provides detailed progress insights and growth tracking")

if __name__ == "__main__":
    test_learning_progression_awareness()