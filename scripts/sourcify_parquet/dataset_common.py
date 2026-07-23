"""Shared analysis and selection helpers for Sourcify benchmark datasets."""

from __future__ import annotations

import collections
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)")


@dataclass(frozen=True)
class Candidate:
    path: Path
    address: str
    compiler: str
    compiler_version: str
    contract_kind: str
    runtime_hash: str
    normalized_hash: str
    bytecode_size: int
    function_count: int
    labels: frozenset[str]
    flow_score: int
    storage_layout: bool


def bucket(value: int, limits: tuple[int, ...]) -> str:
    lower = 0
    for upper in limits:
        if value <= upper:
            return f"{lower}-{upper}"
        lower = upper + 1
    return f"{lower}+"


def strip_cbor_metadata(code: bytes) -> bytes:
    """Strip a plausible terminal length-suffixed CBOR map.

    This intentionally does not try to decode CBOR. Requiring the payload to
    begin with a map marker prevents arbitrary two-byte suffixes from removing
    most normal bytecode tails.
    """
    if len(code) < 3:
        return code
    length = int.from_bytes(code[-2:], "big")
    start = len(code) - length - 2
    if start < 0 or start >= len(code) - 2:
        return code
    first = code[start]
    if 0xA0 <= first <= 0xBF:
        return code[:start]
    return code


def opcode_counts(code: bytes) -> collections.Counter[int]:
    result: collections.Counter[int] = collections.Counter()
    offset = 0
    while offset < len(code):
        opcode = code[offset]
        result[opcode] += 1
        offset += 1
        if 0x60 <= opcode <= 0x7F:
            offset += opcode - 0x5F
    return result


def optimizer_labels(settings: dict) -> set[str]:
    result: set[str] = set()
    optimizer = settings.get("optimizer")
    if isinstance(optimizer, dict):
        enabled = optimizer.get("enabled")
        result.add(f"optimizer:{str(enabled).lower()}" if isinstance(enabled, bool) else "optimizer:unknown")
        runs = optimizer.get("runs")
        if isinstance(runs, int):
            result.add(f"optimizer-runs:{bucket(runs, (0, 1, 199, 200, 999, 9999))}")
    else:
        result.add("optimizer:unknown")

    via_ir = settings.get("viaIR")
    result.add(f"via-ir:{str(via_ir).lower()}" if isinstance(via_ir, bool) else "via-ir:unknown")
    evm_version = settings.get("evmVersion")
    if isinstance(evm_version, str) and evm_version:
        result.add(f"evm-version:{evm_version}")
    optimize = settings.get("optimize")
    if isinstance(optimize, str):
        result.add(f"vyper-optimize:{optimize}")
    elif isinstance(optimize, bool):
        result.add(f"vyper-optimize:{str(optimize).lower()}")
    return result


def abi_labels(abi: list) -> tuple[set[str], int]:
    result: set[str] = set()
    functions = [entry for entry in abi if isinstance(entry, dict) and entry.get("type") == "function"]
    for function in functions:
        mutability = function.get("stateMutability")
        if isinstance(mutability, str):
            result.add(f"mutability:{mutability}")
        inputs = function.get("inputs")
        if not isinstance(inputs, list):
            inputs = []
        result.add(f"arguments:{bucket(len(inputs), (0, 1, 2, 3, 5, 8))}")
        pending = [(item, 0) for item in inputs if isinstance(item, dict)]
        max_depth = 0
        while pending:
            item, depth = pending.pop()
            max_depth = max(max_depth, depth)
            abi_type = item.get("type", "")
            if not isinstance(abi_type, str):
                continue
            if abi_type.startswith("tuple"):
                result.add("abi:tuple")
            if abi_type.endswith("[]"):
                result.add("abi:dynamic-array")
            if re.search(r"\[[0-9]+\]", abi_type):
                result.add("abi:fixed-array")
            if abi_type in {"bytes", "string"}:
                result.add("abi:dynamic-bytes-or-string")
            if re.fullmatch(r"bytes[0-9]+", abi_type):
                result.add("abi:fixed-bytes")
            if re.fullmatch(r"int[0-9]*", abi_type):
                result.add("abi:signed-int")
            if abi_type == "function":
                result.add("abi:function")
            components = item.get("components")
            if isinstance(components, list):
                pending.extend((component, depth + 1) for component in components if isinstance(component, dict))
        result.add(f"abi-depth:{bucket(max_depth, (0, 1, 2, 3))}")
    return result, len(functions)


def storage_labels(document: dict) -> tuple[set[str], bool]:
    result: set[str] = set()
    layout = document.get("storageLayout")
    if not isinstance(layout, dict):
        return result, False
    entries = layout.get("storage")
    types = layout.get("types")
    entries = entries if isinstance(entries, list) else []
    types = types if isinstance(types, dict) else {}
    result.add(f"storage-entries:{bucket(len(entries), (0, 1, 3, 7, 15, 31, 63))}")
    result.add(f"storage-types:{bucket(len(types), (0, 1, 3, 7, 15, 31))}")
    if any(isinstance(entry, dict) and entry.get("offset", 0) not in (0, "0") for entry in entries):
        result.add("storage:packed")
    for information in types.values():
        if not isinstance(information, dict):
            continue
        encoding = information.get("encoding")
        if isinstance(encoding, str):
            result.add(f"storage-encoding:{encoding}")
        label = information.get("label")
        if isinstance(label, str) and label.startswith("struct "):
            result.add("storage:struct")
    transient = document.get("transientStorageLayout")
    if isinstance(transient, dict) and transient.get("storage"):
        result.add("storage:transient")
    return result, True


