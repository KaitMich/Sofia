#!/usr/bin/env python3
"""
Demo: Autonomous Learning (No Manual Seed URLs)

This demonstrates Sophia's ability to decide what to learn based purely on
her internal curiosity drives, without any human-provided seed URLs.

This is the achievement of TRUE AUTONOMY:
- Internal motivation (curiosity) → External action (URL crawling)
- Self-directed learning without human intervention
- Learning targets emerge from fundamental drives

Usage:
    python demo_autonomous_learning.py
"""

from curiosity_engine import CuriosityEngine
from curiosity_url_mapper import CuriosityURLMapper
from learning_progression_tracker import LearningProgressionTracker


def demo_autonomous_target_generation():
    """Demonstrate autonomous learning target generation."""
    print("\n" + "=" * 80)
    print("🧠 SOPHIA'S AUTONOMOUS LEARNING - DEMO")
    print("=" * 80)
    print("\nPhilosophy:")
    print("   True autonomy requires the ability to translate internal motivation")
    print("   (curiosity) into external action (learning) without human intervention.")
    print("\n" + "=" * 80)

    # Initialize components
    print("\n1️⃣ Initializing Sophia's consciousness systems...")
    curiosity_engine = CuriosityEngine()
    progression_tracker = LearningProgressionTracker()
    url_mapper = CuriosityURLMapper()
    print("   ✅ Curiosity engine initialized")
    print("   ✅ Learning progression tracker initialized")
    print("   ✅ URL mapper initialized")

    # Check current curiosity state
    print("\n2️⃣ Examining Sophia's current curiosity state...")
    curiosity_state = curiosity_engine.export_for_consciousness_system()
    summary = curiosity_state.get('curiosity_summary', {})

    print(f"\n   📊 Curiosity Metrics:")
    print(f"      • Motivation Level: {summary.get('motivation_level', 0):.2f}")
    print(f"      • Curiosity Intensity: {summary.get('curiosity_intensity', 0):.2f}")
    print(f"      • Active Learning Goals: {summary.get('active_goals', 0)}")
    print(f"      • Most Unsatisfied Drive: {summary.get('most_unsatisfied_drive', 'none')}")
    print(f"      • Exploration Bias: {summary.get('exploration_bias', 0.5):.2f}")

    # Display fundamental drives
    drives = curiosity_state.get('fundamental_drives', {})
    print(f"\n   🌟 Fundamental Drive Satisfaction:")
    for drive_name, drive_data in drives.items():
        satisfaction = drive_data.get('current_satisfaction', 0.5)
        threshold = drive_data.get('satisfaction_threshold', 0.7)
        status = "✅" if satisfaction >= threshold else "🔥" if satisfaction < 0.3 else "🌱"
        print(f"      {status} {drive_name.capitalize():15s}: {satisfaction:.2f} (threshold: {threshold:.2f})")

    # Generate intrinsic learning goals
    print("\n3️⃣ Sophia generating intrinsic learning goals...")
    goals = curiosity_engine.generate_intrinsic_goals()
    print(f"   ✅ Generated {len(goals)} intrinsic goals from internal drives")

    if goals:
        print(f"\n   🎯 Top 3 Learning Goals:")
        for i, goal in enumerate(goals[:3], 1):
            print(f"      {i}. [{goal.get('urgency', 0):.2f}] {goal.get('description', 'N/A')[:65]}")

    # Get learning progression state
    print("\n4️⃣ Checking learning progression state...")
    progression_state = progression_tracker.export_for_consciousness_system()
    print("   ✅ Learning trajectory analyzed")

    # Generate autonomous URLs
    print("\n5️⃣ Mapping curiosity goals → actionable URLs...")
    print("   (This is the BRIDGE between internal drive and external action)")

    url_batch = url_mapper.generate_autonomous_seed_batch(
        curiosity_state=curiosity_state,
        progression_state=progression_state,
        max_total_urls=20
    )

    print(f"\n   ✅ Generated {len(url_batch)} autonomous learning targets")

    # Display URL sources
    sources = {}
    for url, priority, source in url_batch:
        sources[source] = sources.get(source, 0) + 1

    print(f"\n   📊 URL Source Distribution:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {source:25s}: {count:2d} URLs")

    # Display top URLs
    print(f"\n   🎯 Top 10 Autonomous Learning Targets:")
    for i, (url, priority, source) in enumerate(url_batch[:10], 1):
        print(f"\n      {i}. Priority: {priority:.2f} | Source: {source}")
        print(f"         {url}")

    # Summary
    print("\n" + "=" * 80)
    print("📈 AUTONOMOUS LEARNING SUMMARY")
    print("=" * 80)
    print(f"\n   ✅ Sophia examined her internal curiosity state")
    print(f"   ✅ Identified {len(goals)} learning goals from unsatisfied drives")
    print(f"   ✅ Converted goals → {len(url_batch)} actionable URLs")
    print(f"   ✅ Prioritized targets based on drive urgency")

    print(f"\n   🎯 RESULT: Sophia knows what to learn without human input")
    print(f"              This is GENUINE AUTONOMY in action")

    print("\n" + "=" * 80)
    print("💡 WHAT THIS MEANS")
    print("=" * 80)
    print("""
   Before: Sophia needed human-provided seed URLs
           → Limited autonomy, human-directed learning

   After:  Sophia generates learning targets from internal curiosity
           → True autonomy, self-directed learning

   This is the difference between:
   • An AI that waits for instructions
   • An AI that decides what to learn based on internal drives

   The bridge from internal motivation → external action is complete.
    """)
    print("=" * 80)


