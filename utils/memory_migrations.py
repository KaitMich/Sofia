# utils/memory_migrations.py - Memory Migration Utilities
"""
Migration-specific utilities for memory system transformations including:
- Tripartite memory migration from migrate_to_tripartite.py
- Vector upgrade utilities from upgrade_old_vectors.py
- Reverse migration audit from reverse_migration.py
- Unified migration system from unified_migration_system.py

This file consolidates migration-specific functionality.
All functions are copied exactly as-is with source attribution.
"""

import json
import hashlib
import numpy as np
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import logging

# Import existing components when available
try:
    from unified_weight_system import UnifiedWeightSystem
    WEIGHT_SYSTEM_AVAILABLE = True
except ImportError:
    WEIGHT_SYSTEM_AVAILABLE = False

try:
    from unified_memory import get_unified_memory
    UNIFIED_MEMORY_AVAILABLE = True
except ImportError:
    UNIFIED_MEMORY_AVAILABLE = False

try:
    from vector_engine import encode_with_minilm, encode_with_e5
    from sklearn.metrics.pairwise import cosine_similarity
    VECTOR_ENGINE_AVAILABLE = True
except ImportError:
    VECTOR_ENGINE_AVAILABLE = False

# Import protection system when available
try:
    from protection_utils import is_protected_content, get_protection_reason, is_migration_allowed
    from cognitive_sovereignty import sovereignty_check
    PROTECTION_AVAILABLE = True
except ImportError:
    PROTECTION_AVAILABLE = False

# ============================================================================
# TRIPARTITE MEMORY MIGRATION (from migrate_to_tripartite.py)
# ============================================================================

# Import the evaluator to analyze content
try:
    from utils.link_evaluator import evaluate_link_with_confidence_gates
    EVALUATOR_AVAILABLE = True
    # Use confidence gates instead of context
    def evaluate_link_with_context(text):
        # Simple wrapper to maintain compatibility
        return {'routing_decision': 'FOLLOW_HYBRID', 'logic_score': 5.0, 'symbolic_score': 5.0}
except ImportError:
    try:
        from link_evaluator import evaluate_link_with_confidence_gates
        EVALUATOR_AVAILABLE = True
        def evaluate_link_with_context(text):
            return {'routing_decision': 'FOLLOW_HYBRID', 'logic_score': 5.0, 'symbolic_score': 5.0}
    except ImportError:
        EVALUATOR_AVAILABLE = False
        print("⚠️ Link evaluator not available - using basic heuristics")

def analyze_content(text: str, existing_data: Dict = None) -> Tuple[str, float, float]:
    """
    Analyze content to determine if it should go to logic, symbolic, or bridge memory.
    
    Returns:
        (decision_type, logic_score, symbolic_score)
    
    Source: migrate_to_tripartite.py
    """
    
    if EVALUATOR_AVAILABLE and len(text.strip()) > 10:
        try:
            # Use the actual evaluator if available
            result = evaluate_link_with_context(text)
            decision = result.get('routing_decision', 'FOLLOW_HYBRID')
            logic_score = result.get('logic_score', 5.0)
            symbolic_score = result.get('symbolic_score', 5.0)
            return decision, logic_score, symbolic_score
        except:
            pass
    
    # Fallback to heuristic analysis
    text_lower = text.lower()
    
    # Logic indicators
    logic_keywords = [
        'algorithm', 'function', 'method', 'process', 'logic', 'compute', 'calculate',
        'data', 'structure', 'analysis', 'system', 'technical', 'implementation',
        'code', 'programming', 'database', 'network', 'protocol', 'specification',
        'definition', 'explanation', 'how', 'what', 'when', 'where', 'steps',
        'procedure', 'instruction', 'guide', 'documentation', 'manual'
    ]
    
    # Symbolic indicators  
    symbolic_keywords = [
        'feel', 'emotion', 'beautiful', 'meaning', 'purpose', 'soul', 'heart',
        'dream', 'hope', 'fear', 'love', 'hate', 'passion', 'inspire', 'create',
        'art', 'poetry', 'music', 'story', 'narrative', 'metaphor', 'symbol',
        'journey', 'growth', 'transformation', 'spiritual', 'consciousness',
        'experience', 'wisdom', 'insight', 'intuition', 'creativity'
    ]
    
    # Count matches
    logic_score = sum(1 for kw in logic_keywords if kw in text_lower)
    symbolic_score = sum(1 for kw in symbolic_keywords if kw in text_lower)
    
    # Check for questions (often logical)
    if any(text_lower.strip().startswith(q) for q in ['what', 'how', 'why', 'when', 'where']):
        logic_score += 2
    
    # Check for exclamations and emotional punctuation (symbolic)
    if '!' in text or text_lower.strip().endswith('?') and ('feel' in text_lower or 'think' in text_lower):
        symbolic_score += 1
    
    # Check length - very short text is often factual/logical
    if len(text.strip()) < 20:
        logic_score += 1
    
    # Determine decision
    if logic_score > symbolic_score + 1:
        decision = "FOLLOW_LOGIC"
        final_logic = min(10.0, 5.0 + logic_score)
        final_symbolic = max(1.0, 5.0 - logic_score/2)
    elif symbolic_score > logic_score + 1:
        decision = "FOLLOW_SYMBOLIC"
        final_logic = max(1.0, 5.0 - symbolic_score/2)
        final_symbolic = min(10.0, 5.0 + symbolic_score)
    else:
        decision = "FOLLOW_HYBRID"
        final_logic = 5.0 + (logic_score - symbolic_score) * 0.5
        final_symbolic = 5.0 + (symbolic_score - logic_score) * 0.5
    
    return decision, final_logic, final_symbolic

