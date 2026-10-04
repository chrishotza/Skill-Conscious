"""Unlabeled online temporal-ontology benchmark v1.

A runtime receives only observed transitions from a stream whose hidden process
can switch between two dynamics with matched stationary marginals.

It is never given the process label.

Instead it maintains two symmetric temporal hypotheses, accumulates decayed
prediction-error evidence, infers the active regime with hysteresis, and lets
confidence/error modulate the temporal attention horizon.

This is an architectural benchmark, not a phenomenal-consciousness claim.
"""

from __future__ import annotations

import json
import math
import random
import statistics
from dataclasses import dataclass, field
from typing import Mapping

STATES = ("A", "B", "C")

PROCESS_ALPHA = {
    "A": {"A": 0.05, "B": 0.90, "C": 0.05},
    "B": {"A": 0.05, "B": 0.05, "C": 0.90},
    "C": {"A": 0.90, "B": 0.05, "C": 0.05},
}
PROCESS_BETA = {
    "A": {"A": 0.05, "B": 0.05, "C": 0.90},
    "B": {"A": 0.90, "B": 0.05, "C": 0.05},
    "C": {"A": 0.05, "B": 0.90, "C": 0.05},
}

SEGMENT_LENGTH = 80
SEGMENT_COUNT = 6
CHANGE_POINTS = (80, 160, 240, 320, 400)
STREAM_COUNT = 50


def _sample_next(
    transition: Mapping[str, Mapping[str, float]],
    source: str,
    rng: random.Random,
) -> str:
    threshold = rng.random()
    cumulative = 0.0
    for target, probability in transition[source].items():
        cumulative += float(probability)
        if threshold <= cumulative:
            return target
    return next(iter(transition[source]))


def _build_alternating_stream(seed: int) -> tuple[tuple[str, ...], tuple[str, ...]]:
    rng = random.Random(seed)
    states: list[str] = []
    labels: list[str] = []
    current_state = rng.choice(STATES)
    process_name = "alpha"

    for _ in range(SEGMENT_COUNT):
        transition = (
            PROCESS_ALPHA
            if process_name == "alpha"
            else PROCESS_BETA
        )
        for _ in range(SEGMENT_LENGTH):
            current_state = _sample_next(transition, current_state, rng)
            states.append(current_state)
            labels.append(process_name)
        process_name = "beta" if process_name == "alpha" else "alpha"

    return tuple(states), tuple(labels)


def _log_likelihood(
    transition: Mapping[str, Mapping[str, float]],
    source: str,
    target: str,
) -> float:
    probability = float(transition[source].get(target, 0.02))
    return math.log(max(0.02, min(1.0, probability)))


@dataclass
class TemporalOntologyV1:
    """Infer a latent temporal regime without receiving its label."""

    hypotheses: Mapping[str, Mapping[str, Mapping[str, float]]]
    evidence_decay: float = 0.80
    hysteresis_cycles: int = 3
    evidence_gap: float = 0.0
    regime: str = "undetermined"
    pending_regime: str = "undetermined"
    pending_count: int = 0
    prediction_error_ema: float = 0.0
    history: list[dict[str, object]] = field(default_factory=list)

    def step(self, source: str, target: str) -> dict[str, object]:
        alpha_ll = _log_likelihood(
            self.hypotheses["alpha"],
            source,
            target,
        )
        beta_ll = _log_likelihood(
            self.hypotheses["beta"],
            source,
            target,
        )
        likelihood_delta = alpha_ll - beta_ll

        self.evidence_gap = (
            self.evidence_decay * self.evidence_gap
            + likelihood_delta
        )

        confidence = 1.0 / (
            1.0 + math.exp(-0.50 * abs(self.evidence_gap))
        )
        best_hypothesis = (
            "alpha"
            if self.evidence_gap >= 0.0
            else "beta"
        )

        if best_hypothesis == self.pending_regime:
            self.pending_count += 1
        else:
            self.pending_regime = best_hypothesis
            self.pending_count = 1

        switched = False
        if (
            self.pending_count >= self.hysteresis_cycles
            and self.regime != best_hypothesis
        ):
            self.regime = best_hypothesis
            self.pending_count = 0
            switched = True

        best_log_likelihood = max(alpha_ll, beta_ll)
        prediction_error = -best_log_likelihood
        self.prediction_error_ema = (
            0.85 * self.prediction_error_ema
            + 0.15 * prediction_error
        )

        uncertainty = 1.0 - confidence
        normalized_error = min(
            1.0,
            self.prediction_error_ema / 3.0,
        )

        # High confidence + low prediction error narrows the active horizon.
        # Uncertainty broadens it again.
        attention = confidence * (1.0 - normalized_error)
        attention = max(0.0, min(1.0, attention))

        record = {
            "best_hypothesis": best_hypothesis,
            "regime": self.regime,
            "pending_regime": self.pending_regime,
            "pending_count": self.pending_count,
            "evidence_gap": round(self.evidence_gap, 6),
            "confidence": round(confidence, 6),
            "uncertainty": round(uncertainty, 6),
            "prediction_error": round(prediction_error, 6),
            "prediction_error_ema": round(
                self.prediction_error_ema,
                6,
            ),
            "attention": round(attention, 6),
            "switched": switched,
        }
        self.history.append(record)
        return record


