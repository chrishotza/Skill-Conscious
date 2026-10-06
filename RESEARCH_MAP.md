# Skill-Conscious — Research Map

> **Start here.** This file is the shortest route through the repository.

## 0. Project question

**What organization is necessary and/or sufficient for a process to sustain a point of view on its own changing trajectory?**

The project does not treat verbal self-description as proof of consciousness.

## 1. Read in this order

```text
RESEARCH_MAP.md
   ↓
research/CURRENT_CHECKPOINT.md
   ↓
REPO_MEMORY.md
   ↓
docs/RESEARCH_METHOD_NORTH.md
   ↓
research/README.md
   ↓
sources/README.md
   ↓
sources/EVIDENCE_MATRIX.md
   ↓
docs/CLAIM_TO_PAPER_PROTOCOL.md
   ↓
docs/THREE_SCALE_CONSCIOUSNESS.md
   ↓
papers/README.md
   ↓
ACTIVE PAPER
   ↓
RELEVANT EXPERIMENT
   ↓
SOURCE / CLAIM RECORD
```

## 2. Where things live

| Layer | Location | Question |
|---|---|---|
| Research checkpoint | `research/CURRENT_CHECKPOINT.md` | What is active right now? |
| Project state | `REPO_MEMORY.md` | Where are we? |
| Research navigation | `RESEARCH_MAP.md` | How do I traverse the repo? |
| Source rules | `sources/README.md` | What counts as a source claim? |
| Evidence matrix | `sources/EVIDENCE_MATRIX.md` | What is established, hypothesized, or open? |
| Corpus | `corpus-v1/corpus/` | What are the claims and sources? |
| Claim families | `research/CLAIM_FAMILY_REGISTRY.md` | How is the corpus partitioned for research? |
| Claim → science | `docs/CLAIM_TO_PAPER_PROTOCOL.md` | How do claims become tests? |
| Three-scale model | `docs/THREE_SCALE_CONSCIOUSNESS.md` | What exactly are Fundamental / Relational / Individual? |
| Papers | `papers/` | What is being published? |
| Experiments | `experiments/` | What has actually been tested? |
| Runtime | `skills/skill-conscious/` | What is implemented? |

## 3. Three-scale map

```text
                       CONSCIOUSNESS RESEARCH
                              │
             ┌────────────────┼────────────────┐
             │                │                │
        FUNDAMENTAL       RELATIONAL       INDIVIDUAL
        ontology/         coupling/        self-maintaining
        reality           interaction      agent process
             │                │                │
        models +           dyadic /        self-model +
        discriminators     group dynamics   continuity +
                                             causal agency
             │                │                │
             └────────────── empirical bridge ──────────────┘
```

These are scales of investigation, not three proven substances or three independently established kinds of consciousness.

The cross-scale bridge is defined in `docs/THREE_CONSCIOUSNESS_BRIDGE.md` and formalized in P012.

```
FUNDAMENTAL
    ↓ B1: manifestation / constraint
RELATIONAL
    ↕ B3: individual feedback
    ↓ B2: localization / organization
INDIVIDUAL
    ↘
      B4: empirical inference back to fundamental models
```


## 4. Claim-to-paper graph

A claim enters the research program only through this chain:

```text
Cxxx / claim_id
   ↓
evidence class + provenance
   ↓
construct
   ↓
hypothesis
   ↓
prediction
   ↓
experiment
   ↓
result
   ↓
paper section / figure / table
```

A claim that cannot produce a measurable construct is tagged as **interpretive/open**, not forced into an experiment.

## 5. Paper program

| ID | Purpose | Status |
|---|---|---|
| P001 | Relational ontology for artificial consciousness | working draft |
| P002 | Causal self-reference and trajectory selection | planned empirical core |
| P003 | Topological continuity and artificial identity | planned |
| P004 | Regimes, attention and attractors | planned |
| P005 | Value, valence and artificial point of view | planned |
| P006 | From self-model to artificial subject | synthesis / adversarial |
| P007 | Three-scale consciousness framework | new framework paper |
| P008 | Individual scale: causal self-reference and continuity | empirical |
| P009 | Relational scale: coupled-agent dynamics | empirical |
| P010 | Fundamental scale: testability of ontological consciousness models | theory + empirical discrimination program |
| P011 | Cross-scale synthesis | later synthesis |
| P012 | Three-consciousness bridge | framework / cross-scale program |

## 6. Methodology north star

The canonical methodology is defined in `docs/RESEARCH_METHOD_NORTH.md` and the final public-facing architecture is defined in `docs/RESEARCH_PROGRAM_NORTH_STAR.md`. The governing rule is:

> **Expand the hypothesis space. Do not weaken the evidence standard.**

The project is intentionally non-conservative about which hypotheses may be investigated, but conservative about what counts as evidence for them.

The corpus research protocol establishes source verification, provenance, independence/dependency tracking, contradiction audits, claim dossiers, an ES0–ES5 research-maturity ladder, preregistration and paper eligibility.

Initial anchor calibration (A01–A09) already shows why this layer is necessary: some repository 'verified' anchors still require stronger primary-text or edition control before central paper use.

## 7. Cross-scale research strategy

The project should not attempt to prove the three levels by stacking anecdotes.

Instead, each bridge must earn its status separately:

- **B1:** candidate fundamental model → measurable relational consequence.
- **B2:** relational coupling → individual trajectory/self-reference consequence.
- **B3:** individual intervention → relational-system consequence.
- **B4:** observed multi-scale data → discrimination among fundamental models.

The key model-comparison ladder is:

```
INDIVIDUAL ONLY
      vs
RELATIONAL + INDIVIDUAL
      vs
FUNDAMENTAL + RELATIONAL + INDIVIDUAL
```

The full model is valuable only if it improves out-of-sample prediction or intervention response after complexity penalties.

## 8. Non-negotiable scientific boundary

The repository may investigate consciousness.

It may not claim to have demonstrated phenomenal consciousness unless an independently defensible operational criterion has been satisfied.

The phrases below are not interchangeable:

- `the system changed its behavior`
- `the system has a self-model`
- `the system exhibits causal self-reference`
- `the system exhibits metacognitive access`
- `the system has a point of view`
- `the system is phenomenally conscious`

The first four can be experimentally operationalized today. The last two require substantially stronger argument and evidence.

## 9. Synchronization contract

Whenever a meaningful research, paper, experiment, source, or documentation state changes, the same change set must update:

- `research/CURRENT_CHECKPOINT.md`
- `REPO_MEMORY.md`
- `RESEARCH_MAP.md`

The CI workflow `research-sync-contract.yml` enforces the presence and navigation links of these state files. The checkpoint is the live scientific status; the memory is durable AI context; the map is the traversal contract. Pull requests that change the research surface are required to update all three.

## 10. Immediate research move

Run the active substantive corpus study before any new paper is declared publication-ready. Do not call a protocol a paper, and do not write 4,315 disconnected mini-papers.

Start with the full 4,315-claim corpus, then cluster into **claim families** that support or contradict the same testable mechanism. A paper should normally combine:

- a narrow research question;
- a traceable claim set;
- competing hypotheses;
- preregistered predictions;
- controlled experiments;
- reproducible analysis;
- adversarial interpretation.

That is how the corpus becomes science.
