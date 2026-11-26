#!/usr/bin/env python3
"""Fetch only declared historical PSP archive files from psplinux.info."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "platforms" / "linux-port-sources.json"
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    source = next((item for item in manifest["sources"] if item["id"] == "psp-linux"), None)
    if source is None:
        raise SystemExit("PSP source entry is missing")
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("artifacts/psp-archives")
    output_dir.mkdir(parents=True, exist_ok=True)
    for archive in source.get("archives", []):
        archive_id = archive["id"]
        url = archive["url"]
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "psplinux.info":
            raise SystemExit(f"refusing untrusted archive host for {archive_id}: {url}")
        if not archive_id.replace("-", "").isalnum():
            raise SystemExit(f"invalid archive id: {archive_id}")
        request = Request(url, headers={"User-Agent": "Snakey-Linux-source-audit/1.0"})
        destination = output_dir / archive_id
        total = 0
        with urlopen(request, timeout=45) as response, destination.open("wb") as output:
            final_host = urlparse(response.geturl()).hostname
            if final_host != "psplinux.info":
                raise SystemExit(f"refusing redirect to unexpected host: {final_host}")
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_ARCHIVE_BYTES:
                    raise SystemExit(f"archive exceeds {MAX_ARCHIVE_BYTES} bytes: {archive_id}")
                output.write(chunk)
        if total == 0:
            raise SystemExit(f"empty archive downloaded: {archive_id}")
        print(f"downloaded {archive_id}: {total} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
