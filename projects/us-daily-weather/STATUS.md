# U.S. Daily Weather — Status

**Status date:** 2026-10-04  
**Current phase:** Phase 1 — Data Profiling  
**Current task:** P1T3 — Geographic Coverage  
**Overall status:** In progress — P1T2 passed independent review; P1T3 is the next eligible approved task.  
**Next action:** Builder begins P1T3 under the approved Work Plan. If owner-controlled runtime execution is required, Builder prepares the predefined workflow and updates this status with the required Owner authorization before execution.

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
- Completed P1T1 — Data Dictionary & Source Crosswalk.
- Completed P1T2 — Dataset Structure Profile after independent Reviewer Pass from owner-triggered run `37112147880`.

## Data strategy

NOAA remains the source of truth.

The multi-gigabyte processed historical dataset does not need to be permanently stored when continuous availability is unnecessary. Data Retriever preserves the code and provenance needed to rebuild it.

Intended lifecycle:

**NOAA → retrieval → temporary processed data → validation/feature engineering → model training/testing → preserved model artifact + reproducibility records**

## Execution and security

Runtime execution remains owner-directed.

Agents may prepare scripts and predefined GitHub Actions workflows, but the owner explicitly authorizes runtime execution unless a different execution mode is separately approved.

If current work becomes blocked, this file's normal current status and next-action fields should state the blocker and required next action. No separate blocker section is required.

## Validation boundary

The historical workflow successfully processed all ten requested years and created all ten artifacts. This is execution-level validation.

P1T2 has also passed independent task-level review. Remaining profiling, target-specific row-level checks, feature-quality validation, train/validation/test design, and model evaluation continue under the approved Work Plan.

## Modeling plan

1. **Prediction targets:** V1 predicts both daily maximum temperature (TMAX) and daily minimum temperature (TMIN) using the existing GHCN-Daily dataset.
2. **Location strategy:** User-facing map/location input maps latitude/longitude to appropriate NOAA station data.
3. **V1 features:** Previous-day TMAX/TMIN, recent temperature average/trend, recent precipitation, recent snow/snow depth, time of year, latitude, longitude, and elevation.
4. **Time-based evaluation:** Train on 2016–2022, validate on 2023–2024, and reserve all of 2025 as unseen final-test data.
5. **Baseline:** Persistence — prior-day TMAX predicts target-day TMAX and prior-day TMIN predicts target-day TMIN.
6. **Primary metric:** Mean Absolute Error (MAE), reported separately for TMAX and TMIN as average degrees off.
7. **Model use:** Save the selected trained model as a reusable artifact; build the interactive map/weather interface after training and evaluation.

## Work plan

`planning/WORK_PLAN.md` is the approved eight-phase execution roadmap.

**Phase 1 progress:** P1T1 Complete; P1T2 Complete; P1T3 Geographic Coverage is next.

The remaining approved phases are Modeling Dataset & Feature Engineering, Time-Based Train/Validation/Test Setup, Persistence Baseline Model, ML Model Training, Final Model Evaluation, Save & Package the Final Model, and Interactive Weather App.

## Key project records

- `planning/PROJECT_PLAN.md`
- `planning/WORK_PLAN.md`
- `planning/DATA_STORAGE.md`
- `planning/RETRIEVAL_ARCHITECTURE.md`
- `audit/VALIDATION.md`
- `documentation/PROJECT_LESSONS.md`
- `audit/AGENT_AUDIT_LOG.md`
- `scripts/retrieve_ghcnd.py`
- `.github/workflows/us-daily-weather.yml`
