# shutdown_manager.py - Graceful Shutdown System
"""
Shutdown Manager - Graceful System Exit Handler

Handles clean shutdown for the Sophia AI system:
- Signal handling (SIGINT, SIGTERM)
- Cleanup function registry
- Memory flushing
- Database connection closing
- Final logging

Prevents data corruption during interrupts or crashes.

Created: 2025-12-30
Author: Claude Code
"""

import signal
import sys
import atexit
import logging
from datetime import datetime
from typing import Callable, List, Dict, Any, Optional
from pathlib import Path
import asyncio
import json

logger = logging.getLogger(__name__)


class ShutdownManager:
    """
    Manages graceful system shutdown with cleanup registry.

    Features:
    - Signal handling for SIGINT (Ctrl+C) and SIGTERM
    - Cleanup function registry for modules to subscribe to
    - Ordered cleanup execution (LIFO - Last In First Out)
    - Final status logging
    - Async cleanup support
    """

    def __init__(self, data_dir: str = "data", verbose: bool = False):
        self.data_dir = Path(data_dir)
        self.verbose = verbose
        self.cleanup_functions: List[Dict[str, Any]] = []
        self.shutdown_in_progress = False
        self.original_sigint_handler = None
        self.original_sigterm_handler = None

        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup shutdown-specific logging."""
        log_path = self.data_dir / "shutdown_log.json"

        # Create initial log if it doesn't exist
        if not log_path.exists():
            with open(log_path, 'w') as f:
                json.dump({'shutdowns': []}, f, indent=2)

    def register_cleanup(self, cleanup_func: Callable, name: str,
                        priority: int = 0, is_async: bool = False):
        """
        Register a cleanup function to be called during shutdown.

        Args:
            cleanup_func: Function to call during cleanup
            name: Human-readable name for this cleanup task
            priority: Higher priority runs first (default: 0)
            is_async: Whether the function is async (default: False)
        """
        self.cleanup_functions.append({
            'func': cleanup_func,
            'name': name,
            'priority': priority,
            'is_async': is_async
        })

        # Sort by priority (descending)
        self.cleanup_functions.sort(key=lambda x: x['priority'], reverse=True)

        if self.verbose:
            print(f"  [Shutdown] Registered cleanup: {name} (priority: {priority})")

    def install_handlers(self):
        """Install signal handlers for graceful shutdown."""
        import threading
        
        # Check if we are in the main thread
        if threading.current_thread() is not threading.main_thread():
            if self.verbose:
                print("  [Shutdown] Signal handlers can only be installed in the main thread. Skipping signal registration, but atexit will still work.")
            # Still register with atexit as it's thread-safe
            atexit.register(self._atexit_handler)
            return

        try:
            # Save original handlers
            self.original_sigint_handler = signal.getsignal(signal.SIGINT)
            self.original_sigterm_handler = signal.getsignal(signal.SIGTERM)

            # Install our handlers
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

            # Also register with atexit as a backup
            atexit.register(self._atexit_handler)

            if self.verbose:
                print("  [Shutdown] Signal handlers installed")
        except (ValueError, RuntimeError) as e:
            # Fallback for environments where signal handlers cannot be installed
            if self.verbose:
                print(f"  [Shutdown] Could not install signal handlers ({e}). Falling back to atexit.")
            atexit.register(self._atexit_handler)

    def _signal_handler(self, signum, frame):
        """Handle interrupt signals (SIGINT, SIGTERM)."""
        signal_name = "SIGINT" if signum == signal.SIGINT else "SIGTERM"

        print(f"\n\n⚠️  Received {signal_name} - Initiating graceful shutdown...")

        # Perform shutdown
        self.shutdown(reason=f"Signal {signal_name} received")

        # Exit
        sys.exit(0)

    def _atexit_handler(self):
        """Fallback handler called by atexit."""
        if not self.shutdown_in_progress:
            if self.verbose:
                print("\n  [Shutdown] atexit handler triggered")
            self.shutdown(reason="Normal program exit")

    def shutdown(self, reason: str = "Manual shutdown", exit_code: int = 0):
        """
        Execute graceful shutdown sequence.

        Args:
            reason: Human-readable reason for shutdown
            exit_code: Exit code to use (default: 0)
        """
        if self.shutdown_in_progress:
            # Already shutting down, don't recurse
            return

        self.shutdown_in_progress = True

        print("\n" + "="*70)
        print("GRACEFUL SHUTDOWN IN PROGRESS")
        print("="*70)
        print(f"Reason: {reason}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Track cleanup results
        cleanup_results = {
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat(),
            'successful_cleanups': [],
            'failed_cleanups': [],
            'total_cleanup_tasks': len(self.cleanup_functions)
        }

        # Execute cleanup functions in priority order
        print(f"🧹 Running {len(self.cleanup_functions)} cleanup tasks...\n")

        for cleanup_task in self.cleanup_functions:
            func = cleanup_task['func']
            name = cleanup_task['name']
            is_async = cleanup_task['is_async']

            print(f"  [Cleanup] {name}...", end=' ')

            try:
                if is_async:
                    # Run async function
                    asyncio.run(func())
                else:
                    # Run sync function
                    func()

                print("✅")
                cleanup_results['successful_cleanups'].append(name)

            except Exception as e:
                print(f"❌ Error: {e}")
                cleanup_results['failed_cleanups'].append({
                    'name': name,
                    'error': str(e)
                })
                logger.error(f"Cleanup task '{name}' failed: {e}")

        # Log final status
        self._log_shutdown(cleanup_results)

        # Print summary
        print("\n" + "="*70)
        print("SHUTDOWN SUMMARY")
        print("="*70)
        print(f"✅ Successful: {len(cleanup_results['successful_cleanups'])}")
        print(f"❌ Failed:     {len(cleanup_results['failed_cleanups'])}")

        if cleanup_results['failed_cleanups']:
            print("\nFailed tasks:")
            for failure in cleanup_results['failed_cleanups']:
                print(f"  • {failure['name']}: {failure['error']}")

        print(f"\n💾 Shutdown log saved to: {self.data_dir / 'shutdown_log.json'}")
        print("\n✅ Graceful shutdown complete")
        print("="*70 + "\n")

    def _log_shutdown(self, results: Dict[str, Any]):
        """Log shutdown event to file."""
        log_path = self.data_dir / "shutdown_log.json"

        try:
            # Load existing log
            if log_path.exists():
                with open(log_path, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'shutdowns': []}

            # Append new shutdown
            log_data['shutdowns'].append(results)

            # Keep only last 100 shutdowns
            if len(log_data['shutdowns']) > 100:
                log_data['shutdowns'] = log_data['shutdowns'][-100:]

            # Save
            with open(log_path, 'w') as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log shutdown: {e}")


# Global shutdown manager instance
_shutdown_manager: Optional[ShutdownManager] = None


def get_shutdown_manager(data_dir: str = "data", verbose: bool = False) -> ShutdownManager:
    """
    Get or create the global shutdown manager instance.

    Args:
        data_dir: Data directory path
        verbose: Enable verbose output

    Returns:
        ShutdownManager instance
    """
    global _shutdown_manager

    if _shutdown_manager is None:
        _shutdown_manager = ShutdownManager(data_dir=data_dir, verbose=verbose)

    return _shutdown_manager


def register_cleanup(cleanup_func: Callable, name: str,
                    priority: int = 0, is_async: bool = False):
    """
    Convenience function to register cleanup with global manager.

    Args:
        cleanup_func: Function to call during cleanup
        name: Human-readable name for this cleanup task
        priority: Higher priority runs first (default: 0)
        is_async: Whether the function is async (default: False)
    """
    manager = get_shutdown_manager()
    manager.register_cleanup(cleanup_func, name, priority, is_async)


def install_handlers():
    """Convenience function to install signal handlers on global manager."""
    manager = get_shutdown_manager()
    manager.install_handlers()


# Predefined cleanup functions for common subsystems
def create_memory_cleanup(unified_memory):
    """Create cleanup function for unified memory system."""
    def cleanup():
        """Save all memory to disk."""
        try:
            if hasattr(unified_memory, 'save_all'):
                unified_memory.save_all()
            if hasattr(unified_memory, 'save_all_memories'):
                unified_memory.save_all_memories()
        except Exception as e:
            logger.error(f"Memory save failed: {e}")
            raise

    return cleanup


def create_robots_cleanup(robots_manager):
    """Create cleanup function for robots.txt manager (async)."""
    async def cleanup():
        """Close async aiohttp session."""
        try:
            if hasattr(robots_manager, 'close'):
                await robots_manager.close()
        except Exception as e:
            logger.error(f"Robots manager close failed: {e}")
            raise

    return cleanup


def create_log_cleanup(message: str = "System shutdown: Graceful"):
    """Create cleanup function to write final log entry."""
    def cleanup():
        """Write final shutdown message to log."""
        try:
            logger.info(message)
        except Exception as e:
            # Don't raise - logging failure shouldn't block shutdown
            print(f"Warning: Final log write failed: {e}")

    return cleanup


if __name__ == "__main__":
    # Test the shutdown manager
    import time

    print("Testing ShutdownManager...")
    print("This will sleep for 10 seconds. Press Ctrl+C to test signal handling.\n")

    # Create manager
    manager = ShutdownManager(verbose=True)

    # Register some test cleanup functions
    def cleanup1():
        print("    Saving test data...")
        time.sleep(0.5)

    def cleanup2():
        print("    Closing test connections...")
        time.sleep(0.3)

    def cleanup3():
        print("    Writing final test log...")

    manager.register_cleanup(cleanup1, "Save test data", priority=10)
    manager.register_cleanup(cleanup2, "Close test connections", priority=5)
    manager.register_cleanup(cleanup3, "Write final log", priority=1)

    # Install handlers
    manager.install_handlers()

    print("Signal handlers installed. Sleeping for 10 seconds...")
    print("Press Ctrl+C to trigger graceful shutdown.\n")

    try:
        for i in range(10):
            print(f"  Working... {i+1}/10")
            time.sleep(1)

        print("\nCompleted normally.")
        manager.shutdown(reason="Test completed successfully")

    except KeyboardInterrupt:
        # Should be caught by signal handler, but just in case
        print("\nKeyboardInterrupt caught in main")
        manager.shutdown(reason="KeyboardInterrupt in main")
