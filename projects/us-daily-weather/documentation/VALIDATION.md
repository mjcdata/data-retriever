# U.S. Daily Weather — Validation

## Status

The 2025 proof of concept and 2016 older-year compatibility test are validated. The project is ready to proceed to the full 2016–2025 historical build. Full historical dataset validation remains pending until that build completes.

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

## 2016 older-year compatibility validation

The same predefined manual workflow was executed for calendar year 2016 as GitHub Actions Run `37058669748`.

Result: **success**.

All workflow stages completed successfully, including GHCN-Daily retrieval/processing and artifact upload. The run produced artifact `us-daily-weather-2016` (artifact ID `11249927224`), size 336,631,552 bytes. The artifact is temporary workflow output and is not treated as permanent project storage.

A separate Run `37058701233` was cancelled and is not used as validation evidence.

## Current validation conclusion

The 2016 compatibility gate passed using the same retrieval code and workflow used for 2025. This provides evidence that the pipeline can process both the beginning and end of the planned 2016–2025 historical window.

The next stage is the full 2016–2025 historical build. Each year should remain independently processed and independently artifacted so a failure in one year can be isolated and retried without invalidating successful years.

Full historical validation remains pending until all ten years are built and reviewed.
