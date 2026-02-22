from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load_bump_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "tools" / "support" / "bump_version.py"
    spec = importlib.util.spec_from_file_location("repo_bump_version", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bump = _load_bump_module()


def _write_version_files(tmp_path: Path, version: str = "0.1.0") -> tuple[Path, Path]:
    version_path = tmp_path / "VERSION"
    pyproject_path = tmp_path / "pyproject.toml"
    version_path.write_text(f"{version}\n", encoding="utf-8")
    pyproject_path.write_text(
        (
            "[project]\n"
            'name = "demo"\n'
            f'version = "{version}"\n'
            'description = "x"\n'
        ),
        encoding="utf-8",
    )
    return version_path, pyproject_path


def test_check_sync_true_and_false(tmp_path: Path) -> None:
    version_path, pyproject_path = _write_version_files(tmp_path, "0.1.0")
    assert bump.check_sync(version_path, pyproject_path) is True

    pyproject_path.write_text(
        pyproject_path.read_text(encoding="utf-8").replace('version = "0.1.0"', 'version = "0.1.1"'),
        encoding="utf-8",
    )
    assert bump.check_sync(version_path, pyproject_path) is False


def test_set_version_check_only_does_not_write(tmp_path: Path) -> None:
    version_path, pyproject_path = _write_version_files(tmp_path, "0.1.0")
    changed = bump.set_version(version_path, pyproject_path, "0.1.1", write=False)
    assert changed is True
    assert version_path.read_text(encoding="utf-8").strip() == "0.1.0"
    assert bump.read_pyproject_version(pyproject_path) == "0.1.0"


def test_set_version_fix_updates_both_files(tmp_path: Path) -> None:
    version_path, pyproject_path = _write_version_files(tmp_path, "0.1.0")
    changed = bump.set_version(version_path, pyproject_path, "0.1.1", write=True)
    assert changed is True
    assert version_path.read_text(encoding="utf-8").strip() == "0.1.1"
    assert bump.read_pyproject_version(pyproject_path) == "0.1.1"


def test_set_version_normalizes_drift_when_target_matches_one_side(tmp_path: Path) -> None:
    version_path, pyproject_path = _write_version_files(tmp_path, "0.1.0")
    pyproject_path.write_text(
        pyproject_path.read_text(encoding="utf-8").replace('version = "0.1.0"', 'version = "0.1.9"'),
        encoding="utf-8",
    )
    changed = bump.set_version(version_path, pyproject_path, "0.1.0", write=True)
    assert changed is True
    assert bump.check_sync(version_path, pyproject_path) is True
    assert bump.read_pyproject_version(pyproject_path) == "0.1.0"


def test_invalid_version_is_rejected(tmp_path: Path) -> None:
    version_path, pyproject_path = _write_version_files(tmp_path, "0.1.0")
    with pytest.raises(ValueError):
        bump.set_version(version_path, pyproject_path, "1.2", write=False)


def test_cli_check_and_fix_modes(tmp_path: Path) -> None:
    version_path, pyproject_path = _write_version_files(tmp_path, "0.1.0")
    rc = bump.main(
        [
            "--version",
            "0.1.2",
            "--check",
            "--version-file",
            str(version_path),
            "--pyproject",
            str(pyproject_path),
        ]
    )
    assert rc == 2
    assert bump.read_version_file(version_path) == "0.1.0"

    rc = bump.main(
        [
            "--version",
            "0.1.2",
            "--version-file",
            str(version_path),
            "--pyproject",
            str(pyproject_path),
        ]
    )
    assert rc == 0
    assert bump.read_version_file(version_path) == "0.1.2"
    assert bump.read_pyproject_version(pyproject_path) == "0.1.2"
