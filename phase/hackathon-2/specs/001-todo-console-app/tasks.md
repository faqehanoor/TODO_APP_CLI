---

description: "Task list for Todo In-Memory Python Console App implementation"
---

# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/, research.md

**Tests**: Tests are included as this follows TDD approach per plan.md Constitutional requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan with src/, tests/, scripts/ directories
- [ ] T002 Initialize Python project with uv (pyproject.toml with dependencies: rich>=13.7.0, typer>=0.12.0, pydantic>=2.6.0)
- [ ] T003 [P] Add development dependencies to pyproject.toml (pytest>=8.0.0, pytest-cov>=4.1.0, mypy>=1.8.0, ruff>=0.2.0)
- [ ] T004 [P] Configure mypy in pyproject.toml with strict=true, python_version="3.13"
- [ ] T005 [P] Configure pytest in pyproject.toml with testpaths=["tests"], addopts="-v --strict-markers"
- [ ] T006 [P] Configure ruff in pyproject.toml with line-length=100, target-version="py313"
- [ ] T007 [P] Create .gitignore with __pycache__/, .venv/, *.pyc, .pytest_cache/, .mypy_cache/, htmlcov/, .coverage
- [ ] T008 [P] Create README.md with project overview and link to quickstart.md
- [ ] T009 Create scripts/validate.sh with type checking, testing, and linting commands

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 [P] Create src/__init__.py as empty package marker
- [ ] T011 [P] Create src/models/__init__.py as empty package marker
- [ ] T012 [P] Implement TaskStatus enum in src/models/task.py with PENDING and COMPLETED values
- [ ] T013 Implement Task model in src/models/task.py using Pydantic BaseModel with id, title, description, status fields
- [ ] T014 [P] Implement custom exception hierarchy in src/models/exceptions.py (TodoAppError, ValidationError, EmptyTitleError, InvalidIDError, NotFoundError, RepositoryError)
- [ ] T015 [P] Create src/storage/__init__.py as empty package marker
- [ ] T016 Implement TaskRepositoryProtocol in src/storage/protocol.py with add, get_all, get_by_id, update, delete, toggle_status methods
- [ ] T017 [P] Create src/services/__init__.py as empty package marker
- [ ] T018 [P] Create src/ui/__init__.py as empty package marker
- [ ] T019 [P] Create tests/__init__.py as empty package marker
- [ ] T020 [P] Create tests/unit/__init__.py as empty package marker
- [ ] T021 [P] Create tests/integration/__init__.py as empty package marker
- [ ] T022 [P] Create tests/performance/__init__.py as empty package marker
- [ ] T023 Create tests/conftest.py with pytest fixtures for sample tasks and repository instances

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create & View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with titles/descriptions and view them in rich table format

**Independent Test**: Launch app, add multiple tasks, list to verify rich table formatting with proper columns and sorting

### Tests for User Story 1 (TDD: Write FIRST, ensure they FAIL) ⚠️

- [ ] T024 [P] [US1] Write unit test for Task model validation in tests/unit/test_models.py (test_task_creation, test_empty_title_rejected, test_whitespace_title_rejected)
- [ ] T025 [P] [US1] Write unit test for TaskStatus enum in tests/unit/test_models.py (test_status_values, test_default_pending)
- [ ] T026 [P] [US1] Write integration test for create and view flow in tests/integration/test_user_stories.py::test_create_and_view_tasks
- [ ] T027 [P] [US1] Write integration test for empty list handling in tests/integration/test_user_stories.py::test_list_empty_tasks

### Implementation for User Story 1

- [ ] T028 [US1] Implement InMemoryTaskRepository.add() in src/storage/in_memory.py with auto-increment ID logic (max(ids) + 1)
- [ ] T029 [US1] Implement InMemoryTaskRepository.get_all() in src/storage/in_memory.py with sorting by ID ascending
- [ ] T030 [US1] Implement TaskService.create_task() in src/services/task_service.py with title validation and EmptyTitleError handling
- [ ] T031 [US1] Implement TaskService.list_tasks() in src/services/task_service.py calling repository.get_all()
- [ ] T032 [US1] Implement RichTableRenderer in src/ui/renderer.py to format tasks as Rich table with ID, Title, Description, Status columns
- [ ] T033 [US1] Implement MenuHandler.show_menu() in src/ui/menu.py to display numbered menu options (1-6)
- [ ] T034 [US1] Implement MenuHandler.prompt_add_task() in src/ui/menu.py with Typer prompts for title and description
- [ ] T035 [US1] Implement MenuHandler.display_tasks() in src/ui/menu.py calling RichTableRenderer for output
- [ ] T036 [US1] Implement main application loop in src/app.py with Typer CLI and menu routing to add/list operations
- [ ] T037 [US1] Add empty list friendly message "No tasks found. Add your first task to get started!" in src/ui/renderer.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP COMPLETE)

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can toggle task status between PENDING and COMPLETED with visual feedback (green checkmark ✓)

