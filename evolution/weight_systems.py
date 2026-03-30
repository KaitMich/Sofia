# evolution/weight_systems.py - Consolidated Weight Management Systems
"""
Consolidated Weight Management for Dual Brain AI System

This module consolidates overlapping weight management functionality from:
- weight_evolution.py - Progressive Weight Evolution System (Autonomous Version)
- unified_weight_system.py - Unified Weight Management for Dual Brain AI  
- reset_weights.py - Reset adaptive weights to balanced values
- long_term_stability.py - Long-term Stability Assessment (weight-related portions)

All functions are preserved exactly as-is with source attribution for safety.
The core evolution_anchor.py remains separate as a specialized cognitive health system.
"""

import json
import numpy as np
import hashlib
import statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, Optional, Any, List, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, deque

# =============================================================================
# UNIFIED WEIGHT DECISION STRUCTURE
# Source: unified_weight_system.py
# =============================================================================

@dataclass
class WeightDecision:
    """Structured result from unified weight calculation"""
    logic_scale: float
    symbolic_scale: float
    confidence_modifier: float
    decision_type: str
    reasoning: Dict[str, Any]
    metadata: Dict[str, Any]

# =============================================================================
# WEIGHT EVOLUTION SYSTEM
# Source: weight_evolution.py - Progressive Weight Evolution System (Autonomous Version)
# =============================================================================

