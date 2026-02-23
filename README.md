# Postman PyPNMApps API Collections

This repository contains Postman collections, environment/globals files, and example visualizers for PyPNM API workflows.

## What This Repo Provides

- `postman/collections/PyPNM.postman_collection.json` (primary collection)
- `postman/collections/PyPNM-CMTS.postman_collection.json` (placeholder shell)
- `postman/environments/PyPNM Remote Server.postman_environment.json`
- `postman/globals/workspace.postman_globals.json`
- `visual/` example Postman Visualizer templates + sample data

## Basic Setup

1. Install Postman Desktop: `https://www.postman.com/downloads/`
2. Clone this repository:

```bash
git clone https://github.com/PyPNMApps/Postman-PyPNMApps-API.git
cd Postman-PyPNMApps-API
```

3. In Postman, import:
   - `postman/collections/PyPNM.postman_collection.json`
   - `postman/collections/PyPNM-CMTS.postman_collection.json`
   - `postman/environments/PyPNM Remote Server.postman_environment.json`
   - `postman/globals/workspace.postman_globals.json`

4. Set `pypnm_url` in Postman Globals (example: `http://127.0.0.1:8000`)

Important:
- Collection requests use `{{pypnm_url}}` (global), while the provided environment includes `base_url`.

## Local Tooling (Repo Maintenance)

This repo uses local Python tooling in `tools/` for sanitization, versioning, and release workflows.

```bash
./install.sh
```

Common commands:

```bash
.venv/bin/python tools/sanitize.py --check
.venv/bin/python tools/sanitize.py --fix
.venv/bin/python tools/support/bump_version.py --version 0.1.1 --check
.venv/bin/python tools/release/release.py --version-info
./tools/git/git-save.sh --help
./tools/git/git-push.sh --help
```

Version source of truth:
- `VERSION` (must stay in sync with `pyproject.toml`)

## Documentation

Detailed instructions were moved to `docs/`:

- `docs/docs-index.md` (docs index)
- `docs/user-guide.md` (full Postman import/use walkthrough)
- `docs/tools.md` (sanitize/version/release/git helpers)
- `docs/release.md` (release process and versioning)
