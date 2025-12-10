from datetime import datetime
from typing import Optional
from rich.text import Text

class Task:
    def __init__(self, task_id: int, title: str, description: str = ""):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def mark_complete(self) -> None:
        self.completed = True
        self.updated_at = datetime.now()
    
    def mark_incomplete(self) -> None:
        self.completed = False
        self.updated_at = datetime.now()
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        """Fallback plain-text version."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title}"

    def rich(self) -> Text:
        """Colorful text rendering for Rich console."""
        status_text = Text("✓ Completed", style="bold green") if self.completed else Text("○ Pending", style="bold yellow")

        text = Text()
        text.append(f"[{self.id}] ", style="bold cyan")
        text.append(self.title, style="bold white")
        text.append(" — ")
        text.append(status_text)

        return text
