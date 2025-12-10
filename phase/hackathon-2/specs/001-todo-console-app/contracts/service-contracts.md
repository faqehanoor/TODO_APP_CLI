# Service Contracts: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-07
**Phase**: Phase 1 - Service Layer Contracts

## Overview

This document defines the service layer contracts (business logic interface) that sit between the UI layer and the repository layer. The service layer enforces business rules, orchestrates operations, and provides a clean API for the UI.

---

## Service: TaskService

**Purpose**: Coordinates task operations with business logic validation, error handling, and repository interaction

**Responsibilities**:
- Validate business rules before repository calls
- Translate repository exceptions to user-friendly errors
- Orchestrate multi-step operations if needed
- Provide clean interface for UI layer

**Does NOT Handle**:
- User input parsing (UI layer responsibility)
- Data persistence details (repository responsibility)
- Output formatting (UI layer responsibility)

---

### Method: create_task

**Signature**:
```python
def create_task(self, title: str, description: str = "") -> Task
```

**Purpose**: Create new task with validation

**Parameters**:
- `title`: Task title (required, non-empty)
- `description`: Optional task description (default: empty string)

**Returns**:
- Task instance with auto-generated ID and PENDING status

**Business Rules**:
1. Title MUST NOT be empty (FR-002)
2. Title MUST NOT be whitespace-only
3. Description CAN be empty (valid state)
4. Status is always PENDING for new tasks

**Error Conditions**:
- Raises `EmptyTitleError` if title is empty or whitespace-only
  - Message: "Title cannot be empty. Please provide a title for your task."

**Flow**:
1. Validate title not empty (strip whitespace, check length > 0)
2. If invalid, raise EmptyTitleError
3. Create Task instance (no ID yet, status=PENDING)
4. Call repository.add(task)
5. Return task with assigned ID

**Acceptance Scenarios** (from spec):
- User Story 1, Scenario 1: Title "Buy groceries", description "Milk, eggs, bread" → Task created with ID 1, status PENDING
- User Story 1, Scenario 2: Title "Call dentist", no description → Task created with ID 2, empty description, status PENDING
- Edge case: Empty title → EmptyTitleError raised

---

### Method: list_tasks

**Signature**:
```python
def list_tasks(self) -> list[Task]
```

**Purpose**: Retrieve all tasks sorted by ID

**Parameters**: None

**Returns**:
- List of all tasks, sorted by ID ascending (FR-011)
- Empty list if no tasks exist (FR-019)

**Business Rules**:
- Tasks MUST be sorted by ID (1, 2, 3, ...)
- Empty list is valid return value

**Error Conditions**: None (empty list is success)

**Flow**:
1. Call repository.get_all()
2. Return tasks (already sorted by repository contract)

**Acceptance Scenarios** (from spec):
- User Story 1, Scenario 3: Multiple tasks exist → All displayed in ID order
- User Story 1, Scenario 5: No tasks exist → Empty list (UI shows friendly message)

---

### Method: get_task

**Signature**:
```python
def get_task(self, task_id: int) -> Task
```

**Purpose**: Retrieve specific task by ID with validation

**Parameters**:
- `task_id`: Unique task identifier

**Returns**:
- Task instance if found

**Business Rules**:
- Task ID MUST exist (FR-003)

**Error Conditions**:
- Raises `NotFoundError` if task doesn't exist
  - Message: f"Task with ID {task_id} not found. Please check the ID and try again."

**Flow**:
1. Call repository.get_by_id(task_id)
2. If None returned, raise NotFoundError with task_id in message
3. Return task

**Acceptance Scenarios** (from spec):
- User Story 3, Scenario 4: Update non-existent ID 50 → NotFoundError
- User Story 4, Scenario 3: Delete non-existent ID 100 → NotFoundError

---

### Method: update_task

**Signature**:
```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> Task
```

**Purpose**: Update task title and/or description with validation

**Parameters**:
- `task_id`: Task to update (required)
- `title`: New title (None = no change)
- `description`: New description (None = no change)

**Returns**:
- Updated task instance

