# U.S. Daily Weather — Work Plan

**Status:** Approved  
**Approved:** 2026-10-02  
**Task structure adopted:** 2026-10-03

## Purpose
Move from completed NOAA retrieval into a reproducible machine-learning pipeline and interactive daily high/low temperature prediction application.

## Locked modeling decisions
- **Prediction targets:** Predict both daily maximum temperature (TMAX) and daily minimum temperature (TMIN) using the existing GHCN-Daily dataset. V1 does not require a separate hourly historical target source.
- **Location strategy:** User-facing map/location input maps latitude/longitude to appropriate NOAA station data.
- **V1 features:** Previous-day TMAX/TMIN, recent temperature average/trend, recent precipitation, recent snow and snow depth, time of year, latitude, longitude, and elevation.
- **Primary metric:** Mean Absolute Error (MAE), reported separately for TMAX and TMIN as average degrees off.
- **Execution:** Owner-directed. Agents prepare scripts, documentation, and predefined workflows; the owner triggers runtime execution unless separately approved.

## Task convention
Task IDs use `P#T#`: phase number followed by task number. The Project Manager assigns work by task ID. Builder implements against the listed acceptance criteria. Reviewer independently validates the same criteria before the Project Manager marks the task complete.

## Phase 1 — Data Profiling
**Goal:** Understand the structure, meaning, completeness, and quality of the retrieved NOAA data before modeling.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P1T1 | Data Dictionary & Source Crosswalk | Document observation and station fields, source definitions/codes, units, standardized names, transformations, modeling relevance, dates, NOAA abbreviations and flags. | One master source-to-model crosswalk exists and covers the combined dataset fields needed for the project. | `documentation/DATA_DICTIONARY.md` | Complete |
| P1T2 | Dataset Structure Profile | Quantify the historical dataset structure. | Reports total rows, deduplicated stations, overall date range, yearly counts, and counts by core element; results are reproducible. | Profiling results | Not Started |
| P1T3 | Geographic Coverage | Measure station and observation coverage geographically. | Reports coverage by state/location at a useful level and identifies material geographic gaps or limitations. | Profiling results | Not Started |
| P1T4 | Missingness & Observation Coverage | Measure nulls, missing observations, and TMAX/TMIN availability. | Quantifies field missingness and target availability; distinguishes expected source behavior from material modeling gaps. | Profiling results | Not Started |
| P1T5 | Duplicate Analysis | Check duplicate observation keys, especially station/date/element. | Duplicate counts are reproducible; any duplicates are characterized and their modeling impact documented. | Profiling results | Not Started |
| P1T6 | NOAA Flag Profile | Profile measurement, quality, and source flags. | MFLAG, QFLAG, and SFLAG values/frequencies are documented and implications for later quality rules are identified without unsupported exclusions. | Quality findings | Not Started |
| P1T7 | Value & Range Checks | Review values, distributions, units, sentinels, and unusual observations for core weather elements and relevant metadata. | Element ranges and notable anomalies/sentinels are documented, including elevation sentinel behavior; suspicious values are not silently changed. | Quality findings | Not Started |
| P1T8 | Station Modeling Eligibility | Assess whether stations have sufficient TMAX/TMIN history and continuity for intended modeling. | Reproducible station-level eligibility evidence is produced and limitations are documented; final eligibility rules are supported by profiling evidence. | Station eligibility results | Not Started |
| P1T9 | Phase 1 Profiling Report & Quality Rules | Consolidate Phase 1 evidence into modeling-relevant findings. | Findings, limitations, expected source behavior, actual quality problems, and required pre-modeling quality rules are documented and traceable to profiling evidence. | Written profiling report | Not Started |

## Phase 2 — Modeling Dataset & Feature Engineering
**Goal:** Use Phase 1 findings to construct the modeling dataset and implement V1 features without target leakage.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P2T1 | Define Feature Specifications | Define exact calculation, timing, source fields, units, and missing-data handling for each V1 feature. | Every V1 feature has a reproducible definition using only information available before the target. | Feature specification | Not Started |
| P2T2 | Join Observations & Station Metadata | Build the modeling grain and attach required location/elevation metadata. | Join logic is reproducible, row grain is documented, and unintended row multiplication is checked. | Modeling join logic | Not Started |
| P2T3 | Build Historical Features | Construct prior-day and recent-history temperature, precipitation, snow/snow-depth, seasonal, and location features. | Features match P2T1 definitions, preserve chronology, and pass leakage checks. | Feature-building pipeline | Not Started |
| P2T4 | Apply Phase 1 Quality Rules | Apply approved exclusions/standardizations from profiling. | Every applied rule traces to Phase 1 evidence; no undocumented cleaning is introduced. | Quality-controlled modeling data | Not Started |
| P2T5 | Produce Reproducible Modeling Dataset | Assemble final feature/target dataset for baseline and ML work. | Dataset is reproducible, chronologically ordered, schema documented, and suitable for the approved split. | Modeling dataset | Not Started |

