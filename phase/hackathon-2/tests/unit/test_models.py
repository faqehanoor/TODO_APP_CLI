"""Unit tests for Task model and TaskStatus enum."""

import pytest
from pydantic import ValidationError as PydanticValidationError

from src.models.task import Task, TaskStatus


class TestTaskStatus:
    """Test TaskStatus enum values and behavior."""

    def test_status_values(self) -> None:
        """Verify TaskStatus has PENDING and COMPLETED values."""
        assert TaskStatus.PENDING == "PENDING"
        assert TaskStatus.COMPLETED == "COMPLETED"

    def test_default_pending(self) -> None:
        """Verify default status is PENDING when not specified."""
        task = Task(title="Test task")
        assert task.status == TaskStatus.PENDING


class TestTaskModel:
    """Test Task model validation and behavior."""

    def test_task_creation(self) -> None:
        """Verify task creation with valid data."""
        task = Task(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            status=TaskStatus.PENDING,
        )
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == TaskStatus.PENDING

    def test_task_creation_minimal(self) -> None:
        """Verify task creation with only title (minimal required data)."""
        task = Task(title="Call dentist")
        assert task.id == 0  # Default value before repository assigns ID
        assert task.title == "Call dentist"
        assert task.description == ""  # Default empty description
        assert task.status == TaskStatus.PENDING  # Default status

    def test_empty_title_rejected(self) -> None:
        """Verify empty title raises validation error."""
        with pytest.raises(PydanticValidationError) as exc_info:
            Task(title="")

        # Verify the error is about title validation
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_whitespace_title_rejected(self) -> None:
        """Verify whitespace-only title raises validation error."""
        with pytest.raises(PydanticValidationError) as exc_info:
            Task(title="   ")

        # Verify the error is about title validation
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_title_trimmed(self) -> None:
        """Verify title is automatically trimmed of leading/trailing whitespace."""
        task = Task(title="  Buy groceries  ")
        assert task.title == "Buy groceries"

    def test_title_max_length(self) -> None:
        """Verify title respects max length of 200 characters."""
        valid_title = "a" * 200
        task = Task(title=valid_title)
        assert task.title == valid_title

        # Title exceeding 200 characters should raise error
        invalid_title = "a" * 201
        with pytest.raises(PydanticValidationError) as exc_info:
            Task(title=invalid_title)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_description_max_length(self) -> None:
        """Verify description respects max length of 1000 characters."""
        valid_description = "a" * 1000
        task = Task(title="Test", description=valid_description)
        assert task.description == valid_description

        # Description exceeding 1000 characters should raise error
        invalid_description = "a" * 1001
        with pytest.raises(PydanticValidationError) as exc_info:
            Task(title="Test", description=invalid_description)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("description",) for error in errors)

    def test_id_must_be_positive(self) -> None:
        """Verify ID must be >= 1 when assigned."""
        # ID of 0 is allowed (default before repository assigns ID)
        task = Task(title="Test")
        assert task.id == 0

        # Positive IDs should work
        task = Task(id=1, title="Test")
        assert task.id == 1

        # Negative IDs should raise error
        with pytest.raises(PydanticValidationError) as exc_info:
            Task(id=-1, title="Test")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("id",) for error in errors)

    def test_status_enum_values(self) -> None:
        """Verify only valid TaskStatus enum values are accepted."""
        task_pending = Task(title="Test", status=TaskStatus.PENDING)
        assert task_pending.status == TaskStatus.PENDING

        task_completed = Task(title="Test", status=TaskStatus.COMPLETED)
        assert task_completed.status == TaskStatus.COMPLETED
