#!/bin/bash
# Constitutional Compliance Validation Script
# Validates type safety, test coverage, and linting

set -e

echo "========================================="
echo "Constitutional Compliance Validation"
echo "========================================="
echo ""

# Type Safety (Principle X - NON-NEGOTIABLE)
echo "→ Running mypy --strict (Type Safety)..."
mypy src tests --strict
echo "✅ Type checking passed"
echo ""

# Test Coverage (Principle VIII - TDD)
echo "→ Running pytest with coverage..."
pytest --cov=src --cov-report=term --cov-report=html
echo "✅ Tests passed"
echo ""

# Linting (Code Quality)
echo "→ Running ruff check..."
ruff check src tests
echo "✅ Linting passed"
echo ""

echo "========================================="
echo "✅ ALL VALIDATION CHECKS PASSED"
echo "========================================="
