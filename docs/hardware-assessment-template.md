# Retro Console Linux Hardware Assessment

Copy this sheet for every proposed native Linux target. Do not mark a field
"supported" from speculation; attach a source, test log or reproducible result.

## Identity

- Console / hardware revision:
- Region / model identifier:
- CPU and architecture:
- RAM:
- GPU / display controller:
- Storage expansion:
- Network hardware:
- Boot / homebrew entry method:
- Emulator used for early tests:

## Kernel feasibility

| Requirement | Evidence / source | Result |
| --- | --- | --- |
| Linux-supported CPU architecture | | Unknown |
| MMU and kernel port available | | Unknown |
| Bootloader or kernel handoff documented | | Unknown |
| Interrupt controller / timers | | Unknown |
| RAM map and reserved regions | | Unknown |
| Serial or debug output | | Unknown |
| Storage driver | | Unknown |
| Display / framebuffer driver | | Unknown |
| Controller / input driver | | Unknown |
| Audio driver | | Unknown |

## Resource budget

- RAM available to Linux after firmware reservations:
- Estimated kernel + initramfs footprint:
- Root filesystem size:
- Free RAM after minimal userspace:
- Free RAM after graphical server:
- Free RAM after XFCE4 session:
- CPU performance observations:

## Test evidence

- Kernel source / branch:
- Kernel configuration:
- Build command:
- Image checksum:
- Boot method:
- Exact boot milestone reached:
- Emulator and version:
- Physical hardware revision (if tested):
- Logs / photos / recordings:

## Decision

Choose exactly one:

- [ ] Class A — native homebrew only; no feasible Linux port identified.
- [ ] Class B — Linux port appears feasible; evidence and development required.
- [ ] Class C — Linux runs on a host; console is accessed through emulation.
- [ ] Rejected — insufficient evidence or a hard architectural blocker.

XFCE4 decision:

- [ ] Not evaluated.
- [ ] Not feasible with current RAM / drivers.
- [ ] Feasible in theory; not tested.
- [ ] XFCE4 session launched in emulator.
- [ ] XFCE4 session launched on physical hardware.

## Sign-off

- Reviewer:
- Date:
- Evidence links:
- Known limitations:
