# TDD Project Task Runner
# Usage: just <task>
#
# QUALITY GATES:
#   - check       : Run strict checks (what hooks enforce)
#   - check-all   : Run all checks including advisory tools (sourcery)
#   - ci          : Full CI simulation (check + test-cov)

# Default task - show available tasks
default:
    @just --list

# ===========================================================================
# TESTING
# ===========================================================================

# Run all tests
test *ARGS:
    uv run pytest {{ARGS}}

# Run tests with coverage
test-cov:
    uv run pytest --cov --cov-report=term-missing --cov-report=html

# Run tests for a specific file or pattern
test-file FILE:
    uv run pytest {{FILE}} -v

# ===========================================================================
# STRICT QUALITY CHECKS (enforced by hooks)
# ===========================================================================

# Run linting with ruff
lint:
    uv run ruff check src tests

# Run linting and auto-fix issues
lint-fix:
    uv run ruff check src tests --fix

# Check code formatting
format-check:
    uv run ruff format src tests --check

# Format code
format:
    uv run ruff format src tests

# Run type checking with ty
types:
    uvx ty check src tests

# Run all strict quality checks (same as pre-commit hooks)
check: lint format-check types
    @echo ""
    @echo "✅ All strict checks passed!"

# ===========================================================================
# SOURCERY CODE REVIEW (blocking when token available)
# ===========================================================================

# Run sourcery on changed files (diff from main)
sourcery-review:
    @echo "Running Sourcery review (changed files)..."
    @if [ -n "$$SOURCERY_TOKEN" ]; then \
        uvx sourcery login --token "$$SOURCERY_TOKEN" && \
        uvx sourcery review --diff "git diff main" --check . ; \
    else \
        echo "SOURCERY_TOKEN not set, skipping"; \
    fi

# Run sourcery on full codebase (use before PR)
sourcery-full:
    @echo "Running Sourcery full codebase review..."
    @if [ -n "$$SOURCERY_TOKEN" ]; then \
        uvx sourcery login --token "$$SOURCERY_TOKEN" && \
        uvx sourcery review --check . ; \
    else \
        echo "SOURCERY_TOKEN not set, skipping"; \
    fi

# Login to sourcery (requires SOURCERY_TOKEN env var)
sourcery-login:
    @if [ -z "$$SOURCERY_TOKEN" ]; then echo "Error: SOURCERY_TOKEN not set"; exit 1; fi
    uvx sourcery login --token "$$SOURCERY_TOKEN"

# Run all checks including sourcery
check-all: check sourcery-review
    @echo ""
    @echo "All checks (strict + sourcery) passed!"

# ===========================================================================
# HOOKS & CI
# ===========================================================================

# Install prek git hooks
hooks-install:
    uvx prek install

# Run all prek hooks on staged files
hooks-run:
    uvx prek run

# Run all prek hooks on all files
hooks-run-all:
    uvx prek run --all-files

# Run pre-push hooks (pytest)
hooks-push:
    uvx prek run --hook-stage pre-push --all-files

# Validate prek config
hooks-validate:
    uvx prek validate-config

# Full CI simulation locally (use before pushing)
ci: hooks-run-all test-cov
    @echo ""
    @echo "✅ All CI checks passed locally!"

# ===========================================================================
# DEVELOPMENT
# ===========================================================================

# Install development dependencies
install:
    uv sync --all-extras
    @just hooks-install

# Clean build artifacts
clean:
    rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache __pycache__
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true

# ===========================================================================
# GIT WORKTREES
# ===========================================================================

# Create a new feature worktree
worktree-new NAME:
    git worktree add ../{{NAME}} -b feat/{{NAME}}
    @echo "Created worktree at ../{{NAME}} on branch feat/{{NAME}}"
    @echo "cd ../{{NAME}} to start working"

# Remove a feature worktree
worktree-remove NAME:
    git worktree remove ../{{NAME}}
    @echo "Removed worktree ../{{NAME}}"

# List all worktrees
worktree-list:
    git worktree list

# ===========================================================================
# PR WORKFLOW
# ===========================================================================

# Create PR for current branch
pr TITLE:
    gh pr create --title "{{TITLE}}" --body "$(cat <<'PREOF'
## Summary

<!-- Describe the changes -->

## Test plan

- [ ] All tests pass
- [ ] Coverage maintained
- [ ] Linting passes
- [ ] Type checking passes

---
Generated with Claude Code TDD Workflow
PREOF
)"

# Run all checks before creating a PR
pre-pr: check test-cov
    @echo ""
    @echo "✅ All pre-PR checks passed!"
    @echo "Ready to create PR with: just pr 'title'"

# Full pre-PR with blocking sourcery review
pre-pr-full: pre-pr sourcery-full
    @echo ""
    @echo "All checks including full Sourcery review passed!"
