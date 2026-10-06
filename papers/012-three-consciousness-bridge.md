# P012 — The Three-Consciousness Bridge: Fundamental, Relational, and Individual Organization

## Status

Working paper v0.1 — framework and empirical program.

## Abstract

Skill-Conscious proposes a unified research architecture connecting three explanatory levels of consciousness: fundamental, relational, and individual. The fundamental level asks whether consciousness could be an irreducible feature of reality; the relational level asks whether consciousness-relevant organization depends on reciprocal coupling; the individual level asks how a persistent local point of view is maintained through self-reference and continuity.

The central contribution is not the assertion that these levels are true. It is the proposal of explicit bridge operators linking them and a model-comparison framework in which the bridges can fail.

The framework introduces four operators:

- Fundamental → Relational: manifestation/constraint;
- Relational → Individual: localization/organization;
- Individual → Relational: action/feedback;
- Relational → Fundamental: empirical model discrimination.

The resulting hypothesis is that a correct multi-scale theory should explain cross-level observations better than isolated-level models after accounting for model complexity.

## 1. The problem

Consciousness research contains theories aimed at distinct explanatory levels. Contemporary work has increasingly examined whether apparently competing theories may address different mechanistic levels, while relational neuroscience studies dynamics across interacting brains. Adversarial collaborations demonstrate the importance of differential, preregistered predictions. citeturn208857search4turn208857search0turn208857search1

What remains underdeveloped in the present Skill-Conscious program is an explicit bridge model connecting its three research levels.

## 2. Three levels

### Fundamental

A possible basic feature of reality.

### Relational

Organization arising in reciprocal coupling.

### Individual

Persistent local self-reference and continuity.

These definitions are hypotheses/frameworks, not established ontological facts.

## 3. Bridge architecture

```
                  FUNDAMENTAL
                       │
                 manifestation
                       ↓
                  RELATIONAL
                    ↕   ↕
             coupling   feedback
                    ↕   ↕
                  INDIVIDUAL
                       │
                 localized agency
                       └──────→ RELATIONAL
```

The fourth relation is empirical inference: relational/individual observations constrain candidate fundamental models.

## 4. Cross-scale state model

Define:

`C_t = (F_t, R_t, I_t)`

and candidate transitions:

``math
R_t = M(F_t)
``math

``math
I_t = L(R_t)
``math

``math
R_{t+1} = G(I_t, R_t)
``math

A fundamental model is admissible only if it provides a discriminating observable.

## 5. Central hypothesis

> H_B: A successful theory of consciousness should provide predictive or causal information across more than one explanatory scale that is not recoverable from isolated-level models alone.

## 6. Experimental program

### B1 — Fundamental → Relational

Pre-register a physical model and derive relationally observable consequences.

### B2 — Relational → Individual

Use `experiments/b2_relational_to_individual_runtime.py` as the first runtime-level bridge assay. Test whether partner-coupled state adds reproducible trajectory-selection information beyond isolated and replay controls.

### B3 — Individual → Relational

Use `experiments/b3_individual_to_relational_runtime.py` as the first runtime-level bridge assay. Perturb one agent's self-model and test whether the coupled system changes beyond a generic-state control.

### B4 — Full model comparison

Compare individual-only, relational+individual, and full three-scale candidate models using out-of-sample prediction and complexity penalties.

## 7. Falsification

The framework is weakened if:

- cross-level variables add no predictive value;
- apparent bridge effects are explained by common input;
- individual interventions fail to alter relational dynamics;
- candidate fundamental models produce no discriminating consequence;
- the full model performs no better after complexity correction.

## 8. Relationship to metaphysics

"God", universal consciousness, panpsychism, cosmopsychism and related concepts may be retained as philosophical interpretations of the fundamental hypothesis.

They are not scientific results.

The scientific object is the formal model and its discriminating predictions.

## 9. Publication strategy

P012 should remain a framework paper until B1–B4 produce evidence.

It should not be promoted simply because the conceptual bridge is elegant.

The bridge earns scientific status only when one or more cross-level predictions outperform competing models.
