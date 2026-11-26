#!/usr/bin/env python3
"""Deterministic minimal homebrew image writers for SNES, GBA and Nintendo DS.

These produce correctly sized/container-structured experimental images. They are
not substitutes for SDKs, commercial firmware, or physical-hardware validation.
"""
from __future__ import annotations
import argparse
import struct
from pathlib import Path

def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(f"ROM built: {path} ({len(data)} bytes)")

def build_snes(path: Path, name: str) -> None:
    # LoROM, 32 KiB. 65816 reset stub leaves the display safely enabled and
    # loops; a later milestone will replace this boot stub with the menu UI.
    rom = bytearray([0xEA] * 0x8000)
    code = bytes([
        0x78,             # SEI
        0x18, 0xFB,       # CLC / XCE: enter native mode
        0xC2, 0x30,       # REP #$30
        0xA2, 0xFF, 0x1F, # LDX #$1FFF
        0x9A,             # TXS
        0xE2, 0x20,       # SEP #$20
        0xA9, 0x0F,       # LDA #$0F
        0x8D, 0x00, 0x21, # STA $2100 (display enable, full brightness)
        0x80, 0xFE        # BRA forever
    ])
    rom[:len(code)] = code
    header = bytearray(0x40)
    title = (name.upper().encode("ascii", "ignore")[:21]).ljust(21, b" ")
    header[0:21] = title
    header[0x15:0x1B] = bytes([0x20, 0x00, 0x07, 0x00, 0x01, 0x00])
    # LoROM vectors: native/emulation NMI, reset and IRQ. Reset points to $8000.
    struct.pack_into("<6H", header, 0x20, *([0x8000] * 6))
    struct.pack_into("<6H", header, 0x34, *([0x8000] * 6))
    header[0x1C:0x20] = bytes(4)
    rom[0x7FC0:0x8000] = header
    rom[0x7FDC:0x7FE0] = bytes(4)
    checksum = sum(rom) & 0xFFFF
    struct.pack_into("<HH", rom, 0x7FDC, checksum ^ 0xFFFF, checksum)
    _write(path, bytes(rom))

def _arm_branch_to(offset: int) -> bytes:
    # ARM unconditional branch at address 0 to offset, PC is address+8.
    imm24 = (offset - 8) // 4
    return struct.pack("<I", 0xEA000000 | (imm24 & 0xFFFFFF))

def build_gba(path: Path, name: str) -> None:
    rom = bytearray(0x8000)
    rom[0:4] = _arm_branch_to(0xC0)
    # Header fields and a homebrew title/code. Logo bytes intentionally remain
    # zero: this is an emulator-development image, not a retail-BIOS-certified ROM.
    title = name.upper().encode("ascii", "ignore")[:12].ljust(12, b" ")
    rom[0xA0:0xAC] = title
    rom[0xAC:0xB0] = b"SNKY"
    rom[0xB0:0xB2] = b"01"
    rom[0xB2] = 0x96
    rom[0xB3] = 0
    rom[0xB4:0xBC] = bytes(8)
    rom[0xBC] = 0
    rom[0xBD] = (-sum(rom[0xA0:0xBD]) - 0x19) & 0xFF
    rom[0xBE] = 0
    rom[0xBF] = 0
    # ARM code at 0xC0: Mode 3 framebuffer filled with a teal field, then loop.
    # Use a conservative, visibly colored screen fill loop (38400 pixels).
    code = struct.pack("<15I",
        0xE59F0030, # ldr r0,[pc,#48] -> DISPCNT literal
        0xE3A01003, # mov r1,#3 (Mode 3)
        0xE3811B01, # orr r1,r1,#0x400 (enable BG2)
        0xE5801000, # str r1,[r0]
        0xE59F3018, # ldr r3,[pc,#24] -> VRAM literal
        0xE59F2018, # ldr r2,[pc,#24] -> pixel count literal
        0xE3A0401F, # mov r4,#31 (red)
        0xE1C340B0, # strh r4,[r3]
        0xE2833002, # add r3,r3,#2
        0xE2522001, # subs r2,r2,#1
        0x1AFFFFFB, # bne back to strh
        0xEAFFFFFE, # loop forever
        0x06000000, # VRAM
        0x00009600, # 38,400 pixels
        0x04000000  # DISPCNT
    )
    rom[0xC0:0xC0+len(code)] = code
    _write(path, bytes(rom))

def _crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0xA001 if crc & 1 else 0)
    return crc & 0xFFFF

def build_nds(path: Path, name: str) -> None:
    rom = bytearray(0x10000)
    title = name.upper().encode("ascii", "ignore")[:12].ljust(12, b" ")
    rom[0:12] = title
    rom[12:16] = b"SNKY"
    rom[16:18] = b"01"
    rom[0x1E] = 0
    # ARM9 and ARM7 binaries are small ARM branch-to-self stubs. Real dual-screen
    # rendering and retail logo compatibility are deliberately future work.
    arm9_offset, arm7_offset = 0x4000, 0x5000
    arm9 = struct.pack("<4I", 0xEAFFFFFE, 0xE1A00000, 0xE1A00000, 0xE1A00000)
    arm7 = struct.pack("<4I", 0xEAFFFFFE, 0xE1A00000, 0xE1A00000, 0xE1A00000)
    struct.pack_into("<8I", rom, 0x20,
        arm9_offset, 0x02000000, 0x02000000, len(arm9),
        arm7_offset, 0x03800000, 0x03800000, len(arm7))
    struct.pack_into("<I", rom, 0x80, len(rom)) # total used ROM size
    struct.pack_into("<I", rom, 0x84, 0x4000) # header-size field
    rom[arm9_offset:arm9_offset+len(arm9)] = arm9
    rom[arm7_offset:arm7_offset+len(arm7)] = arm7
    struct.pack_into("<H", rom, 0x15C, _crc16(rom[0xC0:0x15C]))
    struct.pack_into("<H", rom, 0x15E, _crc16(rom[:0x15E]))
    _write(path, bytes(rom))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=("snes", "game-boy-advance", "nintendo-ds"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--name", default="SNAKEY")
    args = parser.parse_args()
    {"snes": build_snes, "game-boy-advance": build_gba, "nintendo-ds": build_nds}[args.target](args.output, args.name)

if __name__ == "__main__":
    main()
