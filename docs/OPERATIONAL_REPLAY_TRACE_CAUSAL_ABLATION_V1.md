# Operational Replay Trace Causal Ablation v1

## Purpose

PR #78 established reversible history dependence. This layer asks a sharper causal question:

> Does the persistent replay trace itself mediate the later WAKE selection?

The benchmark therefore performs an explicit runtime-owned intervention:

```
DREAM-LIKE replay
      ↓
persistent replay profile
      ↓
restart
      ↓
WAKE → beta
      ↓
ABlate replay profile
      ↓
WAKE → alpha
      ↓
restore exact replay profile
      ↓
WAKE → beta
```

## Required causal signature

The benchmark passes only when:

- replay repeatedly selects beta;
- intact replay state produces beta after restart;
- replacing the replay profile with an empty profile produces alpha;
- restoring the captured runtime-owned profile recovers beta;
- the intervention creates no learning evidence.

This distinguishes **the replay trace as a causal variable** from generic elapsed computation or the mere existence of a history.

## Interpretation boundary

The result is an architectural causal intervention.

It does not establish phenomenal consciousness, biological dreaming, subjective experience, or substrate equivalence.

The intervention is explicitly an experimental runtime operation and is not represented as environmental reward or authoritative world evidence.
