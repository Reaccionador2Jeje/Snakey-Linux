import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
LINUX = ROOT / "linux"

class ConsoleModeTests(unittest.TestCase):
    def test_console_mode_script_has_modes(self):
        script = (LINUX / "rootcopy/usr/bin/snakey-console-mode").read_text()
        for mode in ('on|enable', 'off|disable', 'toggle', 'status'):
            self.assertIn(mode, script)

    def test_tv_desktop_shortcuts_exist(self):
        desktop = LINUX / "rootcopy/etc/skel/Desktop"
        expected = [
            "Snakey-Console-Mode.desktop",
            "Snakey-Files.desktop",
            "Snakey-Terminal.desktop",
            "Snakey-Settings.desktop",
            "Snakey-Keyboard.desktop",
            "Snakey-Games.desktop",
        ]
        for name in expected:
            with self.subTest(name=name):
                self.assertTrue((desktop / name).is_file())

    def test_console_mode_is_executable_in_build_script(self):
        build = (LINUX / "build-live.sh").read_text()
        self.assertIn('chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-console-mode"', build)

if __name__ == "__main__":
    unittest.main()
