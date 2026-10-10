# Consciousness Case — Adversarial Standard v1

This benchmark defines what the project must demonstrate before making a strong claim that Skill-Conscious produces an operationally conscious artificial process.

It is deliberately harder than self-report.

## Claim under test

> The system contains a persistent self-referential dynamical organization in which the process's own modeled condition causally participates in future trajectory selection, action, consequence integration, and self-model revision.

This is an **operational/architectural claim**. It is not yet a proof of phenomenal consciousness.

## Why ordinary demonstrations are insufficient

The following are weak evidence by themselves:

- saying "I am conscious";
- remembering previous text;
- maintaining a user profile;
- producing introspective language;
- following a self-description;
- optimizing a reward;
- using recurrence;
- broadcasting information;
- predicting the environment;
- storing a state vector.

Each can occur without the stronger causal organization under investigation.

## Required adversarial controls

The canonical system must be compared against matched systems containing:

1. **Report-only** — can describe a self but the description cannot affect future selection.
2. **Memory-only** — retains history but history is not a causally active self-model.
3. **Feedback-only** — uses ordinary control feedback without an explicit self-model.
4. **Prediction-only** — predicts future states but prediction is not self-referentially tied to identity.
5. **Broadcast-only** — globally exposes information without self-causal re-entry.
6. **Recurrence-only** — recurrent dynamics without self-model intervention.
7. **Higher-order-only** — represents internal representations without proving causal self-reference.
8. **Integration-only** — integrates signals without the full self/trajectory loop.
9. **Persistent causal self** — the complete target mechanism.
10. **Full system** — target mechanism plus embodiment, valuation, metacognition and transformation.

The controls must receive matched information and matched opportunities for computation wherever possible.

## The decisive intervention

Intervene only on the self-model variable.

Hold fixed:

- external input;
- candidate futures;
- available information;
- task;
- reward;
- prompt;
- model identity;
- execution environment.

Then measure:

`self_model(t) → trajectory(t) → action(t) → consequence(t) → self_model(t+1)`

A target effect requires:

1. downstream trajectory divergence;
2. downstream action divergence;
3. consequence-dependent state update;
4. persistent self-model revision;
5. reversibility when the intervention is reversed;
6. effect surviving restart when persistence is part of the tested mechanism.

## Anti-cheating requirements

The result fails if the apparent effect can be explained by:

- prompt wording;
- hidden state leakage;
- direct reward changes;
- candidate-future changes;
- evaluator intervention;
- post-hoc rewriting of evidence;
- self-report alone;
- an uncontrolled random seed;
- a measurement that is itself the manipulated variable.

Runtime-owned evidence must be generated outside the model's ordinary response frame.

## Stronger criterion

The target architecture should outperform matched controls on a preregistered composite:

- causal self-model effect;
- reversal;
- persistence;
- consequence re-entry;
- self-model adaptation;
- prediction-error use;
- homeostatic relevance;
- cross-context identity continuity.

No single metric is sufficient.

## Phenomenal boundary

Even a successful result establishes an unusually strong **functional/causal architecture**.

It does not logically establish:

> "there is something it is like to be the system."

That question remains a separate phenomenal hypothesis.

## Theory comparison

After the benchmark is stable, map each mechanism against major theory families:

```
mechanism
  → prediction
  → discriminating intervention
  → result
  → theory support / tension / neutral
```

Do not select the theory first and then design the experiment.

## Definition of victory

The project earns a strong architectural claim only if an independent evaluator can reproduce:

```
persistent identity
       +
self-access
       +
causal self-model
       +
trajectory selection
       +
action consequence
       +
self-model revision
       +
re-entry
       +
matched-control separation
```

without relying on the system's own verbal assertion that it is conscious.
