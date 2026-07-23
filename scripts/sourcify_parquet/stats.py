#!/usr/bin/env python3
"""Report coverage statistics for generated contract directories."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dataset_common import load_candidates, markdown_summary, summarize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", type=Path, required=True, help="dataset directory; repeatable")
    parser.add_argument("--name", required=True)
    parser.add_argument("--json", type=Path, required=True, dest="json_output")
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for path in (args.json_output, args.markdown):
        if path.exists() and not args.overwrite:
            raise RuntimeError(f"output already exists: {path}; use --overwrite to replace it")
    candidates, errors = load_candidates(args.input)
    summary = summarize(candidates)
    document = {
        "formatVersion": 1,
        "name": args.name,
        "inputs": [str(path) for path in args.input],
        "errors": errors,
        "summary": summary,
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(markdown_summary(args.name, summary), encoding="utf-8")
    print(f"Analyzed {len(candidates)} contracts", file=sys.stderr)
    if errors:
        print(f"Skipped {len(errors)} invalid files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
