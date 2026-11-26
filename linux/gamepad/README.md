# Snakey Gamepad UI

Snakey Gamepad UI translates Linux joystick events into X11 key events for XFCE.
It reads the first /dev/input/jsN device by default and reconnects when a
controller is plugged in.

## Default mapping

| Controller input | XFCE action |
| --- | --- |
| D-pad / left stick | Arrow keys |
| A / button 0 | Enter |
| B / button 1 | Escape |
| X / button 2 | Tab |
| Y / button 3 | Open virtual keyboard |
| LB / button 4 | Shift + Tab |
| RB / button 5 | Tab |
| Start / button 6 | Enter |

Actual button indexes depend on the controller.

## Controller Center

Open **Snakey Controller Center** from the XFCE applications menu. Its
gamepad/keyboard navigable terminal interface lets you select a device,
adjust axis deadzone, change actions assigned to standard button indexes,
choose the virtual-keyboard button, and inspect live joystick events.

Use Up/Down to select, Left/Right to change values, Enter to run the test or
save, and Q to exit. Profiles are saved to ~/.config/snakey/gamepad.json.
The gamepad helper reads the saved profile when it starts; restart it or
log out/in after changing mappings.

## Virtual keyboard

Y/Triangle launches Onboard first, then Matchbox Keyboard. Install at least
one of these packages in the live image for on-screen text entry.

## Runtime requirements

- Python 3 with curses support
- xdotool
- XFCE/Xorg session
- A controller exposed as /dev/input/jsN
- Onboard or Matchbox Keyboard for on-screen typing

## Limitations

- X11/XFCE only; this profile is not a Wayland input mapper.
- The first controller is selected unless a device is configured.
- The event monitor observes Linux joystick events; it does not yet remap
  unknown controller layouts automatically.
- Hardware-specific mappings must be tested before claiming universal support.
