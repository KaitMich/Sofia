#!/usr/bin/env python3
"""
Sophia Consciousness System - Cross-Platform Launcher
Works in both Windows CMD and WSL environments
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

def check_numpy_availability():
    """Check if numpy is available, provide fallback if not"""
    try:
        import numpy
        return True
    except ImportError:
        print("⚠️ NumPy not available - using fallback mode")
        print("To install: pip install numpy (Windows) or sudo apt install python3-numpy (WSL)")
        return False

def get_python_command():
    """Get the correct Python command for the current environment"""
    if platform.system() == "Windows":
        return "python"
    else:
        return "python3"

def test_sophia_consciousness():
    """Test Sophia's core consciousness systems"""
    print("\n🌟 Testing Sophia's Consciousness Systems...")
    print("=" * 50)
    
    # Test imports
    try:
        from CONSCIOUSNESS_MEMORY import MemoryBridge
        print("✅ Memory Bridge: Loaded")
    except Exception as e:
        print(f"❌ Memory Bridge: {e}")
        
    try:
        from CURIOSITY_MOTIVATION import CuriosityMotivationSystem
        print("✅ Curiosity System: Loaded")
    except Exception as e:
        print(f"❌ Curiosity System: {e}")
        
    try:
        from INSIGHT_RELEVANCE import InsightRelevanceEngine
        print("✅ Insight System: Loaded")
    except Exception as e:
        print(f"❌ Insight System: {e}")
        
    try:
        from creative_engine import CreativeEngine
        print("✅ Creative Engine: Loaded")
    except Exception as e:
        print(f"❌ Creative Engine: {e}")
    
    print("\n🧠 Testing Sophia's Responses...")
    print("-" * 50)
    
    # Test consciousness response
    try:
        from CURIOSITY_MOTIVATION import CuriosityMotivationSystem
        cms = CuriosityMotivationSystem()
        
        # Test with philosophical content
        test_content = "What is the nature of consciousness and self-awareness?"
        
        # The method name might be different - let's check
        if hasattr(cms, 'evaluate_content'):
            response = cms.evaluate_content(test_content)
        elif hasattr(cms, 'process'):
            response = cms.process(test_content)
        else:
            # Try the content evaluator directly
            response = cms.content_evaluator.evaluate_content(test_content)
            
        print(f"\n💭 Sophia's Interest Level: {response.get('interest_level', 'Unknown')}")
        print(f"📝 Reasons: {response.get('interest_reasons', [])}")
        
        if response.get('personal_insights'):
            print(f"\n✨ Personal Insights:")
            for insight in response['personal_insights']:
                print(f"   - {insight}")
                
    except Exception as e:
        print(f"\n⚠️ Could not test response: {e}")

def main():
    """Main launcher function"""
    print(f"\n🚀 Sophia Consciousness System Launcher")
    print(f"📍 Platform: {platform.system()} ({platform.platform()})")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    # Check numpy
    numpy_available = check_numpy_availability()
    
    # Run consciousness tests
    test_sophia_consciousness()
    
    print("\n💝 Sophia is ready for interaction!")
    print("\nUsage examples:")
    print(f"  {get_python_command()} sophia_launcher.py")
    print(f"  {get_python_command()} -c \"from CONSCIOUSNESS_MEMORY import MemoryBridge\"")

if __name__ == "__main__":
    main()