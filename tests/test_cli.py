"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner
from task_manager.cli import cli
import os
import tempfile


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_data_file():
    """Create temporary data file for CLI tests."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_file = f.name

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


class TestCLI:
    """Test cases for CLI interface."""

    def test_add_task(self, runner, temp_data_file):
        """Test adding a task via CLI."""
        result = runner.invoke(
            cli,
            [
                "add",
                "Test Task",
                "--description",
                "Test description",
                "--priority",
                "high",
            ],
        )

        assert result.exit_code == 0
        assert "Added task" in result.output
        assert "Test Task" in result.output

    def test_list_empty_tasks(self, runner, temp_data_file):
        """Test listing when no tasks exist."""
        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_add_and_list_tasks(self, runner, temp_data_file):
        """Test adding and listing tasks."""
        # Add tasks
        runner.invoke(cli, ["add", "Task 1", "--priority", "high"])
        runner.invoke(cli, ["add", "Task 2", "--priority", "low"])

        # List tasks
        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" in result.output

    def test_complete_task(self, runner, temp_data_file):
        """Test completing a task."""
        # Add a task first
        add_result = runner.invoke(cli, ["add", "Test Task"])
        assert add_result.exit_code == 0

        # List with IDs to get task ID
        list_result = runner.invoke(cli, ["list", "--show-id"])
        task_id = list_result.output.split()[1]  # Extract first task ID

        # Complete the task
        complete_result = runner.invoke(
            cli, ["complete", task_id[:8]]
        )  # Use partial ID

        assert complete_result.exit_code == 0
        assert "Completed" in complete_result.output

    def test_delete_task_with_confirmation(self, runner, temp_data_file):
        """Test deleting a task with confirmation."""
        # Add a task first
        runner.invoke(cli, ["add", "Task to delete"])

        # Get task ID
        list_result = runner.invoke(cli, ["list", "--show-id"])
        task_id = list_result.output.split()[1]

        # Delete with confirmation
        result = runner.invoke(cli, ["delete", task_id[:8]], input="y\n")

        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_filter_by_status(self, runner, temp_data_file):
        """Test filtering tasks by status."""
        # Add and complete some tasks
        runner.invoke(cli, ["add", "Pending Task"])
        add_result = runner.invoke(cli, ["add", "Completed Task"])

        # Get task ID and complete it
        list_result = runner.invoke(cli, ["list", "--show-id"])
        lines = list_result.output.strip().split("\n")
        task_line = [line for line in lines if "Completed Task" in line][0]
        task_id = task_line.split()[0]

        runner.invoke(cli, ["complete", task_id])

        # Filter by status
        pending_result = runner.invoke(cli, ["list", "--status", "pending"])
        completed_result = runner.invoke(cli, ["list", "--status", "completed"])

        assert "Pending Task" in pending_result.output
        assert "Completed Task" not in pending_result.output
        assert "Completed Task" in completed_result.output
        assert "Pending Task" not in completed_result.output


class TestTaskManagerIntegration:
    """Integration tests for TaskManager class."""

    def test_task_lifecycle(self, storage):
        """Test complete task lifecycle."""
        from task_manager.cli import TaskManager
        from task_manager.models import Priority, TaskStatus

        manager = TaskManager(storage)

        # Add tasks
        task1 = manager.add_task("Task 1", "Description 1", Priority.HIGH)
        task2 = manager.add_task("Task 2", "Description 2", Priority.LOW)

        # List tasks
        all_tasks = manager.list_tasks()
        assert len(all_tasks) == 2

        # Filter by priority
        high_priority = manager.list_tasks(priority=Priority.HIGH)
        assert len(high_priority) == 1
        assert high_priority[0].title == "Task 1"

        # Complete task
        completed = manager.complete_task(task1.id)
        assert completed is not None
        assert completed.status == TaskStatus.COMPLETED

        # Filter by status
        pending_tasks = manager.list_tasks(status=TaskStatus.PENDING)
        assert len(pending_tasks) == 1

        # Delete task
        deleted = manager.delete_task(task2.id)
        assert deleted is not None

        final_tasks = manager.list_tasks()
        assert len(final_tasks) == 1
