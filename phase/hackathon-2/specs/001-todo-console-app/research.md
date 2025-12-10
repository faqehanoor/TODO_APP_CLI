# Research: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-07
**Phase**: Phase 0 - Technology Research & Validation

## Overview

This document captures research findings and technology decisions for implementing the in-memory Python console todo application. All decisions align with Constitutional requirements and Phase I (Console App) of the 5-phase evolution.

---

## Technology Stack Research

### 1. CLI Framework: Typer vs Click vs argparse

**Decision**: Typer

**Rationale**:
- Type-safe by design (aligns with Constitutional Principle X)
- Built on Click, leveraging battle-tested foundation
- Automatic help generation from type hints
- Interactive prompts support (required for menu-driven interface per FR-001)
- Excellent developer experience with minimal boilerplate
- Forward-compatible with FastAPI (Phase II planning)

**Alternatives Considered**:
- **Click**: Mature but requires more decorators; less type-safe
- **argparse**: Standard library but verbose; poor UX for interactive menus
- **Fire**: Auto-generates CLIs but less control over validation

**References**:
- Typer documentation: https://typer.tiangolo.com/
- Type safety comparison: Typer uses Pydantic internally

---

### 2. Terminal UI: Rich vs Colorama vs Tabulate

**Decision**: Rich

**Rationale**:
- Advanced table formatting with automatic column sizing (FR-009)
- Built-in color support with semantic markup (FR-010: green checkmark)
- Progress bars, panels, and console management for future phases
- Active maintenance and modern Python 3.13+ compatibility
- Single dependency vs combining colorama + tabulate
- Superior error rendering (aligns with Principle VI: User Experience First)

**Alternatives Considered**:
- **Colorama**: Colors only, no table formatting
- **Tabulate**: Tables only, no colors or advanced formatting
- **Textual**: Full TUI framework (over-engineered for Phase I console app)

**Trade-offs**:
- Rich is heavier (~500KB) vs colorama (~50KB)
- Justified: Rich's feature set matches all UI requirements in single dependency

**References**:
- Rich documentation: https://rich.readthedocs.io/
- Table examples: https://rich.readthedocs.io/en/stable/tables.html

---

### 3. Testing Framework: pytest vs unittest

**Decision**: pytest

**Rationale**:
- Fixture system ideal for repository pattern testing
- Better assertion introspection (clearer failure messages)
- Parameterized testing for edge cases (10 edge cases in spec)
- Plugin ecosystem (pytest-cov for coverage, pytest-xdist for parallel)
- Industry standard for Python projects
- Cleaner syntax (no class inheritance required)

**Alternatives Considered**:
- **unittest**: Standard library but verbose, less expressive assertions
- **nose2**: Less active development, pytest supersedes it

**Test Strategy**:
- Unit tests: Models, Repository, Service layer
- Integration tests: End-to-end user story flows (4 user stories)
- Fixtures: Shared repository instances, sample task data

**References**:
- pytest documentation: https://docs.pytest.org/

---

### 4. Type Checking: mypy Configuration

**Decision**: `mypy --strict` with zero tolerance

**Rationale**:
- Constitutional requirement (Principle X: Type Safety NON-NEGOTIABLE)
- Strict mode enforces: no implicit Any, no untyped calls, no untyped defs
- Catches errors at analysis time vs runtime (SC-006: zero type errors)

