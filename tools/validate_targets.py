#!/usr/bin/env python3
"""Validate Snakey's machine-readable console target registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "platforms" / "targets.json"
BOOT_REGISTRY = ROOT / "boot" / "methods.json"
ALLOWED_FAMILIES = {"native-homebrew", "linux-system"}
ALLOWED_STATUSES = {
    "planned", "toolchain-ready", "buildable",
    "emulator-tested", "hardware-tested", "experimental-buildable",
}
ALLOWED_EXECUTION = {
    "cartridge-rom", "emulator", "homebrew-image", "linux-boot",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read target registry: {exc}")

    if data.get("schema_version") != 1:
        fail("schema_version must be 1")
    targets = data.get("targets")
    if not isinstance(targets, list) or not targets:
        fail("targets must be a non-empty array")

    try:
        boot_data = json.loads(BOOT_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read boot method registry: {exc}")
    boot_methods = boot_data.get("methods")
    if not isinstance(boot_methods, list) or not boot_methods:
        fail("boot registry methods must be a non-empty array")
    boot_ids = {item.get("id") for item in boot_methods if isinstance(item, dict)}
    if len(boot_ids) != len(boot_methods) or None in boot_ids:
        fail("boot method IDs must be unique and non-empty")

    seen: set[str] = set()
    for index, target in enumerate(targets):
        prefix = f"targets[{index}]"
        if not isinstance(target, dict):
            fail(f"{prefix} must be an object")
        for field in ("id", "name", "family", "cpu", "output", "execution", "linux_capable", "status"):
            if field not in target:
                fail(f"{prefix} is missing {field}")
        target_id = target["id"]
        if not isinstance(target_id, str) or not target_id or target_id in seen:
            fail(f"{prefix}.id must be a unique non-empty string")
        seen.add(target_id)
        if target["family"] not in ALLOWED_FAMILIES:
            fail(f"{prefix}.family is unsupported")
        if target["status"] not in ALLOWED_STATUSES:
            fail(f"{prefix}.status is unsupported")
        if not isinstance(target["linux_capable"], bool):
            fail(f"{prefix}.linux_capable must be boolean")
        if not isinstance(target["output"], list) or not target["output"]:
            fail(f"{prefix}.output must be a non-empty array")
        if not all(isinstance(ext, str) and ext.startswith(".") for ext in target["output"]):
            fail(f"{prefix}.output entries must be extensions beginning with a dot")
        if not isinstance(target["execution"], list) or not target["execution"]:
            fail(f"{prefix}.execution must be a non-empty array")
        if not set(target["execution"]).issubset(ALLOWED_EXECUTION):
            fail(f"{prefix}.execution contains an unsupported value")
        if not isinstance(target.get("boot_methods"), list) or not target["boot_methods"]:
            fail(f"{prefix}.boot_methods must be a non-empty array")
        unknown_methods = set(target["boot_methods"]) - boot_ids
        if unknown_methods:
            fail(f"{prefix}.boot_methods contains unknown methods: {sorted(unknown_methods)}")
        if target["family"] == "native-homebrew" and "linux-boot-media" in target["boot_methods"]:
            fail(f"{prefix}: native-homebrew targets cannot use Linux boot media")
        if target["family"] == "native-homebrew" and target["linux_capable"]:
            fail(f"{prefix}: native-homebrew targets cannot be marked Linux-capable")
        if target["family"] == "linux-system" and not target["linux_capable"]:
            fail(f"{prefix}: linux-system targets must be Linux-capable")

    print(f"Snakey target registry: OK ({len(targets)} targets)")
    for target in targets:
        print(f"  {target['id']}: {target['name']} [{target['status']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
