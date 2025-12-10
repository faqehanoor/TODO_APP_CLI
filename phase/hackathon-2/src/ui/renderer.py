"""Rich table renderer for task display.

Provides formatted output using the Rich library for
enhanced terminal UI experience.
"""

from rich.console import Console
from rich.table import Table

from src.models.task import Task, TaskStatus


class RichTableRenderer:
    """Renderer for displaying tasks in Rich table format.

    Provides formatted output with proper columns, colors,
    and visual indicators for task status.
    """

    def __init__(self) -> None:
        """Initialize renderer with Rich console."""
        self.console = Console()

    def render_tasks(self, tasks: list[Task]) -> None:
        """Render tasks as formatted Rich table.

        Args:
            tasks: List of tasks to display (can be empty)
        """
        # Handle empty list with friendly message
        if not tasks:
            self.console.print(
                "\n[yellow]No tasks found. Add your first task to get started![/yellow]\n"
            )
            return

        # Create table with styled columns
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title", style="bold")
        table.add_column("Description")
        table.add_column("Status", width=12)

        # Add rows with status formatting
        for task in tasks:
            status_display = self._format_status(task.status)
            # Truncate long text for display (full text still stored)
            title_display = self._truncate(task.title, 50)
            description_display = self._truncate(task.description, 60)

            table.add_row(
                str(task.id),
                title_display,
                description_display,
                status_display,
            )

        # Display table
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")

    def _format_status(self, status: TaskStatus) -> str:
        """Format status with visual indicator.

        Args:
            status: Task status enum

        Returns:
            Formatted status string with color markup
        """
        if status == TaskStatus.COMPLETED:
            return "[green]✓ COMPLETED[/green]"
        return "[yellow]PENDING[/yellow]"

    def _truncate(self, text: str, max_length: int) -> str:
        """Truncate text to maintain table formatting.

        Args:
            text: Text to truncate
            max_length: Maximum length before truncation

        Returns:
            Truncated text with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."
