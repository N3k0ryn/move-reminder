#!/usr/bin/env python3
"""Move Reminder for macOS — always-on-top 3x4 inch strip with time and movement prompts."""

from __future__ import annotations

import json
import sys
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import font as tkfont

APP_VERSION = "1.1.1"
APP_NAME = "Move Reminder"
MADE_WITH = "Made with Cursor ♥"

DEFAULT_START_HOUR = 9
DEFAULT_END_HOUR = 17
DEFAULT_INTERVAL = 20
WORK_WEEKDAYS = {0, 1, 2, 3, 4}  # Monday–Friday
START_HOUR_CHOICES = tuple(range(6, 12))
END_HOUR_CHOICES = tuple(range(13, 21))
INTERVAL_CHOICES = (20, 30)

MORNING_REMINDERS = (
    "Stand up: 10 air squats",
    "Chair squats - 10-12 reps",
    "Get that heart pumping! 20-30 jumping jacks!",
    "March in place for one minute",
    "High Knee March in place with Reach and Pull for 20 reps",
    "Get moving - jog in place 45 seconds",
    "Stand up: Butt kicks for 30 seconds",
    "Shadow boxing for 30 seconds",
    "Calf raises while you wait",
    "Wall sit for 20-30 seconds",
    "Standing side leg raises - 10 per leg",
    "Arm circle, big and small, 20 seconds of each",
    "Shake it out! Full body shake for 15 seconds",
    "Balance: Single leg stand, eyes closed - 15 seconds per side",
)

AFTERNOON_REMINDERS = (
    "Desk push-ups or wall push-ups — 8–12",
    "Stretch: neck, shoulders, back, hips",
    "Drop a Plank for 20–30s",
    "Tricep dips off chair or floor - 8-10 reps",
    "On the floor: 12 Glute bridges",
    "Stretch: 10 Cat-cows",
    "Stretch: Standing forward fold for 20 seconds",
    "Stretch: Doorway chest stretch for 30 seconds",
    "Stretch: Wrist and forearm stretch",
    "Stretch: 10 Ankle circles in each direction",
    "Stretch: Standing spinal twist - 5 each side",
    "Balance: Standing knee-to-elbow crunches - 10 per side",
    "Balance: Bird dog - 10 each side",
    "Balance: Side plank - 20 seconds per side",
    "Look out the window at something outside, aim for 20+ feet away (eye strain break)",
    "Toe touches for 10 each side",
)

MORNING_MOTIVATIONS = (
    "A healthy body and mind keeps you grounded",
    "Have you hydrated?",
    "You are doing great!",
    "Remember you are the author of your life",
    "Small moves add up to a stronger you",
    "Show up for you — that’s enough",
    "How are you feeling? Need to fill your water, get a snack?",
    "Everything you need to get it done is already inside of you",
    "Your wildest dream deserve a chance",
    "There's no such thing as -the right time- Trust yourself and do it!",
    "Choose you. Everytime.",
    "Your ending is still unwritten. It's never too late to create a life you love.",
)

AFTERNOON_MOTIVATIONS = (
    "Breathe and exhale your stress",
    "Be kind to yourself in this hour",
    "Unclench your jaw. Drop your shoulders.",
    "Progress, not perfection",
    "Straighten up, your back will thank you",
    "Sometimes letting go is the best way to free yourself",
    "Drown out the fucking noise and keep doing you",
    "The things that you say to yourself matter. Be kind.",
    "Ask yourself if it will matter in 10 years. If it won't, don't sweat it.",
    "Don't forget to celebrate the silent battles that you fought and won",
    "No one else is dwelling on your mistakes. Move the fuck on.",
    "Tell the negative assholes in our head to sit in a corner for a lifelong timeout",
    "Your best is more than enough, I promise.",
    "You are worthy of everything good in this life. Everything.",
    "Be a fucking weirdo. There's power in that",
    "That thing you're self-conscious about is what makes you light up the fucking room",
    "If you don't believe in yourself, how can you expect anyone else to?",
    "You are in control. You are in control. You are in control.",
    "Don't take anyone's shit. You are to be respected. Always.",
    "Your opinions aren't tatoos. You can change them any time.",
)

