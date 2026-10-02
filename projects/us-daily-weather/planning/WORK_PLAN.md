# U.S. Daily Weather — Work Plan

**Status:** Approved
**Approved:** 2026-10-02

## Purpose
Move from completed NOAA retrieval into a reproducible machine-learning pipeline and interactive daily high/low temperature prediction application.

## Locked modeling decisions
- **Prediction targets:** Predict both the daily maximum temperature (TMAX) and daily minimum temperature (TMIN) using the existing GHCN-Daily dataset. V1 does not require a separate hourly historical target source.
- **Location strategy:** User-facing map/location input maps latitude/longitude to appropriate NOAA station data.
- **V1 features:** Previous-day TMAX/TMIN, recent temperature average/trend, recent precipitation, recent snow and snow depth, time of year, latitude, longitude, and elevation.
- **Primary metric:** Mean Absolute Error (MAE), reported separately for TMAX and TMIN as average degrees off.
- **Execution:** Owner-directed. The agent prepares scripts, documentation, and predefined workflows; the owner triggers runtime execution unless separately approved.

## Phase 1 — Data Profiling
**Goal:** Understand the structure, meaning, completeness, and quality of the retrieved NOAA data before modeling.

### Work
- Document dataset structure and fields.
- Create `documentation/DATA_DICTIONARY.md` as one master source-to-model crosswalk table covering all fields used in the combined dataset.
- For each field, trace the source dataset, source column/code, source definition, source unit, standardized/final column name, standardized unit, transformation/conversion, modeling use, and notes.
- Include observation fields and station-metadata fields in the same master crosswalk rather than separate source-specific dictionaries.
- Document date fields and their meaning within the crosswalk.
- Document NOAA abbreviations, codes, flags, and units within the same crosswalk/notes where applicable.
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
A written profiling report documenting findings, limitations, and data-quality rules required before modeling.

## Phase 2 — Modeling Dataset & Feature Engineering
**Goal:** Use Phase 1 findings to construct the modeling dataset and implement the V1 features without target leakage.

### Work
- Define the exact calculation for each V1 feature.
- Join observations to required station metadata.
- Construct recent-history features using only information available before the target.
- Apply documented quality rules from Phase 1.
- Preserve chronological order.
- Produce a reproducible modeling dataset for baseline and ML training.

## Phase 3 — Time-Based Train / Validation / Test Setup
**Goal:** Create an honest chronological evaluation structure that prevents future data from leaking into earlier model development.

### Split
- **Training:** 2016–2022
- **Validation:** 2023–2024
- **Final test:** 2025

### Rule
Do not use 2025 to select features, choose algorithms, tune models, or otherwise make development decisions. Keep it untouched until final evaluation.

## Phase 4 — Baseline Model
**Goal:** Establish a simple benchmark that the ML model must improve upon.

### Work
- Implement persistence baselines using prior-day TMAX as the TMAX guess and prior-day TMIN as the TMIN guess.
- Evaluate it using the agreed time-based structure.
- Calculate TMAX MAE and TMIN MAE separately.
- Preserve the baseline results as the benchmark for later comparison.

## Phase 5 — ML Model Training
**Goal:** Train a small set of appropriate candidate ML models and let validation performance determine which candidate moves forward.

### Work
- Select a small set of sensible candidate algorithms after profiling and dataset construction.
- Train candidates on 2016–2022.
- Compare candidates on 2023–2024 using TMAX MAE and TMIN MAE.
- Select the candidate with the strongest supported validation performance.
- Keep 2025 untouched throughout model selection.

## Phase 6 — Model Evaluation
**Goal:** Produce the final evidence-based assessment on unseen data.

### Work
- Unlock 2025 only after model selection is complete.
- Evaluate the selected ML model on 2025.
- Evaluate the persistence baseline on the same eligible 2025 observations.
- Compare TMAX MAE and TMIN MAE on the same evaluation population.
- Examine useful error patterns such as season and geography where supported by the data.
- Document where the model performs well or poorly and record limitations.
- Do not claim model improvement unless the results support it.

## Phase 7 — Save & Package the Final Model
**Goal:** Preserve the selected trained model and everything needed to reproduce its predictions.

### Preserve
- Trained model artifact.
- Feature definitions and feature-building logic.
- Preprocessing logic.
- Model configuration/settings.
- Required dependencies.
- Final evaluation results.
- Data/model provenance and reproducibility records.
- Artifact checksum where practical.

The application should load the saved model rather than retrain on the full historical dataset for every prediction.

## Phase 8 — Interactive Weather App
**Goal:** Turn the model into an interactive daily high/low temperature prediction experience.

### Intended experience
- **Left:** Model's predicted daily high (TMAX) and low (TMIN).
- **Center:** Interactive U.S. map/location selection.
- **Right:** Actual observed daily high and low when available for comparison.
- Display prediction errors separately for the high and low.

### Prediction flow
1. User selects a location.
2. Resolve the location to the appropriate station/history needed for the model.
3. Build the required features without target leakage.
4. Load the saved model and generate TMAX and TMIN predictions.
5. Retrieve or use the actual observed TMAX and TMIN when available for comparison.
6. Compare predicted versus actual high and low and display both errors.

### Integrity rule
Actual target-day TMAX and TMIN must not be provided to the model as inputs. Features must use only information available before the target values.

## Completion
When all phases are complete, update project validation, lessons learned, status, and audit documentation with the final evidence and reproducibility chain.
