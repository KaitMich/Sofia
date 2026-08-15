import sitecustomize
import sys
import re
import asyncio
from typing import Dict, List, Optional
from datetime import datetime

# New autonomous architecture
from unified_orchestration import get_unified_orchestration_system, DataManager, Config
orchestrator = get_unified_orchestration_system()
data_manager = DataManager()

# Legacy imports for compatibility
from sofia.utils.parser import parse_input, extract_symbolic_units, parse_with_emotion
from sofia.crawler.web_parser import process_web_url
from sofia.core.unified_memory import VectorMemory
vector_memory = VectorMemory()
# cluster_vectors_and_plot moved to unified_symbol_system if needed
from sofia.core.unified_memory import log_trail, add_emotions
from sofia.utils.trail_graph import show_trail_graph
from sofia.utils.emotion_handler import predict_emotions
from sofia.core.unified_symbol_system import UnifiedSymbolSystem
symbol_system = UnifiedSymbolSystem()

# Graph tools
from sofia.utils.symbol_drift_plot import show_symbol_drift
from sofia.core.symbol_emotion_cluster import show_emotion_clusters
from sofia.core.symbol_cluster import cluster_vectors_and_plot


def is_url(text):
    return re.match(r"https?://", text.strip()) is not None

def generate_response(user_input, extracted_symbols):
    similar = retrieve_similar_vectors(user_input)
    if not similar:
        return "I'm still learning. Nothing comes to mind yet."

    trust_order = {"high": 0, "medium": 1, "low": 2, "unknown": 3}
    similar.sort(key=lambda x: (trust_order.get(x[1].get("source_trust", "unknown"), 3), -x[0]))

    if any(entry[1].get("source_trust") in ("high", "medium") for entry in similar):
        similar = [entry for entry in similar if entry[1].get("source_trust", "unknown") in ("high", "medium")]

    response = "🧠 Here's what I remember:\n"
    for sim, memory in similar:
        txt = memory["text"]
        trust = memory.get("source_trust", "unknown")
        source_note = f" (source: {memory['source_url']})" if memory.get("source_url") else ""

        if trust == "high":
            trust_note = " — from a trusted source"
        elif trust == "medium":
            trust_note = " — moderately trusted"
        elif trust == "low":
            trust_note = " — caution: low-trust source"
        else:
            trust_note = " — source unknown"

        response += f" - {txt[:100]}...{source_note}{trust_note} (sim={sim:.2f})\n"

    if extracted_symbols:
        response += "\n🔗 Symbolic cues detected:"
        for sym in extracted_symbols:
            response += f"\n → {sym['symbol']} ({sym['name']})"

    return response

