"""Unit tests for repository layer."""

import pytest
from pydantic import ValidationError as PydanticValidationError

from src.models.exceptions import EmptyTitleError, NotFoundError
from src.models.task import Task, TaskStatus
from src.storage.in_memory import InMemoryTaskRepository


class TestInMemoryTaskRepository:
    """Test InMemoryTaskRepository implementation."""

    def test_add_assigns_sequential_ids(self) -> None:
        """Verify add() assigns sequential IDs starting from 1."""
        repository = InMemoryTaskRepository()

        task1 = Task(title="First task")
        task2 = Task(title="Second task")

        saved1 = repository.add(task1)
        saved2 = repository.add(task2)

        assert saved1.id == 1
        assert saved2.id == 2

    def test_add_validates_empty_title(self) -> None:
        """Verify empty titles are rejected (by Pydantic validation)."""
        repository = InMemoryTaskRepository()

        # Pydantic validates at model level, so we catch that error
        with pytest.raises(PydanticValidationError):
            repository.add(Task(title=""))

    def test_get_all_returns_sorted_by_id(self) -> None:
        """Verify get_all() returns tasks sorted by ID ascending."""
        repository = InMemoryTaskRepository()

        repository.add(Task(title="Task 1"))
        repository.add(Task(title="Task 2"))
        repository.add(Task(title="Task 3"))

        all_tasks = repository.get_all()

        assert len(all_tasks) == 3
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2
        assert all_tasks[2].id == 3

    def test_get_all_empty_repository(self) -> None:
        """Verify get_all() returns empty list for empty repository."""
        repository = InMemoryTaskRepository()
        assert repository.get_all() == []

    def test_get_by_id_existing(self) -> None:
        """Verify get_by_id() returns task when it exists."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Test task"))

        retrieved = repository.get_by_id(task.id)

        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.title == task.title

    def test_get_by_id_not_found(self) -> None:
        """Verify get_by_id() returns None when task doesn't exist."""
        repository = InMemoryTaskRepository()
        assert repository.get_by_id(999) is None

    def test_toggle_pending_to_completed(self) -> None:
        """Verify toggle_status() changes PENDING to COMPLETED."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Test task", status=TaskStatus.PENDING))

        toggled = repository.toggle_status(task.id)

        assert toggled.status == TaskStatus.COMPLETED
        assert toggled.id == task.id

    def test_toggle_completed_to_pending(self) -> None:
        """Verify toggle_status() changes COMPLETED to PENDING."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Test task"))
        repository.toggle_status(task.id)  # PENDING -> COMPLETED

        toggled_again = repository.toggle_status(task.id)  # COMPLETED -> PENDING

        assert toggled_again.status == TaskStatus.PENDING

    def test_toggle_not_found_error(self) -> None:
        """Verify toggle_status() raises NotFoundError for non-existent ID."""
        repository = InMemoryTaskRepository()

        with pytest.raises(NotFoundError) as exc_info:
            repository.toggle_status(999)

        assert exc_info.value.task_id == 999

    def test_update_title(self) -> None:
        """Verify update() changes title when provided."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Old title", description="Description"))

        updated = repository.update(task.id, title="New title")

        assert updated.title == "New title"
        assert updated.description == "Description"  # Unchanged
        assert updated.id == task.id

    def test_update_description(self) -> None:
        """Verify update() changes description when provided."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Title", description="Old description"))

        updated = repository.update(task.id, description="New description")

        assert updated.title == "Title"  # Unchanged
        assert updated.description == "New description"
        assert updated.id == task.id

    def test_update_both(self) -> None:
        """Verify update() changes both title and description."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Old title", description="Old description"))

        updated = repository.update(task.id, title="New title", description="New description")

        assert updated.title == "New title"
        assert updated.description == "New description"
        assert updated.id == task.id

    def test_update_not_found_error(self) -> None:
        """Verify update() raises NotFoundError for non-existent ID."""
        repository = InMemoryTaskRepository()

        with pytest.raises(NotFoundError) as exc_info:
            repository.update(999, title="New title")

        assert exc_info.value.task_id == 999

    def test_update_empty_title_error(self) -> None:
        """Verify update() raises EmptyTitleError for empty title."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Valid title"))

        with pytest.raises(EmptyTitleError):
            repository.update(task.id, title="")

    def test_update_preserves_status(self) -> None:
        """Verify update() preserves task status."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Task"))
        repository.toggle_status(task.id)  # Set to COMPLETED

        updated = repository.update(task.id, title="Updated title")

        assert updated.status == TaskStatus.COMPLETED  # Status preserved

    def test_delete_existing(self) -> None:
        """Verify delete() removes task and returns True."""
        repository = InMemoryTaskRepository()
        task = repository.add(Task(title="Task to delete"))

        deleted = repository.delete(task.id)

        assert deleted is True
        assert repository.get_by_id(task.id) is None

    def test_delete_not_found(self) -> None:
        """Verify delete() returns False for non-existent ID."""
        repository = InMemoryTaskRepository()

        deleted = repository.delete(999)

        assert deleted is False

    def test_id_sequence_after_delete(self) -> None:
        """Verify ID sequence continues after deletion (no ID reuse)."""
        repository = InMemoryTaskRepository()

        repository.add(Task(title="Task 1"))
        task2 = repository.add(Task(title="Task 2"))
        repository.add(Task(title="Task 3"))

        # Delete middle task
        repository.delete(task2.id)

        # Add new task - should get ID 4, not 2
        task4 = repository.add(Task(title="Task 4"))

        assert task4.id == 4  # ID sequence continues, no reuse
        assert repository.get_by_id(2) is None  # ID 2 is gone
