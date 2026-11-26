# Snakey Linux — Ten Console Port Program

Snakey Linux now tracks ten independent console ports. A shared distribution identity does **not** mean a shared kernel, boot chain, root filesystem or graphics stack.

## Official platform matrix

| Platform | CPU architecture | Engineering lane | First milestone |
|---|---|---|---|
| PSP | MIPS Allegrex (MIPS little-endian) | Feasibility research | Establish whether a maintained Linux kernel/platform port exists |
| PS Vita | ARMv7 Cortex-A9 | Pinned upstream reproduction | Reproduce Vita Linux Next build in hosted CI |
| PS3 | PowerPC64 big-endian PPE | Mainline/platform research | Audit PS3 kernel config, memory and boot prerequisites |
| PS4 | x86-64 AMD Jaguar | **Priority 1** | Audit Linux psX source and exact kernel build contract |
| PS5 | x86-64 AMD Zen 2 | **Priority 2** | Audit patch set and exact upstream kernel base |
| Xbox Original | i686 x86 | Historical research | Identify maintained/reproducible source and driver status |
| Wii | PowerPC32 big-endian | Historical research | Identify source tree and realistic shell-only target |
| Wii U | PowerPC32 big-endian | Independent research | Identify a verifiable platform port; never assume Wii compatibility |
| Nintendo Switch | AArch64 Tegra X1 | **Priority 3** | Audit L4T kernel, device tree, graphics and input support |
| Nintendo Switch 2 | AArch64 (SoC-specific) | Feasibility research | Identify public kernel/platform enablement evidence before any build |

The machine-readable source of truth is [platforms/linux-targets.json](../platforms/linux-targets.json). Upstream source provenance is tracked separately in [linux-port-sources.json](../platforms/linux-port-sources.json).

## Build lanes and acceptance gates

1. **Source audit:** identify the upstream project, exact source repository, full commit SHA, kernel base, submodules, toolchain, build command and license.
2. **Host build:** reproduce an upstream build in GitHub Actions. Save logs, config, source provenance and SHA-256 checksums.
3. **Snakey kernel integration:** only after the upstream build is understood; do not relabel an upstream kernel as an original Snakey kernel.
4. **Root filesystem:** select architecture/ABI and build a minimal userspace; keep kernel modules matched to the exact kernel.
5. **Kernel boot:** record independent evidence for a specific hardware model and configuration.
6. **Userspace and drivers:** validate storage, display, input, audio and network separately.
7. **Desktop:** add a graphical session only when memory and drivers justify it. XFCE is not a universal requirement and is unrealistic on some legacy systems.

Status vocabulary: `source-audit-required`, `source-pinned`, `kernel-buildable`, `kernel-built`, `kernel-boots`, `userspace-boots`, `desktop-tested`, `hardware-verified`.

A CI metadata pass is not a kernel build. A kernel build is not a boot. An emulator result is not physical-hardware evidence.

## GitHub Actions

- `.github/workflows/linux-platform-matrix.yml` validates all ten platform records, architecture mappings, source provenance and repository tests.
- `.github/workflows/console-linux-research.yml` retains the existing pinned Vita upstream build.
- PS4, PS5 and Switch build jobs are intentionally blocked until their upstream source audits and exact revision pins are complete. The manifest must never contain guessed SHAs or invented source repositories.

## Development boundaries

CI performs repository validation and host-side builds only. It does not modify console firmware, execute exploits, deploy boot payloads, or write to physical consoles. Hardware boot validation must be performed and documented separately by an appropriately supported test setup.

## Current verified Snakey state

- Ten requested platforms are registered in the machine-readable matrix.
- Vita has a pinned upstream reproduction workflow.
- PS4, PS5 and Switch have identified research references but remain unpinned.
- PSP, Wii U, Xbox Original and Switch 2 remain source-discovery/feasibility work.
- No Snakey console kernel or physical console boot is claimed by this milestone.
