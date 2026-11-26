# Snakey Linux — PlayStation 3 bring-up

## Current direction

PS3 is now an active Snakey Linux kernel research lane. The first reproducible
milestone uses the upstream Linux v6.12 release commit
adc218676eef25575469234709c2d87185ca223a and its
arch/powerpc/configs/ps3_defconfig.

The pinned CI job:
- validates the source pin and PS3 target metadata;
- cross-compiles the upstream PS3 kernel configuration for PowerPC64
  big-endian;
- checks that the resulting vmlinux is a PowerPC64 big-endian ELF;
- uploads the kernel, config, System.map, provenance and SHA-256 checksums.

This is a kernel build artifact, not a bootable PS3 image. It does not
include a root filesystem, PS3 firmware, a bootloader, or a tested launch
method. CI does not modify console firmware, execute exploits, deploy payloads,
or write to a physical console.

## About aPS3e

[aPS3e](https://github.com/aenu1/aps3e) is an Android PlayStation 3 game
emulator based on RPCS3. Its published feature set describes game formats,
Vulkan rendering and game save/load features; it does not document booting
arbitrary PS3 Linux kernels or emulating the PS3 OtherOS boot path.

Therefore aPS3e is not currently accepted as a Snakey kernel test platform.
It may be useful for testing PS3 games, but a successful game launch says
nothing about whether Snakey Linux boots. Do not mark the PS3 Linux port as
emulator-tested based on aPS3e.

## Bring-up gates

1. Kernel source build: pinned upstream PS3 defconfig compiles in CI.
2. Boot-path research: document the supported PS3 model and lawful,
   documented boot environment before attempting a boot test.
3. Root filesystem: create a PowerPC64 big-endian Slackware-compatible
   userspace only after package availability, ABI and init dependencies are
   audited. Do not reuse PPC32 Wii packages or assume Slackware x86_64 packages
   are compatible.
4. Console drivers: validate PS3 framebuffer, storage, network and input
   support against the selected kernel configuration.
5. Userspace boot: reach a TTY login and collect memory/driver evidence.
6. Snakey Desktop: enable XFCE4 only after X11, display/input drivers and the
   actual available memory budget are proven.

## Run the PS3 CI lane

From GitHub Actions, run the PSP and Vita Linux research builds workflow with
the workflow-dispatch target set to ps3. The PS3 job is also triggered by
changes to the source/target manifests, this document, or the workflow itself.

## Evidence policy

A source pin is not a hardware test. A successful cross-build is not a boot
test. Keep snakey_kernel_built and snakey_hardware_tested false until
their corresponding evidence exists. The PS3 registry entry remains
source-audit-required until the project has completed the separate boot
and userspace validation gates.
