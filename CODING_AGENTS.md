# Coding Agent Guidance

## Example Data Sanitization (Required)

- All examples, fixtures, screenshots, and visual JSON payloads MUST use generic values.
- Remove or replace vendor-specific identifiers (vendor names, model names, firmware versions, sysDescr values) unless explicitly required and approved for the task.
- MAC addresses in examples MUST be generic placeholders (preferred: `aa:bb:cc:dd:ee:ff`, preserving source formatting when needed).
- `system_description` / sysDescr example fields MUST be generic and non-vendor-specific.
- Use the PyPNM default generic placeholders:
- MAC: `aa:bb:cc:dd:ee:ff`
- system_description JSON: `{"HW_REV":"1.0","VENDOR":"LANCity","BOOTR":"NONE","SW_REV":"1.0.0","MODEL":"LCPET-3"}`
- Before committing visual JSON fixtures, run `.venv/bin/python tools/sanitize.py --check` (check only) or `.venv/bin/python tools/sanitize.py --fix` (apply changes) to sanitize MAC/sysDescr metadata.
- Version source of truth is the repo `VERSION` file. When bumping versions, use `.venv/bin/python tools/support/bump_version.py --version X.Y.Z` so both `VERSION` and `pyproject.toml` stay in sync.

## Tooling Layout (Required)

- Keep the project root lean. Prefer placing executable utilities under `tools/` (for example `tools/release/release.py`, `tools/git/git-save.sh`, `tools/git/git-push.sh`, `tools/support/bump_version.py`).
- Do not add root-level wrapper scripts for tools unless explicitly requested.
- Execute tools from their direct path under `tools/`.

## Commit Message Suggestions (Required)

- When the user asks for a commit message, provide plain text for direct paste into the terminal or UI text box.
- Do not wrap commit message suggestions in quotes (`"`), backticks (`` ` ``), or code fences unless the user explicitly asks for that format.
- Prefer detailed commit messages that describe the current change set clearly.
- Avoid redundant wording and avoid repeating the exact prior commit message suggestion unless the diff is unchanged and the user explicitly asks to reuse it.
