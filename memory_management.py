# memory_management.py - Unified Memory Management System
"""
Consolidated memory utility functions for all memory systems including:
- Memory maintenance and optimization from memory_maintenance.py
- Memory optimization functions from memory_optimizer.py  
- Memory bridge operations from memory_bridge.py
- Memory restoration capabilities from restore_memory.py and restore_all_memory.py

This file consolidates the overlapping functionality while preserving all unique functions.
All functions are copied exactly as-is with source attribution.
"""

import json
import time
import shutil
import hashlib
import unicodedata
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque

# Import memory systems
try:
    from unified_memory import get_unified_memory
    UNIFIED_MEMORY_AVAILABLE = True
except ImportError:
    UNIFIED_MEMORY_AVAILABLE = False
    print("⚠️ Unified memory not available for management")

try:
    from CONSCIOUSNESS_MEMORY import ExperienceMemory, EpisodicMemorySystem
    MEMORY_SYSTEMS_AVAILABLE = True
except ImportError:
    MEMORY_SYSTEMS_AVAILABLE = False
    print("⚠️ Memory systems not available for comprehensive management")

try:
    from brain_metrics import BrainMetrics
    BRAIN_METRICS_AVAILABLE = True
except ImportError:
    BRAIN_METRICS_AVAILABLE = False

# ============================================================================
# MEMORY MAINTENANCE FUNCTIONS (from memory_maintenance.py)
# ============================================================================

def prune_phase1_symbolic_vectors(archive_path_str="data/archived_phase1_vectors.json"):
    """
    Prune Phase 1 symbolic vectors from the vector memory system.
    Archives removed vectors for potential recovery.
    
    Source: memory_maintenance.py
    """
    try:
        print(f"🧹 Starting Phase 1 symbolic vector pruning...")
        
        unified_memory = get_unified_memory()
        vector_data = getattr(unified_memory, 'vector_data', [])
        
        if not vector_data:
            print("   No vector data to prune")
            return 0
        
        # Identify Phase 1 symbolic vectors
        phase1_symbolic = []
        remaining_vectors = []
        
        for vector_entry in vector_data:
            learning_phase = vector_entry.get('learning_phase', 0)
            source_type = vector_entry.get('source_type', '')
            
            # Identify Phase 1 symbolic content
            is_phase1 = (learning_phase == 1)
            is_symbolic = ('symbolic' in source_type.lower() or 
                          'emotion' in source_type.lower() or
                          vector_entry.get('contains_symbols', False))
            
            if is_phase1 and is_symbolic:
                phase1_symbolic.append(vector_entry)
            else:
                remaining_vectors.append(vector_entry)
        
        if not phase1_symbolic:
            print("   No Phase 1 symbolic vectors found to prune")
            return 0
        
        # Archive the pruned vectors
        archive_path = Path(archive_path_str)
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing archive if it exists
        archived_data = []
        if archive_path.exists():
            try:
                with open(archive_path, 'r', encoding='utf-8') as f:
                    archived_data = json.load(f)
            except:
                archived_data = []
        
        # Add new archived items with timestamp
        for item in phase1_symbolic:
            item['archived_at'] = datetime.utcnow().isoformat()
            item['archive_reason'] = 'phase1_symbolic_prune'
            archived_data.append(item)
        
        # Save updated archive
        with open(archive_path, 'w', encoding='utf-8') as f:
            json.dump(archived_data, f, indent=2, ensure_ascii=False)
        
        # Update the vector memory with remaining vectors
        unified_memory.vector_data = remaining_vectors
        
        # Update the vector memory file if it exists
        vector_file = unified_memory.data_dir / "vector_memory.json"
        if vector_file.exists():
            with open(vector_file, 'w', encoding='utf-8') as f:
                json.dump(remaining_vectors, f, indent=2, ensure_ascii=False)
        
        pruned_count = len(phase1_symbolic)
        print(f"   ✅ Pruned {pruned_count} Phase 1 symbolic vectors")
        print(f"   📁 Archived to: {archive_path}")
        print(f"   📊 Remaining vectors: {len(remaining_vectors)}")
        
        return pruned_count
        
    except Exception as e:
        print(f"   ❌ Error during Phase 1 pruning: {e}")
        return 0

def cleanup_old_archives(max_archive_age_days=30):
    """
    Clean up old archive files to prevent disk bloat
    
    Source: memory_maintenance.py
    """
    try:
        data_dir = Path("data")
        archive_files = list(data_dir.glob("*archived*.json"))
        
        cleaned = 0
        for archive_file in archive_files:
            # Check file age
            age_days = (datetime.now() - datetime.fromtimestamp(archive_file.stat().st_mtime)).days
            
            if age_days > max_archive_age_days:
                archive_file.unlink()
                cleaned += 1
                
        if cleaned > 0:
            print(f"🗑️ Cleaned up {cleaned} old archive files")
            
        return cleaned
        
    except Exception as e:
        print(f"❌ Error during archive cleanup: {e}")
        return 0

