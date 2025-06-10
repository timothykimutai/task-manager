# Development Guide

This guide will help you set up the development environment and contribute to the Task Manager project.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- Git for version control
- Docker (optional) for containerized development

### Setting Up the Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=task_manager

# Run specific test file
poetry run pytest tests/test_cli.py

# Run tests with specific marker
poetry run pytest -m "not slow"
```

### Code Quality

```bash
# Format code
poetry run black task_manager/ tests/

# Check code style
poetry run flake8 task_manager/ tests/

# Type checking
poetry run mypy task_manager/
```

## Project Structure

```
task-manager/
├── task_manager/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── models.py       # Data models
│   ├── storage.py      # Storage handling
│   └── utils.py        # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Test configuration
│   ├── test_cli.py     # CLI tests
│   ├── test_models.py  # Model tests
│   └── test_storage.py # Storage tests
├── docs/               # Documentation
├── pyproject.toml      # Project configuration
└── README.md          # Project overview
```

## Adding New Features

### 1. Create a New Branch

```bash
git checkout -b feature/new-feature
```

### 2. Implement the Feature

- Add new code in the appropriate module
- Add tests for the new functionality
- Update documentation

### 3. Run Tests and Checks

```bash
# Run all checks
poetry run black task_manager/ tests/
poetry run flake8 task_manager/ tests/
poetry run mypy task_manager/
poetry run pytest
```

### 4. Create a Pull Request

- Push your branch to GitHub
- Create a pull request
- Wait for review and CI checks

## Code Style Guide

### Python Code

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Example

```python
from typing import List, Optional

def get_tasks_by_priority(
    tasks: List[Task],
    priority: str
) -> List[Task]:
    """
    Filter tasks by priority.

    Args:
        tasks: List of tasks to filter
        priority: Priority level to filter by

    Returns:
        List of tasks with the specified priority
    """
    return [task for task in tasks if task.priority == priority]
```

### Testing Guidelines

- Write unit tests for all new code
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies
- Test edge cases and error conditions

### Example

```python
def test_get_tasks_by_priority():
    # Arrange
    tasks = [
        Task("Task 1", priority="high"),
        Task("Task 2", priority="low"),
        Task("Task 3", priority="high")
    ]

    # Act
    high_priority_tasks = get_tasks_by_priority(tasks, "high")

    # Assert
    assert len(high_priority_tasks) == 2
    assert all(task.priority == "high" for task in high_priority_tasks)
```

## Release Process

### 1. Update Version

```bash
# Update version in pyproject.toml
poetry version patch  # or minor/major
```

### 2. Update Changelog

- Add release notes to CHANGELOG.md
- Document new features and bug fixes

### 3. Create Release

```bash
# Create and push tag
git tag v0.1.0
git push origin v0.1.0
```

### 4. Build and Publish

```bash
# Build package
poetry build

# Publish to PyPI
poetry publish
```

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and checks
5. Submit a pull request

### Commit Messages

Follow the Conventional Commits specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for test changes
- `chore:` for maintenance tasks

### Example

```
feat: add task filtering by date

- Add date field to Task model
- Implement date filtering in CLI
- Add tests for date filtering
- Update documentation
```

## Troubleshooting

### Common Issues

1. **Poetry Installation Issues**
   - Clear Poetry cache: `poetry cache clear . --all`
   - Update Poetry: `poetry self update`

2. **Test Failures**
   - Check test data directory permissions
   - Verify test environment variables
   - Check for conflicting test data

3. **Docker Issues**
   - Rebuild Docker image: `docker compose build --no-cache`
   - Check volume permissions
   - Verify Docker daemon is running 