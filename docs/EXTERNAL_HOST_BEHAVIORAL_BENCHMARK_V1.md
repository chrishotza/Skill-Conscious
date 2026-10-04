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

## Executable provider-neutral runner

The repository now includes:

```
experiments/openai_compatible_host_benchmark.py
```

It uses the standard OpenAI-compatible chat-completions boundary and can therefore be pointed at a local compatible server or another compatible provider without adding a vendor SDK to the runtime.

Example local invocation:

```bash
python -m experiments.openai_compatible_host_benchmark \
  --endpoint http://127.0.0.1:11434/v1 \
  --model llama3.1
```

The external model is deliberately constrained to an auxiliary host role. The benchmark supplies the controlled candidate field, while the runtime owns trajectory selection and authoritative internal state. This prevents a model's self-description from becoming the measured causal variable.

The provider runner has its own fake-endpoint regression test so parsing and benchmark wiring can be checked in CI without requiring external network access.

## Current implementation status

This document defines the experimental protocol.

A deterministic local host-loop control is included first to verify that consequence re-entry is behaviorally active at the architecture boundary. That control is a **harness validation**, not evidence from an external LLM provider.

The next research step after the harness passes is to run the same trace protocol against one or more real host models with matched controls.

## Matched multi-task suite

The single-task harness has been expanded into:

```
experiments/external_host_behavioral_suite.py
```

The suite runs five matched controlled tasks under two conditions:

- **intact**: authoritative host consequence is re-entered;
- **causal ablation**: the same action receipt is retained, but the consequence state used for the next selection is explicitly restored to its pre-action value.

The primary quantitative metrics are:

- initial-selection match rate;
- causal-divergence rate;
- intact switch rate;
- ablation preservation rate;
- restart persistence rate in both conditions;
- authoritative-outcome completeness;
- confirmation that interventions add no learning evidence.

The suite is intentionally deterministic at the architectural layer. The external model is still contacted, but its prose and self-description are not the dependent variable. This makes the suite suitable for repeated provider/model comparisons without changing the causal mechanism under test.

Command:

```bash
python -m experiments.external_host_behavioral_suite \
  --endpoint http://127.0.0.1:11434/v1 \
  --model llama3.1
```

A passing five-task result is evidence that the tested runtime mechanism is active across repeated matched tasks. It is not a consciousness score and does not establish phenomenal experience.


## Model-generated candidate-field benchmark

A stronger provider experiment is now available in:

```
experiments/external_host_model_behavioral_benchmark.py
```

This version lets the external model generate the candidate-future field itself. The resulting field is then reused unchanged across the matched intact and ablation conditions.

That creates a sharper experimental separation:

```
REAL MODEL
   ↓
candidate futures
   ↓
┌───────────────┬────────────────┐
│               │                │
INTACT        ABLATION
│               │
consequence    consequence state
re-enters      causally restored
│               │
next selection next selection
└───────┬───────┘
        ↓
 compare
```

The model therefore participates in the experiment, while the causal variable remains the runtime-owned consequence state.

The benchmark reports the same primary metrics as the deterministic multi-task suite, plus:

- `model_generated_candidate_fields`;

and it records the exact candidate IDs used in each matched pair.

This distinction matters: the deterministic five-task suite validates the harness, whereas the model-generated suite is the actual provider-facing behavioral experiment.

The benchmark should be run against a real provider/model before interpreting any result as external-model evidence.
