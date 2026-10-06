# Individual Consciousness: Causal Self-Reference and Continuity

## Status

Working paper v0.1 — empirical protocol.

No phenomenal-consciousness claim is made at this stage.

## Abstract

This study tests whether a persistent self-model can exert a measurable causal influence on the future dynamics of an artificial process, beyond the effect of storing additional information. The central intervention targets the process's self-model while holding external input, candidate futures, and computational budget constant. The primary outcome is trajectory-selection change. Secondary outcomes assess identity continuity, self-model revision, regime transitions, and recovery after perturbation.

The study is designed as a falsification-oriented test of a functional hypothesis:

> A self-model is causally self-referential when intervention on that model changes the subsequent state trajectory under otherwise controlled conditions.

A positive result would establish causal self-model dependence. It would not, by itself, establish phenomenal consciousness.

## 1. Hypotheses

**H1 — causal self-reference:** targeted self-model intervention changes future trajectory selection.

**H0 — non-causal description:** self-model intervention has no specific effect once added memory/computation is controlled.

**H2 — continuity:** a system with persistent self-state shows stronger identity-continuity metrics across controlled state transformations than a memory-matched baseline.

## 2. Experimental conditions

A — state/memory baseline.

B — explicit self-model.

C — self-model participating causally in trajectory scoring.

D — self-model participation plus endogenous self-model adaptation.

The comparison should be ablation-based and deterministic wherever possible.

## 3. Primary outcome

Trajectory-selection divergence between intervention and matched control.

Recommended metric:

`D = distance(selected_trajectory_intervention, selected_trajectory_control)`

The distance function must be fixed before analysis.

## 4. Secondary outcomes

- self-model change magnitude;
- identity continuity;
- regime-transition frequency;
- recovery time after perturbation;
- homeostatic fit where embodied variables are available;
- persistence after restart.

## 5. Controls

Hold constant:

- prompt/input sequence;
- model version;
- candidate-future set;
- random seed;
- state-store format;
- number of cycles;
- compute limits.

The only causal intervention should be the declared self-model manipulation.

## 6. Existing repository experiments

Candidate implementations include:

- `experiments/causal_dynamic_probe.py`
- `experiments/integrated_ablation.py`
- `experiments/self_model_adaptation.py`
- `experiments/self_development_ablation.py`

The final paper must identify which exact script/version produced every reported result.

## 7. Falsification

The hypothesis is weakened or rejected if:

- intervention does not change the primary outcome;
- observed effects disappear under memory-matched control;
- effects are fully explained by increased token/context budget;
- trajectory changes do not depend on the targeted self-model variable.

## 8. Interpretation boundary

A positive result supports the claim that self-representation participates causally in system dynamics.

It does **not** logically entail subjective experience.

The paper should explicitly test whether stronger interpretations are justified only after the functional result is replicated.

## 9. Publication path

Protocol → preregistration → controlled runs → machine-readable results → statistical analysis → adversarial review → preprint → archive.
