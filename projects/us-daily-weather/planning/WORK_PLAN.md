# U.S. Daily Weather — Work Plan

**Status:** Approved
**Approved:** 2026-10-02

## Purpose
Move from completed NOAA retrieval into a reproducible machine-learning pipeline and interactive current-temperature guessing application.

## Locked modeling decisions
- **Prediction target:** Guess the current temperature without using the actual current temperature as a model input. The application retrieves the actual current temperature separately after the prediction for comparison.
- **Location strategy:** User-facing map/location input maps latitude/longitude to appropriate NOAA station data.
- **V1 features:** Previous-day TMAX/TMIN, recent temperature average/trend, recent precipitation, recent snow and snow depth, time of year, latitude, longitude, and elevation.
- **Primary metric:** Mean Absolute Error (MAE), reported as average degrees off.
- **Execution:** Owner-directed. The agent prepares scripts, documentation, and predefined workflows; the owner triggers runtime execution unless separately approved.

## Phase 1 — Data Profiling
**Goal:** Understand the structure, meaning, completeness, and quality of the retrieved NOAA data before modeling.

### Work
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
- Implement the persistence baseline using the prior relevant temperature as the guess.
- Evaluate it using the agreed time-based structure.
- Calculate MAE.
- Preserve the baseline results as the benchmark for later comparison.

## Phase 5 — ML Model Training
**Goal:** Train a small set of appropriate candidate ML models and let validation performance determine which candidate moves forward.

### Work
- Select a small set of sensible candidate algorithms after profiling and dataset construction.
- Train candidates on 2016–2022.
- Compare candidates on 2023–2024 using MAE.
- Select the candidate with the strongest supported validation performance.
- Keep 2025 untouched throughout model selection.

## Phase 6 — Model Evaluation
**Goal:** Produce the final evidence-based assessment on unseen data.

### Work
- Unlock 2025 only after model selection is complete.
- Evaluate the selected ML model on 2025.
- Evaluate the persistence baseline on the same eligible 2025 observations.
- Compare MAE on the same evaluation population.
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
**Goal:** Turn the model into the interactive current-temperature guessing experience.

### Intended experience
- **Left:** Model's current-temperature guess.
- **Center:** Interactive U.S. map/location selection.
- **Right:** Actual current temperature from a separate live weather source.
- Display the prediction error clearly, for example: **Model was 3°F off.**

### Prediction flow
1. User selects a location.
2. Resolve the location to the appropriate station/history needed for the model.
3. Build the required features without using the actual current temperature.
4. Load the saved model and generate the guess.
5. Retrieve the actual current temperature separately.
6. Compare the prediction with the actual reading and display the error.

### Integrity rule
The actual current temperature used for comparison must not be provided to the model as an input.

## Completion
When all phases are complete, update project validation, lessons learned, status, and audit documentation with the final evidence and reproducibility chain.
