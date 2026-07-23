# Sourcify Parquet benchmark datasets

These scripts synchronize Sourcify's v2 Parquet export and generate the
coverage-oriented EVMole benchmark suite. Dependencies are installed
automatically by `uv`.

Run all examples from this directory.

## Dataset suite

[`suite.json`](suite.json) is the source of truth for dataset names, sizes,
candidate pools, filters, and selection seeds. It currently defines:

| Dataset | Contracts | Selection purpose |
|---|---:|---|
| `solidity-random10k` | 10,000 | Stable random Solidity baseline |
| `solidity-coverage2k` | 2,000 | Solidity compiler, ABI, settings, opcode, and size coverage |
| `vyper-coverage1k` | 1,000 | Vyper compiler and bytecode coverage |
| `storage-coverage1k` | 1,000 | Persistent and transient storage-layout coverage |
| `flow-challenge500` | 500 | Structurally difficult control-flow examples |

The suite deliberately has two kinds of general-purpose data:

- `solidity-random10k` is the dataset whose aggregate accuracy is closest to a
  population-style measurement.
- Coverage and challenge datasets intentionally oversample rare categories.
  Their results should also be reported by compiler/feature slice; their
  aggregate error percentage is not an estimate of mainnet prevalence.

`solidity-coverage2k` excludes normalized bytecodes already selected for
`solidity-random10k`, so it contributes 2,000 additional general-purpose
contracts rather than re-benchmarking part of the baseline.

All datasets use Ethereum mainnet, successful runtime matches, nonempty
deployed bytecode, and exclude Solidity libraries that the current reference
selector implementation cannot handle. Library classification resolves each
compilation target to its exact verified source and parses the top-level
declaration; bytecode-prefix checks remain as an early filter but are not
treated as authoritative. Solidity pools additionally require exact runtime
metadata matches. Vyper uses runtime matches without the metadata-match
requirement because Sourcify does not populate that flag for the eligible Vyper
deployments in this snapshot. Candidate generation allows ABI function count
zero so fallback-only and false-positive control contracts remain eligible.

## 1. Synchronize the Parquet cache

```sh
uv run sync.py --cache /mnt/sourcify-parquet
```

The synchronizer downloads missing or changed objects. It writes
`/mnt/sourcify-parquet/.sourcify-export-v2.json`, recording the upstream object
keys, sizes, ETags, and modification timestamps. On later syncs, ETags detect a
rewritten newest Parquet object even if its compressed size did not change.
The suite requires the `sources` and `compiled_contracts_sources` tables in
addition to the five bytecode, compilation, deployment, and verification
tables. These two tables connect a compilation target to its source content for
contract-kind classification.

Use `--status` to check without downloading, `--jobs` to control parallelism,
or `--prune` to remove local Parquet files absent upstream.

## 2. Generate the complete suite

```sh
uv run suite.py \
  --cache /mnt/sourcify-parquet \
  --work /mnt/evmole-dataset-work \
  --output /mnt/evmole-dataset-suite \
  --memory-limit 8GB
```

The command performs three stages:

1. `generate.py` creates bounded random candidate pools, resolves every exact
   Solidity compilation target to its verified source, and excludes targets
   declared as libraries before writing candidates. Separate legacy and modern
   Solidity pools prevent a current-version-heavy main pool from hiding old
   compiler families or recent opcodes.
2. `select_dataset.py` defensively excludes libraries, removes duplicate executable
   bytecode, and applies the
   selection strategy from `suite.json`. Storage selections are materialized
   with the legacy-compatible `runtimeBytecode` field.
3. `package.py` creates deterministic `.tar.gz` files with sorted entries,
   normalized ownership, permissions, and timestamps.

The output layout is:

```text
/mnt/evmole-dataset-suite/
├── archives/
│   ├── solidity-random10k.tar.gz
│   └── ...
├── datasets/
│   ├── solidity-random10k/
│   └── ...
├── manifests/
│   ├── solidity-random10k.json
│   └── ...
├── reports/
│   ├── solidity-random10k.md
│   └── ...
├── cache-manifest.json
├── generation-metadata.json
└── suite-profile.json
```

Candidate directories are intentionally outside the suite output because they
are large, temporary inputs:

```text
/mnt/evmole-dataset-work/candidates/
├── solc-main/
├── solc-legacy/
├── solc-modern/
└── vyper-main/
```

If suite selection or packaging needs to be repeated without scanning the
Parquet files again:

```sh
uv run suite.py \
  --cache /mnt/sourcify-parquet \
  --work /mnt/evmole-dataset-work \
  --output /mnt/evmole-dataset-suite \
  --skip-candidates \
  --overwrite
```

