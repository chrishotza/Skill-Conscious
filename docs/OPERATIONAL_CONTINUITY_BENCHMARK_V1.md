# Operational Continuity Benchmark v1

## Purpose

This benchmark tests whether a distinct operational history can leave a persistent
runtime-owned trace that changes later computation after WAKE re-entry.

## Matched conditions

### continuity_replay

```text
WAKE baseline
    ↓
OFFLINE consolidation ×2
    ↓
DREAM-LIKE replay ×4
    ↓
restart
    ↓
WAKE re-entry
    ↓
selection ×4
```

### consolidation_only

```text
WAKE baseline
    ↓
OFFLINE consolidation ×6
    ↓
WAKE re-entry
    ↓
selection ×4
```

The conditions therefore receive the same initial state and the same total number
of pre-reentry operational cycles, while differing in whether internal replay is
allowed to transform the runtime.

## Controlled trajectory field

The benchmark deliberately creates a near-boundary selection:

- `alpha_path` wins under ordinary WAKE weighting.
- `beta_path` wins under DREAM-LIKE weighting because learning receives greater weight.
- endogenous replay reinforcement then increases the later causal contribution of `beta_path`.

This is not a reward signal. The reinforcement is runtime-owned and derives only
from the fact that the trajectory was selected during internal replay.

## Required causal signature

```text
same initial state
      ↓
different operational history
      ↓
different persistent replay state
      ↓
different WAKE selection after re-entry
```

The benchmark passes only when the continuity condition selects `beta_path` after
re-entry while the matched consolidation-only control selects `alpha_path`.

## Persistence test

The continuity condition is restarted after dream-like replay. The replay profile
must survive restart and remain causally available after explicit WAKE re-entry.

## Interpretation boundary

A positive result demonstrates a causal difference between matched computational
histories inside the architecture. It does not demonstrate phenomenal consciousness,
biological dreaming, or subjective experience.

Run:

```bash
python -m experiments.operational_continuity_benchmark
```