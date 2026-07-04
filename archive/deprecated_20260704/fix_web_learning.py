#!/usr/bin/env python3
"""
Debug script to find where the regex error is occurring
"""

import traceback
from enhanced_autonomous_learner import EnhancedAutonomousLearner

# Test with a simple URL first
test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

print(f"Testing URL processing for: {test_url}")
print("="*60)

# Initialize learner
learner = EnhancedAutonomousLearner()

# Try to process the URL directly
try:
    print("\n1. Testing fetch_raw_html...")
    from web_parser import fetch_raw_html
    html = fetch_raw_html(test_url)
    if html:
        print("   ✅ HTML fetched successfully")
    else:
        print("   ❌ Failed to fetch HTML")
        
    print("\n2. Testing clean_html_to_text...")
    from web_parser import clean_html_to_text
    text = clean_html_to_text(html)
    if text:
        print(f"   ✅ Text extracted: {len(text)} characters")
    else:
        print("   ❌ Failed to extract text")
        
    print("\n3. Testing process_url method...")
    learner.process_url(test_url, {"context": "test", "depth": 0})
    print("   ✅ URL processed successfully")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    
    # Try to find where in the stack trace the regex error occurs
    import sys
    tb = sys.exc_info()[2]
    print("\nAnalyzing stack frames:")
    while tb is not None:
        frame = tb.tb_frame
        print(f"  File: {frame.f_code.co_filename}, Line: {tb.tb_lineno}, Function: {frame.f_code.co_name}")
        tb = tb.tb_next