#!/usr/bin/env python3
"""
Test script for web learning with simple URLs that don't have special characters
"""

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

print("\n✅ Test complete!")