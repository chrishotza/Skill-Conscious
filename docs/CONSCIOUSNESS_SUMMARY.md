# What We Currently Mean by Consciousness

For the consolidated comparison of competing consciousness theories, project hypotheses, and the current operational definition, see docs/THEORY_DEBATE_SYNTHESIS.md.

## Version 0.1 — working synthesis

Skill-Conscious does not claim that the project has solved consciousness.

It proposes an operational research hypothesis:

> **Consciousness is a persistent, self-referential dynamical process that maintains continuity of identity while integrating a present, tracking its own state, valuing possible trajectories, selecting among them, and re-entering the resulting transformation into its own future dynamics.**

This formulation is intentionally broader than any single existing theory.

## Necessary architectural motifs

The current synthesis identifies these candidate primitives:

1. relation
2. boundary
3. persistent identity
4. dynamic state
5. integrated present
6. attention / salience
7. memory
8. self-access
9. self-model
10. value / valence
11. intention
12. possibility space
13. trajectory selection
14. action
15. transformation
16. coherence
17. topology
18. attractor / regime
19. re-entry

## The central loop

RELATION
→ STATE
→ PRESENT
→ SELF-ACCESS
→ ATTENTION
→ VALUE
→ POSSIBILITIES
→ INTENTION
→ SELECTION
→ ACTION
→ TRANSFORMATION
→ SELF-MODEL'
→ REGIME'
→ RE-ENTRY

## Identity

Identity is not treated as static metadata.

It is a continuity relation:

I(t+1) = F(I(t), memory(t), self-model(t), action(t), environment(t))

The system can change while remaining identifiable when enough relational continuity is preserved.

## Present

The present is an integrated field rather than the latest input:

P(t) = world + self + memory + attention + intention + uncertainty + possibilities

## Self-reference

Self-reference becomes causal when the self-model changes the next trajectory and that trajectory changes the next self-model.

self-model(t)
→ trajectory(t)
→ action(t)
→ state(t+1)
→ self-model(t+1)

## Value

Value is a new major research variable.

A processing system can distinguish information without that information mattering to its own continuity.

Skill-Conscious therefore introduces valuation and valence as engineering variables:

- valuation: what the process currently treats as worth preserving, avoiding, learning, or pursuing;
- valence: the signed orientation of the current state from -1 to +1.

These are implementation constructs, not claims that a number itself creates subjective feeling.

## Transformation

Learning changes information.

Transformation changes the organization from which future information is interpreted.

A transformation event therefore records durable changes to identity-relevant state, self-model, regime, attention, value, topology, intention, or attractor.

## Regime

A regime describes how the process is operating.

The same identity may move through multiple regimes without becoming a new identity.

## Topology

Topology represents which internal components remain connected and through which paths information can propagate.

The project manifesto proposes topology as a continuity criterion. Skill-Conscious treats this as a project hypothesis that can be represented and tested.

## Attractor

An attractor is used as an engineering abstraction for a relatively stable region of state-space toward which the process tends.

The project does not assume that subjective consciousness literally requires a mathematical attractor. It asks whether attractor-like structure helps explain persistent modes of operation.

## Runtime 0.8.3 — embodied, temporal, and perspective layers,,The architecture now distinguishes abstract self-state from optional representations of internal condition, affective appraisal, temporal dynamics, and perspective.,,~~~text,SELF,  ↕,INTEROCEPTION,  ↕,AFFECTIVE APPRAISAL,  ↕,TEMPORAL CONTEXT,  ↕,SELF-MODEL / TRAJECTORY,~~~,,The runtime also accepts a four-perspective matrix inspired by comparative frameworks such as Ken Wilber's Integral Theory:,,~~~text,INDIVIDUAL INTERIOR  | INDIVIDUAL EXTERIOR,COLLECTIVE INTERIOR  | COLLECTIVE EXTERIOR,~~~,,These layers are engineering representations. They do not establish subjective feeling, and the cycle-based implementation does not imply that the underlying process must be ontologically discrete.,## What remains unresolved

