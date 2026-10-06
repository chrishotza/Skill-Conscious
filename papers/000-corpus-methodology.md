# P000 — A Machine-Readable Cross-Cultural Corpus of Consciousness Claims: Provenance, Phenomenology, Ontology and Testability

## Status
**Working paper v0.1 — methodological foundation / corpus audit protocol**

This paper does not claim that the corpus proves any theory of consciousness. Its purpose is to define and evaluate a reproducible method for converting heterogeneous consciousness-related source material into auditable research objects and, where possible, falsifiable empirical hypotheses.

## Abstract

Consciousness research spans empirical neuroscience, cognitive science, philosophy of mind, phenomenology, contemplative traditions, religious texts, anomalous-experience literature, esoteric systems and machine-consciousness research. These materials do not share a common evidential status, vocabulary or method. A research program that combines them therefore requires a formal separation between what a source says, what a researcher infers, what a model predicts and what an experiment measures.

Skill-Conscious currently maintains a closed corpus containing 325 registered source records, 328 effective source identifiers and 4,315 effective claim records. This paper proposes a machine-readable research method for transforming that corpus into testable science without treating recurrence as proof, source claims as facts, or project interpretations as discoveries.

The proposed method has six core components: (1) source verification; (2) provenance and dependency tracking; (3) claim-family clustering; (4) explicit separation of phenomenological, ontological and project-interpretive layers; (5) conversion to operational constructs, competing hypotheses and falsifiable predictions; and (6) preregistered, reproducible experiments followed by replication and adversarial interpretation.

The contribution is methodological. The corpus is treated as a hypothesis-generation substrate and evidence-traceability system rather than a truth database. The method deliberately permits unconventional hypotheses, including fundamental-consciousness models, while applying the same evidential burden to conventional and heterodox explanations.

## 1. Research questions

### RQ1 — Corpus auditability
Can heterogeneous consciousness-related source material be represented as traceable, machine-readable claims without collapsing source statements and researcher interpretations?

### RQ2 — Independence
Can repeated claims be distinguished from genuinely independent recurrence by modelling textual, cultural, translational and empirical dependencies?

### RQ3 — Testability
Can source claims be transformed into constructs and competing hypotheses that generate discriminating predictions?

### RQ4 — Falsifiability
Can the method expose explicit conditions under which a preferred interpretation should be weakened, rejected or replaced?

### RQ5 — Cross-scale integration
Can the same evidence architecture support Individual, Relational and Fundamental research programs without granting the Fundamental scale a lower evidential threshold?

## 2. Corpus status

Current audit state:

| Quantity | Value | Interpretation |
|---|---:|---|
| Registered source records | 325 | Corpus source register |
| Effective source IDs | 328 | Effective ledger coverage |
| Effective claim records | 4,315 | Machine-readable claims |
| Unique global claim IDs | 4,315 | No duplicate global identifiers |

These values are corpus accounting, not empirical validation.

### Known integrity issue
The effective ledger contains 52 records whose provenance values are not yet normalized to the canonical provenance classes. They are concentrated in three source groups:
- S069 — Yoruba Ifá / Odu corpus;
- S070 — Huarochirí Manuscript;
- S071 — Diné Bahane'.

These records require source-level review before normalization. Silent relabelling is prohibited.

## 3. Why a conventional bibliography is insufficient

A bibliography can answer:

> Which sources were consulted?

A research-grade corpus must additionally answer:

> What exactly did each source claim, where, in what language, through which translation, under what provenance, with what confidence, and how independently is it supported?

The unit of analysis therefore becomes the **claim record**, not the citation alone.

## 4. Claim record

Every central claim should preserve, where available:
- source identifier;
- claim identifier;
- quotation or precise paraphrase;
- location;
- source type;
- original language;
- translation;
- translation confidence;
- claim type;
- phenomenological content;
- ontological content;
- metaphysical content;
- self-model/body-model/world-model fields;
- temporality;
- transformation;
- persistence/death;
- universal/transpersonal scope;
- normalized motifs;
- provenance class;
- interpretation confidence;
- notes and limitations.

The original source statement remains recoverable.

## 5. Source claim versus project hypothesis

The method enforces the following separation:

~~~
SOURCE
  ↓
SOURCE CLAIM
  ↓
PROJECT INTERPRETATION
  ↓
PROJECT HYPOTHESIS
  ↓
OPERATIONAL DEFINITION
  ↓
EMPIRICAL PREDICTION
~~~

A statement such as 'consciousness is fundamental' may be a SOURCE CLAIM or PROJECT HYPOTHESIS depending on provenance. It cannot become 'consciousness is scientifically established as fundamental' without an empirical model and discriminating evidence.

