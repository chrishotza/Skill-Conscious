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
