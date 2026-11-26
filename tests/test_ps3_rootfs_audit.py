#!/usr/bin/env python3
"""Unit tests for the PS3 PPC64 rootfs ELF architecture audit."""
from __future__ import annotations

import pathlib
import struct
import tempfile
import unittest

from audit_ps3_rootfs import audit, inspect_header


def elf_header(elf_class: int = 2, encoding: int = 2, machine: int = 21) -> bytes:
    data = bytearray(64)
    data[:4] = b"\x7fELF"
    data[4] = elf_class
    data[5] = encoding
    data[6] = 1
    data[16:18] = struct.pack(">H", 2)
    data[18:20] = struct.pack(">H", machine)
    return bytes(data)


class PS3RootfsAuditTests(unittest.TestCase):
    def test_accepts_ppc64_big_endian(self):
        self.assertEqual(inspect_header(elf_header()), (2, 2, 21))

    def test_rejects_ppc32(self):
        with self.assertRaisesRegex(ValueError, "ELFCLASS32"):
            inspect_header(elf_header(elf_class=1))

    def test_rejects_little_endian(self):
        with self.assertRaisesRegex(ValueError, "big-endian"):
            inspect_header(elf_header(encoding=1))

    def test_rejects_non_ppc64(self):
        with self.assertRaisesRegex(ValueError, "EM_PPC64"):
            inspect_header(elf_header(machine=3))

    def test_rootfs_scan_requires_elf_and_checks_every_elf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "good").write_bytes(elf_header())
            (root / "text-file").write_text("not an ELF")
            self.assertEqual(audit(root), 1)
            (root / "bad").write_bytes(elf_header(machine=3))
            with self.assertRaisesRegex(ValueError, "bad"):
                audit(root)


if __name__ == "__main__":
    unittest.main()
