> **ARCHIVED DOCUMENT -- CORRECTED March 27, 2026**
> See [SOPHIA_TRUTH_FRAMEWORK.md](/docs/SOPHIA_TRUTH_FRAMEWORK.md) for authoritative corrections.
> Key corrections for this file: Technical utility descriptions are valid. References to
> "AI system" describe software components. Bridge = intake, not temporary staging.

# Utils Directory

This directory contains analysis, debug, and utility tools for the AI system. These tools provide insights into system behavior, help with debugging, and support data visualization.

## Analysis Tools

### analyze_dependencies.py
Analyzes import dependencies across the codebase to identify potential circular dependencies and coupling issues.

### analyze_imports.py
Examines import patterns and provides recommendations for import optimization and organization.

### create_dependency_graph.py
Generates visual dependency graphs showing relationships between modules and components.

### create_text_dependency_graph.py
Creates text-based dependency representations for systems without graphical capabilities.

### system_analytics.py
Provides comprehensive system analytics including memory usage, performance metrics, and health indicators.

## Debugging Tools

### debug_regex_error.py
Helps debug regular expression issues in pattern matching and text processing.

### fix_regex_escaping.py
Utility for fixing regex escaping issues in string patterns.

### fix_web_learning.py
Debug tool for web learning and content processing issues.

### inspect_vectors.py
Tool for inspecting and analyzing vector embeddings and their properties.

## Visualization Tools

### neural_pathways_visual.py
Creates visualizations of neural pathways and decision flows within the AI system.

### symbol_drift_plot.py
Generates plots showing how symbol meanings and associations drift over time.

### visualization_prep.py
Enhanced frontend visualization preparation layer with tripartite integration. Prepares text and processing results for frontend display.

### graph_visualizer.py
General-purpose graph visualization tool for displaying network relationships.

## Processing Utilities

### regex_utils.py
Collection of regex utilities and patterns for text processing.

### smart_link_processor.py
Intelligent link processing for web content analysis and evaluation.

### link_evaluator.py
Evaluates links and content for relevance, safety, and routing decisions.

## Memory Management

### memory_migrations.py
Comprehensive memory migration utilities including:
- Tripartite memory migration from vector storage
- Vector upgrade utilities with enhanced embeddings
- Reverse migration audit for catching misclassifications
- Unified migration system with data consolidation
- Trail log analysis for migration insights

### start_learning.py
Utility to start learning sessions and initialize the AI system.

### view_learning_data.py
Tool for viewing and analyzing accumulated learning data.

## Usage

Most utilities can be run standalone or imported as modules:

```python
# Example: Using memory migrations
from utils.memory_migrations import run_tripartite_migration
success = run_tripartite_migration()

# Example: Using visualization prep
from utils.visualization_prep import visualize_processing_result
viz_data = visualize_processing_result(text, processing_result)

# Example: Using system analytics
from utils.system_analytics import SystemAnalytics
analytics = SystemAnalytics()
health_report = analytics.generate_health_report()
```

## Dependencies

These utilities may require additional dependencies from the main system:
- Core AI modules (parser, emotion_handler, etc.)
- Vector processing libraries (numpy, sklearn)
- Visualization libraries (matplotlib, networkx)
- Web processing tools (requests, beautifulsoup4)

## Notes

- Tools are designed to be non-intrusive and safe to run on production systems
- Most analysis tools provide read-only insights without modifying system state
- Migration tools include backup and safety mechanisms
- Visualization tools support multiple output formats (HTML, JSON, images)