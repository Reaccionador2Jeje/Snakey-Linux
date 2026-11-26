import tempfile
import unittest
from pathlib import Path
from tools.native_roms import build_snes, build_gba, build_nds

class NativeRomTests(unittest.TestCase):
    def test_snes_lorom_image_and_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "test.sfc"
            build_snes(out, "Snakey")
            data = out.read_bytes()
            self.assertEqual(len(data), 0x8000)
            self.assertEqual(data[0x7FC0:0x7FC6], b"SNAKEY")
            self.assertEqual(data[0x7FFC:0x7FFE], b"\x00\x80")

    def test_gba_header_and_entry_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "test.gba"
            build_gba(out, "Snakey")
            data = out.read_bytes()
            self.assertEqual(len(data), 0x8000)
            self.assertEqual(data[0xAC:0xB0], b"SNKY")
            self.assertEqual(data[0xB2], 0x96)\n            self.assertEqual((sum(data[0xA0:0xBD]) + data[0xBD] + 0x19) & 0xFF, 0)
            self.assertEqual(data[0xC0:0xC4], b"\x30\x00\x9f\xe5")

    def test_nds_header_offsets_and_crcs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "test.nds"
            build_nds(out, "Snakey")
            data = out.read_bytes()
            self.assertEqual(len(data), 0x10000)
            self.assertEqual(data[12:16], b"SNKY")
            self.assertEqual(int.from_bytes(data[0x20:0x24], "little"), 0x4000)
            self.assertEqual(int.from_bytes(data[0x80:0x84], "little"), len(data))
            self.assertEqual(int.from_bytes(data[0x15E:0x160], "little"),
                             __import__("tools.native_roms", fromlist=["_crc16"])._crc16(data[:0x15E]))

if __name__ == "__main__":
    unittest.main()
