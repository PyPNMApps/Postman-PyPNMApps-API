#!/usr/bin/env python3
"""Generate MkDocs pages from visual HTML/JSON examples.

Current source of truth:
- visual/**/*.html (Postman visualizer scripts/templates)
- visual/**/*.json (sample response payloads)

This generator builds:
- docs/visual/index.md
- docs/visual/**/*.md      (one page per visual example)
- docs/visual-previews/**/*.html (browser preview wrappers with a Postman shim)
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PREVIEW_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      padding: 12px;
      background: #f8fafc;
      color: #111827;
      font-family: ui-sans-serif, system-ui, sans-serif;
    }}
    .frame {{
      background: #ffffff;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      padding: 12px;
    }}
    .error {{
      white-space: pre-wrap;
      color: #fecaca;
      background: #450a0a;
      border: 1px solid #7f1d1d;
      padding: 8px;
      border-radius: 6px;
    }}
    @media (prefers-color-scheme: dark) {{
      body {{
        background: #0f172a;
        color: #e5e7eb;
      }}
      .frame {{
        background: #111827;
        border-color: #374151;
      }}
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/handlebars@4.7.8/dist/handlebars.min.js"></script>
</head>
<body>
  <div id="app" class="frame"></div>
  <script>
  (function() {{
    const sampleData = {json_payload};
    const visualSource = {script_payload};
    const app = document.getElementById("app");
    let visualizerData = sampleData;
    let lastTemplate = null;

    function showError(prefix, err) {{
      const msg = String(err && err.stack || err);
      app.innerHTML = '<div class="error">' + prefix + '\\n' + msg + '</div>';
    }}

    async function executeRenderedScripts(root) {{
      const scripts = Array.from(root.querySelectorAll("script"));
      for (const oldScript of scripts) {{
        const newScript = document.createElement("script");
        for (const attr of oldScript.attributes) {{
          newScript.setAttribute(attr.name, attr.value);
        }}
        const parent = oldScript.parentNode;
        if (!parent) continue;

        if (oldScript.src) {{
          await new Promise((resolve, reject) => {{
            newScript.onload = resolve;
            newScript.onerror = function() {{
              reject(new Error('Failed to load script: ' + oldScript.src));
            }};
            parent.replaceChild(newScript, oldScript);
          }});
          continue;
        }}

        newScript.textContent = oldScript.textContent;
        parent.replaceChild(newScript, oldScript);
      }}
    }}

    function renderTemplate(template, data) {{
      lastTemplate = template;
      visualizerData = data == null ? sampleData : data;
      try {{
        const looksLikeHandlebars =
          typeof template === "string" &&
          template.indexOf("{{") !== -1 &&
          template.indexOf("}}") !== -1;
        if (window.Handlebars && looksLikeHandlebars) {{
          const compiled = window.Handlebars.compile(template);
          app.innerHTML = compiled(visualizerData);
          void executeRenderedScripts(app).catch((err) => showError('Rendered script execution error', err));
        }} else if (typeof template === "string") {{
          app.innerHTML = template;
          void executeRenderedScripts(app).catch((err) => showError('Rendered script execution error', err));
        }} else {{
          app.textContent = String(template);
        }}
      }} catch (err) {{
        showError('Template render error', err);
      }}
    }}

    function makeKVStore() {{
      const store = Object.create(null);
      return {{
        get: function(key) {{ return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : undefined; }},
        set: function(key, value) {{ store[key] = value; return value; }},
        unset: function(key) {{ delete store[key]; }}
      }};
    }}

    window.pm = {{
      response: {{
        json: function() {{ return sampleData; }},
        text: function() {{ return JSON.stringify(sampleData); }}
      }},
      request: {{
        body: {{
          raw: "{{}}"
        }}
      }},
      environment: makeKVStore(),
      globals: makeKVStore(),
      variables: makeKVStore(),
      getData: function(cb) {{
        if (typeof cb === "function") cb(null, visualizerData);
      }},
      visualizer: {{
        set: function(template, data) {{
          renderTemplate(template, data);
        }}
      }}
    }};

    window.console = window.console || {{ log(){{}}, warn(){{}}, error(){{}} }};
    window.addEventListener('error', function(ev) {{
      if (ev && ev.error) showError('Window error', ev.error);
    }});
    window.addEventListener('unhandledrejection', function(ev) {{
      showError('Unhandled promise rejection', ev && ev.reason);
    }});

    if (sampleData && typeof sampleData === 'object' && sampleData.__error__) {{
      app.innerHTML = '<div class="error">Preview unavailable\\nInvalid sample JSON fixture\\n' + String(sampleData.__error__) + '</div>';
      return;
    }}

    try {{
      const fn = new Function(visualSource);
      fn();
      if (!lastTemplate && !app.innerHTML.trim()) {{
        app.innerHTML = '<div class="error">No visualizer output produced. The script may require unsupported Postman APIs.</div>';
      }}
    }} catch (err) {{
      showError('Script execution error', err);
    }}
  }})();
  </script>
</body>
</html>
"""


