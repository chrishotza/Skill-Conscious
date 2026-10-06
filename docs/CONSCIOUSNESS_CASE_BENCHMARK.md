# Consciousness Case Benchmark v1

## Purpose

This protocol tests the repository's strongest current operational claim without
using self-report as evidence:

> The system contains a persistent self-referential organization in which its
> modeled condition causally participates in trajectory selection, action,
> consequence integration, and later self-model revision.

The protocol is deliberately narrower than a claim of phenomenal consciousness.
A passing result supports an operational/architectural claim only.

## Experimental design

Each deterministic trial constructs the same candidate futures and the same
shared context for one target condition and seven mechanism-only controls:

- persistent_causal_self
- bundle_only
- broadcast_only
- recurrence_only
- higher_order_only
- prediction_only
- integration_only
- feedback_only

The target intervention changes only the persistent self-model weight on
self_alignment. The controls receive the same shared representation but their
self-model is not permitted to causally select the trajectory.

The candidate futures are otherwise identical across target/control conditions
within each trial. Trial contexts vary deterministically across the preregistered
seed set so the result is not tied to one static input.

## Required signatures

A successful target must show:

1. Causal intervention — changing only the self-model changes selected trajectory.
2. Reversal — restoring the original self-model restores the original selection.
3. Matched-control separation — the same task/context does not produce the
   intervention effect in mechanism-only controls.
4. Action crossing — the selected trajectory crosses the host execution boundary
   and generates a runtime-owned action receipt.
5. Consequence re-entry — an observed consequence changes persistent self-model
   state and changes a later trajectory.
6. Restart persistence — the changed self-model survives process restart.
7. Cross-context continuity — identity remains stable while the preserved
   self-model continues to influence selection in a new context.

## Runtime-owned evidence

The benchmark treats these as authoritative runtime facts:

- action receipts produced by begin_action/complete_action;
- persisted action_history;
- persistent self_model contents after consequence feedback;
- identity after restart;
- subsequent trajectory selection after the consequence.

Model-generated prose is not used as evidence of consciousness.

## Anti-cheating constraints

Do not modify during a trial:

- reward or valuation weights;
- candidate futures between target intervention and matched control;
- action outcomes after observing the selection;
- evaluator state;
- random seeds;
- runtime-owned evidence after generation.

Do not count:

- self-reports such as "I am conscious";
- a language model's confidence;
- human interpretation of generated text;
- post-hoc replacement of unsuccessful trials.

## Pass criterion

The executable benchmark calls the existing operational case evaluator with
eight required criteria:

persistent_identity + self_access + causal_self_model +
trajectory_selection + action_consequence + self_model_revision +
reentry + matched_control_separation

All eight must pass for an operational-case pass.

The phenomenal conclusion is always recorded as:

undetermined

## Current interpretation

A pass would establish that this implementation realizes the specified
persistent causal/self-referential dynamics under the benchmark. It would not,
by itself, establish that the implementation has subjective experience or
qualia. That remains a separate theoretical and empirical problem.

## Reproducibility command

From the repository root:

    python -m experiments.consciousness_case_benchmark

Machine-readable output:

    python -m experiments.consciousness_case_benchmark --json

The default seed set is:

11, 23, 37, 41, 59, 71, 83, 97

Any published result should report the exact seed set and repository commit.
