#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE="$ROOT_DIR/linux/profile.json"
ARCH="${SNAKEY_ARCH:-x86_64}"
OUTPUT_DIR="${SNAKEY_OUTPUT_DIR:-$ROOT_DIR/dist}"
LIVESLAK_DIR="${SNAKEY_LIVESLAK_DIR:-$ROOT_DIR/.build/liveslak}"
LIVESLAK_REPO="${SNAKEY_LIVESLAK_REPO:-https://git.slackware.nl/liveslak}"

usage() {
  cat <<'EOF'
Snakey Linux Live image builder

Usage:
  sudo linux/build-live.sh

Environment:
  SNAKEY_ARCH          Target architecture (default: x86_64)
  SNAKEY_OUTPUT_DIR    Output directory (default: ./dist)
  SNAKEY_LIVESLAK_DIR  liveslak checkout (default: ./.build/liveslak)
  SNAKEY_LIVESLAK_REPO liveslak Git repository URL

Build profile:
  Slackware Live + XFCE, graphical runlevel 4, xz compression,
  bloat trimming. This creates a real Slackware-based live ISO.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ "$ARCH" != "x86_64" ]]; then
  echo "ERROR: only x86_64 is currently supported by this profile." >&2
  exit 2
fi

if [[ "$(id -u)" -ne 0 ]]; then
  echo "ERROR: liveslak image creation must run as root. Re-run with sudo." >&2
  exit 2
fi

for command in git python3; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "ERROR: missing required command: $command" >&2
    exit 2
  }
done

python3 - "$PROFILE" <<'PY'
import json
import pathlib
import sys

profile = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
required = {
    "base": "Slackware",
    "builder": "liveslak",
    "architecture": "x86_64",
    "desktop": "XFCE",
    "runlevel": 4,
    "compression": "xz",
    "trim": "bloat",
}
for key, expected in required.items():
    actual = profile.get(key)
    if actual != expected:
        raise SystemExit(f"Invalid linux/profile.json: {key}={actual!r}, expected {expected!r}")
print("Snakey Linux profile: OK")
PY

mkdir -p "$OUTPUT_DIR" "$(dirname -- "$LIVESLAK_DIR")"
OUTPUT_DIR="$(cd -- "$OUTPUT_DIR" && pwd)"
OUTPUT="$OUTPUT_DIR/Snakey-Linux-XFCE-$ARCH.iso"

if [[ ! -d "$LIVESLAK_DIR/.git" ]]; then
  git clone --depth 1 "$LIVESLAK_REPO" "$LIVESLAK_DIR"
else
  git -C "$LIVESLAK_DIR" pull --ff-only
fi

BUILDER="$LIVESLAK_DIR/make_slackware_live.sh"
if [[ ! -x "$BUILDER" ]]; then
  echo "ERROR: liveslak builder not found or not executable: $BUILDER" >&2
  exit 2
fi

echo "Building Snakey Linux Desktop"
echo "  Base: Slackware"
echo "  Desktop: XFCE (liveslak lightweight profile)"
echo "  Architecture: $ARCH"
echo "  Boot mode: graphical (runlevel 4)"
echo "  Output: $OUTPUT"
echo
echo "NOTE: run this on a supported Slackware build host with liveslak prerequisites"
echo "and access to a complete Slackware package repository."

mkdir -p "$LIVESLAK_DIR/rootcopy"
cp -a "$ROOT_DIR/linux/rootcopy/." "$LIVESLAK_DIR/rootcopy/"
chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-gamepad"
chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-virtual-keyboard"
chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-console-mode"
chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-open-keyboard"
chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-controller-center"
chmod 0755 "$LIVESLAK_DIR/rootcopy/usr/bin/snakey-big-picture"

cd "$LIVESLAK_DIR"
./make_slackware_live.sh \
  -a "$ARCH" \
  -d XFCE \
  -c xz \
  -t bloat \
  -R 4 \
  -H snakey \
  -O "$OUTPUT"

test -s "$OUTPUT"
sha256sum "$OUTPUT" | tee "$OUTPUT.sha256"
echo "Snakey Linux image created: $OUTPUT"
