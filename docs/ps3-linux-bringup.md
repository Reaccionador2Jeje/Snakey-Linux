# Snakey Linux — PlayStation 3 bring-up

## Current direction

PS3 is the active Snakey Linux kernel research lane. The first reproducible
milestone uses the upstream Linux v6.12 release commit
adc218676eef25575469234709c2d87185ca223a and its
`arch/powerpc/configs/ps3_defconfig`.

The pinned CI job:
- validates the source pin and PS3 target metadata;
- cross-compiles the upstream PS3 kernel configuration for PowerPC64
  big-endian;
- checks that the resulting `vmlinux` is a PowerPC64 big-endian ELF;
- uploads the kernel, config, System.map, provenance and SHA-256 checksums.

This is a kernel build artifact, not a bootable PS3 image. It does not
include a root filesystem, PS3 firmware, a bootloader, or a tested launch
method. CI does not modify console firmware, execute exploits, deploy payloads,
or write to a physical console.

## aPS3e: supported and unsupported test roles

[aPS3e](https://github.com/aenu1/aps3e) is an Android PS3 **game emulator**
based on RPCS3. Its published feature list describes game execution, game
formats, Vulkan rendering and save/load features. It does not document a
PS3 OtherOS environment, arbitrary external-kernel boot, or Linux virtual
machine support.

Consequently, aPS3e cannot currently be used to boot or validate the Snakey
Linux kernel, Slackware root filesystem, or XFCE4 session. Installing the
official PS3 system-software file in aPS3e configures the emulator; it does
not add a Linux boot facility. A game launching successfully is not evidence
that Snakey Linux works.

**Permitted project use for aPS3e:** keep it as a separate PS3 game-emulation
reference only. Do not label any Snakey Linux component as aPS3e-tested unless
the emulator developers document and expose a Linux/OtherOS boot feature and
we verify it independently.

## Practical validation path for Slackware + XFCE4

Use a layered test strategy instead of treating aPS3e as a Linux VM:

1. **Kernel cross-build:** compile the pinned PS3 kernel configuration in CI
   and archive its configuration, ELF metadata and checksums.
2. **PPC64 userspace audit:** assemble the candidate package set in
   `linux/rootfs/ps3.packages` from mutually compatible PowerPC64 big-endian
   Slackware-compatible archives. For the desktop candidate set, use
   `linux/rootfs/ps3-xfce4.packages` with `SNAKEY_PACKAGE_MANIFEST`. Run `tools/audit_ps3_rootfs.py ROOTFS` to
   reject non-ELF64, little-endian or non-PPC64 binaries. Then verify the ELF
   interpreter, shared-library dependencies, init scripts and package
   provenance. Never reuse Wii PPC32 packages or x86_64 Slackware binaries.
3. **Userspace smoke tests:** where suitable PPC64 user-mode emulation is
   available, test basic binaries, package scripts and service startup in an
   isolated rootfs. This validates userspace behavior only—not PS3 devices,
   kernel boot, framebuffer, networking, or controller support.
4. **XFCE4 dependency and session tests:** check the complete XFCE4/X11
   dependency closure and attempt a virtual-display session in the emulated
   userspace. Record memory use and startup failures. This is not proof that
   PS3 graphics or input drivers work.
5. **PS3-specific boot and drivers:** validate the documented boot path,
   storage, framebuffer, input and network on a supported PS3 environment.
   Keep this separate from emulator and userspace tests.
6. **Desktop acceptance:** only call XFCE4 supported after the PS3 session
   starts with working display/input and measured memory headroom. PS3 has a
   256 MiB system-memory class, so XFCE4 remains conditional; prioritize a
   minimal service set and retain a TTY fallback.

## Bring-up gates

- [ ] Kernel source build: pinned upstream PS3 defconfig compiles in CI.
- [ ] PPC64 big-endian Slackware-compatible package set is assembled from `linux/rootfs/ps3.packages`.
- [ ] `tools/audit_ps3_rootfs.py` passes on the assembled rootfs; dynamic loader and shared-library closure are audited separately.
- [ ] Rootfs passes architecture, dependency, init and package-integrity checks.
- [ ] Userspace smoke tests pass; their scope is explicitly marked as emulated.
- [ ] PS3 XFCE4 candidate manifest passes `python3 tools/validate_ps3_xfce4_manifest.py`.
- [ ] XFCE4/X11 dependency closure and virtual-session tests pass.
- [ ] A documented PS3 boot environment is identified for the exact supported
      model and firmware state.
- [ ] PS3 framebuffer, storage, network and input support are validated.
- [ ] TTY login and resource measurements are collected on the PS3 target.
- [ ] XFCE4 starts on the PS3 target with working display and input.

## Run the PS3 CI lane

From GitHub Actions, run the **PSP, Vita and PS3 Linux research builds**
workflow with the workflow-dispatch target set to `ps3`. The PS3 job is also
triggered by changes to the source/target manifests, this document, or the
workflow itself.

## Evidence policy

A source pin is not a hardware test. A successful cross-build is not a boot
test. A PPC64 user-mode test is not a PS3 kernel or device test. An aPS3e game
test is not a Linux test.

Keep `snakey_kernel_built` and `snakey_hardware_tested` false until their
corresponding evidence exists. The PS3 registry entry remains
`source-audit-required` until the project has completed the separate boot
and userspace validation gates.