**Configuration** (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Type Annotations Required**:
- All function signatures (params and return types)
- Class attributes (with typing.Final for constants)
- Protocol definitions for repository interface

**References**:
- mypy strict mode: https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict

---

### 5. Package Management: uv vs pip vs poetry

**Decision**: uv

**Rationale**:
- Constitutional requirement (Tech Stack Guidelines: "Python 3.13+/uv")
- 10-100x faster than pip for dependency resolution
- Built in Rust, modern architecture
- Lock file support (pyproject.toml + uv.lock)
- Compatible with standard Python packaging (PEP 621)
- Future-proof: growing ecosystem adoption

**Project Structure**:
- `pyproject.toml`: Project metadata, dependencies, tool configs
- `uv.lock`: Locked dependency tree (committed to git)
- No separate requirements.txt needed

**References**:
- uv documentation: https://github.com/astral-sh/uv

---

### 6. Repository Pattern Implementation

**Decision**: Protocol-based abstraction with in-memory concrete implementation

**Rationale**:
- Constitutional Principle IV: Evolutionary Architecture (design for future, implement for present)
- FR-016: Repository pattern required for data access separation
- Phase II will swap in-memory → PostgreSQL without changing business logic
- Protocol (PEP 544) provides structural subtyping (more flexible than ABC)

**Architecture**:
```
TaskRepositoryProtocol (interface)
    ↑
    └── InMemoryTaskRepository (Phase I implementation)
    └── PostgreSQLTaskRepository (Phase II - future)
```

**Interface Methods**:
- `add(task: Task) -> Task`: Add new task with auto-generated ID
- `get_all() -> list[Task]`: Retrieve all tasks sorted by ID
- `get_by_id(task_id: int) -> Task | None`: Retrieve specific task
- `update(task_id: int, title: str | None, description: str | None) -> Task`: Update task
- `delete(task_id: int) -> bool`: Delete task, return success status
- `toggle_status(task_id: int) -> Task`: Toggle PENDING ↔ COMPLETED

**Trade-offs**:
- Additional abstraction layer adds ~50 LOC overhead
- Justified: Prevents Phase II rewrite, validates Constitutional Principle IV

**References**:
- PEP 544 Protocols: https://peps.python.org/pep-0544/
- Repository pattern: Martin Fowler's PoEAA

---

### 7. Error Handling Strategy

**Decision**: Custom exception hierarchy + typed error responses

**Rationale**:
- Constitutional Principle XI: No silent failures
- FR-018: User-friendly error messages with actionable guidance
- Type-safe error propagation (mypy can track exception types)

**Exception Hierarchy**:
```
TodoAppError (base)
    ├── ValidationError
    │   ├── EmptyTitleError
    │   └── InvalidIDError
    ├── NotFoundError (task ID doesn't exist)
    └── RepositoryError (storage failures)
```

**Error Message Format**:
- User-facing: "Title cannot be empty. Please provide a title for your task."
- Includes: What happened + Why it's wrong + What to do next
- No stack traces in user output (logged only)

**References**:
- Python exception best practices: PEP 3151

---

### 8. ID Generation Strategy

**Decision**: Max-based auto-increment with atomic counter

**Rationale**:
- FR-005: Unique auto-incrementing IDs starting from 1
- FR-006: Maintain sequence even after deletions
- In-memory: Simple counter tracking max ID ever assigned
- Thread-safe not required (single-user per spec assumption)

**Implementation**:
```python
# Pseudocode
class InMemoryTaskRepository:
    _tasks: dict[int, Task] = {}
    _next_id: int = 1

    def add(self, task: Task) -> Task:
        task.id = self._next_id
        self._tasks[task.id] = task
        self._next_id += 1
        return task
```

**Edge Case**: After deleting tasks 1-5, next task gets ID 6 (spec requirement)

---

### 9. Data Validation Strategy

**Decision**: Service layer validation + Pydantic models

**Rationale**:
- FR-002, FR-003, FR-004: Multiple validation requirements
- Pydantic provides automatic validation with type safety
- Service layer enforces business rules (empty title, ID existence)
- Repository layer is validation-free (assumes pre-validated data)

**Validation Points**:
- **Model level** (Pydantic): Type constraints, required fields
- **Service level**: Business rules (title non-empty, ID exists)
- **UI level**: Input parsing (numeric IDs, menu options)

**References**:
- Pydantic validation: https://docs.pydantic.dev/

---

### 10. Performance Targets

**Decision**: In-memory operations with O(1) lookups via dict

**Rationale**:
- SC-002: Display under 1 second for 1000 tasks
- SC-007: All operations respond within 1 second
- Dict-based storage: O(1) lookup by ID
- List comprehension for get_all: O(n) but <1ms for 1000 items

**Memory Budget**:
- Task object: ~500 bytes (ID + title 200 chars + description 1000 chars + status)
- 1000 tasks: ~500KB
- 10,000 tasks: ~5MB (well under 10MB constraint per spec)

**Optimization**: No sorting overhead (dict maintains insertion order Python 3.7+, manual sort for display only)

---

## Unresolved Questions

**None** - All technical decisions resolved. Specification provides sufficient detail for implementation.

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| Rich library ANSI compatibility issues | Low | Medium | Test on target platforms; fallback to plain text if needed |
| Typer interactive prompts UX issues | Low | High | Prototype menu flow early; user testing in task validation |
| mypy strict mode friction | Medium | Low | Start strict from day 1; fix incrementally if needed |
| ID overflow edge case | Very Low | Low | Document assumption (Python int unlimited) |

---

## Next Steps

Proceed to **Phase 1: Design & Contracts**:
1. Create `data-model.md` with Task and TaskRepository entities
2. Define service layer contracts (TaskService)
3. Document quickstart guide for development setup
4. Generate checklist for implementation readiness
