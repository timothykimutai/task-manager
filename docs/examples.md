# Examples

This document provides practical examples of using the Task Manager CLI.

## Basic Task Management

### Creating a Task List

```bash
# Add some tasks
task-manager add "Buy groceries" --description "Milk, eggs, bread" --priority high
task-manager add "Call mom" --priority medium
task-manager add "Read book" --description "Chapter 5" --priority low

# List all tasks
task-manager list
```

### Managing Task Priorities

```bash
# Add high priority tasks
task-manager add "Fix critical bug" --priority high
task-manager add "Update documentation" --priority high

# Add medium priority tasks
task-manager add "Code review" --priority medium
task-manager add "Team meeting" --priority medium

# Add low priority tasks
task-manager add "Clean desk" --priority low
task-manager add "Update resume" --priority low

# List tasks by priority
task-manager list --priority high
task-manager list --priority medium
task-manager list --priority low
```

### Task Completion Workflow

```bash
# Add a task
task-manager add "Complete project" --description "Finish all pending work"

# List incomplete tasks
task-manager list --status incomplete

# Complete the task
task-manager complete <task-id>

# Verify completion
task-manager list --status complete
```

## Advanced Usage

### Custom Output Formatting

```bash
# Show only task titles
task-manager list --format "{title}"

# Show task details in a custom format
task-manager list --format "Task {id}: {title} ({priority}) - {status}"

# Show task with description
task-manager list --format "{title}\n  Description: {description}\n  Priority: {priority}"
```

### Task Filtering

```bash
# Show incomplete high priority tasks
task-manager list --status incomplete --priority high

# Show completed low priority tasks
task-manager list --status complete --priority low

# Show tasks with specific text in title
task-manager list | grep "bug"
```

### Task Updates

```bash
# Add a task
task-manager add "Initial task" --priority low

# Update task priority
task-manager update <task-id> --priority high

# Update task description
task-manager update <task-id> --description "Updated description"

# Update multiple fields
task-manager update <task-id> --title "New title" --priority medium --description "New description"
```

## Integration Examples

### Using with Shell Scripts

```bash
#!/bin/bash
# Add tasks from a file
while read -r line; do
    task-manager add "$line"
done < tasks.txt

# Export tasks to a file
task-manager list > completed_tasks.txt
```

### Using with Python

```python
import subprocess

def add_task(title, description=None, priority=None):
    cmd = ["task-manager", "add", title]
    if description:
        cmd.extend(["--description", description])
    if priority:
        cmd.extend(["--priority", priority])
    subprocess.run(cmd)

def list_tasks():
    result = subprocess.run(["task-manager", "list"], capture_output=True, text=True)
    return result.stdout

# Example usage
add_task("Python task", "Created from Python", "high")
tasks = list_tasks()
print(tasks)
```

### Using with Docker

```bash
# Run with custom data directory
docker run -v /path/to/data:/data task-manager list

# Run with environment variables
docker run -e TASK_DATA_FILE=/data/tasks.json task-manager add "Docker task"
```

## Best Practices

### Task Organization

```bash
# Use clear, descriptive titles
task-manager add "Fix login page CSS issues" --description "Update styles for mobile view"

# Group related tasks with similar descriptions
task-manager add "Update user documentation" --description "Part 1: Installation guide"
task-manager add "Update user documentation" --description "Part 2: Configuration"
task-manager add "Update user documentation" --description "Part 3: Troubleshooting"
```

### Regular Maintenance

```bash
# Complete finished tasks
task-manager complete <task-id>

# Delete obsolete tasks
task-manager delete <task-id>

# Review and update priorities
task-manager update <task-id> --priority high
```

### Backup and Restore

```bash
# Backup tasks
cp ~/.task_manager/tasks.json tasks_backup.json

# Restore tasks
cp tasks_backup.json ~/.task_manager/tasks.json
``` 