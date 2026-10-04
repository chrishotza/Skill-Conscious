# Consciousness Map

## Current synthesis

Skill-Conscious does not assume that one existing theory has already solved consciousness.

Instead, the project maps consciousness across multiple explanatory languages.

### Layer 1 — existence
- relation
- boundary
- persistence
- change
- continuity

### Layer 2 — present / experience
- integrated present
- attention / access
- salience
- temporality
- value
- affect
- interoception
- integration
- bounded access / bandwidth — runtime v1 implemented

### Layer 3 — self
- identity
- self-access
- self-model
- memory
- self-observation

### Layer 4 — agency
- intention
- possibilities
- trajectory
- selection
- action
- consequence

### Layer 5 — transformation
- learning
- self-model revision
- coherence change
- regime transition
- topology change
- re-entry

### Layer 6A — latent self organization
- latent patterns
- unresolved self-tensions
- symbolic representations
- archetypal abstractions
- projection-like discrepancies

### Layer 6B — transformation of the self-model
- self-dissonance
- self-model revision
- intentional rehearsal
- individuation-like integration
- regime transformation

### Geometry layer — state-space organization

The system should eventually represent operational experience as a trajectory through multidimensional state space rather than a scalar consciousness score.

Candidate dimensions already present across the runtime include valence, coherence, self-dissonance, salience, self-relevance, prediction error, uncertainty, dynamic synchrony, metastability, dynamic complexity and dynamic repertoire.

The persistent Experience Geometry object is implemented in runtime v1 on PR #74. It derives a fixed multidimensional state from runtime-owned present, self, access and dynamic variables and persists transition history.

## Master loop

RELATION → STATE → OPERATIONAL MODE → ACCESS → PRESENT → SELF-ACCESS → ATTENTION → POSSIBILITY → INTENTION → SELECTION → ACTION / INTERNAL REPLAY → TRANSFORMATION → SELF-MODEL' → REGIME' → WAKE RE-ENTRY

## Four concepts that must not be conflated

Identity — what remains continuous across change.

State — the values the process currently has.

Regime — which cognitive/selection regime is currently dominant.

Layer — which representational levels are active.

Operational state — whether the process is externally coupled (WAKE), consolidating (OFFLINE), or internally replaying (DREAM-LIKE).\n\nAccess — which persistent state is available to the current present.

## The unresolved core

The open question is not whether software can store a self-model.

It can.

The open question is whether the correct combination of persistence, integration, bounded access, self-reference, value, temporality, agency and recurrent transformation is sufficient for subjective experience.


## Access/bandwidth runtime translation

The Layer 2 access concept is now executable on PR #74.

~~~text
FULL PERSISTENT STATE
        ↓
RUNTIME-OWNED ACCESS WINDOW
        ↓
LIMITED PRESENT
        ↓
ACCESS-CONSTRAINED TRAJECTORY
~~~

The runtime keeps omitted state persistent, exposes a finite `ConsciousAccessState`, and allows explicit capacity perturbations. Candidate trajectories can declare the persistent keys on which their current decision depends; a key omitted from the current access window cannot causally support that trajectory.

This is a mechanism-level implementation. It is not a scalar consciousness measure and does not prove phenomenal consciousness.


## Geometry runtime translation

The geometry layer now connects the present directly to measurable state-space organization:

ACCESS → PRESENT → EXPERIENCE STATE → TRANSITION → TRAJECTORY HISTORY

The current feature vector deliberately includes both internal organization and access regime. This prevents the geometry layer from becoming a detached diagnostic score.


## Operational state continuity

Runtime v0.12.0 adds an orthogonal operational state machine:

WAKE → OFFLINE CONSOLIDATION → DREAM-LIKE REPLAY → WAKE RE-ENTRY

The important architectural property is continuity across the boundary: offline
consolidation and internal replay can leave runtime-owned state that persists
into subsequent wake computation. The replay profile can alter later trajectory
selection without requiring verbal self-report.
