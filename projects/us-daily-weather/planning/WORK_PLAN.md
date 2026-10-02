# U.S. Daily Weather — Work Plan

**Status:** In development
**Started:** 2026-10-02

## Purpose
Turn the completed retrieval work and modeling decisions into an execution plan.

## Modeling decisions so far
- Location: map/location input will map to appropriate NOAA station data.
- V1 features: previous-day TMAX/TMIN, recent temperature average/trend, recent precipitation, recent snow and snow depth, time of year, latitude, longitude, and elevation.
- Evaluation order: preserve time order; use 2016–2024 for development and hold out 2025 as unseen final-test data.
- Baseline: persistence — use the prior relevant temperature as the simple benchmark.
- Primary metric: Mean Absolute Error (MAE), reported as average degrees off.
- Model use: save the selected trained model as a reusable artifact so the application can make predictions without retraining on the full history for every request.
- Prediction target: V1 will guess the current temperature without receiving the actual current temperature as an input. The application will compare the model guess with the actual current temperature and report the error. Next-day maximum temperature is not the V1 target.

## Phase 1 — Data Profiling
**Status:** Agreed

### Goal
Understand the structure, meaning, completeness, and quality of the retrieved NOAA weather data before building the modeling dataset.

### Planned work
- Document dataset structure and fields.
- Create or complete the data dictionary.
- Document date fields and their meaning.
- Document NOAA abbreviations, codes, flags, and units in a glossary where applicable.
- Count rows, stations, dates, and relevant observations.
- Measure date, station, and geographic coverage.
- Measure nulls and missing observations.
- Check duplicates.
- Review expected values, ranges, and unusual values.
- Review NOAA measurement, quality, and source flags.
- Check whether stations have sufficient TMAX/TMIN history for the intended model.
- Identify gaps or quality issues that could affect modeling.
- Distinguish expected source behavior from actual data-quality problems.

### Deliverable
A written profiling report documenting findings, limitations, and any data-quality rules required before modeling.

## Phase 2 — Modeling Dataset & Feature Engineering
**Status:** Agreed at a high level; detailed execution depends on Phase 1 findings.

### Goal
Use the profiling results to construct the modeling dataset and implement the agreed V1 features without target leakage.

### Planned direction
- Define the exact calculation for each V1 feature.
- Join observations to required station metadata.
- Construct recent-history features using only information available before the target.
- Apply documented quality rules from Phase 1.
- Preserve time ordering for evaluation.
- Produce a reproducible modeling dataset for baseline and ML training.

## Remaining phases
The remaining work-plan phases will be developed with the owner. Expected later work includes time-split implementation, baseline evaluation, candidate ML training, model evaluation, model artifact preservation, and the interactive application.

## Execution rule
Follow the Data Retriever owner-directed execution model. The agent may prepare scripts, documentation, and predefined workflows; runtime execution remains owner-triggered unless separately approved.
