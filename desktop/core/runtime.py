"""Platform-neutral Snakey Desktop state transitions.

This module is the executable reference model for native platform adapters.
It does not run on a console; each ROM adapter implements the same contract
using that console's CPU, graphics and input hardware.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

APP_IDS = ("files", "console", "settings", "about")
FILES = ("README.TXT", "SYSTEM.CFG", "LICENSE.TXT")
COMMANDS = ("HELP", "ABOUT", "CLEAR")
Screen = Literal["launcher", "files", "console", "settings", "about"]


@dataclass(frozen=True)
class DesktopState:
    screen: Screen = "launcher"
    selection: int = 0
    palette: int = 0
    console_output: str = "SNAKEY CONSOLE READY"
    file_detail: str | None = None


def _wrap(value: int, count: int) -> int:
    return value % count


def step(state: DesktopState, button: str) -> DesktopState:
    """Apply one newly-pressed logical button and return a new state."""
    button = button.lower()
    if button not in {"up", "down", "confirm", "back"}:
        return state

    if state.screen == "launcher":
        if button == "up":
            return replace(state, selection=_wrap(state.selection - 1, len(APP_IDS)))
        if button == "down":
            return replace(state, selection=_wrap(state.selection + 1, len(APP_IDS)))
        if button == "confirm":
            return replace(state, screen=APP_IDS[state.selection], selection=0,
                           file_detail=None)
        return state

    if button == "back":
        return replace(state, screen="launcher", selection=0, file_detail=None)

    if state.screen == "files":
        if button == "up":
            return replace(state, selection=_wrap(state.selection - 1, len(FILES)))
        if button == "down":
            return replace(state, selection=_wrap(state.selection + 1, len(FILES)))
        if button == "confirm":
            return replace(state, file_detail=FILES[state.selection])
        return state

    if state.screen == "console":
        if button == "up":
            return replace(state, selection=_wrap(state.selection - 1, len(COMMANDS)))
        if button == "down":
            return replace(state, selection=_wrap(state.selection + 1, len(COMMANDS)))
        if button == "confirm":
            command = COMMANDS[state.selection]
            output = {
                "HELP": "HELP  ABOUT  CLEAR",
                "ABOUT": "SNAKEY DESKTOP - NATIVE HOMEBREW",
                "CLEAR": "",
            }[command]
            return replace(state, console_output=output)
        return state

    if state.screen == "settings" and button == "confirm":
        return replace(state, palette=(state.palette + 1) % 2)

    return state
