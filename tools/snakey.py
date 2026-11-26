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
    entry = ("src/main.asm" if args.target in {"game-boy", "game-boy-color"}
             else "src/main.s" if args.target == "nes"
             else "src/rom.json" if args.target in {"snes", "game-boy-advance", "nintendo-ds"}
             else "src/main.c")
    manifest = {"schema_version": 1, "name": name, "target": args.target,
                "version": "0.1.0", "entry": entry}
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
    ld [$FF40], a
MainLoop:
    halt
    jr MainLoop
"""
        (destination / "src/main.asm").write_text(source, encoding="utf-8")
    elif args.target == "nes":
        (destination / "cfg").mkdir(exist_ok=True)
        source = """; Snakey NES NROM-256 interactive menu and page navigation (ca65)
.segment "HEADER"
.byte "NES", $1A
.byte 2, 1
.byte $00, $00
.res 8, $00

.segment "CODE"
Reset:
    sei
    cld
    ldx #$40
    stx $4017
    ldx #$FF
    txs
    inx
    stx $2000
    stx $2001
    stx $4010
@vblank1:
    bit $2002
    bpl @vblank1
@vblank2:
    bit $2002
    bpl @vblank2
    lda #$00
    sta $00
    sta $01
    sta $02
    sta $03
    lda #$FF
    sta $04
    jsr SetPalette
    jsr DrawMenu

MainLoop:
@wait:
    bit $2002
    bpl @wait
    jsr ReadController
    lda $04
    cmp #$FF
    bne @pageMode
    jsr HandleMenu
    lda $04
    cmp #$FF
    bne @noCursor
    jsr UpdateCursor
@noCursor:
    jmp MainLoop
@pageMode:
    ; B returns from a page to the main menu.
    lda $07
    and #$02
    beq @continue
    lda #$FF
    sta $04
    jsr DrawMenu
@continue:
    jmp MainLoop

SetPalette:
    lda #$3F
    sta $2006
    lda #$00
    sta $2006
    lda #$0F
    sta $2007
    lda #$30
    sta $2007
    lda #$21
    sta $2007
    lda #$11
    sta $2007
    rts

ReadController:
    lda #$01
    sta $4016
    lda #$00
    sta $4016
    sta $02
    ldx #$00
@read:
    lda $4016
    and #$01
    beq @next
    lda ControllerMasks,x
    ora $02
    sta $02
@next:
    inx
    cpx #$08
    bne @read
    ; Keep only newly pressed buttons in $07.
    lda $03
    eor #$FF
    and $02
    sta $07
    lda $02
    sta $03
    rts

HandleMenu:
    lda $07
    and #$10
    beq @down
    lda $00
    beq @down
    dec $00
@down:
    lda $07
    and #$20
    beq @select
    lda $00
    cmp #$02
    bcs @select
    inc $00
@select:
    ; A opens the selected page.
    lda $07
    and #$01
    beq @done
    lda $00
    sta $04
    jsr DrawPage
@done:
    rts

ClearScreen:
    lda #$00
    sta $2001
    bit $2002
    lda #$20
    sta $2006
    lda #$00
    sta $2006
    lda #$00
    ldx #$04
@page:
    ldy #$00
@clear:
    sta $2007
    iny
    bne @clear
    dex
    bne @page
    rts

DrawMenu:
    jsr ClearScreen
    ; SNAKEY title.
    lda #$21
    sta $2006
    lda #$CD
    sta $2006
    ldx #$01
@title:
    txa
    sta $2007
    inx
    cpx #$07
    bne @title
    ; PLAY.
    lda #$22
    sta $2006
    lda #$8D
    sta $2006
    lda #$07
    sta $2007
    lda #$08
    sta $2007
    lda #$03
    sta $2007
    lda #$06
    sta $2007
    ; CART.
    lda #$22
    sta $2006
    lda #$CD
    sta $2006
    lda #$09
    sta $2007
    lda #$03
    sta $2007
    lda #$0A
    sta $2007
    lda #$0B
    sta $2007
    ; INFO.
    lda #$23
    sta $2006
    lda #$0D
    sta $2006
    lda #$0C
    sta $2007
    lda #$02
    sta $2007
    lda #$0E
    sta $2007
    lda #$0D
    sta $2007
    lda #$00
    sta $2005
    sta $2005
    lda #$08
    sta $2001
    rts

