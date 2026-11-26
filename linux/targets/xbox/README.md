# Snakey Linux — Original Xbox target

**Status: research-only. No Snakey kernel, root filesystem or desktop has been built or booted.**

## Intended desktop model

The Original Xbox edition will run Snakey Desktop **inside Snakey Linux userspace**.
It will not be a standalone Xbox homebrew desktop. The intended boot sequence is:

1. A separately validated Xbox-compatible Linux boot path loads the Snakey kernel.
2. The kernel initializes supported storage, framebuffer and controller/input drivers.
3. The Snakey root filesystem starts its init system.
4. Init launches `/usr/bin/snakey-desktop` as the primary fullscreen session.

## Hardware and desktop budget

- Architecture: i686 x86.
- Memory class: 64 MiB.
- Desktop profile: `snakey-ultralight`.
- Initial graphics target: software-rendered Linux framebuffer (`/dev/fb0`).
- Initial input target: Linux evdev controller events.
- Xorg, Wayland and XFCE4 are not planned for this memory class.

The shared desktop must keep its working set small, use a limited asset/font set,
and avoid background services that are not required for the session.

## Shared desktop contract

The common Linux session and application model are defined in:
- `desktop/linux/README.md`
- `desktop/linux/desktop-contract.json`

Applications: Launcher, Files, Console, System Monitor, Settings and About.
Unavailable storage or input devices must be reported, never represented as
mounted or working when they are not.

## Engineering gates

1. [ ] Identify and audit a redistributable, maintained Xbox Linux kernel/loader source.
2. [ ] Pin an exact source revision and reproducible i686 toolchain.
3. [ ] Build and inspect a kernel without claiming it boots.
4. [ ] Build a minimal Snakey root filesystem.
5. [ ] Reach a Linux userspace shell in an explicitly named emulator or on hardware.
6. [ ] Verify framebuffer and controller input drivers.
7. [ ] Cross-build and launch Snakey Desktop from Linux init.
8. [ ] Measure memory use and validate the desktop on the named target.

CI is limited to source review, cross-builds and static artifacts. It must not
modify firmware, deploy payloads, or write to physical console storage.

A successful cross-build is not a kernel boot. A kernel boot is not a working
userspace. A working userspace is not a tested desktop.

## Slackware base — 32-bit x86

The Original Xbox userspace is intended to derive from **Slackware 15.0
32-bit x86**, rebuilt/trimmed for the console's i686-class CPU. Slackware 15.0
publishes a native 32-bit x86 package tree; this is a much closer base than
starting from an unrelated distribution.

Because the Xbox has only a 64 MiB memory class, this is not a full Slackware
installation. Snakey will select a minimal package subset and build a
console-specific root filesystem.

Base requirements:
- Slackware package format and pkgtools database/operations.
- Slackware filesystem layout and SysVinit startup conventions.
- A minimal shell, core utilities, libc, device management and required
  libraries only.
- i686-compatible kernel and userspace ABI, verified together.
- Snakey's framebuffer desktop and controller/input services added after the
  base system boots to a shell.

The standard Slackware 15.0 x86 package tree is the package/source baseline;
Xbox kernel, boot integration, drivers and the final package set remain
console-specific engineering work. No bootable image is claimed.
