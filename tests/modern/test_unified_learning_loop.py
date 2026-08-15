#!/usr/bin/env python3
"""
Modern Test 2: Unified Learning Loop
Verifies the complete cycle from curiosity to choice to preference learning.
"""

import pytest
import os
import shutil
import json
from pathlib import Path
from sofia.core.curiosity_engine import CuriosityEngine
from sofia.core.choice_architecture import ChoiceArchitecture, LearningChoice
from sofia.memory.preference_learning_system import PreferenceLearningSystem
from sofia.core.CONSCIOUSNESS_MEMORY import ExperienceMemory

# Use a dedicated test data directory
TEST_DATA_DIR = "data/test_unified_learning_loop"

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
    
    yield
    
    # Cleanup after tests
    # if test_path.exists():
    #    shutil.rmtree(test_path)

@pytest.fixture
def learning_systems():
    """Initialize the learning systems for testing."""
    curiosity = CuriosityEngine(data_dir=TEST_DATA_DIR)
    choice_arch = ChoiceArchitecture(data_dir=TEST_DATA_DIR)
    preference_sys = PreferenceLearningSystem(data_dir=TEST_DATA_DIR)
    experience_mem = ExperienceMemory(data_dir=TEST_DATA_DIR)
    
    return {
        "curiosity": curiosity,
        "choice": choice_arch,
        "preference": preference_sys,
        "experience": experience_mem
    }

def test_curiosity_stimulation(learning_systems):
    """Test 2.1: Curiosity Engine identifies triggers in new content."""
    curiosity = learning_systems["curiosity"]
    
    # Content with mystery and complexity triggers
    novel_content = "This discovery reveals an unknown mystery about a complex relationship in quantum physics."
    
    initial_momentum = curiosity.curiosity_momentum
    result = curiosity.stimulate_curiosity_from_content(novel_content)
    
    assert result["curiosity_stimulated"] is True
    assert result["stimulation_level"] > 0
    # Momentum should increase if stimulation is high enough
    if result["stimulation_level"] > 0.3:
        assert curiosity.curiosity_momentum > initial_momentum

def test_autonomous_learning_choice(learning_systems):
    """Test 2.2: Choice Architecture makes a decision based on content and context."""
    choice_arch = learning_systems["choice"]
    
    test_content = {
        "id": "quantum_physics_001",
        "text": "Quantum entanglement is a complex and mysterious phenomenon where particles become linked.",
        "content_type": "scientific",
        "topics": ["physics", "quantum_mechanics"],
        "complexity": 0.8,
        "depth": 0.7
    }
    
    test_context = {
        "available_time": 3600,
        "cognitive_load": 0.2,
        "current_curiosity_focus": "fundamental_physics"
    }
    
    choice = choice_arch.make_learning_choice(test_content, test_context)
    
    assert isinstance(choice, LearningChoice)
    assert choice.choice_type in ["accept", "reject", "defer", "selective"]
    assert choice.confidence_in_choice > 0
    assert len(choice.choice_reasoning) > 0

def test_preference_evolution_loop(learning_systems):
    """Test 2.3: Successful choice leads to preference update."""
    choice_arch = learning_systems["choice"]
    preference_sys = learning_systems["preference"]
    
    # Define a specific topic to learn preference for (must match hardcoded keywords in preference_learning_system.py)
    topic = "consciousness"
    test_content = {
        "id": "consciousness_insight",
        "text": "Consciousness might emerge from complex information integration patterns.",
        "content_type": "philosophical",
        "topics": [topic],
        "complexity": 0.9,
        "depth": 0.8
    }
    
    # Set high interest context to ensure acceptance
    test_context = {
        "available_time": 5000,
        "cognitive_load": 0.1,
        "interests": [topic]
    }
    
    # Initial state check
    initial_prefs = [p for p in preference_sys.preferences.values() if p.preference_type == "topic"]
    initial_topic_pref = next((p for p in initial_prefs if p.item_name == topic), None)
    initial_strength = initial_topic_pref.preference_strength if initial_topic_pref else 0.0
    
    # Make choice (this calls preference_sys.learn_from_choice_decision internally)
    choice = choice_arch.make_learning_choice(test_content, test_context)
    
    # Use the preference system instance from choice_arch to check updated state
    active_pref_sys = choice_arch._get_preference_learning_system()
    assert active_pref_sys is not None
    
    # Verify preference updated
    updated_prefs = [p for p in active_pref_sys.preferences.values() if p.preference_type == "topic"]
    updated_topic_pref = next((p for p in updated_prefs if p.item_name == topic), None)
    
    assert updated_topic_pref is not None
    if choice.choice_type == "accept":
        assert updated_topic_pref.preference_strength >= initial_strength
        assert updated_topic_pref.evidence_count > (initial_topic_pref.evidence_count if initial_topic_pref else 0)

def test_intrinsic_goal_generation(learning_systems):
    """Test 2.4: System generates new goals based on drive satisfaction."""
    curiosity = learning_systems["curiosity"]
    
    # Manually lower a drive to trigger goal generation
    if "exploration" in curiosity.fundamental_drives:
        curiosity.fundamental_drives["exploration"]["current_satisfaction"] = 0.1
    
    goals = curiosity.generate_intrinsic_goals()
    
    assert len(goals) > 0
    # At least one goal should be related to exploration
    exploration_goals = [g for g in goals if "exploration" in g.get("description", "").lower() or g.get("type") == "exploration"]
    assert len(exploration_goals) > 0 or any(g.get("urgency", 0) > 0.5 for g in goals)

if __name__ == "__main__":
    pytest.main([__file__])
