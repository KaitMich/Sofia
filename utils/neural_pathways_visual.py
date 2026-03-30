#!/usr/bin/env python3
"""
Neural Pathways Visualization
Creates visual representations of the AI system's dependency structure
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict, Counter
import networkx as nx

def load_analysis():
    """Load the dependency analysis"""
    with open('ai_dependency_analysis.json', 'r') as f:
        return json.load(f)

def create_neural_pathway_graph(analysis):
    """Create a network graph showing neural pathways"""
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Get dependency graph from analysis
    dep_graph = analysis['dependency_map']['dependency_graph']
    
    # Add nodes and edges
    for source, targets in dep_graph.items():
        source_clean = source.replace('.py', '')
        G.add_node(source_clean)
        
        for target in targets:
            target_clean = target.replace('.py', '')
            G.add_edge(source_clean, target_clean)
    
    return G

def categorize_nodes(analysis):
    """Categorize nodes by their function"""
    categories = {
        'memory': ['unified_memory', 'memory_analytics', 'memory_evolution_engine', 
                  'memory_maintenance', 'memory_optimizer', 'symbol_memory'],
        'security': ['quarantine_layer', 'linguistic_warfare', 'alphawall', 
                    'adaptive_quarantine_layer', 'adaptive_alphawall'],
        'processing': ['processing_nodes', 'parser', 'emotion_handler', 'vector_engine',
                      'unified_weight_system', 'unified_symbol_system'],
        'interface': ['talk_to_ai', 'cli', 'web_parser', 'visualization_prep', 'main'],
        'learning': ['evolution_anchor', 'weight_evolution', 'adaptive_migration',
                    'reverse_migration', 'brain_metrics'],
        'analysis': ['symbol_cluster', 'trail_graph', 'symbol_drift_plot', 
                    'symbol_emotion_cluster', 'system_analytics'],
        'orchestration': ['unified_orchestration', 'link_evaluator', 'decision_validator',
                         'context_engine']
    }
    
    node_categories = {}
    for category, nodes in categories.items():
        for node in nodes:
            node_categories[node] = category
    
    return node_categories, categories

def visualize_critical_pathways(analysis):
    """Create visualization focusing on critical files"""
    
    critical_files = [
        'memory_optimizer', 'memory_analytics', 'memory_evolution_engine',
        'unified_memory', 'symbol_memory', 'processing_nodes'
    ]
    
    # Create subgraph with critical files and their immediate connections
    G = create_neural_pathway_graph(analysis)
    
    # Get nodes to include (critical files + their immediate neighbors)
    nodes_to_include = set(critical_files)
    for critical in critical_files:
        if critical in G:
            # Add predecessors (files that import this critical file)
            nodes_to_include.update(G.predecessors(critical))
            # Add successors (files this critical file imports)
            nodes_to_include.update(G.successors(critical))
    
    # Create subgraph
    G_critical = G.subgraph(nodes_to_include)
    
    # Categorize nodes
    node_categories, categories = categorize_nodes(analysis)
    
    # Color mapping
    colors = {
        'memory': '#FF6B6B',      # Red - Core memory
        'security': '#4ECDC4',    # Teal - Security
        'processing': '#45B7D1',  # Blue - Processing
        'interface': '#96CEB4',   # Green - Interface
        'learning': '#FFEAA7',    # Yellow - Learning
        'analysis': '#DDA0DD',    # Plum - Analysis
        'orchestration': '#F39C12' # Orange - Orchestration
    }
    
    # Create figure
    plt.figure(figsize=(16, 12))
    
    # Use hierarchical layout
    pos = nx.spring_layout(G_critical, k=3, iterations=50)
    
    # Draw nodes by category
    for category, node_list in categories.items():
        category_nodes = [n for n in G_critical.nodes() if node_categories.get(n) == category]
        if category_nodes:
            nx.draw_networkx_nodes(G_critical, pos, 
                                 nodelist=category_nodes,
                                 node_color=colors.get(category, '#CCCCCC'),
                                 node_size=1000,
                                 alpha=0.8)
    
    # Highlight critical files
    critical_in_graph = [n for n in critical_files if n in G_critical.nodes()]
    nx.draw_networkx_nodes(G_critical, pos,
                         nodelist=critical_in_graph,
                         node_color='gold',
                         node_size=1500,
                         alpha=0.9,
                         edgecolors='black',
                         linewidths=2)
    
    # Draw edges
    nx.draw_networkx_edges(G_critical, pos,
                         edge_color='gray',
                         arrows=True,
                         arrowsize=20,
                         alpha=0.6,
                         width=1.5)
    
    # Draw labels
    nx.draw_networkx_labels(G_critical, pos, font_size=8, font_weight='bold')
    
    # Create legend
    legend_elements = []
    for category, color in colors.items():
        legend_elements.append(mpatches.Patch(color=color, label=category.title()))
    
    legend_elements.append(mpatches.Patch(color='gold', label='Critical Files'))
    
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('AI System Neural Pathways - Critical Components\n(Each arrow represents a dependency/import)', 
              fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('neural_pathways_critical.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_dependency_heatmap(analysis):
    """Create a heatmap showing dependency intensity"""
    
    # Get dependency counts
    dep_graph = analysis['dependency_map']['dependency_graph']
    
    # Count incoming dependencies (how many files depend on each file)
    incoming_deps = Counter()
    outgoing_deps = Counter()
    
    for source, targets in dep_graph.items():
        source_clean = source.replace('.py', '')
        outgoing_deps[source_clean] = len(targets)
        
        for target in targets:
            target_clean = target.replace('.py', '')
            incoming_deps[target_clean] += 1
    
    # Get top files by dependency count
    top_files = sorted(incoming_deps.items(), key=lambda x: x[1], reverse=True)[:15]
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Incoming dependencies (how many files depend on this file)
    files, counts = zip(*top_files)
    bars1 = ax1.barh(range(len(files)), counts, color='#FF6B6B', alpha=0.7)
    ax1.set_yticks(range(len(files)))
    ax1.set_yticklabels(files, fontsize=10)
    ax1.set_xlabel('Number of files that depend on this file')
    ax1.set_title('Most Critical Files\n(Incoming Dependencies)', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars1, counts)):
        ax1.text(count + 0.1, i, str(count), va='center', fontweight='bold')
    
    # Outgoing dependencies (how many files this file imports)
    top_outgoing = sorted(outgoing_deps.items(), key=lambda x: x[1], reverse=True)[:15]
    files2, counts2 = zip(*top_outgoing)
    bars2 = ax2.barh(range(len(files2)), counts2, color='#4ECDC4', alpha=0.7)
    ax2.set_yticks(range(len(files2)))
    ax2.set_yticklabels(files2, fontsize=10)
    ax2.set_xlabel('Number of files this file imports')
    ax2.set_title('Most Connected Files\n(Outgoing Dependencies)', fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars2, counts2)):
        ax2.text(count + 0.1, i, str(count), va='center', fontweight='bold')
    
    plt.suptitle('AI System Dependency Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('dependency_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_circular_dependency_visualization(analysis):
    """Visualize circular dependencies"""
    
    # For now, we know there's one circular dependency from the analysis
    circular_files = ['unified_memory', 'linguistic_warfare', 'symbol_memory']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create a circle layout for the circular dependency
    import math
    n = len(circular_files)
    angles = [i * 2 * math.pi / n for i in range(n)]
    radius = 2
    
    positions = {}
    for i, file in enumerate(circular_files):
        x = radius * math.cos(angles[i])
        y = radius * math.sin(angles[i])
        positions[file] = (x, y)
    
    # Draw the circular dependency
    G = nx.DiGraph()
    for i in range(n):
        current = circular_files[i]
        next_file = circular_files[(i + 1) % n]
        G.add_edge(current, next_file)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, positions,
                         node_color='red',
                         node_size=2000,
                         alpha=0.8)
    
    # Draw edges with curved arrows to show the cycle
    nx.draw_networkx_edges(G, positions,
                         edge_color='red',
                         arrows=True,
                         arrowsize=30,
                         width=3,
                         alpha=0.8,
                         connectionstyle="arc3,rad=0.1")
    
    # Draw labels
    nx.draw_networkx_labels(G, positions, font_size=10, font_weight='bold')
    
    ax.set_title('⚠️ Circular Dependency Detected\n' + 
                'unified_memory.py → linguistic_warfare.py → symbol_memory.py → unified_memory.py',
                fontsize=14, fontweight='bold', color='red')
    
    # Add warning text
    ax.text(0, -3, 'This circular dependency can cause:\n' +
                  '• Import errors\n' +
                  '• Initialization problems\n' +
                  '• Maintenance difficulties\n\n' +
                  'Recommendation: Break the cycle by refactoring\n' +
                  'the symbol_memory → unified_memory connection',
            ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('circular_dependency_warning.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all visualizations"""
    print("🎨 Creating neural pathway visualizations...")
    
    # Load analysis
    analysis = load_analysis()
    
    try:
        # Create critical pathways visualization
        print("  📊 Creating critical pathways network...")
        visualize_critical_pathways(analysis)
        print("     ✅ Saved: neural_pathways_critical.png")
        
        # Create dependency heatmap
        print("  📈 Creating dependency heatmap...")
        create_dependency_heatmap(analysis)
        print("     ✅ Saved: dependency_heatmap.png")
        
        # Create circular dependency warning
        print("  ⚠️ Creating circular dependency visualization...")
        create_circular_dependency_visualization(analysis)
        print("     ✅ Saved: circular_dependency_warning.png")
        
        print("\n✅ All visualizations created successfully!")
        print("\nGenerated files:")
        print("  📊 neural_pathways_critical.png - Main system architecture")
        print("  📈 dependency_heatmap.png - Dependency analysis")
        print("  ⚠️ circular_dependency_warning.png - Problem areas")
        
    except ImportError as e:
        print(f"❌ Visualization libraries not available: {e}")
        print("Install with: pip install matplotlib networkx")

if __name__ == "__main__":
    main()