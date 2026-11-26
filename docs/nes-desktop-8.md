# Snakey Desktop 8 — NES Edition

## Honest hardware boundary

The original Nintendo Entertainment System cannot boot Linux or XFCE4. Its Ricoh 2A03 CPU is an 8-bit 6502-family processor, it has 2 KiB of internal work RAM, and its PPU renders a 256×240 picture from tile and palette memory. It has no Linux-capable memory-management unit, no conventional disk subsystem, and no supported Linux device-driver platform.

Therefore the NES edition is **not a Linux port**. It is a native NES homebrew environment that borrows the visual and interaction concepts of Snakey Linux and XFCE4. The real Slackware/XFCE4 distribution remains for supported Linux hardware.

## Product definition

**Name:** Snakey Desktop 8  
**Target:** NES NROM-256 (mapper 0) initial baseline  
**Output:** homebrew `.nes` ROM  
**Primary test environment:** RetroArch with a compatible NES core  
**Input:** NES controller (D-pad, A, B, START, SELECT)

### Desktop metaphor adapted to NES

This is a console-native, tile-based UI, not a pixel-for-pixel desktop clone:

- Home screen with Snakey branding, status strip and selectable application tiles.
- A single active application view at a time (no overlapping desktop windows).
- Application launcher and return-to-home navigation.
- Settings and About screens.
- A virtual file catalog containing built-in demo entries; no writable filesystem is implied.
- A command-console-style screen with a small fixed command set. It is a UI command interpreter, not a Unix shell and cannot execute Linux commands.
- Optional controller help overlay.

### Initial applications

| App | NES implementation |
| --- | --- |
| Launcher | Native menu and focus cursor |
| Files | Read-only list of ROM-bundled demo entries |
| Terminal | Fixed built-in commands such as HELP, ABOUT and CLEAR |
| Settings | UI preferences that fit the selected mapper/RAM profile |
| System info | Target, mapper, controller and build metadata |

## Memory and graphics rules

- Keep the first release compatible with mapper 0 / NROM-256.
- Keep mutable state within internal RAM; avoid assuming extra cartridge RAM.
- Use the PPU's tile and attribute model; do not assume a framebuffer.
- Keep CHR data within the selected NROM layout and verify the iNES header and exact output size.
- Prefer a single screen/page at a time to limit memory and rendering complexity.
- Avoid dynamic allocation. Use fixed-size buffers and bounded input.
- Keep the ROM self-contained; no external disk, network or Linux process support is claimed.

## Milestones

1. **M0 — Existing ROM baseline:** boot, palette, title/menu and controller navigation. This is the existing starter baseline, not yet proof of a finished desktop.
2. **M1 — Desktop shell:** home screen, app launcher, focus movement, application view routing, return action and controller help.
3. **M2 — Built-in apps:** read-only Files catalog, command-console interpreter, Settings and About.
4. **M3 — Visual polish:** custom tile set, consistent panels, icons, status strip and transition effects within NES limits.
5. **M4 — RetroArch verification:** run the ROM in a real NES core, inspect screenshots and test every controller path. Only then mark it emulator-tested.
6. **M5 — Physical hardware:** separately assess a compatible flash cartridge and real console. Do not claim physical compatibility based only on emulator success.

## Build and test

From the repository root:

```bash
python3 tools/snakey.py new build-snakey-nes --target nes --name SnakeyDesktop8
python3 tools/snakey.py validate build-snakey-nes
python3 tools/snakey.py build build-snakey-nes
```

The build needs the NES assembler/linker toolchain already used by the repository (cc65/ca65/ld65). Open the generated `.nes` in RetroArch with a NES core. The current CI structural smoke test checks the NROM-256 output; it does not replace interactive emulator testing.

## Naming and compatibility

Use “Snakey Desktop 8 for NES” or “NES edition” in UI and release notes. Do not label the ROM as Slackware, Linux, XFCE4, a kernel, or a Linux distribution. Those names describe inspiration, not the executable architecture.
