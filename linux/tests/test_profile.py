import json
import pathlib
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
LINUX = ROOT / "linux"


class SnakeyLinuxProfileTests(unittest.TestCase):
    def test_profile_is_slackware_xfce_x86_64(self):
        profile = json.loads((LINUX / "profile.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["base"], "Slackware")
        self.assertEqual(profile["builder"], "liveslak")
        self.assertEqual(profile["architecture"], "x86_64")
        self.assertEqual(profile["desktop"], "XFCE")
        self.assertEqual(profile["runlevel"], 4)
        self.assertEqual(profile["compression"], "xz")
        self.assertEqual(profile["trim"], "bloat")

    def test_snake_identity_files_exist(self):
        paths = [
            "rootcopy/etc/os-release",
            "rootcopy/etc/issue",
            "rootcopy/etc/motd",
            "rootcopy/usr/share/backgrounds/snakey/snakey.svg",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((LINUX / path).is_file())

    def test_xfce_default_configuration_is_valid_xml(self):
        paths = [
            "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml",
            "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml",
            "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml",
            "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml",
        ]
        for path in paths:
            with self.subTest(path=path):
                ET.parse(LINUX / path)

    def test_snake_theme_is_complete_and_selected(self):
        theme = LINUX / "rootcopy/usr/share/themes/Snakey-Dark"
        required = ["index.theme", "gtk-2.0/gtkrc", "gtk-3.0/gtk.css"]
        for path in required:
            with self.subTest(path=path):
                self.assertTrue((theme / path).is_file())
        settings = ET.parse(
            LINUX / "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml"
        )
        values = [node.attrib.get("value") for node in settings.iter("property")]
        self.assertIn("Snakey-Dark", values)

    def test_panel_and_window_manager_defaults_are_valid(self):
        for path in (
            "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml",
            "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml",
        ):
            with self.subTest(path=path):
                ET.parse(LINUX / path)

    def test_wallpaper_configuration_points_to_bundled_asset(self):
        config = LINUX / "rootcopy/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml"
        tree = ET.parse(config)
        values = [node.attrib.get("value") for node in tree.iter("property")]
        wallpaper = "/usr/share/backgrounds/snakey/snakey.svg"
        self.assertIn(wallpaper, values)
        self.assertTrue((LINUX / "rootcopy" / wallpaper.lstrip("/")).is_file())


if __name__ == "__main__":
    unittest.main()
