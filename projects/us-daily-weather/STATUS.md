# U.S. Daily Weather — Status

**Status date:** 2026-10-02  
**Current phase:** Work plan approved → Phase 1 Data Profiling next  
**Overall status:** Ready to begin model-preparation execution

## Completed

- Defined NOAA GHCN-Daily as the authoritative source.
- Limited the project to U.S. observations and core elements: PRCP, SNOW, SNWD, TMAX, and TMIN.
- Built and validated the streaming retrieval/processing pipeline.
- Completed the 2025 proof of concept.
- Completed the 2016 older-year compatibility test.
- Completed the full owner-triggered 2016–2025 historical GitHub Actions build.
- Verified GitHub Actions Run `37060323541` completed successfully.
- Verified ten yearly artifacts were produced, one for each year from 2016 through 2025.
- Closed out retrieval validation, storage strategy, lessons learned, and audit documentation.

## Data strategy

NOAA remains the source of truth.

The multi-gigabyte processed historical dataset does not need to be permanently stored when continuous availability is unnecessary. Data Retriever preserves the code and provenance needed to rebuild it.

Intended lifecycle:

**NOAA → retrieval → temporary processed data → validation/feature engineering → model training/testing → preserved model artifact + reproducibility records**

## Execution and security

Runtime execution remains owner-directed.

The agent may prepare scripts and predefined GitHub Actions workflows, but the owner explicitly triggers execution unless a different execution mode is separately approved.

## Validation boundary

The historical workflow successfully processed all ten requested years and created all ten artifacts. This is execution-level validation.

Target-specific row-level checks, feature-quality validation, train/validation/test design, and model evaluation belong to the model-preparation phase.

## Modeling plan completed

1. **Prediction targets:** V1 predicts both daily maximum temperature (TMAX) and daily minimum temperature (TMIN) using the existing GHCN-Daily dataset.
2. **Location strategy:** User-facing map/location input maps latitude/longitude to appropriate NOAA station data.
3. **V1 features:** Previous-day TMAX/TMIN, recent temperature average/trend, recent precipitation, recent snow/snow depth, time of year, latitude, longitude, and elevation.
4. **Time-based evaluation:** Use 2016–2024 for development and reserve all of 2025 as unseen final-test data.
5. **Baseline:** Persistence — prior-day TMAX predicts target-day TMAX and prior-day TMIN predicts target-day TMIN.
6. **Primary metric:** Mean Absolute Error (MAE), reported separately for TMAX and TMIN as average degrees off.
7. **Model use:** Save the selected trained model as a reusable artifact; build the interactive map/weather interface after training and evaluation.

## Work plan

`planning/WORK_PLAN.md` is the approved eight-phase execution roadmap.

1. Data Profiling.
2. Modeling Dataset & Feature Engineering.
3. Time-Based Train / Validation / Test Setup: train 2016–2022, validate 2023–2024, final test 2025.
4. Persistence Baseline Model.
5. ML Model Training with a small set of candidates selected by validation performance.
6. Final Model Evaluation on untouched 2025 data against the baseline using MAE.
7. Save & Package the Final Model and reproducibility records.
8. Interactive Weather App with predicted daily high/low, U.S. map/location selection, observed high/low comparison, and separate prediction errors.

**Next execution phase:** Phase 1 — Data Profiling.

## Key project records

- `planning/WORK_PLAN.md`
- `planning/DATA_STORAGE.md`
- `planning/RETRIEVAL_ARCHITECTURE.md`
- `audit/VALIDATION.md`
- `documentation/LESSONS_LEARNED.md`
- `audit/AGENT_AUDIT_LOG.md`
- `scripts/retrieve_ghcnd.py`
- `.github/workflows/us-daily-weather.yml`
