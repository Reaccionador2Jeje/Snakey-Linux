# Snakey Gamepad UI

Snakey Gamepad UI adds controller-first navigation to the XFCE live desktop.
It translates Linux joystick events (/dev/input/js0 or the first available
/dev/input/js*) into normal X11 key events, so XFCE widgets receive the same
keys they would receive from a physical keyboard.

## Default mapping

| Controller input | XFCE action |
| --- | --- |
| D-pad / left stick horizontal | Left / Right |
| D-pad / left stick vertical | Up / Down |
| A / Cross (button 0) | Enter |
| B / Circle (button 1) | Escape |
| X / Square (button 2) | Tab |
| Y / Triangle (button 3) | Open virtual keyboard |
| LB (button 4) | Shift + Tab |
| RB (button 5) | Tab |
| Start (button 6) | Enter |

Button numbering can differ by controller. The first implementation uses the
Linux joystick API's standard button indexes; remapping profiles will follow.

## Virtual keyboard

The desktop launcher **Snakey Virtual Keyboard** and Y/Triangle action launch
Onboard first, then Matchbox Keyboard. Install at least one of these packages
in the live image for on-screen text entry. The launcher gives a notification
if neither is present.

## Runtime requirements

- Python 3
- xdotool
- A controller exposed as /dev/input/jsN
- Onboard or Matchbox Keyboard for on-screen typing

The gamepad service starts automatically in XFCE. It exits harmlessly if no
controller is connected. Set SNAKEY_GAMEPAD_DEVICE=/dev/input/js1 in its
environment to select a specific joystick device.

## Current limitations

- X11/XFCE only; this profile uses Xorg, not Wayland.
- The first controller found is used.
- Analog axes provide directional navigation, not mouse-pointer movement.
- Hardware button numbering varies; validate each controller and adjust its
  mapping before claiming universal compatibility.
- The mapping is a first working layer, not a replacement for full controller
  configuration or accessibility testing.
