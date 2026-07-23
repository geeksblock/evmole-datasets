# EVMole Datasets

This repository contains smart contract datasets used for [EVMole benchmarks](https://github.com/cdump/evmole/tree/master/benchmark).

## July 2026 refresh

The current datasets were generated on July 23, 2026 from Sourcify's v2
Parquet export. They replace `largest1k`, `random50k`, `vyper`, and `storage3k`.
The legacy archives and their Etherscan/Sourcify generation scripts were
removed from the current tree; they remain available in the
[last commit containing the legacy suite](https://github.com/cdump/evmole-datasets/tree/65fe45409ffa8e5c4b74c5a0620b30c896f09df9).

The new suite gives better benchmark coverage with substantially fewer
contracts to process:

- a 10,000-contract random Solidity baseline is kept separate from an
  additional, non-overlapping 2,000-contract coverage set;
- dedicated Vyper, storage-layout, and difficult control-flow datasets exercise
  behavior that a single large random sample can underrepresent;
- selection covers compiler generations, compiler settings, ABI shapes,
  bytecode sizes, structural complexity, modern opcodes, and persistent and
  transient storage layouts;
- runtime bytecode is deduplicated after normalizing compiler metadata; and
- every release includes the selected-contract manifests, coverage reports,
  source-cache inventory, tool versions, generation-code hashes, and
  deterministic archives.

This makes the suite quicker to run than the old 50,000-contract random
baseline while making rare and difficult bytecode features explicit and
measurable.

## Current generation workflow

New datasets should be generated from Sourcify's v2 Parquet export with
[`scripts/sourcify_parquet/`](scripts/sourcify_parquet/). The profile-driven
workflow creates a random Solidity baseline plus Solidity, Vyper, storage, and
control-flow coverage datasets. It also produces selection manifests, coverage
reports, a cache snapshot manifest, and deterministic archives.

See
[`scripts/sourcify_parquet/README.md`](scripts/sourcify_parquet/README.md) for
the complete reproducible procedure and release checklist.

## Current release

The generated archives at the repository root are the
[`sourcify-v1`](releases/sourcify-v1/) suite:

| Dataset | Contracts | Purpose |
|---|---:|---|
| `solidity-random10k` | 10,000 | Population-style Solidity baseline |
| `solidity-coverage2k` | 2,000 | Additional, non-overlapping Solidity coverage |
| `vyper-coverage1k` | 1,000 | Vyper compiler and bytecode coverage |
| `storage-coverage1k` | 1,000 | Persistent and transient storage-layout coverage |
| `flow-challenge500` | 500 | Difficult control-flow examples |

The release directory contains its exact profile, selected-contract manifests,
coverage reports, cache snapshot manifest, generation metadata, checksums, and
validation record.
