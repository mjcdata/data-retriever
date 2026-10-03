#!/usr/bin/env python3
"""Profile the structure of processed U.S. GHCN-Daily yearly Parquet files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.parquet as pq

CORE_ELEMENTS = ("PRCP", "SNOW", "SNWD", "TMAX", "TMIN")


def profile_file(path: Path) -> dict:
    dataset = ds.dataset(path, format="parquet")
    table = dataset.to_table(columns=["station_id", "date", "element"])

    rows = table.num_rows
    station_count = pc.count_distinct(table["station_id"]).as_py()
    date_min = pc.min(table["date"]).as_py()
    date_max = pc.max(table["date"]).as_py()

    elements = {}
    for element in CORE_ELEMENTS:
        elements[element] = int(pc.sum(pc.equal(table["element"], element)).as_py() or 0)

    return {
        "file": path.name,
        "rows": int(rows),
        "unique_stations": int(station_count),
        "date_min": date_min.date().isoformat() if hasattr(date_min, "date") else str(date_min),
        "date_max": date_max.date().isoformat() if hasattr(date_max, "date") else str(date_max),
        "element_counts": elements,
    }


def main(input_dir: Path, output: Path) -> None:
    files = sorted(input_dir.glob("us_ghcnd_*.parquet"))
    if not files:
        raise FileNotFoundError(f"No us_ghcnd_*.parquet files found in {input_dir}")

    yearly = [profile_file(path) for path in files]
    full_dataset = ds.dataset([str(path) for path in files], format="parquet")
    station_table = full_dataset.to_table(columns=["station_id"])

    totals = {
        "total_rows": sum(item["rows"] for item in yearly),
        "deduplicated_stations": int(pc.count_distinct(station_table["station_id"]).as_py()),
        "date_min": min(item["date_min"] for item in yearly),
        "date_max": max(item["date_max"] for item in yearly),
        "element_counts": {
            element: sum(item["element_counts"][element] for item in yearly)
            for element in CORE_ELEMENTS
        },
    }

    result = {
        "profile": "P1T2 Dataset Structure Profile",
        "input_pattern": "us_ghcnd_*.parquet",
        "yearly": yearly,
        "overall": totals,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "processed",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "audit"
        / "profiles"
        / "P1T2_DATASET_STRUCTURE.json",
    )
    args = parser.parse_args()
    main(args.input_dir, args.output)
