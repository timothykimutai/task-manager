"""Tests for data models."""

import pytest
from datetime import datetime
from task_manager.models import Task, TaskStatus, Priority


class TestTask:
    """Test cases for Task model."""

    def test_task_creation(self):
        """Test basic task creation."""
        task = Task.create("Test Task", "Description", Priority.HIGH)

        assert task.title == "Test Task"
        assert task.description == "Description"
        assert task.priority == Priority.HIGH
        assert task.status == TaskStatus.PENDING
        assert task.id is not None
        assert isinstance(task.created_at, datetime)
        assert task.completed_at is None

    def test_task_completion(self):
        """Test task completion."""
        task = Task.create("Test Task")
        initial_time = datetime.now()

        task.complete()

        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None
        assert task.completed_at >= initial_time

    def test_task_serialization(self):
        """Test task to/from dict conversion."""
        original_task = Task.create("Test Task", "Description", Priority.HIGH)
        original_task.complete()

        # Convert to dict and back
        task_dict = original_task.to_dict()
        restored_task = Task.from_dict(task_dict)

        assert restored_task.id == original_task.id
        assert restored_task.title == original_task.title
        assert restored_task.description == original_task.description
        assert restored_task.priority == original_task.priority
        assert restored_task.status == original_task.status
        assert restored_task.created_at == original_task.created_at
        assert restored_task.completed_at == original_task.completed_at

    def test_task_dict_format(self):
        """Test task dictionary format."""
        task = Task.create("Test Task", "Description", Priority.HIGH)
        task_dict = task.to_dict()

        assert "id" in task_dict
        assert "title" in task_dict
        assert "description" in task_dict
        assert task_dict["priority"] == "high"
        assert task_dict["status"] == "pending"
        assert "created_at" in task_dict
        assert "completed_at" in task_dict
