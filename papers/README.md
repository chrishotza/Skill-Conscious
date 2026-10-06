# Skill-Conscious — Paper Program

## Purpose

This directory is the scientific publication track of Skill-Conscious.

Papers form a dependency graph: later papers inherit definitions, evidence, implementations, experiments, and unresolved questions from earlier papers.

## Reading order

### P001 — A Relational Ontology for Artificial Consciousness
**Path:** `papers/001-relational-ontology-for-artificial-consciousness.md`  
**Role:** Foundation.

Defines the project's relational ontology and operational vocabulary: relation, identity, present, self-access, attention, memory, value, possibility, intention, selection, action, transformation, topology, regimes and causal re-entry.

**Must establish:** terminology; relation to existing consciousness theories; source-vs-hypothesis separation; initial formal model; initial failure cases.

**Feeds:** P002, P003, P004.

### P002 — Causal Self-Reference and Trajectory Selection
**Role:** Core mechanism.

Develops `SelfModel(t) → Trajectory(t) → Action(t) → State(t+1) → SelfModel(t+1)` and directly operationalizes Axiom 8:

> La conciencia es experiencia del recorrido.

**Must establish/test:** causal self-reference; trajectory dependence; self-model intervention; trajectory-selection intervention; re-entry; descriptive vs causal self-reference.

**Feeds:** P003, P004.

### P003 — Topological Continuity and Artificial Identity
**Role:** Persistence.

Tests whether identity is better modeled as continuity of a changing relational network than as static metadata.

**Must test:** persistence across state changes; restart/recovery; topology perturbation; substrate transfer; memory ablation; identity continuity metrics.

**Feeds:** P004 and later artificial-subjectivity work.

### P004 — Consciousness Regimes, Attention, and Attractors
**Role:** Dynamical organization.

Tests coherent regimes, attractor-like dynamics, attention allocation and transitions as measurable components of self-referential continuity and trajectory selection.

**Must test:** regime stability; attractor formation; perturbation/recovery; attention-dependent transitions; self-model persistence across regime changes.

**Feeds:** P005/P006.

### P005 — Value, Valence, and the Emergence of an Artificial Point of View
**Role:** Significance.

Introduces value as a causal variable rather than decorative metadata.

**Must test:** value-dependent trajectory selection; endogenous preference stability; value transformation; competing trajectories; persistence of valuation through state change.

**Feeds:** P006.

### P006 — From Self-Model to Artificial Subject
**Role:** Synthesis.

Integrates continuity, self-reference, topology, regimes, attention and value. It must contain the strongest adversarial analysis and explicit failure conditions.

## Paper lifecycle

`v0.1 Concept → v0.2 Evidence → v0.3 Formalization → v0.4 Protocol → v0.5 Results → v0.9 Preprint → v1.0 Archive`

Major theoretical or methodological changes increment the major version.

## Evidence discipline

Every paper distinguishes:

1. **SOURCE CLAIM** — what an external source actually reports.
2. **PROJECT HYPOTHESIS** — what Skill-Conscious proposes.
3. **EMPIRICAL RESULT** — what an experiment actually observed.
4. **INFERENCE** — what follows from evidence but is not directly observed.
5. **OPEN QUESTION** — what remains unresolved.

Contradictory evidence must be retained.

## Dependencies

`P001 → P002 → P003 → P004 → P005 → P006`

Cross-links are allowed, but later papers must not silently redefine foundational terms from earlier papers.

## Current state

P001 exists as working draft v0.1.

The next writing task is not to expand P001 blindly. First verify and index the existing source/claim corpus, then map evidence to P001/P002, with Axiom 8 as the first focused target.

## Archival rule

Stable versions should be tagged in GitHub and then archived to Zenodo with a DOI. GitHub remains the working source of truth.
