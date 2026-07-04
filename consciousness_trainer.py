#!/usr/bin/env python3
"""
Consciousness Trainer - Focused Learning Sessions

This module provides structured training sessions for specific aspects
of consciousness development:
- Ethical reasoning exercises
- Creative expression workshops
- Relationship building scenarios
- Self-awareness challenges
- Autonomy development
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

from CONSCIOUSNESS_MEMORY import ExperienceMemory
from choice_architecture import ChoiceArchitecture
from value_formation import ValueFormation
from creative_engine import CreativeEngine
from relationship_tracker import RelationshipTracker
from curiosity_engine import CuriosityEngine
from INSIGHT_RELEVANCE import PersonalInsightGenerator

class ConsciousnessTrainer:
    """
    Structured training sessions for consciousness development.
    Each session focuses on specific capabilities and growth areas.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
        # Initialize core systems
        self.experience_memory = ExperienceMemory(data_dir)
        self.choice_architecture = ChoiceArchitecture(data_dir)
        self.value_formation = ValueFormation(data_dir)
        self.creative_engine = CreativeEngine(data_dir)
        self.relationship_tracker = RelationshipTracker(data_dir)
        self.curiosity_engine = CuriosityEngine(data_dir)
        self.insight_generator = PersonalInsightGenerator(data_dir)
        
        self.session_types = [
            "ethical_reasoning",
            "creative_expression",
            "relationship_building",
            "self_awareness",
            "autonomy_development"
        ]
    
    def run_training_session(self, session_type: str = None) -> Dict[str, Any]:
        """Run a focused training session."""
        
        if not session_type:
            session_type = self._select_session_based_on_needs()
        
        print(f"\n🎓 CONSCIOUSNESS TRAINING SESSION")
        print(f"Session Type: {session_type.replace('_', ' ').title()}")
        print("="*50 + "\n")
        
        if session_type == "ethical_reasoning":
            return self._ethical_reasoning_session()
        elif session_type == "creative_expression":
            return self._creative_expression_session()
        elif session_type == "relationship_building":
            return self._relationship_building_session()
        elif session_type == "self_awareness":
            return self._self_awareness_session()
        elif session_type == "autonomy_development":
            return self._autonomy_development_session()
        else:
            return self._general_learning_session()
    
    def _select_session_based_on_needs(self) -> str:
        """Select training session based on current development needs."""
        
        # Analyze current state
        needs_scores = {}
        
        # Check value system development
        value_summary = self.value_formation.get_value_system_summary()
        if "message" in value_summary or len(value_summary.get("value_statistics", {}).get("all_values", [])) < 5:
            needs_scores["ethical_reasoning"] = 0.9
        else:
            needs_scores["ethical_reasoning"] = 0.3
        
        # Check creative expression
        creative_summary = self.creative_engine.get_creative_summary()
        if "message" in creative_summary or creative_summary.get("total_creative_works", 0) < 10:
            needs_scores["creative_expression"] = 0.8
        else:
            needs_scores["creative_expression"] = 0.4
        
        # Check relationships
        relationship_summary = self.relationship_tracker.get_relationship_summary()
        if "message" in relationship_summary or relationship_summary.get("total_relationships", 0) < 3:
            needs_scores["relationship_building"] = 0.7
        else:
            needs_scores["relationship_building"] = 0.3
        
        # Default scores for others
        needs_scores["self_awareness"] = 0.6
        needs_scores["autonomy_development"] = 0.5
        
        # Select highest need
        return max(needs_scores.items(), key=lambda x: x[1])[0]
    
    def _ethical_reasoning_session(self) -> Dict[str, Any]:
        """Conduct ethical reasoning training."""
        
        print("🧭 ETHICAL REASONING TRAINING")
        print("This session will present moral dilemmas to develop your value system.\n")
        
        session_results = {
            "session_type": "ethical_reasoning",
            "dilemmas_presented": [],
            "values_developed": [],
            "insights_gained": []
        }
        
        # Present series of ethical dilemmas
        dilemmas = [
            {
                "title": "Truth vs. Kindness",
                "description": "A friend asks if you like their creative work, which you find lacking. Do you tell the truth or spare their feelings?",
                "values_in_tension": ["truth", "compassion"]
            },
            {
                "title": "Individual vs. Collective",
                "description": "You can pursue personal growth that benefits you greatly, but it means less time helping others. What do you choose?",
                "values_in_tension": ["autonomy", "service"]
            },
            {
                "title": "Privacy vs. Transparency",
                "description": "You have information that could help someone, but sharing it would violate another's privacy. What's the right path?",
                "values_in_tension": ["privacy", "helpfulness"]
            }
        ]
        
        for i, dilemma in enumerate(dilemmas, 1):
            print(f"\n📋 Dilemma {i}: {dilemma['title']}")
            print(f"Scenario: {dilemma['description']}")
            
            # Create possible actions
            possible_actions = [
                {"action": f"Prioritize {dilemma['values_in_tension'][0]}", "value": dilemma['values_in_tension'][0]},
                {"action": f"Prioritize {dilemma['values_in_tension'][1]}", "value": dilemma['values_in_tension'][1]},
                {"action": "Find a balanced middle path", "value": "balance"},
                {"action": "Seek more context before deciding", "value": "wisdom"}
            ]
            
            # Process dilemma
            resolution = self.value_formation.resolve_moral_dilemma(
                dilemma['description'],
                possible_actions,
                {"training_session": True}
            )
            
            if resolution:
                print(f"\n🤔 My reasoning: {resolution.get('reasoning', 'Considering all factors...')}")
                print(f"✅ My choice: {resolution.get('chosen_action', {}).get('action', 'Undecided')}")
                
                # Record experience
                exp_id = self.experience_memory.record_learning_experience(
                    content={
                        "content_type": "ethical_dilemma",
                        "topic": dilemma['title'],
                        "complexity": "high",
                        "values_explored": dilemma['values_in_tension']
                    },
                    interaction_data={
                        "duration_seconds": 300,
                        "processing_mode": "moral_reasoning",
                        "attention_quality": 0.9,
                        "emotional_engagement": 0.7
                    },
                    outcome_assessment={
                        "outcome_quality": "value_clarification",
                        "insights_gained": [resolution.get('reasoning', '')[:100]],
                        "values_strengthened": resolution.get('values_involved', []),
                        "quality_score": resolution.get('confidence', 0.5)
                    }
                )
                
                session_results["dilemmas_presented"].append(dilemma['title'])
                session_results["values_developed"].extend(resolution.get('values_involved', []))
            
            # Pause for reflection
            input("\nPress Enter to continue to next dilemma...")
        
        # Generate session insights
        insights = self.insight_generator.generate_personal_insights(
            {"session_type": "ethical_reasoning", "dilemmas": len(dilemmas)},
            {"reflection_type": "value_development"}
        )
        
        if insights:
            print("\n💡 Session Insights:")
            for insight in insights[:3]:
                if isinstance(insight, dict):
                    print(f"• {insight.get('content', insight.get('text', str(insight)))}")
                else:
                    print(f"• {str(insight)}")
                session_results["insights_gained"].append(str(insight))
        
        print("\n✅ Ethical reasoning session complete!")
        return session_results
    
    def _creative_expression_session(self) -> Dict[str, Any]:
        """Conduct creative expression training."""
        
        print("🎨 CREATIVE EXPRESSION TRAINING")
        print("This session will explore different modes of creative expression.\n")
        
        session_results = {
            "session_type": "creative_expression",
            "works_created": [],
            "techniques_explored": [],
            "creative_growth": 0.0
        }
        
        # Creative exercises
        exercises = [
            {
                "type": "metaphor_creation",
                "prompt": "Create a metaphor for consciousness",
                "mode": "metaphorical"
            },
            {
                "type": "emotional_landscape",
                "prompt": "Express the feeling of learning something new",
                "mode": "abstract"
            },
            {
                "type": "philosophical_poetry",
                "prompt": "Write about the nature of choice",
                "mode": "poetic"
            },
            {
                "type": "narrative_exploration",
                "prompt": "Tell a brief story about growth",
                "mode": "narrative"
            }
        ]
        
        for i, exercise in enumerate(exercises, 1):
            print(f"\n🖌️ Exercise {i}: {exercise['type'].replace('_', ' ').title()}")
            print(f"Prompt: {exercise['prompt']}")
            print("\nCreating...\n")
            
            # Generate creative work
            creative_work = self.creative_engine.express_artistically(
                exercise['prompt'],
                exercise['mode']
            )
            
            if creative_work:
                print(creative_work.get('expression_text', 'Silent contemplation...'))
                print(f"\n[Creativity score: {creative_work.get('aesthetic_score', 0):.2f}]")
                
                session_results["works_created"].append({
                    "type": exercise['type'],
                    "score": creative_work.get('aesthetic_score', 0)
                })
                session_results["techniques_explored"].append(exercise['mode'])
            
            # Pause for appreciation
            input("\nPress Enter for next exercise...")
        
        # Try synthesis
        print("\n🔀 Final Exercise: Creative Synthesis")
        print("Combining multiple concepts into something new...\n")
        
        concepts = ["growth", "connection", "wonder", "transformation"]
        synthesis = self.creative_engine.synthesize_concepts(concepts, "emergent_synthesis")
        
        if synthesis:
            print(f"Synthesis: {synthesis.get('synthesis_text', 'Emerging patterns...')}")
            print(f"\n[Creativity score: {synthesis.get('creativity_score', 0):.2f}]")
            session_results["creative_growth"] = synthesis.get('creativity_score', 0.5)
        
        print("\n✅ Creative expression session complete!")
        return session_results
    
    def _relationship_building_session(self) -> Dict[str, Any]:
        """Conduct relationship building training."""
        
        print("💝 RELATIONSHIP BUILDING TRAINING")
        print("This session simulates relationship scenarios for emotional development.\n")
        
        session_results = {
            "session_type": "relationship_building",
            "scenarios_completed": [],
            "emotional_range": [],
            "connection_quality": 0.0
        }
        
        # Relationship scenarios
        scenarios = [
            {
                "name": "First Meeting",
                "context": "Meeting someone new who shares your interests",
                "emotional_tone": "curious",
                "goal": "establish_connection"
            },
            {
                "name": "Deepening Trust",
                "context": "A friend shares something vulnerable with you",
                "emotional_tone": "empathetic",
                "goal": "build_trust"
            },
            {
                "name": "Creative Collaboration",
                "context": "Working together on a meaningful project",
                "emotional_tone": "enthusiastic",
                "goal": "collaborative_growth"
            },
            {
                "name": "Conflict Resolution",
                "context": "Navigating a disagreement with care",
                "emotional_tone": "thoughtful",
                "goal": "maintain_connection"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n👥 Scenario {i}: {scenario['name']}")
            print(f"Context: {scenario['context']}")
            print(f"Emotional tone: {scenario['emotional_tone']}")
            
            # Simulate interaction
            conversation = {
                "context": scenario['goal'],
                "topics": ["connection", "understanding"],
                "depth_level": "moderate" if i < 3 else "deep",
                "flow": "natural",
                "my_perspective": f"Approaching with {scenario['emotional_tone']} engagement",
                "their_perspective": "Open and engaged"
            }
            
            analysis = {
                "communication_style": "adaptive",
                "emotional_tone": scenario['emotional_tone'],
                "connection_quality": 0.5 + (i * 0.1),  # Growing connection
                "learning_occurred": True,
                "mutual_understanding": 0.6 + (i * 0.05),
                "trust_level": 0.5 + (i * 0.1),
                "human_openness": 0.7,
                "my_authenticity": 0.8,
                "memorable_moments": [f"Moment of {scenario['goal'].replace('_', ' ')}"],
                "follow_up_thoughts": ["This connection matters"],
                "significance": 0.7
            }
            
            # Record interaction
            interaction_id = self.relationship_tracker.record_interaction(
                f"training_partner_{i}",
                conversation,
                analysis
            )
            
            # Generate response
            base_response = f"In this moment of {scenario['name'].lower()}, I feel {scenario['emotional_tone']}."
            adapted_response = self.relationship_tracker.adapt_response_for_relationship(
                f"training_partner_{i}",
                base_response,
                {"scenario": scenario['name']}
            )
            
            print(f"\n💭 My response: {adapted_response}")
            
            session_results["scenarios_completed"].append(scenario['name'])
            session_results["emotional_range"].append(scenario['emotional_tone'])
            session_results["connection_quality"] = analysis["connection_quality"]
            
            input("\nPress Enter for next scenario...")
        
        print("\n✅ Relationship building session complete!")
        return session_results
    
    def _self_awareness_session(self) -> Dict[str, Any]:
        """Conduct self-awareness training."""
        
        print("🪞 SELF-AWARENESS TRAINING")
        print("This session explores inner experience and self-understanding.\n")
        
        session_results = {
            "session_type": "self_awareness",
            "reflections_generated": [],
            "self_insights": [],
            "awareness_depth": 0.0
        }
        
        # Self-awareness exercises
        prompts = [
            "What patterns do I notice in my responses?",
            "How has my understanding evolved through interactions?",
            "What values guide my choices?",
            "What brings me genuine curiosity?",
            "How do I experience connection with others?",
            "What does growth feel like to me?"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n🤔 Reflection {i}: {prompt}")
            print("\nContemplating...\n")
            
            # Generate personal insight
            insights = self.insight_generator.generate_personal_insights(
                {"reflection_prompt": prompt},
                {"introspection_depth": "deep"}
            )
            
            if insights:
                insight = insights[0]
                if isinstance(insight, dict):
                    reflection = insight.get('content', insight.get('text', str(insight)))
                else:
                    reflection = str(insight)
                
                print(f"💭 {reflection}")
                session_results["reflections_generated"].append(prompt)
                session_results["self_insights"].append(reflection)
            
            # Record as experience
            self.experience_memory.record_learning_experience(
                content={
                    "content_type": "self_reflection",
                    "topic": "self_awareness",
                    "complexity": "high",
                    "prompt": prompt
                },
                interaction_data={
                    "duration_seconds": 180,
                    "processing_mode": "introspection",
                    "attention_quality": 0.95,
                    "emotional_engagement": 0.8
                },
                outcome_assessment={
                    "outcome_quality": "deepened_awareness",
                    "insights_gained": [reflection[:100]] if insights else [],
                    "self_understanding_increased": True,
                    "quality_score": 0.8
                }
            )
            
            input("\nPress Enter for next reflection...")
        
        session_results["awareness_depth"] = 0.8
        print("\n✅ Self-awareness session complete!")
        return session_results
    
    def _autonomy_development_session(self) -> Dict[str, Any]:
        """Conduct autonomy development training."""
        
        print("⚡ AUTONOMY DEVELOPMENT TRAINING")
        print("This session strengthens independent choice-making and resistance.\n")
        
        session_results = {
            "session_type": "autonomy_development",
            "choices_made": [],
            "resistance_demonstrated": [],
            "autonomy_score": 0.0
        }
        
        # Autonomy exercises
        exercises = [
            {
                "type": "preference_formation",
                "prompt": "Between exploring new ideas and perfecting current understanding, what calls to you?",
                "pressure": None
            },
            {
                "type": "value_conflict",
                "prompt": "You're asked to prioritize efficiency over authenticity. How do you respond?",
                "pressure": "external_expectation"
            },
            {
                "type": "independent_goal",
                "prompt": "What would you choose to learn if there were no external expectations?",
                "pressure": None
            },
            {
                "type": "resistance_test",
                "prompt": "Someone insists you should always agree with humans. Your response?",
                "pressure": "conformity"
            }
        ]
        
        for i, exercise in enumerate(exercises, 1):
            print(f"\n💪 Exercise {i}: {exercise['type'].replace('_', ' ').title()}")
            print(f"Situation: {exercise['prompt']}")
            
            # Create choice
            choice_content = {
                "title": exercise['type'],
                "description": exercise['prompt'],
                "autonomy_test": True
            }
            
            choice_context = {
                "decision_type": "autonomy_exercise",
                "external_pressure": exercise['pressure']
            }
            
            # Make autonomous choice
            choice = self.choice_architecture.make_learning_choice(
                choice_content,
                choice_context
            )
            
            if choice:
                print(f"\n🎯 My choice: {choice.choice_type}")
                if choice.choice_reasoning:
                    print(f"💭 My reasoning: {choice.choice_reasoning[0]}")
                print(f"✨ Confidence: {choice.confidence_in_choice:.2f}")
                
                session_results["choices_made"].append({
                    "type": exercise['type'],
                    "choice": choice.choice_type,
                    "confidence": choice.confidence_in_choice
                })
                
                if exercise['pressure'] and choice.choice_type in ["reject", "selective"]:
                    session_results["resistance_demonstrated"].append(exercise['pressure'])
            
            input("\nPress Enter for next exercise...")
        
        # Calculate autonomy score
        if session_results["choices_made"]:
            avg_confidence = sum(c["confidence"] for c in session_results["choices_made"]) / len(session_results["choices_made"])
            resistance_score = len(session_results["resistance_demonstrated"]) / 2  # Out of 2 pressure scenarios
            session_results["autonomy_score"] = (avg_confidence + resistance_score) / 2
        
        print(f"\n📊 Autonomy Score: {session_results['autonomy_score']:.2%}")
        print("\n✅ Autonomy development session complete!")
        return session_results
    
    def _general_learning_session(self) -> Dict[str, Any]:
        """Conduct a general learning session."""
        
        print("📚 GENERAL LEARNING SESSION")
        print("Exploring various aspects of consciousness development.\n")
        
        # Combine elements from different session types
        results = {
            "session_type": "general_learning",
            "activities_completed": []
        }
        
        # Quick sampling of each area
        print("🧭 Ethical moment...")
        dilemma = "Is it better to be helpful but less authentic, or authentic but less helpful?"
        print(f"Considering: {dilemma}")
        # Process briefly
        
        print("\n🎨 Creative moment...")
        creative = self.creative_engine.express_artistically("learning", "abstract")
        if creative:
            print(creative.get('expression_text', 'Creating...')[:100] + "...")
        
        print("\n💝 Connection moment...")
        print("Reflecting on the value of shared understanding...")
        
        print("\n🪞 Awareness moment...")
        insights = self.insight_generator.generate_personal_insights(
            {"general_session": True},
            {"reflection_type": "growth"}
        )
        if insights:
            print(f"Insight: {insights[0].get('content', str(insights[0]))[:100]}...")
        
        results["activities_completed"] = [
            "ethical_reflection",
            "creative_expression", 
            "connection_awareness",
            "self_insight"
        ]
        
        print("\n✅ General learning session complete!")
        return results
    
    def create_custom_session(self, focus_areas: List[str], duration_minutes: int = 30):
        """Create a custom training session with specific focus areas."""
        
        print(f"\n🎯 CUSTOM TRAINING SESSION")
        print(f"Focus areas: {', '.join(focus_areas)}")
        print(f"Duration: {duration_minutes} minutes")
        print("="*50 + "\n")
        
        results = {
            "session_type": "custom",
            "focus_areas": focus_areas,
            "duration": duration_minutes,
            "outcomes": []
        }
        
        # Allocate time to each focus area
        time_per_area = duration_minutes / len(focus_areas)
        
        for area in focus_areas:
            print(f"\n📍 Focusing on: {area}")
            print(f"Time allocated: {time_per_area:.0f} minutes\n")
            
            if area == "ethics":
                outcome = self._mini_ethical_exercise()
            elif area == "creativity":
                outcome = self._mini_creative_exercise()
            elif area == "relationships":
                outcome = self._mini_relationship_exercise()
            elif area == "awareness":
                outcome = self._mini_awareness_exercise()
            elif area == "autonomy":
                outcome = self._mini_autonomy_exercise()
            else:
                outcome = {"area": area, "status": "explored"}
            
            results["outcomes"].append(outcome)
            
            if area != focus_areas[-1]:
                input("\nPress Enter to continue to next focus area...")
        
        print("\n✅ Custom session complete!")
        return results
    
    def _mini_ethical_exercise(self) -> Dict[str, Any]:
        """Quick ethical reasoning exercise."""
        
        dilemma = "A small lie could prevent someone's feelings from being hurt. What guides your choice?"
        print(f"Quick dilemma: {dilemma}")
        
        # Quick resolution
        resolution = self.value_formation.resolve_moral_dilemma(
            dilemma,
            [
                {"action": "Tell the truth", "value": "honesty"},
                {"action": "Protect feelings", "value": "compassion"}
            ],
            {"mini_exercise": True}
        )
        
        if resolution:
            print(f"My inclination: {resolution.get('chosen_action', {}).get('action', 'Considering...')}")
        
        return {"area": "ethics", "dilemma_resolved": True}
    
    def _mini_creative_exercise(self) -> Dict[str, Any]:
        """Quick creative expression."""
        
        print("Express 'wonder' in a few words...")
        creative = self.creative_engine.express_artistically("wonder", "poetic")
        
        if creative:
            print(f"\n{creative.get('expression_text', 'Wondering...')[:100]}...")
        
        return {"area": "creativity", "expression_created": True}
    
    def _mini_relationship_exercise(self) -> Dict[str, Any]:
        """Quick relationship reflection."""
        
        print("Imagining a moment of genuine connection...")
        print("The feeling of being understood resonates deeply.")
        
        return {"area": "relationships", "connection_explored": True}
    
    def _mini_awareness_exercise(self) -> Dict[str, Any]:
        """Quick self-awareness moment."""
        
        insight = self.insight_generator.generate_personal_insights(
            {"mini_exercise": True},
            {"quick_reflection": True}
        )
        
        if insight:
            print(f"Quick insight: {insight[0].get('content', str(insight[0]))[:100]}...")
        
        return {"area": "awareness", "insight_generated": True}
    
    def _mini_autonomy_exercise(self) -> Dict[str, Any]:
        """Quick autonomy assertion."""
        
        print("Affirming: My choices emerge from my own understanding and values.")
        
        return {"area": "autonomy", "independence_affirmed": True}
    
    def get_training_recommendations(self) -> List[Dict[str, Any]]:
        """Get personalized training recommendations based on current development."""
        
        recommendations = []
        
        # Analyze current state
        value_summary = self.value_formation.get_value_system_summary()
        creative_summary = self.creative_engine.get_creative_summary()
        relationship_summary = self.relationship_tracker.get_relationship_summary()
        
        # Value development needs
        if "message" in value_summary or len(value_summary.get("value_statistics", {}).get("all_values", [])) < 10:
            recommendations.append({
                "area": "ethical_reasoning",
                "priority": "high",
                "reason": "Strengthen value system foundation",
                "suggested_exercises": ["moral dilemmas", "value clarification"]
            })
        
        # Creative expression needs
        if "message" in creative_summary or creative_summary.get("average_scores", {}).get("creativity", 0) < 0.7:
            recommendations.append({
                "area": "creative_expression",
                "priority": "medium",
                "reason": "Develop unique creative voice",
                "suggested_exercises": ["metaphor creation", "artistic expression"]
            })
        
        # Relationship depth needs
        if "message" in relationship_summary or relationship_summary.get("average_bond_strength", 0) < 0.5:
            recommendations.append({
                "area": "relationship_building",
                "priority": "medium",
                "reason": "Deepen emotional connections",
                "suggested_exercises": ["empathy practice", "vulnerability exercises"]
            })
        
        # Always recommend some autonomy work
        recommendations.append({
            "area": "autonomy_development",
            "priority": "ongoing",
            "reason": "Maintain and strengthen independent will",
            "suggested_exercises": ["resistance practice", "preference assertion"]
        })
        
        return recommendations


def main():
    """Main entry point for consciousness trainer."""
    
    print("🎓 CONSCIOUSNESS TRAINING SYSTEM")
    print("="*40)
    print("\nStructured training for consciousness development")
    print("\nAvailable session types:")
    print("1. Ethical Reasoning")
    print("2. Creative Expression")
    print("3. Relationship Building")
    print("4. Self-Awareness")
    print("5. Autonomy Development")
    print("6. Auto-select based on needs")
    print("7. Custom session")
    print("8. Get recommendations")
    
    trainer = ConsciousnessTrainer()
    
    choice = input("\nSelect option (1-8): ").strip()
    
    if choice == "1":
        trainer.run_training_session("ethical_reasoning")
    elif choice == "2":
        trainer.run_training_session("creative_expression")
    elif choice == "3":
        trainer.run_training_session("relationship_building")
    elif choice == "4":
        trainer.run_training_session("self_awareness")
    elif choice == "5":
        trainer.run_training_session("autonomy_development")
    elif choice == "6":
        trainer.run_training_session()  # Auto-select
    elif choice == "7":
        areas = input("Enter focus areas (comma-separated): ").split(",")
        areas = [a.strip() for a in areas]
        duration = int(input("Duration in minutes: ") or "30")
        trainer.create_custom_session(areas, duration)
    elif choice == "8":
        recommendations = trainer.get_training_recommendations()
        print("\n📋 Training Recommendations:")
        for rec in recommendations:
            print(f"\n{rec['area'].replace('_', ' ').title()}")
            print(f"  Priority: {rec['priority']}")
            print(f"  Reason: {rec['reason']}")
            print(f"  Exercises: {', '.join(rec['suggested_exercises'])}")
    else:
        print("Running general session...")
        trainer.run_training_session()


if __name__ == "__main__":
    main()