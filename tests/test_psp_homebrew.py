#!/usr/bin/env python3
"""Host-side contract checks for the Snakey PSP homebrew target."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "psp" / "Makefile"
SOURCE = ROOT / "psp" / "src" / "main.c"
README = ROOT / "psp" / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "psp-homebrew.yml"


def main() -> None:
    for path in (MAKEFILE, SOURCE, README, WORKFLOW):
        assert path.is_file(), f"missing PSP homebrew file: {path.relative_to(ROOT)}"

    makefile = MAKEFILE.read_text(encoding="utf-8")
    source = SOURCE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "include $(PSPSDK)/lib/build.mak" in makefile
    assert "EXTRA_TARGETS = EBOOT.PBP" in makefile
    assert "PSP_MODULE_INFO" in source
    assert "sceCtrlReadBufferPositive" in source
    assert "PSP_CTRL_CROSS" in source
    assert "PSP_CTRL_CIRCLE" in source
    assert "VIEW_DESKTOP" in source
    assert "VIEW_TERMINAL" in source
    assert "execute_command" in source
    for command in ("help", "clear", "uname", "version", "mem", "pwd", "ls", "echo ", "exit"):
        assert command in source, f"missing built-in command: {command}"
    assert "pspdev/pspdev" in workflow
    assert "EBOOT.PBP" in workflow
    print("Snakey PSP homebrew contract: OK")


if __name__ == "__main__":
    main()
