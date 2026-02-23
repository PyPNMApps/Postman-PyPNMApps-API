#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
SCRIPT_VERSION="v1.0.0"

usage() {
  cat <<'USAGE'
Stage and commit changes for Postman-PyPNMApps-API.

Usage:
  git-save.sh [--commit-msg "Message"] [--push]

Options:
  --commit-msg  Commit message prefix (default: "Update").
  --push        Push after commit.
  -h, --help    Show help.
  -v, --version Show script version.
USAGE
}

run_check() {
  local label="$1"
  shift
  echo "[check] ${label}..."
  if "$@"; then
    echo "[pass]  ${label}"
  else
    echo "[fail]  ${label}" >&2
    exit 1
  fi
}

preferred_python() {
  if [[ -x ".venv/bin/python" ]]; then
    echo ".venv/bin/python"
  else
    echo "python3"
  fi
}

run_quality_gates() {
  local py_bin
  py_bin="$(preferred_python)"

  if [[ -f "./tools/sanitize.py" ]]; then
    run_check "sanitize --check" "${py_bin}" ./tools/sanitize.py --check
  else
    echo "[skip]  sanitize --check (tools/sanitize.py not found)"
  fi

  if [[ -f "./tools/docs/build_visual_docs.py" ]]; then
    run_check "visual docs build --check" "${py_bin}" ./tools/docs/build_visual_docs.py --check
  else
    echo "[skip]  visual docs build --check (tools/docs/build_visual_docs.py not found)"
  fi

  if [[ -d "tests" ]]; then
    run_check "pytest -q" "${py_bin}" -m pytest -q
  else
    echo "[skip]  pytest -q (no tests/ directory found)"
  fi
}

commit_msg="Update"
do_push="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --commit-msg)
      shift
      if [[ "${1:-}" == "" ]] || [[ "$1" =~ ^[[:space:]]*$ ]]; then
        echo "ERROR: --commit-msg requires a non-empty value." >&2
        exit 1
      fi
      commit_msg="$1"
      shift
      ;;
    --push)
      do_push="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -v|--version)
      echo "${SCRIPT_NAME} ${SCRIPT_VERSION}"
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: This script must be run inside a Git repository." >&2
  exit 1
fi

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"

current_branch="$(git rev-parse --abbrev-ref HEAD)"
pending_changes="$(git status --short)"

echo "========================================"
echo "Git Save"
echo "Branch: ${current_branch}"
echo "Changes:"
if [[ -z "${pending_changes}" ]]; then
  echo "  (none)"
else
  printf '%s\n' "${pending_changes}"
fi
echo "========================================"

if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

echo "Running quality and sanitize checks..."
run_quality_gates

echo "Staging changes..."
git add -A

timestamp="$(date +'%Y-%m-%d %H:%M:%S')"
final_msg="${commit_msg} - ${timestamp}"

echo "Creating commit..."
git commit -m "${final_msg}"

if [[ "${do_push}" == "true" ]]; then
  remote_name="$(git config branch."${current_branch}".remote || true)"
  echo "Pushing to ${remote_name:-origin} (${current_branch})..."
  if [[ -z "${remote_name}" ]]; then
    git push -u origin "${current_branch}"
  else
    git push "${remote_name}" "${current_branch}"
  fi
else
  echo "Push skipped. Use --push to push."
fi

echo "Done."