INDEX_HEADER = """# Visual Examples

Generated from `visual/` (current source of truth for both visualizer HTML/script and sample JSON data).

How to regenerate:

```bash
source .venv/bin/activate
tools/docs/build_visual_docs.py
```
"""


@dataclass(frozen=True)
class VisualExample:
    key_rel: Path  # relative path without suffix under visual root
    html_path: Path | None
    json_path: Path | None

    @property
    def title(self) -> str:
        parts = list(self.key_rel.parts)
        if not parts:
            return "Visual"
        return " / ".join(parts)

    @property
    def top_group(self) -> str:
        return self.key_rel.parts[1] if len(self.key_rel.parts) > 1 else self.key_rel.parts[0]

    @property
    def source_family(self) -> str:
        return self.key_rel.parts[0] if self.key_rel.parts else "visual"

    @property
    def has_json_sample(self) -> bool:
        return self.json_path is not None


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json_for_inline_script(value: object) -> str:
    """Serialize JSON safely for embedding inside an HTML <script> tag."""
    text = json.dumps(value, ensure_ascii=False)
    # Prevent HTML parser from terminating the containing script tag.
    return text.replace("</script>", "<\\/script>").replace("</SCRIPT>", "<\\/SCRIPT>")


def _rel_display(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _write_if_changed(path: Path, content: str, check_only: bool) -> bool:
    existing = None
    if path.exists():
        existing = path.read_text(encoding="utf-8")
    changed = existing != content
    if changed and not check_only:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return changed


def _sanitize_md_anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def collect_examples(visual_root: Path) -> list[VisualExample]:
    buckets: dict[Path, dict[str, Path]] = {}
    for path in sorted(visual_root.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in {".html", ".json"}:
            continue
        rel = path.relative_to(visual_root)
        key = rel.with_suffix("")
        bucket = buckets.setdefault(key, {})
        bucket[suffix] = path
    return [
        VisualExample(key_rel=key, html_path=pair.get(".html"), json_path=pair.get(".json"))
        for key, pair in sorted(buckets.items())
    ]


def build_preview_html(example: VisualExample, repo_root: Path) -> str:
    title = html.escape(example.title)
    script_source = _read_text(example.html_path) if example.html_path else ""
    sample_data_obj: object
    if example.json_path:
        try:
            sample_data_obj = json.loads(_read_text(example.json_path))
        except json.JSONDecodeError as exc:
            sample_data_obj = {"__error__": f"Invalid JSON: {exc}"}
    else:
        sample_data_obj = {"__warning__": "No matching JSON sample file found for this visual."}
    return PREVIEW_HTML_TEMPLATE.format(
        title=title,
        json_payload=_json_for_inline_script(sample_data_obj),
        script_payload=_json_for_inline_script(script_source),
    )


def build_example_markdown(
    example: VisualExample,
    repo_root: Path,
    preview_rel_path: Path | None,
) -> str:
    title = example.title
    html_rel = _rel_display(example.html_path, repo_root) if example.html_path else None
    json_rel = _rel_display(example.json_path, repo_root) if example.json_path else None

    lines: list[str] = [f"# {title}", ""]
    lines.append("## Source Files")
    lines.append("")
    lines.append(f"- HTML/script: `{html_rel}`" if html_rel else "- HTML/script: missing")
    lines.append(f"- JSON sample: `{json_rel}`" if json_rel else "- JSON sample: missing")
    lines.append("")

    if preview_rel_path and example.html_path and example.has_json_sample:
        lines.append("## Preview")
        lines.append("")
        lines.append(
            f'<iframe src="{preview_rel_path.as_posix()}" '
            'style="width:100%;height:900px;border:1px solid #ccc;border-radius:6px;"></iframe>'
        )
        lines.append("")
        lines.append(
            "Preview is best-effort. Some templates may rely on Postman-specific APIs that are not yet shimmed."
        )
        lines.append("")
    elif example.html_path and not example.has_json_sample:
        lines.append("## Preview")
        lines.append("")
        lines.append("Preview unavailable because no matching sample JSON fixture exists for this visual.")
        lines.append("")

    if example.html_path:
        html_text = _read_text(example.html_path)
        lines.append("<details>")
        lines.append("<summary>Visualizer HTML/script source</summary>")
        lines.append("")
        lines.append("````html")
        lines.append(html_text.rstrip())
        lines.append("````")
        lines.append("</details>")
        lines.append("")

    if example.json_path:
        json_text = _read_text(example.json_path)
        lines.append("<details>")
        lines.append("<summary>Sample JSON payload</summary>")
        lines.append("")
        lines.append("````json")
        lines.append(json_text.rstrip())
        lines.append("````")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _github_blob_link_for_path(path: Path, repo_root: Path) -> str:
    rel = _rel_display(path, repo_root).replace(" ", "%20")
    return f"https://github.com/PyPNMApps/Postman-PyPNMApps-API/blob/main/{rel}"


def build_index_markdown(examples: Iterable[VisualExample], repo_root: Path) -> str:
    family_grouped: dict[str, dict[str, list[VisualExample]]] = {}
    for ex in examples:
        family_grouped.setdefault(ex.source_family, {}).setdefault(ex.top_group, []).append(ex)

    lines = [INDEX_HEADER.strip(), ""]
    lines.append("## Coverage")
    lines.append("")
    total = sum(len(v) for fam in family_grouped.values() for v in fam.values())
    lines.append(f"- Total visual examples discovered: `{total}`")
    lines.append("- Pairing is based on matching `.html` / `.json` paths under `visual/`")
    lines.append("")

    family_order = ["PyPNM", "PyPNM-CMTS"]
    all_families = [f for f in family_order if f in family_grouped] + sorted(
        f for f in family_grouped if f not in family_order
    )

    for family in all_families:
        lines.append(f"## {family}")
        lines.append("")
        lines.append(
            f"Visual source root: `visual/{family}`"
        )
        lines.append("")
        grouped = family_grouped[family]
        for group in sorted(grouped):
            lines.append(f"### {group}")
            lines.append("")
            lines.append("| Example | Preview | JSON | Docs |")
            lines.append("| --- | --- | --- | --- |")
            for ex in grouped[group]:
                page_parts = ex.key_rel.parts[1:] if ex.key_rel.parts else ex.key_rel.parts
                page_rel = Path(*page_parts).with_suffix(".md")
                preview_rel = Path("..") / "visual-previews" / Path(*page_parts)
                preview_link = preview_rel.with_suffix(".html").as_posix()
                json_link = _github_blob_link_for_path(ex.json_path, repo_root) if ex.json_path else ""
                # Endpoint-style example label (full path under family root, not only basename)
                example_name = "/".join(page_parts) if page_parts else ex.key_rel.as_posix()
                render_cell = f"[preview]({preview_link})" if ex.html_path else "missing"
                json_cell = f"[json]({json_link})" if ex.json_path else "missing"
                details_cell = f"[docs]({page_rel.as_posix()})"
                lines.append(f"| `{example_name}` | {render_cell} | {json_cell} | {details_cell} |")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate MkDocs visual catalog pages from visual/ examples.")
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root (default: .)")
    parser.add_argument("--visual-root", type=Path, default=Path("visual"), help="Visual source root (default: visual)")
    parser.add_argument("--docs-root", type=Path, default=Path("docs"), help="MkDocs docs root (default: docs)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check only; report generated-file drift and exit non-zero if updates are needed.",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    visual_root = (repo_root / args.visual_root).resolve()
    docs_root = (repo_root / args.docs_root).resolve()
    visual_docs_root = docs_root / "visual"
    preview_root = docs_root / "visual-previews"
    check_only = bool(args.check)

    if not visual_root.exists():
        print(f"ERROR: visual root not found: {visual_root}", file=sys.stderr)
        return 1

    examples = collect_examples(visual_root)
    print(f"Visual docs build ({'check' if check_only else 'write'}): discovered {len(examples)} examples under {visual_root}")

    changed_count = 0
    written_count = 0

    for ex in examples:
        page_rel_parts = ex.key_rel.parts[1:] if ex.key_rel.parts and ex.key_rel.parts[0] == "PyPNM" else ex.key_rel.parts
        page_path = visual_docs_root.joinpath(*page_rel_parts).with_suffix(".md")
        preview_path: Path | None = None
        preview_rel_from_page: Path | None = None
        if ex.html_path:
            preview_path = preview_root.joinpath(*page_rel_parts).with_suffix(".html")
            if not check_only:
                preview_path.parent.mkdir(parents=True, exist_ok=True)
            preview_content = build_preview_html(ex, repo_root=repo_root)
            if _write_if_changed(preview_path, preview_content, check_only=check_only):
                changed_count += 1
                written_count += 0 if check_only else 1
                print(f"{'DRIFT' if check_only else 'WRITE'}: {preview_path.relative_to(repo_root)}")
            # MkDocs serves markdown pages as directory URLs by default, e.g.
            # docs/visual/foo/bar.md -> /visual/foo/bar/, so relative iframe paths
            # must be computed from a virtual "bar/" directory, not page_path.parent.
            # Relative URLs are required for GitHub Pages project sites so the repo
            # path prefix is preserved.
            preview_rel_from_page = Path(os_path_rel(page_path.with_suffix(""), preview_path))

        md_content = build_example_markdown(
            example=ex,
            repo_root=repo_root,
            preview_rel_path=preview_rel_from_page,
        )
        if _write_if_changed(page_path, md_content, check_only=check_only):
            changed_count += 1
            written_count += 0 if check_only else 1
            print(f"{'DRIFT' if check_only else 'WRITE'}: {page_path.relative_to(repo_root)}")

    index_path = visual_docs_root / "index.md"
    index_content = build_index_markdown(examples, repo_root=repo_root)
    if _write_if_changed(index_path, index_content, check_only=check_only):
        changed_count += 1
        written_count += 0 if check_only else 1
        print(f"{'DRIFT' if check_only else 'WRITE'}: {index_path.relative_to(repo_root)}")

    print(
        f"Visual docs build ({'check' if check_only else 'write'}): "
        f"examples={len(examples)} generated_changes={changed_count}"
    )

    if check_only and changed_count:
        return 2
    return 0


def os_path_rel(start: Path, target: Path) -> str:
    return os.path.relpath(target, start)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
