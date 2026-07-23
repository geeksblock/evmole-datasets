#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Synchronize a local cache of Sourcify's v2 Parquet export."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


EXPORT_URL = "https://export.sourcify.dev"
DEFAULT_TABLES = (
    "code",
    "contracts",
    "contract_deployments",
    "compiled_contracts",
    "verified_contracts",
)


@dataclass(frozen=True)
class RemoteObject:
    key: str
    size: int
    etag: str
    last_modified: str


def request(url: str):
    return urllib.request.urlopen(  # noqa: S310 - the URL is configured by the user
        urllib.request.Request(url, headers={"User-Agent": "evmole-benchmark-dataset/1"}),
        timeout=120,
    )


def list_table(base_url: str, table: str) -> list[RemoteObject]:
    prefix = f"v2/{table}/"
    marker: str | None = None
    objects: list[RemoteObject] = []

    while True:
        params = {"prefix": prefix, "max-keys": "1000"}
        if marker:
            params["marker"] = marker
        url = f"{base_url}/?{urllib.parse.urlencode(params)}"
        with request(url) as response:
            root = ET.fromstring(response.read())

        def text(element: ET.Element, name: str, default: str = "") -> str:
            child = element.find(f"{{*}}{name}")
            return child.text if child is not None and child.text is not None else default

        page: list[RemoteObject] = []
        for element in root.findall("{*}Contents"):
            key = text(element, "Key")
            if not key.endswith(".parquet"):
                continue
            page.append(
                RemoteObject(
                    key=key,
                    size=int(text(element, "Size", "0")),
                    etag=text(element, "ETag").strip('"'),
                    last_modified=text(element, "LastModified"),
                )
            )
        objects.extend(page)

        if text(root, "IsTruncated").lower() != "true":
            break
        marker = text(root, "NextMarker") or (page[-1].key if page else None)
        if not marker:
            raise RuntimeError(f"truncated listing for {table} did not contain a continuation marker")

    return objects


def local_path(cache: Path, obj: RemoteObject) -> Path:
    # The key is always v2/TABLE/FILE. Avoid trusting a remote path directly.
    parts = Path(obj.key).parts
    if len(parts) != 3 or parts[0] != "v2" or parts[2] in {"", ".", ".."}:
        raise RuntimeError(f"unexpected object key: {obj.key!r}")
    return cache / parts[1] / parts[2]


def local_files(cache: Path, table: str) -> dict[str, int]:
    table_dir = cache / table
    if not table_dir.exists():
        return {}
    return {path.name: path.stat().st_size for path in table_dir.glob("*.parquet") if path.is_file()}


def manifest_path(cache: Path) -> Path:
    return cache / ".sourcify-export-v2.json"


def read_manifest(cache: Path) -> dict[str, dict]:
    path = manifest_path(cache)
    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    return {
        item["key"]: item
        for item in document.get("objects", [])
        if isinstance(item, dict) and isinstance(item.get("key"), str)
    }


def write_manifest(
    cache: Path,
    base_url: str,
    listings: dict[str, list[RemoteObject]],
) -> None:
    path = manifest_path(cache)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    objects = sorted(
        (obj for listing in listings.values() for obj in listing),
        key=lambda obj: obj.key,
    )
    document = {
        "formatVersion": 1,
        "baseUrl": base_url,
        "objects": [
            {
                "key": obj.key,
                "size": obj.size,
                "etag": obj.etag,
                "lastModified": obj.last_modified,
            }
            for obj in objects
        ],
    }
    try:
        temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def download(base_url: str, cache: Path, obj: RemoteObject) -> None:
    destination = local_path(cache, obj)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.part")
    size = 0
    try:
        url = f"{base_url}/{urllib.parse.quote(obj.key, safe='/')}"
        with request(url) as response, temporary.open("wb") as handle:
            while chunk := response.read(1024 * 1024):
                handle.write(chunk)
                size += len(chunk)
        if size != obj.size:
            raise RuntimeError(f"size mismatch for {obj.key}: expected {obj.size}, downloaded {size}")
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True, help="local Parquet cache directory")
    parser.add_argument("--tables", nargs="+", default=list(DEFAULT_TABLES), help="tables to synchronize")
    parser.add_argument("--jobs", type=int, default=4, help="parallel downloads (default: 4)")
    parser.add_argument("--status", action="store_true", help="report changes without downloading")
    parser.add_argument("--prune", action="store_true", help="remove cached files absent upstream")
    parser.add_argument("--base-url", default=EXPORT_URL, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")
    if len(args.tables) != len(set(args.tables)):
        parser.error("--tables contains duplicates")
    return args


def synchronize(args: argparse.Namespace) -> int:
    listings: dict[str, list[RemoteObject]] = {}
    changed: list[RemoteObject] = []
    previous_manifest = read_manifest(args.cache)

    for table in args.tables:
        print(f"Listing {table}...", file=sys.stderr)
        listing = list_table(args.base_url.rstrip("/"), table)
        listings[table] = listing
        cached = local_files(args.cache, table)
        table_changed = [
            obj
            for obj in listing
            if cached.get(Path(obj.key).name) != obj.size
            or (
                obj.key in previous_manifest
                and previous_manifest[obj.key].get("etag") != obj.etag
            )
        ]
        changed.extend(table_changed)
        print(f"  {len(listing)} files, {len(table_changed)} new or changed", file=sys.stderr)

    if args.status:
        return 1 if changed else 0

    if changed:
        total = sum(obj.size for obj in changed)
        print(f"Downloading {len(changed)} files ({total / 1024**3:.2f} GiB)...", file=sys.stderr)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = {
                executor.submit(download, args.base_url.rstrip("/"), args.cache, obj): obj
                for obj in changed
            }
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                obj = futures[future]
                future.result()
                completed += 1
                print(f"  [{completed}/{len(changed)}] {obj.key}", file=sys.stderr)

    if args.prune:
        for table, listing in listings.items():
            wanted = {local_path(args.cache, obj) for obj in listing}
            table_dir = args.cache / table
            if table_dir.exists():
                for path in table_dir.glob("*.parquet"):
                    if path not in wanted:
                        path.unlink()
                        print(f"Removed {path}", file=sys.stderr)

    write_manifest(args.cache, args.base_url.rstrip("/"), listings)
    print("Cache is up to date.", file=sys.stderr)
    return 0


def main() -> int:
    args = parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    return synchronize(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    except (OSError, RuntimeError, ValueError, ET.ParseError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
