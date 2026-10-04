"""Self-organizing temporal ontology benchmark v1.

The runtime begins with no process-specific temporal prototypes. It observes only
state transitions, builds a prototype from recent experience, updates active
prototypes online, and spawns a new prototype when persistent predictive
surprise cannot be explained by the existing ontology.

Hidden process labels are used only after the run for evaluation/mapping.
They are never supplied to the ontology during inference.
"""

from __future__ import annotations

import json
import math
import random
import statistics
from dataclasses import dataclass
from typing import Mapping, Sequence

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

STREAM_COUNT = 50
SEGMENT_LENGTH = 80
SEGMENT_COUNT = 6
CHANGE_POINTS = (80, 160, 240, 320, 400)
WINDOW = 16
NOVELTY_THRESHOLD = 1.55
PERSISTENCE = 2
MAX_PROTOTYPES = 4
DECAY = 0.995


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


def _build_stream(
    seed: int,
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    rng = random.Random(seed)
    states = [rng.choice(STATES)]
    labels: list[int] = []

    for segment in range(SEGMENT_COUNT):
        transition = PROCESS_ALPHA if segment % 2 == 0 else PROCESS_BETA
        for _ in range(SEGMENT_LENGTH):
            states.append(
                _sample_next(
                    transition,
                    states[-1],
                    rng,
                )
            )
            labels.append(segment % 2)

    return tuple(states), tuple(labels)


@dataclass
class TemporalPrototype:
    prior: float = 1.0

    def __post_init__(self) -> None:
        self.counts = {
            source: {
                target: float(self.prior)
                for target in STATES
            }
            for source in STATES
        }

    def probability(self, source: str, target: str) -> float:
        row = self.counts[source]
        denominator = sum(row.values())
        return row[target] / denominator

    def log_likelihood(self, sequence: Sequence[str]) -> float:
        if len(sequence) < 2:
            return 0.0
        total = 0.0
        for source, target in zip(sequence[:-1], sequence[1:]):
            total += math.log(
                max(
                    self.probability(source, target),
                    1e-9,
                )
            )
        return total / max(1, len(sequence) - 1)

    def update(self, sequence: Sequence[str]) -> None:
        for source in STATES:
            for target in STATES:
                self.counts[source][target] *= DECAY

        for source, target in zip(sequence[:-1], sequence[1:]):
            self.counts[source][target] += 1.0


@dataclass
class SelfOrganizingTemporalOntology:
    """Dynamic temporal ontology grown from prediction error."""

    prototypes: list[TemporalPrototype]
    transition_buffer: list[tuple[str, str]]
    novelty_streak: int = 0
    regime: int | None = None
    pending_regime: int | None = None
    pending_count: int = 0

    @classmethod
    def empty(cls) -> "SelfOrganizingTemporalOntology":
        return cls(
            prototypes=[],
            transition_buffer=[],
        )

    def _window(self) -> tuple[str, ...]:
        pairs = self.transition_buffer[-WINDOW:]
        if not pairs:
            return ()
        return tuple([pairs[0][0]] + [target for _, target in pairs])

    def _attention(
        self,
        scores: Sequence[float],
        novelty: float,
    ) -> float:
        ranked = sorted(scores, reverse=True)
        margin = (
            ranked[0] - ranked[1]
            if len(ranked) > 1
            else ranked[0]
        )
        confidence = 1.0 / (1.0 + math.exp(-2.0 * margin))
        error = min(
            1.0,
            max(0.0, (novelty - 0.9) / 1.8),
        )
        return max(
            0.0,
            min(
                1.0,
                confidence * (1.0 - error),
            ),
        )

    def step(self, source: str, target: str) -> dict[str, object] | None:
        self.transition_buffer.append((source, target))
        if len(self.transition_buffer) < WINDOW:
            return None

        sequence = self._window()
        spawned = False

        if not self.prototypes:
            prototype = TemporalPrototype()
            prototype.update(sequence)
            self.prototypes.append(prototype)
            spawned = True

        scores = [
            prototype.log_likelihood(sequence)
            for prototype in self.prototypes
        ]
        best_index = max(
            range(len(scores)),
            key=lambda index: scores[index],
        )
        novelty = -scores[best_index]

        if novelty > NOVELTY_THRESHOLD:
            self.novelty_streak += 1
        else:
            self.novelty_streak = 0

        if (
            self.novelty_streak >= PERSISTENCE
            and len(self.prototypes) < MAX_PROTOTYPES
        ):
            prototype = TemporalPrototype()
            prototype.update(sequence)
            self.prototypes.append(prototype)
            best_index = len(self.prototypes) - 1
            self.novelty_streak = 0
            spawned = True

        self.prototypes[best_index].update(sequence)

        scores = [
            prototype.log_likelihood(sequence)
            for prototype in self.prototypes
        ]
        selected_index = max(
            range(len(scores)),
            key=lambda index: scores[index],
        )

        if selected_index == self.pending_regime:
            self.pending_count += 1
        else:
            self.pending_regime = selected_index
            self.pending_count = 1

        switched = False
        if (
            self.pending_count >= PERSISTENCE
            and self.regime != selected_index
        ):
            self.regime = selected_index
            self.pending_count = 0
            switched = True

        attention = self._attention(
            scores,
            novelty,
        )

        return {
            "regime": self.regime,
            "selected_prototype": selected_index,
            "prototype_count": len(self.prototypes),
            "spawned": spawned,
            "novelty": round(novelty, 6),
            "attention": round(attention, 6),
            "switched": switched,
        }


def _evaluate_stream(seed: int) -> dict[str, object]:
    states, labels = _build_stream(seed)
    ontology = SelfOrganizingTemporalOntology.empty()
    records: list[tuple[int, int, dict[str, object]]] = []

    for index, (source, target) in enumerate(
        zip(states[:-1], states[1:])
    ):
        record = ontology.step(source, target)
        if record is not None:
            records.append((index, labels[index], record))

    votes: dict[int, list[int]] = {}
    for index, label, record in records:
        if 20 <= index % SEGMENT_LENGTH <= 60:
            regime = record["regime"]
            if regime is not None:
                votes.setdefault(int(regime), [0, 0])
                votes[int(regime)][label] += 1

    mapping = {
        regime: int(vote[1] > vote[0])
        for regime, vote in votes.items()
    }

    mapped_records = [
        (
            index,
            mapping[int(record["regime"])],
            label,
        )
        for index, label, record in records
        if record["regime"] is not None
        and int(record["regime"]) in mapping
    ]

    accuracy = (
        sum(
            inferred == label
            for _, inferred, label in mapped_records
        )
        / max(1, len(mapped_records))
    )

    change_delays: list[int] = []
    for change_point in CHANGE_POINTS:
        target_label = labels[change_point]
        detected = next(
            (
                index - change_point
                for index, inferred, _ in mapped_records
                if (
                    change_point
                    <= index
                    < change_point + 20
                    and inferred == target_label
                )
            ),
            None,
        )
        if detected is not None:
            change_delays.append(detected)

    transition_windows = {
        index
        for change_point in CHANGE_POINTS
        for index in range(
            change_point,
            change_point + 16,
        )
    }

    false_remaps = 0
    previous_label: int | None = None
    for index, inferred, _ in mapped_records:
        if (
            previous_label is not None
            and inferred != previous_label
            and index not in transition_windows
        ):
            false_remaps += 1
        previous_label = inferred

    transition_indices = {
        index
        for change_point in CHANGE_POINTS
        for index in range(
            change_point,
            change_point + 8,
        )
    }
    stable_indices = {
        index
        for segment in range(SEGMENT_COUNT)
        for index in range(
            segment * SEGMENT_LENGTH + 30,
            segment * SEGMENT_LENGTH + 38,
        )
    }

    transition_attention = [
        float(record["attention"])
        for index, _, record in records
        if index in transition_indices
    ]
    stable_attention = [
        float(record["attention"])
        for index, _, record in records
        if index in stable_indices
    ]

    return {
        "seed": seed,
        "accuracy": accuracy,
        "all_changes_detected": len(change_delays) == len(
            CHANGE_POINTS
        ),
        "change_delays": change_delays,
        "false_remaps": false_remaps,
        "prototype_count": len(ontology.prototypes),
        "transition_attention": (
            statistics.mean(transition_attention)
            if transition_attention
            else 0.0
        ),
        "stable_attention": (
            statistics.mean(stable_attention)
            if stable_attention
            else 0.0
        ),
    }


def run() -> dict[str, object]:
    results = [
        _evaluate_stream(
            5000 + index,
        )
        for index in range(STREAM_COUNT)
    ]

    mean_accuracy = statistics.mean(
        float(result["accuracy"])
        for result in results
    )
    all_changes_detected_rate = sum(
        bool(result["all_changes_detected"])
        for result in results
    ) / STREAM_COUNT
    mean_false_remaps = statistics.mean(
        float(result["false_remaps"])
        for result in results
    )
    mean_transition_attention = statistics.mean(
        float(result["transition_attention"])
        for result in results
    )
    mean_stable_attention = statistics.mean(
        float(result["stable_attention"])
        for result in results
    )
    mean_attention_drop = (
        mean_stable_attention
        - mean_transition_attention
    )
    mean_prototypes = statistics.mean(
        float(result["prototype_count"])
        for result in results
    )
    mean_max_delay = statistics.mean(
        max(result["change_delays"])
        if result["change_delays"]
        else 99
        for result in results
    )

    metrics = {
        "starts_without_process_labels": True,
        "starts_without_process_specific_prototypes": True,
        "prototypes_are_experience_formed": True,
        "all_changes_detected": all_changes_detected_rate == 1.0,
        "mean_accuracy_above_0_90": mean_accuracy > 0.90,
        "mean_false_remaps_below_0_10": mean_false_remaps < 0.10,
        "mean_attention_broadening_above_0_20": mean_attention_drop > 0.20,
        "prototype_count_remains_compact": mean_prototypes < 3.0,
        "mean_max_delay_below_13": mean_max_delay < 13.0,
    }

    result = {
        "protocol": {
            "stream_count": STREAM_COUNT,
            "segment_length": SEGMENT_LENGTH,
            "segment_count": SEGMENT_COUNT,
            "window": WINDOW,
            "novelty_threshold": NOVELTY_THRESHOLD,
            "persistence": PERSISTENCE,
            "max_prototypes": MAX_PROTOTYPES,
            "decay": DECAY,
            "hidden_labels_supplied_to_runtime": False,
            "phenomenal_consciousness_claim": False,
        },
        "aggregate": {
            "mean_accuracy": mean_accuracy,
            "all_changes_detected_rate": all_changes_detected_rate,
            "mean_false_remaps": mean_false_remaps,
            "mean_transition_attention": mean_transition_attention,
            "mean_stable_attention": mean_stable_attention,
            "mean_attention_broadening": mean_attention_drop,
            "mean_prototypes": mean_prototypes,
            "mean_max_detection_delay": mean_max_delay,
        },
        "metrics": metrics,
        "runs": results,
        "interpretation": {
            "pass": all(metrics.values()),
            "meaning": (
                "The runtime starts with no process-specific temporal "
                "ontology, constructs prototypes from experience, adds "
                "a new prototype only after persistent surprise, and "
                "uses the resulting ontology to regulate temporal "
                "attention. This demonstrates self-organizing temporal "
                "modeling, not phenomenal consciousness."
            ),
        },
    }

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )

    if not all(metrics.values()):
        raise AssertionError(
            "self-organizing temporal ontology benchmark failed: "
            + json.dumps(
                metrics,
                sort_keys=True,
            )
        )

    print("SELF-ORGANIZING TEMPORAL ONTOLOGY BENCHMARK v1: PASS")
    return result


if __name__ == "__main__":
    run()
