from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_sanitize_module():
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "tools" / "sanitize.py"
    spec = importlib.util.spec_from_file_location("repo_sanitize", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sanitize = _load_sanitize_module()


def test_sanitize_mac_string_preserves_known_formats() -> None:
    assert sanitize._sanitize_mac_string("00:50:f1:12:03:60") == "aa:bb:cc:dd:ee:ff"
    assert sanitize._sanitize_mac_string("00-50-f1-12-03-60") == "aa-bb-cc-dd-ee-ff"
    assert sanitize._sanitize_mac_string("00_50_f1_12_03_60") == "aa_bb_cc_dd_ee_ff"
    assert sanitize._sanitize_mac_string("0050f1120360") == "aabbccddeeff"


def test_malformed_mac_values_are_left_unchanged() -> None:
    assert sanitize._sanitize_mac_string("00:50:f1:12:03") == "00:50:f1:12:03"
    assert sanitize._sanitize_mac_string("zz:50:f1:12:03:60") == "zz:50:f1:12:03:60"
    assert sanitize._sanitize_mac_string("not-a-mac") == "not-a-mac"


def test_weird_filename_replaces_only_mac_token() -> None:
    src = "us_pre_equalizer_coef_0050f1120360_41_1771794417.bin"
    got = sanitize._sanitize_mac_substrings(src)
    assert got == "us_pre_equalizer_coef_aabbccddeeff_41_1771794417.bin"


def test_boundary_prevents_overmatching_long_hex_runs() -> None:
    src = "prefix_abcdef01234567_suffix"
    assert sanitize._sanitize_mac_substrings(src) == src


def test_sanitize_json_handles_system_description_sysdescr_and_mac_variants() -> None:
    payload = {
        "mac_address": "00:50:f1:12:03:60",
        "cmts_mac_address": "00-90-f0-05-00-00",
        "device_details": {
            "system_description": {
                "VENDOR": "Intel Corporation.",
                "MODEL": "Cougar Run",
                "HW_REV": "150.11",
                "BOOTR": "NONE",
                "SW_REV": "7.3.5",
            }
        },
        "legacy": {"sysDescr": {"foo": "bar"}},
        "filename": "ds_ofdm_rxmer_per_subcar_0050f1120360_194_1771792481.bin",
        "bad_mac_address": "00:50:f1:12:03",  # malformed; should not be modified
    }

    out = sanitize._sanitize_json(payload)
    assert out["mac_address"] == "aa:bb:cc:dd:ee:ff"
    assert out["cmts_mac_address"] == "aa-bb-cc-dd-ee-ff"
    assert out["device_details"]["system_description"] == sanitize.GENERIC_SYSTEM_DESCRIPTION
    assert out["legacy"]["sysDescr"] == sanitize.GENERIC_SYSTEM_DESCRIPTION
    assert out["filename"] == "ds_ofdm_rxmer_per_subcar_aabbccddeeff_194_1771792481.bin"
    assert out["bad_mac_address"] == "00:50:f1:12:03"


def test_root_system_description_is_lifted_and_ordered_first() -> None:
    payload = {
        "status": 0,
        "data": {
            "analysis": [
                {
                    "device_details": {
                        "system_description": {
                            "VENDOR": "Intel Corporation.",
                            "MODEL": "Cougar Run",
                            "HW_REV": "150.11",
                            "BOOTR": "NONE",
                            "SW_REV": "7.3.5",
                        }
                    }
                }
            ]
        },
    }

    out = sanitize._normalize_root_system_description(sanitize._sanitize_json(payload))
    assert list(out.keys())[0] == "system_description"
    assert out["system_description"] == sanitize.GENERIC_SYSTEM_DESCRIPTION
    assert out["status"] == 0


def test_root_system_description_defaults_for_capture_response_when_missing() -> None:
    payload = {
        "mac_address": "00:50:f1:12:03:60",
        "status": 0,
        "message": "ok",
        "data": {"results": []},
    }
    out = sanitize._normalize_root_system_description(sanitize._sanitize_json(payload))
    assert list(out.keys())[0] == "system_description"
    assert out["system_description"] == sanitize.GENERIC_SYSTEM_DESCRIPTION


def test_sanitize_file_invalid_json_returns_false(tmp_path: Path) -> None:
    path = tmp_path / "empty.json"
    path.write_text("", encoding="utf-8")
    assert sanitize.sanitize_file(path, write=False) is False


def test_sanitize_text_content_html_rewrites_sysdescr_keys_and_macs() -> None:
    html = """
    <script>
    const sample = {
      system_description: {
        "VENDOR": "Intel Corporation.",
        MODEL: 'Cougar Run',
        HW_REV: "150.11",
        BOOTR: "CUSTOM",
        SW_REV: "7.3.5.3.521"
      },
      mac_address: "00:50:f1:12:03:60",
      fileName: "ds_ofdm_rxmer_per_subcar_0050f1120360_194_1771792481.bin"
    };
    </script>
    """
    out = sanitize._sanitize_text_content(html)
    assert '"VENDOR": "LANCity"' in out
    assert "MODEL: 'LCPET-3'" in out
    assert 'HW_REV: "1.0"' in out
    assert 'BOOTR: "NONE"' in out
    assert 'SW_REV: "1.0.0"' in out
    assert 'mac_address: "aa:bb:cc:dd:ee:ff"' in out
    assert "aabbccddeeff_194_1771792481.bin" in out


def test_sanitize_file_html_check_only_and_fix(tmp_path: Path) -> None:
    path = tmp_path / "sample.html"
    path.write_text(
        '<script>const x={VENDOR:"Intel Corporation.",MODEL:"Cougar Run",mac:"00-50-f1-12-03-60"};</script>',
        encoding="utf-8",
    )

    assert sanitize.sanitize_file(path, write=False) is True
    # No write in check-only mode
    original = path.read_text(encoding="utf-8")
    assert "Intel Corporation." in original

    assert sanitize.sanitize_file(path, write=True) is True
    updated = path.read_text(encoding="utf-8")
    assert 'VENDOR:"LANCity"' in updated
    assert 'MODEL:"LCPET-3"' in updated
    assert 'mac:"aa-bb-cc-dd-ee-ff"' in updated


def test_cli_check_and_fix_modes(tmp_path: Path) -> None:
    visual_root = tmp_path / "visual"
    visual_root.mkdir()
    sample = visual_root / "sample.json"
    sample.write_text(
        json.dumps(
            {
                "mac_address": "0050f1120360",
                "system_description": {
                    "VENDOR": "Intel Corporation.",
                    "MODEL": "Cougar Run",
                    "HW_REV": "150.11",
                    "BOOTR": "NONE",
                    "SW_REV": "7.3.5",
                },
            }
        ),
        encoding="utf-8",
    )

    rc_check_before = sanitize.main(["--root", str(visual_root), "--check"])
    assert rc_check_before == 2

    # check mode must not write changes
    before = json.loads(sample.read_text(encoding="utf-8"))
    assert before["mac_address"] == "0050f1120360"

    rc_fix = sanitize.main(["--root", str(visual_root), "--fix"])
    assert rc_fix == 0

    after = json.loads(sample.read_text(encoding="utf-8"))
    assert after["mac_address"] == "aabbccddeeff"
    assert after["system_description"] == sanitize.GENERIC_SYSTEM_DESCRIPTION

    rc_check_after = sanitize.main(["--root", str(visual_root), "--check"])
    assert rc_check_after == 0


def test_cli_fix_adds_root_system_description_when_nested_only(tmp_path: Path) -> None:
    visual_root = tmp_path / "visual"
    visual_root.mkdir()
    sample = visual_root / "nested-only.json"
    sample.write_text(
        json.dumps(
            {
                "status": 0,
                "data": {
                    "analysis": [
                        {
                            "device_details": {
                                "system_description": {
                                    "VENDOR": "Something",
                                    "MODEL": "X",
                                    "HW_REV": "2.0",
                                    "BOOTR": "Y",
                                    "SW_REV": "3.0",
                                }
                            }
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    assert sanitize.main(["--root", str(visual_root), "--fix"]) == 0
    after = json.loads(sample.read_text(encoding="utf-8"))
    assert list(after.keys())[0] == "system_description"
    assert after["system_description"] == sanitize.GENERIC_SYSTEM_DESCRIPTION
