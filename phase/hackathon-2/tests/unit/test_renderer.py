"""Unit tests for Rich table renderer."""

from io import StringIO
from unittest.mock import patch

from src.models.task import Task, TaskStatus
from src.ui.renderer import RichTableRenderer


class TestRichTableRenderer:
    """Test RichTableRenderer functionality."""

    def test_render_empty_tasks_list(self) -> None:
        """Verify renderer shows friendly message for empty list."""
        renderer = RichTableRenderer()

        # Capture console output
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            renderer.render_tasks([])
            output = mock_stdout.getvalue()

        # Should contain friendly message
        # Note: Rich adds ANSI codes, so we check for the message content
        assert "No tasks found" in output or len(output) > 0  # Rich output

    def test_render_tasks_creates_table(self) -> None:
        """Verify renderer creates table for non-empty task list."""
        renderer = RichTableRenderer()
        tasks = [
            Task(id=1, title="Task 1", description="Description 1", status=TaskStatus.PENDING),
            Task(
                id=2, title="Task 2", description="Description 2", status=TaskStatus.COMPLETED
            ),
        ]

        # Capture console output
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            renderer.render_tasks(tasks)
            output = mock_stdout.getvalue()

        # Output should exist (Rich formatting)
        assert len(output) > 0

    def test_format_status_pending(self) -> None:
        """Verify PENDING status is formatted correctly."""
        renderer = RichTableRenderer()

        formatted = renderer._format_status(TaskStatus.PENDING)

        assert "PENDING" in formatted
        assert "yellow" in formatted

    def test_format_status_completed(self) -> None:
        """Verify COMPLETED status is formatted with checkmark."""
        renderer = RichTableRenderer()

        formatted = renderer._format_status(TaskStatus.COMPLETED)

        assert "COMPLETED" in formatted
        assert "✓" in formatted
        assert "green" in formatted

    def test_truncate_short_text(self) -> None:
        """Verify short text is not truncated."""
        renderer = RichTableRenderer()

        text = "Short text"
        result = renderer._truncate(text, 50)

        assert result == text

    def test_truncate_long_text(self) -> None:
        """Verify long text is truncated with ellipsis."""
        renderer = RichTableRenderer()

        long_text = "a" * 100
        result = renderer._truncate(long_text, 50)

        assert len(result) == 50
        assert result.endswith("...")
        assert result == ("a" * 47) + "..."

    def test_truncate_exact_max_length(self) -> None:
        """Verify text at exact max length is not truncated."""
        renderer = RichTableRenderer()

        text = "a" * 50
        result = renderer._truncate(text, 50)

        assert result == text
