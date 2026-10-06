# P000 — Corpus Audit Protocol v0.1

## Goal

Turn the 4,315-claim corpus into an auditable research object before central claims are used as evidence in downstream papers.

## Work packages

### WP1 — Source verification

For every central-source candidate:
- verify bibliographic identity;
- verify source existence and edition;
- recover original passage when legally and practically possible;
- record location;
- record language;
- record translation;
- assign translation confidence;
- preserve uncertainty.

### WP2 — Provenance

For every source:
- assign canonical provenance class;
- retain prior/noncanonical labels in an audit field;
- record the reason for the final class;
- prohibit silent normalization.

### WP3 — Dependency graph

Construct typed source relations:
- DERIVED_FROM
- QUOTES
- TRANSLATES
- COMMENTS_ON
- SHARES_DATA_WITH
- SAME_LINEAGE_AS
- POSSIBLE_DEPENDENCY
- UNKNOWN

### WP4 — Claim adjudication

Each central claim receives:
- source-faithfulness status;
- interpretation status;
- contradiction status;
- independence status;
- evidence maturity ES0–ES5.

### WP5 — Construct extraction

For each candidate claim family:
- define construct;
- define operational variable;
- define alternative interpretations;
- define null;
- define competing model;
- define falsifier.

### WP6 — Paper eligibility

A claim can enter the central evidence table of a paper only when:
- source is traceable;
- interpretation is explicit;
- construct is operationalized or clearly labelled as theoretical;
- competitor exists;
- contradiction search is documented.

## Audit outputs

Required machine-readable artifacts:
- p000_source_audit.json
- p000_dependency_graph.json
- p000_claim_adjudication.json
- p000_contradiction_log.json
- p000_claim_dossiers.json
- p000_paper_eligibility.json

## Sampling strategy

The first audit should use two passes.

### Pass A — High-impact audit
Review all sources/claims currently intended to support P008, P009, P010 and P012.

### Pass B — Corpus quality sample
Draw a reproducible stratified sample across provenance class, source family, language/translation status, claim type, three-scale family, historical period and unresolved/cross-cutting status.

The sampling rule must be frozen before the results are inspected.

## Failure handling

A failed verification becomes a recorded status, not a deletion.

Possible states:
- VERIFIED
- PARTIALLY_VERIFIED
- UNVERIFIED
- CONTRADICTED
- TRANSLATION_UNCERTAIN
- DEPENDENCY_UNCERTAIN
- SOURCE_UNAVAILABLE
- INTERPRETATION_ONLY

## Decision rule

A paper must not silently upgrade:

UNVERIFIED → VERIFIED

or:

SOURCE CLAIM → EMPIRICAL RESULT

The audit itself must have a change log.

## Preregistered analysis principle

Once the audit sampling and adjudication rules are frozen, changing them in response to observed results requires a versioned amendment and preservation of the original plan.