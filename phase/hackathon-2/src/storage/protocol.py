"""Repository protocol defining storage interface."""

from typing import Protocol

from src.models.task import Task


class TaskRepositoryProtocol(Protocol):
    """Protocol for task storage operations.

    Defines the contract that all repository implementations must follow.
    Enables Phase I (in-memory) to Phase II (PostgreSQL) swap without
    changing business logic.
    """

    def add(self, task: Task) -> Task:
        """Add new task with auto-generated ID.

        Args:
            task: Task instance without ID assigned

        Returns:
            Task instance with ID assigned

        Raises:
            ValidationError: If task data is invalid
        """
        ...

    def get_all(self) -> list[Task]:
        """Retrieve all tasks sorted by ID (ascending).

        Returns:
            List of all tasks (empty list if none exist)
        """
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve specific task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task instance if found, None otherwise
        """
        ...

    def update(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task:
        """Update task title and/or description.

        Args:
            task_id: Task to update
            title: New title (None = no change)
            description: New description (None = no change)

        Returns:
            Updated task instance

        Raises:
            NotFoundError: If task_id doesn't exist
            ValidationError: If title is empty
        """
        ...

    def delete(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Task to delete

        Returns:
            True if deleted, False if not found
        """
        ...

    def toggle_status(self, task_id: int) -> Task:
        """Toggle task between PENDING and COMPLETED.

        Args:
            task_id: Task to toggle

        Returns:
            Updated task instance

        Raises:
            NotFoundError: If task_id doesn't exist
        """
        ...
