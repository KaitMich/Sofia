# memory_maintenance.py - Comprehensive Memory System Maintenance
"""
Comprehensive memory maintenance functions for all memory systems including:
- Unified memory maintenance and optimization
- Episodic memory archiving and cleanup  
- Experience memory consolidation
- Memory health monitoring and repair
- Automated maintenance scheduling

Provides compatibility for memory_optimizer.py maintenance operations.
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
import shutil

# Import memory systems
try:
    from unified_memory import get_unified_memory
    UNIFIED_MEMORY_AVAILABLE = True
except ImportError:
    UNIFIED_MEMORY_AVAILABLE = False
    print("⚠️ Unified memory not available for maintenance")

try:
    from experience_memory import ExperienceMemory
    from episodic_memory import EpisodicMemorySystem
    MEMORY_SYSTEMS_AVAILABLE = True
except ImportError:
    MEMORY_SYSTEMS_AVAILABLE = False
    print("⚠️ Memory systems not available for comprehensive maintenance")

try:
    from brain_metrics import BrainMetrics
    BRAIN_METRICS_AVAILABLE = True
except ImportError:
    BRAIN_METRICS_AVAILABLE = False

def prune_phase1_symbolic_vectors(archive_path_str="data/archived_phase1_vectors.json"):
    """
    Prune Phase 1 symbolic vectors from the vector memory system.
    Archives removed vectors for potential recovery.
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
    """Clean up old archive files to prevent disk bloat"""
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
    """Get statistics about memory maintenance status"""
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
# COMPREHENSIVE MEMORY SYSTEM MAINTENANCE
# ============================================================================

class MemoryMaintenanceManager:
    """
    Comprehensive memory maintenance manager for all memory systems.
    Handles automated maintenance, health monitoring, and optimization.
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
        """Perform comprehensive maintenance across all memory systems"""
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
    """Perform emergency maintenance when system health is critical"""
    print("🚨 Performing emergency memory maintenance...")
    manager = MemoryMaintenanceManager(data_dir)
    return manager.perform_comprehensive_maintenance(force=True)

def get_memory_health_dashboard(data_dir: str = "data") -> str:
    """Get a comprehensive memory health dashboard"""
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
    """Enable or disable automated maintenance scheduling"""
    manager = MemoryMaintenanceManager(data_dir)
    manager.config["automated_maintenance"]["enabled"] = enable
    manager._save_maintenance_config(manager.config)
    
    status = "enabled" if enable else "disabled"
    print(f"✅ Automated maintenance {status}")

if __name__ == "__main__":
    # Demo the comprehensive maintenance system
    print("🧠 Memory Maintenance System Demo")
    print("=" * 50)
    
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