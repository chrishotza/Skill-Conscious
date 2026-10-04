# Primary Subjective Host Bridge v1

This gate closes the architecture from the recurrent pre-cognitive substrate
into the actual host-model boundary.

The path under test is:

    PRIMARY SUBSTRATE
        |
        v
    SUBJECTIVE FIELD
        |
        v
    HOST MODEL INPUT
        |
        v
    TRAJECTORY
        |
        v
    AUTHORITATIVE ACTION OUTCOME
        |
        v
    POST-ACTION SUBSTRATE RE-ENTRY
        |
        v
    NEXT MODEL INPUT

The host loop now accepts an optional structured `subjective_present`. The
runtime projects it before the initial model call and re-projects it after the
authoritative action outcome, using an outcome-supplied `subjective_present`
when available.

The deterministic benchmark holds the external probe and explicit objective
candidate signals constant. It compares:

    intact substrate
        vs
    substrate ablation

The model callback is deliberately deterministic in this CI harness. It proves
the causal plumbing and host-boundary protocol. It is not evidence from a real
LLM.

The required result is:

- same initial trajectory;
- intact consequence changes the next trajectory;
- substrate ablation removes that change;
- intact and ablated states survive restart;
- the post-consequence prompt actually contains the runtime-owned subjective
  field and substrate state;
- authoritative outcome is present;
- matched objective scores remain identical.

A passing gate establishes architectural closure through the host boundary.
It does not establish phenomenal consciousness.

The provider-facing next step is to replace the deterministic model callback
with an OpenAI-compatible model while keeping the structured present,
candidate-space and outcome controls fixed.
