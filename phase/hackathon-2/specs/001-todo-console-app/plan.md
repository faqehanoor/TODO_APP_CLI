# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

## Summary

Create a strictly in-memory Python console application for managing todo tasks with five core operations: Add, List, Update, Delete, and Toggle Completion. The application implements the Repository Pattern to enable future Phase II database migration, enforces strict type safety with mypy, follows Test-Driven Development with pytest, uses Rich library for terminal UI formatting, and Typer framework for CLI interactions. All business logic is separated from UI and storage layers to support the 5-phase evolutionary architecture defined in the Project Constitution.

**Primary Requirement**: Menu-driven console interface for CRUD operations on todo tasks with rich table formatting and visual completion indicators.

**Technical Approach**: Multi-layer architecture (Models → Storage → Services → UI) with Protocol-based repository abstraction enabling seamless Phase I (in-memory) to Phase II (PostgreSQL) transition without business logic changes.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: rich (terminal UI), typer (CLI framework), pydantic (data validation), pytest (testing)
**Package Manager**: uv (Constitutional requirement)
**Storage**: In-memory dictionary (Phase I), PostgreSQL-ready via repository protocol (Phase II)
**Testing**: pytest with fixtures, parameterized tests for edge cases, pytest-cov for coverage
**Target Platform**: Cross-platform console (Windows, macOS, Linux with ANSI support)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second for 1000 task operations, <100ms per CRUD operation, instant menu responsiveness
**Constraints**: No file/database persistence (in-memory only), strict type checking (mypy --strict), <10MB memory for 10,000 tasks
**Scale/Scope**: Single-user local session, max 10,000 tasks (practical in-memory limit), 200-char titles, 1000-char descriptions

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-First Development

**Status**: ✅ PASS

**Justification**: Complete feature specification exists at `specs/001-todo-console-app/spec.md` with 4 user stories, 20 functional requirements, 10 success criteria, and edge cases. Implementation plan created after spec approval. Workflow followed: Constitution → Spec → Plan → (Tasks) → Implement.

---

### II. No Manual Code

**Status**: ✅ PASS

**Justification**: All code will be AI-generated via Spec-Kit Plus following this implementation plan. Human role is architectural (specification, planning) not implementation. PHR tracking enabled for all agent sessions.

---

### III. Reusable Intelligence

**Status**: ✅ PASS

**Justification**:
- PHR created for spec generation (history/prompts/001-todo-console-app/0001-todo-console-app-specification.spec.prompt.md)
- PHR will be created for plan generation
- ADR planned for Repository Pattern decision (significant architectural choice)
- Repository Protocol pattern will be reusable across all Phase I features

---

### IV. Evolutionary Architecture

**Status**: ✅ PASS

**Justification**:
- Repository Pattern implements Protocol-based abstraction (TaskRepositoryProtocol)
- InMemoryTaskRepository (Phase I) swappable with PostgreSQLTaskRepository (Phase II)
- Business logic (TaskService) depends on Protocol, not concrete implementation
- UI layer (Typer CLI) depends on Service, not storage details
- Zero business logic changes required for Phase II migration
- See "Repository Pattern Justification" section for detailed analysis

---

### V. Single Responsibility Principle (SRP)

**Status**: ✅ PASS

**Justification**:
- **Models layer**: Task, TaskStatus (data only, no business logic)
- **Storage layer**: TaskRepositoryProtocol, InMemoryTaskRepository (storage only)
- **Services layer**: TaskService (business logic only, no UI or storage details)
- **UI layer**: Typer CLI, Rich renderer (presentation only, no business logic)
- Each module has one clear purpose, enabling independent testing and future phase reuse

---

### VI. User Experience First

**Status**: ✅ PASS