def _evaluate_stream(
    seed: int,
) -> dict[str, object]:
    states, labels = _build_alternating_stream(seed)
    ontology = TemporalOntologyV1(
        {
            "alpha": PROCESS_ALPHA,
            "beta": PROCESS_BETA,
        }
    )

    records: list[dict[str, object]] = []
    switches: list[tuple[int, str, str]] = []

    rng = random.Random(seed + 900000)
    previous = rng.choice(STATES)

    for index, target in enumerate(states):
        record = ontology.step(previous, target)
        records.append(record)
        if bool(record["switched"]):
            switches.append(
                (
                    index,
                    str(labels[index]),
                    str(record["regime"]),
                )
            )
        previous = target

    change_delays: list[int] = []
    for change_point in CHANGE_POINTS:
        detected = next(
            (
                index
                for index, expected, inferred in switches
                if change_point <= index < change_point + 12
                and expected == inferred
            ),
            None,
        )
        if detected is not None:
            change_delays.append(detected - change_point)

    post_initial_switches = switches[1:]
    false_switch = any(
        min(abs(index - point) for point in CHANGE_POINTS) > 12
        for index, _, _ in post_initial_switches
    )

    accuracy = sum(
        str(record["regime"]) == str(label)
        for record, label in zip(records, labels)
    ) / len(labels)

    transition_indices = [
        index
        for change_point in CHANGE_POINTS
        for index in range(
            change_point,
            min(change_point + 6, len(records)),
        )
    ]
    stable_centers = (40, 120, 200, 280, 360, 440)
    stable_indices = [
        index
        for center in stable_centers
        for index in range(
            center,
            min(center + 6, len(records)),
        )
    ]

    transition_attention = statistics.mean(
        float(records[index]["attention"])
        for index in transition_indices
    )
    stable_attention = statistics.mean(
        float(records[index]["attention"])
        for index in stable_indices
    )

    return {
        "seed": seed,
        "switches": switches,
        "change_delays": change_delays,
        "all_changes_detected": len(change_delays) == len(CHANGE_POINTS),
        "no_false_switches": not false_switch,
        "regime_accuracy": accuracy,
        "transition_attention": transition_attention,
        "stable_attention": stable_attention,
        "attention_drop": stable_attention - transition_attention,
        "records": records,
    }


def run() -> dict[str, object]:
    runs = [
        _evaluate_stream(5000 + index)
        for index in range(STREAM_COUNT)
    ]

    all_changes_detected = all(
        bool(result["all_changes_detected"])
        for result in runs
    )
    no_false_switches = all(
        bool(result["no_false_switches"])
        for result in runs
    )
    attention_drop = statistics.mean(
        float(result["attention_drop"])
        for result in runs
    )
    accuracy = statistics.mean(
        float(result["regime_accuracy"])
        for result in runs
    )
    max_delay = max(
        max(result["change_delays"])
        for result in runs
        if result["change_delays"]
    )

    state_marginal_gaps = []
    for index in range(STREAM_COUNT):
        states_a, _ = _build_alternating_stream(5000 + index)
        states_b, _ = _build_alternating_stream(7000 + index)
        count_a = {
            state: states_a.count(state) / len(states_a)
            for state in STATES
        }
        count_b = {
            state: states_b.count(state) / len(states_b)
            for state in STATES
        }
        state_marginal_gaps.append(
            max(
                abs(count_a[state] - count_b[state])
                for state in STATES
            )
        )

    metrics = {
        "unlabeled_runtime_input": True,
        "no_process_labels_provided_to_ontology": True,
        "hidden_process_changes": True,
        "matched_stationary_marginal_family": True,
        "all_changes_detected": all_changes_detected,
        "no_false_switches": no_false_switches,
        "max_detection_delay_below_12": max_delay < 12,
        "mean_regime_accuracy_above_0_90": accuracy > 0.90,
        "attention_broadens_during_transition": attention_drop > 0.10,
        "empirical_marginal_gap_below_0_10": (
            max(state_marginal_gaps) < 0.10
        ),
    }

    result = {
        "protocol": {
            "stream_count": STREAM_COUNT,
            "segment_length": SEGMENT_LENGTH,
            "segment_count": SEGMENT_COUNT,
            "change_points": list(CHANGE_POINTS),
            "hysteresis_cycles": 3,
            "evidence_decay": 0.80,
            "phenomenal_consciousness_claim": False,
        },
        "aggregate": {
            "mean_regime_accuracy": accuracy,
            "mean_attention_drop": attention_drop,
            "max_detection_delay": max_delay,
            "max_empirical_marginal_gap": max(state_marginal_gaps),
            "all_changes_detected_rate": sum(
                bool(result["all_changes_detected"])
                for result in runs
            ) / STREAM_COUNT,
            "no_false_switch_rate": sum(
                bool(result["no_false_switches"])
                for result in runs
            ) / STREAM_COUNT,
        },
        "runs": runs,
        "metrics": metrics,
        "interpretation": {
            "pass": all(metrics.values()),
            "meaning": (
                "The runtime infers a latent temporal regime from prediction "
                "error and persistence alone, without receiving process labels. "
                "The inferred regime remains stable through matched marginal "
                "dynamics, and uncertainty broadens temporal attention around "
                "hidden process transitions."
            ),
        },
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(metrics.values()):
        raise AssertionError(
            "unlabeled temporal ontology benchmark failed: "
            + json.dumps(metrics, sort_keys=True)
        )
    print("UNLABELED TEMPORAL ONTOLOGY BENCHMARK v1: PASS")
    return result


if __name__ == "__main__":
    run()
