# Snakey Linux Desktop

Snakey Desktop is a **Linux userspace session**, not a console homebrew launched
by the console's original operating system. On supported targets the boot chain
must reach the Snakey Linux kernel and root filesystem first; the Linux init
system then starts the desktop as PID-managed userspace.

## Shared architecture

The three target adapters use one desktop identity and application model:

1. Linux kernel and target drivers initialize display, storage and input.
2. Init mounts the root filesystem and starts the Snakey userspace.
3. `S99snakey-desktop` starts `/usr/bin/snakey-desktop` on the active console.
4. Snakey Desktop owns the display in a single fullscreen session.
5. Controller events are translated by the target input adapter into the
   shared logical actions: UP, DOWN, LEFT, RIGHT, CONFIRM and BACK.

The first graphics backend is a small software renderer over Linux framebuffer
(`/dev/fb0`); input is read through Linux evdev (`/dev/input/event*`). This
avoids requiring Xorg, Wayland, a compositing window manager or a heavyweight
desktop stack on the constrained consoles. It is a design target: each backend
must be implemented and validated against its actual kernel drivers before
being marked operational.

## Shared applications

- **Launcher** — start the built-in applications.
- **Files** — browse Snakey system files and mounted user storage when available.
- **Console** — run the restricted built-in Snakey command interpreter.
- **System Monitor** — report CPU, memory, uptime and detected devices.
- **Settings** — controller mapping, display mode and theme.
- **About** — edition, kernel and build provenance.

The desktop must never pretend virtual files or unavailable devices are mounted.
The Files app reports unavailable storage clearly. The console is not a POSIX
shell until a real shell and userspace utilities are included in the rootfs.

## Target profiles

| Target | CPU / memory class | Initial desktop profile |
|---|---|---|
| PS Vita | ARMv7 / ~480 MiB | Snakey Desktop software framebuffer; XFCE4 only as later measured option |
| Original Xbox | i686 / 64 MiB | Ultra-minimal Snakey Desktop; no XFCE4 |
| Wii | PowerPC32 big-endian / 88 MiB | Ultra-minimal Snakey Desktop; no XFCE4 |

The same application semantics and visual identity are shared. Rendering,
controller mapping, memory budget, storage and boot integration remain
platform-specific.

## Startup contract

The root filesystem integration installs:

- `/usr/bin/snakey-desktop` — the native desktop executable.
- `/etc/init.d/S99snakey-desktop` — starts the desktop after kernel drivers,
  filesystems and basic userspace are ready.
- `/etc/snakey/desktop.conf` — target-specific display and input configuration.

The init script must check for a usable framebuffer and input device, log a
clear error when either is missing, and avoid respawning in a tight crash loop.
A shell on a serial/virtual terminal remains the recovery path.

## Validation gates

A successful cross-build is not a boot. The target status only advances when
evidence exists for each gate:

1. pinned kernel source and reproducible kernel build;
2. boot reaches Linux userspace;
3. framebuffer and controller input are detected;
4. desktop binary starts in the target emulator;
5. desktop is tested on named physical hardware.

No firmware modification, exploit execution, payload deployment or automatic
writes to physical console storage are part of CI.
