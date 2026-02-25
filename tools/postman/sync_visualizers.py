#!/usr/bin/env python3
from __future__ import annotations

# SPDX-License-Identifier: Apache-2.0

import argparse
import difflib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

COLLECTION_PATH = Path("postman/collections/PyPNM.postman_collection.json")
VISUAL_ROOT = Path("visual/PyPNM")


@dataclass
class SyncResult:
    visualizer_requests: int = 0
    matched_html: int = 0
    missing_html: int = 0
    drifted_scripts: int = 0
    changed_scripts: int = 0
    extra_visual_html: int = 0


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _join_script_lines(lines: list[str] | None) -> str:
    return "\n".join(lines or [])


def _has_visualizer(req: dict) -> bool:
    for event in req.get("event", []) or []:
        if event.get("listen") != "test":
            continue
        script = event.get("script") or {}
        if "pm.visualizer.set" in _join_script_lines(script.get("exec")):
            return True
    return False


def _find_visualizer_test_event(req: dict) -> dict | None:
    for event in req.get("event", []) or []:
        if event.get("listen") != "test":
            continue
        script = event.get("script") or {}
        if "pm.visualizer.set" in _join_script_lines(script.get("exec")):
            return event
    return None


def _walk_items(items: list[dict] | None, path_parts: list[str], out: list[tuple[list[str], dict]]) -> None:
    for item in items or []:
        name = item.get("name", "")
        if "item" in item:
            _walk_items(item.get("item"), [*path_parts, name], out)
            continue
        if _has_visualizer(item):
            out.append((path_parts, item))


def _all_visual_html_paths(root: Path) -> set[str]:
    if not root.exists():
        return set()
    return {p.relative_to(root).with_suffix("").as_posix() for p in root.rglob("*.html")}


def _diff_line_stats(old_lines: list[str], new_lines: list[str]) -> tuple[int, int, int, int]:
    """
    Return a compact diff summary:
    (added_lines, removed_lines, replaced_old_lines, replaced_new_lines)
    """
    added = 0
    removed = 0
    replaced_old = 0
    replaced_new = 0
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            added += (j2 - j1)
        elif tag == "delete":
            removed += (i2 - i1)
        elif tag == "replace":
            replaced_old += (i2 - i1)
            replaced_new += (j2 - j1)
    return added, removed, replaced_old, replaced_new


def sync_visualizers(*, root: Path, fix: bool, verbose: bool) -> SyncResult:
    collection_path = root / COLLECTION_PATH
    visual_root = root / VISUAL_ROOT
    if not collection_path.exists():
        raise SystemExit(f"ERROR: Collection not found: {collection_path}")
    if not visual_root.exists():
        raise SystemExit(f"ERROR: Visual root not found: {visual_root}")

    collection = _load_json(collection_path)
    visualizer_reqs: list[tuple[list[str], dict]] = []
    _walk_items(collection.get("item"), [], visualizer_reqs)

    result = SyncResult(visualizer_requests=len(visualizer_reqs))
    mapped_paths: set[str] = set()
    missing: list[str] = []

    for parent_parts, req in visualizer_reqs:
        req_name = req.get("name", "")
        rel = "/".join([*parent_parts, req_name])
        mapped_paths.add(rel)
        html_path = visual_root / f"{rel}.html"
        if not html_path.exists():
            result.missing_html += 1
            missing.append(rel)
            if verbose:
                print(f"MISSING: {html_path.relative_to(root)}")
            continue

        result.matched_html += 1
        html_lines = html_path.read_text(encoding="utf-8").splitlines()
        event = _find_visualizer_test_event(req)
        if event is None:
            # Should not happen because _has_visualizer gated this request.
            continue
        script = event.setdefault("script", {})
        old_lines = script.get("exec") or []
        if old_lines != html_lines:
            result.drifted_scripts += 1
            added, removed, repl_old, repl_new = _diff_line_stats(old_lines, html_lines)
            summary = (
                f"{rel} "
                f"(lines {len(old_lines)} -> {len(html_lines)}; "
                f"+{added} -{removed}"
            )
            if repl_old or repl_new:
                summary += f"; ~{repl_old}->{repl_new}"
            summary += ")"
            if fix:
                script["exec"] = html_lines
                script.setdefault("type", "text/javascript")
                result.changed_scripts += 1
                print(f"CHANGE: {summary}")
            else:
                print(f"DRIFT: {summary}")

    all_visual_html = _all_visual_html_paths(visual_root)
    result.extra_visual_html = len(all_visual_html - mapped_paths)

    if missing and fix:
        raise SystemExit("ERROR: Missing matching visual HTML file(s) for one or more Postman visualizer requests.")

    if fix and result.changed_scripts:
        collection_path.write_text(json.dumps(collection, indent=2) + "\n", encoding="utf-8")

    return result


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sync Postman visualizer test scripts from visual/PyPNM HTML files")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Read-only check mode (exit 2 on drift)")
    mode.add_argument("--update", action="store_true", help="Update collection visualizer scripts in place")
    mode.add_argument("--fix", action="store_true", help="Deprecated alias for --update")
    p.add_argument("--verbose", action="store_true", help="Print missing path details")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    update = bool(args.update or args.fix)
    check = bool(args.check or not update)

    mode_label = "update" if update else "check"
    root = Path.cwd()
    print(f"Visualizer sync {mode_label}: collection={COLLECTION_PATH} visual_root={VISUAL_ROOT}")

    result = sync_visualizers(root=root, fix=update, verbose=args.verbose)
    print(
        "Visualizer sync "
        f"{mode_label}: visualizer_requests={result.visualizer_requests} "
        f"matched_html={result.matched_html} "
        f"missing_html={result.missing_html} "
        f"drift={result.drifted_scripts} "
        f"changed={result.changed_scripts} "
        f"extra_visual_html={result.extra_visual_html}"
    )

    if result.missing_html:
        sys.exit(1)
    if check and result.drifted_scripts:
        sys.exit(2)


if __name__ == "__main__":
    main()
