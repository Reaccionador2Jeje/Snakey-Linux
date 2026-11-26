# Snakey Desktop 8 — NES adapter

This is the first native console implementation of the shared Snakey Desktop
application model. It is a real 6502 program: the ROM polls the NES controller,
updates application state, writes tile IDs to the PPU nametable, and changes
the PPU palette in Settings.

## Applications

- **Files**: navigable ROM-bundled catalog entries (README, configuration,
  license). Cartridge filesystem access is not claimed.
- **Console**: built-in fixed command selector (HELP, ABOUT, CLEAR). It is not
  a Unix shell and does not execute arbitrary code.
- **Settings**: changes the actual PPU background palette.
- **About**: identifies the native NES edition and hardware target.

A opens the selected item/action. B returns to the launcher. Up/Down changes
the selection. Controller input is edge-triggered to avoid repeating actions
while a button remains held.

## Build

```sh
ca65 desktop/nes/main.s -o /tmp/snakey-nes.o
ld65 -C desktop/nes/nes.cfg -o /tmp/snakey-desktop.nes /tmp/snakey-nes.o
```

Expected output: 40,976-byte iNES NROM-256 image (16-byte header, 32 KiB PRG,
8 KiB CHR). Successful assembly is not equivalent to emulator verification;
interactive testing remains required.
