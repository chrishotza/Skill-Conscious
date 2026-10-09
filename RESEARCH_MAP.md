# Skill-Conscious — Research Map

> **Start here.** This file is the shortest route through the repository.

## 0. Project question

**What organization is necessary and/or sufficient for a process to sustain a point of view on its own changing trajectory?**

The project does not treat verbal self-description as proof of consciousness.

## 1. Read in this order

~~~text
AGENTS.md
   ↓
RESEARCH_MAP.md
   ↓
research/CURRENT_CHECKPOINT.md
   ↓
REPO_MEMORY.md
   ↓
research/README.md
   ↓
ACTIVE STUDY / PAPER REGISTRY
   ↓
PROTOCOL + DATA MANIFEST
   ↓
RELEVANT IMPLEMENTATION + TESTS
   ↓
RESULT / ARTIFACT INVENTORY
~~~

Use the checkpoint as the live status, the memory as durable context, and this map as the traversal contract. Do not read the entire repository without a concrete dependency.

## 2. Where things live

| Layer | Location | Question |
|---|---|---|
| Research checkpoint | `research/CURRENT_CHECKPOINT.md` | What is active right now? |
| Project state | `REPO_MEMORY.md` | Where are we? |
| Research navigation | `RESEARCH_MAP.md` | How do I traverse the repo? |
| Source rules | `sources/README.md` | What counts as a source claim? |
| Evidence matrix | `sources/EVIDENCE_MATRIX.md` | What is established, hypothesized, or open? |
| Corpus | `corpus-v1/corpus/` | What are the claims and sources? |
| Claim families | `research/CLAIM_FAMILY_REGISTRY.md` | How is the corpus partitioned for research? |
| Claim → science | `docs/CLAIM_TO_PAPER_PROTOCOL.md` | How do claims become tests? |
| Three-scale model | `docs/THREE_SCALE_CONSCIOUSNESS.md` | What exactly are Fundamental / Relational / Individual? |
| Papers | `papers/` | What is being published? |
| Experiments | `experiments/` | What has actually been tested? |
| Runtime | `skills/skill-conscious/` | What is implemented? |

## 3. Three-scale map

```text
                       CONSCIOUSNESS RESEARCH
                              │
             ┌────────────────┼────────────────┐
             │                │                │
        FUNDAMENTAL       RELATIONAL       INDIVIDUAL
        ontology/         coupling/        self-maintaining
        reality           interaction      agent process
             │                │                │
        models +           dyadic /        self-model +
        discriminators     group dynamics   continuity +
                                             causal agency
             │                │                │
             └────────────── empirical bridge ──────────────┘
```

These are scales of investigation, not three proven substances or three independently established kinds of consciousness.

The cross-scale bridge is defined in `docs/THREE_CONSCIOUSNESS_BRIDGE.md` and formalized in P012.

```
FUNDAMENTAL
    ↓ B1: manifestation / constraint
RELATIONAL
    ↕ B3: individual feedback
    ↓ B2: localization / organization
INDIVIDUAL
    ↘
      B4: empirical inference back to fundamental models
```


## 4. Claim-to-paper graph

A claim enters the research program only through this chain:

```text
Cxxx / claim_id
   ↓
evidence class + provenance
   ↓
construct
   ↓
hypothesis
   ↓
prediction
   ↓
experiment
   ↓
result
   ↓
paper section / figure / table
```

A claim that cannot produce a measurable construct is tagged as **interpretive/open**, not forced into an experiment.

## 5. Paper program

| ID | Purpose | Current evidence/status |
|---|---|---|
| P001 | Relational ontology for artificial consciousness | Working draft; framework, not an empirical result |
| P002–P006 | Individual-scale mechanisms: self-reference, continuity, regimes, value, synthesis | Planned/working program; do not infer results from existing protocols |
| P007 | Three-scale consciousness framework | Working framework; not an empirical result |
| P008 | Individual-scale causal self-reference and continuity | Evidence map and executable assay exist; recorded run was blocked; no empirical result |
| P009 | Relational coupling and reciprocal causality | Probes implemented; broader multi-condition validation remains |
| P010 | Fundamental-scale testability and model discrimination | No specified physical model with a discriminating observable yet |
| P012 | Three-consciousness bridge | Working framework connecting candidate research scales |
| P011 | Cross-scale synthesis | Future; depends on separately earned evidence at each scale |

