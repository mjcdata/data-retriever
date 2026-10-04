#!/usr/bin/env python3
"""Profile geographic station and observation coverage for processed U.S. GHCN-Daily data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.compute as pc
import pyarrow.dataset as ds


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def main(input_dir: Path, output: Path) -> None:
    files = sorted(input_dir.glob("us_ghcnd_*.parquet"))
    if not files:
        raise FileNotFoundError(f"No us_ghcnd_*.parquet files found in {input_dir}")

    dataset = ds.dataset([str(path) for path in files], format="parquet")
    table = dataset.to_table(columns=["station_id", "state", "latitude", "longitude"])

    station_rows = table.select(["station_id", "state", "latitude", "longitude"]).group_by(
        ["station_id", "state", "latitude", "longitude"]
    ).aggregate([])

    observations_by_state: dict[str, int] = {}
    stations_by_state: dict[str, set[str]] = {}
    missing_state_observations = 0

    station_ids = table["station_id"].to_pylist()
    states = table["state"].to_pylist()
    for station_id, raw_state in zip(station_ids, states):
        state = _text(raw_state)
        if not state:
            missing_state_observations += 1
            continue
        observations_by_state[state] = observations_by_state.get(state, 0) + 1
        stations_by_state.setdefault(state, set()).add(str(station_id))

    station_records = station_rows.to_pylist()
    missing_state_stations = sum(1 for row in station_records if not _text(row["state"]))
    missing_coordinate_stations = sum(
        1
        for row in station_records
        if row["latitude"] is None or row["longitude"] is None
    )

    states_present = sorted(stations_by_state)
    state_coverage = [
        {
            "state": state,
            "stations": len(stations_by_state[state]),
            "observations": observations_by_state[state],
        }
        for state in states_present
    ]

    result = {
        "profile": "P1T3 Geographic Coverage",
        "input_pattern": "us_ghcnd_*.parquet",
        "overall": {
            "observations": int(table.num_rows),
            "deduplicated_station_metadata_rows": int(station_rows.num_rows),
            "state_codes_present": len(states_present),
            "missing_state_observations": int(missing_state_observations),
            "missing_state_stations": int(missing_state_stations),
            "missing_coordinate_stations": int(missing_coordinate_stations),
        },
        "coverage_by_state_or_territory": state_coverage,
        "limitations": [
            "State/territory coverage describes NOAA station metadata coverage, not uniform spatial density within each state.",
            "Observation counts reflect retained PRCP, SNOW, SNWD, TMAX, and TMIN rows and should not be interpreted as equal target availability.",
            "Stations with blank state metadata are reported separately rather than assigned to a location.",
            "Coordinate completeness is reported at the deduplicated station-metadata level; geographic density and unsupported-location behavior require later station-eligibility and app-resolution analysis.",
        ],
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
        / "P1T3_GEOGRAPHIC_COVERAGE.json",
    )
    args = parser.parse_args()
    main(args.input_dir, args.output)
