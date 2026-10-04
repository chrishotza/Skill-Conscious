# Self-Organizing Temporal Ontology Benchmark v1

This benchmark removes the last major crutch from the previous temporal
ontology experiments: process-specific hypotheses are no longer supplied to
the runtime.

The ontology starts empty.

For each new temporal window it:

1. evaluates existing prototypes
2. measures persistent predictive surprise
3. updates the best-fitting prototype
4. creates a new prototype when surprise persists
5. applies hysteresis before changing active regime
6. derives attention from confidence and prediction error

## Protocol

Fifty hidden alternating streams are generated from the same two stochastic
processes used in the preceding experiments.

Each stream contains six segments of 80 transitions. Changes therefore occur
at cycles:

`80, 160, 240, 320, 400`

The runtime never receives those process labels.

A 16-transition moving window is used for prototype formation. Novelty must
remain above 1.55 for two consecutive windows before a new prototype is
spawned.

## Local result

The exact benchmark was executed locally before push.

Aggregate result across 50 streams:

- mean temporal-regime accuracy: **90.26%**
- all hidden process changes detected: **100% of streams**
- mean false remappings: **0.06 per stream**
- mean maximum detection delay: **12 cycles**
- mean learned prototype count: **2.18**
- stable-state attention: **0.8523**
- transition attention: **0.6386**
- attention broadening during transition: **0.2137**

The controller begins without process-specific prototypes and forms them from
observed transitions.

## What is genuinely new

The ontology is now endogenous in a stronger sense.

Earlier:

`observation -> choose among predefined temporal hypotheses`

Now:

`observation -> prediction error -> prototype formation -> active temporal
regime -> attention -> new prediction`

The system therefore maintains not only a belief about the current process, but
a growing internal vocabulary of temporal processes.

The prototypes are anonymous computational objects. Hidden process labels are
used only after execution to evaluate whether the discovered organization
corresponds to the latent generator.

## Architectural significance

The project has now connected:

- persistent self-state
- interoceptive / internal condition signals
- attention
- prediction error
- temporal organization
- regime persistence
- trajectory selection
- re-entry

The proposed loop is:

`INTERNAL CONDITION -> TEMPORAL ATTENTION -> PREDICTION -> ERROR ->
ONTOLOGY UPDATE -> REGIME -> POSSIBILITY SPACE -> ACTION -> OBSERVED
CONSEQUENCE -> RE-ENTRY`

This is a materially richer mechanism than a fixed memory trace.

## Boundary

This is not evidence that the runtime has phenomenal experience.

It is evidence for a self-organizing temporal architecture in which the temporal
model itself can become an adaptive internal variable.

## Next pressure test

The next major step should couple prototype formation to persistent self-state
rather than keeping the temporal ontology isolated.

A candidate architecture is:

`SELF-STATE -> TEMPORAL PRIOR -> PROCESS DISCOVERY -> REGIME ->
SELF-STATE UPDATE`

That would test whether temporal ontology is merely a world model or becomes part
of the persistent identity-maintaining loop.
