# Snakey Boot System

## Purpose

Snakey supports multiple ways to launch software. A ROM is a target-specific program image, not a universal operating system installer. The boot method must match the actual console hardware.

## Boot methods

| Method ID | Cartridge needed? | What happens |
| --- | --- | --- |
| `emulator-file` | No | An emulator opens a ROM/homebrew image as a file. |
| `cartridge-rom` | Yes | A compatible physical cartridge exposes the ROM to the console. |
| `flashcart-sd` | Yes | A flash cartridge reads a ROM from its SD card and presents it through the cartridge slot. |
| `homebrew-loader` | No | A supported console model/firmware loads a homebrew image. |
| `linux-boot-media` | No | Linux-capable hardware boots a kernel from supported SD, USB or internal storage. |

**Important:** putting a ROM on an SD card does not make an ordinary NES, SNES or Game Boy boot from SD. For those systems, an SD card normally belongs inside a compatible flash cartridge, which still plugs into the console.

## Per-console policy

The `platforms/targets.json` registry declares which methods are considered possible for each target. The SDK's `boot-plan` command checks that declaration and prints the prerequisites. It does not claim that a particular cartridge, firmware revision or physical console has been tested.

- NES, SNES, Game Boy, Game Boy Color and Game Boy Advance: emulator file, physical ROM cartridge, or a compatible flash cartridge with SD.
- Nintendo DS: emulator file, compatible flash cartridge with SD, or a model/firmware-specific homebrew loader.
- Linux-capable boards: Linux boot media, once a concrete board profile, kernel and boot chain have been validated.

## Linux is a separate execution family

A classic 8/16-bit console cannot boot a conventional Slackware kernel. Snakey's native-homebrew targets execute small programs built for their own CPUs and hardware. Snakey Linux is reserved for devices with a supported Linux boot chain, memory-management unit, sufficient RAM and kernel drivers.

## Cartridge and SD compatibility

Cartridge compatibility depends on console revision, mapper/board, ROM size, save-memory type, voltage and flash-cart firmware. SD compatibility depends on the flash cart's supported capacity and filesystem. Snakey will publish compatibility profiles only when they are documented and tested; it will not promise that every ROM works on every flash cart.

## Current implementation boundary

The SDK currently provides boot-method metadata and a boot-plan checker. It does not flash cartridges, modify console firmware, detect attached physical hardware or create Linux disk images. Those require separate, model-specific implementations and testing.
