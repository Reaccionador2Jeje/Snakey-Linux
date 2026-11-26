#!/usr/bin/env python3
"""Audit ELF architecture consistency for a staged Snakey PS3 rootfs."""
from __future__ import annotations

import argparse
import pathlib
import struct
import sys

ELF_MAGIC = b"\x7fELF"
EM_PPC64 = 21


def inspect_header(data: bytes) -> tuple[int, int, int]:
    if len(data) < 20 or data[:4] != ELF_MAGIC:
        raise ValueError("not a valid ELF header")
    elf_class, encoding = data[4], data[5]
    if elf_class != 2:
        raise ValueError(f"ELFCLASS{32 if elf_class == 1 else elf_class}: expected ELFCLASS64")
    if encoding != 2:
        raise ValueError("ELF is not big-endian")
    machine = struct.unpack(">H", data[18:20])[0]
    if machine != EM_PPC64:
        raise ValueError(f"e_machine={machine}: expected EM_PPC64 (21)")
    return elf_class, encoding, machine


def audit(root: pathlib.Path) -> int:
    if not root.is_dir():
        raise ValueError(f"rootfs directory does not exist: {root}")
    scanned = 0
    failures: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            with path.open("rb") as stream:
                head = stream.read(64)
            if head[:4] != ELF_MAGIC:
                continue
            inspect_header(head)
            scanned += 1
        except (OSError, ValueError) as exc:
            failures.append(f"{path.relative_to(root)}: {exc}")
    if failures:
        raise ValueError("ELF architecture audit failed:\n" + "\n".join(failures))
    if scanned == 0:
        raise ValueError("no ELF files found; refusing to treat an empty/non-binary tree as audited")
    print(f"PS3 rootfs ELF audit: OK ({scanned} ELF files; ELF64 big-endian PowerPC)")
    return scanned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rootfs", type=pathlib.Path)
    args = parser.parse_args()
    try:
        audit(args.rootfs)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
