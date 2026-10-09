# P008 Execution Log

## 2026-10-06 — execution attempt

### Target

`experiments/p008_self_model_causal_runtime.py`

### Purpose

Execute the P008 runtime-connected self-model causal intervention against the actual `ConsciousRuntime` implementation.

### Attempt

A local repository clone/execution was attempted.

Observed environment failure:

`fatal: unable to access 'https://github.com/chrishotza/Skill-Conscious/': Could not resolve host: github.com`

### Scientific status

**NO EMPIRICAL RESULT PRODUCED.**

The assay remains a protocol.

No trajectory-selection effect, null effect, replication claim, or consciousness claim is inferred from the failed execution.

### Static validation

The assay source was successfully retrieved from the canonical GitHub repository and its Python import/header structure was syntax-checked locally.

This is only a code-integrity check. It is not an experimental result.

### Next execution requirement

Run the exact repository commit containing the assay in an environment with:

- repository access;
- Python runtime;
- project dependencies installed;
- deterministic seed control;
- output artifact persistence.

Then store one machine-readable result artifact per seed/condition under the experiment-results layer, with commit SHA and runtime version.


## 2026-10-09 — CF01 assay contract revision (implementation only)

The primary assay source was revised on branch `research/p008-cf01-audit-assay` to match the four registered condition labels and to freeze a one-factor intervention: self-model `continuity` weight 1.0 → 0.0. The assay now executes two fixed-input integration cycles, reloads the persisted state between cycles, records a fixed consequence without utility/weight adaptation, and writes a provenance-bearing JSON result.

A dedicated CPU GitHub Actions workflow runs the complete pytest suite, runs the assay, and uploads the result artifact with 90-day retention. Unit tests cover condition definitions, the expected selector mechanism, state persistence/restart, hashes, and artifact round-tripping.

**Status at the time of this log entry: NO EMPIRICAL P008 RESULT CLAIMED.** The revised assay's outcome and the full test-suite verdict remain pending the workflow run. Even if the predeclared mechanism criterion passes, the result supports only functional causal influence in this fixed runtime fixture, not phenomenal consciousness.

## 2026-10-09 — P008 CF01 mechanism-fixture run 37898192199

**Execution status:** the focused CF01 test job, assay process, and result-artifact upload completed successfully in GitHub Actions. The full repository pytest suite was still running at the time this record was written; overall PR validation therefore remains pending.

- Workflow run: https://github.com/chrishotza/Skill-Conscious/actions/runs/37898192199
- Source artifact ID: `11601426903`; ZIP SHA-256: `f44bbfc08c1879b25ddede846ea48e660a9c122059e1895d9e5e838f8dc50ffe`.
- Canonical JSON copy: `research/results/p008/P008_CF01_37898192199.json`.
- Executed workflow merge-ref commit recorded in the artifact: `7f1381cfd17ce75d92a92e5c43ba51cbdb0d13cb`; runtime `skill-conscious 0.9.0`, Python `3.11.17`.
- Candidate-set SHA-256: `142b80d90ab428c8bf81ecba996a72ceaf3ce2647bfb718302f4bf04943e2425`; fixed-input SHA-256: `72ee237aebb0fe244a7b98326f57c715d24e6b836c96fb2945ea5d38b1c03263`.
- Selections in both cycles: A=`preserve`, B=`preserve`, C=`explore`, D=`preserve`.
- Primary fixture metric: C-vs-B divergence `1.0`; C-vs-D divergence `1.0`; B-vs-D control disagreement `0.0`. All four condition-state checks survived restart.
- The predeclared *mechanism-fixture* criterion was met.

**Interpretation boundary:** this is a deliberately hand-constructed, deterministic two-candidate mechanism fixture with two cycles and no RNG. It demonstrates that, under this configuration, the scorer's selection changes when its `continuity` self-model weight changes from 1.0 to 0.0 and the difference is not reproduced by the disconnected or generic-state controls. It does **not** provide broad empirical validation, estimate variability across seeds/candidate sets, or establish phenomenal consciousness. The full suite and PR checks still need their final verdict.
