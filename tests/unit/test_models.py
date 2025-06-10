"""Unit tests for task manager models."""

import pytest
from datetime import datetime, timedelta
from task_manager.models import Task, TaskStatus, Priority


def test_task_creation():
    """Test basic task creation."""
    task = Task.create("Test task")
    assert task.title == "Test task"
    assert task.description == ""
    assert task.status == TaskStatus.PENDING
    assert task.priority == Priority.MEDIUM
    assert task.category is None
    assert task.tags == []
    assert task.due_date is None
    assert task.reminder is None
    assert task.created_at is not None
    assert task.completed_at is None


def test_task_creation_with_all_fields():
    """Test task creation with all fields."""
    now = datetime.now()
    task = Task.create(
        title="Test task",
        description="Test description",
        priority=Priority.HIGH,
        category="test",
        tags=["tag1", "tag2"],
        due_date=now + timedelta(days=1),
        reminder=now + timedelta(hours=1),
    )
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.priority == Priority.HIGH
    assert task.category == "test"
    assert task.tags == ["tag1", "tag2"]
    assert task.due_date == now + timedelta(days=1)
    assert task.reminder == now + timedelta(hours=1)


def test_task_completion():
    """Test task completion."""
    task = Task.create("Test task")
    assert task.status == TaskStatus.PENDING
    assert task.completed_at is None

    task.complete()
    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None


def test_task_tag_operations():
    """Test task tag operations."""
    task = Task.create("Test task")
    assert task.tags == []

    # Add tags
    task.add_tag("tag1")
    assert task.tags == ["tag1"]
    task.add_tag("tag2")
    assert task.tags == ["tag1", "tag2"]

    # Add duplicate tag
    task.add_tag("tag1")
    assert task.tags == ["tag1", "tag2"]

    # Remove tag
    task.remove_tag("tag1")
    assert task.tags == ["tag2"]

    # Remove non-existent tag
    task.remove_tag("nonexistent")
    assert task.tags == ["tag2"]

    # Check tag existence
    assert task.has_tag("tag2")
    assert not task.has_tag("tag1")


def test_task_overdue():
    """Test task overdue status."""
    now = datetime.now()
    
    # Task with past due date
    past_task = Task.create(
        "Past task",
        due_date=now - timedelta(days=1)
    )
    assert past_task.is_overdue()

    # Task with future due date
    future_task = Task.create(
        "Future task",
        due_date=now + timedelta(days=1)
    )
    assert not future_task.is_overdue()

    # Task without due date
    no_date_task = Task.create("No date task")
    assert not no_date_task.is_overdue()

    # Completed task with past due date
    completed_task = Task.create(
        "Completed task",
        due_date=now - timedelta(days=1)
    )
    completed_task.complete()
    assert not completed_task.is_overdue()


def test_task_serialization():
    """Test task serialization to and from dictionary."""
    now = datetime.now()
    task = Task.create(
        title="Test task",
        description="Test description",
        priority=Priority.HIGH,
        category="test",
        tags=["tag1", "tag2"],
        due_date=now + timedelta(days=1),
        reminder=now + timedelta(hours=1),
    )

    # Convert to dictionary
    data = task.to_dict()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert data["category"] == "test"
    assert data["tags"] == ["tag1", "tag2"]
    assert data["due_date"] == (now + timedelta(days=1)).isoformat()
    assert data["reminder"] == (now + timedelta(hours=1)).isoformat()

    # Create new task from dictionary
    new_task = Task.from_dict(data)
    assert new_task.title == task.title
    assert new_task.description == task.description
    assert new_task.priority == task.priority
    assert new_task.status == task.status
    assert new_task.category == task.category
    assert new_task.tags == task.tags
    assert new_task.due_date == task.due_date
    assert new_task.reminder == task.reminder


def test_task_serialization_edge_cases():
    """Test task serialization with edge cases."""
    # Task with None values
    task = Task.create("Test task")
    data = task.to_dict()
    assert data["category"] is None
    assert data["due_date"] is None
    assert data["reminder"] is None
    assert data["completed_at"] is None

    # Task with empty tags
    task = Task.create("Test task", tags=[])
    data = task.to_dict()
    assert data["tags"] == []

    # Task with completed status
    task = Task.create("Test task")
    task.complete()
    data = task.to_dict()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

    # Create task from minimal data
    minimal_data = {
        "id": "test-id",
        "title": "Test task",
        "status": "pending",
        "priority": "medium",
        "created_at": datetime.now().isoformat(),
    }
    task = Task.from_dict(minimal_data)
    assert task.title == "Test task"
    assert task.description == ""
    assert task.category is None
    assert task.tags == []
    assert task.due_date is None
    assert task.reminder is None
    assert task.completed_at is None


def test_task_validation():
    """Test task validation."""
    # Test empty title
    with pytest.raises(ValueError):
        Task.create("")

    # Test invalid priority
    with pytest.raises(ValueError):
        Task.create("Test task", priority="invalid")

    # Test invalid status
    with pytest.raises(ValueError):
        Task(id="test", title="Test task", status="invalid")

    # Test invalid date format
    with pytest.raises(ValueError):
        Task.from_dict({
            "id": "test",
            "title": "Test task",
            "status": "pending",
            "priority": "medium",
            "created_at": "invalid-date",
        })


def test_task_equality():
    """Test task equality comparison."""
    task1 = Task.create("Test task")
    task2 = Task.create("Test task")
    task3 = Task.create("Different task")

    # Tasks with same ID should be equal
    task2.id = task1.id
    assert task1 == task2
    assert task1 != task3

    # Tasks with different IDs should not be equal
    task2.id = "different-id"
    assert task1 != task2


def test_task_string_representation():
    """Test task string representation."""
    task = Task.create(
        "Test task",
        description="Test description",
        priority=Priority.HIGH,
        category="test",
        tags=["tag1", "tag2"],
    )
    task_str = str(task)
    assert "Test task" in task_str
    assert "Test description" in task_str
    assert "high" in task_str
    assert "test" in task_str
    assert "tag1" in task_str
    assert "tag2" in task_str 