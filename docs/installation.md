# Installation Guide

This guide will help you install and set up the Task Manager CLI application.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- (Optional) Docker for containerized installation

## Installation Methods

### Using pip

```bash
# Install from PyPI
pip install task-manager

# Verify installation
task-manager --version
```

### Using Docker

```bash
# Pull the Docker image
docker pull yourusername/task-manager:latest

# Run the container
docker run -v task_data:/data yourusername/task-manager:latest
```

### Development Installation

For development purposes, you can install the package in editable mode:

```bash
# Clone the repository
git clone https://github.com/yourusername/task-manager.git
cd task-manager

# Install dependencies using Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Configuration

The Task Manager uses a JSON file to store tasks. By default, it's located at:
- Linux/macOS: `~/.task_manager/tasks.json`
- Windows: `%APPDATA%\task_manager\tasks.json`

You can customize the storage location using the `TASK_DATA_FILE` environment variable:

```bash
# Linux/macOS
export TASK_DATA_FILE=/path/to/your/tasks.json

# Windows (PowerShell)
$env:TASK_DATA_FILE = "C:\path\to\your\tasks.json"
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure you have write permissions to the data directory
   - Try running with elevated privileges if necessary

2. **Python Version Error**
   - Verify your Python version: `python --version`
   - Install Python 3.9 or higher if needed

3. **Docker Issues**
   - Ensure Docker is running
   - Check Docker permissions
   - Verify the volume mount is working

### Getting Help

If you encounter any issues:
1. Check the [GitHub Issues](https://github.com/yourusername/task-manager/issues)
2. Create a new issue if your problem isn't listed
3. Check the [User Guide](user-guide.md) for usage instructions 