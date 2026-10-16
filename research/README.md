# Research operating system

This directory connects sources and claims to testable hypotheses, experiments, results, inferences, and papers.

## Current state

S01 has recorded confirmatory coded and semantic outcomes plus 23 robustness conditions. The reported outcomes do not support the preregistered cross-family-recurrence prediction in its tested direction. Its original raw-output archive remains incomplete, so the study is not promoted to a paper. See research/S01_RESULTS_STATUS_2026-10-09.md and research/CURRENT_CHECKPOINT.md.

P008/CF01 has a validated deterministic, hand-built mechanism fixture (128/128 CI tests on 2026-10-16; merged PR #90). Its result does not establish broad empirical generalization or phenomenal consciousness. A separate, unexecuted draft for generalized synthetic candidate sets is in research/P008_CF01_GENERALIZATION_PROTOCOL_V1.md and research/p008_generalization_protocol_v1.json.

## Canonical navigation

1. AGENTS.md — contributor/agent operating rules.
2. RESEARCH_MAP.md — full repository map.
3. research/CURRENT_CHECKPOINT.md — authoritative live research state.
4. REPO_MEMORY.md — durable state and anti-drift rules.
5. docs/RESEARCH_METHOD_NORTH.md — methodological standard.
6. research/CLAIM_FAMILY_REGISTRY.md and research/CLAIM_FAMILY_TRIAGE.md — claim families and research triage.
7. research/S01_PREREGISTRATION_V1.md, research/S01_DATA_MANIFEST_V1.json, and research/S01_RESULTS_STATUS_2026-10-09.md — S01 protocol, frozen data description, and reported outcome/archive status.
8. research/P008_EVIDENCE_MAP_V1.md, research/p008_prediction_registry.json, research/P008_EXECUTION_LOG.md, and research/P008_CF01_GENERALIZATION_PROTOCOL_V1.md — P008 completed fixture, controls, provenance and *draft* next assay.
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

## Development pilot implementation

The current generalized P008 runner `experiments/p008_generalization_pilot.py` is **pilot-only**. It accepts scenario IDs 0..31, enforces matched controls and restart, writes hashed per-arm raw artifacts, and refuses holdout IDs 1000..1127. See the workflow `.github/workflows/p008-generalization-pilot.yml`. CI and pilot results must be inspected before any empirical result is claimed. The generalization protocol remains an unfrozen draft.

## Audited P008 development pilot (2026-10-16)

The 32-scenario pilot CI run 38978718548 completed; 8 focused tests and 136 full tests passed, raw output was SHA-256 audited and uploaded as artifact 12079189698. C-vs-B/C-vs-D divergence: 0.125, controls 0. This is **exploratory synthetic functional evidence only**, not a frozen confirmatory generalization or consciousness result. Raw archive expires 2027-01-14. See research/results/p008/P008_GENERALIZATION_PILOT_2026-10-16.md.

## P008 internally sealed release

The frozen synthetic evaluation baseline is PR #94 merge `c0278493e8ef31520beea29355f947a7ea3739a8`. A separately proposed `research/p008_holdout_release.json` authorizes the guarded workflow on main; it is **not evidence that the 128 reserved cases ran**. The archived run and analysis must be verified before presenting a holdout result. Independent external methodological review remains pending.

## Verified P008 internal holdout (2026-10-16)

Internally frozen code `c0278493` and separate release `c9728d25` executed a complete 128-scenario synthetic reserved-split in Actions run 38980796822, with 140 passing pre-run tests and SHA-256 re-audit. C-vs-B/C-vs-D divergence 0.234375 (scenario bootstrap 95% 0.164062–0.3125); B-vs-D and A-vs-B 0. The software mechanism gate passed. The original frozen protocol is intentionally unchanged after execution; new outcome record is `research/p008_holdout_result_v1.json` and `research/results/p008/P008_CF01_INTERNAL_HOLDOUT_2026-10-16.md`. Evidence artifact 12081087004 expires January 2027 unless durable archive step succeeds. **Not independent confirmation or consciousness evidence.**

## Long-lived P008 raw archive verified

Original 128-scenario holdout ZIP preserved unchanged in GitHub Release `p008-cf01-internal-holdout-20261016` on 2026-10-16 (archive workflow run 38981166451), release ID 415457666, asset 648924054, SHA-256 `8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32`, 633705 bytes. It matches original Actions artifact 12081087004; see `research/p008_holdout_result_v1.json`. This archives software evidence, not independent validation of a consciousness hypothesis.
