# Snakey Linux — Nintendo Wii research target

## Decision

The Wii is Snakey's first active Linux-on-console research target. This is a
research selection, not a claim that Snakey currently boots on Wii hardware.

The Wii-Linux continuation project reports maintained PowerPC kernels,
framebuffer output, optional Xorg, and a current ArchPOWER-based userspace.
Its public compatibility and download pages must be checked again whenever a
kernel revision is selected:
- https://wii-linux.org/
- https://wii-linux.org/downloads
- https://wiki.wii-linux.org/wiki/Wii-Linux

## Hardware budget

- CPU: IBM Broadway PowerPC, approximately 729 MHz.
- Main memory: 88 MB total (24 MB 1T-SRAM + 64 MB GDDR3).
- GPU embedded memory: 3 MB; do not count it as general-purpose RAM.
- Storage options reported by the platform ecosystem: SD and USB.
- Display target: 480i/480p framebuffer path; exact mode depends on kernel/loader.

The memory budget is the major constraint. Snakey must not promise XFCE4.
The order of work is kernel boot, console shell, storage/network, framebuffer,
then a minimal Xorg session. XFCE4 is evaluated only after measuring actual
free memory and graphics stability.

## Non-invasive development policy

- No PlayStation 3 is required for this work.
- No console is to be opened, electrically modified, or subjected to firmware
  changes as part of this research.
- Do not write images to removable media or physical hardware without the
  owner's explicit decision and a verified backup.
- Initial work is source review, pinned toolchains, cross-compilation and
  static validation on the development host.
- Emulator boot is a separate milestone and must be reported with the exact
  emulator/version. It is not physical-hardware validation.

## Milestones

1. [x] Record Wii as the preferred research candidate.
2. [ ] Review upstream kernel/loader repositories and select a maintained,
   reproducible revision.
3. [ ] Pin the PowerPC cross-toolchain and kernel configuration.
4. [ ] Build a kernel artifact in CI and archive its checksum/config/log.
5. [ ] Reach a documented boot milestone in an appropriate emulator, if
   supported by the selected loader and emulator.
6. [ ] Reach a Linux shell.
7. [ ] Validate SD/USB, input, network and framebuffer.
8. [ ] Measure whether Xorg plus a minimal window manager is viable.
9. [ ] Evaluate XFCE4 only if measured resources justify the attempt.

## Status vocabulary

- Research candidate: evidence supports investigation; no Snakey build yet.
- Cross-buildable: CI generated an artifact from a pinned source/toolchain.
- Emulator-tested: artifact booted in a named emulator.
- Kernel boots: actual kernel reached a recorded boot milestone.
- Userspace boots: init and shell run.
- Hardware-tested: tested on a physical Wii with model and logs recorded.

Never promote a milestone without evidence.

## Snakey Desktop session

The target desktop is a **Linux userspace session**, not a Wii homebrew
application. Once a Snakey Linux kernel and root filesystem reach userspace,
Linux init will start the shared `/usr/bin/snakey-desktop` process.

The Wii profile is ultra-light: fullscreen software rendering through Linux
framebuffer (`/dev/fb0`) and controller input through evdev. It does not
depend on Xorg, Wayland or XFCE4. The 88 MiB memory budget requires keeping the
desktop, fonts, assets and background services tightly bounded.

Shared architecture and application contract:
- `desktop/linux/README.md`
- `desktop/linux/desktop-contract.json`

Current state: architecture defined only. Kernel/loader source selection,
Snakey rootfs, native renderer, init integration and emulator boot remain
pending. No Wii desktop build or boot is claimed.
