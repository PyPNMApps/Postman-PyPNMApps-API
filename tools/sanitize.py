#!/usr/bin/env python3
"""Visual fixture sanitizer for Postman visual examples.

Inspired by the PyPNM demo sanitizer patterns:
- Preserve MAC formatting variants while rewriting values to a generic example.
- Normalize system_description payloads to a generic, non-vendor-specific example.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


GENERIC_SYSTEM_DESCRIPTION: dict[str, str] = {
    "HW_REV": "1.0",
    "VENDOR": "LANCity",
    "BOOTR": "NONE",
    "SW_REV": "1.0.0",
    "MODEL": "LCPET-3",
}

GENERIC_MAC_COLON = "aa:bb:cc:dd:ee:ff"

MAC_PATTERN = re.compile(
    r"(?<![0-9a-f])(?:[0-9a-f]{12}|(?:[0-9a-f]{2}(?::|-|_)){5}[0-9a-f]{2})(?![0-9a-f])",
    re.IGNORECASE,
)

SYSTEM_DESCRIPTION_KEY_DEFAULTS: dict[str, str] = {
    "HW_REV": GENERIC_SYSTEM_DESCRIPTION["HW_REV"],
    "VENDOR": GENERIC_SYSTEM_DESCRIPTION["VENDOR"],
    "BOOTR": GENERIC_SYSTEM_DESCRIPTION["BOOTR"],
    "SW_REV": GENERIC_SYSTEM_DESCRIPTION["SW_REV"],
    "MODEL": GENERIC_SYSTEM_DESCRIPTION["MODEL"],
}

def _build_mac_variants(mac: str) -> tuple[str, str, str, str]:
    compact = re.sub(r"[^0-9a-f]", "", mac.lower())
    if len(compact) != 12:
        raise ValueError(f"Expected 12 hex chars, got '{mac}'")
    colon = ":".join(compact[i : i + 2] for i in range(0, 12, 2))
    dash = "-".join(compact[i : i + 2] for i in range(0, 12, 2))
    underscore = "_".join(compact[i : i + 2] for i in range(0, 12, 2))
    return colon, dash, underscore, compact


GENERIC_MAC_VARIANTS = _build_mac_variants(GENERIC_MAC_COLON)


def _sanitize_mac_string(text: str) -> str:
    compact = re.sub(r"[^0-9a-f]", "", text.lower())
    if len(compact) != 12:
        return text
    if ":" in text:
        return GENERIC_MAC_VARIANTS[0]
    if "-" in text:
        return GENERIC_MAC_VARIANTS[1]
    if "_" in text:
        return GENERIC_MAC_VARIANTS[2]
    return GENERIC_MAC_VARIANTS[3]


def _sanitize_mac_substrings(text: str) -> str:
    return MAC_PATTERN.sub(lambda m: _sanitize_mac_string(m.group(0)), text)


def _sanitize_system_description_key_values_in_text(text: str) -> str:
    # Replace values for uppercase sysDescr/system_description keys in JS/JSON snippets.
    for key, generic_value in SYSTEM_DESCRIPTION_KEY_DEFAULTS.items():
        pattern = re.compile(
            rf'(?P<prefix>(?:"{key}"|\'{key}\'|{key})\s*:\s*)(?P<quote>["\'])(?P<value>.*?)(?P=quote)',
            re.MULTILINE,
        )

        def _replace(match: re.Match[str]) -> str:
            return f"{match.group('prefix')}{match.group('quote')}{generic_value}{match.group('quote')}"

        text = pattern.sub(_replace, text)
    return text


def _sanitize_text_content(text: str) -> str:
    text = _sanitize_system_description_key_values_in_text(text)
    text = _sanitize_mac_substrings(text)
    return text


def _sanitize_json(obj: Any, parent_key: str | None = None) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, value in obj.items():
            key_lower = key.lower()

            if key == "system_description" and isinstance(value, dict):
                out[key] = dict(GENERIC_SYSTEM_DESCRIPTION)
                continue

            if key_lower == "sysdescr" and isinstance(value, dict):
                out[key] = dict(GENERIC_SYSTEM_DESCRIPTION)
                continue

            if isinstance(value, str):
                if "mac" in key_lower and MAC_PATTERN.fullmatch(value):
                    out[key] = _sanitize_mac_string(value)
                    continue
                out[key] = _sanitize_mac_substrings(value)
                continue

            out[key] = _sanitize_json(value, parent_key=key)
        return out

    if isinstance(obj, list):
        return [_sanitize_json(item, parent_key=parent_key) for item in obj]

    if isinstance(obj, str):
        if parent_key and "mac" in parent_key.lower() and MAC_PATTERN.fullmatch(obj):
            return _sanitize_mac_string(obj)
        return _sanitize_mac_substrings(obj)

    return obj


def _find_first_system_description(obj: Any) -> dict[str, Any] | None:
    if isinstance(obj, dict):
        for key in ("system_description", "sysDescr"):
            value = obj.get(key)
            if isinstance(value, dict):
                return value
        for value in obj.values():
            found = _find_first_system_description(value)
            if found is not None:
                return found
        return None
    if isinstance(obj, list):
        for item in obj:
            found = _find_first_system_description(item)
            if found is not None:
                return found
    return None


def _looks_like_capture_response_root(obj: dict[str, Any]) -> bool:
    return "status" in obj and "data" in obj and "mac_address" in obj


def _normalize_root_system_description(obj: Any) -> Any:
    if not isinstance(obj, dict):
        return obj

    root = dict(obj)

    if "system_description" not in root and "sysDescr" not in root:
        found = _find_first_system_description(root)
        if isinstance(found, dict):
            root["system_description"] = dict(found)
        elif _looks_like_capture_response_root(root):
            root["system_description"] = dict(GENERIC_SYSTEM_DESCRIPTION)

    ordered: dict[str, Any] = {}
    for key in ("system_description", "sysDescr"):
        if key in root:
            ordered[key] = root[key]
    for key, value in root.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def sanitize_file(path: Path, write: bool = True) -> bool:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"WARNING: Skipping {path}: {exc}", file=sys.stderr)
        return False

    if path.suffix.lower() == ".json":
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"WARNING: Skipping {path}: {exc}", file=sys.stderr)
            return False
        sanitized = _normalize_root_system_description(_sanitize_json(data))
        rendered = json.dumps(sanitized, indent=4) + "\n"
    elif path.suffix.lower() == ".html":
        rendered = _sanitize_text_content(raw)
    else:
        return False

    changed = rendered != raw

    if changed and write:
        path.write_text(rendered, encoding="utf-8")

    return changed


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Sanitize visual JSON fixtures to generic MAC/sysDescr examples."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("visual"),
        help="Root directory to scan for visual JSON fixtures (default: visual).",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Check only; do not write changes. Exit non-zero if files would change.",
    )
    mode_group.add_argument(
        "--fix",
        action="store_true",
        help="Apply sanitize fixes in-place.",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    json_files = sorted(args.root.rglob("*.json"))
    html_files = sorted(args.root.rglob("*.html"))
    files = json_files + html_files
    found_files: list[Path] = []
    changed_files: list[Path] = []
    do_write = bool(args.fix)
    mode = "fix" if do_write else "check"

    print(f"Sanitize {mode}: root={root}")
    print(f"Checking directories under: {root}")
    print(f"File candidates: {len(json_files)} JSON, {len(html_files)} HTML")

    for path in files:
        changed = sanitize_file(path, write=do_write)
        if changed:
            found_files.append(path)
            rel = path.relative_to(root) if path.is_relative_to(root) else path
            if do_write:
                changed_files.append(path)
                print(f"CHANGE: {rel}")
            else:
                print(f"FIND: {rel}")

    print(
        f"Sanitize {mode}: scanned {len(files)} files (.json/.html); "
        f"finds {len(found_files)}; changes {len(changed_files)}."
    )

    if not do_write and found_files:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
