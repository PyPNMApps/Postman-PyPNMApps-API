# Tools

Project utilities live under `tools/` to keep the repository root clean.

See also:

- `docs/visual-workflow.md` for the recommended visual edit -> Postman sync -> docs workflow
- `docs/postman-collection-format.md` for local YAML Postman conventions and migration notes

## Setup

Create the local virtual environment and install dev dependencies:

```bash
./install.sh
source .venv/bin/activate
```

Notes:

- `./install.sh` prints Windows (PowerShell) command examples by default
- use `./install.sh --os-linux` to print Linux/macOS command examples

## Visual Docs Generator (MkDocs)

Path:

- `tools/docs/build_visual_docs.py`

Purpose:

- Scans `visual/` for `.html` + `.json` examples
- Generates MkDocs pages under `docs/visual/`
- Generates local preview wrappers under `docs/visual-previews/`

Usage:

```bash
tools/docs/build_visual_docs.py
tools/docs/build_visual_docs.py --check
mkdocs serve -a 127.0.0.1:8030
```

Notes:

- In this version, `visual/` is the source of truth for both visualizer HTML/script and sample data.
- Preview rendering uses a lightweight Postman API shim and is best-effort.

## Sanitization Tool

Path:

- `tools/sanitize.py`

Purpose:

- Sanitizes example data in `visual/` (`.json` and `.html`)
- Rewrites MAC addresses to generic placeholders
- Normalizes `system_description` / sysDescr fields to PyPNM defaults

Usage:

```bash
tools/sanitize.py --check
tools/sanitize.py --check-pass-fail
tools/sanitize.py --fix
```

Modes:

- `--check` : read-only, reports findings, exits non-zero when changes would be needed
- `--check-pass-fail` : read-only, reports findings, always exits zero
- `--fix` : applies changes in-place

## Postman Visualizer Sync Tool

Path:

- `tools/postman/sync_visualizers.py`

Purpose:

- Syncs Postman request visualizer scripts from `visual/**/*.html` into local YAML request files
- Treats request header mapping (`// Postman Visualizer: ...`) as source for HTML path resolution
- Detects drift between `visual/` HTML and `postman/collections/**/.request.yaml`

Usage:

```bash
tools/postman/sync_visualizers.py --check
tools/postman/sync_visualizers.py --update
```

Modes:

- `--check` : read-only, exits non-zero if visualizer scripts drift from `visual/`
- `--update` : updates request YAML `scripts[].code` from matched HTML files

## Version Bump Tool

Path:

- `tools/support/bump_version.py`

Purpose:

- Keeps `VERSION` and `pyproject.toml` `[project].version` synchronized

Usage:

```bash
tools/support/bump_version.py --version 0.1.1 --check
tools/support/bump_version.py --version 0.1.1
```

## Release Tool

Path:

- `tools/release/release.py`

Purpose:

- Common release workflow helper (branch checks, clean worktree checks, quality gates, version bump, tag creation)

Usage:

```bash
tools/release/release.py --version-info
tools/release/release.py --no-push
tools/release/release.py --version 0.1.1 --no-push
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
- `tools/postman/sync_visualizers.py --check`
- `pytest -q`
