# Snakey Linux — Ten Console Port Program

Snakey Linux tracks ten independent console ports. Every Linux lane targets a **Slackware-compatible base** and the same product identity: **Snakey Console Desktop**, with XFCE4 as the standard desktop on hardware that can genuinely support it. A shared distribution identity does **not** mean a shared kernel, boot chain, root filesystem, package repository or graphics stack. Architectures without maintained official Slackware support require a separately maintained port/adaptation; we will not pretend an x86_64 Slackware package can run on MIPS, ARM or PowerPC.

## Official platform matrix

| Platform | CPU architecture | Engineering lane | First milestone |
|---|---|---|---|
| PSP | MIPS Allegrex (MIPS little-endian) | **Priority 1** | Audit historical uClinux 0.22 archives and toolchain |
| PS Vita | ARMv7 Cortex-A9 | **Priority 2** | Reproduce pinned Vita Linux Next kernel build in hosted CI |
| PS3 | PowerPC64 big-endian PPE | Mainline/platform research | Audit PS3 kernel config, memory and boot prerequisites |
| PS4 | x86-64 AMD Jaguar | Deferred | Audit Linux psX after first-wave handheld ports |
| PS5 | x86-64 AMD Zen 2 | Deferred | Audit patch set after first-wave handheld ports |
| Xbox Original | i686 x86 | Historical research | Identify maintained/reproducible source and driver status |
| Wii | PowerPC32 big-endian | Historical research | Identify source tree and realistic shell-only target |
| Wii U | PowerPC32 big-endian | Independent research | Identify a verifiable platform port; never assume Wii compatibility |
| Nintendo Switch | AArch64 Tegra X1 | Deferred | Audit L4T kernel after first-wave handheld ports |
| Nintendo Switch 2 | AArch64 (SoC-specific) | Feasibility research | Identify public kernel/platform enablement evidence before any build |

The machine-readable source of truth is [platforms/linux-targets.json](../platforms/linux-targets.json). Upstream source provenance is tracked separately in [linux-port-sources.json](../platforms/linux-port-sources.json).

## Build lanes and acceptance gates

1. **Source audit:** identify the upstream project, exact source repository, full commit SHA, kernel base, submodules, toolchain, build command and license.
2. **Host build:** reproduce an upstream build in GitHub Actions. Save logs, config, source provenance and SHA-256 checksums.
3. **Snakey kernel integration:** only after the upstream build is understood; do not relabel an upstream kernel as an original Snakey kernel.
4. **Root filesystem:** select architecture/ABI and build a minimal userspace; keep kernel modules matched to the exact kernel.
5. **Kernel boot:** record independent evidence for a specific hardware model and configuration.
6. **Userspace and drivers:** validate storage, display, input, audio and network separately.
7. **Desktop:** integrate Snakey Console Desktop (XFCE4) where memory, MMU, display, GPU and input drivers justify it. PSP, Original Xbox and Wii are classified for a minimal Snakey native console UI instead; forcing XFCE4 onto those memory-constrained systems would be misleading. Vita is experimental; PS3 is conditional; the remaining capable platforms keep XFCE4 as the target after their ports are proven.

Status vocabulary: `source-audit-required`, `source-pinned`, `kernel-buildable`, `kernel-built`, `kernel-boots`, `userspace-boots`, `desktop-tested`, `hardware-verified`.

A CI metadata pass is not a kernel build. A kernel build is not a boot. An emulator result is not physical-hardware evidence.

## Slackware base + Snakey Console Desktop

The package/userland goal is a Slackware-compatible system per CPU architecture, with architecture-specific package builds and kernel modules matched to each console kernel. The desktop goal is one recognizable XFCE4-based Snakey Console Desktop, including controller-first launcher integration. XFCE4 is not forced onto hardware that cannot reasonably run it: those ports receive a small native Snakey console interface while retaining the same branding and application concepts.

The matrix records `distribution_base`, `distribution_strategy`, `console_desktop` and `xfce4_status` for each console. `planned` is a target, not a build or boot claim; only evidence gates can advance it.

## First-wave focus: PSP + PS Vita

The active order is PSP first, then PS Vita. PSP starts with integrity-only auditing of archived uClinux source bundles because the historical port is not a maintained modern kernel tree. Vita starts with a pinned ARMv7 upstream build. See [psp-vita-first-wave.md](psp-vita-first-wave.md).

## GitHub Actions

- `.github/workflows/linux-platform-matrix.yml` validates all ten platform records, architecture mappings, source provenance and repository tests.
- `.github/workflows/console-linux-research.yml` retains the existing pinned Vita upstream build.
- PS4, PS5 and Switch build jobs are intentionally blocked until their upstream source audits and exact revision pins are complete. The manifest must never contain guessed SHAs or invented source repositories.

## Development boundaries

CI performs repository validation and host-side builds only. It does not modify console firmware, execute exploits, deploy boot payloads, or write to physical consoles. Hardware boot validation must be performed and documented separately by an appropriately supported test setup.

## Current verified Snakey state

- Ten requested platforms are registered in the machine-readable matrix, each with a Slackware-compatible base target and a Snakey Console Desktop policy.
- Vita has a pinned upstream reproduction workflow.
- PS4, PS5 and Switch have identified research references but remain unpinned.
- PSP has a documented historical uClinux 0.22 archive-audit lane; no Snakey kernel build is claimed.
- PS Vita has a pinned upstream kernel reproduction lane; no Snakey kernel or hardware boot is claimed.
- PS4, PS5, Switch and other platforms are deferred while PSP and Vita are first-wave targets.
- XFCE4 is the standard desktop target where hardware permits; PSP, Original Xbox and Wii are explicitly minimal-UI targets, Vita is experimental, and PS3 is conditional.
- No Snakey console kernel or physical console boot is claimed by this milestone.
