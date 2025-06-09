"""Command-line interface for task manager."""

import os
import logging
from pathlib import Path
from typing import Optional

import click
from colorama import init, Fore, Style

from .models import Task, TaskStatus, Priority
from .storage import TaskStorage, TaskStorageError


# Initialize colorama for cross-platform colored output
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TaskManager:
    """Task manager business logic."""

    def __init__(self, storage: TaskStorage):
        """Initialize with storage backend."""
        self.storage = storage
        self._tasks = None

    @property
    def tasks(self) -> list[Task]:
        """Get current tasks, loading from storage if needed."""
        if self._tasks is None:
            self._tasks = self.storage.load_tasks()
        return self._tasks

    def add_task(
        self, title: str, description: str = "", priority: Priority = Priority.MEDIUM
    ) -> Task:
        """Add a new task."""
        task = Task.create(title=title, description=description, priority=priority)
        self.tasks.append(task)
        self._save_tasks()
        logger.info(f"Added task: {task.title}")
        return task

    def complete_task(self, task_id: str) -> Optional[Task]:
        """Mark a task as completed."""
        task = self._find_task(task_id)
        if task:
            task.complete()
            self._save_tasks()
            logger.info(f"Completed task: {task.title}")
        return task

    def delete_task(self, task_id: str) -> Optional[Task]:
        """Delete a task."""
        task = self._find_task(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            logger.info(f"Deleted task: {task.title}")
        return task

    def list_tasks(
        self, status: Optional[TaskStatus] = None, priority: Optional[Priority] = None
    ) -> list[Task]:
        """List tasks with optional filtering."""
        filtered_tasks = self.tasks

        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]

        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]

        return filtered_tasks

    def _find_task(self, task_id: str) -> Optional[Task]:
        """Find task by ID or partial ID."""
        # Try exact match first
        for task in self.tasks:
            if task.id == task_id:
                return task

        # Try partial match
        matching_tasks = [t for t in self.tasks if t.id.startswith(task_id)]
        if len(matching_tasks) == 1:
            return matching_tasks[0]
        elif len(matching_tasks) > 1:
            raise click.ClickException(
                f"Ambiguous task ID '{task_id}'. Multiple matches found."
            )

        return None

    def _save_tasks(self) -> None:
        """Save tasks to storage."""
        try:
            self.storage.save_tasks(self.tasks)
        except TaskStorageError as e:
            raise click.ClickException(f"Failed to save tasks: {e}")


# Global task manager instance
task_manager = None


def get_task_manager() -> TaskManager:
    """Get or create task manager instance."""
    global task_manager
    if task_manager is None:
        data_file = os.getenv("TASK_DATA_FILE", "~/.task_manager/tasks.json")
        storage = TaskStorage(Path(data_file))
        task_manager = TaskManager(storage)
    return task_manager


def format_task(task: Task, show_id: bool = False) -> str:
    """Format task for display."""
    status_color = Fore.GREEN if task.status == TaskStatus.COMPLETED else Fore.YELLOW
    priority_symbol = {"low": "◦", "medium": "●", "high": "◉"}[task.priority.value]

    parts = []
    if show_id:
        parts.append(f"{Fore.CYAN}{task.id[:8]}{Style.RESET_ALL}")

    parts.extend(
        [
            f"{status_color}{priority_symbol}{Style.RESET_ALL}",
            f"{Fore.WHITE}{task.title}{Style.RESET_ALL}",
        ]
    )

    if task.description:
        parts.append(f"{Fore.LIGHTBLACK_EX}- {task.description}{Style.RESET_ALL}")

    return " ".join(parts)


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
def cli(debug: bool):
    """Task Manager CLI - A simple task management tool."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


@cli.command()
@click.argument("title")
@click.option("--description", "-d", default="", help="Task description")
@click.option(
    "--priority",
    "-p",
    type=click.Choice(["low", "medium", "high"]),
    default="medium",
    help="Task priority",
)
def add(title: str, description: str, priority: str):
    """Add a new task."""
    try:
        priority_enum = Priority(priority)
        task = get_task_manager().add_task(title, description, priority_enum)
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Added task: {format_task(task)}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    "--status", type=click.Choice(["pending", "completed"]), help="Filter by status"
)
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high"]),
    help="Filter by priority",
)
@click.option("--show-id", is_flag=True, help="Show task IDs")
def list(status: Optional[str], priority: Optional[str], show_id: bool):
    """List tasks."""
    try:
        status_enum = TaskStatus(status) if status else None
        priority_enum = Priority(priority) if priority else None

        tasks = get_task_manager().list_tasks(status_enum, priority_enum)

        if not tasks:
            click.echo(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
            return

        click.echo(f"\n{Fore.CYAN}Tasks:{Style.RESET_ALL}")
        for task in tasks:
            click.echo(f"  {format_task(task, show_id)}")
        click.echo()

    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_id")
def complete(task_id: str):
    """Mark a task as completed."""
    try:
        task = get_task_manager().complete_task(task_id)
        if task:
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Completed: {format_task(task)}")
        else:
            click.echo(
                f"{Fore.RED}Task not found: {task_id}{Style.RESET_ALL}", err=True
            )
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_id")
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
def delete(task_id: str):
    """Delete a task."""
    try:
        task = get_task_manager().delete_task(task_id)
        if task:
            click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Deleted: {task.title}")
        else:
            click.echo(
                f"{Fore.RED}Task not found: {task_id}{Style.RESET_ALL}", err=True
            )
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
