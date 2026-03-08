# Coding Agent Guidance

## Example Data Sanitization (Required)

- All examples, fixtures, screenshots, and visual JSON payloads MUST use generic values.
- Remove or replace vendor-specific identifiers (vendor names, model names, firmware versions, sysDescr values) unless explicitly required and approved for the task.
- MAC addresses in examples MUST be generic placeholders (preferred: `aa:bb:cc:dd:ee:ff`, preserving source formatting when needed).
- `system_description` / sysDescr example fields MUST be generic and non-vendor-specific.
- Use the PyPNM default generic placeholders:
- MAC: `aa:bb:cc:dd:ee:ff`
- system_description JSON: `{"HW_REV":"1.0","VENDOR":"LANCity","BOOTR":"NONE","SW_REV":"1.0.0","MODEL":"LCPET-3"}`
- Before committing visual JSON fixtures, activate the repo venv (`source .venv/bin/activate`) and run `tools/sanitize.py --check` (check only) or `tools/sanitize.py --fix` (apply changes) to sanitize MAC/sysDescr metadata.
- Version source of truth is the repo `VERSION` file. After activating the repo venv, use `tools/support/bump_version.py --version X.Y.Z` so both `VERSION` and `pyproject.toml` stay in sync.

## Tooling Layout (Required)

- Keep the project root lean. Prefer placing executable utilities under `tools/` (for example `tools/release/release.py`, `tools/git/git-save.sh`, `tools/git/git-push.sh`, `tools/support/bump_version.py`).
- Do not add root-level wrapper scripts for tools unless explicitly requested.
- Execute tools from their direct path under `tools/`.

## Commit Message Suggestions (Required)

