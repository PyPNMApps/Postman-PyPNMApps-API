# Visual MkDocs Plan

## Current Source of Truth (This Version)

- `visual/**/*.html` - Postman visualizer scripts/templates
- `visual/**/*.json` - sample response payloads

The MkDocs visual catalog is generated directly from these files.

## Current Implementation (MVP)

- `tools/docs/build_visual_docs.py` scans `visual/`
- Generates pages under `docs/visual/`
- Generates preview wrappers under `docs/visual-previews/`
- Uses a lightweight Postman shim for previews:
  - `pm.response.json()`
  - `pm.getData(...)`
  - `pm.visualizer.set(...)`

## Future Direction (Planned)

Later, the HTML/script source of truth will move into the Postman collection files.

Planned migration path:

1. Keep `visual/*.json` as sample data source
2. Add a collection extractor adapter for visualizer scripts
3. Preserve generated MkDocs page URLs
4. Switch generator input from filesystem HTML to collection-derived scripts

## Commands

```bash
source .venv/bin/activate
tools/docs/build_visual_docs.py
mkdocs serve -a 127.0.0.1:8030
```
