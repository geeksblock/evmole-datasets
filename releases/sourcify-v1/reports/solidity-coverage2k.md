# Dataset report: solidity-coverage2k

- Contracts: 2000
- Unique runtime hashes: 2000
- Unique normalized hashes: 2000
- Compilers: solc=2000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 108 | 1159 | 3149 | 6961 | 12873 | 19730 | 22769 | 24375 | 24574 |
| ABI functions | 0 | 2 | 9 | 19 | 32 | 48 | 60 | 96 | 135 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 1905 |
| `abi-depth:1-1` | 272 |
| `abi-depth:2-2` | 74 |
| `abi-depth:3-3` | 40 |
| `abi-depth:4+` | 10 |
| `abi:dynamic-array` | 729 |
| `abi:dynamic-bytes-or-string` | 765 |
| `abi:fixed-array` | 46 |
| `abi:fixed-bytes` | 619 |
| `abi:signed-int` | 80 |
| `abi:tuple` | 323 |
| `arguments:0-0` | 1807 |
| `arguments:1-1` | 1729 |
| `arguments:2-2` | 1497 |
| `arguments:3-3` | 1317 |
| `arguments:4-5` | 611 |
| `arguments:6-8` | 321 |
| `arguments:9+` | 65 |
| `bytecode-size:0-127` | 12 |
| `bytecode-size:1024-2047` | 168 |
| `bytecode-size:128-255` | 41 |
| `bytecode-size:16384-24575` | 309 |
| `bytecode-size:2048-4095` | 308 |
| `bytecode-size:256-511` | 44 |
| `bytecode-size:4096-8191` | 517 |
| `bytecode-size:512-1023` | 62 |
| `bytecode-size:8192-16383` | 539 |
| `compiler-era:solc:0` | 2000 |
| `compiler-minor:solc:0.4` | 42 |
| `compiler-minor:solc:0.5` | 56 |
| `compiler-minor:solc:0.6` | 204 |
| `compiler-minor:solc:0.7` | 121 |
| `compiler-minor:solc:0.8` | 1577 |
| `compiler-patch-bucket:solc:0-0` | 63 |
| `compiler-patch-bucket:solc:1-4` | 104 |
| `compiler-patch-bucket:solc:10-19` | 570 |
| `compiler-patch-bucket:solc:20+` | 1008 |
| `compiler-patch-bucket:solc:5-9` | 255 |
| `compiler:solc` | 2000 |
| `contract-kind:contract` | 2000 |
| `evm-version:berlin` | 45 |
| `evm-version:byzantium` | 40 |
| `evm-version:cancun` | 259 |
| `evm-version:constantinople` | 9 |
| `evm-version:homestead` | 2 |
| `evm-version:istanbul` | 356 |
| `evm-version:london` | 301 |
| `evm-version:osaka` | 28 |
| `evm-version:paris` | 342 |
| `evm-version:petersburg` | 25 |
| `evm-version:prague` | 55 |
| `evm-version:shanghai` | 153 |
| `functions:0-0` | 80 |
| `functions:1-1` | 64 |
| `functions:10-19` | 516 |
| `functions:100+` | 18 |
| `functions:2-4` | 178 |
| `functions:20-49` | 765 |
| `functions:5-9` | 215 |
| `functions:50-99` | 164 |
| `jumpdests:1-4` | 44 |
| `jumpdests:1024+` | 48 |
| `jumpdests:16-63` | 208 |
| `jumpdests:256-1023` | 929 |
| `jumpdests:5-15` | 49 |
| `jumpdests:64-255` | 722 |
| `jumps:1-4` | 40 |
| `jumps:1024+` | 109 |
| `jumps:16-63` | 178 |
| `jumps:256-1023` | 984 |
| `jumps:5-15` | 46 |
| `jumps:64-255` | 643 |
| `mutability:nonpayable` | 1747 |
| `mutability:payable` | 506 |
| `mutability:pure` | 485 |
| `mutability:view` | 1810 |
| `opcode:create` | 77 |
| `opcode:create2` | 91 |
| `opcode:delegatecall` | 296 |
| `opcode:mcopy` | 342 |
| `opcode:push0` | 755 |
| `opcode:selfdestruct` | 42 |
| `opcode:sload` | 1758 |
| `opcode:sstore` | 1666 |
| `opcode:staticcall` | 1249 |
| `opcode:tload` | 78 |
| `opcode:tstore` | 55 |
| `optimizer-runs:0-0` | 31 |
| `optimizer-runs:1-1` | 45 |
| `optimizer-runs:1000-9999` | 148 |
| `optimizer-runs:10000+` | 195 |
| `optimizer-runs:2-199` | 75 |
| `optimizer-runs:200-200` | 1444 |
| `optimizer-runs:201-999` | 58 |
| `optimizer:false` | 532 |
| `optimizer:true` | 1425 |
| `optimizer:unknown` | 43 |
| `storage-encoding:bytes` | 767 |
| `storage-encoding:dynamic_array` | 390 |
| `storage-encoding:inplace` | 1562 |
| `storage-encoding:mapping` | 1315 |
| `storage-entries:0-0` | 360 |
| `storage-entries:1-1` | 123 |
| `storage-entries:16-31` | 446 |
| `storage-entries:2-3` | 143 |
| `storage-entries:32-63` | 82 |
| `storage-entries:4-7` | 376 |
| `storage-entries:8-15` | 402 |
| `storage-types:0-0` | 360 |
| `storage-types:1-1` | 101 |
| `storage-types:16-31` | 170 |
| `storage-types:2-3` | 149 |
| `storage-types:32+` | 38 |
| `storage-types:4-7` | 490 |
| `storage-types:8-15` | 624 |
| `storage:packed` | 719 |
| `storage:struct` | 523 |
| `storage:transient` | 7 |
| `via-ir:false` | 107 |
| `via-ir:true` | 214 |
| `via-ir:unknown` | 1679 |
