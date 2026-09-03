# Changelog

All notable changes to Move Reminder (macOS) since the original release.

The version shown in the widget, Setup, and the built `.app` is `APP_VERSION` in `app.py`.

## 1.1.1 — 2026-09-02

- After the shift, a pep message based on the day's completion rate (under 50%, 50–70%, 70–80%, 80–90%, 90–100%, or 100%).

## 1.1.0 — 2026-09-02

- **Completed** marks a prompt done and hides until the next interval.
- **Ignore** skips a prompt (counts as ignored) and hides until the next interval.
- **Lunch** / **Back** so lunch slots are not counted as skips.
- End-of-shift tally: completed vs ignored for the day.
- **Setup**: choose shift start/end (default 9:00 AM–5:00 PM) and interval (20 or 30 minutes).
- Morning vs afternoon prompt sets (wakeup vs desk reset), split at the midpoint of the shift.
- Hours, interval, and tally saved under `~/Library/Application Support/MoveReminder/`.

## 1.0.2 — 2026-09-01

- More exercise reminders (chair squats, wall sits, stretches, balance, eye break, and others).
- More motivation lines from collaborators.

## 1.0.1 — 2026-08-31

- Replaced the close control with **Hide** so the window can return at the next slot (the old close control crashed Tk on macOS).
- Local timezone label on the title line.
- Unix line endings and Mac run/build scripts.
- Project laid out at the repository root (no nested `mac/` copy).

## 1.0.0 — 2026-08

Original macOS widget:

- Always-on-top, about 3 inches tall by 4 inches wide.
- Local time, date, and weekday.
- Motivation line plus a movement prompt.
- Color change when the prompt rotates.
- Default shift Monday–Friday 9:00 AM–5:00 PM, rotating every 20 minutes.
- Drag to move; Esc / Cmd-Q to dismiss or quit.