Likewise, mystical unity mapped to relational integration is a project mapping, not a faithful translation of the historical source unless independently justified.

## 6. Provenance

The corpus uses explicit provenance classes rather than a single undifferentiated evidence pool.

The repository currently distinguishes, among others:
- P1 / P2 / P2* — corpus source-level evidence categories;
- S1 / S2 — scholarly/secondary interpretive material;
- X1 — heterodox/speculative material;
- O1 — project-original ontology.

Provenance is a constraint on what may be claimed, not a truth score.

## 7. Independence model

### Principle

~~~
N sources ≠ N independent evidences
~~~

Sources may depend on one another through:
- direct citation;
- quotation;
- shared translator;
- shared editorial tradition;
- common primary manuscript;
- cultural transmission;
- shared dataset;
- common experiment;
- derivative secondary literature.

The next corpus phase therefore introduces a source-dependency graph.

Each source relation should be represented, where known, by a typed edge such as:
- DERIVED_FROM;
- QUOTES;
- TRANSLATES;
- COMMENTS_ON;
- SHARES_DATA_WITH;
- SAME_LINEAGE_AS;
- POSSIBLE_DEPENDENCY;
- UNKNOWN_DEPENDENCY.

Independent recurrence requires explicit justification.

## 8. Claim-family formation

The 4,315 claims are not treated as 4,315 papers. They are clustered into mechanistic families.

Current high-level reservoirs:

| Family | Candidates | Main research program |
|---|---:|---|
| Individual | 1,311 | P008 |
| Relational | 528 | P009 |
| Fundamental | 164 | P010 |
| Cross-cutting / unresolved | 2,312 | P007 / P011 / evidence layers |

The unassigned/cross-cutting reservoir is not discarded. It can supply controls, contradictions, historical context, boundary conditions or later hypotheses.

## 9. Evidence maturity ladder

The project uses the following maturity ladder:

| Level | Meaning |
|---|---|
| ES0 | catalogued claim |
| ES1 | source passage verified |
| ES2 | corroboration/contradiction and dependency audit |
| ES3 | operational construct fixed |
| ES4 | pre-registered/frozen prediction tested |
| ES5 | independent replication or strong external confirmation |

This is a maturity index, not a probability of truth.

A claim may be theoretically important while remaining ES1. A technically precise hypothesis may be ES4 while the underlying metaphysical interpretation remains unresolved.

## 10. Contradiction and negative-evidence audit

Each major family must actively collect support, contradiction, alternative interpretation, boundary cases, null cases and negative experiments.

This prevents the corpus from behaving as a confirmation engine.

The method treats a failed prediction as information about the model.

## 11. Conversion to empirical science

The canonical transformation is:

~~~
CLAIM
↓
CONSTRUCT
↓
HYPOTHESIS
↓
NULL
↓
COMPETING MODEL
↓
PREDICTION
↓
FALSIFIER
↓
PROTOCOL
↓
RESULT
↓
REPLICATION
↓
INFERENCE
~~~

Example:

**Source-level family**
A set of independent sources describes self-knowledge, persistence of identity and recursive awareness.

**Project construct**
Persistent self-model with causal participation in future state selection.

**Hypothesis**
Intervening on the self-model changes future trajectory selection under matched external input, candidate futures and computational budget.

**Null**
The effect is fully explained by additional memory, context or generic computation.

**Prediction**
Self-model intervention produces a reproducible trajectory-selection divergence not present in memory-matched controls.

This is the exact logic currently instantiated in P008.

## 12. Operationalization

Metaphysical vocabulary is never used as an experimental variable without operational definition.

| Source vocabulary | Research status |
|---|---|
| soul | philosophical/source construct until operationalized |
| spirit | interpretive/source construct until operationalized |
| energy | undefined until physical quantity is specified |
| field | undefined until a physical field and observable are specified |
| unity | candidate relational/phenomenological construct |
| self-knowledge | candidate self-model/metacognitive construct |
| continuity | candidate temporal/identity construct |
| fundamental consciousness | candidate ontological model requiring discriminating observable |

The project's translation of a source concept into an engineering or experimental construct must always be visibly labelled as an interpretation.

## 13. Three-scale integration

The same corpus can generate hypotheses at three research scales:

### Fundamental
Does a specified consciousness-bearing physical model make an observable prediction that differs from a non-conscious physical null?

### Relational
Does reciprocal coupling add predictive or causal information beyond isolated state and common input?

### Individual
Does persistent self-reference causally participate in future trajectory selection?

