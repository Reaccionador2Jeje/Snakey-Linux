#!/usr/bin/env bash
set -Eeuo pipefail
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE_DIR="$ROOT_DIR/linux/packages/snakey-browser"
VERSION="0.1.0"
PACKAGE_NAME="snakey-browser-${VERSION}-noarch-1.txz"
DEST_DIR="${1:-$ROOT_DIR/dist/packages}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "ERROR: Slackware makepkg must run as root." >&2
  exit 2
fi
command -v makepkg >/dev/null 2>&1 || {
  echo "ERROR: makepkg is missing; build this package on a Slackware host." >&2
  exit 2
}

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
PKGROOT="$WORK/package"
mkdir -p "$PKGROOT/usr/bin" "$PKGROOT/usr/share/applications" "$PKGROOT/install" "$PKGROOT/usr/doc/snakey-browser-$VERSION" "$DEST_DIR"
install -m 0755 "$SOURCE_DIR/usr/bin/snakey-browser" "$PKGROOT/usr/bin/snakey-browser"
install -m 0644 "$SOURCE_DIR/usr/share/applications/snakey-browser.desktop" "$PKGROOT/usr/share/applications/snakey-browser.desktop"
install -m 0644 "$SOURCE_DIR/slack-desc" "$PKGROOT/install/slack-desc"
install -m 0644 "$ROOT_DIR/linux/packages/README.md" "$PKGROOT/usr/doc/snakey-browser-$VERSION/README"

(
  cd "$PKGROOT"
  makepkg -l y -c n "$DEST_DIR/$PACKAGE_NAME"
)
test -s "$DEST_DIR/$PACKAGE_NAME"
echo "Built Slackware package: $DEST_DIR/$PACKAGE_NAME"
