#!/usr/bin/env python3
from __future__ import annotations

# SPDX-License-Identifier: Apache-2.0

import argparse
import re
import sys
from pathlib import Path

SEMVER_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
PYPROJECT_VERSION_PATTERN = re.compile(
    r'(^version\s*=\s*")(?P<version>\d+\.\d+\.\d+)(")',
    re.MULTILINE,
)


def _validate_semver(value: str) -> str:
    if not SEMVER_PATTERN.fullmatch(value.strip()):
        raise ValueError(f"Invalid version '{value}'. Expected X.Y.Z")
    return value.strip()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def read_version_file(version_path: Path) -> str:
    return _validate_semver(_read_text(version_path).strip())


def read_pyproject_version(pyproject_path: Path) -> str:
    text = _read_text(pyproject_path)
    match = PYPROJECT_VERSION_PATTERN.search(text)
    if not match:
        raise ValueError(f"Could not find [project].version in {pyproject_path}")
    return _validate_semver(match.group("version"))


def _replace_pyproject_version(pyproject_text: str, new_version: str) -> str:
    updated, count = PYPROJECT_VERSION_PATTERN.subn(rf'\g<1>{new_version}\3', pyproject_text, count=1)
    if count != 1:
        raise ValueError("Expected to update exactly one project version in pyproject.toml")
    return updated


def set_version(version_path: Path, pyproject_path: Path, new_version: str, *, write: bool) -> bool:
    new_version = _validate_semver(new_version)

    version_before = read_version_file(version_path)
    pyproject_before_text = _read_text(pyproject_path)
    pyproject_before_version = read_pyproject_version(pyproject_path)

    version_after_text = f"{new_version}\n"
    pyproject_after_text = _replace_pyproject_version(pyproject_before_text, new_version)

    changed = (version_before != new_version) or (pyproject_before_version != new_version)

    if changed and write:
        _write_text(version_path, version_after_text)
        _write_text(pyproject_path, pyproject_after_text)

    return changed


def check_sync(version_path: Path, pyproject_path: Path) -> bool:
    return read_version_file(version_path) == read_pyproject_version(pyproject_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bump and sync VERSION + pyproject.toml version.")
    parser.add_argument("--version", required=True, help="Target version (X.Y.Z)")
    parser.add_argument("--check", action="store_true", help="Check only; do not write changes.")
    parser.add_argument(
        "--version-file",
        type=Path,
        default=Path("VERSION"),
        help="Path to VERSION file (default: VERSION)",
    )
    parser.add_argument(
        "--pyproject",
        type=Path,
        default=Path("pyproject.toml"),
        help="Path to pyproject.toml (default: pyproject.toml)",
    )
    args = parser.parse_args(argv)

    try:
        changed = set_version(
            args.version_file,
            args.pyproject,
            args.version,
            write=not args.check,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    mode = "check" if args.check else "fix"
    print(
        f"Bump version ({mode}): target={args.version} "
        f"version_file={args.version_file} pyproject={args.pyproject} changed={changed}"
    )
    if args.check and changed:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