ACTIVE_PALETTES = (
    ((255, 70, 50), (190, 20, 80)),
    ((30, 190, 140), (15, 70, 95)),
    ((255, 170, 20), (200, 50, 30)),
    ((90, 70, 255), (40, 20, 140)),
    ((40, 210, 255), (20, 90, 160)),
    ((255, 80, 170), (90, 20, 90)),
    ((120, 230, 50), (30, 100, 40)),
)

OFF_HOURS = (
    "Off the clock — rest, hydrate, and move when it feels good",
    "Take some time to enjoy the things you worked hard for!",
)
WEEKEND = (
    "Weekend — enjoy the rest; a short walk still counts",
    "If it is a showerless, stay in bed all day type of day, that's okay",
)

FONT_CANDIDATES = (
    "Helvetica Neue",
    "SF Pro Display",
    "SF Pro Text",
    "Avenir Next",
    "Lucida Grande",
    "Helvetica",
)

CLICK_TAGS = ("completed", "ignore", "lunch", "setup", "done", "start_down", "start_up", "end_down", "end_up", "int20", "int30")


def data_dir() -> Path:
    home = Path.home()
    path = home / "Library" / "Application Support" / "MoveReminder"
    path.mkdir(parents=True, exist_ok=True)
    return path


def prefs_path() -> Path:
    return data_dir() / "prefs.json"


def stats_path() -> Path:
    return data_dir() / "stats.json"


