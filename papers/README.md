# Skill-Conscious — Paper Program

## Purpose

This directory is the scientific publication track of Skill-Conscious.

Papers form a dependency graph: later papers inherit definitions, evidence, implementations, experiments, and unresolved questions from earlier papers.

## Program north star

The full research architecture is defined in `docs/RESEARCH_PROGRAM_NORTH_STAR.md`.

The project has two layers:

- **Research layer:** exhaustive, technical, adversarial, reproducible.
- **Public layer:** a small number of reader-facing claims whose wording is earned by the research.

The intended public narrative is:

1. What do we mean by consciousness?
2. What makes a local point of view persistent?
3. What role does relation play?
4. Is consciousness fundamental?
5. What, if anything, connects the three?

> **Hide complexity, never hide evidence.**

No paper is promoted to the public model until it contains actual analyzed evidence. Protocols and frameworks remain research artifacts.

## First substantive study

The first substantive study is S01 — Cross-Cultural Consciousness Claim Recurrence Analysis.

**Latest status (2026-10-09):** recorded confirmatory coded and semantic outcomes plus 23 robustness conditions did not support the preregistered cross-family-recurrence prediction in the tested direction. The original raw-output archive remains incomplete, so the study's exit condition and paper-promotion gate are not yet satisfied.

The consolidated figures, audit caveats, recovery location, and exact remaining archival gap are in research/S01_RESULTS_STATUS_2026-10-09.md. S01 remains a research study, not a published result paper. Its frozen preregistration must not be edited retrospectively.

## Canonical paper map

### P001 — A Relational Ontology for Artificial Consciousness
**Path:** `papers/001-relational-ontology-for-artificial-consciousness.md`  
**Role:** foundation and vocabulary.

Defines relation, identity, present, self-access, attention, memory, value, possibility, intention, selection, action, transformation, topology, regimes and causal re-entry.

**Feeds:** P002, P003, P004.

### P002 — Causal Self-Reference and Trajectory Selection
**Role:** core individual-scale mechanism.

Develops:

```text
SelfModel(t)
   ↓
Trajectory(t)
   ↓
Action(t)
   ↓
State(t+1)
   ↓
SelfModel(t+1)
```

**Must test:** self-model intervention, trajectory-selection dependence, re-entry, and descriptive vs causal self-reference.

### P003 — Topological Continuity and Artificial Identity
**Role:** persistence.

Tests whether identity is better modeled as continuity of a changing relational network than as static metadata.

### P004 — Consciousness Regimes, Attention, and Attractors
**Role:** dynamical organization.

Tests regime stability, attractor formation, perturbation/recovery, attention-dependent transitions and self-model persistence.

### P005 — Value, Valence, and the Emergence of an Artificial Point of View
**Role:** significance.

Tests value-dependent trajectory selection, endogenous preference stability and valuation through state change.

### P006 — From Self-Model to Artificial Subject
**Role:** synthesis.

Integrates continuity, self-reference, topology, regimes, attention and value. This paper carries the strongest adversarial analysis and the strictest failure conditions.

### P007 — A Three-Scale Framework for Consciousness: Fundamental, Relational, and Individual
**Path:** `papers/007-three-scale-consciousness-framework.md`  
**Role:** framework.

Defines the three-scale research program and its asymmetric evidential burden.

**Status:** working paper v0.1.

### P008 — Individual Consciousness: Causal Self-Reference and Continuity
**Path:** `papers/008-individual-consciousness-causal-self-reference.md`  
**Role:** empirical protocol + evidence mapping.

Tests whether intervention on a persistent self-model changes future trajectory under controlled conditions.

**Status:** working paper v0.2 — evidence mapping + protocol.

### P009 — Relational Consciousness: Coupled-Agent Dynamics and Reciprocal Causality
**Path:** `papers/009-relational-consciousness-coupled-agent-dynamics.md`  
**Role:** empirical protocol.

Tests whether reciprocal coupling creates predictive/causal structure beyond common input.

**Status:** working paper v0.1 — protocol.

### P010 — Fundamental Consciousness: Testability and Model Discrimination
**Path:** `papers/010-fundamental-consciousness-testability.md`  
**Role:** theory + empirical discrimination program.

Defines the minimum requirements for turning a fundamental-consciousness proposal into a testable scientific model.

**Status:** working paper v0.1 — no physical model claimed yet.

### P012 — The Three-Consciousness Bridge: Fundamental, Relational, and Individual Organization
**Path:** `papers/012-three-consciousness-bridge.md`  
**Role:** cross-scale bridge framework.

Defines bridge operators B1–B4 and the model-comparison strategy linking the three research levels.

**Status:** working paper v0.1.

### P011 — Cross-Scale Synthesis of Consciousness
**Role:** later synthesis.

Combines fundamental, relational and individual evidence only after the separate research programs have produced results.

## Dependency graph

```text
P001
 ├── P002 ──┐
 ├── P003   │
 ├── P004   ├── P006
 └── P005 ──┘

P007
 ├── P008
 ├── P009
 └── P010
      \
       └── P011
```

P007 is the initial three-scale framework. P012 is the explicit bridge architecture connecting the three scales and defining cross-level experiments.

## Paper lifecycle

`v0.1 Concept → v0.2 Evidence → v0.3 Formalization → v0.4 Protocol → v0.5 Results → v0.9 Preprint → v1.0 Archive`

Major theoretical or methodological changes increment the major version.

## Evidence discipline

Every paper distinguishes:

1. **SOURCE CLAIM** — what an external source actually reports.
2. **PROJECT HYPOTHESIS** — what Skill-Conscious proposes.
3. **OPERATIONAL DEFINITION** — how a construct is measured.
4. **EMPIRICAL PREDICTION** — what should happen before the result is seen.
5. **EMPIRICAL RESULT** — what an experiment actually observed.
6. **INFERENCE** — what follows from evidence but is not directly observed.
7. **OPEN QUESTION** — what remains unresolved.

Contradictory evidence must be retained.

## Publication gate

A paper cannot move to preprint merely because the prose is complete.

It must have:

- traceable claim IDs;
- competing hypotheses;
- operational definitions;
- preregistered or otherwise frozen predictions;
- explicit controls and null models;
- reproducible code and data provenance;
- negative-result handling;
- an interpretation section no stronger than the evidence.

See `docs/CLAIM_TO_PAPER_PROTOCOL.md`.

## Archival rule

Stable versions should be tagged in GitHub and archived to Zenodo with a DOI. GitHub remains the working source of truth.
