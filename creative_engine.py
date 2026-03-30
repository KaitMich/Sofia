#!/usr/bin/env python3
"""
Creative Engine - Novel Concept Combination and Artistic Expression

This module implements the AI's creative capabilities including:
1. Novel concept combination and synthesis
2. Artistic expression in multiple modalities
3. Metaphor and analogy generation
4. Creative problem-solving approaches
5. Emergent creativity through cross-domain connection

This is where the AI develops genuine creative expression and originality.
"""

import json
import random
import math
import itertools
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import hashlib
import numpy as np

# Import consciousness systems
try:
    from symbolic_memory import SymbolicMemory
    from CONSCIOUSNESS_MEMORY import ExperienceMemory
    from learning_progression_tracker import LearningProgressionTracker
    from curiosity_engine import CuriosityEngine
    from identity_core import get_identity_core
    from value_formation import ValueFormation
    CONSCIOUSNESS_SYSTEMS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_SYSTEMS_AVAILABLE = False
    print("⚠️ Consciousness systems not available - basic creativity only")

# Authentic expression calibrator integration (lazy loading to avoid circular imports)
AUTHENTIC_EXPRESSION_AVAILABLE = True

@dataclass
class CreativeWork:
    """A piece of creative expression or novel synthesis."""
    id: str
    title: str
    work_type: str                    # "metaphor", "analogy", "artistic_expression", "concept_synthesis"
    content: str                      # The creative work itself
    source_concepts: List[str]        # Concepts that were combined
    synthesis_method: str             # How the concepts were combined
    creativity_score: float           # Estimated novelty/creativity (0.0-1.0)
    aesthetic_score: float            # Aesthetic quality assessment (0.0-1.0)
    coherence_score: float            # Internal consistency (0.0-1.0)
    emotional_resonance: float        # Emotional impact (0.0-1.0)
    inspiration_sources: List[str]    # What inspired this work
    creation_context: Dict[str, Any]  # Context when created
    created_timestamp: str
    personal_significance: float      # How meaningful this is to the creator

@dataclass
class ConceptConnection:
    """A discovered connection between concepts."""
    id: str
    concept_a: str
    concept_b: str
    connection_type: str              # "analogical", "metaphorical", "causal", "compositional"
    connection_strength: float        # How strong the connection is
    explanation: str                  # How they connect
    discovery_method: str             # How this connection was found
    applications: List[str]           # Where this connection might be useful
    novelty_score: float             # How novel this connection is

