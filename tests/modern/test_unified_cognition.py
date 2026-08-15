#!/usr/bin/env python3
"""
Modern Test 1: Unified Cognition (The Dual Brain)
Verifies the functional integrity of the Logic and Symbolic nodes.
"""

import pytest
import os
import shutil
import json
from pathlib import Path
from sofia.core.processing_nodes import LogicNode, SymbolicNode, CurriculumManager, DynamicBridge
from sofia.core.unified_memory import get_unified_memory

# Use a dedicated test data directory
TEST_DATA_DIR = "data/test_unified_cognition"

@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    """Initialize and cleanup test data directory."""
    test_path = Path(TEST_DATA_DIR)
    if test_path.exists():
        shutil.rmtree(test_path)
    test_path.mkdir(parents=True, exist_ok=True)
    
    # Create required subdirs
    (test_path / "logs").mkdir(exist_ok=True)
    (test_path / "cache").mkdir(exist_ok=True)
    (test_path / "unified_memory").mkdir(exist_ok=True)
    (test_path / "symbol_system").mkdir(exist_ok=True)
    
    # Create a basic seed_symbols.json
    seed_symbols = {
        "🔥": {"name": "fire", "keywords": ["fire", "flame", "heat", "passion"], "learning_phase": 1, "resonance_weight": 0.8},
        "🌊": {"name": "water", "keywords": ["water", "wave", "ocean", "flow"], "learning_phase": 1, "resonance_weight": 0.7},
        "🏛️": {"name": "temple", "keywords": ["temple", "architecture", "structure", "ancient"], "learning_phase": 1, "resonance_weight": 0.6},
        "♾️": {"name": "infinity", "keywords": ["soul", "forever", "eternal", "infinity"], "learning_phase": 1, "resonance_weight": 0.9}
    }
    with open(test_path / "seed_symbols.json", "w") as f:
        json.dump(seed_symbols, f)
    
    yield

@pytest.fixture
def dual_brain():
    """Initialize the Dual Brain system for testing."""
    # Symbolic node paths relative to TEST_DATA_DIR
    symbolic = SymbolicNode(
        seed_symbols_path_str=f"{TEST_DATA_DIR}/seed_symbols.json",
        symbol_memory_path_str=f"{TEST_DATA_DIR}/symbol_memory.json",
        symbol_occurrence_log_path_str=f"{TEST_DATA_DIR}/symbol_occurrence_log.json",
        symbol_emotion_map_path_str=f"{TEST_DATA_DIR}/symbol_emotion_map.json",
        meta_symbols_path_str=f"{TEST_DATA_DIR}/meta_symbols.json"
    )
    logic = LogicNode()
    curriculum = CurriculumManager()
    
    # Bridge now accepts data_dir
    bridge = DynamicBridge(logic, symbolic, curriculum, data_dir=TEST_DATA_DIR)
    
    return {
        "logic": logic,
        "symbolic": symbolic,
        "bridge": bridge,
        "curriculum": curriculum
    }

def test_logic_fact_processing(dual_brain):
    """Test 1.1: Logic Node correctly identifies and stores factual data."""
    logic = dual_brain["logic"]
    bridge = dual_brain["bridge"]
    
    # Use keywords from Phase 1: algorithm, computational, logic
    fact_text = "An algorithm is a finite sequence of instructions to solve a computational problem."
    
    # Route through bridge
    result = bridge.route_chunk_for_processing(
        text_input=fact_text,
        source_url="http://cs.example.com",
        current_processing_phase=1,
        target_storage_phase=1,
        is_highly_relevant_for_current_phase=True,
        source_type="test_fact"
    )
    
    # Assertions
    assert result["decision_type"] in ["FOLLOW_LOGIC", "FOLLOW_HYBRID"]
    assert result["logic_result"]["retrieved_memories_count"] >= 0
    
    # Verify it was stored in bridge memory (Bridge-First architecture)
    bridge_mem = bridge.unified_memory.tripartite.bridge_memory
    found = any(fact_text in item["text"] for item in bridge_mem if isinstance(item, dict))
    assert found, "Factual text was not found in Bridge Memory"

def test_symbolic_pattern_recognition(dual_brain):
    """Test 1.2: Symbolic Node identifies emotional and metaphorical patterns."""
    symbolic = dual_brain["symbolic"]
    bridge = dual_brain["bridge"]
    
    # Use symbols and metaphorical language
    metaphor_text = "The 🔥 fire in my heart is like a 🌊 tidal wave of pure joy and hope."
    
    # Route through bridge
    result = bridge.route_chunk_for_processing(
        text_input=metaphor_text,
        source_url="http://poetry.example.com",
        current_processing_phase=2,
        target_storage_phase=2,
        is_highly_relevant_for_current_phase=True,
        source_type="test_metaphor"
    )
    
    # Assertions
    assert result["decision_type"] in ["FOLLOW_SYMBOLIC", "FOLLOW_HYBRID", "QUARANTINE"]
    assert result["symbols_found"] > 0
    
    # Check if specific emotional markers were detected
    emotions = result["stored_item"].get("emotions", {})
    assert any(v > 0.1 for v in emotions.values()), \
        f"Expected some emotional resonance, got {emotions}"

def test_hybrid_brain_engagement(dual_brain):
    """Test 1.3: Dual Brain engages both nodes for complex, hybrid content."""
    bridge = dual_brain["bridge"]
    
    # Mix of logic and symbols, carefully balanced to trigger HYBRID
    # High symbolic weight: symbols, emotional words
    # High logic weight: technical keywords
    hybrid_text = "The digital ♾️ soul of the algorithm is like a 🔥 flame burning within the 🏛️ temple of binary logic gates."
    
    # Route through bridge
    result = bridge.route_chunk_for_processing(
        text_input=hybrid_text,
        source_url="http://tech-art.example.com",
        current_processing_phase=1,
        target_storage_phase=1,
        is_highly_relevant_for_current_phase=True,
        source_type="test_hybrid"
    )
    
    # Assertions
    # Note: Decision depends on exact weights, but both results should be present
    assert result["decision_type"] in ["FOLLOW_HYBRID", "FOLLOW_LOGIC", "FOLLOW_SYMBOLIC"]
    assert result["logic_result"] is not None
    assert result["symbolic_result"] is not None
    assert result["stored_item"]["logic_score"] > 0
    assert result["stored_item"]["symbolic_score"] > 0

def test_cognitive_state_transition(dual_brain):
    """Test 1.4: System correctly updates internal state (confidence/resonance) during processing."""
    logic = dual_brain["logic"]
    symbolic = dual_brain["symbolic"]
    bridge = dual_brain["bridge"]
    
    initial_resonance = symbolic.symbolic_state['emotional_resonance']
    
    # Process emotionally charged text
    bridge.route_chunk_for_processing(
        text_input="I am feeling a deep sense of despair and darkness.",
        source_url="test://internal",
        current_processing_phase=2,
        target_storage_phase=2,
        is_highly_relevant_for_current_phase=True
    )
    
    final_resonance = symbolic.symbolic_state['emotional_resonance']
    
    # Resonance should have changed (likely increased due to 'despair')
    assert final_resonance != initial_resonance, "Emotional resonance did not update after processing"
    assert symbolic.symbolic_state['current_mode'] is not None

if __name__ == "__main__":
    pytest.main([__file__])