**Business Rules**:
1. Task ID MUST exist (FR-003)
2. If title provided, MUST NOT be empty (FR-002)
3. None for title/description means "no change"
4. Empty string for description is valid (clears description)
5. Status and ID are preserved (FR-014)

**Error Conditions**:
- Raises `NotFoundError` if task_id doesn't exist
  - Message: f"Task with ID {task_id} not found. Please check the ID and try again."
- Raises `EmptyTitleError` if title is empty or whitespace-only
  - Message: "Title cannot be empty. Please provide a title for your task."

**Flow**:
1. If title provided, validate not empty (strip, check length > 0)
2. If title invalid, raise EmptyTitleError
3. Call repository.update(task_id, title, description)
4. If repository raises NotFoundError, propagate with user-friendly message
5. Return updated task

**Acceptance Scenarios** (from spec):
- User Story 3, Scenario 1: Update ID 1 title "Buy groceries" → "Buy organic groceries"
- User Story 3, Scenario 2: Update ID 2 description → "Call by 3pm tomorrow"
- User Story 3, Scenario 3: Update both title and description → Both updated
- User Story 3, Scenario 4: Update non-existent ID 50 → NotFoundError
- User Story 3, Scenario 5: Empty description on update → description unchanged (None passed)
- User Story 3, Scenario 6: Update completed task → status preserved

---

### Method: delete_task

**Signature**:
```python
def delete_task(self, task_id: int) -> None
```

**Purpose**: Delete task by ID with validation

**Parameters**:
- `task_id`: Task to delete

**Returns**: None

**Business Rules**:
- Task ID MUST exist (FR-003)
- ID sequence continues after deletion (FR-006)

**Error Conditions**:
- Raises `NotFoundError` if task_id doesn't exist
  - Message: f"Task with ID {task_id} not found. Please check the ID and try again."

**Flow**:
1. Call repository.delete(task_id)
2. If returns False (not found), raise NotFoundError
3. Return None (success)

**Acceptance Scenarios** (from spec):
- User Story 4, Scenario 1: Delete ID 2 from [1,2,3] → Task 2 removed, [1,3] remain
- User Story 4, Scenario 2: Delete all tasks, add new → ID sequence continues (e.g., 6)
- User Story 4, Scenario 3: Delete non-existent ID 100 → NotFoundError
- User Story 4, Scenario 4: Delete ID 1 → Cannot toggle or update afterward

---

### Method: toggle_task_status

**Signature**:
```python
def toggle_task_status(self, task_id: int) -> Task
```

**Purpose**: Toggle task between PENDING and COMPLETED

**Parameters**:
- `task_id`: Task to toggle

**Returns**:
- Updated task with toggled status

**Business Rules**:
- Task ID MUST exist (FR-003)
- PENDING → COMPLETED
- COMPLETED → PENDING
- All other fields preserved (FR-012)

**Error Conditions**:
- Raises `NotFoundError` if task_id doesn't exist
  - Message: f"Task with ID {task_id} not found. Please check the ID and try again."

**Flow**:
1. Call repository.toggle_status(task_id)
2. If repository raises NotFoundError, propagate with user-friendly message
3. Return updated task

**Acceptance Scenarios** (from spec):
- User Story 2, Scenario 1: Toggle ID 1 (PENDING) → COMPLETED
- User Story 2, Scenario 2: Toggle ID 2 (COMPLETED) → PENDING
- User Story 2, Scenario 3: Toggle non-existent ID 99 → NotFoundError

---

## Exception Hierarchy

### TodoAppError (Base Exception)

**Purpose**: Base class for all application-specific errors

**Attributes**:
- `message`: User-friendly error description

**Usage**: Catch-all for application errors vs system errors

---

### ValidationError (extends TodoAppError)

**Purpose**: Input validation failures

**Subclasses**:
- `EmptyTitleError`: Title is empty or whitespace-only
- `InvalidIDError`: ID format is not numeric (handled at UI layer, not service)

**User Message Format**: "{Problem}. {Guidance}."

**Examples**:
- "Title cannot be empty. Please provide a title for your task."
- "Invalid ID format. Please enter a numeric ID (e.g., 1, 2, 3)."

