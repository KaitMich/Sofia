#!/usr/bin/env python3
"""
Standalone live test for bridge reclassification.
Runs without numpy dependency.

Created: 2025-11-24
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath, data):
    """Save JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    print("\n" + "="*70)
    print("BRIDGE RECLASSIFICATION - LIVE TEST")
    print("="*70 + "\n")

    # Check current state
    print("📊 PRE-TEST STATE:")
    print("-" * 70)

    bridge_path = Path("data/bridge_memory.json")
    logic_path = Path("data/logic_memory.json")
    symbolic_path = Path("data/symbolic_memory.json")

    bridge_items = load_json(bridge_path)
    logic_items = load_json(logic_path)
    symbolic_items = load_json(symbolic_path)

    print(f"Bridge memory:   {len(bridge_items)} items")
    print(f"Logic memory:    {len(logic_items)} items")
    print(f"Symbolic memory: {len(symbolic_items)} items")

    if not bridge_items:
        print("\n⚠️  No items in bridge memory to test!")
        return 1

    print(f"\nBridge item to review:")
    item = bridge_items[0]
    print(f"  ID: {item.get('id')}")
    print(f"  Text: {item.get('text')[:60]}...")
    print(f"  Timestamp: {item.get('timestamp')}")
    print(f"  Age: ~162 days (from 2025-06-15)")

    print("\n" + "="*70)
    print("RUNNING RECLASSIFICATION (DRY-RUN FIRST)")
    print("="*70 + "\n")

    # Import and run reclassifier
    try:
        from bridge_reclassifier import BridgeReclassifier
        from unified_memory import TripartiteMemory

        # Create simple memory wrapper
        class SimpleMemory:
            def __init__(self):
                self.tripartite = TripartiteMemory()
                self.logic_memory = self.tripartite.logic_memory
                self.symbolic_memory = self.tripartite.symbolic_memory
                self.bridge_memory = self.tripartite.bridge_memory

            def move_item_from_bridge(self, item, target, reason):
                """Move item from bridge to target memory."""
                item_id = item.get('id')

                # Remove from bridge
                self.tripartite.bridge_memory = [i for i in self.tripartite.bridge_memory if i.get('id') != item_id]

                # Add metadata
                item['reclassified_from_bridge'] = True
                item['reclassification_date'] = datetime.utcnow().isoformat()
                item['reclassification_reason'] = reason

                # Add to target
                if target == 'LOGIC':
                    item['decision_type'] = 'FOLLOW_LOGIC'
                    self.tripartite.logic_memory.append(item)
                else:
                    item['decision_type'] = 'FOLLOW_SYMBOLIC'
                    self.tripartite.symbolic_memory.append(item)

                # Save
                self.tripartite._save_tripartite_memory()
                return True

        memory = SimpleMemory()
        reclassifier = BridgeReclassifier(memory)

        # DRY RUN
        print("🔍 DRY-RUN MODE (preview only):")
        results = reclassifier.review_bridge_memory(dry_run=True)

        print(f"\n  Items reviewed: {results['items_reviewed']}")
        print(f"  Items ready:    {results['items_ready']}")

        if results['details']:
            for detail in results['details']:
                print(f"\n  Item: {detail['id'][:30]}...")
                print(f"    Related items: {detail['related_count']}")
                print(f"    Decision: {detail['reason']}")
                if detail.get('should_reclassify'):
                    print(f"    ✓ READY to reclassify → {detail['target']}")
                else:
                    print(f"    ○ WAIT - {detail['reason']}")

        if results['items_ready'] == 0:
            print("\n⚠️  No items ready for reclassification.")
            print("   Reasons could be:")
            print("   - Item too recent (< 7 days)")
            print("   - Insufficient related items (< 5)")
            print("   - Cluster not dominated enough (need 70%+)")
            print("\n✅ DRY-RUN complete - system working correctly")
            return 0

        print("\n" + "="*70)
        print("RUNNING LIVE RECLASSIFICATION")
        print("="*70 + "\n")

        input("Press ENTER to proceed with live reclassification (or Ctrl+C to cancel): ")

        # Reload memory for live run
        memory = SimpleMemory()
        reclassifier = BridgeReclassifier(memory)

        # LIVE RUN
        print("\n⚡ LIVE MODE (making actual changes):")
        results = reclassifier.review_bridge_memory(dry_run=False)

        print(f"\n  Items reclassified: {results['items_reclassified']}")
        print(f"    → To Logic:       {results['to_logic']}")
        print(f"    → To Symbolic:    {results['to_symbolic']}")
        print(f"  Items remaining:    {results['items_remaining']}")

        # Verify results
        print("\n" + "="*70)
        print("POST-TEST VERIFICATION")
        print("="*70 + "\n")

        bridge_after = load_json(bridge_path)
        logic_after = load_json(logic_path)
        symbolic_after = load_json(symbolic_path)

        print(f"Bridge memory:   {len(bridge_after)} items (was {len(bridge_items)})")
        print(f"Logic memory:    {len(logic_after)} items (was {len(logic_items)})")
        print(f"Symbolic memory: {len(symbolic_after)} items (was {len(symbolic_items)})")

        # Check for reclassified items
        reclassified = [i for i in logic_after + symbolic_after if i.get('reclassified_from_bridge')]

        if reclassified:
            print(f"\n✅ Found {len(reclassified)} reclassified item(s):")
            for item in reclassified:
                print(f"\n  Item ID: {item.get('id')}")
                print(f"  Text: {item.get('text')[:60]}...")
                print(f"  Reclassified: {item.get('reclassification_date')}")
                print(f"  Reason: {item.get('reclassification_reason')}")
                print(f"  New decision: {item.get('decision_type')}")

        # Check log file
        log_path = Path("data/bridge_reclassification_log.json")
        if log_path.exists():
            print(f"\n📝 Audit log created: {log_path}")
            log_data = load_json(log_path)
            print(f"   Total reviews logged: {len(log_data.get('reviews', []))}")

        print("\n" + "="*70)
        print("✅ LIVE TEST COMPLETE")
        print("="*70)
        print("\nBackups available at:")
        print("  - data/bridge_memory.json.backup")
        print("  - data/logic_memory.json.backup")
        print("  - data/symbolic_memory.json.backup")

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
