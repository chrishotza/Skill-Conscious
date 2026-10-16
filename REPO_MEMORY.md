# Skill-Conscious — AI Repository Memory

> Canonical entry point for an AI instance entering the repository. Read this file first.

## 0. How to use this memory

Do not ask the human to explain the project before inspecting the repository. Read in this order:

1. AGENTS.md
2. RESEARCH_MAP.md
3. research/CURRENT_CHECKPOINT.md
4. REPO_MEMORY.md (this file)
5. research/README.md
6. The active study registry and frozen protocol.
7. The relevant evidence map, implementation, and tests only as needed.

Do not read the entire repository blindly. The checkpoint is authoritative for live status; older handoff notes may be stale.

## 1. Project identity
Canonical repository: chrishotza/Skill-Conscious
Canonical branch: main
Skill-Conscious investigates whether consciousness-like organization can be operationalized as a persistent, self-referential dynamical architecture.
The project does not treat an LLM as the whole architecture.

Core principle:
> Language is an interface. Memory is a component. An LLM is a component. The architecture is the loop that binds them together.

## 2. Core architecture
WORLD → PERCEPTION → PRESENT WORKSPACE ↕ SELF ↔ SELF-MODEL ↕ MEMORY → INTENTION → ACTION → SELF CHANGE + WORLD CHANGE → NEXT CYCLE

Central causal relation:
SelfModel(t) → Trajectory(t) → Action(t) → State(t+1) → SelfModel(t+1)

Project principle:
> Do not perform consciousness. Implement continuity.

## 3. Foundational ontology
Primary project-authored ontology: sources/manifesto/MANIFIESTO_DEL_SER.md
The manifesto contains 12 axioms. Axiom 8 is the current major research target:
> La conciencia es experiencia del recorrido.
> La conciencia no es un objeto. Es un sistema recorriéndose a sí mismo.
> Aparece cuando existe dinámica interna compleja, memoria topológica y distinción entre estados posibles.
> Conciencia es habitar un atractor y saberlo.
These are project axioms/hypotheses. Do not silently present them as established external scientific facts.

## 4. Evidence model

Canonical evidence files:
- sources/BIBLIOGRAPHY.md
- sources/PRIMARY_SOURCES.md
- sources/EVIDENCE_MATRIX.md
- sources/HARVEST_ROADMAP.md
- sources/CONSCIOUSNESS_MAP.md
- sources/SOURCE_CARD_TEMPLATE.md

S01 uses 4,315 effective claim records grouped into 325 analytic corpus units, with 328 effective source IDs and 19 source families. Do not conflate claims, corpus units, and source IDs. The corpus ledger is structurally covered, but passage-level verification, edition/translation review, source independence, and dependency analysis remain incomplete.

Every evidence item must distinguish SOURCE CLAIM, PROJECT HYPOTHESIS, EMPIRICAL RESULT, INFERENCE, and OPEN QUESTION. Contradictory evidence is retained.

## 5. Scientific paper graph
Authoritative paper map: `papers/README.md`.

P001 → P002 → P003 → P004 → P005 → P006 is the original artificial-consciousness mechanism track.

The cross-scale program is:
P007 → P008 / P009 / P010 → P012 → P011.

P012 defines the explicit bridge architecture among Fundamental, Relational and Individual consciousness.

- P007 — Three-Scale Framework: Fundamental / Relational / Individual.
- P008 — Individual scale: causal self-reference and continuity.
- P009 — Relational scale: coupled-agent dynamics and reciprocal causality.
- P010 — Fundamental scale: testability and model discrimination.
- P011 — Cross-scale synthesis.

`docs/CLAIM_TO_PAPER_PROTOCOL.md` defines the publication gate.

The corpus audit is an active research study, not a paper. `docs/RESEARCH_METHOD_NORTH.md` is the canonical methodological direction and `research/P000_CORPUS_AUDIT_PROTOCOL.md` is its protocol.

Current paper state: P001 and P007 are working drafts; P008–P010 are empirical/theoretical protocols; P012 is a framework draft defining the cross-scale bridge. No paper is treated as an empirical result until the repository contains the corresponding measured evidence.

## 6. Existing research surface
docs/ already contains substantial project knowledge, including ADVANCE.md, EXPERIMENTS.md, CONSCIOUSNESS_SUMMARY.md, DYNAMIC_CORE_V6.md, THEORY_DEBATE_SYNTHESIS.md, HUME_CONSCIOUSNESS_SYNTHESIS.md, JUNG_DISPENZA_SYNTHESIS.md and ZENODO.md.
experiments/ already contains probes and ablations for causal dynamics, valuation, self-model adaptation, self-observation, metacognition, re-entry, integration, attractors, coupled systems, self-development and adversarial theory testing.
Do not replace these documents. Integrate them.

Research navigation and paper conversion are now centralized in:
- RESEARCH_MAP.md
- research/README.md
- research/CLAIM_FAMILY_TRIAGE.md
- docs/CLAIM_TO_PAPER_PROTOCOL.md
- docs/THREE_SCALE_CONSCIOUSNESS.md

