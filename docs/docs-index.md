# Documentation

This directory contains user documentation for working with the Postman PyPNMApps API repository.

## Documents

- `docs/user-guide.md` - End-user setup and Postman import/use instructions.
- `docs/tools.md` - Local developer tooling (`sanitize`, `bump_version`, `release`, `git-save`, `git-push`).
- `docs/release.md` - Versioning and release workflow (`VERSION` source of truth).
- `docs/visual/index.md` - Generated visual examples catalog (from `visual/`).
- `docs/visual-mkdocs-plan.md` - MkDocs visual catalog source-of-truth plan.

## Quick Start

1. Create the local Python virtual environment:
   - `./install.sh`
2. Run sanitization checks:
   - `.venv/bin/python tools/sanitize.py --check`
3. Review version state:
   - `cat VERSION`
4. Run tests:
   - `.venv/bin/python -m pytest -q`
5. Generate visual docs pages:
   - `.venv/bin/python tools/docs/build_visual_docs.py`
6. Serve docs locally:
   - `.venv/bin/mkdocs serve`