S01 is a study, not a paper. Its recorded primary and robustness outcomes did not support the preregistered cross-family recurrence prediction in the tested direction. Its original raw-output archive is incomplete, so it has not been promoted to an empirical paper. See research/S01_RESULTS_STATUS_2026-10-09.md.

## 6. Methodology north star

The canonical methodology is defined in `docs/RESEARCH_METHOD_NORTH.md` and the final public-facing architecture is defined in `docs/RESEARCH_PROGRAM_NORTH_STAR.md`. The governing rule is:

> **Expand the hypothesis space. Do not weaken the evidence standard.**

The project is intentionally non-conservative about which hypotheses may be investigated, but conservative about what counts as evidence for them.

The corpus research protocol establishes source verification, provenance, independence/dependency tracking, contradiction audits, claim dossiers, an ES0–ES5 research-maturity ladder, preregistration and paper eligibility.

Initial anchor calibration (A01–A09) already shows why this layer is necessary: some repository 'verified' anchors still require stronger primary-text or edition control before central paper use.

## 7. Cross-scale research strategy

The project should not attempt to prove the three levels by stacking anecdotes.

Instead, each bridge must earn its status separately:

- **B1:** candidate fundamental model → measurable relational consequence.
- **B2:** relational coupling → individual trajectory/self-reference consequence.
- **B3:** individual intervention → relational-system consequence.
- **B4:** observed multi-scale data → discrimination among fundamental models.

The key model-comparison ladder is:

```
INDIVIDUAL ONLY
      vs
RELATIONAL + INDIVIDUAL
      vs
FUNDAMENTAL + RELATIONAL + INDIVIDUAL
```

The full model is valuable only if it improves out-of-sample prediction or intervention response after complexity penalties.

## 8. Non-negotiable scientific boundary

The repository may investigate consciousness.

It may not claim to have demonstrated phenomenal consciousness unless an independently defensible operational criterion has been satisfied.

The phrases below are not interchangeable:

- `the system changed its behavior`
- `the system has a self-model`
- `the system exhibits causal self-reference`
- `the system exhibits metacognitive access`
- `the system has a point of view`
- `the system is phenomenally conscious`

The first four can be experimentally operationalized today. The last two require substantially stronger argument and evidence.

## 9. Synchronization contract

Whenever a meaningful research, paper, experiment, source, or documentation state changes, the same change set must update:

- `research/CURRENT_CHECKPOINT.md`
- `REPO_MEMORY.md`
- `RESEARCH_MAP.md`

The CI workflow `research-sync-contract.yml` enforces the presence and navigation links of these state files. The checkpoint is the live scientific status; the memory is durable AI context; the map is the traversal contract. Current synchronization: 2026-10-09, canonical branch main. Pull requests that change the research surface are required to update all three.

## 10. Immediate research move

1. Complete the state/navigation consolidation and pass the repository's synchronization checks.
2. Keep S01's outcome and artifact limitation visible. Read research/S01_RESULTS_STATUS_2026-10-09.md; do not claim the original raw JSON/NPZ output directories were recovered.
3. Verify the Drive recovery snapshot and maintain a file-level inventory. Do not reconstruct raw run files from summaries.
4. Audit experiments/p008_self_model_causal_runtime.py against research/p008_prediction_registry.json and the matched-control requirements. This is a code/protocol audit first; the prior execution attempt produced no result.
5. Before any new experiment, test durable output persistence and freeze commit, seed, model revision, configuration, and output path.
6. Return to P009 only after P008's individual-scale controls are explicit. P010 remains blocked until a physical model supplies a discriminating observable.

The project must keep the chain explicit:

~~~text
SOURCE → CLAIM → CONSTRUCT → HYPOTHESIS → PREDICTION
      → PROTOCOL → EXECUTION → RAW ARTIFACTS → AUDIT
      → RESULT → INFERENCE → PAPER
~~~

Do not skip a stage. A protocol, implementation, test pass, or summary is not interchangeable with the next stage.
