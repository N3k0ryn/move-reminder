"""Move Reminder for macOS — always-on-top 3x4 inch strip with time and movement prompts."""

from __future__ import annotations

import sys
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import font as tkfont

WORK_START_HOUR = 9
WORK_END_HOUR = 17
WORK_WEEKDAYS = {0, 1, 2, 3, 4}  # Monday–Friday
ROTATE_MINUTES = 20

REMINDERS = (
    "Walk it out — get those steps in",
    "Stand up: 10 air squats",
    "Desk push-ups or wall push-ups — 8–12",
    "Stretch: neck, shoulders, hips",
    "Calf raises while you wait",
    "Plank or dead hang for 20–30s",
    "March in place for one minute",
)

MOTIVATIONS = (
    "A healthy body and mind keeps you grounded",
    "Hydrate — have you yet?",
    "You are doing great!",
    "Breathe and exhale your stress",
    "Remember you are the author of your life",
    "Small moves add up to a stronger you",
    "Be kind to yourself in this hour",
    "Show up for you — that’s enough",
    "Unclench your jaw. Drop your shoulders.",
    "Progress, not perfection",
)

# Distinct looks so a new suggestion is obvious at a glance.
ACTIVE_PALETTES = (
    ((255, 70, 50), (190, 20, 80)),
    ((30, 190, 140), (15, 70, 95)),
    ((255, 170, 20), (200, 50, 30)),
    ((90, 70, 255), (40, 20, 140)),
    ((40, 210, 255), (20, 90, 160)),
    ((255, 80, 170), (90, 20, 90)),
    ((120, 230, 50), (30, 100, 40)),
)

OFF_HOURS = "Off the clock — rest, hydrate, and move when it feels good"
WEEKEND = "Weekend — enjoy the rest; a short walk still counts"

FONT_CANDIDATES = (
    "Helvetica Neue",
    "SF Pro Display",
    "SF Pro Text",
    "Avenir Next",
    "Lucida Grande",
    "Helvetica",
)


def is_work_window(now: datetime) -> bool:
    if now.weekday() not in WORK_WEEKDAYS:
        return False
    return WORK_START_HOUR <= now.hour < WORK_END_HOUR


def slot_index(now: datetime) -> int:
    minutes = now.hour * 60 + now.minute
    return minutes // ROTATE_MINUTES


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


def status_for(now: datetime) -> tuple[str, str, str, int]:
    slot = slot_index(now)
    motivation = MOTIVATIONS[slot % len(MOTIVATIONS)]
    if now.weekday() not in WORK_WEEKDAYS:
        return "weekend", WEEKEND, motivation, slot
    if is_work_window(now):
        idx = slot % len(REMINDERS)
        return "active", REMINDERS[idx], motivation, idx
    return "off", OFF_HOURS, motivation, slot


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
        self.root = tk.Tk()
        self.root.title("Move Reminder")
        self.family = pick_family(self.root)

        # Borderless float. Aqua Tk needs both topmost and overrideredirect.
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

        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.root.bind("<Escape>", lambda _e: self._quit())
        try:
            self.root.createcommand("tk::mac::Quit", self._quit)
        except tk.TclError:
            pass

        self._draw_static_ids()
        self._schedule()

    def _quit(self) -> None:
        self.root.after_idle(self.root.destroy)

    def _place_top_center(self) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        x = max(0, (sw - self.width) // 2)
        y = 28  # sit below the menu bar
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def _start_drag(self, event: tk.Event) -> None:
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

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
        self.title_line = self.canvas.create_text(
            pad,
            pad + 2,
            anchor="nw",
            fill="#fff8e7",
            font=self._font(12, "bold"),
            text="Move Reminder  ·  local",
        )
        self.clock = self.canvas.create_text(
            pad,
            self.height * 0.26,
            anchor="w",
            fill="#ffffff",
            font=self._font(28, "bold"),
            text="--:--:--",
        )
        self.date_line = self.canvas.create_text(
            pad,
            self.height * 0.46,
            anchor="w",
            fill="#ffe8c8",
            font=self._font(13),
            text="",
        )
        self.hours_line = self.canvas.create_text(
            pad,
            self.height * 0.56,
            anchor="w",
            fill="#ffe8c8",
            font=self._font(13),
            text="9:00 AM - 5:00 PM",
        )
        self.motivation_line = self.canvas.create_text(
            pad,
            self.height * 0.70,
            anchor="w",
            fill="#fff4d6",
            font=self._font(12, "bold"),
            width=inner_w,
            text="",
        )
        self.prompt = self.canvas.create_text(
            pad,
            self.height - pad - 6,
            anchor="sw",
            fill="#ffffff",
            font=self._font(12, "bold"),
            width=inner_w,
            text="",
        )

    def _hex(self, r: float, g: float, b: float) -> str:
        def c(v: float) -> int:
            return max(0, min(255, int(v)))

        return f"#{c(r):02x}{c(g):02x}{c(b):02x}"

    def _palette(self, mode: str, color_idx: int) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        if mode == "active":
            return ACTIVE_PALETTES[color_idx % len(ACTIVE_PALETTES)]
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
        mode, message, motivation, color_idx = status_for(now)
        if color_idx != self._color_idx:
            self._color_idx = color_idx
        self._paint_gradient(mode, color_idx)

        self.canvas.itemconfigure(
            self.title_line,
            text=f"Move Reminder  ·  {tz_label(now)}",
        )
        self.canvas.itemconfigure(self.clock, text=now.strftime("%I:%M:%S %p").lstrip("0"))
        self.canvas.itemconfigure(
            self.date_line,
            text=f"{now.strftime('%A')}  ·  {now.strftime('%b %d, %Y')}",
        )
        self.canvas.itemconfigure(self.hours_line, text="9:00 AM - 5:00 PM")
        self.canvas.itemconfigure(self.motivation_line, text=motivation)
        self.canvas.itemconfigure(self.prompt, text=message)

        self.root.after(250, self._schedule)

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    MoveReminderApp().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
