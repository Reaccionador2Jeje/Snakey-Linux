import tempfile
import unittest
from pathlib import Path
from tools.native_roms import _crc16, build_gba, build_nds, build_snes


class NativeRomTests(unittest.TestCase):
    def test_snes_lorom_image_and_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "test.sfc"
            build_snes(out, "Snakey")
            data = out.read_bytes()
            self.assertEqual(len(data), 0x8000)
            self.assertEqual(data[0x7FC0:0x7FC6], b"SNAKEY")
            self.assertEqual(data[0x7FFC:0x7FFE], bytes([0x00, 0x80]))
            complement = int.from_bytes(data[0x7FDC:0x7FDE], "little")
            checksum = int.from_bytes(data[0x7FDE:0x7FE0], "little")
            self.assertEqual(complement ^ checksum, 0xFFFF)

    def test_gba_header_and_entry_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "test.gba"
            build_gba(out, "Snakey")
            data = out.read_bytes()
            self.assertEqual(len(data), 0x8000)
            self.assertEqual(data[0xAC:0xB0], b"SNKY")
            self.assertEqual(data[0xB2], 0x96)
            self.assertEqual((sum(data[0xA0:0xBD]) + data[0xBD] + 0x19) & 0xFF, 0)
            self.assertEqual(data[0xC0:0xC4], bytes([0x34, 0x00, 0x9F, 0xE5]))
            # Mode-3 framebuffer writer now advances through RGB555 colours.
            self.assertEqual(int.from_bytes(data[0xC0 + 9 * 4:0xC0 + 10 * 4], "little"), 0xE2844001)

    def test_nds_header_offsets_and_crcs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "test.nds"
            build_nds(out, "Snakey")
            data = out.read_bytes()
            self.assertEqual(len(data), 0x10000)
            self.assertEqual(data[12:16], b"SNKY")
            self.assertEqual(int.from_bytes(data[0x20:0x24], "little"), 0x4000)
            self.assertEqual(int.from_bytes(data[0x80:0x84], "little"), len(data))
            self.assertEqual(int.from_bytes(data[0x15E:0x160], "little"), _crc16(data[:0x15E]))
            arm9 = [int.from_bytes(data[i:i+4], "little") for i in range(0x4000, 0x4000 + 20 * 4, 4)]
            self.assertEqual(arm9[0], 0xE59F0034)  # DISPCNT literal load
            self.assertEqual(arm9[1], 0xE59F1034)  # bitmap mode 5 + BG2
            self.assertEqual(arm9[4], 0xE3A01081)  # VRAM A -> main BG
            self.assertEqual(arm9[9], 0xE1C040B0)  # RGB555 pixel write


if __name__ == "__main__":
    unittest.main()
