# Dataset report: storage-coverage1k

- Contracts: 1000
- Unique runtime hashes: 1000
- Unique normalized hashes: 1000
- Compilers: solc=1000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 57 | 675 | 2698 | 6871 | 13496 | 20424 | 23767 | 24491 | 24574 |
| ABI functions | 0 | 1 | 6 | 16 | 32 | 53 | 70 | 107 | 148 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 922 |
| `abi-depth:1-1` | 145 |
| `abi-depth:2-2` | 41 |
| `abi-depth:3-3` | 30 |
| `abi-depth:4+` | 23 |
| `abi:dynamic-array` | 376 |
| `abi:dynamic-bytes-or-string` | 369 |
| `abi:fixed-array` | 35 |
| `abi:fixed-bytes` | 310 |
| `abi:signed-int` | 44 |
| `abi:tuple` | 177 |
| `arguments:0-0` | 860 |
| `arguments:1-1` | 822 |
| `arguments:2-2` | 718 |
| `arguments:3-3` | 623 |
| `arguments:4-5` | 310 |
| `arguments:6-8` | 155 |
| `arguments:9+` | 38 |
| `bytecode-size:0-127` | 22 |
| `bytecode-size:1024-2047` | 75 |
| `bytecode-size:128-255` | 30 |
| `bytecode-size:16384-24575` | 179 |
| `bytecode-size:2048-4095` | 134 |
| `bytecode-size:256-511` | 31 |
| `bytecode-size:4096-8191` | 223 |
| `bytecode-size:512-1023` | 48 |
| `bytecode-size:8192-16383` | 258 |
| `compiler-era:solc:0` | 1000 |
| `compiler-minor:solc:0.5` | 31 |
| `compiler-minor:solc:0.6` | 99 |
| `compiler-minor:solc:0.7` | 68 |
| `compiler-minor:solc:0.8` | 802 |
| `compiler-patch-bucket:solc:0-0` | 43 |
| `compiler-patch-bucket:solc:1-4` | 61 |
| `compiler-patch-bucket:solc:10-19` | 292 |
| `compiler-patch-bucket:solc:20+` | 448 |
| `compiler-patch-bucket:solc:5-9` | 156 |
| `compiler:solc` | 1000 |
| `contract-kind:contract` | 1000 |
| `evm-version:berlin` | 31 |
| `evm-version:byzantium` | 16 |
| `evm-version:cancun` | 97 |
| `evm-version:constantinople` | 9 |
| `evm-version:homestead` | 1 |
| `evm-version:istanbul` | 186 |
| `evm-version:london` | 166 |
| `evm-version:osaka` | 30 |
| `evm-version:paris` | 152 |
| `evm-version:petersburg` | 13 |
| `evm-version:prague` | 32 |
| `evm-version:shanghai` | 73 |
| `functions:0-0` | 62 |
| `functions:1-1` | 55 |
| `functions:10-19` | 249 |
| `functions:100+` | 29 |
| `functions:2-4` | 102 |
| `functions:20-49` | 320 |
| `functions:5-9` | 99 |
| `functions:50-99` | 84 |
| `jumpdests:0-0` | 5 |
| `jumpdests:1-4` | 38 |
| `jumpdests:1024+` | 35 |
| `jumpdests:16-63` | 108 |
| `jumpdests:256-1023` | 456 |
| `jumpdests:5-15` | 35 |
| `jumpdests:64-255` | 323 |
| `jumps:0-0` | 5 |
| `jumps:1-4` | 35 |
| `jumps:1024+` | 76 |
| `jumps:16-63` | 108 |
| `jumps:256-1023` | 456 |
| `jumps:5-15` | 33 |
| `jumps:64-255` | 287 |
| `mutability:nonpayable` | 838 |
| `mutability:payable` | 268 |
| `mutability:pure` | 235 |
| `mutability:view` | 854 |
| `opcode:create` | 44 |
| `opcode:create2` | 43 |
| `opcode:delegatecall` | 164 |
| `opcode:mcopy` | 171 |
| `opcode:push0` | 360 |
| `opcode:selfdestruct` | 31 |
| `opcode:sload` | 860 |
| `opcode:sstore` | 798 |
| `opcode:staticcall` | 596 |
| `opcode:tload` | 45 |
| `opcode:tstore` | 37 |
| `optimizer-runs:0-0` | 30 |
| `optimizer-runs:1-1` | 32 |
| `optimizer-runs:1000-9999` | 68 |
| `optimizer-runs:10000+` | 85 |
| `optimizer-runs:2-199` | 46 |
| `optimizer-runs:200-200` | 686 |
| `optimizer-runs:201-999` | 46 |
| `optimizer:false` | 275 |
| `optimizer:true` | 693 |
| `optimizer:unknown` | 32 |
| `storage-encoding:bytes` | 398 |
| `storage-encoding:dynamic_array` | 196 |
| `storage-encoding:inplace` | 781 |
| `storage-encoding:mapping` | 639 |
| `storage-entries:0-0` | 214 |
| `storage-entries:1-1` | 76 |
| `storage-entries:16-31` | 171 |
| `storage-entries:2-3` | 86 |
| `storage-entries:32-63` | 70 |
| `storage-entries:4-7` | 189 |
| `storage-entries:64+` | 1 |
| `storage-entries:8-15` | 193 |
| `storage-types:0-0` | 214 |
| `storage-types:1-1` | 68 |
| `storage-types:16-31` | 87 |
| `storage-types:2-3` | 77 |
| `storage-types:32+` | 30 |
| `storage-types:4-7` | 260 |
| `storage-types:8-15` | 264 |
| `storage:packed` | 308 |
| `storage:struct` | 261 |
| `storage:transient` | 8 |
| `via-ir:false` | 58 |
| `via-ir:true` | 101 |
| `via-ir:unknown` | 841 |
