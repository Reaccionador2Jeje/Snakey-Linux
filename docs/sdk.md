# Snakey SDK

The first SDK milestone is a dependency-free Python CLI. It can list targets, scaffold projects, validate project manifests, inspect installed toolchains and build Game Boy / Game Boy Color ROMs when RGBDS is installed.

## Requirements

- Python 3.10+
- RGBDS for Game Boy and Game Boy Color ROM builds

## Run from a checkout

```sh
python3 tools/snakey.py targets
python3 tools/snakey.py doctor
python3 tools/snakey.py new hello-gb --target game-boy --name HelloGB
cd hello-gb
python3 ../tools/snakey.py validate
python3 ../tools/snakey.py build
```

The build command uses RGBDS tools (`rgbasm`, `rgblink`, `rgbfix`) and writes the ROM to `build/`. It does not download toolchains or execute arbitrary project scripts.

## Project manifest

Each project contains `snakey.project.json` with schema version, name, target, version and entry source. Target IDs must exist in `platforms/targets.json`.

## Current adapter support

| Target | Project scaffold | Build adapter |
| --- | --- | --- |
| Game Boy | Yes | RGBDS |
| Game Boy Color | Yes | RGBDS (DMG-compatible starter) |
| NES, SNES, GBA, Nintendo DS | Yes | Not implemented yet |

A generated starter is a minimal template, not a complete game or a claim of hardware validation. The Game Boy Color starter currently uses a DMG-compatible code path; GBC-specific features will be added separately.
