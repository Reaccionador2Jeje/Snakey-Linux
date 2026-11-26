import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from desktop.core.runtime import APP_IDS, DesktopState, step


class DesktopRuntimeTests(unittest.TestCase):
    def test_launcher_opens_each_registered_app(self):
        for index, app_id in enumerate(APP_IDS):
            state = DesktopState()
            for _ in range(index):
                state = step(state, "down")
            state = step(state, "confirm")
            self.assertEqual(state.screen, app_id)

    def test_launcher_selection_wraps(self):
        state = step(DesktopState(), "up")
        self.assertEqual(state.selection, len(APP_IDS) - 1)
        state = step(state, "down")
        self.assertEqual(state.selection, 0)

    def test_back_returns_from_every_app(self):
        for app_id in APP_IDS:
            state = DesktopState(screen=app_id)
            self.assertEqual(step(state, "back").screen, "launcher")

    def test_files_catalog_is_read_only_and_selectable(self):
        state = DesktopState(screen="files")
        state = step(state, "confirm")
        self.assertEqual(state.file_detail, "README.TXT")
        self.assertEqual(step(state, "back").screen, "launcher")

    def test_console_commands_have_real_state_effects(self):
        state = DesktopState(screen="console")
        state = step(state, "confirm")
        self.assertEqual(state.console_output, "HELP  ABOUT  CLEAR")
        state = step(state, "down")
        state = step(state, "confirm")
        self.assertEqual(state.console_output, "SNAKEY DESKTOP - NATIVE HOMEBREW")
        state = step(state, "down")
        state = step(state, "confirm")
        self.assertEqual(state.console_output, "")

    def test_settings_toggle_palette(self):
        state = DesktopState(screen="settings")
        state = step(state, "confirm")
        self.assertEqual(state.palette, 1)
        state = step(state, "confirm")
        self.assertEqual(state.palette, 0)

    def test_unknown_inputs_are_ignored(self):
        state = DesktopState()
        self.assertEqual(step(state, "start"), state)


if __name__ == "__main__":
    unittest.main()
