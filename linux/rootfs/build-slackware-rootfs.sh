#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET="${1:-}"
OUT_ARG="${2:-}"
PACKAGE_DIR="${SNAKEY_PACKAGE_DIR:-}"

usage() {
  echo "Usage: SNAKEY_PACKAGE_DIR=/path/to/txz $0 {vita|xbox|wii} [output-dir]" >&2
  exit 2
}
[[ "$TARGET" == vita || "$TARGET" == xbox || "$TARGET" == wii ]] || usage
[[ -n "$PACKAGE_DIR" && -d "$PACKAGE_DIR" ]] || usage
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 required" >&2; exit 2; }
command -v sha256sum >/dev/null 2>&1 || { echo "ERROR: sha256sum required" >&2; exit 2; }

MANIFEST="${SNAKEY_PACKAGE_MANIFEST:-$ROOT_DIR/linux/rootfs/$TARGET.packages}"
OUT_DIR="${OUT_ARG:-$ROOT_DIR/dist/rootfs-$TARGET}"
[[ -f "$MANIFEST" ]] || { echo "ERROR: missing manifest $MANIFEST" >&2; exit 2; }
[[ ! -e "$OUT_DIR" ]] || { echo "ERROR: output already exists: $OUT_DIR (remove it explicitly to rebuild)" >&2; exit 2; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/packages" "$OUT_DIR"

mapfile -t NAMES < <(sed -e 's/#.*//' -e '/^[[:space:]]*$/d' "$MANIFEST")
(("${#NAMES[@]}" > 0)) || { echo "ERROR: empty package manifest" >&2; exit 2; }

for name in "${NAMES[@]}"; do
  mapfile -t matches < <(find "$PACKAGE_DIR" -maxdepth 1 -type f -name "${name}-*.txz" -print | sort)
  if (("${#matches[@]}" != 1)); then
    echo "ERROR: expected exactly one ${name}-*.txz in $PACKAGE_DIR; found ${#matches[@]}" >&2
    exit 1
  fi
  cp -- "${matches[0]}" "$WORK/packages/"
done

python3 - "$OUT_DIR" "$WORK/packages" "$TARGET" "$MANIFEST" <<'PY'
import hashlib, json, pathlib, re, sys, tarfile

out = pathlib.Path(sys.argv[1]).resolve()
pkgdir = pathlib.Path(sys.argv[2])
target = sys.argv[3]
manifest = pathlib.Path(sys.argv[4])
(out / "var/log/packages").mkdir(parents=True)
(out / "var/log/scripts").mkdir(parents=True)

records = []
for archive in sorted(pkgdir.glob("*.txz")):
    package_name = archive.name[:-4]
    with tarfile.open(archive, "r:xz") as tf:
        members = tf.getmembers()
        for member in members:
            name = member.name
            normalized = pathlib.PurePosixPath(name)
            if normalized.is_absolute() or ".." in normalized.parts:
                raise SystemExit(f"unsafe path in {archive.name}: {name}")
            if member.isdev() or member.isfifo():
                raise SystemExit(f"unsupported special file in {archive.name}: {name}")
            if member.issym() or member.islnk():
                link = pathlib.PurePosixPath(member.linkname)
                if link.is_absolute() or ".." in link.parts:
                    raise SystemExit(f"unsafe link in {archive.name}: {name} -> {member.linkname}")
        payload = [m for m in members if not m.name.startswith("./install/") and m.name != "install"]
        # Reject links that could escape through an earlier symlink component.
        # Slackware official package archives are expected to contain normal
        # relative links; each extracted destination is additionally resolved.
        for member in payload:
            dest = (out / member.name.removeprefix("./")).resolve()
            if dest != out and out not in dest.parents:
                raise SystemExit(f"archive path escapes rootfs: {member.name}")
        for member in payload:
            tf.extract(member, out, set_attrs=True)
        install_files = [m for m in members if m.name.startswith("./install/")]
        desc = next((m for m in install_files if m.name.endswith("/slack-desc")), None)
        doinst = next((m for m in install_files if m.name.endswith("/doinst.sh")), None)
        if desc:
            src = tf.extractfile(desc)
            if src:
                (out / "var/log/packages" / package_name).write_bytes(src.read())
        if doinst:
            src = tf.extractfile(doinst)
            if src:
                (out / "var/log/scripts" / package_name).write_bytes(src.read())
        records.append({
            "package": package_name,
            "archive": archive.name,
            "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()
        })

(out / "etc").mkdir(exist_ok=True)
(out / "etc/snakey-release").write_text(
    f"NAME=Snakey Linux\nID=snakey\nVERSION=0.1.0-rootfs-bootstrap\n"
    f"BASE=Slackware-derived\nTARGET={target}\n",
    encoding="utf-8"
)
(out / "var/log/snakey-rootfs-manifest.json").write_text(
    json.dumps({"target": target, "stage": "package-extraction-only",
                "packages": records}, indent=2) + "\n", encoding="utf-8"
)
(out / "var/log/snakey-rootfs-stage.txt").write_text(
    "Package payloads extracted. Package doinst.sh scripts are staged, not run.\n"
    "This directory is not a bootable root filesystem.\n", encoding="utf-8"
)
PY

(
  cd "$OUT_DIR"
  find . -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)
echo "Slackware package rootfs staged: $OUT_DIR"
echo "Target: $TARGET"
echo "Packages: ${#NAMES[@]}"
echo "Status: package extraction only; not a bootable image"
