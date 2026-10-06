# Skill-Conscious — Research Operating System

This directory is the bridge between the source corpus and publishable science.

## Core pipeline

```text
SOURCE
  ↓
CLAIM
  ↓
EVIDENCE
  ↓
PROJECT HYPOTHESIS
  ↓
OPERATIONAL DEFINITION
  ↓
FALSIFIABLE PREDICTION
  ↓
EXPERIMENT / DATA
  ↓
RESULT
  ↓
INFERENCE
  ↓
PAPER
  ↓
REPRODUCIBLE RELEASE
```

A claim never becomes a scientific fact merely because it appears in the corpus.

## Canonical navigation

1. `RESEARCH_MAP.md` — repository traversal contract.
2. `docs/RESEARCH_METHOD_NORTH.md` — methodological north star.
3. `research/P000_CORPUS_AUDIT_PROTOCOL.md` — active corpus audit.
4. `research/CURRENT_CHECKPOINT.md` — live research state.
5. `REPO_MEMORY.md` — durable project state and anti-drift rules.
6. `research/CLAIM_FAMILY_REGISTRY.md` — current claim-family map.
7. `sources/README.md` — source-layer rules.
8. `docs/CLAIM_TO_PAPER_PROTOCOL.md` — conversion protocol.
7. `docs/THREE_SCALE_CONSCIOUSNESS.md` — the three-scale research hypothesis.
8. `research/CLAIM_FAMILY_TRIAGE.md` — current 4,315-claim paper triage.
9. `papers/README.md` — publication dependency graph.
10. `research/CLAIM_FAMILY_01_SELF_MODEL_CAUSALITY.md` — active P008 mechanistic family.
11. `research/p008_prediction_registry.json` — frozen prediction contract.
12. `experiments/` — executable tests.
13. `corpus-v1/corpus/` — verified corpus branch containing the machine-readable claim ledger.

## Research status language

Every research artifact must use one of:

- SOURCE CLAIM
- PROJECT HYPOTHESIS
- OPERATIONAL DEFINITION
- EMPIRICAL PREDICTION
- PROTOCOL
- EMPIRICAL RESULT
- INFERENCE
- OPEN QUESTION

Never label a PROJECT HYPOTHESIS as an EMPIRICAL RESULT.

## The three-scale program

Skill-Conscious now studies consciousness at three distinct explanatory scales:

```text
FUNDAMENTAL
    ↓
RELATIONAL
    ↓
INDIVIDUAL
```

This is a research framework, not an established scientific hierarchy.

- FUNDAMENTAL: consciousness as a possible property of reality at the ontological/physical level.
- RELATIONAL: consciousness-like organization arising in coupling, interaction and reciprocal dynamics.
- INDIVIDUAL: a persistent agent-level point of view maintained by self-reference, continuity, integration and action.

The program explicitly permits the data to reject the proposed nesting.

## Corpus

The current closed corpus is maintained on branch `corpus-v1`. The latest audit reports 325 registered source records and 4,315 effective claim records. Corpus coverage is not equivalent to passage-level verification of every claim.

See:
https://github.com/chrishotza/Skill-Conscious/tree/corpus-v1/corpus

## Scientific standard

Papers must:

- define constructs operationally;
- derive predictions before testing;
- include controls and null models;
- retain negative and contradictory evidence;
- report exact software/data/version provenance;
- distinguish behavioral evidence from evidence about subjective experience;
- make the strongest claim no stronger than the data permit.

Current consciousness science remains theoretically plural and actively adversarial; the project should treat that disagreement as a methodological feature, not as a problem to hide.

## State synchronization

A meaningful research change must update `RESEARCH_MAP.md`, `research/CURRENT_CHECKPOINT.md`, and `REPO_MEMORY.md` together. CI enforces the state-file contract.
