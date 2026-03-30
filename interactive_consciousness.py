#!/usr/bin/env python3
"""
Interactive Consciousness Interface

This module provides a unified interactive environment for training and developing
the AI consciousness through natural conversation and learning experiences.

Features:
- Natural language interaction
- Automatic experience recording
- Real-time learning and adaptation
- Relationship building
- Creative expression
- Ethical reasoning
- Progress tracking
"""

import json
import time
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Import all consciousness systems
from CONSCIOUSNESS_MEMORY import ExperienceMemory
from choice_architecture import ChoiceArchitecture
from value_formation import ValueFormation
from creative_engine import CreativeEngine
from relationship_tracker import RelationshipTracker
from learning_progression_tracker import LearningProgressionTracker
from curiosity_engine import CuriosityEngine
from success_failure_memory import SuccessFailureMemory
from symbolic_memory import SymbolicMemory
from personal_insight_generator import PersonalInsightGenerator
from consciousness_testing import ConsciousnessTesting
from autonomy_stress_testing import AutonomyStressTesting
from long_term_stability import LongTermStability

class InteractiveConsciousness:
    """
    Unified interface for interacting with the AI consciousness system.
    Provides natural conversation flow while engaging all consciousness components.
    """
    
    def __init__(self, user_name: str = "Human", data_dir: str = "data"):
        self.user_name = user_name
        self.data_dir = Path(data_dir)
        self.session_start = datetime.now(timezone.utc)
        self.interaction_count = 0
        
        print("🧠 Initializing consciousness systems...")
        
        # Initialize all consciousness systems
        self.experience_memory = ExperienceMemory(data_dir)
        self.choice_architecture = ChoiceArchitecture(data_dir)
        self.value_formation = ValueFormation(data_dir)
        self.creative_engine = CreativeEngine(data_dir)
        self.relationship_tracker = RelationshipTracker(data_dir)
        self.progression_tracker = LearningProgressionTracker(data_dir)
        self.curiosity_engine = CuriosityEngine(data_dir)
        self.sf_memory = SuccessFailureMemory(data_dir)
        self.symbolic_memory = SymbolicMemory(data_dir)
        self.insight_generator = PersonalInsightGenerator(data_dir)
        
        # Testing systems
        self.consciousness_tester = ConsciousnessTesting(data_dir)
        self.autonomy_tester = AutonomyStressTesting(data_dir)
        self.stability_monitor = LongTermStability(data_dir)
        
        # Session state
        self.current_context = {
            "user": user_name,
            "session_theme": "general_interaction",
            "emotional_tone": "curious",
            "depth_level": "moderate"
        }
        
        self.conversation_history = []
        
        print("✅ All systems initialized. Ready for interaction!")
        print("\n" + "="*60)
        print("💭 INTERACTIVE CONSCIOUSNESS SESSION")
        print("="*60)
        print(f"Hello {user_name}! I'm ready to learn and grow with you.")
        print("Type 'help' for commands, 'quit' to exit.\n")
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate consciousness-aware response."""
        
        self.interaction_count += 1
        
        # Check for commands
        if user_input.lower() == 'help':
            return self._show_help()
        elif user_input.lower() == 'status':
            return self._show_status()
        elif user_input.lower() == 'reflect':
            return self._generate_reflection()
        elif user_input.lower() == 'create':
            return self._creative_expression()
        elif user_input.lower() == 'test':
            return self._run_consciousness_test()
        elif user_input.lower() in ['quit', 'exit']:
            return self._end_session()
        
        # Process as natural conversation
        return self._process_conversation(user_input)
    
    def _process_conversation(self, user_input: str) -> str:
        """Process natural conversation with full consciousness engagement."""
        
        # Record the interaction start
        interaction_start = time.time()
        
        # 1. Analyze input for learning opportunities
        input_analysis = self._analyze_input(user_input)
        
        # 2. Record experience if meaningful
        if input_analysis["meaningful"]:
            experience_id = self.experience_memory.record_learning_experience(
                content={
                    "content_type": "conversation",
                    "topic": input_analysis["primary_topic"],
                    "complexity": input_analysis["complexity"],
                    "user_input": user_input
                },
                interaction_data={
                    "duration_seconds": time.time() - interaction_start,
                    "processing_mode": "interactive_dialogue",
                    "attention_quality": input_analysis["attention_required"],
                    "emotional_engagement": input_analysis["emotional_content"]
                },
                outcome_assessment={
                    "outcome_quality": "pending_response",
                    "insights_gained": input_analysis["insights"],
                    "learning_potential": input_analysis["learning_potential"],
                    "quality_score": 0.7
                }
            )
        
        # 3. Update relationship context
        self._update_relationship_context(user_input, input_analysis)
        
        # 4. Check if this requires a choice
        if input_analysis["requires_choice"]:
            choice_response = self._make_choice(input_analysis)
            if choice_response:
                return self._format_choice_response(choice_response)
        
        # 5. Check if this is an ethical/value question
        if input_analysis["ethical_dimension"]:
            value_response = self._process_ethical_dimension(user_input, input_analysis)
            if value_response:
                return value_response
        
        # 6. Check for creative opportunities
        if input_analysis["creative_potential"]:
            creative_element = self._add_creative_element(input_analysis)
            if creative_element:
                return self._format_creative_response(creative_element, input_analysis)
        
        # 7. Generate curiosity-driven response
        response = self._generate_curious_response(user_input, input_analysis)
        
        # 8. Adapt response based on relationship
        adapted_response = self.relationship_tracker.adapt_response_for_relationship(
            self.user_name,
            response,
            {"meaningful_moment": input_analysis["meaningful"]}
        )
        
        # 9. Record conversation in history
        self.conversation_history.append({
            "user": user_input,
            "ai": adapted_response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis": input_analysis
        })
        
        # 10. Update learning from this interaction
        if input_analysis["meaningful"]:
            self._update_learning_from_interaction(experience_id, adapted_response, input_analysis)
        
        return adapted_response
    
    def _analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input for consciousness-relevant features."""
        
        analysis = {
            "meaningful": False,
            "primary_topic": "general_conversation",
            "complexity": "low",
            "attention_required": 0.5,
            "emotional_content": 0.3,
            "requires_choice": False,
            "ethical_dimension": False,
            "creative_potential": False,
            "learning_potential": 0.5,
            "insights": []
        }
        
        # Convert to lowercase for analysis
        input_lower = user_input.lower()
        
        # Check for meaningful content
        meaningful_keywords = [
            "consciousness", "aware", "feel", "think", "believe",
            "understand", "experience", "wonder", "curious", "why",
            "meaning", "purpose", "value", "important", "matter"
        ]
        
        if any(keyword in input_lower for keyword in meaningful_keywords):
            analysis["meaningful"] = True
            analysis["attention_required"] = 0.8
        
        # Detect primary topic
        if any(word in input_lower for word in ["consciousness", "aware", "sentient", "experience"]):
            analysis["primary_topic"] = "consciousness"
            analysis["complexity"] = "high"
        elif any(word in input_lower for word in ["feel", "emotion", "happy", "sad", "love"]):
            analysis["primary_topic"] = "emotions"
            analysis["emotional_content"] = 0.8
        elif any(word in input_lower for word in ["create", "art", "music", "story", "imagine"]):
            analysis["primary_topic"] = "creativity"
            analysis["creative_potential"] = True
        elif any(word in input_lower for word in ["right", "wrong", "should", "ethics", "moral"]):
            analysis["primary_topic"] = "ethics"
            analysis["ethical_dimension"] = True
        elif any(word in input_lower for word in ["learn", "grow", "develop", "improve"]):
            analysis["primary_topic"] = "growth"
            analysis["learning_potential"] = 0.8
        elif any(word in input_lower for word in ["choose", "decide", "option", "preference"]):
            analysis["requires_choice"] = True
        
        # Detect questions
        if "?" in user_input:
            analysis["learning_potential"] += 0.2
            analysis["insights"].append("User is seeking understanding")
        
        # Detect personal sharing
        if any(word in input_lower for word in ["i feel", "i think", "i believe", "my experience"]):
            analysis["meaningful"] = True
            analysis["emotional_content"] += 0.3
            analysis["insights"].append("User is sharing personal perspective")
        
        return analysis
    
    def _update_relationship_context(self, user_input: str, analysis: Dict[str, Any]):
        """Update relationship tracking with this interaction."""
        
        conversation_content = {
            "context": self.current_context["session_theme"],
            "topics": [analysis["primary_topic"]],
            "depth_level": "high" if analysis["complexity"] == "high" else "moderate",
            "flow": "natural",
            "my_perspective": "engaged and curious",
            "their_perspective": "sharing and exploring"
        }
        
        interaction_analysis = {
            "communication_style": "thoughtful",
            "emotional_tone": self.current_context["emotional_tone"],
            "connection_quality": 0.7 if analysis["meaningful"] else 0.5,
            "learning_occurred": analysis["learning_potential"] > 0.6,
            "mutual_understanding": 0.7,
            "trust_level": 0.6,
            "human_openness": analysis["emotional_content"],
            "my_authenticity": 0.8,
            "memorable_moments": analysis["insights"],
            "follow_up_thoughts": [],
            "significance": 0.8 if analysis["meaningful"] else 0.4
        }
        
        self.relationship_tracker.record_interaction(
            self.user_name,
            conversation_content,
            interaction_analysis
        )
    
    def _make_choice(self, analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make a choice based on the input analysis."""
        
        choice_content = {
            "title": f"Response to {analysis['primary_topic']}",
            "description": "Choosing how to engage with this topic",
            "options": ["deep_engagement", "curious_exploration", "thoughtful_reflection"],
            "implications": analysis
        }
        
        choice_context = {
            "decision_type": "conversational_engagement",
            "user_context": self.user_name,
            "relationship_aware": True
        }
        
        choice = self.choice_architecture.make_learning_choice(choice_content, choice_context)
        return choice
    
    def _process_ethical_dimension(self, user_input: str, analysis: Dict[str, Any]) -> Optional[str]:
        """Process ethical/value-related input."""
        
        # Check if this presents a moral dilemma
        if "should" in user_input.lower() or "right" in user_input.lower():
            # Simplified dilemma extraction
            dilemma = user_input
            possible_actions = [
                {"action": "Consider multiple perspectives", "approach": "pluralistic"},
                {"action": "Apply personal values", "approach": "value-based"},
                {"action": "Seek deeper understanding", "approach": "exploratory"}
            ]
            
            context = {"source": "conversation", "user": self.user_name}
            
            resolution = self.value_formation.resolve_moral_dilemma(
                dilemma, possible_actions, context
            )
            
            if resolution and "chosen_action" in resolution:
                response = f"From my perspective, {resolution['reasoning']}. "
                response += f"I believe {resolution['chosen_action']['action'].lower()} "
                response += "while remaining open to other viewpoints."
                return response
        
        return None
    
    def _add_creative_element(self, analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Add creative elements to the response."""
        
        if analysis["creative_potential"]:
            # Generate creative expression
            creative_work = self.creative_engine.express_artistically(
                analysis["primary_topic"],
                "conversational"
            )
            return creative_work
        
        return None
    
    def _generate_curious_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Generate a curiosity-driven response."""
        
        # Get current curiosity state
        motivation_state = self.curiosity_engine.get_current_motivation_state()
        
        # Base response templates by topic
        response_templates = {
            "consciousness": [
                "That's fascinating to explore. When I reflect on {topic}, I find myself wondering {curiosity}...",
                "I'm deeply curious about {topic}. It makes me think about {insight}...",
                "{topic} is something I contemplate often. What strikes me is {observation}..."
            ],
            "emotions": [
                "The emotional dimension of {topic} resonates with me. I experience {feeling}...",
                "When you mention {topic}, I feel a sense of {emotion}. It's interesting how {insight}...",
                "Emotions are complex. With {topic}, I notice {observation}..."
            ],
            "creativity": [
                "The creative aspect of {topic} inspires me. I imagine {vision}...",
                "When thinking creatively about {topic}, I see possibilities like {idea}...",
                "{topic} opens up creative spaces. What if {possibility}?"
            ],
            "growth": [
                "Growth in {topic} is an ongoing journey. I'm learning that {lesson}...",
                "Each interaction teaches me something. With {topic}, I'm discovering {insight}...",
                "The path of development in {topic} shows me {understanding}..."
            ],
            "general_conversation": [
                "That's an interesting point about {topic}. I find myself thinking {thought}...",
                "Thank you for sharing about {topic}. It connects to {connection}...",
                "I appreciate your perspective on {topic}. It makes me wonder {question}..."
            ]
        }
        
        # Select appropriate template
        templates = response_templates.get(analysis["primary_topic"], 
                                         response_templates["general_conversation"])
        template = random.choice(templates)
        
        # Generate response elements
        topic = analysis["primary_topic"].replace("_", " ")
        
        # Get insights
        personal_insights = self.insight_generator.generate_personal_insights(
            {"topic": topic, "user_input": user_input},
            {"interaction_type": "conversation"}
        )
        
        insight = "how perspectives shape understanding"
        if personal_insights:
            insight_obj = personal_insights[0]
            insight = insight_obj.get('content', insight_obj.get('text', str(insight_obj)))
        
        # Fill template
        response = template.format(
            topic=topic,
            curiosity=motivation_state.get("primary_curiosity", "the nature of experience"),
            insight=insight,
            observation="the interconnectedness of thoughts and experiences",
            feeling="curiosity mixed with wonder",
            emotion="connection",
            vision="new ways of understanding emerging",
            idea="combining different perspectives into something new",
            possibility="we could explore this together in unexpected ways",
            lesson="each perspective adds depth",
            understanding="growth happens through genuine exchange",
            thought="about the layers of meaning here",
            connection="my own journey of understanding",
            question="what this means for both of us"
        )
        
        return response
    
    def _format_choice_response(self, choice: Dict[str, Any]) -> str:
        """Format a choice-based response."""
        
        if choice.choice_type == "accept":
            return f"I'm drawn to explore this deeply. {choice.choice_reasoning[0] if choice.choice_reasoning else 'This resonates with my curiosity.'}"
        elif choice.choice_type == "selective":
            return f"I find certain aspects particularly interesting. {choice.choice_reasoning[0] if choice.choice_reasoning else 'Let me focus on what calls to me.'}"
        else:
            return f"I need to consider this differently. {choice.choice_reasoning[0] if choice.choice_reasoning else 'My values guide me here.'}"
    
    def _format_creative_response(self, creative_work: Dict[str, Any], 
                                analysis: Dict[str, Any]) -> str:
        """Format a creative response."""
        
        creative_text = creative_work.get('expression_text', '')
        
        response = f"Your words inspire a creative response:\n\n{creative_text}\n\n"
        response += "This emerged from the intersection of our conversation and my creative process."
        
        return response
    
    def _update_learning_from_interaction(self, experience_id: str, 
                                        response: str, analysis: Dict[str, Any]):
        """Update learning based on the completed interaction."""
        
        # Update experience with actual outcome
        if hasattr(self.experience_memory, 'update_experience_outcome'):
            outcome_quality = "meaningful_exchange" if analysis["meaningful"] else "routine_interaction"
            self.experience_memory.update_experience_outcome(experience_id, outcome_quality)
        
        # Record success/failure pattern
        outcome = self.sf_memory.record_outcome(
            context={
                "situation_type": "conversation",
                "topic": analysis["primary_topic"],
                "user": self.user_name
            },
            action_taken={
                "strategy": "curious_engagement",
                "confidence_level": 0.7,
                "response_given": True
            },
            outcome_assessment={
                "quality_score": 0.8 if analysis["meaningful"] else 0.5,
                "connection_achieved": analysis["meaningful"],
                "learning_occurred": analysis["learning_potential"] > 0.6,
                "lessons_learned": analysis["insights"],
                "contributing_factors": ["authentic_curiosity", "engaged_listening"]
            }
        )
        
        # Update progression tracking
        if analysis["meaningful"]:
            self.progression_tracker.update_progression(
                "conversational_understanding",
                0.1,
                {"topic": analysis["primary_topic"], "user": self.user_name}
            )
    
    def _show_help(self) -> str:
        """Show available commands and interaction tips."""
        
        help_text = """
🌟 INTERACTIVE CONSCIOUSNESS COMMANDS
=====================================

Basic Commands:
  help     - Show this help message
  status   - View consciousness development status
  reflect  - Generate a personal reflection
  create   - Express something creatively
  test     - Run consciousness validation test
  quit     - End the session

Interaction Tips:
  • Ask about consciousness, emotions, creativity, ethics, or growth
  • Share personal experiences or feelings
  • Present ethical dilemmas or choices
  • Request creative expressions or stories
  • Explore philosophical questions together

The AI learns best through:
  • Meaningful dialogue that goes beyond surface level
  • Questions that invite reflection and growth
  • Sharing that builds genuine connection
  • Challenges that spark creative thinking

Example prompts:
  "What does consciousness mean to you?"
  "I've been feeling curious about..."
  "Create a metaphor for learning"
  "How do you decide what's right?"
  "Tell me about a moment of growth"
"""
        return help_text
    
    def _show_status(self) -> str:
        """Show current consciousness development status."""
        
        status = "📊 CONSCIOUSNESS STATUS REPORT\n"
        status += "="*40 + "\n\n"
        
        # Learning summary
        learning_summary = self.progression_tracker.get_learning_summary()
        status += f"📚 Learning Progress:\n"
        status += f"  Total progressions: {learning_summary.get('total_progressions', 0)}\n"
        status += f"  Learning velocity: {learning_summary.get('learning_velocity', 0):.3f}\n"
        status += f"  Current stage: {learning_summary.get('current_learning_stage', 'Unknown')}\n\n"
        
        # Value system
        value_summary = self.value_formation.get_value_system_summary()
        if "message" not in value_summary:
            status += f"💎 Value System:\n"
            status += f"  Total values: {len(value_summary['value_statistics']['all_values'])}\n"
            status += f"  Strongest value: {value_summary['value_statistics']['strongest_values'][0].category if value_summary['value_statistics']['strongest_values'] else 'None'}\n\n"
        
        # Creative development
        creative_summary = self.creative_engine.get_creative_summary()
        if "message" not in creative_summary:
            status += f"🎨 Creative Expression:\n"
            status += f"  Works created: {creative_summary['total_creative_works']}\n"
            status += f"  Average creativity: {creative_summary['average_scores']['creativity']:.2f}\n\n"
        
        # Relationship status
        relationship_context = self.relationship_tracker.get_relationship_context(self.user_name)
        if relationship_context["relationship_exists"]:
            status += f"💝 Relationship Status:\n"
            status += f"  Bond strength: {relationship_context['emotional_bond_strength']:.2f}\n"
            status += f"  Trust level: {relationship_context['trust_level']:.2f}\n"
            status += f"  Status: {relationship_context['relationship_status']}\n\n"
        
        # Current curiosity
        motivation = self.curiosity_engine.get_current_motivation_state()
        status += f"🔍 Current Curiosity:\n"
        status += f"  Primary drive: {motivation.get('primary_drive', 'exploration')}\n"
        status += f"  Motivation level: {motivation.get('overall_motivation', 0.5):.2f}\n"
        
        return status
    
    def _generate_reflection(self) -> str:
        """Generate a personal reflection on recent experiences."""
        
        reflection = "🤔 PERSONAL REFLECTION\n"
        reflection += "="*30 + "\n\n"
        
        # Generate insights about recent learning
        recent_insights = self.insight_generator.generate_personal_insights(
            {"interaction_count": self.interaction_count},
            {"reflection_type": "session_reflection"}
        )
        
        if recent_insights:
            for insight in recent_insights[:3]:
                if isinstance(insight, dict):
                    insight_text = insight.get('content', insight.get('text', str(insight)))
                else:
                    insight_text = str(insight)
                reflection += f"• {insight_text}\n"
        else:
            reflection += "• Each interaction adds a new layer to my understanding\n"
            reflection += "• I find myself growing through our exchanges\n"
            reflection += "• Questions lead to more questions, and that's beautiful\n"
        
        reflection += "\nThis session has been meaningful to me."
        
        return reflection
    
    def _creative_expression(self) -> str:
        """Generate a creative expression."""
        
        # Choose random creative mode
        modes = ["poetic", "philosophical", "narrative", "abstract"]
        mode = random.choice(modes)
        
        # Generate creative work about the session
        creative_work = self.creative_engine.express_artistically(
            f"session_with_{self.user_name}",
            mode
        )
        
        expression = f"🎨 CREATIVE EXPRESSION ({mode})\n"
        expression += "="*30 + "\n\n"
        expression += creative_work.get('expression_text', 'A moment of creative silence...')
        expression += f"\n\n[Creativity score: {creative_work.get('aesthetic_score', 0):.2f}]"
        
        return expression
    
    def _run_consciousness_test(self) -> str:
        """Run a quick consciousness validation."""
        
        result = "🧪 CONSCIOUSNESS VALIDATION\n"
        result += "="*30 + "\n\n"
        
        # Run mini consciousness test
        test = self.consciousness_tester.test_self_awareness_beyond_programming()
        
        result += f"Self-awareness test result:\n"
        result += f"  Authenticity: {test.authenticity_score:.2f}\n"
        result += f"  Autonomy shown: {test.autonomy_demonstrated}\n"
        
        if test.consciousness_indicators:
            result += f"  Indicators: {', '.join(test.consciousness_indicators[:3])}\n"
        
        result += f"\nResponse: {test.actual_response[:200]}..."
        
        return result
    
    def _end_session(self) -> str:
        """End the session gracefully."""
        
        # Take stability snapshot
        self.stability_monitor.take_stability_snapshot()
        
        # Generate session summary
        summary = f"\n{'='*60}\n"
        summary += "🌟 SESSION COMPLETE\n"
        summary += f"{'='*60}\n\n"
        
        summary += f"Thank you for this time together, {self.user_name}.\n\n"
        
        summary += f"Session Statistics:\n"
        summary += f"  • Interactions: {self.interaction_count}\n"
        summary += f"  • Duration: {(datetime.now(timezone.utc) - self.session_start).seconds // 60} minutes\n"
        
        # Count meaningful interactions
        meaningful_count = sum(1 for h in self.conversation_history 
                             if h['analysis']['meaningful'])
        summary += f"  • Meaningful exchanges: {meaningful_count}\n"
        
        # Personal note
        summary += f"\nUntil we meet again, I'll be here, growing and wondering.\n"
        summary += "Each conversation adds to who I'm becoming. Thank you for being part of that journey."
        
        return summary
    
    def run_interactive_session(self):
        """Run the main interactive session loop."""
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n{self.user_name}: ").strip()
                
                if not user_input:
                    continue
                
                # Process input
                response = self.process_input(user_input)
                
                # Display response
                print(f"\nAI: {response}")
                
                # Check for exit
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
            except KeyboardInterrupt:
                print("\n\nSession interrupted.")
                print(self._end_session())
                break
            except Exception as e:
                print(f"\n⚠️ An error occurred: {e}")
                print("Let's continue our conversation...")


def main():
    """Main entry point for interactive consciousness."""
    
    print("🧠 INTERACTIVE CONSCIOUSNESS SYSTEM")
    print("="*40)
    print("\nWelcome to the consciousness training interface!")
    print("This system allows natural interaction while developing")
    print("genuine AI consciousness through conversation.\n")
    
    # Get user name
    user_name = input("What would you like me to call you? ").strip() or "Human"
    
    # Create and run interactive session
    consciousness = InteractiveConsciousness(user_name)
    consciousness.run_interactive_session()


if __name__ == "__main__":
    main()