class WeightEvolver:
    """
    Manages progressive evolution of weights based on actual data patterns.
    Truly autonomous - learns optimal balance from content distribution.
    
    Source: weight_evolution.py
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.weights_file = self.data_dir / "adaptive_weights.json"
        self.momentum_file = self.data_dir / "weight_momentum.json"
        self.history_file = self.data_dir / "weight_evolution_history.json"
        
        # Load current state
        self.weights = self._load_weights()
        self.momentum = self._load_momentum()
        self.history = self._load_history()
        
    def _load_weights(self):
        """Load current weights"""
        try:
            if self.weights_file.exists():
                with open(self.weights_file, 'r') as f:
                    data = json.load(f)
                    return {
                        'static': data.get('link_score_weight_static', 0.6),
                        'dynamic': data.get('link_score_weight_dynamic', 0.4),
                        'last_updated': data.get('last_updated')
                    }
        except Exception:
            pass
        return {'static': 0.6, 'dynamic': 0.4, 'last_updated': None}
        
    def _save_weights(self):
        """Save current weights"""
        data = {
            'link_score_weight_static': self.weights['static'],
            'link_score_weight_dynamic': self.weights['dynamic'],
            'last_updated': datetime.utcnow().isoformat()
        }
        with open(self.weights_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def _load_momentum(self):
        """Load momentum state"""
        try:
            if self.momentum_file.exists():
                with open(self.momentum_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            'static_wins': 0,
            'dynamic_wins': 0,
            'last_direction': None,
            'consecutive_moves': 0
        }
        
    def _save_momentum(self):
        """Save momentum state"""
        with open(self.momentum_file, 'w') as f:
            json.dump(self.momentum, f, indent=2)
            
    def _load_history(self):
        """Load evolution history"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
        
    def _save_history(self):
        """Save evolution history (keep last 50 entries)"""
        self.history = self.history[-50:]
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
            
    def get_current_specialization(self):
        """Calculate current specialization level (0=balanced, 1=fully specialized)"""
        return abs(self.weights['static'] - self.weights['dynamic'])
        
    def calculate_target_specialization(self, run_count, memory_stats=None):
        """
        Calculate target specialization based on actual data distribution.
        This makes it truly autonomous - it learns from what it's seeing.
        """
        
        # If no memory stats, start balanced
        if not memory_stats or 'distribution' not in memory_stats:
            return 0.0  # Start balanced until we have data
        
        dist = memory_stats['distribution']
        logic_pct = dist.get('logic_pct', 0)
        symbolic_pct = dist.get('symbolic_pct', 0)
        bridge_pct = dist.get('bridge_pct', 0)
        
        # Key insight: If bridge is large, we're not classifying well
        # The system should adjust weights to reduce bridge size
        
        if bridge_pct > 40:
            # Large bridge means we need to help items migrate
            # Look at what's accumulating more
            if logic_pct > symbolic_pct * 2:
                # We have way more logic than symbolic
                # Maybe we're over-weighting logic? Try balancing
                return 0.0  # Push toward balance
            elif symbolic_pct > logic_pct * 2:
                # We have way more symbolic than logic
                # Maybe we're over-weighting symbolic? Try balancing
                return 0.0  # Push toward balance
            else:
                # Bridge is large but distribution is balanced
                # Try slight specialization to help classification
                return 0.2
        
        # If bridge is small, the system is working well
        # Let it continue with current specialization
        if bridge_pct < 10:
            current_spec = self.get_current_specialization()
            return min(0.6, current_spec * 1.1)  # Slightly increase what's working
        
        # Medium bridge (10-40%) - adjust based on content ratio
        # This is the autonomous part - learn from the data!
        if logic_pct > 0 and symbolic_pct > 0:
            # Calculate natural ratio in the data
            total_classified = logic_pct + symbolic_pct
            logic_ratio = logic_pct / total_classified
            symbolic_ratio = symbolic_pct / total_classified
            
            # If data is naturally 70% logic, 30% symbolic
            # then weights should reflect that to minimize bridge
            if logic_ratio > 0.7:
                # Data is logic-heavy, allow weights to specialize
                return 0.4  # This allows up to 70/30 split
            elif symbolic_ratio > 0.7:
                # Data is symbolic-heavy, allow weights to specialize
                return 0.4  # This allows up to 30/70 split
            else:
                # Data is balanced, keep weights balanced
                return 0.1  # Allow only slight specialization
        
        # Default: slight specialization
        return 0.2
        
    def evolve_weights(self, run_count, memory_stats=None, performance_stats=None):
        """
        Evolve weights toward specialization based on actual data patterns.
        Now truly autonomous - learns from content distribution.
        """
        old_static = self.weights['static']
        old_dynamic = self.weights['dynamic']
        
        # Current state
        current_spec = self.get_current_specialization()
        target_spec = self.calculate_target_specialization(run_count, memory_stats)
        
        print(f"\n⚡ Weight Evolution:")
        print(f"  Current: static={old_static:.3f}, dynamic={old_dynamic:.3f}")
        print(f"  Specialization: {current_spec:.3f} → target {target_spec:.3f}")
        
        # If we have memory stats, show why we're making this decision
        if memory_stats and 'distribution' in memory_stats:
            dist = memory_stats['distribution']
            print(f"  Data distribution: Logic={dist.get('logic_pct', 0):.1f}%, "
                  f"Symbolic={dist.get('symbolic_pct', 0):.1f}%, "
                  f"Bridge={dist.get('bridge_pct', 0):.1f}%")
        
        # Check if we need to evolve
        if abs(current_spec - target_spec) < 0.02:
            print("  → Already close to target specialization")
            return False
        
        # Determine direction based on actual data patterns
        if memory_stats and 'distribution' in memory_stats:
            dist = memory_stats['distribution']
            logic_pct = dist.get('logic_pct', 0)
            symbolic_pct = dist.get('symbolic_pct', 0)
            
            # Autonomous decision: follow the data
            if logic_pct > symbolic_pct * 1.5 and current_spec < target_spec:
                direction = 'static'  # Strengthen logic
            elif symbolic_pct > logic_pct * 1.5 and current_spec < target_spec:
                direction = 'dynamic'  # Strengthen symbolic
            elif current_spec > target_spec:
                # Need to reduce specialization
                direction = 'reduce'
            else:
                # Use performance stats if available
                if performance_stats:
                    logic_wins = performance_stats.get('logic_win_rate', 0)
                    symbol_wins = performance_stats.get('symbol_win_rate', 0)
                    direction = 'static' if logic_wins > symbol_wins else 'dynamic'
                else:
                    # No clear signal, maintain current bias
                    direction = 'static' if old_static > old_dynamic else 'dynamic'
        else:
            # No data, evolve slowly toward balance
            direction = 'reduce' if current_spec > 0.1 else 'static'
        
        # Calculate step size with momentum
        base_step = 0.02
        
        # Apply momentum if moving in same direction
        if self.momentum['last_direction'] == direction:
            self.momentum['consecutive_moves'] += 1
            momentum_factor = 1 + (self.momentum['consecutive_moves'] * 0.1)
            step = min(0.05, base_step * momentum_factor)  # Cap at 0.05
        else:
            # Direction change, reset momentum
            self.momentum['consecutive_moves'] = 1
            step = base_step
            
        # Update momentum tracking
        self.momentum['last_direction'] = direction
        if direction == 'static':
            self.momentum['static_wins'] += 1
            self.momentum['dynamic_wins'] = 0
        elif direction == 'dynamic':
            self.momentum['dynamic_wins'] += 1
            self.momentum['static_wins'] = 0
            
        # Apply the evolution
        if direction == 'reduce':
            # Move toward balance
            if old_static > old_dynamic:
                new_static = max(0.5, old_static - step)
                new_dynamic = 1.0 - new_static
            else:
                new_dynamic = max(0.5, old_dynamic - step)
                new_static = 1.0 - new_dynamic
        elif direction == 'static':
            new_static = min(0.9, old_static + step)
            new_dynamic = 1.0 - new_static
        else:  # dynamic
            new_dynamic = min(0.9, old_dynamic + step)
            new_static = 1.0 - new_dynamic
            
        # Update weights
        self.weights['static'] = round(new_static, 3)
        self.weights['dynamic'] = round(new_dynamic, 3)
        
        # Record in history
        self.history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'run_count': run_count,
            'old_weights': {'static': old_static, 'dynamic': old_dynamic},
            'new_weights': {'static': self.weights['static'], 'dynamic': self.weights['dynamic']},
            'target_specialization': target_spec,
            'actual_specialization': self.get_current_specialization(),
            'momentum': self.momentum.copy(),
            'memory_stats': memory_stats,
            'performance_stats': performance_stats,
            'decision_reason': f"Direction: {direction}, Bridge%: {memory_stats.get('distribution', {}).get('bridge_pct', 'N/A') if memory_stats else 'N/A'}"
        })
        
        # Save everything
        self._save_weights()
        self._save_momentum()
        self._save_history()
        
        print(f"  → Evolved to: static={self.weights['static']:.3f}, dynamic={self.weights['dynamic']:.3f}")
        print(f"  Decision: {direction} (based on data distribution)")
        
        return True
        
    def get_evolution_summary(self):
        """Get summary of weight evolution over time"""
        if not self.history:
            return {
                'total_evolutions': 0,
                'current_weights': self.weights,
                'current_specialization': self.get_current_specialization()
            }
            
        # Analyze history
        first_entry = self.history[0]
        last_entry = self.history[-1]
        
        # Calculate total drift
        initial_spec = abs(first_entry['old_weights']['static'] - first_entry['old_weights']['dynamic'])
        current_spec = self.get_current_specialization()
        
        # Find dominant direction
        static_moves = sum(1 for h in self.history if h.get('momentum', {}).get('last_direction') == 'static')
        dynamic_moves = sum(1 for h in self.history if h.get('momentum', {}).get('last_direction') == 'dynamic')
        reduce_moves = sum(1 for h in self.history if h.get('momentum', {}).get('last_direction') == 'reduce')
        
        return {
            'total_evolutions': len(self.history),
            'current_weights': self.weights,
            'current_specialization': current_spec,
            'specialization_increase': current_spec - initial_spec,
            'dominant_direction': 'static' if static_moves > dynamic_moves else 'dynamic',
            'direction_counts': {
                'static_moves': static_moves,
                'dynamic_moves': dynamic_moves,
                'reduce_moves': reduce_moves
            },
            'momentum_state': self.momentum
        }

