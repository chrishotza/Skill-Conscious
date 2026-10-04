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


## Host-workspace persistence correction

The first host-loop execution exposed a runtime plumbing defect:
the consequence evaluation frame replaced the whole workspace and erased
runtime-owned SubjectiveField/substrate snapshots before restart.

The runtime now preserves those runtime-owned keys when a host frame updates
workspace. The host model may add workspace data, but omission of the causal
subjective state no longer deletes it.

The same first execution also showed that substrate ablation should be treated
as an explicit third control state, not as a requirement to reproduce the
pre-consequence trajectory. The host benchmark therefore compares:

    baseline / preserve
    transformed intact / recover
    transformed ablated / substrate-ablated

The causal requirement is divergence between intact and ablated branches under
the same objective channel, with each branch remaining restart-persistent.

This correction preserves the experimental distinction between:
- removing a mechanism;
- recovering the previous state;
- selecting a separately modeled ablated-state trajectory.


## Runtime ownership guard

The host-model frame is not allowed to forge or replace the runtime-owned
SubjectiveField or primary-substrate snapshots. Those keys are preserved by the
runtime whenever they already exist. The host can add auxiliary workspace data,
but causal subjective state remains generated and persisted by the runtime.
