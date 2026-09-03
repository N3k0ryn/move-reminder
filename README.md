# Move Reminder (macOS)

A floating, always-on-top window about **3 inches tall** and **4 inches wide**. It uses the Mac's **local time zone**.

Weekdays during your shift it shows a motivation line and an exercise. **Morning** slots use wakeup moves (heart rate, standing, marching). **Afternoon** slots use desk resets (stretch, posture, eyes). The split is the midpoint of your shift.

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

- Drag to move.
- **Completed** marks the prompt done and hides until the next interval.
- **Ignore** skips it (counts as ignored) and hides until the next interval.
- **Lunch** / **Back** toggles lunch. While you are on lunch, skips are not counted against you.
- **Setup** (or the hours line): change start/end (default 9:00 AM-5:00 PM) and interval (20 or 30 minutes).
- After the shift, the widget shows that day's completed vs ignored tally.
- **Esc**, Cmd-H, or Cmd-W acts like Ignore. **Cmd-Q** quits.

Hours, interval, and the daily tally are saved under `~/Library/Application Support/MoveReminder/`.

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
