#!/usr/bin/env python3
"""
Personal Insight Generator - Compatibility Wrapper

This module provides backwards-compatible imports for PersonalInsightGenerator.
The main implementation lives in INSIGHT_RELEVANCE.py (consolidated file).

This wrapper:
1. Re-exports PersonalInsightGenerator from INSIGHT_RELEVANCE.py
2. Maintains backwards compatibility with existing imports
3. Prevents ModuleNotFoundError when importing
"""

# Re-export PersonalInsightGenerator from the consolidated file
from sofia.core.INSIGHT_RELEVANCE import PersonalInsightGenerator

__all__ = ['PersonalInsightGenerator']