def load_candidate(path: Path) -> Candidate:
    document = json.loads(path.read_text(encoding="utf-8"))
    code_value = document.get("code", document.get("runtimeBytecode"))
    if not isinstance(code_value, str) or not code_value.startswith("0x"):
        raise ValueError("missing 0x-prefixed code or runtimeBytecode")
    code = bytes.fromhex(code_value[2:])
    executable = strip_cbor_metadata(code)
    opcodes = opcode_counts(executable)
    metadata = document.get("_meta")
    metadata = metadata if isinstance(metadata, dict) else {}
    compiler = str(metadata.get("compiler", "unknown")).lower()
    version = str(metadata.get("compilerVersion", "unknown"))
    contract_kind = metadata.get("contractKind")
    if contract_kind not in {"contract", "interface", "library"}:
        raise ValueError("missing or invalid _meta.contractKind; regenerate with generate.py")
    address = str(metadata.get("address", path.stem))
    settings = metadata.get("compilerSettings")
    settings = settings if isinstance(settings, dict) else {}
    abi = document.get("abi")
    abi = abi if isinstance(abi, list) else []

    labels: set[str] = {
        f"compiler:{compiler}",
        f"contract-kind:{contract_kind}",
        f"bytecode-size:{bucket(len(code), (127, 255, 511, 1023, 2047, 4095, 8191, 16383, 24575))}",
    }
    match = SEMVER_RE.match(version)
    if match:
        major, minor, patch = match.groups()
        labels.add(f"compiler-minor:{compiler}:{major}.{minor}")
        labels.add(f"compiler-era:{compiler}:{major}")
        labels.add(
            f"compiler-patch-bucket:{compiler}:{bucket(int(patch), (0, 4, 9, 19))}"
        )
    labels.update(optimizer_labels(settings))
    abi_features, function_count = abi_labels(abi)
    labels.update(abi_features)
    labels.add(f"functions:{bucket(function_count, (0, 1, 4, 9, 19, 49, 99))}")

    named_opcodes = {
        0x5F: "push0",
        0x5E: "mcopy",
        0x5C: "tload",
        0x5D: "tstore",
        0x54: "sload",
        0x55: "sstore",
        0xF4: "delegatecall",
        0xFA: "staticcall",
        0xFF: "selfdestruct",
        0xF0: "create",
        0xF5: "create2",
    }
    for opcode, name in named_opcodes.items():
        if opcodes[opcode]:
            labels.add(f"opcode:{name}")
    jumps = opcodes[0x56] + opcodes[0x57]
    jumpdests = opcodes[0x5B]
    labels.add(f"jumps:{bucket(jumps, (0, 4, 15, 63, 255, 1023))}")
    labels.add(f"jumpdests:{bucket(jumpdests, (0, 4, 15, 63, 255, 1023))}")
    storage_features, has_storage_layout = storage_labels(document)
    labels.update(storage_features)

    runtime_hash = metadata.get("runtimeCodeHash")
    if not isinstance(runtime_hash, str):
        runtime_hash = "0x" + hashlib.sha256(code).hexdigest()
    normalized_hash = hashlib.sha256(executable).hexdigest()
    flow_score = len(executable) + jumps * 48 + jumpdests * 24
    return Candidate(
        path=path,
        address=address,
        compiler=compiler,
        compiler_version=version,
        contract_kind=contract_kind,
        runtime_hash=runtime_hash,
        normalized_hash=normalized_hash,
        bytecode_size=len(code),
        function_count=function_count,
        labels=frozenset(labels),
        flow_score=flow_score,
        storage_layout=has_storage_layout,
    )


def load_candidates(inputs: Iterable[Path]) -> tuple[list[Candidate], list[str]]:
    candidates: list[Candidate] = []
    errors: list[str] = []
    for directory in inputs:
        for path in sorted(directory.glob("*.json")):
            try:
                candidates.append(load_candidate(path))
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
                errors.append(f"{path}: {error}")
    return candidates, errors


def stable_key(candidate: Candidate, seed: str) -> str:
    value = f"{seed}\0{candidate.normalized_hash}\0{candidate.address.lower()}"
    return hashlib.sha256(value.encode()).hexdigest()


def deduplicate(candidates: Iterable[Candidate], seed: str) -> list[Candidate]:
    result: dict[str, Candidate] = {}
    for candidate in candidates:
        previous = result.get(candidate.normalized_hash)
        if previous is None or stable_key(candidate, seed) < stable_key(previous, seed):
            result[candidate.normalized_hash] = candidate
    return list(result.values())


