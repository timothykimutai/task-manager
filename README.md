# Task Manager

A simple command-line task management tool built with Python.

## Features

- Add, list, complete, and delete tasks
- Set task priorities
- Filter tasks by status and priority
- Persistent storage of tasks

## Installation

```bash
# Using pip
pip install task-manager

# Using Docker
docker run -v task_data:/data task-manager
```

## Usage

```bash
# Add a task
task-manager add "Buy groceries" --description "Milk, eggs, bread" --priority high

# List tasks
task-manager list

# Complete a task
task-manager complete <task-id>

# Delete a task
task-manager delete <task-id>
```

## Development

This project uses Poetry for dependency management. To set up the development environment:

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest