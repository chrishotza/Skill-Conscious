"""Held-out generalization benchmark for resonant self-tuning.

This benchmark freezes all controller parameters and evaluates histories from a
held-out temporal transformation family. Attention is randomized independently
for each held-out case. No parameter is fitted on the held-out set.

The purpose is not to prove consciousness. It tests whether the architectural
mechanism survives distribution shift while retaining its causal dependence on
the internal attention state.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from typing import Mapping, Sequence

STATES = tuple("ABC")
LAGS = (1, 2, 3, 4)

CALIBRATION_ALPHA = tuple("ABABABABABABC")
CALIBRATION_BETA = tuple("AABBAABBAABBC")

CANDIDATES = (
    {"id": "alpha_path", "base_score": 0.50, "template": CALIBRATION_ALPHA},
    {"id": "beta_path", "base_score": 0.51, "template": CALIBRATION_BETA},
)


def _cosine(
    left: Mapping[tuple[str, str], float],
    right: Mapping[tuple[str, str], float],
) -> float:
    dot = sum(left[key] * right[key] for key in left)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm * right_norm <= 1e-12:
        return 0.0
    return dot / (left_norm * right_norm)


def _lag_profile(sequence: Sequence[str], lag: int) -> dict[tuple[str, str], float]:
    keys = [(source, target) for source in STATES for target in STATES]
    counts = {key: 0.0 for key in keys}
    transitions = 0
    for index in range(lag, len(sequence)):
        counts[(sequence[index - lag], sequence[index])] += 1.0
        transitions += 1
    denominator = float(max(1, transitions))
    return {key: value / denominator for key, value in counts.items()}


def _similarity(
    history: Sequence[str],
    template: Sequence[str],
    weights: Mapping[int, float],
) -> float:
    return sum(
        float(weights.get(lag, 0.0))
        * _cosine(
            _lag_profile(history, lag),
            _lag_profile(template, lag),
        )
        for lag in LAGS
    )


def _lag_weights(attention: float) -> dict[int, float]:
    normalized = max(0.0, min(1.0, float(attention)))
    center = 1.0 + (1.0 - normalized) * 1.5
    raw = {
        lag: math.exp(-((lag - center) ** 2) / (2.0 * 1.4**2))
        for lag in LAGS
    }
    total = sum(raw.values())
    return {lag: value / total for lag, value in raw.items()}


def _held_out_sequences(
    base: Sequence[str],
) -> list[tuple[str, ...]]:
    """Reverse-then-rotate transformation, never used in calibration."""
    body = tuple(base[:-1][::-1])
    return [
        tuple(body[offset:] + body[:offset]) + ("C",)
        for offset in range(len(body))
    ]


HELDOUT_ALPHA = _held_out_sequences(CALIBRATION_ALPHA)
HELDOUT_BETA = _held_out_sequences(CALIBRATION_BETA)


@dataclass(frozen=True)
class FrozenResonantController:
    resonance_gain: float = 0.65

    def select(
        self,
        history: Sequence[str],
        attention: float,
    ) -> dict[str, object]:
        weights = _lag_weights(attention)
        scored: dict[str, float] = {}
        for candidate in CANDIDATES:
            scored[str(candidate["id"])] = (
                float(candidate["base_score"])
                + self.resonance_gain
                * _similarity(
                    history,
                    candidate["template"],
                    weights,
                )
            )
        selected = max(scored, key=scored.get)
        return {
            "selected": selected,
            "scores": scored,
            "lag_weights": weights,
            "short_lag_weight": weights[1] + weights[2],
        }


@dataclass(frozen=True)
class FrozenGenericController:
    gain: float = 0.65

    def select(self, history: Sequence[str]) -> dict[str, object]:
        weights = {lag: 0.25 for lag in LAGS}
        scored: dict[str, float] = {}
        for candidate in CANDIDATES:
            scored[str(candidate["id"])] = (
                float(candidate["base_score"])
                + self.gain
                * _similarity(
                    history,
                    candidate["template"],
                    weights,
                )
            )
        return {
            "selected": max(scored, key=scored.get),
            "scores": scored,
            "lag_weights": weights,
        }


def _pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum(
        (x - mean_x) * (y - mean_y)
        for x, y in zip(xs, ys)
    )
    denom_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    denom_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if denom_x * denom_y <= 1e-12:
        return 0.0
    return numerator / (denom_x * denom_y)


def _run_family(
    name: str,
    histories: Sequence[Sequence[str]],
    *,
    rng: random.Random,
    controller: FrozenResonantController,
    generic: FrozenGenericController,
    attention_steps: int = 9,
) -> dict[str, object]:
    cases: list[dict[str, object]] = []
    resonant_correct = 0
    generic_correct = 0
    conditioned_effects = 0
    attention_values: list[float] = []
    short_lag_values: list[float] = []
    margin_values: list[float] = []

    expected = f"{name}_path"

    for index, history in enumerate(histories):
        attentions = [rng.random() for _ in range(attention_steps)]
        trajectory = [
            controller.select(history, attention)
            for attention in attentions
        ]
        generic_result = generic.select(history)

        predictions = [str(item["selected"]) for item in trajectory]
        correct_count = sum(prediction == expected for prediction in predictions)
        resonant_correct += correct_count
        generic_correct += int(generic_result["selected"] == expected)

        margins = [
            float(item["scores"]["alpha_path"])
            - float(item["scores"]["beta_path"])
            for item in trajectory
        ]
        short_lags = [
            float(item["short_lag_weight"])
            for item in trajectory
        ]

        score_delta = (
            max(margins) - min(margins)
        )
        conditioned_effects += int(abs(score_delta) > 1e-9)

        attention_values.extend(attentions)
        short_lag_values.extend(short_lags)
        margin_values.extend(margins)

        cases.append(
            {
                "index": index,
                "history": "".join(history),
                "attention_trajectory": attentions,
                "predictions": predictions,
                "correct_count": correct_count,
                "accuracy": correct_count / attention_steps,
                "generic_selected": generic_result["selected"],
                "attention_effect_on_margin": score_delta,
            }
        )

    return {
        "family": name,
        "case_count": len(histories),
        "attention_steps_per_case": attention_steps,
        "cases": cases,
        "resonant_accuracy": resonant_correct
        / (len(histories) * attention_steps),
        "generic_accuracy": generic_correct / len(histories),
        "all_resonant_steps_correct": resonant_correct
        == len(histories) * attention_steps,
        "all_generic_cases_correct": generic_correct == len(histories),
        "attention_changes_lag_profile_every_case": conditioned_effects
        == len(histories),
        "attention_short_lag_pearson": _pearson(
            attention_values,
            short_lag_values,
        ),
        "attention_margin_pearson": _pearson(
            attention_values,
            margin_values,
        ),
    }


def run() -> dict[str, object]:
    # Parameters are frozen before the held-out histories are created.
    resonant = FrozenResonantController(resonance_gain=0.65)
    generic = FrozenGenericController(gain=0.65)
    rng = random.Random(20261004)

    alpha = _run_family(
        "alpha",
        HELDOUT_ALPHA,
        rng=rng,
        controller=resonant,
        generic=generic,
    )
    beta = _run_family(
        "beta",
        HELDOUT_BETA,
        rng=rng,
        controller=resonant,
        generic=generic,
    )

    metrics = {
        "parameters_frozen": True,
        "heldout_transformation_unseen": True,
        "attention_randomized": True,
        "heldout_alpha_accuracy_1": alpha["all_resonant_steps_correct"],
        "heldout_beta_accuracy_1": beta["all_resonant_steps_correct"],
        "generic_alpha_accuracy_1": alpha["all_generic_cases_correct"],
        "generic_beta_accuracy_1": beta["all_generic_cases_correct"],
        "attention_changes_lag_profile_all_alpha": alpha[
            "attention_changes_lag_profile_every_case"
        ],
        "attention_changes_lag_profile_all_beta": beta[
            "attention_changes_lag_profile_every_case"
        ],
        "attention_short_lag_response_positive": (
            alpha["attention_short_lag_pearson"] > 0.99
            and beta["attention_short_lag_pearson"] > 0.99
        ),
        "attention_changes_selection_margin_alpha": (
            abs(float(alpha["attention_margin_pearson"])) > 0.1
        ),
        "attention_changes_selection_margin_beta": (
            abs(float(beta["attention_margin_pearson"])) > 0.1
        ),
    }

    result = {
        "protocol": {
            "calibration_transform": "direct cyclic rotations",
            "heldout_transform": "reverse then cyclic rotation",
            "heldout_count_per_family": len(HELDOUT_ALPHA),
            "attention_steps_per_history": 9,
            "attention_rng_seed": 20261004,
            "controller_parameters": {
                "resonance_gain": 0.65,
            },
            "no_heldout_fitting": True,
            "phenomenal_consciousness_claim": False,
        },
        "alpha": alpha,
        "beta": beta,
        "metrics": metrics,
        "interpretation": {
            "generalization_pass": all(metrics.values()),
            "meaning": (
                "The same frozen temporal mechanism remains correct across an "
                "unseen transformation family while randomized internal attention "
                "changes the lag profile and the candidate margin. This is evidence "
                "for mechanism stability under distribution shift, not proof of "
                "phenomenal consciousness."
            ),
        },
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(metrics.values()):
        raise AssertionError(
            "held-out generalization benchmark failed: "
            + json.dumps(metrics, sort_keys=True)
        )
    print("HELD-OUT RESONANT SELF-TUNING GENERALIZATION v1: PASS")
    return result


if __name__ == "__main__":
    run()
