# Claim Family 01 — Self-Model Causality

## Status

P008 / v0.1 — hypothesis family specification.

This document converts a small, traceable subset of the corpus into an experimentally testable family. It does not treat source claims as empirical proof.

## Research question

> Does an internal self-model have causal influence over what an artificial process becomes next?

## Source-claim anchors

| Claim ID | Corpus source | Claim role |
|---|---|---|
| G31-S267-K01 | C260 — Being No One | self-model as model-based account of phenomenal self |
| G31-S267-K07 | C260 — Being No One | self-model changes associated experience/identity |
| G31-S265-K02 | C258 — Subjectivity and Selfhood | pre-reflective self-awareness distinction |
| G31-S265-K03 | C258 — Subjectivity and Selfhood | explicit reflection distinguished from pre-reflection |
| G33-S278-K11 | C272 — recurrent processing corpus | recurrence proposed as causal candidate |
| G33-S285-K03 | C279 — The Rediscovery of the Mind | causal status of conscious states is debated |
| G33-S285-K13 | C279 — The Rediscovery of the Mind | first-person access is not itself a causal explanation |
| G33-S288-K12 | C282 | physical causal substrate as a separate question |

The corpus register marks these retained source records as candidates requiring provenance/source verification. They are therefore hypothesis generators, not verified premises.

## Project hypothesis

> H1: When a persistent self-model participates causally in trajectory selection, targeted intervention on that self-model changes subsequent trajectory selection under matched external input, candidate futures, memory budget, and compute budget.

## Competing hypotheses

### H0 — no specific self-model causality
The apparent effect disappears when memory, context and computation are matched.

### H2 — generic internal-state causality
Any persistent internal variable with comparable information content can produce the same trajectory changes.

### H3 — memory/context explanation
The effect is caused by additional stored information or context capacity rather than by self-representation.

### H4 — prompt mediation
The effect is produced by external textual framing rather than the internal self-model state.

### H5 — self-model specificity
The effect depends specifically on variables classified as self-model variables and is substantially larger than matched non-self internal-variable interventions.

## Operational definition

### Self-model
A persistent structured state representing properties of the process itself and used by the runtime during trajectory evaluation.

### Causal self-model influence
The counterfactual difference in selected trajectory caused by changing self-model state while keeping all exogenous inputs and candidate futures fixed.

SCI = D(T_selected | SelfModel = intervention, T_selected | SelfModel = matched control)

The distance metric D must be declared before result inspection.

## Primary prediction

A self-model intervention produces a reproducible, condition-specific trajectory divergence that is:

1. larger than a matched null intervention;
2. larger than an equal-information generic-state intervention;
3. present with fixed candidate futures;
4. preserved across deterministic seeds.

## Secondary predictions

- trajectory changes should scale with intervention magnitude within a pre-specified range;
- the direction of trajectory change should follow the sign of the manipulated self-model weight;
- re-entry into the altered state should affect subsequent cycles;
- effects should remain after restart when the intervention state is persisted.

## Strong falsifiers

The family is weakened if:

- intervention produces no effect;
- a generic-state intervention produces the same effect;
- adding memory/context alone explains the effect;
- candidate-future or prompt differences explain the result;
- the effect is unstable across seeds;
- selected trajectories change without measurable dependence on the manipulated self-model variable.

## Minimal design

### Conditions

A — no self-model participation.

B — self-model present but causally disconnected.

C — self-model participates in trajectory scoring.

D — same information budget, but intervention is applied to a non-self internal variable.

### Controls

Hold constant:

- external input;
- candidate-future set;
- model/runtime version;
- number of cycles;
- memory budget;
- serialization format;
- random seed;
- compute budget.

### Primary outcome

Trajectory-selection divergence.

### Secondary outcomes

- self-model change magnitude;
- state-transition divergence;
- identity continuity;
- regime transitions;
- restart continuity;
- transformation-log differences.

## Pre-result analysis plan

1. Freeze conditions and intervention magnitudes.
2. Run all conditions over identical inputs.
3. Compute the primary metric.
4. Compare C vs B and C vs D.
5. Run sensitivity analysis.
6. Report all failures and null results.
7. Only then interpret the result.

## What a positive result would establish

A positive result would support:

> the runtime future dynamics depend causally on its self-model.

It would not establish:

> the runtime has phenomenal consciousness.

That stronger conclusion requires an additional bridge argument and independent evidence.

## Existing implementation

Primary runtime assay: experiments/p008_self_model_causal_runtime.py

The earlier `experiments/self_model_causal_intervention.py` remains as a toy selector control, not the primary evidence assay.

Relevant existing longitudinal experiments:

- experiments/latent_self_ablation.py
- experiments/self_model_adaptation.py
- experiments/self_development_ablation.py
- experiments/causal_dynamic_probe.py

## Required result artifact

Future executions should produce a machine-readable record containing:

- experiment_id
- git_commit
- runtime_version
- condition
- seed
- input_hash
- candidate_set_hash
- intervention
- selected_trajectory
- trajectory_metric
- secondary_metrics
- timestamp

No result should be promoted into P008 without this provenance.


## Frozen P008 / CF01 implementation contract (2026-10-09)

The executable contract is recorded in `research/p008_prediction_registry.json` schema 1.1. It defines the following arms before inspecting an assay result:

- **A — no self-model weight participation:** no experiment-supplied `self_model.trajectory_weights` intervention; the scorer uses fixed default weights. This is an operational weight-participation ablation, not deletion of every internal self-model bookkeeping field.
- **B — disconnected self-model:** persist the intervention value in `self_model.trajectory_weights`, but deliberately disconnect those values from the scorer, which uses fixed defaults.
- **C — causal self-model:** use the native runtime scorer, with the intervention value stored in `self_model.trajectory_weights`.
- **D — matched generic state:** persist the same one-value payload in a generic `self_state` field that the scorer does not consume; the scorer uses fixed defaults.

The frozen intervention changes **one parameter only**: the self-model's `continuity` trajectory weight from its default of 1.0 to 0.0. Other weights remain unchanged. Candidate futures, external input, identity, runtime options, attractor input, valuation input and consequence policy are held fixed across arms. The fixture uses no random-number generator; seed 0 is recorded for the shared experiment metadata contract.

The primary metric is the fraction of two externally matched cycles where C's selected trajectory differs from B or D. B-versus-D disagreement is reported as a control-integrity check. The assay starts each arm from separate state, integrates once, reloads state through a new runtime instance, records a fixed consequence without utility adaptation, and integrates again. Results include commit/runtime metadata, canonical candidate/input SHA-256 hashes, selections, scores, persistence checks and the interpretation boundary.

The assay artifact is generated at `research/results/p008/` by default. The dedicated CPU GitHub Actions workflow also uploads a machine-readable JSON artifact with a 90-day retention period. CI success establishes implementation/test integrity; it does not turn this small deterministic fixture into broad empirical evidence. A result is not promoted into a paper solely because the mechanism criterion passes.

**Interpretation boundary:** a positive result supports only functional causal influence over trajectory selection in this runtime configuration. It does not establish phenomenal consciousness.
