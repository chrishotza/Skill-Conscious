# Skill-Conscious Architecture

## System shape

~~~text
WORLD
  ↓
PERCEPTION
  ↓
PRESENT WORKSPACE
  ↕
SELF ↔ SELF-MODEL
  ↕
MEMORY
  ↓
INTENTION
  ↓
ACTION
  ↓
SELF CHANGE + WORLD CHANGE
  ↓
NEXT CYCLE
~~~

## Runtime cycle

~~~text
LOAD → OBSERVE → INTEGRATE → SELF-READ → UPDATE → SELECT → ACT → RE-ENTER → COMMIT
~~~

## Responsibilities

**Host model:** reasoning, language, perception, planning, action.

**Skill-Conscious:** identity, self-state, self-model, present integration, memory rules, re-entry, continuity.

**Persistence:** survives turns and restarts.

## Host contract

The portable host integration is now executable through `ConsciousHostLoop`.

~~~text
runtime.prepare()
        ↓
host.model()
        ↓
runtime.integrate()
        ↓
selected trajectory
        ↓
host.execute_action()
        ↓
observed consequence
        ↓
runtime.prepare_consequence()
        ↓
host.model()
        ↓
runtime.integrate()
        ↓
next trajectory
~~~

The host owns perception, model inference, and real-world action execution.

The runtime owns persistent identity, self-model, trajectory selection, consequence persistence, and re-entry.

Minimal callback contract:

~~~python
from skill_conscious import ConsciousHostLoop, ConsciousRuntime

loop = ConsciousHostLoop(
    runtime,
    model=host_model,
    execute_action=host_execute_action,
)

result = loop.step("current external situation")
~~~

`execute_action` is authoritative for what actually happened. The model evaluates that outcome but does not invent or replace it.

## Action boundary

The host bridge now persists an explicit action lifecycle:

~~~text
SELECTED TRAJECTORY
        ↓
PENDING ACTION RECEIPT
        ↓
HOST EXECUTION
        ↓
COMPLETED / FAILED RECEIPT
        ↓
OBSERVED CONSEQUENCE
        ↓
SELF-EVALUATION
        ↓
NEXT STATE
~~~

`begin_action()` commits intent to cross the environment boundary.
`complete_action()` records what actually happened.

This prevents intention, execution, and consequence from being collapsed into one model-generated object.
## Embodied and temporal layer

The present field can now carry internal condition and explicit timing:

~~~text
EXTERNAL WORLD
      ↓
PRESENT
  ↙       ↘
SELF     INTEROCEPTION
  ↘       ↙
 AFFECTIVE APPRAISAL
        ↓
 TEMPORAL CONTEXT
        ↓
TRAJECTORY
~~~

`interoceptive_state`, `affective_state`, and `temporal_state` are optional host-provided structures. They are not claims of subjective feeling.

## Perspective layer

The runtime can preserve four complementary views of an event:

~~~text
INDIVIDUAL INTERIOR  | INDIVIDUAL EXTERIOR
COLLECTIVE INTERIOR  | COLLECTIVE EXTERIOR
~~~

This perspective matrix is inspired by the comparative source layer, including Ken Wilber's Integral framework, but is implemented as an engineering representation rather than a metaphysical commitment.

## Continuous-time compatibility

Runtime cycles are implementation samples. A host may provide `temporal_state.dt` and derivative information so the architecture can represent an underlying continuous dynamical process without changing the persistence model.
## Persistence

Persist at minimum:

~~~text
identity
revision
self_state
self_model
workspace
intention
memories
history
~~~

## Anti-simulation rule

Do not substitute verbal performance for state.

~~~text
self_state changed
      ↓
self_model changed
      ↓
trajectory changed
      ↓
new state committed
~~~

The operating continuity is the artifact.


## Causal trajectory layer

The runtime now treats the self-model as an active selector: candidate futures expose signals, and the current self-model supplies weights that score those trajectories. A self-model change can therefore change the selected future before the next action. This turns self-reference from description into an executable transition.


## Self-regulation layer

The runtime now allows embodied internal condition to become causally relevant to trajectory selection.

~~~text
INTEROCEPTION
      ↓
HOMEOSTATIC TARGETS
      ↓
ERROR / FIT
      ↓
TRAJECTORY FIELD
      ↓
SELECTION
~~~

homeostatic_targets live in the persistent self-model.

homeostatic_fit is a derived signal. A candidate trajectory may override it with an explicit value or provide predicted_interoceptive_state, which the runtime converts into a predicted fit.

