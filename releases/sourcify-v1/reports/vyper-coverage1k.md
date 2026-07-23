# Dataset report: vyper-coverage1k

- Contracts: 1000
- Unique runtime hashes: 1000
- Unique normalized hashes: 1000
- Compilers: vyper=1000

## Percentiles

| Metric | p0 | p10 | p25 | p50 | p75 | p90 | p95 | p99 | p100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bytecode bytes | 39 | 954 | 3443 | 10725 | 23635 | 23635 | 23635 | 24349 | 24538 |
| ABI functions | 0 | 4 | 13 | 49 | 61 | 61 | 66 | 80 | 92 |

## Coverage labels

| Label | Contracts |
|---|---:|
| `abi-depth:0-0` | 994 |
| `abi-depth:1-1` | 61 |
| `abi-depth:2-2` | 35 |
| `abi-depth:3-3` | 13 |
| `abi:dynamic-array` | 371 |
| `abi:dynamic-bytes-or-string` | 169 |
| `abi:fixed-array` | 173 |
| `abi:fixed-bytes` | 515 |
| `abi:signed-int` | 325 |
| `abi:tuple` | 88 |
| `arguments:0-0` | 952 |
| `arguments:1-1` | 912 |
| `arguments:2-2` | 831 |
| `arguments:3-3` | 765 |
| `arguments:4-5` | 542 |
| `arguments:6-8` | 547 |
| `arguments:9+` | 49 |
| `bytecode-size:0-127` | 12 |
| `bytecode-size:1024-2047` | 76 |
| `bytecode-size:128-255` | 16 |
| `bytecode-size:16384-24575` | 397 |
| `bytecode-size:2048-4095` | 96 |
| `bytecode-size:256-511` | 34 |
| `bytecode-size:4096-8191` | 113 |
| `bytecode-size:512-1023` | 44 |
| `bytecode-size:8192-16383` | 212 |
| `compiler-era:vyper:0` | 1000 |
| `compiler-minor:vyper:0.1` | 34 |
| `compiler-minor:vyper:0.2` | 73 |
| `compiler-minor:vyper:0.3` | 742 |
| `compiler-minor:vyper:0.4` | 151 |
| `compiler-patch-bucket:vyper:0-0` | 54 |
| `compiler-patch-bucket:vyper:1-4` | 176 |
| `compiler-patch-bucket:vyper:10-19` | 685 |
| `compiler-patch-bucket:vyper:5-9` | 85 |
| `compiler:vyper` | 1000 |
| `evm-version:berlin` | 34 |
| `evm-version:cancun` | 50 |
| `evm-version:istanbul` | 5 |
| `evm-version:paris` | 45 |
| `evm-version:petersburg` | 42 |
| `evm-version:prague` | 8 |
| `evm-version:shanghai` | 37 |
| `functions:0-0` | 2 |
| `functions:1-1` | 30 |
| `functions:10-19` | 145 |
| `functions:2-4` | 77 |
| `functions:20-49` | 187 |
| `functions:5-9` | 66 |
| `functions:50-99` | 493 |
| `jumpdests:0-0` | 2 |
| `jumpdests:1-4` | 16 |
| `jumpdests:16-63` | 181 |
| `jumpdests:256-1023` | 409 |
| `jumpdests:5-15` | 68 |
| `jumpdests:64-255` | 324 |
| `jumps:0-0` | 2 |
| `jumps:1-4` | 8 |
| `jumps:16-63` | 135 |
| `jumps:256-1023` | 613 |
| `jumps:5-15` | 33 |
| `jumps:64-255` | 209 |
| `mutability:nonpayable` | 905 |
| `mutability:payable` | 99 |
| `mutability:pure` | 71 |
| `mutability:view` | 944 |
| `opcode:create` | 458 |
| `opcode:create2` | 319 |
| `opcode:delegatecall` | 183 |
| `opcode:mcopy` | 529 |
| `opcode:push0` | 736 |
| `opcode:selfdestruct` | 314 |
| `opcode:sload` | 889 |
| `opcode:sstore` | 863 |
| `opcode:staticcall` | 886 |
| `opcode:tload` | 431 |
| `opcode:tstore` | 393 |
| `optimizer:unknown` | 1000 |
| `via-ir:unknown` | 1000 |
| `vyper-optimize:gas` | 7 |
