#!/usr/bin/env python3
"""Validate Snakey's Linux-capable hardware target registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "platforms" / "linux-targets.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read Linux target registry: {exc}")

    if data.get("schema_version") != 1:
        fail("schema_version must be 1")
    targets = data.get("targets")
    if not isinstance(targets, list) or not targets:
        fail("targets must be a non-empty array")

    seen = set()
    for index, target in enumerate(targets):
        prefix = f"targets[{index}]"
        if not isinstance(target, dict):
            fail(f"{prefix} must be an object")
        required = (
            "id", "name", "family", "architecture", "cpu", "system_ram_mb",
            "video_ram_mb", "video_ram_counts_as_system_ram",
            "kernel_platform_option", "boot_chain", "storage", "graphics",
            "network", "desktop_goal", "status", "snakey_tested",
            "requires_physical_hardware",
        )
        for field in required:
            if field not in target:
                fail(f"{prefix} is missing {field}")
        target_id = target["id"]
        if not isinstance(target_id, str) or not target_id or target_id in seen:
            fail(f"{prefix}.id must be unique and non-empty")
        seen.add(target_id)
        if target["family"] != "linux-system":
            fail(f"{prefix}.family must be linux-system")
        for field in ("system_ram_mb", "video_ram_mb"):
            if not isinstance(target[field], int) or target[field] <= 0:
                fail(f"{prefix}.{field} must be a positive integer")
        if not isinstance(target["video_ram_counts_as_system_ram"], bool):
            fail(f"{prefix}.video_ram_counts_as_system_ram must be boolean")
        if not isinstance(target["boot_chain"], list) or not target["boot_chain"]:
            fail(f"{prefix}.boot_chain must be a non-empty list")
        if not isinstance(target["snakey_tested"], bool):
            fail(f"{prefix}.snakey_tested must be boolean")
        if not isinstance(target["requires_physical_hardware"], bool):
            fail(f"{prefix}.requires_physical_hardware must be boolean")
        if target["status"] not in {"research-candidate", "kernel-buildable", "kernel-boots", "userspace-boots", "desktop-tested"}:
            fail(f"{prefix}.status is unsupported")
        if target["snakey_tested"] and target["status"] == "research-candidate":
            fail(f"{prefix}: tested target cannot remain research-candidate")

    print(f"Snakey Linux target registry: OK ({len(targets)} targets)")
    for target in targets:
        print(f"  {target['id']}: {target['name']} [{target['status']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
