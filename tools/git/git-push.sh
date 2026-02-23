#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
SCRIPT_VERSION="v1.0.0"

usage() {
  cat <<'USAGE'
Commit and push changes for Postman-PyPNMApps-API.

Usage:
  git-push.sh [--commit-msg "Message"]

Options:
  --commit-msg  Commit message (default: timestamped Auto-push).
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

commit_msg=""
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

if [[ -z "${commit_msg}" ]]; then
  commit_msg="Auto-push: $(date +'%Y-%m-%d %H:%M:%S')"
fi

current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "${current_branch}" == "HEAD" ]]; then
  echo "ERROR: Detached HEAD detected. Check out a branch before pushing." >&2
  exit 1
fi

if [[ "${current_branch}" != "main" && "${current_branch}" != "hot-fix" ]]; then
  echo "WARNING: Current branch is '${current_branch}' (not main/hot-fix)." >&2
  read -r -p "Continue anyway? [y/N]: " confirm
  if [[ "${confirm,,}" != "y" && "${confirm,,}" != "yes" ]]; then
    echo "Aborted."
    exit 1
  fi
fi

if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

echo "Running quality and sanitize checks..."
run_quality_gates

echo "Staging changes..."
git add -A

echo "Creating commit..."
git commit -m "${commit_msg}"

remote_name="$(git config branch."${current_branch}".remote || true)"
push_remote="${remote_name:-origin}"

echo "Pushing to ${push_remote} (${current_branch})..."
if [[ -z "${remote_name}" ]]; then
  git push -u "${push_remote}" "${current_branch}"
else
  if ! git push "${push_remote}" "${current_branch}"; then
    echo "Initial push failed; retrying with upstream setup..."
    git push -u "${push_remote}" "${current_branch}"
  fi
fi

echo "Done."
