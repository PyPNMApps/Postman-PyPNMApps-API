# Tools

Project utilities live under `tools/` to keep the repository root clean.

## Setup

Create the local virtual environment and install dev dependencies:

```bash
./install.sh
```

## Sanitization Tool

Path:

- `tools/sanitize.py`

Purpose:

- Sanitizes example data in `visual/` (`.json` and `.html`)
- Rewrites MAC addresses to generic placeholders
- Normalizes `system_description` / sysDescr fields to PyPNM defaults

Usage:

```bash
.venv/bin/python tools/sanitize.py --check
.venv/bin/python tools/sanitize.py --fix
```

Modes:

- `--check` : read-only, reports findings, exits non-zero when changes would be needed
- `--fix` : applies changes in-place

## Version Bump Tool

Path:

- `tools/support/bump_version.py`

Purpose:

- Keeps `VERSION` and `pyproject.toml` `[project].version` synchronized

Usage:

```bash
.venv/bin/python tools/support/bump_version.py --version 0.1.1 --check
.venv/bin/python tools/support/bump_version.py --version 0.1.1
```

## Release Tool

Path:

- `tools/release/release.py`

Purpose:

- Common release workflow helper (branch checks, clean worktree checks, quality gates, version bump, tag creation)

Usage:

```bash
.venv/bin/python tools/release/release.py --version-info
.venv/bin/python tools/release/release.py --no-push
.venv/bin/python tools/release/release.py --version 0.1.1 --no-push
```

## Git Convenience Tools

Paths:

- `tools/git/git-save.sh`
- `tools/git/git-push.sh`

Examples:

```bash
./tools/git/git-save.sh --commit-msg "Update visuals"
./tools/git/git-save.sh --commit-msg "Update visuals" --push
./tools/git/git-push.sh --commit-msg "Auto sync docs"
```

These run local quality checks before commit/push:

- `tools/sanitize.py --check`
- `pytest -q`
