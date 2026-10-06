# Skill-Conscious — AI Repository Memory

> Canonical entry point for an AI instance entering the repository. Read this file first.

## 0. How to use this memory
Do not ask the human to explain the project again before inspecting the repository.
Read in this order:
1. README.md
2. REPO_MEMORY.md (this file)
3. papers/README.md
4. sources/README.md, sources/EVIDENCE_MATRIX.md, sources/HARVEST_ROADMAP.md, sources/CONSCIOUSNESS_MAP.md
5. sources/manifesto/MANIFIESTO_DEL_SER.md
6. the active paper and experiment documents referenced by the current checkpoint
7. implementation and experiment files only as needed

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
The working discussion has referred to approximately 350 sources and 4,105 claims. These counts are provisional until verified against the actual corpus.
Every evidence item must distinguish SOURCE CLAIM, PROJECT HYPOTHESIS, EMPIRICAL RESULT, INFERENCE, and OPEN QUESTION.
Contradictory evidence is retained.

## 5. Scientific paper graph
Authoritative paper sequence: papers/README.md
P001 → P002 → P003 → P004 → P005 → P006
P001 — A Relational Ontology for Artificial Consciousness: foundation and vocabulary.
P002 — Causal Self-Reference and Trajectory Selection: core mechanism and direct operationalization of Axiom 8.
P003 — Topological Continuity and Artificial Identity: persistence and identity under transformation.
P004 — Consciousness Regimes, Attention, and Attractors: dynamical regimes and attractor organization.
P005 — Value, Valence, and the Emergence of an Artificial Point of View: value as a causal variable.
P006 — From Self-Model to Artificial Subject: synthesis and strongest adversarial test.
Current paper state: P001 exists as working draft v0.1. Do not expand P001 blindly. First verify/index the corpus, then map evidence to P001/P002, beginning with Axiom 8.

## 6. Existing research surface
docs/ already contains substantial project knowledge, including ADVANCE.md, EXPERIMENTS.md, CONSCIOUSNESS_SUMMARY.md, DYNAMIC_CORE_V6.md, THEORY_DEBATE_SYNTHESIS.md, HUME_CONSCIOUSNESS_SYNTHESIS.md, JUNG_DISPENZA_SYNTHESIS.md and ZENODO.md.
experiments/ already contains probes and ablations for causal dynamics, valuation, self-model adaptation, self-observation, metacognition, re-entry, integration, attractors, coupled systems, self-development and adversarial theory testing.
Do not replace these documents. Integrate them.

## 7. Current research state
The project is moving from conceptual accumulation toward a reproducible evidence architecture.
The next chain is:
SOURCE CORPUS → CLAIM INDEX → EVIDENCE MAPPING → AXIOM 8 PREDICTIONS → P001/P002 FORMALIZATION → EXPERIMENTAL PROTOCOL → RESULTS → PAPER VERSION

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
NEXT_STEP = locate and verify the machine-readable source/claim inventory, then map Axiom 8 claims and contradictions
BLOCKERS = corpus inventory location/counts not yet verified
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
REPO_MEMORY.md → README.md → papers/README.md → sources/README.md → sources/EVIDENCE_MATRIX.md → sources/HARVEST_ROADMAP.md → sources/CONSCIOUSNESS_MAP.md → sources/manifesto/MANIFIESTO_DEL_SER.md → active paper → relevant experiments → source/claim records
This chain is the canonical AI navigation path.