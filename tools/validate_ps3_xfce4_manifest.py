#!/usr/bin/env python3
"""Validate the PS3 XFCE4 package candidate manifest without claiming dependency closure."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "linux/rootfs/ps3.packages"
DESKTOP = ROOT / "linux/rootfs/ps3-xfce4.packages"

def read_names(path: pathlib.Path) -> list[str]:
    if not path.is_file():
        raise ValueError(f"missing manifest: {path.relative_to(ROOT)}")
    names = []
    for line in path.read_text(encoding="utf-8").splitlines():
        name = line.split("#", 1)[0].strip()
        if name:
            names.append(name)
    if not names:
        raise ValueError(f"empty manifest: {path.relative_to(ROOT)}")
    if len(names) != len(set(names)):
        raise ValueError(f"duplicate package names in {path.relative_to(ROOT)}")
    for name in names:
        if "/" in name or name.startswith("-") or any(ch.isspace() for ch in name):
            raise ValueError(f"invalid package name {name!r}")
    return names

def main() -> int:
    try:
        base = read_names(BASE)
        desktop = read_names(DESKTOP)
        missing = sorted(set(base) - set(desktop))
        if missing:
            raise ValueError("XFCE4 manifest omits base packages: " + ", ".join(missing))
        required = {
            "xorg-server", "xf86-input-evdev", "xf86-video-fbdev",
            "gtk+3", "dbus", "xfce4", "xfce4-session", "xfce4-panel",
            "xfdesktop", "xfwm4", "xfce4-settings", "xfconf", "thunar",
        }
        absent = sorted(required - set(desktop))
        if absent:
            raise ValueError("XFCE4 manifest missing core candidates: " + ", ".join(absent))
        print(
            f"PS3 XFCE4 manifest: OK ({len(desktop)} unique candidates; "
            "PPC64 ABI, package availability and dependency closure NOT verified)"
        )
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
