# U.S. Daily Weather — Data Dictionary

## Purpose

This is the master source-to-model crosswalk for the fields currently produced by the U.S. Daily Weather retrieval pipeline. It combines GHCN-Daily annual observations with the station metadata joined by `station_id`.

**Authoritative source documentation:** NOAA NCEI GHCN-Daily `readme.txt` and the project's retrieval script.

## Current combined dataset

| Final field | Meaning | Type | Source dataset/system | Source table/file | Source field(s) | Source unit | Current final unit | Transformation / notes | Modeling use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `station_id` | Unique GHCN-Daily station identifier. | Text | NOAA GHCN-Daily | Annual by-year CSV + `ghcnd-stations.txt` | ID | None | None | Used as the join key. The pipeline keeps station IDs present in the U.S. station metadata subset. | Station identity; grouping; location resolution. |
| `date` | Calendar date of the daily observation. | Date/datetime | NOAA GHCN-Daily | Annual by-year CSV | DATE | YYYYMMDD in source | Parsed date | Parsed with format `%Y%m%d`. | Time ordering, lags, seasonal features, train/validation/test split. |
| `element` | Code identifying the weather measurement represented by the row. | Text/code | NOAA GHCN-Daily | Annual by-year CSV | ELEMENT | None | None | V1 retrieval keeps only PRCP, SNOW, SNWD, TMAX, and TMIN. | Determines target/feature meaning. |
| `value` | Numeric observation for the row's element. | Numeric | NOAA GHCN-Daily | Annual by-year CSV | DATA VALUE | Depends on `element` | Source unit retained | Converted to numeric, but the retrieval script does **not** yet rescale values. TMAX/TMIN and PRCP therefore retain NOAA tenths-based source units; SNOW/SNWD are millimeters. | Raw measurement used to construct targets and weather-history features. |
| `mflag` | NOAA measurement flag describing how certain measurements were obtained or represented. | Text/code, nullable | NOAA GHCN-Daily | Annual by-year CSV | M-FLAG | None | None | Blank means no measurement information applicable. Codes require NOAA flag interpretation during profiling/quality-rule design. | Data-quality/provenance context; not assumed to be a predictive feature. |
| `qflag` | NOAA quality flag identifying observations that failed a NOAA quality-assurance check. | Text/code, nullable | NOAA GHCN-Daily | Annual by-year CSV | Q-FLAG | None | None | Blank means the value did not fail a listed QA check. Nonblank values must be profiled before modeling rules are set. | Quality filtering/validation; not assumed to be a predictive feature. |
| `sflag` | NOAA source flag identifying the source from which the observation was selected. | Text/code, nullable | NOAA GHCN-Daily | Annual by-year CSV | S-FLAG | None | None | Preserve for provenance. NOAA can select among multiple available sources according to its source-priority rules. | Provenance and quality analysis; not assumed to be a predictive feature. |
| `obstime` | Time of observation when supplied by the by-year data. | Text/time-like, nullable | NOAA GHCN-Daily | Annual by-year CSV | OBS-TIME | HHMM local station time when available | Source representation retained | Optional. The retrieval script currently preserves the source field without converting it. | Profiling/context; V1 modeling use not yet established. |
| `latitude` | Station latitude. | Numeric | NOAA GHCN-Daily | `ghcnd-stations.txt` | LATITUDE | Decimal degrees | Decimal degrees | Joined to each observation by `station_id`. | V1 geographic feature and map/station resolution. |
| `longitude` | Station longitude. | Numeric | NOAA GHCN-Daily | `ghcnd-stations.txt` | LONGITUDE | Decimal degrees | Decimal degrees | Joined to each observation by `station_id`. | V1 geographic feature and map/station resolution. |
| `elevation` | Station elevation. | Numeric | NOAA GHCN-Daily | `ghcnd-stations.txt` | ELEVATION | Meters | Meters | NOAA documents -999.9 as missing. The retrieval script currently preserves the source value; profiling must quantify and standardize missing elevation before modeling. | V1 geographic/topographic feature. |
| `state` | U.S. postal code for the station's state/territory. | Text/code, nullable | NOAA GHCN-Daily | `ghcnd-stations.txt` | STATE | None | None | Joined by `station_id`. | Geographic profiling, reporting, and app/location support. |
| `station_name` | NOAA station name. | Text | NOAA GHCN-Daily | `ghcnd-stations.txt` | NAME | None | None | Joined by `station_id`. | Human-readable station identification and location support. |

## Element codes and units

| Element | Full name | NOAA source unit | Meaning in this project |
| --- | --- | --- | --- |
| `TMAX` | Maximum temperature | Tenths of degrees Celsius | Daily maximum temperature; V1 prediction target. Divide raw value by 10 for degrees Celsius before human-facing/model-standardized use. |
| `TMIN` | Minimum temperature | Tenths of degrees Celsius | Daily minimum temperature; V1 prediction target. Divide raw value by 10 for degrees Celsius before human-facing/model-standardized use. |
| `PRCP` | Precipitation | Tenths of millimeters | Daily precipitation. Divide raw value by 10 for millimeters before standardized use. |
| `SNOW` | Snowfall | Millimeters | Daily snowfall. |
| `SNWD` | Snow depth | Millimeters | Snow depth. |

## Flag interpretation

### Measurement flag (`mflag`)
The measurement flag records special measurement/derivation information. Examples relevant to the retained elements include trace precipitation/snow, temperatures derived from hourly extremes, and precipitation totals formed from shorter-period totals. Blank means no measurement information is applicable.

### Quality flag (`qflag`)
Blank means the observation did not fail a listed NOAA quality-assurance check. Nonblank codes identify a failed check such as duplicate, gap, internal consistency, climatological outlier, spatial consistency, temporal consistency, or bounds checks. Phase 1 profiling must count these codes and establish a documented modeling rule before flagged observations are included or excluded.

### Source flag (`sflag`)
The source flag identifies the contributing source selected by GHCN-Daily. Preserve it for provenance and profile its distribution; do not treat different source codes as interchangeable without evidence.

## Current transformation boundary

The retrieval pipeline currently performs a deliberately small set of transformations:

1. Filters station metadata to station IDs beginning with `US`.
2. Filters annual observations to those U.S. station IDs.
3. Keeps the five core elements PRCP, SNOW, SNWD, TMAX, and TMIN.
4. Parses `date` to a datetime value.
5. Converts `value` to numeric.
6. Joins latitude, longitude, elevation, state, and station name by `station_id`.
7. Writes the result to Parquet.

It does **not** currently convert the weather measurements to display/model units, resolve NOAA quality flags, replace elevation's -999.9 missing sentinel, pivot elements into one row per station/date, or construct model features. Those decisions belong to profiling and Phase 2 feature engineering.

## Profiling items still required

The dictionary defines what the fields mean; it does not prove their quality. Phase 1 still needs to measure:

- row and distinct-station counts across the full 2016–2025 period;
- date and geographic coverage;
- null/missingness by field and element;
- duplicate station/date/element records;
- distributions of `mflag`, `qflag`, and `sflag`;
- invalid or implausible ranges;
- elevation missing sentinel frequency;
- station-level TMAX/TMIN completeness and continuity;
- whether the retained observations are sufficient for the approved modeling population.

## Sources

- NOAA NCEI GHCN-Daily documentation: `https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt`
- NOAA annual data directory: `https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/`
- NOAA station metadata: `https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt`
- Project retrieval implementation: `scripts/retrieve_ghcnd.py`
