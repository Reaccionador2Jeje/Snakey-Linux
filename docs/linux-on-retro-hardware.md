# Snakey Linux on Retro Hardware

## Long-term objective

Run a genuine Linux kernel on supported retro console hardware and, where
resources and drivers permit, launch the XFCE4 desktop. Snakey must distinguish
a native Linux boot from a homebrew ROM that merely presents a console-style UI.

## The hardware reality

A console ROM is not a Linux distribution. The NES, Game Boy, Game Boy Color,
SNES and Game Boy Advance targets in this repository are native homebrew targets.
Their processors, memory capacities and platform architecture do not provide
the normal environment required by a Linux kernel plus XFCE4. They remain
valuable Snakey targets, but must not be advertised as Linux-capable.

The Nintendo DS has ARM CPUs but very limited memory and no general-purpose
desktop-class memory-management environment. Its current homebrew target is
not a Linux port and must not be presented as one.

The Wii is one candidate in a broader survey including Switch, Vita, 3DS,
original Xbox and Dreamcast. Their project maturity varies; see
[the console Linux candidate matrix](console-linux-candidates.md). The Switch
has the most memory headroom, while Wii/3DS/Xbox/Dreamcast are constrained.
XFCE4 is never assumed feasible.

The PlayStation 3 is deferred. The owner does not currently have compatible
power or a display and has explicitly chosen not to use or modify it. Snakey
must not require PS3 access for ongoing development.

## Three execution classes

| Class | Meaning | Snakey direction |
| --- | --- | --- |
| A — Native homebrew | Original console CPU executes a ROM | Build Snakey menus, apps and games using each console SDK |
| B — Linux-capable retro hardware | Console has a usable MMU/CPU, enough RAM, boot path and accessible drivers | Port or integrate a real Linux kernel, then bring up userspace |
| C — Linux host / console frontend | Linux runs on a PC or supported handheld and emulates the console | Run Snakey Linux XFCE4 on the host and use controller-first Big Picture |

A Class B target is accepted only after its hardware and boot chain are
documented. A successful ROM build, emulator screenshot or frontend launch is
not proof of a native Linux boot.

## Requirements for a real Linux port

Before selecting a console, record and verify:

1. CPU architecture and supported Linux kernel port.
2. MMU availability and kernel configuration support.
3. RAM size and memory map, including reserved video/audio memory.
4. Boot chain, firmware requirements and a reproducible boot method.
5. Storage or filesystem access, such as SD, USB, network or internal media.
6. Display, input, audio and storage drivers.
7. A maintained toolchain and a reproducible kernel build.
8. A minimal userspace that boots to a shell before attempting a desktop.

## XFCE4 acceptance stages

XFCE4 is a later milestone, not the first boot target. The sequence is:

1. Boot a real Linux kernel and reach a serial or framebuffer console.
2. Mount a root filesystem and start a minimal init/userspace.
3. Bring up display, input and storage drivers.
4. Start a lightweight graphical server supported by the platform.
5. Measure available RAM and CPU under load.
6. Add XFCE4 only if the platform can sustain it; otherwise use a smaller
   native graphical shell and document the limitation.

The XFCE4 live image currently built through liveslak is x86_64. It is not a
universal image for every console architecture. Wii XFCE4 remains an
unverified stretch goal; 88 MB main memory is a severe constraint.

## Development roadmap

- [x] Separate native ROM targets from the Linux distribution track.
- [x] Document Linux capability and acceptance criteria.
- [x] Create a reusable hardware evidence sheet for each proposed Class B console.
- [x] Create a multi-console Linux research matrix; all candidates remain untested.
- [ ] Audit Switch and Vita source projects, licenses, toolchains and drivers.
- [ ] Audit Wii and 3DS kernel sources and compare reproducible build paths.
- [x] Defer PlayStation 3 hardware work until the owner independently chooses to use it.
- [ ] Select a target after source/toolchain/driver audit.
- [ ] Build a reproducible kernel artifact for that target; no hardware boot claim.
- [ ] Reach a real Linux shell.
- [ ] Add display and controller support.
- [ ] Evaluate XFCE4 memory and performance requirements.
- [ ] Publish emulator-tested and, where possible, hardware-tested images.

## Truthful status labels

Use these terms consistently:

- **ROM buildable:** a file is generated and passes structural checks.
- **Emulator-tested:** the ROM or image was actually launched in a named emulator.
- **Kernel boots:** a real Linux kernel reaches a documented boot milestone.
- **Linux userspace boots:** init and a shell run on the target.
- **XFCE4 runs:** the actual XFCE4 session launches on the target hardware or a
  clearly identified emulator.
- **Hardware-tested:** the result was verified on physical hardware.

Never promote one status to another without evidence.
