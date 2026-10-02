# U.S. Daily Weather — Data Storage Decision

## Decision date
2026-10-02

## Decision

Use a **hybrid storage approach**:

- GitHub stores project documentation, retrieval and processing code, schemas/metadata, retrieval records/checksums when practical, validation artifacts, and small samples.
- Full raw and processed nationwide weather data should **not** be committed directly to GitHub by default.
- NOAA NCEI remains the authoritative upstream source from which raw data can be reproduced.
- The project should create a reproducible local/external data directory structure for raw and processed files. The exact external persistence mechanism can be selected when execution tooling and expected U.S.-only volume are measured during retrieval.

## Rationale

GHCNd's complete global compressed archive is roughly 3.7 GB, and recent global annual compressed CSV files are roughly 160–175 MB each. A ten-year nationwide subset plus extracted/processed derivatives, repeated refreshes, and validation artifacts can grow beyond what is sensible to version as ordinary GitHub repository content.

The project is intended to update over time, which makes repeatedly committing large changing data files especially undesirable.

Keeping retrieval code and provenance in GitHub while treating NOAA as the reproducible source preserves traceability without turning the repository into bulk data storage.

## Planned project structure

- `documentation/` — durable human-readable project records
- `scripts/` — retrieval, transformation, update, and validation code
- `data/raw/` — source extracts, excluded from ordinary Git tracking when large
- `data/processed/` — analysis-ready outputs, excluded from ordinary Git tracking when large
- `data/samples/` — small representative samples suitable for GitHub
- `validation/` — validation summaries and compact evidence
- `retrieval_records/` — source versions, retrieval dates, file inventories, checksums when practical

## Reproducibility requirements

For each retrieval or refresh, preserve enough metadata to identify the NOAA source, retrieval date, requested years/geography, source version where available, files obtained, and transformation code used.

Because NOAA notes that recent U.S. real-time observations can later be replaced by archive-quality data, refresh logic must allow recent periods to be re-read rather than assuming previously retrieved recent observations are immutable.

## Security

No NOAA API token or other credential may be committed to GitHub. Bulk HTTPS access should be preferred where it removes the need for credentials and meets the retrieval requirement.

## Status

Storage strategy approved by framework rules for execution. The external/local persistence implementation may be refined after Phase 3 measures actual U.S.-only data volume; any material change must be documented here.
