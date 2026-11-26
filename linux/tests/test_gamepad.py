import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "linux/rootcopy/usr/bin/snakey-gamepad"
SPEC = importlib.util.spec_from_file_location("snakey_gamepad", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class GamepadMappingTests(unittest.TestCase):
    def test_axis_deadzone(self):
        self.assertIsNone(MODULE.key_for_axis(0, 15999))
        self.assertIsNone(MODULE.key_for_axis(1, -16000))

    def test_horizontal_and_vertical_navigation(self):
        self.assertEqual(MODULE.key_for_axis(0, 20000), "Right")
        self.assertEqual(MODULE.key_for_axis(0, -20000), "Left")
        self.assertEqual(MODULE.key_for_axis(1, 20000), "Down")
        self.assertEqual(MODULE.key_for_axis(1, -20000), "Up")

    def test_unsupported_axis_is_ignored(self):
        self.assertIsNone(MODULE.key_for_axis(3, 30000))

    def test_autostart_and_launcher_exist(self):
        self.assertTrue((ROOT / "linux/rootcopy/etc/xdg/autostart/snakey-gamepad.desktop").is_file())
        self.assertTrue((ROOT / "linux/rootcopy/usr/share/applications/snakey-virtual-keyboard.desktop").is_file())

if __name__ == "__main__":
    unittest.main()