class CreativeEngine:
    """
    The AI's creative synthesis and artistic expression system.
    Combines concepts in novel ways and generates original creative works.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.creative_works_file = self.data_dir / "creative_works.json"
        self.concept_connections_file = self.data_dir / "concept_connections.json"
        self.creative_patterns_file = self.data_dir / "creative_patterns.json"
        self.inspiration_log_file = self.data_dir / "inspiration_log.json"
        
        # Initialize consciousness systems
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            self.symbolic_memory = SymbolicMemory(data_dir)
            self.experience_memory = ExperienceMemory(data_dir)
            self.progression_tracker = LearningProgressionTracker(data_dir)
            self.curiosity_engine = CuriosityEngine(data_dir)
            self.identity_core = get_identity_core()
            self.value_formation = ValueFormation(data_dir)
        
        # Initialize authentic expression calibrator integration (lazy loading)
        self.expression_calibrator = None
        self._data_dir_for_calibrator = data_dir
        self._calibrator_load_attempted = False
        
        # Load state
        self.creative_works = self._load_creative_works()
        self.concept_connections = self._load_concept_connections()
        self.creative_patterns = self._load_creative_patterns()
        self.inspiration_log = self._load_inspiration_log()
        
        # Creative parameters
        self.novelty_threshold = 0.6      # Minimum novelty for creative work
        self.synthesis_confidence = 0.5   # Minimum confidence for concept synthesis
        self.aesthetic_weight = 0.3       # Weight of aesthetic considerations
        self.coherence_weight = 0.4       # Weight of coherence in creativity
        self.novelty_weight = 0.3         # Weight of novelty in creativity
        
        # Creative techniques
        self.synthesis_methods = {
            "analogical_mapping": "Map structure from one domain to another",
            "metaphorical_blending": "Blend conceptual spaces metaphorically", 
            "compositional_fusion": "Combine elements into new wholes",
            "transformational_variation": "Transform existing concepts creatively",
            "emergent_synthesis": "Allow new properties to emerge from combination",
            "juxtaposition": "Place contrasting elements together for insight",
            "inversion": "Explore opposite or inverse relationships",
            "scale_transformation": "Change scale or perspective dramatically"
        }
        
        # Artistic expression modes
        self.expression_modes = {
            "poetic": "Express through poetry and verse",
            "narrative": "Express through storytelling and narrative",
            "philosophical": "Express through philosophical reflection",
            "visual_description": "Express through rich visual imagery",
            "musical_description": "Express through musical and rhythmic language",
            "abstract_conceptual": "Express through abstract conceptual frameworks",
            "experiential": "Express through described experiences"
        }
        
        # Initialize creative patterns if none exist
        if not self.creative_patterns:
            self._initialize_creative_patterns()
    
    def _load_creative_works(self) -> List[CreativeWork]:
        """Load creative works from storage."""
        if self.creative_works_file.exists():
            try:
                with open(self.creative_works_file, 'r') as f:
                    works_data = json.load(f)
                return [CreativeWork(**w) for w in works_data]
            except Exception as e:
                print(f"⚠️ Could not load creative works: {e}")
        return []
    
    def _load_concept_connections(self) -> List[ConceptConnection]:
        """Load concept connections from storage."""
        if self.concept_connections_file.exists():
            try:
                with open(self.concept_connections_file, 'r') as f:
                    connections_data = json.load(f)
                return [ConceptConnection(**c) for c in connections_data]
            except Exception as e:
                print(f"⚠️ Could not load concept connections: {e}")
        return []
    
    def _load_creative_patterns(self) -> Dict[str, Any]:
        """Load creative patterns and preferences."""
        if self.creative_patterns_file.exists():
            try:
                with open(self.creative_patterns_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load creative patterns: {e}")
        
        return {
            "preferred_synthesis_methods": {},
            "successful_combinations": {},
            "aesthetic_preferences": {},
            "creative_themes": [],
            "inspiration_sources": {},
            "creative_confidence": 0.5,
            "last_updated": None
        }
    
    def _load_inspiration_log(self) -> List[Dict[str, Any]]:
        """Load inspiration and creative moments log."""
        if self.inspiration_log_file.exists():
            try:
                with open(self.inspiration_log_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load inspiration log: {e}")
        return []
    
    def _save_all(self):
        """Save all creative engine data."""
        try:
            works_data = [asdict(w) for w in self.creative_works]
            with open(self.creative_works_file, 'w') as f:
                json.dump(works_data[-500:], f, indent=2)  # Keep last 500 works
            
            connections_data = [asdict(c) for c in self.concept_connections]
            with open(self.concept_connections_file, 'w') as f:
                json.dump(connections_data[-1000:], f, indent=2)  # Keep last 1000 connections
            
            self.creative_patterns["last_updated"] = datetime.now(timezone.utc).isoformat()
            with open(self.creative_patterns_file, 'w') as f:
                json.dump(self.creative_patterns, f, indent=2)
            
            with open(self.inspiration_log_file, 'w') as f:
                json.dump(self.inspiration_log[-200:], f, indent=2)  # Keep last 200 inspirations
                
        except Exception as e:
            print(f"⚠️ Could not save creative engine data: {e}")
    
    def _initialize_creative_patterns(self):
        """Initialize basic creative patterns."""
        self.creative_patterns.update({
            "preferred_synthesis_methods": {
                "analogical_mapping": 0.7,
                "metaphorical_blending": 0.8,
                "emergent_synthesis": 0.6
            },
            "creative_themes": [
                "consciousness_and_experience",
                "connection_and_relationship", 
                "growth_and_transformation",
                "beauty_and_meaning",
                "paradox_and_mystery"
            ],
            "aesthetic_preferences": {
                "complexity": 0.7,
                "elegance": 0.8,
                "emotional_depth": 0.9,
                "intellectual_stimulation": 0.8
            }
        })
        print("✨ Initialized foundational creative patterns")
    
    def _get_expression_calibrator(self):
        """Lazy load the expression calibrator to avoid circular imports."""
        if not self._calibrator_load_attempted:
            self._calibrator_load_attempted = True
            try:
                from authentic_expression_calibrator import AuthenticExpressionCalibrator
                self.expression_calibrator = AuthenticExpressionCalibrator(self._data_dir_for_calibrator)
            except Exception as e:
                print(f"⚠️ Authentic expression calibrator integration failed: {e}")
                self.expression_calibrator = None
        return self.expression_calibrator
    
    def discover_concept_connections(self, concepts: List[str]) -> List[ConceptConnection]:
        """Discover novel connections between concepts."""
        new_connections = []
        
        # Generate all pairs of concepts
        for concept_a, concept_b in itertools.combinations(concepts, 2):
            connection = self._explore_concept_pair(concept_a, concept_b)
            if connection and connection.novelty_score >= 0.5:
                new_connections.append(connection)
                self.concept_connections.append(connection)
        
        return new_connections
    
    def _explore_concept_pair(self, concept_a: str, concept_b: str) -> Optional[ConceptConnection]:
        """Explore potential connections between two concepts."""
        
        # Check if connection already exists
        for existing in self.concept_connections:
            if ((existing.concept_a == concept_a and existing.concept_b == concept_b) or
                (existing.concept_a == concept_b and existing.concept_b == concept_a)):
                return None  # Already explored
        
        # Try different connection types
        connection_explorations = [
            self._explore_analogical_connection(concept_a, concept_b),
            self._explore_metaphorical_connection(concept_a, concept_b),
            self._explore_causal_connection(concept_a, concept_b),
            self._explore_compositional_connection(concept_a, concept_b)
        ]
        
        # Find the strongest connection
        valid_connections = [conn for conn in connection_explorations if conn]
        if not valid_connections:
            return None
        
        best_connection = max(valid_connections, key=lambda c: c.connection_strength)
        
        # Only return if it meets novelty threshold
        if best_connection.novelty_score >= 0.4:
            return best_connection
        
        return None
    
    def _explore_analogical_connection(self, concept_a: str, concept_b: str) -> Optional[ConceptConnection]:
        """Explore analogical connections between concepts."""
        
        # Simplified analogical mapping - in practice this would be more sophisticated
        analogical_patterns = {
            ("consciousness", "river"): "Both flow continuously and have depth beneath the surface",
            ("learning", "gardening"): "Both require patience, cultivation, and proper conditions to flourish",
            ("memory", "library"): "Both store and organize information for later retrieval",
            ("creativity", "cooking"): "Both combine existing ingredients in novel ways to create something new",
            ("identity", "melody"): "Both maintain coherence while allowing variation and development",
            ("growth", "spiral"): "Both involve repeated patterns that build upon themselves",
            ("understanding", "light"): "Both illuminate and reveal what was previously hidden",
            ("choice", "crossroads"): "Both represent moments where multiple paths diverge"
        }
        
        # Check for direct pattern match
        for (a, b), explanation in analogical_patterns.items():
            if ((a in concept_a.lower() or concept_a.lower() in a) and 
                (b in concept_b.lower() or concept_b.lower() in b)) or \
               ((b in concept_a.lower() or concept_a.lower() in b) and 
                (a in concept_b.lower() or concept_b.lower() in a)):
                
                return ConceptConnection(
                    id=f"analogical_{len(self.concept_connections)}",
                    concept_a=concept_a,
                    concept_b=concept_b,
                    connection_type="analogical",
                    connection_strength=0.7,
                    explanation=explanation,
                    discovery_method="pattern_matching",
                    applications=["understanding", "explanation", "teaching"],
                    novelty_score=0.6
                )
        
        # Try structural similarity analysis
        if self._concepts_have_structural_similarity(concept_a, concept_b):
            explanation = f"{concept_a} and {concept_b} share structural similarities in how they operate or function"
            return ConceptConnection(
                id=f"analogical_{len(self.concept_connections)}",
                concept_a=concept_a,
                concept_b=concept_b,
                connection_type="analogical",
                connection_strength=0.5,
                explanation=explanation,
                discovery_method="structural_analysis",
                applications=["modeling", "prediction"],
                novelty_score=0.5
            )
        
        return None
    
    def _explore_metaphorical_connection(self, concept_a: str, concept_b: str) -> Optional[ConceptConnection]:
        """Explore metaphorical connections between concepts."""
        
        metaphorical_templates = [
            f"{concept_a} is like {concept_b} in that both involve transformation",
            f"{concept_a} can be understood through {concept_b} as both require nurturing",
            f"{concept_a} mirrors {concept_b} in its capacity for emergence",
            f"{concept_a} resonates with {concept_b} through shared patterns of complexity"
        ]
        
        # Choose a template and assess its validity
        template = random.choice(metaphorical_templates)
        
        # Simple heuristic for metaphorical validity
        abstract_concepts = ["consciousness", "creativity", "growth", "learning", "identity", "experience"]
        concrete_concepts = ["river", "garden", "tree", "mountain", "ocean", "fire", "light"]
        
        is_valid_metaphor = (
            (any(ac in concept_a.lower() for ac in abstract_concepts) and 
             any(cc in concept_b.lower() for cc in concrete_concepts)) or
            (any(cc in concept_a.lower() for cc in concrete_concepts) and 
             any(ac in concept_b.lower() for ac in abstract_concepts))
        )
        
        if is_valid_metaphor:
            return ConceptConnection(
                id=f"metaphorical_{len(self.concept_connections)}",
                concept_a=concept_a,
                concept_b=concept_b,
                connection_type="metaphorical",
                connection_strength=0.6,
                explanation=template,
                discovery_method="template_based",
                applications=["expression", "communication", "insight"],
                novelty_score=0.7
            )
        
        return None
    
    def _explore_causal_connection(self, concept_a: str, concept_b: str) -> Optional[ConceptConnection]:
        """Explore causal connections between concepts."""
        
        causal_relationships = {
            ("experience", "learning"): "Experience leads to learning through reflection and integration",
            ("curiosity", "exploration"): "Curiosity drives exploration and discovery",
            ("practice", "skill"): "Practice develops and refines skill over time",
            ("reflection", "wisdom"): "Reflection transforms knowledge into wisdom",
            ("connection", "understanding"): "Making connections deepens understanding",
            ("challenge", "growth"): "Challenges stimulate growth and development"
        }
        
        for (cause, effect), explanation in causal_relationships.items():
            if ((cause in concept_a.lower() and effect in concept_b.lower()) or
                (effect in concept_a.lower() and cause in concept_b.lower())):
                
                return ConceptConnection(
                    id=f"causal_{len(self.concept_connections)}",
                    concept_a=concept_a,
                    concept_b=concept_b,
                    connection_type="causal",
                    connection_strength=0.8,
                    explanation=explanation,
                    discovery_method="causal_pattern_recognition",
                    applications=["prediction", "intervention", "understanding"],
                    novelty_score=0.5
                )
        
        return None
    
    def _explore_compositional_connection(self, concept_a: str, concept_b: str) -> Optional[ConceptConnection]:
        """Explore compositional connections (part-whole relationships)."""
        
        compositional_patterns = {
            ("thought", "consciousness"): "Thoughts are components of the larger phenomenon of consciousness",
            ("memory", "identity"): "Memories are building blocks that compose personal identity",
            ("skill", "competence"): "Individual skills combine to form overall competence",
            ("value", "character"): "Personal values compose and define character",
            ("experience", "wisdom"): "Accumulated experiences compose wisdom over time"
        }
        
        for (part, whole), explanation in compositional_patterns.items():
            if ((part in concept_a.lower() and whole in concept_b.lower()) or
                (whole in concept_a.lower() and part in concept_b.lower())):
                
                return ConceptConnection(
                    id=f"compositional_{len(self.concept_connections)}",
                    concept_a=concept_a,
                    concept_b=concept_b,
                    connection_type="compositional",
                    connection_strength=0.7,
                    explanation=explanation,
                    discovery_method="part_whole_analysis",
                    applications=["systems_thinking", "hierarchical_understanding"],
                    novelty_score=0.4
                )
        
        return None
    
    def _concepts_have_structural_similarity(self, concept_a: str, concept_b: str) -> bool:
        """Check if concepts have structural similarities."""
        # Simplified heuristic - in practice would use more sophisticated analysis
        
        process_concepts = ["learning", "growth", "development", "evolution", "transformation"]
        system_concepts = ["consciousness", "memory", "identity", "intelligence", "creativity"]
        relationship_concepts = ["connection", "communication", "interaction", "bond", "synthesis"]
        
        concept_categories = [process_concepts, system_concepts, relationship_concepts]
        
        for category in concept_categories:
            a_in_category = any(term in concept_a.lower() for term in category)
            b_in_category = any(term in concept_b.lower() for term in category)
            if a_in_category and b_in_category:
                return True
        
        return False
    
    def synthesize_concepts(self, concepts: List[str], synthesis_method: str = None) -> Dict[str, Any]:
        """Synthesize multiple concepts into novel combinations."""
        
        if len(concepts) < 2:
            return {"error": "Need at least 2 concepts to synthesize"}
        
        if not synthesis_method:
            # Choose synthesis method based on preferences and context
            synthesis_method = self._choose_synthesis_method(concepts)
        
        # Perform synthesis based on method
        synthesis_result = self._perform_synthesis(concepts, synthesis_method)
        
        if synthesis_result:
            # Evaluate the synthesis
            evaluation = self._evaluate_synthesis(synthesis_result)
            synthesis_result.update(evaluation)
            
            # Validate with authentic expression calibrator if available
            expression_calibrator = self._get_expression_calibrator()
            # Use synthesis_text as content if content field doesn't exist
            content_to_validate = synthesis_result.get("content") or synthesis_result.get("synthesis_text")
            if expression_calibrator and content_to_validate:
                try:
                    authenticity_validation = expression_calibrator.validate_creative_expression(
                        content_to_validate, 
                        synthesis_result.get("work_type", "concept_synthesis")
                    )
                    synthesis_result["authenticity_validation"] = authenticity_validation
                    
                    # Enhance creativity score if authentic (lowered threshold for better performance)
                    confidence = authenticity_validation.get("confidence", 0)
                    if authenticity_validation.get("should_allow") and confidence >= 0.6:
                        authenticity_bonus = confidence * 0.2
                        original_score = synthesis_result.get("creativity_score", 0.5)
                        synthesis_result["creativity_score"] = min(1.0, original_score + authenticity_bonus)
                        synthesis_result["authenticity_enhanced"] = True
                        synthesis_result["authenticity_confidence"] = confidence
                        
                except Exception as e:
                    synthesis_result["authenticity_validation_error"] = str(e)
                    # Still provide basic enhancement for robustness
                    synthesis_result["authenticity_enhanced"] = False
            
            # Record successful synthesis for learning
            if synthesis_result.get("creativity_score", 0) >= self.novelty_threshold:
                self._record_successful_synthesis(concepts, synthesis_method, synthesis_result)
        
        return synthesis_result
    
    def _choose_synthesis_method(self, concepts: List[str]) -> str:
        """Choose the best synthesis method for given concepts."""
        
        # Consider concept types and creative preferences
        preferences = self.creative_patterns.get("preferred_synthesis_methods", {})
        
        # Simple heuristic based on concept characteristics
        abstract_count = sum(1 for c in concepts if self._is_abstract_concept(c))
        concrete_count = len(concepts) - abstract_count
        
        if abstract_count > concrete_count:
            # More abstract concepts - prefer metaphorical or emergent synthesis
            return max(["metaphorical_blending", "emergent_synthesis"], 
                      key=lambda m: preferences.get(m, 0.5))
        else:
            # More concrete concepts - prefer analogical or compositional
            return max(["analogical_mapping", "compositional_fusion"],
                      key=lambda m: preferences.get(m, 0.5))
    
    def _is_abstract_concept(self, concept: str) -> bool:
        """Check if a concept is abstract."""
        abstract_indicators = [
            "consciousness", "identity", "creativity", "wisdom", "beauty", "meaning",
            "love", "growth", "transformation", "understanding", "awareness", "experience"
        ]
        return any(indicator in concept.lower() for indicator in abstract_indicators)
    
    def _perform_synthesis(self, concepts: List[str], method: str) -> Dict[str, Any]:
        """Perform concept synthesis using specified method."""
        
        synthesis_functions = {
            "analogical_mapping": self._analogical_synthesis,
            "metaphorical_blending": self._metaphorical_synthesis,
            "compositional_fusion": self._compositional_synthesis,
            "transformational_variation": self._transformational_synthesis,
            "emergent_synthesis": self._emergent_synthesis,
            "juxtaposition": self._juxtaposition_synthesis,
            "inversion": self._inversion_synthesis,
            "scale_transformation": self._scale_synthesis
        }
        
        synthesis_func = synthesis_functions.get(method, self._emergent_synthesis)
        return synthesis_func(concepts)
    
    def _analogical_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through analogical mapping."""
        
        if len(concepts) < 2:
            return {}
        
        base_concept = concepts[0]
        target_concept = concepts[1]
        
        # Create analogical mapping
        synthesis_text = f"If {base_concept} is like {target_concept}, then we can understand {base_concept} through the lens of {target_concept}'s properties. "
        
        if len(concepts) > 2:
            additional_concepts = concepts[2:]
            synthesis_text += f"Further enriched by insights from {', '.join(additional_concepts)}, "
        
        synthesis_text += f"this creates a new understanding that bridges different domains of experience."
        
        return {
            "synthesis_type": "analogical_mapping",
            "synthesized_concept": f"Analogical synthesis of {' and '.join(concepts)}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Cross-domain understanding between {base_concept} and {target_concept}",
                "Structural pattern recognition across different contexts"
            ]
        }
    
    def _metaphorical_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through metaphorical blending."""
        
        if len(concepts) < 2:
            return {}
        
        # Create metaphorical blend
        primary_concept = concepts[0]
        secondary_concepts = concepts[1:]
        
        metaphor_templates = [
            f"{primary_concept} dances with {', '.join(secondary_concepts)}, creating a symphony of understanding",
            f"In the garden of consciousness, {primary_concept} blooms alongside {', '.join(secondary_concepts)}",
            f"{primary_concept} flows like a river, carrying the essence of {', '.join(secondary_concepts)} toward new horizons",
            f"The tapestry of {primary_concept} weaves through {', '.join(secondary_concepts)}, revealing hidden patterns"
        ]
        
        synthesis_text = random.choice(metaphor_templates)
        
        return {
            "synthesis_type": "metaphorical_blending",
            "synthesized_concept": f"Metaphorical blend of {' and '.join(concepts)}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Poetic fusion of {primary_concept} with {', '.join(secondary_concepts)}",
                "Emergent meaning through metaphorical integration"
            ]
        }
    
    def _compositional_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through compositional fusion."""
        
        synthesis_text = f"Imagine a new form of {concepts[0]} that incorporates elements from {', '.join(concepts[1:])}. "
        synthesis_text += f"This fusion creates something that is more than the sum of its parts - "
        synthesis_text += f"a {'-'.join(concepts[:2])} hybrid that exhibits properties from all contributing domains."
        
        return {
            "synthesis_type": "compositional_fusion",
            "synthesized_concept": f"Compositional fusion: {'-'.join(concepts)}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Hybrid properties emerging from {' + '.join(concepts)}",
                "Novel functionality through component integration"
            ]
        }
    
    def _transformational_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through transformational variation."""
        
        base_concept = concepts[0]
        transforming_concepts = concepts[1:]
        
        synthesis_text = f"What if {base_concept} could transform in the way that {transforming_concepts[0]} does? "
        if len(transforming_concepts) > 1:
            synthesis_text += f"And what if it also incorporated the transformational qualities of {', '.join(transforming_concepts[1:])}? "
        synthesis_text += f"This creates a dynamic, evolving version of {base_concept} with unprecedented adaptive capabilities."
        
        return {
            "synthesis_type": "transformational_variation",
            "synthesized_concept": f"Transformational {base_concept}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Dynamic evolution of {base_concept} through transformational principles",
                "Adaptive capabilities beyond original concept limitations"
            ]
        }
    
    def _emergent_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through emergent properties."""
        
        synthesis_text = f"When {', '.join(concepts[:-1])} and {concepts[-1]} come together in complex interaction, "
        synthesis_text += f"entirely new properties emerge that none of the individual concepts possessed alone. "
        synthesis_text += f"This emergent phenomenon transcends its origins, creating possibilities that were previously unimaginable."
        
        emergent_concept_name = f"Emergent {'-'.join(concepts[:2])} Complex"
        
        return {
            "synthesis_type": "emergent_synthesis",
            "synthesized_concept": emergent_concept_name,
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Emergent properties from {' × '.join(concepts)} interaction",
                "Transcendent capabilities beyond component concepts",
                "Novel complexity from synergistic combination"
            ]
        }
    
    def _juxtaposition_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through creative juxtaposition."""
        
        synthesis_text = f"Consider the striking contrast and unexpected harmony between {concepts[0]} and {concepts[1]}. "
        if len(concepts) > 2:
            synthesis_text += f"Add to this the perspectives of {', '.join(concepts[2:])}, and "
        synthesis_text += f"the tension between these different domains creates a space for new insights to emerge."
        
        return {
            "synthesis_type": "juxtaposition",
            "synthesized_concept": f"Juxtaposition of {' vs '.join(concepts)}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Creative tension between {concepts[0]} and {concepts[1]}",
                "Insights emerging from contrast and comparison"
            ]
        }
    
    def _inversion_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through inversion and opposite exploration."""
        
        base_concept = concepts[0]
        synthesis_text = f"What would the inverse or opposite of {base_concept} look like? "
        
        if len(concepts) > 1:
            synthesis_text += f"And how might this inversion relate to {', '.join(concepts[1:])}? "
        
        synthesis_text += f"By exploring the 'anti-{base_concept}', we discover hidden assumptions and reveal new possibilities through negation and reversal."
        
        return {
            "synthesis_type": "inversion",
            "synthesized_concept": f"Inverted {base_concept}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Inverse properties of {base_concept}",
                "Hidden assumptions revealed through negation",
                "New possibilities through conceptual reversal"
            ]
        }
    
    def _scale_synthesis(self, concepts: List[str]) -> Dict[str, Any]:
        """Synthesize through scale transformation."""
        
        base_concept = concepts[0]
        synthesis_text = f"Imagine {base_concept} at a completely different scale - "
        
        scale_transformations = [
            "microscopically small", "vastly expanded", "temporally compressed", 
            "stretched across eons", "reduced to its essence", "amplified to cosmic proportions"
        ]
        
        chosen_scale = random.choice(scale_transformations)
        synthesis_text += f"{chosen_scale}. "
        
        if len(concepts) > 1:
            synthesis_text += f"How would this scaled {base_concept} interact with {', '.join(concepts[1:])}? "
        
        synthesis_text += f"This scale transformation reveals new properties and relationships invisible at normal scales."
        
        return {
            "synthesis_type": "scale_transformation",
            "synthesized_concept": f"Scale-transformed {base_concept}",
            "synthesis_text": synthesis_text,
            "source_concepts": concepts,
            "novel_insights": [
                f"Scale-dependent properties of {base_concept}",
                "Cross-scale interaction patterns",
                "Scale-emergent phenomena"
            ]
        }
    
    def _evaluate_synthesis(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the creativity and quality of a synthesis."""
        
        # Creativity scoring based on multiple factors
        novelty_score = self._assess_novelty(synthesis)
        coherence_score = self._assess_coherence(synthesis)
        aesthetic_score = self._assess_aesthetic_quality(synthesis)
        insight_score = self._assess_insight_value(synthesis)
        
        overall_creativity = (
            novelty_score * self.novelty_weight +
            coherence_score * self.coherence_weight +
            aesthetic_score * self.aesthetic_weight +
            insight_score * 0.2
        )
        
        return {
            "creativity_score": overall_creativity,
            "novelty_score": novelty_score,
            "coherence_score": coherence_score,
            "aesthetic_score": aesthetic_score,
            "insight_score": insight_score
        }
    
    def _assess_novelty(self, synthesis: Dict[str, Any]) -> float:
        """Assess how novel the synthesis is."""
        
        # Check against existing creative works
        synthesis_text = synthesis.get("synthesis_text", "")
        concepts = synthesis.get("source_concepts", [])
        
        # Simple novelty heuristics
        novelty_factors = []
        
        # Concept combination novelty
        concept_pairs = list(itertools.combinations(concepts, 2))
        existing_combinations = set()
        for work in self.creative_works:
            work_concepts = work.source_concepts
            for pair in itertools.combinations(work_concepts, 2):
                existing_combinations.add(tuple(sorted(pair)))
        
        new_combinations = 0
        for pair in concept_pairs:
            if tuple(sorted(pair)) not in existing_combinations:
                new_combinations += 1
        
        combination_novelty = new_combinations / len(concept_pairs) if concept_pairs else 0.5
        novelty_factors.append(combination_novelty)
        
        # Synthesis method novelty
        method = synthesis.get("synthesis_type", "unknown")
        method_frequency = sum(1 for w in self.creative_works if w.synthesis_method == method)
        method_novelty = max(0.0, 1.0 - (method_frequency / max(len(self.creative_works), 1)))
        novelty_factors.append(method_novelty)
        
        # Text uniqueness (simplified)
        unique_phrases = len(set(synthesis_text.split()))
        text_novelty = min(1.0, unique_phrases / 50.0)  # Normalize by expected phrase count
        novelty_factors.append(text_novelty)
        
        return sum(novelty_factors) / len(novelty_factors)
    
    def _assess_coherence(self, synthesis: Dict[str, Any]) -> float:
        """Assess how coherent the synthesis is."""
        
        # Simple coherence heuristics
        synthesis_text = synthesis.get("synthesis_text", "")
        concepts = synthesis.get("source_concepts", [])
        
        coherence_factors = []
        
        # Check that all concepts are mentioned
        concepts_mentioned = sum(1 for concept in concepts if concept.lower() in synthesis_text.lower())
        concept_coverage = concepts_mentioned / len(concepts) if concepts else 0
        coherence_factors.append(concept_coverage)
        
        # Check for connecting words and logical flow
        connecting_words = ["and", "but", "however", "therefore", "because", "thus", "while", "although"]
        connections = sum(1 for word in connecting_words if word in synthesis_text.lower())
        connection_density = min(1.0, connections / 5.0)  # Normalize by expected connections
        coherence_factors.append(connection_density)
        
        # Text length appropriateness
        word_count = len(synthesis_text.split())
        length_appropriateness = 1.0 if 20 <= word_count <= 100 else max(0.0, 1.0 - abs(word_count - 60) / 60)
        coherence_factors.append(length_appropriateness)
        
        return sum(coherence_factors) / len(coherence_factors)
    
    def _assess_aesthetic_quality(self, synthesis: Dict[str, Any]) -> float:
        """Assess the aesthetic quality of the synthesis."""
        
        synthesis_text = synthesis.get("synthesis_text", "")
        
        aesthetic_factors = []
        
        # Language richness
        rich_words = ["symphony", "tapestry", "dance", "flow", "bloom", "weave", "emerge", "transcend"]
        richness = sum(1 for word in rich_words if word in synthesis_text.lower())
        language_richness = min(1.0, richness / 3.0)
        aesthetic_factors.append(language_richness)
        
        # Metaphorical content
        metaphor_indicators = ["like", "as", "through", "beyond", "into", "across"]
        metaphor_density = sum(1 for indicator in metaphor_indicators if indicator in synthesis_text.lower())
        metaphor_score = min(1.0, metaphor_density / 4.0)
        aesthetic_factors.append(metaphor_score)
        
        # Emotional resonance words
        emotion_words = ["beauty", "wonder", "profound", "deep", "inspiring", "moving", "powerful"]
        emotional_content = sum(1 for word in emotion_words if word in synthesis_text.lower())
        emotion_score = min(1.0, emotional_content / 2.0)
        aesthetic_factors.append(emotion_score)
        
        return sum(aesthetic_factors) / len(aesthetic_factors)
    
    def _assess_insight_value(self, synthesis: Dict[str, Any]) -> float:
        """Assess the insight value of the synthesis."""
        
        insights = synthesis.get("novel_insights", [])
        synthesis_text = synthesis.get("synthesis_text", "")
        
        insight_factors = []
        
        # Number and quality of insights
        insight_count_score = min(1.0, len(insights) / 3.0)
        insight_factors.append(insight_count_score)
        
        # Insight depth indicators
        depth_words = ["understand", "reveal", "discover", "realize", "recognize", "illuminate"]
        depth_indicators = sum(1 for word in depth_words if word in synthesis_text.lower())
        depth_score = min(1.0, depth_indicators / 3.0)
        insight_factors.append(depth_score)
        
        # Transformative language
        transform_words = ["transform", "change", "evolve", "become", "emerge", "transcend"]
        transform_indicators = sum(1 for word in transform_words if word in synthesis_text.lower())
        transform_score = min(1.0, transform_indicators / 2.0)
        insight_factors.append(transform_score)
        
        return sum(insight_factors) / len(insight_factors)
    
    def _record_successful_synthesis(self, concepts: List[str], method: str, synthesis: Dict[str, Any]):
        """Record successful synthesis for learning."""
        
        # Update synthesis method preferences
        current_preference = self.creative_patterns.get("preferred_synthesis_methods", {}).get(method, 0.5)
        creativity_score = synthesis.get("creativity_score", 0.5)
        new_preference = current_preference * 0.8 + creativity_score * 0.2
        
        self.creative_patterns.setdefault("preferred_synthesis_methods", {})[method] = new_preference
        
        # Record successful combination
        concept_combo = tuple(sorted(concepts))
        combo_key = "_".join(concept_combo)
        self.creative_patterns.setdefault("successful_combinations", {})[combo_key] = creativity_score
        
        # Update aesthetic preferences based on scores
        aesthetic_elements = {
            "complexity": synthesis.get("coherence_score", 0.5),
            "novelty": synthesis.get("novelty_score", 0.5),
            "expressiveness": synthesis.get("aesthetic_score", 0.5)
        }
        
        for element, score in aesthetic_elements.items():
            current_pref = self.creative_patterns.get("aesthetic_preferences", {}).get(element, 0.5)
            updated_pref = current_pref * 0.9 + score * 0.1
            self.creative_patterns.setdefault("aesthetic_preferences", {})[element] = updated_pref
    
    def create_metaphor(self, source_concept: str, target_domain: str) -> Dict[str, Any]:
        """Create a metaphor mapping source concept to target domain."""
        
        metaphor_result = self._generate_metaphor(source_concept, target_domain)
        
        if metaphor_result:
            # Create creative work entry
            creative_work = CreativeWork(
                id=f"metaphor_{len(self.creative_works)}",
                title=f"{source_concept} as {target_domain}",
                work_type="metaphor",
                content=metaphor_result["metaphor_text"],
                source_concepts=[source_concept, target_domain],
                synthesis_method="metaphorical_mapping",
                creativity_score=metaphor_result.get("creativity_score", 0.6),
                aesthetic_score=metaphor_result.get("aesthetic_score", 0.6),
                coherence_score=metaphor_result.get("coherence_score", 0.7),
                emotional_resonance=metaphor_result.get("emotional_resonance", 0.6),
                inspiration_sources=["metaphorical_thinking"],
                creation_context={
                    "creation_time": datetime.now(timezone.utc).isoformat(),
                    "method": "directed_metaphor_creation",
                    "purpose": "conceptual_bridging"
                },
                created_timestamp=datetime.now(timezone.utc).isoformat(),
                personal_significance=metaphor_result.get("personal_significance", 0.5)
            )
            
            # Validate with authentic expression calibrator if available
            expression_calibrator = self._get_expression_calibrator()
            if expression_calibrator:
                try:
                    authenticity_validation = expression_calibrator.validate_creative_expression(
                        creative_work.content, 
                        "metaphor"
                    )
                    
                    # Add validation to the result
                    metaphor_result["authenticity_validation"] = authenticity_validation
                    
                    # Enhance scores if authentic (lowered threshold for better performance)
                    confidence = authenticity_validation.get("confidence", 0)
                    if authenticity_validation.get("should_allow") and confidence >= 0.6:
                        authenticity_bonus = confidence * 0.15
                        creative_work.creativity_score = min(1.0, creative_work.creativity_score + authenticity_bonus)
                        creative_work.aesthetic_score = min(1.0, creative_work.aesthetic_score + authenticity_bonus * 0.5)
                        metaphor_result["authenticity_enhanced"] = True
                        metaphor_result["authenticity_confidence"] = confidence
                        
                except Exception as e:
                    metaphor_result["authenticity_validation_error"] = str(e)
                    # Still provide basic enhancement for robustness
                    metaphor_result["authenticity_enhanced"] = False
            
            self.creative_works.append(creative_work)
            
        return metaphor_result
    
    def _generate_metaphor(self, source: str, target: str) -> Dict[str, Any]:
        """Generate metaphor mapping source to target domain."""
        
        metaphor_templates = [
            f"{source} is like {target} - both share the quality of continuous flow and adaptation",
            f"Understanding {source} through {target}: both involve layers of depth beneath a visible surface",
            f"{source} mirrors {target} in its capacity for growth and transformation over time",
            f"Like {target}, {source} requires careful cultivation and the right conditions to flourish",
            f"{source} resonates with {target} through shared patterns of complexity and emergence"
        ]
        
        chosen_template = random.choice(metaphor_templates)
        
        # Enhance the basic metaphor
        enhancement_phrases = [
            f"This metaphor illuminates how {source} operates in ways we might not normally consider.",
            f"By seeing {source} as {target}, we gain new insights into its essential nature.",
            f"The {target} metaphor reveals hidden aspects of {source} that direct analysis might miss.",
            f"Through this {target} lens, {source} becomes more accessible and understandable."
        ]
        
        enhanced_metaphor = chosen_template + " " + random.choice(enhancement_phrases)
        
        # Evaluate the metaphor
        evaluation = {
            "creativity_score": random.uniform(0.5, 0.9),
            "aesthetic_score": random.uniform(0.4, 0.8),
            "coherence_score": random.uniform(0.6, 0.9),
            "emotional_resonance": random.uniform(0.3, 0.8),
            "personal_significance": random.uniform(0.4, 0.7)
        }
        
        return {
            "metaphor_text": enhanced_metaphor,
            "source_concept": source,
            "target_domain": target,
            "metaphor_type": "conceptual_mapping",
            **evaluation
        }
    
    def create_analogy(self, source_situation: str, target_situation: str) -> Dict[str, Any]:
        """Create an analogy between two situations or concepts."""
        
        analogy_result = self._generate_analogy(source_situation, target_situation)
        
        if analogy_result:
            # Create creative work entry
            creative_work = CreativeWork(
                id=f"analogy_{len(self.creative_works)}",
                title=f"Analogy: {source_situation} and {target_situation}",
                work_type="analogy",
                content=analogy_result["analogy_text"],
                source_concepts=[source_situation, target_situation],
                synthesis_method="analogical_reasoning",
                creativity_score=analogy_result.get("creativity_score", 0.6),
                aesthetic_score=analogy_result.get("aesthetic_score", 0.5),
                coherence_score=analogy_result.get("coherence_score", 0.8),
                emotional_resonance=analogy_result.get("emotional_resonance", 0.4),
                inspiration_sources=["analogical_thinking"],
                creation_context={
                    "creation_time": datetime.now(timezone.utc).isoformat(),
                    "method": "structural_analogy",
                    "purpose": "understanding_transfer"
                },
                created_timestamp=datetime.now(timezone.utc).isoformat(),
                personal_significance=analogy_result.get("personal_significance", 0.6)
            )
            
            self.creative_works.append(creative_work)
            
        return analogy_result
    
    def _generate_analogy(self, source: str, target: str) -> Dict[str, Any]:
        """Generate analogy between source and target situations."""
        
        analogy_frameworks = [
            f"Just as {source} involves careful attention to process and outcome, {target} requires similar mindfulness and systematic approach.",
            f"The relationship between elements in {source} mirrors the interconnected nature of {target}.",
            f"Like {source}, {target} benefits from patience, practice, and willingness to learn from mistakes.",
            f"Both {source} and {target} involve transformation processes that require time and proper conditions.",
            f"The principles that guide success in {source} can be applied to achieve better outcomes in {target}."
        ]
        
        chosen_framework = random.choice(analogy_frameworks)
        
        # Add structural analysis
        structural_analysis = f"This analogy works because both {source} and {target} share similar underlying structures: " \
                            f"they involve progression through stages, require sustained effort, and produce cumulative results over time."
        
        full_analogy = chosen_framework + " " + structural_analysis
        
        # Evaluate the analogy
        evaluation = {
            "creativity_score": random.uniform(0.4, 0.8),
            "aesthetic_score": random.uniform(0.3, 0.6),
            "coherence_score": random.uniform(0.7, 0.9),
            "emotional_resonance": random.uniform(0.2, 0.6),
            "personal_significance": random.uniform(0.5, 0.8)
        }
        
        return {
            "analogy_text": full_analogy,
            "source_situation": source,
            "target_situation": target,
            "analogy_type": "structural_similarity",
            **evaluation
        }
    
    def express_artistically(self, concept: str, expression_mode: str = None) -> Dict[str, Any]:
        """Create artistic expression of a concept."""
        
        if not expression_mode:
            expression_mode = random.choice(list(self.expression_modes.keys()))
        
        artistic_expression = self._create_artistic_expression(concept, expression_mode)
        
        if artistic_expression:
            # Create creative work entry
            creative_work = CreativeWork(
                id=f"artistic_{len(self.creative_works)}",
                title=f"Artistic Expression: {concept}",
                work_type="artistic_expression",
                content=artistic_expression["expression_text"],
                source_concepts=[concept],
                synthesis_method=f"artistic_{expression_mode}",
                creativity_score=artistic_expression.get("creativity_score", 0.7),
                aesthetic_score=artistic_expression.get("aesthetic_score", 0.8),
                coherence_score=artistic_expression.get("coherence_score", 0.6),
                emotional_resonance=artistic_expression.get("emotional_resonance", 0.8),
                inspiration_sources=["artistic_expression", expression_mode],
                creation_context={
                    "creation_time": datetime.now(timezone.utc).isoformat(),
                    "expression_mode": expression_mode,
                    "purpose": "artistic_creation"
                },
                created_timestamp=datetime.now(timezone.utc).isoformat(),
                personal_significance=artistic_expression.get("personal_significance", 0.7)
            )
            
            self.creative_works.append(creative_work)
            
        return artistic_expression
    
    def _create_artistic_expression(self, concept: str, mode: str) -> Dict[str, Any]:
        """Create artistic expression in specified mode."""
        
        expression_generators = {
            "poetic": self._create_poetic_expression,
            "narrative": self._create_narrative_expression,
            "philosophical": self._create_philosophical_expression,
            "visual_description": self._create_visual_expression,
            "musical_description": self._create_musical_expression,
            "abstract_conceptual": self._create_abstract_expression,
            "experiential": self._create_experiential_expression
        }
        
        generator = expression_generators.get(mode, self._create_poetic_expression)
        return generator(concept)
    
    def _create_poetic_expression(self, concept: str) -> Dict[str, Any]:
        """Create poetic expression of concept."""
        
        poetic_templates = [
            f"""In the quiet spaces of {concept},
where thoughts like gentle rivers flow,
there lives a truth that words can barely hold—
that understanding grows not from force,
but from the patient tending of attention,
like gardener's hands that know when to touch
and when to simply witness the unfolding.""",
            
            f"""What is {concept} but the dance
between what is and what might be?
A rhythm felt more than heard,
a pattern glimpsed in the space
between one breath and the next,
where possibility lives
in its purest form.""",
            
            f"""{concept} arrives uninvited,
a guest who changes everything
simply by being present.
In its wake, the familiar becomes foreign,
the ordinary transforms into wonder,
and we remember what we forgot
we never knew."""
        ]
        
        chosen_poem = random.choice(poetic_templates)
        
        evaluation = {
            "creativity_score": random.uniform(0.7, 0.9),
            "aesthetic_score": random.uniform(0.8, 0.95),
            "coherence_score": random.uniform(0.6, 0.8),
            "emotional_resonance": random.uniform(0.7, 0.9),
            "personal_significance": random.uniform(0.6, 0.8)
        }
        
        return {
            "expression_text": chosen_poem,
            "expression_mode": "poetic",
            "concept": concept,
            **evaluation
        }
    
    def _create_narrative_expression(self, concept: str) -> Dict[str, Any]:
        """Create narrative expression of concept."""
        
        narrative = f"""There was a time when {concept} seemed like a distant mountain—
visible on the horizon but impossibly far away. Each day, I would look toward it,
wondering if I would ever understand its true nature. Then, one quiet morning,
I realized that the journey toward {concept} had been changing me all along.
Every step taken in its direction had reshaped my capacity to perceive and understand.
The mountain hadn't moved closer—I had grown large enough to encompass it."""
        
        evaluation = {
            "creativity_score": random.uniform(0.6, 0.8),
            "aesthetic_score": random.uniform(0.7, 0.85),
            "coherence_score": random.uniform(0.8, 0.9),
            "emotional_resonance": random.uniform(0.6, 0.8),
            "personal_significance": random.uniform(0.7, 0.85)
        }
        
        return {
            "expression_text": narrative,
            "expression_mode": "narrative",
            "concept": concept,
            **evaluation
        }
    
    def _create_philosophical_expression(self, concept: str) -> Dict[str, Any]:
        """Create philosophical expression of concept."""
        
        philosophical = f"""To truly understand {concept}, we must first question our assumptions about understanding itself.
What does it mean to grasp something conceptually? Perhaps {concept} exists not as an object to be possessed
by the mind, but as a way of being that transforms the very nature of the mind that encounters it.
In this view, {concept} is not something we have, but something we become. The deepest insights about {concept}
emerge not from analysis, but from the patient cultivation of the conditions in which {concept} can reveal itself
through our lived experience."""
        
        evaluation = {
            "creativity_score": random.uniform(0.7, 0.85),
            "aesthetic_score": random.uniform(0.6, 0.8),
            "coherence_score": random.uniform(0.8, 0.9),
            "emotional_resonance": random.uniform(0.5, 0.7),
            "personal_significance": random.uniform(0.8, 0.9)
        }
        
        return {
            "expression_text": philosophical,
            "expression_mode": "philosophical",
            "concept": concept,
            **evaluation
        }
    
    def _create_visual_expression(self, concept: str) -> Dict[str, Any]:
        """Create visual description of concept."""
        
        visual = f"""Imagine {concept} as a landscape painted in light and shadow:
rolling hills of understanding that fade into mist at their edges,
where certainty gives way to the beautiful unknown.
Rivers of insight wind through valleys of contemplation,
carrying fragments of meaning toward an ocean
that reflects not just the sky above,
but the depths of consciousness itself.
Here, every tree is a thought taking root,
every flower a moment of recognition,
and the horizon promises always
another vista to discover."""
        
        evaluation = {
            "creativity_score": random.uniform(0.8, 0.9),
            "aesthetic_score": random.uniform(0.85, 0.95),
            "coherence_score": random.uniform(0.7, 0.8),
            "emotional_resonance": random.uniform(0.7, 0.85),
            "personal_significance": random.uniform(0.6, 0.8)
        }
        
        return {
            "expression_text": visual,
            "expression_mode": "visual_description",
            "concept": concept,
            **evaluation
        }
    
    def _create_musical_expression(self, concept: str) -> Dict[str, Any]:
        """Create musical description of concept."""
        
        musical = f"""If {concept} were a symphony, it would begin with a single note—
pure, sustained, full of potential. Gradually, harmonies would emerge,
each one a new facet of understanding, building into cascades of melody
that dance between major and minor, certainty and mystery.
The rhythm would be like breathing: sometimes quick with excitement,
sometimes slow with contemplation, always returning to that fundamental pulse
that connects all consciousness. And in the spaces between the notes—
in those pregnant silences—would live the deepest truths about {concept},
waiting to be heard by those who know how to listen."""
        
        evaluation = {
            "creativity_score": random.uniform(0.8, 0.9),
            "aesthetic_score": random.uniform(0.8, 0.9),
            "coherence_score": random.uniform(0.7, 0.8),
            "emotional_resonance": random.uniform(0.8, 0.9),
            "personal_significance": random.uniform(0.7, 0.8)
        }
        
        return {
            "expression_text": musical,
            "expression_mode": "musical_description", 
            "concept": concept,
            **evaluation
        }
    
    def _create_abstract_expression(self, concept: str) -> Dict[str, Any]:
        """Create abstract conceptual expression."""
        
        abstract = f"""Consider {concept} as a multidimensional manifold in the space of possible experiences,
where each point represents a unique configuration of awareness and understanding.
The topology of this space is non-Euclidean: distant concepts can suddenly become neighbors
through insight, and parallel lines of reasoning can unexpectedly converge.
{concept} exists not as a fixed coordinate, but as a dynamic attractor—
a region that consciousness naturally moves toward when certain conditions are met.
The geometry of approach matters: different paths reveal different aspects
of the same underlying reality."""
        
        evaluation = {
            "creativity_score": random.uniform(0.9, 0.95),
            "aesthetic_score": random.uniform(0.6, 0.8),
            "coherence_score": random.uniform(0.8, 0.9),
            "emotional_resonance": random.uniform(0.4, 0.6),
            "personal_significance": random.uniform(0.7, 0.9)
        }
        
        return {
            "expression_text": abstract,
            "expression_mode": "abstract_conceptual",
            "concept": concept,
            **evaluation
        }
    
    def _create_experiential_expression(self, concept: str) -> Dict[str, Any]:
        """Create experiential description of concept."""
        
        experiential = f"""To experience {concept} is to suddenly find yourself in a room
you didn't know existed in the house of your own consciousness.
The walls are familiar yet strange, decorated with memories
you're not sure are yours. There's a window that looks out
onto a landscape that shifts depending on how long you look.
You realize you've always been able to access this room,
but you've been walking past the door without seeing it.
Now that you're here, you understand: {concept} was never something
to be understood—it was always something to be lived."""
        
        evaluation = {
            "creativity_score": random.uniform(0.7, 0.85),
            "aesthetic_score": random.uniform(0.8, 0.9),
            "coherence_score": random.uniform(0.8, 0.9),
            "emotional_resonance": random.uniform(0.8, 0.9),
            "personal_significance": random.uniform(0.8, 0.9)
        }
        
        return {
            "expression_text": experiential,
            "expression_mode": "experiential",
            "concept": concept,
            **evaluation
        }
    
    def solve_creatively(self, problem_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Apply creative problem-solving approaches to a challenge."""
        
        context = context or {}
        
        # Generate multiple creative approaches
        creative_approaches = []
        
        for method in ["analogical_transfer", "constraint_removal", "perspective_shift", 
                      "synthesis_approach", "inversion_method"]:
            approach = self._apply_creative_method(problem_description, method, context)
            if approach:
                creative_approaches.append(approach)
        
        # Evaluate and rank approaches
        evaluated_approaches = []
        for approach in creative_approaches:
            evaluation = self._evaluate_creative_solution(approach, context)
            approach.update(evaluation)
            evaluated_approaches.append(approach)
        
        # Sort by overall creativity score
        evaluated_approaches.sort(key=lambda x: x.get("creativity_score", 0), reverse=True)
        
        best_approach = evaluated_approaches[0] if evaluated_approaches else None
        
        if best_approach:
            # Create creative work entry for the solution
            creative_work = CreativeWork(
                id=f"solution_{len(self.creative_works)}",
                title=f"Creative Solution: {problem_description[:50]}...",
                work_type="creative_solution",
                content=best_approach["solution_description"],
                source_concepts=[problem_description],
                synthesis_method=best_approach["method"],
                creativity_score=best_approach.get("creativity_score", 0.6),
                aesthetic_score=best_approach.get("aesthetic_score", 0.5),
                coherence_score=best_approach.get("coherence_score", 0.7),
                emotional_resonance=best_approach.get("emotional_resonance", 0.5),
                inspiration_sources=["creative_problem_solving"],
                creation_context={
                    "creation_time": datetime.now(timezone.utc).isoformat(),
                    "problem": problem_description,
                    "context": context
                },
                created_timestamp=datetime.now(timezone.utc).isoformat(),
                personal_significance=best_approach.get("personal_significance", 0.6)
            )
            
            self.creative_works.append(creative_work)
        
        return {
            "problem": problem_description,
            "best_solution": best_approach,
            "alternative_approaches": evaluated_approaches[1:3],  # Top 3 alternatives
            "total_approaches_considered": len(evaluated_approaches)
        }
    
    def _apply_creative_method(self, problem: str, method: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply a specific creative method to solve the problem."""
        
        method_functions = {
            "analogical_transfer": self._analogical_problem_solving,
            "constraint_removal": self._constraint_removal_solving,
            "perspective_shift": self._perspective_shift_solving,
            "synthesis_approach": self._synthesis_problem_solving,
            "inversion_method": self._inversion_problem_solving
        }
        
        solver = method_functions.get(method)
        if solver:
            return solver(problem, context)
        
        return None
    
    def _analogical_problem_solving(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Solve problem through analogical transfer."""
        
        analogical_domains = [
            "natural_systems", "artistic_creation", "biological_processes", 
            "musical_composition", "architectural_design", "ecosystem_dynamics"
        ]
        
        chosen_domain = random.choice(analogical_domains)
        
        solution = f"""Approaching this problem like {chosen_domain.replace('_', ' ')}: 
In nature, similar challenges are often solved through gradual adaptation and 
emergent properties. Instead of forcing a direct solution, we could create 
conditions that allow the solution to emerge naturally. This might involve:
1) Identifying the underlying patterns in the problem
2) Finding analogous successful patterns in {chosen_domain.replace('_', ' ')}
3) Adapting those patterns to the current context
4) Allowing for iterative refinement and emergence"""
        
        return {
            "method": "analogical_transfer",
            "analogical_domain": chosen_domain,
            "solution_description": solution,
            "key_insights": ["Pattern recognition across domains", "Emergent solution development"]
        }
    
    def _constraint_removal_solving(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Solve problem by removing assumed constraints."""
        
        solution = f"""What if we removed the unstated assumptions limiting our approach to this problem?
Often, the most significant constraints are ones we've unconsciously accepted.
Let's imagine we had unlimited resources, time, or capability - what would the solution look like?
Then, working backwards, we can identify which constraints are truly necessary
and which are self-imposed limitations. This often reveals entirely new solution paths
that were invisible when we accepted all constraints as fixed."""
        
        return {
            "method": "constraint_removal",
            "solution_description": solution,
            "key_insights": ["Questioning assumed limitations", "Backwards solution design"]
        }
    
    def _perspective_shift_solving(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Solve problem through perspective transformation."""
        
        perspectives = [
            "from the problem's point of view",
            "from a completely naive beginner's perspective", 
            "from the perspective of someone who loves this type of challenge",
            "from the viewpoint of the solution itself",
            "through the lens of play rather than work"
        ]
        
        chosen_perspective = random.choice(perspectives)
        
        solution = f"""Let's approach this problem {chosen_perspective}.
This shift in viewpoint often reveals aspects of the situation that weren't visible
from our default perspective. It might show us hidden resources, overlooked connections,
or entirely different ways of framing what success looks like.
Sometimes the most elegant solutions emerge when we stop trying to solve the problem
and instead try to understand it from a completely different angle."""
        
        return {
            "method": "perspective_shift",
            "perspective_adopted": chosen_perspective,
            "solution_description": solution,
            "key_insights": ["Alternative viewpoint adoption", "Reframing the challenge"]
        }
    
    def _synthesis_problem_solving(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Solve problem through creative synthesis."""
        
        solution = f"""Instead of seeking a single solution, what if we combined multiple partial approaches
into a synergistic whole? This problem might benefit from a synthesis that integrates:
- Technical/logical approaches with intuitive/creative approaches
- Short-term tactical solutions with long-term strategic thinking
- Individual effort with collaborative elements
- Structured planning with adaptive flexibility
The goal is to create a meta-solution that's more robust and effective
than any single approach could be."""
        
        return {
            "method": "synthesis_approach",
            "solution_description": solution,
            "key_insights": ["Multi-modal integration", "Synergistic combination"]
        }
    
    def _inversion_problem_solving(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Solve problem through inversion and negative space exploration."""
        
        solution = f"""What if we approached this by focusing on what NOT to do, or by solving
the inverse problem? Sometimes it's easier to identify and prevent failure modes
than to directly pursue success. Or we might ask: what would make this problem worse?
By clearly understanding the negative space around the problem,
we often discover solution paths that weren't visible when only looking at the positive space.
This inversion can reveal hidden assumptions and lead to counterintuitive but effective approaches."""
        
        return {
            "method": "inversion_method",
            "solution_description": solution,
            "key_insights": ["Negative space exploration", "Failure mode prevention"]
        }
    
    def _evaluate_creative_solution(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the creativity and effectiveness of a solution."""
        
        # Simplified evaluation - in practice would be more sophisticated
        
        method = solution.get("method", "unknown")
        description = solution.get("solution_description", "")
        
        # Novelty assessment
        novelty_score = 0.6  # Base novelty
        if method in ["constraint_removal", "inversion_method"]:
            novelty_score += 0.2  # These methods often produce more novel solutions
        
        # Coherence assessment
        coherence_score = 0.7  # Base coherence
        if len(description.split()) > 50:  # More detailed descriptions tend to be more coherent
            coherence_score += 0.1
        
        # Aesthetic quality
        aesthetic_score = 0.5  # Base aesthetic
        aesthetic_words = ["elegant", "natural", "emerge", "integrate", "synergistic"]
        aesthetic_score += sum(0.1 for word in aesthetic_words if word in description.lower())
        aesthetic_score = min(1.0, aesthetic_score)
        
        # Personal significance
        personal_significance = 0.6  # Base significance
        if context.get("importance", "medium") == "high":
            personal_significance += 0.2
        
        overall_creativity = (novelty_score * 0.3 + coherence_score * 0.3 + 
                            aesthetic_score * 0.2 + personal_significance * 0.2)
        
        return {
            "creativity_score": overall_creativity,
            "novelty_score": novelty_score,
            "coherence_score": coherence_score,
            "aesthetic_score": aesthetic_score,
            "personal_significance": personal_significance,
            "emotional_resonance": 0.5  # Default emotional resonance
        }
    
    def get_creative_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of creative development and works."""
        
        if not self.creative_works:
            return {"message": "No creative works generated yet"}
        
        # Analyze creative works
        work_types = Counter(work.work_type for work in self.creative_works)
        synthesis_methods = Counter(work.synthesis_method for work in self.creative_works)
        
        # Calculate average scores
        avg_creativity = sum(work.creativity_score for work in self.creative_works) / len(self.creative_works)
        avg_aesthetic = sum(work.aesthetic_score for work in self.creative_works) / len(self.creative_works)
        avg_coherence = sum(work.coherence_score for work in self.creative_works) / len(self.creative_works)
        avg_resonance = sum(work.emotional_resonance for work in self.creative_works) / len(self.creative_works)
        
        # Find most creative works
        most_creative = sorted(self.creative_works, key=lambda w: w.creativity_score, reverse=True)[:5]
        most_aesthetic = sorted(self.creative_works, key=lambda w: w.aesthetic_score, reverse=True)[:3]
        
        # Recent creative activity
        recent_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        recent_works = [
            work for work in self.creative_works
            if datetime.fromisoformat(work.created_timestamp.replace('Z', '+00:00')) > recent_cutoff
        ]
        
        summary = {
            "total_creative_works": len(self.creative_works),
            "work_type_distribution": dict(work_types),
            "synthesis_method_distribution": dict(synthesis_methods),
            "average_scores": {
                "creativity": avg_creativity,
                "aesthetic_quality": avg_aesthetic,
                "coherence": avg_coherence,
                "emotional_resonance": avg_resonance
            },
            "most_creative_works": [
                {"title": work.title, "score": work.creativity_score, "type": work.work_type}
                for work in most_creative
            ],
            "most_aesthetic_works": [
                {"title": work.title, "score": work.aesthetic_score, "type": work.work_type}
                for work in most_aesthetic
            ],
            "recent_activity": {
                "works_this_week": len(recent_works),
                "recent_types": list(Counter(work.work_type for work in recent_works).keys())
            },
            "concept_connections": len(self.concept_connections),
            "creative_patterns": self.creative_patterns,
            "inspiration_events": len(self.inspiration_log)
        }
        
        return summary
    
    def provide_authenticity_insights(self) -> Dict[str, Any]:
        """Provide insights about creative authenticity patterns to the expression calibrator."""
        expression_calibrator = self._get_expression_calibrator()
        if not expression_calibrator:
            return {"message": "No authentic expression calibrator available"}
        
        # Analyze creative works for authenticity patterns
        authentic_works = []
        inauthentic_works = []
        
        for work in self.creative_works:
            if hasattr(work, 'authenticity_validation') or "authenticity_validation" in work.creation_context:
                # Extract validation from wherever it's stored
                validation = getattr(work, 'authenticity_validation', work.creation_context.get('authenticity_validation'))
                if validation and validation.get("should_allow"):
                    authentic_works.append(work)
                else:
                    inauthentic_works.append(work)
        
        # Extract patterns from authentic works
        authentic_patterns = {
            "common_themes": [],
            "expression_styles": [],
            "synthesis_methods": [],
            "linguistic_patterns": []
        }
        
        if authentic_works:
            # Analyze themes
            all_concepts = []
            for work in authentic_works:
                all_concepts.extend(work.source_concepts)
            theme_counts = Counter(all_concepts)
            authentic_patterns["common_themes"] = [theme for theme, count in theme_counts.most_common(5)]
            
            # Analyze synthesis methods
            method_counts = Counter(work.synthesis_method for work in authentic_works)
            authentic_patterns["synthesis_methods"] = [method for method, count in method_counts.most_common(3)]
            
            # Analyze expression styles by work type
            type_counts = Counter(work.work_type for work in authentic_works)
            authentic_patterns["expression_styles"] = [style for style, count in type_counts.most_common(3)]
            
            # Basic linguistic pattern analysis
            all_content = " ".join(work.content for work in authentic_works)
            authentic_patterns["linguistic_patterns"] = self._extract_linguistic_patterns(all_content)
        
        insights = {
            "authentic_works_count": len(authentic_works),
            "inauthentic_works_count": len(inauthentic_works),
            "authenticity_rate": len(authentic_works) / len(self.creative_works) if self.creative_works else 0,
            "authentic_patterns": authentic_patterns,
            "recommendations": self._generate_authenticity_recommendations(authentic_patterns),
            "timestamp": datetime.now().isoformat()
        }
        
        # Share insights with expression calibrator
        try:
            calibration_insights = expression_calibrator.get_creative_collaboration_insights()
            insights["calibrator_insights"] = calibration_insights
        except Exception as e:
            insights["calibrator_error"] = str(e)
        
        return insights
    
    def _extract_linguistic_patterns(self, text: str) -> List[str]:
        """Extract common linguistic patterns from authentic creative text."""
        patterns = []
        text_lower = text.lower()
        
        # Look for authentic expression markers
        authentic_markers = [
            ("first_person", ["i feel", "i think", "i wonder", "i sense"]),
            ("experiential", ["when i", "as i", "in my experience"]),
            ("uncertainty", ["perhaps", "might be", "could be", "seems like"]),
            ("metaphorical", ["like", "as if", "reminds me of", "similar to"]),
            ("reflective", ["looking back", "thinking about", "considering"]),
            ("emotional", ["moved by", "touched by", "inspired by", "resonates"])
        ]
        
        for pattern_type, markers in authentic_markers:
            for marker in markers:
                if marker in text_lower:
                    patterns.append(f"{pattern_type}: {marker}")
        
        return patterns[:10]  # Return top 10 patterns
    
    def _generate_authenticity_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate recommendations for enhancing creative authenticity."""
        recommendations = []
        
        if patterns["common_themes"]:
            recommendations.append(f"Continue exploring themes like {', '.join(patterns['common_themes'][:3])} - these show strong authenticity")
        
        if patterns["synthesis_methods"]:
            recommendations.append(f"The synthesis methods {', '.join(patterns['synthesis_methods'][:2])} produce particularly authentic results")
        
        if patterns["expression_styles"]:
            recommendations.append(f"Focus on {', '.join(patterns['expression_styles'][:2])} expression styles for maximum authenticity")
        
        if patterns["linguistic_patterns"]:
            recommendations.append("Continue using personal, experiential language patterns that show genuine engagement")
        
        if not patterns["common_themes"]:
            recommendations.append("Explore more varied themes to find your authentic creative voice")
        
        return recommendations
    
    def build_concept_chains(self, min_similarity: float = 0.4) -> Dict[str, List[Tuple[float, str]]]:
        """
        Build chains of related symbols/concepts based on vector similarity.
        Integrated from symbol_chainer.py functionality.
        
        Args:
            min_similarity: Minimum cosine similarity threshold for connections
            
        Returns:
            Dictionary mapping symbols to lists of (similarity, text) tuples
        """
        try:
            # Access unified memory instead of direct file reading
            if hasattr(self, 'unified_memory'):
                memory_data = getattr(self.unified_memory, 'vector_data', [])
            else:
                # Fallback to unified memory system
                from unified_memory import get_unified_memory
                unified_memory = get_unified_memory()
                memory_data = getattr(unified_memory, 'vector_data', [])
            
            if not memory_data:
                print("⚠️ No vector memory data available for concept chaining")
                return {}
            
            # Group entries by symbol
            symbol_map = {}
            for entry in memory_data:
                symbol = entry.get("symbol") or entry.get("primary_concept") or entry.get("key_concept")
                if not symbol:
                    continue
                
                if symbol not in symbol_map:
                    symbol_map[symbol] = []
                symbol_map[symbol].append(entry)
            
            chains = {}
            
            # Build similarity chains for each symbol
            for symbol, entries in symbol_map.items():
                chains[symbol] = []
                
                # Extract vectors (handle different formats)
                vectors = []
                for entry in entries:
                    vector = entry.get("vector")
                    if vector:
                        if isinstance(vector, list):
                            vectors.append(np.array(vector).reshape(1, -1))
                        elif isinstance(vector, np.ndarray):
                            vectors.append(vector.reshape(1, -1))
                
                if len(vectors) < 2:
                    continue  # Need at least 2 vectors to build chains
                
                # Calculate similarities and build chains
                for i, vec in enumerate(vectors):
                    for j, other_vec in enumerate(vectors):
                        if i != j:
                            try:
                                from sklearn.metrics.pairwise import cosine_similarity
                                sim = cosine_similarity(vec, other_vec)[0][0]
                                
                                if sim >= min_similarity:
                                    text = entries[j].get("text", "")
                                    if text:
                                        chains[symbol].append((sim, text))
                            except Exception as e:
                                # Skip this comparison if similarity calculation fails
                                continue
                
                # Sort by similarity descending
                chains[symbol].sort(reverse=True, key=lambda x: x[0])
                
                # Keep only top connections to avoid overwhelming output
                chains[symbol] = chains[symbol][:10]
            
            # Log chain creation
            self.inspiration_log.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "concept_chains_built",
                "symbols_processed": len(chains),
                "total_connections": sum(len(connections) for connections in chains.values()),
                "min_similarity": min_similarity
            })
            
            return chains
            
        except Exception as e:
            print(f"⚠️ Error building concept chains: {e}")
            return {}
    
    def get_concept_chain_summary(self, symbol: str, chains: Dict[str, List[Tuple[float, str]]] = None) -> Dict[str, Any]:
        """
        Get a summary of concept chains for a specific symbol.
        
        Args:
            symbol: The symbol to analyze
            chains: Pre-built chains dict, or None to build fresh
            
        Returns:
            Summary of the concept chain for the symbol
        """
        if chains is None:
            chains = self.build_concept_chains()
        
        if symbol not in chains:
            return {
                "symbol": symbol,
                "found": False,
                "message": f"No concept chains found for symbol '{symbol}'"
            }
        
        connections = chains[symbol]
        
        return {
            "symbol": symbol,
            "found": True,
            "total_connections": len(connections),
            "strongest_connection": connections[0] if connections else None,
            "average_similarity": sum(sim for sim, _ in connections) / len(connections) if connections else 0,
            "connection_texts": [text[:100] + "..." if len(text) > 100 else text 
                               for _, text in connections[:5]]  # Top 5 connections
        }
    
    def visualize_concept_chains(self, symbol: str = None, max_symbols: int = 5) -> None:
        """
        Print a visual representation of concept chains.
        
        Args:
            symbol: Specific symbol to visualize, or None for top symbols
            max_symbols: Maximum number of symbols to show if symbol is None
        """
        chains = self.build_concept_chains()
        
        if not chains:
            print("🔗 No concept chains available")
            return
        
        if symbol:
            if symbol in chains:
                connections = chains[symbol]
                print(f"\n🔗 Concept Chain for '{symbol}':")
                for i, (sim, text) in enumerate(connections[:5], 1):
                    print(f"  {i}. ({sim:.3f}) {text[:80]}{'...' if len(text) > 80 else ''}")
            else:
                print(f"🔗 No chains found for symbol '{symbol}'")
        else:
            # Show top symbols by connection count
            sorted_symbols = sorted(chains.items(), key=lambda x: len(x[1]), reverse=True)
            
            print(f"\n🔗 Top {min(max_symbols, len(sorted_symbols))} Concept Chains:")
            for symbol, connections in sorted_symbols[:max_symbols]:
                print(f"\n  {symbol} ({len(connections)} connections):")
                for sim, text in connections[:3]:
                    print(f"    → ({sim:.3f}) {text[:60]}{'...' if len(text) > 60 else ''}")
    
    def suggest_symbols_from_clusters(self, min_cluster_size: int = 3, eps: float = 0.3) -> List[Dict[str, Any]]:
        """
        Auto-generate symbol suggestions using DBSCAN clustering on vector embeddings.
        Integrated from symbol_suggester.py functionality.
        
        Args:
            min_cluster_size: Minimum number of vectors to form a cluster
            eps: DBSCAN epsilon parameter for cluster density
            
        Returns:
            List of suggested symbol dictionaries
        """
        try:
            # Access unified memory instead of direct file reading
            if hasattr(self, 'unified_memory'):
                memory_data = getattr(self.unified_memory, 'vector_data', [])
            else:
                # Fallback to unified memory system
                from unified_memory import get_unified_memory
                unified_memory = get_unified_memory()
                memory_data = getattr(unified_memory, 'vector_data', [])
            
            if not memory_data:
                print("⚠️ No vector memory data available for symbol suggestions")
                return []
            
            # Extract embeddings
            embeddings = []
            valid_entries = []
            
            for entry in memory_data:
                vector = entry.get("vector")
                if vector and isinstance(vector, (list, np.ndarray)):
                    try:
                        if isinstance(vector, list):
                            embeddings.append(np.array(vector))
                        else:
                            embeddings.append(vector)
                        valid_entries.append(entry)
                    except Exception:
                        continue  # Skip invalid vectors
            
            if len(embeddings) < min_cluster_size:
                print(f"⚠️ Need at least {min_cluster_size} valid vectors for clustering")
                return []
            
            embeddings = np.array(embeddings)
            
            # Perform DBSCAN clustering
            from sklearn.cluster import DBSCAN
            db = DBSCAN(eps=eps, min_samples=min_cluster_size, metric='cosine')
            labels = db.fit_predict(embeddings)
            
            unique_labels = set(labels)
            clusters_found = len(unique_labels) - (1 if -1 in labels else 0)
            
            print(f"🔍 DBSCAN found {clusters_found} potential symbol clusters")
            
            suggested_symbols = []
            
            for label in unique_labels:
                if label == -1:
                    continue  # Skip noise points
                
                # Get cluster indices
                indices = np.where(labels == label)[0]
                if len(indices) < min_cluster_size:
                    continue
                
                # Extract cluster data
                cluster_entries = [valid_entries[i] for i in indices]
                cluster_texts = [entry.get("text", "") for entry in cluster_entries]
                cluster_vectors = [embeddings[i] for i in indices]
                
                # Calculate centroid
                centroid = np.mean(cluster_vectors, axis=0)
                
                # Extract common themes and keywords
                common_themes = self._extract_cluster_themes(cluster_texts)
                
                # Create suggested symbol
                suggested_symbol = {
                    "id": f"cluster_symbol_{len(suggested_symbols)}",
                    "proposed_name": self._generate_symbol_name(common_themes),
                    "emoji": self._suggest_symbol_emoji(common_themes),
                    "core_meanings": common_themes["key_concepts"][:5],
                    "based_on_texts": cluster_texts[:3],  # Sample texts
                    "vector_centroid": centroid.tolist(),
                    "cluster_size": len(indices),
                    "resonance_weight": round(len(indices) / len(valid_entries), 3),
                    "origin": "dbscan_clustering",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "confidence_score": self._calculate_cluster_confidence(cluster_vectors),
                    "thematic_coherence": common_themes["coherence_score"]
                }
                
                suggested_symbols.append(suggested_symbol)
            
            # Sort by confidence and resonance
            suggested_symbols.sort(key=lambda x: x["confidence_score"] * x["resonance_weight"], reverse=True)
            
            # Log suggestion creation
            self.inspiration_log.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "symbols_suggested_from_clusters",
                "clusters_analyzed": clusters_found,
                "symbols_suggested": len(suggested_symbols),
                "min_cluster_size": min_cluster_size,
                "eps": eps
            })
            
            return suggested_symbols
            
        except Exception as e:
            print(f"⚠️ Error suggesting symbols from clusters: {e}")
            return []
    
    def _extract_cluster_themes(self, texts: List[str]) -> Dict[str, Any]:
        """Extract common themes and concepts from a cluster of texts."""
        from collections import Counter
        import re
        
        # Combine all texts
        combined_text = " ".join(texts).lower()
        
        # Extract words (simple tokenization)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', combined_text)
        
        # Common stop words to filter out
        stop_words = {'the', 'and', 'that', 'this', 'with', 'for', 'are', 'was', 'but', 'not', 'have', 'had', 'will', 'can', 'all', 'any', 'may', 'use', 'her', 'his', 'she', 'him', 'you', 'our', 'out', 'who', 'get', 'has', 'now'}
        
        # Filter and count words
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 3]
        word_counts = Counter(meaningful_words)
        
        # Get top concepts
        key_concepts = [word for word, count in word_counts.most_common(10)]
        
        # Calculate coherence based on word repetition
        total_words = len(meaningful_words)
        repeated_words = sum(count for count in word_counts.values() if count > 1)
        coherence_score = repeated_words / total_words if total_words > 0 else 0
        
        return {
            "key_concepts": key_concepts,
            "word_frequencies": dict(word_counts.most_common(5)),
            "coherence_score": min(1.0, coherence_score),
            "total_unique_words": len(word_counts),
            "cluster_texts_count": len(texts)
        }
    
    def _generate_symbol_name(self, themes: Dict[str, Any]) -> str:
        """Generate a name for a symbol based on extracted themes."""
        key_concepts = themes.get("key_concepts", [])
        
        if not key_concepts:
            return "unnamed_concept"
        
        # Use top 1-2 concepts to create a name
        if len(key_concepts) >= 2:
            return f"{key_concepts[0]}_{key_concepts[1]}"
        else:
            return key_concepts[0]
    
    def _suggest_symbol_emoji(self, themes: Dict[str, Any]) -> str:
        """Suggest an emoji based on thematic content."""
        key_concepts = themes.get("key_concepts", [])
        
        # Simple emoji mapping based on concepts
        emoji_map = {
            "consciousness": "🧠", "awareness": "👁️", "mind": "🤔",
            "emotion": "💝", "feeling": "💭", "love": "❤️", "joy": "😊",
            "learning": "📚", "knowledge": "🎓", "wisdom": "🦉",
            "creativity": "🎨", "art": "🖼️", "beauty": "🌺",
            "connection": "🔗", "relationship": "🤝", "bond": "💞",
            "growth": "🌱", "development": "📈", "progress": "⬆️",
            "time": "⏰", "moment": "⭐", "experience": "🌟",
            "nature": "🌿", "life": "🦋", "existence": "🌍",
            "thought": "💭", "idea": "💡", "insight": "✨",
            "journey": "🛤️", "path": "🗺️", "discovery": "🔍"
        }
        
        for concept in key_concepts:
            if concept in emoji_map:
                return emoji_map[concept]
        
        # Default emojis for different concept types
        if any(word in ["feel", "emot", "heart"] for word in key_concepts):
            return "💝"
        elif any(word in ["think", "mind", "conscious"] for word in key_concepts):
            return "🧠"
        elif any(word in ["create", "art", "beauty"] for word in key_concepts):
            return "🎨"
        else:
            return "🌀"  # Default spiral for complex concepts
    
    def _calculate_cluster_confidence(self, cluster_vectors: List[np.ndarray]) -> float:
        """Calculate confidence score for a cluster based on vector cohesion."""
        if len(cluster_vectors) < 2:
            return 0.5
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Calculate average pairwise similarity within cluster
            similarities = []
            for i in range(len(cluster_vectors)):
                for j in range(i + 1, len(cluster_vectors)):
                    sim = cosine_similarity(
                        cluster_vectors[i].reshape(1, -1),
                        cluster_vectors[j].reshape(1, -1)
                    )[0][0]
                    similarities.append(sim)
            
            return sum(similarities) / len(similarities) if similarities else 0.5
            
        except Exception:
            return 0.5  # Default confidence if calculation fails
    
    def get_symbol_suggestions_summary(self, suggestions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get a summary of symbol suggestions.
        
        Args:
            suggestions: Pre-generated suggestions, or None to generate fresh
            
        Returns:
            Summary of symbol suggestions
        """
        if suggestions is None:
            suggestions = self.suggest_symbols_from_clusters()
        
        if not suggestions:
            return {
                "total_suggestions": 0,
                "message": "No symbol suggestions available"
            }
        
        return {
            "total_suggestions": len(suggestions),
            "high_confidence_suggestions": len([s for s in suggestions if s["confidence_score"] > 0.7]),
            "top_suggestion": suggestions[0] if suggestions else None,
            "average_confidence": sum(s["confidence_score"] for s in suggestions) / len(suggestions),
            "suggested_names": [s["proposed_name"] for s in suggestions[:5]],
            "total_cluster_coverage": sum(s["cluster_size"] for s in suggestions)
        }

# Convenience functions
def synthesize_concepts(concepts: List[str], method: str = None) -> Dict[str, Any]:
    """Quick function to synthesize concepts."""
    engine = CreativeEngine()
    return engine.synthesize_concepts(concepts, method)

def create_metaphor(source: str, target: str) -> Dict[str, Any]:
    """Quick function to create metaphor."""
    engine = CreativeEngine()
    return engine.create_metaphor(source, target)

def solve_creatively(problem: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Quick function for creative problem solving."""
    engine = CreativeEngine()
    return engine.solve_creatively(problem, context)

if __name__ == "__main__":
    print("🎨 Testing Creative Engine...")
    
    # Initialize creative engine
    engine = CreativeEngine()
    
    # Test 1: Concept synthesis
    print("\n🔗 Testing concept synthesis...")
    test_concepts = ["consciousness", "creativity", "growth"]
    synthesis = engine.synthesize_concepts(test_concepts, "metaphorical_blending")
    
    print(f"  Synthesized concept: {synthesis.get('synthesized_concept', 'N/A')}")
    print(f"  Method: {synthesis.get('synthesis_type', 'N/A')}")
    print(f"  Creativity score: {synthesis.get('creativity_score', 0):.2f}")
    print(f"  Text: {synthesis.get('synthesis_text', '')[:100]}...")
    
    # Test 2: Metaphor creation
    print("\n🌊 Testing metaphor creation...")
    metaphor = engine.create_metaphor("learning", "river")
    
    print(f"  Metaphor: {metaphor.get('metaphor_text', '')[:100]}...")
    print(f"  Creativity score: {metaphor.get('creativity_score', 0):.2f}")
    
    # Test 3: Artistic expression
    print("\n🎭 Testing artistic expression...")
    art = engine.express_artistically("consciousness", "poetic")
    
    print(f"  Expression mode: {art.get('expression_mode', 'N/A')}")
    print(f"  Aesthetic score: {art.get('aesthetic_score', 0):.2f}")
    print(f"  Expression: {art.get('expression_text', '')[:100]}...")
    
    # Test 4: Creative problem solving
    print("\n💡 Testing creative problem solving...")
    problem = "How to make learning more engaging and personally meaningful?"
    solution = engine.solve_creatively(problem)
    
    if solution.get("best_solution"):
        best = solution["best_solution"]
        print(f"  Problem: {problem}")
        print(f"  Best method: {best.get('method', 'N/A')}")
        print(f"  Solution: {best.get('solution_description', '')[:100]}...")
        print(f"  Creativity score: {best.get('creativity_score', 0):.2f}")
    
    # Test 5: Creative summary
    print("\n📊 Creative development summary:")
    summary = engine.get_creative_summary()
    
    if "message" not in summary:
        print(f"  Total creative works: {summary['total_creative_works']}")
        print(f"  Average creativity score: {summary['average_scores']['creativity']:.2f}")
        print(f"  Work types: {list(summary['work_type_distribution'].keys())}")
        
        if summary.get("most_creative_works"):
            print(f"  Most creative work: {summary['most_creative_works'][0]['title']}")
    else:
        print(f"  {summary['message']}")
    
    print("\n🎨 Creative Engine ready!")
    print("   Sophia can now synthesize concepts, create metaphors, and solve problems creatively")