**Independent Test**: Create task, toggle status, list to verify green checkmark for completed tasks

### Tests for User Story 2 (TDD: Write FIRST, ensure they FAIL) ⚠️

- [ ] T038 [P] [US2] Write unit test for toggle_status in tests/unit/test_repository.py (test_toggle_pending_to_completed, test_toggle_completed_to_pending)
- [ ] T039 [P] [US2] Write unit test for toggle on non-existent ID in tests/unit/test_service.py (test_toggle_not_found_error)
- [ ] T040 [P] [US2] Write integration test for toggle completion flow in tests/integration/test_user_stories.py::test_mark_tasks_complete

### Implementation for User Story 2

- [ ] T041 [US2] Implement InMemoryTaskRepository.get_by_id() in src/storage/in_memory.py returning Task or None
- [ ] T042 [US2] Implement InMemoryTaskRepository.toggle_status() in src/storage/in_memory.py (PENDING ↔ COMPLETED, raise NotFoundError if not exist)
- [ ] T043 [US2] Implement TaskService.toggle_task_status() in src/services/task_service.py with ID existence validation
- [ ] T044 [US2] Add green checkmark (✓) rendering for COMPLETED status in src/ui/renderer.py using Rich green color markup
- [ ] T045 [US2] Implement MenuHandler.prompt_toggle_task() in src/ui/menu.py with Typer prompt for task ID
- [ ] T046 [US2] Add toggle completion menu option (5) routing in src/app.py main loop

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can update task titles and/or descriptions while preserving ID and status

**Independent Test**: Create task, update title/description, list to verify changes saved and ID/status unchanged

### Tests for User Story 3 (TDD: Write FIRST, ensure they FAIL) ⚠️

- [ ] T047 [P] [US3] Write unit test for repository update in tests/unit/test_repository.py (test_update_title, test_update_description, test_update_both)
- [ ] T048 [P] [US3] Write unit test for update validation in tests/unit/test_service.py (test_update_empty_title_error, test_update_preserves_status)
- [ ] T049 [P] [US3] Write integration test for update flow in tests/integration/test_user_stories.py::test_update_task_details

### Implementation for User Story 3

- [ ] T050 [US3] Implement InMemoryTaskRepository.update() in src/storage/in_memory.py with partial update logic (None = no change)
- [ ] T051 [US3] Implement TaskService.update_task() in src/services/task_service.py with title validation and NotFoundError handling
- [ ] T052 [US3] Implement MenuHandler.prompt_update_task() in src/ui/menu.py with Typer prompts for ID, new title, new description
- [ ] T053 [US3] Add update task menu option (3) routing in src/app.py main loop

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Remove Unwanted Tasks (Priority: P3)

**Goal**: Users can delete tasks by ID, maintaining ID sequence integrity (no ID reuse)

**Independent Test**: Create multiple tasks, delete specific IDs, list to verify deletion and remaining tasks unchanged, add new task to verify ID sequence continues

### Tests for User Story 4 (TDD: Write FIRST, ensure they FAIL) ⚠️

- [ ] T054 [P] [US4] Write unit test for repository delete in tests/unit/test_repository.py (test_delete_existing, test_delete_not_found, test_id_sequence_after_delete)
- [ ] T055 [P] [US4] Write unit test for delete validation in tests/unit/test_service.py (test_delete_not_found_error)
- [ ] T056 [P] [US4] Write integration test for delete flow in tests/integration/test_user_stories.py::test_remove_unwanted_tasks

### Implementation for User Story 4

- [ ] T057 [US4] Implement InMemoryTaskRepository.delete() in src/storage/in_memory.py returning bool (True if deleted, False if not found)
- [ ] T058 [US4] Implement TaskService.delete_task() in src/services/task_service.py with ID existence validation and NotFoundError
- [ ] T059 [US4] Implement MenuHandler.prompt_delete_task() in src/ui/menu.py with Typer prompt for task ID
- [ ] T060 [US4] Add delete task menu option (4) routing in src/app.py main loop

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Edge Cases & Error Handling

**Purpose**: Implement all edge cases from spec.md to ensure robust error handling

- [ ] T061 [P] Add validation for whitespace-only titles in src/services/task_service.py (strip and check length > 0)
- [ ] T062 [P] Add validation for non-numeric ID input in src/ui/menu.py with InvalidIDError and user-friendly message "Invalid ID format. Please enter a numeric ID (e.g., 1, 2, 3)."
- [ ] T063 [P] Add handling for very long title/description in src/ui/renderer.py (truncate display to maintain table formatting, full text still stored)
- [ ] T064 [P] Add validation to reject description-only task creation (title required) in src/services/task_service.py
- [ ] T065 Implement empty description on update behavior (None means no change) in src/storage/in_memory.py

