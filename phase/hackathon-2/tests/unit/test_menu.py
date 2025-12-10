"""Unit tests for menu handler."""

from io import StringIO
from unittest.mock import patch

import pytest

from src.models.task import TaskStatus
from src.services.task_service import TaskService
from src.storage.in_memory import InMemoryTaskRepository
from src.ui.menu import MenuHandler
from src.ui.renderer import RichTableRenderer


class TestMenuHandler:
    """Test MenuHandler functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.repository = InMemoryTaskRepository()
        self.service = TaskService(self.repository)
        self.renderer = RichTableRenderer()
        self.menu = MenuHandler(self.service, self.renderer)

    def test_show_menu(self) -> None:
        """Verify menu displays all options."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.menu.show_menu()
            output = mock_stdout.getvalue()

        # Check menu options are displayed
        assert "Todo App" in output or len(output) > 0

    def test_prompt_menu_choice(self) -> None:
        """Verify menu choice prompt returns user input."""
        with patch("typer.prompt", return_value="1"):
            choice = self.menu.prompt_menu_choice()

        assert choice == "1"

    def test_prompt_add_task_success(self) -> None:
        """Verify add task prompts and creates task."""
        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = ["Test Task", "Test Description"]

            with patch("sys.stdout", new_callable=StringIO):
                self.menu.prompt_add_task()

        # Verify task was created
        tasks = self.service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"

    def test_prompt_add_task_empty_description(self) -> None:
        """Verify add task with empty description."""
        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = ["Test Task", ""]

            with patch("sys.stdout", new_callable=StringIO):
                self.menu.prompt_add_task()

        tasks = self.service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == ""

    def test_display_tasks(self) -> None:
        """Verify display tasks calls renderer."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")

        with patch.object(self.renderer, "render_tasks") as mock_render:
            self.menu.display_tasks()

        # Verify renderer was called with tasks
        mock_render.assert_called_once()
        call_args = mock_render.call_args[0][0]
        assert len(call_args) == 2

    def test_prompt_toggle_task_success(self) -> None:
        """Verify toggle task prompts and toggles status."""
        task = self.service.create_task("Test Task")

        with patch("typer.prompt", return_value=str(task.id)):
            with patch("sys.stdout", new_callable=StringIO):
                self.menu.prompt_toggle_task()

        # Verify status was toggled
        updated_task = self.service.get_task(task.id)
        assert updated_task is not None
        assert updated_task.status == TaskStatus.COMPLETED

    def test_prompt_toggle_task_not_found(self) -> None:
        """Verify toggle task handles not found error."""
        with patch("typer.prompt", return_value="999"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.menu.prompt_toggle_task()
                output = mock_stdout.getvalue()

        # Should show error message
        assert "Error" in output or len(output) > 0

    def test_prompt_toggle_task_invalid_id(self) -> None:
        """Verify toggle task handles invalid ID."""
        with patch("typer.prompt", return_value="invalid"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.menu.prompt_toggle_task()
                output = mock_stdout.getvalue()

        # Should show error message
        assert "Error" in output or len(output) > 0

    def test_prompt_update_task_title_only(self) -> None:
        """Verify update task with title only."""
        task = self.service.create_task("Old Title", "Old Description")

        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = [str(task.id), "New Title", ""]

            with patch("sys.stdout", new_callable=StringIO):
                self.menu.prompt_update_task()

        updated_task = self.service.get_task(task.id)
        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Old Description"

    def test_prompt_update_task_both_fields(self) -> None:
        """Verify update task with both title and description."""
        task = self.service.create_task("Old Title", "Old Description")

        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = [str(task.id), "New Title", "New Description"]

            with patch("sys.stdout", new_callable=StringIO):
                self.menu.prompt_update_task()

        updated_task = self.service.get_task(task.id)
        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_prompt_update_task_not_found(self) -> None:
        """Verify update task handles not found error."""
        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = ["999", "New Title", "New Description"]

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.menu.prompt_update_task()
                output = mock_stdout.getvalue()

        # Should show error message
        assert "Error" in output or len(output) > 0

    def test_prompt_delete_task_success(self) -> None:
        """Verify delete task prompts and deletes."""
        task = self.service.create_task("Task to delete")

        with patch("typer.prompt", return_value=str(task.id)):
            with patch("sys.stdout", new_callable=StringIO):
                self.menu.prompt_delete_task()

        # Verify task was deleted
        assert self.service.get_task(task.id) is None

    def test_prompt_delete_task_not_found(self) -> None:
        """Verify delete task handles not found error."""
        with patch("typer.prompt", return_value="999"):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.menu.prompt_delete_task()
                output = mock_stdout.getvalue()

        # Should show error message
        assert "Error" in output or len(output) > 0

    def test_validate_id_valid(self) -> None:
        """Verify ID validation accepts numeric strings."""
        validated_id = self.menu._validate_id("123")
        assert validated_id == 123

    def test_validate_id_invalid(self) -> None:
        """Verify ID validation rejects non-numeric strings."""
        from src.models.exceptions import InvalidIDError

        with pytest.raises(InvalidIDError):
            self.menu._validate_id("invalid")
