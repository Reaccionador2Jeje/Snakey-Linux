#!/usr/bin/env python3
"""Snakey SDK command-line interface (Python standard library only)."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "platforms" / "targets.json"
BOOT_REGISTRY = ROOT / "boot" / "methods.json"
MANIFEST = "snakey.project.json"


def load_targets():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data["targets"]}


def load_boot_methods():
    data = json.loads(BOOT_REGISTRY.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data["methods"]}


def project_manifest(path):
    manifest_path = path / MANIFEST
    if not manifest_path.is_file():
        raise ValueError(f"{manifest_path} not found; run snakey new first")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported project manifest schema")
    if data.get("target") not in load_targets():
        raise ValueError(f"unknown target: {data.get('target')}")
    return data


def command_new(args):
    targets = load_targets()
    if args.target not in targets:
        print(f"Unknown target '{args.target}'. Use snakey targets.", file=sys.stderr)
        return 2
    name = args.name or args.directory.name
    if not name or not name.replace("-", "").replace("_", "").isalnum():
        print("Project name must contain only letters, numbers, '-' or '_'.", file=sys.stderr)
        return 2
    destination = args.directory.resolve()
    if destination.exists() and any(destination.iterdir()):
        print(f"Refusing to overwrite non-empty directory: {destination}", file=sys.stderr)
        return 2
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "src").mkdir(exist_ok=True)
    manifest = {"schema_version": 1, "name": name, "target": args.target,
                "version": "0.1.0",
                "entry": "src/main.asm" if args.target in {"game-boy", "game-boy-color"} else "src/main.c"}
    (destination / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if args.target in {"game-boy", "game-boy-color"}:
        source = """; Snakey Game Boy starter (RGBDS)
SECTION "Entry", ROM0[$100]
    nop
    jp Entry
    ds $150 - @, 0
SECTION "Main", ROM0
Entry:
    di
    ld sp, $FFFE
    xor a
    ldh [$40], a
MainLoop:
    halt
    jr MainLoop
"""
        (destination / "src/main.asm").write_text(source, encoding="utf-8")
    else:
        (destination / "src/main.c").write_text(
            "/* Snakey homebrew starter. Add target SDK headers/toolchain. */\n"
            "int main(void) { for (;;) { } }\n", encoding="utf-8")
    print(f"Created {destination}")
    print(f"Target: {targets[args.target]['name']}")
    return 0


def command_targets(_):
    for target in load_targets().values():
        print(f"{target['id']:<20} {target['name']:<42} {target['status']}")
    return 0


def command_validate(args):
    path = args.directory.resolve()
    try:
        data = project_manifest(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    entry = path / data.get("entry", "")
    if not entry.is_file():
        print(f"ERROR: entry source does not exist: {entry}", file=sys.stderr)
        return 1
    print(f"Project OK: {data['name']} ({data['target']})")
    print(f"Entry: {data['entry']}")
    return 0


def command_boot_plan(args):
    target = load_targets().get(args.target)
    methods = load_boot_methods()
    if target is None:
        print(f"Unknown target: {args.target}", file=sys.stderr)
        return 2
    allowed = target.get("boot_methods", [])
    if not allowed:
        print(f"No boot methods registered for {args.target}.", file=sys.stderr)
        return 2
    if args.method and args.method not in allowed:
        print(f"Method '{args.method}' is not registered for {args.target}.", file=sys.stderr)
        print("Available: " + ", ".join(allowed), file=sys.stderr)
        return 2
    for method_id in ([args.method] if args.method else allowed):
        method = methods.get(method_id)
        if method is None:
            print(f"Unknown method in boot registry: {method_id}", file=sys.stderr)
            return 1
        print(f"\n{method['name']} [{method_id}]")
        print("Cartridge required: " + ("yes" if method["cartridge_required"] else "no"))
        for requirement in method["requires"]:
            print(" - " + requirement)
        print(method["description"])
    print("\nPlan only; physical hardware compatibility is not implied.")
    return 0


def command_doctor(_):
    checks = {
        "Python 3": shutil.which("python3"),
        "RGBDS assembler (rgbasm)": shutil.which("rgbasm"),
        "RGBDS linker (rgblink)": shutil.which("rgblink"),
        "RGBDS fixer (rgbfix)": shutil.which("rgbfix"),
        "NES assembler (ca65)": shutil.which("ca65"),
        "NES linker (ld65)": shutil.which("ld65"),
        "ARM cross compiler": shutil.which("arm-none-eabi-gcc"),
    }
    for label, executable in checks.items():
        print(f"{'FOUND' if executable else 'MISSING':<8} {label}" +
              (f" — {executable}" if executable else ""))
    print("\nBoot planner available. Game Boy build adapter requires RGBDS.")
    return 0


def command_build(args):
    path = args.directory.resolve()
    try:
        data = project_manifest(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if data["target"] not in {"game-boy", "game-boy-color"}:
        print(f"Build adapter not implemented for target '{data['target']}'.", file=sys.stderr)
        return 3
    if not all(shutil.which(name) for name in ("rgbasm", "rgblink", "rgbfix")):
        print("RGBDS is required: rgbasm, rgblink and rgbfix must be on PATH.", file=sys.stderr)
        return 4
    source = path / data["entry"]
    build = path / "build"
    build.mkdir(exist_ok=True)
    obj = build / "main.o"
    rom = build / (data["name"] + ".gb")
    commands = [
        ["rgbasm", "-o", str(obj), str(source)],
        ["rgblink", "-o", str(rom), str(obj)],
        ["rgbfix", "-v", "-p", "0xFF", str(rom)],
    ]
    for command in commands:
        print("+", " ".join(command))
        result = subprocess.run(command, cwd=path, check=False)
        if result.returncode:
            return result.returncode
    print(f"ROM built: {rom}")
    return 0


def main():
    parser = argparse.ArgumentParser(prog="snakey", description="Snakey retro-console SDK")
    sub = parser.add_subparsers(dest="command", required=True)
    targets = sub.add_parser("targets", help="list registered console targets")
    targets.set_defaults(func=command_targets)
    new = sub.add_parser("new", help="create a homebrew project")
    new.add_argument("directory", type=Path)
    new.add_argument("--target", required=True, choices=sorted(load_targets()))
    new.add_argument("--name")
    new.set_defaults(func=command_new)
    validate = sub.add_parser("validate", help="validate a project")
    validate.add_argument("directory", nargs="?", type=Path, default=Path("."))
    validate.set_defaults(func=command_validate)
    plan = sub.add_parser("boot-plan", help="show launch methods for a console")
    plan.add_argument("--target", required=True, choices=sorted(load_targets()))
    plan.add_argument("--method", choices=sorted(load_boot_methods()))
    plan.set_defaults(func=command_boot_plan)
    doctor = sub.add_parser("doctor", help="inspect installed toolchains")
    doctor.set_defaults(func=command_doctor)
    build = sub.add_parser("build", help="build a supported project")
    build.add_argument("directory", nargs="?", type=Path, default=Path("."))
    build.set_defaults(func=command_build)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
