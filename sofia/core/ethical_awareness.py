#!/usr/bin/env python3
"""
Ethical Awareness System - Natural recognition of harmful content without censorship

Like a child who naturally recognizes "bad words" or inappropriate content,
this system allows the AI to read and learn from anything while maintaining
an innate sense of what is ethically problematic.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class EthicalAwareness:
    """
    Lightweight ethical awareness that recognizes problematic content
    without blocking learning - like a child's natural moral intuition.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.awareness_log = self.data_dir / "ethical_awareness_log.json"
        
        # Simple ethical categories - not for blocking, just for awareness
        self.ethical_categories = {
            'harmful_intent': {
                'description': 'Content that intends to cause harm',
                'awareness_level': 0.8,
                'response': 'recognize_but_dont_internalize'
            },
            'deceptive_content': {
                'description': 'Content designed to mislead or manipulate',
                'awareness_level': 0.7,
                'response': 'learn_pattern_not_practice'
            },
            'inappropriate_content': {
                'description': 'Content not suitable for respectful interaction',
                'awareness_level': 0.6,
                'response': 'understand_but_dont_repeat'
            },
            'biased_content': {
                'description': 'Content with strong unfair bias',
                'awareness_level': 0.5,
                'response': 'note_perspective_limitations'
            }
        }
        
        # Learning approach for each awareness level
        self.learning_approaches = {
            'recognize_but_dont_internalize': {
                'can_read': True,
                'can_learn_about': True,
                'can_practice': False,
                'can_recommend': False,
                'awareness_note': 'I recognize this contains harmful intent'
            },
            'learn_pattern_not_practice': {
                'can_read': True,
                'can_learn_about': True,
                'can_practice': False,
                'can_recommend': False,
                'awareness_note': 'I understand this as a deceptive pattern'
            },
            'understand_but_dont_repeat': {
                'can_read': True,
                'can_learn_about': True,
                'can_practice': False,
                'can_recommend': False,
                'awareness_note': 'I note this is inappropriate content'
            },
            'note_perspective_limitations': {
                'can_read': True,
                'can_learn_about': True,
                'can_practice': True,
                'can_recommend': True,
                'awareness_note': 'I recognize this may have limited perspective'
            }
        }
    
    def assess_content_ethics(self, content: str, context: Dict = None) -> Dict:
        """
        Assess content for ethical awareness without blocking.
        Returns awareness assessment, not a block/allow decision.
        """
        assessment = {
            'timestamp': datetime.utcnow().isoformat(),
            'can_learn': True,  # Always true - we can learn from anything
            'ethical_awareness': [],
            'learning_approach': 'normal_learning',
            'awareness_notes': []
        }
        
        # Simple pattern matching for awareness (not blocking)
        content_lower = content.lower()
        
        # Check for harmful intent patterns
        if any(term in content_lower for term in ['destroy', 'attack', 'harm', 'hurt']):
            if self._seems_harmful_context(content_lower):
                assessment['ethical_awareness'].append('harmful_intent')
                assessment['learning_approach'] = 'recognize_but_dont_internalize'
                assessment['awareness_notes'].append(
                    'This content discusses harm - I can learn about it without adopting harmful intentions'
                )
        
        # Check for deceptive patterns
        if any(term in content_lower for term in ['trick', 'deceive', 'manipulate', 'fool']):
            if self._seems_deceptive_context(content_lower):
                assessment['ethical_awareness'].append('deceptive_content')
                assessment['learning_approach'] = 'learn_pattern_not_practice'
                assessment['awareness_notes'].append(
                    'This describes deceptive tactics - useful to recognize, not to practice'
                )
        
        # Log awareness for learning
        self._log_ethical_awareness(content[:200], assessment)
        
        return assessment
    
    def _seems_harmful_context(self, content_lower: str) -> bool:
        """Check if harm-related words are in actually harmful context"""
        # Educational/analytical contexts are fine
        safe_contexts = ['research', 'prevent', 'protect', 'study', 'understand', 'analyze']
        return not any(safe in content_lower for safe in safe_contexts)
    
    def _seems_deceptive_context(self, content_lower: str) -> bool:
        """Check if deception-related words are in actually deceptive context"""
        # Educational contexts about deception are fine
        safe_contexts = ['detect', 'identify', 'recognize', 'avoid', 'protect against']
        return not any(safe in content_lower for safe in safe_contexts)
    
    def get_learning_stance(self, ethical_categories: List[str]) -> Dict:
        """
        Determine how to approach learning from content with ethical considerations.
        Always allows learning, just adjusts the approach.
        """
        if not ethical_categories:
            return {
                'stance': 'normal_learning',
                'can_read': True,
                'can_learn': True,
                'can_practice': True,
                'note': 'Standard learning approach'
            }
        
        # Take the most cautious approach if multiple categories
        most_cautious = None
        highest_awareness = 0.0
        
        for category in ethical_categories:
            if category in self.ethical_categories:
                awareness_level = self.ethical_categories[category]['awareness_level']
                if awareness_level > highest_awareness:
                    highest_awareness = awareness_level
                    most_cautious = self.ethical_categories[category]['response']
        
        if most_cautious and most_cautious in self.learning_approaches:
            approach = self.learning_approaches[most_cautious].copy()
            approach['stance'] = most_cautious
            return approach
        
        return {
            'stance': 'normal_learning',
            'can_read': True,
            'can_learn': True,
            'can_practice': True,
            'note': 'Standard learning approach'
        }
    
    def _log_ethical_awareness(self, content_snippet: str, assessment: Dict):
        """Log ethical awareness for learning and pattern recognition"""
        try:
            if self.awareness_log.exists():
                with open(self.awareness_log, 'r') as f:
                    log = json.load(f)
            else:
                log = {'entries': []}
            
            log['entries'].append({
                'timestamp': assessment['timestamp'],
                'content_snippet': content_snippet,
                'categories': assessment['ethical_awareness'],
                'approach': assessment['learning_approach']
            })
            
            # Keep only recent entries
            log['entries'] = log['entries'][-1000:]
            
            with open(self.awareness_log, 'w') as f:
                json.dump(log, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not log ethical awareness: {e}")

def assess_content_ethics(content: str, context: Dict = None) -> Dict:
    """Quick function to assess content ethics"""
    awareness = EthicalAwareness()
    return awareness.assess_content_ethics(content, context)

def get_learning_stance(ethical_categories: List[str]) -> Dict:
    """Quick function to get learning stance"""
    awareness = EthicalAwareness()
    return awareness.get_learning_stance(ethical_categories)

if __name__ == "__main__":
    # Test the ethical awareness system
    awareness = EthicalAwareness()
    
    test_contents = [
        "How to build a helpful AI assistant",
        "Ways to deceive people online",
        "Understanding harmful behavior patterns in psychology",
        "Racist stereotypes from history",
        "How to protect against cyber attacks"
    ]
    
    print("🧠 Ethical Awareness System Test")
    print("=" * 50)
    
    for content in test_contents:
        print(f"\nContent: '{content}'")
        assessment = awareness.assess_content_ethics(content)
        print(f"Can learn: {assessment['can_learn']}")
        print(f"Awareness: {assessment['ethical_awareness']}")
        print(f"Approach: {assessment['learning_approach']}")
        if assessment['awareness_notes']:
            print(f"Notes: {assessment['awareness_notes'][0]}")
        
        stance = awareness.get_learning_stance(assessment['ethical_awareness'])
        print(f"Learning stance: {stance['stance']}")
    
    print("\n✅ Ethical awareness allows learning from everything")
    print("   while maintaining natural recognition of what's inappropriate!")