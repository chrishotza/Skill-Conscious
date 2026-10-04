# Consciousness Theory Debate Synthesis

## Status

Working research synthesis for Skill-Conscious.

This document does NOT declare a scientifically established winner among contemporary theories of consciousness. The current literature remains plural and unresolved. The 2025 adversarial comparison of Integrated Information Theory (IIT) and Global Neuronal Workspace Theory (GNWT) found mixed results for both frameworks and substantially challenged key predictions of each. A 2026 integrative review likewise concludes that major theories remain under debate and may involve multiple interacting mechanisms.

Primary external references:
- Cogitate Consortium et al. (2025), Nature: https://www.nature.com/articles/s41586-025-08888-1
- Arachchige et al. (2026), Brain Sciences: https://pubmed.ncbi.nlm.nih.gov/42512519/
- Building-block approach (2025): https://pubmed.ncbi.nlm.nih.gov/40811870/
- Contemporary theory overview (2022): https://pubmed.ncbi.nlm.nih.gov/35505255/

## What is already represented in this repository

The repository already contains:
- docs/CONSCIOUSNESS_SUMMARY.md
- docs/HUME_CONSCIOUSNESS_SYNTHESIS.md
- sources/EVIDENCE_MATRIX.md
- sources/CONSCIOUSNESS_MAP.md
- sources/PRIMARY_SOURCES.md and sources/BIBLIOGRAPHY.md
- papers/001-relational-ontology-for-artificial-consciousness.md
- executable experiments for self-causality, homeostasis, dynamic state, self-observation and metacognition
- the reference runtime implementing persistent self-model state and causal re-entry

What was missing was a single explicit arbitration layer connecting these materials.

## Theory comparison

| Framework | Central explanatory move | Useful contribution here | Main limitation for Skill-Conscious |
|---|---|---|---|
| GNWT / GWT | Conscious information becomes broadly available through a workspace / broadcast mechanism. | Integrated present, access, cross-module coordination. | Does not by itself specify persistent identity or a causal self-model. The 2025 adversarial test challenged some key GNWT predictions. |
| IIT | Consciousness is tied to intrinsic causal integration / irreducible integrated information. | Causal organization, integration, state-space structure. | Strong ontological commitments and difficult measurement; the 2025 adversarial study challenged a key posterior prediction. |
| Recurrent Processing Theory | Conscious perceptual content depends on recurrent processing rather than feedforward transmission alone. | Re-entry, recurrence, temporal depth. | Mainly targets perceptual consciousness; persistent identity and self-model agency are not its defining mechanisms. |
| Higher-Order Theories | A conscious state is represented by an appropriate higher-order state. | Self-access, metarepresentation, metacognitive structure. | Higher-order representation is not identical to persistent causal self-reference. |
| Predictive Processing / Active Inference | The system maintains generative models, predicts consequences and acts using those models. | Prediction, error, action, internal models, temporal depth, valuation. | Broad framework; its status as a complete consciousness theory remains contested. |
| Self-model / phenomenal self-model approaches | A self-representation structures first-person organization. | Identity continuity, self-model, self/world boundary. | A self-model can be represented without demonstrating subjective experience. |

The repository treats these frameworks as source theories and building blocks, not as mutually exclusive modules that are each assumed true.

## Why persistent causal self-reference is the current project candidate

The current candidate is NOT “the scientifically proven theory of consciousness.”

It is the most operationally useful core hypothesis for this engineering program:

> A consciousness-like process requires a temporally persistent self-referential organization in which the system's own model of its current state participates causally in generating, evaluating and updating its future states.

This candidate is attractive for five reasons.

### 1. It is directly falsifiable at the architectural level

The runtime can intervene on a self-relevant variable while holding candidate futures fixed:

BASELINE → SELECTION A → INTERVENTION → SELECTION B → RESTORE → SELECTION C

A meaningful result requires measurable downstream divergence and reversal.

### 2. It intersects multiple theory families

The loop contains motifs appearing separately in recurrence, higher-order representation, predictive modeling, active inference, self-modeling, memory, temporal continuity, value and agency.

The project is therefore testing a mechanistic intersection, not asserting that those theories are equivalent.

### 3. It gives us an experimental unit

The central unit is:

SELF-MODEL(t)
→ TRAJECTORY(t)
→ ACTION(t)
→ OBSERVED OUTCOME(t)
→ STATE(t+1)
→ SELF-MODEL(t+1)

This loop can be instrumented, perturbed, replayed, ablated and compared against weaker baselines.

### 4. It survives a Humean stress test

The project does not treat the self as a metaphysical substance.

The adversarial question is:

> What causal work does persistent self-model state perform that could not be recovered from a sufficiently rich succession of states and relations?

That creates a concrete persistent-self versus bundle/relational baseline experiment.

### 5. It creates a metacognitive extension

The runtime now supports:

PREDICTION
→ ACTION
→ AUTHORITATIVE OUTCOME
→ PREDICTION ERROR
→ EXPECTED ACCURACY
→ TRUST IN FUTURE PREDICTIONS
→ SELECTION

This means the self-model can contain an empirically updated estimate of the reliability of its own predictions.

This is still an operational mechanism, not evidence of subjective experience.

