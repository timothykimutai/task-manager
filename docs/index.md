# Task Manager Documentation

Welcome to the Task Manager documentation! This documentation will help you understand how to use and extend the Task Manager CLI application.

## Table of Contents

1. [Installation Guide](installation.md)
2. [User Guide](user-guide.md)
3. [API Reference](api-reference.md)
4. [Examples](examples.md)
5. [Development Guide](development.md)

## Overview

Task Manager is a command-line task management tool that helps you organize and track your tasks efficiently. It provides a simple yet powerful interface for managing tasks with features like:

- Task creation with descriptions and priorities
- Task listing and filtering
- Task completion tracking
- Task deletion
- Persistent storage of tasks

## Quick Start

```bash
# Install the package
pip install task-manager

# Add your first task
task-manager add "Complete project documentation" --priority high

# List your tasks
task-manager list
```

For more detailed information, please refer to the specific sections in the documentation.

# Task Manager CLI

Welcome to the Task Manager CLI documentation!

Task Manager is a simple, elegant command-line tool for managing your daily tasks. Built with Python, it provides a clean interface for adding, listing, completing, and organizing your tasks.

## Why Task Manager CLI?

- **Simple**: Intuitive commands that are easy to remember
- **Fast**: Quick task management from your terminal
- **Persistent**: Your tasks are saved automatically
- **Flexible**: Filter and organize tasks by status and priority
- **Beautiful**: Colorful output that's easy to read

## Key Features

!!! tip "Core Functionality"
    - Add tasks with descriptions and priorities
    - List tasks with filtering options
    - Mark tasks as completed
    - Delete tasks you no longer need
    - Persistent JSON storage
    - Colorful CLI interface

## Quick Example

```bash
# Add a high-priority task
$ task-manager add "Review quarterly report" --priority high

# List all pending tasks
$ task-manager list --status pending

# Complete a task
$ task-manager complete abc123