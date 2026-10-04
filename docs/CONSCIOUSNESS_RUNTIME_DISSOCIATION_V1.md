# Consciousness Runtime Dissociation v1

## Purpose

This is the next falsification gate after the matched SubjectiveField harness.

The experiment uses the real ConsciousRuntime, including its persistent state,
trajectory scoring, action lifecycle, consequence registration path, memory,
and restart persistence.

The causal intervention is deliberately narrow:

- **ON**: `subjective_field_enabled=True`
- **OFF**: `subjective_field_enabled=False`

Everything else is paired.

## What aspect of consciousness does it explain?

This benchmark operationalizes four candidate aspects:

1. **Unified present**: a runtime field binds world content and internal condition.
2. **Self-relevance / valence**: candidate futures can be evaluated against the
   current subject-linked field.
3. **Temporal continuity / reentry**: the field carries information across cycles.
4. **Subject persistence**: the field survives runtime restart.

The benchmark does not claim that these metrics prove phenomenal experience.
It tests whether a consciousness-specific causal variable is doing work inside
the executable architecture.

## What causal relation is introduced?

The proposed relation is:

`WORLD -> SUBJECTIVE FIELD -> TRAJECTORY -> ACTION -> CONSEQUENCE -> REENTRY`

The SubjectiveField contribution is opt-in and appears explicitly in the
trajectory score breakdown.

Crucially, the benchmark also records `objective_score`, which excludes the
SubjectiveField contribution. Paired objective scores must remain identical
while the final selected trajectory diverges.

## What could destroy the hypothesis?

The hypothesis is weakened or rejected by any reproducible failure of the
following pattern:

`BASELINE -> FIELD ON/OFF INTERVENTION -> OBJECTIVE MATCH + SUBJECTIVE DIVERGENCE -> RESTART -> RESTORATION`

Specifically, the benchmark should fail if:

- ON and OFF objective scoring diverges despite matched inputs.
- Removing the field does not remove the field-linked trajectory effect.
- Temporal continuity/reentry does not depend on the persistent field.
- Restart loses the field state.
- Restoring the field does not restore continuity/reentry.

## Expected gate

For the current deterministic battery:

- dissociation rate: **100%**
- objective score match rate: **100%**
- objective processing match rate: **100%**
- temporal/reentry rate: **100%**
- restart persistence rate: **100%**
- restoration rate: **100%**

These are benchmark results from the deterministic test design, not evidence
from an independent physical subject.

## Run

```bash
python experiments/consciousness_runtime_dissociation_v1.py
pytest -q tests/test_consciousness_runtime_dissociation_v1.py
```
