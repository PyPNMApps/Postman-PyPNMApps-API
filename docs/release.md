# Release and Versioning

## Source of Truth

The repository version source of truth is the root `VERSION` file.

- `VERSION` contains `X.Y.Z`
- `pyproject.toml` `[project].version` must match `VERSION`

Do not manually update only one of them.

## Bump Version

Use the bump tool to keep both files synchronized:

```bash
.venv/bin/python tools/support/bump_version.py --version 0.1.1 --check
.venv/bin/python tools/support/bump_version.py --version 0.1.1
```

## Release Flow

Use:

```bash
.venv/bin/python tools/release/release.py --no-push
```

What it does:

1. Ensures you are in `Postman-PyPNMApps-API`
2. Ensures branch is `main` or `hot-fix`
3. Ensures worktree is clean
4. Runs quality gates:
   - `tools/support/bump_version.py --check` using current `VERSION`
   - `tools/sanitize.py --check`
   - `pytest -q`
5. Resolves the release version (auto-increment patch from `VERSION`, unless `--version` is provided)
6. Updates `VERSION` and `pyproject.toml`
7. Creates an empty release commit (if needed) and an annotated `vX.Y.Z` tag
8. Pushes branch and tag unless `--no-push` is used

## Recommended Sequence

```bash
.venv/bin/python tools/sanitize.py --check
.venv/bin/python -m pytest -q
.venv/bin/python tools/support/bump_version.py --version 0.1.1 --check
.venv/bin/python tools/release/release.py --version 0.1.1 --no-push
```
