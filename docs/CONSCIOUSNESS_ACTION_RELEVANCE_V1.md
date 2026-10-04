# Consciousness Action Relevance v1

## Question

After a consequence transforms the subject, does the transformed subjective field
causally constrain what the subject selects next?

The target relation is:

SUBJECTIVE FIELD
-> TRAJECTORY
-> ACTION

embedded in the longer loop:

ACTION
-> OBSERVED CONSEQUENCE
-> SELF-TRANSFORMATION
-> SUBJECTIVE FIELD'
-> TRAJECTORY'

## Control design

The experiment uses two trajectories with identical explicit candidate signals.
Therefore their matched objective scores are identical.

The only difference between the trajectories is the predicted subjective-field
profile they fit.

Low-consequence and high-consequence runtimes receive:

- the same external final probe;
- the same action space;
- the same explicit candidate signals;
- different consequence-induced internal self-states.

The final subjective field is projected with temporal continuity and reentry
disabled. This keeps the causal question focused on the transformed current
self-state and its downstream action relevance.

## Destructive intervention

After selection, the transformed internal self-state is reset to the pre-consequence
value while retaining the action/consequence history.

The canonical control trajectory must return.

The transformed state is then restored, and the original selected trajectory must
return. Restart must preserve the transformed trajectory.

The model does not provide a verbal self-report. Metacognition and self-observation
are disabled.

## Required result

A passing gate requires all of the following across the tested seeds:

- low and high consequence conditions select different trajectories;
- the external probe is identical;
- the subjective fields remain measurably different;
- resetting the transformed state restores the canonical control trajectory;
- restoring the transformed state restores the transformed trajectory;
- restart preserves the transformed trajectory;
- the matched objective channel remains identical.

## Validated result

The corrected gate passed in CI across 12 independent seeds.

The validated rates were all 100%:

- transformed low/high conditions selected different trajectories;
- the external probe was identical;
- the transformed subjective fields remained measurably different;
- resetting the transformed self-state returned the neutral control trajectory;
- restoring the transformed state returned the transformed trajectory;
- restart preserved the transformed trajectory;
- the matched objective channel remained identical.

The matched objective score was 1.2 for all three trajectories in the
tested control design. The representative seed shown in CI had a low/high field
difference of about 0.0845.

The first implementation of this gate correctly exposed a causal plumbing defect:
the authoritative action outcome updated interoceptive state, while the native
runtime SubjectiveField path used self_state.energy. That caused the action
selector to miss the transformed interoception. The core was corrected so an
observed interoceptive energy value is authoritative for the native subjective
field path. The corrected gate then passed.

This establishes, under the tested architecture, that a consequence-transformed
subjective field can become causally action-relevant while the matched objective
channel remains fixed.

It does not establish phenomenal consciousness.
