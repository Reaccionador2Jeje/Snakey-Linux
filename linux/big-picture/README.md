# Snakey Big Picture

Snakey Big Picture is a controller-first launcher for the XFCE live desktop.
It runs inside a fullscreen XFCE terminal and uses the same arrow/Enter/Escape
key events emitted by Snakey Gamepad UI.

## Menu

- Games: starts RetroArch when installed.
- Applications: opens XFCE Application Finder.
- Files: opens Thunar.
- Terminal: opens XFCE Terminal.
- Controller Center: opens Snakey controller configuration.
- Settings: opens XFCE Settings Manager.
- Desktop / Console Mode: toggles Snakey's large-control XFCE profile.

## Launch

Run `snakey-big-picture` from a terminal, or use the **Snakey Big Picture**
desktop shortcut. The menu is intentionally not forced at login yet, so users
can choose between the conventional XFCE desktop and the console launcher.

## Requirements and limitations

- XFCE/Xorg and Python 3 with curses.
- Snakey Gamepad UI and xdotool for controller navigation.
- RetroArch is optional; the Games entry reports when it is unavailable.
- This is a fullscreen launcher, not a replacement desktop shell.
