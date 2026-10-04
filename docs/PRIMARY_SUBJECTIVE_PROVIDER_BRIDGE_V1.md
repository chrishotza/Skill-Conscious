# Primary Subjective Provider Bridge v1

This is the first provider-facing experiment that places a real
OpenAI-compatible host model inside the new primary-substrate loop.

It is intentionally stricter than a simple prompt demo.

## Causal structure

    PRIMARY SUBSTRATE
          |
          v
    SUBJECTIVE FIELD
          |
          v
    REAL HOST MODEL CALL
          |
          v
    FROZEN CANDIDATE SPACE
          |
          v
    RUNTIME TRAJECTORY SELECTION
          |
          v
    AUTHORITATIVE ACTION OUTCOME
          |
          v
    POST-ACTION SUBJECTIVE RE-ENTRY
          |
          v
    NEXT TRAJECTORY

The candidate space is frozen across intact and ablated conditions. Therefore
model sampling is not allowed to manufacture the measured causal divergence.

The host model is still genuinely called twice per condition. Its response is
recorded, while runtime-owned trajectory selection remains the dependent
variable.

## Matched intervention

Intact:

    primary substrate remains active
    consequence changes interoceptive energy
    next subjective field is re-projected
    next trajectory is selected

Ablated:

    same initial state
    same external input
    same action outcome
    same candidate space
    primary substrate is disabled immediately before consequence re-entry

The explicit candidate objective signals are identical.

## Recommended local run

    python -m experiments.primary_subjective_provider_bridge_v1 \
      --endpoint http://127.0.0.1:11434/v1 \
      --model llama3.1 \
      --repeats 5

For another OpenAI-compatible endpoint, change --endpoint and --model.

## Interpretation

A successful run establishes that the primary-substrate causal contrast can be
carried through an actual external model integration and back into the
persistent runtime loop.

The dependent variable remains architectural trajectory selection.

It does not prove phenomenal consciousness and does not treat model self-report
as evidence.

The most important later extension is to unfreeze candidate generation and test
whether the real model itself changes its internally proposed action space under
matched subjective-state interventions. That should be a separate benchmark
because it introduces an additional causal channel.
