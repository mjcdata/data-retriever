# U.S. Daily Weather — Retrieval Architecture

## Status
Phase 3 retrieval architecture approved for proof-of-concept execution.

## Objective
Build a reproducible retrieval pipeline for approximately ten years of nationwide U.S. NOAA GHCN-Daily observations, with repeatable refreshes for forecasting-oriented downstream work.

## Source
Primary source: NOAA NCEI Global Historical Climatology Network Daily (GHCNd)

Bulk root: https://www.ncei.noaa.gov/pub/data/ghcn/daily/

Annual files: https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/

Station metadata: https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt

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
Before the nationwide ten-year load, run a small retrieval that exercises the same architecture:
- retrieve NOAA station metadata;
- retrieve one annual bulk file;
- select a small U.S. station subset;
- retain PRCP, SNOW, SNWD, TMAX, TMIN and NOAA flags;
- verify dates, station joins, units, missing values, and quality flags;
- create a sample output and retrieval record.

The proof of concept is successful only if another run can reproduce the same transformation from the documented NOAA source.

## Data integrity rules
- Never convert NOAA missing values into observed zeroes.
- Preserve original NOAA flags.
- Keep raw/source values distinguishable from transformed analytical values.
- Record unit conversions explicitly.
- Do not silently discard flagged observations; quality handling belongs to profiling/cleaning and must be documented.

## Full-load gate
Proceed to the full ten-year nationwide retrieval only after the proof of concept validates the file format, U.S. filtering, core variables, station metadata join, retrieval record, and expected storage footprint.
