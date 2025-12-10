"""Task service layer - business logic for task operations.

This service layer sits between the UI and repository,
providing a clean interface for task operations.
"""

from src.models.exceptions import EmptyTitleError, NotFoundError
from src.models.task import Task
from src.storage.protocol import TaskRepositoryProtocol


class TaskService:
    """Service for task operations.

    Handles business logic and validation before delegating
    to repository layer.
    """

    def __init__(self, repository: TaskRepositoryProtocol) -> None:
        """Initialize service with repository dependency.

        Args:
            repository: Repository implementation for task storage
        """
        self._repository = repository

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with validation.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)

        Returns:
            Created task with assigned ID

        Raises:
            EmptyTitleError: If title is empty or whitespace-only
        """
        # Validate title
        if not title or not title.strip():
            raise EmptyTitleError()

        # Create task instance
        task = Task(title=title.strip(), description=description)

        # Delegate to repository
        return self._repository.add(task)

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks in sorted order.

        Returns:
            List of all tasks sorted by ID (empty list if none exist)
        """
        return self._repository.get_all()

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve specific task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task instance if found, None otherwise
        """
        return self._repository.get_by_id(task_id)

    def update_task(
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
            EmptyTitleError: If new title is empty
        """
        # Validate title if provided
        if title is not None and not title.strip():
            raise EmptyTitleError()

        return self._repository.update(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Task to delete

        Returns:
            True if deleted, False if not found

        Raises:
            NotFoundError: If strict validation is needed (not implemented yet)
        """
        deleted = self._repository.delete(task_id)
        if not deleted:
            raise NotFoundError(task_id)
        return deleted

    def toggle_task_status(self, task_id: int) -> Task:
        """Toggle task between PENDING and COMPLETED.

        Args:
            task_id: Task to toggle

        Returns:
            Updated task instance

        Raises:
            NotFoundError: If task_id doesn't exist
        """
        return self._repository.toggle_status(task_id)
