# User Guide

This guide will help you use the Task Manager CLI effectively.

## Basic Commands

### Adding Tasks

```bash
# Add a simple task
task-manager add "Buy groceries"

# Add a task with description
task-manager add "Complete project" --description "Finish the documentation and tests"

# Add a high priority task
task-manager add "Fix critical bug" --priority high
```

### Listing Tasks

```bash
# List all tasks
task-manager list

# List only incomplete tasks
task-manager list --status incomplete

# List high priority tasks
task-manager list --priority high

# List tasks with custom format
task-manager list --format "ID: {id}, Task: {title}, Priority: {priority}"
```

### Managing Tasks

```bash
# Complete a task
task-manager complete <task-id>

# Delete a task
task-manager delete <task-id>

# Update a task
task-manager update <task-id> --title "New title" --priority low
```

## Advanced Usage

### Task Priorities

Tasks can have the following priorities:
- `low`: Low priority tasks
- `medium`: Default priority
- `high`: High priority tasks

### Task Status

Tasks can be in one of these states:
- `incomplete`: Default state for new tasks
- `complete`: Tasks that have been completed

### Filtering Tasks

You can combine multiple filters:

```bash
# List incomplete high priority tasks
task-manager list --status incomplete --priority high

# List completed low priority tasks
task-manager list --status complete --priority low
```

### Output Formatting

The `--format` option allows custom output formatting using Python's string formatting syntax:

```bash
# Show only task titles
task-manager list --format "{title}"

# Show task details in a custom format
task-manager list --format "Task {id}: {title} ({priority}) - {status}"
```

Available format fields:
- `{id}`: Task ID
- `{title}`: Task title
- `{description}`: Task description
- `{priority}`: Task priority
- `{status}`: Task status
- `{created_at}`: Creation timestamp
- `{completed_at}`: Completion timestamp (if completed)

## Best Practices

1. **Task Organization**
   - Use clear, descriptive titles
   - Add detailed descriptions for complex tasks
   - Set appropriate priorities

2. **Regular Maintenance**
   - Complete tasks when finished
   - Delete obsolete tasks
   - Review and update task priorities

3. **Backup**
   - Regularly backup your tasks file
   - Use version control for important task lists

## Tips and Tricks

1. **Quick Task Addition**
   ```bash
   # Add multiple tasks quickly
   echo "Task 1" | task-manager add
   echo "Task 2" | task-manager add
   ```

2. **Task Search**
   ```bash
   # Use grep to search tasks
   task-manager list | grep "important"
   ```

3. **Task Export**
   ```bash
   # Export tasks to a file
   task-manager list > tasks.txt
   ``` 