def coverage_select(
    candidates: list[Candidate],
    count: int,
    seed: str,
    target: int,
    *,
    flow: bool = False,
) -> list[Candidate]:
    """Select candidates to fill multi-label quotas, then fill deterministically."""
    available: dict[str, list[Candidate]] = collections.defaultdict(list)
    for candidate in candidates:
        for label in candidate.labels:
            available[label].append(candidate)
    for values in available.values():
        values.sort(key=lambda candidate: stable_key(candidate, seed))

    deficits = {label: min(target, len(values)) for label, values in available.items()}
    selected: list[Candidate] = []
    selected_hashes: set[str] = set()

    while len(selected) < count:
        active = [label for label, deficit in deficits.items() if deficit > 0]
        if not active:
            break
        active.sort(key=lambda label: (len(available[label]), -deficits[label], label))
        progress = False
        for label in active:
            if len(selected) >= count or deficits[label] <= 0:
                continue
            choices = [
                candidate
                for candidate in available[label]
                if candidate.normalized_hash not in selected_hashes
            ][:128]
            if not choices:
                deficits[label] = 0
                continue

            def score(candidate: Candidate) -> tuple[float, int, str]:
                coverage = sum(
                    1 / max(1, len(available[item]))
                    for item in candidate.labels
                    if deficits.get(item, 0) > 0
                )
                flow_value = candidate.flow_score if flow else 0
                return coverage, flow_value, stable_key(candidate, seed)

            chosen = max(choices, key=score)
            selected.append(chosen)
            selected_hashes.add(chosen.normalized_hash)
            for item in chosen.labels:
                if deficits.get(item, 0) > 0:
                    deficits[item] -= 1
            progress = True
        if not progress:
            break

    remaining = [
        candidate for candidate in candidates if candidate.normalized_hash not in selected_hashes
    ]
    if flow:
        remaining.sort(key=lambda candidate: (-candidate.flow_score, stable_key(candidate, seed)))
    else:
        remaining.sort(key=lambda candidate: stable_key(candidate, seed))
    selected.extend(remaining[: max(0, count - len(selected))])
    return selected


def select_candidates(
    candidates: list[Candidate],
    strategy: str,
    count: int,
    seed: str,
    coverage_target: int,
) -> list[Candidate]:
    candidates = deduplicate(candidates, seed)
    if strategy == "storage":
        candidates = [candidate for candidate in candidates if candidate.storage_layout]
    if strategy == "random":
        return sorted(candidates, key=lambda candidate: stable_key(candidate, seed))[:count]
    if strategy == "coverage":
        return coverage_select(candidates, count, seed, coverage_target)
    if strategy == "storage":
        return coverage_select(candidates, count, seed, coverage_target)
    if strategy == "flow":
        return coverage_select(candidates, count, seed, coverage_target, flow=True)
    raise ValueError(f"unknown strategy: {strategy}")


def percentile(values: list[int], percent: int) -> int:
    values = sorted(values)
    if not values:
        return 0
    index = max(0, min(len(values) - 1, math.ceil(len(values) * percent / 100) - 1))
    return values[index]


def summarize(candidates: list[Candidate]) -> dict:
    label_counts: collections.Counter[str] = collections.Counter(
        label for candidate in candidates for label in candidate.labels
    )
    sizes = [candidate.bytecode_size for candidate in candidates]
    functions = [candidate.function_count for candidate in candidates]
    return {
        "contracts": len(candidates),
        "compilers": dict(sorted(collections.Counter(c.compiler for c in candidates).items())),
        "uniqueRuntimeHashes": len({candidate.runtime_hash for candidate in candidates}),
        "uniqueNormalizedHashes": len({candidate.normalized_hash for candidate in candidates}),
        "bytecodeSize": {
            f"p{percent}": percentile(sizes, percent) for percent in (0, 10, 25, 50, 75, 90, 95, 99, 100)
        },
        "functionCount": {
            f"p{percent}": percentile(functions, percent) for percent in (0, 10, 25, 50, 75, 90, 95, 99, 100)
        },
        "labels": dict(sorted(label_counts.items())),
    }


def markdown_summary(name: str, summary: dict) -> str:
    lines = [
        f"# Dataset report: {name}",
        "",
        f"- Contracts: {summary['contracts']}",
        f"- Unique runtime hashes: {summary['uniqueRuntimeHashes']}",
        f"- Unique normalized hashes: {summary['uniqueNormalizedHashes']}",
        f"- Compilers: {', '.join(f'{key}={value}' for key, value in summary['compilers'].items())}",
        "",
        "## Percentiles",
        "",
        "| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for title, key in (("Bytecode bytes", "bytecodeSize"), ("ABI functions", "functionCount")):
        values = summary[key]
        lines.append(
            "| " + title + " | " + " | ".join(str(values[f"p{p}"]) for p in (0, 10, 25, 50, 75, 90, 95, 99, 100)) + " |"
        )
    lines.extend(["", "## Coverage labels", "", "| Label | Contracts |", "|---|---:|"])
    lines.extend(f"| `{label}` | {value} |" for label, value in summary["labels"].items())
    lines.append("")
    return "\n".join(lines)
