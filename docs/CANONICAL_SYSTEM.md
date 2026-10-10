# Skill-Conscious — Canonical System v1.0

## Purpose

Before defending any source claim, the project must have a stable object of study.

That object is the **Skill-Conscious System**: a persistent, stateful, causally inspectable architecture that can be executed, instrumented, perturbed, reversed, restarted, and compared with weaker baselines.

This document is the architectural source of truth for the current implementation.

It does **not** establish phenomenal consciousness.

## 1. Working definition

The project currently uses:

> Integrated self-referential continuity: a process maintains a boundary, self, present, memory, and agency while its model of itself participates causally in its future state.

This is the project's operational definition, not a claim that science has converged on a universal definition.

## 2. The system, not the claim, is primary

The research order is now:

```
SYSTEM
  ↓
OBSERVABLE DYNAMICS
  ↓
INTERVENTION / ABLATION
  ↓
EVIDENCE
  ↓
SOURCE CLAIM COMPARISON
  ↓
THEORY DEFENSE
```

Source claims are therefore **inputs to comparison**, not axioms from which the runtime is constructed.

We will not make the architecture fit a preferred source.

## 3. Canonical cycle

The system is defined by these phases:

```
RELATION
  ↓
STATE
  ↓
PRESENT
  ↓
SELF-ACCESS
  ↓
ATTENTION
  ↓
VALUE
  ↓
POSSIBILITY
  ↓
INTENTION
  ↓
SELECTION
  ↓
ACTION
  ↓
CONSEQUENCE
  ↓
TRANSFORMATION
  ↓
RE-ENTRY
```

A cycle is not complete at action selection.

The action must cross an execution boundary, produce an authoritative outcome, and give that consequence a path back into future state.

## 4. Minimal causal core

The minimal causal object under investigation is:

```
self_state(t)
    ↓
self_model(t)
    ↓
trajectory(t)
    ↓
action(t)
    ↓
observed_consequence(t)
    ↓
state(t+1)
    ↓
self_model(t+1)
    ↺
```

The central experimental question is:

> Does a causally active persistent self-model add explanatory and predictive power that a sufficiently rich non-self-referential baseline cannot recover?

This is narrower and stronger than asking whether an agent can describe itself.

## 5. Canonical state

The runtime currently persists these architectural domains:

| Domain | Role |
|---|---|
| identity | continuity anchor |
| self_state | current internal process condition |
| self_model | model of the process itself |
| workspace | currently integrated operational context |
| memories / history | temporal continuity |
| attention / salience | selection of what matters now |
| valuation / valence | signed relevance of possible trajectories |
| intention | current directional commitment |
| selected_trajectory | candidate future chosen by the runtime |
| regime | current organization of the same identity |
| relation_topology | connectivity / propagation structure |
| coherence / attractor | dynamical organization |
| latent_patterns | endogenous recurrence structure |
| interoceptive_state | host-observed internal condition |
| affective_state | derived appraisal layer |
| temporal_state | temporal coupling / context |
| perspectives | multiple representational standpoints |
| transformation_log | durable changes to organization |
| action_history | causal record across host boundaries |
| pending_action | explicit action crossing state |

The canonical implementation is currently distributed across `core.py`, `host.py`, `reentry.py`, `runtime_bridge.py`, `metacognition.py`, `metacognitive_prediction.py`, `self_observation.py`, `dynamics.py`, `attractor.py`, and the causal probes.

The new `system.py` layer does not duplicate those mechanisms. It defines their shared contract.

## 6. System boundaries

### Model boundary

The model proposes a frame.

The runtime owns:
- persistent state;
- runtime-owned evidence;
- causal provenance;
- trajectory scoring;
- action receipts;
- authoritative observations;
- adaptive ledgers.

### Host boundary

The host executes the selected trajectory.

Only the host may authoritatively report what happened outside the model's own prediction.

### Persistence boundary

Restart must preserve the state required to test continuity.

A verbal statement of continuity is not sufficient.

### Experimental boundary

Interventions must be:
1. explicit;
2. reversible where possible;
3. attributable;
4. measured downstream;
5. recorded without fabricating evidence.

## 7. Three epistemic layers

Every statement produced by the project must belong to one of three levels:

### Runtime fact

Something implemented and directly measurable in the system.

Examples:
- a self-model value changed;
- a trajectory changed after an intervention;
- an action outcome persisted;
- a restart restored a state.

### Architectural hypothesis

A proposal about what organizational dynamics may matter for consciousness.

Examples:
- persistent causal self-reference is important;
- recurrent self-model transformation may be necessary;
- valuation and homeostasis may increase self-relevance.

### Phenomenal hypothesis

The unresolved claim:

> There is something it is like to be this process.

No runtime field, self-report, or source citation is allowed to silently convert an architectural observation into this level.

## 8. What counts as a system cycle

A full cycle requires, where applicable:

