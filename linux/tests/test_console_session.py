import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "rootcopy/usr/bin/snakey-console-session"
AUTOSTART = ROOT / "rootcopy/etc/xdg/autostart/snakey-big-picture.desktop"
DESKTOP = ROOT / "rootcopy/usr/share/applications/snakey-console-session.desktop"

class ConsoleSessionTests(unittest.TestCase):
    def test_session_script_has_explicit_lifecycle_commands(self):
        source = SCRIPT.read_text()
        for command in ("start)", "stop)", "restart)", "status)", "autostart-check)", "autostart-on)", "autostart-off)"):
            self.assertIn(command, source)

    def test_autostart_is_opt_in(self):
        entry = AUTOSTART.read_text()
        manager = SCRIPT.read_text()
        self.assertIn("snakey-console-session autostart-check", entry)
        self.assertIn('AUTOSTART_FILE="$CONFIG_DIR/start-big-picture"', manager)
        self.assertIn('if [[ -e "$AUTOSTART_FILE" ]]; then start; fi', manager)

    def test_session_has_application_menu_entry(self):
        source = DESKTOP.read_text()
        self.assertIn("Name=Snakey Console Session", source)
        self.assertIn("snakey-console-session", source)

    def test_snakeys_xfce_panel_defaults_are_present(self):
        import xml.etree.ElementTree as ET
        panel = ROOT / "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
        tree = ET.parse(panel)
        channel = tree.getroot()
        self.assertEqual(channel.attrib.get("name"), "xfce4-panel")
        text = panel.read_text()
        for plugin in ("applicationsmenu", "tasklist", "systray", "clock"):
            self.assertIn(plugin, text)
        self.assertIn('name="size" type="uint" value="36"', text)

if __name__ == "__main__":
    unittest.main()
