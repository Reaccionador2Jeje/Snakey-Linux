# Snakey Desktop 8 — NES adapter

This is a native 6502 application for the NES PPU and controller. It is not
Linux, XFCE, a browser engine, or a host-side simulation.

## Applications

- **Files**: ROM-bundled read-only catalog (README, configuration, license).
- **Console**: fixed HELP, ABOUT and CLEAR actions; no arbitrary shell.
- **Settings**: changes the real PPU background palette.
- **About**: identifies the NES homebrew edition and target.

Up/Down changes selection, A confirms, and B returns to the launcher. Every page shares the Snakey title strip and an `A OPEN / B BACK` footer. The Settings page switches the accent color.

## Graphics

The renderer uses native 8x8 CHR tiles, nametable drawing and a four-colour
background palette. The character set is stored as contiguous tile IDs so text labels map to their intended glyphs; tiles 26–29 are reserved for the emblem. The launcher includes a 16x16 multi-colour Snakey emblem;
its tile pixels use both NES bitplanes and the palette includes cyan, orange
and white accents over a dark background. The palette toggle changes those
colours rather than switching to a monochrome-only text display.

If RetroArch still shows grayscale, check that the selected NES core has not
enabled its grayscale/monochrome video option and that the ROM is loaded with
its iNES header intact. This code change still requires interactive testing
in RetroArch; a successful build alone does not prove the displayed result.

## Build

```sh
ca65 desktop/nes/main.s -o /tmp/snakey-nes.o
ld65 -C desktop/nes/nes.cfg -o /tmp/snakey-desktop.nes /tmp/snakey-nes.o
```

Expected output: 40,976-byte iNES NROM-256 image (16-byte header, 32 KiB PRG,
8 KiB CHR).
