"""Performance tests for storage operations."""

import time
import tempfile
from pathlib import Path
import pytest
from datetime import datetime, timedelta

from task_manager.models import Task, Priority, TaskStatus
from task_manager.storage import TaskStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        yield TaskStorage(Path(f.name))
    Path(f.name).unlink()


def generate_test_tasks(count: int) -> list[Task]:
    """Generate a list of test tasks."""
    tasks = []
    for i in range(count):
        task = Task.create(
            title=f"Test Task {i}",
            description=f"Description for task {i}",
            priority=Priority.HIGH if i % 3 == 0 else Priority.MEDIUM,
            category=f"Category {i % 5}",
            tags=[f"tag{j}" for j in range(i % 4)],
            due_date=datetime.now() + timedelta(days=i),
            reminder=datetime.now() + timedelta(hours=i),
        )
        if i % 2 == 0:
            task.complete()
        tasks.append(task)
    return tasks


def test_save_performance(temp_storage):
    """Test performance of saving tasks."""
    # Generate test data
    task_counts = [10, 100, 1000]
    results = {}

    for count in task_counts:
        tasks = generate_test_tasks(count)
        
        # Measure save time
        start_time = time.time()
        temp_storage.save_tasks(tasks)
        end_time = time.time()
        
        save_time = end_time - start_time
        results[count] = save_time
        
        # Verify data was saved correctly
        loaded_tasks = temp_storage.load_tasks()
        assert len(loaded_tasks) == count

    # Print results
    print("\nSave Performance Results:")
    for count, time_taken in results.items():
        print(f"{count} tasks: {time_taken:.3f} seconds")


def test_load_performance(temp_storage):
    """Test performance of loading tasks."""
    # Generate and save test data
    task_counts = [10, 100, 1000]
    results = {}

    for count in task_counts:
        tasks = generate_test_tasks(count)
        temp_storage.save_tasks(tasks)
        
        # Measure load time
        start_time = time.time()
        loaded_tasks = temp_storage.load_tasks()
        end_time = time.time()
        
        load_time = end_time - start_time
        results[count] = load_time
        
        # Verify data was loaded correctly
        assert len(loaded_tasks) == count

    # Print results
    print("\nLoad Performance Results:")
    for count, time_taken in results.items():
        print(f"{count} tasks: {time_taken:.3f} seconds")


def test_export_import_performance(temp_storage):
    """Test performance of export and import operations."""
    # Generate test data
    task_counts = [10, 100, 1000]
    results = {}

    for count in task_counts:
        tasks = generate_test_tasks(count)
        temp_storage.save_tasks(tasks)
        
        # Test JSON export/import
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            export_file = Path(f.name)
        
        # Measure JSON export time
        start_time = time.time()
        temp_storage.export_to_json(export_file)
        json_export_time = time.time() - start_time
        
        # Measure JSON import time
        start_time = time.time()
        imported_tasks = temp_storage.import_from_json(export_file)
        json_import_time = time.time() - start_time
        
        # Test CSV export/import
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            export_file = Path(f.name)
        
        # Measure CSV export time
        start_time = time.time()
        temp_storage.export_to_csv(export_file)
        csv_export_time = time.time() - start_time
        
        # Measure CSV import time
        start_time = time.time()
        imported_tasks = temp_storage.import_from_csv(export_file)
        csv_import_time = time.time() - start_time
        
        results[count] = {
            "json_export": json_export_time,
            "json_import": json_import_time,
            "csv_export": csv_export_time,
            "csv_import": csv_import_time,
        }
        
        # Clean up
        export_file.unlink()

    # Print results
    print("\nExport/Import Performance Results:")
    for count, times in results.items():
        print(f"\n{count} tasks:")
        print(f"  JSON Export: {times['json_export']:.3f} seconds")
        print(f"  JSON Import: {times['json_import']:.3f} seconds")
        print(f"  CSV Export:  {times['csv_export']:.3f} seconds")
        print(f"  CSV Import:  {times['csv_import']:.3f} seconds")


def test_concurrent_operations(temp_storage):
    """Test performance of concurrent operations."""
    # Generate test data
    tasks = generate_test_tasks(100)
    temp_storage.save_tasks(tasks)
    
    # Measure time for multiple operations
    start_time = time.time()
    
    # Perform multiple operations
    for _ in range(10):
        # Load tasks
        loaded_tasks = temp_storage.load_tasks()
        
        # Modify some tasks
        for task in loaded_tasks[:10]:
            task.complete()
        
        # Save tasks
        temp_storage.save_tasks(loaded_tasks)
        
        # Export to JSON
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            export_file = Path(f.name)
        temp_storage.export_to_json(export_file)
        export_file.unlink()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nConcurrent Operations Performance:")
    print(f"10 iterations of load-modify-save-export: {total_time:.3f} seconds")
    print(f"Average time per iteration: {total_time/10:.3f} seconds") 