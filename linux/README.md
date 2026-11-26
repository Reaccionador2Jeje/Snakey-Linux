# Snakey Linux Desktop

Snakey Linux Desktop is the Linux distribution track of this repository. It is
built from Slackware packages with the upstream **liveslak** live-image
builder. It is separate from the console homebrew ROMs under the SDK.

## First desktop profile

The initial profile is defined in [profile.json](profile.json):

- **Slackware 15.0 stable** (`slackware64-15.0`), x86_64
- Native Slackware package management (`pkgtools`) and SysVinit
- Snakey custom liveslak variant (`LIVEDE=SNAKEY`) using the lean XFCE package sequence
- Graphical runlevel 4, XZ-compressed SquashFS and liveslak's `bloat` trimming
- Hostname: `snakey`

This is a real XFCE desktop, not a mockup or a ROM menu. The rootcopy installs
Snakey's release identity, wallpaper, theme, Gamepad UI, Console Mode and
Big Picture launcher.

## Snakey Web

Snakey Web is the Linux desktop's browser entry point. It registers HTTP/HTTPS
URLs and opens them in an installed browser engine, preferring Firefox,
Chromium, Falkon and SeaMonkey. The small Snakey launcher validates the URL
and delegates rendering, TLS, cookies and standards support to that engine;
it does not pretend that a custom text viewer is a modern browser.

The Slackware image build creates and includes the `snakey-browser` package.
The selected browser engine must be installed in the Slackware package set;
the launcher reports a clear error if none is available. You can override
detection with `SNAKEY_BROWSER=executable-name`.

## Build

The image builder must run as root on a supported Slackware 15.0 x86_64 host
with liveslak prerequisites and a local mirror containing
`slackware64-15.0/`. By default, the mirror root is
`/var/cache/snakey/slackware`; set `SNAKEY_SLACKWARE_REPO` to change it.

```bash
sudo linux/build-live.sh
```

Output:
- `dist/Snakey-Linux-XFCE-x86_64.iso`
- `dist/Snakey-Linux-XFCE-x86_64.iso.sha256`

The builder creates native Slackware packages with `makepkg`, then invokes
liveslak. It has not yet been run on a supported Slackware build host, and
the ISO has not been boot-tested in Limbo/QEMU.

## Limbo test target

Create an x86_64 VM, attach the ISO as a CD-ROM and boot from it. Confirm the
bootloader, kernel, live root, XFCE session, keyboard, pointer, network and
shutdown. Then launch Snakey Web and visit an HTTPS site. Record emulator
results separately from image-build results.

## Ultra-light policy

- Keep XFCE rather than adding a heavier desktop environment.
- Avoid KDE, Plasma, GNOME and unnecessary background services.
- Keep the browser engine optional/detected rather than claiming a bundled
  browser that is not actually present in the Slackware mirror.
- Measure idle RAM, boot time and image size before making performance claims.
- Keep a console-only recovery path.
