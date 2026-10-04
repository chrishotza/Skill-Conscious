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
| Sleep / dreams / state regimes | PARTIAL | Temporal state, memory and regimes exist; dream/sleep and offline consolidation are not implemented. |
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
Still incomplete: a theory-by-theory benchmark matrix that maps GNWT, IIT, recurrent processing, higher-order theories, predictive processing, active inference, attention-schema and world-model approaches to discriminating runtime ablations.

### Neuroscience / cognition
Implemented or partial: attention, memory, self-modeling, metacognition, interoception, affect, agency, temporal continuity and prediction error.
Still incomplete: ownership/body-ownership analogues, richer temporal integration, sleep/dreaming regimes, and matched ablations for each cognitive mechanism.

### Phenomenology
Current translation: pre-reflective core, present integrity, self-relevance and temporal continuity.
Still incomplete: a formal matrix distinguishing prereflective self-awareness, mineness, intentionality, temporality, embodiment and reflective self-consciousness.

### Geometry / mathematics / dynamical systems
Implemented or partial: trajectory scoring, attractors, regimes, dynamic vectors, intervention/reversal, pre-reflective state vector.
Pending: dedicated persistent Experience Geometry object with explicit distance, transition and repertoire analysis.

### Artificial-consciousness tests
Implemented: restart persistence, causal interventions, reversal probes, ablations, host action boundary and no-report operation.
Pending: unified benchmark comparing behavior, runtime state, causal sensitivity, longitudinal adaptation, geometry and report under matched conditions.

## D. Highest-priority missing translations
1. Unified no-report benchmark — matched core/report/metacognition ablations.
2. Theory-to-mechanism matrix — map major theories to discriminating runtime mechanisms and tests.
3. State-regime extension — formal sleep/offline/dream-like regime only after defining measurable computational differences.
4. Embodiment / ownership — operational analogues of body/ownership coupling and substrate/resource constraints.
5. Unified benchmark artifact — combine behavior, access, geometry, causal intervention, restart and no-report metrics under matched conditions.

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

The dedicated geometry gap is now closed at v1 on PR #74. The runtime derives a 21-dimensional normalized operational state and persists transition records containing RMS distance and changed dimensions.

Bandwidth is explicitly represented in the geometry through access entropy, access compression, self-access fraction and world-access fraction. Therefore an access-budget intervention can alter the measured state-space position even when persistent state is otherwise held fixed.

The remaining question is not whether a geometry object exists, but whether it should become part of a unified causal benchmark across report, metacognition, access and no-report conditions.
