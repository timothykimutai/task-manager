"""Data storage and persistence layer."""

import json
import csv
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, TextIO
from datetime import datetime
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

    def export_to_json(self, file_path: Path) -> None:
        """
        Export tasks to a JSON file.

        Args:
            file_path: Path to export file
        """
        try:
            tasks = self.load_tasks()
            data = [task.to_dict() for task in tasks]
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Exported {len(tasks)} tasks to {file_path}")
        except (IOError, OSError) as e:
            error_msg = f"Failed to export tasks: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e

    def import_from_json(self, file_path: Path) -> List[Task]:
        """
        Import tasks from a JSON file.

        Args:
            file_path: Path to import file

        Returns:
            List of imported tasks
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            tasks = [Task.from_dict(task_data) for task_data in data]
            logger.info(f"Imported {len(tasks)} tasks from {file_path}")
            return tasks
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in import file: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e
        except (IOError, OSError) as e:
            error_msg = f"Failed to import tasks: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e

    def export_to_csv(self, file_path: Path) -> None:
        """
        Export tasks to a CSV file.

        Args:
            file_path: Path to export file
        """
        try:
            tasks = self.load_tasks()
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "id", "title", "description", "status", "priority",
                    "category", "tags", "due_date", "reminder",
                    "created_at", "completed_at"
                ])
                writer.writeheader()
                for task in tasks:
                    data = task.to_dict()
                    data["tags"] = ",".join(data["tags"])
                    writer.writerow(data)
            logger.info(f"Exported {len(tasks)} tasks to {file_path}")
        except (IOError, OSError) as e:
            error_msg = f"Failed to export tasks: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e

    def import_from_csv(self, file_path: Path) -> List[Task]:
        """
        Import tasks from a CSV file.

        Args:
            file_path: Path to import file

        Returns:
            List of imported tasks
        """
        try:
            tasks = []
            with open(file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert tags string back to list
                    row["tags"] = row["tags"].split(",") if row["tags"] else []
                    # Convert datetime strings
                    for field in ["due_date", "reminder", "created_at", "completed_at"]:
                        if row[field]:
                            row[field] = datetime.fromisoformat(row[field])
                        else:
                            row[field] = None
                    tasks.append(Task.from_dict(row))
            logger.info(f"Imported {len(tasks)} tasks from {file_path}")
            return tasks
        except (IOError, OSError) as e:
            error_msg = f"Failed to import tasks: {e}"
            logger.error(error_msg)
            raise TaskStorageError(error_msg) from e
