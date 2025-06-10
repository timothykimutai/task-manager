"""Command-line interface for task manager."""

import os
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import click
from colorama import init, Fore, Style

from .models import Task, TaskStatus, Priority
from .storage import TaskStorage, TaskStorageError
from .utils import (
    colorize,
    format_datetime,
    format_priority,
    format_status,
    format_category,
    format_reminder,
)


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
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        category: Optional[str] = None,
        tags: List[str] = None,
        due_date: Optional[datetime] = None,
        reminder: Optional[datetime] = None,
    ) -> Task:
        """Add a new task."""
        task = Task.create(
            title=title,
            description=description,
            priority=priority,
            category=category,
            tags=tags or [],
            due_date=due_date,
            reminder=reminder,
        )
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
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[Priority] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """List tasks with optional filtering."""
        filtered_tasks = self.tasks

        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]

        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]

        if category:
            filtered_tasks = [t for t in filtered_tasks if t.category == category]

        if tag:
            filtered_tasks = [t for t in filtered_tasks if t.has_tag(tag)]

        if overdue:
            filtered_tasks = [t for t in filtered_tasks if t.is_overdue()]

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
    parts = []

    if show_id:
        parts.append(f"{Fore.CYAN}{task.id[:8]}{Style.RESET_ALL}")

    parts.extend([
        format_priority(task.priority.value),
        format_category(task.category),
        f"{Fore.WHITE}{task.title}{Style.RESET_ALL}",
    ])

    if task.description:
        parts.append(f"{Fore.LIGHTBLACK_EX}- {task.description}{Style.RESET_ALL}")

    if task.tags:
        tags_str = " ".join(f"#{tag}" for tag in task.tags)
        parts.append(f"{Fore.BLUE}{tags_str}{Style.RESET_ALL}")

    if task.due_date:
        due_str = format_datetime(task.due_date)
        if task.is_overdue():
            parts.append(f"{Fore.RED}Due: {due_str}{Style.RESET_ALL}")
        else:
            parts.append(f"{Fore.YELLOW}Due: {due_str}{Style.RESET_ALL}")

    if task.reminder:
        parts.append(format_reminder(task.reminder))

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
@click.option("--category", "-c", help="Task category")
@click.option("--tags", "-t", help="Comma-separated list of tags")
@click.option("--due-date", help="Due date (YYYY-MM-DD)")
@click.option("--reminder", help="Reminder date and time (YYYY-MM-DD HH:MM)")
def add(title: str, description: str, priority: str, category: str, tags: str, due_date: str, reminder: str):
    """Add a new task."""
    try:
        priority_enum = Priority(priority)
        tags_list = tags.split(",") if tags else []
        
        # Parse dates
        due_date_dt = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
        reminder_dt = datetime.strptime(reminder, "%Y-%m-%d %H:%M") if reminder else None

        task = get_task_manager().add_task(
            title=title,
            description=description,
            priority=priority_enum,
            category=category,
            tags=tags_list,
            due_date=due_date_dt,
            reminder=reminder_dt,
        )
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
@click.option("--category", help="Filter by category")
@click.option("--tag", help="Filter by tag")
@click.option("--overdue", is_flag=True, help="Show only overdue tasks")
@click.option("--show-id", is_flag=True, help="Show task IDs")
def list(status: Optional[str], priority: Optional[str], category: Optional[str], tag: Optional[str], overdue: bool, show_id: bool):
    """List tasks."""
    try:
        status_enum = TaskStatus(status) if status else None
        priority_enum = Priority(priority) if priority else None

        tasks = get_task_manager().list_tasks(
            status=status_enum,
            priority=priority_enum,
            category=category,
            tag=tag,
            overdue=overdue,
        )

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


@cli.command()
@click.argument("file_path", type=click.Path())
@click.option("--format", type=click.Choice(["json", "csv"]), default="json", help="Export format")
def export(file_path: str, format: str):
    """Export tasks to a file."""
    try:
        storage = get_task_manager().storage
        if format == "json":
            storage.export_to_json(Path(file_path))
        else:
            storage.export_to_csv(Path(file_path))
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Exported tasks to {file_path}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--format", type=click.Choice(["json", "csv"]), default="json", help="Import format")
def import_tasks(file_path: str, format: str):
    """Import tasks from a file."""
    try:
        storage = get_task_manager().storage
        if format == "json":
            tasks = storage.import_from_json(Path(file_path))
        else:
            tasks = storage.import_from_csv(Path(file_path))
        get_task_manager()._tasks = tasks
        get_task_manager()._save_tasks()
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Imported {len(tasks)} tasks from {file_path}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", err=True)
        raise click.Abort()


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