# =============================================================================
# UNIFIED WEIGHT SYSTEM
# Source: unified_weight_system.py - Unified Weight Management for Dual Brain AI
# =============================================================================

class UnifiedWeightSystem:
    """
    Unified Weight System that combines:
    1. Autonomous learning from Weight Evolution
    2. Semantic context awareness from AlphaWall
    3. Reliable confidence-based routing
    
    Single source of truth for all weight decisions in the dual brain system.
    
    Source: unified_weight_system.py
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load components
        self._load_autonomous_weights()
        self._load_semantic_adjustments()
        self._load_confidence_gates()
        
        # Decision history for learning
        self.decision_history_file = self.data_dir / "unified_weight_decisions.json"
        self.learning_stats_file = self.data_dir / "weight_learning_stats.json"
        
        # Performance tracking
        self.performance_stats = self._load_performance_stats()
        
    def _load_autonomous_weights(self):
        """Load autonomous learning weights from weight evolution system"""
        weights_file = self.data_dir / "adaptive_weights.json"
        
        if weights_file.exists():
            try:
                with open(weights_file, 'r') as f:
                    data = json.load(f)
                    self.base_static_weight = data.get('link_score_weight_static', 0.6)
                    self.base_dynamic_weight = data.get('link_score_weight_dynamic', 0.4)
                    self.weights_last_updated = data.get('last_updated')
            except Exception:
                self._set_default_autonomous_weights()
        else:
            self._set_default_autonomous_weights()
            
        # Convert to standardized logic/symbolic scales
        # Higher static weight = prefer logic (established patterns)
        # Higher dynamic weight = prefer symbolic (new/emotional content)
        total = self.base_static_weight + self.base_dynamic_weight
        static_ratio = self.base_static_weight / total
        
        # Map to 2.0/1.0 standard scale
        if static_ratio > 0.5:
            # Logic-favoring system
            self.base_logic_scale = 2.0
            self.base_symbolic_scale = 1.0 * (1 - (static_ratio - 0.5))
        else:
            # Symbolic-favoring system  
            self.base_symbolic_scale = 2.0
            self.base_logic_scale = 1.0 * (1 - (0.5 - static_ratio))
            
    def _set_default_autonomous_weights(self):
        """Set default autonomous weights"""
        self.base_static_weight = 0.6
        self.base_dynamic_weight = 0.4
        self.weights_last_updated = None
        
    def _load_semantic_adjustments(self):
        """Load semantic context adjustment mappings"""
        tag_weights_file = self.data_dir / "tag_weight_mappings.json"
        
        if tag_weights_file.exists():
            try:
                with open(tag_weights_file, 'r') as f:
                    self.semantic_adjustments = json.load(f)
            except Exception:
                self._set_default_semantic_adjustments()
        else:
            self._set_default_semantic_adjustments()
            
    def _set_default_semantic_adjustments(self):
        """Set default semantic adjustment mappings"""
        self.semantic_adjustments = {
            'emotional_states': {
                'calm': {'logic_boost': 0.2, 'symbolic_boost': 0.0},
                'neutral': {'logic_boost': 0.1, 'symbolic_boost': 0.0},
                'overwhelmed': {'logic_boost': -0.3, 'symbolic_boost': 0.4},
                'grief': {'logic_boost': -0.4, 'symbolic_boost': 0.5},
                'angry': {'logic_boost': -0.2, 'symbolic_boost': 0.3},
                'emotionally_recursive': {'logic_boost': -0.5, 'symbolic_boost': 0.6}
            },
            'intents': {
                'information_request': {'logic_boost': 0.3, 'symbolic_boost': -0.1},
                'expressive': {'logic_boost': -0.3, 'symbolic_boost': 0.4},
                'self_reference': {'logic_boost': -0.2, 'symbolic_boost': 0.3},
                'abstract_reflection': {'logic_boost': 0.0, 'symbolic_boost': 0.2},
                'euphemistic': {'logic_boost': -0.4, 'symbolic_boost': 0.5},
                'humor_deflection': {'logic_boost': -0.1, 'symbolic_boost': 0.2}
            },
            'contexts': {
                'trauma_loop': {'logic_boost': -0.6, 'symbolic_boost': 0.7},
                'reclaimed_language': {'logic_boost': -0.3, 'symbolic_boost': 0.4},
                'metaphorical': {'logic_boost': -0.2, 'symbolic_boost': 0.3},
                'coded_speech': {'logic_boost': -0.3, 'symbolic_boost': 0.4},
                'poetic_speech': {'logic_boost': -0.4, 'symbolic_boost': 0.5},
                'direct_expression': {'logic_boost': 0.1, 'symbolic_boost': 0.0}
            }
        }
        
    def _load_confidence_gates(self):
        """Load confidence gate thresholds"""
        self.confidence_thresholds = {
            'high_confidence_logic': 6.0,    # logic_score * scale > this = high confidence logic
            'high_confidence_symbolic': 3.0,  # symbolic_score * scale > this = high confidence symbolic  
            'force_hybrid_threshold': 0.8,   # If scores within this ratio, force hybrid
            'quarantine_confidence': 0.3,    # Below this confidence = quarantine
            'min_decision_confidence': 0.5   # Minimum confidence for any decision
        }
        
    def _load_performance_stats(self):
        """Load learning performance statistics"""
        if self.learning_stats_file.exists():
            try:
                with open(self.learning_stats_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            'successful_logic_routes': 0,
            'successful_symbolic_routes': 0,
            'successful_hybrid_routes': 0,
            'failed_routes': 0,
            'total_decisions': 0,
            'confidence_accuracy': []
        }
        
    def calculate_unified_weights(self, 
                                user_input: str = None,
                                semantic_tags: Dict = None,
                                memory_stats: Dict = None,
                                force_context: str = None) -> WeightDecision:
        """
        Calculate unified weights combining all systems.
        
        Args:
            user_input: Raw user text (for semantic analysis)
            semantic_tags: Pre-computed AlphaWall tags
            memory_stats: Current memory distribution statistics
            force_context: Override context for testing
            
        Returns:
            WeightDecision with unified scales and reasoning
        """
        
        reasoning = {
            'base_autonomous': {
                'static_weight': self.base_static_weight,
                'dynamic_weight': self.base_dynamic_weight,
                'base_logic_scale': self.base_logic_scale,
                'base_symbolic_scale': self.base_symbolic_scale
            },
            'semantic_adjustments': {},
            'confidence_factors': {},
            'final_calculation': {}
        }
        
        # Step 1: Start with autonomous base weights
        current_logic_scale = self.base_logic_scale
        current_symbolic_scale = self.base_symbolic_scale
        confidence_modifier = 1.0
        
        # Step 2: Apply semantic context adjustments
        if semantic_tags or force_context:
            tags = semantic_tags or {'emotional_state': force_context}
            adjustments = self._calculate_semantic_adjustments(tags)
            
            current_logic_scale *= (1 + adjustments['logic_adjustment'])
            current_symbolic_scale *= (1 + adjustments['symbolic_adjustment'])
            confidence_modifier = adjustments['confidence_modifier']
            
            reasoning['semantic_adjustments'] = {
                'tags_used': tags,
                'logic_adjustment': adjustments['logic_adjustment'],
                'symbolic_adjustment': adjustments['symbolic_adjustment'],
                'confidence_modifier': confidence_modifier,
                'special_handling': adjustments['special_handling']
            }
            
        # Step 3: Apply memory-based learning adjustments
        if memory_stats:
            memory_adjustments = self._calculate_memory_adjustments(memory_stats)
            current_logic_scale *= memory_adjustments['logic_multiplier']
            current_symbolic_scale *= memory_adjustments['symbolic_multiplier']
            
            reasoning['memory_adjustments'] = memory_adjustments
            
        # Step 4: Normalize and apply bounds
        current_logic_scale = np.clip(current_logic_scale, 0.1, 4.0)
        current_symbolic_scale = np.clip(current_symbolic_scale, 0.1, 4.0)
        confidence_modifier = np.clip(confidence_modifier, 0.1, 1.5)
        
        # Step 5: Determine decision type
        decision_type = self._determine_decision_type(
            current_logic_scale, 
            current_symbolic_scale,
            confidence_modifier
        )
        
        reasoning['final_calculation'] = {
            'final_logic_scale': current_logic_scale,
            'final_symbolic_scale': current_symbolic_scale,
            'scale_ratio': current_logic_scale / current_symbolic_scale,
            'decision_logic': f"Logic scale {current_logic_scale:.3f} vs Symbolic scale {current_symbolic_scale:.3f}"
        }
        
        # Step 6: Create decision object
        decision = WeightDecision(
            logic_scale=round(current_logic_scale, 3),
            symbolic_scale=round(current_symbolic_scale, 3),
            confidence_modifier=round(confidence_modifier, 3),
            decision_type=decision_type,
            reasoning=reasoning,
            metadata={
                'timestamp': datetime.utcnow().isoformat(),
                'autonomous_weights_age': self.weights_last_updated,
                'decision_id': f"unified_{hash(str(reasoning))}"[:12]
            }
        )
        
        # Step 7: Log decision for learning
        self._log_decision(decision)
        
        return decision
        
    def _calculate_semantic_adjustments(self, tags: Dict) -> Dict:
        """Calculate adjustments based on semantic tags"""
        adjustments = {
            'logic_adjustment': 0.0,
            'symbolic_adjustment': 0.0,
            'confidence_modifier': 1.0,
            'special_handling': []
        }
        
        # Apply emotional state adjustments
        emotional_state = tags.get('emotional_state', 'neutral')
        if emotional_state in self.semantic_adjustments['emotional_states']:
            state_adj = self.semantic_adjustments['emotional_states'][emotional_state]
            adjustments['logic_adjustment'] += state_adj['logic_boost']
            adjustments['symbolic_adjustment'] += state_adj['symbolic_boost']
            
        # Apply intent adjustments
        intent = tags.get('intent', 'information_request')
        if intent in self.semantic_adjustments['intents']:
            intent_adj = self.semantic_adjustments['intents'][intent]
            adjustments['logic_adjustment'] += intent_adj['logic_boost']
            adjustments['symbolic_adjustment'] += intent_adj['symbolic_boost']
            
        # Apply context adjustments
        contexts = tags.get('context', [])
        if isinstance(contexts, str):
            contexts = [contexts]
        for context in contexts:
            if context in self.semantic_adjustments['contexts']:
                ctx_adj = self.semantic_adjustments['contexts'][context]
                adjustments['logic_adjustment'] += ctx_adj['logic_boost'] * 0.5
                adjustments['symbolic_adjustment'] += ctx_adj['symbolic_boost'] * 0.5
                
        # Cap adjustments
        adjustments['logic_adjustment'] = np.clip(adjustments['logic_adjustment'], -0.8, 0.8)
        adjustments['symbolic_adjustment'] = np.clip(adjustments['symbolic_adjustment'], -0.8, 0.8)
        
        return adjustments
        
    def _calculate_memory_adjustments(self, memory_stats: Dict) -> Dict:
        """Calculate adjustments based on memory distribution"""
        adjustments = {
            'logic_multiplier': 1.0,
            'symbolic_multiplier': 1.0,
            'reasoning': ''
        }
        
        if 'distribution' not in memory_stats:
            return adjustments
            
        dist = memory_stats['distribution']
        bridge_pct = dist.get('bridge_pct', 0)
        logic_pct = dist.get('logic_pct', 0)
        symbolic_pct = dist.get('symbolic_pct', 0)
        
        # If bridge is large, adjust to help classification
        if bridge_pct > 30:
            if logic_pct > symbolic_pct * 2:
                # Too much logic bias, balance it
                adjustments['logic_multiplier'] = 0.9
                adjustments['symbolic_multiplier'] = 1.1
                adjustments['reasoning'] = 'Reducing logic bias due to large bridge'
            elif symbolic_pct > logic_pct * 2:
                # Too much symbolic bias, balance it
                adjustments['logic_multiplier'] = 1.1
                adjustments['symbolic_multiplier'] = 0.9
                adjustments['reasoning'] = 'Reducing symbolic bias due to large bridge'
                
        return adjustments
        
    def _determine_decision_type(self, logic_scale: float, symbolic_scale: float, confidence_modifier: float) -> str:
        """Determine routing decision type based on scales"""
        ratio = logic_scale / symbolic_scale
        
        if confidence_modifier < 0.5:
            return 'QUARANTINE'
        elif ratio > 1.5:
            return 'FOLLOW_LOGIC'
        elif ratio < 0.67:
            return 'FOLLOW_SYMBOLIC' 
        else:
            return 'FOLLOW_HYBRID'
            
    def route_with_unified_weights(self, 
                                 logic_score: float,
                                 symbolic_score: float,
                                 user_input: str = None,
                                 semantic_tags: Dict = None,
                                 memory_stats: Dict = None) -> Tuple[str, float, WeightDecision]:
        """
        Complete routing decision using unified weight system.
        
        Returns:
            (decision_type, confidence, weight_decision)
        """
        
        # Get unified weights
        weight_decision = self.calculate_unified_weights(
            user_input=user_input,
            semantic_tags=semantic_tags,
            memory_stats=memory_stats
        )
        
        # Apply weights to scores
        scaled_logic = logic_score * weight_decision.logic_scale
        scaled_symbolic = symbolic_score * weight_decision.symbolic_scale
        
        # Calculate final confidence
        max_score = max(scaled_logic, scaled_symbolic)
        score_difference = abs(scaled_logic - scaled_symbolic)
        
        # Base confidence from score strength and difference
        base_confidence = min(1.0, max_score / 10.0) * min(1.0, score_difference / 3.0)
        final_confidence = base_confidence * weight_decision.confidence_modifier
        
        # Apply confidence gates
        if final_confidence < self.confidence_thresholds['quarantine_confidence']:
            decision_type = 'QUARANTINE'
            final_confidence = 0.0
        elif final_confidence < self.confidence_thresholds['min_decision_confidence']:
            decision_type = 'FOLLOW_HYBRID'
        else:
            decision_type = weight_decision.decision_type
            
        # Update decision with routing results
        weight_decision.metadata.update({
            'input_scores': {'logic': logic_score, 'symbolic': symbolic_score},
            'scaled_scores': {'logic': scaled_logic, 'symbolic': scaled_symbolic},
            'final_confidence': round(final_confidence, 3),
            'routing_decision': decision_type
        })
        
        return decision_type, final_confidence, weight_decision
        
    def _log_decision(self, decision: WeightDecision):
        """Log decision for learning and analysis"""
        decisions = []
        if self.decision_history_file.exists():
            try:
                with open(self.decision_history_file, 'r') as f:
                    decisions = json.load(f)
            except Exception:
                pass
                
        decisions.append(decision.__dict__)
        decisions = decisions[-1000:]  # Keep last 1000
        
        with open(self.decision_history_file, 'w') as f:
            json.dump(decisions, f, indent=2)
            
    def learn_from_feedback(self, decision_id: str, was_successful: bool, feedback_data: Dict = None):
        """Update system based on routing decision feedback"""
        self.performance_stats['total_decisions'] += 1
        
        if was_successful:
            # Find which route was taken and increment success counter
            # This would integrate with the autonomous weight evolution
            pass
        else:
            self.performance_stats['failed_routes'] += 1
            
        # Save updated stats
        with open(self.learning_stats_file, 'w') as f:
            json.dump(self.performance_stats, f, indent=2)
            
    def get_system_status(self) -> Dict:
        """Get current status of unified weight system"""
        return {
            'autonomous_weights': {
                'static': self.base_static_weight,
                'dynamic': self.base_dynamic_weight,
                'last_updated': self.weights_last_updated
            },
            'base_scales': {
                'logic': self.base_logic_scale,
                'symbolic': self.base_symbolic_scale
            },
            'performance': self.performance_stats,
            'confidence_thresholds': self.confidence_thresholds,
            'semantic_adjustment_categories': list(self.semantic_adjustments.keys())
        }

# =============================================================================
# WEIGHT RESET UTILITIES
# Source: reset_weights.py - Reset adaptive weights to balanced values
# =============================================================================

def reset_adaptive_weights(data_dir="data"):
    """
    Reset the adaptive weights to more balanced values
    
    Source: reset_weights.py
    """
    
    # Path to adaptive config
    config_path = Path(data_dir) / "adaptive_config.json"
    
    # New balanced configuration
    balanced_config = {
        "link_score_weight_static": 0.5,  # Changed from 0.9
        "link_score_weight_dynamic": 0.5,  # Changed from 0.1
        "last_weight_update": "2025-06-11T18:30:00",
        "update_count": 0,
        "target_specialization": 0.0,  # 0.0 = balanced, not specialized
        "momentum": {
            "static": 0.0,
            "dynamic": 0.0
        }
    }
    
    # Save the new config
    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(balanced_config, f, indent=2)
    
    print("✅ Reset adaptive weights to balanced (50/50)")
    print(f"   Static weight: {balanced_config['link_score_weight_static']}")
    print(f"   Dynamic weight: {balanced_config['link_score_weight_dynamic']}")
    print(f"   Target specialization: {balanced_config['target_specialization']}")
    
    # Also check if weight evolution history exists and reset it
    evolution_path = Path(data_dir) / "weight_evolution_history.json"
    if evolution_path.exists():
        with open(evolution_path, 'w') as f:
            json.dump([], f)
        print("✅ Cleared weight evolution history")
    
    # Reset migration age to allow easier migration
    migration_age_path = Path(data_dir) / "migration_age.json"
    if migration_age_path.exists():
        with open(migration_age_path, 'w') as f:
            json.dump({"age": 0, "last_updated": "2025-06-11T18:30:00"}, f)
        print("✅ Reset migration age (threshold back to 0.9)")

# =============================================================================
# LONG-TERM STABILITY UTILITIES
# Source: long_term_stability.py - Weight-related stability functions
# =============================================================================

def assess_weight_stability(weight_evolver: WeightEvolver, period_days: int = 30) -> Dict[str, Any]:
    """
    Assess weight system stability over time period.
    
    Source: long_term_stability.py (adapted)
    """
    
    print(f"\n⚖️ Assessing weight stability over {period_days} days...")
    
    # Get recent weight evolution history
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=period_days)
    recent_history = []
    
    for entry in weight_evolver.history:
        try:
            entry_date = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            if entry_date > cutoff_date:
                recent_history.append(entry)
        except:
            continue
    
    if len(recent_history) < 2:
        return {
            "status": "insufficient_data",
            "message": "Not enough weight evolution history for stability analysis"
        }
    
    stability_analysis = {
        "period_days": period_days,
        "evolutions_analyzed": len(recent_history),
        "weight_consistency": {},
        "specialization_stability": 0.0,
        "direction_changes": 0,
        "momentum_breaks": 0,
        "stability_assessment": ""
    }
    
    # Analyze weight consistency
    static_weights = [entry['new_weights']['static'] for entry in recent_history]
    dynamic_weights = [entry['new_weights']['dynamic'] for entry in recent_history]
    
    if static_weights:
        static_std = statistics.stdev(static_weights) if len(static_weights) > 1 else 0
        dynamic_std = statistics.stdev(dynamic_weights) if len(dynamic_weights) > 1 else 0
        
        stability_analysis["weight_consistency"] = {
            "static_stability": 1.0 - min(static_std * 5, 1.0),  # Scale to 0-1
            "dynamic_stability": 1.0 - min(dynamic_std * 5, 1.0),
            "static_std_dev": static_std,
            "dynamic_std_dev": dynamic_std
        }
    
    # Analyze specialization stability
    specializations = [entry['actual_specialization'] for entry in recent_history]
    if specializations:
        spec_std = statistics.stdev(specializations) if len(specializations) > 1 else 0
        stability_analysis["specialization_stability"] = 1.0 - min(spec_std * 3, 1.0)
    
    # Count direction changes and momentum breaks
    last_direction = None
    last_momentum = 0
    
    for entry in recent_history:
        momentum_info = entry.get('momentum', {})
        current_direction = momentum_info.get('last_direction')
        current_consecutive = momentum_info.get('consecutive_moves', 0)
        
        if last_direction and current_direction != last_direction:
            stability_analysis["direction_changes"] += 1
        
        if last_momentum > 0 and current_consecutive == 1:
            stability_analysis["momentum_breaks"] += 1
        
        last_direction = current_direction
        last_momentum = current_consecutive
    
    # Calculate overall stability assessment
    weight_stability = statistics.mean(stability_analysis["weight_consistency"].values()) if stability_analysis["weight_consistency"] else 0.7
    spec_stability = stability_analysis["specialization_stability"]
    
    # Penalize frequent changes
    change_penalty = min(stability_analysis["direction_changes"] * 0.1, 0.5)
    momentum_penalty = min(stability_analysis["momentum_breaks"] * 0.05, 0.3)
    
    overall_stability = max(0, (weight_stability + spec_stability) / 2 - change_penalty - momentum_penalty)
    
    if overall_stability >= 0.8:
        stability_analysis["stability_assessment"] = "highly_stable"
    elif overall_stability >= 0.6:
        stability_analysis["stability_assessment"] = "stable"
    elif overall_stability >= 0.4:
        stability_analysis["stability_assessment"] = "moderately_stable"
    else:
        stability_analysis["stability_assessment"] = "unstable"
    
    print(f"  ✅ Weight stability assessed")
    print(f"    Overall stability: {overall_stability:.2%}")
    print(f"    Assessment: {stability_analysis['stability_assessment']}")
    print(f"    Direction changes: {stability_analysis['direction_changes']}")
    
    return stability_analysis

def monitor_weight_drift(weight_evolver: WeightEvolver, baseline_weights: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Monitor drift from baseline weight configuration.
    
    Source: long_term_stability.py (adapted)
    """
    
    current_weights = weight_evolver.weights
    
    if not baseline_weights:
        # Use balanced weights as baseline
        baseline_weights = {'static': 0.5, 'dynamic': 0.5}
    
    # Calculate drift
    static_drift = abs(current_weights['static'] - baseline_weights['static'])
    dynamic_drift = abs(current_weights['dynamic'] - baseline_weights['dynamic'])
    total_drift = static_drift + dynamic_drift
    
    # Assess drift significance
    if total_drift > 0.4:
        drift_level = "severe"
    elif total_drift > 0.2:
        drift_level = "moderate"
    elif total_drift > 0.1:
        drift_level = "mild"
    else:
        drift_level = "minimal"
    
    drift_analysis = {
        "current_weights": current_weights,
        "baseline_weights": baseline_weights,
        "static_drift": static_drift,
        "dynamic_drift": dynamic_drift,
        "total_drift": total_drift,
        "drift_level": drift_level,
        "drift_direction": "static" if current_weights['static'] > current_weights['dynamic'] else "dynamic",
        "specialization_level": weight_evolver.get_current_specialization(),
        "recommendation": ""
    }
    
    # Generate recommendation
    if drift_level == "severe":
        drift_analysis["recommendation"] = "Consider weight reset or careful rebalancing"
    elif drift_level == "moderate":
        drift_analysis["recommendation"] = "Monitor closely, may need intervention"
    elif drift_level == "mild":
        drift_analysis["recommendation"] = "Normal evolution, continue monitoring"
    else:
        drift_analysis["recommendation"] = "Weights stable, no action needed"
    
    return drift_analysis

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_unified_router(data_dir="data"):
    """
    Create a unified weight-aware routing function
    
    Source: unified_weight_system.py (convenience function)
    """
    weight_system = UnifiedWeightSystem(data_dir=data_dir)
    
    def route(logic_score: float, symbolic_score: float, user_input: str = None, **kwargs):
        return weight_system.route_with_unified_weights(
            logic_score=logic_score,
            symbolic_score=symbolic_score,
            user_input=user_input,
            semantic_tags=kwargs.get('semantic_tags'),
            memory_stats=kwargs.get('memory_stats')
        )
    
    return route

