#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "duckdb>=1.3,<2",
# ]
# ///

"""Generate candidate pools, select the benchmark suite, and package its datasets."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True, help="Sourcify Parquet cache")
    parser.add_argument("--work", type=Path, required=True, help="candidate and intermediate output")
    parser.add_argument("--output", type=Path, required=True, help="suite output directory")
    parser.add_argument("--profile", type=Path, default=SCRIPT_DIR / "suite.json")
    parser.add_argument("--memory-limit", default="8GB")
    parser.add_argument("--temp-directory", type=Path)
    parser.add_argument("--skip-candidates", action="store_true", help="reuse existing candidate pools")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def run(command: list[str]) -> None:
    print("+ " + " ".join(command), file=sys.stderr)
    subprocess.run(command, check=True)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def local_cache_manifest(cache: Path) -> dict:
    objects = []
    for table in ("code", "contracts", "contract_deployments", "compiled_contracts", "verified_contracts"):
        for path in sorted((cache / table).glob("*.parquet")):
            information = path.stat()
            objects.append(
                {
                    "path": str(path.relative_to(cache)),
                    "size": information.st_size,
                    "mtimeNs": information.st_mtime_ns,
                }
            )
    return {
        "formatVersion": 1,
        "source": "local-cache",
        "objects": objects,
    }


def generator_command(args: argparse.Namespace, profile: dict, name: str, pool: dict) -> list[str]:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "generate.py"),
        "--cache",
        str(args.cache),
        "--output",
        str(args.work / "candidates" / name),
        "--count",
        str(pool["count"]),
        "--chain-id",
        str(profile["chainId"]),
        "--compiler",
        pool["compiler"],
        "--functions-min",
        "0",
        "--bytecode-size-max",
        str(profile["bytecodeSizeMax"]),
        "--match",
        pool.get("match", profile["match"]),
        "--candidate-factor",
        str(profile["candidateFactor"]),
        "--seed",
        f"{profile['seed']}/candidate/{name}",
        "--memory-limit",
        args.memory_limit,
    ]
    if args.temp_directory:
        command.extend(["--temp-directory", str(args.temp_directory)])
    if pool.get("compilerVersionMin"):
        command.extend(["--compiler-version-min", pool["compilerVersionMin"]])
    if pool.get("compilerVersionMax"):
        command.extend(["--compiler-version-max", pool["compilerVersionMax"]])
    if pool.get("includeStorageLayout"):
        command.append("--include-storage-layout")
    if args.overwrite:
        command.append("--overwrite")
    return command


def selector_command(args: argparse.Namespace, profile: dict, name: str, dataset: dict) -> list[str]:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "select_dataset.py"),
        "--output",
        str(args.output / "datasets" / name),
        "--manifest",
        str(args.output / "manifests" / f"{name}.json"),
        "--report",
        str(args.output / "reports" / f"{name}.md"),
        "--name",
        name,
        "--count",
        str(dataset["count"]),
        "--strategy",
        dataset["strategy"],
        "--coverage-target",
        str(dataset["coverageTarget"]),
        "--seed",
        f"{profile['seed']}/dataset/{name}",
    ]
    for pool in dataset["pools"]:
        command.extend(["--input", str(args.work / "candidates" / pool)])
    for compiler in dataset.get("compilers", []):
        command.extend(["--compiler", compiler])
    for excluded in dataset.get("excludeDatasets", []):
        command.extend(
            [
                "--exclude-manifest",
                str(args.output / "manifests" / f"{excluded}.json"),
            ]
        )
    if args.overwrite:
        command.append("--overwrite")
    return command


def main() -> int:
    args = parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    if profile.get("formatVersion") != 1:
        raise RuntimeError(f"unsupported suite profile version: {profile.get('formatVersion')}")
    profile_output = args.output / "suite-profile.json"
    if profile_output.exists() and not args.overwrite:
        raise RuntimeError(f"output already exists: {profile_output}; use --overwrite to replace it")

    args.work.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)
    if not args.skip_candidates:
        for name, pool in profile["candidatePools"].items():
            run(generator_command(args, profile, name, pool))

    for name, dataset in profile["datasets"].items():
        run(selector_command(args, profile, name, dataset))
        package_command = [
            sys.executable,
            str(SCRIPT_DIR / "package.py"),
            "--input",
            str(args.output / "datasets" / name),
            "--output",
            str(args.output / "archives" / f"{name}.tar.gz"),
            "--name",
            name,
        ]
        if args.overwrite:
            package_command.append("--overwrite")
        run(package_command)

    profile_output.write_text(
        json.dumps(profile, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        duckdb_version = version("duckdb")
    except PackageNotFoundError:
        duckdb_version = "unknown"
    provenance_files = {
        "suite.json": args.profile,
        "generate.py": SCRIPT_DIR / "generate.py",
        "dataset_common.py": SCRIPT_DIR / "dataset_common.py",
        "select_dataset.py": SCRIPT_DIR / "select_dataset.py",
        "package.py": SCRIPT_DIR / "package.py",
        "suite.py": SCRIPT_DIR / "suite.py",
    }
    generation_metadata = {
        "formatVersion": 1,
        "pythonVersion": sys.version,
        "duckdbVersion": duckdb_version,
        "files": {
            name: file_sha256(path)
            for name, path in provenance_files.items()
        },
    }
    (args.output / "generation-metadata.json").write_text(
        json.dumps(generation_metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    cache_manifest = args.cache / ".sourcify-export-v2.json"
    if cache_manifest.exists():
        shutil.copyfile(cache_manifest, args.output / "cache-manifest.json")
    else:
        (args.output / "cache-manifest.json").write_text(
            json.dumps(local_cache_manifest(args.cache), indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Suite is ready under {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
