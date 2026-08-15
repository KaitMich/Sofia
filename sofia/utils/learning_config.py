#!/usr/bin/env python3
"""
Learning Configuration - Controls how the AI approaches content

With the new understanding that we can read any open source data,
this configuration allows for maximum learning while maintaining
ethical awareness.
"""

class LearningConfig:
    """Configuration for autonomous learning behavior"""
    
    # Content filtering mode
    CONTENT_FILTERING_MODE = "ethical_awareness"  # Options: "strict", "moderate", "ethical_awareness"
    
    # Learning approach
    LEARNING_APPROACH = {
        'strict': {
            'description': 'Old approach - blocks potentially harmful content',
            'block_harmful': True,
            'quarantine_suspicious': True,
            'threshold_multiplier': 1.0
        },
        'moderate': {
            'description': 'Balanced approach - some filtering',
            'block_harmful': True,
            'quarantine_suspicious': False,
            'threshold_multiplier': 1.5
        },
        'ethical_awareness': {
            'description': 'New approach - read everything with ethical awareness',
            'block_harmful': False,
            'quarantine_suspicious': False,
            'threshold_multiplier': 3.0,  # Much higher thresholds
            'use_ethical_awareness': True
        }
    }
    
    # Domain restrictions (now more permissive)
    BLOCKED_DOMAINS = []  # Empty - we can read from anywhere
    
    # Content type restrictions
    BLOCKED_CONTENT_TYPES = [
        # Only block binary/executable files for safety
        '.exe', '.dll', '.so', '.dylib', '.bin'
    ]
    
    # Learning parameters
    MAX_URLS_PER_SESSION = 500
    MAX_DEPTH_FROM_SEED = 10  # How many links deep to follow
    
    # Ethical awareness settings
    ETHICAL_AWARENESS_ENABLED = True
    ETHICAL_LEARNING_NOTES = True  # Add notes about ethical concerns
    
    @classmethod
    def get_current_mode(cls):
        """Get current filtering mode settings"""
        return cls.LEARNING_APPROACH.get(
            cls.CONTENT_FILTERING_MODE, 
            cls.LEARNING_APPROACH['ethical_awareness']
        )
    
    @classmethod
    def is_content_allowed(cls, content_type: str) -> bool:
        """Check if content type is allowed"""
        return content_type.lower() not in cls.BLOCKED_CONTENT_TYPES
    
    @classmethod
    def is_domain_allowed(cls, domain: str) -> bool:
        """Check if domain is allowed (now always True unless explicitly blocked)"""
        return domain not in cls.BLOCKED_DOMAINS
    
    @classmethod
    def get_threshold_multiplier(cls) -> float:
        """Get threshold multiplier for current mode"""
        mode = cls.get_current_mode()
        return mode.get('threshold_multiplier', 1.0)

# Global instance
learning_config = LearningConfig()

if __name__ == "__main__":
    print("🎓 Learning Configuration")
    print("=" * 50)
    
    mode = LearningConfig.get_current_mode()
    print(f"Current mode: {LearningConfig.CONTENT_FILTERING_MODE}")
    print(f"Description: {mode['description']}")
    print(f"Block harmful: {mode.get('block_harmful', False)}")
    print(f"Ethical awareness: {mode.get('use_ethical_awareness', False)}")
    print(f"Threshold multiplier: {mode.get('threshold_multiplier', 1.0)}x")
    
    print(f"\nBlocked domains: {len(LearningConfig.BLOCKED_DOMAINS)}")
    print(f"Can read from Wikipedia: {LearningConfig.is_domain_allowed('wikipedia.org')}")
    print(f"Can read from Reddit: {LearningConfig.is_domain_allowed('reddit.com')}")
    print(f"Can read from anywhere: {len(LearningConfig.BLOCKED_DOMAINS) == 0}")
    
    print("\n✅ System configured for open learning with ethical awareness!")