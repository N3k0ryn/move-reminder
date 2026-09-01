#!/bin/bash
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python 3 is required. Install from https://www.python.org/downloads/macos/" >&2
  exit 1
fi
if ! "$PY" -c "import tkinter" 2>/dev/null; then
  echo "Tkinter is missing." >&2
  echo "Install Python from python.org, or: brew install python-tk" >&2
  exit 1
fi
exec "$PY" app.py
