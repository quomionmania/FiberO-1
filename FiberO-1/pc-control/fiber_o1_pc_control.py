"""
FiberO-1 PC Control Prototype (Windows)
--------------------------------------
Experimental local prototype that demonstrates:
- Dark overlay with "FiberO using the PC"
- Mouse/keyboard control primitives via pynput
- Global Esc kill switch (immediate stop)

Safety:
- Run only on your own machine.
- Save work before using control mode.
- Press Esc at any time to stop control immediately.
"""

from __future__ import annotations

import argparse
import ctypes
import queue
import sys
import threading
import time
import tkinter as tk
from dataclasses import dataclass

try:
    from pynput import keyboard, mouse
    from pynput.keyboard import Controller as KeyboardController, Key
    from pynput.mouse import Button, Controller as MouseController
except Exception as exc:  # pragma: no cover - dependency/runtime guard
    print("Missing dependency: pynput")
    print("Install with: python -m pip install pynput pillow")
    print(f"Import error: {exc}")
    sys.exit(1)


@dataclass
class ControlState:
    running: bool = True
    controlling: bool = False
    last_action: str = "Idle"


class OverlayUI:
    def __init__(self, state: ControlState, stop_event: threading.Event):
        self.state = state
        self.stop_event = stop_event
        self.root = tk.Tk()
        self.root.title("FiberO-1 PC Control")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.82)
        self.root.configure(bg="#050505")

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        border = 8
        self.root.geometry(f"{sw}x{sh}+0+0")

        # Outer frame creates a dark "glow"/border effect.
        self.frame = tk.Frame(self.root, bg="#0b0f14", highlightthickness=border, highlightbackground="#1f2937")
        self.frame.pack(fill="both", expand=True)

        self.center = tk.Frame(self.frame, bg="#050505")
        self.center.place(relx=0.5, rely=0.08, anchor="n")

        self.label = tk.Label(
            self.center,
            text="FiberO using the PC",
            font=("Segoe UI", 28, "bold"),
            fg="#7dd3fc",
            bg="#050505",
        )
        self.label.pack(padx=24, pady=(18, 6))

        self.sub = tk.Label(
            self.center,
            text="Esc to interrupt  |  Experimental prototype",
            font=("Segoe UI", 12),
            fg="#cbd5e1",
            bg="#050505",
        )
        self.sub.pack(padx=24, pady=(0, 8))

        self.status = tk.Label(
            self.center,
            text="Status: Idle",
            font=("Consolas", 11),
            fg="#94a3b8",
            bg="#050505",
        )
        self.status.pack(padx=24, pady=(0, 18))

        # Click-through-ish behavior is not fully possible in pure tkinter; keep it small-ish visually by transparency.
        # The overlay is topmost to be visible. User can stop with Esc.
        self.root.bind("<Escape>", lambda _e: self.request_stop())
        self._pulse = 0
        self._tick()

    def _tick(self):
        if self.stop_event.is_set() or not self.state.running:
            self.close()
            return
        self._pulse = (self._pulse + 1) % 40
        # Subtle glow pulse by changing border color.
        glow = "#38bdf8" if self._pulse < 20 else "#0ea5e9"
        self.frame.configure(highlightbackground=glow)
        status = "CONTROLLING" if self.state.controlling else "IDLE"
        self.status.configure(text=f"Status: {status} | {self.state.last_action}")
        self.root.after(120, self._tick)

    def request_stop(self):
        self.state.running = False
        self.state.last_action = "Esc pressed - stopping"
        self.stop_event.set()

    def close(self):
        try:
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()


