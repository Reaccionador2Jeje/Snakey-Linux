# Snakey Desktop Core

This directory defines the shared application semantics used by the native
console editions.

## Reference runtime

`runtime.py` is an executable, platform-neutral state machine. It defines
launcher navigation and the behavior of four built-in applications:

- **Files** — a read-only catalog of data bundled in the ROM.
- **Console** — a fixed command set (HELP, ABOUT, CLEAR), not arbitrary code
  execution or a Linux shell.
- **Settings** — a real runtime palette toggle.
- **About** — system identity is supplied by each platform adapter.

The Python module is a reference model and host-side test target. It is not
embedded in console ROMs. Native adapters must implement these same state
transitions in their platform language/toolchain.

## Native adapter boundary

Each platform adapter owns its graphics renderer, physical button mapping,
storage interface, sound and memory layout. It must not claim support for
hardware features that the console does not provide.

The NES adapter is the first implementation target. Later adapters will map
the same app IDs and state transitions to SNES, Game Boy, Game Boy Color, GBA
and Nintendo DS hardware.

## Verify

```sh
python3 tools/validate_desktop_core.py
python3 -m unittest tests.test_desktop_core -v
```
