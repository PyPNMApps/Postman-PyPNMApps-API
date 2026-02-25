#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
OS_MODE="windows"

usage() {
  cat <<'USAGE'
Bootstrap the local Python environment and print repo workflow commands.

Usage:
  ./install.sh [--os-windows|--os-window|--os-linux]

Options:
  --os-windows   Print Windows (PowerShell) command examples. Default.
  --os-window    Alias for --os-windows.
  --os-linux     Print Linux/macOS shell command examples.
  -h, --help     Show this help.

Examples:
  ./install.sh
  ./install.sh --os-windows
  ./install.sh --os-linux
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --os-windows|--os-window)
      OS_MODE="windows"
      shift
      ;;
    --os-linux)
      OS_MODE="linux"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "ERROR: ${PYTHON_BIN} not found on PATH" >&2
  exit 1
fi

if [ ! -d "${VENV_DIR}" ]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

"${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install -e "${ROOT_DIR}[dev]"

print_windows_examples() {
  echo "Windows (PowerShell) commands (default examples):"
  echo "  .\\.venv\\Scripts\\Activate.ps1"
  echo "  .\\tools\\postman\\format_collection.ps1 -Check"
  echo "  .\\tools\\postman\\format_collection.ps1 -Fix"
  echo "  python .\\tools\\postman\\sync_visualizers.py --check"
  echo "  python .\\tools\\postman\\sync_visualizers.py --update"
  echo "  python .\\tools\\sanitize.py --check"
  echo "  python .\\tools\\sanitize.py --fix"
  echo "  python .\\tools\\docs\\build_visual_docs.py"
  echo "  pytest -q"
  echo "  mkdocs serve -a 127.0.0.1:8030"
}

print_linux_examples() {
  echo "Linux/macOS shell commands:"
  echo "  source .venv/bin/activate"
  echo "  tools/postman/format_collection.sh --check"
  echo "  tools/postman/format_collection.sh --fix"
  echo "  tools/postman/sync_visualizers.py --check"
  echo "  tools/postman/sync_visualizers.py --update"
  echo "  tools/sanitize.py --check"
  echo "  tools/sanitize.py --fix"
  echo "  tools/docs/build_visual_docs.py"
  echo "  pytest -q"
  echo "  mkdocs serve -a 127.0.0.1:8030"
}

echo "Python virtual environment ready at: ${VENV_DIR}"
echo "Activate it with:"
echo "  source ${VENV_DIR}/bin/activate"
echo "OS mode for printed examples: ${OS_MODE}"
if [[ "${OS_MODE}" == "windows" ]]; then
  print_windows_examples
  echo "Linux/macOS equivalent (optional):"
  echo "  source .venv/bin/activate"
  echo "  tools/postman/format_collection.sh --fix"
else
  print_linux_examples
fi
echo "Version / release tools:"
echo "  tools/support/bump_version.py --version X.Y.Z --check"
echo "  tools/support/bump_version.py --version X.Y.Z"
echo "  tools/release/release.py --version-info"
echo "Recommended visual workflow:"
echo "  1) Format collection JSON (if collection changed)"
if [[ "${OS_MODE}" == "windows" ]]; then
  echo "     .\\tools\\postman\\format_collection.ps1 -Fix"
else
  echo "     tools/postman/format_collection.sh --fix"
fi
echo "  2) Sync visualizer scripts"
echo "     tools/postman/sync_visualizers.py --update"
echo "  3) Regenerate visual docs"
echo "     tools/docs/build_visual_docs.py"
echo "  4) Run tests"
echo "     pytest -q"
