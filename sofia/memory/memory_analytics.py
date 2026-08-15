# memory_analytics.py - Deep Analytics and Observability System

from datetime import datetime
from collections import Counter
import json
from pathlib import Path
from typing import Dict, List, Any

# Import the Memory Bridge for compatibility
try:
    from sofia.core.CONSCIOUSNESS_MEMORY import MemoryBridge
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False

class MemoryAnalyzer:
    """
    Provides deep analytics and insights into memory distribution,
    patterns, and evolution over time.
    """
    
    def __init__(self, memory, data_dir="data"):
        self.memory = memory
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.analytics_file = self.data_dir / "memory_analytics_history.json"
        
    def get_memory_stats(self):
        """Get comprehensive statistics about memory distribution"""
        # Use bridge for compatibility with different memory system versions
        if BRIDGE_AVAILABLE:
            bridge = MemoryBridge(self.memory)
            counts = bridge.get_counts()
        else:
            counts = self.memory.get_counts()
        
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'distribution': {
                'logic': {
                    'count': counts['logic'],
                    'percentage': (counts['logic'] / max(1, counts['total'])) * 100,
                    'avg_score': self._calculate_avg_score(self.memory.logic_memory, 'logic_score'),
                    'avg_age_days': self._calculate_avg_age(self.memory.logic_memory),
                    'stability': self._calculate_stability(self.memory.logic_memory)
                },
                'symbolic': {
                    'count': counts['symbolic'],
                    'percentage': (counts['symbolic'] / max(1, counts['total'])) * 100,
                    'avg_score': self._calculate_avg_score(self.memory.symbolic_memory, 'symbolic_score'),
                    'avg_age_days': self._calculate_avg_age(self.memory.symbolic_memory),
                    'stability': self._calculate_stability(self.memory.symbolic_memory)
                },
                'bridge': {
                    'count': counts['bridge'],
                    'percentage': (counts['bridge'] / max(1, counts['total'])) * 100,
                    'avg_logic_score': self._calculate_avg_score(self.memory.bridge_memory, 'logic_score'),
                    'avg_symbolic_score': self._calculate_avg_score(self.memory.bridge_memory, 'symbolic_score'),
                    'avg_age_days': self._calculate_avg_age(self.memory.bridge_memory),
                    'stability': self._calculate_stability(self.memory.bridge_memory),
                    'volatility': self._calculate_volatility(self.memory.bridge_memory)
                }
            },
            'total_items': counts['total'],
            'health_indicators': self._calculate_health_indicators(counts)
        }
        
        return stats
        
    def _calculate_avg_score(self, items, score_key):
        """Calculate average score for items"""
        if not items:
            return 0.0
        scores = [item.get(score_key, 0) for item in items]
        return sum(scores) / len(scores) if scores else 0.0
        
    def _calculate_avg_age(self, items):
        """Calculate average age in days"""
        if not items:
            return 0.0
            
        now = datetime.utcnow()
        ages = []
        
        for item in items:
            if 'stored_at' in item:
                try:
                    stored = datetime.fromisoformat(item['stored_at'].replace('Z', '+00:00'))
                    age_days = (now - stored).days
                    ages.append(age_days)
                except:
                    pass
                    
        return sum(ages) / len(ages) if ages else 0.0
        
    def _calculate_stability(self, items):
        """Calculate overall stability of items (0-1)"""
        if not items:
            return 1.0
            
        stable_count = 0
        for item in items:
            stability = self.memory.get_item_stability(item)
            if stability['is_stable']:
                stable_count += 1
                
        return stable_count / len(items)
        
    def _calculate_volatility(self, items):
        """Calculate volatility (frequency of decision changes)"""
        if not items:
            return 0.0
            
        volatilities = []
        for item in items:
            history = item.get('decision_history', [])
            if len(history) >= 2:
                # Count decision changes
                changes = sum(1 for i in range(1, len(history)) 
                            if history[i]['decision'] != history[i-1]['decision'])
                volatility = changes / (len(history) - 1)
                volatilities.append(volatility)
                
        return sum(volatilities) / len(volatilities) if volatilities else 0.0
        
    def _calculate_health_indicators(self, counts):
        """Calculate system health indicators"""
        total = counts['total']
        if total == 0:
            return {
                'status': 'empty', 
                'issues': ['No items in memory'],
                'recommendations': ['Process some content to build knowledge base']
            }
            
        bridge_pct = (counts['bridge'] / total) * 100
        
        indicators = {
            'status': 'healthy',
            'bridge_percentage': bridge_pct,
            'issues': [],
            'recommendations': []
        }
        
        # Check for issues
        if bridge_pct > 50:
            indicators['status'] = 'needs_attention'
            indicators['issues'].append(f'High bridge percentage: {bridge_pct:.1f}%')
            indicators['recommendations'].append('Consider lowering migration threshold')
            
        if counts['logic'] == 0 or counts['symbolic'] == 0:
            indicators['issues'].append('Severe imbalance: one memory type is empty')
            indicators['recommendations'].append('Review classification criteria')
            
        if total < 10:
            indicators['issues'].append('Very few items in memory')
            indicators['recommendations'].append('Process more content to build knowledge')
            
        return indicators
        
    def analyze_bridge_patterns(self):
        """Deep analysis of bridge memory patterns"""
        bridge_items = self.memory.bridge_memory
        
        if not bridge_items:
            return {
                'total': 0,
                'patterns': {},
                'insights': ['Bridge memory is empty']
            }
            
        analysis = {
            'total': len(bridge_items),
            'patterns': {},
            'insights': [],
            'keyword_analysis': {},
            'score_distribution': {}
        }
        
        # Categorize patterns
        patterns = {
            'volatile': [],  # Frequently changing classification
            'balanced': [],  # Similar logic/symbolic scores
            'conflicted': [],  # High scores in both
            'weak': [],  # Low scores in both
            'stuck': []  # Been in bridge for a long time
        }
        
        # Analyze each item
        for item in bridge_items:
            logic_score = item.get('logic_score', 0)
            symbolic_score = item.get('symbolic_score', 0)
            
            # Check patterns
            stability = self.memory.get_item_stability(item)
            
            if len(stability['decision_counts']) >= 3:
                patterns['volatile'].append(item)
                
            if abs(logic_score - symbolic_score) < 1.0:
                patterns['balanced'].append(item)
                
            if logic_score > 6 and symbolic_score > 6:
                patterns['conflicted'].append(item)
                
            if logic_score < 3 and symbolic_score < 3:
                patterns['weak'].append(item)
                
            # Check age
            if 'stored_at' in item:
                try:
                    stored = datetime.fromisoformat(item['stored_at'].replace('Z', '+00:00'))
                    age_days = (datetime.utcnow() - stored).days
                    if age_days > 7:
                        patterns['stuck'].append(item)
                except:
                    pass
                    
        # Store pattern counts
        analysis['patterns'] = {
            name: len(items) for name, items in patterns.items()
        }
        
        # Extract keywords from bridge items
        all_text = ' '.join(item.get('text', '') for item in bridge_items)
        # Simple keyword extraction (in real system, use proper NLP)
        words = all_text.lower().split()
        word_freq = Counter(word for word in words if len(word) > 4)
        analysis['keyword_analysis']['top_keywords'] = word_freq.most_common(10)
        
        # Score distribution
        analysis['score_distribution'] = {
            'avg_logic_score': self._calculate_avg_score(bridge_items, 'logic_score'),
            'avg_symbolic_score': self._calculate_avg_score(bridge_items, 'symbolic_score'),
            'high_both': len(patterns['conflicted']),
            'low_both': len(patterns['weak'])
        }
        
        # Generate insights
        if patterns['volatile']:
            pct = (len(patterns['volatile']) / len(bridge_items)) * 100
            analysis['insights'].append(
                f"{pct:.1f}% of bridge items are volatile (frequently changing classification)"
            )
            
        if patterns['stuck']:
            analysis['insights'].append(
                f"{len(patterns['stuck'])} items have been in bridge for over 7 days"
            )
            
        if patterns['conflicted']:
            analysis['insights'].append(
                f"{len(patterns['conflicted'])} items have high scores in both logic and symbolic"
            )
            
        if analysis['score_distribution']['avg_logic_score'] > analysis['score_distribution']['avg_symbolic_score'] + 2:
            analysis['insights'].append(
                "Bridge items lean heavily toward logic - consider adjusting weights"
            )
            
        return analysis
        
    def generate_evolution_report(self, migration_summary=None, audit_summary=None):
        """Generate comprehensive evolution report"""
        stats = self.get_memory_stats()
        bridge_analysis = self.analyze_bridge_patterns()
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'summary': {
                'total_items': stats['total_items'],
                'distribution': {
                    'logic': f"{stats['distribution']['logic']['count']} ({stats['distribution']['logic']['percentage']:.1f}%)",
                    'symbolic': f"{stats['distribution']['symbolic']['count']} ({stats['distribution']['symbolic']['percentage']:.1f}%)",
                    'bridge': f"{stats['distribution']['bridge']['count']} ({stats['distribution']['bridge']['percentage']:.1f}%)"
                }
            },
            'health': stats['health_indicators'],
            'bridge_analysis': bridge_analysis,
            'stability_metrics': {
                'logic_stability': stats['distribution']['logic']['stability'],
                'symbolic_stability': stats['distribution']['symbolic']['stability'],
                'bridge_stability': stats['distribution']['bridge']['stability'],
                'bridge_volatility': stats['distribution']['bridge']['volatility']
            }
        }
        
        # Add migration info if provided
        if migration_summary:
            report['migrations'] = migration_summary
            
        if audit_summary:
            report['audit'] = audit_summary
            
        # Save to history
        self._save_report(report)
        
        return report
        
    def _save_report(self, report):
        """Save report to history file"""
        history = []
        
        # Load existing history
        if self.analytics_file.exists():
            try:
                with open(self.analytics_file, 'r') as f:
                    history = json.load(f)
            except:
                pass
                
        # Add new report and keep last 100
        history.append(report)
        history = history[-100:]
        
        # Save
        with open(self.analytics_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    def print_report(self, report):
        """Pretty print the evolution report"""
        print("\n" + "="*60)
        print("📊 MEMORY EVOLUTION REPORT")
        print("="*60)
        
        print(f"\n📅 Generated: {report['timestamp']}")
        
        print("\n📈 Distribution:")
        for mem_type, info in report['summary']['distribution'].items():
            print(f"  {mem_type.capitalize()}: {info}")
            
        print(f"\n💚 Health Status: {report['health']['status'].upper()}")
        if report['health']['issues']:
            print("  Issues:")
            for issue in report['health']['issues']:
                print(f"    ⚠️  {issue}")
        
        # FIXED: Safely check for recommendations
        if report['health'].get('recommendations'):
            print("  Recommendations:")
            for rec in report['health']['recommendations']:
                print(f"    💡 {rec}")
                
        print("\n🌉 Bridge Analysis:")
        print(f"  Total items: {report['bridge_analysis']['total']}")
        if report['bridge_analysis']['patterns']:
            print("  Patterns:")
            for pattern, count in report['bridge_analysis']['patterns'].items():
                if count > 0:
                    print(f"    {pattern}: {count}")
                    
        if report['bridge_analysis']['insights']:
            print("  Insights:")
            for insight in report['bridge_analysis']['insights']:
                print(f"    → {insight}")
                
        print("\n📊 Stability Metrics:")
        print(f"  Logic: {report['stability_metrics']['logic_stability']:.2%}")
        print(f"  Symbolic: {report['stability_metrics']['symbolic_stability']:.2%}")
        print(f"  Bridge: {report['stability_metrics']['bridge_stability']:.2%}")
        print(f"  Bridge Volatility: {report['stability_metrics']['bridge_volatility']:.2%}")
        
        if 'migrations' in report:
            print(f"\n🔄 Migrations: {report['migrations'].get('total_migrated', 0)} items")
            
        if 'audit' in report:
            print(f"\n🔍 Audit: {report['audit'].get('total_reversed', 0)} items reversed")
            
        print("\n" + "="*60)
    
    def analyze_symbol_clusters(self, max_features: int = 300, n_clusters: int = None, show_visualization: bool = False) -> Dict[str, Any]:
        """
        Analyze symbol clustering patterns in memory using vector data.
        Integrated from symbol_cluster.py functionality.
        
        Args:
            max_features: Maximum features for TfidfVectorizer
            n_clusters: Number of clusters (auto-determined if None)
            show_visualization: Whether to display matplotlib visualization
            
        Returns:
            Dictionary containing cluster analysis results
        """
        try:
            # Access vector data from unified memory
            if hasattr(self.memory, 'vector_data'):
                vector_data = self.memory.vector_data
            else:
                # Try to get from unified memory system
                try:
                    from sofia.core.unified_memory import get_unified_memory
                    unified_memory = get_unified_memory()
                    vector_data = getattr(unified_memory, 'vector_data', [])
                except ImportError:
                    vector_data = []
            
            # Handle both dict and list memory formats
            if isinstance(vector_data, list):
                entries = vector_data
            elif isinstance(vector_data, dict):
                entries = list(vector_data.values())
            else:
                entries = []
            
            if len(entries) < 3:
                return {
                    "error": "Not enough entries for clustering analysis",
                    "entry_count": len(entries),
                    "min_required": 3
                }
            
            # Extract texts
            texts = []
            valid_entries = []
            
            for entry in entries:
                text = entry.get("text", "")
                if text and len(text.strip()) > 10:  # Filter very short texts
                    texts.append(text)
                    valid_entries.append(entry)
            
            if len(texts) < 3:
                return {
                    "error": "Not enough valid text entries for clustering",
                    "valid_entries": len(texts),
                    "total_entries": len(entries)
                }
            
            # Perform clustering analysis
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.cluster import KMeans
            import numpy as np
            
            # Vectorize texts
            vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
            X = vectorizer.fit_transform(texts).toarray()
            
            # Determine optimal number of clusters
            if n_clusters is None:
                n_clusters = min(5, len(texts) // 2)
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            
            # Analyze clusters
            cluster_analysis = {
                "timestamp": datetime.utcnow().isoformat(),
                "total_entries": len(entries),
                "valid_text_entries": len(texts),
                "n_clusters": n_clusters,
                "cluster_results": {},
                "cluster_statistics": {},
                "top_features_per_cluster": {}
            }
            
            # Group texts by cluster
            from collections import defaultdict
            cluster_groups = defaultdict(list)
            cluster_entries = defaultdict(list)
            
            for idx, label in enumerate(labels):
                cluster_groups[label].append(texts[idx])
                cluster_entries[label].append(valid_entries[idx])
            
            # Analyze each cluster
            feature_names = vectorizer.get_feature_names_out()
            
            for cluster_id in range(n_clusters):
                cluster_texts = cluster_groups[cluster_id]
                cluster_data = cluster_entries[cluster_id]
                
                if not cluster_texts:
                    continue
                
                # Get cluster centroid and top features
                centroid = kmeans.cluster_centers_[cluster_id]
                top_indices = centroid.argsort()[-10:][::-1]  # Top 10 features
                top_features = [feature_names[i] for i in top_indices]
                top_scores = [centroid[i] for i in top_indices]
                
                # Calculate cluster statistics
                cluster_size = len(cluster_texts)
                avg_text_length = sum(len(text.split()) for text in cluster_texts) / cluster_size
                
                # Analyze entry types in cluster
                entry_types = defaultdict(int)
                logic_scores = []
                symbolic_scores = []
                
                for entry in cluster_data:
                    entry_type = entry.get("source_type", "unknown")
                    entry_types[entry_type] += 1
                    
                    logic_score = entry.get("logic_score", 0)
                    symbolic_score = entry.get("symbolic_score", 0)
                    
                    if logic_score:
                        logic_scores.append(logic_score)
                    if symbolic_score:
                        symbolic_scores.append(symbolic_score)
                
                cluster_name = self._generate_cluster_name(top_features[:3])
                
                cluster_analysis["cluster_results"][cluster_id] = {
                    "cluster_name": cluster_name,
                    "size": cluster_size,
                    "percentage": round((cluster_size / len(texts)) * 100, 1),
                    "sample_texts": cluster_texts[:3],  # First 3 as samples
                    "avg_text_length": round(avg_text_length, 1),
                    "entry_types": dict(entry_types),
                    "avg_logic_score": round(sum(logic_scores) / len(logic_scores), 2) if logic_scores else 0,
                    "avg_symbolic_score": round(sum(symbolic_scores) / len(symbolic_scores), 2) if symbolic_scores else 0
                }
                
                cluster_analysis["top_features_per_cluster"][cluster_id] = {
                    "features": top_features,
                    "scores": [round(score, 3) for score in top_scores]
                }
            
            # Overall statistics
            cluster_sizes = [len(cluster_groups[i]) for i in range(n_clusters)]
            cluster_analysis["cluster_statistics"] = {
                "largest_cluster_size": max(cluster_sizes),
                "smallest_cluster_size": min(cluster_sizes),
                "avg_cluster_size": round(sum(cluster_sizes) / len(cluster_sizes), 1),
                "size_variance": round(np.var(cluster_sizes), 2),
                "balance_score": round(1.0 - (np.var(cluster_sizes) / np.mean(cluster_sizes)), 3) if cluster_sizes else 0
            }
            
            # Visualization if requested
            if show_visualization:
                self._create_cluster_visualization(X, labels, cluster_analysis)
            
            return cluster_analysis
            
        except Exception as e:
            return {
                "error": f"Symbol clustering analysis failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _generate_cluster_name(self, top_features: List[str]) -> str:
        """Generate a descriptive name for a cluster based on top features."""
        if not top_features:
            return "unnamed_cluster"
        
        # Use top 1-2 features to create a meaningful name
        if len(top_features) >= 2:
            return f"{top_features[0]}_{top_features[1]}"
        else:
            return top_features[0]
    
    def _create_cluster_visualization(self, X, labels, cluster_analysis):
        """Create and display cluster visualization using t-SNE."""
        try:
            import matplotlib.pyplot as plt
            from sklearn.manifold import TSNE
            import numpy as np
            
            # Reduce dimensionality for visualization
            if X.shape[1] > 50:  # Only use t-SNE if we have many features
                tsne = TSNE(n_components=2, perplexity=min(30, len(X)//4), random_state=42)
                X_reduced = tsne.fit_transform(X)
            else:
                # For smaller feature sets, use first 2 principal components
                from sklearn.decomposition import PCA
                pca = PCA(n_components=2)
                X_reduced = pca.fit_transform(X)
            
            # Create scatter plot
            fig, ax = plt.subplots(figsize=(10, 8))
            
            colors = plt.cm.Set3(np.linspace(0, 1, cluster_analysis["n_clusters"]))
            
            for cluster_id in range(cluster_analysis["n_clusters"]):
                cluster_points = X_reduced[labels == cluster_id]
                if len(cluster_points) > 0:
                    cluster_name = cluster_analysis["cluster_results"][cluster_id]["cluster_name"]
                    ax.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                             c=[colors[cluster_id]], label=f"Cluster {cluster_id}: {cluster_name}", 
                             alpha=0.7, s=50)
            
            ax.set_title(f"Symbol Clusters Visualization ({cluster_analysis['n_clusters']} clusters)")
            ax.set_xlabel("Dimension 1")
            ax.set_ylabel("Dimension 2")
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("⚠️ Matplotlib not available - skipping visualization")
        except Exception as e:
            print(f"⚠️ Could not create visualization: {e}")
    
    def print_cluster_analysis(self, cluster_analysis: Dict):
        """Print a formatted cluster analysis report."""
        if "error" in cluster_analysis:
            print(f"❌ Cluster Analysis Error: {cluster_analysis['error']}")
            return
        
        print("\n🔍 SYMBOL CLUSTER ANALYSIS")
        print("=" * 60)
        print(f"📊 Analyzed {cluster_analysis['valid_text_entries']} valid entries")
        print(f"🎯 Found {cluster_analysis['n_clusters']} clusters")
        
        stats = cluster_analysis["cluster_statistics"]
        print(f"\n📈 Cluster Statistics:")
        print(f"   Largest cluster: {stats['largest_cluster_size']} entries")
        print(f"   Smallest cluster: {stats['smallest_cluster_size']} entries") 
        print(f"   Average size: {stats['avg_cluster_size']} entries")
        print(f"   Balance score: {stats['balance_score']} (1.0 = perfectly balanced)")
        
        print(f"\n🏷️ Cluster Details:")
        for cluster_id, details in cluster_analysis["cluster_results"].items():
            print(f"\n   Cluster {cluster_id}: {details['cluster_name']}")
            print(f"      Size: {details['size']} entries ({details['percentage']}%)")
            print(f"      Logic/Symbolic: {details['avg_logic_score']:.2f}/{details['avg_symbolic_score']:.2f}")
            print(f"      Sample: {details['sample_texts'][0][:60]}..." if details['sample_texts'] else "      No samples")
            
            # Show top features
            if cluster_id in cluster_analysis["top_features_per_cluster"]:
                features = cluster_analysis["top_features_per_cluster"][cluster_id]["features"][:3]
                print(f"      Key terms: {', '.join(features)}")
        
        print("\n" + "=" * 60)
        

# Unit tests
if __name__ == "__main__":
    import tempfile
    from sofia.memory.decision_history import HistoryAwareMemory
    
    print("🧪 Testing Memory Analytics...")
    
    # Test 1: Basic statistics
    print("\n1️⃣ Test: Basic memory statistics")
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = HistoryAwareMemory(data_dir=tmpdir)
        analyzer = MemoryAnalyzer(memory, data_dir=tmpdir)
        
        # Add some items
        for i in range(5):
            memory.store({'text': f'Logic item {i}', 'logic_score': 8, 'symbolic_score': 2}, 'FOLLOW_LOGIC')
        for i in range(3):
            memory.store({'text': f'Symbolic item {i}', 'logic_score': 2, 'symbolic_score': 8}, 'FOLLOW_SYMBOLIC')
        for i in range(7):
            memory.store({'text': f'Bridge item {i}', 'logic_score': 5, 'symbolic_score': 5}, 'FOLLOW_HYBRID')
            
        stats = analyzer.get_memory_stats()
        
        assert stats['total_items'] == 15
        assert stats['distribution']['logic']['count'] == 5
        assert stats['distribution']['symbolic']['count'] == 3
        assert stats['distribution']['bridge']['count'] == 7
        assert abs(stats['distribution']['bridge']['percentage'] - 46.7) < 1
        
        print("✅ Basic statistics work correctly")
        
    # Test 2: Bridge pattern analysis
    print("\n2️⃣ Test: Bridge pattern analysis")
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = HistoryAwareMemory(data_dir=tmpdir)
        analyzer = MemoryAnalyzer(memory, data_dir=tmpdir)
        
        # Add various bridge patterns
        # Volatile item
        volatile = {'text': 'Volatile content', 'logic_score': 5, 'symbolic_score': 5}
        for dec in ['FOLLOW_LOGIC', 'FOLLOW_SYMBOLIC', 'FOLLOW_HYBRID', 'FOLLOW_LOGIC']:
            memory.store(volatile.copy(), dec)
            
        # Conflicted item
        memory.store({'text': 'High both', 'logic_score': 8, 'symbolic_score': 7}, 'FOLLOW_HYBRID')
        
        # Weak item
        memory.store({'text': 'Low both', 'logic_score': 2, 'symbolic_score': 2}, 'FOLLOW_HYBRID')
        
        analysis = analyzer.analyze_bridge_patterns()
        
        assert analysis['total'] > 0
        assert 'volatile' in analysis['patterns']
        assert len(analysis['insights']) > 0
        
        print("✅ Bridge pattern analysis works")
        
    # Test 3: Full evolution report
    print("\n3️⃣ Test: Full evolution report")
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = HistoryAwareMemory(data_dir=tmpdir)
        analyzer = MemoryAnalyzer(memory, data_dir=tmpdir)
        
        # Add diverse items
        for i in range(10):
            score_type = i % 3
            if score_type == 0:
                memory.store({'text': f'Item {i}', 'logic_score': 8, 'symbolic_score': 2}, 'FOLLOW_LOGIC')
            elif score_type == 1:
                memory.store({'text': f'Item {i}', 'logic_score': 2, 'symbolic_score': 8}, 'FOLLOW_SYMBOLIC')
            else:
                memory.store({'text': f'Item {i}', 'logic_score': 5, 'symbolic_score': 5}, 'FOLLOW_HYBRID')
                
        # Generate report
        report = analyzer.generate_evolution_report(
            migration_summary={'total_migrated': 2, 'to_logic': 1, 'to_symbolic': 1},
            audit_summary={'total_reversed': 1, 'from_logic': 1}
        )
        
        assert 'summary' in report
        assert 'health' in report
        assert 'bridge_analysis' in report
        assert 'stability_metrics' in report
        
        # Test pretty printing
        analyzer.print_report(report)
        
        print("✅ Evolution report generation works")
        
    # Test 4: Health indicators
    print("\n4️⃣ Test: Health indicators")
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = HistoryAwareMemory(data_dir=tmpdir)
        analyzer = MemoryAnalyzer(memory, data_dir=tmpdir)
        
        # Create unhealthy distribution (too much in bridge)
        for i in range(2):
            memory.store({'text': f'Logic {i}', 'logic_score': 8, 'symbolic_score': 2}, 'FOLLOW_LOGIC')
        for i in range(8):
            memory.store({'text': f'Bridge {i}', 'logic_score': 5, 'symbolic_score': 5}, 'FOLLOW_HYBRID')
            
        stats = analyzer.get_memory_stats()
        health = stats['health_indicators']
        
        assert health['status'] == 'needs_attention'
        assert len(health['issues']) > 0
        assert len(health['recommendations']) > 0
        assert health['bridge_percentage'] > 50
        
        print("✅ Health indicators detect issues correctly")
        
    # Test 5: Empty memory handling
    print("\n5️⃣ Test: Empty memory handling")
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = HistoryAwareMemory(data_dir=tmpdir)
        analyzer = MemoryAnalyzer(memory, data_dir=tmpdir)
        
        # Generate report with empty memory
        report = analyzer.generate_evolution_report()
        
        # This should not raise KeyError
        analyzer.print_report(report)
        
        assert report['health']['status'] == 'empty'
        assert 'recommendations' in report['health']
        assert len(report['health']['recommendations']) > 0
        
        print("✅ Empty memory handling works correctly")
        
    print("\n✅ All analytics tests passed!")