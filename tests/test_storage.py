"""Tests for storage layer."""

import pytest
import json
from pathlib import Path
from task_manager.storage import TaskStorage, TaskStorageError
from task_manager.models import Task, Priority


class TestTaskStorage:
    """Test cases for TaskStorage."""

    def test_save_and_load_tasks(self, storage, sample_tasks):
        """Test saving and loading tasks."""
        # Save tasks
        storage.save_tasks(sample_tasks)

        # Load tasks
        loaded_tasks = storage.load_tasks()

        assert len(loaded_tasks) == len(sample_tasks)
        assert loaded_tasks[0].title == sample_tasks[0].title
        assert loaded_tasks[1].priority == sample_tasks[1].priority

    def test_load_empty_file(self, temp_dir):
        """Test loading from non-existent file."""
        storage = TaskStorage(temp_dir / "nonexistent.json")
        tasks = storage.load_tasks()
        assert tasks == []

    def test_load_invalid_json(self, temp_dir):
        """Test loading from file with invalid JSON."""
        data_file = temp_dir / "invalid.json"
        data_file.write_text("invalid json content")

        storage = TaskStorage(data_file)

        with pytest.raises(TaskStorageError):
            storage.load_tasks()

    def test_save_to_read_only_location(self, temp_dir):
        """Test saving to read-only location."""
        # Create read-only directory
        readonly_dir = temp_dir / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)

        storage = TaskStorage(readonly_dir / "tasks.json")

        with pytest.raises(TaskStorageError):
            storage.save_tasks([Task.create("Test")])

    def test_backup_creation(self, storage, sample_tasks):
        """Test backup file creation."""
        # Save tasks first
        storage.save_tasks(sample_tasks)

        # Create backup
        backup_file = storage.backup_data()

        assert backup_file is not None
        assert backup_file.exists()
        assert backup_file.suffix == ".backup"

        # Verify backup content
        with open(backup_file) as f:
            backup_data = json.load(f)
        assert len(backup_data) == len(sample_tasks)
