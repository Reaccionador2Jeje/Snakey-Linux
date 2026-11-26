# Snakey Slackware console root filesystems

This directory assembles **Slackware package archives** into target-specific
root filesystem staging trees for conventional MMU Linux ports. PSP is a
separate MIPSel no-MMU/uClinux adaptation and is not yet handled by this
standard `.txz` rootfs builder. It does not replace Slackware with Buildroot,
Debian, Alpine or a BusyBox-only image.

## Build lanes

| Target | Package source | ABI | Status |
|---|---|---|---|
| Vita | Slackware ARM 15.0 package mirror | ARMv7 hard-float | Legacy upstream package baseline |
| Original Xbox | Slackware 15.0 x86 package mirror | i686-compatible 32-bit x86 | Minimal subset; ABI still to validate |
| Wii | Locally built Slackware-compatible PowerPC packages | PPC32 big-endian | Port required; no official Slackware tree |
| PS3 | Locally built Slackware-compatible package set | PPC64 big-endian | Bootstrap manifest added; package availability/ABI audit required |
| PSP | Separate Slackware-style no-MMU adaptation | MIPSel / uClinux ABI | Toolchain and package ABI audit required; not handled by this builder |

## Assemble a rootfs

Use a Linux host with Bash, Python 3 and GNU tar. Download/prepare the
architecture-correct Slackware `.txz` package archives separately. The
builder accepts a directory containing those archives and extracts only the
packages named in the selected manifest.

```sh
SNAKEY_PACKAGE_DIR=/path/to/slackware-packages \
  linux/rootfs/build-slackware-rootfs.sh vita dist/rootfs-vita
```

For Xbox use `xbox`; for Wii use `wii`; for PS3 use `ps3`. The PS3 package directory must contain only mutually compatible **PowerPC64 big-endian** (`ppc64`) Slackware-compatible `.txz` archives. Do not use Wii PPC32 packages or ordinary x86_64 Slackware packages. The PS3 manifest is a candidate bootstrap contract, not evidence that an official Slackware PPC64 package tree exists. The Wii package directory must
contain packages built for big-endian PowerPC; x86 or ARM packages are rejected
by the package manifest convention and must never be mixed.

The builder:
- requires every manifest package to be present exactly once;
- rejects unsafe archive paths before extraction;
- stages package payloads under the target root;
- records Slackware package descriptions in `/var/log/packages`;
- preserves package `doinst.sh` scripts under
  `/var/log/scripts` for controlled execution on the target;
- writes a build manifest and SHA-256 checksums.

It does **not** execute package install scripts on the build host, run foreign
architecture binaries, create a bootable disk image, or claim a bootable
console system. First boot still needs target-specific kernel, device nodes,
mount setup, init configuration, libraries, firmware and input/display drivers.

## Package selection

The three `*.packages` files are deliberately small bootstrap selections,
not complete Slackware installations. Package names are matched by the
Slackware package-name prefix, independent of the version/build suffix. If an
upstream package name differs, update the manifest only after verifying it
against the selected architecture's official/community package tree.

## Next validation gates

1. Verify each manifest against the exact package mirror and architecture.
2. Assemble the rootfs and inspect its ELF interpreter and shared libraries.
3. For PS3, build/audit every package for the same PPC64 big-endian ABI and verify ELF class, endianness, machine, dynamic interpreter and library closure before treating the rootfs as usable.\n4. Add target-specific kernel modules, firmware and device configuration.
4. Boot to a serial/console shell before starting Snakey Desktop.
5. Add Snakey Desktop only after the base userspace is stable.

## PSP exception

The PSP target must not consume ordinary Slackware MIPS/glibc binaries. Its historical no-MMU/uClinux execution model requires a separately audited toolchain, libc/ABI, kernel and package format. The Snakey goal is to retain Slackware package conventions and management semantics where they can be ported, not to claim an official or binary-compatible Slackware PSP release. A PSP rootfs builder will be added only after that ABI is specified and validated.

## Desktop policy

XFCE4 is the target desktop on all Linux console ports except PSP. PSP uses the native Snakey micro desktop. Xbox Original and Wii retain XFCE4 as experimental targets; their low memory budgets mean a successful build and runtime memory/driver measurements are mandatory before any image can claim XFCE4 support.

## Console desktop package contracts

The per-console desktop intent and package groups are recorded in
[`desktop-profiles.json`](desktop-profiles.json). It defines shared XFCE4
groups (desktop, X11/graphics/input, fonts) for Vita, PS3, PS4, PS5, Xbox
Original, Wii, Wii U, Switch and Switch 2. PSP is deliberately excluded from
XFCE4 and uses a separate Snakey native micro desktop target.

These are **package-selection contracts**, not downloaded or built package
sets. Package names and dependencies must be checked against the exact
architecture-specific Slackware tree (or rebuilt port) before assembly. In
particular, Xbox Original (64 MiB) and Wii (88 MiB) remain experimental: a
successful package build is not enough; runtime memory, graphics and input
must be measured. No console rootfs currently claims to contain a working
XFCE4 session.

Validate the contract with:

```sh
python3 tools/validate_desktop_profiles.py
```

The console matrix workflow runs this validator on pushes and pull requests.
The runtime contract uses `xfce4-session` with no display manager by default
and preserves a TTY fallback if X or XFCE fails.
