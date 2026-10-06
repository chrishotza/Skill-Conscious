# Corpus → Paper Triage

## Audit basis

Source branch: `corpus-v1`

Effective ledger:

- 4,315 claim records;
- 4,315 unique global claim IDs;
- 325 unique corpus/source-register IDs;
- 328 effective source IDs.

This is coverage accounting, not passage-level verification.

## Immediate triage

A first machine-readable triage was performed using **explicit claim-type tags only**. This is intentionally conservative: it does not infer a three-scale classification from free-text similarity.

| Research family | Candidate claims | Triage rule |
|---|---:|---|
| Individual | 1,311 | explicit types such as SELF_MODEL, REFLEXIVITY, CONTINUITY, PERSISTENCE, MEMORY, INTERIORITY, EMBODIMENT, INTEROCEPTION, VALENCE, ATTENTION, PERCEPTION, ACTION, IDENTITY, AWARENESS, PHEN, TEMPORAL, DYNAMICS, TRANSFORMATION, etc. |
| Relational | 528 | explicit types such as RELATION, COLLECTIVE, INTERSUBJECTIVITY, SOCIAL_SELF, GROUP, COMMUNITY, UNITY, INTERPENETRATION, CORRESPONDENCE, TRANSPERSONAL, etc. |
| Fundamental | 164 | explicit types such as COSMO, GLOBAL, UNIVERSAL, NONLOCAL, FIELD, QUANTUM, IDEALISM, PANPSYCHISM, PANPROTOPSYCHISM, PHYS_SUBSTRATE, PHYSICAL, PHYSICS, RELATIVITY, ULTIMATE, COSMIC, REALITY, etc. |
| Unassigned / cross-cutting | 2,312 | no high-confidence exact-type rule yet |

Categories are not mutually exclusive in principle. The table above counts a first-pass family bucket, not a final ontology.

## Why the unassigned set matters

The 2,312 unassigned records should not be discarded.

Many are:

- META;
- PRACTICE;
- ONTO;
- STATE;
- CONTRAST;
- CAUSAL;
- COSMO/RELATION combinations without a dedicated scale tag;
- historical, methodological or source-context claims.

These are likely to become the **evidence, controls, boundary conditions and contradiction sections** of the papers rather than independent papers.

## Paper allocation

### P008 — Individual

Primary reservoir: the 1,311 individual candidates.

First filter:

1. self-model causality;
2. temporal continuity;
3. identity persistence;
4. embodiment/interoception;
5. metacognitive access;
6. transformation/re-entry.

### P009 — Relational

Primary reservoir: the 528 relational candidates.

First filter:

1. reciprocal causal influence;
2. intersubjectivity;
3. coupling;
4. collective dynamics;
5. common-input controls;
6. network-level prediction.

### P010 — Fundamental

Primary reservoir: the 164 fundamental candidates.

Hard requirement:

> no metaphysical claim enters an empirical result section without a specified discriminator against a non-conscious physical null model.

### P011 — Cross-scale synthesis

Uses:

- overlapping claims;
- contradictions;
- failure conditions;
- results from P008/P009/P010;
- claims in the unassigned set that establish boundaries or alternative explanations.

## Provenance integrity finding

The effective ledger contains 52 records whose `provenance` value is not one of the canonical schema classes `P1, P2, P2*, S1, S2, X1, O1`.

They are concentrated in three source groups:

- S069 — Yoruba Ifá / Odu corpus — 18 records;
- S070 — Huarochirí Manuscript — 17 records;
- S071 — Diné Bahane' — 17 records.

These labels currently carry source names rather than canonical provenance classes.

**Action:** normalize only after source-level review. Do not silently overwrite them.

## Research consequence

The corpus is large enough to support a real publication program, but the correct unit of work is now:

```text
4,315 CLAIMS
     ↓
CLAIM FAMILIES
     ↓
OPERATIONAL CONSTRUCTS
     ↓
COMPETING HYPOTHESES
     ↓
PREDICTIONS
     ↓
EXPERIMENTS
     ↓
RESULTS
     ↓
PAPERS
```

The goal is not to publish 4,315 claims.

The goal is to make the strongest recurrent claims testable and let the data decide which survive.
