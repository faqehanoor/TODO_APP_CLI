"""Menu handler for user interaction.

Provides interactive menu display and prompts for
task operations using Typer.
"""

from typing import Any

import typer
from rich.console import Console

from src.models.exceptions import InvalidIDError
from src.services.task_service import TaskService
from src.ui.renderer import RichTableRenderer


class MenuHandler:
    """Handler for menu display and user prompts.

    Manages user interaction flow using Typer prompts
    and Rich console output.
    """

    def __init__(self, service: TaskService, renderer: RichTableRenderer) -> None:
        """Initialize menu handler with dependencies.

        Args:
            service: Task service for business operations
            renderer: Renderer for task display
        """
        self.service = service
        self.renderer = renderer
        self.console = Console()

    def show_menu(self) -> None:
        """Display numbered menu options."""
        self.console.print("\n[bold cyan]Todo App - Main Menu[/bold cyan]")
        self.console.print("1. Add Task")
        self.console.print("2. List Tasks")
        self.console.print("3. Update Task")
        self.console.print("4. Delete Task")
        self.console.print("5. Toggle Task Status")
        self.console.print("6. Exit")
        self.console.print()

    def prompt_menu_choice(self) -> str:
        """Prompt user for menu choice.

        Returns:
            User's menu choice as string
        """
        choice: Any = typer.prompt("Enter your choice")
        return str(choice)

    def prompt_add_task(self) -> None:
        """Prompt user for task details and create task.

        Handles title and description input via Typer prompts.
        """
        self.console.print("\n[bold]Add New Task[/bold]")

        # Prompt for title (required)
        title = typer.prompt("Enter task title")

        # Prompt for description (optional)
        description = typer.prompt(
            "Enter task description (optional, press Enter to skip)", default=""
        )

        # Create task via service
        try:
            task = self.service.create_task(title=title, description=description)
            self.console.print(
                f"\n[green]✓ Task created successfully with ID {task.id}[/green]\n"
            )
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]\n")

    def display_tasks(self) -> None:
        """Display all tasks using renderer.

        Retrieves tasks from service and delegates rendering.
        """
        tasks = self.service.list_tasks()
        self.renderer.render_tasks(tasks)

    def prompt_toggle_task(self) -> None:
        """Prompt user for task ID and toggle status.

        Handles ID input validation and status toggling.
        """
        self.console.print("\n[bold]Toggle Task Status[/bold]")

        # Prompt for task ID
        task_id_str = typer.prompt("Enter task ID to toggle")

        try:
            # Validate ID is numeric
            task_id = self._validate_id(task_id_str)

            # Toggle status via service
            task = self.service.toggle_task_status(task_id)
            status_text = "COMPLETED" if task.status.value == "COMPLETED" else "PENDING"
            self.console.print(
                f"\n[green]✓ Task {task_id} status toggled to {status_text}[/green]\n"
            )
        except Exception as e:
            error_msg = e.message if hasattr(e, "message") else str(e)
            self.console.print(f"\n[red]Error: {error_msg}[/red]\n")

    def prompt_update_task(self) -> None:
        """Prompt user for task ID and new details.

        Handles ID, title, and description input for updates.
        """
        self.console.print("\n[bold]Update Task[/bold]")

        # Prompt for task ID
        task_id_str = typer.prompt("Enter task ID to update")

        try:
            # Validate ID is numeric
            task_id = self._validate_id(task_id_str)

            # Prompt for new title (optional)
            new_title_input = typer.prompt(
                "Enter new title (press Enter to keep current)", default=""
            )
            new_title = new_title_input if new_title_input else None

            # Prompt for new description (optional)
            new_description_input = typer.prompt(
                "Enter new description (press Enter to keep current)", default=""
            )
            new_description = new_description_input if new_description_input else None

            # Update via service
            self.service.update_task(task_id, title=new_title, description=new_description)
            self.console.print(f"\n[green]✓ Task {task_id} updated successfully[/green]\n")
        except Exception as e:
            error_msg = e.message if hasattr(e, "message") else str(e)
            self.console.print(f"\n[red]Error: {error_msg}[/red]\n")

    def prompt_delete_task(self) -> None:
        """Prompt user for task ID and delete task.

        Handles ID input validation and deletion.
        """
        self.console.print("\n[bold]Delete Task[/bold]")

        # Prompt for task ID
        task_id_str = typer.prompt("Enter task ID to delete")

        try:
            # Validate ID is numeric
            task_id = self._validate_id(task_id_str)

            # Delete via service
            self.service.delete_task(task_id)
            self.console.print(f"\n[green]✓ Task {task_id} deleted successfully[/green]\n")
        except Exception as e:
            error_msg = e.message if hasattr(e, "message") else str(e)
            self.console.print(f"\n[red]Error: {error_msg}[/red]\n")

    def _validate_id(self, id_str: str) -> int:
        """Validate ID input is numeric.

        Args:
            id_str: ID input as string

        Returns:
            Validated ID as integer

        Raises:
            InvalidIDError: If ID is not numeric
        """
        try:
            return int(id_str)
        except ValueError as e:
            raise InvalidIDError() from e