## Phase 3 — Time-Based Train / Validation / Test Setup
**Goal:** Create an honest chronological evaluation structure that prevents future data from leaking into earlier model development.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P3T1 | Implement Chronological Split | Assign training 2016–2022, validation 2023–2024, and final test 2025. | Every eligible row belongs to the correct time partition with no overlap. | Split logic and counts | Not Started |
| P3T2 | Validate Leakage Boundary | Verify 2025 remains unavailable to feature/model selection and tuning. | Checks confirm development uses only training/validation data and target construction does not cross forbidden time boundaries. | Split validation evidence | Not Started |

**Locked rule:** Do not use 2025 to select features, choose algorithms, tune models, or otherwise make development decisions. Keep it untouched until final evaluation.

## Phase 4 — Baseline Model
**Goal:** Establish a simple benchmark that the ML model must improve upon.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P4T1 | Implement Persistence Baseline | Prior-day TMAX predicts TMAX and prior-day TMIN predicts TMIN. | Baseline uses only prior information and runs on the eligible evaluation population. | Baseline implementation | Not Started |
| P4T2 | Evaluate Baseline | Calculate and preserve separate TMAX and TMIN MAE. | MAE calculations are reproducible and evaluation population/counts are documented. | Baseline results | Not Started |

## Phase 5 — ML Model Training
**Goal:** Train a small set of appropriate candidate models and let validation performance determine which candidate moves forward.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P5T1 | Select Candidate Algorithms | Choose a small sensible candidate set based on profiling and modeling-data characteristics. | Choices and rationale are documented without using 2025 results. | Candidate model plan | Not Started |
| P5T2 | Train Candidates | Train candidates on 2016–2022 using the approved feature pipeline. | Training is reproducible and 2025 remains untouched. | Trained candidates | Not Started |
| P5T3 | Validate & Select Model | Compare candidates on 2023–2024 using separate TMAX/TMIN MAE and select the supported candidate. | Selection is traceable to validation evidence and documented before 2025 is unlocked. | Selected model decision | Not Started |

## Phase 6 — Final Model Evaluation
**Goal:** Produce the final evidence-based assessment on unseen data.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P6T1 | Unlock & Evaluate 2025 | Evaluate the already-selected ML model and persistence baseline on the same eligible 2025 observations. | Separate TMAX/TMIN MAE and evaluation counts are reported on the same population; no post-test model selection occurs. | Final test results | Not Started |
| P6T2 | Analyze Error Patterns | Examine supported error patterns such as season and geography. | Analysis uses 2025 only for final evaluation/interpretation and documents limitations without unsupported claims. | Error analysis | Not Started |
| P6T3 | Final Model Assessment | Document model vs baseline evidence and limitations. | Improvement is claimed only where supported by final evidence; results are reproducible and traceable. | Final evaluation report | Not Started |

## Phase 7 — Save & Package the Final Model
**Goal:** Preserve the selected trained model and everything needed to reproduce its predictions.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P7T1 | Save Model Artifact | Serialize the selected trained model for application use. | Artifact loads successfully without retraining and has a checksum where practical. | Trained model artifact | Not Started |
| P7T2 | Package Prediction Pipeline | Preserve feature-building, preprocessing, configuration, and dependencies. | A reproducible prediction path uses the saved model and approved feature definitions. | Prediction package | Not Started |
| P7T3 | Preserve Model Provenance | Record training/evaluation provenance, settings, results, and reproducibility information. | Another person can identify what model was built, from what process/data periods, and how it was evaluated. | Model provenance records | Not Started |

## Phase 8 — Interactive Weather App
**Goal:** Turn the model into an interactive daily high/low temperature prediction experience.

| Task ID | Task | Details | Acceptance Criteria | Deliverable | Status |
| --- | --- | --- | --- | --- | --- |
| P8T1 | Location-to-Station Resolution | Map user-selected U.S. locations/coordinates to appropriate NOAA station history. | Resolution logic is documented, reproducible, and handles unsupported locations clearly. | Location resolution component | Not Started |
| P8T2 | Prediction Service | Build target-day features and load the saved model to generate TMAX/TMIN predictions. | Service does not retrain per request and never uses target-day TMAX/TMIN as model inputs. | Prediction component | Not Started |
| P8T3 | Observed Weather Comparison | Retrieve/use actual observed TMAX/TMIN when available and calculate separate errors. | Predicted and observed values are clearly distinguished; unavailable actuals are handled honestly. | Comparison component | Not Started |
| P8T4 | Interactive Interface | Present predicted high/low on the left, map/location selection in the center, and observed high/low on the right. | Core flow works end-to-end and displays separate high/low prediction errors with clear missing-data behavior. | Interactive application | Not Started |
| P8T5 | Final Project Closeout | Update validation, lessons learned, status, and audit records. | Final evidence and reproducibility chain are documented and project status reflects completion. | Completed project records | Not Started |

## Integrity rule
Actual target-day TMAX and TMIN must not be provided to the model as inputs. Features must use only information available before the target values.
