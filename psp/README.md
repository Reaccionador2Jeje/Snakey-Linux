# Snakey PSP

Snakey PSP is the native PSP homebrew edition of Snakey Linux. It runs as a PSP application in PPSSPP or on compatible PSP homebrew setups. This milestone provides a controller-driven desktop shell; it is **not yet a bootable Linux kernel or Slackware installation**.

## Build

Use the official PSPSDK toolchain or the repository GitHub Actions workflow:

```sh
cd psp
make
```

The build produces `EBOOT.PBP`.

## Install in PPSSPP

Download `EBOOT.PBP` from the latest [Snakey PSP GitHub release](https://github.com/Reaccionador2Jeje/Snakey-Linux/releases), then place it at:

```
PSP/GAME/SNAKEY/EBOOT.PBP
```

Open **Games** in PPSSPP and launch **Snakey PSP**. Do not launch the PBP as a loose file from Downloads.

## Desktop controls

- D-pad Up/Down: select a desktop application.
- Cross: open the selected application.
- Circle: return to the desktop.
- Start: exit Snakey PSP.

## Terminal controls

- D-pad: move around the on-screen keyboard.
- Cross: type the selected key.
- Square: delete the last character.
- Start: execute the command.
- Circle: return to the desktop.

## Built-in commands

- `help`: list available commands.
- `clear`: clear terminal output.
- `uname`: show Snakey PSP platform information.
- `version`: show the build version.
- `mem`: show the target memory class.
- `pwd`: show the virtual working directory.
- `ls`: show the current virtual workspace entries.
- `echo TEXT`: print text.
- `exit`: return to the desktop.

The current `ls` output is a virtual workspace preview. Persistent storage, cartridge mounting, package management, and a Linux kernel boot are future milestones. The command runtime is a small built-in interpreter, not a general POSIX shell.

## Automated releases

Every successful push build on the main branch publishes a GitHub prerelease containing `EBOOT.PBP`, this installation guide, and `SHA256SUMS`. Pull requests build and validate the application but do not publish releases.
