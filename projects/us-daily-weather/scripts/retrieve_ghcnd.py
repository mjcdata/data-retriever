#!/usr/bin/env python3
"""Retrieve and size one year of U.S. NOAA GHCN-Daily data."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

BASE = "https://www.ncei.noaa.gov/pub/data/ghcn/daily"
COLUMNS = ["station_id", "date", "element", "value", "mflag", "qflag", "sflag", "obstime"]
CORE = {"PRCP", "SNOW", "SNWD", "TMAX", "TMIN"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_stations(path: Path) -> pd.DataFrame:
    specs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71)]
    names = ["station_id", "latitude", "longitude", "elevation", "state", "station_name"]
    df = pd.read_fwf(
        path,
        colspecs=specs,
        names=names,
        dtype={"station_id": "string", "state": "string"},
    )
    return df[df["station_id"].str.startswith("US", na=False)].copy()


def main(year: int, root: Path) -> None:
    raw = root / "data" / "raw"
    processed = root / "data" / "processed"
    samples = root / "data" / "samples"
    records = root / "retrieval_records"
    for p in (raw, processed, samples, records):
        p.mkdir(parents=True, exist_ok=True)

    annual_url = f"{BASE}/by_year/{year}.csv.gz"
    stations_url = f"{BASE}/ghcnd-stations.txt"
    annual_path = raw / f"{year}.csv.gz"
    stations_path = raw / "ghcnd-stations.txt"

    if not annual_path.exists():
        print(f"Downloading {annual_url}")
        urlretrieve(annual_url, annual_path)
    if not stations_path.exists():
        print(f"Downloading {stations_url}")
        urlretrieve(stations_url, stations_path)

    stations = parse_stations(stations_path)
    us_ids = set(stations["station_id"].dropna())

    parquet_path = processed / f"us_ghcnd_{year}.parquet"
    sample_path = samples / f"us_ghcnd_{year}_sample.csv"
    if parquet_path.exists():
        parquet_path.unlink()
    if sample_path.exists():
        sample_path.unlink()

    writer = None
    sample_frames = []
    sample_rows = 0
    row_count = 0
    station_ids_seen = set()
    date_min = None
    date_max = None

    try:
        for chunk_number, chunk in enumerate(
            pd.read_csv(
                annual_path,
                compression="gzip",
                header=None,
                names=COLUMNS,
                dtype={
                    "station_id": "string",
                    "element": "string",
                    "mflag": "string",
                    "qflag": "string",
                    "sflag": "string",
                    "obstime": "string",
                },
                chunksize=250_000,
            ),
            start=1,
        ):
            chunk = chunk[chunk["station_id"].isin(us_ids) & chunk["element"].isin(CORE)].copy()
            if chunk.empty:
                continue

            chunk["date"] = pd.to_datetime(chunk["date"].astype(str), format="%Y%m%d")
            result = chunk.merge(stations, on="station_id", how="left", validate="many_to_one")

            table = pa.Table.from_pandas(result, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(parquet_path, table.schema, compression="snappy")
            writer.write_table(table)

            row_count += len(result)
            station_ids_seen.update(result["station_id"].dropna().tolist())
            chunk_min = result["date"].min()
            chunk_max = result["date"].max()
            date_min = chunk_min if date_min is None or chunk_min < date_min else date_min
            date_max = chunk_max if date_max is None or chunk_max > date_max else date_max

            if sample_rows < 1000:
                take = result.head(1000 - sample_rows)
                sample_frames.append(take)
                sample_rows += len(take)

            if chunk_number % 20 == 0:
                print(f"Processed {chunk_number:,} source chunks; retained {row_count:,} rows")

    finally:
        if writer is not None:
            writer.close()

    if row_count == 0 or not parquet_path.exists():
        raise RuntimeError("No matching U.S. core weather observations were found.")

    if sample_frames:
        pd.concat(sample_frames, ignore_index=True).to_csv(sample_path, index=False)

    source_bytes = annual_path.stat().st_size
    parquet_bytes = parquet_path.stat().st_size
    record = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "year": year,
        "source_url": annual_url,
        "station_metadata_url": stations_url,
        "source_bytes": source_bytes,
        "source_sha256": sha256(annual_path),
        "us_core_rows": int(row_count),
        "unique_stations": int(len(station_ids_seen)),
        "date_min": date_min.date().isoformat(),
        "date_max": date_max.date().isoformat(),
        "parquet_bytes": parquet_bytes,
        "parquet_sha256": sha256(parquet_path),
        "projected_ten_year_parquet_bytes": parquet_bytes * 10,
        "core_elements": sorted(CORE),
    }
    record_path = records / f"ghcnd_{year}_poc.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2025)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    main(args.year, args.project_root)
