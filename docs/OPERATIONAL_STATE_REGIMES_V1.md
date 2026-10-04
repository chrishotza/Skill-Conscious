# Operational State Regimes v1

## Purpose

Skill-Conscious already contains a cognitive regime label such as `baseline`,
`exploration`, or `integration`. This layer adds a separate **operational
state** describing how the runtime is computationally coupled to the world.

The three states are:

- **WAKE** — external input is accepted; candidate futures can be generated;
  selected trajectories may cross the host action boundary.
- **OFFLINE** — external input is unavailable; no trajectory is selected and
  no action can execute; persistent memory/history can undergo consolidation.
- **DREAM-LIKE** — external input is unavailable; persistent material is replayed
  internally; candidate futures can be evaluated and a trajectory can be
  selected internally, but it cannot cross the action boundary.

This is an engineering mechanism, not evidence that a system has biological
sleep, dreams, or phenomenal experience.

## Architectural role

```text
WAKE
  WORLD → PRESENT → POSSIBILITY → TRAJECTORY → ACTION
    ↓
OFFLINE
  PERSISTENT MEMORY / HISTORY → CONSOLIDATION
    ↓
DREAM-LIKE
  CONSOLIDATED STATE → INTERNAL REPLAY → POSSIBILITY → TRAJECTORY
    ↓
WAKE RE-ENTRY
  INTERNAL CHANGE → NEW WORLD INPUT → RE-ENTRY
```

The existing `regime` field remains the cognitive/selection regime. The new
`operational_state` is orthogonal and persistent.

## Runtime invariants

1. Operational mode is runtime-owned and persisted across restart.
2. OFFLINE and DREAM-LIKE reject external world input.
3. OFFLINE cannot generate an action trajectory.
4. DREAM-LIKE may select an internal trajectory but cannot execute it.
5. Memory consolidation is deterministic and auditable.
6. Re-entry to WAKE is explicit and counted.
7. Self-report and metacognition are not required for the state machine.

## Measurement boundary

Useful measures include mode dwell time, consolidation count, replay count,
re-entry count, replay signatures, trajectory divergence across modes, and
action-boundary integrity.

None of these measures establishes phenomenal consciousness.


## Longitudinal continuity

The operational-state machine is intentionally not reset at mode boundaries.

### OFFLINE → DREAM-LIKE

OFFLINE builds a deterministic consolidation profile from persistent history:

`trajectory_counts → trajectory_scores → dominant_trajectory`

DREAM-LIKE then performs internal replay and records a separate
`operational_replay_profile`. A replayed trajectory receives bounded endogenous
reinforcement with decay.

That reinforcement is runtime-owned. It is not treated as external reward,
ground-truth evidence, or proof that the replayed trajectory was useful.

### DREAM-LIKE → WAKE

After explicit WAKE re-entry, the replay profile remains persistent and can
causally alter trajectory selection. This creates a testable chain:

```text
OFFLINE CONSOLIDATION
        ↓
DREAM-LIKE REPLAY
        ↓
ENDOGENOUS REPLAY PROFILE
        ↓
ATTRACTOR / TRAJECTORY BIAS
        ↓
WAKE RE-ENTRY
        ↓
NEW SELECTION
```

The benchmark property is that a state transition leaves a runtime-owned,
persistent causal trace that changes subsequent computation.
