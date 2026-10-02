# U.S. Daily Weather — Validation

## Status

2025 retrieval proof of concept validated. Full historical dataset validation has not yet been completed.

## 2025 proof-of-concept evidence

The completed 2025 retrieval produced:

- 20,495,507 retained U.S. core observation rows
- 31,742 unique stations
- date coverage from 2025-01-01 through 2025-12-31
- core elements PRCP, SNOW, SNWD, TMAX, and TMIN
- compressed NOAA source size of 158,395,357 bytes
- processed Parquet size of 442,769,277 bytes
- source and processed SHA-256 checksums recorded by the retrieval process

The retrieval completed after the implementation was changed to filter the compressed global NOAA stream before pandas/Arrow batching. This avoided the termination encountered by the earlier pandas-first approach.

## GitHub Actions execution validation

The predefined manual workflow was executed for calendar year 2025 as GitHub Actions Run `37053074876`.

Result: **success**.

Verified workflow stages:

- repository checkout
- Python setup
- dependency installation
- GHCN-Daily retrieval and processing
- artifact upload

The run produced artifact `us-daily-weather-2025` (artifact ID `11246774656`). The artifact is temporary workflow output and is not treated as permanent project storage.

## Current validation conclusion

The proof of concept supports moving beyond the 2025 execution test. Before the full approximately ten-year historical build, execute and review one older calendar year to detect historical format, coverage, or processing differences that a single recent year cannot reveal.

Full historical validation remains pending.
