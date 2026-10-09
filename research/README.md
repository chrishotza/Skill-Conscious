# Research operating system

This directory connects sources and claims to testable hypotheses, experiments, results, inferences, and papers.

## Current state

S01 has recorded confirmatory coded and semantic outcomes plus 23 robustness conditions. The reported outcomes do not support the preregistered cross-family-recurrence prediction in its tested direction. Its original raw-output archive remains incomplete, so the study is not promoted to a paper. See research/S01_RESULTS_STATUS_2026-10-09.md and research/CURRENT_CHECKPOINT.md.

P008 is the next individual-scale mechanism target. Its evidence map, prediction registry, executable assay, and blocked-execution log exist; no empirical P008 result has been produced.

## Canonical navigation

1. AGENTS.md — contributor/agent operating rules.
2. RESEARCH_MAP.md — full repository map.
3. research/CURRENT_CHECKPOINT.md — authoritative live research state.
4. REPO_MEMORY.md — durable state and anti-drift rules.
5. docs/RESEARCH_METHOD_NORTH.md — methodological standard.
6. research/CLAIM_FAMILY_REGISTRY.md and research/CLAIM_FAMILY_TRIAGE.md — claim families and research triage.
7. research/S01_PREREGISTRATION_V1.md, research/S01_DATA_MANIFEST_V1.json, and research/S01_RESULTS_STATUS_2026-10-09.md — S01 protocol, frozen data description, and reported outcome/archive status.
8. research/P008_EVIDENCE_MAP_V1.md, research/p008_prediction_registry.json, and research/P008_EXECUTION_LOG.md — P008 target, controls, prediction, and execution status.
9. papers/README.md and docs/CLAIM_TO_PAPER_PROTOCOL.md — publication map and promotion gate.
10. Relevant files under experiments/, src/, tests/, and corpus-v1 only after identifying the specific question.

## Evidence-status vocabulary

Use one or more explicit labels:

- SOURCE CLAIM
- PROJECT HYPOTHESIS
- OPERATIONAL DEFINITION
- EMPIRICAL PREDICTION
- PROTOCOL
- EMPIRICAL RESULT
- INFERENCE
- OPEN QUESTION

A file, protocol, successful unit test, or architecture diagram is not an empirical result. Record negative/null outcomes and contradictory evidence.

## Corpus and limits

S01 analyzes 4,315 effective claims grouped into 325 corpus units, with 328 effective source IDs and 19 source families. Ledger coverage is not equivalent to passage-level verification, and source IDs are not interchangeable with corpus units.

The frozen preregistration is on s01-preregistered-v1 at commit 4fdea2f26ef2449e32ab74b67c2c19904bb3270c. Do not alter its hypothesis or analysis definitions retrospectively.

## State synchronization

Any substantive change in research/, papers/, experiments/, docs/, sources/, or README.md must update research/CURRENT_CHECKPOINT.md, REPO_MEMORY.md, and RESEARCH_MAP.md in the same change set. Update study/paper registries when their status changes.

## Scientific standard

- Define constructs operationally.
- Freeze predictions before confirmatory testing.
- Include matched controls and explicit null models.
- Preserve exact commit, dataset hashes, model revision, seed, parameters, runtime, timestamps, and raw outputs.
- Persist artifacts before declaring a run complete.
- State the strongest inference the data support—no stronger.
- Functional continuity or causal self-reference is not, by itself, evidence of phenomenal consciousness.
