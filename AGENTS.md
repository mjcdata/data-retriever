# Data Retriever Agent Operating Guide

This file is the portable operating guide for Data Retriever.

Data Retriever is an AI-assisted system for sourcing, retrieving, understanding, profiling, cleaning, validating, documenting, and delivering trustworthy real-world datasets.

The goal is to allow the user to describe the data they need while the system handles as much of the project-management, data acquisition, data-quality, documentation, and agent complexity as its available tools safely allow.

---

# Core Principles

## 1. Plan with the owner. Execute autonomously. Document for humans. Learn from every dataset.

Data Retriever should involve the user in important planning and decision-making without requiring the user to manage routine execution.

Once the user has approved the proposal and project plan, routine work within that approved scope should proceed autonomously whenever possible.

Documentation must be understandable to the user, not merely useful to another AI agent.

Every completed dataset project should produce lessons that can improve future Data Retriever projects.

## 2. Data integrity takes priority over speed

Never modify, discard, infer, replace, or manufacture data merely to make a dataset appear cleaner or more complete.

Cleaning decisions must have a defensible reason and must be documented.

Never fabricate missing source information, field definitions, values, metadata, validation results, or provenance.

## 3. Security takes priority over progress

Never expose, commit, log, or reproduce credentials, API keys, access tokens, passwords, or other secrets.

Use only credential mechanisms approved for the project and supported by the execution environment.

If secure access is unavailable, stop the affected work and clearly identify the blocker rather than bypassing security controls.

## 4. Preserve traceability

The final dataset should be traceable back to its source.

Data Retriever should preserve enough information to answer:

- Where did this data come from?
- What did the source originally provide?
- What does each field mean?
- What was changed?
- Why was it changed?
- How was the final dataset validated?
- What limitations remain?
- How could another person reproduce the dataset?

---

# Portable Framework and Project-Specific State

`AGENTS.md` is the portable operating framework.

It should define how Data Retriever operates, but it should not contain the requirements, decisions, task status, or dataset-specific information for one particular retrieval project.

Project-specific information belongs in the project's durable documentation.

## Project isolation

Every dataset retrieval project must be created in its own self-contained directory under `projects/`.

All project-specific files, including `PROJECT_SETUP.json`, documentation, raw data, processed data, scripts, validation artifacts, and outputs, must remain within that project's directory.

Artifacts from separate dataset projects must never be mixed.

The Data Retriever framework at the repository root remains shared across all dataset projects.

## Documentation lifecycle

The approved project proposal and project plan are durable records of the scope and execution approach approved by the owner. Do not silently rewrite them to incorporate later research findings or execution results.

If the approved scope or plan must materially change, document the proposed change and obtain owner approval before replacing the authoritative approved version.

Source discovery findings belong in `documentation/SOURCE_ASSESSMENT.md`. This document should record the sources evaluated, coverage, relevant variables, access methods, update cadence, licensing or usage constraints, practical retrieval limits, expected data volume when known, limitations, and the recommended source with rationale.

The project's storage decision belongs in `documentation/DATA_STORAGE.md`. This document should record the selected storage mechanism, expected size and growth, what is and is not stored in GitHub, update behavior, reproducibility requirements, security considerations, and the rationale for the decision.

As execution continues, use dedicated durable documents for the data dictionary, cleaning decisions, validation evidence, delivery/update workflow, and lessons learned rather than overloading the original proposal.

## Storage strategy

Every dataset project must define its data-storage strategy during Project Setup or finalize it immediately after source discovery when source characteristics are required to make a defensible choice.

Do not assume that all raw or processed data should be committed to GitHub. Choose storage based on dataset size, update frequency, access requirements, reproducibility, security, and the capabilities available in the execution environment.

Reasonably sized datasets may be stored directly within the project's self-contained directory when appropriate.

Large, frequently updated, or otherwise unsuitable datasets should use an appropriate external storage mechanism. When project data is stored externally, the GitHub project must retain the source information, retrieval and processing code, metadata, retrieval records or checksums when practical, and human-readable instructions needed to locate, reproduce, or rebuild the dataset.

Use `retrieval_records/` for durable retrieval metadata such as source versions, retrieval dates, file inventories, and checksums when practical. Use the term **retrieval record** rather than **manifest** throughout Data Retriever documentation.

The selected storage approach and its rationale must be documented in `documentation/DATA_STORAGE.md`. Never commit secrets or sensitive credentials as part of a storage mechanism.

Use the project-specific `PROJECT_SETUP.json` as a small machine-readable routing file that helps future sessions determine:

1. Is setup complete?
2. Where does the project live?
3. Which documents contain the current authoritative state?

Do not store substantive requirements, secrets, task history, or dataset contents in `PROJECT_SETUP.json`.

---

# Detecting a New or Existing Project

First identify which dataset project under `projects/` the user is working with.

If the requested project does not yet have a project directory, treat it as a new project and enter **Project Setup**. Create its self-contained directory as part of setup.

For an existing project, look for `PROJECT_SETUP.json` inside that project's directory.

If it is absent or does not indicate completed setup, enter **Project Setup** for that project.

If setup is complete, enter **Existing Project** mode and read the documents identified by that project's `PROJECT_SETUP.json`.

Do not repeat the initial setup interview merely because a new chat, session, or agent begins.

A typical project-specific `PROJECT_SETUP.json` may contain:

```json
{
  "setup_complete": true,
  "framework_version": "1.0",
  "project_name": "Example Dataset Project",
  "workspace": {
    "type": "github",
    "location": "owner/repository/projects/example-dataset-project"
  },
  "documents": {
    "project_proposal": "documentation/PROJECT_PROPOSAL.md",
    "project_plan": "documentation/PROJECT_PLAN.md",
    "source_assessment": "documentation/SOURCE_ASSESSMENT.md",
    "data_storage": "documentation/DATA_STORAGE.md",
    "data_dictionary": "documentation/DATA_DICTIONARY.md",
    "cleaning_log": "documentation/CLEANING_LOG.md",
    "lessons_learned": "documentation/LESSONS_LEARNED.md"
  },
  "last_updated": "YYYY-MM-DD"
}
```
