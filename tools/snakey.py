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
MANIFEST = "snakey.project.json"


def load_targets() -> dict[str, dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data["targets"]}


def project_manifest(path: Path) -> dict:
    manifest_path = path / MANIFEST
    if not manifest_path.is_file():
        raise ValueError(f"{manifest_path} not found; run 'snakey new' first")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported project manifest schema")
    if data.get("target") not in load_targets():
        raise ValueError(f"unknown target: {data.get('target')}")
    return data


def command_new(args: argparse.Namespace) -> int:
    targets = load_targets()
    if args.target not in targets:
        print(f"Unknown target '{args.target}'. Use 'snakey targets'.", file=sys.stderr)
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
    manifest = {
        "schema_version": 1,
        "name": name,
        "target": args.target,
        "version": "0.1.0",
        "entry": "src/main.asm" if args.target in {"game-boy", "game-boy-color"} else "src/main.c",
    }
    (destination / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if args.target in {"game-boy", "game-boy-color"}:
        source = """; Snakey Game Boy starter (RGBDS)
; Build with: snakey build
SECTION "Entry", ROM0[$100]
    nop
    jp Entry
    ds $150 - @, 0

SECTION "Main", ROM0
Entry:
    di
    ld sp, $FFFE
    xor a
    ldh [$40], a       ; LCD off during initialization
MainLoop:
    halt
    jr MainLoop
"""
        (destination / "src/main.asm").write_text(source, encoding="utf-8")
    else:
        (destination / "src/main.c").write_text(
            "/* Snakey homebrew starter. Add the target SDK headers/toolchain. */\n"
            "int main(void) { for (;;) { } }\n", encoding="utf-8")
    print(f"Created {destination}")
    print(f"Target: {targets[args.target]['name']}")
    print("Next: cd into the project and run 'snakey validate' or 'snakey build'.")
    return 0


def command_targets(_: argparse.Namespace) -> int:
    for target in load_targets().values():
        print(f"{target['id']:<20} {target['name']:<42} {target['status']}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
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


def command_doctor(_: argparse.Namespace) -> int:
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
    print("\nOnly the Game Boy RGBDS build adapter is currently implemented.")
    return 0


def command_build(args: argparse.Namespace) -> int:
    path = args.directory.resolve()
    try:
        data = project_manifest(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if data["target"] not in {"game-boy", "game-boy-color"}:
        print(f"Build adapter not implemented for target '{data['target']}'. "
              "Project scaffolding and validation are available.", file=sys.stderr)
        return 3
    tools = [shutil.which(name) for name in ("rgbasm", "rgblink", "rgbfix")]
    if not all(tools):
        print("RGBDS is required. Install RGBDS and ensure rgbasm, rgblink and rgbfix are on PATH.",
              file=sys.stderr)
        return 4
    source = path / data["entry"]
    if not source.is_file():
        print(f"Missing source file: {source}", file=sys.stderr)
        return 1
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


def main() -> int:
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
    doctor = sub.add_parser("doctor", help="inspect available development tools")
    doctor.set_defaults(func=command_doctor)
    build = sub.add_parser("build", help="build a supported project")
    build.add_argument("directory", nargs="?", type=Path, default=Path("."))
    build.set_defaults(func=command_build)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
