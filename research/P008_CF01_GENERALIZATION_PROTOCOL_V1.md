# P008 / CF01 — Generalization Stress-Test Design (Draft v0.1)

**Status: DRAFT, NOT FROZEN, NOT EXECUTED (2026-10-16).** This is a proposed next experiment, not a preregistered result. Do not call it confirmatory until a generator, harness and complete analysis plan have been implemented, independently reviewed and frozen in a main-branch commit **before** holdout execution.

## Scope and contrast

The October CF01 run proved only the native selector reacts to a hand-picked, directly connected `continuity` weight. The next test asks whether that counterfactual dependency survives **varied synthetic candidate and input scenarios** with equal state payloads, fixed compute, two cycles and restarts. It cannot establish consciousness or real-world utility; successful results are still functional software evidence.

## Matched conditions

| Arm | Intervention stored | Scorer reads it? |
|---|---|---|
| A no-self-model | None | Default weights |
| B disconnected self-model | `self_model.trajectory_weights.continuity=0` | No; uses defaults |
| C causal self-model | Same self-model value | Yes; uses native runtime |
| D generic-state control | Same value in non-scoring generic state | No; uses defaults |

The only intervention is `continuity: 1.0 → 0.0`. Do not adjust other weights, the candidate set, external input, identity, compute budget, persistence policy, or outcome feedback separately by arm. Disable online adaptation, dynamic core and self-observation for this assay.

## Candidate universe, split and generation

A pilot set uses scenario IDs **0–31**; the separate holdout uses IDs **1000–1127**. Each scenario generates exactly two candidates with stable IDs and four numeric signals (`goal_fit`, `continuity`, `learning`, `risk`) in [0,1] from a local `random.Random(scenario_id)`. Store canonical candidate/input JSON and SHA-256. Feed identical inputs to all four arms. Perform two cycles per arm with persistence/reload and fixed consequence. The second cycle belongs to the same scenario: never count it as an independent sample.

**Pilot may diagnose and revise** this still-draft design. Every substantive change before holdout requires a new protocol version and SHA. Once frozen, include *every* holdout scenario, do not change thresholds, and report null/negative results. These published scenario IDs are deterministic reproducibility keys, not a claim of cryptographic blinding.

## Metrics and decision rule

The primary paired outcome is the fraction of holdout (scenario, cycle) selections differing between C vs B and C vs D; the B vs D disagreement rate is a negative-control check. Compute 95% bootstrap intervals resampling **scenarios** (not individual cycles), 2,000 resamples with bootstrap seed 20261016. Include A vs B agreement, score-margin and continuity-gap stratifications as explicitly secondary, with no post-hoc promotion.

The pre-proposed *software mechanism gate*: positive lower bootstrap bound for both C vs B and C vs D, **zero** B vs D disagreement, and 100% matched-input/restart/intervention integrity. This may fail naturally if the generated candidate preferences do not depend enough on the weight. Failure is recorded as failure, never fixed by silently changing candidates. A pass proves only causal dependence of this scorer on this weight under these synthetic scenarios.

## Evidence requirements and next stages

Persist one per-scenario/per-arm raw record with provenance, effective weights, candidate/input hashes, selections, score margins, restart check and timestamp; persist a manifest plus protocol/generator hashes. Verify identical candidate sets and inputs before comparing arms. Record any mismatch or timeout. The complete machine-readable draft and required fields are in `research/p008_generalization_protocol_v1.json`.

**Missing, not implied complete:** (1) generator and executable harness, (2) full raw-artifact persistence, (3) pilot/performance inspection, (4) independent pre-holdout freeze, (5) confirmatory execution, (6) audit. Closed-loop outcome quality and genuine generalization outside hand-coded scoring are separate stronger research questions, not measured here.


## Pilot implementation checkpoint (2026-10-16)

A development-only implementation is provided in `experiments/p008_generalization_pilot.py`, with `.github/workflows/p008-generalization-pilot.yml` and tests. It generates IDs 0..31 only, runs four A/B/C/D controls and two restarted cycles, writes input/per-arm raw JSON with SHA-256 manifest, computes scenario-clustered descriptive bootstrap intervals, and re-audits output. CI will retain raw artifacts for 90 days. **CI verification is pending. The holdout is not accessed and the protocol is not frozen.**
