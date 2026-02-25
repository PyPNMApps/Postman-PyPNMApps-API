#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

DEFAULT_COLLECTION = Path("postman/collections/PyPNM.postman_collection.json")


def _load_json_permissive(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _scrub_non_finite(value: object) -> object:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, list):
        return [_scrub_non_finite(v) for v in value]
    if isinstance(value, dict):
        return {k: _scrub_non_finite(v) for k, v in value.items()}
    return value


def _detect_schema_version(data: object) -> str:
    if not isinstance(data, dict):
        return "unknown"
    schema = ((data.get("info") or {}).get("schema")) if isinstance(data.get("info"), dict) else None
    if not isinstance(schema, str):
        return "unknown"
    m = re.search(r"/v(\d+\.\d+)\.\d+/collection\.json$", schema)
    return f"v{m.group(1)}" if m else schema


def _format_json(data: object, *, compact: bool) -> str:
    if compact:
        return json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"
    return json.dumps(data, ensure_ascii=False, allow_nan=False, indent=2) + "\n"


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Format a Postman collection JSON file with LF endings")
    p.add_argument("--path", default=str(DEFAULT_COLLECTION), help="Collection JSON path")
    p.add_argument("--check", action="store_true", help="Check only; exit 2 if formatting changes are needed")
    p.add_argument("--fix", action="store_true", help="Write formatted output in place")
    p.add_argument("--compact", action="store_true", help="Use compact/minified JSON instead of 2-space indentation")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    if args.check and args.fix:
        raise SystemExit("ERROR: Use only one of --check or --fix.")

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"ERROR: Collection not found: {path}")

    mode = "fix" if args.fix else "check"
    raw = path.read_text(encoding="utf-8")
    data = _scrub_non_finite(_load_json_permissive(path))
    schema_version = _detect_schema_version(data)

    if schema_version not in {"v2.0", "v2.1"}:
        print(f"WARNING: Unrecognized Postman schema version: {schema_version}")

    formatted = _format_json(data, compact=args.compact)
    changed = raw != formatted

    print(
        f"Postman collection format {mode}: path={path} "
        f"schema={schema_version} style={'compact' if args.compact else 'indent=2'} changed={str(changed).lower()}"
    )

    if args.fix and changed:
        path.write_text(formatted, encoding="utf-8", newline="\n")
        print(f"WRITE: {path}")

    if args.check and changed:
        sys.exit(2)


if __name__ == "__main__":
    main()
