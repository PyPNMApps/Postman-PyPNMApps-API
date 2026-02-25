# Documentation

This directory contains user documentation for working with the Postman PyPNMApps API repository.

## Documents

- `docs/postman-install.md` - Postman Desktop download/install steps for Ubuntu and Windows.
- `docs/postman-import-and-navigation.md` - Import Postman files, configure globals, and navigate collections.
- `docs/postman-collection-format.md` - Format Postman collection JSON consistently on Windows/Linux.
- `docs/user-guide.md` - End-user setup and Postman import/use instructions.
- `docs/tools.md` - Local developer tooling (`sanitize`, `bump_version`, `release`, `git-save`, `git-push`).
- `docs/visual-workflow.md` - Simple workflow for editing visuals and syncing Postman visualizer scripts.
- `docs/release.md` - Versioning and release workflow (`VERSION` source of truth).
- `docs/visual/index.md` - Generated visual examples catalog (from `visual/`).
- `docs/visual-mkdocs-plan.md` - MkDocs visual catalog source-of-truth plan.

## Quick Start

1. Create the local Python virtual environment:
   - `./install.sh`
2. Activate the virtual environment:
   - `source .venv/bin/activate`
3. Run sanitization checks:
   - `tools/sanitize.py --check`
4. Review version state:
   - `cat VERSION`
5. Run tests:
   - `pytest -q`
6. Generate visual docs pages:
   - `tools/docs/build_visual_docs.py`
7. Serve docs locally:
   - `mkdocs serve -a 127.0.0.1:8030`