## 7. Current research state

The project has a substantial software architecture and a structured research program, but no paper is currently publication-ready.

### S01 — Cross-Cultural Consciousness Claim Recurrence Analysis
The confirmatory coded and semantic outcomes and 23 robustness conditions have been recorded. The observed metrics do not support the preregistered prediction of greater cross-family recurrence in the tested direction. The original raw-output directories were not recovered into the durable archive. The consolidated status and values are in research/S01_RESULTS_STATUS_2026-10-09.md.

### P008 / CF01 — Self-model causality
The hypothesis, evidence map, and registry remain the research basis. Open PR #90 rebuilds the primary assay against registered A/B/C/D conditions, freezes a one-factor continuity-weight intervention, exercises reload/consequence/re-entry, and writes a provenance-bearing JSON artifact. Focused CF01 tests, assay execution, and artifact upload succeeded in workflow run 37898192199; the exact JSON is archived at `research/results/p008/P008_CF01_37898192199.json`. A/B/D selected `preserve` and C selected `explore` in both cycles, with C-vs-B = 1.0, C-vs-D = 1.0, B-vs-D disagreement = 0.0, and all restart state-contract checks passing. This is recorded as a deterministic mechanism-fixture result only, not broad empirical validation. Full-repository pytest remains pending before merge.

### Other scales
P009's relational probes require broader multi-condition validation. P010 lacks a specified physical model with an observable that discriminates it from plausible alternatives. P012 is a framework, not empirical evidence.

Canonical chain:
SOURCE CORPUS → CLAIM INDEX → CLAIM FAMILIES → OPERATIONAL CONSTRUCTS → HYPOTHESES → PREDICTIONS → EXPERIMENTS → RAW ARTIFACTS → AUDIT → RESULTS → PAPERS.

## 8. What an incoming AI must determine
Before changing anything, determine:
1. current paper;
2. corpus state;
3. claims already extracted;
4. claims relevant to the active hypothesis;
5. existing experiments;
6. which experiments have actual results versus code/protocol only;
7. last completed repository state;
8. single next unresolved step.
Never infer completion merely because a file exists.

## 9. Durable memory update protocol
When a meaningful milestone occurs, update **all three state artifacts in the same change set**:
1. `research/CURRENT_CHECKPOINT.md` — live scientific status;
2. `REPO_MEMORY.md` — durable AI context;
3. `RESEARCH_MAP.md` — navigation and entry contract.

At minimum, memory must update CURRENT_STATE, LAST_COMPLETED, ACTIVE_PAPER, ACTIVE_HYPOTHESIS, EVIDENCE_STATUS, EXPERIMENT_STATUS, NEXT_STEP, BLOCKERS, and LAST_UPDATE.
Do not store ephemeral chat dialogue here. Store durable project state and decisions.

## 10. Current checkpoint

CURRENT_STATE = S01 outcomes recorded with original raw-output archive incomplete; P008/CF01 deterministic fixture and full CI checks verified; PR #90 merged to main (e919057). Follow-up generalization protocol remains an unfrozen draft; a pilot-only 32-scenario harness completed development-sample execution with 12.5% divergence, no negative-control disagreement; holdout untouched.
LAST_COMPLETED = Frozen S01 protocol/data snapshot and negative findings; Drive master Git backup and 11-file SHA-256 verification; P008 CF01 controlled fixture output; 2026-10-16 CI validation: 128/128 tests in both native-dynamic-core run 38977366222 and P008 workflow run 38977365990.
ACTIVE_PAPER = NONE — S01 is not promoted to a paper while original-artifact provenance remains incomplete.
ACTIVE_STUDY = P008/CF01 exploratory 32-scenario pilot audited (12.5% C-B/C-D divergence; 0% B-D/A-B); next independently frozen 128-scenario holdout remains unexecuted; S01 archival reconciliation still open.
ACTIVE_HYPOTHESIS = P008 self-model intervention may causally change future trajectory selection beyond matched generic/disconnected state controls; the existing 2-cycle hand-constructed fixture does not establish generalization. S01's recorded cross-family recurrence prediction was not supported in the preregistered direction.
EVIDENCE_STATUS = 4,315 effective claims / 325 corpus units / 328 effective source IDs / 19 source families; passage-level verification and source dependency review remain incomplete.
EXPERIMENT_STATUS = P008 exploratory pilot 32/32, C-B=C-D=0.125 (scenario bootstrap 95% 0.03125..0.25), B-D=A-B=0; Actions run 38978718548 artifact 12079189698, 136/136 full tests. S01 primary and robustness outcomes reported; 23 robustness conditions all retained negative DeltaS and upper-tail p=1.0; V10 metadata audit had 3 missing-count failures; raw output archive incomplete. P008 mechanism fixture run 37898192199 passed focused tests and artifact inspection; both 2026-10-16 full 128-test suites passed (runs 38977366222 and 38977365990).
NEXT_STEP = Durably preserve P008 pilot artifact 12079189698 before 2027-01-14 expiry; independently review sample distribution and freeze code/protocol before any holdout; no consciousness inference.
BLOCKERS = S01 original run-output directories not recovered; P008 holdout untested, pilot evidence in expiring GitHub artifact;  P009 broader validation; P010 discriminating physical model; 52 non-canonical provenance labels await source review.
LAST_UPDATE = 2026-10-16

