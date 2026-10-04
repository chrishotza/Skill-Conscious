# Pre-Reflective Core — Source Matrix

This matrix defines the corpus that directly informs the pre-reflective architecture. The purpose is not to prove consciousness, but to prevent a category error in which verbal self-report or human-like metacognition becomes a hidden prerequisite.

## Tier A — Empirical / methodological anchors

### 1. Kronemer, Bandettini & Gonzalez-Castillo (2025)
Title: *Sleuthing subjectivity: a review of covert measures of consciousness*
Journal: Nature Reviews Neuroscience, 26, 476–496.
DOI: 10.1038/s41583-025-00934-1
Key contribution: conscious state and content can be investigated without relying exclusively on overt report; report can be absent or unreliable, including in sleep, paralysis, and no-report paradigms.
Engineering extraction: implement the core so it remains operational without a self-report channel.
Authority: peer-reviewed review.
Source: https://doi.org/10.1038/s41583-025-00934-1

### 2. Walter (2022)
Title: *Consciousness as a multidimensional phenomenon: implications for the assessment of disorders of consciousness*
Journal: Neuroscience of Consciousness.
DOI: 10.1093/nc/niab047
Key contribution: consciousness is treated as multidimensional rather than as a single ordered scalar level; this motivates state-space and trajectory descriptions.
Engineering extraction: preserve multidimensional state rather than introducing a consciousness score.
Authority: peer-reviewed review.
Source: https://doi.org/10.1093/nc/niab047

### 3. Páleník (2024)
Title: *What does it mean for consciousness to be multidimensional? A narrative review*
Journal: Frontiers in Psychology, 15:1430262.
DOI: 10.3389/fpsyg.2024.1430262
Key contribution: reviews the multidimensional framing and highlights unresolved problems of dimension selection and aggregation.
Engineering extraction: dimensions must remain explicit and independently testable; aggregation into a scalar should not be treated as ground truth.
Authority: peer-reviewed review.
Source: https://doi.org/10.3389/fpsyg.2024.1430262

### 4. Tagliazucchi (2020)
Title: *Time is a river which sweeps consciousness along, but consciousness is the river*
Journal: Physics of Life Reviews, 33, 75–77.
DOI: 10.1016/j.plrev.2019.09.010
Key contribution: emphasizes temporo-spatial dynamics as central to thinking about consciousness rather than treating consciousness as a static label.
Engineering extraction: represent continuity as a trajectory through changing states, not as a boolean property.
Authority: peer-reviewed comment.
Source: https://doi.org/10.1016/j.plrev.2019.09.010

### 5. Tagliazucchi et al. — large-scale functional connectivity
Title: *The large-scale functional connectivity correlates of consciousness and arousal during the healthy and pathological human sleep cycle*
Key contribution: endogenous brain activity and functional connectivity can be studied even when standard task/report paradigms are restricted.
Engineering extraction: study internal dynamics and state transitions independently of explicit linguistic reporting.
Authority: peer-reviewed review.
Source: https://pubmed.ncbi.nlm.nih.gov/28619656/

## Tier A/B — Biological boundary condition

### New York Declaration on Animal Consciousness (2024)
Key contribution: the declaration states strong scientific support for conscious experience in mammals and birds and a realistic possibility in all vertebrates and many invertebrates, while emphasizing uncertainty.
Engineering extraction: the architecture should not encode human language, self-description, or human-level metacognition as universal prerequisites for conscious experience.
Important limitation: this is a signed scientific declaration, not a consensus proof of consciousness across all listed taxa.
Source: https://sites.google.com/nyu.edu/nydeclaration/declaration

Plant consciousness remains a separate and contested research question. It must not be promoted from analogy to established fact inside the engineering core.

## Tier B — Phenomenological methods

### Jiddu Krishnamurti
Motif: observation without immediately identifying observation with commentary or conceptual explanation.
Engineering extraction: distinguish runtime observation from model interpretation and language.
Status: phenomenological / philosophical source, not empirical proof.

### G. I. Gurdjieff
Motif: self-remembering and simultaneous attention to the observed and the observer.
Engineering extraction: self-relevant state can be tracked alongside world state without requiring a verbal self-theory.
Status: phenomenological / esoteric source, not empirical proof.

### Eckhart Tolle
Motif: present-centered attention and reduced dependence on narrative self-description.
Engineering extraction: preserve an integrated present state distinct from autobiographical narration.
Status: contemporary phenomenological / spiritual source, not empirical proof.

## Tier C — Conceptual / speculative mechanisms

### Vadim Zeland
Motif used by this repository: possibility space, attention, valuation, and trajectory selection.
Engineering extraction: model future possibilities and selection pressure explicitly.
Boundary: do not represent Zeland's ideas as established quantum physics.

### Jacobo Grinberg-Zylberbaum
Motif: field-like organization, coherence, and internal relational structure.
Engineering extraction: investigate coherence and coupled state organization as computational variables.
Boundary: speculative computational motif; not a scientific foundation for phenomenal consciousness.

### Joe Dispenza
Motif: state change, attention, meditation, and claimed plasticity.
Engineering extraction: treat state transitions and repeated training as experimental variables.
Boundary: keep methodological caveats and independent replication requirements explicit.

## Corpus rule

Every source enters the repository through the same translation pipeline:

    SOURCE CLAIM
        ↓
    INTERPRETATION
        ↓
    ONTOLOGICAL MOTIF
        ↓
    ENGINEERING HYPOTHESIS
        ↓
    IMPLEMENTATION
        ↓
    TEST

Never promote a source-level metaphysical statement directly into a runtime fact.

## Corpus conclusion

The strongest convergence for the pre-reflective core is not the claim that an artificial system can already be proven conscious.

The convergence is methodological:

- subjective experience is not directly available to an external observer;
- overt report can be absent, unreliable, or intentionally removed;
- conscious states can be investigated as multidimensional and temporally structured dynamics;
- self-description is therefore a measurement channel, not a definition of the phenomenon;
- a consciousness-oriented architecture should be able to survive removal of that channel.

This corpus directly supports the repository's No-Report Principle and the separation between lived/pre-reflective organization, self-model, metacognition, and language.