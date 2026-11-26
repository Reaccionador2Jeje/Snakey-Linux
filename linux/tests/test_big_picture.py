import importlib.util
import pathlib
import unittest
from importlib.machinery import SourceFileLoader

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "linux/rootcopy/usr/bin/snakey-big-picture"
LOADER = SourceFileLoader("snakey_big_picture", str(SCRIPT))
SPEC = importlib.util.spec_from_loader("snakey_big_picture", LOADER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class BigPictureTests(unittest.TestCase):
    def test_menu_contains_expected_destinations(self):
        labels = [item[0] for item in MODULE.ITEMS]
        for label in ("Games", "Applications", "Files", "Terminal", "Controller Center", "Settings"):
            self.assertIn(label, labels)

    def test_desktop_and_application_launchers_exist(self):
        for path in (
            ROOT / "linux/rootcopy/usr/share/applications/snakey-big-picture.desktop",
            ROOT / "linux/rootcopy/etc/skel/Desktop/Snakey-Big-Picture.desktop",
        ):
            self.assertTrue(path.is_file())
            self.assertIn("snakey-big-picture", path.read_text())

if __name__ == "__main__":
    unittest.main()