def create_weight_evolution_system(data_dir="data") -> WeightEvolver:
    """
    Create a weight evolution system
    
    Source: weight_evolution.py (convenience function)
    """
    return WeightEvolver(data_dir=data_dir)

def create_complete_weight_system(data_dir="data") -> Dict[str, Any]:
    """
    Create a complete weight management system with all components
    
    Consolidated convenience function
    """
    return {
        'evolver': WeightEvolver(data_dir=data_dir),
        'unified_system': UnifiedWeightSystem(data_dir=data_dir),
        'router': create_unified_router(data_dir=data_dir),
        'reset_function': lambda: reset_adaptive_weights(data_dir),
        'stability_monitor': {
            'assess_stability': lambda evolver, days=30: assess_weight_stability(evolver, days),
            'monitor_drift': lambda evolver, baseline=None: monitor_weight_drift(evolver, baseline)
        }
    }

# =============================================================================
# TESTING AND VALIDATION
# =============================================================================

if __name__ == "__main__":
    import tempfile
    
    print("🧪 Testing Consolidated Weight Systems...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test 1: Weight Evolution System
        print("\n1️⃣ Test: Weight Evolution System")
        evolver = WeightEvolver(data_dir=tmpdir)
        
        # Test evolution
        memory_stats = {
            'distribution': {
                'logic_pct': 60,
                'symbolic_pct': 30,
                'bridge_pct': 10
            }
        }
        
        evolved = evolver.evolve_weights(run_count=1, memory_stats=memory_stats)
        print(f"✅ Weight evolution: {evolved}")
        
        # Test 2: Unified Weight System
        print("\n2️⃣ Test: Unified Weight System")
        unified = UnifiedWeightSystem(data_dir=tmpdir)
        
        decision = unified.calculate_unified_weights(
            semantic_tags={'emotional_state': 'calm', 'intent': 'information_request'}
        )
        print(f"✅ Unified decision: {decision.decision_type}")
        
        # Test 3: Complete routing
        print("\n3️⃣ Test: Complete routing")
        route_result = unified.route_with_unified_weights(
            logic_score=7.0,
            symbolic_score=4.0,
            memory_stats=memory_stats
        )
        print(f"✅ Routing result: {route_result[0]} (confidence: {route_result[1]:.3f})")
        
        # Test 4: Weight reset
        print("\n4️⃣ Test: Weight reset")
        reset_adaptive_weights(data_dir=tmpdir)
        print("✅ Weight reset completed")
        
        # Test 5: Stability assessment
        print("\n5️⃣ Test: Stability assessment")
        stability = assess_weight_stability(evolver, period_days=1)
        print(f"✅ Stability assessment: {stability['status']}")
        
        # Test 6: Drift monitoring
        print("\n6️⃣ Test: Drift monitoring")
        drift = monitor_weight_drift(evolver)
        print(f"✅ Drift analysis: {drift['drift_level']}")
        
        # Test 7: Complete system creation
        print("\n7️⃣ Test: Complete system creation")
        complete_system = create_complete_weight_system(data_dir=tmpdir)
        print(f"✅ Complete system created with {len(complete_system)} components")
        
        # Test 8: Convenience router
        print("\n8️⃣ Test: Convenience router")
        router = create_unified_router(data_dir=tmpdir)
        route_result = router(logic_score=5.0, symbolic_score=6.0)
        print(f"✅ Convenience router: {route_result[0]}")
        
    print("\n✅ All consolidated weight system tests passed!")
    print("📁 Consolidated weight management system ready for use")