from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_visual_docs_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "tools" / "docs" / "build_visual_docs.py"
    spec = importlib.util.spec_from_file_location("repo_build_visual_docs", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


visual_docs = _load_visual_docs_module()


def test_json_for_inline_script_escapes_script_end_tag() -> None:
    text = visual_docs._json_for_inline_script({"x": "</script><script>alert(1)</script>"})
    assert "</script>" not in text
    assert "<\\/script>" in text


def test_build_example_markdown_skips_iframe_when_json_missing(tmp_path: Path) -> None:
    html_path = tmp_path / "sample.html"
    html_path.write_text("pm.visualizer.set('<div>x</div>', {});", encoding="utf-8")

    example = visual_docs.VisualExample(
        key_rel=Path("PyPNM/SingleCapture/SpectrumAnalysis/GetCapture-FBC"),
        html_path=html_path,
        json_path=None,
    )
    md = visual_docs.build_example_markdown(
        example=example,
        repo_root=tmp_path,
        preview_rel_path=Path("/visual-previews/SingleCapture/SpectrumAnalysis/GetCapture-FBC.html"),
    )
    assert "Preview unavailable because no matching sample JSON fixture exists" in md
    assert "<iframe" not in md


def test_build_preview_html_escapes_embedded_script_tags(tmp_path: Path) -> None:
    html_path = tmp_path / "vis.html"
    json_path = tmp_path / "vis.json"
    html_path.write_text(
        'pm.visualizer.set("<div><script src=\\"https://cdn.example/chart.js\\"></script></div>", {});',
        encoding="utf-8",
    )
    json_path.write_text('{"ok": true}', encoding="utf-8")

    example = visual_docs.VisualExample(key_rel=Path("PyPNM/X/Test"), html_path=html_path, json_path=json_path)
    preview = visual_docs.build_preview_html(example, repo_root=tmp_path)

    # Wrapper script tags remain, but embedded visual source must be escaped.
    assert "<\\/script>" in preview
    assert 'const visualSource =' in preview


def test_main_generates_pages_and_check_is_clean(tmp_path: Path) -> None:
    repo_root = tmp_path
    visual_root = repo_root / "visual" / "PyPNM" / "DOCSIS-General"
    docs_root = repo_root / "docs"
    visual_root.mkdir(parents=True)
    docs_root.mkdir(parents=True)

    (visual_root / "InterfaceStats.html").write_text(
        "pm.visualizer.set('<div>{{status}}</div>', {status: pm.response.json().status});",
        encoding="utf-8",
    )
    (visual_root / "InterfaceStats.json").write_text('{"status": 0}', encoding="utf-8")

    rc_write = visual_docs.main(
        [
            "--repo-root",
            str(repo_root),
            "--visual-root",
            "visual",
            "--docs-root",
            "docs",
        ]
    )
    assert rc_write == 0

    generated_page = docs_root / "visual" / "DOCSIS-General" / "InterfaceStats.md"
    generated_preview = docs_root / "visual-previews" / "DOCSIS-General" / "InterfaceStats.html"
    generated_index = docs_root / "visual" / "index.md"

    assert generated_page.exists()
    assert generated_preview.exists()
    assert generated_index.exists()
    assert '/visual-previews/DOCSIS-General/InterfaceStats.html' in generated_page.read_text(encoding="utf-8")

    rc_check = visual_docs.main(
        [
            "--repo-root",
            str(repo_root),
            "--visual-root",
            "visual",
            "--docs-root",
            "docs",
            "--check",
        ]
    )
    assert rc_check == 0
