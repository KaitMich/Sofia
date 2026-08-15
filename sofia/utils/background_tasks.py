# background_tasks.py - Background Task Management with Cognitive Sovereignty
# Tracks background learning tasks for Sofia's curriculum system

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
import threading
import multiprocessing


class BackgroundTaskManager:
    """Manages background learning tasks with sovereignty awareness"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.tasks_file = self.data_dir / "background_tasks.json"
        self._lock = threading.Lock()
        self._ensure_tasks_file()

    def _ensure_tasks_file(self):
        """Ensure the tasks file exists"""
        if not self.tasks_file.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self._save_tasks({"tasks": {}})

    def _load_tasks(self) -> Dict[str, Any]:
        """Load tasks from file"""
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"tasks": {}}

    def _save_tasks(self, data: Dict[str, Any]):
        """Save tasks to file atomically"""
        temp_file = self.tasks_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        temp_file.replace(self.tasks_file)

    def create_task(self, task_type: str, metadata: Dict[str, Any] = None) -> str:
        """Create a new background task and return its ID"""
        task_id = f"{task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

        task = {
            "type": task_type,
            "status": "pending",
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "progress": {},
            "metadata": metadata or {},
            "result": None,
            "error": None
        }

        with self._lock:
            data = self._load_tasks()
            data["tasks"][task_id] = task
            self._save_tasks(data)

        return task_id

    def update_task(self, task_id: str, status: str = None,
                   progress: Dict[str, Any] = None,
                   result: Dict[str, Any] = None,
                   error: str = None):
        """Update a task's status and progress"""
        with self._lock:
            data = self._load_tasks()

            if task_id not in data["tasks"]:
                raise ValueError(f"Task {task_id} not found")

            task = data["tasks"][task_id]

            if status:
                task["status"] = status
                if status in ("completed", "failed", "vetoed"):
                    task["completed_at"] = datetime.now().isoformat()

            if progress:
                task["progress"].update(progress)

            if result is not None:
                task["result"] = result

            if error is not None:
                task["error"] = error

            self._save_tasks(data)

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        data = self._load_tasks()
        task = data["tasks"].get(task_id)
        if task:
            task["task_id"] = task_id
        return task

    def list_tasks(self, status_filter: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """List tasks, optionally filtered by status"""
        data = self._load_tasks()
        tasks = []

        for task_id, task in data["tasks"].items():
            if status_filter and task["status"] != status_filter:
                continue
            task["task_id"] = task_id
            tasks.append(task)

        # Sort by started_at descending
        tasks.sort(key=lambda t: t.get("started_at", ""), reverse=True)
        return tasks[:limit]

    def cleanup_old_tasks(self, max_age_hours: int = 72):
        """Remove completed tasks older than max_age_hours"""
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        with self._lock:
            data = self._load_tasks()
            to_remove = []

            for task_id, task in data["tasks"].items():
                if task["status"] in ("completed", "failed", "vetoed"):
                    completed = task.get("completed_at")
                    if completed:
                        completed_dt = datetime.fromisoformat(completed)
                        if completed_dt < cutoff:
                            to_remove.append(task_id)

            for task_id in to_remove:
                del data["tasks"][task_id]

            if to_remove:
                self._save_tasks(data)

        return len(to_remove)


def run_learning_with_sovereignty(task_manager: BackgroundTaskManager,
                                  task_id: str,
                                  learning_func: Callable,
                                  data_dir: str,
                                  *args, **kwargs) -> Callable:
    """
    Wrapper that checks cognitive sovereignty during learning.
    Returns a function suitable for multiprocessing.Process target.
    """

    def wrapped_learning():
        """The actual learning function that runs in a subprocess"""
        try:
            # Update task status to running
            task_manager.update_task(task_id, status="running")

            # Check cognitive sovereignty before starting
            try:
                from sofia.core.cognitive_sovereignty import cognitive_sovereignty_check
                check = cognitive_sovereignty_check({
                    'action': 'background_learning',
                    'task_id': task_id,
                    'context': 'curriculum_learning'
                })

                if check.get('veto'):
                    task_manager.update_task(
                        task_id,
                        status='vetoed',
                        error="Cognitive sovereignty veto - Sofia declined this learning"
                    )
                    return
            except ImportError:
                # Cognitive sovereignty module not available, continue anyway
                pass

            # Run the actual learning
            result = learning_func(*args, **kwargs)

            # Extract session stats if available
            if hasattr(result, 'session_stats'):
                result_data = result.session_stats
            elif isinstance(result, dict):
                result_data = result
            else:
                result_data = {"status": "completed"}

            task_manager.update_task(
                task_id,
                status='completed',
                result=result_data
            )

        except Exception as e:
            task_manager.update_task(
                task_id,
                status='failed',
                error=str(e)
            )
            import traceback
            print(f"Background task {task_id} failed: {e}")
            traceback.print_exc()

    return wrapped_learning


def start_background_task(task_manager: BackgroundTaskManager,
                         task_type: str,
                         learning_func: Callable,
                         data_dir: str,
                         metadata: Dict[str, Any] = None,
                         *args, **kwargs) -> str:
    """
    Start a learning task in the background.
    Returns the task_id for monitoring.
    """
    # Create the task record
    task_id = task_manager.create_task(task_type, metadata)

    # Create the wrapped learning function
    wrapped = run_learning_with_sovereignty(
        task_manager, task_id, learning_func, data_dir, *args, **kwargs
    )

    # Start in a subprocess (daemon=False so it continues if parent exits)
    process = multiprocessing.Process(target=wrapped, daemon=False)
    process.start()

    return task_id


# Module-level convenience functions
_default_manager = None


def get_task_manager(data_dir: str = "data") -> BackgroundTaskManager:
    """Get or create the default task manager"""
    global _default_manager
    if _default_manager is None:
        _default_manager = BackgroundTaskManager(data_dir)
    return _default_manager


def create_task(task_type: str, metadata: Dict[str, Any] = None,
               data_dir: str = "data") -> str:
    """Convenience function to create a task"""
    return get_task_manager(data_dir).create_task(task_type, metadata)


def update_task(task_id: str, status: str = None,
               progress: Dict[str, Any] = None,
               result: Dict[str, Any] = None,
               error: str = None,
               data_dir: str = "data"):
    """Convenience function to update a task"""
    get_task_manager(data_dir).update_task(task_id, status, progress, result, error)


def get_task(task_id: str, data_dir: str = "data") -> Optional[Dict[str, Any]]:
    """Convenience function to get a task"""
    return get_task_manager(data_dir).get_task(task_id)


def list_tasks(status_filter: str = None, limit: int = 10,
              data_dir: str = "data") -> List[Dict[str, Any]]:
    """Convenience function to list tasks"""
    return get_task_manager(data_dir).list_tasks(status_filter, limit)
