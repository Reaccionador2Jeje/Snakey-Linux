# Snakey Desktop — Retro Edition Family

Snakey Desktop is a shared family of native homebrew interfaces for the retro platforms supported by this repository. **It is not a Linux distribution and does not run XFCE4 on these consoles.** The Linux-capable Snakey distribution remains a separate product.

## Product model

All editions share a recognizable interaction model and application concepts, while each platform has its own renderer, input adapter, memory budget and build target.

Shared concepts:
- Snakey home screen and application launcher.
- One active app/page at a time on constrained systems; richer dual-screen layouts where supported.
- Files: read-only catalog of content bundled in the ROM, unless a target-specific writable save mechanism is later implemented.
- Terminal: a small built-in command interpreter, never represented as a Unix shell.
- Settings: controls only for features actually implemented on that platform.
- About/system information and controller help.

The shared design is a specification and reusable data model, not a promise that one binary runs on every console.

## Platform editions

| Edition | ROM target | Interface direction | Initial constraints |
| --- | --- | --- | --- |
| Snakey Desktop 8 NES | `.nes` | Tile-based launcher and page UI | NROM baseline, 2 KiB internal RAM, controller input |
| Snakey Desktop 8 SNES | `.sfc` | More elaborate tile/panel desktop | LoROM baseline; verify actual PPU, VRAM and controller implementation |
| Snakey Desktop Pocket | `.gb` | Monochrome compact launcher | DMG palette, small tile map and limited RAM |
| Snakey Desktop Color | `.gbc` | Color compact launcher | CGB features only after CGB-aware code and emulator tests |
| Snakey Desktop Advance | `.gba` | Richer icon/menu interface | GBA display modes, buttons and bounded memory |
| Snakey Desktop Dual | `.nds` | Dual-screen interface | Touch input optional; ARM9/ARM7 startup and screen initialization must be validated |

Names are working edition names and can be adjusted without changing target IDs.

## Architecture

Keep the implementation split into:

1. **Desktop model:** app IDs, labels, navigation state and command definitions in platform-neutral metadata.
2. **Platform adapter:** input polling, screen/tile rendering, text drawing, save access and frame scheduling for each console.
3. **Applications:** small app modules using only the desktop model and platform adapter contracts.
4. **ROM packaging:** target-specific linker configuration, headers, startup code and output validation.
5. **Verification:** build checks, emulator runtime checks and separate physical-hardware evidence.

Do not add dynamic allocation or assume a framebuffer on NES/GB. Each target must explicitly declare its memory and graphics capabilities. Shared application metadata can be reused; low-level rendering code cannot be assumed portable.

## Development stages

- **Stage 1 — Common UX contract:** define app IDs, navigation, input actions, screen states and edition capability profiles.
- **Stage 2 — NES reference edition:** complete home screen, app switching, back navigation, help, About and first built-in apps. Preserve NROM-256 compatibility initially.
- **Stage 3 — GB/GBC:** implement monochrome and color-aware renderers using RGBDS.
- **Stage 4 — SNES:** implement a native LoROM renderer and input layer.
- **Stage 5 — GBA:** implement a native ARM7TDMI display/input layer and richer app tiles.
- **Stage 6 — DS:** implement dual-screen layout, touch optionality and controller navigation.
- **Stage 7 — RetroArch matrix:** run each built ROM in a named compatible core, record tested version, startup result, controls and screenshots/logs. Build success alone is not runtime certification.

## Build and test

Each edition uses its existing Snakey SDK target:

```bash
python3 tools/snakey.py new build-snakey-nes --target nes --name SnakeyDesktop8
python3 tools/snakey.py build build-snakey-nes
```

Substitute `snes`, `game-boy`, `game-boy-color`, `game-boy-advance` or `nintendo-ds` for the other editions. Current SDK adapters for some targets are still experimental startup-image generators; they are not yet full desktop implementations.

## Naming rule

Use **Snakey Desktop** as the family name and the platform edition as a suffix. Do not call these ROMs Linux, Slackware or XFCE4. XFCE4 remains the real desktop option on Snakey Linux hardware that can run Linux.
