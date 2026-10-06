# S01 — Cross-Cultural Consciousness Claim Recurrence Analysis

## Status
**Preregistered protocol v1 — frozen before confirmatory semantic/T4 execution**

This is a substantive research study, not a paper. A paper will be drafted only after the study produces and archives confirmatory results.

## Research question

> Which recurrent structures related to consciousness remain after controlling for source-family structure, claim duplication, motif prevalence, and independent text-level semantic similarity?

The study does not test whether any metaphysical interpretation is true.

## Data snapshot

The effective corpus is frozen to:
- core ledger: 2,482 records;
- append v24–v36: 130 records each;
- append v37: 143 records;
- total effective claims: 4,315;
- source-register units: 325;
- effective source IDs: 328;
- primary analytic unit: corpus_id.

Three corpus IDs map to multiple effective source IDs and are therefore collapsed at the corpus-unit level: C083, C084 and C230.

Exact Git blob SHAs are frozen in research/S01_DATA_MANIFEST_V1.json.

## Hypotheses

### H1 — coded recurrence
Source-level motif organization contains cross-family similarity greater than expected under random assignment of source-family labels.

### H0 — coded null
Observed cross-family similarity is fully explained by family sizes and the underlying motif distribution.

### H2 — semantic recurrence
Raw claim text contains cross-family semantic neighborhoods more similar than expected after randomizing source-family labels.

### H0-semantic
Semantic neighborhoods do not contain cross-family structure beyond the source-family label distribution.

## Primary coded outcome

For each pair of corpus units:

Jaccard(source_i motifs, source_j motifs)

Primary statistic:

DeltaJ = mean cross-family Jaccard minus mean within-family Jaccard.

Positive values favor cross-family recurrence. Negative values indicate stronger within-family clustering.

### Primary null
Randomly permute source-family labels across the 325 corpus units while preserving family sizes.

Use 5,000 permutations.

Primary p-value:

P(null DeltaJ >= observed DeltaJ).

Report observed effect, null mean, 95 percent null interval and standardized effect.

## Secondary coded null

Construct a binary corpus-unit by motif matrix.

Randomize it with bipartite degree-preserving edge swaps so that every corpus unit keeps its motif degree and every motif keeps its support degree.

Compute the same DeltaJ statistic.

## Motif recurrence profile

For every M01–M25 report:
- supporting corpus units;
- source families represented;
- within-family prevalence;
- normalized Shannon entropy across source families;
- permutation-null entropy distribution.

This is descriptive/secondary and is not a truth score.

## Primary semantic analysis

The raw claim text field is embedded without using the motif labels.

Model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2.

Pinned model revision: ef15aed8b328d308d7237b9bf15269f2cd19e268.

For each claim:
1. exclude itself;
2. exclude claims from the same corpus_id;
3. find its top 10 eligible semantic neighbors by cosine similarity;
4. record similarities;
5. mark neighbors as same-family or cross-family.

Primary semantic statistic:

DeltaS = mean cosine of cross-family neighbors minus permutation-null expectation.

Use 5,000 source-family label permutations.

## Semantic sensitivity analyses

Pre-specified:
1. top-5 instead of top-10;
2. exclude Heterodoxo/extendido;
3. exclude Ciencia/IA and Suplementario;
4. P1/P2/S1-only provenance subset;
5. leave-one-family-out robustness;
6. repeat CPU/GPU inference only as a reproducibility check.

Additional post-result analyses are exploratory.

## Falsification / failure criteria

The recurrence hypothesis is weakened if:
- coded DeltaJ is not above its family-label null;
- semantic DeltaS is not above its label-permutation null;
- recurrence disappears after collapsing to corpus units;
- the effect disappears in P1/P2/S1-only analysis;
- leave-one-family-out analysis reverses the direction;
- semantic recurrence is explained entirely by same-family clustering;
- the result depends on post-hoc grouping decisions.

A null result is retained as a scientific result.

## Interpretation limits

A positive recurrence result means only that source claims share structures that recur across the tested source families and representations.

It does not establish truth, independent discovery, fundamental consciousness, or any specific metaphysical ontology.

## Leakage controls

The semantic analysis must not use motif labels.
Source-family assignments are frozen from the source register.
Primary statistics and randomization settings are frozen before the confirmatory T4 run.
The 2026-10-06 pilot is exploratory only.

## Reproducibility requirements

Archive for every run:
- Git commit;
- exact corpus blob SHA manifest;
- Python/runtime/package versions;
- CUDA version and GPU model;
- seed;
- model name and exact revision;
- command/config;
- run timestamp;
- result JSON/CSV;
- stdout/stderr;
- protocol deviations.

## Exit condition

S01 exits when both primary analyses and robustness checks are complete and all artifacts are archived.

Only then does the project decide whether the study becomes the first paper.