`--overwrite` replaces the named candidate/dataset outputs. Do not use it
during an initial run.

## Reproducibility

Selection is deterministic for the same:

- Parquet snapshot;
- DuckDB version and candidate-pool generation behavior;
- `suite.json`;
- seed;
- candidate pool contents.

Candidate JSON records include the compilation ID, fully qualified target name,
and source-derived contract kind. `generate.py` resolves kinds in a bounded
pass over the source tables while hydrating each candidate pool.

Sourcify is continuously updated, so running against a newer cache is expected
to produce a different but equivalently selected suite. The copied cache
manifest identifies the upstream snapshot. If the cache predates ETag tracking,
the suite instead records every local Parquet path, size, and modification time.
Each dataset manifest records the actual addresses, compiler versions, raw and
normalized runtime hashes, coverage labels, selection strategy, and seed. These
manifests are the authoritative record of a released dataset.
`generation-metadata.json` records the Python and DuckDB versions and hashes of
the profile and generation scripts.

The archives themselves are byte-for-byte deterministic when their selected
JSON inputs are identical.

The currently checked-in example of all release artifacts is
[`../../releases/sourcify-v1/`](../../releases/sourcify-v1/).

Before publishing a refresh:

1. Inspect all Markdown reports and selection manifests.
2. Confirm each dataset reached its requested contract count.
3. Compare compiler/version and feature counts with the previous release.
4. Run at least the reference selector provider on every dataset.
5. Run storage ground-truth conversion on `storage-coverage1k`.
6. Run basic-block generation on `flow-challenge500`.
7. Copy the archives, reports, manifests, suite profile, and cache manifest
   into the dataset release.
8. Change benchmark defaults only after the archives are available.

Do not replace an existing archive under the same release identity when the
selected contract list changes. Increment the suite profile/version or release
tag so historical benchmark results remain comparable.

## Selection features

`select_dataset.py` derives coverage labels without running EVMole or another provider,
avoiding selection bias toward a benchmarked implementation. Labels include:

- compiler major/minor and compiler settings;
- optimizer state/runs, `viaIR`, and EVM target;
- bytecode and ABI-function-count buckets;
- tuple, array, bytes/string, signed integer, and function ABI arguments;
- ABI nesting depth and state mutability;
- structural jump and `JUMPDEST` counts;
- selected modern, storage, call, and creation opcodes;
- storage entry/type counts, packing, structs, encoding classes, and transient
  storage.

Coverage selection fills a target number from each available label and then
uses deterministic hash ordering for the remainder. Flow selection uses the
same coverage pass and fills the remainder by a provider-independent structural
complexity score.

Executable-bytecode deduplication strips a plausible terminal length-suffixed
CBOR map and hashes the remaining bytes. This removes contracts that differ
only in compiler metadata while retaining contracts whose executable code
differs.

## Individual tools

Generate a simple filtered candidate dataset:

```sh
uv run generate.py \
  --cache /mnt/sourcify-parquet \
  --output /tmp/recent-solidity \
  --count 5000 \
  --chain-id 1 \
  --compiler solc \
  --compiler-version-min 0.8.24 \
  --compiler-version-max 0.8.30 \
  --bytecode-size-min 500 \
  --bytecode-size-max 24576 \
  --functions-min 0 \
  --include-storage-layout \
  --memory-limit 8GB
```

Select a dataset from one or more existing candidate directories:

```sh
python3 select_dataset.py \
  --input /mnt/work/candidates/solc-main \
  --input /mnt/work/candidates/solc-legacy \
  --output /tmp/solidity-coverage2k \
  --manifest /tmp/solidity-coverage2k.manifest.json \
  --report /tmp/solidity-coverage2k.md \
  --name solidity-coverage2k \
  --strategy coverage \
  --compiler solc \
  --exclude-contract-kind library \
  --coverage-target 40 \
  --count 2000 \
  --seed evmole-sourcify-suite-v1/dataset/solidity-coverage2k
```

Produce a standalone report:

```sh
python3 stats.py \
  --input /tmp/solidity-coverage2k \
  --name solidity-coverage2k \
  --json /tmp/solidity-coverage2k.stats.json \
  --markdown /tmp/solidity-coverage2k.stats.md
```

Package deterministically:

```sh
python3 package.py \
  --input /tmp/solidity-coverage2k \
  --output /tmp/solidity-coverage2k.tar.gz \
  --name solidity-coverage2k
```

Run any script with `--help` for all options.
