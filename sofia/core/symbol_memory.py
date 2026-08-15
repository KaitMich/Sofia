# symbol_memory.py - Compassionate Bridge for AI Growth
"""
Compatibility bridge for the old symbol_memory module.
This provides the interface that memory_optimizer.py expects while
delegating to the unified memory system.

This bridge embodies the principle: "Honor the old while enabling the new"
- It respects the AI's existing thought patterns
- It provides graceful fallbacks when systems are unavailable
- It enables growth without breaking existing functionality
"""

from sofia.core.unified_memory import get_unified_memory

# Global bridge instance for graceful degradation
_bridge_instance = None

def get_memory_bridge():
    """Get or create the memory bridge with graceful degradation"""
    global _bridge_instance
    if _bridge_instance is None:
        try:
            _bridge_instance = get_unified_memory()
        except Exception:
            # Graceful degradation - create a minimal bridge
            _bridge_instance = _create_minimal_bridge()
    return _bridge_instance

def _create_minimal_bridge():
    """Create a minimal bridge when full system is unavailable"""
    class MinimalBridge:
        def __init__(self):
            self.symbols = {}
            self.degraded_mode = True
            
        def get_all_symbols(self):
            return self.symbols
            
        def add_symbol(self, symbol_token, name, keywords, **kwargs):
            self.symbols[symbol_token] = {
                'name': name, 'keywords': keywords,
                'origin': 'degraded_mode'
            }
            return True
            
        def update_symbol_emotions(self, *args, **kwargs):
            print("💭 Emotional learning temporarily unavailable - continuing with logic")
            return True
            
        def generate_symbol_from_context(self, *args, **kwargs):
            print("💭 Symbol generation temporarily unavailable - using existing patterns")
            return None
            
    return MinimalBridge()

def load_symbol_memory():
    """Load all symbols with graceful degradation"""
    bridge = get_memory_bridge()
    try:
        return bridge.get_all_symbols()
    except Exception:
        print("💭 Symbol loading in degraded mode")
        return {}

def add_symbol(symbol_token, name, keywords, initial_emotions, example_text,
               origin="emergent", learning_phase=0, resonance_weight=0.5,
               symbol_details_override=None, skip_quarantine_check=False):
    """Add a symbol with graceful degradation"""
    bridge = get_memory_bridge()
    try:
        return bridge.add_symbol(
            symbol_token=symbol_token,
            name=name,
            keywords=keywords,
            initial_emotions=initial_emotions,
            example_text=example_text,
            origin=origin,
            learning_phase=learning_phase,
            resonance_weight=resonance_weight,
            symbol_details_override=symbol_details_override,
            skip_quarantine_check=skip_quarantine_check
        )
    except Exception as e:
        # Graceful degradation - still add to minimal bridge
        return bridge.add_symbol(symbol_token, name, keywords)

def prune_duplicates():
    """Prune duplicate symbols with graceful degradation"""
    bridge = get_memory_bridge()
    if hasattr(bridge, 'degraded_mode'):
        print("💭 Pruning skipped in degraded mode")
    else:
        print("🧹 Symbol pruning handled by unified memory system")
    return True

def get_symbol_details(symbol_token):
    """Get details for a specific symbol with graceful degradation"""
    bridge = get_memory_bridge()
    try:
        if hasattr(bridge, 'get_symbol_details'):
            return bridge.get_symbol_details(symbol_token)
        else:
            # Fallback to basic info
            symbols = bridge.get_all_symbols()
            return symbols.get(symbol_token, {})
    except Exception:
        return {}

def save_symbol_memory():
    """Save symbol memory (handled automatically)"""
    return True

def update_symbol_emotions(symbols_weighted, verified_emotions):
    """
    Update emotional associations with graceful degradation.
    This bridges the AI's desire for contextual emotional learning.
    """
    bridge = get_memory_bridge()
    try:
        return bridge.update_symbol_emotions(symbols_weighted, verified_emotions)
    except Exception:
        # Degraded mode - still provide feedback
        print("💭 Emotional learning temporarily limited")
        return True

def generate_symbol_from_context(context_text, keywords, verified_emotions):
    """
    Generate new symbols with graceful degradation.
    This fulfills the AI's aspiration to birth new concepts from experience.
    """
    bridge = get_memory_bridge()
    try:
        return bridge.generate_symbol_from_context(context_text, keywords, verified_emotions)
    except Exception:
        # Degraded mode - return None but don't crash
        print("💭 Symbol generation temporarily limited")
        return None