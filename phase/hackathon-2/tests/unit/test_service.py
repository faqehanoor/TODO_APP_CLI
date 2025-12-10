"""Unit tests for service layer."""

import pytest

from src.models.exceptions import EmptyTitleError, NotFoundError
from src.models.task import TaskStatus
from src.services.task_service import TaskService
from src.storage.in_memory import InMemoryTaskRepository


class TestTaskService:
    """Test TaskService business logic."""

    def test_create_task_success(self) -> None:
        """Verify create_task() creates task with valid data."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Buy groceries", description="Milk, eggs")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs"
        assert task.status == TaskStatus.PENDING

    def test_create_task_trims_title(self) -> None:
        """Verify create_task() trims whitespace from title."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="  Buy groceries  ")

        assert task.title == "Buy groceries"

    def test_create_task_empty_title_error(self) -> None:
        """Verify create_task() rejects empty title."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        with pytest.raises(EmptyTitleError):
            service.create_task(title="")

    def test_create_task_whitespace_title_error(self) -> None:
        """Verify create_task() rejects whitespace-only title."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        with pytest.raises(EmptyTitleError):
            service.create_task(title="   ")

    def test_list_tasks_returns_all(self) -> None:
        """Verify list_tasks() returns all tasks."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        service.create_task(title="Task 1")
        service.create_task(title="Task 2")

        tasks = service.list_tasks()

        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_list_tasks_empty(self) -> None:
        """Verify list_tasks() returns empty list when no tasks."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        tasks = service.list_tasks()

        assert tasks == []

    def test_get_task_success(self) -> None:
        """Verify get_task() retrieves existing task."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        created = service.create_task(title="Test task")
        retrieved = service.get_task(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_task_not_found(self) -> None:
        """Verify get_task() returns None for non-existent ID."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.get_task(999)

        assert task is None

    def test_toggle_not_found_error(self) -> None:
        """Verify toggle_task_status() raises NotFoundError for non-existent ID."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        with pytest.raises(NotFoundError) as exc_info:
            service.toggle_task_status(999)

        assert exc_info.value.task_id == 999

    def test_toggle_task_status_pending_to_completed(self) -> None:
        """Verify toggle_task_status() changes PENDING to COMPLETED."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Test task")
        toggled = service.toggle_task_status(task.id)

        assert toggled.status == TaskStatus.COMPLETED

    def test_toggle_task_status_completed_to_pending(self) -> None:
        """Verify toggle_task_status() changes COMPLETED back to PENDING."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Test task")
        service.toggle_task_status(task.id)  # PENDING -> COMPLETED
        toggled_again = service.toggle_task_status(task.id)  # COMPLETED -> PENDING

        assert toggled_again.status == TaskStatus.PENDING

    def test_update_empty_title_error(self) -> None:
        """Verify update_task() raises EmptyTitleError for empty title."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Original title")

        with pytest.raises(EmptyTitleError):
            service.update_task(task.id, title="")

    def test_update_preserves_status(self) -> None:
        """Verify update_task() preserves status when updating."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Original title")
        service.toggle_task_status(task.id)  # Set to COMPLETED

        updated = service.update_task(task.id, title="New title")

        assert updated.status == TaskStatus.COMPLETED  # Status preserved
        assert updated.title == "New title"

    def test_update_task_title_only(self) -> None:
        """Verify update_task() updates only title when specified."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Old title", description="Old description")
        updated = service.update_task(task.id, title="New title")

        assert updated.title == "New title"
        assert updated.description == "Old description"  # Unchanged

    def test_update_task_description_only(self) -> None:
        """Verify update_task() updates only description when specified."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Title", description="Old description")
        updated = service.update_task(task.id, description="New description")

        assert updated.title == "Title"  # Unchanged
        assert updated.description == "New description"

    def test_update_task_both_fields(self) -> None:
        """Verify update_task() updates both title and description."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Old title", description="Old description")
        updated = service.update_task(
            task.id, title="New title", description="New description"
        )

        assert updated.title == "New title"
        assert updated.description == "New description"

    def test_update_task_not_found_error(self) -> None:
        """Verify update_task() raises NotFoundError for non-existent ID."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        with pytest.raises(NotFoundError) as exc_info:
            service.update_task(999, title="New title")

        assert exc_info.value.task_id == 999

    def test_delete_task_success(self) -> None:
        """Verify delete_task() deletes existing task."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        task = service.create_task(title="Task to delete")
        deleted = service.delete_task(task.id)

        assert deleted is True
        assert service.get_task(task.id) is None

    def test_delete_not_found_error(self) -> None:
        """Verify delete_task() raises NotFoundError for non-existent ID."""
        repository = InMemoryTaskRepository()
        service = TaskService(repository)

        with pytest.raises(NotFoundError) as exc_info:
            service.delete_task(999)

        assert exc_info.value.task_id == 999
