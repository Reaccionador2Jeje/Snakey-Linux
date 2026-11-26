# Snakey PSP

Snakey PSP is the native PSP homebrew edition of the Snakey project. It is a PSP application for real PSP homebrew environments and PPSSPP; it is **not** a PSP Linux kernel or a Slackware installation.

## Build

Use the official PSPSDK toolchain (devkitPro PSP toolchain) or the repository GitHub Actions workflow:

```sh
cd psp
make
```

The build produces `EBOOT.PBP` in this directory. The CI artifact is named `snakey-psp-homebrew`.

## Run in PPSSPP

1. Download the `snakey-psp-homebrew` artifact from the PSP Homebrew workflow.
2. Extract the artifact.
3. Copy the resulting `EBOOT.PBP` into a folder such as `PSP/GAME/SNAKEY/` in PPSSPP's memory stick directory.
4. Open **Games** in PPSSPP and launch **Snakey PSP**.

## Controls

- D-pad Up/Down: move through the menu.
- Cross: select.
- Circle: return from a page.
- Start: exit.

## Current scope

The first milestone is a native, controller-driven bootable homebrew shell. The shell and system-information pages are initial UI scaffolding; a command interpreter, persistent storage, cartridge/package support and Linux kernel boot are not implemented yet. A successful CI build proves compilation and packaging only; PPSSPP runtime verification must be recorded separately.
