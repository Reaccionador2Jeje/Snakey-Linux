# Snakey Console Mode

Snakey Console Mode adapts the XFCE desktop for television-distance use and
gamepad navigation. It keeps XFCE as the desktop instead of replacing it with
a separate shell.

## Enable / disable

Run from an active XFCE session:

```sh
snakey-console-mode on
snakey-console-mode off
snakey-console-mode toggle
snakey-console-mode status
```

The mode enlarges the XFCE panel, panel icons, desktop icons and GTK font.
A **Snakey Console Mode** shortcut is also placed on the desktop through
`/etc/skel/Desktop`.

## Desktop shortcuts

The default desktop contains shortcuts for Files, Terminal, Settings,
On-screen Keyboard, Games and Console Mode. Games opens RetroArch when it is
installed; this initial image profile does not yet bundle game content.

## Controller operation

Snakey Gamepad UI remains the input layer: D-pad/left stick navigates, A
activates, B backs out, X/RB sends Tab, LB sends Shift+Tab and Y opens the
virtual keyboard. Exact button indexes vary by controller.

## Scope and limitations

- This is a large-control XFCE profile, not a dedicated 10-foot shell.
- It requires an active XFCE session and `xfconf-query`.
- The script creates XFCE settings; exact panel IDs may differ in a customized
  upstream liveslak profile, so test the image and adjust the panel path if
  needed.
- Virtual keyboard availability depends on Onboard or Matchbox Keyboard being
  installed. The launcher reports when neither is present.
- No physical gamepad or television test has been claimed yet.
