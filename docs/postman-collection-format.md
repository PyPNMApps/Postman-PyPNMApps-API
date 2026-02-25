# Postman Collection Formatting

Use the Postman collection formatter to normalize `postman/collections/PyPNM.postman_collection.json` across Linux and Windows.

It provides:

- consistent JSON formatting (default: 2-space indent)
- LF line endings (`\n`)
- schema version detection (`v2.0` / `v2.1`)
- normalization of non-finite numeric values (`NaN` / `Infinity`) to `null` for valid JSON output

## Setup

Create and activate the repo virtual environment:

```bash
./install.sh
source .venv/bin/activate
```

## Windows (PowerShell) - Default

Formatter wrapper:

- `tools/postman/format_collection.ps1`

Check formatting only:

```powershell
.\tools\postman\format_collection.ps1 -Check
```

Apply formatting:

```powershell
.\tools\postman\format_collection.ps1 -Fix
```

Compact/minified output (optional):

```powershell
.\tools\postman\format_collection.ps1 -Fix -Compact
```

## Linux / macOS (Shell)

Formatter wrapper:

- `tools/postman/format_collection.sh`

If needed, make sure the shell wrapper is executable:

```bash
chmod +x tools/postman/format_collection.sh
```

Check formatting only (no file changes):

```bash
tools/postman/format_collection.sh --check
```

Apply formatting:

```bash
tools/postman/format_collection.sh --fix
```

Compact/minified output (optional):

```bash
tools/postman/format_collection.sh --fix --compact
```

## Alternate Collection Path

Both wrappers support formatting a different collection file (for example `PyPNM-CMTS`).

Linux / macOS:

```bash
tools/postman/format_collection.sh --path postman/collections/PyPNM-CMTS.postman_collection.json --fix
```

Windows PowerShell:

```powershell
.\tools\postman\format_collection.ps1 -Path postman/collections/PyPNM-CMTS.postman_collection.json -Fix
```

## Recommended Usage

Run formatting before commit when the collection JSON changes:

1. Format collection:
   - `.\tools\postman\format_collection.ps1 -Fix`
2. Sync visualizer scripts (if visual HTML changed):
   - `tools/postman/sync_visualizers.py --fix`
3. Regenerate visual docs (if visual HTML/JSON changed):
   - `tools/docs/build_visual_docs.py`
