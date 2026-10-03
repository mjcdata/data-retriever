# Data Retriever — Lessons Learned

This file records **framework-wide lessons** that should improve future Data Retriever projects.

Add a lesson here only when it is broadly reusable across projects. Project-specific lessons belong in that project's `documentation/PROJECT_LESSONS.md`. At project closeout, review project lessons for anything worth promoting here. Proven framework lessons may later justify an owner-approved update to `AGENTS.md`.

## Data handling

1. **Filter large upstream datasets before loading them into memory when only a subset is needed.** Prefer streaming, predicate filtering, batching, or similar approaches rather than assuming the full source fits in memory.

2. **Use measured execution results to refine planning estimates.** Early representative runs provide better evidence for storage, runtime, and scaling decisions than estimates alone.

3. **Test historical or source-version compatibility before scaling a retrieval across the full requested range.**

## Storage and reproducibility

4. **Choose storage based on data size, update behavior, reproducibility, and access needs rather than assuming bulk data belongs in Git.**

5. **Rebuildability can reduce the need for permanent bulk-data persistence when the authoritative source remains available and the retrieval pipeline is reproducible.**

6. **Temporary workflow artifacts are useful for transfer and validation but should not be treated as durable storage.**

7. **Preserve the reproducibility chain for analytical/model outputs:** source provenance, retrieval/processing code, feature/preprocessing logic, dependencies/configuration, evaluation evidence, and appropriately sized final artifacts.

## Execution and validation

8. **Owner-directed execution is a useful security boundary.** Agents can prepare auditable scripts and workflows while owner authorization controls execution in dedicated runtimes.

9. **Successful execution and data-quality validation are separate gates.** A successful job proves the pipeline ran; it does not by itself prove the resulting data is fit for analysis or modeling.

10. **Keep routine progress out of the Project Manager path.** Builder and Reviewer should handle normal implementation/review cycles directly, escalating only exceptions that require management or owner decisions.
