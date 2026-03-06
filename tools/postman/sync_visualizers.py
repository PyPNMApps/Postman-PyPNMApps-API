#!/usr/bin/env python3
from __future__ import annotations

# SPDX-License-Identifier: Apache-2.0

import argparse
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_COLLECTION_PATH = Path("postman/collections/PyPNM")
DEFAULT_VISUAL_ROOT = Path("visual/PyPNM")


@dataclass
class SyncResult:
    visualizer_requests: int = 0
    matched_html: int = 0
    missing_html: int = 0
    drifted_scripts: int = 0
    changed_scripts: int = 0
    extra_visual_html: int = 0


class _LiteralStr(str):
    pass


def _represent_literal_str(dumper: yaml.Dumper, data: _LiteralStr) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="|")


yaml.SafeDumper.add_representer(_LiteralStr, _represent_literal_str)


def _to_literal_multiline(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _to_literal_multiline(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_literal_multiline(v) for v in obj]
    if isinstance(obj, str) and "\n" in obj:
        return _LiteralStr(obj)
    return obj


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _dump_yaml(path: Path, data: dict[str, Any]) -> None:
    out = yaml.safe_dump(
        _to_literal_multiline(data),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1_000_000,
    )
    path.write_text(out, encoding="utf-8")


def _has_visualizer(req: dict[str, Any]) -> bool:
    for script in req.get("scripts", []) or []:
        if "pm.visualizer.set" in str(script.get("code", "")):
            return True
    return False


def _find_visualizer_script(req: dict[str, Any]) -> dict[str, Any] | None:
    for script in req.get("scripts", []) or []:
        if "pm.visualizer.set" in str(script.get("code", "")):
            return script
    return None


def _extract_visualizer_header_rel(req: dict[str, Any]) -> str | None:
    script = _find_visualizer_script(req)
    if script is None:
        return None
    code = str(script.get("code", ""))
    pattern = re.compile(r"^\s*//\s*Postman Visualizer:\s*(.+?)\s*$")
    for line in code.splitlines():
        match = pattern.match(line)
        if match:
            rel = match.group(1).strip().strip("/")
            return rel or None
    return None


def _request_rel_from_file(path: Path, collection_root: Path) -> str:
    rel = path.relative_to(collection_root).as_posix()
    if rel.endswith(".request.yaml"):
        return rel[: -len(".request.yaml")]
    return rel


def _all_visual_html_paths(root: Path) -> set[str]:
    if not root.exists():
        return set()
    return {p.relative_to(root).with_suffix("").as_posix() for p in root.rglob("*.html")}


def _resolve_visual_html_path(visual_root: Path, rel: str) -> tuple[Path | None, str | None]:
    direct = visual_root / f"{rel}.html"
    if direct.exists():
        return direct, rel
    basic = visual_root / rel / "basic.html"
    if basic.exists():
        return basic, f"{rel}/basic"
    if rel.endswith("/Results"):
        parent_rel = rel.rsplit("/", 1)[0]
        parent_basic = visual_root / parent_rel / "basic.html"
        if parent_basic.exists():
            return parent_basic, f"{parent_rel}/basic"
    return None, None


def _diff_line_stats(old_lines: list[str], new_lines: list[str]) -> tuple[int, int, int, int]:
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


def sync_visualizers(*, root: Path, collection_rel: Path, visual_root_rel: Path, fix: bool, verbose: bool) -> SyncResult:
    collection_root = root / collection_rel
    visual_root = root / visual_root_rel
    if not collection_root.exists() or not collection_root.is_dir():
        raise SystemExit(f"ERROR: Collection root not found: {collection_root}")
    if not visual_root.exists():
        raise SystemExit(f"ERROR: Visual root not found: {visual_root}")

    request_files = sorted(collection_root.rglob("*.request.yaml"))
    visualizer_req_files: list[Path] = []
    for req_file in request_files:
        req = _load_yaml(req_file)
        if _has_visualizer(req):
            visualizer_req_files.append(req_file)

    result = SyncResult(visualizer_requests=len(visualizer_req_files))
    mapped_paths: set[str] = set()
    missing: list[str] = []

    for req_file in visualizer_req_files:
        req = _load_yaml(req_file)
        header_rel = _extract_visualizer_header_rel(req)
        fallback_rel = _request_rel_from_file(req_file, collection_root)
        rel = header_rel or fallback_rel

        root_prefix = f"{visual_root.name}/"
        if rel.startswith(root_prefix):
            rel = rel[len(root_prefix) :]

        html_path, matched_rel = _resolve_visual_html_path(visual_root, rel)
        if matched_rel:
            mapped_paths.add(matched_rel)
        if html_path is None:
            result.missing_html += 1
            missing.append(rel)
            if verbose:
                print(f"MISSING: {visual_root / (rel + '.html')} (also tried {visual_root / rel / 'basic.html'})")
            continue

        result.matched_html += 1
        html_text = html_path.read_text(encoding="utf-8").rstrip("\n")
        html_lines = html_text.splitlines()
        script = _find_visualizer_script(req)
        if script is None:
            continue
        old_text = str(script.get("code", "")).rstrip("\n")
        old_lines = old_text.splitlines()

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
                script["code"] = html_text
                result.changed_scripts += 1
                _dump_yaml(req_file, req)
                print(f"CHANGE: {summary}")
            else:
                print(f"DRIFT: {summary}")

    all_visual_html = _all_visual_html_paths(visual_root)
    result.extra_visual_html = len(all_visual_html - mapped_paths)

    if missing and fix:
        raise SystemExit("ERROR: Missing matching visual HTML file(s) for one or more Postman visualizer requests.")

    return result


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Sync Postman visualizer scripts from visual HTML files into local YAML requests"
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Read-only check mode (exit 2 on drift)")
    mode.add_argument("--update", action="store_true", help="Update YAML request visualizer scripts in place")
    mode.add_argument("--fix", action="store_true", help="Deprecated alias for --update")
    p.add_argument(
        "--collection",
        default=str(DEFAULT_COLLECTION_PATH),
        help=f"Collection root dir (default: {DEFAULT_COLLECTION_PATH})",
    )
    p.add_argument(
        "--visual-root",
        default=str(DEFAULT_VISUAL_ROOT),
        help=f"Visual HTML root path (default: {DEFAULT_VISUAL_ROOT})",
    )
    p.add_argument("--verbose", action="store_true", help="Print missing path details")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    update = bool(args.update or args.fix)
    check = bool(args.check or not update)
    collection_rel = Path(args.collection)
    visual_root_rel = Path(args.visual_root)

    mode_label = "update" if update else "check"
    root = Path.cwd()
    print(f"Visualizer sync {mode_label}: collection={collection_rel} visual_root={visual_root_rel}")

    result = sync_visualizers(
        root=root,
        collection_rel=collection_rel,
        visual_root_rel=visual_root_rel,
        fix=update,
        verbose=args.verbose,
    )
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
