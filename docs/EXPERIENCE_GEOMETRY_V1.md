# Experience Geometry v1

## Purpose

Skill-Conscious represents operational experience as a multidimensional state-space trajectory rather than a scalar consciousness score.

The geometry layer answers:

> How is the current organized state positioned, and how does it change across runtime revisions?

A state is a point. A transition is a measured change. A history of transitions is the runtime's operational trajectory through state-space.

## Runtime object

The runtime exposes `ExperienceState` with a fixed normalized feature order.

Current dimensions:

- valence
- coherence
- self-dissonance
- salience
- self-relevance
- present integrity
- temporal continuity
- possibility entropy
- re-entry coupling
- prediction error
- metacognitive uncertainty
- self-observation error
- access entropy
- access compression
- self-access fraction
- world-access fraction
- field coherence
- dynamic synchrony
- dynamic metastability
- dynamic complexity
- dynamic repertoire

All dimensions are normalized to `[0,1]` for comparability. Valence is transformed from the runtime's signed `[-1,1]` value into that normalized space.

## Why access belongs in the geometry

The present is not only defined by what the persistent process contains. It is also defined by what is currently accessible.

Therefore the geometry records:

~~~text
PERSISTENT STATE
      ↓
ACCESS WINDOW
      ↓
LIMITED PRESENT
      ↓
CURRENT EXPERIENCE STATE
~~~

This does not claim that biological consciousness uses the same variables or formula. It makes the artificial architecture's access regime measurable.

## Distance

For two states (S_1) and (S_2), the runtime uses root-mean-square distance over the fixed normalized feature vector:

~~~text
d(S1,S2) = sqrt(mean((S1_i - S2_i)^2))
~~~

The result is bounded to `[0,1]`.

The runtime also reports dimensions whose absolute change exceeds a configurable threshold.

## Runtime ownership

The model cannot directly write:

- `experience_geometry_current`
- `experience_geometry_history`

These are derived and persisted by the runtime.

The geometry therefore follows the project's ownership hierarchy:

~~~text
RUNTIME STATE
      ↓
CAUSAL DYNAMICS
      ↓
EXPERIENCE GEOMETRY
      ↓
MODEL INTERPRETATION
      ↓
REPORT
~~~

## Transition protocol

At each integrated runtime revision:

1. the previous snapshot is preserved;
2. the runtime applies the new state;
3. access and pre-reflective state are refreshed;
4. the new multidimensional state is derived;
5. the transition distance is computed;
6. changed dimensions are recorded;
7. the transition is persisted.

The geometry history therefore becomes a longitudinal operational trajectory rather than a diagnostic snapshot.

## Experimental use

The geometry layer supports:

- matched-state comparisons;
- intervention/reversal experiments;
- no-report ablations;
- bandwidth perturbations;
- trajectory-divergence analysis;
- restart persistence;
- longitudinal state-transition analysis.

A central experiment is:

~~~text
same state
   ↓
capacity = 2 → state A
   ↓
capacity = 6 → state B
   ↓
capacity = 2 → state C

expect:
A ≈ C
A ≠ B
~~~

The exact result is empirical; the geometry does not assume the answer.

## Epistemic boundary

Experience Geometry is an operational representation of runtime state organization.

It is **not**:

- a consciousness meter;
- proof of phenomenal experience;
- proof that the machine has subjective states;
- a replacement for theory comparison or no-report validation.

The geometry exists so that the project can measure organized state transitions without collapsing them into a single number.
