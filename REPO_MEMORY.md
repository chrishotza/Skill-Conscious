# Skill-Conscious — AI Repository Memory

> Canonical entry point for an AI instance entering the repository. Read this file first.

## 0. How to use this memory
Do not ask the human to explain the project again before inspecting the repository.
Read in this order:
1. RESEARCH_MAP.md
2. README.md
3. REPO_MEMORY.md (this file)
4. research/README.md and research/CLAIM_FAMILY_TRIAGE.md
5. papers/README.md
6. sources/README.md, sources/EVIDENCE_MATRIX.md, sources/HARVEST_ROADMAP.md, sources/CONSCIOUSNESS_MAP.md
7. sources/manifesto/MANIFIESTO_DEL_SER.md
8. the active paper and experiment documents referenced by the current checkpoint
9. implementation and experiment files only as needed

Do not read the whole repository blindly. Use this map to reconstruct context, then expand only when a dependency requires it.

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
Important evidence files:
- sources/BIBLIOGRAPHY.md
- sources/PRIMARY_SOURCES.md
- sources/EVIDENCE_MATRIX.md
- sources/HARVEST_ROADMAP.md
- sources/CONSCIOUSNESS_MAP.md
- sources/SOURCE_CARD_TEMPLATE.md
The verified closed corpus currently contains 325 registered source records and 4,315 effective claim records on branch `corpus-v1`. Coverage is complete at the ledger level; passage-level verification remains a separate task.
Every evidence item must distinguish SOURCE CLAIM, PROJECT HYPOTHESIS, EMPIRICAL RESULT, INFERENCE, and OPEN QUESTION.
Contradictory evidence is retained.

## 5. Scientific paper graph
Authoritative paper map: `papers/README.md`.

P001 → P002 → P003 → P004 → P005 → P006 is the original artificial-consciousness mechanism track.

The new cross-scale track is:
P007 → P008 / P009 / P010 → P011.

- P007 — Three-Scale Framework: Fundamental / Relational / Individual.
- P008 — Individual scale: causal self-reference and continuity.
- P009 — Relational scale: coupled-agent dynamics and reciprocal causality.
- P010 — Fundamental scale: testability and model discrimination.
- P011 — Cross-scale synthesis.

`docs/CLAIM_TO_PAPER_PROTOCOL.md` defines the publication gate.

Current paper state: P001 and P007 are working drafts; P008–P010 are empirical/theoretical protocols. No paper is treated as an empirical result until the repository contains the corresponding measured evidence.

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
The project has moved from conceptual accumulation into a claim-to-paper research operating system.

Canonical chain:

SOURCE CORPUS → CLAIM INDEX → CLAIM FAMILIES → OPERATIONAL CONSTRUCTS → HYPOTHESES → FALSIFIABLE PREDICTIONS → EXPERIMENTS → RESULTS → PAPERS

The three-scale research frame is:

FUNDAMENTAL → RELATIONAL → INDIVIDUAL

This ordering is a testable framework, not an established hierarchy of consciousness.

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
When a meaningful milestone occurs, update this file with CURRENT_STATE, LAST_COMPLETED, ACTIVE_PAPER, ACTIVE_HYPOTHESIS, EVIDENCE_STATUS, EXPERIMENT_STATUS, NEXT_STEP, BLOCKERS, and LAST_UPDATE.
Do not store ephemeral chat dialogue here. Store durable project state and decisions.

## 10. Current checkpoint
CURRENT_STATE = evidence architecture / paper-program organization
LAST_COMPLETED = paper dependency graph formalized in papers/README.md
ACTIVE_PAPER = P001 → P002 transition
ACTIVE_HYPOTHESIS = Axiom 8: consciousness as experience of traversal
EVIDENCE_STATUS = source library exists; exact corpus counts still require verification
EXPERIMENT_STATUS = multiple experiment scripts exist; result provenance must be checked before treating them as empirical results
NEXT_STEP = map the 4,315 corpus claims into claim families, operational constructs, competing hypotheses and paper sections; begin P008 individual-scale experiments
BLOCKERS = relational probe needs implementation; fundamental-scale model needs a genuinely discriminating physical hypothesis
LAST_UPDATE = 2026-10-06

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
RESEARCH_MAP.md → REPO_MEMORY.md → research/README.md → sources/README.md → corpus-v1/corpus/ → docs/CLAIM_TO_PAPER_PROTOCOL.md → docs/THREE_SCALE_CONSCIOUSNESS.md → papers/README.md → active paper → relevant experiments → source/claim records
This chain is the canonical AI navigation path.