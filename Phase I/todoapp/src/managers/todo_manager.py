from typing import List, Optional
from models.task import Task

class TodoManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
    
    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None) -> bool:
        task = self.get_task(task_id)
        if task:
            task.update(title, description)
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def mark_complete(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            return True
        return False
    
    def mark_incomplete(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            return True
        return False
    
    def list_tasks(self) -> List[Task]:
        return self.tasks[:]
    
    def get_completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]