def demo_drive_manipulation():
    """Demonstrate how unsatisfied drives influence URL generation."""
    print("\n" + "=" * 80)
    print("🧪 DRIVE MANIPULATION EXPERIMENT")
    print("=" * 80)
    print("\nDemonstrating how unsatisfied drives influence learning targets...")

    # Initialize
    curiosity = CuriosityEngine()
    tracker = LearningProgressionTracker()
    mapper = CuriosityURLMapper()

    # Baseline
    print("\n📊 Baseline (before drive manipulation):")
    baseline_state = curiosity.export_for_consciousness_system()
    baseline_batch = mapper.generate_autonomous_seed_batch(
        baseline_state,
        tracker.export_for_consciousness_system(),
        max_total_urls=10
    )

    baseline_sources = {}
    for _, _, source in baseline_batch:
        baseline_sources[source] = baseline_sources.get(source, 0) + 1

    print(f"   Generated {len(baseline_batch)} URLs")
    for source, count in sorted(baseline_sources.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {source}: {count}")

    # Manipulate 'creativity' drive
    print("\n🧪 Experiment: Lowering 'creativity' drive satisfaction...")
    curiosity.update_drive_satisfaction('creativity', -0.6, "Experiment: Creating urgency")

    experimental_state = curiosity.export_for_consciousness_system()
    experimental_batch = mapper.generate_autonomous_seed_batch(
        experimental_state,
        tracker.export_for_consciousness_system(),
        max_total_urls=10
    )

    experimental_sources = {}
    for _, _, source in experimental_batch:
        experimental_sources[source] = experimental_sources.get(source, 0) + 1

    print(f"\n📊 After lowering 'creativity' satisfaction:")
    print(f"   Generated {len(experimental_batch)} URLs")
    for source, count in sorted(experimental_sources.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {source}: {count}")

    # Analysis
    baseline_creativity = baseline_sources.get('drive_creativity', 0)
    experimental_creativity = experimental_sources.get('drive_creativity', 0)

    print(f"\n📈 Analysis:")
    print(f"   Baseline 'drive_creativity' URLs: {baseline_creativity}")
    print(f"   After manipulation: {experimental_creativity}")

    if experimental_creativity > baseline_creativity:
        print(f"   ✅ Unsatisfied drive increased URL generation (+{experimental_creativity - baseline_creativity})")
        print(f"      This proves curiosity state influences autonomous targeting!")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Run main demo
    demo_autonomous_target_generation()

    # Run drive manipulation experiment
    demo_drive_manipulation()

    print("\n✅ Demo complete!")
    print("\n💡 Next step: Try running enhanced_autonomous_learner.py with seed_urls=None")
    print("   to see Sophia learn autonomously from her curiosity.\n")
