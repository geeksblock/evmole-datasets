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


TABLES = ("code", "contracts", "contract_deployments", "compiled_contracts", "verified_contracts")
SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)")
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
    parser.add_argument("--count", type=int, required=True, help="number of contracts to generate")
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
) -> tuple[list[tuple], list[str]]:
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
        SELECT id AS deployment_id, address, contract_id
        FROM (
            SELECT id, address, contract_id
            FROM {tables['contract_deployments']}
            WHERE chain_id = ?
        ) AS chain_deployments
        USING SAMPLE reservoir({sample_count} ROWS) REPEATABLE({repeatable_seed})
        """,
        [args.chain_id],
    )

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
    return rows, columns


def json_value(value, fallback):
    if value is None:
        return fallback
    if isinstance(value, str):
        return json.loads(value)
    return value


def prepare_destination(output: Path, overwrite: bool) -> Path:
    if output.exists():
        if not overwrite:
            raise RuntimeError(f"output already exists: {output}; use --overwrite to replace it")
        if not output.is_dir():
            raise RuntimeError(f"output exists and is not a directory: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.parent / f".{output.name}.tmp-{uuid.uuid4().hex}"
    temporary.mkdir()
    return temporary


def deduplicate_rows(
    rows: list[tuple],
    columns: list[str],
    count: int,
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
        if len(result) == count:
            break
    return result


def hydrate_and_write(
    connection: duckdb.DuckDBPyConnection,
    tables: dict[str, str],
    selected: list[tuple],
    selected_columns: list[str],
    destination: Path,
    batch_size: int,
    chain_id: int,
) -> int:
    indexes = {name: selected_columns.index(name) for name in selected_columns}
    connection.execute(
        """
        CREATE TEMP TABLE selected_contracts (
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
            "INSERT INTO selected_contracts VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row[indexes["verified_contract_id"]],
                    row[indexes["compilation_id"]],
                    chain_id,
                    row[indexes["address"]],
                    row[indexes["runtime_code_hash"]],
                    row[indexes["bytecode_size"]],
                    row[indexes["function_count"]],
                )
                for row in selected
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
            cc.compiler_settings,
            json_extract(cc.compilation_artifacts, '$.abi') AS abi
        FROM {tables['compiled_contracts']} AS cc
        JOIN selected_compilation_ids AS selected ON selected.compilation_id = cc.id
        """
    )
    connection.execute("DROP TABLE selected_compilation_ids")

    result = connection.execute(
        f"""
        SELECT
            selected.verified_contract_id,
            selected.chain_id,
            selected.address,
            details.compiler,
            details.compiler_version,
            details.compiler_settings,
            details.abi,
            selected.runtime_code_hash,
            code.code,
            selected.bytecode_size,
            selected.function_count
        FROM {tables['code']} AS code
        JOIN selected_contracts AS selected ON selected.runtime_code_hash = code.code_hash
        JOIN compilation_details AS details ON details.compilation_id = selected.compilation_id
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
                    "compiler": row["compiler"],
                    "compilerVersion": row["compiler_version"],
                    "compilerSettings": json_value(row["compiler_settings"], {}),
                    "runtimeCodeHash": runtime_hash,
                    "bytecodeSize": row["bytecode_size"],
                    "functionCount": row["function_count"],
                },
            }
            with (destination / f"{address}.json").open("w", encoding="utf-8") as handle:
                json.dump(document, handle, separators=(",", ":"))
                handle.write("\n")
            written += 1
    connection.execute("DROP TABLE compilation_details")
    connection.execute("DROP TABLE selected_contracts")
    return written


def main() -> int:
    args = parse_args()
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

        selected, selected_columns = select_candidates(connection, args, tables)
        selected = deduplicate_rows(
            selected,
            selected_columns,
            args.count,
            args.allow_duplicates,
        )
        temporary = prepare_destination(args.output, args.overwrite)
        written = hydrate_and_write(
            connection,
            tables,
            selected,
            selected_columns,
            temporary,
            args.write_batch_size,
            args.chain_id,
        )
        if written != len(selected):
            raise RuntimeError(f"selected {len(selected)} contracts, but hydrated {written}")
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

    print(f"Wrote {written} contracts to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (duckdb.Error, OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from None
