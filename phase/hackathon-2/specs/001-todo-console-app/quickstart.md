# Quickstart Guide: Todo In-Memory Python Console App

**Feature**: 001-todo-console-app
**Date**: 2025-12-07
**Target Audience**: Developers implementing or testing the application

## Overview

This guide provides step-by-step instructions for setting up the development environment, running the application, executing tests, and validating Constitutional compliance.

---

## Prerequisites

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.13 or higher
- **Terminal**: Any ANSI-compatible terminal (Windows Terminal, iTerm2, GNOME Terminal)
- **Git**: For version control (optional but recommended)

### Package Manager

- **uv**: Install from https://github.com/astral-sh/uv

**Installation**:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

---

## Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-app
git checkout 001-todo-console-app
```

### 2. Create Virtual Environment

```bash
# Create virtual environment using uv
uv venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all dependencies from pyproject.toml
uv pip install -e ".[dev]"

# Verify installation
python -c "import rich; import typer; import pytest; print('Dependencies OK')"
```

**Expected dependencies**:
- `rich`: Terminal UI formatting
- `typer`: CLI framework
- `pydantic`: Data validation
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `mypy`: Type checking

---

## Running the Application

### Launch Todo App

```bash
# From project root
python -m src.app

# Or if installed as package
todo-app
```

**Expected Output**:
```
╔════════════════════════════════════╗
║      Todo Console Application      ║
╚════════════════════════════════════╝

Main Menu:
  1. Add Task
  2. List Tasks
  3. Update Task
  4. Delete Task
  5. Toggle Task Completion
  6. Exit

Select an option [1-6]:
```

### Basic Usage Flow

**1. Add a Task**:
```
Select: 1
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task created successfully! ID: 1
```

**2. List Tasks**:
```
Select: 2

┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Description      ┃ Status    ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 1  │ Buy groceries  │ Milk, eggs, bread│ PENDING   │
└────┴────────────────┴──────────────────┴───────────┘
```

**3. Toggle Completion**:
```
Select: 5
Enter task ID: 1
✓ Task 1 marked as COMPLETED

# List again shows:
│ 1  │ Buy groceries  │ Milk, eggs, bread│ ✓ COMPLETED │
```

**4. Exit**:
```
Select: 6
Goodbye! Your tasks will not be saved.
```

---

## Development Workflow

### Run Type Checking

```bash
# Run mypy in strict mode (Constitutional requirement)
mypy src tests --strict

# Expected: Success: no issues found
```

**Configuration** (in `pyproject.toml`):
```toml
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Run Tests

**All Tests**:
```bash
pytest

# Expected output:
# ===== test session starts =====
# collected 47 items
# tests/unit/test_models.py ......
# tests/unit/test_repository.py .........
# tests/unit/test_service.py ..............
# tests/integration/test_user_stories.py ............
# ===== 47 passed in 1.23s =====
```

**With Coverage**:
```bash
pytest --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

**Target Coverage**: 90%+ (Constitutional Definition of Done)

**Specific Test Categories**:
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific user story
pytest tests/integration/test_user_stories.py::test_create_and_view_tasks

# Edge cases
pytest tests/unit/test_service.py::test_empty_title_validation
```

### Run Linting

```bash
# Ruff (fast Python linter)
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

---

## Validation Checklist

### Constitutional Compliance Check

Run these commands to validate against Project Constitution:

**1. Type Safety (Principle X: NON-NEGOTIABLE)**:
```bash
mypy src tests --strict
# MUST PASS with zero errors
```

**2. Test Coverage (Principle VIII: TDD)**:
```bash
pytest --cov=src --cov-report=term
# MUST be ≥90% coverage
```

**3. Spec Alignment (Principle I: Spec-First)**:
```bash
# Manually verify user stories from spec.md
pytest tests/integration/test_user_stories.py -v
# ALL user story tests MUST PASS
```

**4. Clean Build (Definition of Done)**:
```bash
# Run all quality gates
./scripts/validate.sh

