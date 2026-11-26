# Snakey physical hardware test matrix

This matrix separates source/build checks, emulator checks and tests performed on actual consoles. A test is not considered passed without a dated report and evidence.

| Target | Build adapter | Emulator test | Physical test path | Current verified level |
| --- | --- | --- | --- | --- |
| NES | cc65 NROM-256 mapper 0 | RetroArch NES core; verify video, D-pad, A/B and reset | Compatible NES flash cartridge or correctly supported NROM board; verify exact console revision and cartridge compatibility first | CI build only; physical test pending |
| SNES | Not implemented | Compatible SNES emulator after adapter exists | Compatible SNES flash cartridge; board/mapper and region compatibility must be confirmed | Scaffold only |
| Game Boy | RGBDS | RetroArch GB core; verify DMG boot and controls | Compatible GB flash cartridge or cartridge board; test on DMG hardware | CI build being added; physical test pending |
| Game Boy Color | RGBDS (current starter is DMG-compatible) | RetroArch GBC core; verify compatibility mode | Compatible GBC flash cartridge; test DMG-compatible and CGB-specific features only when implemented | CI build being added; physical test pending |
| Game Boy Advance | Not implemented | Compatible GBA emulator after adapter exists | Compatible GBA flash cartridge; verify supported ROM size and save type | Scaffold only |
| Nintendo DS | Not implemented | melonDS/DeSmuME or supported RetroArch core after adapter exists | Compatible DS flashcart or documented homebrew loader for exact model/firmware | Scaffold only |

## Safe physical test procedure

1. Identify the exact console model/revision and region. Record it; do not assume all revisions behave identically.
2. Use only a known-compatible, commercially supported flash cartridge or a legitimate development cartridge. Check its documentation and supported ROM format.
3. Start with a self-built, non-destructive test ROM. Do not modify console firmware or write to unknown cartridge hardware.
4. Verify the ROM checksum before copying it to the flashcart's SD card. Keep the original ROM and SD contents backed up.
5. Test boot, video, input, reset and stability. Stop if the console or cartridge behaves abnormally.
6. Record the flashcart model/firmware, SD filesystem, console model, ROM SHA-256, test date and observed result.
7. Mark the platform hardware-tested only after the report is reviewed and attached to the repository.

## Test report template

Copy docs/hardware-test-report-template.md for each physical session. Never mark an untested platform as passed. A successful emulator test is not a physical hardware test.