---

## Phase 8: Performance & Polish

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T066 [P] Write performance test for 1000 tasks list in tests/performance/test_performance.py (verify <1 second per SC-002)
- [ ] T067 [P] Write performance test for all CRUD operations in tests/performance/test_performance.py (verify <1 second per SC-007)
- [ ] T068 [P] Add exit menu option (6) in src/app.py with goodbye message "Goodbye! Your tasks will not be saved."
- [ ] T069 [P] Add docstrings to all public methods in src/models/, src/services/, src/storage/ (Google-style docstrings)
- [ ] T070 [P] Run mypy --strict on src/ tests/ and fix all type errors to achieve zero errors (SC-006)
- [ ] T071 [P] Run pytest --cov=src --cov-report=term and verify ≥90% coverage
- [ ] T072 [P] Run ruff check src/ tests/ and fix all linting issues
- [ ] T073 Validate quickstart.md instructions by running through full setup on fresh environment
- [ ] T074 Create .env.example file (empty for Phase I, placeholder for Phase II database config)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P3)
- **Edge Cases (Phase 7)**: Depends on user stories being functional
- **Performance & Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses same models/repo)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses same models/repo)
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses same models/repo)

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Repository methods before service methods
- Service methods before UI components
- UI components before app.py routing
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T009)
- All Foundational tasks marked [P] can run in parallel within constraints (T010-T022)
- Once Foundational phase completes, **all 4 user stories can start in parallel** (ideal for team)
- All tests for a user story marked [P] can run in parallel (write tests together)
- Edge case tasks marked [P] can run in parallel (T061-T064)
- Performance & Polish tasks marked [P] can run in parallel (T066-T074)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T024: "Write unit test for Task model validation"
Task T025: "Write unit test for TaskStatus enum"
Task T026: "Write integration test for create and view flow"
Task T027: "Write integration test for empty list handling"

# After tests written and failing, implement models in parallel:
(Models are foundational - completed in Phase 2)

# Then implement repository and service in sequence:
Task T028: "Implement InMemoryTaskRepository.add()"
Task T029: "Implement InMemoryTaskRepository.get_all()"
Task T030: "Implement TaskService.create_task()"
Task T031: "Implement TaskService.list_tasks()"

# Then implement UI components in sequence:
Task T032: "Implement RichTableRenderer"
Task T033: "Implement MenuHandler.show_menu()"
Task T034: "Implement MenuHandler.prompt_add_task()"
Task T035: "Implement MenuHandler.display_tasks()"
Task T036: "Implement main application loop"
Task T037: "Add empty list friendly message"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T023) **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T024-T037)
4. **STOP and VALIDATE**: Run tests, manually test User Story 1
5. Demo/validate before proceeding

**MVP Deliverable**: Add tasks and list them in rich table format ✅

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T023)
2. Add User Story 1 → Test independently → MVP! (T024-T037)
3. Add User Story 2 → Test independently → Enhanced value (T038-T046)
4. Add User Story 3 → Test independently → Quality of life (T047-T053)
5. Add User Story 4 → Test independently → Complete CRUD (T054-T060)
6. Add Edge Cases → Robustness (T061-T065)
7. Add Performance & Polish → Production ready (T066-T074)

Each phase adds value without breaking previous work.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T023)
2. Once Foundational is done, split:
   - **Developer A**: User Story 1 (T024-T037) - MVP priority
   - **Developer B**: User Story 2 (T038-T046) - Run parallel
   - **Developer C**: User Story 3 (T047-T053) - Run parallel
   - **Developer D**: User Story 4 (T054-T060) - Run parallel
3. Stories complete and integrate independently
4. Team collaborates on Edge Cases + Performance & Polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- TDD: Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group with task ID in commit message
- Stop at any checkpoint to validate story independently
- Run `mypy --strict`, `pytest`, `ruff check` frequently during implementation
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Statistics

**Total Tasks**: 74
**Setup Tasks**: 9 (T001-T009)
**Foundational Tasks**: 14 (T010-T023)
**User Story 1 Tasks**: 14 (T024-T037) - MVP
**User Story 2 Tasks**: 9 (T038-T046)
**User Story 3 Tasks**: 7 (T047-T053)
**User Story 4 Tasks**: 7 (T054-T060)
**Edge Cases Tasks**: 5 (T061-T065)
**Performance & Polish Tasks**: 9 (T066-T074)

**Parallel Opportunities**: 34 tasks marked [P] can run in parallel
**Independent Stories**: All 4 user stories are independently testable after Foundational phase

---

**Tasks Status**: ✅ READY FOR TDD IMPLEMENTATION
**Last Updated**: 2025-12-07
**Branch**: 001-todo-console-app
**Next Phase**: Red-Green-Refactor cycle starting with T001
