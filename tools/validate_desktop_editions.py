#!/usr/bin/env python3
"""Validate the shared Snakey Desktop retro-edition registry."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
targets = json.loads((root / "platforms/targets.json").read_text(encoding="utf-8"))
desktop = json.loads((root / "platforms/desktop-editions.json").read_text(encoding="utf-8"))
target_map = {item["id"]: item for item in targets["targets"]}
assert desktop["schema_version"] == 1
assert desktop["family"] == "Snakey Desktop"
assert len(desktop["editions"]) == 6
seen = set()
for edition in desktop["editions"]:
    assert edition["id"] not in seen, edition["id"]
    seen.add(edition["id"])
    target = target_map[edition["target"]]
    assert edition["output"] in target["output"], edition
    assert edition["status"] in {"design", "planned", "in-development", "buildable", "emulator-tested", "hardware-tested"}
    assert edition["renderer"] and edition["input"] and edition["profile"]
    assert target["linux_capable"] is False, "Retro ROM editions must not be mislabeled Linux"
print("Snakey Desktop edition registry: OK (6 native retro targets)")
