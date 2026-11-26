#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE="$ROOT_DIR/linux/profile.json"
ARCH="${SNAKEY_ARCH:-x86_64}"
OUTPUT_DIR="${SNAKEY_OUTPUT_DIR:-$ROOT_DIR/dist}"
LIVESLAK_DIR="${SNAKEY_LIVESLAK_DIR:-$ROOT_DIR/.build/liveslak}"
LIVESLAK_REPO="${SNAKEY_LIVESLAK_REPO:-https://git.slackware.nl/liveslak}"
SLACKWARE_REPO="${SNAKEY_SLACKWARE_REPO:-/var/cache/snakey/slackware}"

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
  SNAKEY_SLACKWARE_REPO Local mirror root containing slackware64-15.0

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

for command in git python3 makepkg; do
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
    "live_variant": "SNAKEY",
    "custom_package": "snakey-base",
    "base_release": "15.0",
    "base_channel": "stable",
    "package_manager": "pkgtools",
    "init_system": "SysVinit",
    "slackware_repository": "slackware64-15.0",
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

if [[ ! -d "$SLACKWARE_REPO/slackware64-15.0" ]]; then
  echo "ERROR: Slackware 15.0 repository not found: $SLACKWARE_REPO/slackware64-15.0" >&2
  echo "Set SNAKEY_SLACKWARE_REPO to a local mirror root containing slackware64-15.0." >&2
  exit 2
fi

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
echo "  Base: Slackware 15.0 (stable, x86_64)"
echo "  Package manager: pkgtools"
echo "  Init system: SysVinit"
echo "  Desktop: XFCE4 (Snakey custom liveslak variant)"
echo "  Native package: snakey-base"
echo "  Slackware mirror: $SLACKWARE_REPO/slackware64-15.0"
echo "  Architecture: $ARCH"
echo "  Boot mode: graphical (runlevel 4)"
echo "  Output: $OUTPUT"
echo
echo "NOTE: run this on a supported Slackware build host with liveslak prerequisites"
echo "and access to a complete Slackware package repository."

mkdir -p "$LIVESLAK_DIR/rootcopy" "$LIVESLAK_DIR/local64/snakey-base"
PACKAGE_OUTPUT="$OUTPUT_DIR/packages"
"$ROOT_DIR/linux/packages/build-snakey-base.sh" "$PACKAGE_OUTPUT"
install -m 0644 "$PACKAGE_OUTPUT/snakey-base-0.1.0-noarch-1.txz" "$LIVESLAK_DIR/local64/snakey-base/"
cp "$ROOT_DIR/linux/make_slackware_live.conf" "$LIVESLAK_DIR/make_slackware_live.conf"
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
  -d SNAKEY \
  -z 15.0 \
  -s "$SLACKWARE_REPO" \
  -c xz \
  -t bloat \
  -R 4 \
  -H snakey \
  -O "$OUTPUT"

test -s "$OUTPUT"
sha256sum "$OUTPUT" | tee "$OUTPUT.sha256"
echo "Snakey Linux image created: $OUTPUT"
