"""Integration tests for user stories - end-to-end flows."""


from src.models.task import Task, TaskStatus
from src.storage.in_memory import InMemoryTaskRepository


class TestUserStory1:
    """Test User Story 1: Create & View Tasks."""

    def test_create_and_view_tasks(self) -> None:
        """Test creating multiple tasks and viewing them in sorted order.

        User Story: As a user, I want to add tasks with titles and descriptions
        and view them in a formatted list.
        """
        # Given: An empty repository
        repository = InMemoryTaskRepository()

        # When: User creates multiple tasks
        task1 = Task(title="Buy groceries", description="Milk, eggs, bread")
        task2 = Task(title="Call dentist", description="Schedule checkup")
        task3 = Task(title="Finish report", description="Q4 analysis")

        saved_task1 = repository.add(task1)
        saved_task2 = repository.add(task2)
        saved_task3 = repository.add(task3)

        # Then: Tasks are assigned sequential IDs
        assert saved_task1.id == 1
        assert saved_task2.id == 2
        assert saved_task3.id == 3

        # And: All tasks are returned in sorted order (by ID ascending)
        all_tasks = repository.get_all()
        assert len(all_tasks) == 3
        assert all_tasks[0].id == 1
        assert all_tasks[0].title == "Buy groceries"
        assert all_tasks[1].id == 2
        assert all_tasks[1].title == "Call dentist"
        assert all_tasks[2].id == 3
        assert all_tasks[2].title == "Finish report"

        # And: All tasks have default PENDING status
        assert all(task.status == TaskStatus.PENDING for task in all_tasks)

    def test_list_empty_tasks(self) -> None:
        """Test viewing tasks when repository is empty.

        User Story: As a user, I want to see a friendly message when no tasks exist.
        """
        # Given: An empty repository
        repository = InMemoryTaskRepository()

        # When: User lists all tasks
        all_tasks = repository.get_all()

        # Then: Empty list is returned (no errors)
        assert all_tasks == []
        assert len(all_tasks) == 0


class TestUserStory2:
    """Test User Story 2: Mark Tasks Complete."""

    def test_mark_tasks_complete(self) -> None:
        """Test toggling task status between PENDING and COMPLETED.

        User Story: As a user, I want to mark tasks as complete/incomplete
        to track my progress.
        """
        # Given: Repository with pending tasks
        repository = InMemoryTaskRepository()
        task = Task(title="Buy groceries", description="Milk, eggs, bread")
        saved_task = repository.add(task)
        assert saved_task.status == TaskStatus.PENDING

        # When: User toggles task to COMPLETED
        toggled_task = repository.toggle_status(saved_task.id)

        # Then: Task status is COMPLETED
        assert toggled_task.status == TaskStatus.COMPLETED
        assert toggled_task.id == saved_task.id
        assert toggled_task.title == saved_task.title

        # When: User toggles task again (back to PENDING)
        toggled_again = repository.toggle_status(saved_task.id)

        # Then: Task status is PENDING again
        assert toggled_again.status == TaskStatus.PENDING


class TestUserStory3:
    """Test User Story 3: Update Task Details."""

    def test_update_task_details(self) -> None:
        """Test updating task title and/or description.

        User Story: As a user, I want to update task details to reflect changes
        while preserving ID and status.
        """
        # Given: Repository with existing task
        repository = InMemoryTaskRepository()
        task = Task(title="Buy groceries", description="Milk, eggs")
        saved_task = repository.add(task)
        original_id = saved_task.id
        original_status = saved_task.status

        # When: User updates only title
        updated_task = repository.update(saved_task.id, title="Buy groceries and pharmacy")

        # Then: Title is updated, description and ID/status preserved
        assert updated_task.id == original_id
        assert updated_task.title == "Buy groceries and pharmacy"
        assert updated_task.description == "Milk, eggs"  # Unchanged
        assert updated_task.status == original_status

        # When: User updates only description
        updated_task2 = repository.update(saved_task.id, description="Milk, eggs, bread, medicine")

        # Then: Description is updated, title and ID/status preserved
        assert updated_task2.id == original_id
        assert updated_task2.title == "Buy groceries and pharmacy"  # From previous update
        assert updated_task2.description == "Milk, eggs, bread, medicine"
        assert updated_task2.status == original_status

        # When: User updates both title and description
        updated_task3 = repository.update(
            saved_task.id,
            title="Weekend shopping",
            description="Complete grocery list",
        )

        # Then: Both are updated, ID/status preserved
        assert updated_task3.id == original_id
        assert updated_task3.title == "Weekend shopping"
        assert updated_task3.description == "Complete grocery list"
        assert updated_task3.status == original_status


class TestUserStory4:
    """Test User Story 4: Remove Unwanted Tasks."""

    def test_remove_unwanted_tasks(self) -> None:
        """Test deleting tasks by ID with ID sequence integrity.

        User Story: As a user, I want to delete tasks I no longer need
        while maintaining ID sequence (no ID reuse).
        """
        # Given: Repository with multiple tasks
        repository = InMemoryTaskRepository()
        task1 = repository.add(Task(title="Task 1"))
        task2 = repository.add(Task(title="Task 2"))
        task3 = repository.add(Task(title="Task 3"))

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

        # When: User deletes middle task (ID 2)
        deleted = repository.delete(task2.id)

        # Then: Deletion succeeds
        assert deleted is True

        # And: Remaining tasks are intact
        all_tasks = repository.get_all()
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 3

        # When: User adds a new task after deletion
        task4 = repository.add(Task(title="Task 4"))

        # Then: New task gets next ID in sequence (4, not 2 - no ID reuse)
        assert task4.id == 4

        # When: User tries to delete non-existent task
        deleted_missing = repository.delete(999)

        # Then: Deletion returns False (not found, no error)
        assert deleted_missing is False
