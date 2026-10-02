# U.S. Daily Weather — Data Storage Decision

## Decision date
2026-10-02

## Decision

Use a **rebuildable-data lifecycle**:

- GitHub stores project documentation, retrieval/processing code, schemas and metadata, compact retrieval records/checksums when practical, validation evidence, model code/configuration, and small samples.
- Full raw and processed nationwide weather data should **not** be committed to ordinary Git history.
- NOAA NCEI remains the authoritative upstream source from which the training data can be rebuilt.
- GitHub Actions artifacts may be used temporarily for execution transfer, inspection, validation, and model-building handoff.
- Permanent storage of the full processed training dataset is optional rather than required when the dataset can be reproducibly rebuilt from NOAA.

## Rationale

The 2025 proof of concept measured a 158,395,357-byte compressed NOAA annual source file and a 442,769,277-byte U.S.-only processed Parquet output containing 20,495,507 core observation rows. A straight-line projection is approximately 4.12 GiB across ten similarly sized years.

The full 2016–2025 historical GitHub Actions build subsequently completed successfully, demonstrating that Data Retriever can reconstruct the historical processed outputs from the authoritative source through an owner-triggered workflow.

Keeping retrieval code, provenance, transformation logic, and validation evidence in GitHub preserves reproducibility without requiring the repository to become a bulk data store.

## Data and model lifecycle

The intended lifecycle is:

**NOAA → reproducible retrieval → temporary processed dataset → validation/feature engineering → model training/testing → preserved model artifact and reproducibility records**

After a model is satisfactorily trained and validated, bulk processed training data may be discarded when continuous availability is unnecessary, provided the source and pipeline remain available to rebuild it.

Rebuild the training set when newer observations are needed, feature engineering changes, the prediction target changes, a processing issue is discovered, retraining is required, or reproducibility/audit work requires reconstruction.

## Planned project structure

- `planning/` — approved planning and decision records
- `documentation/` — execution and data documentation
- `scripts/` — retrieval, transformation, update, and validation code
- `data/raw/` — temporary or externally stored source extracts when needed
- `data/processed/` — temporary or externally stored analysis-ready outputs when needed
- `data/samples/` — small representative samples suitable for GitHub
- `validation/` — validation summaries and compact evidence
- `retrieval_records/` — source versions, retrieval dates, file inventories, checksums when practical

## Reproducibility requirements

Preserve enough metadata to identify the NOAA source, retrieval date, requested years/geography, files obtained, transformation code used, and relevant checksums.

For a trained model, preserve the model artifact, feature/preprocessing code, model configuration and dependency information, training/validation strategy, evaluation results, and the retrieval/provenance information needed to reconstruct the training set.

Because recent observations can be revised upstream, refresh logic must allow recent periods to be re-read rather than assuming prior retrievals are immutable.

## Security

No NOAA API token or other credential may be committed to GitHub. Owner-directed execution remains the default: the agent prepares predefined retrieval/model workflows and the owner explicitly triggers execution unless a different execution mode is separately approved.

## Status

The full historical build has demonstrated that the 2016–2025 processed dataset is reproducibly rebuildable. Permanent multi-gigabyte persistence is therefore not a prerequisite for the project. Temporary artifacts remain subject to their retention period and should not be treated as durable storage.
