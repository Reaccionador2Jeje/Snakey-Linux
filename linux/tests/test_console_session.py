import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "rootcopy/usr/bin/snakey-console-session"
AUTOSTART = ROOT / "rootcopy/etc/xdg/autostart/snakey-big-picture.desktop"
DESKTOP = ROOT / "rootcopy/usr/share/applications/snakey-console-session.desktop"

class ConsoleSessionTests(unittest.TestCase):
    def test_session_script_has_explicit_lifecycle_commands(self):
        source = SCRIPT.read_text()
        for command in ("start)", "stop)", "restart)", "status)", "autostart-on)", "autostart-off)"):
            self.assertIn(command, source)

    def test_autostart_is_opt_in(self):
        source = AUTOSTART.read_text()
        self.assertIn('autostart-check', source)
        self.assertIn('start-big-picture', source)
        self.assertIn("snakey-console-session autostart-check", source)

    def test_session_has_application_menu_entry(self):
        source = DESKTOP.read_text()
        self.assertIn("Name=Snakey Console Session", source)
        self.assertIn("snakey-console-session", source)

if __name__ == "__main__":
    unittest.main()
