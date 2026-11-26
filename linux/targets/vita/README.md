# Snakey Linux — PlayStation Vita research lane

## Why Vita is the first reproducible build lane

The public Vita Linux Next project documents Linux 6.12 on Vita 1000 and
PlayStation TV, with four Cortex-A9 cores, framebuffer console, input, storage,
and network support. Its CI already describes a Bootlin ARMv7 cross-toolchain,
kernel configuration, device-tree build/verification, zImage build and staged
artifacts.

Snakey pins the outer integration source at:

`acgh213/vita-linux-next`
`05ee2d57b1d5a6f7b477141c3c68f65a069d682c`

Upstream source: https://github.com/acgh213/vita-linux-next

## Scope of Snakey CI

The `console-linux-research.yml` workflow:
- checks out the exact upstream commit and its recorded submodules;
- uses the upstream Bootlin ARMv7 toolchain release;
- runs the upstream host/demo build contract;
- configures and builds the Vita kernel and device trees;
- verifies the generated DTBs;
- uploads the upstream zImage/DTB staging directory with provenance.

The artifact is explicitly an **upstream Vita Linux integration artifact**.
It is not an original Snakey kernel, not a complete Snakey root filesystem,
and not proof that Snakey boots on physical hardware.

## Safety and non-deployment boundary

CI must never deploy a payload, write removable media, alter console firmware,
or run hardware-gate/deploy scripts. This repository only performs source
builds and static validation. Physical hardware testing is a separate milestone
and is not required for the CI build.

## Next engineering gates

1. Reproduce the pinned upstream kernel build in GitHub Actions.
2. Record artifact SHA-256 and source/submodule provenance.
3. Design a Snakey-specific Buildroot rootfs only after kernel output is stable.
4. Keep GPU/SGX acceleration separate from framebuffer support.
5. Evaluate XFCE4 only after a measured memory/display session; a working shell
   does not imply a complete desktop.

## Snakey Desktop session

The intended desktop is a **Linux userspace session**, not a standalone Vita
homebrew. After the Snakey Linux kernel and root filesystem boot, Linux init
will start the shared `/usr/bin/snakey-desktop` session.

Initial backend: fullscreen software rendering on Linux framebuffer
(`/dev/fb0`) with controller input through evdev. This avoids requiring
Xorg/Wayland for the first desktop milestone. Vita's available memory makes
XFCE4 a later optional experiment, not the first session.

Shared architecture and application contract:
- `desktop/linux/README.md`
- `desktop/linux/desktop-contract.json`

Current state: architecture defined only. The pinned upstream Vita build is
not yet a Snakey kernel/rootfs or a bootable Snakey Desktop image. Native
renderer, init integration and emulator/hardware validation remain pending.
