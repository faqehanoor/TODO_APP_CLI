import sys
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from managers.todo_manager import TodoManager
from models.task import Task

console = Console()

class ConsoleUI:
    def __init__(self, todo_manager: TodoManager):
        self.todo_manager = todo_manager
    
    # ---------------------------------------------------------
    # MENU
    # ---------------------------------------------------------
    def display_menu(self) -> None:
        console.print(
            Panel.fit(
                "[bold cyan]MY TODO APP[/bold cyan]\n"
                "[white]1.[/white] Add New Task\n"
                "[white]2.[/white] Show All Tasks\n"
                "[white]3.[/white] Edit Task\n"
                "[white]4.[/white] Delete Task\n"
                "[white]5.[/white] Mark Task Done\n"
                "[white]6.[/white] Mark Task Not Done\n"
                "[white]7.[/white] Exit Program",
                title="📋 Menu",
                border_style="cyan",
            )
        )
    
    def get_user_choice(self) -> str:
        return Prompt.ask("[bold green]Enter your choice[/bold green]", choices=[str(i) for i in range(1, 8)])
    
    # ---------------------------------------------------------
    # INPUT HELPERS
    # ---------------------------------------------------------
    def get_task_details(self) -> tuple[str, str]:
        title = Prompt.ask("[yellow]What do you need to do?[/yellow]").strip()
        description = Prompt.ask("[yellow]Any extra details? (optional)[/yellow]", default="").strip()
        return title, description
    
    def get_task_id(self) -> Optional[int]:
        try:
            return int(Prompt.ask("[cyan]Enter task number[/cyan]"))
        except ValueError:
            console.print("[bold red]❌ That's not a valid number![/bold red]")
            return None

    # ---------------------------------------------------------
    # ACTIONS
    # ---------------------------------------------------------
    def add_task(self) -> None:
        console.print(Panel("[bold cyan]➕ Adding New Task[/bold cyan]", border_style="cyan"))
        
        title, description = self.get_task_details()
        
        if not title:
            console.print("[bold red]❌ You must enter what you need to do![/bold red]")
            return
        
        task = self.todo_manager.add_task(title, description)
        console.print(f"[bold green]✔ Task Added:[/bold green] [cyan]#{task.id}[/cyan] {task.title}")
    
    def list_tasks(self) -> None:
        tasks = self.todo_manager.list_tasks()
        
        if not tasks:
            console.print("[bold yellow]⚠ No tasks yet! Add one to get started.[/bold yellow]")
            return
        
        table = Table(title="📋 Your Tasks", show_header=True, header_style="bold cyan")
        table.add_column("ID", width=5)
        table.add_column("Title", width=30)
        table.add_column("Status", width=12)
        
        for task in tasks:
            status = "[green]✓ Done[/green]" if task.completed else "[yellow]○ Pending[/yellow]"
            table.add_row(str(task.id), task.title, status)

        console.print(table)
    
    def update_task(self) -> None:
        console.print(Panel("[bold cyan]✏ Editing Task[/bold cyan]", border_style="cyan"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        task = self.todo_manager.get_task(task_id)
        if not task:
            console.print(f"[bold red]❌ No task found with number {task_id}[/bold red]")
            return
        
        console.print(f"[cyan]Current task:[/cyan] [white]{task.title}[/white]")
        console.print(f"[cyan]Details:[/cyan] [dim]{task.description}[/dim]")
        
        new_title = Prompt.ask("New task name (press Enter to keep current)", default="").strip()
        new_description = Prompt.ask("New details (press Enter to keep current)", default="").strip()
        
        if not new_title:
            new_title = None
        if not new_description:
            new_description = None
        
        if self.todo_manager.update_task(task_id, new_title, new_description):
            console.print("[bold green]✔ Task updated successfully![/bold green]")
        else:
            console.print("[bold red]❌ Could not update task.[/bold red]")
    
    def delete_task(self) -> None:
        console.print(Panel("[bold red]🗑 Deleting Task[/bold red]", border_style="red"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        task = self.todo_manager.get_task(task_id)
        if not task:
            console.print(f"[bold red]❌ No task found with number {task_id}[/bold red]")
            return
        
        confirm = Confirm.ask(f"Delete [yellow]{task.title}[/yellow]?", default=False)
        if confirm:
            if self.todo_manager.delete_task(task_id):
                console.print("[bold green]✔ Task deleted![/bold green]")
            else:
                console.print("[bold red]❌ Could not delete task.[/bold red]")
        else:
            console.print("[cyan]Deletion cancelled.[/cyan]")
    
    def mark_complete(self) -> None:
        console.print(Panel("[bold green]✅ Marking Task Done[/bold green]", border_style="green"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        if self.todo_manager.mark_complete(task_id):
            console.print("[bold green]✔ Task marked as done![/bold green]")
        else:
            console.print(f"[bold red]❌ No task found with number {task_id}[/bold red]")
    
    def mark_incomplete(self) -> None:
        console.print(Panel("[bold yellow]📋 Marking Task Not Done[/bold yellow]", border_style="yellow"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        if self.todo_manager.mark_incomplete(task_id):
            console.print("[yellow]○ Task marked as not done.[/yellow]")
        else:
            console.print(f"[bold red]❌ No task found with number {task_id}[/bold red]")
    
    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------
    def run(self) -> None:
        console.print(Panel("[bold cyan]Welcome to My Todo App! 🚀[/bold cyan]", border_style="cyan"))
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.mark_complete()
            elif choice == '6':
                self.mark_incomplete()
            elif choice == '7':
                console.print("[bold cyan]👋 Thanks for using My Todo App! See you next time![/bold cyan]")
                sys.exit(0)
