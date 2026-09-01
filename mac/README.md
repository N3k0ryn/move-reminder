# Move Reminder (macOS)

A floating, always-on-top window about **3 inches tall** and **4 inches wide**. It uses the Mac's **local time zone**, shows a motivation line, and rotates the exercise prompt and colors every 20 minutes, Monday-Friday 9:00 AM-5:00 PM local.

## What you need

1. **Python 3.9 or newer** (3.11+ is fine).
2. **Tkinter** (the GUI toolkit). It is *not* a pip package.
   - **Best:** install Python from [python.org](https://www.python.org/downloads/macos/). That build includes Tk.
   - **Homebrew:** `brew install python` is not enough by itself — also `brew install python-tk`.
   - Check: `python3 -c "import tkinter; print(tkinter.TkVersion)"`
3. No extra pip modules to run from source.

Accessibility permission is not required. If the window never stays above other apps, check **System Settings -> Desktop & Dock**, and avoid a full-screen Space that hides floating windows.

## Run

```bash
chmod +x run.command
./run.command
```

Or:

```bash
python3 app.py
```

Drag to move. Click **Hide** or press **Esc** (or Cmd-H / Cmd-W) to tuck the window away; it comes back at the next 20-minute workout slot (weekdays 9-5). **Cmd-Q** quits.

## Build a Mac app

```bash
chmod +x build.sh
./build.sh
```

Output: `dist/Move Reminder.app`

Drag it to Applications. First launch: right-click the app -> **Open** (Gatekeeper). It is set as a menu-bar-style agent (`LSUIElement`), so it may not show a Dock icon.

To start at login: System Settings -> General -> Login Items -> add **Move Reminder**.

## License

[MIT](LICENSE).
