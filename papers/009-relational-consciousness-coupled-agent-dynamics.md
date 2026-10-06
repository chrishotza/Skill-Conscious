# Relational Consciousness: Coupled-Agent Dynamics and Reciprocal Causality

## Status

Working paper v0.1 — empirical protocol.

The term "relational consciousness" denotes a research level, not an established claim that interacting agents form a shared phenomenal subject.

## Abstract

This study tests whether reciprocal coupling between agents creates measurable dynamical structure that is not reducible to isolated-agent state plus common external input. The study operationalizes relational organization through bidirectional causal influence, coupling-dependent prediction, synchronization beyond common input, and changes in task dynamics following disruption of the coupling channel.

The core hypothesis is:

> A relational system acquires a measurable dynamical property when the state of each participant causally constrains the future state of the other in a way that cannot be explained by common input alone.

The study is motivated by contemporary relational neuroscience and hyperscanning work, while avoiding the invalid inference that synchronization or coordination automatically equals shared consciousness.

## 1. Conditions

A — isolated agent A.

B — isolated agent B.

C — coupled A ↔ B.

D — sham coupling / replay control.

E — delayed or bandwidth-limited coupling.

## 2. Primary measures

- incremental predictive information from partner state;
- bidirectional causal influence;
- coupling-specific prediction gain;
- recovery after communication disruption;
- coordination cost / benefit;
- state divergence between isolated and coupled conditions.

## 3. Main confound

Common input can create apparent synchrony.

Therefore the analysis must condition on:

- identical external stimuli;
- shared task structure;
- individual internal state;
- latency;
- communication bandwidth.

The critical comparison is not "synchronous vs asynchronous"; it is "coupling provides unique predictive/causal information vs common-input explanation."

## 4. Main prediction

If relational organization is causally relevant, the coupled condition should contain information about future system state that cannot be reconstructed from the isolated trajectories and shared input alone.

## 5. Stronger consciousness claim

The study must not conclude "shared consciousness" from synchronization.

A stronger claim would require an independently justified bridge between relational dynamics and phenomenal experience.

## 6. Human empirical extension

The computational protocol can later be mapped to hyperscanning experiments in which participants interact under controlled conditions.

Relevant empirical literature includes work on inter-brain dynamics, interactivity, and social closeness.

## 8. Falsification

The relational hypothesis is weakened if:

- common-input models explain the observed coupling effects;
- coupling adds no predictive or causal information;
- apparent interaction effects vanish under sham/replay control;
- effects are entirely attributable to extra communication bandwidth.

## 9. Next implementation

The repository now contains three generations of the probe. The first versions exposed design confounds; the current controlled assay is `experiments/relational_coupling_probe_v3.py`, which uses independent deterministic disturbances and a permuted replay control.

Create/extend the probe so that it logs:

`state_A(t), state_B(t), message(t), intervention(t), state_A(t+1), state_B(t+1)`

and computes pre-registered relational metrics.

## 10. Publication path

Protocol → preregistration → simulation benchmark → replication across seeds/models → statistical analysis → adversarial interpretation → empirical paper.
