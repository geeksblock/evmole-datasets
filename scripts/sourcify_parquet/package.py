#!/usr/bin/env python3
"""Create a deterministic tar.gz archive from a generated dataset directory."""

from __future__ import annotations

import argparse
import gzip
import io
import sys
import tarfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="contract directory")
    parser.add_argument("--output", type=Path, required=True, help="output .tar.gz")
    parser.add_argument("--name", required=True, help="root directory name in the archive")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def tar_info(name: str, size: int, mode: int) -> tarfile.TarInfo:
    information = tarfile.TarInfo(name)
    information.size = size
    information.mode = mode
    information.uid = 0
    information.gid = 0
    information.uname = ""
    information.gname = ""
    information.mtime = 0
    return information


def main() -> int:
    args = parse_args()
    if args.output.exists() and not args.overwrite:
        raise RuntimeError(f"output already exists: {args.output}; use --overwrite to replace it")
    paths = sorted(args.input.glob("*.json"))
    if not paths:
        raise RuntimeError(f"no JSON contract files found in {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(f".{args.output.name}.tmp")
    try:
        with temporary.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w") as archive:
                    directory = tar_info(f"{args.name}/", 0, 0o755)
                    directory.type = tarfile.DIRTYPE
                    archive.addfile(directory)
                    for path in paths:
                        content = path.read_bytes()
                        information = tar_info(f"{args.name}/{path.name}", len(content), 0o644)
                        archive.addfile(information, io.BytesIO(content))
        temporary.replace(args.output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Wrote {args.output} with {len(paths)} contracts", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, tarfile.TarError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
