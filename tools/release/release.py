#!/usr/bin/env python3
from __future__ import annotations

# SPDX-License-Identifier: Apache-2.0
# Adapted from PyPNM-Common-Development/release.py for common release practice.

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_VERSION = "v1.0.0"
ALLOWED_BRANCHES = {"main"}
SEMVER_TAG_PATTERN = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
EXPECTED_REPO_NAME = "Postman-PyPNMApps-API"
VERSION_FILE_PATH = Path("VERSION")
BUMP_SCRIPT_PATH = Path("tools") / "support" / "bump_version.py"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, text=True, capture_output=True)
    if check and result.returncode != 0:
        sys.stderr.write(result.stdout or "")
        sys.stderr.write(result.stderr or "")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def tag_exists(tag: str) -> bool:
    result = run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"], check=False)
    return result.returncode == 0


def get_head_commit() -> str:
    return run(["git", "rev-parse", "HEAD"]).stdout.strip()


def get_tag_commit(tag: str) -> str:
    return run(["git", "rev-list", "-n", "1", tag]).stdout.strip()


def _read_repo_version(root: Path) -> str:
    version_path = root / VERSION_FILE_PATH
    if not version_path.exists():
        raise SystemExit(f"ERROR: VERSION file not found at {version_path}")
    value = version_path.read_text(encoding="utf-8").strip()
    if not SEMVER_TAG_PATTERN.match(f"v{value}"):
        raise SystemExit(f"ERROR: Invalid VERSION contents '{value}'. Expected X.Y.Z")
    return value


def resolve_release_version(root: Path, explicit_version: str | None) -> str:
    if explicit_version:
        return explicit_version

    current = _read_repo_version(root)
    major, minor, patch = [int(part) for part in current.split(".")]
    return f"{major}.{minor}.{patch + 1}"


def ensure_repo_root() -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"])
    root = Path(result.stdout.strip())
    if root.name != EXPECTED_REPO_NAME:
        raise SystemExit(f"ERROR: release.py only supports {EXPECTED_REPO_NAME}.")
    return root


def get_current_branch() -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def ensure_branch_allowed() -> None:
    branch = get_current_branch()
    if branch not in ALLOWED_BRANCHES:
        raise SystemExit("ERROR: release can only run on main.")


def ensure_clean_worktree() -> None:
    status = run(["git", "status", "--porcelain"]).stdout.strip()
    if status:
        raise SystemExit("ERROR: Working tree is not clean. Commit or stash changes first.")


def _preferred_python(root: Path) -> str:
    venv_py = root / ".venv" / "bin" / "python"
    if venv_py.exists():
        return str(venv_py)
    return sys.executable


def run_quality_gates(root: Path) -> None:
    python_bin = _preferred_python(root)

    sanitize_script = root / "tools" / "sanitize.py"
    if sanitize_script.exists():
        print("[check] sanitize (check mode)")
        run([python_bin, str(sanitize_script), "--check"])

    bump_script = root / BUMP_SCRIPT_PATH
    if bump_script.exists():
        print("[check] version sync")
        current_version = _read_repo_version(root)
        run([python_bin, str(bump_script), "--version", current_version, "--check"])

    pytest_candidates = [
        root / ".venv" / "bin" / "pytest",
    ]
    pytest_bin = next((str(p) for p in pytest_candidates if p.exists()), None)
    if pytest_bin is not None:
        print("[check] pytest")
        run([pytest_bin, "-q"])
    else:
        print("[check] pytest (python -m pytest)")
        run([python_bin, "-m", "pytest", "-q"])


def bump_version_files(root: Path, version: str) -> None:
    python_bin = _preferred_python(root)
    bump_script = root / BUMP_SCRIPT_PATH
    if not bump_script.exists():
        raise SystemExit(f"ERROR: bump script not found at {bump_script}")
    print(f"[release] bump VERSION + pyproject.toml -> {version}")
    run([python_bin, str(bump_script), "--version", version])


def create_release_commit_and_tag(version: str, push: bool) -> None:
    tag = f"v{version}"
    branch = get_current_branch()
    head_commit = get_head_commit()

    if tag_exists(tag):
        tag_commit = get_tag_commit(tag)
        if tag_commit == head_commit:
            print(f"Tag {tag} already exists at HEAD; skipping commit/tag creation.")
            if push:
                run(["git", "push", "origin", branch])
                run(["git", "push", "origin", tag])
            return
        raise SystemExit(
            f"ERROR: tag {tag} already exists at commit {tag_commit[:7]}. "
            "Use a new --version."
        )

    run(["git", "add", str(VERSION_FILE_PATH), "pyproject.toml"])
    run(["git", "commit", "--allow-empty", "-m", f"Release {version}"])
    run(["git", "tag", "-a", tag, "-m", f"Release {version}"])

    if push:
        run(["git", "push", "origin", branch])
        run(["git", "push", "origin", tag])


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Release helper for {EXPECTED_REPO_NAME}")
    parser.add_argument(
        "--version",
        default=None,
        help="Release version. If omitted, auto-bump to next patch from existing vX.Y.Z tags.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Do not push branch and tag to origin (push is enabled by default)",
    )
    parser.add_argument("--skip-checks", action="store_true", help="Skip sanitize/tests checks")
    parser.add_argument("--version-info", action="store_true", help="Print script version and exit")
    args = parser.parse_args()

    if args.version_info:
        print(f"release.py {SCRIPT_VERSION}")
        return

    root = ensure_repo_root()
    ensure_branch_allowed()
    ensure_clean_worktree()

    if not args.skip_checks:
        run_quality_gates(root)

    release_version = resolve_release_version(root, args.version)
    print(f"Selected release version: {release_version}")

    bump_version_files(root, release_version)
    create_release_commit_and_tag(release_version, not args.no_push)
    print(f"Release {release_version} complete.")


if __name__ == "__main__":
    main()
