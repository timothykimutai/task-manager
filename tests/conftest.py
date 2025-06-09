"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil
import os
import sys
from task_manager.storage import TaskStorage
from task_manager.models import Task, Priority, TaskStatus


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def storage(temp_dir):
    """Create TaskStorage instance with temporary file."""
    data_file = temp_dir / "test_tasks.json"
    return TaskStorage(data_file)


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task.create(
        title="Test Task", description="A task for testing", priority=Priority.HIGH
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks."""
    return [
        Task.create("Task 1", "First task", Priority.HIGH),
        Task.create("Task 2", "Second task", Priority.MEDIUM),
        Task.create("Task 3", "Third task", Priority.LOW),
    ]


@pytest.fixture
def temp_data_file():
    """Create temporary data file for CLI tests, always empty at start."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_file = f.name
        f.write("[]")  # Ensure file is empty JSON array
        f.flush()

    # Set environment variable for CLI
    original_value = os.environ.get("TASK_DATA_FILE")
    os.environ["TASK_DATA_FILE"] = temp_file

    yield temp_file

    # Cleanup
    if original_value is not None:
        os.environ["TASK_DATA_FILE"] = original_value
    else:
        os.environ.pop("TASK_DATA_FILE", None)

    if os.path.exists(temp_file):
        os.unlink(temp_file)


# Fixture to reset the global task_manager in cli.py before each CLI test
@pytest.fixture(autouse=True)
def reset_task_manager(monkeypatch):
    import task_manager.cli

    monkeypatch.setattr(task_manager.cli, "task_manager", None)


# Skip read-only test on Windows
def pytest_collection_modifyitems(config, items):
    if sys.platform.startswith("win"):
        skip_marker = pytest.mark.skip(
            reason="Read-only directory test is not reliable on Windows."
        )
        for item in items:
            if item.name == "test_save_to_read_only_location":
                item.add_marker(skip_marker)