DrawPage:
    jsr ClearScreen
    ; Select a four-glyph page heading through a zero-page pointer.
    ldx $04
    lda PageTextLo,x
    sta $05
    lda PageTextHi,x
    sta $06
    lda #$21
    sta $2006
    lda #$4E
    sta $2006
    ldy #$00
@heading:
    lda ($05),y
    sta $2007
    iny
    cpy #$04
    bne @heading
    ; SNAKEY footer.
    lda #$22
    sta $2006
    lda #$8D
    sta $2006
    ldx #$01
@footer:
    txa
    sta $2007
    inx
    cpx #$07
    bne @footer
    ; CART page reports status as unknown until a hardware-specific
    ; cartridge interface is implemented. Draw a question-mark tile.
    lda $04
    cmp #$01
    bne @render
    lda #$22
    sta $2006
    lda #$0E
    sta $2006
    lda #$10
    sta $2007
@render:
    lda #$00
    sta $2005
    sta $2005
    lda #$08
    sta $2001
    rts

UpdateCursor:
    ldx $01
    lda CursorHigh,x
    sta $2006
    lda CursorLow,x
    sta $2006
    lda #$00
    sta $2007
    ldx $00
    lda CursorHigh,x
    sta $2006
    lda CursorLow,x
    sta $2006
    lda #$0F
    sta $2007
    lda $00
    sta $01
    rts

ControllerMasks:
.byte $01,$02,$04,$08,$10,$20,$40,$80
CursorLow:
.byte $8A, $CA, $0A
CursorHigh:
.byte $22, $22, $23
PageTextLo:
.byte <PlayText, <CartText, <InfoText
PageTextHi:
.byte >PlayText, >CartText, >InfoText
PlayText:
.byte 7,8,3,6
CartText:
.byte 9,3,10,11
InfoText:
.byte 12,2,14,13

.segment "VECTORS"
.word Reset, Reset, Reset

