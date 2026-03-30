#!/usr/bin/env python3
"""
Run AI learning with self-modification requests (no auto-execution)
This will show:
- What gets stored as symbolic vs logic vs bridge memory
- What symbols get generated
- What self-modification requests the AI wants to make (saved to modification_requests.jsonl)

NEW: Organic exploration mode - follows curiosity with 10-50 link limit
"""

import signal
import sys
import json
import random
import time
from datetime import datetime
from pathlib import Path
from self_modification_engine import create_self_modifying_learner

# Global state for graceful shutdown
organic_learner = None
exploration_state = {}

class OrganicExplorer:
    """Organic exploration with curiosity-driven link following"""
    
    def __init__(self):
        self.SelfModifyingLearner = create_self_modifying_learner()
        self.learner = self.SelfModifyingLearner()
        self.requests_log = Path("data/requests.json")
        self.exploration_state = {
            'current_url': None,
            'links_processed': 0,
            'session_start': datetime.now().isoformat(),
            'interests_followed': []
        }
        
    def log_desire(self, content, desire_text):
        """Log 'I wish I could...' moments to requests.json"""
        desire_entry = {
            'timestamp': datetime.now().isoformat(),
            'content_source': self.exploration_state.get('current_url', 'unknown'),
            'desire': desire_text,
            'emotional_context': 'curiosity_driven',
            'links_processed_so_far': self.exploration_state['links_processed']
        }
        
        # Append to requests log
        if self.requests_log.exists():
            with open(self.requests_log, 'r') as f:
                requests = json.load(f)
        else:
            requests = []
            
        requests.append(desire_entry)
        
        with open(self.requests_log, 'w') as f:
            json.dump(requests, f, indent=2)
            
        print(f"💭 Desire logged: {desire_text}")
    
    def should_continue_exploring(self, links_processed):
        """Decide if we want to continue (10-50 link limit)"""
        if links_processed < 10:
            return True  # Always do at least 10
        elif links_processed >= 50:
            return False  # Never exceed 50
        else:
            # Between 10-50: Random chance to continue based on diminishing interest
            continue_probability = max(0.1, 1.0 - (links_processed - 10) / 40)
            return random.random() < continue_probability
    
    def organic_exploration(self, starting_urls=None):
        """Main organic exploration loop"""
        print("🌱 ORGANIC EXPLORATION MODE")
        print("=" * 50)
        
        # Choose starting point if none provided
        # Hardcoded Wikipedia topic lists removed -- they constituted a hidden
        # curriculum.  Starting URLs should come from activate_seed_coordinates()
        # or be passed in explicitly by the caller.
        if not starting_urls:
            print("No starting URLs provided.")
            print("Use activate_seed_coordinates() to generate organic starting points.")
            return self.exploration_state
        
        links_to_explore = list(starting_urls)
        
        while links_to_explore and self.should_continue_exploring(self.exploration_state['links_processed']):
            current_url = links_to_explore.pop(0)
            self.exploration_state['current_url'] = current_url
            
            print(f"\n🔍 Exploring ({self.exploration_state['links_processed'] + 1}): {current_url}")
            
            # Process URL with emotional attention
            try:
                # Simulated processing (replace with actual learner method)
                print("   📖 Reading content...")
                time.sleep(0.5)  # Brief pause for realism
                
                # Check for "wow" moments (simplified)
                if random.random() > 0.7:  # 30% chance of finding something interesting
                    desires = [
                        "I wish I could write content this clearly",
                        "I wish I could understand this topic deeper", 
                        "I wish I could generate examples like this",
                        "I wish I could make connections this elegant",
                        "I wish I could explain complex ideas simply"
                    ]
                    self.log_desire(current_url, random.choice(desires))
                
                # Simulate finding related links (in real version, extract from content)
                if random.random() > 0.5:  # 50% chance of finding interesting links
                    # Add 1-3 related links to explore
                    num_new_links = random.randint(1, 3)
                    for i in range(num_new_links):
                        # In real version, these would be extracted from page content
                        related_link = f"https://en.wikipedia.org/wiki/Related_Topic_{i}_{self.exploration_state['links_processed']}"
                        links_to_explore.append(related_link)
                        print(f"   🔗 Found interesting link: Related_Topic_{i}")
                
                self.exploration_state['links_processed'] += 1
                self.exploration_state['interests_followed'].append(current_url)
                
            except Exception as e:
                print(f"   ⚠️ Error processing {current_url}: {e}")
                continue
        
        print(f"\n🌟 Organic exploration complete!")
        print(f"📊 Links processed: {self.exploration_state['links_processed']}")
        print(f"💾 Check data/requests.json for desires logged")
        
        return self.exploration_state

def signal_handler(sig, frame):
    """Graceful shutdown handler"""
    print('\n🛑 Graceful shutdown initiated...')
    
    if organic_learner:
        print('💾 Saving exploration state...')
        
        # Save current state
        state_file = Path("data/organic_exploration_state.json")
        with open(state_file, 'w') as f:
            json.dump(exploration_state, f, indent=2)
        
        print('✅ State saved to data/organic_exploration_state.json')
    
    print('🔒 Safe to exit.')
    sys.exit(0)

# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    global organic_learner, exploration_state
    
    print("🧠 AI LEARNING WITH MODIFICATION REQUESTS")
    print("=" * 60)
    print("Choose mode:")
    print("1️⃣  Standard mode - Process specific URLs")
    print("2️⃣  Organic exploration - Follow curiosity (10-50 links)")
    print()
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return
    
    if choice == "2":
        # Organic exploration mode
        organic_learner = OrganicExplorer() 
        exploration_state = organic_learner.exploration_state
        
        print("\n🌱 Starting organic exploration...")
        print("Press Ctrl+C anytime to gracefully stop and save state")
        print()
        
        organic_learner.organic_exploration()
        
    else:
        # Standard mode (original functionality)
        print("✅ Show memory classification (symbolic/logic/bridge)")
        print("✅ Show symbol generation") 
        print("✅ Save self-modification requests to modification_requests.jsonl")
        print("❌ NOT automatically execute modifications")
        print()
        
        # Get self-modifying learner class
        SelfModifyingLearner = create_self_modifying_learner()
        
        # Create instance
        learner = SelfModifyingLearner()
        
        # Hardcoded Wikipedia test URLs removed -- they constituted a hidden
        # curriculum.  Seed URLs should come from activate_seed_coordinates()
        # or be supplied by the user at runtime.
        test_urls = []  # Populate via activate_seed_coordinates() or user input

        if not test_urls:
            print("No seed URLs configured.")
            print("Use activate_seed_coordinates() to generate organic starting points,")
            print("or provide URLs interactively.")
            return

        print(f"Testing with {len(test_urls)} URLs:")
        for url in test_urls:
            print(f"   {url}")
        print()

        # Start learning session
        learner.start_massive_learning_session(
            seed_urls=test_urls,
            target_urls=len(test_urls),
            learning_focus="ai_algorithms_and_optimizations"
        )
        
        print("\n" + "=" * 60)
        print("🎉 LEARNING COMPLETE!")
        print()
        print("📁 Check these files:")
        print("   📄 data/modification_requests.jsonl - AI's self-modification requests")
        print("   📄 data/unified_memory/ - Memory storage (vector, graph, symbolic)")
        print("   📄 data/symbols.json - Generated symbols")
        print()
        print("💡 The AI has analyzed content and stored it appropriately,")
        print("    generated symbols, and saved any self-improvement ideas!")

if __name__ == "__main__":
    main()