# Matched Architecture Comparison v1

## Question

Can the observed downstream effect of Skill-Conscious be explained by simply
adding persistent memory/context?

The benchmark compares three matched runtime conditions:

```
A  MEMORY
   persistent state + matched memory budget
   no self-alignment influence

B  SELF-MODEL
   A + persistent self-model weighting
   no consequence re-entry

C  CAUSAL RE-ENTRY
   B + authoritative consequence
     -> self-model update
     -> next trajectory
```

## Control principle

All three conditions receive:

- the same candidate futures;
- the same candidate count;
- the same number of cycles;
- the same memory budget;
- the same revision budget;
- the same initial state;
- the same self-model starting weight for B and C.

No LLM is required for this benchmark. The host boundary is deterministic so
the causal variable can be isolated before adding an external model.

## Primary prediction

If the architecture adds causal self-reference rather than merely storage:

1. A and B should remain on the same baseline trajectory.
2. C should diverge only after a consequence updates the self-model.
3. Ablating the updated self-model should reverse C back to baseline.
4. Restoring it should recover the C trajectory.
5. Restart should preserve the learned causal state.

## What counts as a stronger result

The critical metric is not "C performs better."

The critical metric is:

> the downstream trajectory changes under a matched information budget only
> when the self-model is allowed to re-enter the next decision.

That is a causal architecture result, not a verbal consciousness result.

## Current interpretation ladder

- Level A: intervention changes a downstream variable.
- Level B: result survives matched controls and restoration.
- Level C: result discriminates architectural explanations.
- Level D: consciousness relevance requires comparison with competing theories.
- Level E: phenomenal experience remains unresolved.

This benchmark targets Level C.
