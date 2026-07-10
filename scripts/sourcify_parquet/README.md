# Sourcify Parquet datasets

These scripts synchronize the Sourcify v2 Parquet export and generate benchmark-compatible contract datasets. Dependencies are installed automatically by `uv`.

Run the examples from `benchmark/datasets/scripts/sourcify_parquet/`.

## Synchronize the cache

```sh
uv run sync.py --cache /mnt/sourcify-parquet
```

The synchronizer downloads files that are missing from the cache or whose local size differs from the upstream size. Use `--status` to check without downloading, `--jobs` to control parallelism, or `--prune` to remove local Parquet files absent upstream.

## Generate a dataset

```sh
uv run generate.py \
  --cache /mnt/sourcify-parquet \
  --output /tmp/recent-solidity \
  --count 5000 \
  --chain-id 1 \
  --compiler solc \
  --compiler-version-min 0.8.24 \
  --compiler-version-max 0.8.30 \
  --bytecode-size-min 500 \
  --bytecode-size-max 24576 \
  --functions-min 2 \
  --functions-max 100 \
  --memory-limit 8GB
```

Use repeated `--compiler-version` arguments to select exact versions. Output files are named `<deployed-address>.json` and contain deployed bytecode, ABI, and source metadata. Run either script with `--help` for all options.

Generation first reservoir-samples deployments on the requested chain, then joins each other Parquet table against that bounded set in a separate stage. Each stage replaces and drops the previous temporary table, so no hash join has two full-dataset inputs. The default candidate factor samples four deployments per requested output; increase `--candidate-factor` if compiler, match, or bytecode filters produce too few results. Output can contain fewer contracts than requested. Use `--allow-duplicates` to deduplicate addresses only.

DuckDB spills temporary join data under `CACHE/.duckdb-tmp` by default; use `--temp-directory` to place it on another disk and `--write-batch-size` to tune output buffering. `--seed` makes reservoir selection repeatable for the same cache and DuckDB version.
The default DuckDB memory limit is 4 GB; override it with `--memory-limit` when appropriate for the host.

As with the existing EVMole datasets, contracts with empty deployed bytecode and contracts whose bytecode starts with `PUSH20` (`0x73`) or `0x608060405230` are excluded. These prefixes identify compiled Solidity libraries that require unsupported fully qualified library function signatures.