- If a chat request starts with `commit-msg`, use: `./tools/git/git-save.sh --commit-msg "<commit-msg>"`
- Do not use `commit-msg` as a positional argument; `git-save.sh` expects `--commit-msg`.
- One line summary (max 50 characters)
- One line Summary start: Feature: , Bugfix: , Docs: , Refactor: , Test:
- Detailed description lines (max 72 characters per line); every line after the first must start with `-`
- When the user asks for a commit message, provide plain text for direct paste into the terminal or UI text box.
- Do not wrap commit message suggestions in quotes (`"`), backticks (`` ` ``), or code fences unless the user explicitly asks for that format.
- Prefer detailed commit messages that describe the current change set clearly.
- Do not default to a one-line commit message when the change set is broad; provide a title plus concise bullet points.
- Avoid redundant wording and avoid repeating the exact prior commit message suggestion unless the diff is unchanged and the user explicitly asks to reuse it.
- If the user asks for "in a text box", return plain text only (no markdown fence).
- If the user asks for "in a markdown text box", return the commit message inside a fenced code block with `text`.

## Visual Development Rules (Required)

- `visual/` is the source of truth for visual HTML (`*.html`) and sample JSON (`*.json`) in this repo version.
- Start new visual work from `visual/templates/Postman-Visualizer-SectionTemplate.md` and build the page section-by-section from that scaffold.
- Do not manually edit generated visual docs (`docs/visual/`, `docs/visual-previews/`); regenerate from `visual/`.
- No comments in visual code/templates unless explicitly requested.
- Required exception: every visual script must begin with a three-line header comment in this format:
- `// Postman Visualizer: <<Description of Visual >>`
- `// Last Update: <<Date and Time>>`
- `// Visual Constraints: Follow canonical visual rules in CODING_AGENTS.md.`
- No emoji in visual UI labels, titles, legends, table headers, axis labels, or status text unless explicitly requested.
- At the top of each visual HTML file, maintain the visual rules/constraints and indicate that `CODING_AGENTS.md` defines the canonical rules so they are not forgotten.
- Do not scatter magic numbers through visual HTML/script logic. Put tunable constants in a clearly named `TUNING` section near the top of the visual (for example chart heights, tick limits, sampling caps, render-bin caps, animation timings).
- When tuning values are chosen for readability/performance, name them descriptively (for example `CHANNEL_CHART_HEIGHT`, `MAX_RENDER_BINS`, `Y_TICKS_PER_CHANNEL`) so later adjustments do not require re-reading the whole file.
- Visuals should support dark/light mode behavior and check system settings when rendering theme-sensitive output.
- If `sysDescr` / `system_description` is present in the JSON response, show it prominently at the top of the visual.
- Standardize `sysDescr` / `system_description` presentation as a dedicated `Device Info` block separate from channel/capture graph blocks.
- `Device Info` should render before channel-specific charts/content.
- Prefer a horizontal one-row table for common modem identity fields with display labels exactly:
- `MacAddress`, `Model`, `Vendor`, `SW Version`, `HW Version`, `Boot ROM`
- Use proper display casing/spacing for labels (for example `SW Version`, not `SW_REV`; `Boot ROM`, not `BOOTR`).
- When a capture timestamp is available (for example `pnm_header.capture_time`), place `Capture Time` next to the visual title/header as a layout-only element (not inside chart/graph sections).
- Format capture timestamps as a human-readable date/time string (not raw epoch seconds).
- Keep channel metadata in a separate block below `Device Info` (for example `Channel`, center/subcarrier frequency).
- Display frequencies in `MHz` for UI-facing labels; raw `Hz` may be shown secondarily in parentheses when useful.
- Default UI frequency labels/ticks to whole-number `MHz` (frequency is not a float in the UI by default; no decimal floats) unless precision is required for the specific visual.
- If the axis title already includes the unit (for example `Frequency (MHz)`), do not repeat the unit on every tick label.
- Include units in graph titles/axis labels for measured values (for example `Magnitude (dB)` instead of `Magnitude`).
- Center graph/panel titles for scanability and consistent visual layout.
- When a visual can plot both raw values and moving-average/smoothed values, prefer a per-graph `Actual / Moving Avg` radio toggle instead of showing both at once by default (reduces clutter).
- For `Moving Avg` overlays, use the same base color as `Actual` with a dashed line style.
- Avoid redundant repetition of values already shown in `Device Info` (for example, do not repeat `MacAddress` in the channel header if it is already in the device table).
- If `system_description` is missing/partial, render `N/A` for missing fields instead of vendor-specific fallback values.
- Never hardcode vendor/model/firmware fallback values in visualizer runtime logic.
- PyPNM generic placeholder values are for fixture JSON only and must not be used as runtime script fallbacks.
- JSON responses may contain multiple upstream/downstream channels; each channel must render as its own graph for the selected graph type.
- For multi-channel visuals with repeated per-channel panels/boxes, default to a 2-column layout (max 2 per row) with a 1-column fallback on narrower widths.
- For channel-related multi-channel visuals, place the combined graph at the top and per-channel graphs below it.
- For channel-related multi-channel visuals, include the channel count in the combined graph title (for example `All Channels (N)`).
- Do not add a separate `Analysis Summary` block when it only repeats channel count/status; surface channel count in the combined graph title and keep status elsewhere only when needed.
- Multi-channel combined graphs should line up all channels by frequency in a single graph.
- For any frequency-type graph (US and DS), show frequency range and spacing at the channel/group header level and do not repeat frequency range text inside each per-modem/per-card graph (avoid redundant per-card frequency metadata).
- For QAM order labels, use `QX` display format (for example `Q4096`) in UI text, chart axes, legends, tooltips, and summaries; do not display raw keys such as `qam_4096`.

## Visual Color Rules (Required)

- Default visual shell/theme should use the current dark-blue palette family used by recent visuals (for example page bg `#141821`, panel bg `#1b2332`, panel title accent blue, primary text near-white).
- Do not use the older red-accent page theme (`#e94560` headings on `#1a1a2e` / `#16213e`) for new/refactored visuals unless explicitly requested.
- High / max = red
- Mid / avg = blue
- Low / min = green
- Downstream (`DS`) lines = blue
- Upstream (`US`) lines = green
- Warning = yellow
- OK = green
- NOK = red
- In dark mode, all chart x/y axis labels, axis titles, and tick text must be white.
- In light mode, all chart x/y axis labels, axis titles, and tick text must be dark (near-black/navy) for contrast.
- Regression / trend / fitted reference lines must use a high-contrast color distinct from waveform traces (prefer dashed).
- Default regression/reference line color: white.
- If white reduces readability against the chart/waveform palette, use a dark red contrast line (for example `#c62828`) or another clearly contrasting color and document the choice in the visual remarks.

## Postman Request YAML Guardrails (Required)

- Use this top-level key order for every `*.request.yaml`:
- `$kind`, `url`, `method`, `body`, `scripts`, `order`
- Keep `language: text/javascript` present under every script entry.
- Keep `order` unique among sibling requests in the same folder.
- Request URL must use `{{variable}}` base prefix (no hardcoded host/base).
- JSON bodies must use the repo escaped multi-line body style used by existing request files in that folder.

### New Endpoint Workflow (Do This Every Time)

- Create the new request YAML with the correct endpoint body and variable names.
- Add a temporary visualizer stub header that matches the visual path.
- Run `tools/postman/sync_visualizers.py --update` to copy script content from `visual/` 1:1.
- Do not hand-edit long synced script blocks in YAML unless explicitly required; fix the source HTML in `visual/` and re-sync.

### Post-Sync Verification Checklist

- Confirm the script header has all 3 required lines.
- Confirm canonical dark-blue palette is present (page `#141821`, panel `#1b2332`).
- Confirm `language: text/javascript` is present.
- Confirm sibling `order` remains unique.
- If any check fails, fix source visual and rerun sync before commit.
