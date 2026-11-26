#!/usr/bin/env python3
"""Validate the shared Snakey Desktop contract against its reference runtime."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
contract = json.loads((ROOT / "desktop/core/contract.json").read_text(encoding="utf-8"))
runtime = ROOT / contract["runtime_module"]
assert contract["schema_version"] == 1
assert contract["family"] == "Snakey Desktop"
assert runtime.is_file()
assert contract["navigation"]["default_screen"] == "launcher"
assert contract["navigation"]["single_active_app"] is True
apps = contract["applications"]
ids = [app["id"] for app in apps]
assert ids == ["files", "console", "settings", "about"]
assert len(ids) == len(set(ids))
assert all(app.get("actions") for app in apps)
assert contract["security"]["arbitrary_code_execution"] is False
assert contract["security"]["external_storage_writes"] is False
assert set(contract["platform_rules"]["shared"]).isdisjoint(
    contract["platform_rules"]["platform_specific"]
)
print("Snakey Desktop shared runtime contract: OK (4 applications)")
