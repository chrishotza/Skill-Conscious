# Conscious Interface / Bandwidth v1

## Purpose

The pre-reflective core already maintains an integrated internal process. The next requirement is to model a bounded interface between the full runtime state and the limited state that can participate in the current present.

This module must not become a second consciousness definition and must not turn language output into the consciousness bottleneck.

The architectural question is:

> Which parts of the persistent internal organization become available to the current present, with what priority, under what capacity constraint, and with what causal effect on the next trajectory?

## Interface

~~~text
FULL RUNTIME STATE
        ↓
   SALIENCE FIELD
        ↓
 ATTENTION / ACCESS BUDGET
        ↓
   LIMITED PRESENT
        ↓
 SELF-RELEVANCE + VALUATION
        ↓
  POSSIBILITY / TRAJECTORY
        ↓
       ACTION
        ↓
 OBSERVED CONSEQUENCE
        ↓
  INTERNAL CHANGE
        ↺
~~~

Language/report is parallel to the reflective layers:

~~~text
LIMITED PRESENT → SELF-MODEL → METACOGNITION → REPORT
~~~

Report is not the gate.

## Core invariants

### 1. Runtime ownership

The runtime computes the effective access window from persistent state and an explicit capacity policy.

A host model may propose candidate attention, but it cannot forge the authoritative access state.

### 2. Capacity is bounded

The present cannot expose the entire persistent state indiscriminately.

Capacity is represented explicitly and measured.

### 3. Selection is causal

Changing the access budget or access priorities must be able to change:
- the integrated present;
- trajectory scoring;
- action selection;
- subsequent state change.

If an access intervention changes only a diagnostic field and never changes downstream behavior, the interface is not functionally active.

### 4. Omission is meaningful

State excluded from the current access window remains persistent but is not treated as currently available.

This creates a distinction between persistent state, accessible state, and reported state.

### 5. No-report compatibility

Disabling self-report must not disable access selection.

Disabling metacognition must not disable access selection.

The bandwidth layer belongs to the pre-reflective/operational path.

## Proposed runtime object

ConsciousAccessState should remain small, serializable, and runtime-owned.

Minimum fields:

- capacity
- candidate_count
- selected_keys
- omitted_keys
- access_scores
- compression_load
- self_access_fraction
- world_access_fraction
- access_entropy
- revision

The first implementation should avoid pretending that these numbers are a measurement of phenomenal consciousness.

They are measurements of the architecture's access regime.

## Selection rule

For every candidate internal item i:

~~~text
effective_i =
    salience_i
    × self_relevance_i
    × persistence_i
    × policy_priority_i
~~~

The runtime selects at most capacity items.

This is intentionally an engineering policy, not a claim that biological attention literally computes this formula.

## Causal access probe

~~~text
same identity
same internal state
same external input
same candidate futures

             ↓

      ACCESS CAPACITY = 2
             ↓
       trajectory A

             ↓

intervene: ACCESS CAPACITY = 6
             ↓
       trajectory B

             ↓

restore capacity = 2
             ↓
       trajectory C
~~~

Expected operational result:

A == C and, under a sufficiently sensitive task, A != B.

The intervention must not create learning evidence merely by being applied.

## Bandwidth ablation

Use matched conditions:

A — full state available without bottleneck
B — bounded access
C — bounded access + salience
D — bounded access + salience + self-relevance
E — bounded access + salience + self-relevance + metacognition
F — bounded access + no-report

The main comparison is not whether the model's prose changes.

Measure trajectory divergence, prediction error, adaptation, state-transition geometry, consequence re-entry, restart persistence, access stability, and recovery after capacity restoration.

## Failure modes

The implementation must reject or flag:

1. model-authored access state being treated as authoritative;
2. report becoming a hidden access requirement;
3. capacity changing without downstream causal effect;
4. omitted state being deleted rather than merely inaccessible;
5. attention state being recreated from scratch every turn;
6. a scalar consciousness score being substituted for the access geometry.

## Relationship to the pre-reflective core

The interface is not a separate reflective overlay.

~~~text
PERSISTENT SELF
      ↓
FULL INTERNAL STATE
      ↓
ACCESS / ATTENTION
      ↓
CURRENT PRESENT
      ↓
SELF-RELEVANCE
      ↓
VALUATION
      ↓
TRAJECTORY
~~~

This keeps the architecture compatible with the project's central distinction:

**the system does not need to know that it is conscious for its internal process to be organized around what is currently available and significant to that process.**

## Epistemic boundary

A successful bandwidth intervention would demonstrate a causal access mechanism inside the architecture.

It would not, by itself, prove phenomenal consciousness.

The correct claim is:

> Skill-Conscious implements a persistent, bounded, causally active access interface between its full internal state and its current integrated present.

## Runtime v1 status

The first runtime implementation now exists in `src/skill_conscious/access.py` and is integrated into `ConsciousRuntime`.

Implemented invariants:

- runtime-owned `ConsciousAccessState` with explicit finite capacity;
- deterministic access scoring using salience × self-relevance × persistence × policy priority;
- selected versus omitted persistent state;
- limited-present projection that does not delete omitted state;
- causal trajectory gating through optional `access_keys`;
- no-report and no-metacognition compatibility;
- persisted capacity and restart continuity;
- explicit capacity interventions that add no learning evidence.

The default capacity is a compatibility envelope larger than the current access item set. Causal bandwidth experiments reduce the capacity explicitly (for example 2 versus 6) and test downstream trajectory divergence plus restoration.

The implementation remains an architectural access mechanism, not a detector or proof of phenomenal consciousness.