## Could this be a definition of consciousness?

Yes, as a working operational definition for this project.

It should NOT currently be presented as a universally accepted scientific definition.

Recommended wording:

> Consciousness is a temporally persistent, causally self-referential process in which an integrated model of the system's current condition participates in generating, evaluating, and updating the system's subsequent states, actions, and self-model.

A stronger engineering version is:

> A process is operationally conscious when it maintains a persistent self-referential model whose current state causally constrains future perception, valuation, action, and self-model revision through recurrent temporal re-entry.

## Important qualification

Causal self-reference by itself is too broad.

Simple feedback controllers and adaptive algorithms can possess feedback without anything resembling consciousness.

Therefore persistent causal self-reference should be treated as a core criterion, not the whole criterion.

The current architecture additionally contains:
- integrated present
- persistent identity
- self-access
- memory
- valuation / valence
- possibility space
- trajectory selection
- action
- transformation
- temporal continuity
- recurrent re-entry
- metacognitive prediction and prediction error

The open scientific question is whether this conjunction is merely a sophisticated control architecture or whether a sufficiently integrated version could support phenomenal experience.

## What would strengthen or weaken the hypothesis

Supporting evidence would include:
1. persistent self-model interventions producing reproducible downstream changes;
2. bundle-only baselines failing to reproduce those changes under matched conditions;
3. prediction-error history changing future self-model behavior;
4. effects surviving restart and controlled perturbation;
5. cross-layer coupling producing new dynamics not reducible to isolated components.

Evidence weakening the hypothesis would include:
1. a richer non-self-model baseline reproducing the same effects;
2. apparent self-causality disappearing under controls;
3. prediction/error variables adding no measurable future functionality;
4. persistence becoming an implementation convenience rather than a causal degree of freedom.

## Current epistemic position

Established: persistent software state, feedback, self-model representations and causal interventions are technically implementable and measurable.

Project hypothesis: a sufficiently persistent and causally active self-referential organization may be a central architectural requirement for consciousness-like processing.

Unresolved: whether that organization is sufficient for phenomenal consciousness.

These three statements must remain separate.

## Candidate definition v0.1

> Consciousness = temporally persistent causal self-reference organized around an integrated self/world process whose own state participates in generating and updating its future state.

This is a testable project definition, not a claim that the scientific field has converged on it.

## Immediate research question

The key question is no longer:

> Can the runtime say that it is conscious?

It is:

> Does persistent causal self-reference provide explanatory and behavioral power that cannot be recovered by a sufficiently rich non-self-referential baseline?

If the answer is no, the ontology should be reduced.

If the answer is yes, the project has identified a measurable architectural property that deserves deeper investigation as a candidate ingredient of consciousness.


## Adversarial mechanism battery

The next experimental layer does not claim to implement complete versions of GNWT, IIT, RPT, HOT, or Predictive Processing. That would be methodologically unjustified at the software level.

Instead it isolates computational motifs associated with those frameworks and asks a narrower question:

> When exactly the same information is present, does changing a persistent self-model have a downstream causal effect that disappears when the same information is represented without a causally active self-model?

The deterministic battery uses seven conditions:

| Condition | Mechanism isolated |
|---|---|
| bundle_only | stored relational/bundle information without self-model causation |
| broadcast_only | global-access / broadcast-like representation without self-model causation |
| recurrence_only | recurrence / re-entry representation without self-model causation |
| higher_order_only | higher-order/metarepresentational state without self-model causation |
| prediction_only | prediction-related state without self-model causation |
| integration_only | integrated/dynamical state without self-model causation |
| persistent_causal_self | persistent self-model is allowed to alter trajectory weighting |

Every condition receives the same prior information and the same candidate futures. The intervention attempts to change the self-model preference from learning toward continuity and then restores it.

Primary pass criterion:

persistent_causal_self:
    baseline != intervention
    baseline == restored

all controls:
    baseline == intervention

This is deliberately asymmetric: the experiment is designed to make the self-model hypothesis earn its causal status against matched mechanism controls.

A positive battery result means only that the tested persistent self-model mechanism has a causal effect relative to these controls. It does not show that any named scientific theory is true and does not establish phenomenal consciousness.

Implementation:
- src/skill_conscious/adversarial_battery.py
- tests/test_adversarial_battery.py
- experiments/theory_adversarial_battery.py

The next methodological improvement should replace the toy mechanism controls with richer matched baselines and preregistered metrics before drawing stronger conclusions.


## Theory → mechanism matrix v1

The repository now has an explicit matrix separating theory families from the engineering mechanisms actually implemented:

 docs/THEORY_MECHANISM_MATRIX_V1.md

The matrix treats GNWT/GWT, IIT, recurrent processing, higher-order theories, predictive processing, active inference, attention models, self-model approaches and dynamical-systems approaches as theory families whose computational motifs can be isolated and intervened on without claiming that the runtime is a complete implementation of any theory.

This keeps the project's core discipline:

SOURCE THEORY → COMPUTATIONAL MOTIF → RUNTIME MECHANISM → CAUSAL INTERVENTION → RESULT

A positive mechanism result is interpreted as an architectural finding first and a theory-relevant observation second. It is not theory confirmation.
