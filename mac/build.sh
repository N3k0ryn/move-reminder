#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install -r requirements-build.txt
python3 -m PyInstaller --noconfirm --clean MoveReminder.spec
echo
echo "Built: $(pwd)/dist/Move Reminder.app"
echo "Drag that .app to Applications, then open it (first time: right-click → Open)."
