# Snakey Architecture

## 1. Product model

Snakey is a multi-target retro development ecosystem, not one kernel image that can boot every console. The repository shares metadata, build conventions, validation and documentation while each target supplies its own toolchain and output format.

There are two distinct execution families:

1. **Native console homebrew:** programs compiled for a console's CPU, memory map, graphics/audio hardware and boot format. Outputs are ROM or homebrew images. These targets do not run Slackware.
2. **Linux-capable hardware:** devices with a supported boot chain, MMU, sufficient memory and kernel drivers. These may receive a Snakey Linux system derived from Slackware.

A target must never be labelled Linux-capable merely because an emulator can run Linux on a different host.

## 2. Layers

- **Project metadata:** target IDs, output extensions, architecture and support status.
- **SDK/toolchains:** compiler, assembler, linker, SDK headers and reproducible build settings per target.
- **Build adapters:** translate a project into a target-specific binary and package it in the required container/header format.
- **Validation:** structural checks, emulator smoke tests and (when available) physical-device testing.
- **Distribution:** checksummed artifacts, build manifests, licenses and release notes.

## 3. Target lifecycle

`planned → toolchain-ready → buildable → emulator-tested → hardware-tested`

A status advances only when the corresponding evidence exists. Hardware testing is optional for development but must be clearly distinguished from emulator testing.

## 4. ROM and cartridge boundary

A ROM file is software data, not a universal bootable operating system. Cartridge compatibility depends on the console's mapper/board, memory layout, save hardware and physical cartridge implementation. Snakey's future cartridge documentation will describe supported boards and safe, read-only verification procedures. It will not claim that a file can be written to any arbitrary cartridge.

## 5. Emulator integration

Emulators are test backends, not target architectures. A target can have multiple emulator profiles, and a profile is considered supported only after a reproducible smoke test. RetroArch core availability and standalone emulator compatibility vary by platform and version.

## 6. Build reproducibility

Every release should record target ID, toolchain version, source revision, build flags, output format and SHA-256 checksum. Build outputs must be generated from source; copyrighted commercial game ROMs and firmware are not part of this repository.

## 7. Current scope

The initial registry describes NES, SNES, Game Boy, Game Boy Color, Game Boy Advance and Nintendo DS homebrew targets. The registry is descriptive: it does not imply that compilers, ROM packagers or hardware tests have already been implemented.