class PcController:
    def __init__(self, state: ControlState, stop_event: threading.Event):
        self.state = state
        self.stop_event = stop_event
        self.mouse = MouseController()
        self.kbd = KeyboardController()

    def _check(self):
        if self.stop_event.is_set() or not self.state.running:
            raise KeyboardInterrupt("Stopped by user")

    def move_mouse(self, x: int, y: int, duration: float = 0.4):
        self._check()
        start = self.mouse.position
        steps = max(1, int(duration / 0.01))
        for i in range(1, steps + 1):
            self._check()
            nx = int(start[0] + (x - start[0]) * (i / steps))
            ny = int(start[1] + (y - start[1]) * (i / steps))
            self.mouse.position = (nx, ny)
            time.sleep(duration / steps)
        self.state.last_action = f"Mouse moved to ({x},{y})"

    def click(self, x: int | None = None, y: int | None = None, button: str = "left"):
        self._check()
        if x is not None and y is not None:
            self.move_mouse(x, y, duration=0.2)
        btn = Button.left if button == "left" else Button.right if button == "right" else Button.middle
        self.mouse.click(btn, 1)
        self.state.last_action = f"Click {button} at {self.mouse.position}"

    def type_text(self, text: str, interval: float = 0.02):
        self._check()
        for ch in text:
            self._check()
            self.kbd.type(ch)
            time.sleep(interval)
        self.state.last_action = f"Typed {len(text)} chars"

    def press(self, key_name: str):
        self._check()
        key = getattr(Key, key_name, None)
        if key is None:
            if len(key_name) == 1:
                self.kbd.press(key_name)
                self.kbd.release(key_name)
            else:
                raise ValueError(f"Unknown key: {key_name}")
        else:
            self.kbd.press(key)
            self.kbd.release(key)
        self.state.last_action = f"Pressed {key_name}"


def start_esc_listener(state: ControlState, stop_event: threading.Event):
    def on_press(key):
        if key == keyboard.Key.esc:
            state.running = False
            state.last_action = "Esc pressed - stopping"
            stop_event.set()
            return False
        return True

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener


def demo_sequence(controller: PcController, state: ControlState, stop_event: threading.Event):
    """Safe demo: moves mouse in a small square and does not click/type into apps."""
    state.controlling = True
    state.last_action = "Demo: moving mouse in safe square"
    try:
        # Move near center-ish area; no clicks, no typing.
        w = ctypes.windll.user32.GetSystemMetrics(0)
        h = ctypes.windll.user32.GetSystemMetrics(1)
        cx, cy = w // 2, h // 2
        points = [(cx - 120, cy - 80), (cx + 120, cy - 80), (cx + 120, cy + 80), (cx - 120, cy + 80)]
        for _ in range(2):
            for x, y in points:
                if stop_event.is_set():
                    break
                controller.move_mouse(x, y, duration=0.25)
                time.sleep(0.1)
        state.last_action = "Demo complete"
    except KeyboardInterrupt:
        state.last_action = "Interrupted by Esc"
    finally:
        state.controlling = False
        # Keep overlay visible briefly, then stop.
        time.sleep(0.5)
        state.running = False
        stop_event.set()


def parse_args():
    p = argparse.ArgumentParser(description="FiberO-1 PC Control Prototype")
    p.add_argument("--demo", action="store_true", help="Run a safe mouse-movement demo (no clicks/typing)")
    p.add_argument("--overlay-only", action="store_true", help="Show overlay only until Esc")
    return p.parse_args()


def main():
    args = parse_args()
    state = ControlState()
    stop_event = threading.Event()

    listener = start_esc_listener(state, stop_event)

    if args.demo:
        controller = PcController(state, stop_event)
        t = threading.Thread(target=demo_sequence, args=(controller, state, stop_event), daemon=True)
        t.start()
    elif args.overlay_only:
        state.last_action = "Overlay only - press Esc to exit"
    else:
        state.last_action = "Overlay only (default) - press Esc to exit"

    ui = OverlayUI(state, stop_event)
    try:
        ui.run()
    finally:
        stop_event.set()
        state.running = False
        try:
            listener.stop()
        except Exception:
            pass


if __name__ == "__main__":
    main()
