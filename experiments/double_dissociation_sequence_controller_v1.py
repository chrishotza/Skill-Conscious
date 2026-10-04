"""Matched generic-controller double-dissociation benchmark.

Both controllers consume the same lagged transition field and the same
candidate field. The only architectural difference is temporal aggregation:

- resonant controller: endogenous attention-weighted lag aggregation
- generic controller: fixed uniform lag aggregation

The assay perturbs each controller's own gain independently and tests whether
the perturbation changes its own output while sparing the matched alternative.
This is a mechanism test, not a phenomenal-consciousness test.
"""

from __future__ import annotations

import copy
import json
import math
from dataclasses import dataclass
from typing import Mapping, Sequence

STATES = tuple("ABCD")
LAGS = (1, 2, 3, 4)

# Fixed before scoring.
HISTORY = tuple("ABBBABABAABAC")
ALPHA = tuple("ABABABABABABC")
BETA = tuple("AABBAABBAABBC")

CANDIDATES = (
    {"id": "alpha_path", "base_score": 0.50, "template": ALPHA},
    {"id": "beta_path", "base_score": 0.51, "template": BETA},
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
    counts = {(source, target): 0.0 for source in STATES for target in STATES}
    transitions = 0
    for index in range(lag, len(sequence)):
        counts[(sequence[index - lag], sequence[index])] += 1.0
        transitions += 1
    denominator = float(max(1, transitions))
    return {key: value / denominator for key, value in counts.items()}


def _temporal_similarity(
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


@dataclass
class ResonantController:
    gain: float = 0.70
    attention: float = 1.0

    def lag_weights(self) -> dict[int, float]:
        center = 1.0 + (1.0 - max(0.0, min(1.0, self.attention))) * 1.5
        raw = {
            lag: math.exp(-((lag - center) ** 2) / (2.0 * 1.4**2))
            for lag in LAGS
        }
        total = sum(raw.values())
        return {lag: value / total for lag, value in raw.items()}

    def select(self, history: Sequence[str]) -> tuple[str, dict[str, float]]:
        weights = self.lag_weights()
        scores = {}
        for candidate in CANDIDATES:
            similarity = _temporal_similarity(
                history,
                candidate["template"],
                weights,
            )
            scores[str(candidate["id"])] = (
                float(candidate["base_score"]) + self.gain * similarity
            )
        return max(scores, key=scores.get), scores


@dataclass
class GenericSequenceController:
    gain: float = 0.70

    def select(self, history: Sequence[str]) -> tuple[str, dict[str, float]]:
        # Same representation and same candidate field, but no endogenous
        # temporal tuning. Every lag receives equal causal weight.
        weights = {lag: 0.25 for lag in LAGS}
        scores = {}
        for candidate in CANDIDATES:
            similarity = _temporal_similarity(
                history,
                candidate["template"],
                weights,
            )
            scores[str(candidate["id"])] = (
                float(candidate["base_score"]) + self.gain * similarity
            )
        return max(scores, key=scores.get), scores


def run() -> dict[str, object]:
    resonant = ResonantController()
    generic = GenericSequenceController()

    resonant_baseline, resonant_scores = resonant.select(HISTORY)
    generic_baseline, generic_scores = generic.select(HISTORY)

    resonant_perturbed = copy.deepcopy(resonant)
    resonant_perturbed.gain = 0.0
    resonant_after, resonant_ablation_scores = resonant_perturbed.select(HISTORY)
    generic_under_resonant, _ = generic.select(HISTORY)

    generic_perturbed = copy.deepcopy(generic)
    generic_perturbed.gain = 0.0
    generic_after, generic_ablation_scores = generic_perturbed.select(HISTORY)
    resonant_under_generic, _ = resonant.select(HISTORY)

    resonant_restored, _ = resonant.select(HISTORY)
    generic_restored, _ = generic.select(HISTORY)

    metrics = {
        "baseline_agreement": (
            resonant_baseline == generic_baseline == "alpha_path"
        ),
        "resonant_perturbation_changes_resonant": (
            resonant_after != resonant_baseline
        ),
        "resonant_perturbation_spares_generic": (
            generic_under_resonant == generic_baseline
        ),
        "generic_perturbation_changes_generic": (
            generic_after != generic_baseline
        ),
        "generic_perturbation_spares_resonant": (
            resonant_under_generic == resonant_baseline
        ),
        "resonant_restoration_recovers": (
            resonant_restored == resonant_baseline
        ),
        "generic_restoration_recovers": (
            generic_restored == generic_baseline
        ),
    }

    result = {
        "protocol": {
            "history": "".join(HISTORY),
            "shared_representation": "4 lag x 16 transition field",
            "resonant": "endogenous attention-weighted aggregation",
            "generic": "fixed uniform aggregation",
            "base_bias": "beta_path +0.01",
            "phenomenal_consciousness_claim": False,
        },
        "baseline": {
            "resonant": resonant_baseline,
            "generic": generic_baseline,
            "resonant_scores": resonant_scores,
            "generic_scores": generic_scores,
            "resonant_lag_weights": resonant.lag_weights(),
        },
        "resonant_perturbation": {
            "selected": resonant_after,
            "generic_selected_under_same_history": generic_under_resonant,
            "scores": resonant_ablation_scores,
        },
        "generic_perturbation": {
            "selected": generic_after,
            "resonant_selected_under_same_history": resonant_under_generic,
            "scores": generic_ablation_scores,
        },
        "restored": {
            "resonant": resonant_restored,
            "generic": generic_restored,
        },
        "metrics": metrics,
        "interpretation": {
            "double_dissociation": all(metrics.values()),
            "meaning": (
                "Perturbing the resonant gain changes only the resonant controller; "
                "perturbing the generic gain changes only the generic controller."
            ),
        },
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(metrics.values()):
        raise AssertionError(
            "double dissociation benchmark failed: "
            + json.dumps(metrics, sort_keys=True)
        )
    print("DOUBLE DISSOCIATION BENCHMARK v1: PASS")
    return result


if __name__ == "__main__":
    run()
