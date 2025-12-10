"""Main application entry point.

Wires together all components and runs the main application loop
using Typer CLI framework.
"""

import typer
from rich.console import Console

from src.services.task_service import TaskService
from src.storage.in_memory import InMemoryTaskRepository
from src.ui.menu import MenuHandler
from src.ui.renderer import RichTableRenderer

app: typer.Typer = typer.Typer()


def create_app_components() -> tuple[TaskService, MenuHandler]:
    """Create and wire application components.

    Returns:
        Tuple of (service, menu_handler) ready for use
    """
    # Create repository (in-memory for Phase I)
    repository = InMemoryTaskRepository()

    # Create service layer
    service = TaskService(repository)

    # Create UI components
    renderer = RichTableRenderer()
    menu_handler = MenuHandler(service, renderer)

    return service, menu_handler


@app.command()  # type: ignore[misc]
def main() -> None:
    """Main application loop - interactive todo app.

    Displays menu, handles user input, and routes to appropriate
    operations until user exits.
    """
    console = Console()

    # Display welcome banner
    console.print("\n[bold cyan]═══════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Welcome to Todo Console App     [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════[/bold cyan]\n")

    # Initialize components
    service, menu_handler = create_app_components()

    # Main application loop
    while True:
        try:
            # Display menu
            menu_handler.show_menu()

            # Get user choice
            choice = menu_handler.prompt_menu_choice()

            # Route to appropriate handler
            if choice == "1":
                menu_handler.prompt_add_task()
            elif choice == "2":
                menu_handler.display_tasks()
            elif choice == "3":
                menu_handler.prompt_update_task()
            elif choice == "4":
                menu_handler.prompt_delete_task()
            elif choice == "5":
                menu_handler.prompt_toggle_task()
            elif choice == "6":
                # Exit with goodbye message
                console.print(
                    "\n[yellow]Goodbye! Your tasks will not be saved.[/yellow]\n"
                )
                break
            else:
                console.print("\n[red]Invalid choice. Please enter 1-6.[/red]\n")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print(
                "\n\n[yellow]Goodbye! Your tasks will not be saved.[/yellow]\n"
            )
            break
        except Exception as e:
            # Handle unexpected errors
            console.print(f"\n[red]Unexpected error: {e}[/red]\n")
            console.print("[yellow]Returning to main menu...[/yellow]\n")


if __name__ == "__main__":
    app()
