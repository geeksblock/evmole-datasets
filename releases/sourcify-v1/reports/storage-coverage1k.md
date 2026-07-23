# Dataset report: storage-coverage1k

- Contracts: 1000
- Unique runtime hashes: 1000
- Unique normalized hashes: 1000
- Compilers: solc=1000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 57 | 680 | 2502 | 6607 | 13122 | 21351 | 24047 | 24516 | 24576 |
| ABI functions | 0 | 1 | 5 | 16 | 32 | 50 | 71 | 108 | 171 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 923 |
| `abi-depth:1-1` | 141 |
| `abi-depth:2-2` | 36 |
| `abi-depth:3-3` | 30 |
| `abi-depth:4+` | 26 |
| `abi:dynamic-array` | 336 |
| `abi:dynamic-bytes-or-string` | 381 |
| `abi:fixed-array` | 35 |
| `abi:fixed-bytes` | 330 |
| `abi:signed-int` | 53 |
| `abi:tuple` | 172 |
| `arguments:0-0` | 878 |
| `arguments:1-1` | 821 |
| `arguments:2-2` | 710 |
| `arguments:3-3` | 611 |
| `arguments:4-5` | 317 |
| `arguments:6-8` | 176 |
| `arguments:9+` | 38 |
| `bytecode-size:0-127` | 23 |
| `bytecode-size:1024-2047` | 82 |
| `bytecode-size:128-255` | 31 |
| `bytecode-size:16384-24575` | 174 |
| `bytecode-size:2048-4095` | 142 |
| `bytecode-size:24576+` | 1 |
| `bytecode-size:256-511` | 32 |
| `bytecode-size:4096-8191` | 218 |
| `bytecode-size:512-1023` | 47 |
| `bytecode-size:8192-16383` | 250 |
| `compiler-era:solc:0` | 1000 |
| `compiler-minor:solc:0.5` | 33 |
| `compiler-minor:solc:0.6` | 107 |
| `compiler-minor:solc:0.7` | 61 |
| `compiler-minor:solc:0.8` | 799 |
| `compiler-patch-bucket:solc:0-0` | 43 |
| `compiler-patch-bucket:solc:1-4` | 62 |
| `compiler-patch-bucket:solc:10-19` | 293 |
| `compiler-patch-bucket:solc:20+` | 476 |
| `compiler-patch-bucket:solc:5-9` | 126 |
| `compiler:solc` | 1000 |
| `evm-version:berlin` | 33 |
| `evm-version:byzantium` | 27 |
| `evm-version:cancun` | 101 |
| `evm-version:constantinople` | 12 |
| `evm-version:istanbul` | 186 |
| `evm-version:london` | 138 |
| `evm-version:osaka` | 30 |
| `evm-version:paris` | 165 |
| `evm-version:petersburg` | 12 |
| `evm-version:prague` | 32 |
| `evm-version:shanghai` | 72 |
| `evm-version:spuriousDragon` | 1 |
| `functions:0-0` | 65 |
| `functions:1-1` | 55 |
| `functions:10-19` | 233 |
| `functions:100+` | 30 |
| `functions:2-4` | 95 |
| `functions:20-49` | 326 |
| `functions:5-9` | 118 |
| `functions:50-99` | 78 |
| `jumpdests:0-0` | 6 |
| `jumpdests:1-4` | 33 |
| `jumpdests:1024+` | 33 |
| `jumpdests:16-63` | 124 |
| `jumpdests:256-1023` | 422 |
| `jumpdests:5-15` | 37 |
| `jumpdests:64-255` | 345 |
| `jumps:0-0` | 6 |
| `jumps:1-4` | 33 |
| `jumps:1024+` | 74 |
| `jumps:16-63` | 109 |
| `jumps:256-1023` | 444 |
| `jumps:5-15` | 33 |
| `jumps:64-255` | 301 |
| `mutability:nonpayable` | 839 |
| `mutability:payable` | 286 |
| `mutability:pure` | 234 |
| `mutability:view` | 868 |
| `opcode:create` | 51 |
| `opcode:create2` | 58 |
| `opcode:delegatecall` | 162 |
| `opcode:mcopy` | 177 |
| `opcode:push0` | 370 |
| `opcode:selfdestruct` | 30 |
| `opcode:sload` | 866 |
| `opcode:sstore` | 801 |
| `opcode:staticcall` | 584 |
| `opcode:tload` | 47 |
| `opcode:tstore` | 39 |
| `optimizer-runs:0-0` | 30 |
| `optimizer-runs:1-1` | 31 |
| `optimizer-runs:1000-9999` | 71 |
| `optimizer-runs:10000+` | 80 |
| `optimizer-runs:2-199` | 48 |
| `optimizer-runs:200-200` | 693 |
| `optimizer-runs:201-999` | 45 |
| `optimizer:false` | 250 |
| `optimizer:true` | 719 |
| `optimizer:unknown` | 31 |
| `storage-encoding:bytes` | 407 |
| `storage-encoding:dynamic_array` | 192 |
| `storage-encoding:inplace` | 792 |
| `storage-encoding:mapping` | 655 |
| `storage-entries:0-0` | 198 |
| `storage-entries:1-1` | 92 |
| `storage-entries:16-31` | 188 |
| `storage-entries:2-3` | 76 |
| `storage-entries:32-63` | 58 |
| `storage-entries:4-7` | 182 |
| `storage-entries:64+` | 3 |
| `storage-entries:8-15` | 203 |
| `storage-types:0-0` | 198 |
| `storage-types:1-1` | 79 |
| `storage-types:16-31` | 95 |
| `storage-types:2-3` | 67 |
| `storage-types:32+` | 30 |
| `storage-types:4-7` | 243 |
| `storage-types:8-15` | 288 |
| `storage:packed` | 310 |
| `storage:struct` | 288 |
| `storage:transient` | 13 |
| `via-ir:false` | 73 |
| `via-ir:true` | 124 |
| `via-ir:unknown` | 803 |
