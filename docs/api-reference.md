# API Reference

This document provides detailed information about the Task Manager's internal API.

## Models

### Task

The `Task` class represents a single task in the system.

```python
from task_manager.models import Task

# Create a new task
task = Task(
    title="Example task",
    description="Task description",
    priority="high"
)
```

#### Attributes

- `id` (str): Unique identifier for the task
- `title` (str): Task title
- `description` (str, optional): Task description
- `priority` (str): Task priority ("low", "medium", "high")
- `status` (str): Task status ("incomplete", "complete")
- `created_at` (datetime): Task creation timestamp
- `completed_at` (datetime, optional): Task completion timestamp

#### Methods

- `complete()`: Mark the task as complete
- `to_dict()`: Convert task to dictionary
- `from_dict(data)`: Create task from dictionary

## Storage

### TaskStorage

The `TaskStorage` class handles task persistence.

```python
from task_manager.storage import TaskStorage

# Initialize storage
storage = TaskStorage()

# Add a task
storage.add_task(task)

# Get all tasks
tasks = storage.get_tasks()

# Get task by ID
task = storage.get_task(task_id)
```

#### Methods

- `add_task(task)`: Add a new task
- `get_tasks()`: Get all tasks
- `get_task(task_id)`: Get task by ID
- `update_task(task)`: Update an existing task
- `delete_task(task_id)`: Delete a task
- `save()`: Save tasks to storage
- `load()`: Load tasks from storage

## CLI

### Command Line Interface

The CLI module provides the command-line interface for the application.

```python
from task_manager.cli import main

# Run the CLI
main()
```

#### Commands

- `add`: Add a new task
- `list`: List tasks
- `complete`: Complete a task
- `delete`: Delete a task
- `update`: Update a task

#### Options

- `--priority`: Set task priority
- `--description`: Set task description
- `--status`: Filter by status
- `--format`: Custom output format

## Utilities

### Color Output

The `utils` module provides color output functionality.

```python
from task_manager.utils import colorize

# Colorize text
colored_text = colorize("Important", "red")
```

#### Available Colors

- `red`: Error messages
- `green`: Success messages
- `yellow`: Warning messages
- `blue`: Information messages

## Error Handling

### Exceptions

- `TaskError`: Base exception for task-related errors
- `TaskNotFoundError`: Task not found
- `StorageError`: Storage-related errors
- `ValidationError`: Input validation errors

## Configuration

### Environment Variables

- `TASK_DATA_FILE`: Path to the tasks data file
- `TASK_COLOR_OUTPUT`: Enable/disable color output

### Default Values

- Default data file location:
  - Linux/macOS: `~/.task_manager/tasks.json`
  - Windows: `%APPDATA%\task_manager\tasks.json`
- Default priority: "medium"
- Default status: "incomplete" 