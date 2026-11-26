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

## Official website and Cloudflare Worker

The complete Snakey website is in `site/`. It includes the platform catalog, boot-method guide, RetroArch testing instructions, documentation links and an automatically populated GitHub Releases section.

The Cloudflare Worker in `worker/index.js` serves the static site and exposes:
- `/api/health`
- `/api/targets`
- `/api/releases`

Local development: `npm install && npm test && npm run dev`.
Deployment instructions: [docs/website-worker.md](docs/website-worker.md). A Cloudflare account token is required to deploy; CI performs tests and a Wrangler dry-run, but does not deploy to an account.

## Repository layout

    site/                  Official website assets\n    worker/                Cloudflare Worker and read-only API\n    boot/                  Boot method registry
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

The SDK builds an NES NROM-256 (.nes) image with cc65 and Game Boy / Game Boy Color ROMs with RGBDS. The NES starter has an interactive controller-driven menu: Up/Down selects PLAY, CART or INFO; A opens the corresponding page; B returns. Cartridge hardware status remains unknown without a target-specific detection interface. CI assembles the ROM and checks the iNES header and expected 40 KiB file size. Cartridge flashing, physical-device detection, emulator automation and Linux disk-image generation are not implemented yet.

## License

Apache-2.0. See LICENSE.


## NES boot-screen milestone

The NES NROM-256 starter now initializes the PPU, draws a `SNAKEY` title and an interactive `PLAY` / `CART` / `INFO` menu. Up/Down moves the cursor, A opens a page, and B returns. The PLAY page is not yet an application runtime, and CART status is explicitly unknown until hardware-specific support exists. Visual emulator verification remains a separate next step.
