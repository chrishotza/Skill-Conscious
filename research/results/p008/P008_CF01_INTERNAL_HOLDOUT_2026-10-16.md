# P008 / CF01 — first frozen internal reserved-split result

**Date:** 2026-10-16. **Classification:** verified controlled synthetic software result, not an externally preregistered or peer-reviewed study and **not evidence of phenomenal consciousness**.

## Freeze and execution chain

1. Initial mechanism fixture PR #90 → 32-scenario exploratory pilot PR #92 (C-vs-B and C-vs-D mean divergence 0.125).
2. Sealed holdout runner PR #93 → frozen code and protocol PR #94, immutable main baseline `c0278493e8ef31520beea29355f947a7ea3739a8`.
3. Separately merged release marker PR #95; main merge `c9728d2552b184d4b37c8590279e8ea4e8a04337`. The registered frozen path diff and ancestry checks passed before any holdout data were generated.
4. GitHub Actions run `38980796822`, job `117240940963`: **140 passed** (12.07 seconds), release verified, all 128 held-out IDs (1000–1127) executed, separate raw-file analysis + SHA-256 audit passed. Recorded 4 arms and 2 cycles per scenario (**1024 arm cycles**). The holdout was not sampled in preceding CI tests.

## Recorded primary and negative-control outcomes

| Scenario-clustered paired contrast | Mean divergence | Percentile bootstrap 95% |
|---|---:|---:|
| Active self-model C vs disconnected B | **0.234375** | [0.164062, 0.312500] |
| Active self-model C vs generic-state D | **0.234375** | [0.164062, 0.312500] |
| Disconnected B vs generic-state D | **0** | [0, 0] |
| No intervention A vs disconnected B | **0** | [0, 0] |

The predeclared **internal software-mechanism gate passed**: lower 95% cluster-bootstrap bounds for C-B and C-D were positive, B-D disagreement was zero and all matched input/state, intervention and restart contracts passed. Bootstrap used 2,000 resamples of *scenarios*, seed 20261016, not resampling correlated cycles independently. Reported uncertainty is conditional on the selected synthetic generator.

## Raw evidence and reproducibility

GitHub Actions artifact `p008-reserved-holdout` ID **12081087004** contains **128 input JSON + 512 per-arm JSON** files and the SHA-256 manifest. Archive size: **633705 bytes**; uploaded ZIP SHA-256:

```text
8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32
```

Artifact upload succeeded on 2026-10-16 and expires 2027-01-14 23:19:20 UTC. The separate archival workflow will attempt to preserve the identical ZIP as a long-lived GitHub Release asset tagged `p008-cf01-internal-holdout-20261016`, checking this checksum *before* publication. Treat that persistent backup as pending until its workflow succeeds. The result is bound to the original workflow run and frozen commit and is never regenerated to impersonate the original bytes.

## Boundaries and unanswered questions

This is an internal synthetic counterfactual test of a *hand-engineered deterministic selector*. Its conditions differ by whether the selector consumes a specific parameter. Positive divergence is expected in this architecture and tests a reproducible implementation property. The result cannot establish phenomenal experience, awareness, learned agency, real-world outcome quality, generalization to new models or agents, or causal self-reference beyond the tested parameter path. Independent external methodological review and replication on an alternative implementation remain open. Keep the original S01 negative and provenance-limited outcomes separate.

## Permanent evidence preservation — VERIFIED 2026-10-16

Archive workflow run **38981166451** completed, after downloading the *original* GitHub Actions artifact 12081087004 and verifying its exact original ZIP SHA-256 and size before upload. GitHub Release `p008-cf01-internal-holdout-20261016` was created at `https://github.com/chrishotza/Skill-Conscious/releases/tag/p008-cf01-internal-holdout-20261016`, release ID **415457666**, asset ID **648924054**, published 2026-10-16 23:23:27 UTC. GitHub's published asset metadata independently displays **633705 bytes** and `sha256:8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32`, exactly matching the ephemeral Actions archive. The original run and frozen protocol remain unchanged. This is a persistent copy, but normal repository/Release access control and deletion rights still apply.