**Justification**:
- All error messages actionable with guidance (FR-018): "Title cannot be empty. Please provide a title for your task."
- Rich table formatting for readability (FR-009)
- Visual completion indicators (green checkmark ✓) (FR-010)
- Graceful empty state handling with friendly message (FR-019)
- Menu-driven interface with numbered options (FR-001)
- All 10 edge cases have defined user-friendly behaviors

---

### VII. The Checkpoint Pattern

**Status**: ✅ PASS

**Justification**: Tasks will be broken down (via `/sp.tasks`) into atomic units with independent commit points. Each task maps to single file or logical module. Task IDs will be included in commit messages for traceability.

---

### VIII. Test-Driven Development (TDD)

**Status**: ✅ PASS

**Justification**:
- 25+ acceptance scenarios defined in spec (User Stories 1-4)
- 10 edge cases with expected behaviors
- Test strategy: Red-Green-Refactor for each task
- Unit tests for models, repository, service
- Integration tests for user story flows
- Tests will be written before implementation code

---

### IX. Core Technologies (Tech Stack Alignment)

**Status**: ✅ PASS

**Justification**:
- Python 3.13+ (Constitutional requirement)
- uv package manager (Constitutional requirement)
- Stack supports Phase I (console) and Phase II (FastAPI web, PostgreSQL)
- All dependencies (rich, typer, pytest, pydantic) are production-grade and maintained

---

### X. Type Safety (NON-NEGOTIABLE)

**Status**: ✅ PASS

**Justification**:
- `mypy --strict` configured in pyproject.toml
- All functions, methods, classes will have complete type annotations
- Protocol definitions for repository interface (PEP 544)
- Pydantic models enforce runtime type validation
- FR-017: Strict type hints required
- SC-006: Zero type errors success criterion

---

### XI. Error Handling

**Status**: ✅ PASS

**Justification**:
- Custom exception hierarchy (TodoAppError → ValidationError, NotFoundError, RepositoryError)
- All exceptions include user-friendly messages with guidance (FR-018)
- No silent failures (all errors propagate with context)
- Service layer validates and raises explicit exceptions
- UI layer catches and displays error messages
- Logging context included (user action, timestamp)

---

### XII. Configuration Management

**Status**: ✅ PASS (N/A for Phase I)

**Justification**: Phase I console app has no external configuration (in-memory only). Phase II will add .env for database credentials following 12-Factor App principles. No hardcoded secrets in current phase.

---

### XIII. Definition of Done

**Status**: ✅ PASS (Gates Defined)

**Justification**: Implementation will meet all 6 criteria:
1. Constitutional Compliance: Validated above (all principles pass)
2. Spec Alignment: All FR, user stories, edge cases traceable to tests
3. Clean Build: mypy --strict, pytest --cov, ruff checks configured
4. Reproducibility: pyproject.toml + uv.lock ensure fresh clone builds
5. Documentation: PHRs, ADRs, docstrings planned
6. Phase Independence: Repository Protocol enables Phase II swap

---

