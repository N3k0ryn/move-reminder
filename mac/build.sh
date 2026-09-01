#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to build." >&2
  exit 1
fi
if ! python3 -c "import tkinter" 2>/dev/null; then
  echo "Tkinter is missing; the app bundle needs it." >&2
  echo "Install Python from python.org, or: brew install python-tk" >&2
  exit 1
fi
python3 -m pip install -r requirements-build.txt
python3 -m PyInstaller --noconfirm --clean MoveReminder.spec
echo
echo "Built: $(pwd)/dist/Move Reminder.app"
echo "Drag that .app to Applications, then open it (first time: right-click -> Open)."
