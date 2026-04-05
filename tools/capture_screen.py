#!/usr/bin/env python3
"""
Screen Capture Tool - Cross-platform (Windows/Linux)
Captures full screen, active window, or specific region.
Saves to {project}/screenshot/YYYYMMDD_HHMMSS.png
"""

import sys
import os
import argparse
from datetime import datetime

def get_save_path(project_dir):
    """Create screenshot directory and return timestamped file path."""
    screenshot_dir = os.path.join(project_dir, "screenshot")
    os.makedirs(screenshot_dir, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    return os.path.join(screenshot_dir, filename)


def capture_full_screen(save_path, monitor_index=0):
    """Capture full screen."""
    import mss
    with mss.mss() as sct:
        # monitor 0 = all monitors, 1 = primary, 2+ = secondary
        monitor = sct.monitors[monitor_index + 1] if monitor_index < len(sct.monitors) - 1 else sct.monitors[1]
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
    return save_path


def capture_region(save_path, left, top, width, height):
    """Capture specific region."""
    import mss
    region = {"left": left, "top": top, "width": width, "height": height}
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
    return save_path


def capture_active_window(save_path):
    """Capture the active (foreground) window."""
    import mss
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        region = {
            "left": rect.left,
            "top": rect.top,
            "width": rect.right - rect.left,
            "height": rect.bottom - rect.top,
        }
    else:
        # Linux: use xdotool
        import subprocess
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowgeometry", "--shell"],
            capture_output=True, text=True
        )
        geo = {}
        for line in result.stdout.strip().split("\n"):
            if "=" in line:
                k, v = line.split("=", 1)
                geo[k.strip()] = int(v.strip())

        result2 = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowfocus", "getactivewindow"],
            capture_output=True, text=True
        )
        wid = result2.stdout.strip().split("\n")[0]
        size_result = subprocess.run(
            ["xwininfo", "-id", wid],
            capture_output=True, text=True
        )
        width = height = 0
        abs_x = abs_y = 0
        for line in size_result.stdout.split("\n"):
            line = line.strip()
            if "Absolute upper-left X:" in line:
                abs_x = int(line.split(":")[-1].strip())
            elif "Absolute upper-left Y:" in line:
                abs_y = int(line.split(":")[-1].strip())
            elif "Width:" in line:
                width = int(line.split(":")[-1].strip())
            elif "Height:" in line:
                height = int(line.split(":")[-1].strip())
        region = {"left": abs_x, "top": abs_y, "width": width, "height": height}

    with mss.mss() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
    return save_path


def main():
    parser = argparse.ArgumentParser(description="Screen Capture Tool")
    parser.add_argument("--project", required=True, help="Project root directory")
    parser.add_argument("--mode", choices=["full", "active", "region"], default="active",
                        help="Capture mode: full(full screen), active(active window), region(specific area)")
    parser.add_argument("--monitor", type=int, default=0, help="Monitor index for full screen mode")
    parser.add_argument("--left", type=int, default=0)
    parser.add_argument("--top", type=int, default=0)
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--height", type=int, default=600)

    args = parser.parse_args()
    save_path = get_save_path(args.project)

    if args.mode == "full":
        result = capture_full_screen(save_path, args.monitor)
    elif args.mode == "active":
        result = capture_active_window(save_path)
    elif args.mode == "region":
        result = capture_region(save_path, args.left, args.top, args.width, args.height)

    print(result)


if __name__ == "__main__":
    main()
