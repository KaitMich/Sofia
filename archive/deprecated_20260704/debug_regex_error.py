#!/usr/bin/env python3
"""
Debug script to find the exact location of the regex error
"""

import sys
import re

# Monkey-patch re.compile to track what patterns are being compiled
original_compile = re.compile
failed_patterns = []

def debug_compile(pattern, flags=0):
    try:
        return original_compile(pattern, flags)
    except re.error as e:
        print(f"\n❌ REGEX ERROR FOUND!")
        print(f"   Pattern: {pattern}")
        print(f"   Error: {e}")
        print(f"   Stack trace:")
        import traceback
        traceback.print_stack()
        failed_patterns.append((pattern, str(e)))
        raise

re.compile = debug_compile

# Now run the enhanced autonomous learner
print("Starting enhanced autonomous learner with regex debugging...")
print("="*60)

try:
    from enhanced_autonomous_learner import start_massive_web_learning
    
    seed_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence"
    ]
    
    learner = start_massive_web_learning(
        seed_urls=seed_urls,
        target_urls=1,  # Just process 1 URL
        focus="test"
    )
except Exception as e:
    print(f"\nMain error: {e}")
    
print(f"\nTotal failed patterns: {len(failed_patterns)}")
for pattern, error in failed_patterns:
    print(f"  Pattern: {pattern}")
    print(f"  Error: {error}")