async def autonomous_main():
    """Main function using the new autonomous architecture"""
    print("🧠 Autonomous Dual-Brain AI System v2.0")
    print("Enhanced with contextual understanding, privacy protection, and autonomous learning")
    print("Type a thought or paste a URL (type 'exit', 'legacy', or 'status' for commands).\n")
    
    # Start autonomous learning cycle in background
    learning_task = asyncio.create_task(orchestrator.autonomous_learning_cycle())
    
    session_id = None
    conversation_history = []
    
    try:
        while True:
            user_input = input("💬 You: ").strip()
            
            if user_input.lower() in ("exit", "quit"):
                break
            elif user_input.lower() == "legacy":
                print("🔄 Switching to legacy mode...")
                await legacy_main()
                continue
            elif user_input.lower() == "status":
                await show_system_status()
                continue
            elif user_input.lower() == "help":
                show_help()
                continue
            
            if not user_input:
                continue
            
            print("🔄 Processing with autonomous dual-brain system...")
            
            # Process through the orchestrator
            result = await orchestrator.process_user_input(
                user_input=user_input,
                session_id=session_id,
                conversation_history=conversation_history
            )
            
            # Store session ID for continuity
            if not session_id and 'session_id' in result:
                session_id = result['session_id']
            
            # Display results
            await display_processing_result(result, user_input)
            
            # Update conversation history
            conversation_history.append({
                'user': user_input,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep history manageable
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
    
    except KeyboardInterrupt:
        print("\n\n⚡ Interrupted by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")
    finally:
        # Cancel background tasks
        learning_task.cancel()
        try:
            await learning_task
        except asyncio.CancelledError:
            pass
        
        # Show final analytics
        await show_final_analytics()

def legacy_main():
    """Legacy main function for compatibility"""
    print("🧠 Legacy Mode: Symbolic + Vector Memory")
    print("Type a thought or paste a URL (type 'exit' to quit, 'autonomous' to return).\n")

    while True:
        user_input = input("💬 You (Legacy): ").strip()
        if user_input.lower() in ("exit", "quit", "autonomous"):
            break

        if is_url(user_input):
            print("🌐 Detected URL. Parsing web content...")
            process_web_url(user_input)
        else:
            print("📝 Detected input. Parsing and storing...")
            parse_input(user_input)
            vector_memory.store_vector(text=user_input, source_type="user_direct_input")

            # Emotion detection
            emotions = predict_emotions(user_input)
            print("\n💓 Emotions detected:")
            for tag, score in emotions["verified"]:
                print(f"   → {tag} ({score:.2f})")

            add_emotions(user_input, emotions)
            symbols = parse_with_emotion(user_input, emotions["verified"])
            symbol_system.emotion_mapper.update_symbol_emotions(symbols, emotions["verified"])

            for s in symbols:
                s["influencing_emotions"] = emotions["verified"]

            # ✅ Add to symbol memory
            for sym in symbols:
                symbol_system.vector_symbols.add_symbol(
                    glyph=sym["symbol"],
                    name=sym["name"],
                    mathematical_concepts=[sym["matched_keyword"]],
                    metaphorical_concepts=[],
                    learning_phase=1
                )

            if symbols:
                print("\n✨ Extracted symbols:")
                for s in symbols:
                    print(f"   → {s['symbol']} ({s['name']}) [matched: {s['matched_keyword']}]")
            else:
                print("💀 No symbolic units extracted.")
            # Try generating a symbol if none matched
            if not symbols:
                keywords = [k for k in extract_symbolic_units(user_input)]
                new_sym = symbol_system.generate_contextual_symbol(user_input, keywords, emotions["verified"])
                if new_sym:
                    print(f"✨ Created new emergent symbol: {new_sym}")

            matches = vector_memory.retrieve_similar_vectors(user_input)
            log_trail(user_input, symbols, matches)

            response = generate_response(user_input, symbols)
            print("\n🗣️ Response:")
            print(response)

    if user_input.lower() != "autonomous":
        # On exit: run legacy diagnostics
        print("\n🔍 Running legacy diagnostics...")
        cluster_vectors_and_plot(show_graph=True)
        show_trail_graph()
        show_symbol_drift()
        show_emotion_clusters()
        # prune_duplicates() - handled automatically by unified systems

async def display_processing_result(result: Dict, user_input: str):
    """Display the results of autonomous processing"""
    if result.get('quarantined'):
        print(f"🚨 Input quarantined: {result['reason']}")
        print(f"   Risk score: {result['risk_score']:.2f}")
        return
    
    if not result.get('success'):
        print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
        return
    
    # Success case
    print(f"✅ Processed successfully (confidence: {result['confidence']:.2f})")
    print(f"🧠 Route used: {result['route_used']}")
    print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
    print(f"📊 Validation score: {result['validation_score']:.2f}")
    
    # Context insights
    insights = result.get('context_insights', {})
    if insights:
        print(f"🔍 Detected intent: {insights['detected_intent']} (confidence: {insights['confidence']:.2f})")
        if insights.get('ambiguous_terms'):
            print(f"⚠️  Ambiguous terms: {', '.join(insights['ambiguous_terms'])}")
    
    # Brain consultations
    if result.get('brain_consultations'):
        print("🧠 Brain consultations:")
        for consultation in result['brain_consultations']:
            print(f"   → {consultation['brain']}: {consultation['reasoning']} (confidence: {consultation['confidence']:.2f})")
    
    # Result data
    if 'result' in result:
        result_data = result['result']
        if isinstance(result_data, dict):
            if 'memory_id' in result_data:
                print(f"💾 Stored in {result_data['type']} memory: {result_data['memory_id'][:8]}...")
            elif 'recommended_brain' in result_data:
                print(f"🎯 Recommended for: {result_data['recommended_brain']} brain")

async def show_system_status():
    """Show comprehensive system status"""
    print("\n📊 System Status:")
    
    status = orchestrator.get_system_status()
    
    print(f"   Active sessions: {status['active_sessions']}")
    print(f"   Total decisions: {status['total_decisions']}")
    print(f"   Success rate: {status['success_rate']:.2%}")
    print(f"   Quarantine rate: {status['quarantine_rate']:.2%}")
    print(f"   Learning events: {status['learning_events']}")
    
    print("\n🔧 Components:")
    for component, loaded in status['components_loaded'].items():
        status_icon = "✅" if loaded else "❌"
        print(f"   {status_icon} {component}")
    
    print("\n📈 Analytics:")
    dv_stats = status['decision_validator_stats']
    print(f"   Decisions analyzed: {dv_stats['total_decisions']}")
    print(f"   Average feedback score: {dv_stats['average_feedback_score']:.2f}")
    print(f"   Patterns learned: {dv_stats['patterns_learned']}")
    
    ce_stats = status['context_engine_stats']
    print(f"   Ambiguous terms tracked: {ce_stats['ambiguous_terms_tracked']}")
    print(f"   Context patterns learned: {ce_stats['patterns_learned']}")
    print(f"   Overall accuracy: {ce_stats['overall_accuracy']:.2%}")
    
    # Add comprehensive memory status
    print("\n🧠 Memory Inventory:")
    try:
        from sofia.core.unified_memory import get_unified_memory
        memory = get_unified_memory()
        stats = memory.get_unified_stats()
        
        print(f"   📊 Total Memory Items: {stats['total_memory_items']:,}")
        breakdown = stats['breakdown']
        print(f"   📚 Logic Memory: {breakdown['logic_memory']:,} entries")
        print(f"   🎨 Symbolic Memory: {breakdown['symbolic_memory']:,} entries") 
        print(f"   🌉 Bridge Memory: {breakdown['bridge_memory']:,} entries")
        print(f"   🔢 Vector Data: {breakdown['vector_data']:,} entries")
        print(f"   📝 Trail Log: {breakdown['trail_log']:,} entries")
        print(f"   🔮 Symbols: {breakdown['symbols']:,} items")
        print(f"   📋 Occurrences: {breakdown['occurrences']:,} items")
        
    except Exception as e:
        print(f"   ❌ Memory stats unavailable: {e}")

def show_help():
    """Show available commands"""
    print("\n📋 Available Commands:")
    print("   exit/quit    - Exit the system")
    print("   legacy       - Switch to legacy mode")
    print("   status       - Show system status")
    print("   help         - Show this help")
    print("   [URL]        - Process a web URL")
    print("   [text]       - Process text input\n")

async def show_final_analytics():
    """Show final analytics before shutdown"""
    print("\n🔍 Final System Analytics:")
    
    # Get final status
    status = orchestrator.get_system_status()
    
    print(f"📊 Session Summary:")
    print(f"   Total decisions made: {status['total_decisions']}")
    print(f"   Success rate: {status['success_rate']:.2%}")
    print(f"   Learning events triggered: {status['learning_events']}")
    
    # Show decision breakdown
    dv_stats = status['decision_validator_stats']
    if dv_stats['choice_distribution']:
        print(f"\n🧠 Brain Usage Distribution:")
        for brain, percentage in dv_stats['choice_distribution'].items():
            print(f"   {brain}: {percentage:.1%}")
    
    if dv_stats['success_by_choice']:
        print(f"\n✅ Success Rate by Brain:")
        for brain, success_rate in dv_stats['success_by_choice'].items():
            print(f"   {brain}: {success_rate:.2f}")
    
    print("\n🎯 The system has learned from your interactions and improved its decision-making.")
    print("   Next session will benefit from this learning.")

def main():
    """Entry point - choose between autonomous and legacy modes"""
    print("🚀 Autonomous Dual-Brain AI System")
    print("Choose mode:")
    print("  1. Autonomous (recommended) - Full AI with learning and adaptation")
    print("  2. Legacy - Original symbolic + vector system")
    
    while True:
        choice = input("\nEnter choice (1/2) or 'autonomous'/'legacy': ").strip().lower()
        
        if choice in ('1', 'autonomous', 'a'):
            # Run autonomous system
            try:
                asyncio.run(autonomous_main())
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
            break
        elif choice in ('2', 'legacy', 'l'):
            # Run legacy system
            try:
                legacy_main()
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 'autonomous', or 'legacy'")

if __name__ == "__main__":
    main()
