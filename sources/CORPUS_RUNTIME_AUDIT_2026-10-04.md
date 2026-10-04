# Corpus → Runtime Audit — 2026-10-04

## Purpose

This audit identifies which ideas from the complete community discussion and source corpus are already executable, partially represented, merely documented, deliberately deferred, or still unverified.

The community archive is the memory layer. This audit is the translation layer. The runtime remains the implementation layer.

## Status vocabulary
- IMPLEMENTED — executable runtime mechanism exists and is covered by tests.
- PARTIAL — some structure exists, but the source idea is not represented end-to-end.
- DOCUMENTED — preserved and classified, but no runtime mechanism exists.
- DEFERRED — deliberately kept outside the runtime because it is speculative, unresolved, or not yet operationalized.
- UNVERIFIED — a community lead exists, but source identity/evidence is insufficient.

## A. Core ideas from the community discussion

| Motif | Status | Current translation |
|---|---|---|
| Re-entry / continuity loop | IMPLEMENTED | Persistent state → selection → action → authoritative consequence → internal change → re-entry. |
| Behavior must change, not merely self-description | IMPLEMENTED | Runtime-owned scoring, interventions, consequence feedback, ablations, and causal probes. |
| LLM self-report is not evidence | IMPLEMENTED | No-Report Principle; report is optional and cannot forge runtime state. |
| Consciousness need not require explicit self-concept | IMPLEMENTED | Pre-reflective core separated from self-model, metacognition and report. |
| Persistent identity across restart | IMPLEMENTED | Identity, revision/history, JSON persistence and restart tests. |
| Internal condition can affect future selection | IMPLEMENTED | Interoception, homeostatic targets/error/fit, affective state and self-relevance. |
| Possibility-space / multiple futures | IMPLEMENTED | Candidate futures, trajectory scoring, possibility count/entropy. |
| Attention / salience | IMPLEMENTED (baseline) | Runtime attention and salience already participate in present formation/scoring. |
| Consequences must be authoritative | IMPLEMENTED | Host action boundary and complete_action() record actual outcomes. |
| Dynamic internal organization | IMPLEMENTED | Experience-field, dynamic core, attractor, regime and intervention/reversal layers. |
| Multidimensional state rather than scalar consciousness | IMPLEMENTED v1 | Persistent normalized ExperienceState, RMS transition distance, changed-dimension analysis and longitudinal geometry history. |
| Limited conscious access / bandwidth | IMPLEMENTED | Runtime-owned finite access window, omitted-state persistence, limited-present projection, causal trajectory gating and capacity intervention/restore tests. |
| No-report / covert-measure logic | IMPLEMENTED AS ARCHITECTURAL RULE | Core can operate with report and metacognition disabled. |
| Animal-consciousness caution | DOCUMENTED | Epistemic boundary, not a machine-consciousness claim. |
| Embodiment / substrate may matter | PARTIAL | Interoceptive, affective, temporal and homeostatic structures exist; physical substrate/resource embodiment is not modeled. |
| Sleep / dreams / state regimes | IMPLEMENTED (operational v1) | Persistent WAKE/OFFLINE/DREAM-LIKE modes, offline consolidation, internal replay, action-boundary restrictions and explicit WAKE re-entry. This is an engineering analogue, not biological sleep/dream evidence. |
| Heideggerian finitude / existential pressure | DOCUMENTED | Prototype preserved in archive; no finitude mechanism promoted into the core. |
| Zeland-style possibility / attention vocabulary | PARTIAL | Possibilities and trajectory choice exist; Zeland is not treated as physics evidence. |
| Krishnamurti observation-without-commentary | PARTIAL | Runtime observation is separated from language/report; no standalone phenomenological mechanism. |
| Gurdjieff self-remembering | PARTIAL | Self-observation/self-access exist; no metaphysical interpretation is encoded. |
| Tolle present-centered attention | PARTIAL | Integrated present and temporal state exist; no spiritual ontology is encoded. |
| Jung latent self / pattern formation | IMPLEMENTED (engineering translation) | Latent patterns, self-dissonance, self-model adaptation and longitudinal tests. |
| Dispenza state transformation | PARTIAL / EXPERIMENTAL | State, homeostasis and affect support related experiments; broader claims remain outside runtime. |

