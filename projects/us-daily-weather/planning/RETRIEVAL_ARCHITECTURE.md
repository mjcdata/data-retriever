# U.S. Daily Weather — Retrieval Architecture

## Status
Phase 3 proof of concept completed and independently re-executed successfully through the owner-directed GitHub Actions workflow.

## Objective
Build a reproducible retrieval pipeline for approximately ten years of nationwide U.S. NOAA GHCN-Daily observations, with repeatable refreshes for forecasting-oriented downstream work.

## Source
Primary source: NOAA NCEI Global Historical Climatology Network Daily (GHCNd)

Bulk root: https://www.ncei.noaa.gov/pub/data/ghcn/daily/

Annual files: https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/

Station metadata: https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt

## Retrieval method
- Implementation language: Python.
- Primary access method: NOAA bulk files over HTTPS.
- Historical annual files are read from NOAA's `by_year` bulk directory.
- Pandas may be used as the in-memory processing layer.
- Processed analytical output will be written to Parquet for the proof of concept.
- The NOAA API is not the primary historical retrieval method; it may be evaluated later for targeted or incremental use cases.

Planned script: `scripts/retrieve_ghcnd.py`.

## Initial historical retrieval
1. Retrieve station metadata and identify U.S. stations.
2. Retrieve annual GHCNd bulk files for the approved approximately ten-year window.
3. Filter observations to U.S. station IDs.
4. Preserve the five core elements required by the project: PRCP, SNOW, SNWD, TMAX, and TMIN.
5. Preserve NOAA measurement, quality, and source flags.
6. Join station metadata needed for geographic use, including station ID, latitude, longitude, elevation, state, and station name.
7. Write processed data using the storage strategy defined in planning/DATA_STORAGE.md.
8. Create a durable retrieval record containing source URLs, retrieval date, files retrieved, file sizes and checksums when practical, date coverage, filters applied, and output inventory.

## Incremental refresh strategy
Do not treat recent observations as immutable. Refresh a recent rolling window so preliminary observations can be replaced by later archive-quality values. The exact rolling-window duration will be finalized after the proof of concept and source behavior are profiled.

Each refresh must be reproducible and produce a new retrieval record.

## Proof of concept
Use calendar year **2025**, a completed year, for the first storage-sizing proof of concept.

The proof of concept will:
- retrieve NOAA station metadata;
- retrieve the 2025 annual bulk file;
- identify and retain U.S. stations;
- retain PRCP, SNOW, SNWD, TMAX, TMIN and NOAA flags;
- join station metadata;
- write the processed U.S.-only result to Parquet;
- measure the downloaded compressed source file size;
- measure the U.S.-only processed Parquet size;
- record row counts and basic coverage;
- estimate the approximate ten-year processed storage footprint from the measured one-year result;
- create a small GitHub-safe sample and a retrieval record.

The storage measurement is part of the proof of concept. Do not decide that the full processed dataset belongs in GitHub or external storage until the measured result is reviewed against repository practicality and the storage rules in `planning/DATA_STORAGE.md`.

The proof of concept is successful only if another run can reproduce the same transformation from the documented NOAA source.

## Proof-of-concept results

The 2025 proof of concept completed successfully with the following measured results:

- U.S. core observation rows: **20,495,507**
- Unique U.S. stations represented: **31,742**
- Date coverage: **2025-01-01 through 2025-12-31**
- Downloaded compressed NOAA annual source: **158,395,357 bytes**
- Processed Parquet output: **442,769,277 bytes**
- Straight-line ten-year Parquet projection: **4,427,692,770 bytes** (approximately 4.12 GiB)
- Core elements retained: PRCP, SNOW, SNWD, TMAX, TMIN

The initial pandas-first processing approach was terminated in the available Codespaces environment. The retrieval implementation was revised to stream the compressed NOAA CSV with Python's gzip/csv readers, filter to U.S. stations and core elements before constructing pandas/Arrow batches, and write those batches incrementally to Parquet. That approach completed successfully.

The same predefined retrieval script was then executed through the manually triggered GitHub Actions workflow for 2025. GitHub Actions Run `37053074876` completed successfully, including retrieval/processing and artifact upload. Artifact `us-daily-weather-2025` was created as temporary execution output.

The proof of concept therefore validates the retrieval path, U.S. filtering, core-element filtering, station metadata join, processed Parquet generation, retrieval-record generation, and owner-directed GitHub Actions execution path. Before the full historical build, one older year should be executed and checked for historical compatibility.

## Data integrity rules
- Never convert NOAA missing values into observed zeroes.
- Preserve original NOAA flags.
- Keep raw/source values distinguishable from transformed analytical values.
- Record unit conversions explicitly.
- Do not silently discard flagged observations; quality handling belongs to profiling/cleaning and must be documented.

## Full-load gate
The 2025 proof-of-concept gate has passed. The next gate is a single older-year compatibility run. Proceed to the full approximately ten-year nationwide retrieval only after that older-year run succeeds and its output is reviewed.
