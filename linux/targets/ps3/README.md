# Snakey Linux — PlayStation 3 bring-up

<badge>Research candidate — not a Snakey release</badge>

## Why PS3 first

The PS3 has a PowerPC 64-bit Cell PPE, 256 MiB of system RAM and 256 MiB of
video RAM. The video RAM is separate and must **not** be counted as ordinary
system memory. Linux has a dedicated `CONFIG_PPC_PS3` platform option and
PS3-specific storage, framebuffer, system-manager and GELIC Ethernet drivers.

A recent independent project documents Debian sid ppc64 on a PS3 with a
PS3-specific 6.4 kernel and OtherOS++/Petitboot. Its hardware verification is
specific to a Slim CECH-2503B configuration; it is not proof that all PS3
models or firmware combinations work.

## Boot-chain reality

There are two historically used paths:

- Sony's legacy OtherOS feature, restricted to compatible older firmware and
  models.
- OtherOS++ with Petitboot on specifically compatible configurations.

Snakey does not install custom firmware, modify console flash, repartition a
console, or run destructive setup steps. Any future physical test must use a
known-compatible configuration, preserve the existing system, and be performed
by the hardware owner with appropriate adult supervision. Until then, work is
limited to source review, cross-compilation and non-destructive validation.

## Memory and desktop strategy

- System memory: 256 MiB.
- Video memory: 256 MiB, separate from system RAM.
- First milestone: kernel reaches a visible framebuffer console.
- Second: root filesystem mounts and a shell starts.
- Third: wired Ethernet and USB keyboard/controller work.
- Fourth: measure memory with a minimal graphical server.
- Fifth: evaluate XFCE4. It is experimental and may be too heavy; LXDE/LXQt or
  Snakey Big Picture may be the practical fallback.

The official hypervisor framebuffer is the baseline. Do not assume accelerated
RSX graphics or treat VRAM swap as equivalent to physical RAM.

## Kernel baseline

The reference kernel work uses Geoff Levand's PS3 Linux tree. A recent Debian
bring-up project uses a 6.4-based PS3 kernel with additional storage fixes.
Snakey tracks that work as an external reference; we do not copy its scripts
or claim its patches are already integrated.

`kernel.fragment` records the minimum Snakey feature goals to compare against
a PS3 `ps3_defconfig`. It is a requirements overlay, not a standalone kernel
configuration. Symbol availability and dependencies must be checked against
the exact kernel source before a build.

## Reproducible development stages

1. [x] Register PS3 as a separate Linux-system target.
2. [x] Record hardware, memory and boot-chain constraints.
3. [x] Add a kernel requirements overlay for review.
4. [ ] Pin an auditable PS3 kernel source revision and patch set.
5. [ ] Set up a reproducible ppc64 cross-build in GitHub Actions.
6. [ ] Build and inspect the kernel image without claiming it boots.
7. [ ] Obtain a compatible test console and verify boot to framebuffer.
8. [ ] Boot a minimal userspace and collect memory measurements.
9. [ ] Test XFCE4 only after the shell and display path are stable.

## External technical references

- Linux kernel PS3 platform Kconfig: https://code.googlesource.com/linux/torvalds/linux/+/master/arch/powerpc/platforms/ps3/Kconfig
- Linux PS3 Ethernet driver Kconfig: https://kernel.googlesource.com/pub/scm/linux/kernel/git/ralf/linux/+/ea0dc0dc1c1dca25e50384e300a528db57ee7de5/drivers/net/Kconfig
- Debian on PS3, kernel and hardware notes: https://github.com/setsid/ps3-linux-internal-ssd
- PS3 Linux distribution notes: https://playstationdev.wiki/ps3/Distributions

## Status vocabulary

A kernel compiling is not a kernel booting. A framebuffer console is not a
Linux desktop. XFCE4 is only complete when the actual session has launched and
been measured on a named PS3 configuration.
