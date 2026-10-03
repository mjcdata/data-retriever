# U.S. Daily Weather — Project Lessons

This file records lessons specific to the U.S. Daily Weather project. Lessons that become broadly reusable across Data Retriever projects should be promoted to the repository-root `LESSONS_LEARNED.md`.

## Retrieval and processing

1. **NOAA GHCN-Daily annual files are global.** The U.S. Daily Weather pipeline must filter for U.S. stations and the approved core weather elements before downstream processing.

2. **The pandas-first retrieval attempt exceeded the available execution memory.** Streaming the NOAA gzip, filtering first, and writing in batches completed successfully.

3. **The 2025 proof-of-concept established the project's measured scale.** It produced 20,495,507 U.S. core rows and a 442,769,277-byte processed Parquet file.

4. **A 2016 compatibility run succeeded before the historical build was scaled.**

5. **The predefined owner-triggered workflow successfully processed 2016–2025.** GitHub Actions Run `37060323541` produced ten yearly artifacts.

## Storage and reproducibility

6. **The full historical weather dataset is too large for ordinary Git history under the approved storage design.** GitHub retains code, documentation, provenance, validation/audit records, retrieval metadata, and small samples while bulk data remains outside ordinary Git tracking.

7. **NOAA remains the authoritative upstream source, so the historical dataset can be rebuilt from the retrieval pipeline when needed.**

8. **The yearly GitHub Actions artifacts are temporary handoff outputs, not the project's durable data store.**

## Validation and modeling boundary

9. **Historical workflow success validates execution and artifact creation, not row-level modeling quality.** Profiling, target coverage, flag interpretation, duplicates, ranges, and modeling eligibility remain separate validation work.

10. **The approved modeling target is daily TMAX and TMIN.** Actual target-day values must remain excluded from model inputs to prevent leakage.