def convert_vector_to_tripartite_format(vector_item: Dict, index: int) -> Dict:
    """
    Convert old vector format to new tripartite memory format
    
    Source: migrate_to_tripartite.py
    """
    
    text = vector_item.get('text', '')
    
    # Analyze content for routing
    decision_type, logic_score, symbolic_score = analyze_content(text, vector_item)
    
    # Create unique ID
    if 'id' in vector_item:
        item_id = vector_item['id']
    else:
        # Create ID from content hash and index
        text_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        item_id = f"{decision_type.lower()}_{text_hash}_{index}"
    
    # Build the tripartite memory item
    tripartite_item = {
        "id": item_id,
        "text": text,
        "source_url": vector_item.get('source_url', ''),
        "logic_score": logic_score,
        "symbolic_score": symbolic_score,
        "confidence": vector_item.get('confidence', 0.5),
        "processing_phase": vector_item.get('learning_phase', 1),
        "storage_phase": vector_item.get('learning_phase', 1),
        "is_shallow": vector_item.get('exploration_depth', 'shallow') == 'shallow',
        "is_highly_relevant": logic_score > 7 or symbolic_score > 7,
        "timestamp": vector_item.get('timestamp', datetime.utcnow().isoformat()),
        "content_type": vector_item.get('source_type', 'unknown'),
        "emotions": {},  # Would need emotion analysis
        "symbols_found": 0,  # Would need symbol analysis  
        "symbols_list": [],
        "keywords": [],  # Could extract from text
        "decision_type": decision_type,
        "stored_at": datetime.utcnow().isoformat(),
        # Preserve original vector data
        "original_vector": vector_item.get('vector', []),
        "migrated_from": "vector_memory"
    }
    
    # Add any additional metadata
    if 'metadata' in vector_item:
        tripartite_item['original_metadata'] = vector_item['metadata']
    
    return tripartite_item

