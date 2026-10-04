#!/usr/bin/env python3
"""Create a deterministic skill.zip for ARX Backend."""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

import validate_repo

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "arx-be"
MAX_BYTES = 25 * 1024 * 1024
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def build(output: Path) -> str:
    errors = validate_repo.validate_repo(ROOT)
    if errors:
        print("Refusing to package an invalid repository:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    output.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            rel = path.relative_to(SOURCE)
            arcname = Path("arx-be") / rel
            info = zipfile.ZipInfo(arcname.as_posix(), date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    size = output.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit(f"skill.zip exceeds 25 MiB: {size} bytes")

    with zipfile.ZipFile(output, "r") as zf:
        names = set(zf.namelist())
        required = {"arx-be/SKILL.md", "arx-be/agents/openai.yaml"}
        missing = required - names
        if missing:
            raise SystemExit(f"packaged archive missing required paths: {sorted(missing)}")
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"zip integrity check failed at: {bad}")

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"Packaged {output.relative_to(ROOT)} ({size} bytes)")
    print(f"sha256 {digest}")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dist/skill.zip")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    try:
        output.relative_to(ROOT)
    except ValueError:
        print("Output must stay inside the repository", file=sys.stderr)
        return 2
    build(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