.segment "CHARS"
; Tile 0 blank. Tiles 1..6 spell SNAKEY.
.res 16, $00
; S
.byte $3C,$42,$40,$3C,$02,$42,$3C,$00
.res 8, $00
; N
.byte $42,$62,$52,$4A,$46,$42,$42,$00
.res 8, $00
; A
.byte $18,$24,$42,$7E,$42,$42,$42,$00
.res 8, $00
; K
.byte $42,$44,$48,$70,$48,$44,$42,$00
.res 8, $00
; E
.byte $7E,$40,$40,$7C,$40,$40,$7E,$00
.res 8, $00
; Y
.byte $42,$42,$24,$18,$18,$18,$18,$00
.res 8, $00
; P
.byte $7C,$42,$42,$7C,$40,$40,$40,$00
.res 8, $00
; L
.byte $40,$40,$40,$40,$40,$40,$7E,$00
.res 8, $00
; C
.byte $3C,$42,$40,$40,$40,$42,$3C,$00
.res 8, $00
; R
.byte $7C,$42,$42,$7C,$48,$44,$42,$00
.res 8, $00
; T
.byte $7E,$18,$18,$18,$18,$18,$18,$00
.res 8, $00
; I
.byte $7E,$18,$18,$18,$18,$18,$7E,$00
.res 8, $00
; O
.byte $3C,$42,$42,$42,$42,$42,$3C,$00
.res 8, $00
; F
.byte $7E,$40,$40,$7C,$40,$40,$40,$00
.res 8, $00
; >
.byte $40,$20,$10,$08,$10,$20,$40,$00
.res 8, $00
; ?
.byte $3C,$42,$02,$0C,$10,$00,$10,$00
.res 8, $00
.res $2000 - (16 + 16 * 16), $00
"""
        (destination / "src/main.s").write_text(source, encoding="utf-8")
        config = """MEMORY {
    HEADER: start = $0000, size = $0010, file = %O, fill = yes;
    PRG:    start = $8000, size = $8000, file = %O, fill = yes, fillval = $EA;
    CHR:    start = $0000, size = $2000, file = %O, fill = yes, fillval = $00;
}
SEGMENTS {
    HEADER:  load = HEADER, type = ro;
    CODE:    load = PRG, type = ro;
    VECTORS: load = PRG, start = $FFFA, type = ro;
    CHARS:   load = CHR, type = ro;
}
"""
        (destination / "cfg/nes.cfg").write_text(config, encoding="utf-8")
    elif args.target in {"snes", "game-boy-advance", "nintendo-ds"}:
        descriptor = {"schema_version": 1, "target": args.target,
                      "generator": "tools/native_roms.py",
                      "status": "experimental-template",
                      "note": "The current adapter emits a minimal platform image; user CPU source compilation is a future milestone."}
        (destination / "src/rom.json").write_text(json.dumps(descriptor, indent=2) + "\n", encoding="utf-8")
    else:
        (destination / "src/main.c").write_text(
            "/* Snakey homebrew starter. Add target SDK headers/toolchain. */\\n"
            "int main(void) { for (;;) { } }\\n", encoding="utf-8")
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
    print("\nBuild adapters: NES requires cc65 (ca65/ld65); Game Boy and Game Boy Color require RGBDS. SNES/GBA/DS use experimental native image writers; emulator compatibility is not yet certified.")
    return 0


def command_build(args):
    path = args.directory.resolve()
    try:
        data = project_manifest(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if data["target"] in {"snes", "game-boy-advance", "nintendo-ds"}:
        build = path / "build"
        build.mkdir(exist_ok=True)
        extension = {"snes": ".sfc", "game-boy-advance": ".gba", "nintendo-ds": ".nds"}[data["target"]]
        rom = build / (data["name"] + extension)
        command = [sys.executable, str(ROOT / "tools" / "native_roms.py"),
                   data["target"], str(rom), "--name", data["name"]]
        print("+", " ".join(command))
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
        print(f"Experimental {data['target']} homebrew image built: {rom}")
        return 0
    if data["target"] == "nes":
        if not all(shutil.which(name) for name in ("ca65", "ld65")):
            print("cc65 is required: install ca65 and ld65 and ensure they are on PATH.", file=sys.stderr)
            return 4
        source = path / data["entry"]
        config = path / "cfg" / "nes.cfg"
        if not source.is_file() or not config.is_file():
            print("NES project is missing src/main.s or cfg/nes.cfg.", file=sys.stderr)
            return 1
        build = path / "build"
        build.mkdir(exist_ok=True)
        obj = build / "main.o"
        rom = build / (data["name"] + ".nes")
        commands = [
            ["ca65", "-o", str(obj), str(source)],
            ["ld65", "-C", str(config), "-o", str(rom), str(obj)],
        ]
        for command in commands:
            print("+", " ".join(command))
            result = subprocess.run(command, cwd=path, check=False)
            if result.returncode:
                return result.returncode
        if not rom.is_file() or rom.stat().st_size != 16 + 32768 + 8192:
            print("NES ROM has an unexpected size; expected iNES header + 32 KiB PRG + 8 KiB CHR.", file=sys.stderr)
            return 1
        with rom.open("rb") as stream:
            header = stream.read(16)
        if header[:4] != b"NES\x1a" or header[4:6] != bytes((2, 1)):
            print("Generated ROM has an invalid iNES header.", file=sys.stderr)
            return 1
        print(f"NROM-256 ROM built and header checked: {rom}")
        return 0
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
    rom = build / (data["name"] + (".gbc" if data["target"] == "game-boy-color" else ".gb"))
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
