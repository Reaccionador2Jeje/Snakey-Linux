# Console Linux candidate matrix

This matrix is an evidence-oriented shortlist, not a compatibility promise.
All entries remain research candidates until Snakey has a pinned source tree,
reproducible build, and recorded boot evidence.

| Console | Architecture | Main RAM (approx.) | Research assessment | XFCE4 outlook |
| --- | --- | ---: | --- | --- |
| Nintendo Switch | AArch64 | 4 GB | Strongest resources; community Linux ecosystem exists, but hardware/boot/driver compatibility varies | Plausible only after driver and boot validation |
| PlayStation Vita | ARMv7 | 512 MB | Community kernel port exists; maturity and usable peripherals need audit | Uncertain; lightweight desktop first |
| Nintendo 3DS | ARMv6K | 128 MB | Community Linux kernel project exists; current maintenance and graphics path need audit | Very unlikely |
| Nintendo Wii | PowerPC 32-bit | 88 MB | Wii-Linux continuation project; framebuffer/Xorg reported, verify exact current support | Very unlikely; shell first |
| Original Xbox | x86 | 64 MB | Historical Xbox-Linux project; legacy toolchain and drivers | Not a realistic XFCE4 target |
| PlayStation 3 | PowerPC64 | 256 MB system + separate 256 MB video memory | Historical OtherOS/OtherOS++ ecosystem; boot path and model/firmware compatibility vary. ArchPOWER itself does not claim direct PS3 support | Experimental; owner has deferred hardware work |
| PlayStation 4 | x86-64 | 8 GB unified GDDR5 | Linux psX reports a tested PS4 Slim Baikal B1 with Linux 7.2.11 beta2; other southbridges and Pro remain unverified | XFCE/Xorg reported upstream on one tested Slim; Snakey untested |
| PlayStation 5 | x86-64 | 16 GB unified GDDR6 | Active ps5-linux kernel patch/image projects; support varies by model and firmware | Desktop images exist upstream; Snakey untested |
| Sega Dreamcast | SH-4 | 16 MB | Historical LinuxDC port; modern userspace and graphics path are major gaps | Not feasible |
| PlayStation 2 | MIPS R5900 | 32 MB | Historical Linux kit/ports; very constrained memory and specialized CPU | Not feasible |
| GameCube | PowerPC 32-bit | 24 MB | No current Snakey Linux path established | Not feasible |
| NES / SNES / GB / GBC / GBA / DS | Mixed 8/16/32-bit | Very limited | Native Snakey homebrew ROMs, not Linux distro targets | Not feasible |

Memory figures are platform-level approximations; usable RAM can be lower after
hardware reservations. Video memory is not counted as system RAM. Recheck
model-specific specifications before any implementation decision.

## Priority

1. **Switch:** best raw memory/CPU headroom among this shortlist, but support is
   configuration-dependent. Research only; no console modifications planned.
2. **Vita:** useful ARMv7 kernel research candidate; verify current project state.
3. **Wii:** useful PowerPC and framebuffer research target; desktop goal is a
   minimal graphical session, not assumed XFCE4.
4. **3DS:** kernel research only; memory makes a full desktop unrealistic.
5. **Original Xbox and Dreamcast:** preserve as historical port research, not
   primary desktop targets.
6. **PS4:** strongest PlayStation target for Snakey's x86-64 research lane; begin with source audit and host-side build reproduction.
7. **PS5:** source-audit lane after PS4; separate patch set and hardware support matrix.
8. **PS3:** deferred by owner. Do not ask for access or use it for testing.

## Acceptance gates

- Source repository and exact commit pinned.
- Kernel configuration and cross-toolchain reproducible in CI.
- Kernel artifact built and checksummed.
- Boot evidence captured in a named emulator or on hardware.
- Linux userspace and shell proven separately from kernel boot.
- Display/input/storage/network drivers tested individually.
- XFCE4 evaluated only after real memory and graphics measurements.

Sources for the initial research survey:
- https://emulation.gametechwiki.com/index.php/Homebrew_and_ROM_hacks
- https://wii-linux.org/
- https://www.ppsspp.org/docs/development/porting/
- https://wiki.batocera.org/systems
- https://www.kernel.org/
- https://linux.mrz.sh/compatibility/
- https://github.com/ps5-linux/ps5-linux-patches
- https://playstationdev.wiki/ps3/Distributions


## First reproducible build lane: PlayStation Vita

Snakey now pins the public `acgh213/vita-linux-next` integration source at
`05ee2d57b1d5a6f7b477141c3c68f65a069d682c`. Its upstream CI documents an
ARMv7 Bootlin toolchain and a kernel/DTB build. Snakey's workflow reproduces
that source build and labels the output as an upstream integration artifact;
it does not claim the kernel is Snakey-original or hardware-tested.

See [the Vita research lane](../linux/targets/vita/README.md) and
[the pinned source manifest](../platforms/linux-port-sources.json).

Switch and 3DS remain source-audit lanes until their exact repositories,
revision pins, licenses and reproducible build commands are verified.
