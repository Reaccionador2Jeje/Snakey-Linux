import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
LINUX = ROOT / "linux"
SCRIPT = LINUX / "rootcopy/usr/bin/snakey-controller-center"
SPEC = importlib.util.spec_from_file_location("snakey_controller_center", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class ControllerCenterTests(unittest.TestCase):
    def test_default_profile_has_configurable_actions(self):
        self.assertEqual(MODULE.DEFAULT["device"], "auto")
        self.assertEqual(MODULE.DEFAULT["deadzone"], 16000)
        self.assertEqual(MODULE.DEFAULT["keyboard_button"], 3)
        self.assertEqual(MODULE.DEFAULT["buttons"]["0"], "Return")

    def test_controller_center_launcher_exists(self):
        launcher = LINUX / "rootcopy/usr/share/applications/snakey-controller-center.desktop"
        self.assertTrue(launcher.is_file())
        self.assertIn("snakey-controller-center", launcher.read_text())

    def test_desktop_shortcut_exists(self):\n        shortcut = LINUX / "rootcopy/etc/skel/Desktop/Snakey-Controller-Center.desktop"\n        self.assertTrue(shortcut.is_file())\n        self.assertIn("snakey-controller-center", shortcut.read_text())\n\n    def test_gamepad_reads_saved_profile(self):
        gamepad = (LINUX / "rootcopy/usr/bin/snakey-gamepad").read_text()
        self.assertIn("load_profile()", gamepad)
        self.assertIn("gamepad.json", gamepad)
        self.assertIn("configured_device", gamepad)

if __name__ == "__main__":
    unittest.main()
