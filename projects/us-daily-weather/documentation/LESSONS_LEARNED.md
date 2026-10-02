# U.S. Daily Weather — Lessons Learned

## 2025 retrieval proof of concept

1. **Filter before pandas when the upstream file is much larger than the desired subset.** The NOAA annual file is global. A pandas-first approach was terminated in the available Codespaces environment. Streaming the gzip CSV and retaining only U.S. core observations before creating pandas/Arrow batches completed successfully.

2. **One measured year is more useful than relying only on rough source-size estimates.** The 2025 run produced 20,495,507 U.S. core rows and a 442,769,277-byte Parquet file, projecting to roughly 4.12 GiB across ten similarly sized years.

3. **The full historical dataset should not live in ordinary Git history.** GitHub is appropriate for code, documentation, retrieval records, audit records, validation evidence, and small samples. Bulk historical outputs need local or external persistence.

4. **GitHub Actions is a viable owner-directed execution environment.** The same predefined retrieval script completed successfully through a manually triggered workflow, so the owner does not need to keep a local machine or Codespace running for this type of retrieval.

5. **Workflow artifacts are useful for transfer and inspection, not permanent storage.** The successful run uploaded the processed output as a temporary artifact with limited retention. Long-term persistence must be handled separately when required.

6. **Historical compatibility should be tested before scaling.** A successful recent-year run does not prove every older annual file will behave identically. Test one older year before launching the approximately ten-year build.
