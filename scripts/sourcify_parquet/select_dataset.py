#!/usr/bin/env python3
"""Select and materialize a reproducible benchmark dataset from candidate pools."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

from dataset_common import load_candidates, markdown_summary, select_candidates, summarize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True, help="candidate directory; repeatable")
    parser.add_argument("--output", type=Path, required=True, help="selected contract directory")
    parser.add_argument("--manifest", type=Path, required=True, help="selection manifest path")
    parser.add_argument("--report", type=Path, required=True, help="Markdown report path")
    parser.add_argument("--name", required=True, help="dataset name")
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--strategy", choices=("random", "coverage", "storage", "flow"), required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--coverage-target", type=int, default=30)
    parser.add_argument("--compiler", action="append", default=[], help="compiler filter; repeatable")
    parser.add_argument(
        "--exclude-manifest",
        action="append",
        type=Path,
        default=[],
        help="exclude normalized code hashes selected by another dataset; repeatable",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.coverage_target < 1:
        parser.error("--coverage-target must be at least 1")
    return args


def ensure_available(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise RuntimeError(f"output already exists: {path}; use --overwrite to replace it")


def main() -> int:
    args = parse_args()
    for path in (args.output, args.manifest, args.report):
        ensure_available(path, args.overwrite)
    candidates, errors = load_candidates(args.input)
    compiler_filter = {value.lower() for value in args.compiler}
    if compiler_filter:
        candidates = [candidate for candidate in candidates if candidate.compiler in compiler_filter]
    excluded_hashes: set[str] = set()
    for path in args.exclude_manifest:
        document = json.loads(path.read_text(encoding="utf-8"))
        excluded_hashes.update(
            contract["normalizedCodeHash"]
            for contract in document.get("contracts", [])
            if isinstance(contract, dict) and isinstance(contract.get("normalizedCodeHash"), str)
        )
    if excluded_hashes:
        candidates = [
            candidate
            for candidate in candidates
            if candidate.normalized_hash not in excluded_hashes
        ]
    selected = select_candidates(
        candidates,
        args.strategy,
        args.count,
        args.seed,
        args.coverage_target,
    )
    if len(selected) < args.count:
        raise RuntimeError(
            f"{args.name}: selected {len(selected)} unique eligible contracts, requested {args.count}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.parent / f".{args.output.name}.tmp-{uuid.uuid4().hex}"
    temporary.mkdir()
    try:
        for candidate in selected:
            destination = temporary / f"{candidate.address}.json"
            if args.strategy == "storage":
                document = json.loads(candidate.path.read_text(encoding="utf-8"))
                if "runtimeBytecode" not in document and "code" in document:
                    document["runtimeBytecode"] = document.pop("code")
                destination.write_text(
                    json.dumps(document, separators=(",", ":")) + "\n",
                    encoding="utf-8",
                )
            else:
                shutil.copyfile(candidate.path, destination)
        if args.output.exists():
            shutil.rmtree(args.output)
        os.replace(temporary, args.output)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    summary = summarize(selected)
    manifest = {
        "formatVersion": 1,
        "name": args.name,
        "createdAt": datetime.now(UTC).isoformat(),
        "strategy": args.strategy,
        "seed": args.seed,
        "requestedCount": args.count,
        "coverageTarget": args.coverage_target,
        "compilerFilter": sorted(compiler_filter),
        "excludeManifests": [str(path) for path in args.exclude_manifest],
        "excludedNormalizedHashes": len(excluded_hashes),
        "candidateInputs": [str(path) for path in args.input],
        "candidateCount": len(candidates),
        "candidateErrors": errors,
        "summary": summary,
        "contracts": [
            {
                "address": candidate.address,
                "compiler": candidate.compiler,
                "compilerVersion": candidate.compiler_version,
                "runtimeCodeHash": candidate.runtime_hash,
                "normalizedCodeHash": candidate.normalized_hash,
                "bytecodeSize": candidate.bytecode_size,
                "functionCount": candidate.function_count,
                "labels": sorted(candidate.labels),
            }
            for candidate in selected
        ],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    args.report.write_text(markdown_summary(args.name, summary), encoding="utf-8")
    print(f"Wrote {len(selected)} contracts to {args.output}", file=sys.stderr)
    if errors:
        print(f"Skipped {len(errors)} invalid candidate files; see the manifest", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
