#!/usr/bin/env python3
"""Validate per-console Snakey desktop package contracts."""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"linux/rootfs/desktop-profiles.json"
EXPECTED={"psp","ps-vita","ps3","ps4","ps5","xbox-original","wii","wii-u","switch","switch-2"}
def fail(message):
    print(f"ERROR: {message}",file=sys.stderr)
    raise SystemExit(1)
def main():
    try:
        data=json.loads(PATH.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        fail(f"cannot read desktop profiles: {exc}")
    if data.get("schema_version") != 1:
        fail("unsupported desktop profile schema")
    groups=data.get("xfce4_package_groups",{})
    required={"desktop","x11","fonts"}
    if set(groups) != required:
        fail("XFCE4 package groups must be desktop, x11 and fonts")
    for name, packages in groups.items():
        if not isinstance(packages,list) or not packages or len(packages)!=len(set(packages)):
            fail(f"{name}: package list must be non-empty and unique")
        if any(not isinstance(p,str) or not p or "/" in p or p.startswith("-") for p in packages):
            fail(f"{name}: invalid package name")
    targets=data.get("targets")
    if not isinstance(targets,list):
        fail("targets must be an array")
    by_id={t.get("id"):t for t in targets if isinstance(t,dict)}
    if set(by_id)!=EXPECTED:
        fail(f"target set mismatch: {sorted(set(by_id))}")
    psp=by_id["psp"]
    if psp.get("desktop")!="snakey-native-micro" or psp.get("xfce4")!="excluded" or psp.get("package_groups"):
        fail("PSP must use native micro desktop and exclude XFCE4")
    for tid,t in by_id.items():
        if tid!="psp":
            if t.get("desktop")!="xfce4":
                fail(f"{tid}: XFCE4 must be the desktop target")
            if set(t.get("package_groups",[]))!=required:
                fail(f"{tid}: incomplete XFCE4 package groups")
        if t.get("build_status") not in {"not-started","package-audit-required","packages-verified","built","runtime-tested"}:
            fail(f"{tid}: invalid build_status")
        if not isinstance(t.get("reason"),str) or not t["reason"].strip():
            fail(f"{tid}: missing rationale")
    runtime=data.get("runtime_contract",{})
    if runtime.get("session")!="xfce4-session" or runtime.get("fallback") is None:
        fail("missing XFCE session/fallback contract")
    print(f"Snakey desktop profiles: OK ({len(by_id)} targets; {len(groups)} XFCE4 package groups)")
    print("PSP native micro desktop exception: OK; XFCE4 package contract: OK")
if __name__=="__main__":
    raise SystemExit(main())
