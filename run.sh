#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -x "$PROJECT_DIR/backend/.venv/bin/python" ]; then
    PYTHON="$PROJECT_DIR/backend/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Python 3.10 or newer is required. Install Python and run this script again." >&2
    exit 1
fi

exec "$PYTHON" "$PROJECT_DIR/run.py" "$@"
