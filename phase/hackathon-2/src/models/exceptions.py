"""Custom exceptions for todo application."""


class TodoAppError(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str) -> None:
        """Initialize exception with user-friendly message.

        Args:
            message: User-friendly error description with actionable guidance
        """
        self.message = message
        super().__init__(self.message)


class ValidationError(TodoAppError):
    """Input validation failure."""

    pass


class EmptyTitleError(ValidationError):
    """Title is empty or whitespace-only."""

    def __init__(self) -> None:
        """Initialize with predefined user-friendly message."""
        super().__init__("Title cannot be empty. Please provide a title for your task.")


class InvalidIDError(ValidationError):
    """ID format is not numeric."""

    def __init__(self) -> None:
        """Initialize with predefined user-friendly message."""
        super().__init__("Invalid ID format. Please enter a numeric ID (e.g., 1, 2, 3).")


class NotFoundError(TodoAppError):
    """Resource (task) doesn't exist."""

    def __init__(self, task_id: int) -> None:
        """Initialize with task ID in message.

        Args:
            task_id: The ID that wasn't found
        """
        self.task_id = task_id
        super().__init__(
            f"Task with ID {task_id} not found. Please check the ID and try again."
        )


class RepositoryError(TodoAppError):
    """Storage layer failure."""

    pass
