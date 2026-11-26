#!/usr/bin/env python3
"""Validate the ten-platform Snakey Linux console matrix and source evidence."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"platforms/linux-targets.json"
SOURCES=ROOT/"platforms/linux-port-sources.json"
EXPECTED={"psp","ps-vita","ps3","ps4","ps5","xbox-original","wii","wii-u","switch","switch-2"}
ARCH={"psp":"mipsel","ps-vita":"armv7","ps3":"powerpc64-big-endian","ps4":"x86_64","ps5":"x86_64","xbox-original":"i686","wii":"powerpc32-big-endian","wii-u":"powerpc32-big-endian","switch":"aarch64","switch-2":"aarch64"}
HEX40=re.compile(r"^[0-9a-f]{40}$")
def load(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: fail(f"cannot read {path.name}: {exc}")
def fail(message):
    print(f"ERROR: {message}",file=sys.stderr); raise SystemExit(1)
def main():
    data=load(REGISTRY)
    if data.get("schema_version")!=2: fail("linux-targets schema_version must be 2")
    targets=data.get("targets")
    if not isinstance(targets,list): fail("targets must be an array")
    by_id={}
    for i,t in enumerate(targets):
        if not isinstance(t,dict): fail(f"targets[{i}] must be an object")
        for key in ("id","name","family","architecture","cpu","system_ram_mb","status","priority","snakey_kernel_built","snakey_hardware_tested","toolchain_strategy","desktop_goal","notes"):
            if key not in t: fail(f"targets[{i}] missing {key}")
        tid=t["id"]
        if tid in by_id: fail(f"duplicate target id: {tid}")
        by_id[tid]=t
        if t["family"]!="linux-console": fail(f"{tid}: family must be linux-console")
        if t["architecture"]!=ARCH.get(tid): fail(f"{tid}: incorrect architecture mapping")
        if type(t["system_ram_mb"]) is not int or t["system_ram_mb"]<=0: fail(f"{tid}: system_ram_mb must be positive integer")
        if t["status"] not in {"source-audit-required","source-pinned","kernel-buildable","kernel-built","kernel-boots","userspace-boots","desktop-tested","hardware-verified"}: fail(f"{tid}: unsupported status")
        if t["snakey_hardware_tested"] and t["status"]!="hardware-verified": fail(f"{tid}: hardware test/status mismatch")
        if t["snakey_kernel_built"] and t["status"] not in {"kernel-built","kernel-boots","userspace-boots","desktop-tested","hardware-verified"}: fail(f"{tid}: kernel build/status mismatch")
    if set(by_id)!=EXPECTED: fail(f"platform set mismatch; missing={sorted(EXPECTED-set(by_id))}, extra={sorted(set(by_id)-EXPECTED)}")
    sources=load(SOURCES)
    if sources.get("schema_version")!=2: fail("linux-port-sources schema_version must be 2")
    seen=set()
    for i,s in enumerate(sources.get("sources",[])):
        sid=s.get("id")
        if not isinstance(sid,str) or not sid or sid in seen: fail(f"sources[{i}]: id must be unique")
        seen.add(sid)
        if s.get("target") not in EXPECTED: fail(f"{sid}: unknown target")
        if s.get("architecture")!=ARCH[s["target"]]: fail(f"{sid}: architecture does not match target")
        if not isinstance(s.get("project_url"),str) or not s["project_url"].startswith("https://"): fail(f"{sid}: project_url must be HTTPS")
        repo=s.get("source_repository")
        if repo is not None and (not isinstance(repo,str) or not repo.startswith("https://")): fail(f"{sid}: source_repository must be HTTPS or null")
        if s.get("build_status")=="pinned-upstream-build":
            if not HEX40.fullmatch(s.get("revision","")): fail(f"{sid}: pinned build requires full commit SHA")
            if not s.get("build_workflow"): fail(f"{sid}: pinned build requires workflow")
        elif s.get("build_status")=="source-audit-required":
            if s.get("revision") is not None: fail(f"{sid}: unaudited source cannot have revision pin")
        else: fail(f"{sid}: unsupported build_status")
    print(f"Snakey console matrix: OK ({len(by_id)} platforms; {len(sources.get('sources',[]))} source records)")
    for tid in sorted(by_id): print(f"  {tid:16} {by_id[tid]['architecture']:24} {by_id[tid]['status']}")
    print("Source provenance: OK; unverified upstreams remain explicitly unpinned.")
    return 0
if __name__=="__main__": raise SystemExit(main())
