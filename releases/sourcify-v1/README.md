# Sourcify benchmark suite v1

This release was generated from the local Sourcify v2 Parquet snapshot on
2026-07-23 with
[`scripts/sourcify_parquet/suite.py`](../../scripts/sourcify_parquet/suite.py).
[`suite-profile.json`](suite-profile.json) is the exact generation profile.

| Dataset | Contracts | Archive bytes | SHA-256 |
|---|---:|---:|---|
| `solidity-random10k` | 10,000 | 50,668,464 | `9c8959b29485ca889c84a01910ddef92a50565ff2771e513bea41b1c24a1c728` |
| `solidity-coverage2k` | 2,000 | 10,667,417 | `3fc41469e81393d2ad00ba4a3abac1df240b95bc60375b98389b56f1f35da499` |
| `vyper-coverage1k` | 1,000 | 6,178,050 | `1a23d11425defb3e4a0d781f60271a49d36bfe5ab6de8a04d3991776487d5711` |
| `storage-coverage1k` | 1,000 | 5,524,584 | `5b0a27ea67391a97569720d877d5d019d6bd8846a78aff27ffa68676c34377d4` |
| `flow-challenge500` | 500 | 5,215,506 | `74d40eb8b2dadb602cec203727d8009559f0e84643940c1cdef58f45d8b8034f` |

All 14,500 entries are unique within their dataset by both raw runtime hash and
metadata-normalized runtime hash. The two general Solidity datasets are
disjoint by normalized runtime hash, giving 12,000 distinct general Solidity
contracts.

Every selected entry is source-classified as a contract. Solidity libraries
are rejected during candidate generation by resolving the exact compilation
target declaration, including libraries without the usual bytecode prefix.

The release was checked by:

- regenerating every archive and comparing it byte-for-byte;
- running the Etherscan reference selector extraction on every contract;
- running storage ground-truth conversion on all 1,000 storage contracts; and
- running EVMole basic-block and control-flow extraction on all 500 flow
  contracts.

The `reports/` directory contains the compiler, settings, ABI, bytecode-size,
opcode, storage, and structural coverage counts. The `manifests/` directory is
the authoritative contract list. `cache-manifest.json` describes the 1,680
Parquet objects (100,229,562,558 bytes) used for this release, while
`generation-metadata.json` records tool versions and hashes of the generation
code.
