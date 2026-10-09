# Current Research Checkpoint

**Updated:** 2026-10-09  
**Canonical repository:** chrishotza/Skill-Conscious  
**Canonical branch:** main (this cleanup is being prepared on a review branch)

## Current state

The repository has a substantial experimental runtime and a structured research program. No paper is currently publication-ready. The immediate engineering task is documentation/state consolidation; the immediate scientific task after consolidation is to recover or formally account for S01 artifacts, then audit P008 before any new run.

## Corpus snapshot

- 4,315 effective claim records; 4,315 unique global claim IDs.
- 325 analytic corpus units.
- 328 effective source IDs.
- 19 source families in S01.
- The ledger is structurally covered; passage-level verification, edition/translation control, and independence/dependency review remain separate tasks.
- Frozen data manifest: research/S01_DATA_MANIFEST_V1.json; corpus branch: corpus-v1.

## S01 — current result state

**Status: primary and robustness outcomes recorded; original raw-output archival incomplete.**

Primary run S01_CONFIRMATORY_T4_V1 was recorded at 2026-10-09 02:59:42 UTC from preregistered commit 4fdea2f26ef2449e32ab74b67c2c19904bb3270c. Robustness run S01_ROBUSTNESS_T4_FAST_V1 was recorded at 04:23:54 UTC.

- Coded DeltaJ = -0.0870408416; mean cross-family Jaccard = 0.5222007632, mean within-family Jaccard = 0.6092416048; directional upper-tail p = 1.0.
- Semantic cross-family neighbor fraction = 0.7535341831 versus null mean 0.9400950452; upper-tail p = 1.0.
- Observed semantic cosine = 0.6607122186 versus null mean 0.6642799840; upper-tail p = 1.0.
- 23 robustness conditions were recorded; all had negative DeltaS and both reported upper-tail p-values equal to 1.0.
- The CPU/GPU reproducibility record reports absolute differences of 5.78e-10 for DeltaS and 5.28e-09 for observed cosine.

Interpretation: the tested analyses did not support the preregistered prediction of greater cross-family recurrence in the tested direction. This is not a universal disproof of recurrence or of a consciousness theory.

Canonical consolidated record: research/S01_RESULTS_STATUS_2026-10-09.md.

## S01 artifact integrity

The original primary and robustness run directories were not found in the disconnected Colab runtime, and repository searches did not locate the original output files in tracked GitHub paths. The Drive master backup at MyDrive/Skill-Conscious_PERSISTENT/S01_MASTER_BACKUP_20261009/ preserves the Git bundle, three branch archives, and a recovery snapshot. Its report verifies 11 inventoried files by SHA-256.

This is not a complete raw-run archive. In particular, do not describe the original JSON/NPZ run artifacts as recovered unless the actual files are found and their hashes/contents are inspected. Do not reconstruct originals from summary values.

## P008 — CF01 self-model causality

Hypothesis: intervention on a persistent self-model changes future trajectory selection under otherwise matched conditions.

- Evidence map: research/P008_EVIDENCE_MAP_V1.md and .json.
- Prediction contract: research/p008_prediction_registry.json.
- Target assay: experiments/p008_self_model_causal_runtime.py.
- Execution log: research/P008_EXECUTION_LOG.md.
- Recorded attempt on 2026-10-06 was blocked by inability to resolve github.com.
- **No empirical P008 result has been produced.** Syntax/static integrity checks are not experiment execution.

Before running P008, audit the conditions/controls and verify that results, stdout/stderr, seeds, runtime details, and hashes will be persisted to a tested durable location.

## P009 and P010

- P009 relational probes B2/B3 are implemented; broader multi-condition validation remains open.
- P010 has no specified physical model with an observable that discriminates it from plausible alternatives. B1 remains blocked; B4 follows only after candidate models exist.
- The three-scale bridge is a research framework, not an established hierarchy or empirical finding.

## Completed / recorded

- Research method north star and claim-family operating system.
- S01 protocol, manifest, frozen analysis snapshot, primary and robustness outcomes, and result-direction interpretation.
- Optimization of the secondary null implementation without changing the declared analysis definition.
- Drive master backup creation and SHA-256 verification for the 11 files in its manifest.
- P008 evidence map, prediction registry, runtime assay source, and blocked-execution log.

## Blockers

- S01 original run-output directories and complete raw artifacts remain unrecovered.
- P008 needs an audited execution environment and durable output persistence.
- P009 needs broader validation.
- P010 needs a concrete model-discrimination target.
- 52 non-canonical provenance labels in S069/S070/S071 still require source-level review.

## Immediate sequence

1. Merge the documentation/state consolidation only after CI and link/content checks pass.
2. Verify the actual contents of the Drive recovery snapshot and maintain an explicit raw-artifact inventory.
3. Audit P008's implementation, controls, deterministic seed behavior, and output contract without running an expensive experiment yet.
4. Execute only after the persistent-output path has been tested and the run configuration is frozen.