**Constitution Check Summary**: ✅ ALL GATES PASSED - Ready for implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md              # Feature specification (User Stories, FR, SC)
├── plan.md              # This file (Implementation Plan)
├── research.md          # Technology decisions & rationale
├── data-model.md        # Entity definitions & validation rules
├── quickstart.md        # Development setup & validation guide
├── contracts/
│   └── service-contracts.md  # TaskService method contracts
├── checklists/
│   └── requirements.md  # Spec quality validation checklist
└── tasks.md             # Task breakdown (generated by /sp.tasks)
```

### Source Code (repository root)

```text
todo-app/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task, TaskStatus entities
│   │   └── exceptions.py    # TodoAppError, ValidationError, NotFoundError
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── protocol.py      # TaskRepositoryProtocol (interface)
│   │   └── in_memory.py     # InMemoryTaskRepository (Phase I impl)
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # TaskService (business logic)
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── renderer.py      # RichTableRenderer (Rich table formatting)
│   │   └── menu.py          # MenuHandler (interactive prompts)
│   └── app.py               # Typer CLI entry point (main menu)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures (shared repositories, tasks)
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py   # Task, TaskStatus validation tests
│   │   ├── test_repository.py # InMemoryTaskRepository tests
│   │   └── test_service.py  # TaskService business logic tests
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_user_stories.py  # End-to-end user story flows
│   └── performance/
│       ├── __init__.py
│       └── test_performance.py   # SC-002, SC-007 validation
├── scripts/
│   └── validate.sh          # Constitutional compliance validation script
├── .gitignore
├── pyproject.toml           # Project metadata, dependencies, tool configs
├── uv.lock                  # Locked dependency tree
└── README.md                # Project overview & quickstart link
```

**Structure Decision**: Single project structure chosen (Option 1 from plan template). Rationale:
- Console application with no frontend/backend separation
- All Python code in single `src/` directory
- Clear layer separation via subdirectories (models, storage, services, ui)
- Test structure mirrors source structure for discoverability
- Scales to Phase II by adding web/ or api/ sibling to src/ if needed

---

## Complexity Tracking

**Constitutional Violations**: None

**Complexity Justification**: Not required (no violations)

**Architectural Decisions Requiring ADR**:

1. **Repository Pattern Adoption** (see dedicated section below)
   - Significance: High (affects all future phases)
   - Impact: Adds abstraction layer overhead (~100 LOC)
   - Trade-off: Short-term complexity vs long-term flexibility
   - Constitutional Alignment: Principle IV (Evolutionary Architecture)

**Recommendation**: Create ADR for Repository Pattern decision post-implementation via `/sp.adr "Repository Pattern for Storage Abstraction"`

---

## Repository Pattern Justification

### Decision

Use Protocol-based Repository Pattern for storage abstraction, with InMemoryTaskRepository as Phase I concrete implementation.

### Why Required (Phase II DB Swap)

**Problem**: Phase I uses in-memory storage; Phase II requires PostgreSQL persistence. Without abstraction, Phase II migration would require:
- Rewriting all business logic (TaskService)
- Changing all UI dependencies
- Rewriting all tests
- High risk of bugs and regressions

**Solution**: Repository Pattern decouples business logic from storage mechanism.

### Benefits

1. **Phase Independence** (Constitutional Principle IV):
   - Business logic (TaskService) depends on Protocol, not implementation
   - Phase II migration: Implement PostgreSQLTaskRepository, swap in app.py
   - Zero changes to TaskService, UI, or tests (except repository tests)

2. **Testability**:
   - Mock repositories for unit testing business logic
   - Isolated storage layer testing
   - Fast test execution (no DB overhead in unit tests)

3. **Future Flexibility**:
   - Phase III: Redis caching via CachedTaskRepository
   - Phase IV: Distributed storage via DistributedTaskRepository
   - All phases reuse same Protocol interface

4. **Type Safety**:
   - Protocol (PEP 544) provides structural subtyping
   - mypy validates implementations conform to contract
   - Compile-time verification of phase compatibility

### Trade-offs

| Aspect | Cost | Benefit |
|--------|------|---------|
| Code Volume | +100 LOC (Protocol + Interface) | -500 LOC on Phase II migration |
| Learning Curve | Protocol pattern understanding | Reusable knowledge for all phases |
| Runtime Overhead | Negligible (~1-2 function calls) | <0.1ms per operation |
| Upfront Design | 1 hour additional planning | Saves 5+ hours in Phase II |

**Justification**: Benefits far outweigh costs. Constitutional Principle IV (Evolutionary Architecture) mandates this pattern. Without it, Phase II becomes a rewrite instead of an extension.

### Simpler Alternatives Rejected

1. **Direct implementation (no abstraction)**:
   - Why insufficient: Phase II requires full rewrite
   - Constitutional violation: Principle IV (Evolutionary Architecture)

2. **Abstract Base Class (ABC) instead of Protocol**:
   - Why rejected: Protocol provides structural subtyping (more flexible)
   - Protocol allows gradual typing; ABC requires explicit inheritance

3. **Deferred abstraction (add in Phase II)**:
   - Why rejected: Retrofitting abstractions is risky and time-consuming
   - Violates "design for future, implement for present" (Principle IV)

### Implementation Notes

**Protocol Definition** (src/storage/protocol.py):
```python
from typing import Protocol
from src.models.task import Task

