FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root

# Copy application and README
COPY task_manager/ ./task_manager/
COPY README.md ./

# Install the project itself
RUN poetry install --without dev --no-interaction --no-ansi

# Create data directory
RUN mkdir -p /data

# Set data file location
ENV TASK_DATA_FILE=/data/tasks.json

# Create non-root user
RUN adduser --disabled-password --gecos '' taskuser
RUN chown -R taskuser:taskuser /app /data
USER taskuser

# Entry point
ENTRYPOINT ["python", "-m", "task_manager.cli"]