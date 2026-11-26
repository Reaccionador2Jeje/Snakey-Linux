# PlayStation Linux research

This document tracks upstream evidence only. Snakey does not provide console
firmware modification instructions, boot payloads, exploit procedures, or
physical deployment automation. Builds in CI are source-only and run on hosted
Linux runners.

## PlayStation 3 — PowerPC64

- CPU family: Cell Broadband Engine, PowerPC64 PPE.
- Memory: 256 MB system RAM plus separate 256 MB RSX video memory.
- Linux history: legacy OtherOS and community OtherOS++ paths exist, but depend
  on exact model/configuration and an already compatible boot environment.
- Kernel family: PS3-specific PowerPC kernel support (CONFIG_PPC_PS3).
- Main engineering challenge: old boot chain, low system memory, RSX/display
  limitations and PowerPC big-endian userspace compatibility.
- Status: research-only and explicitly deferred by the owner. No physical
  access, modification or testing is planned.

Important correction: ArchPOWER is a PowerPC distribution, not a direct PS3
port. Its maintainer has explicitly said PS3 support is not currently provided.
Do not describe ArchPOWER as a verified PS3 distribution.

References:
- https://playstationdev.wiki/ps3/Distributions
- https://github.com/kth5/archpower/issues/38

## PlayStation 4 — x86-64

- CPU/GPU: AMD Jaguar APU and Radeon GCN-family graphics.
- Memory: 8 GB unified GDDR5 (hardware-reserved regions reduce what Linux can
  use).
- Upstream project: [Linux psX](https://github.com/meerzulee/linux-psx).
- Evidence: the project reports Linux 7.2.11 beta2 on one PS4 Slim with a
  Baikal B1 southbridge, including Xorg/XFCE, 1080p display and graphics.
- Compatibility: Aeolia, Belize, Belize 2 and PS4 Pro are not verified by the
  cited project's current compatibility table. A model name alone is not
  enough to infer the southbridge.
- Snakey plan: audit source, exact revision, kernel base, build scripts,
  toolchain, modules and license; reproduce a host-side kernel build in CI.
  Only then design a Snakey rootfs.

Reference: https://linux.mrz.sh/compatibility/

## PlayStation 5 — x86-64

- CPU/GPU: AMD Zen 2 APU with RDNA 2-class graphics.
- Memory: 16 GB unified GDDR6; not all memory is necessarily available to Linux.
- Upstream project: [ps5-linux](https://github.com/ps5-linux), including
  kernel patches/configuration and an image builder.
- Evidence: public kernel patch sets and Linux image releases exist. Hardware
  and firmware compatibility varies; a published build is not universal
  compatibility.
- Snakey plan: audit patch history, stable-kernel base, build scripts, module
  set, licenses and artifact provenance before enabling CI.

Reference: https://github.com/ps5-linux/ps5-linux-patches

## Shared Snakey acceptance gates

1. Pin every upstream repository to a full commit SHA.
2. Record kernel base, toolchain version, submodules and license inventory.
3. Build only on hosted CI; do not automate console-side firmware changes.
4. Produce checksums and source provenance for artifacts.
5. Keep kernel build, rootfs build, emulator evidence and physical-hardware
   evidence as separate statuses.
6. Never mark a target bootable based only on a successful compilation.
7. Do not require the owner's PS3 or any other physical console for progress.

## Priority

1. PS4: x86-64 build audit and host-side reproducibility.
2. PS5: separate patch audit after PS4.
3. PS3: PowerPC64 source research only; hardware work remains deferred.
