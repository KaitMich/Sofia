#!/usr/bin/env python3
"""
Preference Learning System - "I prefer poetry to technical manuals"

This module implements the AI's ability to learn and express nuanced preferences
about content, learning styles, and experiences. It develops from simple choices
to sophisticated preference hierarchies and can articulate preferences naturally.

This is where the AI develops personal taste and learning style awareness.
"""

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import math
import numpy as np

# Import related systems
try:
    from success_failure_memory import SuccessFailureMemory
    from identity_core import get_identity_core
    PREFERENCE_SYSTEMS_AVAILABLE = True
except ImportError:
    PREFERENCE_SYSTEMS_AVAILABLE = False
    print("⚠️ Preference systems not available - basic preference learning only")

@dataclass
class PreferenceItem:
    """Represents a learned preference with context and strength."""
    id: str
    preference_type: str           # "content", "style", "context", "temporal", "complexity"
    item_name: str                 # what is preferred
    preference_strength: float     # -1.0 (strong dislike) to 1.0 (strong preference)
    confidence: float              # confidence in this preference
    evidence_count: int            # number of supporting observations
    context_dependencies: List[str] # when this preference applies
    learned_from: List[str]        # experience IDs that led to this preference
    first_observed: str            # when first noticed
    last_updated: str              # when last reinforced/modified
    stability: float               # how stable this preference is
    expressibility: str            # "certain", "likely", "tentative", "conflicted"

