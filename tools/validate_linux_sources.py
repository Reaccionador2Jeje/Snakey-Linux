#!/usr/bin/env python3
"""Validate pinned upstream source metadata for Snakey console Linux research."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "platforms" / "linux-port-sources.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read source manifest: {exc}")

    if data.get("schema_version") != 1:
        fail("schema_version must be 1")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("sources must be a non-empty array")

    seen: set[str] = set()
    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        if not isinstance(source, dict):
            fail(f"{prefix} must be an object")
        for field in ("id", "name", "project_url", "source_repository",
                      "revision", "architecture", "build_status", "license"):
            if field not in source:
                fail(f"{prefix} missing {field}")
        source_id = source["id"]
        if not isinstance(source_id, str) or not source_id or source_id in seen:
            fail(f"{prefix}.id must be unique and non-empty")
        seen.add(source_id)
        if not isinstance(source["project_url"], str) or not source["project_url"].startswith("https://"):
            fail(f"{prefix}.project_url must be an HTTPS URL")
        if source["source_repository"] is not None and (not isinstance(source["source_repository"], str) or not source["source_repository"].startswith("https://")):
            fail(f"{prefix}.source_repository must be an HTTPS URL or null")
        if source["build_status"] == "pinned-upstream-build":
            if not isinstance(source["revision"], str) or not HEX40.fullmatch(source["revision"]):
                fail(f"{prefix} requires a full 40-character pinned commit")
            if not isinstance(source.get("build_workflow"), str):
                fail(f"{prefix} requires build_workflow")
        elif source["build_status"] == "source-audit-required":
            if source["revision"] is not None:
                fail(f"{prefix} must not claim an unverified revision")
        else:
            fail(f"{prefix}.build_status is unsupported")

    print(f"Snakey Linux source manifest: OK ({len(sources)} sources)")
    for source in sources:
        pin = source["revision"] or "not pinned"
        print(f"  {source['id']}: {source['build_status']} ({pin})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
