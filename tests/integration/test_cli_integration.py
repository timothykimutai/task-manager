"""Integration tests for CLI functionality."""

import os
import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from click.testing import CliRunner

from task_manager.cli import cli
from task_manager.models import TaskStatus, Priority


@pytest.fixture
def cli_runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_data_file():
    """Create a temporary data file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        yield Path(f.name)
    os.unlink(f.name)


@pytest.fixture
def runner_with_temp_file(cli_runner, temp_data_file):
    """Create a CLI runner with a temporary data file."""
    os.environ["TASK_DATA_FILE"] = str(temp_data_file)
    return cli_runner


def test_add_and_list_task(runner_with_temp_file):
    """Test adding and listing a task."""
    # Add a task
    result = runner_with_temp_file.invoke(
        cli,
        [
            "add",
            "Test task",
            "--description",
            "Test description",
            "--priority",
            "high",
            "--category",
            "test",
            "--tags",
            "test,integration",
            "--due-date",
            "2024-12-31",
            "--reminder",
            "2024-12-30 10:00",
        ],
    )
    assert result.exit_code == 0
    assert "Added task" in result.output

    # List tasks
    result = runner_with_temp_file.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Test task" in result.output
    assert "Test description" in result.output
    assert "high" in result.output
    assert "test" in result.output
    assert "#test" in result.output
    assert "#integration" in result.output
    assert "2024-12-31" in result.output
    assert "2024-12-30 10:00" in result.output


def test_task_filtering(runner_with_temp_file):
    """Test task filtering functionality."""
    # Add multiple tasks with different properties
    runner_with_temp_file.invoke(
        cli,
        [
            "add",
            "High priority task",
            "--priority",
            "high",
            "--category",
            "work",
        ],
    )
    runner_with_temp_file.invoke(
        cli,
        [
            "add",
            "Low priority task",
            "--priority",
            "low",
            "--category",
            "personal",
        ],
    )
    runner_with_temp_file.invoke(
        cli,
        [
            "add",
            "Tagged task",
            "--tags",
            "important,urgent",
        ],
    )

    # Test filtering by priority
    result = runner_with_temp_file.invoke(cli, ["list", "--priority", "high"])
    assert result.exit_code == 0
    assert "High priority task" in result.output
    assert "Low priority task" not in result.output

    # Test filtering by category
    result = runner_with_temp_file.invoke(cli, ["list", "--category", "work"])
    assert result.exit_code == 0
    assert "High priority task" in result.output
    assert "Low priority task" not in result.output

    # Test filtering by tag
    result = runner_with_temp_file.invoke(cli, ["list", "--tag", "important"])
    assert result.exit_code == 0
    assert "Tagged task" in result.output
    assert "High priority task" not in result.output


def test_task_completion(runner_with_temp_file):
    """Test task completion functionality."""
    # Add a task
    result = runner_with_temp_file.invoke(cli, ["add", "Task to complete"])
    assert result.exit_code == 0

    # Get task ID from list output
    result = runner_with_temp_file.invoke(cli, ["list", "--show-id"])
    assert result.exit_code == 0
    task_id = result.output.split()[0]  # First word should be the task ID

    # Complete the task
    result = runner_with_temp_file.invoke(cli, ["complete", task_id])
    assert result.exit_code == 0
    assert "Completed" in result.output

    # Verify task is marked as completed
    result = runner_with_temp_file.invoke(cli, ["list", "--status", "completed"])
    assert result.exit_code == 0
    assert "Task to complete" in result.output


def test_task_deletion(runner_with_temp_file):
    """Test task deletion functionality."""
    # Add a task
    result = runner_with_temp_file.invoke(cli, ["add", "Task to delete"])
    assert result.exit_code == 0

    # Get task ID from list output
    result = runner_with_temp_file.invoke(cli, ["list", "--show-id"])
    assert result.exit_code == 0
    task_id = result.output.split()[0]  # First word should be the task ID

    # Delete the task (with confirmation)
    result = runner_with_temp_file.invoke(cli, ["delete", task_id], input="y\n")
    assert result.exit_code == 0
    assert "Deleted" in result.output

    # Verify task is gone
    result = runner_with_temp_file.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Task to delete" not in result.output


def test_export_import(runner_with_temp_file, tempfile):
    """Test task export and import functionality."""
    # Add some tasks
    runner_with_temp_file.invoke(cli, ["add", "Task 1"])
    runner_with_temp_file.invoke(cli, ["add", "Task 2"])

    # Export to JSON
    export_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    export_file.close()
    result = runner_with_temp_file.invoke(cli, ["export", export_file.name])
    assert result.exit_code == 0
    assert "Exported" in result.output

    # Clear tasks by using a new data file
    new_data_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    new_data_file.close()
    os.environ["TASK_DATA_FILE"] = new_data_file.name

    # Import from JSON
    result = runner_with_temp_file.invoke(cli, ["import-tasks", export_file.name])
    assert result.exit_code == 0
    assert "Imported" in result.output

    # Verify tasks were imported
    result = runner_with_temp_file.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" in result.output

    # Clean up
    os.unlink(export_file.name)
    os.unlink(new_data_file.name)


def test_overdue_tasks(runner_with_temp_file):
    """Test overdue task functionality."""
    # Add a task with past due date
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    runner_with_temp_file.invoke(
        cli,
        [
            "add",
            "Overdue task",
            "--due-date",
            past_date,
        ],
    )

    # Add a task with future due date
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    runner_with_temp_file.invoke(
        cli,
        [
            "add",
            "Future task",
            "--due-date",
            future_date,
        ],
    )

    # Test overdue filter
    result = runner_with_temp_file.invoke(cli, ["list", "--overdue"])
    assert result.exit_code == 0
    assert "Overdue task" in result.output
    assert "Future task" not in result.output 