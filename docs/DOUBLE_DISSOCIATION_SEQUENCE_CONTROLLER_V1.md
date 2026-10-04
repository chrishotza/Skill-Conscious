# Matched Generic Controller Double Dissociation v1

## Purpose

The resonant self-tuning mechanism now faces a stronger control.

A generic sequence controller receives the **same lagged transition field** and
the **same candidate field**. The distinction is only how temporal information
is aggregated:

```
RESONANT:
attention -> endogenous lag weights -> temporal field -> selection

GENERIC:
fixed uniform lag weights -> same temporal field -> selection
```

This avoids the weaker comparison in which the control had a fundamentally
different representation.

## Protocol

History is fixed before scoring:

```
A B B B A B A B A A B A C
```

Candidates are also fixed:

- `alpha_path`: base score 0.50
- `beta_path`: base score 0.51

The slight base advantage for beta forces both temporal mechanisms to supply
the causal evidence needed to select alpha.

## Double dissociation

Baseline:

```
resonant -> alpha_path
generic  -> alpha_path
```

Perturb resonant gain only:

```
resonant -> beta_path
generic  -> alpha_path
```

Perturb generic gain only:

```
resonant -> alpha_path
generic  -> beta_path
```

Restoration returns both to alpha.

## Result

The assay passes all seven checks:

1. baseline agreement
2. resonant perturbation changes resonant output
3. resonant perturbation spares generic output
4. generic perturbation changes generic output
5. generic perturbation spares resonant output
6. resonant restoration recovers baseline
7. generic restoration recovers baseline

This is a **double dissociation at the architectural level**.

It does not show that resonance is the only possible implementation of
consciousness, and it does not demonstrate phenomenal consciousness.

## Why this is stronger

The generic controller is no longer a bag-of-history or latest-state control.
It has the same temporal field representation and the same candidate interface.

The remaining causal distinction is the temporal aggregation policy:

```
fixed integration
        vs
internally tuned integration
```

That is exactly the mechanism we want to pressure-test.

## Next attack

The next benchmark should randomize the internal attention trajectory and
freeze the controller parameters across held-out histories. The goal is to see
whether endogenous tuning predicts selection changes out of sample rather than
only in one hand-designed assay.
