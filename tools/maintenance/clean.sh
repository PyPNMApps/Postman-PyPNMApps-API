#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026
# Cleans MkDocs output and common Python/local build artifacts for this repo.

set -euo pipefail
IFS=$'\n\t'

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS] [ROOT_DIR]

Options:
  --site     Clean MkDocs build output (site/)
  --all      Clean site/ plus common Python caches and build artifacts
  -h, --help Show this help and exit

ROOT_DIR defaults to the current directory if not provided.
EOF
  exit 1
}

ROOT_DIR="."
declare -a ACTIONS=()

while (( $# )); do
  case "$1" in
    --site|--all)
      ACTIONS+=("$1")
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      ROOT_DIR="$1"
      shift
      ;;
  esac
done

if [[ ${#ACTIONS[@]} -eq 0 ]]; then
  usage
fi

ROOT_DIR=$(realpath "$ROOT_DIR")
if [[ ! -d "$ROOT_DIR" ]]; then
  echo "ERROR: Root directory not found: $ROOT_DIR" >&2
  exit 1
fi

if ! git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: ROOT_DIR must be inside the repository." >&2
  exit 1
fi

ROOT_DIR=$(git -C "$ROOT_DIR" rev-parse --show-toplevel)
echo "Cleaning in root directory: $ROOT_DIR"

safe_rm() {
  local path
  for path in "$@"; do
    if [[ -e $path || -L $path ]]; then
      rm -rf -- "$path"
      echo "Removed: $path"
    else
      echo "Skip (not found): $path"
    fi
  done
}

safe_rm_glob() {
  local pattern="$1"
  local matched="false"
  shopt -s nullglob
  for path in $pattern; do
    matched="true"
    rm -rf -- "$path"
    echo "Removed: $path"
  done
  shopt -u nullglob
  if [[ "$matched" == "false" ]]; then
    echo "Skip (no matches): $pattern"
  fi
}

clean_site() {
  echo "Cleaning MkDocs site output..."
  safe_rm "$ROOT_DIR/site"
}

clean_python() {
  echo "Cleaning Python caches and test artifacts..."

  find "$ROOT_DIR" \
    -path "$ROOT_DIR/.venv" -prune -o \
    -type d -name "__pycache__" -print -exec rm -rf {} +

  find "$ROOT_DIR" \
    -path "$ROOT_DIR/.venv" -prune -o \
    -type f -name "*.pyc" -print -exec rm -f {} +

  safe_rm \
    "$ROOT_DIR/.pytest_cache" \
    "$ROOT_DIR/.mypy_cache" \
    "$ROOT_DIR/.ruff_cache" \
    "$ROOT_DIR/.tox" \
    "$ROOT_DIR/.nox" \
    "$ROOT_DIR/htmlcov" \
    "$ROOT_DIR/.coverage"

  safe_rm_glob "$ROOT_DIR/.coverage.*"
}

clean_build() {
  echo "Cleaning build artifacts..."
  safe_rm \
    "$ROOT_DIR/build" \
    "$ROOT_DIR/dist" \
    "$ROOT_DIR/site"

  safe_rm_glob "$ROOT_DIR/*.egg-info"
  safe_rm "$ROOT_DIR/.eggs" "$ROOT_DIR/pip-wheel-metadata"
}

for action in "${ACTIONS[@]}"; do
  case "$action" in
    --site)
      clean_site
      ;;
    --all)
      clean_site
      clean_python
      clean_build
      ;;
    *)
      echo "ERROR: Unknown action: $action" >&2
      exit 1
      ;;
  esac
done

echo "Cleanup complete."
