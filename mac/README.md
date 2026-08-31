# Move Reminder (macOS)

Copy this `mac` folder to the Mac. Same behavior as the Windows app: ~3" tall × 4" wide, always on top, **local time zone**, motivation line, exercise prompt and color every 20 minutes, Monday–Friday 9:00 AM–5:00 PM local.

## What you need on the Mac

1. **Python 3.9 or newer** (3.11+ is fine). `zoneinfo` is in the standard library.
2. **Tkinter** (the GUI toolkit). It is *not* a pip package.
   - **Best:** install Python from [python.org](https://www.python.org/downloads/macos/). That build includes Tk.
   - **Homebrew:** `brew install python` is not enough by itself — also `brew install python-tk`.
   - Check: `python3 -c "import tkinter; print(tkinter.TkVersion)"`
3. No extra pip modules.

Optional: **Accessibility / Screen & System Audio** is not required. If the window never stays above other apps, check **System Settings → Desktop & Dock** and that you are not using a full-screen Space that hides floating windows.

## Run

```bash
chmod +x run.command
./run.command
```

Or:

```bash
python3 app.py
```

Drag to move. Click **✕** or press **Esc** to close.

## Build a Mac app

This must be run **on a Mac** (Windows cannot produce a `.app`).

```bash
chmod +x build.sh
./build.sh
```

Output: `dist/Move Reminder.app`

Drag it to Applications. First launch: right-click the app → **Open** (Gatekeeper). It is set as a menu-bar-style agent (`LSUIElement`), so it may not show a Dock icon.

To start at login: System Settings → General → Login Items → add **Move Reminder**.

## License

[MIT](LICENSE).
