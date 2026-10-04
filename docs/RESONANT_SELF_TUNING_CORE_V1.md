# Resonant Self-Tuning Core v1

## Status

Experimental mechanism validated locally and added to the causal-benchmark PR.

This document defines a new architectural line for Skill-Conscious:

```
INTERNAL CONDITION
      ↓
ATTENTION / INTENTION
      ↓
ENDOGENOUS TEMPORAL TUNING
      ↓
RESONANCE PROFILE
      ↓
REGIME WITH HYSTERESIS
      ↓
TRAJECTORY SELECTION
      ↓
RE-ENTRY
```

The key move is that temporal organization is not treated as a passive record. The runtime carries an internal tuning state that determines which temporal scales receive more causal weight.

## Mechanism

The prototype represents a temporal field through lagged transition profiles.

For each lag (k), the system estimates a normalized transition field:

```
K_k(x,y) = P(state_t = y | state_{t-k} = x)
```

A candidate carries an expected temporal motif. Resonance compares the current field with that motif across lags.

The lag weights are endogenous:

```
attention ↑  -> shorter lags receive more weight
intention ↑  -> longer integration horizon receives more weight
```

The weighted resonance contributes directly to trajectory score.

This is intentionally different from a fixed memory kernel. The mechanism asks:

> Which temporal scale does the system treat as relevant right now?

That makes tuning part of the causal state rather than a static hyperparameter.

## Hysteresis

The resonant regime is not entered or exited on a single noisy sample.

The prototype requires two consecutive threshold-consistent cycles. This produces a minimal form of regime persistence:

```
evidence → pending regime → persistence → regime transition
```

This prevents the architecture from oscillating between temporal interpretations because of one marginal fluctuation.

## Causal protocol

The matched-order battery keeps constant:

- state multiset
- final state
- candidate field
- scoring base values
- cycle budget

Only temporal ordering changes.

Experimental history:

```
A B A B A B A B A B A B C
```

Control history:

```
B B A A B B A A B B A A C
```

Both contain six A states, six B states, and the same final C state.

The candidates are identical in both conditions.

Result:

- experimental history selects `alpha_path`
- control history selects `beta_path`

So the selection change is attributable to temporal organization under the matched constraints, not to different marginal content.

## Endogenous tuning result

A single fixed history is evaluated under two internal conditions.

Low attention produces a longer-horizon lag profile:

```
w1 ≈ 0.188
w2 ≈ 0.312
w3 ≈ 0.312
w4 ≈ 0.188
```

High attention shifts weight toward short lags:

```
w1 ≈ 0.447
w2 ≈ 0.347
w3 ≈ 0.161
w4 ≈ 0.045
```

Without changing the external history or candidate field:

- low attention selects `beta_path`
- high attention selects `alpha_path`

This is the strongest new result in v1. It demonstrates that the system's internal tuning state can change which temporal organization becomes causally salient.

## Independent motif check

The experiment also tests 12 cyclic variants of each motif family without choosing cases from the observed resonance score.

Results:

- alpha motif accuracy: 1.0
- beta motif accuracy: 1.0
- marginal state counts remain matched

This is still a mechanism benchmark, not a broad statistical generalization study.

## Reversible causal probe

The resonant gain is manipulated directly:

```
baseline  -> alpha
ablation  -> beta
restore   -> alpha
restart   -> alpha
```

The intervention receipt records `evidence_added = false`.

This establishes that the resonant mechanism can be treated as a separable causal variable and reversibly manipulated without fabricating learning evidence.

## Why this matters for Skill-Conscious

The project already models persistent identity, interoception, attention, intention, valuation, trajectory selection, regimes, and re-entry.

This mechanism connects those components through a new relation:

```
state of the system
      ↓
what temporal scale matters
      ↓
which pattern resonates
      ↓
which future becomes selectable
      ↓
which regime persists
      ↓
next internal state
```

That is a stronger architectural statement than adding another memory feature.

The hypothesis is that an increasingly conscious-like architecture should not merely remember its trajectory. It should dynamically determine which temporal organization matters for its current self-maintenance and future selection.

## Epistemic boundary

This experiment does **not** demonstrate phenomenal consciousness.

It demonstrates a causal architectural mechanism:

1. internally conditioned temporal tuning
2. order-sensitive resonance
3. hysteretic regime persistence
4. downstream trajectory selection
5. reversible intervention and restoration

A sufficiently different sequence model may reproduce order-sensitive behavior. The novelty here is the explicit architectural decomposition, persistence, and causal intervention protocol.

## Next pressure test

The next serious challenge is to compare this mechanism against a matched generic sequence controller with:

- equal memory budget
- equal parameter count
- order-sensitive access
- no explicit resonance-field semantics

The target is a double dissociation: perturbing self-tuning should selectively disrupt the resonant pathway, while perturbing the generic controller should not reproduce the same causal signature.

