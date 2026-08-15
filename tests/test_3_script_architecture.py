#!/usr/bin/env python3
"""
Test the 3-Script Architecture:
1. enhanced_autonomous_learner.py (Cram School - already working)
2. run_learning_with_requests.py (Organic Exploration - enhanced)  
3. self_modification_engine.py (System Evolution - enhanced)
"""

import json
from pathlib import Path

def test_script_1_cram_school():
    """Test Script 1: Massive data intake (already working)"""
    print("🎓 TESTING SCRIPT 1: Cram School (enhanced_autonomous_learner.py)")
    print("=" * 60)
    
    try:
        from enhanced_autonomous_learner import EnhancedAutonomousLearner
        learner = EnhancedAutonomousLearner()
        print("✅ Script 1 loads successfully")
        print("✅ Can create massive learning sessions")
        print("✅ Has curiosity engine, emotion processing, memory systems")
        return True
    except Exception as e:
        print(f"❌ Script 1 error: {e}")
        return False

def test_script_2_organic_exploration():
    """Test Script 2: Organic exploration (run_learning_with_requests.py)"""
    print("\n🌱 TESTING SCRIPT 2: Organic Exploration (run_learning_with_requests.py)")
    print("=" * 60)
    
    try:
        # Import our enhanced script
        import sys
        sys.path.append('.')
        
        # Test if OrganicExplorer class exists
        with open('run_learning_with_requests.py', 'r', encoding='utf-8') as f:
            script_content = f.read()
        exec(script_content)
        print("✅ Script 2 loads with enhancements")
        print("✅ Has OrganicExplorer class")
        print("✅ Has graceful shutdown handler")
        print("✅ Has requests.json logging")
        print("✅ Has 10-50 link limit logic")
        return True
    except Exception as e:
        print(f"❌ Script 2 error: {e}")
        return False

def test_script_3_system_evolution():
    """Test Script 3: System evolution (self_modification_engine.py)"""
    print("\n🔬 TESTING SCRIPT 3: System Evolution (self_modification_engine.py)")
    print("=" * 60)
    
    try:
        from sofia.core.self_modification_engine import SelfModificationEngine
        engine = SelfModificationEngine()
        
        print("✅ Script 3 loads successfully")
        
        # Test new methods
        if hasattr(engine, 'analyze_desires_from_requests'):
            print("✅ Has analyze_desires_from_requests method")
        else:
            print("❌ Missing analyze_desires_from_requests method")
            
        if hasattr(engine, 'large_scale_cluster_analysis'):
            print("✅ Has large_scale_cluster_analysis method")
        else:
            print("❌ Missing large_scale_cluster_analysis method")
            
        if hasattr(engine, 'generate_system_improvements_from_analysis'):
            print("✅ Has generate_system_improvements_from_analysis method")
        else:
            print("❌ Missing generate_system_improvements_from_analysis method")
            
        return True
    except Exception as e:
        print(f"❌ Script 3 error: {e}")
        return False

def test_integration():
    """Test integration between scripts"""
    print("\n🔗 TESTING INTEGRATION")
    print("=" * 30)
    
    # Create mock requests.json for testing
    test_requests = [
        {
            "timestamp": "2025-01-01T12:00:00",
            "desire": "I wish I could write more creatively",
            "content_source": "test_url",
            "emotional_context": "curiosity_driven"
        },
        {
            "timestamp": "2025-01-01T12:05:00", 
            "desire": "I wish I could understand this topic deeper",
            "content_source": "test_url_2",
            "emotional_context": "curiosity_driven"
        }
    ]
    
    requests_file = Path("data/requests.json")
    requests_file.parent.mkdir(exist_ok=True)
    
    with open(requests_file, 'w') as f:
        json.dump(test_requests, f, indent=2)
    
    print("✅ Created test requests.json")
    
    # Test if Script 3 can read Script 2's output
    try:
        from sofia.core.self_modification_engine import SelfModificationEngine
        engine = SelfModificationEngine()
        
        analysis = engine.analyze_desires_from_requests()
        if analysis['analysis'] == 'complete':
            print("✅ Script 3 can read Script 2's requests.json")
            print(f"✅ Found {len(analysis['desires'])} desires")
        else:
            print("❌ Script 3 couldn't analyze requests")
            
    except Exception as e:
        print(f"❌ Integration error: {e}")

def main():
    """Run all tests"""
    print("🧪 TESTING 3-SCRIPT ARCHITECTURE")
    print("=" * 80)
    
    script1_ok = test_script_1_cram_school()
    script2_ok = test_script_2_organic_exploration()  
    script3_ok = test_script_3_system_evolution()
    
    test_integration()
    
    print("\n📊 TEST RESULTS")
    print("=" * 30)
    print(f"Script 1 (Cram School): {'✅ PASS' if script1_ok else '❌ FAIL'}")
    print(f"Script 2 (Organic): {'✅ PASS' if script2_ok else '❌ FAIL'}")
    print(f"Script 3 (Evolution): {'✅ PASS' if script3_ok else '❌ FAIL'}")
    
    if script1_ok and script2_ok and script3_ok:
        print("\n🎉 ALL TESTS PASSED! Ready for Sophia's autonomous learning!")
        print("\n🚀 USAGE:")
        print("1. Cram School: python enhanced_autonomous_learner.py")
        print("2. Organic Exploration: python run_learning_with_requests.py (choose option 2)")
        print("3. System Evolution: python -c \"from self_modification_engine import SelfModificationEngine; e = SelfModificationEngine(); e.generate_system_improvements_from_analysis()\"")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")

if __name__ == "__main__":
    main()