# Or manually:
mypy src tests --strict && \
pytest --cov=src && \
ruff check src tests
```

### Performance Validation (Success Criteria)

**SC-002: Display 1000 tasks in <1 second**:
```bash
pytest tests/performance/test_performance.py::test_list_1000_tasks
```

**SC-007: All operations in <1 second**:
```bash
pytest tests/performance/test_performance.py::test_operation_timing
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'rich'`

**Solution**:
```bash
# Reinstall dependencies
uv pip install -e ".[dev]"

# Verify virtual environment is activated
which python  # Should show .venv/bin/python
```

### Issue: mypy errors `Cannot find implementation or library stub`

**Solution**:
```bash
# Install type stubs
uv pip install types-all

# Or specific stubs
uv pip install types-setuptools
```

### Issue: Rich table not displaying colors

**Solution**:
- Ensure terminal supports ANSI codes
- Windows: Use Windows Terminal or enable ANSI in CMD
- Test: `python -c "from rich.console import Console; Console().print('[green]OK[/green]')"`

### Issue: Tests failing with `RepositoryError`

**Solution**:
```bash
# Clear any cached bytecode
find . -type d -name "__pycache__" -exec rm -r {} +

# Re-run tests with verbose output
pytest -vv tests/
```

---

## Project Structure Reference

```
todo-app/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task, TaskStatus
│   │   └── exceptions.py    # Custom exceptions
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── protocol.py      # TaskRepositoryProtocol
│   │   └── in_memory.py     # InMemoryTaskRepository
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # TaskService
│   ├── ui/
│   │   ├── __init__.py
│   │   └── renderer.py      # Rich table rendering
│   └── app.py               # Typer CLI entry point
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_repository.py
│   │   └── test_service.py
│   ├── integration/
│   │   └── test_user_stories.py
│   └── performance/
│       └── test_performance.py
├── specs/
│   └── 001-todo-console-app/
│       ├── spec.md
│       ├── plan.md
│       ├── data-model.md
│       ├── research.md
│       ├── quickstart.md (this file)
│       └── contracts/
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## Next Steps After Setup

### For Developers

1. **Read the spec**: `specs/001-todo-console-app/spec.md`
2. **Review data model**: `specs/001-todo-console-app/data-model.md`
3. **Study contracts**: `specs/001-todo-console-app/contracts/service-contracts.md`
4. **Run implementation**: `/sp.tasks` to generate task breakdown
5. **Start TDD cycle**: Red → Green → Refactor for each task

### For Testers

1. Run all tests: `pytest -v`
2. Check coverage: `pytest --cov=src --cov-report=html`
3. Test user stories manually (follow spec.md scenarios)
4. Validate edge cases (spec.md edge cases section)
5. Performance testing: `pytest tests/performance/`

### For Reviewers

1. Verify Constitutional compliance (see checklist above)
2. Check type safety: `mypy src tests --strict`
3. Review test coverage report
4. Validate spec alignment (user stories vs tests)
5. Confirm Definition of Done criteria met

---

## Support & Resources

**Documentation**:
- Project Constitution: `.specify/memory/constitution.md`
- Feature Specification: `specs/001-todo-console-app/spec.md`
- Implementation Plan: `specs/001-todo-console-app/plan.md`

**External References**:
- Rich documentation: https://rich.readthedocs.io/
- Typer documentation: https://typer.tiangolo.com/
- pytest documentation: https://docs.pytest.org/
- mypy documentation: https://mypy.readthedocs.io/

**Tools**:
- uv package manager: https://github.com/astral-sh/uv
- Python 3.13 docs: https://docs.python.org/3.13/

---

## Quick Reference Commands

```bash
# Setup
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"

# Run app
python -m src.app

# Quality gates (must all pass)
mypy src tests --strict
pytest --cov=src
ruff check src tests

# Full validation
./scripts/validate.sh  # or run commands above manually
```

**Status indicators**:
- ✅ All green: Ready for implementation
- ⚠️ Warnings: Review and fix
- ❌ Errors: Blocks implementation

---

**Last Updated**: 2025-12-07
**Status**: Ready for implementation phase
