import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

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
            args = type("Args", (), {
                "directory": project, "target": "game-boy", "name": "Demo"
            })()
            self.assertEqual(snakey.command_new(args), 0)
            manifest = json.loads((project / snakey.MANIFEST).read_text())
            self.assertEqual(manifest["target"], "game-boy")
            self.assertEqual(snakey.command_validate(
                type("Args", (), {"directory": project})()
            ), 0)

    def test_refuses_unknown_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = type("Args", (), {
                "directory": Path(tmp) / "demo", "target": "unknown", "name": "Demo"
            })()
            self.assertEqual(snakey.command_new(args), 2)


if __name__ == "__main__":
    unittest.main()
