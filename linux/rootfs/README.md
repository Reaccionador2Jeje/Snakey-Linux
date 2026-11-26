# Snakey Slackware console root filesystems

This directory assembles **Slackware package archives** into target-specific
root filesystem staging trees. It does not replace Slackware with Buildroot,
Debian, Alpine or a BusyBox-only image.

## Build lanes

| Target | Package source | ABI | Status |
|---|---|---|---|
| Vita | Slackware ARM 15.0 package mirror | ARMv7 hard-float | Legacy upstream package baseline |
| Original Xbox | Slackware 15.0 x86 package mirror | i686-compatible 32-bit x86 | Minimal subset; ABI still to validate |
| Wii | Locally built Slackware-compatible PowerPC packages | PPC32 big-endian | Port required; no official Slackware tree |

## Assemble a rootfs

Use a Linux host with Bash, Python 3 and GNU tar. Download/prepare the
architecture-correct Slackware `.txz` package archives separately. The
builder accepts a directory containing those archives and extracts only the
packages named in the selected manifest.

```sh
SNAKEY_PACKAGE_DIR=/path/to/slackware-packages \
  linux/rootfs/build-slackware-rootfs.sh vita dist/rootfs-vita
```

For Xbox use `xbox`; for Wii use `wii`. The Wii package directory must
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
3. Add target-specific kernel modules, firmware and device configuration.
4. Boot to a serial/console shell before starting Snakey Desktop.
5. Add Snakey Desktop only after the base userspace is stable.
