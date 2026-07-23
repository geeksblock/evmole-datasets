# Dataset report: solidity-random10k

- Contracts: 10000
- Unique runtime hashes: 10000
- Unique normalized hashes: 10000
- Compilers: solc=10000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 58 | 1732 | 3432 | 6918 | 12142 | 17387 | 20730 | 24252 | 24575 |
| ABI functions | 0 | 4 | 11 | 19 | 31 | 46 | 56 | 73 | 125 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 9656 |
| `abi-depth:1-1` | 1123 |
| `abi-depth:2-2` | 220 |
| `abi-depth:3-3` | 26 |
| `abi-depth:4+` | 15 |
| `abi:dynamic-array` | 3341 |
| `abi:dynamic-bytes-or-string` | 3473 |
| `abi:fixed-array` | 142 |
| `abi:fixed-bytes` | 2912 |
| `abi:signed-int` | 258 |
| `abi:tuple` | 1236 |
| `arguments:0-0` | 9334 |
| `arguments:1-1` | 8940 |
| `arguments:2-2` | 7957 |
| `arguments:3-3` | 6923 |
| `arguments:4-5` | 3050 |
| `arguments:6-8` | 1395 |
| `arguments:9+` | 202 |
| `bytecode-size:0-127` | 16 |
| `bytecode-size:1024-2047` | 799 |
| `bytecode-size:128-255` | 47 |
| `bytecode-size:16384-24575` | 1158 |
| `bytecode-size:2048-4095` | 1756 |
| `bytecode-size:256-511` | 115 |
| `bytecode-size:4096-8191` | 2886 |
| `bytecode-size:512-1023` | 247 |
| `bytecode-size:8192-16383` | 2976 |
| `compiler-era:solc:0` | 10000 |
| `compiler-minor:solc:0.4` | 33 |
| `compiler-minor:solc:0.5` | 91 |
| `compiler-minor:solc:0.6` | 751 |
| `compiler-minor:solc:0.7` | 430 |
| `compiler-minor:solc:0.8` | 8695 |
| `compiler-patch-bucket:solc:0-0` | 225 |
| `compiler-patch-bucket:solc:1-4` | 619 |
| `compiler-patch-bucket:solc:10-19` | 3322 |
| `compiler-patch-bucket:solc:20+` | 4617 |
| `compiler-patch-bucket:solc:5-9` | 1217 |
| `compiler:solc` | 10000 |
| `evm-version:berlin` | 127 |
| `evm-version:byzantium` | 28 |
| `evm-version:cancun` | 762 |
| `evm-version:constantinople` | 5 |
| `evm-version:homestead` | 1 |
| `evm-version:istanbul` | 1654 |
| `evm-version:london` | 2087 |
| `evm-version:osaka` | 24 |
| `evm-version:paris` | 2083 |
| `evm-version:petersburg` | 12 |
| `evm-version:prague` | 100 |
| `evm-version:shanghai` | 942 |
| `functions:0-0` | 293 |
| `functions:1-1` | 206 |
| `functions:10-19` | 2956 |
| `functions:100+` | 8 |
| `functions:2-4` | 634 |
| `functions:20-49` | 4069 |
| `functions:5-9` | 1107 |
| `functions:50-99` | 727 |
| `jumpdests:0-0` | 5 |
| `jumpdests:1-4` | 41 |
| `jumpdests:1024+` | 127 |
| `jumpdests:16-63` | 881 |
| `jumpdests:256-1023` | 4860 |
| `jumpdests:5-15` | 116 |
| `jumpdests:64-255` | 3970 |
| `jumps:0-0` | 5 |
| `jumps:1-4` | 38 |
| `jumps:1024+` | 320 |
| `jumps:16-63` | 774 |
| `jumps:256-1023` | 5322 |
| `jumps:5-15` | 91 |
| `jumps:64-255` | 3450 |
| `mutability:nonpayable` | 9123 |
| `mutability:payable` | 2395 |
| `mutability:pure` | 2409 |
| `mutability:view` | 9354 |
| `opcode:create` | 304 |
| `opcode:create2` | 423 |
| `opcode:delegatecall` | 1096 |
| `opcode:mcopy` | 1235 |
| `opcode:push0` | 3285 |
| `opcode:selfdestruct` | 95 |
| `opcode:sload` | 9145 |
| `opcode:sstore` | 8784 |
| `opcode:staticcall` | 6338 |
| `opcode:tload` | 140 |
| `opcode:tstore` | 125 |
| `optimizer-runs:0-0` | 28 |
| `optimizer-runs:1-1` | 130 |
| `optimizer-runs:1000-9999` | 695 |
| `optimizer-runs:10000+` | 945 |
| `optimizer-runs:2-199` | 296 |
| `optimizer-runs:200-200` | 7593 |
| `optimizer-runs:201-999` | 300 |
| `optimizer:false` | 2941 |
| `optimizer:true` | 6948 |
| `optimizer:unknown` | 111 |
| `storage-encoding:bytes` | 4326 |
| `storage-encoding:dynamic_array` | 1807 |
| `storage-encoding:inplace` | 8463 |
| `storage-encoding:mapping` | 7238 |
| `storage-entries:0-0` | 1427 |
| `storage-entries:1-1` | 464 |
| `storage-entries:16-31` | 2502 |
| `storage-entries:2-3` | 827 |
| `storage-entries:32-63` | 358 |
| `storage-entries:4-7` | 2095 |
| `storage-entries:8-15` | 2275 |
| `storage-types:0-0` | 1427 |
| `storage-types:1-1` | 464 |
| `storage-types:16-31` | 735 |
| `storage-types:2-3` | 722 |
| `storage-types:32+` | 24 |
| `storage-types:4-7` | 3035 |
| `storage-types:8-15` | 3541 |
| `storage:packed` | 3834 |
| `storage:struct` | 2560 |
| `storage:transient` | 2 |
| `via-ir:false` | 396 |
| `via-ir:true` | 831 |
| `via-ir:unknown` | 8773 |
