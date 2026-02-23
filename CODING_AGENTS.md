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

- When the user asks for a commit message, provide plain text for direct paste into the terminal or UI text box.
- Do not wrap commit message suggestions in quotes (`"`), backticks (`` ` ``), or code fences unless the user explicitly asks for that format.
- Prefer detailed commit messages that describe the current change set clearly.
- Do not default to a one-line commit message when the change set is broad; provide a title plus concise bullet points.
- Avoid redundant wording and avoid repeating the exact prior commit message suggestion unless the diff is unchanged and the user explicitly asks to reuse it.
- If the user asks for "in a text box", return plain text only (no markdown fence).
- If the user asks for "in a markdown text box", return the commit message inside a fenced code block with `text`.

## Visual Development Rules (Required)

- `visual/` is the source of truth for visual HTML (`*.html`) and sample JSON (`*.json`) in this repo version.
- Do not manually edit generated visual docs (`docs/visual/`, `docs/visual-previews/`); regenerate from `visual/`.
- No comments in visual code/templates unless explicitly requested.
- At the top of each visual HTML file, maintain the visual rules/constraints and indicate that `CODING_AGENTS.md` defines the canonical rules so they are not forgotten.
- Visuals should support dark/light mode behavior and check system settings when rendering theme-sensitive output.
- If `sysDescr` / `system_description` is present in the JSON response, show it prominently at the top of the visual.
- JSON responses may contain multiple upstream/downstream channels; each channel must render as its own graph for the selected graph type.
- Multi-channel views should also include a combined graph at the bottom with all channels lined up by frequency in a single graph.

## Visual Color Rules (Required)

- High / max = red
- Mid / avg = blue
- Low / min = green
- Downstream (`DS`) lines = blue
- Upstream (`US`) lines = green
- Warning = yellow
- OK = green
- NOK = red
