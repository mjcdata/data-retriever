#!/usr/bin/env python3
"""Profile one processed U.S. GHCN-Daily year and build compact Phase 1 outputs."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import duckdb
import pandas as pd

def main(year:int, root:Path)->None:
    parquet=root/"data"/"processed"/f"us_ghcnd_{year}.parquet"
    out=root/"profiling"; out.mkdir(parents=True,exist_ok=True)
    if not parquet.exists(): raise FileNotFoundError(parquet)
    con=duckdb.connect(); src=str(parquet).replace("'","''")
    overall=con.execute(f"""SELECT COUNT(*) rows, COUNT(DISTINCT station_id) unique_stations,
      MIN(date) date_min, MAX(date) date_max, SUM(value IS NULL)::BIGINT null_values,
      SUM(latitude IS NULL)::BIGINT null_latitude, SUM(longitude IS NULL)::BIGINT null_longitude,
      SUM(elevation IS NULL)::BIGINT null_elevation, SUM(state IS NULL)::BIGINT null_state,
      SUM(station_name IS NULL)::BIGINT null_station_name FROM read_parquet('{src}')""").fetchdf().iloc[0].to_dict()
    con.execute(f"""COPY (SELECT element, COUNT(*) rows, COUNT(DISTINCT station_id) stations,
      MIN(value) min_value, MAX(value) max_value, SUM(value IS NULL)::BIGINT null_values,
      SUM(NULLIF(TRIM(COALESCE(mflag,'')),'') IS NOT NULL)::BIGINT mflag_rows,
      SUM(NULLIF(TRIM(COALESCE(qflag,'')),'') IS NOT NULL)::BIGINT qflag_rows,
      SUM(NULLIF(TRIM(COALESCE(sflag,'')),'') IS NOT NULL)::BIGINT sflag_rows
      FROM read_parquet('{src}') GROUP BY element ORDER BY element)
      TO '{str(out/f"element_profile_{year}.csv")}' (HEADER, DELIMITER ',')""")
    station=con.execute(f"""SELECT station_id, MAX(latitude) latitude, MAX(longitude) longitude,
      MAX(elevation) elevation, MAX(state) state, MAX(station_name) station_name,
      COUNT(DISTINCT CASE WHEN element='TMAX' THEN date END) tmax_days,
      COUNT(DISTINCT CASE WHEN element='TMIN' THEN date END) tmin_days
      FROM read_parquet('{src}') GROUP BY station_id ORDER BY station_id""").fetchdf()
    days=366 if pd.Timestamp(f"{year}-12-31").dayofyear==366 else 365
    station["calendar_days"]=days
    station["tmax_coverage_pct"]=station.tmax_days/days*100
    station["tmin_coverage_pct"]=station.tmin_days/days*100
    station.to_csv(out/f"station_profile_{year}.csv",index=False)
    dup=con.execute(f"""SELECT COALESCE(SUM(n-1),0)::BIGINT FROM
      (SELECT COUNT(*) n FROM read_parquet('{src}') GROUP BY station_id,date,element HAVING COUNT(*)>1)""").fetchone()[0]
    con.execute(f"""COPY (
      SELECT 'mflag' flag_type, COALESCE(NULLIF(TRIM(mflag),''),'(blank)') flag, COUNT(*) rows FROM read_parquet('{src}') GROUP BY 1,2
      UNION ALL SELECT 'qflag',COALESCE(NULLIF(TRIM(qflag),''),'(blank)'),COUNT(*) FROM read_parquet('{src}') GROUP BY 1,2
      UNION ALL SELECT 'sflag',COALESCE(NULLIF(TRIM(sflag),''),'(blank)'),COUNT(*) FROM read_parquet('{src}') GROUP BY 1,2
      ORDER BY 1,2) TO '{str(out/f"flag_profile_{year}.csv")}' (HEADER, DELIMITER ',')""")
    def clean(v):
        if isinstance(v,pd.Timestamp): return v.date().isoformat()
        if pd.isna(v): return None
        return v.item() if hasattr(v,"item") else v
    summary={k:clean(v) for k,v in overall.items()}
    summary.update({"year":year,"duplicate_station_date_element_rows":int(dup)})
    (out/f"profile_{year}.json").write_text(json.dumps(summary,indent=2)+"\n")
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--year",type=int,required=True)
    p.add_argument("--project-root",type=Path,default=Path(__file__).resolve().parents[1])
    a=p.parse_args(); main(a.year,a.project_root)
