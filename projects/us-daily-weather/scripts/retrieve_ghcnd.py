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
    specs = [(0,11),(12,20),(21,30),(31,37),(38,40),(41,71)]
    names = ["station_id","latitude","longitude","elevation","state","station_name"]
    df = pd.read_fwf(path, colspecs=specs, names=names, dtype={"station_id":"string","state":"string"})
    # GHCN station IDs beginning with US are U.S. stations.
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
        urlretrieve(annual_url, annual_path)
    if not stations_path.exists():
        urlretrieve(stations_url, stations_path)

    stations = parse_stations(stations_path)
    us_ids = set(stations["station_id"].dropna())

    chunks = []
    for chunk in pd.read_csv(
        annual_path,
        compression="gzip",
        header=None,
        names=COLUMNS,
        dtype={"station_id":"string","element":"string","mflag":"string","qflag":"string","sflag":"string","obstime":"string"},
        chunksize=1_000_000,
    ):
        chunk = chunk[chunk["station_id"].isin(us_ids) & chunk["element"].isin(CORE)]
        if not chunk.empty:
            chunks.append(chunk)

    weather = pd.concat(chunks, ignore_index=True)
    weather["date"] = pd.to_datetime(weather["date"].astype(str), format="%Y%m%d")
    result = weather.merge(stations, on="station_id", how="left", validate="many_to_one")

    parquet_path = processed / f"us_ghcnd_{year}.parquet"
    result.to_parquet(parquet_path, index=False)
    result.head(1000).to_csv(samples / f"us_ghcnd_{year}_sample.csv", index=False)

    source_bytes = annual_path.stat().st_size
    parquet_bytes = parquet_path.stat().st_size
    record = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "year": year,
        "source_url": annual_url,
        "station_metadata_url": stations_url,
        "source_bytes": source_bytes,
        "source_sha256": sha256(annual_path),
        "us_core_rows": int(len(result)),
        "unique_stations": int(result["station_id"].nunique()),
        "date_min": result["date"].min().date().isoformat(),
        "date_max": result["date"].max().date().isoformat(),
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
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    main(args.year, args.project_root)
