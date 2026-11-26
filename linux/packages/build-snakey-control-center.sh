#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE_DIR="$ROOT_DIR/linux/packages/snakey-control-center"
VERSION="0.1.0"
PACKAGE_NAME="snakey-control-center-${VERSION}-noarch-1.txz"
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
mkdir -p "$PKGROOT/usr/bin" "$PKGROOT/usr/share/applications" "$PKGROOT/etc/skel/Desktop" "$PKGROOT/install" "$PKGROOT/usr/doc/snakey-control-center-$VERSION" "$DEST_DIR"
install -m 0755 "$SOURCE_DIR/usr/bin/snakey-control-center" "$PKGROOT/usr/bin/snakey-control-center"
install -m 0644 "$SOURCE_DIR/usr/share/applications/snakey-control-center.desktop" "$PKGROOT/usr/share/applications/snakey-control-center.desktop"
install -m 0644 "$SOURCE_DIR/etc/skel/Desktop/Snakey-Control-Center.desktop" "$PKGROOT/etc/skel/Desktop/Snakey-Control-Center.desktop"
install -m 0644 "$SOURCE_DIR/slack-desc" "$PKGROOT/install/slack-desc"
install -m 0644 "$ROOT_DIR/linux/README.md" "$PKGROOT/usr/doc/snakey-control-center-$VERSION/README"

(
  cd "$PKGROOT"
  makepkg -l y -c n "$DEST_DIR/$PACKAGE_NAME"
)
test -s "$DEST_DIR/$PACKAGE_NAME"
echo "Built Slackware package: $DEST_DIR/$PACKAGE_NAME"
