#!/usr/bin/env python3
"""Check Snakey's PS3 profile and kernel requirements overlay."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
profile = json.loads((ROOT / "platforms/linux-targets.json").read_text())
target = next(item for item in profile["targets"] if item["id"] == "ps3")
fragment = ROOT / "linux/targets/ps3/kernel.fragment"
settings = {}
for raw in fragment.read_text().splitlines():
    line = raw.strip()
    if line.startswith("CONFIG_") and "=" in line:
        key, value = line.split("=", 1)
        settings[key] = value

required = {
    "CONFIG_PPC64": "y",
    "CONFIG_PPC_BOOK3S": "y",
    "CONFIG_CPU_BIG_ENDIAN": "y",
    "CONFIG_PPC_PS3": "y",
    "CONFIG_PS3_DISK": "y",
    "CONFIG_FB_PS3": "y",
    "CONFIG_GELIC_NET": "y",
    "CONFIG_USB": "y",
    "CONFIG_USB_EHCI_HCD": "y",
    "CONFIG_USB_OHCI_HCD": "y",
    "CONFIG_USB_HID": "y",
    "CONFIG_DEVTMPFS": "y",
    "CONFIG_DEVTMPFS_MOUNT": "y",
}
missing = [key for key, value in required.items() if settings.get(key) != value]
if missing:
    raise SystemExit("Missing PS3 kernel requirements: " + ", ".join(missing))
if target["system_ram_mb"] != 256:
    raise SystemExit("PS3 system RAM must remain 256 MiB; do not add video RAM to this value")
if target["status"] != "source-audit-required" or target["snakey_kernel_built"] or target["snakey_hardware_tested"]:
    raise SystemExit("PS3 must remain explicitly unbuilt and untested until evidence exists")
print("Snakey PS3 profile and kernel requirements: OK (configuration not built)")
