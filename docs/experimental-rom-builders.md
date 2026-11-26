# Experimental SNES, GBA and DS ROM builders

The SDK generates a first native image for each registered target. These are
early bring-up programs, not finished Snakey desktop ports.

## Build

```bash
python3 tools/snakey.py new build-snes --target snes --name Snakey
python3 tools/snakey.py validate build-snes
python3 tools/snakey.py build build-snes

python3 tools/snakey.py new build-gba --target game-boy-advance --name Snakey
python3 tools/snakey.py build build-gba

python3 tools/snakey.py new build-ds --target nintendo-ds --name Snakey
python3 tools/snakey.py build build-ds
```

Artifacts are written to each project's `build/` directory as `.sfc`,
`.gba`, and `.nds`. The builders use Python's standard library.

## Current implementation status

- **SNES:** 32 KiB LoROM image, internal header, reset vector and checksum pair.
  The 65816 reset program sets a cyan CGRAM backdrop and idles. It does not
  draw tiles, a menu, or a game yet.
- **GBA:** 32 KiB image, entry branch and cartridge header/checksum. ARM code
  selects bitmap Mode 3 and writes a changing RGB555 colour-ramp diagnostic
  across the 240×160 framebuffer. This is a graphics bring-up test, not the
  Snakey desktop interface. The Nintendo logo area remains blank, so retail
  BIOS-enforced boot compatibility is not claimed.
- **Nintendo DS:** 64 KiB image with ARM9/ARM7 load metadata and header CRCs.
  ARM9 maps VRAM bank A to main-engine BG memory, selects bitmap Mode 5 and
  writes an RGB555 colour-ramp diagnostic to the 256×192 main screen. ARM7
  remains an idle stub; the second screen, touch input, audio and UI are not
  implemented. Retail logo/firmware and flashcart compatibility are not claimed.

A successful CI build validates source generation, image sizes, selected
instructions and metadata. It does **not** prove that a ROM boots or displays
correctly in RetroArch. Test each artifact with an appropriate core and report
the core name plus a screenshot if the output is still blank or incorrect.
The next milestone is a real SNES tile-based UI, followed by controller-driven
GBA/DS interfaces and proper dual-screen DS support.
