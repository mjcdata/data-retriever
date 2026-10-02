# U.S. Daily Weather — Validation

## Status

The 2016–2025 historical execution build is complete. GitHub Actions Run `37060323541` completed successfully and produced one artifact for each of the ten requested years.

This validates the historical pipeline at the workflow/execution level. Detailed row-level review of every yearly retrieval record remains a separate validation layer and is not implied by workflow success alone.

## 2025 proof-of-concept evidence

The completed 2025 retrieval produced:

- 20,495,507 retained U.S. core observation rows
- 31,742 unique stations
- date coverage from 2025-01-01 through 2025-12-31
- core elements PRCP, SNOW, SNWD, TMAX, and TMIN
- compressed NOAA source size of 158,395,357 bytes
- processed Parquet size of 442,769,277 bytes
- source and processed SHA-256 checksums recorded by the retrieval process

The retrieval completed after the implementation was changed to filter the compressed global NOAA stream before pandas/Arrow batching.

## Historical compatibility evidence

The same predefined workflow succeeded independently for 2016 in Run `37058669748`, establishing an older-year compatibility gate before scaling. A separate cancelled run `37058701233` is excluded from validation evidence.

## Full 2016–2025 historical build

Owner-triggered GitHub Actions Run `37060323541` executed the historical matrix for:

2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, and 2025.

Result: **success**.

The historical run produced exactly ten yearly artifacts:

- `us-daily-weather-2016`
- `us-daily-weather-2017`
- `us-daily-weather-2018`
- `us-daily-weather-2019`
- `us-daily-weather-2020`
- `us-daily-weather-2021`
- `us-daily-weather-2022`
- `us-daily-weather-2023`
- `us-daily-weather-2024`
- `us-daily-weather-2025`

The workflow's `single-year` job was skipped as intended because historical mode was selected. Each historical matrix job independently completed retrieval/processing and artifact upload.

Artifacts are temporary GitHub Actions outputs and expire after the configured retention period. They are evidence and transfer outputs, not permanent project storage.

## Validation conclusion

The retrieval architecture has demonstrated successful execution across the complete planned 2016–2025 window using one owner-triggered historical workflow. This clears the project to proceed toward model preparation.

Workflow success confirms execution and artifact creation. Before a model is treated as production-quality, model preparation should consume and validate the yearly retrieval records and perform data-quality checks appropriate to the selected prediction target.
