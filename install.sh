#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "ERROR: ${PYTHON_BIN} not found on PATH" >&2
  exit 1
fi

if [ ! -d "${VENV_DIR}" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install -e "${ROOT_DIR}[dev]"

echo "Python virtual environment ready at: ${VENV_DIR}"
echo "Use the sanitize tool with:"
echo "  ${VENV_DIR}/bin/python tools/sanitize.py --check"
echo "  ${VENV_DIR}/bin/python tools/sanitize.py --fix"
echo "Use the version bump tool with:"
echo "  ${VENV_DIR}/bin/python tools/support/bump_version.py --version X.Y.Z --check"
echo "  ${VENV_DIR}/bin/python tools/support/bump_version.py --version X.Y.Z"
echo "Run tests with:"
echo "  ${VENV_DIR}/bin/python -m pytest"
echo "Build visual docs pages with:"
echo "  ${VENV_DIR}/bin/python tools/docs/build_visual_docs.py"
echo "Serve MkDocs locally with:"
echo "  ${VENV_DIR}/bin/mkdocs serve"
