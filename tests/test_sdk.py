import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stderr
import io

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("snakey_cli", ROOT / "tools" / "snakey.py")
snakey = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(snakey)


class SnakeySdkTests(unittest.TestCase):
    def test_registry_has_unique_targets(self):
        targets = snakey.load_targets()
        self.assertGreaterEqual(len(targets), 6)
        self.assertEqual(len(targets), len(set(targets)))

    def test_create_and_validate_gameboy_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            args = type("Args", (), {"directory": project, "target": "game-boy", "name": "Demo"})()
            self.assertEqual(snakey.command_new(args), 0)
            manifest = json.loads((project / snakey.MANIFEST).read_text())
            self.assertEqual(manifest["target"], "game-boy")
            self.assertEqual(snakey.command_validate(
                type("Args", (), {"directory": project})()
            ), 0)

    def test_every_target_boot_method_is_registered(self):
        methods = snakey.load_boot_methods()
        for target in snakey.load_targets().values():
            self.assertTrue(target["boot_methods"])
            for method in target["boot_methods"]:
                self.assertIn(method, methods)

    def test_gameboy_has_emulator_and_flashcart_sd(self):
        methods = snakey.load_targets()["game-boy"]["boot_methods"]
        self.assertIn("emulator-file", methods)
        self.assertIn("flashcart-sd", methods)
        self.assertNotIn("linux-boot-media", methods)

    def test_boot_plan_rejects_unsupported_method(self):
        args = type("Args", (), {"target": "game-boy", "method": "homebrew-loader"})()
        with redirect_stderr(io.StringIO()):
            self.assertEqual(snakey.command_boot_plan(args), 2)

    def test_create_nes_nrom_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "nes-demo"
            args = type("Args", (), {
                "directory": project, "target": "nes", "name": "SnakeyNES"
            })()
            self.assertEqual(snakey.command_new(args), 0)
            manifest = json.loads((project / snakey.MANIFEST).read_text())
            self.assertEqual(manifest["entry"], "src/main.s")
            self.assertTrue((project / "cfg/nes.cfg").is_file())
            source = (project / "src/main.s").read_text()
            self.assertIn('.byte "NES", $1A', source)
            self.assertIn('.segment "VECTORS"', source)
            self.assertIn('SNAKEY title.', source)
            self.assertIn('sta $2007', source)
            self.assertIn('Tiles 1..6 spell SNAKEY', source)
            self.assertIn('ReadController:', source)
            self.assertIn('HandleMenu:', source)
            self.assertIn('A opens the selected page.', source)
            self.assertIn('B returns from a page to the main menu.', source)
            self.assertIn('DrawPage:', source)
            self.assertIn('UpdateCursor:', source)
            self.assertIn('ControllerMasks:', source)
            self.assertIn('PageTextLo:', source)
            self.assertIn('CART page reports status as unknown', source)
            self.assertEqual(snakey.command_validate(
                type("Args", (), {"directory": project})()
            ), 0)

    def test_refuses_unknown_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = type("Args", (), {"directory": Path(tmp) / "demo",
                                     "target": "unknown", "name": "Demo"})()
            self.assertEqual(snakey.command_new(args), 2)


if __name__ == "__main__":
    unittest.main()
