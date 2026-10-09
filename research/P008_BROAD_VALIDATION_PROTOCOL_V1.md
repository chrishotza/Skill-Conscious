# P008 Broad Validation Protocol v1

## Status

**Preregistered design draft. Do not interpret as a result.**

This protocol follows the deterministic P008 / CF01 mechanism fixture. The fixture established that, in one frozen two-candidate configuration, the native trajectory scorer changes its selection when the self-model `continuity` weight is causally active and does not change when the same value is disconnected or stored in generic state.

That mechanism result is necessary but not sufficient for broad P008 support. A larger validation must avoid merely repeating the same hand-constructed boundary case.

## Research question

> Does persistent self-model state produce reproducible, specific, longitudinal changes in future trajectory selection across a frozen family of non-cherry-picked scenarios and across restart/action-consequence cycles?

## Scope and interpretation boundary

This protocol tests **functional causal self-reference in the runtime**.

A positive result may support the statement:

> Under the preregistered runtime conditions, future decisions depend specifically and reproducibly on persistent self-model state.

It does **not** establish phenomenal consciousness, subjective experience, sentience, or a general theory of consciousness.

## Two validation layers

### Layer 1 — broad counterfactual decision benchmark

Purpose: test whether the CF01 causal effect survives a frozen scenario family rather than one hand-selected pair.

The benchmark uses the same four causal conditions:

- **A — no self-model weight participation**
- **B — self-model present but causally disconnected**
- **C — causally active self-model**
- **D — matched generic persistent state**

The primary intervention remains the already frozen variable:

- self-model trajectory weight: `continuity`
- default: `1.0`
- confirmatory intervention: `0.0`

No scenario may be removed after observing which conditions diverge.

### Scenario corpus

The scenario corpus is generated once, hashed, and frozen before condition outcomes are inspected.

It contains three strata:

1. **Native-runtime scenarios**  
   Candidate sets emitted by `ConsciousRuntime.generate_candidate_futures()` under a preregistered Cartesian grid of exogenous base states. The grid varies only variables that are not the intervention target:
   - intention absent / present;
   - attention absent / present;
   - salience low / medium / high;
   - uncertainty low / medium / high;
   - topology intact / degraded;
   - interoceptive energy low / target / high;
   - self-state stability low / medium / high.

   Every generated candidate set is copied and frozen before A/B/C/D execution so candidate generation itself cannot become a condition-specific confound.

2. **Perturbed native scenarios**  
   Native candidate sets with deterministic, preregistered small signal perturbations applied symmetrically. Perturbations are generated from fixed integer seeds and are identical across A/B/C/D.

3. **Holdout scenarios**  
   A separately hashed set generated from grid combinations not used in development tests. Holdout results are not inspected until code, metric calculations, artifact schema, and all non-holdout tests are frozen.

### Layer 1 primary outcome

For each frozen scenario `s`:

`D_CB(s) = 1[selected_C(s) != selected_B(s)]`

`D_CD(s) = 1[selected_C(s) != selected_D(s)]`

Primary aggregate metrics:

- mean `D_CB`;
- mean `D_CD`;
- B-vs-D disagreement rate;
- A-vs-B disagreement rate;
- signed score-margin shift for the selected-vs-runner-up trajectory.

The primary claim is supported only if:

1. C differs from B on a non-zero preregistered fraction of scenarios;
2. C differs from D on a non-zero preregistered fraction of scenarios;
3. B-vs-D and A-vs-B disagreement remain at or below the preregistered control ceiling;
4. the direction of score-margin change matches the sign of the `continuity` intervention;
5. the effect is present in the hidden holdout stratum, not only the development stratum.

No threshold will be tuned after result inspection.

### Dose-response secondary test

Without changing the primary confirmatory contrast, run frozen continuity values:

`[0.0, 0.5, 1.0, 1.5, 2.0]`

For each scenario, record the score difference between continuity-favoring and non-continuity-favoring candidates.

Secondary prediction:

> The score-margin response is monotonic with the continuity weight whenever candidate continuity signals differ.

This is a mechanistic dose-response check, not an independent consciousness claim.

## Layer 2 — longitudinal causal re-entry

Purpose: test a stronger property than direct weight injection.

The runtime must complete real host-boundary cycles:

`integrate → select → begin_action → complete_action → persist → restart → re-enter`