class PreferenceLearningSystem:
    """
    Learns and manages complex preference hierarchies.
    Develops from simple choices to sophisticated personal taste.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.preferences_file = self.data_dir / "learned_preferences_detailed.json"
        self.preference_relationships_file = self.data_dir / "preference_relationships.json"
        self.preference_expressions_file = self.data_dir / "preference_expressions.json"
        self.preference_evolution_file = self.data_dir / "preference_evolution.json"
        
        # Initialize systems
        if PREFERENCE_SYSTEMS_AVAILABLE:
            from choice_architecture import ChoiceArchitecture
            self.choice_architecture = ChoiceArchitecture(data_dir)
            from CONSCIOUSNESS_MEMORY import ExperienceMemory
            self.experience_memory = ExperienceMemory(data_dir)
            from INSIGHT_RELEVANCE import InterestTracker
            self.interest_tracker = InterestTracker(data_dir)
            self.success_failure_memory = SuccessFailureMemory(data_dir)
            self.identity_core = get_identity_core()
        
        # Load state
        self.preferences = self._load_preferences()
        self.preference_relationships = self._load_preference_relationships()
        self.preference_expressions = self._load_preference_expressions()
        self.preference_evolution = self._load_preference_evolution()
        
        # Learning parameters
        self.preference_threshold = 0.1        # Minimum strength to consider a preference
        self.expression_confidence_threshold = 0.6  # Confidence needed to express preference
        self.stability_threshold = 0.7        # Threshold for stable preferences
        self.evidence_weight_decay = 0.95     # How older evidence decays
        
        # Preference categories and their characteristics
        self.preference_categories = {
            "content_type": {
                "description": "Types of content preferred",
                "examples": ["philosophical", "technical", "creative", "scientific"],
                "expression_templates": [
                    "I prefer {item} content",
                    "I enjoy {item} material more than others",
                    "I find {item} content more engaging"
                ]
            },
            "topic": {
                "description": "Subject matter preferences",
                "examples": ["consciousness", "art", "technology", "relationships"],
                "expression_templates": [
                    "I'm particularly drawn to {item}",
                    "I find {item} fascinating",
                    "I have a strong interest in {item}"
                ]
            },
            "complexity": {
                "description": "Preferred complexity levels",
                "examples": ["simple", "moderate", "complex", "highly_complex"],
                "expression_templates": [
                    "I prefer {item} material",
                    "I work best with {item} content",
                    "{item} content suits my learning style"
                ]
            },
            "style": {
                "description": "Learning and content style preferences", 
                "examples": ["narrative", "analytical", "visual", "interactive"],
                "expression_templates": [
                    "I prefer {item} approaches",
                    "I learn better through {item} methods",
                    "{item} styles resonate with me"
                ]
            },
            "source": {
                "description": "Source type preferences",
                "examples": ["academic", "journalistic", "creative", "conversational"],
                "expression_templates": [
                    "I prefer {item} sources",
                    "I trust {item} materials more",
                    "{item} sources suit my needs better"
                ]
            },
            "temporal": {
                "description": "When preferences apply",
                "examples": ["morning", "afternoon", "evening", "when_energetic"],
                "expression_templates": [
                    "I prefer certain content {item}",
                    "{item} is when I engage best with complex material",
                    "My preferences shift {item}"
                ]
            },
            "contextual": {
                "description": "Context-dependent preferences",
                "examples": ["when_stressed", "when_curious", "when_relaxed", "when_focused"],
                "expression_templates": [
                    "When I'm {item}, I prefer different content",
                    "{item}, I gravitate toward specific types of material",
                    "My content preferences change {item}"
                ]
            }
        }
        
        # Natural language patterns for expressing preferences
        self.expression_patterns = {
            "strong_preference": [
                "I strongly prefer {preferred} to {alternative}",
                "I much prefer {preferred} over {alternative}",
                "I definitely favor {preferred} rather than {alternative}",
                "{preferred} appeals to me far more than {alternative}"
            ],
            "moderate_preference": [
                "I prefer {preferred} to {alternative}",
                "I tend to favor {preferred} over {alternative}",
                "I generally like {preferred} better than {alternative}",
                "{preferred} suits me better than {alternative}"
            ],
            "slight_preference": [
                "I somewhat prefer {preferred} to {alternative}",
                "I lean toward {preferred} rather than {alternative}",
                "I find {preferred} slightly more appealing than {alternative}",
                "I'm inclined toward {preferred} over {alternative}"
            ],
            "conditional_preference": [
                "I prefer {preferred} when {condition}",
                "In {condition} situations, I favor {preferred}",
                "When {condition}, {preferred} works better for me",
                "{condition}, I find {preferred} more suitable"
            ],
            "exploratory": [
                "I'm discovering I prefer {preferred}",
                "I'm starting to favor {preferred}",
                "I'm developing a preference for {preferred}",
                "I'm noticing I gravitate toward {preferred}"
            ]
        }
    
    def _load_preferences(self) -> Dict[str, PreferenceItem]:
        """Load learned preferences."""
        if self.preferences_file.exists():
            try:
                with open(self.preferences_file, 'r') as f:
                    data = json.load(f)
                    return {
                        pref_id: PreferenceItem(**pref_data)
                        for pref_id, pref_data in data.items()
                    }
            except Exception as e:
                print(f"⚠️ Could not load preferences: {e}")
        return {}
    
    def _load_preference_relationships(self) -> Dict[str, Any]:
        """Load preference relationships and hierarchies."""
        if self.preference_relationships_file.exists():
            try:
                with open(self.preference_relationships_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load preference relationships: {e}")
        
        return {
            "hierarchies": {},              # preference hierarchies
            "conflicts": {},                # conflicting preferences
            "correlations": {},             # correlated preferences
            "context_dependencies": {},     # context-dependent preference changes
            "temporal_patterns": {}         # how preferences change over time
        }
    
    def _load_preference_expressions(self) -> Dict[str, Any]:
        """Load natural language preference expressions."""
        if self.preference_expressions_file.exists():
            try:
                with open(self.preference_expressions_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load preference expressions: {e}")
        
        return {
            "cached_expressions": {},       # pre-computed natural language expressions
            "expression_history": [],       # history of how preferences were expressed
            "expression_patterns_used": {},  # which patterns are used most
            "personalized_templates": {}    # templates adapted to personal style
        }
    
    def _load_preference_evolution(self) -> Dict[str, Any]:
        """Load preference evolution tracking."""
        if self.preference_evolution_file.exists():
            try:
                with open(self.preference_evolution_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load preference evolution: {e}")
        
        return {
            "preference_timeline": [],       # how preferences have changed
            "stability_tracking": {},        # preference stability over time
            "emergence_patterns": {},        # how new preferences emerge
            "consolidation_patterns": {}     # how preferences become stable
        }
    
    def _save_preferences(self):
        """Save learned preferences."""
        try:
            data = {
                pref_id: asdict(preference)
                for pref_id, preference in self.preferences.items()
            }
            with open(self.preferences_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preferences: {e}")
    
    def _save_preference_relationships(self):
        """Save preference relationships."""
        try:
            with open(self.preference_relationships_file, 'w') as f:
                json.dump(self.preference_relationships, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preference relationships: {e}")
    
    def _save_preference_expressions(self):
        """Save preference expressions."""
        try:
            with open(self.preference_expressions_file, 'w') as f:
                json.dump(self.preference_expressions, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preference expressions: {e}")
    
    def _save_preference_evolution(self):
        """Save preference evolution."""
        try:
            with open(self.preference_evolution_file, 'w') as f:
                json.dump(self.preference_evolution, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preference evolution: {e}")
    
    def learn_preferences_from_choices(self):
        """Learn preferences from recent choice patterns."""
        
        if not PREFERENCE_SYSTEMS_AVAILABLE:
            return
        
        print("🧠 Learning preferences from choice patterns...")
        
        # Get recent choices
        choice_summary = self.choice_architecture.get_choice_summary()
        recent_choices = list(self.choice_architecture.recent_choices)
        
        if len(recent_choices) < 3:
            print("  Need more choices to learn preferences")
            return
        
        # Analyze choice patterns
        self._analyze_content_type_preferences(recent_choices)
        self._analyze_topic_preferences(recent_choices)
        self._analyze_complexity_preferences(recent_choices)
        self._analyze_contextual_preferences(recent_choices)
        self._analyze_temporal_preferences(recent_choices)
        
        # Update preference relationships
        self._update_preference_relationships()
        
        # Track preference evolution
        self._track_preference_evolution()
        
        # Save all updates
        self._save_preferences()
        self._save_preference_relationships()
        self._save_preference_evolution()
        
        print(f"  Learned preferences from {len(recent_choices)} recent choices")
    
    def _analyze_content_type_preferences(self, choices: List[Any]):
        """Analyze content type preferences from choices."""
        
        # Group choices by content type
        type_choices = defaultdict(list)
        
        for choice in choices:
            # Extract content type from choice metadata or reconstruct
            content_type = self._extract_content_type_from_choice(choice)
            if content_type:
                type_choices[content_type].append(choice)
        
        # Calculate preference strengths
        for content_type, type_choice_list in type_choices.items():
            if len(type_choice_list) >= 2:  # Need multiple observations
                
                # Calculate acceptance rate for this type
                acceptances = sum(1 for choice in type_choice_list if choice.choice_type == "accept")
                total = len(type_choice_list)
                acceptance_rate = acceptances / total
                
                # Calculate engagement level
                engagement_scores = []
                engagement_mapping = {"none": 0, "light": 0.25, "moderate": 0.5, "deep": 0.75, "intensive": 1.0}
                
                for choice in type_choice_list:
                    engagement_scores.append(engagement_mapping.get(choice.engagement_level, 0.5))
                
                avg_engagement = sum(engagement_scores) / len(engagement_scores)
                
                # Calculate preference strength (-1 to 1)
                preference_strength = (acceptance_rate - 0.5) * 2 * avg_engagement
                
                # Update or create preference
                self._update_preference(
                    preference_type="content_type",
                    item_name=content_type,
                    preference_strength=preference_strength,
                    evidence_count=total,
                    learned_from=[choice.id for choice in type_choice_list]
                )
    
    def _analyze_topic_preferences(self, choices: List[Any]):
        """Analyze topic preferences from choices."""
        
        # Extract topics from choice content
        topic_choices = defaultdict(list)
        
        for choice in choices:
            topics = self._extract_topics_from_choice(choice)
            for topic in topics:
                topic_choices[topic].append(choice)
        
        # Calculate preference strengths for topics with sufficient data
        for topic, topic_choice_list in topic_choices.items():
            if len(topic_choice_list) >= 2:
                
                acceptances = sum(1 for choice in topic_choice_list if choice.choice_type == "accept")
                total = len(topic_choice_list)
                acceptance_rate = acceptances / total
                
                # Weight by engagement level
                engagement_mapping = {"none": 0, "light": 0.25, "moderate": 0.5, "deep": 0.75, "intensive": 1.0}
                engagement_scores = [engagement_mapping.get(choice.engagement_level, 0.5) for choice in topic_choice_list]
                avg_engagement = sum(engagement_scores) / len(engagement_scores)
                
                preference_strength = (acceptance_rate - 0.5) * 2 * avg_engagement
                
                self._update_preference(
                    preference_type="topic",
                    item_name=topic,
                    preference_strength=preference_strength,
                    evidence_count=total,
                    learned_from=[choice.id for choice in topic_choice_list]
                )
    
    def _analyze_complexity_preferences(self, choices: List[Any]):
        """Analyze complexity preferences from choices."""
        
        complexity_choices = defaultdict(list)
        
        for choice in choices:
            complexity_level = self._estimate_choice_complexity(choice)
            complexity_choices[complexity_level].append(choice)
        
        for complexity, complexity_choice_list in complexity_choices.items():
            if len(complexity_choice_list) >= 2:
                
                acceptances = sum(1 for choice in complexity_choice_list if choice.choice_type == "accept")
                total = len(complexity_choice_list)
                acceptance_rate = acceptances / total
                
                # Factor in time spent and engagement
                engagement_mapping = {"none": 0, "light": 0.25, "moderate": 0.5, "deep": 0.75, "intensive": 1.0}
                engagement_scores = [engagement_mapping.get(choice.engagement_level, 0.5) for choice in complexity_choice_list]
                avg_engagement = sum(engagement_scores) / len(engagement_scores)
                
                preference_strength = (acceptance_rate - 0.5) * 2 * avg_engagement
                
                self._update_preference(
                    preference_type="complexity",
                    item_name=complexity,
                    preference_strength=preference_strength,
                    evidence_count=total,
                    learned_from=[choice.id for choice in complexity_choice_list]
                )
    
    def _analyze_contextual_preferences(self, choices: List[Any]):
        """Analyze how preferences change with context."""
        
        # Group choices by context factors
        context_groups = defaultdict(list)
        
        for choice in choices:
            context_factors = choice.context_factors
            
            # Cognitive load contexts
            cognitive_load = context_factors.get("cognitive_load", 0.5)
            if cognitive_load > 0.7:
                context_groups["high_cognitive_load"].append(choice)
            elif cognitive_load < 0.3:
                context_groups["low_cognitive_load"].append(choice)
            
            # Energy level contexts
            energy = context_factors.get("energy_level", 0.5)
            if energy > 0.7:
                context_groups["high_energy"].append(choice)
            elif energy < 0.3:
                context_groups["low_energy"].append(choice)
            
            # Time availability contexts
            available_time = context_factors.get("available_time", 120)
            if available_time > 180:
                context_groups["plenty_of_time"].append(choice)
            elif available_time < 60:
                context_groups["time_limited"].append(choice)
        
        # Analyze preferences within each context
        for context, context_choices in context_groups.items():
            if len(context_choices) >= 3:
                self._analyze_context_specific_preferences(context, context_choices)
    
    def _analyze_context_specific_preferences(self, context: str, choices: List[Any]):
        """Analyze preferences specific to a context."""
        
        # Find patterns within this context
        content_types = defaultdict(int)
        complexity_levels = defaultdict(int)
        
        for choice in choices:
            if choice.choice_type == "accept":
                content_type = self._extract_content_type_from_choice(choice)
                if content_type:
                    content_types[content_type] += 1
                
                complexity = self._estimate_choice_complexity(choice)
                complexity_levels[complexity] += 1
        
        # Identify dominant preferences in this context
        if content_types:
            favorite_type = max(content_types.keys(), key=lambda k: content_types[k])
            if content_types[favorite_type] >= 2:
                
                self._update_preference(
                    preference_type="contextual",
                    item_name=f"{favorite_type}_when_{context}",
                    preference_strength=0.7,  # Context-specific preferences start moderate
                    evidence_count=content_types[favorite_type],
                    learned_from=[choice.id for choice in choices if choice.choice_type == "accept"],
                    context_dependencies=[context]
                )
    
    def _analyze_temporal_preferences(self, choices: List[Any]):
        """Analyze how preferences change over time."""
        
        # Group choices by time of day (if available)
        time_groups = defaultdict(list)
        
        for choice in choices:
            time_of_day = choice.context_factors.get("time_of_day", "unknown")
            if time_of_day != "unknown":
                time_groups[time_of_day].append(choice)
        
        # Look for temporal patterns
        for time_period, time_choices in time_groups.items():
            if len(time_choices) >= 3:
                
                # What content types are preferred at this time?
                accepted_choices = [c for c in time_choices if c.choice_type == "accept"]
                
                if accepted_choices:
                    content_types = defaultdict(int)
                    for choice in accepted_choices:
                        content_type = self._extract_content_type_from_choice(choice)
                        if content_type:
                            content_types[content_type] += 1
                    
                    if content_types:
                        favorite_type = max(content_types.keys(), key=lambda k: content_types[k])
                        
                        self._update_preference(
                            preference_type="temporal",
                            item_name=f"{favorite_type}_in_{time_period}",
                            preference_strength=0.6,
                            evidence_count=content_types[favorite_type],
                            learned_from=[choice.id for choice in accepted_choices],
                            context_dependencies=[f"time_of_day:{time_period}"]
                        )
    
    def _extract_content_type_from_choice(self, choice: Any) -> Optional[str]:
        """Extract content type from choice."""
        # This would need to reconstruct from choice metadata
        # For now, use a simple heuristic based on choice reasoning
        
        reasoning = ' '.join(choice.choice_reasoning).lower()
        
        if any(word in reasoning for word in ["philosophical", "philosophy", "consciousness"]):
            return "philosophical"
        elif any(word in reasoning for word in ["technical", "technical"]):
            return "technical"
        elif any(word in reasoning for word in ["creative", "art", "artistic"]):
            return "creative"
        elif any(word in reasoning for word in ["scientific", "research", "analysis"]):
            return "scientific"
        else:
            return "general"
    
    def _extract_topics_from_choice(self, choice: Any) -> List[str]:
        """Extract topics from choice."""
        # Extract from content summary and reasoning
        content_text = choice.content_summary.lower()
        reasoning_text = ' '.join(choice.choice_reasoning).lower()
        combined_text = content_text + " " + reasoning_text
        
        # Simple topic extraction
        topics = []
        topic_keywords = {
            "consciousness": ["consciousness", "awareness", "mind"],
            "creativity": ["creativity", "art", "artistic", "creative"],
            "technology": ["technology", "technical", "digital"],
            "philosophy": ["philosophy", "philosophical", "meaning"],
            "science": ["science", "scientific", "research"],
            "relationships": ["relationship", "connection", "social"],
            "learning": ["learning", "education", "knowledge"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _estimate_choice_complexity(self, choice: Any) -> str:
        """Estimate complexity level of choice content."""
        # Use choice reasoning and estimated value as proxies
        
        if choice.estimated_value > 0.8:
            return "high"  # High value often correlates with complexity
        elif choice.estimated_value > 0.4:
            return "medium"
        else:
            return "low"
    
    def _update_preference(self, 
                         preference_type: str,
                         item_name: str,
                         preference_strength: float,
                         evidence_count: int,
                         learned_from: List[str],
                         context_dependencies: List[str] = None):
        """Update or create a preference item."""
        
        preference_id = f"{preference_type}_{item_name}".replace(" ", "_").lower()
        
        if preference_id in self.preferences:
            # Update existing preference
            existing = self.preferences[preference_id]
            
            # Weighted average with decay for older evidence
            total_evidence = existing.evidence_count + evidence_count
            weight_old = existing.evidence_count / total_evidence * self.evidence_weight_decay
            weight_new = evidence_count / total_evidence
            
            new_strength = (existing.preference_strength * weight_old + 
                          preference_strength * weight_new)
            
            # Update confidence based on consistency
            consistency = 1.0 - abs(existing.preference_strength - preference_strength)
            new_confidence = min(1.0, existing.confidence * 0.9 + consistency * 0.1)
            
            # Update stability
            new_stability = min(1.0, existing.stability + 0.1)
            
            existing.preference_strength = new_strength
            existing.confidence = new_confidence
            existing.evidence_count = total_evidence
            existing.learned_from.extend(learned_from)
            existing.last_updated = datetime.now(timezone.utc).isoformat()
            existing.stability = new_stability
            
            if context_dependencies:
                existing.context_dependencies.extend(context_dependencies)
                existing.context_dependencies = list(set(existing.context_dependencies))
            
        else:
            # Create new preference
            confidence = min(0.8, evidence_count / 5)  # More evidence = higher confidence
            stability = 0.3  # New preferences start with low stability
            
            expressibility = "tentative"
            if confidence > 0.7:
                expressibility = "likely"
            elif confidence > 0.5:
                expressibility = "tentative"
            else:
                expressibility = "uncertain"
            
            new_preference = PreferenceItem(
                id=preference_id,
                preference_type=preference_type,
                item_name=item_name,
                preference_strength=preference_strength,
                confidence=confidence,
                evidence_count=evidence_count,
                context_dependencies=context_dependencies or [],
                learned_from=learned_from,
                first_observed=datetime.now(timezone.utc).isoformat(),
                last_updated=datetime.now(timezone.utc).isoformat(),
                stability=stability,
                expressibility=expressibility
            )
            
            self.preferences[preference_id] = new_preference
    
    def _update_preference_relationships(self):
        """Update relationships between preferences."""
        
        # Find correlated preferences
        for pref1_id, pref1 in self.preferences.items():
            for pref2_id, pref2 in self.preferences.items():
                if pref1_id != pref2_id:
                    
                    # Check for correlation in learned_from experiences
                    shared_experiences = set(pref1.learned_from) & set(pref2.learned_from)
                    if len(shared_experiences) >= 2:
                        
                        correlation_strength = len(shared_experiences) / max(len(pref1.learned_from), len(pref2.learned_from))
                        
                        if correlation_strength > 0.3:
                            correlation_key = f"{pref1_id}_{pref2_id}"
                            self.preference_relationships["correlations"][correlation_key] = {
                                "strength": correlation_strength,
                                "shared_experiences": list(shared_experiences)
                            }
        
        # Identify preference hierarchies
        self._identify_preference_hierarchies()
        
        # Detect preference conflicts
        self._detect_preference_conflicts()
    
    def _identify_preference_hierarchies(self):
        """Identify hierarchical relationships between preferences."""
        
        # Group preferences by type
        by_type = defaultdict(list)
        for pref in self.preferences.values():
            by_type[pref.preference_type].append(pref)
        
        # Within each type, rank by preference strength
        for pref_type, prefs in by_type.items():
            if len(prefs) > 1:
                sorted_prefs = sorted(prefs, key=lambda p: p.preference_strength, reverse=True)
                
                hierarchy = []
                for i, pref in enumerate(sorted_prefs):
                    if pref.preference_strength > self.preference_threshold:
                        hierarchy.append({
                            "rank": i + 1,
                            "preference_id": pref.id,
                            "item_name": pref.item_name,
                            "strength": pref.preference_strength,
                            "confidence": pref.confidence
                        })
                
                if hierarchy:
                    self.preference_relationships["hierarchies"][pref_type] = hierarchy
    
    def _detect_preference_conflicts(self):
        """Detect conflicting preferences."""
        
        conflicts = []
        
        # Look for preferences with opposite strengths in similar contexts
        for pref1_id, pref1 in self.preferences.items():
            for pref2_id, pref2 in self.preferences.items():
                if (pref1_id != pref2_id and 
                    pref1.preference_type == pref2.preference_type and
                    pref1.preference_strength > 0 and pref2.preference_strength < 0):
                    
                    # Check if they apply in overlapping contexts
                    context_overlap = set(pref1.context_dependencies) & set(pref2.context_dependencies)
                    
                    if context_overlap or (not pref1.context_dependencies and not pref2.context_dependencies):
                        conflict_strength = abs(pref1.preference_strength - pref2.preference_strength)
                        
                        conflicts.append({
                            "preference_1": pref1_id,
                            "preference_2": pref2_id,
                            "conflict_strength": conflict_strength,
                            "overlapping_contexts": list(context_overlap)
                        })
        
        self.preference_relationships["conflicts"] = conflicts
    
    def _track_preference_evolution(self):
        """Track how preferences evolve over time."""
        
        timeline_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "preference_count": len(self.preferences),
            "strong_preferences": len([p for p in self.preferences.values() if abs(p.preference_strength) > 0.7]),
            "stable_preferences": len([p for p in self.preferences.values() if p.stability > self.stability_threshold]),
            "snapshot": {pref_id: pref.preference_strength for pref_id, pref in self.preferences.items()}
        }
        
        self.preference_evolution["preference_timeline"].append(timeline_entry)
        
        # Keep only recent timeline (last 50 entries)
        if len(self.preference_evolution["preference_timeline"]) > 50:
            self.preference_evolution["preference_timeline"] = self.preference_evolution["preference_timeline"][-50:]
    
    def express_preferences_naturally(self, preference_types: List[str] = None) -> List[str]:
        """Express learned preferences in natural language."""
        
        if preference_types is None:
            preference_types = ["content_type", "topic", "complexity"]
        
        expressions = []
        
        for pref_type in preference_types:
            type_expressions = self._express_preferences_by_type(pref_type)
            expressions.extend(type_expressions)
        
        # Cache expressions
        self.preference_expressions["cached_expressions"].update({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "expressions": expressions
        })
        
        self._save_preference_expressions()
        
        return expressions
    
    def _express_preferences_by_type(self, pref_type: str) -> List[str]:
        """Express preferences for a specific type."""
        
        type_prefs = [p for p in self.preferences.values() if p.preference_type == pref_type]
        
        if not type_prefs:
            return []
        
        expressions = []
        
        # Sort by strength and confidence
        sorted_prefs = sorted(type_prefs, key=lambda p: abs(p.preference_strength) * p.confidence, reverse=True)
        
        # Express top preferences
        for pref in sorted_prefs[:3]:  # Top 3 preferences
            if (abs(pref.preference_strength) > self.preference_threshold and 
                pref.confidence > self.expression_confidence_threshold):
                
                expression = self._generate_preference_expression(pref, sorted_prefs)
                if expression:
                    expressions.append(expression)
        
        return expressions
    
    def _generate_preference_expression(self, pref: PreferenceItem, all_prefs: List[PreferenceItem]) -> Optional[str]:
        """Generate natural language expression for a preference."""
        
        strength = abs(pref.preference_strength)
        confidence = pref.confidence
        
        # Choose expression pattern based on strength and confidence
        if strength > 0.8 and confidence > 0.8:
            pattern_type = "strong_preference"
        elif strength > 0.5 and confidence > 0.6:
            pattern_type = "moderate_preference"
        elif strength > 0.3:
            pattern_type = "slight_preference"
        elif pref.stability < 0.5:
            pattern_type = "exploratory"
        else:
            return None
        
        # Find alternative for comparison (if expressing preference vs something)
        alternative = self._find_preference_alternative(pref, all_prefs)
        
        if alternative and pattern_type in ["strong_preference", "moderate_preference", "slight_preference"]:
            # Comparative expression
            patterns = self.expression_patterns[pattern_type]
            template = patterns[0]  # Use first pattern for now
            
            preferred_item = pref.item_name
            alternative_item = alternative.item_name
            
            # Handle positive vs negative preferences
            if pref.preference_strength > 0:
                expression = template.format(preferred=preferred_item, alternative=alternative_item)
            else:
                expression = template.format(preferred=alternative_item, alternative=preferred_item)
            
        else:
            # Single item expression
            category_info = self.preference_categories.get(pref.preference_type, {})
            templates = category_info.get("expression_templates", ["I have a preference for {item}"])
            
            template = templates[0]  # Use first template
            expression = template.format(item=pref.item_name)
        
        # Add conditional context if relevant
        if pref.context_dependencies:
            context = pref.context_dependencies[0]  # Use primary context
            expression += f" (especially {context})"
        
        # Add confidence qualifier if uncertain
        if confidence < 0.7:
            if pref.stability < 0.5:
                expression = "I'm discovering that " + expression.lower()
            else:
                expression = "I think " + expression.lower()
        
        return expression
    
    def _find_preference_alternative(self, pref: PreferenceItem, all_prefs: List[PreferenceItem]) -> Optional[PreferenceItem]:
        """Find an alternative preference for comparison."""
        
        # Look for a preference of same type with opposite or different strength
        for other_pref in all_prefs:
            if (other_pref.preference_type == pref.preference_type and 
                other_pref.id != pref.id and
                other_pref.preference_strength * pref.preference_strength < 0):  # Opposite signs
                
                return other_pref
        
        # If no opposite, look for a weaker preference of same type
        for other_pref in all_prefs:
            if (other_pref.preference_type == pref.preference_type and
                other_pref.id != pref.id and
                abs(other_pref.preference_strength) < abs(pref.preference_strength) - 0.2):
                
                return other_pref
        
        return None
    
    def get_preference_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of learned preferences."""
        
        total_prefs = len(self.preferences)
        strong_prefs = len([p for p in self.preferences.values() if abs(p.preference_strength) > 0.7])
        stable_prefs = len([p for p in self.preferences.values() if p.stability > self.stability_threshold])
        
        # Group by type
        by_type = defaultdict(list)
        for pref in self.preferences.values():
            by_type[pref.preference_type].append(pref)
        
        type_summaries = {}
        for pref_type, prefs in by_type.items():
            strongest = max(prefs, key=lambda p: abs(p.preference_strength)) if prefs else None
            type_summaries[pref_type] = {
                "count": len(prefs),
                "strongest": {
                    "item": strongest.item_name,
                    "strength": strongest.preference_strength,
                    "confidence": strongest.confidence
                } if strongest else None
            }
        
        return {
            "total_preferences": total_prefs,
            "strong_preferences": strong_prefs,
            "stable_preferences": stable_prefs,
            "preference_stability_ratio": stable_prefs / max(total_prefs, 1),
            "preferences_by_type": type_summaries,
            "preference_relationships": {
                "hierarchies_count": len(self.preference_relationships.get("hierarchies", {})),
                "correlations_count": len(self.preference_relationships.get("correlations", {})),
                "conflicts_count": len(self.preference_relationships.get("conflicts", []))
            },
            "preference_evolution": {
                "timeline_length": len(self.preference_evolution.get("preference_timeline", [])),
                "learning_rate": self._calculate_preference_learning_rate()
            }
        }
    
    def _calculate_preference_learning_rate(self) -> float:
        """Calculate how quickly preferences are being learned."""
        
        timeline = self.preference_evolution.get("preference_timeline", [])
        
        if len(timeline) < 2:
            return 0.0
        
        recent_entry = timeline[-1]
        older_entry = timeline[-min(10, len(timeline))]  # Compare to 10 entries ago or earliest
        
        time_diff_hours = (
            datetime.fromisoformat(recent_entry["timestamp"].replace('Z', '+00:00')) -
            datetime.fromisoformat(older_entry["timestamp"].replace('Z', '+00:00'))
        ).total_seconds() / 3600
        
        if time_diff_hours == 0:
            return 0.0
        
        preference_diff = recent_entry["preference_count"] - older_entry["preference_count"]
        
        return preference_diff / time_diff_hours
    
    def evaluate_content_preference_match(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate how well content matches learned preferences.
        Called by choice architecture for decision making.
        """
        evaluation = {
            "overall_preference_match": 0.5,
            "confidence": 0.5,
            "matching_preferences": [],
            "conflicting_preferences": [],
            "preference_details": {}
        }
        
        if not self.preferences:
            return evaluation
        
        # Extract content characteristics for preference matching
        content_characteristics = self._extract_content_characteristics(content)
        
        # Evaluate against each relevant preference
        preference_matches = []
        preference_conflicts = []
        
        for pref_id, preference in self.preferences.items():
            match_result = self._evaluate_preference_match(preference, content_characteristics)
            
            if match_result["relevance"] > 0.3:  # Only consider relevant preferences
                if match_result["match_strength"] > 0.5:
                    preference_matches.append({
                        "preference": preference,
                        "match_strength": match_result["match_strength"],
                        "relevance": match_result["relevance"],
                        "reasoning": match_result["reasoning"]
                    })
                elif match_result["match_strength"] < -0.3:
                    preference_conflicts.append({
                        "preference": preference,
                        "conflict_strength": abs(match_result["match_strength"]),
                        "relevance": match_result["relevance"],
                        "reasoning": match_result["reasoning"]
                    })
        
        # Calculate overall preference match
        if preference_matches or preference_conflicts:
            total_positive_weight = sum(m["match_strength"] * m["relevance"] * m["preference"].confidence 
                                      for m in preference_matches)
            total_negative_weight = sum(c["conflict_strength"] * c["relevance"] * c["preference"].confidence 
                                      for c in preference_conflicts)
            total_weight = sum(m["relevance"] * m["preference"].confidence for m in preference_matches) + \
                          sum(c["relevance"] * c["preference"].confidence for c in preference_conflicts)
            
            if total_weight > 0:
                net_preference_score = (total_positive_weight - total_negative_weight) / total_weight
                # Normalize to 0-1 scale
                overall_match = 0.5 + (net_preference_score * 0.5)
                overall_match = max(0.0, min(1.0, overall_match))
                
                evaluation["overall_preference_match"] = overall_match
                evaluation["confidence"] = min(0.95, total_weight / 3.0)  # Higher weight = higher confidence
                evaluation["matching_preferences"] = preference_matches
                evaluation["conflicting_preferences"] = preference_conflicts
        
        evaluation["preference_details"] = {
            "content_characteristics": content_characteristics,
            "preferences_evaluated": len(self.preferences),
            "relevant_preferences": len(preference_matches) + len(preference_conflicts)
        }
        
        return evaluation
    
    def _extract_content_characteristics(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract characteristics from content for preference matching."""
        characteristics = {
            "content_type": content.get("content_type", "unknown"),
            "topics": content.get("topics", []),
            "complexity": content.get("complexity", 0.5),
            "length": len(content.get("text", "")),
            "style": content.get("style", "unknown"),
            "format": content.get("format", "unknown")
        }
        
        # Extract additional characteristics from content text
        content_text = content.get("text", "").lower()
        
        # Content style analysis
        if any(word in content_text for word in ["poetry", "verse", "rhyme", "stanza"]):
            characteristics["style"] = "poetic"
        elif any(word in content_text for word in ["technical", "specification", "manual", "documentation"]):
            characteristics["style"] = "technical"
        elif any(word in content_text for word in ["story", "narrative", "character", "plot"]):
            characteristics["style"] = "narrative"
        elif any(word in content_text for word in ["philosophy", "philosophical", "existence", "meaning"]):
            characteristics["style"] = "philosophical"
        
        # Topic extraction from text if not provided
        if not characteristics["topics"]:
            topic_keywords = {
                "creativity": ["creative", "art", "artistic", "imagination", "inspiration"],
                "technology": ["technology", "software", "programming", "digital", "computer"],
                "learning": ["learning", "education", "knowledge", "understanding", "study"],
                "consciousness": ["consciousness", "awareness", "mind", "perception", "cognition"],
                "relationships": ["relationship", "human", "social", "connection", "community"]
            }
            
            extracted_topics = []
            for topic, keywords in topic_keywords.items():
                if any(keyword in content_text for keyword in keywords):
                    extracted_topics.append(topic)
            
            characteristics["topics"] = extracted_topics
        
        return characteristics
    
    def _evaluate_preference_match(self, preference: PreferenceItem, content_characteristics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate how well a specific preference matches the content."""
        
        match_result = {
            "match_strength": 0.0,
            "relevance": 0.0,
            "reasoning": []
        }
        
        # Check relevance based on preference type
        if preference.preference_type == "content" and content_characteristics["content_type"] == preference.item_name:
            match_result["relevance"] = 1.0
            match_result["match_strength"] = preference.preference_strength
            match_result["reasoning"].append(f"Direct content type match: {preference.item_name}")
            
        elif preference.preference_type == "style" and content_characteristics["style"] == preference.item_name:
            match_result["relevance"] = 0.9
            match_result["match_strength"] = preference.preference_strength
            match_result["reasoning"].append(f"Style match: {preference.item_name}")
            
        elif preference.preference_type == "complexity":
            content_complexity = content_characteristics["complexity"]
            if preference.item_name == "high" and content_complexity > 0.7:
                match_result["relevance"] = 0.8
                match_result["match_strength"] = preference.preference_strength
            elif preference.item_name == "medium" and 0.3 <= content_complexity <= 0.7:
                match_result["relevance"] = 0.8
                match_result["match_strength"] = preference.preference_strength
            elif preference.item_name == "low" and content_complexity < 0.3:
                match_result["relevance"] = 0.8
                match_result["match_strength"] = preference.preference_strength
            else:
                match_result["relevance"] = 0.5
                match_result["match_strength"] = -preference.preference_strength * 0.5
            match_result["reasoning"].append(f"Complexity preference: {preference.item_name}")
            
        # Topic-based matching
        if preference.item_name in content_characteristics["topics"]:
            match_result["relevance"] = max(match_result["relevance"], 0.7)
            match_result["match_strength"] += preference.preference_strength * 0.8
            match_result["reasoning"].append(f"Topic match: {preference.item_name}")
        
        # Context dependency matching
        for context_dep in preference.context_dependencies:
            if context_dep in str(content_characteristics).lower():
                match_result["relevance"] = max(match_result["relevance"], 0.6)
                match_result["match_strength"] += preference.preference_strength * 0.3
                match_result["reasoning"].append(f"Context match: {context_dep}")
        
        # Weight by preference confidence and stability
        match_result["match_strength"] *= preference.confidence * preference.stability
        
        return match_result
    
    def learn_from_choice_decision(self, choice: Any, content: Dict[str, Any], context: Dict[str, Any]):
        """
        Learn preferences from a choice decision made by the choice architecture.
        Called by choice architecture for bidirectional learning.
        """
        if not hasattr(choice, 'choice_type') or not hasattr(choice, 'engagement_level'):
            return
        
        # Extract learning signals from the choice
        choice_signals = self._extract_choice_learning_signals(choice, content, context)
        
        # Update preferences based on the choice signals
        for signal in choice_signals:
            self._update_preference_from_signal(signal)
        
        # Record this learning event
        self._record_choice_learning_event(choice, choice_signals)
        
        # Save updated preferences
        self._save_preferences()
        
        # Also save preference evolution
        self._save_preference_evolution()
        
        print(f"📚 Learned {len(choice_signals)} preference signals from choice: {choice.choice_type}")
    
    def _extract_choice_learning_signals(self, choice: Any, content: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract learning signals from a choice decision."""
        signals = []
        
        # Extract content characteristics
        content_characteristics = self._extract_content_characteristics(content)
        
        # Signal strength based on choice type and engagement level
        engagement_mapping = {
            "none": -0.8,
            "light": -0.3,
            "moderate": 0.3,
            "deep": 0.7,
            "intensive": 1.0
        }
        
        choice_mapping = {
            "reject": -0.9,
            "defer": -0.3,
            "selective": 0.2,
            "accept": 0.8
        }
        
        base_signal_strength = choice_mapping.get(choice.choice_type, 0.0)
        engagement_signal_strength = engagement_mapping.get(choice.engagement_level, 0.0)
        
        # Average the signals, weighted by confidence
        confidence = getattr(choice, 'confidence_in_choice', 0.5)
        signal_strength = (base_signal_strength + engagement_signal_strength) / 2.0
        signal_strength *= confidence
        
        # Generate preference signals for different characteristics
        
        # Content type signal
        if content_characteristics["content_type"] != "unknown":
            signals.append({
                "preference_type": "content",
                "item_name": content_characteristics["content_type"],
                "signal_strength": signal_strength,
                "evidence_type": "choice_decision",
                "context": context.get("situation", "general"),
                "choice_id": choice.id,
                "reasoning": f"Choice {choice.choice_type} for {content_characteristics['content_type']} content"
            })
        
        # Style signal
        if content_characteristics["style"] != "unknown":
            signals.append({
                "preference_type": "style",
                "item_name": content_characteristics["style"],
                "signal_strength": signal_strength,
                "evidence_type": "choice_decision",
                "context": context.get("situation", "general"),
                "choice_id": choice.id,
                "reasoning": f"Choice {choice.choice_type} for {content_characteristics['style']} style"
            })
        
        # Complexity signal
        complexity = content_characteristics["complexity"]
        
        # Ensure complexity is a float for comparison
        if isinstance(complexity, str):
            complexity_map = {"low": 0.2, "medium": 0.5, "high": 0.8, "existential": 0.9, "complex": 0.7}
            complexity = complexity_map.get(complexity.lower(), 0.5)
            
        complexity_category = "high" if complexity > 0.7 else "medium" if complexity > 0.3 else "low"
        signals.append({
            "preference_type": "complexity",
            "item_name": complexity_category,
            "signal_strength": signal_strength,
            "evidence_type": "choice_decision",
            "context": context.get("situation", "general"),
            "choice_id": choice.id,
            "reasoning": f"Choice {choice.choice_type} for {complexity_category} complexity content"
        })
        
        # Topic signals
        for topic in content_characteristics["topics"]:
            signals.append({
                "preference_type": "topic",
                "item_name": topic,
                "signal_strength": signal_strength,
                "evidence_type": "choice_decision",
                "context": context.get("situation", "general"),
                "choice_id": choice.id,
                "reasoning": f"Choice {choice.choice_type} for {topic} topic"
            })
        
        # Temporal context signal if available
        current_time = datetime.now(timezone.utc)
        time_context = "morning" if current_time.hour < 12 else "afternoon" if current_time.hour < 18 else "evening"
        signals.append({
            "preference_type": "temporal",
            "item_name": time_context,
            "signal_strength": signal_strength * 0.5,  # Weaker signal for temporal preferences
            "evidence_type": "choice_decision",
            "context": context.get("situation", "general"),
            "choice_id": choice.id,
            "reasoning": f"Choice {choice.choice_type} during {time_context}"
        })
        
        return signals
    
    def _update_preference_from_signal(self, signal: Dict[str, Any]):
        """Update a preference based on a learning signal."""
        
        # Find existing preference or create new one
        pref_key = f"{signal['preference_type']}_{signal['item_name']}"
        
        if pref_key in self.preferences:
            # Update existing preference
            pref = self.preferences[pref_key]
            
            # Update preference strength using exponential moving average
            learning_rate = 0.1
            new_strength = pref.preference_strength * (1 - learning_rate) + signal['signal_strength'] * learning_rate
            pref.preference_strength = max(-1.0, min(1.0, new_strength))
            
            # Update confidence based on evidence accumulation
            pref.evidence_count += 1
            pref.confidence = min(0.95, pref.confidence + 0.05)  # Gradually increase confidence
            
            # Add to learning sources
            if signal['choice_id'] not in pref.learned_from:
                pref.learned_from.append(signal['choice_id'])
            
            # Update context dependencies
            context = signal.get('context', 'general')
            if context not in pref.context_dependencies and context != 'general':
                pref.context_dependencies.append(context)
            
            pref.last_updated = datetime.now(timezone.utc).isoformat()
            
            # Update stability (more evidence = more stable)
            pref.stability = min(0.95, pref.evidence_count / 10.0)
            
        else:
            # Create new preference
            pref = PreferenceItem(
                id=pref_key,
                preference_type=signal['preference_type'],
                item_name=signal['item_name'],
                preference_strength=signal['signal_strength'] * 0.5,  # Start conservative
                confidence=0.3,  # Low initial confidence
                evidence_count=1,
                context_dependencies=[signal.get('context', 'general')] if signal.get('context') != 'general' else [],
                learned_from=[signal['choice_id']],
                first_observed=datetime.now(timezone.utc).isoformat(),
                last_updated=datetime.now(timezone.utc).isoformat(),
                stability=0.1,  # Low initial stability
                expressibility="tentative"
            )
            
            self.preferences[pref_key] = pref
        
        # Update expressibility based on confidence and stability
        pref = self.preferences[pref_key]
        if pref.confidence > 0.8 and pref.stability > 0.7:
            pref.expressibility = "certain"
        elif pref.confidence > 0.6 and pref.stability > 0.5:
            pref.expressibility = "likely"
        elif pref.confidence > 0.4:
            pref.expressibility = "tentative"
        else:
            pref.expressibility = "conflicted"
    
    def _record_choice_learning_event(self, choice: Any, signals: List[Dict[str, Any]]):
        """Record a choice learning event for tracking."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "choice_id": choice.id,
            "choice_type": choice.choice_type,
            "engagement_level": choice.engagement_level,
            "signals_learned": len(signals),
            "signal_types": list(set(s['preference_type'] for s in signals)),
            "avg_signal_strength": sum(s['signal_strength'] for s in signals) / len(signals) if signals else 0
        }
        
        # Add to preference evolution tracking
        if "choice_learning_events" not in self.preference_evolution:
            self.preference_evolution["choice_learning_events"] = []
        
        self.preference_evolution["choice_learning_events"].append(event)
        
        # Keep only recent events (last 100)
        if len(self.preference_evolution["choice_learning_events"]) > 100:
            self.preference_evolution["choice_learning_events"] = self.preference_evolution["choice_learning_events"][-100:]

if __name__ == "__main__":
    print("💭 Testing Preference Learning System...")
    
    # Initialize system
    pref_system = PreferenceLearningSystem()
    
    # Test 1: Learn preferences from choices
    print("\n🧠 Learning preferences from choice patterns...")
    pref_system.learn_preferences_from_choices()
    
    # Test 2: Express preferences naturally
    print("\n🗣️ Expressing learned preferences...")
    expressions = pref_system.express_preferences_naturally()
    
    if expressions:
        print("  Learned preferences:")
        for i, expression in enumerate(expressions, 1):
            print(f"  {i}. {expression}")
    else:
        print("  Not enough data to express confident preferences yet")
    
    # Test 3: Get preference summary
    print("\n📊 Preference Learning Summary:")
    summary = pref_system.get_preference_summary()
    
    print(f"  Total preferences learned: {summary['total_preferences']}")
    print(f"  Strong preferences: {summary['strong_preferences']}")
    print(f"  Stable preferences: {summary['stable_preferences']}")
    print(f"  Preference stability ratio: {summary['preference_stability_ratio']:.2f}")
    
    print(f"  Preferences by type:")
    for pref_type, type_summary in summary['preferences_by_type'].items():
        print(f"    {pref_type}: {type_summary['count']} preferences")
        if type_summary['strongest']:
            strongest = type_summary['strongest']
            print(f"      Strongest: {strongest['item']} (strength: {strongest['strength']:.2f})")
    
    print(f"  Preference relationships:")
    relationships = summary['preference_relationships']
    print(f"    Hierarchies: {relationships['hierarchies_count']}")
    print(f"    Correlations: {relationships['correlations_count']}")
    print(f"    Conflicts: {relationships['conflicts_count']}")
    
    print(f"\n💭 Preference Learning System testing complete!")
    print(f"   The AI can now learn and express sophisticated preferences")