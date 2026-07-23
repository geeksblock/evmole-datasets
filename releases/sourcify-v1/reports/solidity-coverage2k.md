# Dataset report: solidity-coverage2k

- Contracts: 2000
- Unique runtime hashes: 2000
- Unique normalized hashes: 2000
- Compilers: solc=2000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 53 | 1180 | 3214 | 7035 | 12981 | 20311 | 23179 | 24429 | 24576 |
| ABI functions | 0 | 2 | 9 | 19 | 34 | 51 | 62 | 100 | 171 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 1899 |
| `abi-depth:1-1` | 283 |
| `abi-depth:2-2` | 72 |
| `abi-depth:3-3` | 40 |
| `abi-depth:4+` | 11 |
| `abi:dynamic-array` | 708 |
| `abi:dynamic-bytes-or-string` | 756 |
| `abi:fixed-array` | 50 |
| `abi:fixed-bytes` | 637 |
| `abi:signed-int` | 87 |
| `abi:tuple` | 326 |
| `arguments:0-0` | 1801 |
| `arguments:1-1` | 1714 |
| `arguments:2-2` | 1533 |
| `arguments:3-3` | 1320 |
| `arguments:4-5` | 654 |
| `arguments:6-8` | 350 |
| `arguments:9+` | 68 |
| `bytecode-size:0-127` | 8 |
| `bytecode-size:1024-2047` | 157 |
| `bytecode-size:128-255` | 40 |
| `bytecode-size:16384-24575` | 352 |
| `bytecode-size:2048-4095` | 312 |
| `bytecode-size:24576+` | 1 |
| `bytecode-size:256-511` | 45 |
| `bytecode-size:4096-8191` | 512 |
| `bytecode-size:512-1023` | 71 |
| `bytecode-size:8192-16383` | 502 |
| `compiler-era:solc:0` | 2000 |
| `compiler-minor:solc:0.4` | 41 |
| `compiler-minor:solc:0.5` | 52 |
| `compiler-minor:solc:0.6` | 181 |
| `compiler-minor:solc:0.7` | 135 |
| `compiler-minor:solc:0.8` | 1591 |
| `compiler-patch-bucket:solc:0-0` | 56 |
| `compiler-patch-bucket:solc:1-4` | 110 |
| `compiler-patch-bucket:solc:10-19` | 587 |
| `compiler-patch-bucket:solc:20+` | 1007 |
| `compiler-patch-bucket:solc:5-9` | 240 |
| `compiler:solc` | 2000 |
| `evm-version:berlin` | 51 |
| `evm-version:byzantium` | 36 |
| `evm-version:cancun` | 226 |
| `evm-version:constantinople` | 15 |
| `evm-version:istanbul` | 345 |
| `evm-version:london` | 288 |
| `evm-version:osaka` | 41 |
| `evm-version:paris` | 336 |
| `evm-version:petersburg` | 24 |
| `evm-version:prague` | 51 |
| `evm-version:shanghai` | 160 |
| `evm-version:spuriousDragon` | 1 |
| `functions:0-0` | 90 |
| `functions:1-1` | 71 |
| `functions:10-19` | 492 |
| `functions:100+` | 22 |
| `functions:2-4` | 174 |
| `functions:20-49` | 745 |
| `functions:5-9` | 217 |
| `functions:50-99` | 189 |
| `jumpdests:0-0` | 2 |
| `jumpdests:1-4` | 43 |
| `jumpdests:1024+` | 46 |
| `jumpdests:16-63` | 194 |
| `jumpdests:256-1023` | 954 |
| `jumpdests:5-15` | 46 |
| `jumpdests:64-255` | 715 |
| `jumps:0-0` | 2 |
| `jumps:1-4` | 41 |
| `jumps:1024+` | 117 |
| `jumps:16-63` | 167 |
| `jumps:256-1023` | 991 |
| `jumps:5-15` | 44 |
| `jumps:64-255` | 638 |
| `mutability:nonpayable` | 1726 |
| `mutability:payable` | 502 |
| `mutability:pure` | 506 |
| `mutability:view` | 1802 |
| `opcode:create` | 75 |
| `opcode:create2` | 103 |
| `opcode:delegatecall` | 270 |
| `opcode:mcopy` | 369 |
| `opcode:push0` | 755 |
| `opcode:selfdestruct` | 41 |
| `opcode:sload` | 1775 |
| `opcode:sstore` | 1671 |
| `opcode:staticcall` | 1267 |
| `opcode:tload` | 65 |
| `opcode:tstore` | 53 |
| `optimizer-runs:0-0` | 40 |
| `optimizer-runs:1-1` | 44 |
| `optimizer-runs:1000-9999` | 137 |
| `optimizer-runs:10000+` | 217 |
| `optimizer-runs:2-199` | 76 |
| `optimizer-runs:200-200` | 1429 |
| `optimizer-runs:201-999` | 55 |
| `optimizer:false` | 565 |
| `optimizer:true` | 1394 |
| `optimizer:unknown` | 41 |
| `storage-encoding:bytes` | 813 |
| `storage-encoding:dynamic_array` | 376 |
| `storage-encoding:inplace` | 1582 |
| `storage-encoding:mapping` | 1329 |
| `storage-entries:0-0` | 348 |
| `storage-entries:1-1` | 118 |
| `storage-entries:16-31` | 426 |
| `storage-entries:2-3` | 164 |
| `storage-entries:32-63` | 109 |
| `storage-entries:4-7` | 351 |
| `storage-entries:64+` | 3 |
| `storage-entries:8-15` | 417 |
| `storage-types:0-0` | 348 |
| `storage-types:1-1` | 98 |
| `storage-types:16-31` | 156 |
| `storage-types:2-3` | 127 |
| `storage-types:32+` | 40 |
| `storage-types:4-7` | 534 |
| `storage-types:8-15` | 633 |
| `storage:packed` | 699 |
| `storage:struct` | 521 |
| `storage:transient` | 11 |
| `via-ir:false` | 122 |
| `via-ir:true` | 202 |
| `via-ir:unknown` | 1676 |
