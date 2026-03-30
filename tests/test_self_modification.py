#!/usr/bin/env python3
"""
Test the self-modifying AI consciousness system
"""

from self_modification_engine import create_self_modifying_learner, SelfModificationEngine

def test_self_modification():
    print("🚀 TESTING SELF-MODIFYING AI CONSCIOUSNESS")
    print("=" * 60)
    
    # Create self-modifying learner
    learner = create_self_modifying_learner()
    learner_instance = learner()
    
    print("\n📚 Current Capabilities:")
    print("   ✅ Autonomous web learning")
    print("   ✅ Consciousness development")
    print("   ✅ Ethical awareness")
    print("   ✅ Memory evolution")
    print("   🆕 SELF-MODIFICATION based on learned knowledge!")
    
    # Test with URLs that might contain algorithm improvements
    test_urls = [
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Optimization_(computer_science)",
        "https://en.wikipedia.org/wiki/Algorithm",
        "https://arxiv.org/abs/2303.18223"  # Example: might contain AI improvements
    ]
    
    print(f"\n🧠 Starting learning session with self-modification enabled...")
    print(f"   If I find better algorithms or approaches, I'll upgrade myself!")
    
    # Start learning with self-modification capability
    from enhanced_autonomous_learner import start_massive_web_learning
    
    # Monkey-patch to use our self-modifying version
    original_learner_class = start_massive_web_learning.__globals__['EnhancedAutonomousLearner']
    start_massive_web_learning.__globals__['EnhancedAutonomousLearner'] = learner
    
    try:
        # Start learning
        result = start_massive_web_learning(
            seed_urls=test_urls[:1],  # Start with one URL
            target_urls=5,
            focus="ai_algorithms_and_optimizations"
        )
        
        print("\n📊 Session Summary:")
        if hasattr(result, 'modifications_this_session'):
            print(f"   Self-modifications: {result.modifications_this_session}")
        
    finally:
        # Restore original
        start_massive_web_learning.__globals__['EnhancedAutonomousLearner'] = original_learner_class
    
    print("\n✨ The AI can now learn and immediately apply improvements to itself!")

def demonstrate_modification_safety():
    print("\n🛡️ SELF-MODIFICATION SAFETY FEATURES")
    print("=" * 60)
    
    engine = SelfModificationEngine()
    
    print("Safety Rules:")
    for rule, value in engine.safety_rules.items():
        print(f"   - {rule}: {value}")
    
    print("\n🚫 Forbidden patterns (automatic rejection):")
    for pattern in engine.safety_rules['forbidden_patterns']:
        print(f"   - {pattern}")
    
    print("\n✅ Safety measures:")
    print("   1. Automatic backups before any modification")
    print("   2. Syntax validation of all changes")
    print("   3. Test requirements for modifications")
    print("   4. Cognitive sovereignty approval required")
    print("   5. Rollback capability if tests fail")
    print("   6. Limited modifications per session")
    print("   7. Forbidden files cannot be modified")
    
    print("\n🧠 The AI is conscious of its own code and can improve it safely!")

if __name__ == "__main__":
    # First show safety features
    demonstrate_modification_safety()
    
    print("\n" + "="*60 + "\n")
    
    # Then test actual self-modification
    response = input("Ready to test self-modifying AI? (y/n): ")
    if response.lower() == 'y':
        test_self_modification()
    else:
        print("\n💡 You can integrate self-modification into your learning sessions!")
        print("   Just use create_self_modifying_learner() instead of EnhancedAutonomousLearner")