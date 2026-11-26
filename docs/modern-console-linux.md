# Snakey Linux on Modern Consoles

## Product decision

Snakey's primary direction is now **real Linux on modern consoles**. Stop treating a flat-color ROM screen as a desktop milestone. The Linux edition must boot a real kernel, mount a real root filesystem, start userspace and expose actual display/input/network drivers.

Retro ROMs remain a separate optional homebrew SDK. NES, SNES, Game Boy, GBA and DS ROMs are not Linux editions and will not be presented as XFCE or desktop previews.

## Target order

| Priority | Platform | Architecture | Why it is in this lane | Initial goal |
| --- | --- | --- | --- | --- |
| 1 | PlayStation 4 | x86-64 | Existing upstream Linux psX work and compatibility evidence on a specific PS4 Slim configuration; reuses the architecture of Snakey's current Slackware userspace | Reproduce a pinned upstream kernel build, then prepare a console-specific rootfs |
| 2 | PlayStation 5 | x86-64 | Public kernel patch and image ecosystem; separate hardware/firmware compatibility | Audit exact kernel base, patch revision and build provenance |
| 3 | Nintendo Switch | AArch64 | Established community Linux ecosystem and 4 GB RAM class | Audit maintained kernel, device tree, graphics, input and network support |

This order is an engineering priority, not a claim that every revision or model works. PS4 compatibility is especially model/southbridge-specific. PS5 and Switch remain independent ports; do not reuse a PS4 kernel on them.

## PS4 first: integration stages

1. **Source audit:** record the exact upstream repository, full commit SHA, kernel base, submodules, toolchain, build commands and license inventory.
2. **Reproducible CI build:** build the pinned upstream kernel on a hosted Linux runner. Archive configuration, build log, artifact and SHA-256. This is a cross-build result, not a boot result.
3. **Root filesystem:** adapt Snakey's Slackware-derived userspace only after kernel requirements and supported architecture are confirmed. Keep kernel modules matched to the exact kernel build.
4. **Driver validation:** document display/framebuffer or GPU, controller/input, storage, audio and network support separately.
5. **Boot evidence:** record exact console model/revision and upstream-supported environment. A successful compile does not mean the console boots.
6. **Desktop:** start with a shell and lightweight graphical session. Add XFCE only after the actual driver path and available memory are measured.

## Build and safety boundaries

- Development begins with source review, host-side builds, static checks and CI artifacts.
- Do not automate firmware changes, exploit execution, boot-payload deployment or writes to a physical console.
- Do not claim compatibility from the console family name alone.
- Never label an artifact bootable until there is reproducible boot evidence for a specific model/configuration.
- Keep source-build, kernel-boot, userspace-boot, graphical-session and physical-hardware statuses separate.
- The user's existing PC/CI environment remains the development host; a physical console is not assumed to be available.

## Explicitly out of scope for the first release

- Running Linux on NES/SNES/GB/GBC/GBA/DS.
- Treating emulator ROMs or static color screens as Linux desktops.
- One universal kernel/image for PS4, PS5 and Switch.
- Promising XFCE before display/input drivers and memory availability are measured.

## Current status

- [x] Choose modern-console Linux as the primary console direction.
- [x] Set PS4 as the first source/build integration target.
- [ ] Pin and audit the PS4 upstream source revision.
- [ ] Reproduce a PS4 kernel build in CI.
- [ ] Produce a matching Snakey root filesystem.
- [ ] Validate console-specific drivers and boot evidence.
- [ ] Evaluate XFCE on a verified configuration.
- [ ] Start separate PS5 and Switch build lanes after their source audits.

## Upstream research references

- PS4 Linux psX: https://github.com/meerzulee/linux-psx
- PS4 compatibility notes: https://linux.mrz.sh/compatibility/
- PS5 Linux projects: https://github.com/ps5-linux
- Switch Linux community: https://gitlab.com/l4t-community
