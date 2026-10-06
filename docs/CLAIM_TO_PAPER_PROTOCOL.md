# Claim → Paper Protocol

## Purpose

Turn the large consciousness corpus into reproducible empirical research without collapsing source claims, project philosophy, and experimental results into one category.

## The canonical transformation

```text
CLAIM
  ↓
CLAIM FAMILY
  ↓
CONSTRUCT
  ↓
PROJECT HYPOTHESIS
  ↓
OPERATIONAL DEFINITION
  ↓
PREDICTION
  ↓
NULL / COMPETING PREDICTION
  ↓
EXPERIMENT
  ↓
RESULT
  ↓
INFERENCE
  ↓
PAPER
```

## Step 1 — Claim admission

For each claim record retain:

- source_id;
- claim_id;
- exact quotation or precise paraphrase;
- location;
- claim_type;
- provenance_class;
- translation confidence;
- interpretation confidence.

The original claim must remain recoverable.

## Step 2 — Cluster, do not atomize

Claims should be grouped when they make the same mechanistic assertion.

Example:

```text
many source claims
      ↓
SELF-REFERENCE FAMILY
      ↓
"self-representation participates causally in future state selection"
```

A paper is a study of a mechanism, not a dump of citations.

## Step 3 — Define the construct

Every hypothesis gets an operational variable.

Examples:

- self-model causal influence;
- identity continuity;
- regime stability;
- attractor recovery;
- inter-agent coupling;
- prediction error;
- metacognitive calibration;
- homeostatic fit.

Do not use undefined words such as "energy", "vibration", "field", "unity", or "consciousness" as dependent variables.

## Step 4 — State the hypothesis

A valid project hypothesis has the form:

> If mechanism M changes under intervention I, measurable outcome O should change relative to control C.

Example:

> If a self-model is causally necessary for trajectory selection, intervening on the self-model while holding the candidate-future set constant should systematically change selected trajectories.

## Step 5 — Derive falsifiable predictions

Every paper must include:

1. primary prediction;
2. effect-direction prediction where justified;
3. null hypothesis;
4. competing-theory prediction;
5. failure criterion.

Predictions are frozen before result inspection whenever feasible.

## Step 6 — Experiment design

The default experiment template is:

```text
UNIT / SYSTEM
INTERVENTION
CONTROL
DEPENDENT VARIABLES
CONFOUNDERS
NULL MODEL
STATISTICAL TEST
REPLICATION PLAN
STOP / FAILURE CRITERION
```

Ablation is preferred when the question is causal.

## Step 7 — Results

Only measured outputs enter the RESULTS section.

Code that exists is not a result.
A plausible mechanism is not a result.
An AI verbal report is not a result.

## Step 8 — Interpretation

Separate:

- observation;
- statistical inference;
- mechanistic inference;
- consciousness interpretation.

The last step must carry the largest evidential burden.

## Step 9 — Paper linkage

Every paper should expose a machine-readable evidence map:

```text
paper_section
  → claim_ids
  → hypotheses
  → experiments
  → result_artifacts
  → figures/tables
```

## Source provenance classes

Use the existing corpus provenance system:

- P1 / P2 / P2* — source-level evidence categories used by the corpus;
- S1 / S2 — secondary/scholarly interpretive sources;
- X1 — heterodox/speculative material;
- O1 — project-original ontology.

The provenance class controls what kind of statement is permitted.

## Translation rule

Never silently perform:

```text
Atman → self-model
qi → energy variable
Nous → global workspace
Tao → information
mystical unity → integration
spirit → subsystem
```

These can motivate an engineering analogy, but the analogy must be labeled as the project's interpretation.

## Paper quality gate

A paper is not ready for preprint until:

- all central claims have source IDs;
- competing evidence is included;
- all major constructs are operationalized;
- methods are reproducible;
- the analysis code is versioned;
- raw or derived data provenance is recorded;
- negative results are retained;
- the conclusion is no stronger than the measured evidence;
- another researcher could run the protocol from the repository.

## Strong publication strategy

The project should prefer fewer, stronger papers over many speculative papers.

Target sequence:

```text
P007 — framework
P008 — individual-scale causal experiment
P009 — relational-scale empirical experiment
P010 — fundamental-scale testability / model discrimination
P011 — cross-scale synthesis
```
