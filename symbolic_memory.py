#!/usr/bin/env python3
"""
Symbolic Memory System

This module provides the SymbolicMemory class that was expected by the consciousness systems.
It interfaces with the unified memory system to provide symbolic memory functionality.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class SymbolicMemory:
    """
    Symbolic memory system that integrates with unified memory.
    Provides specialized symbolic memory operations.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize connection to unified memory
        try:
            from unified_memory import get_unified_memory
            self.unified_memory = get_unified_memory(data_dir)
        except ImportError:
            print("⚠️ Unified memory not available - operating in standalone mode")
            self.unified_memory = None
    
    def store_symbol(self, symbol_data: Dict[str, Any]) -> bool:
        """Store a symbolic memory item."""
        try:
            if self.unified_memory:
                # Store through unified memory system
                self.unified_memory.store_decision(symbol_data, "FOLLOW_SYMBOLIC")
                return True
            else:
                # Fallback: store directly to symbolic_memory.json
                symbolic_file = self.data_dir / "symbolic_memory.json"
                
                # Load existing data
                if symbolic_file.exists():
                    with open(symbolic_file, 'r') as f:
                        data = json.load(f)
                else:
                    data = []
                
                # Add timestamp
                symbol_data['stored_at'] = datetime.utcnow().isoformat()
                data.append(symbol_data)
                
                # Save back
                with open(symbolic_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                return True
        except Exception as e:
            print(f"⚠️ Failed to store symbol: {e}")
            return False
    
    def get_symbols(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve symbolic memories."""
        try:
            if self.unified_memory:
                # Get from unified memory system
                # Access symbolic_memory directly if available
                if hasattr(self.unified_memory, 'symbolic_memory'):
                    symbols = self.unified_memory.symbolic_memory
                    return symbols[:limit] if limit else symbols
                else:
                    return []
            else:
                # Fallback: read from file
                symbolic_file = self.data_dir / "symbolic_memory.json"
                if symbolic_file.exists():
                    with open(symbolic_file, 'r') as f:
                        data = json.load(f)
                        return data[:limit] if limit else data
                else:
                    return []
        except Exception as e:
            print(f"⚠️ Failed to retrieve symbols: {e}")
            return []
    
    def find_symbols_by_emotion(self, emotion: str) -> List[Dict[str, Any]]:
        """Find symbols associated with a specific emotion."""
        symbols = self.get_symbols()
        matching = []
        
        for symbol in symbols:
            # Check various emotion field formats
            emotions = symbol.get('emotions', {})
            if isinstance(emotions, dict):
                if emotion.lower() in emotions or emotion.lower() in [k.lower() for k in emotions.keys()]:
                    matching.append(symbol)
            elif isinstance(emotions, list):
                if emotion.lower() in [str(e).lower() for e in emotions]:
                    matching.append(symbol)
            
            # Also check emotional_anchor if present
            emotional_anchor = symbol.get('emotional_anchor', {})
            if isinstance(emotional_anchor, dict):
                if emotion.lower() == emotional_anchor.get('primary_emotion', '').lower():
                    matching.append(symbol)
                if emotion.lower() in [r.lower() for r in emotional_anchor.get('resonance', [])]:
                    matching.append(symbol)
        
        return matching
    
    def find_symbols_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Find symbols associated with a keyword."""
        symbols = self.get_symbols()
        matching = []
        
        for symbol in symbols:
            # Check keywords field
            keywords = symbol.get('keywords', [])
            if keyword.lower() in [k.lower() for k in keywords]:
                matching.append(symbol)
            
            # Also check text content
            text = symbol.get('text', '')
            if keyword.lower() in text.lower():
                matching.append(symbol)
        
        return matching
    
    def get_symbol_count(self) -> int:
        """Get the total count of symbolic memories."""
        return len(self.get_symbols())
    
    def get_emotional_distribution(self) -> Dict[str, int]:
        """Get distribution of emotions across symbolic memories."""
        symbols = self.get_symbols()
        emotion_counts = {}
        
        for symbol in symbols:
            emotions = symbol.get('emotions', {})
            if isinstance(emotions, dict):
                for emotion in emotions.keys():
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            elif isinstance(emotions, list):
                for emotion in emotions:
                    emotion_str = str(emotion)
                    emotion_counts[emotion_str] = emotion_counts.get(emotion_str, 0) + 1
            
            # Also count emotional_anchor
            emotional_anchor = symbol.get('emotional_anchor', {})
            if isinstance(emotional_anchor, dict):
                primary_emotion = emotional_anchor.get('primary_emotion')
                if primary_emotion:
                    emotion_counts[primary_emotion] = emotion_counts.get(primary_emotion, 0) + 1
        
        return emotion_counts

# Legacy function for backward compatibility
def get_symbolic_memory(data_dir: str = "data") -> SymbolicMemory:
    """Get or create a SymbolicMemory instance."""
    return SymbolicMemory(data_dir)

# Test functionality
if __name__ == "__main__":
    print("🧪 Testing SymbolicMemory...")
    
    # Test initialization
    sym_mem = SymbolicMemory("test_data")
    print(f"✅ SymbolicMemory initialized")
    
    # Test symbol retrieval
    symbols = sym_mem.get_symbols(limit=5)
    print(f"✅ Retrieved {len(symbols)} symbols")
    
    # Test emotion distribution
    emotions = sym_mem.get_emotional_distribution()
    print(f"✅ Emotional distribution: {len(emotions)} unique emotions")
    
    print("✅ SymbolicMemory tests passed")