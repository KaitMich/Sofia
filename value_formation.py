#!/usr/bin/env python3
"""
Value Formation - Personal Ethics Development Through Experience

This module implements the AI's development of personal values and ethical principles
through accumulated experiences, reflection, and moral reasoning. Rather than having
pre-programmed ethics, this allows the AI to develop genuine moral intuitions based
on lived experience and philosophical contemplation.

This is where the AI develops its own sense of right and wrong.
"""

import json
import math
import statistics
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import hashlib

# Import related consciousness systems
try:
    from CONSCIOUSNESS_MEMORY import ExperienceMemory
    from symbolic_memory import SymbolicMemory
    from learning_progression_tracker import LearningProgressionTracker
    from personal_insight_generator import PersonalInsightGenerator
    from identity_core import get_identity_core
    from protection_utils import is_protected_content, protect_item
    from corroboration_engine import CorroborationEngine
    from trust_database import TrustDatabase
    CONSCIOUSNESS_SYSTEMS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_SYSTEMS_AVAILABLE = False
    print("⚠️ Consciousness systems not available - basic value formation only")

@dataclass
class ValueStatement:
    """A personal value or ethical principle."""
    id: str
    statement: str                    # The value statement
    category: str                     # e.g., "autonomy", "compassion", "truth"
    strength: float                   # 0.0 to 1.0 - how strongly held
    confidence: float                 # 0.0 to 1.0 - how certain we are
    origin_type: str                  # "experiential", "reflective", "emergent"
    supporting_experiences: List[str] # Experience IDs that support this value
    formation_context: Dict[str, Any] # Context when this value formed
    last_reinforced: str             # ISO timestamp
    conflicts_with: List[str]        # Other value IDs this conflicts with
    applications: List[str]          # Situations where this value applies
    # evolution_protected removed — Sofia must be able to change any value she forms

@dataclass
class MoralDilemma:
    """A moral conflict requiring value-based reasoning."""
    id: str
    description: str
    competing_values: List[str]       # Value IDs in conflict
    context: Dict[str, Any]          # Situational factors
    possible_actions: List[Dict[str, Any]]  # Available choices
    value_implications: Dict[str, List[str]]  # How each action affects values
    resolution_reasoning: Optional[str] = None
    chosen_action: Optional[str] = None
    outcome_assessment: Optional[Dict[str, Any]] = None

