import importlib.machinery
import importlib.util
import pathlib
import struct
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "linux/rootcopy/usr/bin/snakey-big-picture"
LOADER = importlib.machinery.SourceFileLoader("snakey_big_picture", str(SCRIPT))
SPEC = importlib.util.spec_from_loader("snakey_big_picture", LOADER)
MODULE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(MODULE)


def event(value, kind, number):
    return struct.pack("IhBB", 0, value, kind, number)


class BigPictureControllerTests(unittest.TestCase):
    def test_south_button_confirms(self):
        self.assertEqual(MODULE.decode_gamepad_event(event(1, 1, 0), 2, 8), (2, "confirm"))

    def test_east_button_goes_back(self):
        self.assertEqual(MODULE.decode_gamepad_event(event(1, 1, 1), 2, 8), (2, "back"))

    def test_dpad_wraps_selection(self):
        self.assertEqual(MODULE.decode_gamepad_event(event(1, 1, 5), 7, 8), (0, None))
        self.assertEqual(MODULE.decode_gamepad_event(event(1, 1, 4), 0, 8), (7, None))

    def test_vertical_axis_moves_selection(self):
        self.assertEqual(MODULE.decode_gamepad_event(event(-20000, 2, 1), 3, 8), (2, None))
        self.assertEqual(MODULE.decode_gamepad_event(event(20000, 2, 1), 3, 8), (4, None))

    def test_deadzone_ignores_small_axis_motion(self):
        self.assertEqual(MODULE.decode_gamepad_event(event(1000, 2, 1), 3, 8), (3, None))

    def test_init_flag_is_ignored_for_button_events(self):
        self.assertEqual(MODULE.decode_gamepad_event(event(1, 0x81, 0), 0, 8), (0, "confirm"))


if __name__ == "__main__":
    unittest.main()
