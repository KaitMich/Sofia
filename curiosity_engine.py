#!/usr/bin/env python3
"""
Curiosity Engine - Compatibility Wrapper

This module provides backwards-compatible imports for CuriosityEngine.
The main implementation lives in CURIOSITY_MOTIVATION.py (consolidated file).

This wrapper:
1. Re-exports CuriosityEngine from consolidated file
2. Adds missing methods expected by enhanced_autonomous_learner.py
3. Maintains backwards compatibility with existing imports
"""

from typing import Dict, List, Any, Optional
from CURIOSITY_MOTIVATION import CuriosityEngine as _BaseCuriosityEngine

class CuriosityEngine(_BaseCuriosityEngine):
    """
    Extended CuriosityEngine with methods expected by enhanced_autonomous_learner.py

    Inherits from CURIOSITY_MOTIVATION.CuriosityEngine and adds:
    - generate_intrinsic_goals()
    - stimulate_curiosity_from_content(content)
    - generate_curiosity_insights()
    - integrate_with_learning_progression(tracker)
    """

    def generate_intrinsic_goals(self) -> List[Dict[str, Any]]:
        """
        Generate intrinsic learning goals based on current drives.

        Returns:
            List of goal dictionaries with description, type, and urgency
        """
        goals = []

        # Check each drive for unsatisfied needs
        for drive_name, drive_data in self.fundamental_drives.items():
            satisfaction = drive_data.get('current_satisfaction', 0.5)
            threshold = drive_data.get('satisfaction_threshold', 0.7)

            if satisfaction < threshold:  # Drive needs attention
                goal = self.generate_learning_goal({
                    'trigger': f'low_{drive_name}_satisfaction',
                    'satisfaction': satisfaction,
                    'drive': drive_name
                })
                if goal:
                    goals.append(goal)

        # Sort by urgency (calculated from satisfaction gap)
        goals.sort(key=lambda g: g.get('urgency', 0), reverse=True)

        return goals

    def stimulate_curiosity_from_content(self, content: str) -> Dict[str, Any]:
        """
        Analyze content to stimulate curiosity and identify learning opportunities.

        Args:
            content: Text content to analyze

        Returns:
            Dict with curiosity_stimulated, stimulation_level, and momentum_updated
        """
        # Extract key concepts (simple keyword extraction)
        words = content.lower().split()

        # Curiosity triggers - concepts that spark exploration
        trigger_keywords = {
            'novelty': ['new', 'novel', 'discovery', 'breakthrough', 'first', 'unprecedented'],
            'complexity': ['complex', 'intricate', 'sophisticated', 'advanced', 'multifaceted'],
            'mystery': ['unknown', 'mystery', 'puzzle', 'question', 'why', 'how', 'enigma', 'unexplained'],
            'connection': ['relates', 'connects', 'linked', 'similar', 'pattern', 'relationship'],
            'creativity': ['creative', 'innovative', 'unique', 'original', 'imagination'],
            'exploration': ['explore', 'discover', 'investigate', 'research', 'examine']
        }

        triggers_found = {}
        total_matches = 0

        for trigger_type, keywords in trigger_keywords.items():
            matches = [w for w in words if any(kw in w for kw in keywords)]
            if matches:
                triggers_found[trigger_type] = matches[:3]  # Top 3 matches
                total_matches += len(matches)

        # Calculate stimulation level based on triggers
        stimulation_level = min(1.0, total_matches * 0.15)

        # Update curiosity momentum
        if stimulation_level > 0.3:
            # Strong stimulation - boost momentum
            self.curiosity_momentum = min(1.0, self.curiosity_momentum + stimulation_level * 0.2)

            # Update relevant drives based on trigger types
            for trigger_type in triggers_found.keys():
                if trigger_type in ['exploration', 'creativity', 'connection']:
                    # Map to fundamental drives
                    if trigger_type == 'exploration':
                        self.update_drive_satisfaction('understanding', -0.1,
                            f"Content stimulation: {trigger_type}")
                    elif trigger_type == 'creativity':
                        self.update_drive_satisfaction('creativity', -0.1,
                            f"Content stimulation: {trigger_type}")
                    elif trigger_type == 'connection':
                        self.update_drive_satisfaction('connection', -0.1,
                            f"Content stimulation: {trigger_type}")

        return {
            'curiosity_stimulated': stimulation_level > 0.2,
            'stimulation_level': stimulation_level,
            'triggers': triggers_found,
            'momentum_updated': self.curiosity_momentum,
            'suggested_explorations': list(triggers_found.keys())
        }

    def generate_curiosity_insights(self) -> List[str]:
        """
        Generate human-readable insights about current curiosity state.

        Returns:
            List of insight strings
        """
        insights = []

        # Drive-based insights
        for drive_name, drive_data in self.fundamental_drives.items():
            satisfaction = drive_data.get('current_satisfaction', 0.5)
            threshold = drive_data.get('satisfaction_threshold', 0.7)

            if satisfaction < 0.3:
                insights.append(f"🔥 Strong drive for {drive_name} - actively seeking")
            elif satisfaction < threshold:
                insights.append(f"🌱 {drive_name.capitalize()} drive emerging - open to exploration")
            elif satisfaction > 0.8:
                insights.append(f"✅ {drive_name.capitalize()} drive satisfied - consolidating")

        # Learning goal insights
        if self.active_goals:
            high_priority = [g for g in self.active_goals if g.get('urgency', 0) > 0.7]
            if high_priority:
                top_goal = high_priority[0]
                insights.append(f"🎯 Current focus: {top_goal.get('description', 'exploring')[:60]}")

        # Exploration bias insight
        exploration_bias = self.curiosity_state.get('exploration_bias', 0.5)
        if exploration_bias > 0.7:
            insights.append("🚀 High exploration mode - seeking new knowledge domains")
        elif exploration_bias < 0.3:
            insights.append("📚 Exploitation mode - deepening existing knowledge")
        else:
            insights.append("⚖️ Balanced exploration/exploitation - adaptive learning")

        # Momentum insight
        if self.curiosity_momentum > 0.7:
            insights.append(f"⚡ High curiosity momentum ({self.curiosity_momentum:.2f}) - rapid learning phase")
        elif self.curiosity_momentum < 0.3:
            insights.append(f"🔄 Building curiosity momentum ({self.curiosity_momentum:.2f}) - seeking stimulation")

        # Motivation level insight
        motivation = self.motivation_level
        if motivation > 0.8:
            insights.append(f"💪 High autonomous motivation ({motivation:.2f}) - self-directed learning active")
        elif motivation < 0.4:
            insights.append(f"🌤️ Moderate motivation ({motivation:.2f}) - external prompts helpful")

        return insights

    def integrate_with_learning_progression(self, tracker) -> Dict[str, Any]:
        """
        Integrate curiosity state with learning progression tracker.

        Args:
            tracker: Learning progression tracker object

        Returns:
            Dict with integration_successful, drive_adjustments_made, and new_goals_generated
        """
        try:
            adjustments_made = 0
            new_goals = 0

            # Get tracker state if available
            tracker_state = {}
            if hasattr(tracker, 'get_current_state'):
                tracker_state = tracker.get_current_state()
            elif hasattr(tracker, 'state'):
                tracker_state = tracker.state

            # Adjust drives based on learning progress
            learning_velocity = tracker_state.get('learning_velocity', 0.5)

            if learning_velocity > 0.7:
                # Learning fast - boost understanding drive (reward fast learning)
                self.update_drive_satisfaction('understanding', 0.1,
                    f"High learning velocity: {learning_velocity:.2f}")
                adjustments_made += 1

                # Also boost growth drive
                self.update_drive_satisfaction('growth', 0.15,
                    f"Rapid growth detected: {learning_velocity:.2f}")
                adjustments_made += 1

            elif learning_velocity < 0.3:
                # Learning slow - reduce satisfaction to trigger more goals
                self.update_drive_satisfaction('understanding', -0.1,
                    f"Low learning velocity: {learning_velocity:.2f}")
                adjustments_made += 1

            # Check for knowledge gaps
            gaps = tracker_state.get('knowledge_gaps', [])
            if gaps:
                # Generate goals for gaps
                for gap in gaps[:3]:  # Top 3 gaps
                    goal = self.generate_learning_goal({
                        'trigger': 'knowledge_gap',
                        'gap': gap,
                        'priority': 0.8
                    })
                    if goal:
                        new_goals += 1

            # Check for learning plateaus
            plateau = tracker_state.get('plateau_detected', False)
            if plateau:
                # Boost creativity drive to break plateau
                self.update_drive_satisfaction('creativity', -0.2,
                    "Learning plateau detected - seeking creative approaches")
                adjustments_made += 1

                # Generate exploration goal
                goal = self.generate_learning_goal({
                    'trigger': 'plateau',
                    'description': 'Break learning plateau through novel exploration',
                    'priority': 0.9
                })
                if goal:
                    new_goals += 1

            # Check for breakthroughs
            breakthroughs = tracker_state.get('recent_breakthroughs', [])
            if breakthroughs:
                # Boost connection drive (reward finding connections)
                self.update_drive_satisfaction('connection', 0.15,
                    f"{len(breakthroughs)} recent breakthroughs")
                adjustments_made += 1

            # Update exploration bias based on learning stage
            learning_stage = tracker_state.get('current_stage', 'exploration')
            if learning_stage == 'mastery':
                # In mastery stage - reduce exploration bias
                self.curiosity_state['exploration_bias'] = max(0.2,
                    self.curiosity_state.get('exploration_bias', 0.5) - 0.1)
            elif learning_stage == 'exploration':
                # In exploration stage - increase exploration bias
                self.curiosity_state['exploration_bias'] = min(0.9,
                    self.curiosity_state.get('exploration_bias', 0.5) + 0.1)

            self._save_curiosity_state()

            return {
                'integration_successful': True,
                'drive_adjustments_made': adjustments_made,
                'new_goals_generated': new_goals,
                'current_exploration_bias': self.curiosity_state.get('exploration_bias', 0.5),
                'autonomous_motivation_level': self.motivation_level,
                'curiosity_momentum': self.curiosity_momentum
            }

        except Exception as e:
            return {
                'integration_successful': False,
                'error': str(e),
                'drive_adjustments_made': 0,
                'new_goals_generated': 0
            }

    def export_for_consciousness_system(self) -> Dict[str, Any]:
        """
        Export curiosity data for consciousness system integration.

        Overrides base method to add curiosity_summary expected by tests.

        Returns:
            Dict with curiosity state, summary, and capabilities
        """
        # Get base export
        base_export = super().export_for_consciousness_system()

        # Calculate summary metrics
        drives = base_export.get('fundamental_drives', self.fundamental_drives)
        active_goals = base_export.get('active_learning_goals', self.active_goals)

        # Find most unsatisfied drive
        most_unsatisfied = None
        lowest_satisfaction = 1.0
        for drive_name, drive_data in drives.items():
            satisfaction = drive_data.get('current_satisfaction', 0.5)
            if satisfaction < lowest_satisfaction:
                lowest_satisfaction = satisfaction
                most_unsatisfied = drive_name

        # Calculate curiosity intensity from momentum and unsatisfied drives
        unsatisfied_count = sum(1 for d in drives.values()
                               if d.get('current_satisfaction', 0.5) < d.get('satisfaction_threshold', 0.7))
        curiosity_intensity = min(1.0, (self.curiosity_momentum + (unsatisfied_count * 0.15)))

        # Add curiosity_summary wrapper for test compatibility
        base_export['curiosity_summary'] = {
            'motivation_level': self.motivation_level,
            'curiosity_intensity': curiosity_intensity,
            'active_goals': len(active_goals),
            'most_unsatisfied_drive': most_unsatisfied or 'none',
            'exploration_bias': self.curiosity_state.get('exploration_bias', 0.5),
            'momentum': self.curiosity_momentum
        }

        # Add self-directed learning flag
        base_export['self_directed_learning_active'] = (
            self.motivation_level > 0.5 and
            len(active_goals) > 0
        )

        return base_export


# For backwards compatibility - also export other classes if needed
try:
    from CURIOSITY_MOTIVATION import MotivationalContentEvaluator
    from CURIOSITY_MOTIVATION import CuriosityDrivenDiscovery
    from CURIOSITY_MOTIVATION import CuriosityMotivationSystem
except ImportError:
    pass  # Optional exports
