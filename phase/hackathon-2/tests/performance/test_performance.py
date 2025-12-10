"""Performance tests for todo application.

Tests verify performance requirements from spec.md:
- SC-002: List 1000 tasks in <1 second
- SC-007: All CRUD operations complete in <1 second
"""

import time

from src.services.task_service import TaskService
from src.storage.in_memory import InMemoryTaskRepository


class TestPerformance:
    """Performance tests for CRUD operations."""

    def test_list_1000_tasks_under_1_second(self) -> None:
        """Verify listing 1000 tasks completes in <1 second (SC-002)."""
        # Setup: Create repository with 1000 tasks
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        for i in range(1000):
            service.create_task(title=f"Task {i}", description=f"Description {i}")

        # Performance test: List all tasks
        start_time = time.perf_counter()
        tasks = service.list_tasks()
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        # Verify performance requirement
        assert len(tasks) == 1000
        assert elapsed_time < 1.0, f"List operation took {elapsed_time:.3f}s (should be <1s)"

    def test_create_operation_under_1_second(self) -> None:
        """Verify create operation completes in <1 second (SC-007)."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        start_time = time.perf_counter()
        task = service.create_task(title="Performance test task", description="Test description")
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        assert task.id == 1
        assert elapsed_time < 1.0, f"Create operation took {elapsed_time:.3f}s (should be <1s)"

    def test_read_operation_under_1_second(self) -> None:
        """Verify read operation completes in <1 second (SC-007)."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        # Setup: Create tasks
        for i in range(100):
            service.create_task(title=f"Task {i}")

        start_time = time.perf_counter()
        task = service.get_task(50)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        assert task is not None
        assert elapsed_time < 1.0, f"Read operation took {elapsed_time:.3f}s (should be <1s)"

    def test_update_operation_under_1_second(self) -> None:
        """Verify update operation completes in <1 second (SC-007)."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        # Setup: Create task
        task = service.create_task(title="Original title")

        start_time = time.perf_counter()
        updated_task = service.update_task(task.id, title="Updated title")
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        assert updated_task.title == "Updated title"
        assert elapsed_time < 1.0, f"Update operation took {elapsed_time:.3f}s (should be <1s)"

    def test_delete_operation_under_1_second(self) -> None:
        """Verify delete operation completes in <1 second (SC-007)."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        # Setup: Create task
        task = service.create_task(title="Task to delete")

        start_time = time.perf_counter()
        deleted = service.delete_task(task.id)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        assert deleted is True
        assert elapsed_time < 1.0, f"Delete operation took {elapsed_time:.3f}s (should be <1s)"

    def test_toggle_status_operation_under_1_second(self) -> None:
        """Verify toggle status operation completes in <1 second (SC-007)."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        # Setup: Create task
        task = service.create_task(title="Task to toggle")

        start_time = time.perf_counter()
        toggled_task = service.toggle_task_status(task.id)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        assert toggled_task.status.value == "COMPLETED"
        assert elapsed_time < 1.0, f"Toggle operation took {elapsed_time:.3f}s (should be <1s)"

    def test_bulk_operations_performance(self) -> None:
        """Verify bulk create, update, delete operations are performant."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        # Create 500 tasks
        start_time = time.perf_counter()
        for i in range(500):
            service.create_task(title=f"Task {i}")
        create_time = time.perf_counter() - start_time

        # Update 100 tasks
        start_time = time.perf_counter()
        for i in range(1, 101):
            service.update_task(i, title=f"Updated Task {i}")
        update_time = time.perf_counter() - start_time

        # Delete 50 tasks
        start_time = time.perf_counter()
        for i in range(1, 51):
            service.delete_task(i)
        delete_time = time.perf_counter() - start_time

        # Verify all operations complete in reasonable time
        assert create_time < 5.0, f"Creating 500 tasks took {create_time:.3f}s (should be <5s)"
        assert update_time < 2.0, f"Updating 100 tasks took {update_time:.3f}s (should be <2s)"
        assert delete_time < 2.0, f"Deleting 50 tasks took {delete_time:.3f}s (should be <2s)"

        # Verify final state
        remaining_tasks = service.list_tasks()
        assert len(remaining_tasks) == 450  # 500 - 50 deleted
