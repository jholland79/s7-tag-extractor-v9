# Claude Code Guidelines

This project uses strict TDD with granular commits and focused PRs.

## PR Discipline

**Every PR must be small, focused, and reviewable.**

### PR Categories (never mix)

| Category | Branch Prefix | Content |
|----------|---------------|---------|
| Infrastructure | `infra/` | CI, configs, tooling |
| Fixtures | `test/` | Test data, sample files |
| Features | `feat/` | One feature per PR |

### Size Limits

- ~200 lines of code changes max
- ~5-10 files of actual code
- 1 logical feature per PR

## Commit Discipline

Each TDD cycle = 3 commits minimum:

```bash
# RED - failing test first
git commit -m "feat(scope): RED - add failing test for X"

# GREEN - minimal implementation
git commit -m "feat(scope): GREEN - implement X"

# REFACTOR - improve quality
git commit -m "feat(scope): REFACTOR - clean up X"
```

### Commit Message Format

```
<type>(<scope>): <phase> - <description>

Types: feat, fix, test, refactor, chore, docs
Phases: RED, GREEN, REFACTOR
```

## Quality Gates

Before EVERY commit:

1. `uv run pytest` - tests pass (except RED phase)
2. `just check` - linting/formatting pass
3. Changes are focused and small

## Workflow

1. Read plan section for current PR
2. Create branch: `git checkout -b feat/feature-name`
3. For each task: RED → GREEN → REFACTOR (3 commits)
4. Push and create PR: `git push -u origin HEAD && gh pr create`
5. Wait for CI, report PR URL
6. Start next PR only after current one is ready

## Anti-Patterns (AVOID)

- Batching multiple features in one commit
- Mixing infrastructure and feature code
- Adding fixtures with implementation
- 200+ file PRs
- Skipping RED phase commits
