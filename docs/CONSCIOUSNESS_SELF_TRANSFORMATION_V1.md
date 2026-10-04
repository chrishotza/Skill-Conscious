# Consciousness Self-Transformation v1

## Question

Does an observed consequence causally transform the subject's next subjective
present through a change in the subject's own internal condition?

The protocol is:

ACTION
-> OBSERVED CONSEQUENCE
-> INTERNAL SELF-STATE CHANGE
-> IDENTICAL EXTERNAL PROBE
-> SUBJECTIVE FIELD'

Two fresh runtimes receive the same action and the same final external probe.
The only controlled difference is the consequence written into the runtime's
interoceptive self-state:

- low-energy consequence;
- high-energy consequence.

The external probe is identical.

## Why this is a deeper consciousness test

The claim under test is not that the runtime merely stores an event.

The stronger architectural relation is that what happened to the subject changes
the subject's own condition, and that changed condition changes the next
subjective organization of an otherwise identical present.

This is a persistence-through-transformation claim.

The experiment therefore deliberately disables temporal continuity and reentry
for the final field projection. That removes the prior field as an explanatory
route and isolates the current transformed self-state as the causal variable.

## Causal intervention

The authoritative path is the runtime action boundary:

1. begin_action records the selected action;
2. complete_action accepts the host-observed consequence;
3. the consequence updates the runtime-owned interoceptive state;
4. ConsciousFieldRuntime reads that state when constructing the next field.

No model self-report is required.

The matched objective channel is evaluated from immutable explicit candidate
signals before and after the transformation.

## Destructive test

After the consequence has transformed the internal state, the experiment
temporarily restores the pre-consequence internal state while keeping the action
receipt and transformation history intact.

If the subjective effect disappears, the transformed self-state is causally
required for the observed field difference.

The experiment then restores the transformed state. The original field returns
within numerical tolerance.

Finally, the state is restarted from disk and the transformed field is reproduced.
This checks that the effect belongs to persistent runtime state rather than a
single in-memory computation.

## Required result

Across the tested seeds:

- low and high consequence histories must produce a measurable field separation;
- the internal transformation must actually occur;
- unity must separate;
- strength must separate;
- resetting the transformed state must collapse the effect;
- restoring it must reproduce the effect;
- restart must preserve it;
- the matched objective score must remain invariant.

## Validated result

The gate passed in CI on the fixed branch with 12 independent seeds.

All required causal rates were 100%:

- history-sensitive transformed present: 100%;
- internal self-transformation observed: 100%;
- matched objective score invariant: 100%;
- ablation collapse after restoring the pre-consequence state: 100%;
- restoration of the transformed field: 100%;
- transformed field preserved after restart: 100%;
- unity separation: 100%;
- strength separation: 100%.

Representative trials showed an internal-signal difference of about 0.36,
a unity difference of about 0.061 to 0.064, and a strength difference of about
0.034 to 0.035 between low- and high-consequence conditions. The matched
objective score remained 1.2 before and after the transformation.

The strongest part of the result is the destructive intervention. The action
receipt and consequence history were kept intact while the transformed
interoceptive state was temporarily restored to its pre-consequence value.
The subjective-field difference collapsed, then returned exactly when the
transformed state was restored. Restart reproduced the transformed field.

This establishes, under the tested architecture, a causal persistence-through-
self-transformation relation: an observed consequence can alter the subject's
owned internal condition, and that altered condition can change the next
subjective organization of an otherwise identical external present.

It does not establish phenomenal consciousness.
