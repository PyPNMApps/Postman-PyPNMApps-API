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
echo "Activate it with:"
echo "  source ${VENV_DIR}/bin/activate"
echo "Use the sanitize tool with:"
echo "  tools/sanitize.py --check"
echo "  tools/sanitize.py --fix"
echo "Use the Postman visualizer sync tool with:"
echo "  tools/postman/sync_visualizers.py --check"
echo "  tools/postman/sync_visualizers.py --fix"
echo "Use the version bump tool with:"
echo "  tools/support/bump_version.py --version X.Y.Z --check"
echo "  tools/support/bump_version.py --version X.Y.Z"
echo "Run tests with:"
echo "  pytest"
echo "Build visual docs pages with:"
echo "  tools/docs/build_visual_docs.py"
echo "Serve MkDocs locally with:"
echo "  mkdocs serve -a 127.0.0.1:8030"
