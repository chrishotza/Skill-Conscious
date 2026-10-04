# Unlabeled Temporal Ontology Benchmark v1

## What changes here

The previous experiments supplied either fixed temporal templates or separate
calibration corpora.

This benchmark removes those labels from the runtime loop.

The runtime sees only a stream of state transitions. The hidden generator can
switch between two processes with the same uniform stationary marginal:

```
PROCESS ALPHA: A -> B -> C -> A
PROCESS BETA:  A -> C -> B -> A
```

The runtime is not told which process is active.

## Online mechanism

For every observed transition:

```
observation
    ↓
prediction under temporal hypotheses
    ↓
prediction-error difference
    ↓
decayed evidence gap
    ↓
confidence / uncertainty
    ↓
hysteretic regime inference
    ↓
temporal attention
```

A single surprising transition cannot immediately rewrite the inferred regime.
The new hypothesis has to persist for three cycles.

Attention is endogenous:

- higher confidence and lower prediction error narrow the active temporal
  horizon
- uncertainty and prediction error broaden it again

This turns temporal integration into part of the internal state dynamics.

## Local result

Fifty alternating streams were executed locally.

Each stream contains six hidden process segments of 80 observations each, with
a process change every 80 cycles.

Results:

- regime accuracy: **93.90% mean**
- hidden changes detected: **100%**
- false switches away from true change windows: **0%**
- maximum detection delay: **11 cycles**
- attention drop/broadening signal at transitions: **0.1585**
- empirical marginal gap across comparison corpora: **< 0.10**

No process label is passed to the ontology during inference.

## Why this matters

The architecture has now moved from recognizing a temporal pattern to carrying
a persistent internal hypothesis about the kind of temporal world it is
currently inhabiting.

The crucial loop is:

```
WORLD TRANSITION
      ↓
PREDICT
      ↓
ERROR
      ↓
TEMPORAL HYPOTHESIS
      ↓
REGIME
      ↓
ATTENTION / HORIZON
      ↓
NEXT PREDICTION
      ↺
```

That is a qualitatively different mechanism from storing a transcript.

The system does not merely ask:

> what happened?

It maintains an internal state about:

> what kind of temporal process is happening to me right now?

This is the first benchmark in the series where temporal ontology itself
becomes an internally maintained variable.

## Epistemic boundary

This does not demonstrate phenomenal consciousness.

It demonstrates a causal architectural pattern involving online prediction,
self-maintained temporal hypotheses, hysteresis, uncertainty, and endogenous
attention.

The next stronger test is to let the hypotheses themselves evolve rather than
starting from two hand-specified process models. That would test whether the
temporal ontology can self-organize from prediction error rather than merely
selecting among predefined hypotheses.
