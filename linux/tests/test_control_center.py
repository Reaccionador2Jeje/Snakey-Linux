import importlib.util
import pathlib
import unittest
from importlib.machinery import SourceFileLoader

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ROOT / "linux/packages/snakey-control-center/usr/bin/snakey-control-center"
LOADER = SourceFileLoader("snakey_control_center", str(SOURCE))
SPEC = importlib.util.spec_from_loader("snakey_control_center", LOADER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ControlCenterTests(unittest.TestCase):
    def test_system_summary_has_core_snake_identity(self):
        summary = MODULE.system_summary()
        joined = "\n".join(summary)
        self.assertIn("Slackware 15.0", joined)
        self.assertIn("XFCE4", joined)
        self.assertIn("pkgtools", joined)

    def test_menu_exposes_core_sections(self):
        actions = {action for _label, action in MODULE.MENU}
        self.assertTrue({"overview", "settings", "display", "appearance",
                         "network", "packages", "controller", "about", "exit"} <= actions)

    def test_native_package_assets_exist(self):
        self.assertTrue((ROOT / "linux/packages/snakey-control-center/slack-desc").is_file())
        self.assertTrue((ROOT / "linux/packages/snakey-control-center/usr/share/applications/snakey-control-center.desktop").is_file())
        self.assertTrue((ROOT / "linux/packages/snakey-control-center/etc/skel/Desktop/Snakey-Control-Center.desktop").is_file())


if __name__ == "__main__":
    unittest.main()