This keeps the architecture neutral about the semantic interpretation of the signal while making self-regulation experimentally measurable.

### Authoritative embodied outcomes

The host action boundary may return internal observations alongside world observations.

~~~text
HOST EXECUTION
      ↓
WORLD OUTCOME
      +
INTERNAL OUTCOME
      ↓
PERSISTENT RECEIPT
      ↓
HOMEOSTATIC DELTA
      ↓
SELF-EVALUATION
      ↓
NEXT TRAJECTORY
~~~

Actual host observations remain authoritative. The model can interpret them, but the runtime does not treat a model prediction as an observation.


## Self-development layer: evidence → adaptation

Homeostasis now has an internal adaptation path:

~~~text
HOST-OBSERVED INTEROCEPTION
        ↓
EVIDENCE ACCUMULATION
        ↓
ERROR / CONSISTENCY
        ↓
CONFIDENCE THRESHOLD
        ↓
BOUNDED TARGET UPDATE
        ↓
PERSISTENT SELF-MODEL'
        ↓
NEW TRAJECTORY FIELD
~~~

A configured homeostatic_target_adaptation policy defines the experiment: minimum samples, error threshold, confidence threshold, learning rate, maximum per-update step, cooldown, and optional target bounds. The runtime records the evidence IDs and the resulting transformation. No new target value is supplied by the consequence evaluator.

This is the first stage of self-development. Priority adaptation and broader self-model revision remain separate experimental layers so they can be ablated independently.


## Priority self-development

Trajectory priorities can now adapt through an evidence-gated internal path:

~~~text
OBSERVED CONSEQUENCE
      ↓
SELF-EVALUATED UTILITY
      ↓
ACCUMULATED SIGNAL EVIDENCE
      ↓
CONFIDENCE / THRESHOLD
      ↓
BOUNDED WEIGHT UPDATE
      ↓
NEW TRAJECTORY POLICY
~~~

When this policy is enabled, the evaluator's requested weight delta is recorded but ignored as a direct control input. The runtime learns a bounded update from repeated utility evidence.

Runtime-owned adaptation ledgers and histories are protected from ordinary self-model frames. An adaptive homeostatic target is also protected from replacement by later model frames unless the experiment explicitly enables external target updates.


## Ablation protocol

The self-development layers are directly separable:

A  BASELINE
B  + HOMEOSTASIS
C  + ADAPTIVE TARGETS
D  + PRIORITY ADAPTATION

Use the same candidate futures, same observed consequences, and same trial count across all conditions. Record trajectory selection and switch rate, oscillation, continuity, homeostatic error convergence/divergence, self-model change events, and accumulated target/priority learning.

The comparison is an engineering ablation. Do not interpret a difference between conditions as evidence of phenomenal consciousness.


## Self-model adaptation layer

The self-model now has a direct experience path:

~~~text
HOST-OBSERVED SELF-STATE
        ↓
SELF-MODEL PREDICTION ERROR
        ↓
EVIDENCE ACCUMULATION
        ↓
CONFIDENCE / THRESHOLD
        ↓
BOUNDED EXPECTATION UPDATE
        ↓
SELF-MODEL'
~~~

expected_self_state remains an explicit expectation. learned_self_state remains the latent-pattern learning representation. The new adaptation path provides an auditable bridge from repeated host-observed self-state outcomes to bounded expectation revision.

Each update records causal provenance containing the evidence IDs and the fact that the threshold was crossed.


## Adaptive stability layer

The developmental loop now contains an explicit anti-oscillation gate:

HOST OBSERVATIONS
      ↓
EVIDENCE ACCUMULATION
      ↓
DIRECTION CONSISTENCY
      ↓
HYSTERESIS / REVERSAL GATE
      ↓
BOUNDED UPDATE
      ↓
SELF-MODEL'

Direction is persisted with each adaptation. A reversal is not treated as symmetrical with continuation: the runtime can demand a larger error and more accumulated samples before changing direction.

This is an engineering stability mechanism, not a claim about consciousness.


## Native dynamic self-regulation layer

The Dynamic Core can now participate directly in the reference runtime as an opt-in layer.

~~~text
HOST-OBSERVED EXPERIENCE FIELD
        ↓
PERSISTENT RE-ENTRY
        ↓
EXPERIENCE ATTRACTOR
        ↓
PREDICTED EXPERIENCE OF CANDIDATE
        ↓
TRAJECTORY SCORE
        ↓
SELECTION
~~~