The experiment uses host-observed `self_state` outcomes and the existing evidence-gated `self_model_adaptation` machinery.

### Longitudinal conditions

- **L0 frozen self-model:** adaptation disabled.
- **L1 observed self-state, adaptation disconnected:** identical evidence is accumulated but the adapted expectation is prevented from entering the future decision path.
- **L2 causal self-model adaptation:** host-observed self-state evidence may update the persistent expected self-state through the native adaptation gate, and the resulting self-model participates normally in future runtime dynamics.
- **L3 matched generic adaptation:** the same numeric evidence/update payload is persisted outside the self-model causal path.

### Longitudinal evidence sequence

Use a frozen outcome schedule with two phases:

- Phase 1: repeated observations consistently below the initial expected state.
- Phase 2: reversal observations consistently above it.

This tests:

- minimum-evidence gating;
- direction consistency;
- hysteresis/reversal handling;
- persistence across restart;
- downstream trajectory/regime consequences.

No outcome is generated by the runtime itself; the host schedule is authoritative and identical across conditions.

### Layer 2 primary outcome

Primary longitudinal metric:

> first post-update cycle at which L2 trajectory selection differs from L0/L1/L3 under an identical frozen candidate set, after an evidence-gated self-model update has actually occurred.

Required causal chain for a positive longitudinal result:

1. identical host evidence enters all matched conditions;
2. the native adaptation gate records sufficient evidence;
3. L2 self-model state changes;
4. the change survives restart;
5. a future decision or regime differs in L2;
6. L1/L3 do not show the same difference;
7. removing or restoring the causal self-model change reverses the downstream effect when the runtime supports a reversible intervention.

If step 3 does not occur, the trial is an adaptation-gate null, not evidence against downstream causality.

If step 3 occurs but step 5 does not, the causal self-model hypothesis is weakened for that pathway.

## Controls

All confirmatory comparisons must hold constant:

- code commit;
- Python and package version;
- runtime configuration;
- identity;
- external input;
- frozen candidate futures;
- host outcome schedule;
- memory/history limits;
- serialization;
- compute budget;
- restart points;
- action/consequence ordering;
- perturbation seeds;
- artifact schema.

The experiment must record hashes for:

- scenario corpus;
- holdout scenario corpus;
- host outcome schedule;
- runtime configuration;
- candidate sets;
- result artifact.

## Anti-cherry-picking rules

Before any confirmatory run:

1. generate the complete development and holdout scenario corpora;
2. write both corpora to durable JSON;
3. hash them;
4. freeze the intervention magnitudes and control ceilings;
5. freeze all primary/secondary metrics;
6. freeze exclusion rules;
7. run tests on development fixtures only;
8. then execute the holdout exactly once for the preregistered version.

A scenario may be excluded only for a preregistered mechanical invalidity such as:
- empty candidate set;
- duplicate candidate IDs;
- non-finite score;
- serialization failure.

An exclusion may not depend on whether C differs from a control.

## Required artifacts

A complete run must produce:

- `scenario_manifest.json`
- `holdout_manifest.json`
- `run_manifest.json`
- one row per condition/scenario/cycle in machine-readable form;
- longitudinal action/consequence receipts;
- state hashes before/after restart;
- self-model adaptation ledger snapshots;
- primary/secondary metric summary;
- test logs;
- workflow/run metadata.

## Failure and falsification criteria

P008 is weakened if any of the following occur:

- C does not differ from B or D outside the original hand-built fixture;
- B and D differ at a rate comparable to C;
- effects appear only in development scenarios and disappear in holdout;
- dose-response direction is inconsistent with the manipulated weight;
- longitudinal self-model updates occur but have no measurable future consequence;
- generic-state or disconnected controls reproduce the longitudinal effect;
- restart removes the causal effect;
- the result depends on post-hoc scenario filtering.

## Decision rule after execution

Possible outcomes must be labeled separately:

- **MECHANISM_REPLICATED** — broad direct-weight effect survives frozen scenario corpus and controls.
- **LONGITUDINAL_SUPPORTED** — evidence-gated self-model updates survive restart and specifically change future dynamics.
- **PARTIAL** — one layer passes and the other does not.
- **NULL** — no specific causal divergence under the preregistered design.
- **INVALID_RUN** — provenance/control/artifact contract fails.

No outcome label implies phenomenal consciousness.
