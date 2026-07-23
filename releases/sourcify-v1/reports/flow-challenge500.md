# Dataset report: flow-challenge500

- Contracts: 500
- Unique runtime hashes: 500
- Unique normalized hashes: 500
- Compilers: solc=434, vyper=66

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 39 | 571 | 5988 | 22349 | 24252 | 24449 | 24521 | 24569 | 24576 |
| ABI functions | 0 | 2 | 11 | 41 | 56 | 69 | 84 | 122 | 171 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 474 |
| `abi-depth:1-1` | 178 |
| `abi-depth:2-2` | 39 |
| `abi-depth:3-3` | 15 |
| `abi-depth:4+` | 15 |
| `abi:dynamic-array` | 284 |
| `abi:dynamic-bytes-or-string` | 317 |
| `abi:fixed-array` | 35 |
| `abi:fixed-bytes` | 290 |
| `abi:signed-int` | 46 |
| `abi:tuple` | 197 |
| `arguments:0-0` | 454 |
| `arguments:1-1` | 448 |
| `arguments:2-2` | 392 |
| `arguments:3-3` | 363 |
| `arguments:4-5` | 259 |
| `arguments:6-8` | 174 |
| `arguments:9+` | 35 |
| `bytecode-size:0-127` | 17 |
| `bytecode-size:1024-2047` | 17 |
| `bytecode-size:128-255` | 16 |
| `bytecode-size:16384-24575` | 307 |
| `bytecode-size:2048-4095` | 30 |
| `bytecode-size:24576+` | 1 |
| `bytecode-size:256-511` | 15 |
| `bytecode-size:4096-8191` | 34 |
| `bytecode-size:512-1023` | 15 |
| `bytecode-size:8192-16383` | 48 |
| `compiler-era:solc:0` | 434 |
| `compiler-era:vyper:0` | 66 |
| `compiler-minor:solc:0.4` | 15 |
| `compiler-minor:solc:0.5` | 20 |
| `compiler-minor:solc:0.6` | 21 |
| `compiler-minor:solc:0.7` | 78 |
| `compiler-minor:solc:0.8` | 300 |
| `compiler-minor:vyper:0.1` | 15 |
| `compiler-minor:vyper:0.2` | 16 |
| `compiler-minor:vyper:0.3` | 17 |
| `compiler-minor:vyper:0.4` | 18 |
| `compiler-patch-bucket:solc:0-0` | 15 |
| `compiler-patch-bucket:solc:1-4` | 80 |
| `compiler-patch-bucket:solc:10-19` | 105 |
| `compiler-patch-bucket:solc:20+` | 190 |
| `compiler-patch-bucket:solc:5-9` | 44 |
| `compiler-patch-bucket:vyper:0-0` | 19 |
| `compiler-patch-bucket:vyper:1-4` | 17 |
| `compiler-patch-bucket:vyper:10-19` | 15 |
| `compiler-patch-bucket:vyper:5-9` | 15 |
| `compiler:solc` | 434 |
| `compiler:vyper` | 66 |
| `evm-version:berlin` | 15 |
| `evm-version:byzantium` | 15 |
| `evm-version:cancun` | 60 |
| `evm-version:constantinople` | 15 |
| `evm-version:homestead` | 1 |
| `evm-version:istanbul` | 106 |
| `evm-version:london` | 64 |
| `evm-version:osaka` | 15 |
| `evm-version:paris` | 53 |
| `evm-version:petersburg` | 17 |
| `evm-version:prague` | 25 |
| `evm-version:shanghai` | 28 |
| `evm-version:spuriousDragon` | 1 |
| `functions:0-0` | 21 |
| `functions:1-1` | 20 |
| `functions:10-19` | 47 |
| `functions:100+` | 16 |
| `functions:2-4` | 34 |
| `functions:20-49` | 184 |
| `functions:5-9` | 34 |
| `functions:50-99` | 144 |
| `jumpdests:0-0` | 9 |
| `jumpdests:1-4` | 16 |
| `jumpdests:1024+` | 194 |
| `jumpdests:16-63` | 40 |
| `jumpdests:256-1023` | 160 |
| `jumpdests:5-15` | 20 |
| `jumpdests:64-255` | 61 |
| `jumps:0-0` | 9 |
| `jumps:1-4` | 15 |
| `jumps:1024+` | 263 |
| `jumps:16-63` | 39 |
| `jumps:256-1023` | 104 |
| `jumps:5-15` | 18 |
| `jumps:64-255` | 52 |
| `mutability:nonpayable` | 438 |
| `mutability:payable` | 168 |
| `mutability:pure` | 152 |
| `mutability:view` | 447 |
| `opcode:create` | 45 |
| `opcode:create2` | 58 |
| `opcode:delegatecall` | 90 |
| `opcode:mcopy` | 105 |
| `opcode:push0` | 181 |
| `opcode:selfdestruct` | 21 |
| `opcode:sload` | 450 |
| `opcode:sstore` | 426 |
| `opcode:staticcall` | 369 |
| `opcode:tload` | 51 |
| `opcode:tstore` | 44 |
| `optimizer-runs:0-0` | 15 |
| `optimizer-runs:1-1` | 23 |
| `optimizer-runs:1000-9999` | 28 |
| `optimizer-runs:10000+` | 27 |
| `optimizer-runs:2-199` | 44 |
| `optimizer-runs:200-200` | 218 |
| `optimizer-runs:201-999` | 77 |
| `optimizer:false` | 127 |
| `optimizer:true` | 300 |
| `optimizer:unknown` | 73 |
| `storage-encoding:bytes` | 229 |
| `storage-encoding:dynamic_array` | 138 |
| `storage-encoding:inplace` | 354 |
| `storage-encoding:mapping` | 298 |
| `storage-entries:0-0` | 54 |
| `storage-entries:1-1` | 25 |
| `storage-entries:16-31` | 100 |
| `storage-entries:2-3` | 22 |
| `storage-entries:32-63` | 52 |
| `storage-entries:4-7` | 36 |
| `storage-entries:64+` | 3 |
| `storage-entries:8-15` | 118 |
| `storage-types:0-0` | 54 |
| `storage-types:1-1` | 19 |
| `storage-types:16-31` | 97 |
| `storage-types:2-3` | 22 |
| `storage-types:32+` | 23 |
| `storage-types:4-7` | 39 |
| `storage-types:8-15` | 156 |
| `storage:packed` | 158 |
| `storage:struct` | 240 |
| `storage:transient` | 13 |
| `via-ir:false` | 36 |
| `via-ir:true` | 76 |
| `via-ir:unknown` | 388 |
| `vyper-optimize:gas` | 7 |
