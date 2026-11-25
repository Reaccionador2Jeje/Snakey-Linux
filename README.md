# Snakey Linux 🐍

**An independent retro-console operating-system and homebrew ecosystem inspired by Slackware Linux.**

Snakey is not a single universal Linux image. It is a shared project for building console-specific software, ROM images and (where hardware permits) Linux-based systems for retro gaming platforms.

> **Compatibility rule:** classic 8/16-bit consoles do not run a conventional Slackware Linux distribution. They receive native homebrew ROMs built for their own hardware. The Slackware-inspired Linux core is reserved for platforms that can genuinely boot and support Linux.

## Project components

- **Snakey Core** — shared project conventions, metadata and build interfaces.
- **Snakey Targets** — machine-readable definitions for each console target.
- **Snakey SDK** — planned cross-compilation toolchains and development helpers.
- **Snakey ROM Builder** — planned packaging pipeline for console-specific homebrew.
- **Snakey Emulator Lab** — planned automated validation in supported emulators.
- **Snakey Linux** — Slackware-derived system builds for Linux-capable hardware only.

## Initial homebrew targets

| Platform | Output | Execution model |
| --- | --- | --- |
| Nintendo Entertainment System (NES) | `.nes` | Native cartridge ROM / emulator |
| Super Nintendo (SNES) | `.sfc` | Native cartridge ROM / emulator |
| Game Boy | `.gb` | Native cartridge ROM / emulator |
| Game Boy Color | `.gbc` | Native cartridge ROM / emulator |
| Game Boy Advance | `.gba` | Native cartridge ROM / emulator |
| Nintendo DS | `.nds` | Native homebrew image / emulator |

These are initial build targets, not a claim that every target is already supported by a working compiler or tested on physical hardware. See [the target registry](platforms/targets.json) for status and technical metadata.

## Repository layout

```text
docs/                  Architecture and project documentation
platforms/targets.json Console target registry
tools/                 Repository validation tools
.github/workflows/     Continuous integration
```

## Validate the project

Requires Python 3.10 or newer.

```sh
python3 tools/validate_targets.py
```

Or:

```sh
make validate
```

## Development status

Snakey is in its foundational stage. Target definitions and repository validation come first; toolchains, ROM generation, emulator automation and Linux-capable device ports will be added incrementally and tested per platform.

## License

Apache-2.0. See [LICENSE](LICENSE).
