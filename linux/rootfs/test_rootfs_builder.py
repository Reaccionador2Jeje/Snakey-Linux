#!/usr/bin/env python3
"""Smoke-test Slackware rootfs assembly using synthetic .txz packages."""
from __future__ import annotations

import lzma
import os
import pathlib
import subprocess
import tarfile
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILDER = ROOT / "linux/rootfs/build-slackware-rootfs.sh"
PACKAGES = ["aaa_base", "bash", "coreutils"]


def make_package(path: pathlib.Path, name: str) -> None:
    with tarfile.open(path, "w:xz") as tf:
        for rel, data, mode in (
            ("./usr/bin/" + name, b"synthetic-package-file\n", 0o755),
            ("./install/slack-desc", (name + ": synthetic test package\n").encode(), 0o644),
            ("./install/doinst.sh", b"#!/bin/sh\necho staged\n", 0o755),
        ):
            info = tarfile.TarInfo(rel)
            info.size = len(data)
            info.mode = mode
            import io
            tf.addfile(info, io.BytesIO(data))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="snakey-rootfs-test-") as tmp:
        base = pathlib.Path(tmp)
        pkgdir = base / "packages"
        pkgdir.mkdir()
        manifest = base / "test.packages"
        manifest.write_text("\n".join(PACKAGES) + "\n", encoding="utf-8")
        for name in PACKAGES:
            make_package(pkgdir / f"{name}-1-test-1.txz", name)

        for target in ("vita", "xbox", "wii", "ps3"):
            output = base / f"rootfs-{target}"
            env = os.environ.copy()
            env["SNAKEY_PACKAGE_DIR"] = str(pkgdir)
            env["SNAKEY_PACKAGE_MANIFEST"] = str(manifest)
            subprocess.run(
                ["bash", str(BUILDER), target, str(output)],
                check=True, env=env, cwd=ROOT,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            assert (output / "etc/snakey-release").is_file()
            assert (output / "usr/bin/aaa_base").is_file()
            assert (output / "var/log/packages/aaa_base-1-test-1").is_file()
            assert (output / "var/log/scripts/bash-1-test-1").is_file()
            assert (output / "var/log/snakey-rootfs-manifest.json").is_file()
            assert (output / "SHA256SUMS").is_file()
            stage = (output / "var/log/snakey-rootfs-stage.txt").read_text()
            assert "not a bootable root filesystem" in stage
    print("Slackware rootfs builder synthetic package tests: OK")


if __name__ == "__main__":
    main()
