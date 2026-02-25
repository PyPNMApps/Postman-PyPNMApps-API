# Visual Workflow

Use this workflow when updating Postman visualizer HTML in this repo.

## Source of Truth

- Edit visual HTML in `visual/PyPNM/...`
- Postman request path/name is the file path source of truth
- Postman collection visualizer scripts are synced from `visual/`

## Simple Flow

1. Activate the repo virtual environment
   - `source .venv/bin/activate`
2. Edit the visual HTML (and JSON fixture if needed)
   - `visual/PyPNM/...`
3. Sync visual HTML into the Postman collection
   - `tools/postman/sync_visualizers.py --update`
4. Regenerate visual docs/previews
   - `tools/docs/build_visual_docs.py`
5. Verify no drift
   - `tools/postman/sync_visualizers.py --check`
   - `tools/docs/build_visual_docs.py --check`
   - `pytest -q`

## Helpful Commands

```bash
source .venv/bin/activate
tools/postman/sync_visualizers.py --update
tools/docs/build_visual_docs.py
mkdocs serve -a 127.0.0.1:8030
```

## Git Tools

- `tools/git/git-save.sh` runs fix steps and checks before commit
- `tools/git/git-push.sh` runs check-only validation before push
