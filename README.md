# Snakey Linux 🐍

**An independent retro-console operating-system and homebrew ecosystem inspired by Slackware Linux.**

Snakey is not one universal Linux image. It is a shared ecosystem for building console-specific ROMs and, where hardware genuinely supports it, Linux-based systems.

> Classic 8/16-bit consoles do not run a conventional Slackware Linux distribution. They execute native homebrew built for their own hardware. Snakey Linux is reserved for Linux-capable devices.

## Components

- **Snakey Core** — shared project conventions and metadata.
- **Snakey SDK** — Python CLI, project scaffolding, validation and build adapters.
- **Snakey Boot System** — launch profiles for emulators, physical cartridges, SD flash cartridges and supported homebrew loaders.
- **Snakey Linux** — Slackware-derived systems for supported Linux-capable hardware.

## Initial homebrew targets

| Platform | Output | Registered launch methods |
| --- | --- | --- |
| NES | .nes | Emulator, cartridge, compatible SD flash cartridge |
| SNES | .sfc | Emulator, cartridge, compatible SD flash cartridge |
| Game Boy | .gb | Emulator, cartridge, compatible SD flash cartridge |
| Game Boy Color | .gbc | Emulator, cartridge, compatible SD flash cartridge |
| Game Boy Advance | .gba | Emulator, cartridge, compatible SD flash cartridge |
| Nintendo DS | .nds | Emulator, compatible SD flash cartridge, model-specific homebrew loader |

These are registered paths, not a claim that every cartridge, firmware version or physical console has been tested. A flash-cart SD card still requires a compatible flash cartridge; ordinary legacy consoles do not boot ROMs directly from SD.

## Boot planner

    python3 tools/snakey.py boot-plan --target game-boy
    python3 tools/snakey.py boot-plan --target nintendo-ds --method homebrew-loader

See docs/boot-system.md for prerequisites and limitations.

## Repository layout

    boot/                  Boot method registry
    docs/                  Architecture, SDK and boot documentation
    platforms/targets.json Console and boot-method registry
    tools/                 SDK and validation tools
    tests/                 Automated tests
    .github/workflows/     Continuous integration

## Validate

Requires Python 3.10 or newer.

    make validate
    make test
    python3 tools/snakey.py doctor

## Development status

The SDK currently builds Game Boy and Game Boy Color ROMs when RGBDS is installed. Boot profiles are metadata and planning tools; cartridge flashing, physical-device detection, emulator automation and Linux disk-image generation are not implemented yet.

## License

Apache-2.0. See LICENSE.
