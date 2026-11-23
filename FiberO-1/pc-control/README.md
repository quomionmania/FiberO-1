# FiberO-1 PC Control Prototype (Windows)

Experimental prototype for the FiberO-1 "use the PC" mode.

## What it does

- Shows a topmost dark overlay with: **FiberO using the PC**
- Displays status and an Esc interrupt hint
- Listens for global **Esc** to stop immediately
- Includes safe demo mode (`--demo`) that moves the mouse in a square (no clicks, no typing)

## Requirements

- Windows
- Python 3.10+
- `pynput` (required)
- `pillow` (optional for future extensions)

Install:

```powershell
python -m pip install -r .\requirements.txt
```

## Run

Overlay only:

```powershell
python .\fiber_o1_pc_control.py --overlay-only
```

Safe demo:

```powershell
python .\fiber_o1_pc_control.py --demo
```

Stop anytime with **Esc**.

## Safety

- This prototype can control input devices when extended.
- Do not run it while unsaved sensitive work is open.
- Esc is the emergency stop. Keep it accessible.
- Do not use for bypassing security prompts, passwords, or UAC.
