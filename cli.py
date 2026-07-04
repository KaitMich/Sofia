# cli.py - Command Line Interface for Dual Brain AI System

import sys
import argparse
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Import the master orchestrator
try:
    from unified_orchestration import UnifiedOrchestrationSystem, PipelineManager, AutonomousOrchestrator, SystemMode
    ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Unified orchestration not available: {e}")
    ORCHESTRATOR_AVAILABLE = False

# Import shutdown manager
from shutdown_manager import get_shutdown_manager, create_memory_cleanup, create_log_cleanup

class DualBrainCLI:
    """Command Line Interface for the Dual Brain AI System"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.orchestrator: Optional[UnifiedOrchestrationSystem] = None
        self.verbose = False
        self.shutdown_manager = None
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the command line argument parser"""
        parser = argparse.ArgumentParser(
            description="Dual Brain AI System - Autonomous AI with Logic/Symbolic Intelligence",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s saturation start --seed-url URL --zone-name NAME --keywords K1,K2  # Start saturation learning
  %(prog)s saturation status                                                  # Show recent sessions
  %(prog)s saturation event-horizon                                           # View forbidden concepts
  %(prog)s start --mode autonomous           # Start in autonomous mode (LEGACY)
  %(prog)s start --mode interactive         # Start interactive chat mode
  %(prog)s status                           # Show system status
  %(prog)s health                           # Check system health
            """
        )
        
        # Global options
        parser.add_argument('--data-dir', '-d', default='data', 
                          help='Data directory path (default: data)')
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose output')
        parser.add_argument('--config', '-c', default='config.json',
                          help='Configuration file path (default: config.json)')
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Start command
        start_parser = subparsers.add_parser('start', help='Start the AI system')
        start_parser.add_argument('--mode', '-m', choices=['autonomous', 'interactive', 'learning', 'integration', 'maintenance', 'legacy'],
                                default='autonomous', help='System mode to start in (default: autonomous)')
        start_parser.add_argument('--input', '-i', help='Process this input immediately after start')
        start_parser.add_argument('--urls', type=int, default=10, help='Number of URLs to process in autonomous mode')
        
        # Status command
        subparsers.add_parser('status', help='Show system status')
        
        # Stop command
        subparsers.add_parser('stop', help='Stop all running subsystems')
        
        # Migration commands
        subparsers.add_parser('migrate', help='Run unified migration cycle')
        
        # Integration commands
        subparsers.add_parser('integrate', help='Run integration cycle')
        
        # Data analysis
        subparsers.add_parser('analyze', help='Run data analysis')
        
        # Health check
        subparsers.add_parser('health', help='Check system health')
        
        # Backup
        subparsers.add_parser('backup', help='Create system backup')
        
        # Cleanup
        subparsers.add_parser('cleanup', help='Clean up old files')
        
        # Interactive mode
        interact_parser = subparsers.add_parser('interact', help='Start interactive session')
        interact_parser.add_argument('--continuous', action='store_true',
                                   help='Keep session running until manually stopped')
        
        # Learning mode
        learn_parser = subparsers.add_parser('learn', help='Start learning mode')
        learn_parser.add_argument('--phase', type=int, choices=[1, 2, 3], default=1,
                                help='Learning phase to focus on (default: 1)')
        learn_parser.add_argument('--urls', type=int, default=10,
                                help='Number of URLs to process (default: 10)')
        
        # Chat mode
        chat_parser = subparsers.add_parser('chat', help='Start interactive chat')
        chat_parser.add_argument('message', nargs='?', help='Send a message directly')
        
        # Config commands
        config_parser = subparsers.add_parser('config', help='Configuration management')
        config_subparsers = config_parser.add_subparsers(dest='config_action', help='Config actions')
        config_subparsers.add_parser('show', help='Show current configuration')
        config_subparsers.add_parser('reset', help='Reset configuration to defaults')
        
        # Memory commands
        memory_parser = subparsers.add_parser('memory', help='Memory management')
        memory_subparsers = memory_parser.add_subparsers(dest='memory_action', help='Memory actions')
        memory_subparsers.add_parser('stats', help='Show memory statistics')
        memory_subparsers.add_parser('export', help='Export memory data')
        memory_subparsers.add_parser('import', help='Import memory data')

        # Bridge review command
        bridge_parser = subparsers.add_parser('bridge-review',
                                               help='Review and reclassify bridge memory items')
        bridge_parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=True,
                                  help='Preview changes without executing (default: True)')
        bridge_parser.add_argument('--no-dry-run', dest='dry_run', action='store_false',
                                  help='Actually execute reclassification')
        bridge_parser.add_argument('--min-age', type=int, default=7,
                                  help='Minimum age in days for review (default: 7)')

        # Sleep cycle command
        sleep_parser = subparsers.add_parser('sleep-cycle',
                                              help='Run memory consolidation sleep cycle (NREM + REM phases)')
        sleep_parser.add_argument('--nrem-only', action='store_true',
                                 help='Run only NREM phase (memory stabilization)')
        sleep_parser.add_argument('--rem-only', action='store_true',
                                 help='Run only REM phase (insight generation)')
        sleep_parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=False,
                                 help='Preview what would happen without making changes')

        # Test shutdown command (for testing Ctrl+C handling)
        test_shutdown_parser = subparsers.add_parser('test-shutdown',
                                                     help='Test graceful shutdown system (sleeps for 10s, press Ctrl+C to test)')
        test_shutdown_parser.add_argument('--duration', type=int, default=10,
                                         help='Duration to sleep in seconds (default: 10)')

        # Immune system commands
        immune_parser = subparsers.add_parser('immune-status', help='Show immune system health and statistics')

        immune_review_parser = subparsers.add_parser('immune-review', help='Review recent immune decisions')
        immune_review_parser.add_argument('--limit', type=int, default=20,
                                         help='Number of recent decisions to show (default: 20)')

        immune_trust_parser = subparsers.add_parser('immune-trust', help='Show trust history for a domain')
        immune_trust_parser.add_argument('domain', help='Domain to query')
        immune_trust_parser.add_argument('--limit', type=int, default=50,
                                        help='Number of events to show (default: 50)')

        immune_override_parser = subparsers.add_parser('immune-override', help='Human override of immune decision')
        immune_override_parser.add_argument('item_id', help='Item ID to override')
        immune_override_parser.add_argument('outcome', choices=['correct', 'false_positive', 'false_negative'],
                                           help='Correct outcome for this decision')
        immune_override_parser.add_argument('--reason', required=True,
                                           help='Reason for override (required)')

        immune_export_parser = subparsers.add_parser('immune-export', help='Export full immune audit trail')
        immune_export_parser.add_argument('--output', '-o', default='data/immune/audit_export.json',
                                         help='Output file path (default: data/immune/audit_export.json)')
        immune_export_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                                         help='Output format (default: json)')

        # Crawl infrastructure commands
        crawl_status_parser = subparsers.add_parser('crawl-status', help='Show crawl infrastructure status and statistics')

        crawl_add_parser = subparsers.add_parser('crawl-add', help='Add URL(s) to crawl queue')
        crawl_add_parser.add_argument('urls', nargs='+', help='URL(s) to add to queue')
        crawl_add_parser.add_argument('--priority', type=int, default=0,
                                     help='Priority (higher = crawled sooner, default: 0)')
        crawl_add_parser.add_argument('--depth', type=int, default=0,
                                     help='Link depth from seed (default: 0)')

        crawl_queue_parser = subparsers.add_parser('crawl-queue', help='Show crawl queue status')
        crawl_queue_parser.add_argument('--limit', type=int, default=20,
                                       help='Number of pending URLs to show (default: 20)')

        crawl_clear_parser = subparsers.add_parser('crawl-clear', help='Clear completed URLs from queue')
        crawl_clear_parser.add_argument('--older-than', type=int, default=24,
                                       help='Clear items older than N hours (default: 24)')
        crawl_clear_parser.add_argument('--all', action='store_true',
                                       help='Clear ALL URLs (use with caution)')

        robots_check_parser = subparsers.add_parser('robots-check', help='Check robots.txt status for a URL')
        robots_check_parser.add_argument('url', help='URL to check')

        crawl_health_parser = subparsers.add_parser('crawl-health', help='Run comprehensive crawl health check')

        # ========================================================================
        # SATURATION LEARNING COMMANDS (Associative Emergence)
        # ========================================================================
        saturation_parser = subparsers.add_parser('saturation', help='Associative Emergence / Saturation Learning')
        saturation_subparsers = saturation_parser.add_subparsers(dest='saturation_action', help='Saturation actions')

        # saturation start
        saturation_start_parser = saturation_subparsers.add_parser('start', help='Start a saturation learning session')
        saturation_start_parser.add_argument('--seed-url', required=True, help='Starting URL for learning (Wikipedia recommended)')
        saturation_start_parser.add_argument('--zone-name', required=True, help='Descriptive name for this semantic zone')
        saturation_start_parser.add_argument('--keywords', required=True, help='Comma-separated zone keywords (5-10 recommended)')
        saturation_start_parser.add_argument('--allowed-distance', type=float, default=0.5,
                                            help='Max semantic distance from zone centroid (0.0-1.0, default: 0.5)')
        saturation_start_parser.add_argument('--saturation-threshold', type=float, default=0.55,
                                            help='Phase transition threshold (0.0-1.0, default: 0.55)')
        saturation_start_parser.add_argument('--max-urls', type=int, default=50,
                                            help='Max URLs to process in zone (default: 50)')

        # saturation status
        saturation_status_parser = saturation_subparsers.add_parser('status', help='Show recent saturation sessions')
        saturation_status_parser.add_argument('--limit', type=int, default=10,
                                             help='Number of recent sessions to show (default: 10)')

        # saturation event-horizon
        saturation_horizon_parser = saturation_subparsers.add_parser('event-horizon',
                                                                     help='Show concepts on event horizon (seen but forbidden)')
        saturation_horizon_parser.add_argument('--limit', type=int, default=20,
                                              help='Number of concepts to show (default: 20)')
        saturation_horizon_parser.add_argument('--zone', help='Filter by zone name')

        # saturation chain
        saturation_chain_parser = saturation_subparsers.add_parser('chain',
                                                                   help='Run multi-zone learning chain')
        saturation_chain_parser.add_argument('--seed-url', required=True, help='Starting URL')
        saturation_chain_parser.add_argument('--keywords', required=True, help='Initial keywords (comma-separated)')
        saturation_chain_parser.add_argument('--max-zones', type=int, default=5,
                                            help='Maximum zones to traverse (default: 5)')
        saturation_chain_parser.add_argument('--max-urls-per-zone', type=int, default=50,
                                            help='Max URLs per zone (default: 50)')

        # ========================================================================
        # CURRICULUM COMMANDS (Sofia's Learning System)
        # ========================================================================
        curriculum_parser = subparsers.add_parser('curriculum',
            help='Curriculum learning system - Sofia\'s developmental journey')
        curriculum_subparsers = curriculum_parser.add_subparsers(dest='curriculum_action',
            help='Curriculum actions')

        # curriculum status
        curriculum_status_parser = curriculum_subparsers.add_parser('status',
            help='Show curriculum progress, consciousness metrics, and running tasks')
        curriculum_status_parser.add_argument('--task-id',
            help='Show specific background task status')

        # curriculum learn
        curriculum_learn_parser = curriculum_subparsers.add_parser('learn',
            help='Start a learning session (autonomous or seeded)')
        curriculum_learn_parser.add_argument('--seeds',
            help='Comma-separated seed URLs (omit for autonomous mode - Sofia decides)')
        curriculum_learn_parser.add_argument('--urls', type=int, default=50,
            help='Target number of URLs to process (default: 50)')
        curriculum_learn_parser.add_argument('--focus', default='general',
            choices=['general', 'ai_consciousness', 'science', 'philosophy', 'technology'],
            help='Learning focus area (default: general)')
        curriculum_learn_parser.add_argument('--background', action='store_true',
            help='Run in background (returns immediately with task ID)')

        # curriculum complete-step
        curriculum_step_parser = curriculum_subparsers.add_parser('complete-step',
            help='Complete a specific curriculum step (1-4)')
        curriculum_step_parser.add_argument('step', type=int, choices=[1, 2, 3, 4],
            help='Step number to complete')
        curriculum_step_parser.add_argument('--topic',
            help='Specific topic within step (e.g., "electromagnetism" for step 1)')
        curriculum_step_parser.add_argument('--urls', type=int, default=50,
            help='Target URLs to process (default: 50)')
        curriculum_step_parser.add_argument('--background', action='store_true',
            help='Run in background')
        curriculum_step_parser.add_argument('--witness', action='store_true',
            help='Witness this milestone in foreground with reflection capture (for graduation moments)')

        # curriculum topic
        curriculum_topic_parser = curriculum_subparsers.add_parser('topic',
            help='Learn a specific topic on demand')
        curriculum_topic_parser.add_argument('topic',
            help='Topic name (e.g., "quantum physics") or Wikipedia URL')
        curriculum_topic_parser.add_argument('--urls', type=int, default=30,
            help='Target URLs to process (default: 30)')
        curriculum_topic_parser.add_argument('--background', action='store_true',
            help='Run in background')

        return parser
    
    def print_status(self, message: str, level: str = "info"):
        """Print status message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "error":
            icon = "❌"
        elif level == "warning":
            icon = "⚠️ "
        elif level == "success":
            icon = "✅"
        elif level == "info":
            icon = "ℹ️ "
        else:
            icon = "  "
        
        print(f"[{timestamp}] {icon} {message}")
    
    def ensure_orchestrator(self) -> bool:
        """Ensure orchestrator is initialized"""
        if not ORCHESTRATOR_AVAILABLE:
            self.print_status("Master orchestrator not available", "error")
            return False
            
        if self.orchestrator is None:
            try:
                self.print_status(f"Initializing orchestrator with data directory: {self.data_dir}")
                self.orchestrator = UnifiedOrchestrationSystem(data_dir=self.data_dir)
                self.print_status("Orchestrator initialized successfully", "success")
                return True
            except Exception as e:
                self.print_status(f"Failed to initialize orchestrator: {e}", "error")
                return False
        return True
    
    def cmd_start(self, args) -> int:
        """Start the AI system"""
        if not self.ensure_orchestrator():
            return 1

        try:
            mode = SystemMode(args.mode)
            self.print_status(f"Starting system in {mode.value} mode...")

            # Prepare kwargs based on mode
            kwargs = {}
            if mode == SystemMode.AUTONOMOUS:
                kwargs['target_urls'] = args.urls

            result = self.orchestrator.start_system(mode, **kwargs)

            if result.get('status') == 'error':
                self.print_status(f"Failed to start system: {result.get('error')}", "error")
                return 1

            self.print_status(f"System started successfully in {mode.value} mode", "success")

            if self.verbose:
                subsystems = result.get('subsystems_started', [])
                if subsystems:
                    self.print_status(f"Active subsystems: {', '.join(subsystems)}")

            # Process immediate input if provided
            if args.input:
                self.print_status(f"Processing input: {args.input}")
                input_result = self.orchestrator.process_input(args.input)
                print(json.dumps(input_result, indent=2))

            # If autonomous mode, start the autonomous lifecycle loop
            if mode == SystemMode.AUTONOMOUS:
                self.print_status("Starting autonomous lifecycle loop with idle detection...")
                import asyncio
                asyncio.run(self.orchestrator.run_autonomous_loop())

            return 0

        except Exception as e:
            self.print_status(f"Error starting system: {e}", "error")
            return 1
    
    def cmd_status(self, args) -> int:
        """Show system status"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            status = self.orchestrator.get_system_status()

            print("\n" + "="*60)
            print("🤖 DUAL BRAIN AI SYSTEM STATUS")
            print("="*60)

            print(f"\n🔄 Current Mode: {status.get('learning_mode', 'unknown')}")
            print(f"📊 Health: {status.get('system_health', 'unknown')}")
            print(f"⏱️  Uptime: {status.get('uptime', 'N/A')}")

            # Active subsystems from import status
            import_status = status.get('import_status', {})
            successful = import_status.get('successful', [])
            if successful:
                print(f"\n✅ Active Subsystems ({len(successful)}):")
                for subsystem in successful:
                    print(f"   • {subsystem}")
            else:
                print("\n💤 No active subsystems")

            failed = import_status.get('failed', [])
            if failed:
                print(f"\n⚠️  Unavailable Modules ({len(failed)}):")
                for module in failed:
                    print(f"   • {module}")

            print(f"\n💾 Memory:")
            print(f"   Memory active:        {'✅' if status.get('memory_active') else '❌'}")
            print(f"   Symbols active:       {'✅' if status.get('symbols_active') else '❌'}")
            print(f"   Orchestration active: {'✅' if status.get('orchestration_active') else '❌'}")

            file_stats = status.get('file_statistics', {})
            if file_stats:
                print(f"   Data files: {file_stats.get('total_files', 'N/A')}")
                total_bytes = file_stats.get('total_size_bytes', 0)
                if total_bytes:
                    print(f"   Total size: {total_bytes / (1024*1024):.1f} MB")

            print(f"\n📈 Session Info:")
            print(f"   Active sessions:        {status.get('active_sessions', 0)}")
            print(f"   Reasoning chain length:  {status.get('reasoning_chain_length', 0)}")
            print(f"   Data directory:          {status.get('data_dir', 'N/A')}")

            return 0
            
        except Exception as e:
            self.print_status(f"Error getting status: {e}", "error")
            return 1
    
    def cmd_stop(self, args) -> int:
        """Stop all running subsystems"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Stopping all subsystems...")
            result = self.orchestrator.stop_system()
            
            stopped = result.get('stopped_subsystems', [])
            if stopped:
                self.print_status(f"Stopped {len(stopped)} subsystems: {', '.join(stopped)}", "success")
            else:
                self.print_status("No subsystems were running")
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error stopping system: {e}", "error")
            return 1
    
    def cmd_migrate(self, args) -> int:
        """Run migration cycle"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Starting migration cycle...")
            result = self.orchestrator.execute_command('migration_cycle')
            
            if result.get('status') == 'completed':
                self.print_status("Migration cycle completed successfully", "success")
                if self.verbose:
                    print(f"   Session ID: {result.get('session_id')}")
                    print(f"   Execution time: {result.get('execution_time', 0):.2f}s")
            else:
                self.print_status(f"Migration cycle failed: {result.get('error')}", "error")
                return 1
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error running migration: {e}", "error")
            return 1
    
    def cmd_integrate(self, args) -> int:
        """Run integration cycle"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Starting integration cycle...")
            result = self.orchestrator.execute_command('integration_cycle')
            
            if result.get('status') == 'completed':
                self.print_status("Integration cycle completed successfully", "success")
                if self.verbose:
                    print(f"   Cycle ID: {result.get('cycle_id')}")
                    print(f"   Integration score: {result.get('integration_score', 0):.2f}")
            else:
                self.print_status(f"Integration cycle failed: {result.get('error')}", "error")
                return 1
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error running integration: {e}", "error")
            return 1
    
    def cmd_analyze(self, args) -> int:
        """Run data analysis"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Running data analysis...")
            result = self.orchestrator.execute_command('data_analysis')
            
            if result.get('status') == 'completed':
                self.print_status("Data analysis completed successfully", "success")
                print(f"   Total files analyzed: {result.get('total_files', 0)}")
                print(f"   Total data size: {result.get('total_size_mb', 0):.1f} MB")
            else:
                self.print_status(f"Data analysis failed: {result.get('error')}", "error")
                return 1
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error running analysis: {e}", "error")
            return 1
    
    def cmd_health(self, args) -> int:
        """Check system health"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Checking system health...")
            result = self.orchestrator.execute_command('system_health')
            
            print(f"\n🏥 System Health: {result.get('overall_status', 'unknown').upper()}")
            print(f"   Timestamp: {result.get('timestamp', 'unknown')}")
            print(f"   Data files: {result.get('data_files', 0)}")
            
            subsystems = result.get('subsystems', {})
            if subsystems:
                print(f"\n🔧 Subsystem Status:")
                for name, status in subsystems.items():
                    available = "✅" if status.get('available') else "❌"
                    active = "🟢" if status.get('active') else "⭕"
                    print(f"   {available} {active} {name}")
            
            warnings = result.get('warnings', [])
            if warnings:
                print(f"\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"   • {warning}")
            
            errors = result.get('errors', [])
            if errors:
                print(f"\n❌ Errors:")
                for error in errors:
                    print(f"   • {error}")
                return 1
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error checking health: {e}", "error")
            return 1
    
    def cmd_backup(self, args) -> int:
        """Create system backup"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Creating system backup...")
            result = self.orchestrator.execute_command('backup')
            
            if result.get('status') == 'completed':
                self.print_status("Backup created successfully", "success")
                print(f"   Location: {result.get('backup_dir')}")
                print(f"   Files backed up: {result.get('files_backed_up', 0)}")
            else:
                self.print_status(f"Backup failed: {result.get('error')}", "error")
                return 1
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error creating backup: {e}", "error")
            return 1
    
    def cmd_cleanup(self, args) -> int:
        """Clean up old files"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status("Running system cleanup...")
            result = self.orchestrator.execute_command('cleanup')
            
            if result.get('status') == 'completed':
                cleaned = result.get('cleaned_items', [])
                if cleaned:
                    self.print_status(f"Cleanup completed - removed {len(cleaned)} items", "success")
                    if self.verbose:
                        for item in cleaned:
                            print(f"   • {item}")
                else:
                    self.print_status("No cleanup needed")
            else:
                self.print_status(f"Cleanup failed: {result.get('error')}", "error")
                return 1
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error during cleanup: {e}", "error")
            return 1
    
    def cmd_interact(self, args) -> int:
        """Start interactive session"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            # Start in interactive mode
            mode_result = self.orchestrator.start_system(SystemMode.INTERACTIVE)
            if mode_result.get('status') == 'error':
                self.print_status(f"Failed to start interactive mode: {mode_result.get('error')}", "error")
                return 1
            
            self.print_status("Interactive session started", "success")
            print("\nType 'exit' to end the session")
            print("-" * 50)
            
            while True:
                try:
                    user_input = input("\n🗣️  You: ").strip()
                    
                    if user_input.lower() in ['exit', 'quit']:
                        break
                    
                    if not user_input:
                        continue
                    
                    # Process input
                    result = self.orchestrator.process_input(user_input)
                    
                    if result.get('error'):
                        print(f"❌ Error: {result['error']}")
                    else:
                        response = result.get('response', 'No response generated')
                        print(f"\n🤖 AI: {response}")
                        
                except KeyboardInterrupt:
                    print("\n\nSession interrupted. Type 'exit' to quit properly.")
                    break
                except EOFError:
                    break
            
            # Stop the session
            self.orchestrator.stop_system()
            self.print_status("Interactive session ended")
            return 0
            
        except Exception as e:
            self.print_status(f"Error in interactive session: {e}", "error")
            return 1
    
    def cmd_learn(self, args) -> int:
        """Start learning mode"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            self.print_status(f"Starting learning mode (Phase {args.phase})...")
            
            # Start in learning mode
            mode_result = self.orchestrator.start_system(SystemMode.LEARNING, 
                                                        phase=args.phase, 
                                                        urls=args.urls)
            
            if mode_result.get('status') == 'error':
                self.print_status(f"Failed to start learning mode: {mode_result.get('error')}", "error")
                return 1
            
            self.print_status("Learning mode started successfully", "success")
            
            # Learning mode typically runs autonomously
            self.print_status("Learning is running autonomously...")
            self.print_status("Use 'status' command to monitor progress")
            
            return 0
            
        except Exception as e:
            self.print_status(f"Error starting learning mode: {e}", "error")
            return 1
    
    def cmd_chat(self, args) -> int:
        """Start chat mode or send a single message"""
        if not self.ensure_orchestrator():
            return 1
            
        try:
            # Start in interactive mode
            mode_result = self.orchestrator.start_system(SystemMode.INTERACTIVE)
            if mode_result.get('status') == 'error':
                self.print_status(f"Failed to start chat mode: {mode_result.get('error')}", "error")
                return 1
            
            if args.message:
                # Send single message
                result = self.orchestrator.process_input(args.message)
                
                if result.get('error'):
                    print(f"❌ Error: {result['error']}")
                    return 1
                else:
                    response = result.get('response', 'No response generated')
                    print(f"🤖 AI: {response}")
            else:
                # Interactive chat
                self.print_status("Chat mode started - type your messages", "success")
                print("Type 'exit' to end the chat")
                print("-" * 50)
                
                while True:
                    try:
                        user_input = input("\n💬 You: ").strip()
                        
                        if user_input.lower() in ['exit', 'quit']:
                            break
                        
                        if not user_input:
                            continue
                        
                        result = self.orchestrator.process_input(user_input)
                        
                        if result.get('error'):
                            print(f"❌ Error: {result['error']}")
                        else:
                            response = result.get('response', 'No response generated')
                            print(f"\n🤖 AI: {response}")
                            
                    except KeyboardInterrupt:
                        print("\n\nChat interrupted. Type 'exit' to quit properly.")
                        break
                    except EOFError:
                        break
            
            # Stop the session
            self.orchestrator.stop_system()
            return 0
            
        except Exception as e:
            self.print_status(f"Error in chat mode: {e}", "error")
            return 1
    
    def cmd_config(self, args) -> int:
        """Configuration management"""
        if args.config_action == 'show':
            if self.ensure_orchestrator():
                config = self.orchestrator.config
                print("\n📋 Current Configuration:")
                print(json.dumps(config, indent=2))
                return 0
            return 1
        elif args.config_action == 'reset':
            # Reset configuration logic would go here
            self.print_status("Configuration reset (not implemented)", "warning")
            return 0
        else:
            self.print_status("No config action specified", "error")
            return 1
    
    def cmd_memory(self, args) -> int:
        """Memory management"""
        if args.memory_action == 'stats':
            if self.ensure_orchestrator():
                status = self.orchestrator.get_system_status()
                print("\n🧠 Memory Statistics:")
                mem = status.memory_usage
                print(f"   Data files: {mem.get('data_files', 0)}")
                print(f"   Total size: {mem.get('total_size_mb', 0):.1f} MB")
                return 0
            return 1
        else:
            self.print_status(f"Memory action '{args.memory_action}' not implemented", "warning")
            return 0

    def cmd_bridge_review(self, args) -> int:
        """
        Review bridge memory and reclassify eligible items.

        Bridge memory holds ambiguous items until enough context accumulates
        to classify them as Logic or Symbolic. This command reviews items
        and moves them when they have sufficient related neighbors.
        """
        try:
            from memory_management import run_bridge_reclassification_review

            mode = "DRY RUN (preview only)" if args.dry_run else "LIVE (will make changes)"
            self.print_status(f"Bridge Memory Review - {mode}")
            print(f"   Minimum item age: {args.min_age} days\n")

            results = run_bridge_reclassification_review(
                dry_run=args.dry_run,
                min_age_days=args.min_age
            )

            if 'error' in results:
                self.print_status(f"Error: {results['error']}", "error")
                return 1

            # Display results
            print("📊 Review Results:")
            print(f"   Items in bridge:     {results.get('items_reviewed', 0)}")
            print(f"   Ready to reclassify: {results.get('items_ready', 0)}")

            if args.dry_run:
                print(f"   Would reclassify:    {results.get('items_ready', 0)}")
            else:
                print(f"   Actually reclassified: {results.get('items_reclassified', 0)}")
                print(f"     → To Logic:        {results.get('to_logic', 0)}")
                print(f"     → To Symbolic:     {results.get('to_symbolic', 0)}")

            print(f"   Remaining in bridge: {results.get('items_remaining', 0)}")

            # Show details for each item
            details = results.get('details', [])
            if details:
                print("\n📝 Item Details:")
                for d in details:
                    status_icon = "✓ READY" if d.get('should_reclassify') else "○ WAIT"
                    target = f"→ {d.get('target')}" if d.get('target') else ""
                    item_id = d.get('id', 'unknown')[:20]
                    print(f"   {status_icon} {item_id}... {target}")
                    print(f"         Related: {d.get('related_count', 0)} items | {d.get('reason', '')}")

            if args.dry_run:
                print("\n💡 To execute reclassification, run with --no-dry-run")
                self.print_status("Preview complete (no changes made)", "info")
            else:
                self.print_status("Reclassification complete", "success")

            return 0

        except ImportError as e:
            self.print_status(f"Bridge reclassifier not available: {e}", "error")
            return 1
        except Exception as e:
            self.print_status(f"Bridge review failed: {e}", "error")
            return 1

    def cmd_sleep_cycle(self, args) -> int:
        """
        Run memory consolidation sleep cycle.

        Implements biomimetic sleep architecture:
        - NREM Phase (Deep Sleep): Stabilize bridge memories into permanent storage
        - REM Phase (Dream Sleep): Generate insights from distant connections
        """
        try:
            from dream_cycle import DreamCycleOrchestrator

            # Determine mode
            if args.nrem_only and args.rem_only:
                self.print_status("Cannot specify both --nrem-only and --rem-only", "error")
                return 1

            mode_desc = "FULL CYCLE (NREM + REM)"
            if args.nrem_only:
                mode_desc = "NREM ONLY (Stabilization)"
            elif args.rem_only:
                mode_desc = "REM ONLY (Insight Generation)"

            dry_run_desc = " [DRY RUN]" if args.dry_run else ""
            self.print_status(f"Sleep Cycle - {mode_desc}{dry_run_desc}")

            # Initialize orchestrator
            orchestrator = DreamCycleOrchestrator(data_dir=self.data_dir)

            # Run appropriate phase(s)
            if args.dry_run:
                print("\n⚠️  DRY RUN MODE: No changes will be made to memory")
                print("   This is a preview only. Use without --dry-run to execute.\n")

            if args.nrem_only:
                # NREM phase only
                print("\n🌙 Running NREM Phase (Deep Sleep)...")
                nrem_results = orchestrator.nrem_phase()

                print("\n📊 NREM Results:")
                print(f"   Memories stabilized: {nrem_results.get('items_reclassified', 0)}")
                print(f"     → To Logic:        {nrem_results.get('to_logic', 0)}")
                print(f"     → To Symbolic:     {nrem_results.get('to_symbolic', 0)}")
                print(f"   Remaining in bridge: {nrem_results.get('items_remaining', 0)}")

            elif args.rem_only:
                # REM phase only
                print("\n✨ Running REM Phase (Dream Sleep)...")
                rem_results = orchestrator.rem_phase()

                print("\n📊 REM Results:")
                print(f"   Memories sampled:    {rem_results.get('memories_sampled', 0)}")
                print(f"   Connections found:   {rem_results.get('distant_connections_found', 0)}")
                print(f"   Insights generated:  {rem_results.get('insights_generated', 0)}")
                print(f"   Values affected:     {rem_results.get('values_affected', 0)}")

                # Show insights
                insights = rem_results.get('insights_created', [])
                if insights:
                    print("\n✨ Insights Generated:")
                    for insight in insights:
                        print(f"     • {insight}")

            else:
                # Full cycle
                results = orchestrator.run_sleep_cycle()

                print("\n" + "="*70)
                print("SLEEP CYCLE SUMMARY")
                print("="*70)
                print(f"\n⏱️  Duration: {results.get('duration_seconds', 0):.1f}s")
                print(f"\n🌙 NREM Phase:")
                print(f"   Memories stabilized: {results.get('total_consolidations', 0)}")

                print(f"\n✨ REM Phase:")
                print(f"   Insights generated:  {results.get('total_insights', 0)}")
                print(f"   Values affected:     {results.get('values_affected', 0)}")

                # Show insights
                rem_results = results.get('rem_results', {})
                insights = rem_results.get('insights_created', [])
                if insights:
                    print("\n💡 New Insights:")
                    for insight in insights:
                        print(f"     • {insight}")

            if args.dry_run:
                print("\n💡 This was a dry run. No changes were made.")
                self.print_status("Dry run complete", "info")
            else:
                self.print_status("Sleep cycle complete", "success")

            return 0

        except ImportError as e:
            self.print_status(f"Dream cycle system not available: {e}", "error")
            return 1
        except Exception as e:
            self.print_status(f"Sleep cycle failed: {e}", "error")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return 1

    def cmd_test_shutdown(self, args) -> int:
        """Test the graceful shutdown system."""
        import time

        print("\n" + "="*70)
        print("SHUTDOWN SYSTEM TEST")
        print("="*70)
        print(f"\nThis command will sleep for {args.duration} seconds.")
        print("Press Ctrl+C at any time to test graceful shutdown handling.\n")
        print("The shutdown manager will:")
        print("  1. Catch the SIGINT signal")
        print("  2. Run all registered cleanup functions")
        print("  3. Save memory to disk")
        print("  4. Log the shutdown event")
        print("  5. Exit gracefully")
        print("\n" + "="*70 + "\n")

        try:
            # Initialize shutdown manager with test cleanup functions
            if self.shutdown_manager is None:
                self.shutdown_manager = get_shutdown_manager(
                    data_dir=self.data_dir,
                    verbose=True
                )

            # Register test cleanup functions
            def test_cleanup_1():
                print("    💾 Saving test data...")
                time.sleep(0.3)

            def test_cleanup_2():
                print("    🔌 Closing test connections...")
                time.sleep(0.2)

            def test_cleanup_3():
                print("    📝 Writing final test log...")

            self.shutdown_manager.register_cleanup(
                test_cleanup_1, "Save test data", priority=10
            )
            self.shutdown_manager.register_cleanup(
                test_cleanup_2, "Close test connections", priority=5
            )
            self.shutdown_manager.register_cleanup(
                test_cleanup_3, "Write final log", priority=1
            )

            # Also register real memory cleanup if available
            try:
                from unified_memory import get_unified_memory
                unified_memory = get_unified_memory(data_dir=self.data_dir)
                self.shutdown_manager.register_cleanup(
                    create_memory_cleanup(unified_memory),
                    "Save unified memory",
                    priority=100
                )
                print("✅ Registered real memory cleanup function\n")
            except Exception as e:
                print(f"⚠️  Could not register memory cleanup: {e}\n")

            # Install signal handlers
            self.shutdown_manager.install_handlers()
            print("✅ Signal handlers installed\n")

            # Sleep with progress indicator
            for i in range(args.duration):
                print(f"  ⏳ Working... {i+1}/{args.duration} seconds")
                time.sleep(1)

            print("\n✅ Test completed without interruption")
            print("   (No Ctrl+C was pressed)\n")

            # Trigger shutdown manually
            self.shutdown_manager.shutdown(reason="Test completed successfully")

            return 0

        except KeyboardInterrupt:
            # This shouldn't be reached if signal handler works
            print("\n⚠️  KeyboardInterrupt caught in main (signal handler may have failed)")
            if self.shutdown_manager:
                self.shutdown_manager.shutdown(reason="KeyboardInterrupt in main")
            return 1
        except Exception as e:
            self.print_status(f"Test failed: {e}", "error")
            return 1

    def cmd_immune_status(self, args) -> int:
        """Show immune system health and statistics"""
        try:
            from immune_audit import ImmuneAudit

            self.print_status("Checking immune system health...", "info")
            audit = ImmuneAudit(self.data_dir)

            # Get and display health report
            health = audit.get_system_health_report()

            print(f"\n{'='*70}")
            print(f"IMMUNE SYSTEM HEALTH REPORT")
            print(f"{'='*70}\n")

            print(f"Overall Status: {health['overall_status']}\n")

            # Decisions
            if health['decisions']:
                d = health['decisions']
                print(f"📊 DECISION METRICS:")
                print(f"   Total decisions: {d['total']}")
                print(f"   Evaluated: {d['evaluated']}")
                print(f"   Accuracy: {d['accuracy']:.1%}")
                print(f"   False positive rate: {d['fp_rate']:.1%}")
                print(f"   False negative rate: {d['fn_rate']:.1%}\n")

            # Trust
            if health['trust']:
                t = health['trust']
                print(f"🔒 TRUST METRICS:")
                print(f"   Total domains tracked: {t['total_domains']}")
                print(f"   Trusted domains (≥0.7): {t['trusted_domains']}")
                print(f"   Untrusted domains (≤0.3): {t['untrusted_domains']}")
                print(f"   Average trust: {t['average_trust']:.2f}\n")

            # Corroboration
            if health['corroboration']:
                c = health['corroboration']
                print(f"✓ CORROBORATION METRICS:")
                print(f"   Fact clusters: {c['total_fact_clusters']}")
                print(f"   Corroborated facts: {c['corroborated_facts']}")
                print(f"   Pending verification: {c['pending_verification']}")
                print(f"   Total sightings: {c['total_sightings']}\n")

            # Show pattern performance
            audit.print_pattern_performance_summary()

            self.print_status("Health check complete", "success")
            return 0

        except Exception as e:
            self.print_status(f"Error checking immune health: {e}", "error")
            return 1

    def cmd_immune_review(self, args) -> int:
        """Review recent immune decisions"""
        try:
            from immune_audit import ImmuneAudit

            self.print_status(f"Retrieving last {args.limit} decisions...", "info")
            audit = ImmuneAudit(self.data_dir)

            audit.print_recent_decisions_summary(limit=args.limit)

            self.print_status("Review complete", "success")
            return 0

        except Exception as e:
            self.print_status(f"Error reviewing decisions: {e}", "error")
            return 1

    def cmd_immune_trust(self, args) -> int:
        """Show trust history for a domain"""
        try:
            from immune_audit import ImmuneAudit

            self.print_status(f"Retrieving trust history for {args.domain}...", "info")
            audit = ImmuneAudit(self.data_dir)

            # Get trust evolution
            evolution = audit.get_trust_evolution(args.domain, limit=args.limit)

            if not evolution:
                print(f"\nNo trust data found for domain: {args.domain}")
                return 0

            print(f"\n{'='*70}")
            print(f"TRUST EVOLUTION: {args.domain}")
            print(f"{'='*70}\n")

            # Current trust
            current_trust = evolution[-1].new_score if evolution else 0.5
            print(f"Current trust: {current_trust:.2f}\n")

            # Trust history
            print(f"Trust History (showing {len(evolution)} events):\n")

            for entry in evolution:
                # Format timestamp
                try:
                    dt = datetime.fromisoformat(entry.timestamp)
                    time_str = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = entry.timestamp[:16]

                # Format delta with arrow
                if entry.delta > 0:
                    delta_str = f"+{entry.delta:.2f} ↑"
                    arrow = "📈"
                elif entry.delta < 0:
                    delta_str = f"{entry.delta:.2f} ↓"
                    arrow = "📉"
                else:
                    delta_str = "±0.00"
                    arrow = "→"

                print(f"[{time_str}] {arrow} {entry.old_score:.2f} → {entry.new_score:.2f} ({delta_str})")
                print(f"   {entry.reason}")
                print()

            self.print_status("Trust history retrieved", "success")
            return 0

        except Exception as e:
            self.print_status(f"Error retrieving trust history: {e}", "error")
            return 1

    def cmd_immune_override(self, args) -> int:
        """Human override of immune decision"""
        try:
            from self_correction import SelfCorrection

            self.print_status(f"Recording human override for {args.item_id}...", "info")

            correction = SelfCorrection(self.data_dir)

            # Record the override
            evidence = f"Human override: {args.reason}"
            correction.record_outcome(args.item_id, args.outcome, evidence)

            self.print_status(f"Override recorded: {args.outcome}", "success")
            print(f"\n✅ Decision {args.item_id} marked as '{args.outcome}'")
            print(f"   Reason: {args.reason}")
            print(f"\nThis override will be used for pattern weight adjustment in the next self-correction cycle.")

            return 0

        except Exception as e:
            self.print_status(f"Error recording override: {e}", "error")
            return 1

    def cmd_immune_export(self, args) -> int:
        """Export full immune audit trail"""
        try:
            from immune_audit import ImmuneAudit

            self.print_status(f"Exporting immune audit to {args.output}...", "info")

            audit = ImmuneAudit(self.data_dir)
            audit.export_full_audit(args.output, format=args.format)

            self.print_status(f"Audit exported successfully", "success")
            return 0

        except Exception as e:
            self.print_status(f"Error exporting audit: {e}", "error")
            return 1

    # ═══════════════════════════════════════════════════════════════════════
    # CRAWL INFRASTRUCTURE COMMANDS
    # ═══════════════════════════════════════════════════════════════════════

    def cmd_crawl_status(self, args) -> int:
        """Show crawl infrastructure status and statistics"""
        try:
            from crawl_orchestrator import CrawlOrchestrator

            self.print_status("Crawl Infrastructure Status", "info")
            print("=" * 60)

            orchestrator = CrawlOrchestrator(data_dir=self.data_dir)
            stats = orchestrator.get_stats()

            # Queue stats
            print("\n📊 URL QUEUE:")
            print(f"   Pending:        {stats['queue']['pending']}")
            print(f"   In Progress:    {stats['queue']['in_progress']}")
            print(f"   Completed:      {stats['queue']['completed']}")
            print(f"   Failed:         {stats['queue']['failed']}")
            print(f"   Blocked (robots): {stats['queue']['blocked_robots']}")
            print(f"   Blocked (immune): {stats['queue']['blocked_immune']}")
            print(f"   Total URLs:     {stats['queue']['total_urls']}")

            # Rate limiter stats
            print("\n⏱️  RATE LIMITER:")
            print(f"   Tracked domains:    {stats['rate_limiter']['total_domains']}")
            print(f"   Total requests:     {stats['rate_limiter']['total_requests']}")
            print(f"   Avg crawl delay:    {stats['rate_limiter']['avg_crawl_delay']:.1f}s")
            print(f"   Min delay setting:  {stats['rate_limiter']['min_delay_setting']:.1f}s")

            # Robots.txt cache stats
            print("\n🤖 ROBOTS.TXT CACHE:")
            print(f"   Cached domains:     {stats['robots_cache']['total_cached_domains']}")
            print(f"   Valid cache:        {stats['robots_cache']['valid_cached_domains']}")
            print(f"   Cache hit rate:     {stats['robots_cache']['cache_hit_rate']:.1f}%")
            print(f"   Total checks:       {stats['robots_cache']['total_checks']}")
            print(f"   Allowed:            {stats['robots_cache']['allowed_checks']}")
            print(f"   Blocked:            {stats['robots_cache']['blocked_checks']}")

            # Top domains in queue
            if stats['queue']['top_domains']:
                print("\n🔝 TOP DOMAINS IN QUEUE:")
                for domain, count in stats['queue']['top_domains'][:5]:
                    print(f"   {domain}: {count} URLs")

            return 0

        except Exception as e:
            self.print_status(f"Error getting crawl status: {e}", "error")
            return 1

    def cmd_crawl_add(self, args) -> int:
        """Add URL(s) to crawl queue"""
        try:
            from crawl_orchestrator import CrawlOrchestrator

            orchestrator = CrawlOrchestrator(data_dir=self.data_dir)

            added_count = 0
            for url in args.urls:
                success = orchestrator.add_url(url, priority=args.priority, depth=args.depth)
                if success:
                    added_count += 1
                    self.print_status(f"Added: {url} (priority: {args.priority}, depth: {args.depth})", "success")
                else:
                    self.print_status(f"Already in queue: {url}", "warning")

            print(f"\n✅ Added {added_count}/{len(args.urls)} URLs to queue")
            return 0

        except Exception as e:
            self.print_status(f"Error adding URLs: {e}", "error")
            return 1

    def cmd_crawl_queue(self, args) -> int:
        """Show crawl queue status"""
        try:
            from crawl_orchestrator import CrawlOrchestrator
            import sqlite3

            orchestrator = CrawlOrchestrator(data_dir=self.data_dir)

            self.print_status(f"Crawl Queue (showing up to {args.limit} pending URLs)", "info")
            print("=" * 80)

            # Get pending URLs from queue
            conn = sqlite3.connect(orchestrator.url_queue.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT url, priority, depth, domain, added_timestamp
                FROM url_queue
                WHERE status = 'pending'
                ORDER BY priority DESC, added_timestamp ASC
                LIMIT ?
            ''', (args.limit,))

            rows = cursor.fetchall()
            conn.close()

            if not rows:
                print("\n📭 Queue is empty")
                return 0

            print(f"\n{'URL':<50} {'Pri':<5} {'Depth':<7} {'Domain':<25}")
            print("-" * 87)

            for url, priority, depth, domain, timestamp in rows:
                url_display = url[:47] + "..." if len(url) > 50 else url
                domain_display = domain[:22] + "..." if len(domain) > 25 else domain
                print(f"{url_display:<50} {priority:<5} {depth:<7} {domain_display:<25}")

            print(f"\n{len(rows)} pending URLs shown")
            return 0

        except Exception as e:
            self.print_status(f"Error showing queue: {e}", "error")
            return 1

    def cmd_crawl_clear(self, args) -> int:
        """Clear completed URLs from queue"""
        try:
            from crawl_orchestrator import CrawlOrchestrator

            orchestrator = CrawlOrchestrator(data_dir=self.data_dir)

            if args.all:
                # Clear entire queue
                confirm = input("⚠️  Clear ENTIRE queue? This cannot be undone. Type 'yes' to confirm: ")
                if confirm.lower() != 'yes':
                    self.print_status("Cancelled", "warning")
                    return 0

                cleared = orchestrator.url_queue.clear_all()
                self.print_status(f"Cleared entire queue ({cleared} URLs)", "success")
            else:
                # Clear completed/failed older than threshold
                cleared = orchestrator.clear_completed(older_than_hours=args.older_than)
                self.print_status(f"Cleared {cleared} completed/failed URLs older than {args.older_than}h", "success")

            return 0

        except Exception as e:
            self.print_status(f"Error clearing queue: {e}", "error")
            return 1

    def cmd_robots_check(self, args) -> int:
        """Check robots.txt status for a URL"""
        try:
            from crawl_orchestrator import CrawlOrchestrator

            orchestrator = CrawlOrchestrator(data_dir=self.data_dir)

            self.print_status(f"Checking robots.txt for: {args.url}", "info")
            print("=" * 60)

            # Get comprehensive info
            info = orchestrator.get_url_info(args.url)

            print(f"\n🤖 ROBOTS.TXT STATUS:")
            print(f"   Allowed:        {'✅ Yes' if info['robots_allowed'] else '❌ No'}")
            print(f"   Crawl delay:    {info['robots_crawl_delay']}s" if info['robots_crawl_delay'] else "   Crawl delay:    Not specified")

            print(f"\n📊 QUEUE STATUS:")
            if info['in_queue']:
                queue_info = info['queue_info']
                print(f"   In queue:       ✅ Yes")
                print(f"   Status:         {queue_info['status']}")
                print(f"   Priority:       {queue_info['priority']}")
                print(f"   Depth:          {queue_info['depth']}")
                print(f"   Error count:    {queue_info['error_count']}")
            else:
                print(f"   In queue:       ❌ No")

            print(f"\n⏱️  RATE LIMIT:")
            rate_info = info['rate_limit_info']
            if rate_info['tracked']:
                print(f"   Tracked:        ✅ Yes")
                print(f"   Crawl delay:    {rate_info['crawl_delay']:.1f}s")
                print(f"   Total requests: {rate_info['total_requests']}")
                can_crawl_msg = '✅ Yes' if rate_info['can_crawl_now'] else f"❌ No (wait {rate_info['wait_time_needed']:.1f}s)"
                print(f"   Can crawl now:  {can_crawl_msg}")
            else:
                print(f"   Tracked:        ❌ No (first request)")

            return 0

        except Exception as e:
            self.print_status(f"Error checking robots.txt: {e}", "error")
            return 1

    def cmd_crawl_health(self, args) -> int:
        """Run comprehensive crawl health check"""
        try:
            from crawl_orchestrator import CrawlOrchestrator

            orchestrator = CrawlOrchestrator(data_dir=self.data_dir)

            self.print_status("Running crawl infrastructure health check...", "info")
            print("=" * 60)

            health = orchestrator.health_check()

            # Overall status
            if health['status'] == 'healthy':
                print("\n✅ STATUS: HEALTHY")
            else:
                print("\n⚠️  STATUS: ISSUES DETECTED")

            # Issues
            if health['issues']:
                print("\n⚠️  ISSUES:")
                for issue in health['issues']:
                    print(f"   • {issue}")
            else:
                print("\n✅ No issues detected")

            # Key metrics
            stats = health['stats']
            print("\n📊 KEY METRICS:")
            print(f"   Pending URLs:       {stats['queue']['pending']}")
            print(f"   In-progress URLs:   {stats['queue']['in_progress']}")
            print(f"   Success rate:       {stats['queue']['completed']}/{stats['queue']['completed'] + stats['queue']['failed']} ({100 * stats['queue']['completed'] / (stats['queue']['completed'] + stats['queue']['failed']) if (stats['queue']['completed'] + stats['queue']['failed']) > 0 else 0:.1f}%)")
            print(f"   Robots.txt blocks:  {stats['queue']['blocked_robots']}")
            print(f"   Cache hit rate:     {stats['robots_cache']['cache_hit_rate']:.1f}%")

            return 0 if health['status'] == 'healthy' else 1

        except Exception as e:
            self.print_status(f"Error running health check: {e}", "error")
            return 1

    # ========================================================================
    # SATURATION LEARNING COMMANDS (Associative Emergence)
    # ========================================================================

    def cmd_saturation(self, args) -> int:
        """Route saturation subcommands"""
        if not args.saturation_action:
            self.print_status("No saturation action specified. Use: start, status, event-horizon, or chain", "error")
            return 1

        action_map = {
            'start': self.cmd_saturation_start,
            'status': self.cmd_saturation_status,
            'event-horizon': self.cmd_saturation_event_horizon,
            'chain': self.cmd_saturation_chain,
        }

        handler = action_map.get(args.saturation_action)
        if handler:
            return handler(args)
        else:
            self.print_status(f"Unknown saturation action: {args.saturation_action}", "error")
            return 1

    def cmd_saturation_start(self, args) -> int:
        """Start a saturation learning session"""
        try:
            from enhanced_autonomous_learner import start_saturation_learning

            # Parse keywords
            keywords_list = [k.strip() for k in args.keywords.split(',')]

            self.print_status("=" * 80)
            self.print_status("🌀 ASSOCIATIVE EMERGENCE: SATURATION LEARNING SESSION")
            self.print_status("=" * 80)
            print(f"\n📍 Semantic Zone: {args.zone_name}")
            print(f"🌱 Seed URL: {args.seed_url}")
            print(f"🎯 Zone Keywords: {', '.join(keywords_list)}")
            print(f"📏 Allowed Distance: {args.allowed_distance}")
            print(f"🎚️  Saturation Threshold: {args.saturation_threshold}")
            print(f"📊 Max URLs in Zone: {args.max_urls}")
            print()

            self.print_status(f"Beginning deep saturation in '{args.zone_name}' zone...", "info")

            # Run saturation session
            result = start_saturation_learning(
                seed_url=args.seed_url,
                zone_name=args.zone_name,
                zone_keywords=keywords_list,
                allowed_distance=args.allowed_distance,
                saturation_threshold=args.saturation_threshold,
                max_urls=args.max_urls,
                data_dir=self.data_dir
            )

            # Display results
            print("\n" + "=" * 80)
            print("🌀 SATURATION SESSION COMPLETE")
            print("=" * 80)

            print(f"\n✅ Session ID: {result['session_id']}")
            print(f"✅ Zone: {result['zone']}")
            print(f"⏱️  Duration: {result['elapsed_time_minutes']:.2f} minutes")

            print(f"\n📊 Saturation Metrics:")
            print(f"   URLs Processed:    {result['stats']['urls_processed']}")
            print(f"   Static Nouns:      {result['stats']['static_noun_count']}")
            print(f"   Process Verbs:     {result['stats']['process_verb_count']}")
            print(f"   Phase Score:       {result['stats']['phase_transition_score']:.3f}")
            print(f"   Event Horizon:     {result['stats']['event_horizon_concepts']} concepts")

            if result.get('next_phase_query'):
                print(f"\n✨ PHASE TRANSITION DETECTED!")
                print(f"   Next Phase Query: '{result['next_phase_query']}'")
                print(f"\n   💡 Use this query to start the next zone:")
                next_url = f"https://en.wikipedia.org/wiki/{result['next_phase_query'].replace(' ', '_')}"
                print(f"   python3 cli.py saturation start \\")
                print(f"     --seed-url \"{next_url}\" \\")
                print(f"     --zone-name \"{args.zone_name}_Phase2\" \\")
                print(f"     --keywords \"{result['next_phase_query']},process,action\"")
                self.print_status("Phase transition successful - ready for next zone", "success")
            else:
                print(f"\n⚠️  Phase transition threshold not reached")
                print(f"   Score: {result['stats']['phase_transition_score']:.3f} / {args.saturation_threshold:.3f}")
                print(f"\n   💡 To continue learning in this zone:")
                print(f"   - Increase --max-urls (current: {args.max_urls})")
                print(f"   - Or lower --saturation-threshold (current: {args.saturation_threshold})")

            # Show top keywords
            print(f"\n📚 Top Keywords Learned:")
            top_keywords = sorted(result['keyword_frequencies'].items(),
                                key=lambda x: x[1], reverse=True)[:10]
            for keyword, count in top_keywords:
                print(f"   {keyword:30s} : {count:4d}")

            # Show event horizon sample
            if result.get('event_horizon_sample'):
                print(f"\n🔭 Event Horizon Sample (Forbidden Concepts):")
                for event in result['event_horizon_sample'][:5]:
                    print(f"   - {event['text'][:60]:60s} (distance: {event['distance']:.2f})")

            print(f"\n💾 Session saved: {result.get('session_file', 'N/A')}")

            # Run memory consolidation after phase transition
            if result.get('next_phase_query'):
                print(f"\n💤 Phase transition achieved — running memory consolidation...")
                try:
                    from memory_evolution_engine import run_memory_evolution
                    evo_result = run_memory_evolution(data_dir=self.data_dir)
                    print(f"   Reversed: {evo_result.get('reversed', 0)} | Migrated: {evo_result.get('migrated', 0)}")
                except Exception as e:
                    print(f"   ⚠️  Consolidation skipped: {e}")

            print()

            return 0

        except ImportError as e:
            self.print_status(f"Saturation learning not available: {e}", "error")
            self.print_status("Ensure enhanced_autonomous_learner.py has saturation methods", "error")
            return 1
        except Exception as e:
            self.print_status(f"Saturation session failed: {e}", "error")
            import traceback
            print("\n" + "="*80)
            print("FULL ERROR TRACEBACK:")
            print("="*80)
            traceback.print_exc()
            print("="*80)
            return 1

    def cmd_saturation_status(self, args) -> int:
        """Show recent saturation sessions"""
        try:
            import json
            from pathlib import Path

            sessions_dir = Path(self.data_dir) / "autonomous_sessions"
            if not sessions_dir.exists():
                self.print_status("No saturation sessions found", "warning")
                return 0

            # Find saturation session files
            sessions = sorted(sessions_dir.glob("saturation_*.json"),
                            key=lambda p: p.stat().st_mtime, reverse=True)

            if not sessions:
                self.print_status("No saturation sessions found", "warning")
                return 0

            print("\n" + "=" * 80)
            print(f"📋 RECENT SATURATION SESSIONS ({len(sessions)} total)")
            print("=" * 80)

            for session_file in sessions[:args.limit]:
                with open(session_file) as f:
                    data = json.load(f)

                print(f"\n🌊 {data['zone']}")
                print(f"   Session ID:     {data['session_id']}")
                print(f"   Completed:      {data['completed_at']}")
                print(f"   Duration:       {data['elapsed_time_minutes']:.2f} minutes")
                print(f"   URLs Processed: {data['stats']['urls_processed']}")
                print(f"   Phase Score:    {data['stats']['phase_transition_score']:.3f}")
                print(f"   Next Phase:     {data.get('next_phase_query', 'None')}")

            return 0

        except Exception as e:
            self.print_status(f"Error reading saturation sessions: {e}", "error")
            return 1

    def cmd_saturation_event_horizon(self, args) -> int:
        """Show concepts on the event horizon"""
        try:
            import sqlite3
            from pathlib import Path

            db_path = Path(self.data_dir) / "future_learning_queue.db"
            if not db_path.exists():
                self.print_status("No event horizon data found", "warning")
                return 0

            conn = sqlite3.connect(str(db_path))
            if args.zone:
                rows = conn.execute(
                    "SELECT text, distance, zone, timestamp FROM concepts "
                    "WHERE zone = ? ORDER BY timestamp DESC LIMIT ?",
                    (args.zone, args.limit)).fetchall()
                print(f"\n🔭 EVENT HORIZON (Zone: {args.zone})")
            else:
                rows = conn.execute(
                    "SELECT text, distance, zone, timestamp FROM concepts "
                    "ORDER BY timestamp DESC LIMIT ?",
                    (args.limit,)).fetchall()
                print(f"\n🔭 EVENT HORIZON (All Zones)")
            conn.close()

            if not rows:
                self.print_status("Event horizon is empty", "info")
                return 0

            print("=" * 80)
            print(f"\nTotal Concepts: {len(rows)}\n")

            for i, (text, distance, zone, timestamp) in enumerate(rows, 1):
                print(f"{i:3d}. {text[:70]}")
                print(f"      Distance: {distance:.2f} | Zone: {zone} | Seen: {timestamp[:10]}")
                print()

            print("\n💡 These concepts were seen but forbidden during saturation.")
            print("   They can be used as seeds for future learning zones.")

            return 0

        except Exception as e:
            self.print_status(f"Error reading event horizon: {e}", "error")
            return 1

    def cmd_saturation_chain(self, args) -> int:
        """Run multi-zone learning chain"""
        try:
            from enhanced_autonomous_learner import start_saturation_learning

            keywords_list = [k.strip() for k in args.keywords.split(',')]

            print("\n" + "=" * 80)
            print("🔗 MULTI-ZONE LEARNING CHAIN")
            print("=" * 80)
            print(f"\n🌱 Starting from: {args.seed_url}")
            print(f"🎯 Initial keywords: {', '.join(keywords_list)}")
            print(f"🔄 Max zones: {args.max_zones}")
            print()

            current_url = args.seed_url
            zone_keywords = keywords_list
            zone_num = 1

            while zone_num <= args.max_zones:
                print(f"\n{'=' * 80}")
                print(f"🌊 ZONE {zone_num}/{args.max_zones}")
                print(f"{'=' * 80}")

                result = start_saturation_learning(
                    seed_url=current_url,
                    zone_name=f"Chain_Zone_{zone_num}",
                    zone_keywords=zone_keywords,
                    allowed_distance=0.5,
                    saturation_threshold=0.55,
                    max_urls=args.max_urls_per_zone,
                    data_dir=self.data_dir
                )

                print(f"\n✅ Zone {zone_num} Complete:")
                print(f"   URLs: {result['stats']['urls_processed']}")
                print(f"   Phase Score: {result['stats']['phase_transition_score']:.3f}")
                print(f"   Next Query: {result.get('next_phase_query', 'None')}")

                # Check if transition detected
                if result.get('next_phase_query') is None:
                    print(f"\n⏸️  Learning chain complete: No further emergence detected")
                    break

                # Prepare next zone
                next_topic = result['next_phase_query'].replace(' ', '_')
                current_url = f"https://en.wikipedia.org/wiki/{next_topic}"

                # Extract dominant process verbs for next zone keywords
                verbs = [k for k, v in result['keyword_frequencies'].items()
                        if any(verb in k.lower() for verb in ['refine', 'process', 'make', 'create', 'extract', 'produce'])]
                zone_keywords = (verbs[:6] if verbs else [result['next_phase_query']]) + zone_keywords[:2]

                zone_num += 1

            print(f"\n" + "=" * 80)
            print(f"✅ LEARNING CHAIN COMPLETE: {zone_num - 1} zones explored")
            print("=" * 80)

            return 0

        except ImportError as e:
            self.print_status(f"Saturation learning not available: {e}", "error")
            return 1
        except Exception as e:
            self.print_status(f"Learning chain failed: {e}", "error")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return 1

    # ========================================================================
    # LEARNING COMMANDS - Sofia's Curiosity-Driven Learning
    # ========================================================================
    # STEP_1_TOPICS removed March 27, 2026 — was a hardcoded curriculum.
    # Learning is now driven by Sofia's curiosity state and seed coordinates.
    # See docs/SOPHIA_TRUTH_FRAMEWORK.md Correction 5.

    def cmd_curriculum(self, args) -> int:
        """Route curriculum/learning subcommands"""
        if not args.curriculum_action:
            self.print_status("No action specified. Use: status, learn, seeds, topic", "error")
            print("\nAvailable actions:")
            print("  status  - Show memory counts and learning state")
            print("  learn   - Start a learning session (autonomous or seeded)")
            print("  seeds   - Activate seed coordinates for first learning session")
            print("  topic   - Learn a specific topic by URL")
            return 1

        action_map = {
            'status': self.cmd_curriculum_status,
            'learn': self.cmd_curriculum_learn,
            'seeds': self.cmd_curriculum_seeds,
            'topic': self.cmd_curriculum_topic,
            # Legacy aliases
            'complete-step': self.cmd_curriculum_legacy,
        }

        handler = action_map.get(args.curriculum_action)
        if handler:
            return handler(args)
        else:
            self.print_status(f"Unknown action: {args.curriculum_action}", "error")
            return 1

    def cmd_curriculum_seeds(self, args) -> int:
        """Activate seed coordinates from manifest for first learning session"""
        try:
            from enhanced_autonomous_learner import activate_seed_coordinates
            result = activate_seed_coordinates(
                seed_ids=None,  # Activate all available
                data_dir=self.data_dir,
                target_urls=getattr(args, 'urls', 100)
            )
            if result is None:
                print("\nNo unactivated seeds available.")
                print("Sofia's curiosity state drives subsequent learning.")
                print("Use 'curriculum learn' for curiosity-driven sessions.")
            return 0
        except Exception as e:
            self.print_status(f"Seed activation failed: {e}", "error")
            return 1

    def cmd_curriculum_legacy(self, args) -> int:
        """Handle legacy complete-step commands"""
        print("\nThe 4-Step curriculum has been removed.")
        print("Sofia's learning is now driven by curiosity, not predetermined steps.")
        print("\nUse instead:")
        print("  curriculum seeds  - Activate seed coordinates for first session")
        print("  curriculum learn  - Start curiosity-driven learning")
        print("  curriculum topic  - Learn a specific topic by URL")
        print("\nSee docs/SOPHIA_TRUTH_FRAMEWORK.md for details.")
        return 1

    def _get_memory_counts(self) -> dict:
        """Get current memory counts for consciousness metrics"""
        from pathlib import Path
        import json

        counts = {
            'logic': 0,
            'symbolic': 0,
            'bridge': 0,
            'ratio': 0
        }

        try:
            logic_file = Path(self.data_dir) / "logic_memory.json"
            if logic_file.exists():
                with open(logic_file, 'r') as f:
                    counts['logic'] = len(json.load(f))

            symbolic_file = Path(self.data_dir) / "symbolic_memory.json"
            if symbolic_file.exists():
                with open(symbolic_file, 'r') as f:
                    counts['symbolic'] = len(json.load(f))

            bridge_file = Path(self.data_dir) / "bridge_memory.json"
            if bridge_file.exists():
                with open(bridge_file, 'r') as f:
                    counts['bridge'] = len(json.load(f))

            if counts['symbolic'] > 0:
                counts['ratio'] = counts['logic'] / counts['symbolic']
        except:
            pass

        return counts

    def cmd_curriculum_status(self, args) -> int:
        """Show learning state: memory counts, curiosity drives, seed status"""
        import json
        from pathlib import Path

        # Check for specific task status
        if hasattr(args, 'task_id') and args.task_id:
            try:
                from background_tasks import get_task
                task = get_task(args.task_id, self.data_dir)
                if not task:
                    self.print_status(f"Task not found: {args.task_id}", "error")
                    return 1
                print(f"\nBACKGROUND TASK: {task['task_id']}")
                print(f"Type: {task['type']} | Status: {task['status']}")
                print(f"Started: {task['started_at']}")
                if task.get('completed_at'):
                    print(f"Completed: {task['completed_at']}")
                if task.get('progress'):
                    for k, v in task['progress'].items():
                        print(f"  {k}: {v}")
                return 0
            except ImportError:
                self.print_status("Background tasks module not available", "error")
                return 1

        print("\n" + "=" * 70)
        print("SOFIA'S LEARNING STATE")
        print("=" * 70)

        # Memory counts
        mem = self._get_memory_counts()
        print(f"\nMemory Distribution:")
        print(f"   Logic:    {mem['logic']:,} items")
        print(f"   Symbolic: {mem['symbolic']} items")
        print(f"   Bridge:   {mem['bridge']} items (intake)")

        # Seed coordinate status
        manifest_path = Path(self.data_dir) / "seed_coordinates_manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            seeds = manifest.get('available_seeds', [])
            activated = sum(1 for s in seeds if s['activated'])
            available = sum(1 for s in seeds if not s['activated'])
            print(f"\nSeed Coordinates:")
            print(f"   Available: {available} | Activated: {activated}")
            if available > 0:
                print(f"   Run 'curriculum seeds' to activate for first session")

        # Knowledge state
        if mem['logic'] == 0 and mem['symbolic'] == 0 and mem['bridge'] == 0:
            print(f"\n   Sofia's knowledge graph is EMPTY.")
            print(f"   Activate seed coordinates to begin the learning spiral.")
        else:
            print(f"\n   Knowledge exists. Curiosity-driven learning available.")
            print(f"   Run 'curriculum learn' for autonomous session.")

        # Background tasks
        try:
            from background_tasks import list_tasks
            tasks = list_tasks(limit=5, data_dir=self.data_dir)
            running = [t for t in tasks if t['status'] == 'running']
            if running:
                print(f"\nRunning Tasks:")
                for t in running:
                    print(f"   {t['task_id']} - {t['status']} (started: {t['started_at']})")
        except ImportError:
            pass

        print()
        return 0

    def cmd_curriculum_learn(self, args) -> int:
        """Start a learning session (autonomous or seeded)"""
        try:
            from enhanced_autonomous_learner import start_massive_web_learning

            seed_urls = None
            if args.seeds:
                seed_urls = [s.strip() for s in args.seeds.split(',')]

            if args.background:
                # Run in background
                try:
                    from background_tasks import get_task_manager, start_background_task

                    task_manager = get_task_manager(self.data_dir)
                    metadata = {
                        'seeds': seed_urls,
                        'target_urls': args.urls,
                        'focus': args.focus,
                        'mode': 'autonomous' if seed_urls is None else 'seeded'
                    }

                    # We need to use a different approach for multiprocessing
                    # because the learning function can't be pickled directly
                    task_id = task_manager.create_task('curriculum_learn', metadata)
                    task_manager.update_task(task_id, status='running')

                    import multiprocessing

                    def background_learn(task_id, seeds, urls, focus, data_dir):
                        """Background learning process"""
                        try:
                            from enhanced_autonomous_learner import start_massive_web_learning
                            from background_tasks import update_task

                            result = start_massive_web_learning(
                                seed_urls=seeds,
                                target_urls=urls,
                                focus=focus,
                                data_dir=data_dir
                            )

                            if hasattr(result, 'session_stats'):
                                update_task(task_id, 'completed', result=result.session_stats, data_dir=data_dir)
                            else:
                                update_task(task_id, 'completed', result={'status': 'done'}, data_dir=data_dir)
                        except Exception as e:
                            from background_tasks import update_task
                            update_task(task_id, 'failed', error=str(e), data_dir=data_dir)

                    p = multiprocessing.Process(
                        target=background_learn,
                        args=(task_id, seed_urls, args.urls, args.focus, self.data_dir),
                        daemon=False
                    )
                    p.start()

                    print(f"\n Learning started in background!")
                    print(f"   Task ID: {task_id}")
                    print(f"   Mode: {'Autonomous (Sofia decides)' if seed_urls is None else 'Seeded'}")
                    print(f"   Target URLs: {args.urls}")
                    print(f"   Focus: {args.focus}")
                    print(f"\n   Check progress: python3 cli.py curriculum status --task-id {task_id}")
                    return 0

                except ImportError as e:
                    self.print_status(f"Background tasks not available: {e}", "error")
                    self.print_status("Running in foreground instead...", "warning")
                    # Fall through to foreground execution

            # Foreground execution
            print(f"\n{'='*70}")
            print("CURRICULUM LEARNING SESSION")
            print(f"{'='*70}")
            print(f"Mode: {'AUTONOMOUS (Sofia decides what to learn)' if seed_urls is None else 'SEEDED'}")
            print(f"Target URLs: {args.urls}")
            print(f"Focus: {args.focus}")
            print(f"{'='*70}\n")

            self.print_status("Starting learning session...", "info")

            result = start_massive_web_learning(
                seed_urls=seed_urls,
                target_urls=args.urls,
                focus=args.focus,
                data_dir=self.data_dir
            )

            print(f"\n{'='*70}")
            print(" LEARNING SESSION COMPLETE")
            print(f"{'='*70}")

            if hasattr(result, 'session_stats'):
                stats = result.session_stats
                print(f"   URLs processed:  {stats.get('urls_processed', 'N/A')}")
                print(f"   Facts extracted: {stats.get('facts_extracted', 'N/A')}")
                print(f"   Facts validated: {stats.get('facts_validated', 'N/A')}")

            return 0

        except ImportError as e:
            self.print_status(f"Learning system not available: {e}", "error")
            return 1
        except Exception as e:
            self.print_status(f"Learning session failed: {e}", "error")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return 1

    # cmd_curriculum_complete_step removed — 4-Step curriculum eliminated.
    # Legacy handler in cmd_curriculum_legacy() above.

    # _complete_step_1, _create_step1_completion_memory, _display_step1_ceremony
    # ALL REMOVED March 27, 2026.
    # The 4-Step curriculum was a hardcoded learning path. Sofia's learning
    # is now driven by her cosine-based curiosity, not predetermined steps.
    # Fabricated "completion memories" with preset text were false simulation.
    # See docs/SOPHIA_TRUTH_FRAMEWORK.md Corrections 5 and 7.

    def cmd_curriculum_topic(self, args) -> int:
        """Learn a specific topic on demand"""
        topic = args.topic

        # Check if it's a URL or topic name
        if topic.startswith('http'):
            seed_url = topic
            topic_name = topic.split('/')[-1].replace('_', ' ')
        else:
            # Convert topic name to Wikipedia URL
            topic_name = topic
            wiki_topic = topic.replace(' ', '_')
            seed_url = f"https://en.wikipedia.org/wiki/{wiki_topic}"

        if args.background:
            try:
                from background_tasks import get_task_manager
                import multiprocessing

                task_manager = get_task_manager(self.data_dir)
                task_id = task_manager.create_task('topic_learn', {'topic': topic_name, 'url': seed_url})
                task_manager.update_task(task_id, status='running')

                def bg_topic_learn(task_id, url, urls, data_dir):
                    try:
                        from enhanced_autonomous_learner import start_massive_web_learning
                        from background_tasks import update_task
                        result = start_massive_web_learning([url], urls, 'general', data_dir)
                        if hasattr(result, 'session_stats'):
                            update_task(task_id, 'completed', result=result.session_stats, data_dir=data_dir)
                        else:
                            update_task(task_id, 'completed', data_dir=data_dir)
                    except Exception as e:
                        from background_tasks import update_task
                        update_task(task_id, 'failed', error=str(e), data_dir=data_dir)

                p = multiprocessing.Process(
                    target=bg_topic_learn,
                    args=(task_id, seed_url, args.urls, self.data_dir),
                    daemon=False
                )
                p.start()

                print(f"\n Learning topic in background!")
                print(f"   Topic: {topic_name}")
                print(f"   URL: {seed_url}")
                print(f"   Task ID: {task_id}")
                print(f"\n   Check progress: python3 cli.py curriculum status --task-id {task_id}")
                return 0

            except ImportError as e:
                self.print_status(f"Background tasks not available: {e}", "warning")
                self.print_status("Running in foreground...", "info")

        # Foreground learning
        try:
            from enhanced_autonomous_learner import start_massive_web_learning

            print(f"\n{'='*70}")
            print(f" LEARNING TOPIC: {topic_name.upper()}")
            print(f"{'='*70}")
            print(f"   Source: {seed_url}")
            print(f"   Target URLs: {args.urls}")
            print(f"{'='*70}\n")

            result = start_massive_web_learning(
                seed_urls=[seed_url],
                target_urls=args.urls,
                focus='general',
                data_dir=self.data_dir
            )

            print(f"\n Topic learning complete!")
            if hasattr(result, 'session_stats'):
                stats = result.session_stats
                print(f"   URLs processed: {stats.get('urls_processed', 'N/A')}")

            return 0

        except ImportError as e:
            self.print_status(f"Learning system not available: {e}", "error")
            return 1
        except Exception as e:
            self.print_status(f"Topic learning failed: {e}", "error")
            return 1

    def run(self, args=None) -> int:
        """Run the CLI with given arguments"""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        # Set global options
        self.data_dir = parsed_args.data_dir
        self.verbose = parsed_args.verbose
        
        # Ensure data directory exists
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        if not parsed_args.command:
            parser.print_help()
            return 0
        
        # Route to appropriate command handler
        command_map = {
            'start': self.cmd_start,
            'status': self.cmd_status,
            'stop': self.cmd_stop,
            'migrate': self.cmd_migrate,
            'integrate': self.cmd_integrate,
            'analyze': self.cmd_analyze,
            'health': self.cmd_health,
            'backup': self.cmd_backup,
            'cleanup': self.cmd_cleanup,
            'interact': self.cmd_interact,
            'learn': self.cmd_learn,
            'chat': self.cmd_chat,
            'config': self.cmd_config,
            'memory': self.cmd_memory,
            'bridge-review': self.cmd_bridge_review,
            'sleep-cycle': self.cmd_sleep_cycle,
            'test-shutdown': self.cmd_test_shutdown,
            'immune-status': self.cmd_immune_status,
            'immune-review': self.cmd_immune_review,
            'immune-trust': self.cmd_immune_trust,
            'immune-override': self.cmd_immune_override,
            'immune-export': self.cmd_immune_export,
            'crawl-status': self.cmd_crawl_status,
            'crawl-add': self.cmd_crawl_add,
            'crawl-queue': self.cmd_crawl_queue,
            'crawl-clear': self.cmd_crawl_clear,
            'robots-check': self.cmd_robots_check,
            'crawl-health': self.cmd_crawl_health,
            'saturation': self.cmd_saturation,  # Associative Emergence
            'curriculum': self.cmd_curriculum,  # Sofia's Learning System
        }
        
        handler = command_map.get(parsed_args.command)
        if handler:
            return handler(parsed_args)
        else:
            self.print_status(f"Unknown command: {parsed_args.command}", "error")
            return 1

def main():
    """Main entry point"""
    cli = DualBrainCLI()
    return cli.run()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)