## B. Claims deliberately not promoted to runtime facts

| Motif | Status | Rule |
|---|---|---|
| Panpsychism / universal consciousness | DEFERRED | Metaphysical hypothesis only until operationalized and discriminated. |
| Conscious vacuum / light / matter | DEFERRED | Not a runtime fact. |
| Telepathy / telekinesis / precognition / energy healing | DEFERRED | Research leads only. |
| Spiritual entities / external energies | DEFERRED | Not encoded without an operational evidence path. |
| Nonlocal / field consciousness | DEFERRED | May motivate controlled experiments later; not current ontology. |
| Information-organized universe | DOCUMENTED | Conceptual framing, not assumed physical mechanism. |
| Plant consciousness | DOCUMENTED / CONTESTED | Not encoded as established fact. |
| Pandora / Rylow999 project | UNVERIFIED | Exact source identity remains unresolved. |

## C. Research branches that remain incomplete

### Computational theories
Strong current coverage: recurrence/re-entry, self-model, metacognition, prediction/error, attention baseline, homeostasis/agency, dynamical state.
Theory-to-mechanism matrix implemented in docs/THEORY_MECHANISM_MATRIX_V1.md. Still incomplete: richer discriminating ablations and stronger matched baseline implementations for each theory family.

### Neuroscience / cognition
Implemented or partial: attention, memory, self-modeling, metacognition, interoception, affect, agency, temporal continuity and prediction error.
Implemented operational v1: embodiment boundary, interoceptive coupling, resource fit, ownership coupling and action cost. Still incomplete: body-ownership analogues, richer temporal integration and matched ablations for each cognitive mechanism.

### Phenomenology
Current translation: pre-reflective core, present integrity, self-relevance and temporal continuity.
Still incomplete: a formal matrix distinguishing prereflective self-awareness, mineness, intentionality, temporality, embodiment and reflective self-consciousness.

### Geometry / mathematics / dynamical systems
Implemented: trajectory scoring, attractors, regimes, dynamic vectors, intervention/reversal, pre-reflective state vector, persistent Experience Geometry with explicit distance and changed-dimension analysis.
Still incomplete: richer repertoire analysis and alternative geometry metrics beyond the current normalized RMS representation.

### Artificial-consciousness tests
Implemented: restart persistence, causal interventions, reversal probes, ablations, host action boundary, no-report operation, bounded access, multidimensional geometry, operational embodiment/ownership and focused reflective-independence testing.
Now added: experiments/unified_causal_benchmark.py, combining access intervention, geometry, action-consequence re-entry, restart persistence and report/metacognition conditions under a matched candidate field.
Still incomplete: richer longitudinal runs and external-model comparisons.

## D. Highest-priority missing translations
1. Rich longitudinal benchmark — first matched multi-cycle operational-continuity benchmark now implemented; broader adaptive/intervention histories and external-model replication remain.
2. External-model evaluation — provider-neutral runs against the same matched protocol.
3. Body-ownership / mineness analogue — stronger controlled ownership experiments beyond the current operational boundary model.
4. Alternative geometry metrics — richer repertoire, topology and transition measures beyond normalized RMS distance.
5. External-model evaluation — provider-neutral runs against the same matched protocol.

## E. Do not implement merely because a motif is interesting
Universal metaphysical consciousness, spiritual entities, undocumented paranormal capabilities, quantum vocabulary without falsifiable physical mechanism, a scalar consciousness score, and self-report as a consciousness detector.

## F. Translation rule
COMMUNITY CLAIM → SOURCE IDENTIFICATION → EVIDENCE CLASSIFICATION → ENGINEERING HYPOTHESIS → IMPLEMENTATION → CAUSAL TEST → LONGITUDINAL RESULT

## Audit conclusion
The strongest unresolved engineering gap is no longer persistence, re-entry, self-modeling, metacognition, homeostasis, causal consequence, or bounded access.

