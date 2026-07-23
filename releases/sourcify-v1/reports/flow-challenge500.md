# Dataset report: flow-challenge500

- Contracts: 500
- Unique runtime hashes: 500
- Unique normalized hashes: 500
- Compilers: solc=432, vyper=68

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 39 | 685 | 7131 | 22722 | 24252 | 24435 | 24484 | 24565 | 24574 |
| ABI functions | 0 | 2 | 13 | 45 | 57 | 75 | 87 | 111 | 148 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 476 |
| `abi-depth:1-1` | 168 |
| `abi-depth:2-2` | 42 |
| `abi-depth:3-3` | 24 |
| `abi-depth:4+` | 15 |
| `abi:dynamic-array` | 292 |
| `abi:dynamic-bytes-or-string` | 315 |
| `abi:fixed-array` | 32 |
| `abi:fixed-bytes` | 292 |
| `abi:signed-int` | 47 |
| `abi:tuple` | 194 |
| `arguments:0-0` | 450 |
| `arguments:1-1` | 448 |
| `arguments:2-2` | 409 |
| `arguments:3-3` | 375 |
| `arguments:4-5` | 254 |
| `arguments:6-8` | 178 |
| `arguments:9+` | 27 |
| `bytecode-size:0-127` | 15 |
| `bytecode-size:1024-2047` | 16 |
| `bytecode-size:128-255` | 15 |
| `bytecode-size:16384-24575` | 317 |
| `bytecode-size:2048-4095` | 27 |
| `bytecode-size:256-511` | 15 |
| `bytecode-size:4096-8191` | 25 |
| `bytecode-size:512-1023` | 15 |
| `bytecode-size:8192-16383` | 55 |
| `compiler-era:solc:0` | 432 |
| `compiler-era:vyper:0` | 68 |
| `compiler-minor:solc:0.4` | 17 |
| `compiler-minor:solc:0.5` | 18 |
| `compiler-minor:solc:0.6` | 18 |
| `compiler-minor:solc:0.7` | 97 |
| `compiler-minor:solc:0.8` | 282 |
| `compiler-minor:vyper:0.1` | 15 |
| `compiler-minor:vyper:0.2` | 15 |
| `compiler-minor:vyper:0.3` | 20 |
| `compiler-minor:vyper:0.4` | 18 |
| `compiler-patch-bucket:solc:0-0` | 16 |
| `compiler-patch-bucket:solc:1-4` | 87 |
| `compiler-patch-bucket:solc:10-19` | 84 |
| `compiler-patch-bucket:solc:20+` | 198 |
| `compiler-patch-bucket:solc:5-9` | 47 |
| `compiler-patch-bucket:vyper:0-0` | 20 |
| `compiler-patch-bucket:vyper:1-4` | 18 |
| `compiler-patch-bucket:vyper:10-19` | 15 |
| `compiler-patch-bucket:vyper:5-9` | 15 |
| `compiler:solc` | 432 |
| `compiler:vyper` | 68 |
| `contract-kind:contract` | 500 |
| `evm-version:berlin` | 15 |
| `evm-version:byzantium` | 15 |
| `evm-version:cancun` | 61 |
| `evm-version:constantinople` | 15 |
| `evm-version:homestead` | 1 |
| `evm-version:istanbul` | 114 |
| `evm-version:london` | 53 |
| `evm-version:osaka` | 15 |
| `evm-version:paris` | 44 |
| `evm-version:petersburg` | 18 |
| `evm-version:prague` | 24 |
| `evm-version:shanghai` | 27 |
| `functions:0-0` | 19 |
| `functions:1-1` | 21 |
| `functions:10-19` | 55 |
| `functions:100+` | 15 |
| `functions:2-4` | 31 |
| `functions:20-49` | 171 |
| `functions:5-9` | 28 |
| `functions:50-99` | 160 |
| `jumpdests:0-0` | 8 |
| `jumpdests:1-4` | 18 |
| `jumpdests:1024+` | 209 |
| `jumpdests:16-63` | 35 |
| `jumpdests:256-1023` | 161 |
| `jumpdests:5-15` | 20 |
| `jumpdests:64-255` | 49 |
| `jumps:0-0` | 8 |
| `jumps:1-4` | 15 |
| `jumps:1024+` | 275 |
| `jumps:16-63` | 33 |
| `jumps:256-1023` | 102 |
| `jumps:5-15` | 20 |
| `jumps:64-255` | 47 |
| `mutability:nonpayable` | 438 |
| `mutability:payable` | 183 |
| `mutability:pure` | 134 |
| `mutability:view` | 453 |
| `opcode:create` | 49 |
| `opcode:create2` | 49 |
| `opcode:delegatecall` | 86 |
| `opcode:mcopy` | 117 |
| `opcode:push0` | 194 |
| `opcode:selfdestruct` | 26 |
| `opcode:sload` | 454 |
| `opcode:sstore` | 431 |
| `opcode:staticcall` | 391 |
| `opcode:tload` | 55 |
| `opcode:tstore` | 49 |
| `optimizer-runs:0-0` | 15 |
| `optimizer-runs:1-1` | 26 |
| `optimizer-runs:1000-9999` | 29 |
| `optimizer-runs:10000+` | 20 |
| `optimizer-runs:2-199` | 41 |
| `optimizer-runs:200-200` | 206 |
| `optimizer-runs:201-999` | 92 |
| `optimizer:false` | 113 |
| `optimizer:true` | 309 |
| `optimizer:unknown` | 78 |
| `storage-encoding:bytes` | 240 |
| `storage-encoding:dynamic_array` | 137 |
| `storage-encoding:inplace` | 358 |
| `storage-encoding:mapping` | 320 |
| `storage-entries:0-0` | 49 |
| `storage-entries:1-1` | 24 |
| `storage-entries:16-31` | 108 |
| `storage-entries:2-3` | 24 |
| `storage-entries:32-63` | 50 |
| `storage-entries:4-7` | 33 |
| `storage-entries:64+` | 1 |
| `storage-entries:8-15` | 118 |
| `storage-types:0-0` | 49 |
| `storage-types:1-1` | 20 |
| `storage-types:16-31` | 98 |
| `storage-types:2-3` | 22 |
| `storage-types:32+` | 17 |
| `storage-types:4-7` | 38 |
| `storage-types:8-15` | 163 |
| `storage:packed` | 139 |
| `storage:struct` | 240 |
| `storage:transient` | 8 |
| `via-ir:false` | 26 |
| `via-ir:true` | 84 |
| `via-ir:unknown` | 390 |
| `vyper-optimize:gas` | 7 |
