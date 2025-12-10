"""Pytest fixtures for testing."""

import pytest

from src.models.task import Task, TaskStatus
from src.storage.in_memory import InMemoryTaskRepository


@pytest.fixture
def repository() -> InMemoryTaskRepository:
    """Create a fresh in-memory repository for each test.

    Returns:
        Empty InMemoryTaskRepository instance
    """
    return InMemoryTaskRepository()


@pytest.fixture
def sample_task() -> Task:
    """Create a sample pending task (no ID assigned).

    Returns:
        Task with title, description, and PENDING status
    """
    return Task(title="Buy groceries", description="Milk, eggs, bread", status=TaskStatus.PENDING)


@pytest.fixture
def sample_task_minimal() -> Task:
    """Create a minimal task with only title (no ID assigned).

    Returns:
        Task with title only, empty description
    """
    return Task(title="Call dentist", description="", status=TaskStatus.PENDING)


@pytest.fixture
def sample_completed_task() -> Task:
    """Create a sample completed task (no ID assigned).

    Returns:
        Task with COMPLETED status
    """
    return Task(
        title="Finish report", description="Q4 analysis", status=TaskStatus.COMPLETED
    )


@pytest.fixture
def populated_repository(
    repository: InMemoryTaskRepository, sample_task: Task, sample_task_minimal: Task
) -> InMemoryTaskRepository:
    """Create repository with sample tasks.

    Args:
        repository: Empty repository fixture
        sample_task: Sample task fixture
        sample_task_minimal: Minimal task fixture

    Returns:
        Repository with 2 tasks added (IDs 1 and 2)
    """
    repository.add(sample_task)
    repository.add(sample_task_minimal)
    return repository