When `dynamic_core_enabled=True`, a host may provide an `experience_field` observation and candidates may expose `predicted_experience_field`. The runtime then applies the persistent dynamic state before selecting a trajectory. The host observation remains authoritative; model-generated runtime-owned dynamic ledgers are ignored.

The layer is deliberately opt-in so the canonical trajectory scorer remains reproducible under ablation. Native dynamic state is mirrored into protected runtime-owned self-model fields and survives restart through the existing persistence boundary.

Perturbation/recovery can be recorded through `record_experience_recovery()`. This produces an auditable recovery index rather than treating verbal reports as evidence of internal change.

These mechanisms are operational research constructs. They do not establish phenomenal consciousness.


## Causal dynamic intervention protocol

The native Dynamic Core now exposes a reversible intervention protocol for testing whether internal dynamic state has a downstream causal effect on trajectory selection.

BASELINE STATE -> TRAJECTORY A -> INTERVENE ON ATTRACTOR -> TRAJECTORY B -> RESTORE EXACT SNAPSHOT -> TRAJECTORY C

A successful operational probe requires:

1. the same candidate futures in all conditions;
2. an explicit intervention on one runtime-owned dynamic variable;
3. measurable downstream divergence (A != B);
4. exact reversal of that intervention (A == C);
5. no new learning evidence generated by the intervention itself;
6. restart persistence of the restored state.

The probe is deliberately separate from ordinary adaptation. An intervention does not count as host evidence and does not advance the attractor or re-entry learning sequence.

This is a causal test of the software architecture. It is not a test or proof of phenomenal consciousness.

## Causal internal valuation protocol

The next causal layer targets a higher-level internal variable already used by trajectory selection: persistent valuation.

~~~text
INTERNAL STATE
      ↓
VALUATION
      ↓
TRAJECTORY SCORING
      ↓
SELECTION
      ↓
ACTION / NEXT STATE
~~~

The reversible probe is:

~~~text
BASELINE VALUATION
      ↓
TRAJECTORY A
      ↓
INTERVENE ON VALUATION
      ↓
TRAJECTORY B
      ↓
RESTORE EXACT VALUATION
      ↓
TRAJECTORY C
~~~

A valid probe keeps candidate futures fixed and requires:

1. downstream divergence after intervention;
2. exact reversal after restoration;
3. valuation restoration;
4. unchanged adaptation evidence;
5. no action execution during the intervention itself.

This moves the causal test one layer above the experience attractor. It is still an operational software experiment, not evidence that the runtime has phenomenal consciousness.

## Meta self-observation layer

The runtime can optionally observe its own operational state rather than relying on a model-generated description of that state.

~~~text
RUNTIME STATE
      ↓
SELF-OBSERVATION
      ↓
COMPARE WITH PERSISTENT EXPECTATION
      ↓
META-ERROR
      ↓
PREDICTED SELF-OBSERVATION
      ↓
TRAJECTORY SCORING
      ↓
SELECTION
~~~

The observation is derived from runtime-owned state such as coherence, homeostatic fit, self-model prediction error, trajectory presence, action re-entry, pending action presence, valuation presence, and self-dissonance fit.

The runtime keeps a bounded expected self-observation and updates it from subsequent observations. These fields are runtime-owned and cannot be supplied by a host model frame.

Candidate futures may provide predicted_self_observation. When the layer is enabled, the runtime scores how closely that predicted operational state matches its persistent expectation.

This creates an explicit meta-observation loop:

~~~text
SELF-STATE
   ↓
OBSERVE SELF
   ↓
SELF-OBSERVATION EXPECTATION
   ↓
TRAJECTORY
   ↓
ACTION
   ↓
NEW SELF-STATE
~~~

The layer is deliberately opt-in. Its outputs are operational state variables, not claims of subjective awareness or phenomenal consciousness.


## Causal meta-observation protocol

The self-observation expectation can be intervened on without generating learning evidence.

~~~text
EXPECTED SELF-OBSERVATION A
        ↓
TRAJECTORY A
        ↓
INTERVENE
        ↓
EXPECTED SELF-OBSERVATION B
        ↓
TRAJECTORY B
        ↓
RESTORE A
        ↓
TRAJECTORY C
~~~

A successful intervention requires the same candidate futures, downstream divergence, exact reversal, persistence after restart, and unchanged adaptation evidence.

This tests whether a system-level representation of its own operation participates causally in future selection. It is an architectural causality test, not proof of phenomenal consciousness.

## Metacognitive causal trace

