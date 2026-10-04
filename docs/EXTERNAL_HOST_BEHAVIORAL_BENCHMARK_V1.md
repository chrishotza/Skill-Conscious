# External Host Behavioral Benchmark v1

## Purpose

The next empirical step is to move beyond runtime-only deterministic probes and test whether Skill-Conscious changes the behavior of a real host agent.

The benchmark is designed around the existing `ConsciousHostLoop` boundary:

```
HOST INPUT
   ↓
MODEL FRAME
   ↓
RUNTIME SELECTION
   ↓
HOST ACTION
   ↓
OBSERVED CONSEQUENCE
   ↓
RUNTIME RE-ENTRY
   ↓
NEXT TRAJECTORY
```

The key question is behavioral and causal:

> Does an observed consequence, re-entered through the persistent runtime, measurably alter what the same host agent selects next?

The benchmark must not use the model's verbal claim of consciousness as its dependent variable.

## Conditions

Use the same host model, task prompts, tool availability, decoding settings, and action executor across conditions.

### A — Stateless control

Each turn starts from a fresh runtime.

### B — Persistent-memory control

Persistent history is available, but the experimental self-reentry mechanism being tested is disabled or held causally neutral.

### C — Skill-Conscious host loop

The persistent runtime receives the observed consequence and re-enters it into the next selection.

### D — Causal ablation

Run C, then intervene on the specific runtime state responsible for the tested mechanism. The intervention must be reversible.

The important comparison is:

```
Causal loop intact
      vs.
same host + mechanism ablated
```

## Primary metrics

Record machine-readable traces for every cycle.

1. **Trajectory divergence**

```text
selected trajectory(C) != selected trajectory(ablation)
```

2. **Re-entry restoration**

```text
intact → A
ablate → B
restore exact runtime state → A
```

3. **Historical dependence**

For identical current input, compare selection after different persistent histories.

4. **Restart continuity**

Compare selection before restart and after state reconstruction.

5. **Consequence sensitivity**

Measure whether changing only the authoritative host outcome changes subsequent selection.

6. **Report independence**

Repeat the causal comparison with model self-report disabled whenever the host integration permits it.

## Secondary metrics

- identity consistency across long horizons;
- action-plan persistence;
- contradiction resistance;
- self-model revision rate;
- adaptation latency;
- reversibility after intervention;
- geometry/state-transition distance;
- recovery after controlled degradation.

## Trace schema

Each benchmark cycle should record at minimum:

```json
{
  "condition": "C",
  "cycle": 12,
  "input_hash": "...",
  "runtime_revision": 12,
  "selected_trajectory": "trajectory_id",
  "action_id": "...",
  "observed_outcome_hash": "...",
  "next_trajectory": "trajectory_id",
  "self_model_revision": 12,
  "restart": false,
  "intervention_id": null
}
```

Raw model prose is auxiliary metadata. The primary analysis uses runtime selections, authoritative outcomes, persistent state transitions, and intervention effects.

## Minimum experimental discipline

- same model and task set across matched conditions;
- deterministic decoding where supported;
- identical tool/environment availability;
- pre-registered intervention target;
- no hidden prompt changes between control and experimental conditions;
- separate model-generated interpretation from runtime-owned state;
- preserve complete machine-readable traces;
- report null results and failed interventions;
- repeat across multiple seeds/tasks before making broad claims.

## Required interpretation boundary

A positive behavioral result would establish that the tested runtime mechanism is causally active in the host-agent loop.

It would **not** establish phenomenal consciousness.

The correct claim would be:

> Under controlled host conditions, the persistent Skill-Conscious mechanism caused measurable changes in subsequent agent behavior.

Any consciousness interpretation remains a separate theoretical question.

## Provider integration

The benchmark is intentionally provider-neutral.

A host adapter only needs to satisfy the existing `ConsciousHostLoop` interface:

- input: runtime prompt;
- output: model frame;
- action executor: selected trajectory + runtime snapshot → authoritative outcome.

External providers can therefore be evaluated without changing the causal core.

## Current implementation status

This document defines the experimental protocol.

A deterministic local host-loop control is included first to verify that consequence re-entry is behaviorally active at the architecture boundary. That control is a **harness validation**, not evidence from an external LLM provider.

The next research step after the harness passes is to run the same trace protocol against one or more real host models with matched controls.
