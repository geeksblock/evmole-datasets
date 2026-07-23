# Dataset report: vyper-coverage1k

- Contracts: 1000
- Unique runtime hashes: 1000
- Unique normalized hashes: 1000
- Compilers: vyper=1000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 39 | 941 | 3407 | 10725 | 23635 | 23635 | 23635 | 24349 | 24538 |
| ABI functions | 0 | 4 | 13 | 49 | 61 | 61 | 66 | 80 | 92 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 994 |
| `abi-depth:1-1` | 62 |
| `abi-depth:2-2` | 35 |
| `abi-depth:3-3` | 13 |
| `abi:dynamic-array` | 373 |
| `abi:dynamic-bytes-or-string` | 174 |
| `abi:fixed-array` | 170 |
| `abi:fixed-bytes` | 514 |
| `abi:signed-int` | 324 |
| `abi:tuple` | 88 |
| `arguments:0-0` | 953 |
| `arguments:1-1` | 910 |
| `arguments:2-2` | 832 |
| `arguments:3-3` | 765 |
| `arguments:4-5` | 545 |
| `arguments:6-8` | 543 |
| `arguments:9+` | 49 |
| `bytecode-size:0-127` | 12 |
| `bytecode-size:1024-2047` | 79 |
| `bytecode-size:128-255` | 16 |
| `bytecode-size:16384-24575` | 399 |
| `bytecode-size:2048-4095` | 91 |
| `bytecode-size:256-511` | 35 |
| `bytecode-size:4096-8191` | 110 |
| `bytecode-size:512-1023` | 46 |
| `bytecode-size:8192-16383` | 212 |
| `compiler-era:vyper:0` | 1000 |
| `compiler-minor:vyper:0.1` | 34 |
| `compiler-minor:vyper:0.2` | 69 |
| `compiler-minor:vyper:0.3` | 743 |
| `compiler-minor:vyper:0.4` | 154 |
| `compiler-patch-bucket:vyper:0-0` | 57 |
| `compiler-patch-bucket:vyper:1-4` | 176 |
| `compiler-patch-bucket:vyper:10-19` | 679 |
| `compiler-patch-bucket:vyper:5-9` | 88 |
| `compiler:vyper` | 1000 |
| `contract-kind:contract` | 1000 |
| `evm-version:berlin` | 34 |
| `evm-version:cancun` | 49 |
| `evm-version:istanbul` | 5 |
| `evm-version:paris` | 44 |
| `evm-version:petersburg` | 39 |
| `evm-version:prague` | 8 |
| `evm-version:shanghai` | 37 |
| `functions:0-0` | 2 |
| `functions:1-1` | 30 |
| `functions:10-19` | 143 |
| `functions:2-4` | 76 |
| `functions:20-49` | 185 |
| `functions:5-9` | 69 |
| `functions:50-99` | 495 |
| `jumpdests:0-0` | 2 |
| `jumpdests:1-4` | 16 |
| `jumpdests:16-63` | 182 |
| `jumpdests:256-1023` | 410 |
| `jumpdests:5-15` | 70 |
| `jumpdests:64-255` | 320 |
| `jumps:0-0` | 2 |
| `jumps:1-4` | 8 |
| `jumps:16-63` | 138 |
| `jumps:256-1023` | 616 |
| `jumps:5-15` | 33 |
| `jumps:64-255` | 203 |
| `mutability:nonpayable` | 904 |
| `mutability:payable` | 99 |
| `mutability:pure` | 71 |
| `mutability:view` | 943 |
| `opcode:create` | 456 |
| `opcode:create2` | 317 |
| `opcode:delegatecall` | 181 |
| `opcode:mcopy` | 529 |
| `opcode:push0` | 740 |
| `opcode:selfdestruct` | 312 |
| `opcode:sload` | 886 |
| `opcode:sstore` | 861 |
| `opcode:staticcall` | 884 |
| `opcode:tload` | 428 |
| `opcode:tstore` | 390 |
| `optimizer:unknown` | 1000 |
| `via-ir:unknown` | 1000 |
| `vyper-optimize:gas` | 7 |
