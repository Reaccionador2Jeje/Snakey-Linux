# Snakey Linux Desktop

Snakey Linux Desktop is the Linux distribution track of this repository. It is
built from Slackware packages with the upstream **liveslak** live-image
builder. It is separate from the console homebrew ROMs under the SDK.

## First desktop profile

The initial profile is defined in [profile.json](profile.json):

- Slackware base, x86_64
- XFCE desktop using liveslak's stripped/basic XFCE variant
- Graphical runlevel 4
- XZ-compressed SquashFS modules
- liveslak's `bloat` trimming option
- Hostname: `snakey`

This is deliberately a real XFCE desktop, not a mockup or a ROM menu.
Applications and services will be trimmed further only after boot testing.
The rootcopy also installs Snakey's release identity, login banner, SVG wallpaper,
default XFCE wallpaper/GTK settings, and the Snakey Gamepad UI autostart/launcher.
See [Gamepad UI documentation](gamepad/README.md) for controls and dependencies.

## Build

The image builder must run as root on a supported Slackware build host with
the prerequisites documented by liveslak and access to a complete Slackware
package repository. The build script fetches liveslak on first run.

```bash
sudo linux/build-live.sh
```

The output is:

- `dist/Snakey-Linux-XFCE-x86_64.iso`
- `dist/Snakey-Linux-XFCE-x86_64.iso.sha256`

Optional environment variables:

| Variable | Default |
| --- | --- |
| `SNAKEY_ARCH` | `x86_64` |
| `SNAKEY_OUTPUT_DIR` | `./dist` |
| `SNAKEY_LIVESLAK_DIR` | `./.build/liveslak` |
| `SNAKEY_LIVESLAK_REPO` | `https://git.slackware.nl/liveslak` |

## Limbo test target

Create a new x86_64 virtual machine in Limbo, attach the ISO as a CD-ROM and
boot from it. Start with a conservative virtual hardware profile (2 CPU cores,
2 GiB RAM, standard VGA, and a writable virtual disk if persistence is later
needed). The ISO is a live environment; changes are not persistent unless a
persistent storage mechanism is configured.

The first acceptance checks are:

1. The bootloader appears.
2. The Linux kernel and live initramfs load.
3. The live root filesystem is assembled.
4. XFCE reaches a usable graphical session.
5. Keyboard, pointer, display resizing and shutdown work.

A successful ISO build is not proof that Limbo has booted it. Emulator results
must be recorded separately from build results.

## Ultra-light policy

- Keep XFCE rather than adding a heavier desktop environment.
- Do not install KDE, Plasma, GNOME or unnecessary background services.
- Prefer lightweight applications and avoid bundling large games.
- Measure idle RAM, boot time and image size in Limbo before setting claims.
- Keep a console-only recovery path available in future builds.

## Current status

The profile and build entrypoint are now in the repository. The ISO has not
yet been generated or boot-tested. The builder expects a Slackware build host;
the Debian/Ubuntu GitHub runner is not treated as a valid liveslak build host.
