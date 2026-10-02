# U.S. Daily Weather — Data Storage Decision

## Decision date
2026-10-02

## Decision

Use a **hybrid storage approach**:

- GitHub stores project documentation, retrieval and processing code, schemas/metadata, retrieval records/checksums when practical, validation artifacts, and small samples.
- Full raw and processed nationwide weather data should **not** be committed directly to GitHub by default.
- NOAA NCEI remains the authoritative upstream source from which raw data can be reproduced.
- The project should create a reproducible local/external data directory structure for raw and processed files. The measured proof of concept confirms that full processed history should remain outside ordinary Git tracking. The exact long-term external persistence service may be selected before the full historical build if durable storage beyond transient GitHub Actions artifacts is required.

## Rationale

The 2025 proof of concept measured a 158,395,357-byte compressed NOAA annual source file and a 442,769,277-byte U.S.-only processed Parquet output containing 20,495,507 core observation rows. A straight-line projection from that measured processed output is 4,427,692,770 bytes (approximately 4.12 GiB) for ten years before allowing for year-to-year variation, additional derivatives, refreshes, or validation artifacts. This is beyond what is sensible to version as ordinary GitHub repository content.

The project is intended to update over time, which makes repeatedly committing large changing data files especially undesirable.

Keeping retrieval code and provenance in GitHub while treating NOAA as the reproducible source preserves traceability without turning the repository into bulk data storage.

## Planned project structure

- `planning/` — approved planning and decision records
- `documentation/` — execution and data documentation
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

The hybrid storage decision is confirmed by measured Phase 3 results. Full raw and processed historical data will not be committed to ordinary Git history. GitHub Actions artifacts may be used for temporary execution transfer/inspection, but their retention period does not make them the authoritative long-term data store. A durable external persistence mechanism should be selected before the full historical build if the resulting dataset must remain continuously available without rebuilding from NOAA.
