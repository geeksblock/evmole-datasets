#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "duckdb>=1.3,<2",
# ]
# ///

"""Generate an EVMole benchmark dataset from a Sourcify Parquet cache."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import re
import shutil
import sys
import uuid
from pathlib import Path

import duckdb


TABLES = (
    "code",
    "sources",
    "contracts",
    "compiled_contracts_sources",
    "contract_deployments",
    "compiled_contracts",
    "verified_contracts",
)
SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)")
DECLARATION_RE = re.compile(
    r"\b(?:(abstract)\s+)?(contract|interface|library)\s+"
    r"([A-Za-z_$][A-Za-z0-9_$]*)(?![A-Za-z0-9_$])"
)
EXCLUDED_CODE_PREFIXES = (bytes.fromhex("73"), bytes.fromhex("608060405230"))


def semantic_version(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(value)
    if not match:
        raise argparse.ArgumentTypeError(f"expected a semantic version, got {value!r}")
    return tuple(map(int, match.groups()))  # type: ignore[return-value]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True, help="Sourcify Parquet cache")
    parser.add_argument("--output", type=Path, required=True, help="output directory")
    parser.add_argument(
        "--count", type=int, default=1000, help="number of contracts to generate (default: 1000)"
    )
    parser.add_argument("--chain-id", type=int, default=1, help="chain ID (default: 1)")
    parser.add_argument("--compiler", required=True, help="compiler name, for example solc or vyper")
    parser.add_argument(
        "--compiler-version", action="append", type=semantic_version, default=[], metavar="VERSION",
        help="exact semantic version; may be repeated",
    )
    parser.add_argument("--compiler-version-min", type=semantic_version, metavar="VERSION")
    parser.add_argument("--compiler-version-max", type=semantic_version, metavar="VERSION")
    parser.add_argument("--bytecode-size-min", type=int, default=1, metavar="BYTES")
    parser.add_argument("--bytecode-size-max", type=int, default=24576, metavar="BYTES")
    parser.add_argument("--functions-min", type=int, default=1, metavar="COUNT")
    parser.add_argument("--functions-max", type=int, metavar="COUNT")
    parser.add_argument("--seed", default="evmole", help="deterministic sampling seed")
    parser.add_argument("--match", choices=("any", "exact"), default="exact")
    parser.add_argument("--allow-duplicates", action="store_true", help="retain duplicate runtime bytecodes")
    parser.add_argument(
        "--include-storage-layout",
        action="store_true",
        help="include storageLayout and transientStorageLayout compilation artifacts",
    )
    parser.add_argument(
        "--candidate-factor", type=float, default=4.0, metavar="FACTOR",
        help="deployments to sample per requested contract (default: 4)",
    )
    parser.add_argument(
        "--memory-limit", default="4GB", help="DuckDB memory limit (default: 4GB)"
    )
    parser.add_argument("--temp-directory", type=Path, help="DuckDB spill directory (default: CACHE/.duckdb-tmp)")
    parser.add_argument("--write-batch-size", type=int, default=1000, help="hydration batch size (default: 1000)")
    parser.add_argument("--overwrite", action="store_true", help="replace an existing output directory")
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")
    if args.write_batch_size < 1:
        parser.error("--write-batch-size must be at least 1")
    if not math.isfinite(args.candidate_factor) or args.candidate_factor < 1:
        parser.error("--candidate-factor must be a finite number of at least 1")
    if args.chain_id < 0:
        parser.error("--chain-id cannot be negative")
    for name in ("bytecode_size_min", "bytecode_size_max", "functions_min", "functions_max"):
        value = getattr(args, name)
        if value is not None and value < 0:
            parser.error(f"--{name.replace('_', '-')} cannot be negative")
    if args.bytecode_size_min > args.bytecode_size_max:
        parser.error("--bytecode-size-min cannot exceed --bytecode-size-max")
    if args.functions_max is not None and args.functions_min > args.functions_max:
        parser.error("--functions-min cannot exceed --functions-max")
    if args.compiler_version_min and args.compiler_version_max:
        if args.compiler_version_min > args.compiler_version_max:
            parser.error("--compiler-version-min cannot exceed --compiler-version-max")
    return args


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def parquet_expression(cache: Path, table: str) -> str:
    paths = sorted((cache / table).glob("*.parquet"))
    if not paths:
        raise RuntimeError(f"no Parquet files found for table {table!r} under {cache / table}")
    values = ", ".join(sql_string(str(path.resolve())) for path in paths)
    return f"read_parquet([{values}])"


def semver_comparison(operator: str, version: tuple[int, int, int]) -> str:
    major, minor, patch = version
    if operator == ">=":
        return (
            f"(version_major > {major} OR "
            f"(version_major = {major} AND version_minor > {minor}) OR "
            f"(version_major = {major} AND version_minor = {minor} AND version_patch >= {patch}))"
        )
    if operator == "<=":
        return (
            f"(version_major < {major} OR "
            f"(version_major = {major} AND version_minor < {minor}) OR "
            f"(version_major = {major} AND version_minor = {minor} AND version_patch <= {patch}))"
        )
    raise ValueError(f"unsupported semantic-version operator: {operator}")


def sampling_seed(value: str) -> int:
    """Map an arbitrary seed to the integer accepted by DuckDB."""
    return int.from_bytes(hashlib.sha256(value.encode()).digest()[:4], "big") & 0x7FFF_FFFF


def blob_has_prefix(expression: str, prefix: bytes) -> str:
    """Build a BLOB prefix check without expanding the BLOB to hexadecimal text."""
    bits = "".join(f"{byte:08b}" for byte in prefix)
    comparisons = [
        f"get_bit({expression}::BIT, {index}) = {bit}"
        for index, bit in enumerate(bits)
    ]
    comparison = " AND ".join(comparisons)
    return f"(CASE WHEN octet_length({expression}) >= {len(prefix)} THEN {comparison} ELSE false END)"


def strip_comments_and_strings(source: str) -> str:
    result = list(source)
    index = 0
    state = "code"
    quote = ""
    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if state == "code":
            if char == "/" and following == "/":
                result[index] = result[index + 1] = " "
                index += 2
                state = "line-comment"
                continue
            if char == "/" and following == "*":
                result[index] = result[index + 1] = " "
                index += 2
                state = "block-comment"
                continue
            if char in {'"', "'"}:
                result[index] = " "
                quote = char
                state = "string"
        elif state == "line-comment":
            if char == "\n":
                state = "code"
            else:
                result[index] = " "
        elif state == "block-comment":
            if char == "*" and following == "/":
                result[index] = result[index + 1] = " "
                index += 2
                state = "code"
                continue
            if char != "\n":
                result[index] = " "
        elif state == "string":
            if char == "\\" and following:
                result[index] = result[index + 1] = " "
                index += 2
                continue
            if char == quote:
                state = "code"
            if char != "\n":
                result[index] = " "
        index += 1
    return "".join(result)


def declaration_kinds(source: str, contract_name: str) -> set[str]:
    return {
        kind
        for _abstract, kind, name in DECLARATION_RE.findall(source)
        if name == contract_name
    }


def contract_kind(source: str, contract_name: str) -> str:
    matches = declaration_kinds(strip_comments_and_strings(source), contract_name)
    if not matches:
        # Some verified flattened sources contain lexer-hostile text outside the
        # compiled declaration. A unique raw match is still safe: compilation
        # proves that a declaration with the exact target name exists.
        matches = declaration_kinds(source, contract_name)
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one declaration kind for {contract_name!r}, found {sorted(matches)}"
        )
    return matches.pop()


def version_filter(args: argparse.Namespace) -> str:
    version_conditions: list[str] = []
    if args.compiler_version:
        exact = [
            f"(version_major = {major} AND version_minor = {minor} AND version_patch = {patch})"
            for major, minor, patch in args.compiler_version
        ]
        version_conditions.append("(" + " OR ".join(exact) + ")")
    if args.compiler_version_min:
        version_conditions.append(semver_comparison(">=", args.compiler_version_min))
    if args.compiler_version_max:
        version_conditions.append(semver_comparison("<=", args.compiler_version_max))
    return " AND ".join(version_conditions) if version_conditions else "true"


def select_candidates(
    connection: duckdb.DuckDBPyConnection,
    args: argparse.Namespace,
    tables: dict[str, str],
) -> tuple[list[tuple], list[str], dict[str, int]]:
    """Select candidates while every hash join has one bounded input."""
    sample_count = math.ceil(args.count * args.candidate_factor)
    repeatable_seed = sampling_seed(args.seed)
    exact_match_condition = "AND vc.runtime_metadata_match = true" if args.match == "exact" else ""
    function_max_condition = "AND function_count <= ?" if args.functions_max is not None else ""
    excluded_code_condition = " AND ".join(
        f"NOT {blob_has_prefix('code.code', prefix)}" for prefix in EXCLUDED_CODE_PREFIXES
    )

    connection.execute(
        f"""
        CREATE TEMP TABLE sampled_deployments AS
        SELECT deployment_id, address, contract_id
        FROM (
            SELECT DISTINCT
                deployments.id AS deployment_id,
                deployments.address,
                deployments.contract_id
            FROM {tables['contract_deployments']} AS deployments
            JOIN {tables['verified_contracts']} AS vc
                ON vc.deployment_id = deployments.id
            JOIN {tables['compiled_contracts']} AS cc
                ON cc.id = vc.compilation_id
            WHERE deployments.chain_id = ?
              AND vc.runtime_match = true
              {exact_match_condition}
              AND lower(cc.compiler) = lower(?)
        ) AS compiler_deployments
        USING SAMPLE reservoir({sample_count} ROWS) REPEATABLE({repeatable_seed})
        """,
        [args.chain_id, args.compiler],
    )
    sampled_deployment_count = connection.execute(
        "SELECT count(*) FROM sampled_deployments"
    ).fetchone()[0]

    connection.execute(
        f"""
        CREATE TEMP TABLE matched_verifications AS
        SELECT
            vc.id AS verified_contract_id,
            vc.compilation_id,
            sampled.deployment_id,
            sampled.address,
            sampled.contract_id
        FROM {tables['verified_contracts']} AS vc
        JOIN sampled_deployments AS sampled ON sampled.deployment_id = vc.deployment_id
        WHERE vc.runtime_match = true
          {exact_match_condition}
        """
    )
    matched_verification_count = connection.execute(
        "SELECT count(*) FROM matched_verifications"
    ).fetchone()[0]
    connection.execute("DROP TABLE sampled_deployments")

    compiled_parameters: list = [args.compiler, args.functions_min]
    if args.functions_max is not None:
        compiled_parameters.append(args.functions_max)
    connection.execute(
        f"""
        CREATE TEMP TABLE compiled_candidates AS
        WITH compiled_parsed AS (
            SELECT
                matched.verified_contract_id,
                matched.compilation_id,
                matched.deployment_id,
                matched.address,
                matched.contract_id,
                cc.compilation_artifacts,
                try_cast(regexp_extract(cc.version, '^[vV]?([0-9]+)\\.([0-9]+)\\.([0-9]+)', 1) AS INTEGER)
                    AS version_major,
                try_cast(regexp_extract(cc.version, '^[vV]?([0-9]+)\\.([0-9]+)\\.([0-9]+)', 2) AS INTEGER)
                    AS version_minor,
                try_cast(regexp_extract(cc.version, '^[vV]?([0-9]+)\\.([0-9]+)\\.([0-9]+)', 3) AS INTEGER)
                    AS version_patch
            FROM {tables['compiled_contracts']} AS cc
            JOIN matched_verifications AS matched ON matched.compilation_id = cc.id
            WHERE lower(cc.compiler) = lower(?)
        ),
        compiled_with_function_count AS (
            SELECT
                * EXCLUDE (compilation_artifacts, version_major, version_minor, version_patch),
                list_count(
                    list_filter(
                        json_extract_string(
                            coalesce(compilation_artifacts, '{{}}'),
                            '$.abi[*].type'
                        ),
                        abi_type -> abi_type = 'function'
                    )
                ) AS function_count
            FROM compiled_parsed
            WHERE {version_filter(args)}
        )
        SELECT
            *
        FROM compiled_with_function_count
        WHERE function_count >= ? {function_max_condition}
        """,
        compiled_parameters,
    )
    compiled_candidate_count = connection.execute(
        "SELECT count(*) FROM compiled_candidates"
    ).fetchone()[0]
    connection.execute("DROP TABLE matched_verifications")

    connection.execute(
        f"""
        CREATE TEMP TABLE contract_candidates AS
        SELECT candidates.*, contracts.runtime_code_hash
        FROM {tables['contracts']} AS contracts
        JOIN compiled_candidates AS candidates ON candidates.contract_id = contracts.id
        """
    )
    connection.execute("DROP TABLE compiled_candidates")

    result = connection.execute(
        f"""
        SELECT
            candidates.verified_contract_id,
            candidates.compilation_id,
            candidates.deployment_id,
            candidates.address,
            candidates.runtime_code_hash,
            octet_length(code.code) AS bytecode_size,
            candidates.function_count
        FROM {tables['code']} AS code
        JOIN contract_candidates AS candidates ON candidates.runtime_code_hash = code.code_hash
        WHERE code.code IS NOT NULL
          AND octet_length(code.code) > 0
          AND {excluded_code_condition}
          AND octet_length(code.code) BETWEEN ? AND ?
        """,
        [args.bytecode_size_min, args.bytecode_size_max],
    )
    rows = result.fetchall()
    columns = [item[0] for item in result.description]
    connection.execute("DROP TABLE contract_candidates")
    stats = {
        "sampled_deployments": sampled_deployment_count,
        "matched_verifications": matched_verification_count,
        "compiled_candidates": compiled_candidate_count,
        "bytecode_candidates": len(rows),
    }
    return rows, columns, stats


def json_value(value, fallback):
    if value is None:
        return fallback
    if isinstance(value, str):
        return json.loads(value)
    return value


def prepare_destination(output: Path, overwrite: bool) -> Path:
    validate_destination(output, overwrite)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.parent / f".{output.name}.tmp-{uuid.uuid4().hex}"
    temporary.mkdir()
    return temporary


def validate_destination(output: Path, overwrite: bool) -> None:
    if output.exists():
        if not overwrite:
            raise RuntimeError(f"output already exists: {output}; use --overwrite to replace it")
        if not output.is_dir():
            raise RuntimeError(f"output exists and is not a directory: {output}")


def deduplicate_rows(
    rows: list[tuple],
    columns: list[str],
    limit: int,
    allow_duplicates: bool,
) -> list[tuple]:
    address_index = columns.index("address")
    runtime_hash_index = columns.index("runtime_code_hash")
    addresses: set[bytes] = set()
    runtime_hashes: set[bytes] = set()
    result: list[tuple] = []
    for row in rows:
        address = bytes(row[address_index])
        runtime_hash = bytes(row[runtime_hash_index])
        if address in addresses or (not allow_duplicates and runtime_hash in runtime_hashes):
            continue
        addresses.add(address)
        runtime_hashes.add(runtime_hash)
        result.append(row)
        if len(result) == limit:
            break
    return result


def populate_contract_kinds(
    connection: duckdb.DuckDBPyConnection,
    tables: dict[str, str],
) -> collections.Counter[str]:
    connection.execute(
        """
        CREATE TEMP TABLE contract_kinds (
            compilation_id VARCHAR PRIMARY KEY,
            contract_kind VARCHAR
        )
        """
    )
    connection.execute(
        """
        INSERT INTO contract_kinds
        SELECT compilation_id, 'contract'
        FROM compilation_details
        WHERE lower(compiler) <> 'solc'
        """
    )
    solc_compilations = {
        row[0]: row[1]
        for row in connection.execute(
            """
            SELECT compilation_id, fully_qualified_name
            FROM compilation_details
            WHERE lower(compiler) = 'solc'
            """
        ).fetchall()
    }
    solc_count = len(solc_compilations)
    if not solc_count:
        return collections.Counter({"contract": connection.execute(
            "SELECT count(*) FROM contract_kinds"
        ).fetchone()[0]})

    connection.execute(
        f"""
        CREATE TEMP TABLE target_source_hashes AS
        SELECT
            details.compilation_id,
            details.contract_name,
            details.fully_qualified_name,
            links.source_hash
        FROM {tables['compiled_contracts_sources']} AS links
        JOIN compilation_details AS details
          ON details.compilation_id = links.compilation_id
         AND regexp_replace(details.fully_qualified_name, ':[^:]*$', '') = links.path
        WHERE lower(details.compiler) = 'solc'
        """
    )
    result = connection.execute(
        f"""
        SELECT targets.*, sources.content
        FROM {tables['sources']} AS sources
        JOIN target_source_hashes AS targets
          ON targets.source_hash = sources.source_hash
        """
    )
    columns = [item[0] for item in result.description]
    resolved: set[str] = set()
    kind_rows: list[tuple[str, str]] = []
    counts: collections.Counter[str] = collections.Counter()
    while batch := result.fetchmany(1000):
        for values in batch:
            row = dict(zip(columns, values, strict=True))
            compilation_id = row["compilation_id"]
            if compilation_id in resolved:
                raise RuntimeError(
                    f"multiple target sources for compilation {compilation_id}"
                )
            kind = contract_kind(row["content"], row["contract_name"])
            resolved.add(compilation_id)
            kind_rows.append((compilation_id, kind))
            counts[kind] += 1
    connection.execute("DROP TABLE target_source_hashes")
    if len(resolved) != solc_count:
        missing = [
            (compilation_id, solc_compilations[compilation_id])
            for compilation_id in sorted(set(solc_compilations) - resolved)[:10]
        ]
        raise RuntimeError(
            f"resolved source kinds for {len(resolved)} of {solc_count} Solidity "
            f"compilations; missing examples: {missing}"
        )
    connection.executemany("INSERT INTO contract_kinds VALUES (?, ?)", kind_rows)
    counts["contract"] += connection.execute(
        "SELECT count(*) FROM compilation_details WHERE lower(compiler) <> 'solc'"
    ).fetchone()[0]
    return counts


def hydrate_and_write(
    connection: duckdb.DuckDBPyConnection,
    tables: dict[str, str],
    selected: list[tuple],
    selected_columns: list[str],
    destination: Path,
    batch_size: int,
    chain_id: int,
    include_storage_layout: bool,
    requested_count: int,
) -> tuple[int, collections.Counter[str]]:
    indexes = {name: selected_columns.index(name) for name in selected_columns}
    connection.execute(
        """
        CREATE TEMP TABLE selected_contracts (
            selection_order BIGINT,
            verified_contract_id BIGINT,
            compilation_id VARCHAR,
            chain_id BIGINT,
            address BLOB,
            runtime_code_hash BLOB,
            bytecode_size BIGINT,
            function_count BIGINT
        )
        """
    )
    if selected:
        connection.executemany(
            "INSERT INTO selected_contracts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    selection_order,
                    row[indexes["verified_contract_id"]],
                    row[indexes["compilation_id"]],
                    chain_id,
                    row[indexes["address"]],
                    row[indexes["runtime_code_hash"]],
                    row[indexes["bytecode_size"]],
                    row[indexes["function_count"]],
                )
                for selection_order, row in enumerate(selected)
            ],
        )

    connection.execute(
        """
        CREATE TEMP TABLE selected_compilation_ids AS
        SELECT DISTINCT compilation_id
        FROM selected_contracts
        """
    )
    connection.execute(
        f"""
        CREATE TEMP TABLE compilation_details AS
        SELECT
            cc.id AS compilation_id,
            cc.compiler,
            cc.version AS compiler_version,
            cc.language,
            cc.name AS contract_name,
            cc.fully_qualified_name,
            cc.compiler_settings,
            json_extract(cc.compilation_artifacts, '$.abi') AS abi,
            json_extract(cc.compilation_artifacts, '$.storageLayout') AS storage_layout,
            json_extract(
                cc.compilation_artifacts,
                '$.transientStorageLayout'
            ) AS transient_storage_layout
        FROM {tables['compiled_contracts']} AS cc
        JOIN selected_compilation_ids AS selected ON selected.compilation_id = cc.id
        """
    )
    connection.execute("DROP TABLE selected_compilation_ids")
    kind_counts = populate_contract_kinds(connection, tables)

    result = connection.execute(
        f"""
        SELECT
            selected.verified_contract_id,
            selected.compilation_id,
            selected.chain_id,
            selected.address,
            details.compiler,
            details.compiler_version,
            details.language,
            details.contract_name,
            details.fully_qualified_name,
            details.compiler_settings,
            details.abi,
            details.storage_layout,
            details.transient_storage_layout,
            kinds.contract_kind,
            selected.runtime_code_hash,
            code.code,
            selected.bytecode_size,
            selected.function_count
        FROM {tables['code']} AS code
        JOIN selected_contracts AS selected ON selected.runtime_code_hash = code.code_hash
        JOIN compilation_details AS details ON details.compilation_id = selected.compilation_id
        JOIN contract_kinds AS kinds ON kinds.compilation_id = selected.compilation_id
        WHERE kinds.contract_kind <> 'library'
        ORDER BY selected.selection_order
        """
    )
    columns = [item[0] for item in result.description]
    written = 0
    while batch := result.fetchmany(batch_size):
        for values in batch:
            row = dict(zip(columns, values, strict=True))
            address = "0x" + bytes(row["address"]).hex()
            code = "0x" + bytes(row["code"]).hex()
            runtime_hash = "0x" + bytes(row["runtime_code_hash"]).hex()
            document = {
                "code": code,
                "abi": json_value(row["abi"], []),
                "_meta": {
                    "source": "sourcify-parquet-v2",
                    "chainId": row["chain_id"],
                    "address": address,
                    "verifiedContractId": row["verified_contract_id"],
                    "compilationId": row["compilation_id"],
                    "compiler": row["compiler"],
                    "compilerVersion": row["compiler_version"],
                    "language": row["language"],
                    "contractName": row["contract_name"],
                    "fullyQualifiedName": row["fully_qualified_name"],
                    "contractKind": row["contract_kind"],
                    "compilerSettings": json_value(row["compiler_settings"], {}),
                    "runtimeCodeHash": runtime_hash,
                    "bytecodeSize": row["bytecode_size"],
                    "functionCount": row["function_count"],
                },
            }
            if include_storage_layout:
                document["storageLayout"] = json_value(row["storage_layout"], {})
                document["transientStorageLayout"] = json_value(
                    row["transient_storage_layout"], {}
                )
            with (destination / f"{address}.json").open("w", encoding="utf-8") as handle:
                json.dump(document, handle, separators=(",", ":"))
                handle.write("\n")
            written += 1
            if written == requested_count:
                break
        if written == requested_count:
            break
    connection.execute("DROP TABLE contract_kinds")
    connection.execute("DROP TABLE compilation_details")
    connection.execute("DROP TABLE selected_contracts")
    return written, kind_counts


def main() -> int:
    args = parse_args()
    validate_destination(args.output, args.overwrite)
    tables = {table: parquet_expression(args.cache, table) for table in TABLES}

    connection = duckdb.connect()
    temporary: Path | None = None
    try:
        connection.execute("SET threads TO 4")
        connection.execute("SET preserve_insertion_order = false")
        temp_directory = args.temp_directory or (args.cache / ".duckdb-tmp")
        temp_directory.mkdir(parents=True, exist_ok=True)
        connection.execute(f"SET temp_directory = {sql_string(str(temp_directory.resolve()))}")
        connection.execute(f"SET memory_limit = {sql_string(args.memory_limit)}")

        selected, selected_columns, selection_stats = select_candidates(connection, args, tables)
        reserve = max(250, math.ceil(args.count * 0.05))
        selected = deduplicate_rows(
            selected,
            selected_columns,
            args.count + reserve,
            args.allow_duplicates,
        )
        temporary = prepare_destination(args.output, args.overwrite)
        written, kind_counts = hydrate_and_write(
            connection,
            tables,
            selected,
            selected_columns,
            temporary,
            args.write_batch_size,
            args.chain_id,
            args.include_storage_layout,
            args.count,
        )
        if args.output.exists():
            shutil.rmtree(args.output)
        os.replace(temporary, args.output)
        temporary = None
    except BaseException:
        if temporary is not None:
            shutil.rmtree(temporary, ignore_errors=True)
        raise
    finally:
        connection.close()

    print(f"Wrote {written} contracts to {args.output} (requested {args.count})", file=sys.stderr)
    if kind_counts["library"]:
        print(
            f"Excluded {kind_counts['library']} source-classified Solidity libraries",
            file=sys.stderr,
        )
    if written < args.count:
        match_description = "runtime + metadata" if args.match == "exact" else "runtime"
        print("Selection summary:", file=sys.stderr)
        print(
            f"  candidate deployments on chain {args.chain_id}: "
            f"{selection_stats['sampled_deployments']}",
            file=sys.stderr,
        )
        print(
            f"  {match_description} verification matches: "
            f"{selection_stats['matched_verifications']}",
            file=sys.stderr,
        )
        print(
            f"  compiler/version/function matches: "
            f"{selection_stats['compiled_candidates']}",
            file=sys.stderr,
        )
        print(
            f"  bytecode filter matches: {selection_stats['bytecode_candidates']}",
            file=sys.stderr,
        )
        print(f"  selected after deduplication: {written}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (duckdb.Error, OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
