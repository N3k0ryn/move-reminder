# Changelog

## [1.3.0] — 2026-10-13

### Changed — complete rewrite in Swift + SwiftUI
- Replaced Python / tkinter / PyInstaller stack with native Swift + SwiftUI + AppKit
- `FloatingPanel` (NSPanel subclass) replaces tkinter overrideredirect window
- `AppViewModel` (ObservableObject + Timer) replaces the tkinter `after` loop
- `LinearGradient` replaces the 36-band canvas gradient
- All prefs and stats serialised with `Codable` / `JSONEncoder` — same JSON
  schema as before, so existing `prefs.json` and `stats.json` files are preserved
- Minimum macOS bumped to **13.0 Ventura** (was 10.15); no Python runtime required
- Removed `app.py`, `MoveReminder.spec`, `requirements-build.txt`, `run.command`
- Added `MoveReminder.xcodeproj` and `MoveReminder/` Swift source tree

### Fixed
- Window no longer disappears after macOS security patches that invalidate
  PyInstaller-bundled Python runtimes
- Drag-to-move now works correctly with native `isMovableByWindowBackground`
- Cmd+Q now works via standard NSApplication quit path (no custom Tcl command)

---

## [1.2.0]

- Added lunch-break pause mode
- Afternoon motivation quotes added
- Settings panel for shift hours and interval

## [1.1.1]

- Fixed timezone label on systems where `time.tzset` is unavailable

## [1.0.0]

- Initial release (Python / tkinter)
