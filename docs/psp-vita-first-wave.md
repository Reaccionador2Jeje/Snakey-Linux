# PSP + PS Vita: Snakey Linux first wave

The first active console targets are now **PSP (priority 1)** and **PS Vita (priority 2)**. PS4 and the remaining consoles are deferred while these two independent ports reach reproducible host-side milestones.

## PSP — historical uClinux recovery

The PSP has a documented historical Linux port based on uClinux. The archived PSP Linux project lists a 0.22 bundle, Buildroot patches, BusyBox configuration, kernel configuration and kernel patch. This is archival material, not a maintained modern Linux distribution.

- CPU family: MIPS Allegrex, little-endian.
- Memory: model-dependent; the original PSP-1000 has 32 MiB, later models have different memory configurations.
- Realistic first result: recover the historical source, understand the kernel/toolchain/ABI, then reproduce a host-side build if the sources and licenses permit.
- Not a goal for this phase: XFCE, a PC-style desktop, or claims of current driver completeness.

### PSP milestones

1. Retrieve the published historical source archives in CI.
2. Verify ZIP/GZIP integrity without executing or installing their contents.
3. Record SHA-256, archive members and license-notice candidates.
4. Identify the exact kernel lineage, patch applicability, compiler/binutils/uClibc versions and Buildroot base.
5. Audit licensing and source completeness.
6. Only then design an isolated, reproducible MIPS/uClinux build job.

The PSP archive audit deliberately does not extract or execute archive contents, create a boot image, alter console firmware or deploy anything to hardware. Its fetcher is restricted to the declared psplinux.info HTTPS host. The unified toolchain is listed on an external download host and is not treated as verified or fetched by CI.

## PS Vita — ARMv7 upstream reproduction

The Vita lane uses the pinned acgh213/vita-linux-next upstream source at commit 05ee2d57b1d5a6f7b477141c3c68f65a069d682c. The workflow checks out recursive submodules, records their exact gitlinks, runs upstream build-contract tests, applies vita_defconfig, compiles the kernel and three device trees, verifies them, and uploads checksummed artifacts.

The upstream project documents Linux 6.12 booting to a shell on Vita 1000 and PSTV, with four Cortex-A9 cores, framebuffer, touchscreen/buttons, storage and Wi-Fi. This is upstream project evidence, not a Snakey hardware test. GPU acceleration and a full package-managed distribution remain separate milestones.

### Vita milestones

1. Build the pinned Buildroot initramfs as a separate GitHub Actions job.
2. Preserve the upstream commit, Buildroot submodule revision and initramfs SHA-256.
3. Embed that initramfs into the Vita kernel build using the upstream vita_defconfig.
4. Verify zImage and Vita 1000 / Vita 2000 / PSTV DTBs.
5. Build a Snakey-owned ARMv7 root filesystem as a separate, later stage.
6. Integrate branding and userspace only after ABI and kernel/module compatibility are documented.

CI does not run upstream deploy, push, boot or hardware-gate commands. The rootfs and kernel are upstream artifacts for reproducibility; Snakey-specific integration and hardware boot remain future gates.

## Evidence labels

- archive-audited: archived bytes pass integrity checks; no build claim.
- upstream-build-passed: upstream host build succeeded.
- snakey-kernel-built: Snakey-integrated kernel built.
- kernel-boots: boot evidence for an explicitly named model.
- userspace-boots: Snakey userspace reaches a shell.
- hardware-verified: the stated hardware gates passed.

A source archive audit is not a kernel build. A kernel build is not a console boot.
