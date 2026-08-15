#!/usr/bin/env python3
"""
Motivational Content Evaluator - Compatibility Wrapper

This module provides backwards-compatible imports for MotivationalContentEvaluator.
The main implementation lives in CURIOSITY_MOTIVATION.py (consolidated file).

This wrapper:
1. Re-exports MotivationalContentEvaluator from CURIOSITY_MOTIVATION.py
2. Maintains backwards compatibility with existing imports
3. Prevents ModuleNotFoundError when importing
"""

# Re-export MotivationalContentEvaluator from the consolidated file
from sofia.core.CURIOSITY_MOTIVATION import MotivationalContentEvaluator

__all__ = ['MotivationalContentEvaluator']