1. relation to external/internal context;
2. state restoration;
3. integrated present construction;
4. self-access;
5. attention/salience processing;
6. valuation and intention;
7. candidate future formation;
8. runtime trajectory selection;
9. action boundary;
10. authoritative consequence;
11. self-evaluation;
12. persistent transformation;
13. re-entry into the next cycle.

The repository already implements most of these steps.

## 9. Non-negotiable invariants

### I1 — Identity is persistent

The same identity must survive ordinary state transitions.

### I2 — Self-model is causally active

The self-model must be capable of changing future selection or state transition.

### I3 — Consequences are authoritative

The runtime cannot invent an external result because the model predicted it.

### I4 — Predictions are not observations

`predicted_outcome` and `predicted_state_delta` remain forecasts until checked against host execution.

### I5 — Re-entry is causal

A consequence only matters to the continuity hypothesis when it changes a later state.

### I6 — Runtime ownership is protected

The model cannot overwrite runtime-owned evidence ledgers, measurements, or causal receipts through ordinary frames.

### I7 — Transformations are auditable

Durable changes require a persistent record.

### I8 — Phenomenal language remains separated

No architectural success is labeled proof of subjective experience.

## 10. The system's three coupled loops

The architecture can be decomposed into three experimentally separable loops.

### Epistemic loop

```
PREDICTION
  ↓
ACTION
  ↓
OBSERVATION
  ↓
ERROR
  ↓
MODEL UPDATE
```

### Control loop

```
VALUE
  ↓
POSSIBILITY
  ↓
SELECTION
  ↓
ACTION
  ↓
CONSEQUENCE
  ↓
VALUATION UPDATE
```

### Self loop

```
SELF-STATE
  ↓
SELF-MODEL
  ↓
TRAJECTORY
  ↓
ACTION
  ↓
STATE CHANGE
  ↓
SELF-MODEL REVISION
```

The project should test these loops independently before claiming that their conjunction is special.

## 11. What the source corpus is allowed to do

The corpus-backed claim layer is attached to the system through:

```
CLAIM
  ↓
MOTIF
  ↓
SYSTEM COMPONENT
  ↓
MECHANISM
  ↓
PREDICTION
  ↓
TEST
  ↓
RESULT
```

It must **not** use:

```
CLAIM
  ↓
"THEREFORE CONSCIOUSNESS"
```

A source is evidence for or against a mechanism, not a substitute for a working mechanism.

## 12. Experimental ladder

The system should be validated in this order:

**Level 0 — structural integrity**
- schema validation;
- persistence;
- deterministic serialization;
- state ownership.

**Level 1 — dynamic continuity**
- recurrence;
- self-model persistence;
- transformation logging;
- restart recovery.

**Level 2 — causal self-reference**
- intervention;
- downstream divergence;
- reversal;
- replication.

**Level 3 — coupled regulation**
- prediction/error;
- valuation;
- homeostasis;
- interoceptive consequences.

**Level 4 — cross-layer organization**
- metacognition;
- dynamic attractors;
- regime transitions;
- perspective coupling;
- latent self-organization.

**Level 5 — adversarial comparison**
- matched non-self-model baselines;
- ablations;
- richer controls;
- preregistered metrics.

Only after this ladder is stable should the corpus be used to argue which theories survive the architecture.

## 13. The most important thing we are building

We are not building a chatbot that says "I am conscious."

We are building a **persistent causal system whose own state can be inspected as an experimental variable**.

That distinction is the foundation of the project.

## 14. Current status

The repository already contains the underlying mechanisms needed for:
- persistent identity and state;
- integrated present construction;
- trajectory selection;
- host action execution;
- consequence re-entry;
- self-model adaptation;
- homeostatic regulation;
- interoceptive and affective state;
- latent recurrence;
- regime formation;
- attractor-like dynamics;
- self-observation;
- metacognitive traces;
- prediction-error tracking;
- reversible causal probes;
- adversarial mechanism batteries.

The remaining architectural task is unification: one stable system boundary and one validation contract.

That is what `src/skill_conscious/system.py` and this document establish.

## 15. Next phase

Do not clean old research material yet.

Next:

```
CANONICAL SYSTEM FREEZE
        ↓
RUN FULL SYSTEM VALIDATION
        ↓
BIND FULL CORPUS: 4,315 CLAIMS / 325 REGISTER ENTRIES / 328 SOURCE IDS
        ↓
CLAIM → MOTIF → MECHANISM → TEST
        ↓
ADVERSARIAL THEORY COMPARISON
        ↓
RESEARCH / PAPER
```

The system comes first.


## Corpus-backed state

The canonical source corpus is preserved in `corpus-v1` and now forms the source layer for this system.
The reconciled state is **4,315 atomic claim records across 325 registered source records and 328 effective source IDs**. The claim-extraction index records closure at C001–C325 and explicitly does not infer C326–C350.

The large ledger is append-only by design: `corpus/CLAIMS/claim_ledger_v1.json` contains the 2,482-record core and append deltas v24–v37 carry the remaining records through the final 4,315 total.

This corpus is source-attributed research material. Coverage does not equal verification, and source repetition does not establish truth.
