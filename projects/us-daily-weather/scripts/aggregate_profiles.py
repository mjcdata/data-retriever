#!/usr/bin/env python3
"""Aggregate yearly station profiles into a compact 2016-2025 completeness profile."""
from pathlib import Path
import json, pandas as pd
root=Path(__file__).resolve().parents[1]; pdir=root/"profiling"
files=sorted(pdir.glob("station_profile_*.csv"))
if not files: raise RuntimeError("No station profiles found")
frames=[]
for f in files:
    year=int(f.stem.rsplit("_",1)[1]); d=pd.read_csv(f); d["year"]=year; frames.append(d)
allp=pd.concat(frames,ignore_index=True)
agg=allp.groupby("station_id",as_index=False).agg(latitude=("latitude","last"),longitude=("longitude","last"),
 elevation=("elevation","last"),state=("state","last"),station_name=("station_name","last"),
 years_present=("year","nunique"),tmax_days=("tmax_days","sum"),tmin_days=("tmin_days","sum"),
 expected_days=("calendar_days","sum"))
agg["tmax_coverage_pct"]=agg.tmax_days/agg.expected_days*100
agg["tmin_coverage_pct"]=agg.tmin_days/agg.expected_days*100
agg["both_coverage_pct"]=agg[["tmax_coverage_pct","tmin_coverage_pct"]].min(axis=1)
agg.to_csv(pdir/"station_completeness_2016_2025.csv",index=False)
qs=[0,.1,.25,.5,.75,.9,1]
summary={"years":[int(x) for x in sorted(allp.year.unique())],"distinct_station_union":int(agg.station_id.nunique()),
"stations_present_all_years":int((agg.years_present==len(files)).sum()),
"tmax_coverage_percentiles":{str(k):float(v) for k,v in agg.tmax_coverage_pct.quantile(qs).items()},
"tmin_coverage_percentiles":{str(k):float(v) for k,v in agg.tmin_coverage_pct.quantile(qs).items()},
"both_coverage_percentiles":{str(k):float(v) for k,v in agg.both_coverage_pct.quantile(qs).items()}}
(pdir/"profiling_summary_2016_2025.json").write_text(json.dumps(summary,indent=2)+"\n")
