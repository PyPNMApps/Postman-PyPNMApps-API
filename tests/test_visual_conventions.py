from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_coding_agents_documents_capture_time_header_rule() -> None:
    text = _read("CODING_AGENTS.md")
    assert "place `Capture Time` next to the visual title/header" in text
    assert "human-readable date/time string (not raw epoch seconds)" in text


def test_visual_template_includes_capture_time_header_pattern() -> None:
    text = _read("visual/templates/Postman-Visualizer-SectionTemplate.md")
    assert "Capture Time: {{captureTime}}" in text
    assert "function formatCaptureTime(raw)" in text
    assert "captureTime: null" in text


def test_histogram_visual_uses_capture_time_in_header_and_no_measurement_stats_panel() -> None:
    text = _read("visual/PyPNM/SingleCapture/Histogram/Histogram.html")
    assert '<div class="capture-time">Capture Time: {{capture_time}}</div>' in text
    assert "pnmHeader.capture_time" in text
    assert "Measurement Statistics" not in text
    assert "measurement_stats" not in text


def test_updated_visuals_include_optional_capture_time_header_pill() -> None:
    visual_paths = [
        "visual/PyPNM/SingleCapture/OFDMA/GetCapture-PreEqualization.html",
        "visual/PyPNM/SingleCapture/OFDM/GetCapture-RxMER.html",
        "visual/PyPNM/SingleCapture/OFDM/GetCapture-ConstellationDisplay.html",
    ]
    for rel_path in visual_paths:
        text = _read(rel_path)
        assert "Capture Time: {{captureTime}}" in text, rel_path
        assert "formatCaptureTime(" in text, rel_path

