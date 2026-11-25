# Snakey SDK

The Snakey SDK is a Python CLI for creating, validating and building target-specific homebrew projects.

## Requirements

- Python 3.10+
- cc65 (`ca65` and `ld65`) for NES NROM-256 builds
- RGBDS (`rgbasm`, `rgblink`, `rgbfix`) for Game Boy / Game Boy Color builds

## Commands

    python3 tools/snakey.py targets
    python3 tools/snakey.py doctor
    python3 tools/snakey.py new snakey-nes --target nes --name SnakeyNES
    python3 tools/snakey.py validate snakey-nes
    python3 tools/snakey.py build snakey-nes
    python3 tools/snakey.py boot-plan --target nes --method emulator-file

A built NES image is written to `snakey-nes/build/SnakeyNES.nes`.

## NES adapter: NROM-256

The NES template uses ca65 assembly and an ld65 linker configuration. It creates a standard iNES 1.0 image with mapper 0, 32 KiB PRG ROM and 8 KiB CHR ROM. The starter initializes basic CPU state and enters a stable reset loop; it is a bootable homebrew test image, not a full Snakey OS or game.

The build command checks that the image is exactly 40,976 bytes and validates the iNES magic and PRG/CHR bank counts. CI installs cc65, assembles the sample and performs the same checks.

## Game Boy adapters

Game Boy and Game Boy Color projects use RGBDS. The generated GBC starter is DMG-compatible; it does not yet use color-specific features.

## Boot planner

The `boot-plan` command reads allowed methods from `platforms/targets.json` and prerequisites from `boot/methods.json`.

- `emulator-file`: open a ROM/image in a compatible emulator; no physical cartridge.
- `cartridge-rom`: a compatible physical cartridge is required.
- `flashcart-sd`: an SD card is read by a compatible flash cartridge; the cartridge is still required.
- `homebrew-loader`: depends on exact console model and firmware.
- `linux-boot-media`: reserved for supported Linux-capable boards, not classic cartridge consoles.

The command prints a plan only. It does not detect hardware, flash cartridges, install firmware or boot a device.

## Current adapter support

| Target | Project scaffold | Build adapter |
| --- | --- | --- |
| NES | Yes | cc65, NROM-256 mapper 0 |
| Game Boy | Yes | RGBDS |
| Game Boy Color | Yes | RGBDS (DMG-compatible starter) |
| SNES, GBA, Nintendo DS | Yes | Not implemented yet |

A generated starter is a minimal template, not a complete game or a claim of physical hardware validation.