---

### NotFoundError (extends TodoAppError)

**Purpose**: Resource (task) doesn't exist

**Attributes**:
- `task_id`: The ID that wasn't found

**User Message Format**: "Task with ID {task_id} not found. Please check the ID and try again."

**Usage**: Update, delete, toggle operations on non-existent IDs

---

### RepositoryError (extends TodoAppError)

**Purpose**: Storage layer failures (future use)

**Usage**: Database connection failures in Phase II (not applicable to Phase I in-memory)

---

## Service Dependencies

**TaskService depends on**:
- `TaskRepositoryProtocol`: For data operations
- `Task`, `TaskStatus`: Data models
- Custom exceptions: For error signaling

**TaskService is used by**:
- UI layer (Typer CLI commands)
- Test suite (integration tests)

**Dependency Injection**:
```python
class TaskService:
    def __init__(self, repository: TaskRepositoryProtocol) -> None:
        self._repository = repository
```

**Rationale**: Service receives repository via constructor, enabling:
- Unit testing with mock repositories
- Phase II swap (InMemory → PostgreSQL) without service changes
- Constitutional Principle IV (Evolutionary Architecture)

---

## Error Handling Contract

**Service Layer Guarantees**:
1. **No silent failures** (Principle XI): All errors raise explicit exceptions
2. **User-friendly messages** (FR-018): All exceptions include actionable guidance
3. **Type-safe errors**: All exception types are known at compile time (mypy tracked)

**UI Layer Responsibilities**:
1. Catch TodoAppError and subclasses
2. Display error.message to user
3. Log full exception details (for debugging)
4. No stack traces shown to user

**Example Error Flow**:
```
User inputs empty title
  → UI calls service.create_task("")
  → Service validates, raises EmptyTitleError("Title cannot be empty...")
  → UI catches, displays error.message
  → User sees: "Title cannot be empty. Please provide a title for your task."
```

---

## Performance Contracts

**Service Layer Performance**:
- `create_task`: O(1) - single repository call
- `list_tasks`: O(n log n) - repository get_all + sort (n = task count)
- `get_task`: O(1) - dict lookup in repository
- `update_task`: O(1) - single repository call
- `delete_task`: O(1) - single repository call
- `toggle_task_status`: O(1) - single repository call

**Guarantees** (from Success Criteria):
- SC-001: create_task completes in under 10 seconds (user interaction time)
- SC-002: list_tasks displays in under 1 second for 1000 tasks
- SC-007: All operations respond within 1 second

**Validation**: Service layer adds negligible overhead (<1ms per operation)

---

## Constitutional Alignment

| Principle | Service Layer Support |
|-----------|----------------------|
| I. Spec-First Development | ✅ Contracts defined before implementation |
| IV. Evolutionary Architecture | ✅ Repository Protocol enables Phase II swap |
| V. Single Responsibility | ✅ Service = business logic only (no UI, no storage details) |
| VI. User Experience First | ✅ Actionable error messages in all exceptions |
| VIII. Test-Driven Development | ✅ Contracts enable test-first implementation |
| X. Type Safety | ✅ All methods fully typed, mypy --strict compatible |
| XI. Error Handling | ✅ No silent failures, explicit exception hierarchy |

---

## Appendix: Full Type Signatures

```python
from typing import Protocol

class TaskService:
    def __init__(self, repository: TaskRepositoryProtocol) -> None: ...

    def create_task(self, title: str, description: str = "") -> Task: ...

    def list_tasks(self) -> list[Task]: ...

    def get_task(self, task_id: int) -> Task: ...

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None
    ) -> Task: ...

    def delete_task(self, task_id: int) -> None: ...

    def toggle_task_status(self, task_id: int) -> Task: ...


# Exception classes
class TodoAppError(Exception):
    message: str

class ValidationError(TodoAppError): ...
class EmptyTitleError(ValidationError): ...
class InvalidIDError(ValidationError): ...

class NotFoundError(TodoAppError):
    task_id: int

class RepositoryError(TodoAppError): ...
```
