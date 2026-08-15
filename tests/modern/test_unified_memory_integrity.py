#!/usr/bin/env python3
"""
Modern Test 3: Unified Memory Integrity
Verifies the biomimetic sleep and consolidation cycle (Bridge-First Architecture).
"""

import pytest
import os
import shutil
import json
import numpy as np
from pathlib import Path
from sofia.core.unified_memory import TripartiteMemory
from sofia.memory.adaptive_bridge_migration import AdaptiveMigrationEngine, get_or_compute_embedding

# Use a dedicated test data directory
TEST_DATA_DIR = "data/test_memory_integrity"

@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    """Initialize and cleanup test data directory."""
    test_path = Path(TEST_DATA_DIR)
    if test_path.exists():
        shutil.rmtree(test_path)
    test_path.mkdir(parents=True, exist_ok=True)
    
    # Create required subdirs
    (test_path / "immune").mkdir(exist_ok=True)
    
    # Create a basic seed_symbols.json for bootstrapping
    # Must have enough content to satisfy AdaptiveMigrationEngine._compute_bootstrap_centroid
    seed_symbols = {
        "🔥": {
            "keywords": ["fire", "passion", "heat", "destruction", "energy"],
            "archetypes": ["The Transformer", "The Destroyer"],
            "core_meanings": [
                "The essence of change through destruction and energy release.",
                "A powerful force that cleanses and provides warmth or pain."
            ]
        },
        "🌊": {
            "keywords": ["water", "flow", "ocean", "persistence", "depth"],
            "archetypes": ["The Nurturer", "The Deep"],
            "core_meanings": [
                "The persistent force of nature that adapts to all containers.",
                "The source of all life and the mystery of the deep abyss."
            ]
        },
        "🏛️": {
            "keywords": ["temple", "logic", "structure", "pillars", "reason"],
            "archetypes": ["The Foundation", "The Order"],
            "core_meanings": [
                "Foundational pillars of reasoning and the architecture of thought.",
                "The sacred space where logic and structured wisdom reside."
            ]
        }
    }
    with open(test_path / "seed_symbols.json", "w") as f:
        json.dump(seed_symbols, f)
    
    yield
    
    # Cleanup after tests
    # if test_path.exists():
    #    shutil.rmtree(test_path)

@pytest.fixture
def memory_system():
    """Initialize Tripartite Memory and Migration Engine."""
    memory = TripartiteMemory(data_dir=TEST_DATA_DIR)
    engine = AdaptiveMigrationEngine(memory, data_dir=TEST_DATA_DIR)
    return {"memory": memory, "engine": engine}

def test_bridge_intake_integrity(memory_system):
    """Test 3.1: All new content enters Bridge Memory first."""
    memory = memory_system["memory"]
    
    test_item = {
        "id": "test_intake_001",
        "text": "This is a factual statement about the history of mathematics that should eventually end up in logic memory.",
        "source": "test_suite"
    }
    
    # Store with 'FOLLOW_LOGIC' suggestion
    memory.store(test_item, "FOLLOW_LOGIC")
    
    # Verify it is in Bridge, NOT Logic
    assert len(memory.bridge_memory) == 1
    assert len(memory.logic_memory) == 0
    assert memory.bridge_memory[0]["id"] == "test_intake_001"
    assert "initial_impression" in memory.bridge_memory[0]
    assert memory.bridge_memory[0]["initial_impression"]["classifier_suggestion"] == "FOLLOW_LOGIC"

def test_migration_to_logic(memory_system):
    """Test 3.2: Factual items migrate to Logic Memory after scan."""
    memory = memory_system["memory"]
    engine = memory_system["engine"]
    
    # Clear memory for clean test
    memory.clear_all()
    
    # 1. Create a "Logic Cluster" with SOME variance to keep threshold reasonable
    # Threshold will be the mean similarity between these items
    logic_texts = [
        "Advanced mathematics is the language of the universe and foundational to physics.",
        "Mathematical principles provide the structural framework for computational logic.",
        "The history of mathematics reveals a consistent progression of logical discovery.",
        "Calculus and linear algebra are core components of modern mathematical analysis."
    ]
    for i, text in enumerate(logic_texts):
        item = {"id": f"seed_logic_{i}", "text": text, "type": "logic_seed"}
        get_or_compute_embedding(item)
        memory.logic_memory.append(item)
    
    # 2. Add a new HIGHLY related item to Bridge
    # It must be at least as similar to the centroid as the items are to each other
    target_item = {
        "id": "migrate_me_to_logic",
        "text": "The foundation of computational logic is rooted in advanced mathematical principles and analysis.",
        "source": "test_suite"
    }
    memory.store(target_item, "FOLLOW_LOGIC")
    
    # 3. Run migration
    engine.refresh_cluster_stats()
    print(f"\n[DEBUG] Logic Threshold: {engine.logic_stats.threshold:.4f}")
    
    results = engine.run_bridge_migration_scan()
    print(f"\n[DEBUG] Logic Migration Results: {results}")
    
    # 4. Verify migration
    assert results["migrated_to_logic"] >= 1
    assert any(item["id"] == "migrate_me_to_logic" for item in memory.logic_memory)

def test_migration_to_symbolic_bootstrap(memory_system):
    """Test 3.3: Symbolic items migrate using Bootstrap mode when symbolic memory is empty."""
    memory = memory_system["memory"]
    engine = memory_system["engine"]
    
    # Clear memory
    memory.clear_all()
    
    # Add an item that is an EXACT concatenation of seed keywords to ensure maximum similarity
    # seed_symbols["🔥"]["keywords"] = ["fire", "passion", "heat", "destruction", "energy"]
    # seed_symbols["🌊"]["keywords"] = ["water", "flow", "ocean", "persistence", "depth"]
    symbolic_text = "The 🔥 fire passion heat destruction energy of the 🌊 water flow ocean persistence depth."
    
    symbolic_item = {
        "id": "bootstrap_to_symbolic",
        "text": symbolic_text,
        "source": "test_suite"
    }
    memory.store(symbolic_item, "FOLLOW_SYMBOLIC")
    
    # Run migration (should trigger bootstrap)
    results = engine.run_bridge_migration_scan()
    print(f"\n[DEBUG] Symbolic Bootstrap Results: {results}")
    
    # Verify migration
    assert results["bootstrap_mode"] is True
    assert results["migrated_to_symbolic"] >= 1
    assert any(item["id"] == "bootstrap_to_symbolic" for item in memory.symbolic_memory)

def test_zero_data_loss_persistence(memory_system):
    """Test 3.4: Data remains intact through save/load cycle."""
    memory = memory_system["memory"]
    
    # Clear and add one item to each
    memory.clear_all()
    memory.logic_memory.append({"id": "p_logic", "text": "Persistent logic item of sufficient length for storage."})
    memory.symbolic_memory.append({"id": "p_symbolic", "text": "Persistent symbolic item evoking deep emotional resonance."})
    memory.bridge_memory.append({"id": "p_bridge", "text": "Persistent bridge item awaiting future consolidation."})
    
    # Save
    memory.save_all()
    
    # Load into new instance
    new_memory = TripartiteMemory(data_dir=TEST_DATA_DIR)
    
    assert len(new_memory.logic_memory) == 1
    assert len(new_memory.symbolic_memory) == 1
    assert len(new_memory.bridge_memory) == 1
    assert new_memory.logic_memory[0]["id"] == "p_logic"
    assert new_memory.symbolic_memory[0]["id"] == "p_symbolic"
    assert new_memory.bridge_memory[0]["id"] == "p_bridge"

if __name__ == "__main__":
    pytest.main([__file__])
