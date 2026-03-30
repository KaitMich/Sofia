#!/usr/bin/env python3
"""
Regex utilities for safe pattern matching and compilation.
Prevents regex errors like 'unterminated subpattern' from crashing the application.
"""
import re
from typing import Optional, List, Pattern, Union

def safe_compile(pattern: str) -> Optional[Pattern]:
    """
    Safely compile a regex pattern with error handling.
    
    Args:
        pattern: The regex pattern string to compile
        
    Returns:
        Compiled regex pattern or None if compilation fails
    """
    try:
        return re.compile(pattern)
    except re.error as e:
        print(f"[REGEX_ERROR] Failed to compile pattern '{pattern[:50]}...': {e}")
        return None

def safe_search(pattern: str, text: str, flags: int = 0) -> bool:
    """
    Safely search for a pattern in text with error handling.
    
    Args:
        pattern: The regex pattern string
        text: The text to search in
        flags: Optional regex flags
        
    Returns:
        True if pattern found, False if not found or pattern invalid
    """
    try:
        return re.search(pattern, text, flags) is not None
    except re.error as e:
        print(f"[REGEX_ERROR] Search failed for pattern '{pattern[:50]}...': {e}")
        # Fallback to simple string matching for basic patterns
        if pattern.startswith('r\'') and pattern.endswith('\''):
            # Remove r'' wrapper and try simple matching
            clean_pattern = pattern[2:-1]
            return clean_pattern in text
        return False

def safe_findall(pattern: str, text: str, flags: int = 0) -> List[str]:
    """
    Safely find all matches of a pattern in text with error handling.
    
    Args:
        pattern: The regex pattern string
        text: The text to search in
        flags: Optional regex flags
        
    Returns:
        List of matches or empty list if pattern invalid
    """
    try:
        return re.findall(pattern, text, flags)
    except re.error as e:
        print(f"[REGEX_ERROR] Findall failed for pattern '{pattern[:50]}...': {e}")
        return []

def safe_match(pattern: str, text: str, flags: int = 0) -> bool:
    """
    Safely match a pattern at the beginning of text with error handling.
    
    Args:
        pattern: The regex pattern string
        text: The text to match against
        flags: Optional regex flags
        
    Returns:
        True if pattern matches, False if not or pattern invalid
    """
    try:
        return re.match(pattern, text, flags) is not None
    except re.error as e:
        print(f"[REGEX_ERROR] Match failed for pattern '{pattern[:50]}...': {e}")
        return False

def validate_pattern(pattern: str) -> bool:
    """
    Validate a regex pattern without using it.
    
    Args:
        pattern: The regex pattern to validate
        
    Returns:
        True if pattern is valid, False otherwise
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False

def fix_common_pattern_errors(pattern: str) -> str:
    """
    Attempt to fix common regex pattern errors.
    
    Args:
        pattern: The potentially malformed regex pattern
        
    Returns:
        Fixed pattern or original if no fixes could be applied
    """
    fixed = pattern
    
    # Fix unmatched opening parentheses
    open_parens = fixed.count('(')
    close_parens = fixed.count(')')
    if open_parens > close_parens:
        fixed += ')' * (open_parens - close_parens)
    
    # Fix unmatched opening brackets
    open_brackets = fixed.count('[')
    close_brackets = fixed.count(']')
    if open_brackets > close_brackets:
        fixed += ']' * (open_brackets - close_brackets)
    
    # Fix unmatched opening braces
    open_braces = fixed.count('{')
    close_braces = fixed.count('}')
    if open_braces > close_braces:
        fixed += '}' * (open_braces - close_braces)
    
    return fixed

# Pre-compiled safe patterns for common URL validation
SAFE_URL_PATTERNS = {
    'http_https': r'^https?://',
    'domain': r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$',
    'ip_address': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
}

# Compile all safe patterns on import
COMPILED_SAFE_PATTERNS = {}
for name, pattern in SAFE_URL_PATTERNS.items():
    compiled = safe_compile(pattern)
    if compiled:
        COMPILED_SAFE_PATTERNS[name] = compiled

def is_valid_url(url: str) -> bool:
    """Check if a URL is valid using safe patterns."""
    if not url:
        return False
    
    http_pattern = COMPILED_SAFE_PATTERNS.get('http_https')
    if http_pattern and http_pattern.match(url):
        return True
    
    # Fallback to simple string check
    return url.startswith(('http://', 'https://'))

def is_valid_domain(domain: str) -> bool:
    """Check if a domain is valid using safe patterns."""
    if not domain:
        return False
    
    domain_pattern = COMPILED_SAFE_PATTERNS.get('domain')
    if domain_pattern and domain_pattern.match(domain):
        return True
    
    # Fallback to simple validation
    return '.' in domain and len(domain) > 3

if __name__ == "__main__":
    # Test the utility functions
    print("Testing regex utility functions...")
    
    # Test valid patterns
    print(f"Valid URL pattern: {safe_search(r'https?://', 'https://example.com')}")
    print(f"Valid domain check: {is_valid_domain('example.com')}")
    
    # Test invalid patterns
    print(f"Invalid pattern test: {safe_search('(?:invalid(', 'test text')}")
    
    # Test pattern fixing
    broken_pattern = "(?:test|more("
    fixed_pattern = fix_common_pattern_errors(broken_pattern)
    print(f"Fixed pattern: '{broken_pattern}' -> '{fixed_pattern}'")
    print(f"Fixed pattern valid: {validate_pattern(fixed_pattern)}")