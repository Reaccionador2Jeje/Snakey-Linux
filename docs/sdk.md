# Snakey SDK

The Snakey SDK is a dependency-free Python CLI. It lists targets, scaffolds projects, validates manifests, checks installed toolchains, builds Game Boy / Game Boy Color ROMs with RGBDS, and displays registered launch paths.

## Requirements

- Python 3.10+
- RGBDS for Game Boy and Game Boy Color ROM builds

## Commands

    python3 tools/snakey.py targets
    python3 tools/snakey.py doctor
    python3 tools/snakey.py boot-plan --target game-boy
    python3 tools/snakey.py boot-plan --target nintendo-ds --method homebrew-loader
    python3 tools/snakey.py new hello-gb --target game-boy --name HelloGB
    cd hello-gb
    python3 ../tools/snakey.py validate
    python3 ../tools/snakey.py build

The build command uses rgbasm, rgblink and rgbfix and writes the ROM to build/. It does not download toolchains or execute arbitrary project scripts.

## Boot planner

The boot-plan command reads allowed methods from platforms/targets.json and their prerequisites from boot/methods.json. It rejects combinations not registered for a target.

- emulator-file: open a ROM/image in a compatible emulator; no physical cartridge.
- cartridge-rom: a compatible physical cartridge is required.
- flashcart-sd: an SD card is read by a compatible flash cartridge; the cartridge is still required.
- homebrew-loader: depends on exact console model and firmware.
- linux-boot-media: reserved for supported Linux-capable boards, not classic cartridge consoles.

The command prints a plan only. It does not detect hardware, flash cartridges, install firmware or boot a device.

## Project manifest

Each project contains snakey.project.json with schema version, name, target, version and entry source. Target IDs must exist in platforms/targets.json.

## Current adapter support

| Target | Project scaffold | Build adapter |
| --- | --- | --- |
| Game Boy | Yes | RGBDS |
| Game Boy Color | Yes | RGBDS (DMG-compatible starter) |
| NES, SNES, GBA, Nintendo DS | Yes | Not implemented yet |

A generated starter is a minimal template, not a complete game or a claim of hardware validation.
