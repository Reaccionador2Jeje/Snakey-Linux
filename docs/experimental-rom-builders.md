# Experimental SNES, GBA and DS ROM builders

The SDK now generates a first image for every registered console target.

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
`.gba`, and `.nds`. The build uses Python's standard library and is wired
into GitHub Actions.

## What is implemented

- **SNES:** 32 KiB LoROM image, internal header, reset vector and checksum pair.
  Current CPU program initializes the display backdrop and then idles; no menu or game logic yet.
- **GBA:** 32 KiB image, entry branch, cartridge header and complement checksum.
  Startup code selects bitmap Mode 3 and fills the framebuffer with a solid
  color. The Nintendo logo area is intentionally blank, so this is not
  certified for BIOS-enforced retail boot paths.
- **Nintendo DS:** 64 KiB image, ARM9/ARM7 load offsets, header CRCs and minimal
  CPU stubs. It does not yet initialize either screen; logo/firmware and
  flashcart compatibility are not certified.

These are experimental image-generation milestones, not complete games or
operating systems. A successful CI build validates file structure and metadata,
not actual execution. Test the artifacts in an emulator before attempting any
physical hardware. The next native-development milestone is to replace the
SNES and DS idle stubs with visible controller-driven menus and to move all
three experimental targets toward real source-compiling SDK adapters.
