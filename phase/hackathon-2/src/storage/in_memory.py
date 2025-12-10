"""In-memory task repository implementation.

This implementation uses a dictionary for storage and maintains
ID sequence integrity (no ID reuse after deletion).
"""

from src.models.exceptions import EmptyTitleError, NotFoundError
from src.models.task import Task, TaskStatus


class InMemoryTaskRepository:
    """In-memory implementation of TaskRepositoryProtocol.

    Uses dict for storage with auto-increment ID tracking.
    IDs are never reused, even after deletion.
    """

    def __init__(self) -> None:
        """Initialize empty repository with ID tracking."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        """Add new task with auto-generated ID.

        Args:
            task: Task instance without ID assigned (id=0)

        Returns:
            Task instance with ID assigned

        Raises:
            EmptyTitleError: If task title is empty or whitespace-only
        """
        # Validate title is not empty
        if not task.title or not task.title.strip():
            raise EmptyTitleError()

        # Assign new ID
        task.id = self._next_id
        self._next_id += 1

        # Store task
        self._tasks[task.id] = task

        return task

    def get_all(self) -> list[Task]:
        """Retrieve all tasks sorted by ID (ascending).

        Returns:
            List of all tasks (empty list if none exist)
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get_by_id(self, task_id: int) -> Task | None:
        """Retrieve specific task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task instance if found, None otherwise
        """
        return self._tasks.get(task_id)

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
            EmptyTitleError: If new title is empty
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise NotFoundError(task_id)

        # Update title if provided
        if title is not None:
            if not title.strip():
                raise EmptyTitleError()
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description

        return task

    def delete(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Task to delete

        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_status(self, task_id: int) -> Task:
        """Toggle task between PENDING and COMPLETED.

        Args:
            task_id: Task to toggle

        Returns:
            Updated task instance

        Raises:
            NotFoundError: If task_id doesn't exist
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise NotFoundError(task_id)

        # Toggle status
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.COMPLETED
        else:
            task.status = TaskStatus.PENDING

        return task
