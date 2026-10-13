#!/bin/bash
# Build Move Reminder (Swift) for macOS — requires Xcode 15+ command-line tools.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v xcodebuild &>/dev/null; then
  echo "xcodebuild not found. Install Xcode from the App Store, then run:" >&2
  echo "  xcode-select --install" >&2
  exit 1
fi

xcodebuild \
  -project MoveReminder.xcodeproj \
  -scheme  MoveReminder \
  -configuration Release \
  -derivedDataPath build \
  build

APP="build/Build/Products/Release/Move Reminder.app"
echo
echo "Built: $(pwd)/$APP"
echo "Drag that .app to /Applications, then right-click → Open on first launch."