class TaskRepositoryProtocol(Protocol):
    def add(self, task: Task) -> Task: ...
    def get_all(self) -> list[Task]: ...
    def get_by_id(self, task_id: int) -> Task | None: ...
    def update(self, task_id: int, title: str | None, description: str | None) -> Task: ...
    def delete(self, task_id: int) -> bool: ...
    def toggle_status(self, task_id: int) -> Task: ...
```

**Dependency Injection** (src/app.py):
```python
from src.storage.protocol import TaskRepositoryProtocol
from src.storage.in_memory import InMemoryTaskRepository
from src.services.task_service import TaskService

# Phase I
repository: TaskRepositoryProtocol = InMemoryTaskRepository()

# Phase II (single line change)
# repository: TaskRepositoryProtocol = PostgreSQLTaskRepository(db_url)

service = TaskService(repository)
```

### Phase II Migration Path

**What Changes**:
1. Implement PostgreSQLTaskRepository conforming to TaskRepositoryProtocol
2. Update app.py to instantiate PostgreSQL repository instead of in-memory
3. Add SQLModel models mirroring Task structure
4. Update repository tests (storage-specific tests only)

**What Stays the Same**:
- TaskService (business logic unchanged)
- Task models (fields identical)
- UI layer (Typer CLI unchanged)
- Service tests (mock repository works with both implementations)
- User-facing behavior (same menu, same commands)

**Migration Effort**: ~2 hours vs ~10 hours without Repository Pattern

---

## Design Artifacts Summary

### Phase 0: Research (COMPLETE)

**Output**: `research.md`

**Key Decisions**:
1. Typer for CLI (type-safe, interactive prompts)
2. Rich for terminal UI (tables, colors, formatting)
3. pytest for testing (fixtures, parameterization)
4. mypy --strict for type checking
5. uv for package management
6. Repository Pattern via Protocol (PEP 544)
7. Pydantic for data validation
8. Custom exception hierarchy for error handling
9. Max-based auto-increment for ID generation
10. Dict-based in-memory storage (O(1) lookups)

### Phase 1: Design & Contracts (COMPLETE)

**Outputs**:
1. `data-model.md`: Task, TaskStatus, TaskRepositoryProtocol entity definitions
2. `contracts/service-contracts.md`: TaskService method contracts, exception hierarchy
3. `quickstart.md`: Development setup, validation commands, troubleshooting

**Key Specifications**:
- Task entity: id (int), title (str), description (str), status (TaskStatus)
- TaskStatus enum: PENDING, COMPLETED
- TaskRepositoryProtocol: 6 methods (add, get_all, get_by_id, update, delete, toggle_status)
- TaskService: 6 business logic methods with validation
- Exception hierarchy: TodoAppError → ValidationError, NotFoundError, RepositoryError

---

## Implementation Readiness

### Pre-Implementation Checklist

- [x] Feature specification complete and validated (spec.md, checklists/requirements.md)
- [x] Implementation plan complete (this document)
- [x] Research complete (technology decisions documented)
- [x] Data model defined (entities, validation, state transitions)
- [x] Service contracts defined (method signatures, error handling)
- [x] Quickstart guide created (development setup, validation)
- [x] Constitution Check passed (all 13 principles validated)
- [ ] Tasks generated (run `/sp.tasks` to create task breakdown)
- [ ] ADR created for Repository Pattern (run `/sp.adr` post-implementation)

### Next Command

**Run**: `/sp.tasks`

**Purpose**: Generate task breakdown (tasks.md) organized by user story, with:
- Setup tasks (project initialization, dependencies)
- Foundational tasks (models, repository protocol)
- User Story 1 tasks (create & view - MVP)
- User Story 2 tasks (toggle completion)
- User Story 3 tasks (update task details)
- User Story 4 tasks (delete tasks)
- Polish tasks (documentation, performance validation)

**Expected Output**: `specs/001-todo-console-app/tasks.md` with 40-50 atomic tasks, parallelization markers, dependency ordering

---

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| Rich ANSI compatibility on Windows | Low | Medium | Test on Windows Terminal; provide fallback plain text mode |
| mypy strict mode friction during impl | Medium | Low | Start strict from day 1; fix incrementally per task |
| Typer interactive prompts UX issues | Low | High | Prototype menu flow early; validate against FR-001 |
| ID overflow edge case | Very Low | Low | Document Python int unlimited assumption in code |
| Performance degradation at 1000+ tasks | Low | Medium | Benchmark early; optimize dict operations if needed |

---

## Performance Budget

| Operation | Target | Budget | Validation |
|-----------|--------|--------|------------|
| Create task | <10 seconds (SC-001) | <100ms (actual op) | pytest performance test |
| List 1000 tasks | <1 second (SC-002) | <500ms (sort + render) | pytest performance test |
| Update task | <1 second (SC-007) | <50ms | pytest performance test |
| Delete task | <1 second (SC-007) | <50ms | pytest performance test |
| Toggle status | <1 second (SC-007) | <50ms | pytest performance test |
| Memory (10K tasks) | <10MB (assumption) | ~5MB (actual) | Manual validation |

**Optimization Strategy**: If performance targets missed, optimize in order:
1. Use OrderedDict or bisect for sorted storage (avoid re-sorting on each list)
2. Rich table rendering optimization (streaming instead of full render)
3. Reduce string copies in validation layer

---

## Success Validation

### Functional Validation (All User Stories)

| User Story | Validation Method |
|------------|-------------------|
| US1: Create & View Tasks (P1) | Run integration test `test_create_and_view_tasks()` |
| US2: Mark Tasks Complete (P2) | Run integration test `test_mark_tasks_complete()` |
| US3: Update Task Details (P3) | Run integration test `test_update_task_details()` |
| US4: Remove Unwanted Tasks (P3) | Run integration test `test_remove_unwanted_tasks()` |

### Success Criteria Validation (SC-001 to SC-010)

- **SC-001 to SC-010**: All validated via pytest suite (`tests/integration/`, `tests/performance/`)
- **Manual validation**: Run app, perform full user journey (add → list → toggle → update → delete → exit)
- **Type safety**: `mypy src tests --strict` (zero errors)
- **Coverage**: `pytest --cov=src --cov-report=term` (≥90%)

### Constitutional Compliance

**Final validation checklist** (before PR/merge):
```bash
# Type safety (Principle X)
mypy src tests --strict

# Test coverage (Principle VIII)
pytest --cov=src --cov-report=term

# Linting
ruff check src tests

# All tests pass
pytest -v

# Manual user story validation
python -m src.app  # Execute each user story manually
```

**Expected**: All checks pass, all user stories manually validated, ready for Phase II planning.

---

## Appendix: Dependency Tree

```toml
[project]
name = "todo-app"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "rich>=13.7.0",        # Terminal UI
    "typer>=0.12.0",       # CLI framework
    "pydantic>=2.6.0",     # Data validation
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",       # Testing framework
    "pytest-cov>=4.1.0",   # Coverage reporting
    "mypy>=1.8.0",         # Type checking
    "ruff>=0.2.0",         # Linting
]

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "T20"]
ignore = []
```

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks` command
**Last Updated**: 2025-12-07
**Branch**: 001-todo-console-app
**Next Phase**: Task generation and TDD implementation cycle
