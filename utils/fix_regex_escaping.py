#!/usr/bin/env python3
"""
Fix for regex escaping issues in enhanced_autonomous_learner.py
"""

import re

def find_and_fix_regex_issues():
    """Find places where strings might be used as regex patterns without escaping"""
    
    # Read the enhanced_autonomous_learner.py file
    with open('enhanced_autonomous_learner.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for common patterns where strings might be used as regex
    patterns_to_check = [
        # re.search(variable, ...)
        r're\.search\s*\(\s*([a-zA-Z_]\w*)\s*,',
        # re.match(variable, ...)
        r're\.match\s*\(\s*([a-zA-Z_]\w*)\s*,',
        # re.findall(variable, ...)
        r're\.findall\s*\(\s*([a-zA-Z_]\w*)\s*,',
        # re.compile(variable)
        r're\.compile\s*\(\s*([a-zA-Z_]\w*)\s*\)',
    ]
    
    print("Checking for potential regex issues...")
    found_issues = False
    
    for pattern in patterns_to_check:
        matches = re.finditer(pattern, content)
        for match in matches:
            var_name = match.group(1)
            print(f"Found potential issue: {match.group(0)} - variable '{var_name}' used as regex pattern")
            found_issues = True
    
    if not found_issues:
        print("No obvious regex issues found in enhanced_autonomous_learner.py")
    
    # Check other files that might have issues
    files_to_check = [
        'linguistic_warfare.py',
        'parser.py',
        'smart_link_processor.py',
        'curiosity_engine.py',
        'learning_progression_tracker.py'
    ]
    
    for filename in files_to_check:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for Wikipedia-specific processing
            if 'wikipedia' in content.lower() or '/wiki/' in content:
                print(f"\nChecking {filename} for Wikipedia-related regex...")
                
                # Check if article titles are extracted and used
                if 'split' in content and 'wiki' in content:
                    print(f"  ⚠️ {filename} contains 'split' and 'wiki' - might extract article titles")
                
                # Check for unescaped pattern usage
                for pattern in patterns_to_check:
                    if re.search(pattern, content):
                        print(f"  ⚠️ {filename} might use variables as regex patterns")
                        
        except FileNotFoundError:
            continue
    
    print("\n" + "="*60)
    print("RECOMMENDATION: Add re.escape() when using dynamic strings as patterns")
    print("Example fix:")
    print("  Before: re.search(title, text)")
    print("  After:  re.search(re.escape(title), text)")

if __name__ == "__main__":
    find_and_fix_regex_issues()