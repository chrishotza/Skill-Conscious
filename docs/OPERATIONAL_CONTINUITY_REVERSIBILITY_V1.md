
# Operational Continuity Reversibility Benchmark v1

## Purpose

The longitudinal continuity benchmark established that an internal replay history can survive restart and causally bias a later WAKE selection.

This benchmark raises the bar from **persistence** to **reversible history dependence**:

    BASELINE
       ↓
    BETA REPLAY HISTORY
       ↓
    RESTART
       ↓
    WAKE → beta
       ↓
    COUNTER-HISTORY
       ↓
    RESTART
       ↓
    WAKE → alpha

The target is not merely that an internal trace exists. The target is that the trace is **causally active, persistent, updateable, and reversible**.

## Experimental design

Two matched runtimes begin from the same seeded state.

### Reversible condition

1. WAKE baseline selects alpha_path.
2. OFFLINE consolidation runs.
3. DREAM-LIKE replay is supplied the matched controlled candidate field and repeatedly selects beta_path.
4. The runtime is restarted.
5. WAKE selection now follows the persistent beta replay trace.
6. A second DREAM-LIKE phase uses a controlled counter-history that repeatedly selects alpha_path.
7. The runtime is restarted again.
8. WAKE selection now follows the updated alpha replay trace.

### Matched control

The control receives the same initial state and the same number of internal cycles, but remains in OFFLINE consolidation and never produces a DREAM-LIKE replay profile.

The control therefore tests whether the observed selection history requires the replay mechanism rather than elapsed computational cycles alone.

## Causal signature

The expected signature is:

    same initial state
          ↓
    different operational history
          ↓
    persistent replay trace
          ↓
    different WAKE selection
          ↓
    counter-history
          ↓
    new persistent replay trace
          ↓
    reversed WAKE selection

The benchmark passes only when:

- baseline WAKE selects alpha_path;
- the first replay phase selects beta_path;
- the first post-restart WAKE selects beta_path;
- the counter-replay phase selects alpha_path;
- the second post-restart WAKE selects alpha_path;
- the matched control remains on the baseline trajectory;
- replay state survives both restarts;
- no external reward or authoritative world outcome is used to create replay reinforcement.

## Interpretation boundary

This is an **architectural causal benchmark**.

It demonstrates operational history dependence, persistence, internal replay, re-entry, and reversible modification of runtime-owned trajectory bias. It is not a demonstration of phenomenal consciousness, biological dreaming, subjective experience, or substrate equivalence.

The benchmark intentionally separates:

- **history-dependent causal state** from
- **self-report** and
- **claims about phenomenology**.

The no-report principle therefore remains intact.
