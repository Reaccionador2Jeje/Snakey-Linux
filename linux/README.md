# Snakey Linux Desktop

Snakey Linux Desktop is the Linux distribution track of this repository. It is
built from Slackware packages with the upstream **liveslak** live-image
builder. It is separate from the console homebrew ROMs under the SDK.

## First desktop profile

The initial profile is defined in [profile.json](profile.json):

- **Slackware 15.0 stable** (`slackware64-15.0`), x86_64
- Native Slackware package management (`pkgtools`) and SysVinit
- Snakey custom liveslak variant (`LIVEDE=SNAKEY`) using the lean XFCE package sequence
- Graphical runlevel 4
- XZ-compressed SquashFS modules
- liveslak's `bloat` trimming option
- Hostname: `snakey`

This is deliberately a real XFCE desktop, not a mockup or a ROM menu.
Applications and services will be trimmed further only after boot testing.
The rootcopy also installs Snakey's release identity, login banner, SVG wallpaper,
default XFCE wallpaper/GTK settings, the packaged Snakey Dark theme, and the Snakey Gamepad UI autostart/launcher.
See [Gamepad UI documentation](gamepad/README.md) for controls and dependencies, [Console Mode documentation](console/README.md) for the TV-friendly desktop, and [Big Picture documentation](big-picture/README.md) for the fullscreen controller-first launcher. The [Controller Center](gamepad/README.md#controller-center) configures and tests controller profiles.

## Build

The base is pinned to **Slackware 15.0 stable**, not the moving `current` branch. The committed `make_slackware_live.conf` defines a custom liveslak variant named `SNAKEY` and a package sequence based on `min`, `xbase`, `xapbase`, and `xfcebase`. Snakey adds two native packages through liveslak's `local64` mechanism: `snakey-base` (release identity and system information) and `snakey-theme` (GTK2/GTK3 Snakey Dark theme). Package updates within Slackware 15.0 can still change over time.

The image builder must run as root on a supported Slackware 15.0 x86_64 build host with the prerequisites documented by liveslak. It also needs a local mirror root containing `slackware64-15.0/`; by default this is `/var/cache/snakey/slackware/slackware64-15.0`. Set `SNAKEY_SLACKWARE_REPO` to use another mirror root. The build script fetches liveslak on first run and builds both native `.txz` packages with Slackware `makepkg`.

```bash
sudo linux/build-live.sh
```

The output is:

- `dist/Snakey-Linux-XFCE-x86_64.iso`
- `dist/Snakey-Linux-XFCE-x86_64.iso.sha256`

### Native package

Snakey ships two native packages: `snakey-base` installs `/etc/snakey-release` and `/usr/bin/snakey-info`; `snakey-theme` installs the GTK2/GTK3 theme under `/usr/share/themes/Snakey-Dark`. XFCE's default settings select Snakey Dark, while the window manager and icon theme use Slackware's installed Adwaita assets. Package sources and `makepkg` builders are in [packages/](packages/README.md).

Optional environment variables:

| Variable | Default |
| --- | --- |
| `SNAKEY_ARCH` | `x86_64` |
| `SNAKEY_OUTPUT_DIR` | `./dist` |
| `SNAKEY_LIVESLAK_DIR` | `./.build/liveslak` |
| `SNAKEY_LIVESLAK_REPO` | `https://git.slackware.nl/liveslak` |
| `SNAKEY_SLACKWARE_REPO` | `/var/cache/snakey/slackware` |

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
- Keep a console-only recovery path available in future builds.\n- Keep Snakey Console Mode as an optional large-control profile for TVs and gamepads.

## Current status

The Slackware 15.0 profile, custom liveslak variant, native `snakey-base` and `snakey-theme` package sources, and build entrypoint are now in the repository. The ISO has not
yet been generated or boot-tested. The builder expects a Slackware build host;
the Debian/Ubuntu GitHub runner is not treated as a valid liveslak build host.
