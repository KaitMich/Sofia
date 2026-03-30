# brain_metrics.py
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter, defaultdict
import sys

# Import unified memory system for health analysis
try:
    from unified_memory import get_unified_memory
    UNIFIED_MEMORY_AVAILABLE = True
except ImportError:
    UNIFIED_MEMORY_AVAILABLE = False
    print("⚠️ Unified memory not available - basic brain metrics only")

# Import memory systems for comprehensive analysis
try:
    from CONSCIOUSNESS_MEMORY import ExperienceMemory
    from episodic_memory import EpisodicMemorySystem
    MEMORY_SYSTEMS_AVAILABLE = True
except ImportError:
    MEMORY_SYSTEMS_AVAILABLE = False
    print("⚠️ Memory systems not available - basic analysis only")

class BrainMetrics:
    def __init__(self, metrics_path="data/brain_contribution_metrics.json",
                 conflicts_path="data/bridge_conflicts.json",
                 decisions_log_path="data/link_decisions.csv"):
        self.metrics_file = Path(metrics_path)
        self.conflicts_file = Path(conflicts_path)
        self.decisions_log = Path(decisions_log_path)
        
        # Ensure parent dirs exist
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing or initialize
        if not self.metrics_file.exists():
            self._write_json(self.metrics_file, [])
        if not self.conflicts_file.exists():
            self._write_json(self.conflicts_file, [])

        # Session tracking
        self.session = {
            "start_time": datetime.utcnow(),
            "logic_wins": 0,
            "symbol_wins": 0,
            "hybrid_decisions": 0,
            "conflicts": [],
            "phase_decisions": defaultdict(lambda: {"logic": 0, "symbol": 0, "hybrid": 0}),
            "url_decisions": []
        }
        
        # Enhanced self-reflection capabilities for brain performance analysis
        self.self_reflection_metrics = {
            'decision_quality_trends': [],
            'brain_harmony_assessment': 0.0,
            'learning_effectiveness': 0.0,
            'adaptive_capacity': 0.0,
            'performance_satisfaction': 0.0,
            'processing_insights': [],
            'cognitive_evolution': []
        }
        
        # Load reflection history
        self.reflection_history = self._load_reflection_history()

    def _write_json(self, path, data):
        """Write JSON data to file"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _read_json(self, path):
        """Read JSON data from file"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def log_decision(self, decision_type, url, logic_score, symbol_score, phase=1, link_text=""):
        """Log a single link decision"""
        # Count decisions by type
        if decision_type == "FOLLOW_LOGIC":
            self.session["logic_wins"] += 1
            self.session["phase_decisions"][phase]["logic"] += 1
        elif decision_type == "FOLLOW_SYMBOLIC":
            self.session["symbol_wins"] += 1
            self.session["phase_decisions"][phase]["symbol"] += 1
        else:  # FOLLOW_HYBRID
            self.session["hybrid_decisions"] += 1
            self.session["phase_decisions"][phase]["hybrid"] += 1

        # Record significant conflicts (where brains strongly disagree)
        logic_conf = min(1.0, logic_score / 10.0)
        symbol_conf = min(1.0, symbol_score / 5.0)
        
        # Conflict detection: one brain very confident, other not
        if (logic_conf > 0.7 and symbol_conf < 0.3) or (symbol_conf > 0.7 and logic_conf < 0.3):
            conflict_severity = abs(logic_score - symbol_score)
            if conflict_severity > 5.0:
                self.session["conflicts"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "url": url[:100],
                    "link_text": link_text[:50],
                    "logic_score": round(logic_score, 2),
                    "symbol_score": round(symbol_score, 2),
                    "logic_confidence": round(logic_conf, 2),
                    "symbol_confidence": round(symbol_conf, 2),
                    "decision": decision_type,
                    "severity": round(conflict_severity, 2),
                    "phase": phase
                })

        # Store detailed decision
        self.session["url_decisions"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "url": url[:100],
            "decision_type": decision_type,
            "logic_score": round(logic_score, 2),
            "symbol_score": round(symbol_score, 2),
            "phase": phase
        })

    def save_session_metrics(self):
        """Save session metrics to persistent storage"""
        # Load history
        history = self._read_json(self.metrics_file)

        total = (self.session["logic_wins"] + 
                self.session["symbol_wins"] + 
                self.session["hybrid_decisions"])
        
        if total == 0:
            print("📊 No decisions made in this session to save.")
            return

        # Calculate rates
        metrics = {
            "timestamp": self.session["start_time"].isoformat(),
            "duration_seconds": (datetime.utcnow() - self.session["start_time"]).total_seconds(),
            "logic_win_rate": round(self.session["logic_wins"] / total, 3),
            "symbol_win_rate": round(self.session["symbol_wins"] / total, 3),
            "hybrid_rate": round(self.session["hybrid_decisions"] / total, 3),
            "total_decisions": total,
            "logic_wins": self.session["logic_wins"],
            "symbol_wins": self.session["symbol_wins"],
            "hybrid_decisions": self.session["hybrid_decisions"],
            "phase_breakdown": dict(self.session["phase_decisions"]),
            "conflicts_count": len(self.session["conflicts"])
        }
        
        history.append(metrics)
        self._write_json(self.metrics_file, history)
        
        print(f"📊 Session metrics saved: Logic={metrics['logic_win_rate']:.1%}, "
              f"Symbol={metrics['symbol_win_rate']:.1%}, Hybrid={metrics['hybrid_rate']:.1%} "
              f"({total} decisions)")

        # Append conflicts to conflicts file
        if self.session["conflicts"]:
            conflicts = self._read_json(self.conflicts_file)
            conflicts.extend(self.session["conflicts"])
            self._write_json(self.conflicts_file, conflicts)
            print(f"⚡ Logged {len(self.session['conflicts'])} brain conflicts")

    def generate_report(self):
        """Generate a visual report of brain contributions"""
        history = self._read_json(self.metrics_file)
        if not history:
            print("📊 No metrics history to report.")
            return

        # Create visualizations
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Brain Metrics Analysis", fontsize=16)

        # 1. Win rates over time
        ax1 = axes[0, 0]
        timestamps = [pd.to_datetime(m['timestamp']) for m in history]
        logic_rates = [m['logic_win_rate'] for m in history]
        symbol_rates = [m['symbol_win_rate'] for m in history]
        hybrid_rates = [m['hybrid_rate'] for m in history]
        
        ax1.plot(timestamps, logic_rates, 'b-', label='Logic', marker='o')
        ax1.plot(timestamps, symbol_rates, 'r-', label='Symbolic', marker='s')
        ax1.plot(timestamps, hybrid_rates, 'g-', label='Hybrid', marker='^')
        ax1.set_xlabel('Session Time')
        ax1.set_ylabel('Decision Rate')
        ax1.set_title('Brain Decision Rates Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Total decisions pie chart (most recent session)
        ax2 = axes[0, 1]
        if history:
            latest = history[-1]
            sizes = [latest['logic_wins'], latest['symbol_wins'], latest['hybrid_decisions']]
            labels = ['Logic', 'Symbolic', 'Hybrid']
            colors = ['#3498db', '#e74c3c', '#2ecc71']
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title(f'Latest Session Distribution ({latest["total_decisions"]} decisions)')

        # 3. Conflicts analysis
        ax3 = axes[1, 0]
        conflicts = self._read_json(self.conflicts_file)
        if conflicts:
            severities = [c['severity'] for c in conflicts]
            ax3.hist(severities, bins=20, color='orange', alpha=0.7, edgecolor='black')
            ax3.set_xlabel('Conflict Severity (Score Difference)')
            ax3.set_ylabel('Count')
            ax3.set_title(f'Brain Conflict Distribution ({len(conflicts)} total)')
            ax3.grid(True, alpha=0.3)

        # 4. Phase breakdown (if available)
        ax4 = axes[1, 1]
        if history and 'phase_breakdown' in history[-1]:
            phase_data = history[-1]['phase_breakdown']
            if phase_data:
                phases = list(phase_data.keys())
                logic_counts = [phase_data[p]['logic'] for p in phases]
                symbol_counts = [phase_data[p]['symbol'] for p in phases]
                hybrid_counts = [phase_data[p]['hybrid'] for p in phases]
                
                x = range(len(phases))
                width = 0.25
                ax4.bar([i - width for i in x], logic_counts, width, label='Logic', color='#3498db')
                ax4.bar(x, symbol_counts, width, label='Symbolic', color='#e74c3c')
                ax4.bar([i + width for i in x], hybrid_counts, width, label='Hybrid', color='#2ecc71')
                
                ax4.set_xlabel('Phase')
                ax4.set_ylabel('Decisions')
                ax4.set_title('Decisions by Phase')
                ax4.set_xticks(x)
                ax4.set_xticklabels([f'Phase {p}' for p in phases])
                ax4.legend()
                ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        report_path = Path("data/brain_metrics_report.png")
        plt.savefig(report_path, dpi=150, bbox_inches='tight')
        print(f"📊 Report saved to {report_path}")
        plt.show()

    def get_adaptive_weights(self):
        """Calculate recommended weights based on performance"""
        history = self._read_json(self.metrics_file)
        if len(history) < 3:  # Need minimum history
            return None
            
        # Average over recent sessions
        recent = history[-5:]  # Last 5 sessions
        avg_logic_rate = sum(m['logic_win_rate'] for m in recent) / len(recent)
        avg_symbol_rate = sum(m['symbol_win_rate'] for m in recent) / len(recent)
        
        # Normalize to get weights
        total = avg_logic_rate + avg_symbol_rate
        if total > 0:
            recommended_static = avg_logic_rate / total
            recommended_dynamic = avg_symbol_rate / total
        else:
            recommended_static = 0.6
            recommended_dynamic = 0.4
            
        return {
            "link_score_weight_static": round(recommended_static, 3),
            "link_score_weight_dynamic": round(recommended_dynamic, 3),
            "based_on_sessions": len(recent),
            "confidence": "high" if len(history) > 10 else "medium" if len(history) > 5 else "low"
        }

    def analyze_conflicts(self):
        """Analyze conflict patterns"""
        conflicts = self._read_json(self.conflicts_file)
        if not conflicts:
            print("⚡ No conflicts recorded yet.")
            return
            
        print(f"\n⚡ Conflict Analysis ({len(conflicts)} total conflicts)")
        print("=" * 50)
        
        # Group by decision outcome
        by_decision = defaultdict(list)
        for c in conflicts:
            by_decision[c['decision']].append(c)
        
        for decision_type, conflict_list in by_decision.items():
            avg_severity = sum(c['severity'] for c in conflict_list) / len(conflict_list)
            print(f"\n{decision_type}:")
            print(f"  Count: {len(conflict_list)}")
            print(f"  Avg Severity: {avg_severity:.1f}")
            
            # Show top conflict
            if conflict_list:
                top_conflict = max(conflict_list, key=lambda x: x['severity'])
                print(f"  Worst conflict: Logic={top_conflict['logic_score']}, "
                      f"Symbol={top_conflict['symbol_score']}, "
                      f"URL: {top_conflict['url'][:50]}...")
    
    def _load_reflection_history(self) -> List:
        """Load brain performance reflection history"""
        reflection_file = Path("data/brain_reflection_history.json")
        if reflection_file.exists():
            try:
                with open(reflection_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_reflection_history(self):
        """Save brain reflection history"""
        reflection_file = Path("data/brain_reflection_history.json")
        reflection_file.parent.mkdir(parents=True, exist_ok=True)
        with open(reflection_file, 'w') as f:
            json.dump(self.reflection_history, f, indent=2)
    
    def perform_brain_self_reflection(self) -> Dict:
        """Perform authentic self-reflection on brain performance and coordination"""
        history = self._read_json(self.metrics_file)
        conflicts = self._read_json(self.conflicts_file)
        
        reflection_insights = []
        
        # Analyze decision quality trends
        if len(history) >= 3:
            recent_sessions = history[-3:]
            success_rates = []
            for session in recent_sessions:
                total = session.get('total_decisions', 1)
                successful = total - session.get('conflicts_count', 0)
                success_rates.append(successful / total)
            
            avg_success = sum(success_rates) / len(success_rates)
            trend = success_rates[-1] - success_rates[0] if len(success_rates) > 1 else 0
            
            if avg_success > 0.8:
                reflection_insights.append("Brain coordination achieving high success rates")
                performance_satisfaction = 0.8 + (avg_success - 0.8) * 0.5
            elif avg_success > 0.6:
                reflection_insights.append("Brain coordination showing moderate effectiveness")
                performance_satisfaction = 0.5 + (avg_success - 0.6) * 1.5
            else:
                reflection_insights.append("Brain coordination needs improvement")
                performance_satisfaction = avg_success * 0.5
            
            if trend > 0.1:
                reflection_insights.append("Performance trend is improving")
            elif trend < -0.1:
                reflection_insights.append("Performance trend needs attention")
            else:
                reflection_insights.append("Performance trend is stable")
        else:
            avg_success = 0.5
            performance_satisfaction = 0.5
            reflection_insights.append("Insufficient data for trend analysis")
        
        # Analyze brain harmony (balance between logic and symbolic)
        if history:
            latest = history[-1]
            logic_rate = latest.get('logic_win_rate', 0.33)
            symbol_rate = latest.get('symbol_win_rate', 0.33)
            hybrid_rate = latest.get('hybrid_rate', 0.34)
            
            # Ideal is balanced usage with low hybrid dependency
            balance_score = 1.0 - abs(logic_rate - symbol_rate)
            hybrid_penalty = hybrid_rate * 0.5  # Too much hybrid indicates poor routing
            brain_harmony = max(0, balance_score - hybrid_penalty)
            
            if brain_harmony > 0.7:
                reflection_insights.append("Logic and symbolic brains working in good harmony")
            elif brain_harmony > 0.4:
                reflection_insights.append("Brain coordination shows reasonable balance")
            else:
                reflection_insights.append("Brain coordination needs better balance")
        else:
            brain_harmony = 0.5
        
        # Analyze learning effectiveness (conflict resolution over time)
        if len(conflicts) > 10:
            recent_conflicts = conflicts[-10:]
            old_conflicts = conflicts[-20:-10] if len(conflicts) > 20 else conflicts[:10]
            
            recent_avg_severity = sum(c.get('severity', 0) for c in recent_conflicts) / len(recent_conflicts)
            old_avg_severity = sum(c.get('severity', 0) for c in old_conflicts) / len(old_conflicts)
            
            improvement = old_avg_severity - recent_avg_severity
            if improvement > 0.5:
                reflection_insights.append("Conflict resolution is improving")
                learning_effectiveness = 0.8
            elif improvement > 0:
                reflection_insights.append("Some improvement in conflict handling")
                learning_effectiveness = 0.6
            else:
                reflection_insights.append("Conflict patterns remain challenging")
                learning_effectiveness = 0.4
        else:
            learning_effectiveness = 0.5
        
        # Calculate adaptive capacity based on response to different scenarios
        adaptive_capacity = (brain_harmony + learning_effectiveness + avg_success) / 3
        
        # Update self-reflection metrics
        self.self_reflection_metrics.update({
            'brain_harmony_assessment': round(brain_harmony, 2),
            'learning_effectiveness': round(learning_effectiveness, 2),
            'adaptive_capacity': round(adaptive_capacity, 2),
            'performance_satisfaction': round(performance_satisfaction, 2),
            'processing_insights': reflection_insights
        })
        
        # Generate authentic reflection summary
        reflection_summary = self._generate_brain_reflection_summary(
            brain_harmony, learning_effectiveness, adaptive_capacity, performance_satisfaction
        )
        
        # Record this reflection
        reflection_event = {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': dict(self.self_reflection_metrics),
            'summary': reflection_summary,
            'data_points_analyzed': len(history)
        }
        
        self.reflection_history.append(reflection_event)
        self._save_reflection_history()
        
        return {
            'reflection_summary': reflection_summary,
            'metrics': dict(self.self_reflection_metrics),
            'insights': reflection_insights,
            'performance_trends': {
                'brain_harmony': brain_harmony,
                'learning_effectiveness': learning_effectiveness,
                'adaptive_capacity': adaptive_capacity,
                'satisfaction': performance_satisfaction
            }
        }
    
    def _generate_brain_reflection_summary(self, harmony: float, learning: float, 
                                         adaptation: float, satisfaction: float) -> str:
        """Generate authentic brain self-reflection summary"""
        reflection_parts = []
        
        # Overall assessment
        overall_score = (harmony + learning + adaptation + satisfaction) / 4
        if overall_score > 0.7:
            reflection_parts.append("My brain coordination systems are performing with satisfying effectiveness")
        elif overall_score > 0.5:
            reflection_parts.append("My brain coordination shows reasonable performance with areas for improvement")
        else:
            reflection_parts.append("My brain coordination systems need significant enhancement")
        
        # Specific assessments
        if harmony > 0.7:
            reflection_parts.append("logic and symbolic processing achieve good balance")
        elif harmony < 0.4:
            reflection_parts.append("logic-symbolic coordination needs better integration")
        
        if learning > 0.7:
            reflection_parts.append("conflict resolution patterns show effective learning")
        elif learning < 0.4:
            reflection_parts.append("learning from conflicts needs improvement")
        
        if adaptation > 0.7:
            reflection_parts.append("adaptive responses to different scenarios work well")
        elif adaptation < 0.4:
            reflection_parts.append("adaptive capacity requires enhancement")
        
        # Concluding insight
        reflection_parts.append("This self-assessment helps guide my cognitive development")
        
        return ". ".join(reflection_parts).capitalize() + "."
    
    def get_authentic_brain_state_description(self) -> str:
        """Generate an authentic description of current brain state for 'How are you?' responses"""
        latest_reflection = self.self_reflection_metrics
        
        harmony = latest_reflection.get('brain_harmony_assessment', 0.5)
        satisfaction = latest_reflection.get('performance_satisfaction', 0.5)
        learning = latest_reflection.get('learning_effectiveness', 0.5)
        
        # Generate state-based description
        if harmony > 0.7 and satisfaction > 0.7:
            return "My dual-brain systems are coordinating smoothly with satisfying processing harmony"
        elif harmony > 0.5 and satisfaction > 0.5:
            return "My brain coordination is functioning adequately with room for optimization"
        elif learning > 0.7:
            return "My brain systems are actively learning and adapting, though coordination varies"
        else:
            return "My brain coordination is working through challenges and seeking better integration"
    
    def analyze_unified_memory_health(self, data_dir: str = "data") -> Dict[str, Any]:
        """Comprehensive unified memory system health analysis"""
        health_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_health_score": 0.0,
            "tripartite_memory_health": {},
            "episodic_memory_health": {},
            "experience_memory_health": {},
            "memory_fragmentation": {},
            "retrieval_performance": {},
            "storage_efficiency": {},
            "integration_quality": {},
            "recommendations": []
        }
        
        if not UNIFIED_MEMORY_AVAILABLE:
            health_report["error"] = "Unified memory system not available for analysis"
            return health_report
        
        try:
            # Analyze unified memory system
            unified_memory = get_unified_memory()
            health_scores = []
            
            # 1. Tripartite Memory Analysis
            tripartite_health = self._analyze_tripartite_memory(unified_memory)
            health_report["tripartite_memory_health"] = tripartite_health
            health_scores.append(tripartite_health.get("health_score", 0.5))
            
            # 2. Memory System Integration Analysis
            if MEMORY_SYSTEMS_AVAILABLE:
                episodic_health = self._analyze_episodic_memory_health(data_dir)
                experience_health = self._analyze_experience_memory_health(data_dir)
                health_report["episodic_memory_health"] = episodic_health
                health_report["experience_memory_health"] = experience_health
                health_scores.extend([
                    episodic_health.get("health_score", 0.5),
                    experience_health.get("health_score", 0.5)
                ])
            
            # 3. Memory Performance Analysis
            fragmentation_analysis = self._analyze_memory_fragmentation(unified_memory)
            retrieval_analysis = self._analyze_retrieval_performance(unified_memory)
            storage_analysis = self._analyze_storage_efficiency(unified_memory)
            
            health_report["memory_fragmentation"] = fragmentation_analysis
            health_report["retrieval_performance"] = retrieval_analysis
            health_report["storage_efficiency"] = storage_analysis
            
            health_scores.extend([
                fragmentation_analysis.get("health_score", 0.5),
                retrieval_analysis.get("health_score", 0.5),
                storage_analysis.get("health_score", 0.5)
            ])
            
            # 4. Integration Quality Assessment
            integration_analysis = self._analyze_memory_integration_quality(data_dir)
            health_report["integration_quality"] = integration_analysis
            health_scores.append(integration_analysis.get("health_score", 0.5))
            
            # Calculate overall health score
            health_report["overall_health_score"] = sum(health_scores) / len(health_scores) if health_scores else 0.5
            
            # Generate recommendations
            health_report["recommendations"] = self._generate_memory_health_recommendations(health_report)
            
        except Exception as e:
            health_report["error"] = f"Memory health analysis failed: {str(e)}"
            health_report["overall_health_score"] = 0.0
        
        return health_report
    
    def _analyze_tripartite_memory(self, unified_memory) -> Dict[str, Any]:
        """Analyze tripartite memory (logic, symbolic, bridge) health"""
        analysis = {
            "health_score": 0.0,
            "logic_memory_size": 0,
            "symbolic_memory_size": 0,
            "bridge_memory_size": 0,
            "balance_score": 0.0,
            "issues": []
        }
        
        try:
            # Access tripartite memory if available
            if hasattr(unified_memory, 'tripartite_memory'):
                tm = unified_memory.tripartite_memory
                analysis["logic_memory_size"] = len(getattr(tm, 'logic_memory', []))
                analysis["symbolic_memory_size"] = len(getattr(tm, 'symbolic_memory', []))
                analysis["bridge_memory_size"] = len(getattr(tm, 'bridge_memory', []))
                
                # Calculate balance score
                total_memories = analysis["logic_memory_size"] + analysis["symbolic_memory_size"] + analysis["bridge_memory_size"]
                if total_memories > 0:
                    logic_ratio = analysis["logic_memory_size"] / total_memories
                    symbolic_ratio = analysis["symbolic_memory_size"] / total_memories
                    bridge_ratio = analysis["bridge_memory_size"] / total_memories
                    
                    # Ideal balance is roughly equal distribution
                    ideal_ratio = 1.0 / 3.0
                    balance_deviation = (abs(logic_ratio - ideal_ratio) + 
                                       abs(symbolic_ratio - ideal_ratio) + 
                                       abs(bridge_ratio - ideal_ratio)) / 3.0
                    analysis["balance_score"] = max(0.0, 1.0 - balance_deviation * 3.0)
                else:
                    analysis["balance_score"] = 0.0
                    analysis["issues"].append("No memories found in tripartite system")
                
                # Health score based on balance and presence of memories
                if total_memories == 0:
                    analysis["health_score"] = 0.0
                elif total_memories < 10:
                    analysis["health_score"] = 0.3
                else:
                    analysis["health_score"] = 0.3 + (analysis["balance_score"] * 0.7)
            else:
                analysis["issues"].append("Tripartite memory not accessible")
                analysis["health_score"] = 0.2
                
        except Exception as e:
            analysis["issues"].append(f"Tripartite analysis failed: {str(e)}")
            analysis["health_score"] = 0.1
        
        return analysis
    
    def _analyze_episodic_memory_health(self, data_dir: str) -> Dict[str, Any]:
        """Analyze episodic memory system health"""
        analysis = {
            "health_score": 0.0,
            "total_memories": 0,
            "memory_diversity": 0.0,
            "temporal_distribution": {},
            "issues": []
        }
        
        try:
            episodic_system = EpisodicMemorySystem(data_dir)
            memories = episodic_system.episodic_memories
            
            analysis["total_memories"] = len(memories)
            
            if memories:
                # Analyze memory diversity (different experience types)
                experience_types = [mem.experience_type for mem in memories.values()]
                unique_types = len(set(experience_types))
                analysis["memory_diversity"] = min(1.0, unique_types / 5.0)  # Up to 5 different types is ideal
                
                # Temporal distribution analysis
                now = datetime.now(timezone.utc)
                time_buckets = {"recent_24h": 0, "recent_week": 0, "recent_month": 0, "older": 0}
                
                for memory in memories.values():
                    try:
                        mem_time = datetime.fromisoformat(memory.timestamp.replace('Z', '+00:00'))
                        age_hours = (now - mem_time).total_seconds() / 3600
                        
                        if age_hours <= 24:
                            time_buckets["recent_24h"] += 1
                        elif age_hours <= 168:  # 1 week
                            time_buckets["recent_week"] += 1
                        elif age_hours <= 720:  # 1 month
                            time_buckets["recent_month"] += 1
                        else:
                            time_buckets["older"] += 1
                    except:
                        time_buckets["older"] += 1
                
                analysis["temporal_distribution"] = time_buckets
                
                # Health score calculation
                if analysis["total_memories"] == 0:
                    analysis["health_score"] = 0.0
                elif analysis["total_memories"] < 5:
                    analysis["health_score"] = 0.3
                else:
                    diversity_factor = analysis["memory_diversity"]
                    recency_factor = min(1.0, time_buckets["recent_week"] / max(1, analysis["total_memories"]))
                    analysis["health_score"] = 0.4 + (diversity_factor * 0.3) + (recency_factor * 0.3)
            else:
                analysis["issues"].append("No episodic memories found")
                analysis["health_score"] = 0.0
                
        except Exception as e:
            analysis["issues"].append(f"Episodic memory analysis failed: {str(e)}")
            analysis["health_score"] = 0.1
        
        return analysis
    
    def _analyze_experience_memory_health(self, data_dir: str) -> Dict[str, Any]:
        """Analyze experience memory system health"""
        analysis = {
            "health_score": 0.0,
            "learning_experiences": 0,
            "insight_generation_rate": 0.0,
            "knowledge_progression": 0.0,
            "issues": []
        }
        
        try:
            experience_memory = ExperienceMemory(data_dir)
            experiences = getattr(experience_memory, 'learning_experiences', {})
            
            analysis["learning_experiences"] = len(experiences)
            
            if experiences:
                # Analyze insight generation
                total_insights = sum(len(exp.insights_generated) for exp in experiences.values())
                analysis["insight_generation_rate"] = total_insights / len(experiences) if experiences else 0.0
                
                # Knowledge progression analysis
                understanding_changes = []
                for exp in experiences.values():
                    if hasattr(exp, 'understanding_change') and exp.understanding_change:
                        understanding_changes.extend(exp.understanding_change.values())
                
                if understanding_changes:
                    avg_understanding_change = sum(understanding_changes) / len(understanding_changes)
                    analysis["knowledge_progression"] = max(0.0, min(1.0, avg_understanding_change + 0.5))
                
                # Health score calculation
                insight_factor = min(1.0, analysis["insight_generation_rate"] / 2.0)  # 2 insights per experience is good
                progression_factor = analysis["knowledge_progression"]
                volume_factor = min(1.0, len(experiences) / 20.0)  # 20 experiences is a good base
                
                analysis["health_score"] = (insight_factor * 0.4) + (progression_factor * 0.4) + (volume_factor * 0.2)
            else:
                analysis["issues"].append("No learning experiences found")
                analysis["health_score"] = 0.0
                
        except Exception as e:
            analysis["issues"].append(f"Experience memory analysis failed: {str(e)}")
            analysis["health_score"] = 0.1
        
        return analysis
    
    def _analyze_memory_fragmentation(self, unified_memory) -> Dict[str, Any]:
        """Analyze memory fragmentation and efficiency"""
        analysis = {
            "health_score": 0.8,  # Default to good if we can't measure
            "fragmentation_level": "unknown",
            "consolidation_needed": False,
            "issues": []
        }
        
        try:
            # Check vector memory fragmentation if available
            if hasattr(unified_memory, 'vector_data'):
                vector_data = unified_memory.vector_data
                if vector_data:
                    # Simple fragmentation heuristic: check for gaps in IDs or timestamps
                    ids = [item.get('id', '') for item in vector_data if item.get('id')]
                    if len(set(ids)) < len(ids):
                        analysis["fragmentation_level"] = "high"
                        analysis["consolidation_needed"] = True
                        analysis["health_score"] = 0.4
                        analysis["issues"].append("Duplicate vector IDs detected")
                    else:
                        analysis["fragmentation_level"] = "low"
                        analysis["health_score"] = 0.9
            
        except Exception as e:
            analysis["issues"].append(f"Fragmentation analysis failed: {str(e)}")
            analysis["health_score"] = 0.5
        
        return analysis
    
    def _analyze_retrieval_performance(self, unified_memory) -> Dict[str, Any]:
        """Analyze memory retrieval performance"""
        analysis = {
            "health_score": 0.7,  # Default assumption
            "avg_retrieval_time": "unknown",
            "cache_hit_rate": "unknown",
            "issues": []
        }
        
        # Note: This would need actual performance metrics from unified_memory
        # For now, provide a basic assessment
        try:
            if hasattr(unified_memory, 'vector_data'):
                vector_count = len(getattr(unified_memory, 'vector_data', []))
                if vector_count > 1000:
                    analysis["health_score"] = 0.6
                    analysis["issues"].append("Large vector database may impact retrieval speed")
                elif vector_count < 10:
                    analysis["health_score"] = 0.8
                    analysis["issues"].append("Small vector database - good retrieval speed expected")
                else:
                    analysis["health_score"] = 0.8
            
        except Exception as e:
            analysis["issues"].append(f"Retrieval performance analysis failed: {str(e)}")
            analysis["health_score"] = 0.5
        
        return analysis
    
    def _analyze_storage_efficiency(self, unified_memory) -> Dict[str, Any]:
        """Analyze memory storage efficiency"""
        analysis = {
            "health_score": 0.7,
            "storage_utilization": "unknown",
            "redundancy_level": "unknown",
            "compression_potential": "unknown",
            "issues": []
        }
        
        try:
            # Basic storage analysis
            total_size = 0
            if hasattr(unified_memory, 'vector_data'):
                vector_data = unified_memory.vector_data
                total_size += len(str(vector_data))
            
            if hasattr(unified_memory, 'tripartite_memory'):
                tm = unified_memory.tripartite_memory
                total_size += len(str(getattr(tm, 'logic_memory', [])))
                total_size += len(str(getattr(tm, 'symbolic_memory', [])))
                total_size += len(str(getattr(tm, 'bridge_memory', [])))
            
            # Simple efficiency heuristic
            if total_size > 1000000:  # > 1MB
                analysis["storage_utilization"] = "high"
                analysis["health_score"] = 0.6
                analysis["issues"].append("High memory utilization - consider archiving old data")
            elif total_size < 1000:  # < 1KB
                analysis["storage_utilization"] = "very_low"
                analysis["health_score"] = 0.9
            else:
                analysis["storage_utilization"] = "moderate"
                analysis["health_score"] = 0.8
            
        except Exception as e:
            analysis["issues"].append(f"Storage efficiency analysis failed: {str(e)}")
            analysis["health_score"] = 0.5
        
        return analysis
    
    def _analyze_memory_integration_quality(self, data_dir: str) -> Dict[str, Any]:
        """Analyze quality of integration between memory systems"""
        analysis = {
            "health_score": 0.0,
            "cross_references": 0,
            "integration_patterns": [],
            "consistency_score": 0.0,
            "issues": []
        }
        
        try:
            # Check for cross-references between memory systems
            integration_indicators = 0
            total_checks = 0
            
            # Check if episodic memories reference experience memories
            if MEMORY_SYSTEMS_AVAILABLE:
                episodic_system = EpisodicMemorySystem(data_dir)
                experience_system = ExperienceMemory(data_dir)
                
                episodic_memories = episodic_system.episodic_memories
                experience_memories = getattr(experience_system, 'learning_experiences', {})
                
                # Look for conceptual overlap
                if episodic_memories and experience_memories:
                    episodic_concepts = set()
                    for mem in episodic_memories.values():
                        episodic_concepts.update(getattr(mem, 'key_concepts', []))
                    
                    exp_concepts = set()
                    for exp in experience_memories.values():
                        if hasattr(exp, 'understanding_change'):
                            exp_concepts.update(exp.understanding_change.keys())
                    
                    overlap = len(episodic_concepts.intersection(exp_concepts))
                    total_concepts = len(episodic_concepts.union(exp_concepts))
                    
                    if total_concepts > 0:
                        consistency = overlap / total_concepts
                        analysis["consistency_score"] = consistency
                        analysis["cross_references"] = overlap
                        integration_indicators += 1
                        
                        if consistency > 0.3:
                            analysis["integration_patterns"].append("Good conceptual consistency between episodic and experience memories")
                        else:
                            analysis["issues"].append("Low conceptual overlap between memory systems")
                    
                    total_checks += 1
            
            # Calculate overall integration health
            if total_checks > 0:
                base_score = integration_indicators / total_checks
                consistency_bonus = analysis["consistency_score"] * 0.5
                analysis["health_score"] = min(1.0, base_score + consistency_bonus)
            else:
                analysis["health_score"] = 0.5  # Neutral when we can't assess
                analysis["issues"].append("Unable to assess memory integration - systems not available")
        
        except Exception as e:
            analysis["issues"].append(f"Integration analysis failed: {str(e)}")
            analysis["health_score"] = 0.3
        
        return analysis
    
    def _generate_memory_health_recommendations(self, health_report: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on memory health analysis"""
        recommendations = []
        overall_score = health_report.get("overall_health_score", 0.5)
        
        # Overall health recommendations
        if overall_score < 0.4:
            recommendations.append("CRITICAL: Memory system health is poor - immediate attention required")
        elif overall_score < 0.6:
            recommendations.append("Memory system health needs improvement - schedule maintenance")
        elif overall_score > 0.8:
            recommendations.append("Memory system health is excellent - maintain current practices")
        
        # Specific system recommendations
        tripartite_health = health_report.get("tripartite_memory_health", {})
        if tripartite_health.get("balance_score", 0.5) < 0.5:
            recommendations.append("Improve tripartite memory balance - encourage more diverse memory types")
        
        episodic_health = health_report.get("episodic_memory_health", {})
        if episodic_health.get("memory_diversity", 0.5) < 0.4:
            recommendations.append("Increase episodic memory diversity - engage in varied experiences")
        
        experience_health = health_report.get("experience_memory_health", {})
        if experience_health.get("insight_generation_rate", 0.0) < 1.0:
            recommendations.append("Enhance insight generation - focus on reflection and synthesis")
        
        fragmentation = health_report.get("memory_fragmentation", {})
        if fragmentation.get("consolidation_needed", False):
            recommendations.append("Perform memory consolidation - remove duplicates and optimize storage")
        
        storage = health_report.get("storage_efficiency", {})
        if storage.get("storage_utilization") == "high":
            recommendations.append("Archive old memories - free up storage space for new experiences")
        
        integration = health_report.get("integration_quality", {})
        if integration.get("consistency_score", 0.5) < 0.3:
            recommendations.append("Improve memory integration - strengthen cross-references between systems")
        
        return recommendations
    
    def get_memory_health_summary(self, data_dir: str = "data") -> str:
        """Get a human-readable summary of memory system health"""
        health_report = self.analyze_unified_memory_health(data_dir)
        overall_score = health_report.get("overall_health_score", 0.0)
        
        if overall_score > 0.8:
            status = "excellent"
            emoji = "🟢"
        elif overall_score > 0.6:
            status = "good"
            emoji = "🟡"
        elif overall_score > 0.4:
            status = "fair"
            emoji = "🟠"
        else:
            status = "needs attention"
            emoji = "🔴"
        
        summary_parts = [
            f"{emoji} Memory system health is {status} ({overall_score:.1%})"
        ]
        
        # Add key insights
        recommendations = health_report.get("recommendations", [])
        if recommendations:
            summary_parts.append(f"Key recommendations: {recommendations[0]}")
        
        # Add system-specific insights
        tripartite = health_report.get("tripartite_memory_health", {})
        if tripartite.get("health_score", 0) > 0:
            total_memories = sum([
                tripartite.get("logic_memory_size", 0),
                tripartite.get("symbolic_memory_size", 0),
                tripartite.get("bridge_memory_size", 0)
            ])
            summary_parts.append(f"Tripartite memory: {total_memories} memories with {tripartite.get('balance_score', 0):.1%} balance")
        
        episodic = health_report.get("episodic_memory_health", {})
        if episodic.get("health_score", 0) > 0:
            summary_parts.append(f"Episodic memory: {episodic.get('total_memories', 0)} memories with {episodic.get('memory_diversity', 0):.1%} diversity")
        
        return ". ".join(summary_parts) + "."


# Standalone utility functions
def display_metrics_summary():
    """Quick summary of current metrics"""
    metrics = BrainMetrics()
    history = metrics._read_json(metrics.metrics_file)
    
    if not history:
        print("📊 No metrics history found.")
        return
        
    latest = history[-1]
    print("\n📊 Latest Session Summary:")
    print(f"  Time: {latest['timestamp']}")
    print(f"  Total Decisions: {latest['total_decisions']}")
    print(f"  Logic Win Rate: {latest['logic_win_rate']:.1%}")
    print(f"  Symbol Win Rate: {latest['symbol_win_rate']:.1%}")
    print(f"  Hybrid Rate: {latest['hybrid_rate']:.1%}")
    print(f"  Conflicts: {latest.get('conflicts_count', 0)}")
    
    # Overall trends
    if len(history) > 1:
        logic_trend = latest['logic_win_rate'] - history[-2]['logic_win_rate']
        symbol_trend = latest['symbol_win_rate'] - history[-2]['symbol_win_rate']
        print(f"\n📈 Trends vs Previous Session:")
        print(f"  Logic: {'+' if logic_trend >= 0 else ''}{logic_trend:.1%}")
        print(f"  Symbol: {'+' if symbol_trend >= 0 else ''}{symbol_trend:.1%}")


if __name__ == "__main__":
    # Test the module
    print("🧠 Brain Metrics Module")
    print("=" * 50)
    
    # Create instance
    metrics = BrainMetrics()
    
    # Display current summary
    display_metrics_summary()
    
    # Analyze conflicts
    metrics.analyze_conflicts()
    
    # Check for adaptive weights
    weights = metrics.get_adaptive_weights()
    if weights:
        print(f"\n🎯 Recommended Adaptive Weights ({weights['confidence']} confidence):")
        print(f"  Static (Logic): {weights['link_score_weight_static']:.1%}")
        print(f"  Dynamic (Symbol): {weights['link_score_weight_dynamic']:.1%}")
    
    # Generate visual report
    try:
        metrics.generate_report()
    except Exception as e:
        print(f"⚠️ Could not generate visual report: {e}")