def load_prefs() -> dict:
    try:
        data = json.loads(prefs_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {}
    start = int(data.get("start_hour", DEFAULT_START_HOUR))
    end = int(data.get("end_hour", DEFAULT_END_HOUR))
    interval = int(data.get("interval_minutes", DEFAULT_INTERVAL))
    if start not in START_HOUR_CHOICES:
        start = DEFAULT_START_HOUR
    if end not in END_HOUR_CHOICES:
        end = DEFAULT_END_HOUR
    if start >= end:
        start, end = DEFAULT_START_HOUR, DEFAULT_END_HOUR
    if interval not in INTERVAL_CHOICES:
        interval = DEFAULT_INTERVAL
    return {"start_hour": start, "end_hour": end, "interval_minutes": interval}


def save_prefs(prefs: dict) -> None:
    prefs_path().write_text(json.dumps(prefs, indent=2) + "\n", encoding="utf-8")


def load_stats(day_key: str) -> dict:
    try:
        data = json.loads(stats_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {}
    if data.get("date") != day_key:
        data = {"date": day_key, "completed": 0, "ignored": 0}
    return data


def save_stats(stats: dict) -> None:
    stats_path().write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")


def local_now() -> datetime:
    try:
        time.tzset()
    except (AttributeError, OSError):
        pass
    return datetime.now().astimezone()


def _iana_zone() -> str:
    try:
        resolved = Path("/etc/localtime").resolve()
        parts = resolved.parts
        if "zoneinfo" in parts:
            i = parts.index("zoneinfo")
            return "/".join(parts[i + 1 :])
    except OSError:
        return ""
    return ""


def tz_label(now: datetime) -> str:
    for raw in (now.strftime("%Z"), now.tzname()):
        label = (raw or "").strip()
        if label:
            return label
    isdst = time.localtime().tm_isdst > 0
    names = time.tzname
    if names:
        pick = names[1] if isdst and len(names) > 1 else names[0]
        if pick:
            return pick
    iana = _iana_zone()
    if iana:
        return iana
    key = getattr(now.tzinfo, "key", None)
    if key:
        return str(key)
    return "local"


def hour_label(hour: int) -> str:
    suffix = "AM" if hour < 12 else "PM"
    h12 = hour % 12 or 12
    return f"{h12}:00 {suffix}"


def hours_label(start: int, end: int) -> str:
    return f"{hour_label(start)} - {hour_label(end)}"


def tally_pep(completed: int, ignored: int) -> str:
    """Encouragement from completed / (completed + ignored). Lunch skips are not in ignored."""
    total = completed + ignored
    if total <= 0:
        return "No prompts logged this shift — tomorrow is a fresh start."
    pct = 100.0 * completed / total
    if pct < 50:
        return "Your tally was low, try to beat it tomorrow!"
    if pct < 70:
        return "Good job getting there!"
    if pct < 80:
        return "That was a strong day!"
    if pct < 90:
        return "Great day — keep stacking those wins!"
    if pct < 100:
        return "Excellent work!"
    return (
        "Congratulations! You worked hard to keep your health strong today! "
        "Repeat tomorrow for a stronger body!"
    )


def slot_index(now: datetime, interval: int) -> int:
    minutes = now.hour * 60 + now.minute
    return minutes // interval


def is_morning_half(now: datetime, start: int, end: int) -> bool:
    mid = start + (end - start) / 2
    return (now.hour + now.minute / 60.0) < mid


def pick_line(lines: tuple[str, ...], slot: int) -> str:
    return lines[slot % len(lines)]


def inches_to_px(root: tk.Tk, inches: float) -> int:
    dpi = float(root.winfo_fpixels("1i"))
    return max(1, int(round(inches * dpi)))


def pick_family(root: tk.Tk) -> str:
    families = set(tkfont.families(root))
    for name in FONT_CANDIDATES:
        if name in families:
            return name
    return "TkDefaultFont"


class MoveReminderApp:
    def __init__(self) -> None:
        self.prefs = load_prefs()
        self.stats = load_stats(local_now().date().isoformat())
        self._on_lunch = False
        self._view = "main"
        self._draft_start = self.prefs["start_hour"]
        self._draft_end = self.prefs["end_hour"]
        self._draft_interval = self.prefs["interval_minutes"]

        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.family = pick_family(self.root)

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-alpha", 0.97)
        except tk.TclError:
            pass

        self.height = inches_to_px(self.root, 3.0)
        self.width = inches_to_px(self.root, 4.0)
        self._place_top_center()

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._drag_x = 0
        self._drag_y = 0
        self._color_idx = 0
        self._hidden = False
        self._hide_slot = -1

        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.root.bind("<Escape>", lambda _e: self._on_ignore())
        self.root.bind_all("<Command-w>", lambda _e: self._on_ignore())
        self.root.bind_all("<Command-W>", lambda _e: self._on_ignore())
        self.root.bind_all("<Command-h>", lambda _e: self._on_ignore())
        self.root.bind_all("<Command-H>", lambda _e: self._on_ignore())
        try:
            self.root.createcommand("tk::mac::Quit", self._quit)
        except tk.TclError:
            pass

        self._draw_static_ids()
        self._schedule()

    def _quit(self) -> None:
        self.root.after_idle(self.root.destroy)

    def _day_key(self, now: datetime) -> str:
        return now.date().isoformat()

    def _ensure_stats_day(self, now: datetime) -> None:
        key = self._day_key(now)
        if self.stats.get("date") != key:
            self.stats = {"date": key, "completed": 0, "ignored": 0}
            save_stats(self.stats)

    def _bump(self, field: str) -> None:
        now = local_now()
        self._ensure_stats_day(now)
        self.stats[field] = int(self.stats.get(field, 0)) + 1
        save_stats(self.stats)

    def _hide_until_next(self) -> None:
        if self._hidden:
            return
        self._hidden = True
        self._hide_slot = slot_index(local_now(), self.prefs["interval_minutes"])
        self.root.withdraw()

    def _show(self) -> None:
        if not self._hidden:
            return
        self._hidden = False
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)

    def _on_completed(self, _event: tk.Event | None = None) -> str:
        if self._view != "main":
            return "break"
        now = local_now()
        if self._is_work(now) and not self._on_lunch:
            self._bump("completed")
        self.root.after_idle(self._hide_until_next)
        return "break"

    def _on_ignore(self, _event: tk.Event | None = None) -> str:
        if self._view != "main":
            return "break"
        now = local_now()
        if self._is_work(now) and not self._on_lunch:
            self._bump("ignored")
        self.root.after_idle(self._hide_until_next)
        return "break"

    def _on_lunch(self, _event: tk.Event | None = None) -> str:
        self._on_lunch = not self._on_lunch
        if self._on_lunch:
            self.root.after_idle(self._hide_until_next)
        return "break"

    def _open_setup(self, _event: tk.Event | None = None) -> str:
        self._draft_start = self.prefs["start_hour"]
        self._draft_end = self.prefs["end_hour"]
        self._draft_interval = self.prefs["interval_minutes"]
        self._view = "settings"
        self._apply_view()
        return "break"

    def _close_setup(self, _event: tk.Event | None = None) -> str:
        if self._draft_start < self._draft_end:
            self.prefs = {
                "start_hour": self._draft_start,
                "end_hour": self._draft_end,
                "interval_minutes": self._draft_interval,
            }
            save_prefs(self.prefs)
        self._view = "main"
        self._apply_view()
        return "break"

    def _nudge_start(self, delta: int, _event: tk.Event | None = None) -> str:
        idx = START_HOUR_CHOICES.index(self._draft_start) if self._draft_start in START_HOUR_CHOICES else 0
        idx = max(0, min(len(START_HOUR_CHOICES) - 1, idx + delta))
        self._draft_start = START_HOUR_CHOICES[idx]
        if self._draft_start >= self._draft_end:
            for hour in END_HOUR_CHOICES:
                if hour > self._draft_start:
                    self._draft_end = hour
                    break
        self._refresh_settings_labels()
        return "break"

    def _nudge_end(self, delta: int, _event: tk.Event | None = None) -> str:
        idx = END_HOUR_CHOICES.index(self._draft_end) if self._draft_end in END_HOUR_CHOICES else 0
        idx = max(0, min(len(END_HOUR_CHOICES) - 1, idx + delta))
        self._draft_end = END_HOUR_CHOICES[idx]
        if self._draft_end <= self._draft_start:
            for hour in reversed(START_HOUR_CHOICES):
                if hour < self._draft_end:
                    self._draft_start = hour
                    break
        self._refresh_settings_labels()
        return "break"

    def _set_interval(self, minutes: int, _event: tk.Event | None = None) -> str:
        self._draft_interval = minutes
        self._refresh_settings_labels()
        return "break"

    def _is_work(self, now: datetime) -> bool:
        if now.weekday() not in WORK_WEEKDAYS:
            return False
        return self.prefs["start_hour"] <= now.hour < self.prefs["end_hour"]

    def _status(self, now: datetime) -> tuple[str, str, str, int]:
        slot = slot_index(now, self.prefs["interval_minutes"])
        morning = is_morning_half(now, self.prefs["start_hour"], self.prefs["end_hour"])
        motivations = MORNING_MOTIVATIONS if morning else AFTERNOON_MOTIVATIONS
        motivation = pick_line(motivations, slot)
        if now.weekday() not in WORK_WEEKDAYS:
            return "weekend", pick_line(WEEKEND, slot), motivation, slot
        if self._on_lunch and self._is_work(now):
            return (
                "lunch",
                "On lunch — this slot is not counted as a skip. Tap Lunch when you are back.",
                "Eat, rest, and come back when you are ready",
                slot,
            )
        if self._is_work(now):
            reminders = MORNING_REMINDERS if morning else AFTERNOON_REMINDERS
            period = "Morning wakeup" if morning else "Afternoon reset"
            return "active", f"{period}: {pick_line(reminders, slot)}", motivation, slot
        if now.hour >= self.prefs["end_hour"]:
            completed = int(self.stats.get("completed", 0))
            ignored = int(self.stats.get("ignored", 0))
            tally = f"Shift tally · {completed} completed · {ignored} ignored"
            pep = tally_pep(completed, ignored)
            return "off", f"{tally}. {pep}", pep, slot
        return "off", pick_line(OFF_HOURS, slot), motivation, slot

    def _start_drag(self, event: tk.Event) -> None:
        tags = set(self.canvas.gettags("current"))
        if tags & set(CLICK_TAGS):
            return
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

    def _place_top_center(self) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        x = max(0, (sw - self.width) // 2)
        y = 28
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def _on_drag(self, event: tk.Event) -> None:
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def _font(self, size: int, weight: str = "normal") -> tuple:
        if weight == "bold":
            return (self.family, size, "bold")
        return (self.family, size)

    def _draw_static_ids(self) -> None:
        self.bg_rects: list[int] = []
        bands = 36
        for i in range(bands):
            rid = self.canvas.create_rectangle(
                0,
                i * (self.height / bands),
                self.width,
                (i + 1) * (self.height / bands) + 1,
                outline="",
                fill="#222222",
            )
            self.bg_rects.append(rid)

        pad = 14
        inner_w = self.width - pad * 2
        self.main_items: list[int] = []
        self.settings_items: list[int] = []

        self.title_line = self.canvas.create_text(
            pad,
            pad + 2,
            anchor="nw",
            fill="#fff8e7",
            font=self._font(11, "bold"),
            text=f"{APP_NAME}  ·  local",
        )
        self.clock = self.canvas.create_text(
            pad,
            self.height * 0.24,
            anchor="w",
            fill="#ffffff",
            font=self._font(26, "bold"),
            text="--:--:--",
        )
        self.date_line = self.canvas.create_text(
            pad,
            self.height * 0.42,
            anchor="w",
            fill="#ffe8c8",
            font=self._font(12),
            text="",
        )
        self.hours_line = self.canvas.create_text(
            pad,
            self.height * 0.52,
            anchor="w",
            fill="#ffe8c8",
            font=self._font(12),
            text="",
            tags=("setup",),
        )
        self.motivation_line = self.canvas.create_text(
            pad,
            self.height * 0.64,
            anchor="w",
            fill="#fff4d6",
            font=self._font(11, "bold"),
            width=inner_w,
            text="",
        )
        self.prompt = self.canvas.create_text(
            pad,
            self.height - 36,
            anchor="sw",
            fill="#ffffff",
            font=self._font(11, "bold"),
            width=inner_w,
            text="",
        )
        btn_y = self.height - 12
        self.completed_hit = self.canvas.create_text(
            pad,
            btn_y,
            anchor="sw",
            fill="#fff8e7",
            font=self._font(11, "bold"),
            text="Completed",
            tags=("completed",),
        )
        self.ignore_hit = self.canvas.create_text(
            pad + 92,
            btn_y,
            anchor="sw",
            fill="#fff8e7",
            font=self._font(11, "bold"),
            text="Ignore",
            tags=("ignore",),
        )
        self.lunch_hit = self.canvas.create_text(
            pad + 150,
            btn_y,
            anchor="sw",
            fill="#fff8e7",
            font=self._font(11, "bold"),
            text="Lunch",
            tags=("lunch",),
        )
        self.setup_hit = self.canvas.create_text(
            self.width - 14,
            12,
            anchor="ne",
            fill="#fff8e7",
            font=self._font(11),
            text="Setup",
            tags=("setup",),
        )
        self.main_items = [
            self.title_line,
            self.clock,
            self.date_line,
            self.hours_line,
            self.motivation_line,
            self.prompt,
            self.completed_hit,
            self.ignore_hit,
            self.lunch_hit,
            self.setup_hit,
        ]
        self.canvas.tag_bind("completed", "<Button-1>", self._on_completed)
        self.canvas.tag_bind("ignore", "<Button-1>", self._on_ignore)
        self.canvas.tag_bind("lunch", "<Button-1>", self._on_lunch)
        self.canvas.tag_bind("setup", "<Button-1>", self._open_setup)

        self.settings_title = self.canvas.create_text(
            pad,
            pad + 2,
            anchor="nw",
            fill="#fff8e7",
            font=self._font(12, "bold"),
            text=f"Shift setup  ·  v{APP_VERSION}",
            state="hidden",
        )
        self.start_label = self.canvas.create_text(
            pad,
            self.height * 0.28,
            anchor="w",
            fill="#ffffff",
            font=self._font(13, "bold"),
            text="",
            state="hidden",
        )
        self.start_down = self.canvas.create_text(
            self.width - 52,
            self.height * 0.28,
            anchor="e",
            fill="#fff8e7",
            font=self._font(16, "bold"),
            text="−",
            state="hidden",
            tags=("start_down",),
        )
        self.start_up = self.canvas.create_text(
            self.width - 18,
            self.height * 0.28,
            anchor="e",
            fill="#fff8e7",
            font=self._font(16, "bold"),
            text="+",
            state="hidden",
            tags=("start_up",),
        )
        self.end_label = self.canvas.create_text(
            pad,
            self.height * 0.46,
            anchor="w",
            fill="#ffffff",
            font=self._font(13, "bold"),
            text="",
            state="hidden",
        )
        self.end_down = self.canvas.create_text(
            self.width - 52,
            self.height * 0.46,
            anchor="e",
            fill="#fff8e7",
            font=self._font(16, "bold"),
            text="−",
            state="hidden",
            tags=("end_down",),
        )
        self.end_up = self.canvas.create_text(
            self.width - 18,
            self.height * 0.46,
            anchor="e",
            fill="#fff8e7",
            font=self._font(16, "bold"),
            text="+",
            state="hidden",
            tags=("end_up",),
        )
        self.interval_label = self.canvas.create_text(
            pad,
            self.height * 0.64,
            anchor="w",
            fill="#ffffff",
            font=self._font(13, "bold"),
            text="",
            state="hidden",
        )
        self.int20 = self.canvas.create_text(
            self.width - 70,
            self.height * 0.64,
            anchor="e",
            fill="#fff8e7",
            font=self._font(12, "bold"),
            text="20",
            state="hidden",
            tags=("int20",),
        )
        self.int30 = self.canvas.create_text(
            self.width - 18,
            self.height * 0.64,
            anchor="e",
            fill="#fff8e7",
            font=self._font(12, "bold"),
            text="30",
            state="hidden",
            tags=("int30",),
        )
        self.done_hit = self.canvas.create_text(
            self.width - 14,
            self.height - 12,
            anchor="se",
            fill="#fff8e7",
            font=self._font(12, "bold"),
            text="Done",
            state="hidden",
            tags=("done",),
        )
        self.settings_credit = self.canvas.create_text(
            pad,
            self.height - 12,
            anchor="sw",
            fill="#ffe8c8",
            font=self._font(9),
            text=MADE_WITH,
            state="hidden",
        )
        self.settings_items = [
            self.settings_title,
            self.start_label,
            self.start_down,
            self.start_up,
            self.end_label,
            self.end_down,
            self.end_up,
            self.interval_label,
            self.int20,
            self.int30,
            self.done_hit,
            self.settings_credit,
        ]
        self.canvas.tag_bind("done", "<Button-1>", self._close_setup)
        self.canvas.tag_bind("start_down", "<Button-1>", lambda e: self._nudge_start(-1, e))
        self.canvas.tag_bind("start_up", "<Button-1>", lambda e: self._nudge_start(1, e))
        self.canvas.tag_bind("end_down", "<Button-1>", lambda e: self._nudge_end(-1, e))
        self.canvas.tag_bind("end_up", "<Button-1>", lambda e: self._nudge_end(1, e))
        self.canvas.tag_bind("int20", "<Button-1>", lambda e: self._set_interval(20, e))
        self.canvas.tag_bind("int30", "<Button-1>", lambda e: self._set_interval(30, e))

    def _set_items(self, items: list[int], state: str) -> None:
        for item in items:
            self.canvas.itemconfigure(item, state=state)

    def _apply_view(self) -> None:
        if self._view == "settings":
            self._set_items(self.main_items, "hidden")
            self._set_items(self.settings_items, "normal")
            self._refresh_settings_labels()
        else:
            self._set_items(self.settings_items, "hidden")
            self._set_items(self.main_items, "normal")

    def _refresh_settings_labels(self) -> None:
        self.canvas.itemconfigure(self.start_label, text=f"Start  {hour_label(self._draft_start)}")
        self.canvas.itemconfigure(self.end_label, text=f"End    {hour_label(self._draft_end)}")
        mark20 = "• 20" if self._draft_interval == 20 else "20"
        mark30 = "• 30" if self._draft_interval == 30 else "30"
        self.canvas.itemconfigure(self.interval_label, text="Interval (min)")
        self.canvas.itemconfigure(self.int20, text=mark20)
        self.canvas.itemconfigure(self.int30, text=mark30)

    def _hex(self, r: float, g: float, b: float) -> str:
        def c(v: float) -> int:
            return max(0, min(255, int(v)))

        return f"#{c(r):02x}{c(g):02x}{c(b):02x}"

    def _palette(self, mode: str, color_idx: int) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        if mode == "active":
            return ACTIVE_PALETTES[color_idx % len(ACTIVE_PALETTES)]
        if mode == "lunch":
            return (40, 120, 90), (20, 50, 60)
        if mode == "weekend":
            return (90, 40, 160), (40, 140, 180)
        return (50, 70, 110), (30, 40, 70)

    def _paint_gradient(self, mode: str, color_idx: int) -> None:
        top, bot = self._palette(mode, color_idx)
        n = len(self.bg_rects)
        for i, rid in enumerate(self.bg_rects):
            u = i / max(1, n - 1)
            r = top[0] * (1 - u) + bot[0] * u
            g = top[1] * (1 - u) + bot[1] * u
            b = top[2] * (1 - u) + bot[2] * u
            self.canvas.itemconfigure(rid, fill=self._hex(r, g, b))

    def _schedule(self) -> None:
        now = local_now()
        self._ensure_stats_day(now)
        mode, message, motivation, color_idx = self._status(now)
        slot = slot_index(now, self.prefs["interval_minutes"])
        if color_idx != self._color_idx:
            self._color_idx = color_idx
        self._paint_gradient(mode, color_idx)

        if self._view == "main":
            lunch_mark = "  ·  lunch" if self._on_lunch else ""
            self.canvas.itemconfigure(
                self.title_line,
                text=f"{APP_NAME}  ·  {tz_label(now)}{lunch_mark}",
            )
            self.canvas.itemconfigure(self.clock, text=now.strftime("%I:%M:%S %p").lstrip("0"))
            self.canvas.itemconfigure(
                self.date_line,
                text=f"{now.strftime('%A')}  ·  {now.strftime('%b %d, %Y')}",
            )
            self.canvas.itemconfigure(
                self.hours_line,
                text=hours_label(self.prefs['start_hour'], self.prefs['end_hour']),
            )
            self.canvas.itemconfigure(self.motivation_line, text=motivation)
            self.canvas.itemconfigure(self.prompt, text=message)
            self.canvas.itemconfigure(self.lunch_hit, text="Back" if self._on_lunch else "Lunch")

        show_modes = {"active", "lunch"}
        if self._hidden and mode in show_modes and slot != self._hide_slot:
            self._show()

        self.root.after(250, self._schedule)

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    MoveReminderApp().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