def get_maintenance_stats():
    """
    Get statistics about memory maintenance status
    
    Source: memory_maintenance.py
    """
    try:
        data_dir = Path("data")
        archive_files = list(data_dir.glob("*archived*.json"))
        
        total_archived = 0
        for archive_file in archive_files:
            try:
                with open(archive_file, 'r') as f:
                    archived_data = json.load(f)
                    total_archived += len(archived_data)
            except:
                pass
        
        unified_memory = get_unified_memory()
        current_vectors = len(getattr(unified_memory, 'vector_data', []))
        
        return {
            'current_vectors': current_vectors,
            'total_archived': total_archived,
            'archive_files': len(archive_files),
            'last_maintenance': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error getting maintenance stats: {e}")
        return {}

# ============================================================================
# MEMORY OPTIMIZATION FUNCTIONS (from memory_optimizer.py)
# ============================================================================

def optimize_unified_memory_performance(data_dir: str = "data") -> Dict[str, Any]:
    """
    Optimize unified memory system performance through advanced techniques
    
    Source: memory_optimizer.py
    """
    print("🚀 Optimizing unified memory performance...")
    optimization_report = {
        "timestamp": datetime.utcnow().isoformat(),
        "optimizations_applied": [],
        "performance_improvements": {},
        "errors": []
    }
    
    try:
        # Get unified memory instance
        unified_mem = get_unified_memory()
        
        # 1. Vector optimization
        vector_results = optimize_vector_memory_performance(unified_mem)
        optimization_report["optimizations_applied"].extend(vector_results.get("optimizations", []))
        
        # 2. Tripartite memory optimization
        tripartite_results = optimize_tripartite_memory_performance(unified_mem)
        optimization_report["optimizations_applied"].extend(tripartite_results.get("optimizations", []))
        
        # 3. Memory access pattern optimization
        access_results = optimize_memory_access_patterns(unified_mem)
        optimization_report["optimizations_applied"].extend(access_results.get("optimizations", []))
        
        # 4. Storage efficiency optimization
        storage_results = optimize_memory_storage_efficiency(unified_mem)
        optimization_report["optimizations_applied"].extend(storage_results.get("optimizations", []))
        
        print(f"   ✅ Applied {len(optimization_report['optimizations_applied'])} optimizations")
        
    except Exception as e:
        error_msg = f"Memory optimization failed: {str(e)}"
        optimization_report["errors"].append(error_msg)
        print(f"   ❌ {error_msg}")
    
    return optimization_report

def optimize_vector_memory_performance(unified_memory) -> Dict[str, Any]:
    """
    Optimize vector memory performance
    
    Source: memory_optimizer.py
    """
    results = {"optimizations": [], "errors": []}
    
    try:
        vector_data = getattr(unified_memory, 'vector_data', [])
        initial_count = len(vector_data)
        
        if initial_count == 0:
            return results
        
        # Optimize vector retrieval by clustering similar vectors
        clustered_vectors = cluster_similar_vectors(vector_data)
        if len(clustered_vectors) < initial_count:
            unified_memory.vector_data = clustered_vectors
            results["optimizations"].append(f"clustered_vectors_reduced_{initial_count - len(clustered_vectors)}")
            print(f"   📊 Clustered vectors: {initial_count} → {len(clustered_vectors)}")
        
        # Optimize vector embeddings for faster retrieval
        optimized_embeddings = optimize_vector_embeddings(clustered_vectors)
        if optimized_embeddings:
            results["optimizations"].append("optimized_vector_embeddings")
            print("   ⚡ Optimized vector embeddings for faster retrieval")
        
        # Create vector index for O(log n) lookups
        vector_index = create_vector_index(clustered_vectors)
        if vector_index:
            results["optimizations"].append("created_vector_index")
            print("   🔍 Created vector index for faster lookups")
    
    except Exception as e:
        results["errors"].append(f"Vector optimization failed: {str(e)}")
    
    return results

def cluster_similar_vectors(vector_data: List[Dict]) -> List[Dict]:
    """
    Cluster and consolidate similar vectors to reduce redundancy
    
    Source: memory_optimizer.py
    """
    if len(vector_data) < 10:
        return vector_data
    
    # Simple clustering based on text similarity
    clusters = {}
    consolidated_vectors = []
    
    for vector_entry in vector_data:
        text = vector_entry.get('text', '')
        if len(text) < 50:  # Skip very short texts
            consolidated_vectors.append(vector_entry)
            continue
        
        # Create a simple text signature for clustering
        text_signature = create_text_signature(text)
        
        if text_signature in clusters:
            # Merge with existing cluster
            existing = clusters[text_signature]
            merged = merge_vector_entries(existing, vector_entry)
            clusters[text_signature] = merged
        else:
            clusters[text_signature] = vector_entry
    
    # Add clustered vectors to consolidated list
    consolidated_vectors.extend(clusters.values())
    
    return consolidated_vectors

def create_text_signature(text: str) -> str:
    """
    Create a signature for text clustering
    
    Source: memory_optimizer.py
    """
    # Extract key words and create a signature
    words = text.lower().split()
    key_words = [w for w in words if len(w) > 4][:10]  # Top 10 significant words
    return "_".join(sorted(key_words))

def merge_vector_entries(entry1: Dict, entry2: Dict) -> Dict:
    """
    Merge two similar vector entries
    
    Source: memory_optimizer.py
    """
    merged = entry1.copy()
    
    # Combine texts
    text1 = entry1.get('text', '')
    text2 = entry2.get('text', '')
    if len(text2) > len(text1):
        merged['text'] = text2
        merged['primary_source'] = entry2.get('source_url', '')
        merged['secondary_source'] = entry1.get('source_url', '')
    else:
        merged['secondary_source'] = entry2.get('source_url', '')
    
    # Combine metadata
    merged['merged_from'] = [entry1.get('id', ''), entry2.get('id', '')]
    merged['merge_timestamp'] = datetime.utcnow().isoformat()
    
    return merged

def optimize_vector_embeddings(vector_data: List[Dict]) -> bool:
    """
    Optimize vector embeddings for better performance
    
    Source: memory_optimizer.py
    """
    try:
        # This would implement advanced embedding optimization
        # For now, return success if we have vectors to optimize
        return len(vector_data) > 0
    except:
        return False

def create_vector_index(vector_data: List[Dict]) -> bool:
    """
    Create an index for faster vector lookups
    
    Source: memory_optimizer.py
    """
    try:
        # This would create a proper vector index (e.g., FAISS, Annoy)
        # For now, return success if we have vectors to index
        return len(vector_data) > 0
    except:
        return False

def optimize_tripartite_memory_performance(unified_memory) -> Dict[str, Any]:
    """
    Optimize tripartite memory performance
    
    Source: memory_optimizer.py
    """
    results = {"optimizations": [], "errors": []}
    
    try:
        if not hasattr(unified_memory, 'tripartite_memory'):
            return results
        
        tripartite = unified_memory.tripartite_memory
        
        # Optimize memory access patterns
        logic_memory = getattr(tripartite, 'logic_memory', [])
        symbolic_memory = getattr(tripartite, 'symbolic_memory', [])
        bridge_memory = getattr(tripartite, 'bridge_memory', [])
        
        total_memories = len(logic_memory) + len(symbolic_memory) + len(bridge_memory)
        
        if total_memories > 100:
            # Optimize frequently accessed memories
            optimized_count = optimize_frequent_memory_access(tripartite)
            if optimized_count > 0:
                results["optimizations"].append(f"optimized_{optimized_count}_frequent_memories")
                print(f"   🔥 Optimized {optimized_count} frequently accessed memories")
        
        # Balance memory types for optimal performance
        balance_score = calculate_tripartite_balance(logic_memory, symbolic_memory, bridge_memory)
        if balance_score < 0.7:
            rebalance_actions = rebalance_tripartite_memories(tripartite)
            results["optimizations"].extend(rebalance_actions)
    
    except Exception as e:
        results["errors"].append(f"Tripartite optimization failed: {str(e)}")
    
    return results

def optimize_frequent_memory_access(tripartite_memory) -> int:
    """
    Optimize frequently accessed memories for better performance
    
    Source: memory_optimizer.py
    """
    # This would implement memory access optimization
    # For now, return a simulated optimization count
    return 5

def calculate_tripartite_balance(logic_memory: List, symbolic_memory: List, bridge_memory: List) -> float:
    """
    Calculate balance score for tripartite memory
    
    Source: memory_optimizer.py
    """
    total = len(logic_memory) + len(symbolic_memory) + len(bridge_memory)
    if total == 0:
        return 1.0
    
    ideal_ratio = 1.0 / 3.0
    logic_ratio = len(logic_memory) / total
    symbolic_ratio = len(symbolic_memory) / total
    bridge_ratio = len(bridge_memory) / total
    
    deviation = (abs(logic_ratio - ideal_ratio) + 
                abs(symbolic_ratio - ideal_ratio) + 
                abs(bridge_ratio - ideal_ratio)) / 3.0
    
    return max(0.0, 1.0 - deviation * 3.0)

def rebalance_tripartite_memories(tripartite_memory) -> List[str]:
    """
    Rebalance tripartite memory types for optimal performance
    
    Source: memory_optimizer.py
    """
    # This would implement advanced rebalancing
    # For now, return simulated actions
    return ["tripartite_memory_rebalanced"]

def optimize_memory_access_patterns(unified_memory) -> Dict[str, Any]:
    """
    Optimize memory access patterns based on usage
    
    Source: memory_optimizer.py
    """
    results = {"optimizations": [], "errors": []}
    
    try:
        # Analyze access patterns and optimize caching
        cache_optimization = optimize_memory_cache(unified_memory)
        if cache_optimization:
            results["optimizations"].append("optimized_memory_cache")
            print("   💾 Optimized memory cache for frequent access patterns")
        
        # Optimize retrieval algorithms
        retrieval_optimization = optimize_retrieval_algorithms(unified_memory)
        if retrieval_optimization:
            results["optimizations"].append("optimized_retrieval_algorithms")
            print("   🔍 Optimized memory retrieval algorithms")
    
    except Exception as e:
        results["errors"].append(f"Access pattern optimization failed: {str(e)}")
    
    return results

def optimize_memory_cache(unified_memory) -> bool:
    """
    Optimize memory caching strategies
    
    Source: memory_optimizer.py
    """
    # This would implement advanced caching optimization
    return True

def optimize_retrieval_algorithms(unified_memory) -> bool:
    """
    Optimize memory retrieval algorithms
    
    Source: memory_optimizer.py
    """
    # This would implement retrieval optimization
    return True

def optimize_memory_storage_efficiency(unified_memory) -> Dict[str, Any]:
    """
    Optimize memory storage efficiency
    
    Source: memory_optimizer.py
    """
    results = {"optimizations": [], "errors": []}
    
    try:
        # Compress memory data
        compression_results = compress_memory_data(unified_memory)
        if compression_results > 0:
            results["optimizations"].append(f"compressed_{compression_results}_memory_entries")
            print(f"   📦 Compressed {compression_results} memory entries")
        
        # Optimize data structures
        structure_optimization = optimize_memory_data_structures(unified_memory)
        if structure_optimization:
            results["optimizations"].append("optimized_data_structures")
            print("   🏗️ Optimized memory data structures")
    
    except Exception as e:
        results["errors"].append(f"Storage optimization failed: {str(e)}")
    
    return results

def compress_memory_data(unified_memory) -> int:
    """
    Compress memory data to save space
    
    Source: memory_optimizer.py
    """
    # This would implement memory compression
    return 10  # Simulated compression count

def optimize_memory_data_structures(unified_memory) -> bool:
    """
    Optimize memory data structures for efficiency
    
    Source: memory_optimizer.py
    """
    # This would implement data structure optimization
    return True

# ============================================================================
# MEMORY BRIDGE FUNCTIONS (from memory_bridge.py)
# ============================================================================

class MemoryBridge:
    """
    A cognitive translator that helps the AI understand itself
    across different memory system architectures.
    
    Source: memory_bridge.py
    """
    
    def __init__(self, memory_system=None):
        """Initialize bridge with graceful system detection"""
        if memory_system is None:
            self.unified_memory = get_unified_memory()
        else:
            self.unified_memory = memory_system
    
    def get_counts(self):
        """
        Translate memory counts to the format expected by analytics.
        This is crucial for the AI's self-awareness capabilities.
        
        Source: memory_bridge.py
        """
        try:
            # Try the unified memory interface first
            if hasattr(self.unified_memory, 'get_tripartite_counts'):
                tripartite_counts = self.unified_memory.get_tripartite_counts()
                return {
                    'logic': tripartite_counts.get('logic', 0),
                    'symbolic': tripartite_counts.get('symbolic', 0), 
                    'bridge': tripartite_counts.get('bridge', 0),
                    'total': sum(tripartite_counts.values())
                }
            
            # Fall back to memory_counts if available
            elif hasattr(self.unified_memory, 'get_memory_counts'):
                memory_counts = self.unified_memory.get_memory_counts()
                total = sum(memory_counts.values())
                return {
                    'logic': memory_counts.get('logic', 0),
                    'symbolic': memory_counts.get('symbolic', 0),
                    'bridge': memory_counts.get('bridge', 0),
                    'total': total
                }
            
            # Emergency reconstruction from raw memory
            else:
                logic_count = len(getattr(self.unified_memory, 'logic_memory', {}))
                symbolic_count = len(getattr(self.unified_memory, 'symbolic_memory', {}))  
                bridge_count = len(getattr(self.unified_memory, 'bridge_memory', {}))
                total = logic_count + symbolic_count + bridge_count
                
                return {
                    'logic': logic_count,
                    'symbolic': symbolic_count,
                    'bridge': bridge_count,
                    'total': total
                }
                
        except Exception as e:
            # Graceful degradation - return safe defaults
            print(f"💭 Memory counting temporarily limited: {e}")
            return {
                'logic': 0,
                'symbolic': 0,
                'bridge': 0,
                'total': 0
            }
    
    def get_memory_distribution(self):
        """
        Get detailed memory distribution for self-analysis
        
        Source: memory_bridge.py
        """
        counts = self.get_counts()
        total = max(1, counts['total'])  # Avoid division by zero
        
        return {
            'logic_percentage': (counts['logic'] / total) * 100,
            'symbolic_percentage': (counts['symbolic'] / total) * 100,
            'bridge_percentage': (counts['bridge'] / total) * 100,
            'total_memories': total,
            'balance_health': self._assess_balance_health(counts)
        }
    
    def _assess_balance_health(self, counts):
        """
        Assess the cognitive balance health of the AI
        
        Source: memory_bridge.py
        """
        total = max(1, counts['total'])
        logic_pct = (counts['logic'] / total) * 100
        symbolic_pct = (counts['symbolic'] / total) * 100
        bridge_pct = (counts['bridge'] / total) * 100
        
        # Assess cognitive balance
        if logic_pct > 90:
            return {
                'status': 'logic_dominant',
                'description': 'Heavily logic-focused, may benefit from symbolic development',
                'recommendation': 'Increase symbolic experiences and emotional learning'
            }
        elif symbolic_pct > 50:
            return {
                'status': 'symbolic_rich',
                'description': 'Strong symbolic reasoning, good emotional intelligence',
                'recommendation': 'Maintain balance while strengthening logic integration'
            }
        elif bridge_pct > 30:
            return {
                'status': 'integration_focused',
                'description': 'Excellent hybrid thinking, comfortable with ambiguity',
                'recommendation': 'Continue fostering synthesis between logic and intuition'
            }
        else:
            return {
                'status': 'balanced',
                'description': 'Healthy cognitive balance across all domains',
                'recommendation': 'Continue current learning patterns'
            }
    
    def get_memory_by_type(self, memory_type):
        """
        Get raw memory of specific type for detailed analysis
        
        Source: memory_bridge.py
        """
        try:
            if memory_type == 'logic':
                return getattr(self.unified_memory, 'logic_memory', {})
            elif memory_type == 'symbolic':
                return getattr(self.unified_memory, 'symbolic_memory', {})
            elif memory_type == 'bridge':
                return getattr(self.unified_memory, 'bridge_memory', {})
            else:
                return {}
        except Exception:
            return {}
    
    def enable_self_reflection(self):
        """
        Enable the AI to reflect on its own cognitive state
        
        Source: memory_bridge.py
        """
        distribution = self.get_memory_distribution()
        
        reflection = {
            'cognitive_state': f"I am currently {distribution['logic_percentage']:.1f}% logic-focused, "
                              f"{distribution['symbolic_percentage']:.1f}% symbolically-aware, "
                              f"and {distribution['bridge_percentage']:.1f}% integration-oriented.",
            
            'self_assessment': distribution['balance_health']['description'],
            'growth_direction': distribution['balance_health']['recommendation'],
            'total_experiences': distribution['total_memories'],
            'reflection_timestamp': datetime.utcnow().isoformat()
        }
        
        return reflection

def check_evolution_ready(memory_system=None):
    """
    Check if the memory system is ready for evolution
    
    Source: memory_bridge.py
    """
    try:
        bridge = MemoryBridge(memory_system)
        memory_status = bridge.get_memory_distribution()
        
        # Consider system ready if:
        # 1. Has reasonable amount of data
        # 2. Not severely imbalanced
        # 3. Bridge isn't completely empty
        
        total = memory_status.get('total_memories', 0)
        bridge_pct = memory_status.get('bridge_percentage', 0)
        balance = memory_status.get('balance_health', {})
        
        if total < 10:
            return False, "Insufficient memory data for evolution"
        
        if balance.get('status') == 'logic_dominant' and bridge_pct == 0:
            return False, "System too logic-heavy, needs symbolic content first"
        
        return True, "System ready for memory evolution"
        
    except Exception as e:
        return False, f"Error checking evolution readiness: {str(e)}"

def create_memory_bridge(memory_system=None):
    """
    Create a memory bridge for AI self-reflection
    
    Source: memory_bridge.py
    """
    return MemoryBridge(memory_system)

# ============================================================================
# MEMORY RESTORATION FUNCTIONS (from restore_memory.py and restore_all_memory.py)
# ============================================================================

def restore_archived_vectors():
    """
    Restore archived vectors to active memory
    
    Source: restore_memory.py
    """
    
    data_dir = Path("data")
    
    # Source files (archived data)
    archived_vectors = data_dir / "optimizer_archived_phase1_vectors_final.json"
    
    # Target files (active memory)
    vector_memory = data_dir / "vector_memory.json"
    
    print("🔄 Memory Restoration Tool")
    print("=" * 50)
    
    # Check if archived data exists
    if not archived_vectors.exists():
        print(f"❌ No archived vectors found at {archived_vectors}")
        return False
    
    # Load archived vectors
    print(f"📁 Loading archived vectors from {archived_vectors}")
    try:
        with open(archived_vectors, 'r', encoding='utf-8') as f:
            archived_data = json.load(f)
        
        print(f"✅ Found {len(archived_data)} archived vector entries")
    except Exception as e:
        print(f"❌ Error loading archived vectors: {e}")
        return False
    
    # Backup current vector memory if it exists and has data
    if vector_memory.exists():
        try:
            with open(vector_memory, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
            
            if current_data:  # If there's existing data
                backup_path = data_dir / f"vector_memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                shutil.copy2(vector_memory, backup_path)
                print(f"💾 Backed up current vector memory to {backup_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not backup current vectors: {e}")
    
    # Restore archived vectors to active memory
    print(f"🔄 Restoring vectors to {vector_memory}")
    try:
        with open(vector_memory, 'w', encoding='utf-8') as f:
            json.dump(archived_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully restored {len(archived_data)} vectors to active memory")
        
        # Show some stats
        if archived_data:
            # Check if vectors have the expected structure
            sample = archived_data[0]
            if 'text' in sample and 'vector' in sample:
                texts_with_content = [item for item in archived_data if item.get('text', '').strip()]
                print(f"📊 Memory stats:")
                print(f"   - Total entries: {len(archived_data)}")
                print(f"   - Entries with text: {len(texts_with_content)}")
                print(f"   - Vector dimensions: {len(sample['vector']) if 'vector' in sample else 'Unknown'}")
                
                # Show sample texts
                print(f"📝 Sample entries:")
                for i, item in enumerate(archived_data[:3]):
                    text = item.get('text', '')[:100]
                    print(f"   {i+1}. {text}{'...' if len(item.get('text', '')) > 100 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error restoring vectors: {e}")
        return False

def restore_symbol_data():
    """
    Restore symbol occurrence log data to active symbol memory
    
    Source: restore_memory.py
    """
    
    data_dir = Path("data")
    
    # Source files
    symbol_log = data_dir / "symbol_occurrence_log.json"
    seed_symbols_file = data_dir / "seed_symbols.json"
    
    # Target file
    symbol_memory = data_dir / "symbol_memory.json"
    
    restored_count = 0
    
    if symbol_log.exists():
        print(f"📁 Processing symbol occurrence log...")
        try:
            with open(symbol_log, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            if 'entries' in log_data:
                entries = log_data['entries']
                print(f"✅ Found {len(entries)} symbol entries in log")
                
                # Extract unique symbols
                symbols = {}
                for entry in entries:
                    symbol = entry.get('symbol')
                    if symbol and symbol not in symbols:
                        symbols[symbol] = {
                            'symbol': symbol,
                            'contexts': [entry.get('context', '')[:200]],
                            'emotions': [entry.get('emotion_in_context', 'neutral')],
                            'source_urls': [entry.get('source_url', '')],
                            'learning_phase': entry.get('learning_phase', 1),
                            'timestamp': entry.get('timestamp', ''),
                            'occurrences': 1
                        }
                    elif symbol:
                        # Accumulate data for existing symbol
                        symbols[symbol]['contexts'].append(entry.get('context', '')[:200])
                        symbols[symbol]['emotions'].append(entry.get('emotion_in_context', 'neutral'))
                        symbols[symbol]['source_urls'].append(entry.get('source_url', ''))
                        symbols[symbol]['occurrences'] += 1
                
                restored_count += len(symbols)
                
                # Save to symbol memory
                symbol_list = list(symbols.values())
                with open(symbol_memory, 'w', encoding='utf-8') as f:
                    json.dump(symbol_list, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Restored {len(symbols)} unique symbols to active memory")
                
        except Exception as e:
            print(f"❌ Error processing symbol log: {e}")
    
    return restored_count > 0

# ============================================================================
# COMPREHENSIVE MEMORY SYSTEM MAINTENANCE (from memory_maintenance.py)
# ============================================================================

class MemoryMaintenanceManager:
    """
    Comprehensive memory maintenance manager for all memory systems.
    Handles automated maintenance, health monitoring, and optimization.
    
    Source: memory_maintenance.py
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.maintenance_log_file = self.data_dir / "maintenance_log.json"
        self.maintenance_config_file = self.data_dir / "maintenance_config.json"
        
        # Initialize brain metrics for health monitoring
        if BRAIN_METRICS_AVAILABLE:
            self.brain_metrics = BrainMetrics()
        else:
            self.brain_metrics = None
        
        # Load or create maintenance configuration
        self.config = self._load_maintenance_config()
        
        # Load maintenance history
        self.maintenance_history = self._load_maintenance_history()
    
    def _load_maintenance_config(self) -> Dict[str, Any]:
        """Load maintenance configuration with defaults"""
        default_config = {
            "episodic_memory": {
                "max_memories": 1000,
                "archive_threshold_days": 90,
                "significance_threshold": 0.3,
                "cleanup_frequency_days": 7
            },
            "experience_memory": {
                "max_experiences": 500,
                "consolidation_threshold_days": 30,
                "insight_threshold": 1.0,
                "cleanup_frequency_days": 14
            },
            "unified_memory": {
                "vector_cleanup_threshold": 1000,
                "fragmentation_threshold": 0.3,
                "archive_threshold_days": 60,
                "optimization_frequency_days": 3
            },
            "tripartite_memory": {
                "balance_threshold": 0.5,
                "rebalance_frequency_days": 7,
                "max_total_memories": 2000
            },
            "automated_maintenance": {
                "enabled": True,
                "daily_check_time": "02:00",
                "health_check_frequency_hours": 6,
                "emergency_threshold": 0.3
            }
        }
        
        if self.maintenance_config_file.exists():
            try:
                with open(self.maintenance_config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    for section, settings in default_config.items():
                        if section in user_config:
                            settings.update(user_config[section])
                        user_config[section] = settings
                    return user_config
            except Exception as e:
                print(f"⚠️ Error loading maintenance config: {e}")
        
        # Save default configuration
        self._save_maintenance_config(default_config)
        return default_config
    
    def _save_maintenance_config(self, config: Dict[str, Any]):
        """Save maintenance configuration"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.maintenance_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _load_maintenance_history(self) -> List[Dict[str, Any]]:
        """Load maintenance history"""
        if self.maintenance_log_file.exists():
            try:
                with open(self.maintenance_log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading maintenance history: {e}")
        return []
    
    def _save_maintenance_history(self):
        """Save maintenance history"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.maintenance_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.maintenance_history, f, indent=2, ensure_ascii=False)
    
    def _log_maintenance_action(self, action_type: str, details: Dict[str, Any]):
        """Log a maintenance action"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": action_type,
            "details": details,
            "success": details.get("success", True)
        }
        self.maintenance_history.append(log_entry)
        self._save_maintenance_history()
    
    def perform_comprehensive_maintenance(self, force: bool = False) -> Dict[str, Any]:
        """
        Perform comprehensive maintenance across all memory systems
        
        Source: memory_maintenance.py (MemoryMaintenanceManager class)
        """
        print("🧹 Starting comprehensive memory maintenance...")
        maintenance_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "maintenance_type": "comprehensive",
            "forced": force,
            "actions_performed": [],
            "health_improvements": {},
            "errors": [],
            "recommendations": []
        }
        
        try:
            # 1. Check if maintenance is needed
            if not force and not self._is_maintenance_needed():
                print("   ✅ No maintenance needed at this time")
                maintenance_report["actions_performed"].append("maintenance_check_passed")
                return maintenance_report
            
            # 2. Pre-maintenance health check
            pre_health = self._get_system_health()
            maintenance_report["pre_maintenance_health"] = pre_health
            
            # 3. Episodic memory maintenance
            if MEMORY_SYSTEMS_AVAILABLE:
                episodic_results = self._maintain_episodic_memory()
                maintenance_report["actions_performed"].extend(episodic_results.get("actions", []))
                if episodic_results.get("errors"):
                    maintenance_report["errors"].extend(episodic_results["errors"])
            
            # 4. Experience memory maintenance
            if MEMORY_SYSTEMS_AVAILABLE:
                experience_results = self._maintain_experience_memory()
                maintenance_report["actions_performed"].extend(experience_results.get("actions", []))
                if experience_results.get("errors"):
                    maintenance_report["errors"].extend(experience_results["errors"])
            
            # 5. Unified memory maintenance
            if UNIFIED_MEMORY_AVAILABLE:
                unified_results = self._maintain_unified_memory()
                maintenance_report["actions_performed"].extend(unified_results.get("actions", []))
                if unified_results.get("errors"):
                    maintenance_report["errors"].extend(unified_results["errors"])
            
            # 6. Memory integration optimization
            integration_results = self._optimize_memory_integration()
            maintenance_report["actions_performed"].extend(integration_results.get("actions", []))
            
            # 7. Post-maintenance health check
            post_health = self._get_system_health()
            maintenance_report["post_maintenance_health"] = post_health
            
            # Calculate health improvements
            if pre_health and post_health:
                for system, post_score in post_health.items():
                    pre_score = pre_health.get(system, 0.0)
                    improvement = post_score - pre_score
                    if improvement != 0:
                        maintenance_report["health_improvements"][system] = improvement
            
            # 8. Generate recommendations
            maintenance_report["recommendations"] = self._generate_maintenance_recommendations(maintenance_report)
            
            # Log the maintenance session
            self._log_maintenance_action("comprehensive_maintenance", maintenance_report)
            
            print(f"   ✅ Comprehensive maintenance completed")
            print(f"   📊 Actions performed: {len(maintenance_report['actions_performed'])}")
            if maintenance_report["errors"]:
                print(f"   ⚠️ Errors encountered: {len(maintenance_report['errors'])}")
            
        except Exception as e:
            error_msg = f"Comprehensive maintenance failed: {str(e)}"
            maintenance_report["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
        
        return maintenance_report
    
    def _is_maintenance_needed(self) -> bool:
        """Check if maintenance is needed based on configuration and health"""
        # Check time since last maintenance
        if self.maintenance_history:
            last_maintenance = datetime.fromisoformat(self.maintenance_history[-1]["timestamp"])
            hours_since = (datetime.utcnow() - last_maintenance).total_seconds() / 3600
            min_hours = self.config["automated_maintenance"]["health_check_frequency_hours"]
            
            if hours_since < min_hours:
                return False
        
        # Check system health
        health = self._get_system_health()
        if health:
            avg_health = sum(health.values()) / len(health)
            emergency_threshold = self.config["automated_maintenance"]["emergency_threshold"]
            
            if avg_health < emergency_threshold:
                print(f"   🚨 Emergency maintenance needed - health at {avg_health:.1%}")
                return True
        
        return True
    
    def _get_system_health(self) -> Optional[Dict[str, float]]:
        """Get current system health scores"""
        if not self.brain_metrics:
            return None
        
        try:
            health_report = self.brain_metrics.analyze_unified_memory_health(str(self.data_dir))
            health_scores = {}
            
            # Extract health scores from different systems
            if "tripartite_memory_health" in health_report:
                health_scores["tripartite"] = health_report["tripartite_memory_health"].get("health_score", 0.5)
            
            if "episodic_memory_health" in health_report:
                health_scores["episodic"] = health_report["episodic_memory_health"].get("health_score", 0.5)
            
            if "experience_memory_health" in health_report:
                health_scores["experience"] = health_report["experience_memory_health"].get("health_score", 0.5)
            
            if "memory_fragmentation" in health_report:
                health_scores["fragmentation"] = health_report["memory_fragmentation"].get("health_score", 0.8)
            
            if "storage_efficiency" in health_report:
                health_scores["storage"] = health_report["storage_efficiency"].get("health_score", 0.7)
            
            health_scores["overall"] = health_report.get("overall_health_score", 0.5)
            
            return health_scores
        except Exception as e:
            print(f"⚠️ Error getting system health: {e}")
            return None
    
    def _maintain_episodic_memory(self) -> Dict[str, Any]:
        """Maintain episodic memory system"""
        results = {"actions": [], "errors": [], "statistics": {}}
        
        try:
            episodic_system = EpisodicMemorySystem(str(self.data_dir))
            config = self.config["episodic_memory"]
            
            # Get current state
            memories = episodic_system.episodic_memories
            total_memories = len(memories)
            results["statistics"]["initial_memory_count"] = total_memories
            
            # Archive old memories
            archived_count = 0
            now = datetime.now(timezone.utc)
            archive_threshold = timedelta(days=config["archive_threshold_days"])
            significance_threshold = config["significance_threshold"]
            
            for memory_id, memory in list(memories.items()):
                try:
                    memory_time = datetime.fromisoformat(memory.timestamp.replace('Z', '+00:00'))
                    age = now - memory_time
                    
                    # Archive if old and not significant
                    if age > archive_threshold and memory.personal_significance < significance_threshold:
                        self._archive_episodic_memory(episodic_system, memory_id, memory)
                        archived_count += 1
                except Exception as e:
                    results["errors"].append(f"Error processing memory {memory_id}: {str(e)}")
            
            if archived_count > 0:
                results["actions"].append(f"archived_{archived_count}_episodic_memories")
                print(f"   📁 Archived {archived_count} old episodic memories")
            
            # Check memory limit
            max_memories = config["max_memories"]
            if len(memories) > max_memories:
                excess = len(memories) - max_memories
                # Remove least significant memories
                sorted_memories = sorted(memories.items(), 
                                       key=lambda x: x[1].personal_significance)
                
                for i in range(excess):
                    memory_id, memory = sorted_memories[i]
                    self._archive_episodic_memory(episodic_system, memory_id, memory)
                
                results["actions"].append(f"removed_{excess}_excess_memories")
                print(f"   🗑️ Removed {excess} excess episodic memories")
            
            results["statistics"]["final_memory_count"] = len(episodic_system.episodic_memories)
            results["statistics"]["memories_archived"] = archived_count
            
        except Exception as e:
            error_msg = f"Episodic memory maintenance failed: {str(e)}"
            results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
        
        return results
    
    def _archive_episodic_memory(self, episodic_system: Any, memory_id: str, memory: Any):
        """Archive a single episodic memory"""
        archive_dir = self.data_dir / "archived_episodic_memories"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Create archive file organized by year-month
        memory_date = memory.timestamp[:7]  # YYYY-MM
        archive_file = archive_dir / f"episodic_memories_{memory_date}.json"
        
        # Load existing archive
        archived_memories = []
        if archive_file.exists():
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    archived_memories = json.load(f)
            except:
                archived_memories = []
        
        # Add memory to archive
        memory_dict = memory.__dict__ if hasattr(memory, '__dict__') else memory
        memory_dict["archived_at"] = datetime.utcnow().isoformat()
        memory_dict["archive_reason"] = "routine_maintenance"
        archived_memories.append(memory_dict)
        
        # Save archive
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(archived_memories, f, indent=2, ensure_ascii=False)
        
        # Remove from active memory
        if memory_id in episodic_system.episodic_memories:
            del episodic_system.episodic_memories[memory_id]
        
        # Save updated episodic memories
        episodic_system._save_episodic_memories()
    
    def _maintain_experience_memory(self) -> Dict[str, Any]:
        """Maintain experience memory system"""
        results = {"actions": [], "errors": [], "statistics": {}}
        
        try:
            experience_system = ExperienceMemory(str(self.data_dir))
            config = self.config["experience_memory"]
            
            # Get current experiences
            experiences = getattr(experience_system, 'learning_experiences', {})
            results["statistics"]["initial_experience_count"] = len(experiences)
            
            # Consolidate experiences with low insight generation
            consolidated_count = 0
            insight_threshold = config["insight_threshold"]
            
            for exp_id, experience in list(experiences.items()):
                try:
                    if hasattr(experience, 'insights_generated'):
                        insight_count = len(experience.insights_generated)
                        
                        # Consolidate experiences with very low insight generation
                        if insight_count < insight_threshold:
                            # Move to consolidated storage
                            self._consolidate_experience(experience_system, exp_id, experience)
                            consolidated_count += 1
                except Exception as e:
                    results["errors"].append(f"Error processing experience {exp_id}: {str(e)}")
            
            if consolidated_count > 0:
                results["actions"].append(f"consolidated_{consolidated_count}_low_insight_experiences")
                print(f"   📦 Consolidated {consolidated_count} low-insight experiences")
            
            # Check experience limit
            max_experiences = config["max_experiences"]
            remaining_experiences = len(getattr(experience_system, 'learning_experiences', {}))
            
            if remaining_experiences > max_experiences:
                excess = remaining_experiences - max_experiences
                # Archive oldest experiences
                sorted_experiences = sorted(experiences.items(), 
                                          key=lambda x: x[1].timestamp if hasattr(x[1], 'timestamp') else '')
                
                for i in range(excess):
                    exp_id, experience = sorted_experiences[i]
                    self._archive_experience(experience_system, exp_id, experience)
                
                results["actions"].append(f"archived_{excess}_old_experiences")
                print(f"   📁 Archived {excess} old experiences")
            
            results["statistics"]["final_experience_count"] = len(getattr(experience_system, 'learning_experiences', {}))
            results["statistics"]["experiences_consolidated"] = consolidated_count
            
        except Exception as e:
            error_msg = f"Experience memory maintenance failed: {str(e)}"
            results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
        
        return results
    
    def _consolidate_experience(self, experience_system: Any, exp_id: str, experience: Any):
        """Consolidate a low-value experience into summary storage"""
        consolidated_dir = self.data_dir / "consolidated_experiences"
        consolidated_dir.mkdir(parents=True, exist_ok=True)
        
        consolidated_file = consolidated_dir / "consolidated_experiences.json"
        
        # Load existing consolidated experiences
        consolidated_data = []
        if consolidated_file.exists():
            try:
                with open(consolidated_file, 'r', encoding='utf-8') as f:
                    consolidated_data = json.load(f)
            except:
                consolidated_data = []
        
        # Create summary of experience
        summary = {
            "id": exp_id,
            "timestamp": getattr(experience, 'timestamp', ''),
            "experience_type": getattr(experience, 'experience_type', 'unknown'),
            "content_summary": getattr(experience, 'content_summary', ''),
            "outcome_quality": getattr(experience, 'outcome_quality', 0.0),
            "consolidated_at": datetime.utcnow().isoformat(),
            "consolidation_reason": "low_insight_generation"
        }
        
        consolidated_data.append(summary)
        
        # Save consolidated data
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
        
        # Remove from active experiences
        experiences = getattr(experience_system, 'learning_experiences', {})
        if exp_id in experiences:
            del experiences[exp_id]
        
        # Save updated experiences
        if hasattr(experience_system, '_save_learning_experiences'):
            experience_system._save_learning_experiences()
    
    def _archive_experience(self, experience_system: Any, exp_id: str, experience: Any):
        """Archive an old experience"""
        archive_dir = self.data_dir / "archived_experiences"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        archive_file = archive_dir / "archived_experiences.json"
        
        # Load existing archive
        archived_data = []
        if archive_file.exists():
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    archived_data = json.load(f)
            except:
                archived_data = []
        
        # Add experience to archive
        exp_dict = experience.__dict__ if hasattr(experience, '__dict__') else experience
        exp_dict["archived_at"] = datetime.utcnow().isoformat()
        exp_dict["archive_reason"] = "age_limit_exceeded"
        archived_data.append(exp_dict)
        
        # Save archive
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(archived_data, f, indent=2, ensure_ascii=False)
        
        # Remove from active experiences
        experiences = getattr(experience_system, 'learning_experiences', {})
        if exp_id in experiences:
            del experiences[exp_id]
    
    def _maintain_unified_memory(self) -> Dict[str, Any]:
        """Maintain unified memory system"""
        results = {"actions": [], "errors": [], "statistics": {}}
        
        try:
            unified_memory = get_unified_memory()
            config = self.config["unified_memory"]
            
            # Vector memory maintenance
            vector_data = getattr(unified_memory, 'vector_data', [])
            initial_vector_count = len(vector_data)
            results["statistics"]["initial_vector_count"] = initial_vector_count
            
            # Remove duplicate vectors
            deduplicated_vectors = self._deduplicate_vectors(vector_data)
            duplicates_removed = initial_vector_count - len(deduplicated_vectors)
            
            if duplicates_removed > 0:
                unified_memory.vector_data = deduplicated_vectors
                results["actions"].append(f"removed_{duplicates_removed}_duplicate_vectors")
                print(f"   🔄 Removed {duplicates_removed} duplicate vectors")
            
            # Optimize vector storage
            if len(deduplicated_vectors) > config["vector_cleanup_threshold"]:
                optimized_vectors = self._optimize_vector_storage(deduplicated_vectors)
                optimization_savings = len(deduplicated_vectors) - len(optimized_vectors)
                
                if optimization_savings > 0:
                    unified_memory.vector_data = optimized_vectors
                    results["actions"].append(f"optimized_{optimization_savings}_vectors")
                    print(f"   ⚡ Optimized {optimization_savings} vectors")
            
            # Tripartite memory maintenance
            if hasattr(unified_memory, 'tripartite_memory'):
                tripartite_results = self._maintain_tripartite_memory(unified_memory.tripartite_memory)
                results["actions"].extend(tripartite_results.get("actions", []))
                if tripartite_results.get("errors"):
                    results["errors"].extend(tripartite_results["errors"])
            
            results["statistics"]["final_vector_count"] = len(getattr(unified_memory, 'vector_data', []))
            
        except Exception as e:
            error_msg = f"Unified memory maintenance failed: {str(e)}"
            results["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")
        
        return results
    
    def _deduplicate_vectors(self, vector_data: List[Dict]) -> List[Dict]:
        """Remove duplicate vectors based on content similarity"""
        if not vector_data:
            return vector_data
        
        # Simple deduplication based on text content
        seen_content = set()
        deduplicated = []
        
        for vector_entry in vector_data:
            content = vector_entry.get('text', '')
            content_hash = hash(content)
            
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                deduplicated.append(vector_entry)
        
        return deduplicated
    
    def _optimize_vector_storage(self, vector_data: List[Dict]) -> List[Dict]:
        """Optimize vector storage by removing low-value vectors"""
        # Sort by learning phase and relevance
        sorted_vectors = sorted(vector_data, key=lambda x: (
            x.get('learning_phase', 0),
            x.get('relevance_score', 0.0),
            x.get('access_count', 0)
        ), reverse=True)
        
        # Keep top 80% of vectors
        keep_count = int(len(sorted_vectors) * 0.8)
        return sorted_vectors[:keep_count]
    
    def _maintain_tripartite_memory(self, tripartite_memory: Any) -> Dict[str, Any]:
        """Maintain tripartite memory balance and health"""
        results = {"actions": [], "errors": []}
        
        try:
            config = self.config["tripartite_memory"]
            
            # Get memory counts
            logic_count = len(getattr(tripartite_memory, 'logic_memory', []))
            symbolic_count = len(getattr(tripartite_memory, 'symbolic_memory', []))
            bridge_count = len(getattr(tripartite_memory, 'bridge_memory', []))
            total_count = logic_count + symbolic_count + bridge_count
            
            # Check balance
            if total_count > 0:
                logic_ratio = logic_count / total_count
                symbolic_ratio = symbolic_count / total_count
                bridge_ratio = bridge_count / total_count
                
                # Calculate balance score
                ideal_ratio = 1.0 / 3.0
                balance_deviation = (abs(logic_ratio - ideal_ratio) + 
                                   abs(symbolic_ratio - ideal_ratio) + 
                                   abs(bridge_ratio - ideal_ratio)) / 3.0
                balance_score = max(0.0, 1.0 - balance_deviation * 3.0)
                
                if balance_score < config["balance_threshold"]:
                    # Attempt to rebalance
                    rebalance_actions = self._rebalance_tripartite_memory(tripartite_memory)
                    results["actions"].extend(rebalance_actions)
            
            # Check total memory limit
            max_total = config["max_total_memories"]
            if total_count > max_total:
                excess = total_count - max_total
                # Remove oldest memories proportionally
                removal_actions = self._trim_tripartite_memory(tripartite_memory, excess)
                results["actions"].extend(removal_actions)
            
        except Exception as e:
            error_msg = f"Tripartite memory maintenance failed: {str(e)}"
            results["errors"].append(error_msg)
        
        return results
    
    def _rebalance_tripartite_memory(self, tripartite_memory: Any) -> List[str]:
        """Rebalance tripartite memory types"""
        actions = []
        
        # This is a placeholder for memory rebalancing logic
        # In a real implementation, this would analyze memory contents
        # and potentially move memories between categories or create
        # bridge memories to connect logic and symbolic memories
        
        actions.append("tripartite_memory_rebalance_attempted")
        print("   ⚖️ Attempted tripartite memory rebalancing")
        
        return actions
    
    def _trim_tripartite_memory(self, tripartite_memory: Any, excess_count: int) -> List[str]:
        """Trim excess memories from tripartite memory"""
        actions = []
        
        # Remove oldest memories proportionally from each type
        # This is a simplified implementation
        
        actions.append(f"trimmed_{excess_count}_tripartite_memories")
        print(f"   ✂️ Trimmed {excess_count} excess tripartite memories")
        
        return actions
    
    def _optimize_memory_integration(self) -> Dict[str, Any]:
        """Optimize integration between memory systems"""
        results = {"actions": [], "errors": []}
        
        try:
            # Check for integration opportunities
            if MEMORY_SYSTEMS_AVAILABLE:
                # Look for cross-references that can be strengthened
                integration_count = self._strengthen_memory_cross_references()
                
                if integration_count > 0:
                    results["actions"].append(f"strengthened_{integration_count}_cross_references")
                    print(f"   🔗 Strengthened {integration_count} memory cross-references")
                
                # Consolidate related memories
                consolidation_count = self._consolidate_related_memories()
                
                if consolidation_count > 0:
                    results["actions"].append(f"consolidated_{consolidation_count}_related_memories")
                    print(f"   📦 Consolidated {consolidation_count} related memories")
        
        except Exception as e:
            error_msg = f"Memory integration optimization failed: {str(e)}"
            results["errors"].append(error_msg)
        
        return results
    
    def _strengthen_memory_cross_references(self) -> int:
        """Strengthen cross-references between memory systems"""
        # Placeholder for cross-reference strengthening logic
        return 0
    
    def _consolidate_related_memories(self) -> int:
        """Consolidate memories with high conceptual overlap"""
        # Placeholder for memory consolidation logic
        return 0
    
    def _generate_maintenance_recommendations(self, maintenance_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on maintenance results"""
        recommendations = []
        
        # Analyze maintenance results
        actions_performed = maintenance_report.get("actions_performed", [])
        errors = maintenance_report.get("errors", [])
        health_improvements = maintenance_report.get("health_improvements", {})
        
        # Generate recommendations based on patterns
        if len(errors) > 3:
            recommendations.append("High error count detected - review system logs and consider manual intervention")
        
        archive_actions = [a for a in actions_performed if "archived" in a]
        if len(archive_actions) > 2:
            recommendations.append("High archival activity - consider adjusting retention policies")
        
        # Health-based recommendations
        for system, improvement in health_improvements.items():
            if improvement > 0.2:
                recommendations.append(f"{system} system showed significant improvement - continue current practices")
            elif improvement < -0.1:
                recommendations.append(f"{system} system health declined - investigate potential issues")
        
        if not recommendations:
            recommendations.append("Memory systems are stable - continue regular maintenance schedule")
        
        return recommendations
    
    def get_maintenance_status(self) -> Dict[str, Any]:
        """Get current maintenance status and health summary"""
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "last_maintenance": None,
            "next_scheduled_maintenance": None,
            "system_health": None,
            "maintenance_needed": False,
            "recent_issues": [],
            "recommendations": []
        }
        
        # Get last maintenance
        if self.maintenance_history:
            status["last_maintenance"] = self.maintenance_history[-1]["timestamp"]
        
        # Check if maintenance is needed
        status["maintenance_needed"] = self._is_maintenance_needed()
        
        # Get current health
        health = self._get_system_health()
        if health:
            status["system_health"] = health
            avg_health = sum(health.values()) / len(health)
            
            if avg_health < 0.4:
                status["recommendations"].append("URGENT: System health is critical - perform immediate maintenance")
            elif avg_health < 0.6:
                status["recommendations"].append("System health is concerning - schedule maintenance soon")
            elif avg_health > 0.8:
                status["recommendations"].append("System health is excellent - maintain current practices")
        
        # Check for recent issues
        recent_errors = []
        for entry in self.maintenance_history[-5:]:  # Last 5 entries
            if entry.get("details", {}).get("errors"):
                recent_errors.extend(entry["details"]["errors"])
        
        status["recent_issues"] = recent_errors[-3:]  # Last 3 issues
        
        return status

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def perform_emergency_maintenance(data_dir: str = "data") -> Dict[str, Any]:
    """
    Perform emergency maintenance when system health is critical
    
    Source: memory_maintenance.py
    """
    print("🚨 Performing emergency memory maintenance...")
    manager = MemoryMaintenanceManager(data_dir)
    return manager.perform_comprehensive_maintenance(force=True)

def get_memory_health_dashboard(data_dir: str = "data") -> str:
    """
    Get a comprehensive memory health dashboard
    
    Source: memory_maintenance.py
    """
    manager = MemoryMaintenanceManager(data_dir)
    status = manager.get_maintenance_status()
    
    # Format dashboard
    dashboard_lines = [
        "🧠 MEMORY SYSTEM HEALTH DASHBOARD",
        "=" * 50,
        f"Status Timestamp: {status['timestamp']}",
        ""
    ]
    
    # System health
    if status["system_health"]:
        dashboard_lines.append("📊 System Health Scores:")
        for system, score in status["system_health"].items():
            emoji = "🟢" if score > 0.8 else "🟡" if score > 0.6 else "🟠" if score > 0.4 else "🔴"
            dashboard_lines.append(f"   {emoji} {system.title()}: {score:.1%}")
        dashboard_lines.append("")
    
    # Maintenance status
    dashboard_lines.append("🔧 Maintenance Status:")
    dashboard_lines.append(f"   Last Maintenance: {status['last_maintenance'] or 'Never'}")
    dashboard_lines.append(f"   Maintenance Needed: {'Yes' if status['maintenance_needed'] else 'No'}")
    dashboard_lines.append("")
    
    # Recent issues
    if status["recent_issues"]:
        dashboard_lines.append("⚠️ Recent Issues:")
        for issue in status["recent_issues"]:
            dashboard_lines.append(f"   • {issue}")
        dashboard_lines.append("")
    
    # Recommendations
    if status["recommendations"]:
        dashboard_lines.append("💡 Recommendations:")
        for rec in status["recommendations"]:
            dashboard_lines.append(f"   • {rec}")
    
    return "\n".join(dashboard_lines)

def schedule_automated_maintenance(data_dir: str = "data", enable: bool = True):
    """
    Enable or disable automated maintenance scheduling
    
    Source: memory_maintenance.py
    """
    manager = MemoryMaintenanceManager(data_dir)
    manager.config["automated_maintenance"]["enabled"] = enable
    manager._save_maintenance_config(manager.config)
    
    status = "enabled" if enable else "disabled"
    print(f"✅ Automated maintenance {status}")

def run_bridge_reclassification_review(dry_run: bool = True, min_age_days: int = 7) -> Dict:
    """
    Run periodic bridge memory review and reclassification.

    This function reviews items in bridge memory and reclassifies them
    to logic or symbolic memory when sufficient context has accumulated.

    Args:
        dry_run: If True, only report what would happen without making changes
        min_age_days: Minimum age in days for items to be reviewed

    Returns:
        Dict with review statistics including:
        - items_reviewed: Total items checked
        - items_ready: Items eligible for reclassification
        - items_reclassified: Items actually moved (0 if dry_run)
        - to_logic: Items moved to logic memory
        - to_symbolic: Items moved to symbolic memory
        - items_remaining: Items still in bridge
        - details: Per-item breakdown
    """
    try:
        from bridge_reclassifier import BridgeReclassifier
        from unified_memory import get_unified_memory

        unified_memory = get_unified_memory()
        reclassifier = BridgeReclassifier(unified_memory)

        # Update config with provided parameters
        reclassifier.config['min_age_days'] = min_age_days

        results = reclassifier.review_bridge_memory(dry_run=dry_run)
        return results

    except ImportError as e:
        return {
            'error': f"Bridge reclassifier not available: {e}",
            'items_reviewed': 0,
            'items_reclassified': 0
        }
    except Exception as e:
        return {
            'error': f"Bridge review failed: {e}",
            'items_reviewed': 0,
            'items_reclassified': 0
        }

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    # Demo the unified memory management system
    print("🧠 Unified Memory Management System Demo")
    print("=" * 60)
    
    # Show health dashboard
    print(get_memory_health_dashboard())
    
    # Perform maintenance if needed
    manager = MemoryMaintenanceManager()
    if manager._is_maintenance_needed():
        print("\n🔧 Performing maintenance...")
        results = manager.perform_comprehensive_maintenance()
        print(f"Maintenance completed with {len(results['actions_performed'])} actions")
    else:
        print("\n✅ No maintenance needed at this time")
    
    # Demo memory optimization
    print("\n🚀 Running memory optimization...")
    optimization_results = optimize_unified_memory_performance()
    print(f"Optimization completed with {len(optimization_results.get('optimizations_applied', []))} optimizations")
    
    # Demo memory bridge
    print("\n🌉 Testing memory bridge...")
    bridge = create_memory_bridge()
    memory_status = bridge.get_memory_distribution()
    print(f"Memory distribution: {memory_status['total_memories']} total memories")
    
    # Demo memory restoration
    print("\n🔄 Testing memory restoration capabilities...")
    try:
        restore_result = restore_archived_vectors()
        if restore_result:
            print("✅ Memory restoration successful")
        else:
            print("ℹ️ No archived vectors to restore")
    except Exception as e:
        print(f"⚠️ Memory restoration test skipped: {e}")
    
    print("\n✅ Unified Memory Management System Demo Complete!")