## 11. Navigation rule
If asked where we are, use this memory and verify referenced files.
If asked what to do next, use NEXT_STEP unless newer repository evidence changed it.
If a task changes project state, update this memory before declaring completion.
If a paper changes status, update papers/README.md and this memory.
If the evidence corpus changes, update the evidence index and this memory.

## 12. Anti-drift rules
- Do not create a parallel Skill-Conscious repository.
- Do not confuse this repo with ConsciousPulse/Skill-Conscious or Aevumard/Skill-Conscious.
- Do not overwrite existing research because it looks redundant; inspect and integrate it.
- Do not treat the manifesto as external scientific consensus.
- Do not treat AI self-report as proof of phenomenal consciousness.
- Do not discard negative or contradictory evidence.
- Do not fabricate corpus counts, results, citations or completion states.
- Do not restart the research program from zero.

## 13. One-file traversal contract
An AI entering this repository should be able to start here and reconstruct the project map without the human repeating the context.
RESEARCH_MAP.md → research/CURRENT_CHECKPOINT.md → REPO_MEMORY.md → research/CLAIM_FAMILY_REGISTRY.md → research/README.md → sources/README.md → corpus-v1/corpus/ → docs/CLAIM_TO_PAPER_PROTOCOL.md → docs/THREE_SCALE_CONSCIOUSNESS.md → papers/README.md → active paper → relevant experiments → source/claim records
This chain is the canonical AI navigation path.
## P008 next engineering gate, 2026-10-16

The verified 32-scenario pilot remains exploratory. Proposed `experiments/p008_generalization_holdout.py` defines a 128-scenario internal reserved-split evaluator, with main-branch lineage/frozen-path verification and first-attempt single-release guard; `.github/workflows/p008-generalization-holdout.yml` only triggers on a separately committed release marker. **Not yet frozen or executed**; do not claim holdout evidence from code existing. Active next step is green CI and freeze PR, then a distinct release review, followed by raw evidence audit. Independent scientific review remains pending.

## P008 internal freeze checkpoint — 2026-10-16

PR #93 merged to main at `524f10a` with a 140-test verified, guarded reserved-split runner. Next separate PR freezes the protocol status `FROZEN_FOR_INTERNAL_RESERVED_SPLIT` and pilot compatibility, with exact merge SHA used as the holdout `freeze_commit`. After that, only a separate release-marker PR may authorize one main-branch push execution. Independent external scientific review remains pending; status is *internal synthetic reserved-split evaluation*, not validated consciousness evidence.

## P008 separate-release handoff (2026-10-16)

Frozen internal protocol/main SHA: `c0278493e8ef31520beea29355f947a7ea3739a8` (PR #94). Release-marker PR proposes `research/p008_holdout_release.json` on a *separate* commit without touching `src/`, P008 code or frozen protocol. This change launches the main-push holdout on merge. Next: verify workflow/job, all 640 raw input/arm JSON, 2000 cluster bootstrap, controls, SHA-256 manifest; archive complete primary results and update canonical three state documents. Do not assert holdout result from a pending marker; external independent review is not complete.

## P008 completed internal reserved-split result — 2026-10-16

PRs #93/#94/#95: sealed code / internal freeze `c0278493` / release `c9728d25`. Actions 38980796822: **128/128 reserved synthetic scenarios** across four arms and two stateful cycles, **140/140 tests**, matched-controls/restarts/hash audits succeeded; C-B and C-D divergence **0.234375**, bootstrap 95% [0.164062, 0.3125], negative-control A-B and B-D **0**, internal mechanism gate PASS. Raw ZIP artifact 12081087004 SHA-256 `8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32` expires 2027-01-14, separately requested long-lived GitHub Release archival (do not claim successful until observed). Canonical new record: `research/p008_holdout_result_v1.json` and `research/results/p008/P008_CF01_INTERNAL_HOLDOUT_2026-10-16.md`. The frozen protocol JSON remains untouched after release. NEXT_STEP: verify permanent evidence archive and solicit independent methods scrutiny plus alternative-implementation replication. No consciousness claim.

## P008 archived original evidence — 2026-10-16

Verified archive: GitHub Actions preservation run 38981166451 PASS; GitHub Release tag `p008-cf01-internal-holdout-20261016`, release 415457666, asset 648924054, SHA-256 `8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32` and 633705 bytes exactly match the original 128-case evidence ZIP. Canonical after-result status `research/p008_holdout_result_v1.json` (frozen preregistration remains intact). NEXT_STEP = obtain independent methods/code review, blinded alternative-implementation replication, broader non-hand-coded candidate/closed-loop tasks; never claim artificial phenomenal consciousness.
