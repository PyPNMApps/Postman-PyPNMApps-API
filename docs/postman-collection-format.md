# Postman Local YAML Format

This repository uses Postman local-mode YAML artifacts as the source of truth.

## Paths

- Collections: `postman/collections/<collection>/.../*.request.yaml`
- Environments: `postman/environments/*.environment.yaml`
- Globals: `postman/globals/*.globals.yaml`

## Required Conventions

- Keep one request per file (`*.request.yaml`).
- Preserve folder hierarchy under each collection directory.
- Keep request `name` human-friendly; keep filename filesystem-safe.
- Keep Postman variables as literal `{{var}}`.
- Use quoted strings when needed to avoid YAML type coercion.
- Prefer multiline block style for long scripts/bodies.

## Visualizer Script Sync

Use this tool to check/update embedded visualizer script code:

```bash
source .venv/bin/activate
tools/postman/sync_visualizers.py --check
tools/postman/sync_visualizers.py --update
```

For `PyPNM-CMTS`:

```bash
source .venv/bin/activate
tools/postman/sync_visualizers.py --check --collection postman/collections/PyPNM-CMTS --visual-root visual/PyPNM-CMTS
tools/postman/sync_visualizers.py --update --collection postman/collections/PyPNM-CMTS --visual-root visual/PyPNM-CMTS
```

## Migration Note

Legacy single-file Postman collection JSON exports are not the primary artifact in this repo. Prefer editing YAML request files directly.
