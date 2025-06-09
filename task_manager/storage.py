"""Data storage and persistence layer."""

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from .models import Task, TaskStatus, Priority


logger = logging.getLogger(__name__)


class TaskStorageError(Exception):
    """Custom exception for storage operations."""

    pass


class TaskStorage:
    """Handles task data persistence."""

    def __init__(self, data_file: Path):
        """Initialize storage with data file path."""
        self.data_file = Path(data_file).expanduser()
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"TaskStorage initialized with file: {self.data_file}")
        except (IOError, OSError) as e:
            error_msg = f"Failed to create directory: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to file."""
        try:
            data = [task.to_dict() for task in tasks]
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(tasks)} tasks to {self.data_file}")
        except (IOError, OSError) as e:
            error_msg = f"Failed to save tasks: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e

    def load_tasks(self) -> List[Task]:
        """Load tasks from file."""
        if not self.data_file.exists():
            logger.info("Data file doesn't exist, returning empty task list")
            return []

        try:
            with open(self.data_file, "r") as f:
                content = f.read().strip()
                if not content:  # Handle empty file
                    return []
                data = json.loads(content)

            tasks = [Task.from_dict(task_data) for task_data in data]
            logger.info(f"Loaded {len(tasks)} tasks from {self.data_file}")
            return tasks

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in data file: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e
        except (IOError, OSError) as e:
            error_msg = f"Failed to load tasks: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e

    def backup_data(self) -> Optional[Path]:
        """Create a backup of the current data file."""
        if not self.data_file.exists():
            return None

        backup_file = self.data_file.with_suffix(".json.backup")
        try:
            backup_file.write_text(self.data_file.read_text())
            logger.info(f"Created backup: {backup_file}")
            return backup_file
        except (IOError, OSError) as e:
            logger.error(f"Failed to create backup: {e}")
            return None
