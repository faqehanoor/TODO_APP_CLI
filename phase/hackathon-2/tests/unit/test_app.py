"""Unit tests for main application."""

from io import StringIO
from unittest.mock import MagicMock, patch

from src.app import create_app_components, main
from src.services.task_service import TaskService
from src.ui.menu import MenuHandler


class TestApp:
    """Test main application components."""

    def test_create_app_components(self) -> None:
        """Verify create_app_components creates all required components."""
        service, menu_handler = create_app_components()

        # Verify service is TaskService
        assert isinstance(service, TaskService)

        # Verify menu_handler is MenuHandler
        assert isinstance(menu_handler, MenuHandler)

        # Verify components are wired correctly
        assert menu_handler.service is service

    def test_main_exit_immediately(self) -> None:
        """Verify main() exits cleanly when user chooses exit (6)."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # Mock menu choice to return '6' (exit)
            mock_menu.prompt_menu_choice.return_value = "6"

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

            # Verify show_menu was called
            mock_menu.show_menu.assert_called()

            # Verify exit message displayed
            assert "Goodbye" in output

    def test_main_add_task_then_exit(self) -> None:
        """Verify main() handles add task then exit."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: add task (1), second choice: exit (6)
            mock_menu.prompt_menu_choice.side_effect = ["1", "6"]

            with patch("sys.stdout", new_callable=StringIO):
                main()

            # Verify add task was called
            mock_menu.prompt_add_task.assert_called_once()

    def test_main_list_tasks_then_exit(self) -> None:
        """Verify main() handles list tasks then exit."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: list (2), second choice: exit (6)
            mock_menu.prompt_menu_choice.side_effect = ["2", "6"]

            with patch("sys.stdout", new_callable=StringIO):
                main()

            # Verify display tasks was called
            mock_menu.display_tasks.assert_called_once()

    def test_main_update_task_then_exit(self) -> None:
        """Verify main() handles update task then exit."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: update (3), second choice: exit (6)
            mock_menu.prompt_menu_choice.side_effect = ["3", "6"]

            with patch("sys.stdout", new_callable=StringIO):
                main()

            # Verify update task was called
            mock_menu.prompt_update_task.assert_called_once()

    def test_main_delete_task_then_exit(self) -> None:
        """Verify main() handles delete task then exit."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: delete (4), second choice: exit (6)
            mock_menu.prompt_menu_choice.side_effect = ["4", "6"]

            with patch("sys.stdout", new_callable=StringIO):
                main()

            # Verify delete task was called
            mock_menu.prompt_delete_task.assert_called_once()

    def test_main_toggle_status_then_exit(self) -> None:
        """Verify main() handles toggle status then exit."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: toggle (5), second choice: exit (6)
            mock_menu.prompt_menu_choice.side_effect = ["5", "6"]

            with patch("sys.stdout", new_callable=StringIO):
                main()

            # Verify toggle task was called
            mock_menu.prompt_toggle_task.assert_called_once()

    def test_main_invalid_choice_then_exit(self) -> None:
        """Verify main() handles invalid menu choice."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: invalid (99), second choice: exit (6)
            mock_menu.prompt_menu_choice.side_effect = ["99", "6"]

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

            # Verify error message shown
            assert "Invalid choice" in output

    def test_main_keyboard_interrupt(self) -> None:
        """Verify main() handles Ctrl+C gracefully."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # Simulate Ctrl+C on first menu choice
            mock_menu.prompt_menu_choice.side_effect = KeyboardInterrupt()

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

            # Verify goodbye message shown
            assert "Goodbye" in output

    def test_main_unexpected_error(self) -> None:
        """Verify main() handles unexpected errors gracefully."""
        with patch("src.app.create_app_components") as mock_create:
            mock_service = MagicMock()
            mock_menu = MagicMock()
            mock_create.return_value = (mock_service, mock_menu)

            # First choice: trigger error, second choice: exit
            mock_menu.prompt_menu_choice.side_effect = [Exception("Test error"), "6"]

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

            # Verify error message shown
            assert "error" in output.lower() or "Error" in output