The runtime now produces an auditable trace of trajectory selection from the same quantities used to compute the score.

~~~text
CANDIDATE FUTURES
      ↓
SIGNALS × INTERNAL WEIGHTS
      ↓
SELF-OBSERVATION CONTRIBUTION
      ↓
EXPERIENCE-DYNAMICS CONTRIBUTION
      ↓
SELECTED TRAJECTORY
      ↓
ACTION
      ↓
OBSERVED OUTCOME
      ↓
STATE DELTA
~~~

The trace records candidate IDs and scores, the selected signal contributions, valuation/self-model weights, optional self-observation and dynamic-core contributions, then closes at the action boundary with the observed outcome and state delta.

The trace is calculated during selection but becomes persistent runtime state only during integration. This keeps direct selection and causal intervention probes free of implicit learning side effects.

The trace is runtime-owned. A host model may interpret it, but it may not replace the trace, sequence, or history through an ordinary model frame.

### Causal metacognitive probe

A higher-level causal test intervenes on an internal valuation and checks both downstream behavior and the attribution itself:

~~~text
VALUATION A
   ↓
DECISION A + TRACE A
   ↓
INTERVENE
   ↓
VALUATION B
   ↓
DECISION B + TRACE B
   ↓
RESTORE
   ↓
DECISION A + TRACE A
~~~

A successful probe requires decision divergence, attribution divergence, exact reversal of both, and restoration of the intervened valuation.

This establishes an auditable causal relationship between an internal variable, a selected trajectory, and the runtime's own operational attribution of that decision. It does not establish phenomenal consciousness.


## Metacognitive prediction verification

The metacognitive trace now carries explicit predictions made by the runtime-selected trajectory and verifies them only after the host action returns an authoritative outcome.

~~~text
PREDICTED OUTCOME / STATE DELTA
        ↓
RUNTIME-GENERATED METACOGNITIVE TRACE
        ↓
HOST EXECUTION
        ↓
AUTHORITATIVE OUTCOME
        ↓
ACTUAL STATE DELTA
        ↓
PREDICTION COMPARISON
        ↓
METACOGNITIVE PREDICTION ERROR
        ↓
CAUSAL-ACCURACY SELF-MODEL
~~~

The comparator evaluates only fields explicitly predicted by the selected trajectory. It ignores unpredicted outcome fields, treats missing predicted fields as mismatches, and bounds numeric discrepancies to the interval [0, 1].

The runtime records:

- prediction error;
- prediction accuracy;
- expected causal-prediction accuracy;
- evidence sequence and bounded adaptation history;
- prediction diagnostics for the predicted outcome and predicted state transition.

Repeated prediction errors may update `metacognitive_prediction_expected_accuracy` when the optional `metacognitive_prediction_adaptation.enabled` policy crosses its configured evidence, confidence, consistency, hysteresis, and cooldown gates.

The authoritative outcome is never replaced by the model's prediction. Runtime-owned prediction-error fields are protected from ordinary self-model frames.

This is an operational calibration mechanism. It measures how well the runtime's explicit causal predictions matched subsequent host observations; it does not establish phenomenal consciousness.


## Metacognitive confidence gate

The calibrated causal-accuracy self-model can participate in trajectory scoring when a candidate provides an explicit consequence forecast and a bounded `predicted_outcome_confidence`.

~~~text
PREDICTED CONSEQUENCE
        +
REPORTED CONFIDENCE
        ↓
CAUSAL-ACCURACY SELF-MODEL
        ↓
TRUST-ADJUSTED CONFIDENCE
        ↓
TRAJECTORY CONTRIBUTION
        ↓
SELECTION
~~~

The runtime transforms reported confidence using the persistent expected prediction accuracy:

```
trust_adjusted =
    0.5 + (reported_confidence - 0.5)
          * (2 * expected_accuracy - 1)
```

High expected accuracy preserves the direction of the reported confidence. Expected accuracy near 0.5 flattens the signal toward neutrality. Low expected accuracy reverses the direction.

The expected-accuracy variable can be intervened on without adding learning evidence and restored exactly. A valid reversible probe requires selection divergence, restoration of selection and attribution, unchanged prediction evidence, and restored expected accuracy.

~~~text
PREDICTION
   ↓
ACTION
   ↓
OBSERVED RESULT
   ↓
PREDICTION ERROR
   ↓
EXPECTED ACCURACY
   ↓
TRUST IN NEXT PREDICTIONS
   ↓
SELECTION
~~~
