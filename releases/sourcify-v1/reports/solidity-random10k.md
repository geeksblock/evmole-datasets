# Dataset report: solidity-random10k

- Contracts: 10000
- Unique runtime hashes: 10000
- Unique normalized hashes: 10000
- Compilers: solc=10000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 53 | 1783 | 3534 | 6930 | 12301 | 17537 | 20859 | 24220 | 24567 |
| ABI functions | 0 | 4 | 10 | 19 | 30 | 46 | 56 | 75 | 148 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 9638 |
| `abi-depth:1-1` | 1115 |
| `abi-depth:2-2` | 218 |
| `abi-depth:3-3` | 39 |
| `abi-depth:4+` | 13 |
| `abi:dynamic-array` | 3382 |
| `abi:dynamic-bytes-or-string` | 3579 |
| `abi:fixed-array` | 116 |
| `abi:fixed-bytes` | 2942 |
| `abi:signed-int` | 242 |
| `abi:tuple` | 1223 |
| `arguments:0-0` | 9279 |
| `arguments:1-1` | 8900 |
| `arguments:2-2` | 8018 |
| `arguments:3-3` | 6869 |
| `arguments:4-5` | 2997 |
| `arguments:6-8` | 1390 |
| `arguments:9+` | 201 |
| `bytecode-size:0-127` | 11 |
| `bytecode-size:1024-2047` | 723 |
| `bytecode-size:128-255` | 59 |
| `bytecode-size:16384-24575` | 1216 |
| `bytecode-size:2048-4095` | 1740 |
| `bytecode-size:256-511` | 131 |
| `bytecode-size:4096-8191` | 2926 |
| `bytecode-size:512-1023` | 256 |
| `bytecode-size:8192-16383` | 2938 |
| `compiler-era:solc:0` | 10000 |
| `compiler-minor:solc:0.4` | 33 |
| `compiler-minor:solc:0.5` | 109 |
| `compiler-minor:solc:0.6` | 742 |
| `compiler-minor:solc:0.7` | 442 |
| `compiler-minor:solc:0.8` | 8674 |
| `compiler-patch-bucket:solc:0-0` | 214 |
| `compiler-patch-bucket:solc:1-4` | 568 |
| `compiler-patch-bucket:solc:10-19` | 3370 |
| `compiler-patch-bucket:solc:20+` | 4635 |
| `compiler-patch-bucket:solc:5-9` | 1213 |
| `compiler:solc` | 10000 |
| `contract-kind:contract` | 10000 |
| `evm-version:berlin` | 112 |
| `evm-version:byzantium` | 17 |
| `evm-version:cancun` | 756 |
| `evm-version:constantinople` | 7 |
| `evm-version:istanbul` | 1600 |
| `evm-version:london` | 2023 |
| `evm-version:osaka` | 25 |
| `evm-version:paris` | 2011 |
| `evm-version:petersburg` | 12 |
| `evm-version:prague` | 140 |
| `evm-version:shanghai` | 909 |
| `functions:0-0` | 306 |
| `functions:1-1` | 228 |
| `functions:10-19` | 2869 |
| `functions:100+` | 11 |
| `functions:2-4` | 655 |
| `functions:20-49` | 4102 |
| `functions:5-9` | 1076 |
| `functions:50-99` | 753 |
| `jumpdests:0-0` | 6 |
| `jumpdests:1-4` | 43 |
| `jumpdests:1024+` | 148 |
| `jumpdests:16-63` | 822 |
| `jumpdests:256-1023` | 4854 |
| `jumpdests:5-15` | 140 |
| `jumpdests:64-255` | 3987 |
| `jumps:0-0` | 6 |
| `jumps:1-4` | 41 |
| `jumps:1024+` | 327 |
| `jumps:16-63` | 744 |
| `jumps:256-1023` | 5335 |
| `jumps:5-15` | 108 |
| `jumps:64-255` | 3439 |
| `mutability:nonpayable` | 9097 |
| `mutability:payable` | 2439 |
| `mutability:pure` | 2481 |
| `mutability:view` | 9304 |
| `opcode:create` | 283 |
| `opcode:create2` | 380 |
| `opcode:delegatecall` | 1092 |
| `opcode:mcopy` | 1359 |
| `opcode:push0` | 3409 |
| `opcode:selfdestruct` | 86 |
| `opcode:sload` | 9183 |
| `opcode:sstore` | 8828 |
| `opcode:staticcall` | 6295 |
| `opcode:tload` | 157 |
| `opcode:tstore` | 122 |
| `optimizer-runs:0-0` | 35 |
| `optimizer-runs:1-1` | 140 |
| `optimizer-runs:1000-9999` | 653 |
| `optimizer-runs:10000+` | 916 |
| `optimizer-runs:2-199` | 269 |
| `optimizer-runs:200-200` | 7693 |
| `optimizer-runs:201-999` | 278 |
| `optimizer:false` | 3091 |
| `optimizer:true` | 6817 |
| `optimizer:unknown` | 92 |
| `storage-encoding:bytes` | 4283 |
| `storage-encoding:dynamic_array` | 1792 |
| `storage-encoding:inplace` | 8473 |
| `storage-encoding:mapping` | 7201 |
| `storage-entries:0-0` | 1429 |
| `storage-entries:1-1` | 497 |
| `storage-entries:16-31` | 2478 |
| `storage-entries:2-3` | 817 |
| `storage-entries:32-63` | 339 |
| `storage-entries:4-7` | 2055 |
| `storage-entries:64+` | 1 |
| `storage-entries:8-15` | 2330 |
| `storage-types:0-0` | 1429 |
| `storage-types:1-1` | 460 |
| `storage-types:16-31` | 726 |
| `storage-types:2-3` | 755 |
| `storage-types:32+` | 31 |
| `storage-types:4-7` | 3011 |
| `storage-types:8-15` | 3534 |
| `storage:packed` | 3810 |
| `storage:struct` | 2542 |
| `storage:transient` | 1 |
| `via-ir:false` | 440 |
| `via-ir:true` | 842 |
| `via-ir:unknown` | 8718 |
