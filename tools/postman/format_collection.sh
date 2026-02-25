#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  PY_BIN="${REPO_ROOT}/.venv/bin/python"
else
  PY_BIN="python3"
fi

exec "${PY_BIN}" "${REPO_ROOT}/tools/postman/format_collection.py" "$@"
