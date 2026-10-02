# U.S. Daily Weather — Lessons Learned

## Retrieval and processing

1. **Filter before pandas when the upstream file is much larger than the desired subset.** The NOAA annual file is global. A pandas-first approach was terminated; streaming and filtering U.S. core observations before pandas/Arrow batching completed successfully.

2. **Measured execution is more useful than relying only on estimates.** The 2025 run produced 20,495,507 U.S. core rows and a 442,769,277-byte Parquet file, providing a concrete scale reference.

3. **Historical compatibility should be tested before scaling.** The 2016 compatibility run succeeded before the full historical matrix was launched.

4. **The full 2016–2025 historical matrix can run successfully through the predefined owner-triggered workflow.** Run `37060323541` completed successfully and produced ten yearly artifacts.

## Storage and reproducibility

5. **The full historical dataset should not live in ordinary Git history.** GitHub is appropriate for code, documentation, provenance, validation evidence, audit records, model artifacts when appropriately sized, and small samples.

6. **Rebuildability can replace permanent bulk-data persistence.** Because NOAA remains the authoritative source and the retrieval pipeline can reconstruct the historical dataset, permanent storage of the multi-gigabyte processed training set is optional when continuous availability is unnecessary.

7. **Workflow artifacts are temporary handoff outputs.** They are useful for validation, transfer, and downstream model-building work but should not be treated as permanent storage.

8. **Preserve the model and its reproducibility chain.** After training, retain the model artifact plus feature/preprocessing code, configuration/dependencies, evaluation results, and source/retrieval provenance needed to rebuild the training set.

## Execution and security

9. **Owner-directed GitHub Actions provides a useful execution boundary.** The agent can prepare auditable scripts and workflows while the owner explicitly authorizes runtime execution.

10. **Workflow success and data-quality validation are different gates.** Successful jobs and artifact creation prove that the pipeline executed across all ten years; target-specific row-level and feature-quality checks remain part of model preparation.