These scales are not assumed to be three proven substances. They are research levels connected by hypotheses tested through B1–B4.

## 14. Preregistration and analysis freezing

Confirmatory studies should, when feasible, preregister hypothesis, primary outcome, secondary outcomes, conditions, exclusions, sample/run plan, statistical/model-selection procedure, stopping rule and falsification criterion.

The repository should maintain both the preregistered specification and the executed analysis. Deviations are recorded rather than silently replacing the original plan.

This follows the logic of contemporary preregistration and Registered Report methodology, in which research questions, methods and analyses are fixed before the outcome is known. [Nature Human Behaviour Registered Reports](https://www.nature.com/nathumbehav/submission-guidelines/registeredreports); [OSF Registrations & Preregistrations](https://help.osf.io/article/330-welcome-to-registrations).

## 15. Adversarial design

Consciousness research provides a strong methodological precedent for this approach. The 2025 adversarial collaboration comparing IIT and GNWT specified differential predictions, preregistered pass/fail criteria and tested competing theories within a theory-neutral collaboration. https://www.nature.com/articles/s41586-025-08888-1

Skill-Conscious adopts the methodological lesson rather than assuming either theory is correct.

Every major experiment should ask:

> What result would make our preferred explanation less likely?

## 16. Reporting framework

For corpus synthesis and evidence reporting, the project should borrow the transparency discipline of PRISMA 2020 and PRISMA-ScR: explicitly report search/screening decisions, inclusion/exclusion logic, source characteristics, appraisal and synthesis procedures rather than presenting only the final selected evidence.

Primary anchors:
- PRISMA 2020: https://www.prisma-statement.org/prisma-2020
- PRISMA 2020 checklist: https://www.prisma-statement.org/prisma-2020-checklist
- PRISMA-ScR: https://www.prisma-statement.org/

This paper does not claim that PRISMA alone is sufficient for a cross-cultural consciousness corpus. The repository adapts the relevant transparency principles and documents all departures.

## 17. Publication outputs

P000 should release, alongside the manuscript:
1. corpus schema;
2. source register;
3. claim ledger;
4. provenance map;
5. source-dependency graph;
6. claim-family registry;
7. audit scripts;
8. inclusion/exclusion log;
9. contradiction log;
10. claim-to-paper mappings.

The release must distinguish public-domain/openly redistributable text from bibliographic references to copyrighted material.

## 18. Limitations

1. The corpus is heterogeneous by construction.
2. Some historical sources survive only through translations or layered editorial histories.
3. Independent recurrence can be difficult to establish.
4. Claim extraction necessarily involves judgement.
5. Machine-readable normalization can create false equivalence unless semantic distinctions are preserved.
6. Operationalization may move away from the original source meaning; such movement must be disclosed.
7. Empirical validation of a construct does not automatically validate the source metaphysics from which it was motivated.
8. The current corpus counts are ledger-level counts, not proof that every record has passed passage-level verification.

## 19. Expected contribution

The principal contribution of P000 is methodological:

> a consciousness corpus should function as a traceable hypothesis-generation system in which historical and contemporary claims can be independently audited, transformed into explicit constructs, challenged by competing explanations, and connected to reproducible empirical tests.

This permits an unusually broad hypothesis space without weakening the evidence standard.

## 20. Pre-registered next audit

The first full audit cycle should freeze the following outputs before interpretation of any new findings:
- source-level verification status;
- provenance normalization decisions;
- dependency/independence graph;
- contradiction status;
- claim-family assignment;
- ES maturity level;
- central-paper eligibility.

Only then should a claim be promoted into a paper's central evidence set.

## References / methodological anchors

1. PRISMA Statement. PRISMA 2020. https://www.prisma-statement.org/prisma-2020
2. PRISMA Statement. PRISMA 2020 checklist. https://www.prisma-statement.org/prisma-2020-checklist
3. OSF. Registrations & Preregistrations. https://help.osf.io/article/330-welcome-to-registrations
4. Nature Human Behaviour. Registered Reports. https://www.nature.com/nathumbehav/submission-guidelines/registeredreports
5. Cogitate Consortium. Adversarial testing of global neuronal workspace and integrated information theories of consciousness. Nature (2025). https://www.nature.com/articles/s41586-025-08888-1

## Current status

P000 is **not yet publication-ready**.

The next revisions require:
- full source-method audit of the corpus;
- source-dependency graph;
- passage-verification sample;
- contradiction audit;
- claim-dossier format;
- reproducible audit scripts;
- quantitative reporting of audit outcomes.

The purpose of v0.1 is to freeze the methodological architecture before those audits are interpreted.