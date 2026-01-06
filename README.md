# s7-tag-extractor-v9

Extract tags from Siemens Step 7 projects for OSI Pi and Kepware

## Repository Setup (First Time)

After creating this repository, configure these settings:

### 1. Enable GitHub Actions PR Creation

**Required for release-please to work.**

1. Go to Settings → Actions → General
2. Under "Workflow permissions", enable:
   - ✓ "Allow GitHub Actions to create and approve pull requests"
3. Click Save

### 2. Add Secrets (Optional but Recommended)

Go to Settings → Secrets and variables → Actions:

| Secret | Purpose |
|--------|---------|
| `CODECOV_TOKEN` | Coverage reporting |
| `SOURCERY_TOKEN` | AI code review |

### 3. Verify Setup

The `setup-check` workflow runs automatically on the first 5 pushes.
Check the Actions tab to verify everything is configured correctly.

---

## Development

### Setup

```bash
# Install dependencies
uv sync --all-extras

# Install git hooks
just hooks-install
```

### Commands

```bash
just                 # Show all available tasks
just test            # Run tests
just check           # Run strict quality checks
just check-all       # Run all checks including advisory
just ci              # Full CI simulation
```

### Quality Gates

**On commit (strict):**

- ruff (lint + format)
- ty (type check)
- taplo (TOML format)
- yamllint
- markdownlint
- conventional-commit

**On push (strict):**

- pytest (all tests must pass)

**Advisory (non-blocking):**

- sourcery (code review suggestions)
