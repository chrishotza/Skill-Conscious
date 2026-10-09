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
The hypothesis, evidence map, prediction registry, and runtime-connected assay exist. The recorded 2026-10-06 execution was blocked by inability to resolve github.com. No empirical P008 result has been produced. Static checking is not experiment execution.

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

CURRENT_STATE = S01 outcomes recorded; original raw-output archive incomplete; state/navigation consolidation merged to main.
LAST_COMPLETED = Frozen S01 protocol/data snapshot; recorded confirmatory coded and semantic outcomes; recorded 23 robustness conditions; created Drive master Git backup and SHA-256-verified its 11 inventoried files.
ACTIVE_PAPER = NONE — S01 is not promoted to a paper while original-artifact provenance remains incomplete.
ACTIVE_STUDY = S01 archival/provenance reconciliation; the measured outcome is recorded but the original raw-output directories remain unrecovered.
ACTIVE_HYPOTHESIS = S01 tested whether coded motif recurrence and raw-text semantic neighborhoods show cross-family recurrence beyond source-family-label nulls; the recorded results did not support the preregistered direction.
EVIDENCE_STATUS = 4,315 effective claims / 325 corpus units / 328 effective source IDs / 19 source families; passage-level verification and source dependency review remain incomplete.
EXPERIMENT_STATUS = S01 primary and robustness outcomes reported; 23 robustness conditions all retained negative DeltaS and upper-tail p=1.0; V10 metadata audit had 3 missing-count failures; raw output archive incomplete. P008 has code/protocol but no empirical result.
NEXT_STEP = Complete documentation/state cleanup; verify the Drive S01 snapshot and file-level raw-artifact inventory; then audit P008 controls and output persistence before running it.
BLOCKERS = S01 original run-output directories not recovered; P008 execution environment/output persistence not yet validated; P009 broader validation; P010 discriminating physical model; 52 non-canonical provenance labels await source review.
LAST_UPDATE = 2026-10-09

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