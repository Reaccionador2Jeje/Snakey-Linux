# Snakey Linux 🐍

**A Slackware-derived Linux distribution for capable modern hardware, with a separate retro-console homebrew SDK.**

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

See [experimental SNES/GBA/DS ROM builders](docs/experimental-rom-builders.md) for current image formats, build commands and compatibility limitations. See docs/boot-system.md for boot prerequisites and limitations. The current physical-console compatibility status and repeatable test procedure are tracked in [docs/hardware-test-matrix.md](docs/hardware-test-matrix.md); use [the report template](docs/hardware-test-report-template.md) to record real-device results.

## Linux on modern consoles

The Linux-on-console direction now prioritizes **PlayStation 4 first**, then **PlayStation 5 and Nintendo Switch**. These use real Linux kernels and userspaces; they are not ROM-based desktop simulations. PS4 is the first engineering lane because it is x86-64 and can reuse Snakey's existing Slackware userspace work, subject to the exact console southbridge, kernel and driver support. PS5 and Switch remain separate research lanes. No universal compatibility or Snakey hardware boot is claimed. See [the modern-console Linux plan](docs/modern-console-linux.md), [PlayStation Linux research](docs/playstation-linux-research.md) and [the Linux hardware registry](platforms/linux-targets.json).

## Snakey Linux Desktop

The Linux distribution track now has its first real image profile in `linux/`. The Snakey Big Picture fullscreen controller-first launcher is available alongside XFCE.
It is pinned to **Slackware 15.0 stable** (not `current`), uses native Slackware packages and `pkgtools`/SysVinit, and targets Slackware Live Edition's stripped XFCE variant. It boots graphically
(runlevel 4), trims bloat and produces an x86_64 live ISO for Limbo/QEMU.
Build requirements and the current untested status are documented in
[linux/README.md](linux/README.md). The ISO has not yet been generated or
emulator-tested; this profile is not a claim of a working release.

## Official website and Cloudflare Worker

The complete Snakey website is in `site/`. It includes the platform catalog, boot-method guide, RetroArch testing instructions, documentation links and an automatically populated GitHub Releases section.

The Cloudflare Worker in `worker/index.js` serves the static site and exposes:
- `/api/health`
- `/api/targets`
- `/api/releases`

Local development: `npm install && npm test && npm run dev`.
Deployment instructions: [docs/website-worker.md](docs/website-worker.md). A Cloudflare account token is required to deploy; CI performs tests and a Wrangler dry-run, but does not deploy to an account. Tagged `nes-v*` releases automatically build and publish an experimental NES prerelease with the ROM and SHA-256 checksum.

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

The Linux distribution is the primary desktop product. The existing x86-64 Slackware/XFCE live profile is a generic development base, not yet a console-compatible image. PS4 is the first modern-console Linux integration target; its upstream kernel source, exact revision, southbridge compatibility and reproducible build still need to be pinned and verified. PS5 and Switch follow as independent ports. No console image is called bootable until kernel, rootfs, drivers and boot evidence are separately validated. The retro SDK remains available for genuine native homebrew, but experimental flat-color ROM previews are not treated as Snakey Desktop releases.

## License

Apache-2.0. See LICENSE.


## Snakey Desktop — Retro Edition Family

Snakey Desktop is a shared family of native homebrew interfaces for NES, SNES, Game Boy, Game Boy Color, Game Boy Advance and Nintendo DS. Each edition has a platform-specific renderer and input layer while sharing the same launcher and application concepts. These ROMs are **not Linux or XFCE4**; the real Snakey Linux desktop remains a separate Slackware system for Linux-capable hardware. See [the family specification](docs/desktop-family.md) and [the edition registry](platforms/desktop-editions.json).

## NES boot-screen milestone

The NES NROM-256 starter now initializes the PPU, draws a `SNAKEY` title and an interactive `PLAY` / `CART` / `INFO` menu. Up/Down moves the cursor, A opens a page, and B returns. The PLAY page is not yet an application runtime, and CART status is explicitly unknown until hardware-specific support exists. Visual emulator verification remains a separate next step.


See [the Linux-on-retro-hardware roadmap](docs/linux-on-retro-hardware.md) for the long-term goal of booting a real Linux kernel and, where hardware permits, XFCE4 on retro consoles. ROM homebrew and native Linux targets are deliberately kept separate.

Hardware candidates must be evaluated with the [retro Linux hardware assessment template](docs/hardware-assessment-template.md), including documented CPU/MMU, RAM, boot, storage and driver evidence.

The NES track is evolving into **Snakey Desktop 8**, a native 8-bit homebrew environment inspired by the Snakey Linux/XFCE desktop. The original NES cannot execute a Linux kernel or XFCE4; its edition uses a tile-based launcher and native applications instead. See [the NES Desktop 8 specification](docs/nes-desktop-8.md) for hardware limits, application scope, build steps and RetroArch test milestones.

## NES boot-screen milestone

The NES NROM-256 starter now initializes the PPU, draws a `SNAKEY` title and an interactive `PLAY` / `CART` / `INFO` menu. Up/Down moves the cursor, A opens a page, and B returns. The PLAY page is not yet an application runtime, and CART status is explicitly unknown until hardware-specific support exists. Visual emulator verification remains a separate next step.


See [the Linux-on-retro-hardware roadmap](docs/linux-on-retro-hardware.md) for the long-term goal of booting a real Linux kernel and, where hardware permits, XFCE4 on retro consoles. ROM homebrew and native Linux targets are deliberately kept separate.

Hardware candidates must be evaluated with the [retro Linux hardware assessment template](docs/hardware-assessment-template.md), including documented CPU/MMU, RAM, boot, storage and driver evidence.


## Ten-console Linux program

Snakey tracks ten independent Linux port lanes: PSP (MIPS), PS Vita (ARMv7), PS3 (PowerPC64), PS4 (x86-64), PS5 (x86-64), Original Xbox (i686), Wii (PowerPC32), Wii U (PowerPC32), Switch (AArch64) and Switch 2 (AArch64). Each has a separate architecture, toolchain and hardware evidence gate. See [the ten-console port program](docs/ten-console-port-program.md), [the platform matrix](platforms/linux-targets.json) and [upstream source provenance](platforms/linux-port-sources.json).

GitHub Actions validates all ten records. Only the Vita currently has a pinned upstream build workflow; PS4 is priority one but its source must be audited and pinned before CI builds it. No Snakey kernel or console boot is claimed merely because a target is registered.
