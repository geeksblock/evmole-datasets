# Sourcify benchmark suite v1

This release was generated from the local Sourcify v2 Parquet snapshot on
2026-07-23 with
[`scripts/sourcify_parquet/suite.py`](../../scripts/sourcify_parquet/suite.py).
[`suite-profile.json`](suite-profile.json) is the exact generation profile.

| Dataset | Contracts | Archive bytes | SHA-256 |
|---|---:|---:|---|
| `solidity-random10k` | 10,000 | 49,802,012 | `6a18ec6dc9a20edd69daab6d66eeda93f95d3a047b03f682d676cd2ce7d7f48a` |
| `solidity-coverage2k` | 2,000 | 10,817,469 | `f0916743544a56611e4d8dedb07b6fd45db6b0f9577fcd2dee655d06c8745a01` |
| `vyper-coverage1k` | 1,000 | 6,105,640 | `d0909ba3fd4a3453d54bfa17ba2443ad46e605efdfb2874ff8b547197ae35c51` |
| `storage-coverage1k` | 1,000 | 5,448,681 | `4cfe911a0216691dd5978c0085a857b7fe4165fadcfff70018b8163d69bc7172` |
| `flow-challenge500` | 500 | 4,977,442 | `c1e36daf971ab79ba4a415de547879e582413f9fd2bfc1a1404df1fa5312f870` |

All 14,500 entries are unique within their dataset by both raw runtime hash and
metadata-normalized runtime hash. The two general Solidity datasets are
disjoint by normalized runtime hash, giving 12,000 distinct general Solidity
contracts.

The release was checked by:

- regenerating every archive and comparing it byte-for-byte;
- running the Etherscan reference selector extraction on every contract;
- running storage ground-truth conversion on all 1,000 storage contracts; and
- running EVMole basic-block and control-flow extraction on all 500 flow
  contracts.

The `reports/` directory contains the compiler, settings, ABI, bytecode-size,
opcode, storage, and structural coverage counts. The `manifests/` directory is
the authoritative contract list. `cache-manifest.json` describes the 1,020
Parquet objects (81,017,552,816 bytes) used for this release, while
`generation-metadata.json` records tool versions and hashes of the generation
code.