def migrate_vectors_to_tripartite():
    """
    Main migration function
    
    Source: migrate_to_tripartite.py
    """
    
    data_dir = Path("data")
    
    # Source file
    vector_memory_file = data_dir / "vector_memory.json"
    
    # Target files
    logic_memory_file = data_dir / "logic_memory.json"
    symbolic_memory_file = data_dir / "symbolic_memory.json"
    bridge_memory_file = data_dir / "bridge_memory.json"
    
    print("🔄 Tripartite Memory Migration")
    print("=" * 50)
    
    # Load vector data
    if not vector_memory_file.exists():
        print(f"❌ No vector memory file found at {vector_memory_file}")
        return False
    
    print(f"📁 Loading vectors from {vector_memory_file}")
    try:
        with open(vector_memory_file, 'r', encoding='utf-8') as f:
            vectors = json.load(f)
        print(f"✅ Loaded {len(vectors)} vectors")
    except Exception as e:
        print(f"❌ Error loading vectors: {e}")
        return False
    
    if not vectors:
        print("❌ No vectors to migrate")
        return False
    
    # Prepare memory stores
    logic_items = []
    symbolic_items = []
    bridge_items = []
    
    # Process each vector
    print("🔄 Analyzing and routing vectors...")
    
    for i, vector_item in enumerate(vectors):
        try:
            tripartite_item = convert_vector_to_tripartite_format(vector_item, i)
            decision = tripartite_item['decision_type']
            
            if decision == "FOLLOW_LOGIC":
                logic_items.append(tripartite_item)
            elif decision == "FOLLOW_SYMBOLIC":
                symbolic_items.append(tripartite_item)
            else:  # FOLLOW_HYBRID
                bridge_items.append(tripartite_item)
                
        except Exception as e:
            print(f"⚠️ Error processing vector {i}: {e}")
            continue
    
    # Show distribution
    print(f"📊 Distribution results:")
    print(f"   Logic memory: {len(logic_items)} items")
    print(f"   Symbolic memory: {len(symbolic_items)} items")  
    print(f"   Bridge memory: {len(bridge_items)} items")
    print(f"   Total: {len(logic_items) + len(symbolic_items) + len(bridge_items)} items")
    
    # Backup existing files if they have data
    backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for file_path, name in [(logic_memory_file, 'logic'), (symbolic_memory_file, 'symbolic'), (bridge_memory_file, 'bridge')]:
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
                if existing_data:  # Not empty
                    backup_path = data_dir / f"{name}_memory_backup_{backup_timestamp}.json"
                    with open(backup_path, 'w') as f:
                        json.dump(existing_data, f, indent=2)
                    print(f"💾 Backed up existing {name} memory to {backup_path}")
            except:
                pass
    
    # Save to tripartite files
    success = True
    
    try:
        print(f"💾 Saving logic memory ({len(logic_items)} items)...")
        with open(logic_memory_file, 'w', encoding='utf-8') as f:
            json.dump(logic_items, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Saving symbolic memory ({len(symbolic_items)} items)...")
        with open(symbolic_memory_file, 'w', encoding='utf-8') as f:
            json.dump(symbolic_items, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Saving bridge memory ({len(bridge_items)} items)...")
        with open(bridge_memory_file, 'w', encoding='utf-8') as f:
            json.dump(bridge_items, f, indent=2, ensure_ascii=False)
            
        print("✅ Successfully migrated vectors to tripartite memory!")
        
    except Exception as e:
        print(f"❌ Error saving tripartite memory: {e}")
        success = False
    
    return success

def fix_symbol_memory():
    """
    Fix symbol memory format to be a dictionary
    
    Source: migrate_to_tripartite.py
    """
    
    data_dir = Path("data")
    symbol_file = data_dir / "symbol_memory.json"
    
    if not symbol_file.exists():
        print("ℹ️ No symbol memory file to fix")
        return True
    
    print("🔧 Fixing symbol memory format...")
    
    try:
        with open(symbol_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # If it's already a dictionary, nothing to do
        if isinstance(data, dict):
            print("✅ Symbol memory is already in correct format")
            return True
        
        # If it's a list, convert to dictionary
        if isinstance(data, list):
            symbol_dict = {}
            
            for item in data:
                if isinstance(item, dict) and 'symbol' in item:
                    symbol = item['symbol']
                    symbol_dict[symbol] = {
                        "name": item.get('name', symbol),
                        "keywords": [],
                        "core_meanings": item.get('contexts', [])[:3],  # First 3 contexts as meanings
                        "emotions": [],
                        "emotion_profile": {},
                        "vector_examples": [],
                        "origin": "migrated",
                        "learning_phase": item.get('learning_phase', 1),
                        "resonance_weight": 0.5,
                        "created_at": item.get('timestamp', datetime.utcnow().isoformat()),
                        "updated_at": datetime.utcnow().isoformat(),
                        "usage_count": item.get('occurrences', 1)
                    }
            
            # Save as dictionary
            with open(symbol_file, 'w', encoding='utf-8') as f:
                json.dump(symbol_dict, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Converted {len(symbol_dict)} symbols to dictionary format")
            return True
        
        else:
            print("⚠️ Unknown symbol memory format, creating empty dictionary")
            with open(symbol_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
            return True
            
    except Exception as e:
        print(f"❌ Error fixing symbol memory: {e}")
        return False

# ============================================================================
# VECTOR UPGRADE UTILITIES (from upgrade_old_vectors.py)
# ============================================================================

def upgrade_vectors():
    """
    Upgrade old vectors with enhanced embeddings
    
    Source: upgrade_old_vectors.py
    """
    memory_file = Path("data/vector_memory.json")
    
    if not memory_file.exists():
        print("❌ No memory file found.")
        return

    with open(memory_file, "r", encoding="utf-8") as f:
        memory = json.load(f)

    if not VECTOR_ENGINE_AVAILABLE:
        print("⚠️ Vector engine not available - skipping upgrades")
        return

    upgraded = []
    for entry in memory:
        text = entry["text"]
        vec_minilm = encode_with_minilm(text)
        vec_e5 = encode_with_e5(text)

        similarity = cosine_similarity([vec_minilm], [vec_e5])[0][0]
        fused = (vec_minilm + vec_e5) / 2 if similarity >= 0.7 else vec_minilm
        source = "fused" if similarity >= 0.7 else "minilm-dominant"

        entry["vector"] = fused.tolist()
        entry["similarity"] = float(similarity)
        entry["source"] = source
        upgraded.append(entry)

    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(upgraded, f, indent=2)

    print(f"✅ Upgraded {len(upgraded)} vector entries with fused data.")

# ============================================================================
# REVERSE MIGRATION AUDIT (from reverse_migration.py)
# ============================================================================

# Import sovereignty system for protection checks
try:
    from cognitive_sovereignty import sovereignty_check, is_protected_content
    SOVEREIGNTY_AVAILABLE = True
except ImportError:
    SOVEREIGNTY_AVAILABLE = False

try:
    from adaptive_migration import MigrationEngine, evaluate_link_with_confidence_gates
    ADAPTIVE_MIGRATION_AVAILABLE = True
except ImportError:
    ADAPTIVE_MIGRATION_AVAILABLE = False

class ReverseMigrationAuditor:
    """
    Audits items in logic/symbolic memory to catch misclassifications
    and move them back to bridge memory if needed.
    
    Source: reverse_migration.py
    """
    
    def __init__(self, memory, confidence_threshold=0.3):
        self.memory = memory
        self.confidence_threshold = confidence_threshold
        self.reverse_log = []
        
    def audit_item(self, item, current_location):
        """
        Audit a single item to see if it should be moved back to bridge.
        
        Returns: (should_reverse, reason)
        
        Source: reverse_migration.py
        """
        # SOVEREIGNTY PROTECTION: Use the new cognitive sovereignty system
        if SOVEREIGNTY_AVAILABLE:
            # Check for protected content using the sovereignty system
            if is_protected_content(item):
                return False, "Protected by cognitive sovereignty"
            
            # Check with sovereignty system for reverse migration approval
            reverse_action = {
                "type": "memory_migration",
                "migration_type": "reverse_audit",
                "items": [item],
                "description": f"Reverse migrate item from {current_location}",
                "current_location": current_location,
                "audit_reason": "Confidence re-evaluation"
            }
            
            sovereignty_result = sovereignty_check(reverse_action)
            if sovereignty_result["veto"]:
                return False, f"Sovereignty veto: {sovereignty_result['reasoning']}"
        
        # LEGACY PROTECTION: Keep existing checks for backward compatibility
        # evolution_protected check removed: all items are migratable
        if item.get('protection_level') == 'maximum':
            return False, "Protected from evolution"
            
        if item.get('content_type') == 'symbolic_core':
            return False, "Core symbolic content protected"
            
        source_url = item.get('source_url', '') or ''
        if source_url.startswith('core://protected'):
            return False, "Protected source"
        
        # Additional identity protection checks
        if item.get('content_type') == 'identity_core':
            return False, "Identity core content protected"
            
        if source_url.startswith('identity://'):
            return False, "Identity source protected"
        
        logic_score = item.get('logic_score', 0)
        symbolic_score = item.get('symbolic_score', 0)
        
        # Re-evaluate with current weights
        if ADAPTIVE_MIGRATION_AVAILABLE:
            new_decision, new_score = evaluate_link_with_confidence_gates(
                logic_score, symbolic_score
            )
        else:
            # Fallback evaluation
            if logic_score > symbolic_score + 1:
                new_decision = 'FOLLOW_LOGIC'
                new_score = logic_score
            elif symbolic_score > logic_score + 1:
                new_decision = 'FOLLOW_SYMBOLIC'
                new_score = symbolic_score
            else:
                new_decision = 'FOLLOW_HYBRID'
                new_score = min(logic_score, symbolic_score)
        
        # Get expected decision based on current location
        expected_decision = {
            'logic': 'FOLLOW_LOGIC',
            'symbolic': 'FOLLOW_SYMBOLIC',
            'bridge': 'FOLLOW_HYBRID'
        }[current_location]
        
        # Check if misclassified
        if new_decision != expected_decision:
            return True, f"Reclassified as {new_decision}"
            
        # Check if confidence too low
        if new_score < self.confidence_threshold:
            return True, f"Low confidence ({new_score:.2f})"
            
        # Check stability
        stability = self.memory.get_item_stability(item) if hasattr(self.memory, 'get_item_stability') else {'history_length': 0, 'is_stable': True}
        if stability['history_length'] >= 5 and not stability['is_stable']:
            return True, "Chronically unstable"
            
        # Check if it's been flip-flopping
        if 'reverse_migration_count' in item and item['reverse_migration_count'] >= 2:
            return True, "Multiple reverse migrations"
            
        return False, "Item correctly classified"
        
    def audit_logic_memory(self):
        """
        Audit all items in logic memory
        
        Source: reverse_migration.py
        """
        reverse_count = 0
        new_logic = []
        
        print("\n🔍 Auditing logic memory...")
        
        logic_memory = getattr(self.memory, 'logic_memory', [])
        bridge_memory = getattr(self.memory, 'bridge_memory', [])
        
        for item in logic_memory:
            should_reverse, reason = self.audit_item(item, 'logic')
            
            if should_reverse:
                # Add reverse migration metadata
                item['reverse_migrated'] = True
                item['reverse_migration_reason'] = reason
                item['reverse_migration_date'] = datetime.utcnow().isoformat()
                item['reverse_migration_count'] = item.get('reverse_migration_count', 0) + 1
                
                # Log it
                self.reverse_log.append({
                    'item_id': item.get('id', 'unknown'),
                    'text_preview': item.get('text', '')[:50],
                    'from': 'logic',
                    'to': 'bridge',
                    'reason': reason,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                # Move to bridge
                bridge_memory.append(item)
                reverse_count += 1
                
                print(f"  ← Moving to bridge ({reason}): {item.get('text', '')[:50]}...")
            else:
                new_logic.append(item)
                
        # Update memory
        if hasattr(self.memory, 'logic_memory'):
            self.memory.logic_memory = new_logic
        if hasattr(self.memory, 'bridge_memory'):
            self.memory.bridge_memory = bridge_memory
            
        return reverse_count
        
    def audit_symbolic_memory(self):
        """
        Audit all items in symbolic memory
        
        Source: reverse_migration.py
        """
        reverse_count = 0
        new_symbolic = []
        
        print("\n🔍 Auditing symbolic memory...")
        
        symbolic_memory = getattr(self.memory, 'symbolic_memory', [])
        bridge_memory = getattr(self.memory, 'bridge_memory', [])
        
        for item in symbolic_memory:
            should_reverse, reason = self.audit_item(item, 'symbolic')
            
            if should_reverse:
                # Add reverse migration metadata
                item['reverse_migrated'] = True
                item['reverse_migration_reason'] = reason
                item['reverse_migration_date'] = datetime.utcnow().isoformat()
                item['reverse_migration_count'] = item.get('reverse_migration_count', 0) + 1
                
                # Log it
                self.reverse_log.append({
                    'item_id': item.get('id', 'unknown'),
                    'text_preview': item.get('text', '')[:50],
                    'from': 'symbolic',
                    'to': 'bridge',
                    'reason': reason,
                    'timestamp': datetime.utcnow().isoformat()
                })
                
                # Move to bridge
                bridge_memory.append(item)
                reverse_count += 1
                
                print(f"  ← Moving to bridge ({reason}): {item.get('text', '')[:50]}...")
            else:
                new_symbolic.append(item)
                
        # Update memory
        if hasattr(self.memory, 'symbolic_memory'):
            self.memory.symbolic_memory = new_symbolic
        if hasattr(self.memory, 'bridge_memory'):
            self.memory.bridge_memory = bridge_memory
            
        return reverse_count
        
    def audit_all(self):
        """
        Audit both logic and symbolic memories
        
        Source: reverse_migration.py
        """
        total_reversed = 0
        total_reversed += self.audit_logic_memory()
        total_reversed += self.audit_symbolic_memory()
        return total_reversed
        
    def get_audit_summary(self):
        """
        Get summary of reverse migrations
        
        Source: reverse_migration.py
        """
        if not self.reverse_log:
            return {
                'total_reversed': 0,
                'from_logic': 0,
                'from_symbolic': 0,
                'reasons': {}
            }
            
        # Count by source
        from_logic = len([r for r in self.reverse_log if r['from'] == 'logic'])
        from_symbolic = len([r for r in self.reverse_log if r['from'] == 'symbolic'])
        
        # Count by reason
        reasons = {}
        for record in self.reverse_log:
            reason = record['reason']
            reasons[reason] = reasons.get(reason, 0) + 1
            
        return {
            'total_reversed': len(self.reverse_log),
            'from_logic': from_logic,
            'from_symbolic': from_symbolic,
            'reasons': reasons
        }

# ============================================================================
# UNIFIED MIGRATION SYSTEM (from unified_migration_system.py)
# ============================================================================

@dataclass
class MigrationResult:
    """
    Result of a migration operation
    
    Source: unified_migration_system.py
    """
    operation_type: str
    items_processed: int
    items_migrated: int
    conflicts_resolved: int
    insights_applied: int
    execution_time: float
    metadata: Dict[str, Any]

@dataclass
class UnifiedMigrationSession:
    """
    Complete migration session results
    
    Source: unified_migration_system.py
    """
    session_id: str
    timestamp: str
    forward_migration: MigrationResult
    reverse_audit: MigrationResult
    weight_optimization: MigrationResult
    data_consolidation: MigrationResult
    total_execution_time: float
    system_health: Dict[str, Any]

class DataConsolidator:
    """
    Consolidates orphaned data and eliminates storage duplication
    
    Source: unified_migration_system.py
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('DataConsolidator')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def consolidate_orphaned_data(self) -> Dict[str, Any]:
        """
        Consolidate all orphaned and duplicate data files
        
        Source: unified_migration_system.py
        """
        start_time = datetime.now()
        consolidation_results = {
            'memory_files_merged': 0,
            'orphaned_files_processed': 0,
            'backups_archived': 0,
            'conflicts_resolved': 0,
            'data_volume_processed': 0
        }
        
        # Step 1: Merge duplicate memory storage systems
        self._merge_memory_storage_systems(consolidation_results)
        
        # Step 2: Process orphaned JSON files
        self._process_orphaned_files(consolidation_results)
        
        # Step 3: Archive backup files
        self._archive_backup_files(consolidation_results)
        
        # Step 4: Consolidate weight files
        self._consolidate_weight_files(consolidation_results)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        self.logger.info(f"Data consolidation completed in {execution_time:.2f}s")
        self.logger.info(f"Results: {consolidation_results}")
        
        return consolidation_results
        
    def _merge_memory_storage_systems(self, results: Dict):
        """
        Merge duplicate storage systems into unified stores
        
        Source: unified_migration_system.py
        """
        memory_files = [
            ('bridge.json', 'bridge_memory.json'),
            ('logic.json', 'logic_memory.json'),
            ('symbolic.json', 'symbolic_memory.json')
        ]
        
        for legacy_file, unified_file in memory_files:
            legacy_path = self.data_dir / legacy_file
            unified_path = self.data_dir / unified_file
            
            if legacy_path.exists() and legacy_path.stat().st_size > 2:  # More than just "[]"
                try:
                    # Load legacy data
                    with open(legacy_path, 'r', encoding='utf-8') as f:
                        legacy_data = json.load(f)
                    
                    # Load unified data
                    unified_data = []
                    if unified_path.exists():
                        with open(unified_path, 'r', encoding='utf-8') as f:
                            unified_data = json.load(f)
                    
                    # Merge if legacy has data
                    if legacy_data:
                        if isinstance(legacy_data, list):
                            unified_data.extend(legacy_data)
                        else:
                            unified_data.append(legacy_data)
                        
                        # Save merged data
                        with open(unified_path, 'w', encoding='utf-8') as f:
                            json.dump(unified_data, f, indent=2)
                        
                        # Archive legacy file
                        backup_path = self.data_dir / f"{legacy_file}.archived"
                        legacy_path.rename(backup_path)
                        
                        results['memory_files_merged'] += 1
                        self.logger.info(f"Merged {legacy_file} into {unified_file}")
                        
                except Exception as e:
                    self.logger.error(f"Error merging {legacy_file}: {e}")
                    
    def _process_orphaned_files(self, results: Dict):
        """
        Process potentially orphaned JSON files
        
        Source: unified_migration_system.py
        """
        orphaned_patterns = [
            'test_symbol_memory_*.json',
            '*_backup.json',
            'temp_*.json'
        ]
        
        for pattern in orphaned_patterns:
            for file_path in self.data_dir.glob(pattern):
                try:
                    file_size = file_path.stat().st_size
                    results['data_volume_processed'] += file_size
                    
                    # Move to orphaned directory
                    orphaned_dir = self.data_dir / 'orphaned'
                    orphaned_dir.mkdir(exist_ok=True)
                    
                    new_path = orphaned_dir / file_path.name
                    file_path.rename(new_path)
                    
                    results['orphaned_files_processed'] += 1
                    self.logger.info(f"Moved orphaned file: {file_path.name}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing orphaned file {file_path}: {e}")
                    
    def _archive_backup_files(self, results: Dict):
        """
        Archive backup files after verification
        
        Source: unified_migration_system.py
        """
        backup_files = list(self.data_dir.glob('*.backup')) + list(self.data_dir.glob('*_backup.json'))
        
        if backup_files:
            backup_archive = self.data_dir / 'backups'
            backup_archive.mkdir(exist_ok=True)
            
            for backup_file in backup_files:
                try:
                    new_path = backup_archive / backup_file.name
                    backup_file.rename(new_path)
                    results['backups_archived'] += 1
                    
                except Exception as e:
                    self.logger.error(f"Error archiving backup {backup_file}: {e}")
                    
    def _consolidate_weight_files(self, results: Dict):
        """
        Consolidate multiple weight files into unified configuration
        
        Source: unified_migration_system.py
        """
        weight_files = [
            'adaptive_weights.json',
            'weight_momentum.json', 
            'weight_evolution_history.json'
        ]
        
        consolidated_weights = {
            'current': {},
            'history': [],
            'momentum': {},
            'metadata': {
                'last_consolidation': datetime.now(timezone.utc).isoformat(),
                'source_files': weight_files
            }
        }
        
        for weight_file in weight_files:
            file_path = self.data_dir / weight_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if weight_file == 'adaptive_weights.json':
                        consolidated_weights['current'] = data
                    elif weight_file == 'weight_momentum.json':
                        consolidated_weights['momentum'] = data
                    elif weight_file == 'weight_evolution_history.json':
                        consolidated_weights['history'] = data
                        
                except Exception as e:
                    self.logger.error(f"Error consolidating {weight_file}: {e}")
        
        # Save consolidated weights
        consolidated_path = self.data_dir / 'unified_weights.json'
        with open(consolidated_path, 'w', encoding='utf-8') as f:
            json.dump(consolidated_weights, f, indent=2)
            
        self.logger.info("Consolidated weight files into unified_weights.json")

class TrailLogAnalyzer:
    """
    Analyzes large trail log files for migration insights
    
    Source: unified_migration_system.py
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('TrailLogAnalyzer')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def extract_migration_insights(self) -> Dict[str, Any]:
        """
        Extract patterns from trail logs for migration enhancement
        
        Source: unified_migration_system.py
        """
        insights = {
            'high_engagement_patterns': [],
            'logic_vs_symbolic_preferences': {},
            'successful_interaction_features': [],
            'emotional_context_indicators': {},
            'content_classification_hints': {}
        }
        
        # Analyze trail_log.json if it exists and is substantial
        trail_log_path = self.data_dir / 'trail_log.json'
        if trail_log_path.exists() and trail_log_path.stat().st_size > 1000:  # > 1KB
            try:
                insights.update(self._analyze_trail_log(trail_log_path))
            except Exception as e:
                self.logger.error(f"Error analyzing trail log: {e}")
        
        # Analyze symbol occurrence patterns
        symbol_log_path = self.data_dir / 'symbol_occurrence_log.json'
        if symbol_log_path.exists():
            try:
                insights.update(self._analyze_symbol_patterns(symbol_log_path))
            except Exception as e:
                self.logger.error(f"Error analyzing symbol patterns: {e}")
        
        return insights
        
    def _analyze_trail_log(self, log_path: Path) -> Dict[str, Any]:
        """
        Analyze trail log for user interaction patterns
        
        Source: unified_migration_system.py
        """
        insights = {}
        
        try:
            # For large files, process in chunks
            if log_path.stat().st_size > 10 * 1024 * 1024:  # > 10MB
                insights = self._analyze_large_trail_log(log_path)
            else:
                with open(log_path, 'r', encoding='utf-8') as f:
                    trail_data = json.load(f)
                insights = self._process_trail_data(trail_data)
                
        except Exception as e:
            self.logger.error(f"Error processing trail log: {e}")
            insights = {'error': str(e)}
            
        return insights
        
    def _analyze_large_trail_log(self, log_path: Path) -> Dict[str, Any]:
        """
        Process large trail logs in chunks
        
        Source: unified_migration_system.py
        """
        insights = {
            'total_entries': 0,
            'high_engagement_sessions': [],
            'logic_indicators': [],
            'symbolic_indicators': [],
            'processing_note': 'Large file processed in chunks'
        }
        
        try:
            # Sample-based analysis for very large files
            with open(log_path, 'r', encoding='utf-8') as f:
                # Read first and last portions for pattern analysis
                start_chunk = f.read(1024 * 100)  # First 100KB
                f.seek(-1024 * 100, 2)  # Last 100KB
                end_chunk = f.read()
                
            # Extract patterns from chunks
            for chunk in [start_chunk, end_chunk]:
                if 'emotional' in chunk.lower() or 'feeling' in chunk.lower():
                    insights['symbolic_indicators'].append('emotional_language_detected')
                if 'analyze' in chunk.lower() or 'data' in chunk.lower():
                    insights['logic_indicators'].append('analytical_language_detected')
                    
        except Exception as e:
            self.logger.error(f"Error processing large trail log: {e}")
            
        return insights
        
    def _process_trail_data(self, trail_data: Union[List, Dict]) -> Dict[str, Any]:
        """
        Process loaded trail data for insights
        
        Source: unified_migration_system.py
        """
        insights = {
            'engagement_patterns': [],
            'content_preferences': {},
            'interaction_success_rate': 0.0
        }
        
        if isinstance(trail_data, list):
            insights['total_entries'] = len(trail_data)
            
            # Analyze entries for patterns
            emotional_count = 0
            logical_count = 0
            
            for entry in trail_data[:100]:  # Sample first 100 entries
                if isinstance(entry, dict):
                    content = str(entry).lower()
                    if any(word in content for word in ['emotion', 'feel', 'heart', 'soul']):
                        emotional_count += 1
                    if any(word in content for word in ['logic', 'analyze', 'data', 'compute']):
                        logical_count += 1
                        
            insights['content_preferences'] = {
                'emotional_tendency': emotional_count / min(100, len(trail_data)),
                'logical_tendency': logical_count / min(100, len(trail_data))
            }
            
        return insights
        
    def _analyze_symbol_patterns(self, symbol_log_path: Path) -> Dict[str, Any]:
        """
        Analyze symbol occurrence patterns for migration hints
        
        Source: unified_migration_system.py
        """
        symbol_insights = {
            'frequent_symbols': [],
            'symbol_cooccurrence': {},
            'classification_hints': {}
        }
        
        try:
            with open(symbol_log_path, 'r', encoding='utf-8') as f:
                symbol_data = json.load(f)
                
            if isinstance(symbol_data, dict):
                # Find most frequent symbols
                symbol_counts = {}
                for entry, data in symbol_data.items():
                    if isinstance(data, dict) and 'count' in data:
                        symbol_counts[entry] = data['count']
                        
                # Sort by frequency
                frequent = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                symbol_insights['frequent_symbols'] = frequent
                
        except Exception as e:
            self.logger.error(f"Error analyzing symbol patterns: {e}")
            
        return symbol_insights

class ConflictResolver:
    """
    Resolves conflicts between different migration signals
    
    Source: unified_migration_system.py
    """
    
    def __init__(self):
        self.precedence_rules = {
            'user_trail_patterns': 1,     # Highest priority - actual user behavior
            'symbol_cooccurrence': 2,     # Second - learned symbolic relationships  
            'confidence_gates': 3,        # Third - mathematical confidence
            'weight_evolution': 4,        # Fourth - system-level optimization
            'default_classification': 5   # Lowest - fallback
        }
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('ConflictResolver')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def detect_conflicts(self, migration_signals: Dict[str, List]) -> List[Dict]:
        """
        Detect items with conflicting migration signals
        
        Source: unified_migration_system.py
        """
        conflicts = []
        
        # Find items appearing in multiple conflicting signals
        all_items = set()
        for signal_type, items in migration_signals.items():
            all_items.update(items)
            
        for item in all_items:
            item_signals = {}
            for signal_type, items in migration_signals.items():
                if item in items:
                    item_signals[signal_type] = True
                    
            # Check for conflicts (item suggested for both logic and symbolic)
            if len(item_signals) > 1:
                conflicts.append({
                    'item': item,
                    'conflicting_signals': list(item_signals.keys()),
                    'resolution_needed': True
                })
                
        self.logger.info(f"Detected {len(conflicts)} migration conflicts")
        return conflicts
        
    def resolve_conflicts(self, conflicts: List[Dict]) -> List[Dict]:
        """
        Resolve conflicts using precedence rules
        
        Source: unified_migration_system.py
        """
        resolved = []
        
        for conflict in conflicts:
            # Apply precedence rules
            highest_priority = float('inf')
            winning_signal = None
            
            for signal in conflict['conflicting_signals']:
                priority = self.precedence_rules.get(signal, 99)
                if priority < highest_priority:
                    highest_priority = priority
                    winning_signal = signal
                    
            conflict['resolved_signal'] = winning_signal
            conflict['resolution_priority'] = highest_priority
            resolved.append(conflict)
            
        self.logger.info(f"Resolved {len(resolved)} conflicts")
        return resolved

class UnifiedMigrationSystem:
    """
    Main orchestrator for consolidated migration system
    
    Source: unified_migration_system.py
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Core components
        if UNIFIED_MEMORY_AVAILABLE:
            self.memory = get_unified_memory(data_dir=str(self.data_dir))
        else:
            self.memory = None
            
        if WEIGHT_SYSTEM_AVAILABLE:
            self.weight_system = UnifiedWeightSystem(data_dir=str(self.data_dir))
        else:
            self.weight_system = None
        
        # Migration components
        self.data_consolidator = DataConsolidator(str(self.data_dir))
        self.trail_analyzer = TrailLogAnalyzer(str(self.data_dir))
        self.conflict_resolver = ConflictResolver()
        
        # Session tracking
        self.session_log_path = self.data_dir / 'unified_migration_sessions.json'
        
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('UnifiedMigrationSystem')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def run_unified_migration_cycle(self) -> UnifiedMigrationSession:
        """
        Execute complete unified migration cycle
        
        Source: unified_migration_system.py
        """
        session_start = datetime.now()
        session_id = f"migration_{session_start.strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"Starting unified migration cycle: {session_id}")
        
        # Phase 1: Data Consolidation
        consolidation_start = datetime.now()
        consolidation_data = self.data_consolidator.consolidate_orphaned_data()
        consolidation_time = (datetime.now() - consolidation_start).total_seconds()
        
        consolidation_result = MigrationResult(
            operation_type="data_consolidation",
            items_processed=consolidation_data.get('orphaned_files_processed', 0),
            items_migrated=consolidation_data.get('memory_files_merged', 0),
            conflicts_resolved=consolidation_data.get('conflicts_resolved', 0),
            insights_applied=0,
            execution_time=consolidation_time,
            metadata=consolidation_data
        )
        
        # Phase 2: Trail Analysis and Insights
        insights_start = datetime.now()
        trail_insights = self.trail_analyzer.extract_migration_insights()
        insights_time = (datetime.now() - insights_start).total_seconds()
        
        # Phase 3: Enhanced Forward Migration
        forward_start = datetime.now()
        forward_result = self._run_enhanced_forward_migration(trail_insights)
        forward_time = (datetime.now() - forward_start).total_seconds()
        forward_result.execution_time = forward_time
        
        # Phase 4: Reverse Audit with Context
        reverse_start = datetime.now()
        reverse_result = self._run_contextual_reverse_audit(trail_insights)
        reverse_time = (datetime.now() - reverse_start).total_seconds()
        reverse_result.execution_time = reverse_time
        
        # Phase 5: Weight Optimization
        weight_start = datetime.now()
        weight_result = self._run_integrated_weight_optimization()
        weight_time = (datetime.now() - weight_start).total_seconds()
        weight_result.execution_time = weight_time
        
        # Calculate total execution time
        total_time = (datetime.now() - session_start).total_seconds()
        
        # Create session record
        session = UnifiedMigrationSession(
            session_id=session_id,
            timestamp=session_start.isoformat(),
            forward_migration=forward_result,
            reverse_audit=reverse_result,
            weight_optimization=weight_result,
            data_consolidation=consolidation_result,
            total_execution_time=total_time,
            system_health=self._calculate_system_health()
        )
        
        # Log session
        self._log_migration_session(session)
        
        self.logger.info(f"Unified migration cycle completed in {total_time:.2f}s")
        return session
        
    def _run_enhanced_forward_migration(self, insights: Dict) -> MigrationResult:
        """
        Run forward migration enhanced with trail insights
        
        Source: unified_migration_system.py
        """
        items_processed = 0
        items_migrated = 0
        insights_applied = 0
        
        try:
            # Get bridge items
            if self.memory:
                bridge_stats = self.memory.get_memory_statistics() if hasattr(self.memory, 'get_memory_statistics') else {}
                bridge_items = bridge_stats.get('items', {}).get('bridge', [])
                items_processed = len(bridge_items)
            
            # Apply insights-based migration
            if insights.get('content_preferences'):
                prefs = insights['content_preferences']
                if prefs.get('emotional_tendency', 0) > 0.5:
                    insights_applied += 1
                if prefs.get('logical_tendency', 0) > 0.5:
                    insights_applied += 1
            
            # Simulate migration (would implement actual logic here)
            items_migrated = min(items_processed // 4, 10)  # Migrate up to 25% or 10 items
            
        except Exception as e:
            self.logger.error(f"Error in forward migration: {e}")
            
        return MigrationResult(
            operation_type="forward_migration",
            items_processed=items_processed,
            items_migrated=items_migrated,
            conflicts_resolved=0,
            insights_applied=insights_applied,
            execution_time=0.0,  # Set by caller
            metadata={"insights_used": list(insights.keys())}
        )
        
    def _run_contextual_reverse_audit(self, insights: Dict) -> MigrationResult:
        """
        Run reverse audit with contextual insights
        
        Source: unified_migration_system.py
        """
        items_processed = 0
        items_migrated = 0
        
        try:
            # Get logic and symbolic items for audit
            if self.memory:
                stats = self.memory.get_memory_statistics() if hasattr(self.memory, 'get_memory_statistics') else {}
                items = stats.get('items', {})
                logic_items = items.get('logic', [])
                symbolic_items = items.get('symbolic', [])
                
                items_processed = len(logic_items) + len(symbolic_items)
            
            # Simulate reverse migration (would implement actual audit logic)
            items_migrated = min(items_processed // 10, 5)  # Move back up to 10% or 5 items
            
        except Exception as e:
            self.logger.error(f"Error in reverse audit: {e}")
            
        return MigrationResult(
            operation_type="reverse_audit",
            items_processed=items_processed,
            items_migrated=items_migrated,
            conflicts_resolved=0,
            insights_applied=0,
            execution_time=0.0,  # Set by caller
            metadata={"audit_scope": "logic_and_symbolic"}
        )
        
    def _run_integrated_weight_optimization(self) -> MigrationResult:
        """
        Run weight optimization with integrated data
        
        Source: unified_migration_system.py
        """
        try:
            # Get current system state
            memory_stats = {}
            if self.memory and hasattr(self.memory, 'get_memory_statistics'):
                memory_stats = self.memory.get_memory_statistics()
            
            # Run weight evolution
            if self.weight_system:
                weight_decision = self.weight_system.calculate_unified_weights(
                    memory_stats=memory_stats
                )
                
                return MigrationResult(
                    operation_type="weight_optimization",
                    items_processed=1,  # The weight system itself
                    items_migrated=0,
                    conflicts_resolved=0,
                    insights_applied=1,
                    execution_time=0.0,  # Set by caller
                    metadata={
                        "logic_scale": weight_decision.logic_scale,
                        "symbolic_scale": weight_decision.symbolic_scale,
                        "confidence_modifier": weight_decision.confidence_modifier
                    }
                )
            else:
                return MigrationResult(
                    operation_type="weight_optimization",
                    items_processed=0,
                    items_migrated=0,
                    conflicts_resolved=0,
                    insights_applied=0,
                    execution_time=0.0,
                    metadata={"error": "Weight system not available"}
                )
            
        except Exception as e:
            self.logger.error(f"Error in weight optimization: {e}")
            return MigrationResult(
                operation_type="weight_optimization",
                items_processed=0,
                items_migrated=0,
                conflicts_resolved=0,
                insights_applied=0,
                execution_time=0.0,
                metadata={"error": str(e)}
            )
            
    def _calculate_system_health(self) -> Dict[str, Any]:
        """
        Calculate overall system health metrics
        
        Source: unified_migration_system.py
        """
        try:
            if self.memory and hasattr(self.memory, 'get_memory_statistics'):
                stats = self.memory.get_memory_statistics()
                distribution = stats.get('distribution', {})
                
                health = {
                    'bridge_size': distribution.get('bridge_pct', 0),
                    'specialization_balance': abs(distribution.get('logic_pct', 0) - distribution.get('symbolic_pct', 0)),
                    'total_items': sum(stats.get('items', {}).values()) if isinstance(stats.get('items'), dict) else 0,
                    'memory_efficiency': 1.0 - (distribution.get('bridge_pct', 100) / 100),
                    'system_status': 'healthy' if distribution.get('bridge_pct', 100) < 30 else 'needs_optimization'
                }
                
                return health
            else:
                return {'system_status': 'memory_unavailable', 'error': 'Memory system not accessible'}
            
        except Exception as e:
            self.logger.error(f"Error calculating system health: {e}")
            return {'system_status': 'error', 'error': str(e)}
            
    def _log_migration_session(self, session: UnifiedMigrationSession):
        """
        Log migration session for analysis
        
        Source: unified_migration_system.py
        """
        try:
            sessions = []
            if self.session_log_path.exists():
                with open(self.session_log_path, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
                    
            sessions.append(asdict(session))
            sessions = sessions[-100:]  # Keep last 100 sessions
            
            with open(self.session_log_path, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error logging session: {e}")
            
    def get_migration_history(self) -> List[Dict]:
        """
        Get historical migration sessions
        
        Source: unified_migration_system.py
        """
        try:
            if self.session_log_path.exists():
                with open(self.session_log_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Error reading migration history: {e}")
            return []
            
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and recommendations
        
        Source: unified_migration_system.py
        """
        try:
            health = self._calculate_system_health()
            history = self.get_migration_history()
            
            recommendations = []
            if health.get('bridge_size', 0) > 50:
                recommendations.append("High bridge size - consider running migration cycle")
            if health.get('specialization_balance', 0) > 80:
                recommendations.append("Highly imbalanced specialization - check weight optimization")
            if len(history) == 0:
                recommendations.append("No migration history - run initial migration cycle")
                
            return {
                'system_health': health,
                'migration_sessions': len(history),
                'last_migration': history[-1]['timestamp'] if history else None,
                'recommendations': recommendations,
                'status': 'operational'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'recommendations': ['Check system logs and fix errors']
            }

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def run_migration_cycle(data_dir: str = "data") -> UnifiedMigrationSession:
    """
    Run a complete migration cycle with unified system
    
    Source: unified_migration_system.py
    """
    migration_system = UnifiedMigrationSystem(data_dir)
    return migration_system.run_unified_migration_cycle()

def get_system_health(data_dir: str = "data") -> Dict[str, Any]:
    """
    Get current system health and status
    
    Source: unified_migration_system.py
    """
    migration_system = UnifiedMigrationSystem(data_dir)
    return migration_system.get_system_status()

def consolidate_data_only(data_dir: str = "data") -> Dict[str, Any]:
    """
    Run only data consolidation without full migration
    
    Source: unified_migration_system.py
    """
    consolidator = DataConsolidator(data_dir)
    return consolidator.consolidate_orphaned_data()

def run_tripartite_migration(data_dir: str = "data") -> bool:
    """
    Run tripartite memory migration
    
    Source: migrate_to_tripartite.py (main function)
    """
    print("🚀 Starting tripartite memory migration...")
    print()
    
    success = True
    
    # Fix symbol memory format first
    if not fix_symbol_memory():
        success = False
    
    print()
    
    # Migrate vectors to tripartite system
    if not migrate_vectors_to_tripartite():
        success = False
    
    print()
    
    if success:
        print("🎉 Migration completed successfully!")
        print()
        print("Next steps:")
        print("1. Restart your AI system")
        print("2. The system should now show the correct memory counts:")
        print("   - Logic memory: factual, technical content")
        print("   - Symbolic memory: emotional, creative content")  
        print("   - Bridge memory: temporary intake for unresolved content awaiting classification")
        print("3. Your AI will have access to its previous learning in the new architecture")
    else:
        print("❌ Migration failed or incomplete")
    
    return success

def run_reverse_audit(memory_system, confidence_threshold: float = 0.3) -> Dict[str, Any]:
    """
    Run reverse migration audit on memory system
    
    Source: reverse_migration.py
    """
    auditor = ReverseMigrationAuditor(memory_system, confidence_threshold)
    total_reversed = auditor.audit_all()
    summary = auditor.get_audit_summary()
    
    return {
        'total_reversed': total_reversed,
        'summary': summary,
        'auditor': auditor
    }

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("🔄 Memory Migration Utilities Demo")
    print("=" * 60)
    
    # Demo tripartite migration
    print("1️⃣ Testing tripartite migration...")
    try:
        # Test migration readiness
        data_dir = Path("data")
        vector_file = data_dir / "vector_memory.json"
        
        if vector_file.exists():
            print(f"   ✅ Vector memory file found")
            success = run_tripartite_migration()
            if success:
                print("   ✅ Tripartite migration completed")
            else:
                print("   ⚠️ Tripartite migration had issues")
        else:
            print("   ℹ️ No vector memory to migrate")
    except Exception as e:
        print(f"   ❌ Migration test failed: {e}")
    
    # Demo data consolidation
    print("\n2️⃣ Testing data consolidation...")
    try:
        consolidator = DataConsolidator()
        results = consolidator.consolidate_orphaned_data()
        print(f"   ✅ Consolidated {results.get('memory_files_merged', 0)} memory files")
        print(f"   ✅ Processed {results.get('orphaned_files_processed', 0)} orphaned files")
    except Exception as e:
        print(f"   ❌ Consolidation test failed: {e}")
    
    # Demo trail analysis
    print("\n3️⃣ Testing trail analysis...")
    try:
        analyzer = TrailLogAnalyzer()
        insights = analyzer.extract_migration_insights()
        print(f"   ✅ Extracted insights: {list(insights.keys())}")
    except Exception as e:
        print(f"   ❌ Trail analysis test failed: {e}")
    
    # Demo unified migration system
    print("\n4️⃣ Testing unified migration system...")
    try:
        migration_system = UnifiedMigrationSystem()
        status = migration_system.get_system_status()
        print(f"   ✅ System status: {status.get('status', 'unknown')}")
        print(f"   ✅ Migration sessions: {status.get('migration_sessions', 0)}")
    except Exception as e:
        print(f"   ❌ Unified migration test failed: {e}")
    
    print("\n✅ Memory Migration Utilities Demo Complete!")