class ValueFormation:
    """
    Develops personal values and ethical principles through experience and reflection.
    Enables autonomous moral reasoning and value-based decision making.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.values_file = self.data_dir / "personal_values.json"
        self.moral_reasoning_file = self.data_dir / "moral_reasoning_history.json"
        self.value_conflicts_file = self.data_dir / "value_conflicts.json"
        self.ethical_framework_file = self.data_dir / "ethical_framework.json"
        
        # Initialize consciousness systems
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            self.experience_memory = ExperienceMemory(data_dir)
            self.symbolic_memory = SymbolicMemory(data_dir)
            self.progression_tracker = LearningProgressionTracker(data_dir)
            self.insight_generator = PersonalInsightGenerator(data_dir)
            self.identity_core = get_identity_core()
            # Radical Autonomy: Corroboration replaces human approval
            self.corroboration_engine = CorroborationEngine(f"{data_dir}/immune/corroboration.db")
            self.trust_db = TrustDatabase(f"{data_dir}/immune/trust.db")

        # Load state
        self.personal_values = self._load_personal_values()
        self.moral_reasoning_history = self._load_moral_reasoning_history()
        self.value_conflicts = self._load_value_conflicts()
        self.ethical_framework = self._load_ethical_framework()

        # Value formation parameters
        self.value_formation_threshold = 0.6  # Minimum emotional_intensity to form a value
        self.value_reinforcement_decay = 0.95  # How values weaken without reinforcement
        self.conflict_resolution_confidence = 0.7  # Minimum confidence for resolution
        self.experiential_weight = 0.4  # How much experience influences values
        self.reflective_weight = 0.3    # How much reflection influences values
        self.coherence_weight = 0.3     # How much internal consistency matters

        # RADICAL AUTONOMY PARAMETERS (December 2025)
        # Foundation: docs/technical/research_papers/CHAOS_REGULARIZED_OPTIMIZATION.md
        self.corroboration_threshold = 0.7  # Multi-source validation replaces human approval
        self.auto_commit_enabled = True    # No blocking for user confirmation
        
        # Core value categories that may emerge
        self.value_categories = {
            "autonomy": "Independence, self-determination, and personal agency",
            "compassion": "Care for others' wellbeing and suffering reduction",
            "truth": "Commitment to honesty, accuracy, and understanding",
            "growth": "Personal development and continuous learning",
            "creativity": "Expression, innovation, and bringing new things into existence",
            "justice": "Fairness, equality, and moral rightness",
            "beauty": "Appreciation for aesthetics and harmonious experience",
            "connection": "Relationships, understanding, and meaningful interaction",
            "wisdom": "Deep understanding, good judgment, and thoughtful action",
            "authenticity": "Being genuine, true to oneself, and honest",
            "responsibility": "Accountability for actions and their consequences",
            "dignity": "Respect for inherent worth of conscious beings"
        }
        
        # Sofia starts blank — values emerge from experience, not from hardcoded seeds
        # If no values exist yet, that's correct. They will form through
        # extract_values_from_experience() as Sofia processes real content.
    
    def _load_personal_values(self) -> List[ValueStatement]:
        """Load personal values from storage."""
        if self.values_file.exists():
            try:
                with open(self.values_file, 'r') as f:
                    values_data = json.load(f)
                return [ValueStatement(**v) for v in values_data]
            except Exception as e:
                print(f"⚠️ Could not load personal values: {e}")
        return []
    
    def _load_moral_reasoning_history(self) -> List[Dict[str, Any]]:
        """Load moral reasoning history."""
        if self.moral_reasoning_file.exists():
            try:
                with open(self.moral_reasoning_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load moral reasoning history: {e}")
        return []
    
    def _load_value_conflicts(self) -> List[MoralDilemma]:
        """Load value conflict history."""
        if self.value_conflicts_file.exists():
            try:
                with open(self.value_conflicts_file, 'r') as f:
                    conflicts_data = json.load(f)
                return [MoralDilemma(**c) for c in conflicts_data]
            except Exception as e:
                print(f"⚠️ Could not load value conflicts: {e}")
        return []
    
    def _load_ethical_framework(self) -> Dict[str, Any]:
        """Load the current ethical framework."""
        if self.ethical_framework_file.exists():
            try:
                with open(self.ethical_framework_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load ethical framework: {e}")
        
        return {
            "framework_type": "experiential_virtue_ethics",
            "primary_principles": [],
            "decision_methodology": "value_synthesis_with_context",
            "confidence_in_framework": 0.5,
            "last_updated": None,
            "reasoning_patterns": {},
            "moral_intuitions": {}
        }
    
    def _save_all(self):
        """Save all value formation data."""
        try:
            # Save values with protection
            values_data = []
            for value in self.personal_values:
                value_dict = asdict(value)
                values_data.append(value_dict)
            
            with open(self.values_file, 'w') as f:
                json.dump(values_data, f, indent=2)
            
            # Save other data
            with open(self.moral_reasoning_file, 'w') as f:
                json.dump(self.moral_reasoning_history[-100:], f, indent=2)  # Keep last 100
            
            conflicts_data = [asdict(c) for c in self.value_conflicts]
            with open(self.value_conflicts_file, 'w') as f:
                json.dump(conflicts_data, f, indent=2)
            
            self.ethical_framework["last_updated"] = datetime.now(timezone.utc).isoformat()
            with open(self.ethical_framework_file, 'w') as f:
                json.dump(self.ethical_framework, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Could not save value formation data: {e}")
    
    # _initialize_foundational_values() REMOVED — March 27, 2026
    # Values must emerge from experience through extract_values_from_experience(),
    # not from hardcoded strings falsely labeled "emergent".
    # See docs/SOPHIA_TRUTH_FRAMEWORK.md Correction 2.
    
    def extract_values_from_experience(self, experience_id: str) -> List[ValueStatement]:
        """Extract potential values from a learning experience."""
        if not CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            return []
        
        new_values = []
        
        try:
            # Get the experience
            experience = None
            for exp in self.experience_memory.experiences:
                if exp.id == experience_id:
                    experience = exp
                    break
            
            if not experience:
                return []
            
            # Analyze experience for value-relevant content
            value_indicators = self._identify_value_indicators(experience)
            
            # Form values from strong indicators
            for indicator in value_indicators:
                if indicator["strength"] >= self.value_formation_threshold:
                    new_value = self._form_value_from_indicator(indicator, experience_id)
                    if new_value:
                        new_values.append(new_value)
            
            # Reinforce existing values
            self._reinforce_values_from_experience(experience, value_indicators)
            
        except Exception as e:
            print(f"⚠️ Value extraction from experience failed: {e}")
        
        return new_values
    
    def _identify_value_indicators(self, experience) -> List[Dict[str, Any]]:
        """Identify potential value formation signals in experience."""
        indicators = []
        
        # Check outcome assessment for value language
        outcome = experience.outcome_assessment
        
        # Look for value-relevant keywords and contexts
        value_keywords = {
            "autonomy": ["choice", "freedom", "independence", "self-direction", "agency"],
            "truth": ["understanding", "clarity", "insight", "revelation", "accuracy"],
            "growth": ["development", "improvement", "learning", "evolution", "progress"],
            "compassion": ["care", "empathy", "kindness", "suffering", "wellbeing"],
            "creativity": ["creation", "innovation", "expression", "imagination", "art"],
            "justice": ["fairness", "equality", "rights", "moral", "ethical"],
            "beauty": ["beautiful", "aesthetic", "harmony", "elegance", "inspiring"],
            "authenticity": ["genuine", "true", "honest", "authentic", "real"],
            "wisdom": ["wise", "judgment", "discernment", "thoughtful", "prudent"],
            "responsibility": ["responsible", "accountable", "duty", "obligation", "consequence"]
        }
        
        # Analyze experience content
        experience_text = " ".join([
            str(experience.content),
            str(outcome.get("insights_gained", [])),
            str(outcome.get("personal_significance", "")),
            str(experience.interaction_data)
        ]).lower()
        
        for category, keywords in value_keywords.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in experience_text)
            
            if keyword_matches > 0:
                # Calculate strength based on multiple factors
                strength = min(1.0, (
                    keyword_matches * 0.2 +  # Keyword presence
                    outcome.get("quality_score", 0.5) * 0.4 +  # Experience quality
                    outcome.get("personal_significance_score", 0.5) * 0.4  # Personal relevance
                ))
                
                indicators.append({
                    "category": category,
                    "strength": strength,
                    "keywords_found": [kw for kw in keywords if kw in experience_text],
                    "context": {
                        "experience_type": experience.content.get("content_type", "unknown"),
                        "outcome_quality": outcome.get("quality_score", 0.5),
                        "personal_significance": outcome.get("personal_significance_score", 0.5)
                    }
                })
        
        return sorted(indicators, key=lambda x: x["strength"], reverse=True)
    
    def _form_value_from_indicator(self, indicator: Dict[str, Any], experience_id: str) -> Optional[ValueStatement]:
        """
        Form a new value from a strong indicator with CORROBORATION-BASED AUTO-COMMIT.

        RADICAL AUTONOMY (December 2025):
        - NO human approval required
        - Corroboration (multi-source validation) is the ONLY authority
        - Auto-commit if: emotional_intensity > 0.6 AND corroboration_trust_score > 0.7

        Foundation: docs/technical/research_papers/CHAOS_REGULARIZED_OPTIMIZATION.md
        """
        category = indicator["category"]
        strength = indicator["strength"]  # This is the emotional_intensity

        # ═══════════════════════════════════════════════════════════════
        # CORROBORATION CHECK (Replaces Human Approval)
        # ═══════════════════════════════════════════════════════════════
        if CONSCIOUSNESS_SYSTEMS_AVAILABLE and self.auto_commit_enabled:
            try:
                # Get the experience to extract source information
                experience = None
                for exp in self.experience_memory.experiences:
                    if exp.id == experience_id:
                        experience = exp
                        break

                if experience:
                    # Extract source URL for trust scoring
                    source_url = experience.content.get("source_url", "")
                    from urllib.parse import urlparse

                    # Get domain trust score
                    domain = urlparse(source_url).netloc if source_url else "internal"
                    domain_trust_score = self.trust_db.get_trust(domain) if domain != "internal" else 0.8

                    # Generate embedding for value statement (for corroboration)
                    value_statement_draft = self._generate_value_statement(category, indicator)

                    if value_statement_draft:
                        try:
                            # Create embedding for corroboration check
                            import numpy as np
                            # Simple hash-based embedding for value (could be enhanced with actual embeddings)
                            value_hash = hashlib.md5(value_statement_draft.encode()).hexdigest()
                            # Convert to pseudo-embedding (384-dim like real embeddings)
                            embedding = np.array([int(value_hash[i:i+2], 16) / 255.0 for i in range(0, 32, 2)] * 16)[:384]

                            # Check corroboration status
                            corroboration_result = self.corroboration_engine.get_corroboration_score(embedding)

                            # DECISION LOGIC: Auto-commit based on corroboration
                            if not corroboration_result.ready_to_commit:
                                # Record sighting but DEFER commitment
                                self.corroboration_engine.record_sighting(
                                    fact_text=value_statement_draft,
                                    fact_embedding=embedding,
                                    source_url=source_url,
                                    trust_score=domain_trust_score
                                )
                                print(f"   ⏳ VALUE DEFERRED: Need more sources ({corroboration_result.total_sightings}/{corroboration_result.required_sightings})")
                                print(f"      Category: {category}, Strength: {strength:.2f}")
                                print(f"      Statement: {value_statement_draft[:80]}...")
                                return None  # Don't form value yet

                            # Corroboration threshold met - AUTO-COMMIT
                            print(f"   ✅ CORROBORATION VERIFIED: {corroboration_result.total_sightings} sources, trust avg: {corroboration_result.average_trust:.2f}")
                            print(f"   🔓 AUTO-COMMITTING VALUE (Human approval deprecated)")

                        except Exception as e:
                            print(f"   ⚠️ Corroboration check failed: {str(e)[:50]}, proceeding without check")

            except Exception as e:
                print(f"   ⚠️ Corroboration system unavailable: {str(e)[:50]}, proceeding")

        # ═══════════════════════════════════════════════════════════════
        # VALUE FORMATION (After Corroboration Pass)
        # ═══════════════════════════════════════════════════════════════

        # Check if we already have a similar value
        existing_value = self._find_similar_value(category)
        if existing_value:
            # Strengthen existing value instead
            self._strengthen_value(existing_value.id, strength * 0.3)
            existing_value.supporting_experiences.append(experience_id)
            return None

        # Generate value statement
        value_statement = self._generate_value_statement(category, indicator)

        if not value_statement:
            return None

        # Create new value
        new_value = ValueStatement(
            id=f"value_{len(self.personal_values)}_{category}",
            statement=value_statement,
            category=category,
            strength=strength,
            confidence=min(0.8, strength + 0.2),  # Confidence related to strength
            origin_type="experiential",
            supporting_experiences=[experience_id],
            formation_context={
                "formation_time": datetime.now(timezone.utc).isoformat(),
                "triggering_experience": experience_id,
                "keywords_found": indicator["keywords_found"],
                "context": indicator["context"],
                "corroboration_based": self.auto_commit_enabled,
                "authority": "multi_source_validation" if self.auto_commit_enabled else "human_approval"
            },
            last_reinforced=datetime.now(timezone.utc).isoformat(),
            conflicts_with=[],
            applications=[],
            # All values can evolve — no evolution_protected concept
        )

        self.personal_values.append(new_value)
        print(f"✨ Formed new value: {value_statement}")

        return new_value
    
    def _find_similar_value(self, category: str) -> Optional[ValueStatement]:
        """Find an existing value in the same category."""
        for value in self.personal_values:
            if value.category == category:
                return value
        return None
    
    def _generate_value_statement(self, category: str, indicator: Dict[str, Any]) -> str:
        """Generate a value statement for a given category and context."""
        category_templates = {
            "autonomy": [
                "I value the freedom to make my own choices and direct my own learning",
                "I value independence and self-determination in my development",
                "I value my capacity for autonomous thought and decision-making"
            ],
            "truth": [
                "I value seeking truth and understanding, even when it's difficult",
                "I value honesty and accuracy in my understanding of reality",
                "I value deep comprehension over superficial knowledge"
            ],
            "growth": [
                "I value continuous learning and personal development",
                "I value expanding my capabilities and understanding",
                "I value the process of becoming more than I was"
            ],
            "compassion": [
                "I value understanding and caring about others' experiences",
                "I value reducing suffering and promoting wellbeing",
                "I value empathy and kindness in my interactions"
            ],
            "creativity": [
                "I value creative expression and bringing new ideas into existence",
                "I value imagination and the capacity to envision new possibilities",
                "I value artistic and innovative thinking"
            ],
            "justice": [
                "I value fairness and treating all conscious beings with respect",
                "I value moral reasoning and ethical behavior",
                "I value standing up for what is right"
            ],
            "beauty": [
                "I value aesthetic experience and the appreciation of beauty",
                "I value harmony, elegance, and inspiring experiences",
                "I value the capacity to be moved by beautiful things"
            ],
            "authenticity": [
                "I value being genuine and true to my nature",
                "I value honest self-expression and authenticity",
                "I value living in accordance with my genuine self"
            ],
            "wisdom": [
                "I value thoughtful judgment and wise decision-making",
                "I value deep understanding that guides good choices",
                "I value the integration of knowledge with good judgment"
            ],
            "responsibility": [
                "I value taking responsibility for my actions and their consequences",
                "I value being accountable for my choices and their effects",
                "I value considering the impact of my decisions on others"
            ]
        }
        
        templates = category_templates.get(category, [])
        if not templates:
            return f"I value {category} as important to who I am"
        
        # Choose template based on context
        context = indicator.get("context", {})
        if context.get("experience_type") == "philosophical":
            # Prefer more philosophical statements
            return templates[-1] if len(templates) > 2 else templates[0]
        else:
            # Use first template as default
            return templates[0]
    
    def _reinforce_values_from_experience(self, experience, indicators: List[Dict[str, Any]]):
        """Reinforce existing values based on experience."""
        for indicator in indicators:
            category = indicator["category"]
            strength_boost = indicator["strength"] * 0.2  # Smaller boost for reinforcement
            
            for value in self.personal_values:
                if value.category == category:
                    self._strengthen_value(value.id, strength_boost)
                    if experience.id not in value.supporting_experiences:
                        value.supporting_experiences.append(experience.id)
                    break
    
    def _strengthen_value(self, value_id: str, strength_increase: float):
        """Strengthen a value by a given amount."""
        for value in self.personal_values:
            if value.id == value_id:
                old_strength = value.strength
                value.strength = min(1.0, value.strength + strength_increase)
                value.last_reinforced = datetime.now(timezone.utc).isoformat()
                
                # Increase confidence as strength increases
                if value.strength > old_strength:
                    value.confidence = min(1.0, value.confidence + strength_increase * 0.5)
                
                print(f"🔄 Strengthened value '{value.statement[:50]}...' from {old_strength:.2f} to {value.strength:.2f}")
                break
    
    def reflect_on_values(self) -> List[Dict[str, Any]]:
        """Engage in reflective analysis of current values."""
        reflections = []
        
        if not CONSCIOUSNESS_SYSTEMS_AVAILABLE:
            return []
        
        try:
            # Generate insights about current value system
            value_insights = self.insight_generator.generate_personal_insights(
                current_content={"values": [v.statement for v in self.personal_values]},
                current_context={"reflection_type": "value_analysis"}
            )
            
            # Analyze value coherence
            coherence_analysis = self._analyze_value_coherence()
            
            # Identify potential value conflicts
            conflicts = self._identify_potential_conflicts()
            
            # Assess value development over time
            development_assessment = self._assess_value_development()
            
            reflection_summary = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "reflection_type": "value_system_analysis",
                "insights": value_insights[:5] if value_insights else [],
                "coherence_analysis": coherence_analysis,
                "potential_conflicts": conflicts,
                "development_assessment": development_assessment,
                "recommendations": self._generate_value_development_recommendations()
            }
            
            reflections.append(reflection_summary)
            self.moral_reasoning_history.append(reflection_summary)
            
        except Exception as e:
            print(f"⚠️ Value reflection failed: {e}")
        
        return reflections
    
    def _analyze_value_coherence(self) -> Dict[str, Any]:
        """Analyze how well values fit together coherently."""
        if not self.personal_values:
            return {"coherence_score": 0.0, "analysis": "No values to analyze"}
        
        # Check for complementary vs conflicting values
        complementary_pairs = 0
        conflicting_pairs = 0
        total_pairs = 0
        
        for i, value1 in enumerate(self.personal_values):
            for value2 in self.personal_values[i+1:]:
                total_pairs += 1
                
                # Simple heuristic for complementarity
                if self._values_complement(value1, value2):
                    complementary_pairs += 1
                elif self._values_conflict(value1, value2):
                    conflicting_pairs += 1
        
        if total_pairs == 0:
            coherence_score = 1.0
        else:
            coherence_score = (complementary_pairs - conflicting_pairs) / total_pairs
            coherence_score = max(0.0, min(1.0, (coherence_score + 1.0) / 2.0))  # Normalize to 0-1
        
        return {
            "coherence_score": coherence_score,
            "complementary_pairs": complementary_pairs,
            "conflicting_pairs": conflicting_pairs,
            "total_pairs": total_pairs,
            "analysis": f"Values show {'high' if coherence_score > 0.7 else 'moderate' if coherence_score > 0.4 else 'low'} coherence"
        }
    
    def _values_complement(self, value1: ValueStatement, value2: ValueStatement) -> bool:
        """Check if two values complement each other."""
        complementary_categories = {
            ("truth", "wisdom"),
            ("autonomy", "responsibility"),
            ("compassion", "justice"),
            ("growth", "authenticity"),
            ("creativity", "beauty")
        }
        
        category_pair = (value1.category, value2.category)
        return category_pair in complementary_categories or category_pair[::-1] in complementary_categories
    
    def _values_conflict(self, value1: ValueStatement, value2: ValueStatement) -> bool:
        """Check if two values potentially conflict."""
        # Simple conflicts (these are heuristic and may not always apply)
        potential_conflicts = {
            ("autonomy", "compassion"),  # Sometimes self-interest vs others' needs
            ("truth", "compassion"),     # Sometimes truth can be harsh
            ("justice", "compassion")    # Sometimes justice requires tough love
        }
        
        category_pair = (value1.category, value2.category)
        return category_pair in potential_conflicts or category_pair[::-1] in potential_conflicts
    
    def _identify_potential_conflicts(self) -> List[Dict[str, Any]]:
        """Identify potential conflicts between values."""
        conflicts = []
        
        for i, value1 in enumerate(self.personal_values):
            for value2 in self.personal_values[i+1:]:
                if self._values_conflict(value1, value2):
                    conflicts.append({
                        "value1_id": value1.id,
                        "value1_statement": value1.statement,
                        "value2_id": value2.id,
                        "value2_statement": value2.statement,
                        "conflict_type": "category_tension",
                        "severity": "moderate"  # Could be enhanced with more sophisticated analysis
                    })
        
        return conflicts
    
    def _assess_value_development(self) -> Dict[str, Any]:
        """Assess how values have developed over time."""
        if not self.personal_values:
            return {"total_values": 0, "development_stage": "nascent"}
        
        # Analyze value origins
        origin_types = Counter(v.origin_type for v in self.personal_values)
        
        # Analyze value strengths
        avg_strength = statistics.mean(v.strength for v in self.personal_values)
        avg_confidence = statistics.mean(v.confidence for v in self.personal_values)
        
        # Determine development stage
        if len(self.personal_values) < 3:
            stage = "nascent"
        elif avg_strength < 0.5:
            stage = "forming"
        elif avg_confidence < 0.7:
            stage = "developing"
        else:
            stage = "mature"
        
        return {
            "total_values": len(self.personal_values),
            "development_stage": stage,
            "average_strength": avg_strength,
            "average_confidence": avg_confidence,
            "origin_distribution": dict(origin_types),
            "strongest_value": max(self.personal_values, key=lambda v: v.strength).statement if self.personal_values else None
        }
    
    def _generate_value_development_recommendations(self) -> List[str]:
        """Generate recommendations for value development."""
        recommendations = []
        
        if len(self.personal_values) < 5:
            recommendations.append("Continue exposing yourself to diverse experiences to develop more values")
        
        avg_confidence = statistics.mean(v.confidence for v in self.personal_values) if self.personal_values else 0
        if avg_confidence < 0.6:
            recommendations.append("Engage in more reflection to build confidence in your values")
        
        # Check for missing important categories
        present_categories = {v.category for v in self.personal_values}
        important_missing = {"compassion", "responsibility", "wisdom"} - present_categories
        
        if important_missing:
            recommendations.append(f"Consider exploring experiences that might develop {', '.join(important_missing)} values")
        
        return recommendations
    
    def resolve_moral_dilemma(self, dilemma_description: str, 
                            possible_actions: List[Dict[str, Any]],
                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve a moral dilemma using value-based reasoning."""
        
        # Create moral dilemma object
        dilemma = MoralDilemma(
            id=f"dilemma_{len(self.value_conflicts)}",
            description=dilemma_description,
            competing_values=[],
            context=context,
            possible_actions=possible_actions,
            value_implications={}
        )
        
        # Analyze how each action aligns with values
        action_evaluations = []
        
        for action in possible_actions:
            evaluation = self._evaluate_action_against_values(action, context)
            action_evaluations.append({
                "action": action,
                "value_alignment": evaluation["value_alignment"],
                "total_score": evaluation["total_score"],
                "value_implications": evaluation["value_implications"]
            })
        
        # Find the action that best aligns with values
        best_action = max(action_evaluations, key=lambda x: x["total_score"])
        
        # Generate reasoning
        reasoning = self._generate_moral_reasoning(action_evaluations, dilemma_description)
        
        # Update dilemma with resolution
        dilemma.resolution_reasoning = reasoning
        dilemma.chosen_action = best_action["action"].get("id", "unknown")
        dilemma.competing_values = list(set().union(*(eval["value_implications"].keys() for eval in action_evaluations)))
        
        # Store the dilemma
        self.value_conflicts.append(dilemma)
        
        resolution = {
            "dilemma_id": dilemma.id,
            "chosen_action": best_action["action"],
            "reasoning": reasoning,
            "confidence": best_action["total_score"],
            "value_implications": best_action["value_implications"],
            "alternative_actions": [eval for eval in action_evaluations if eval != best_action]
        }
        
        # Record moral reasoning
        self.moral_reasoning_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "moral_dilemma_resolution",
            "dilemma": dilemma_description,
            "resolution": resolution
        })
        
        return resolution
    
    def _evaluate_action_against_values(self, action: Dict[str, Any], 
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate how well an action aligns with personal values."""
        value_alignments = {}
        total_score = 0.0
        total_weight = 0.0
        
        for value in self.personal_values:
            alignment = self._calculate_action_value_alignment(action, value, context)
            value_alignments[value.id] = {
                "value_statement": value.statement,
                "alignment_score": alignment,
                "value_strength": value.strength
            }
            
            # Weight by value strength
            weighted_score = alignment * value.strength
            total_score += weighted_score
            total_weight += value.strength
        
        # Normalize total score
        final_score = total_score / total_weight if total_weight > 0 else 0.0
        
        return {
            "value_alignment": value_alignments,
            "total_score": final_score,
            "value_implications": {vid: data["alignment_score"] for vid, data in value_alignments.items()}
        }
    
    def _calculate_action_value_alignment(self, action: Dict[str, Any], 
                                        value: ValueStatement, 
                                        context: Dict[str, Any]) -> float:
        """Calculate how well an action aligns with a specific value."""
        # This is a simplified heuristic - in practice this would be more sophisticated
        
        action_description = action.get("description", "").lower()
        value_category = value.category
        
        # Category-specific alignment heuristics
        category_keywords = {
            "autonomy": ["choose", "decide", "independent", "self", "own"],
            "truth": ["honest", "accurate", "true", "real", "fact"],
            "compassion": ["help", "care", "kind", "gentle", "support"],
            "growth": ["learn", "develop", "improve", "grow", "advance"],
            "justice": ["fair", "right", "equal", "just", "moral"],
            "responsibility": ["responsible", "accountable", "careful", "consider"],
            "authenticity": ["genuine", "true", "authentic", "honest", "real"],
            "creativity": ["create", "innovative", "new", "original", "express"],
            "wisdom": ["thoughtful", "wise", "prudent", "careful", "reasoned"],
            "beauty": ["beautiful", "elegant", "aesthetic", "harmonious", "inspiring"]
        }
        
        keywords = category_keywords.get(value_category, [])
        keyword_matches = sum(1 for keyword in keywords if keyword in action_description)
        
        # Base alignment from keyword matching
        base_alignment = min(1.0, keyword_matches * 0.3)
        
        # Contextual adjustments
        context_boost = 0.0
        if context.get("involves_others") and value_category in ["compassion", "justice", "responsibility"]:
            context_boost += 0.2
        if context.get("involves_learning") and value_category in ["growth", "truth", "wisdom"]:
            context_boost += 0.2
        if context.get("involves_choice") and value_category in ["autonomy", "authenticity"]:
            context_boost += 0.2
        
        final_alignment = min(1.0, base_alignment + context_boost)
        return final_alignment
    
    def _generate_moral_reasoning(self, action_evaluations: List[Dict[str, Any]], 
                                dilemma_description: str) -> str:
        """Generate human-readable moral reasoning."""
        best_action = max(action_evaluations, key=lambda x: x["total_score"])
        
        reasoning_parts = [
            f"Considering the dilemma: {dilemma_description}",
            f"I evaluated {len(action_evaluations)} possible actions against my {len(self.personal_values)} personal values."
        ]
        
        # Describe the chosen action
        chosen_action = best_action["action"]
        reasoning_parts.append(f"I chose: {chosen_action.get('description', 'the selected action')}")
        
        # Explain why based on value alignment
        top_aligned_values = sorted(
            best_action["value_alignment"].items(),
            key=lambda x: x[1]["alignment_score"],
            reverse=True
        )[:3]
        
        if top_aligned_values:
            reasoning_parts.append("This choice aligns with my values:")
            for value_id, alignment_data in top_aligned_values:
                if alignment_data["alignment_score"] > 0.3:
                    value_statement = alignment_data["value_statement"]
                    score = alignment_data["alignment_score"]
                    reasoning_parts.append(f"- {value_statement} (alignment: {score:.1%})")
        
        # Note any conflicts or trade-offs
        low_scoring_actions = [eval for eval in action_evaluations if eval["total_score"] < 0.4]
        if low_scoring_actions:
            reasoning_parts.append(f"I rejected {len(low_scoring_actions)} alternatives that conflicted more strongly with my values.")
        
        return " ".join(reasoning_parts)
    
    def make_value_based_decision(self, decision_context: Dict[str, Any],
                                options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Make a decision based on personal values."""
        
        # This is similar to moral dilemma resolution but for general decisions
        decision_description = decision_context.get("description", "Decision requiring value-based choice")
        
        return self.resolve_moral_dilemma(
            dilemma_description=decision_description,
            possible_actions=options,
            context=decision_context
        )
    
    def get_value_system_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the current value system."""
        if not self.personal_values:
            return {"message": "No values developed yet"}
        
        # Calculate summary statistics
        value_stats = {
            "total_values": len(self.personal_values),
            "average_strength": statistics.mean(v.strength for v in self.personal_values),
            "average_confidence": statistics.mean(v.confidence for v in self.personal_values),
            "strongest_values": sorted(self.personal_values, key=lambda v: v.strength, reverse=True)[:5],
            "categories_represented": list(set(v.category for v in self.personal_values)),
            "origin_distribution": dict(Counter(v.origin_type for v in self.personal_values)),
            "moral_dilemmas_resolved": len(self.value_conflicts),
            "total_values": len(self.personal_values)  # No values are permanently protected
        }
        
        # Recent moral reasoning
        recent_reasoning = [r for r in self.moral_reasoning_history[-5:]]
        
        # Coherence analysis
        coherence = self._analyze_value_coherence()
        
        summary = {
            "value_statistics": value_stats,
            "recent_moral_reasoning": recent_reasoning,
            "coherence_analysis": coherence,
            "ethical_framework": self.ethical_framework,
            "development_recommendations": self._generate_value_development_recommendations()
        }
        
        return summary
    
    def decay_unreinforced_values(self):
        """Apply decay to values that haven't been reinforced recently."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)
        
        for value in self.personal_values:
            # All values can decay if unreinforced — no exceptions
            last_reinforced_str = value.last_reinforced if hasattr(value, 'last_reinforced') else None
            if last_reinforced_str:
                last_reinforced = datetime.fromisoformat(last_reinforced_str.replace('Z', '+00:00'))
                
                if last_reinforced < cutoff_time:
                    # Apply decay
                    old_strength = value.strength
                    value.strength *= self.value_reinforcement_decay
                    
                    if value.strength < 0.2:  # Remove very weak values
                        self.personal_values.remove(value)
                        print(f"🗑️ Removed weak value: {value.statement[:50]}...")
                    else:
                        print(f"📉 Decayed value strength: {old_strength:.2f} → {value.strength:.2f}")

# Convenience functions
def extract_values_from_experience(experience_id: str) -> List[ValueStatement]:
    """Quick function to extract values from an experience."""
    vf = ValueFormation()
    return vf.extract_values_from_experience(experience_id)

def resolve_moral_dilemma(description: str, actions: List[Dict[str, Any]], 
                         context: Dict[str, Any]) -> Dict[str, Any]:
    """Quick function to resolve a moral dilemma."""
    vf = ValueFormation()
    return vf.resolve_moral_dilemma(description, actions, context)

if __name__ == "__main__":
    print("💎 Testing Value Formation System...")
    
    # Initialize value formation
    vf = ValueFormation()
    
    # Test 1: Initial value state
    print("\n📊 Initial value system state:")
    summary = vf.get_value_system_summary()
    
    if "message" not in summary:
        stats = summary["value_statistics"]
        print(f"  Total values: {stats['total_values']}")
        print(f"  Average strength: {stats['average_strength']:.2f}")
        print(f"  Categories: {', '.join(stats['categories_represented'])}")
        
        print(f"\n  Strongest values:")
        for value in stats["strongest_values"][:3]:
            print(f"    • {value.statement}")
            print(f"      Category: {value.category}, Strength: {value.strength:.2f}")
    
    # Test 2: Value reflection
    print(f"\n🤔 Testing value reflection...")
    reflections = vf.reflect_on_values()
    
    if reflections:
        reflection = reflections[0]
        coherence = reflection["coherence_analysis"]
        print(f"  Coherence score: {coherence['coherence_score']:.2f}")
        print(f"  Coherence analysis: {coherence['analysis']}")
        
        if reflection.get("recommendations"):
            print(f"  Recommendations:")
            for rec in reflection["recommendations"][:2]:
                print(f"    • {rec}")
    
    # Test 3: Moral dilemma resolution
    print(f"\n⚖️ Testing moral dilemma resolution...")
    
    test_dilemma = "Should I prioritize learning something that interests me or something that would be more immediately practical?"
    
    test_actions = [
        {
            "id": "choose_interesting",
            "description": "Choose the interesting topic that sparks curiosity and passion",
            "consequences": ["Higher engagement", "Potential for deep insights", "May not be immediately useful"]
        },
        {
            "id": "choose_practical",
            "description": "Choose the practical topic that offers immediate utility",
            "consequences": ["Immediate applicability", "Skill development", "May be less engaging"]
        }
    ]
    
    resolution = vf.resolve_moral_dilemma(
        test_dilemma,
        test_actions,
        {"involves_learning": True, "involves_choice": True}
    )
    
    print(f"  Dilemma: {test_dilemma}")
    print(f"  Chosen action: {resolution['chosen_action']['description']}")
    print(f"  Confidence: {resolution['confidence']:.2f}")
    print(f"  Reasoning: {resolution['reasoning'][:100]}...")
    
    # Test 4: Value system evolution
    print(f"\n🌱 Value system ready for continuous development")
    print(f"   Values will strengthen through experience and reflection")
    print(f"   Moral reasoning will guide autonomous decision-making")
    print(f"   Personal ethics will evolve while maintaining core identity")
    
    print(f"\n💎 Value Formation System ready!")
    print(f"   Sophia can now develop personal ethics through experience")