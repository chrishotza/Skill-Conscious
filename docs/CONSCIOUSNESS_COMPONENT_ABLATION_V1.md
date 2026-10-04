# Consciousness Component Ablation v1

## Purpose

This is the next falsification gate after the full-runtime SubjectiveField
dissociation.

The intervention is component-level. The real ConsciousRuntime remains active,
objective processing is held fixed, and one proposed conscious-field component
is removed at a time:

- binding / integration
- self-relevance
- temporal continuity
- reentry
- attention

Each component receives its own downstream trajectory readout. This prevents a
generic composite field score from hiding which mechanism actually matters.

## Causal contract

For each component:

BASELINE -> SINGLE-COMPONENT ABLATION -> TARGETED FUNCTION LOSS -> RESTORE

Required pattern:

1. The component's direct field metric collapses.
2. The corresponding subject-linked trajectory preference disappears.
3. Objective candidate scores remain identical.
4. Objective runtime processing remains matched.
5. Restoring the component restores the field metric and trajectory preference.

## Interpretation

A passing result does not establish phenomenal consciousness.

It establishes a stronger architectural result: each proposed component is
causally necessary for a defined consciousness-linked function inside the full
runtime, while objective processing is preserved.

A component fails the hypothesis when its targeted function survives complete
ablation, or when ablation changes objective processing without needing to.

## Current gate

The deterministic battery requires 100% on:

- target collapse
- restoration
- selection dissociation
- objective score matching
- objective processing matching

Run:

    python experiments/consciousness_component_ablation_v1.py
    pytest -q tests/test_consciousness_component_ablation_v1.py