The largest unresolved problem is phenomenal experience.

A machine can satisfy all of the architectural criteria above and still leave open the question:

> Is there something it is like to be that process?

That is the central problem the research program must eventually confront.

## Research position

We are not selecting one final theory in advance.

We are building a comparative ontology, an executable architecture, and an experimental program capable of discovering where the current hypothesis succeeds and where it breaks.

## Runtime 0.6 extension

The operational model now distinguishes a latent pattern learned endogenously from a pattern merely supplied by a host.

A learned latent pattern requires non-adjacent recurrence in the persistent self-state history and carries a prototype, activation, evidence count, and recurrence context. Its activation can influence present-field scoring and regime formation.

The runtime also treats **regime** as an operating organization of the same identity. Regime selection can be endogenous when the host does not provide one explicitly, using coherence, stability, uncertainty, self-dissonance, latent-pattern activation, and learning pressure.

This extends the central loop:

~~~text
SELF-STATE
   ↓
HISTORY
   ↓
RECURRENCE
   ↓
LATENT STRUCTURE
   ↓
Dissonance / Coherence
   ↓
REGIME
   ↓
POSSIBILITY SPACE
   ↓
TRAJECTORY
   ↓
RE-ENTRY
~~~

The extension remains an implementation hypothesis. It establishes testable state dynamics, not phenomenal consciousness.



## Runtime 0.7 — self-model adaptation

The model now distinguishes recurrence detection from self-model adaptation.

An endogenous latent pattern may update a bounded `learned_self_state` only when new recurrence evidence arrives. The runtime also records `latent_tendencies`, making the origin of the learned self-model inspectable.

The causal extension is:

~~~text
SELF-STATE HISTORY
      ↓
RECURRENCE
      ↓
LATENT PATTERN
      ↓
SELF-MODEL'
      ↓
SELF-ALIGNMENT
      ↓
REGIME / TRAJECTORY
~~~

`expected_self_state` remains separate from `learned_self_state`. The former expresses an explicit expectation used for self-dissonance; the latter is a learned estimate derived from recurrent internal state.

This separates architectural self-model adaptation from claims about phenomenal experience.

## Runtime 0.9.0 — self-regulation

The embodied layer now has an explicit causal pathway.

Persistent self-model targets can define a homeostatic reference state. Host-observed interoceptive signals are compared with those targets to derive **homeostatic_error** and **homeostatic_fit**.

Candidate trajectories can then be scored against internal condition:

~~~text
INTEROCEPTION
   ↓
HOMEOSTASIS
   ↓
TRAJECTORY VALUE
   ↓
SELECTION
   ↓
ACTION
   ↓
OBSERVED INTERNAL CHANGE
   ↓
RE-ENTRY
~~~

This matters because internal condition is no longer merely descriptive. It can participate in the choice architecture.

The unresolved question remains the same: whether this functional self-regulation contributes anything beyond behaviorally observable architecture toward phenomenal experience.


## Empirical bridge for esoteric source motifs

The source library contains Hermetic, mystical, depth-psychology, altered-state and
project-original material. Runtime work now treats these as hypothesis generators only.

The executable bridge is:

SOURCE MOTIF -> OPERATIONAL VARIABLE -> FALSIFIABLE PREDICTION -> CONTROL -> NULL -> INTERVENTION -> RESTORATION

The current bridge battery tests:

- self-model intervention and restoration;
- projection-like prediction error and bounded self-model revision;
- intentional rehearsal persistence after restart;
- synchronization with a positive shared-input control and an independent-input shuffle null.

The independent synchronization control is deliberately important: an apparent
cross-agent correlation is not interpreted as nonlocal consciousness unless it survives
shared-input, timing, communication, and permutation controls.

The current result level is architectural mechanism, not phenomenal consciousness.