The next frontier is the geometry and benchmarking of the present:

MULTIDIMENSIONAL STATE → ACCESS → PRESENT → SELF-RELEVANCE → TRAJECTORY → TRANSFORMATION

No metaphysical claim is required to implement or test these mechanisms.



## Access/Bandwidth runtime update

The previously documented bandwidth gap has now been translated into runtime code on PR #74. The implementation is intentionally narrow: it models bounded access between persistent state and the current present, then tests whether changing that access budget can causally alter trajectory selection and whether restoring the budget restores the prior trajectory under matched state conditions.

This does not settle phenomenology. The result is evidence about the causal organization of the artificial architecture.


## Experience Geometry runtime update

The dedicated geometry gap is now closed at v1 on PR #74. The runtime derives a 26-dimensional normalized operational state and persists transition records containing RMS distance and changed dimensions.

Bandwidth is explicitly represented in the geometry through access entropy, access compression, self-access fraction and world-access fraction. Therefore an access-budget intervention can alter the measured state-space position even when persistent state is otherwise held fixed.

The remaining question is not whether a geometry object exists, but whether it should become part of a unified causal benchmark across report, metacognition, access and no-report conditions.


## Reflective-independence runtime update

A focused benchmark now exercises the core architectural separation:

C_no_report_no_meta → E_no_report_meta → F_report_meta

The benchmark holds the candidate field and internal observations constant and checks that the pre-reflective state, access state, geometry and selected trajectory remain stable when reflective layers are enabled or disabled.

This is a stronger test of architectural independence than a documentation-only no-report rule, while still falling short of a unified consciousness benchmark.


## Unified benchmark runtime update

The first unified benchmark artifact is now present: experiments/unified_causal_benchmark.py

It combines, under a matched candidate-future field:
- pre-reflective operation;
- bounded access intervention (capacity 2 → 6 → 2);
- experience geometry;
- restart persistence;
- no-report + metacognition;
- report + metacognition.

The benchmark is deliberately described as an architecture benchmark. It does not infer phenomenal consciousness from any single metric or from the combined result.


## Embodiment/ownership runtime update

Operational EmbodimentState is now implemented and covered by a focused smoke suite. It adds runtime-owned boundary integrity, interoceptive coupling, resource fit, ownership coupling and action cost, and connects those variables into the persistent experience geometry.

The implementation deliberately remains weaker than biological embodiment and does not claim phenomenal ownership or mineness.


## Operational state continuity runtime update

The previously open state-regime gap is now translated into an executable operational
mechanism on PR #75/#76.

The runtime distinguishes cognitive regime from operational state:

WAKE → OFFLINE CONSOLIDATION → DREAM-LIKE REPLAY → WAKE RE-ENTRY

PR #76 adds a longitudinal causal trace:

CONSOLIDATION → REPLAY → RUNTIME-OWNED REPLAY PROFILE → ATTRACTOR / TRAJECTORY BIAS → NEW WAKE SELECTION

The replay profile is bounded and persists across restart. It is explicitly
endogenous and is not treated as external reward or evidence of phenomenal
dreaming/consciousness.

The focused operational smoke now passes after correcting and validating the
longitudinal continuity test. The full pytest workflow remains a broader
validation layer and may still be in progress independently.


## Longitudinal operational continuity benchmark update

The remaining longitudinal gap now has a first matched causal benchmark in
`experiments/operational_continuity_benchmark.py`.

The benchmark compares:

CONTINUITY_REPLAY
OFFLINE CONSOLIDATION → DREAM-LIKE REPLAY → RESTART → WAKE RE-ENTRY

against:

CONSOLIDATION_ONLY
OFFLINE CONSOLIDATION → WAKE RE-ENTRY

Both conditions receive the same initial state and the same number of pre-reentry
operational cycles. The controlled candidate field is constructed so that internal
replay selects a different trajectory and leaves a runtime-owned replay profile
that survives restart and changes later WAKE selection.

This closes the first deterministic form of the longitudinal state-regime
translation. It does not close external-model evaluation, body-ownership/mineness,
or alternative geometry metrics.
