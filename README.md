# Skill-Conscious

**Skill-Conscious is an experimental engineering and research project investigating persistent self-reference, continuity, integrated state, and causal trajectory selection in AI systems.**

The repository contains a software architecture and a falsifiable research program. It does **not** establish that the runtime or any tested system has phenomenal consciousness.

## Current status — 2026-10-09

- **Engineering:** the repository contains a persistent runtime, self-model interfaces, trajectory-selection mechanisms, tests, and research probes.
- **Corpus:** 4,315 effective claim records, 325 corpus units, 328 effective source IDs, and 19 source families in S01. Ledger coverage is not equivalent to passage-by-passage source verification.
- **S01:** the confirmatory coded and semantic outcomes plus 23 robustness conditions have been reported. The preregistered cross-family recurrence hypothesis was **not supported in its predicted direction**. The complete original run-output directories have not been recovered into the durable archive; see research/S01_RESULTS_STATUS_2026-10-09.md.
- **P008:** the self-model causal assay and prediction contract exist, but the recorded execution attempt was blocked by repository network/DNS access. **No P008 empirical result has been produced.**
- **Publication:** no paper is promoted to a completed empirical paper on the basis of a protocol, software implementation, or summary alone.

## Start here

For any AI or contributor entering the repository, follow this order:

1. **AGENTS.md** — operating rules, evidence discipline, and safe-change protocol.
2. **RESEARCH_MAP.md** — shortest repository navigation path.
3. **research/CURRENT_CHECKPOINT.md** — authoritative live research status.
4. **REPO_MEMORY.md** — durable context and anti-drift rules.
5. **research/README.md** — research operating system and evidence labels.
6. **research/S01_RESULTS_STATUS_2026-10-09.md** — latest S01 findings and artifact limitations.
7. **papers/README.md** — paper map and publication gate.
8. Read only the protocol, source, implementation, and tests relevant to the next unresolved step.

Do not read the whole repository indiscriminately. Do not infer that a study is complete merely because its protocol, code, or result summary exists.

## Core architecture

~~~text
WORLD / INPUT
     ↓
PRESENT WORKSPACE ↔ SELF / SELF-MODEL
     ↕                    ↓
   MEMORY             TRAJECTORY
                          ↓
                        ACTION
                          ↓
                OBSERVED CONSEQUENCE
                          ↓
                  SELF-MODEL UPDATE
                          ↓
                    NEXT CYCLE
~~~

The central engineering question is whether changes to a persistent self-model causally influence subsequent trajectory selection under controlled conditions. Verbal self-description alone does not satisfy that test.

## Runtime and implementation

The reference implementation is under src/, with portable Skill instructions under skills/skill-conscious/. The architectural definitions are in skills/skill-conscious/references/ARCHITECTURE.md and ONTOLOGY.md. The development plan is in docs/ADVANCE.md.

The smallest useful validation path is:

~~~bash
python -m pip install -e ".[dev]"
python -m pytest -q
~~~

Tests and experiments must be run in the relevant environment before claiming that the current commit passes them. GPU experiments are not part of the basic package test.

## Research program

The program separates three scales:

- **Individual:** persistent state, self-model causality, continuity, and trajectory selection.
- **Relational:** coupling and reciprocal effects across interacting agents.
- **Fundamental:** physical/ontological models only when they supply observable discriminators against alternatives.

These are research tracks, not established kinds or levels of consciousness. The current map is in docs/THREE_SCALE_CONSCIOUSNESS.md and docs/THREE_CONSCIOUSNESS_BRIDGE.md.

## Scientific boundaries

Every research artifact must distinguish source claims, project hypotheses, operational definitions, preregistered predictions, empirical results, inferences, and open questions. Retain negative and contradictory results. Do not present behavioral changes, self-model functionality, or persistence as proof of subjective experience.

## Canonical state files

A research-state change must update all three in the same change set:

- research/CURRENT_CHECKPOINT.md — live status.
- REPO_MEMORY.md — durable AI context.
- RESEARCH_MAP.md — traversal contract.

The research-sync-contract workflow enforces this synchronization on relevant pull requests. The detailed previous README is preserved at docs/README_RUNTIME_HISTORY_2026-10-09.md for historical reference only.
