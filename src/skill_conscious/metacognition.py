from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping


METACOGNITIVE_RUNTIME_KEYS = {
    "metacognitive_trace",
    "metacognitive_sequence",
    "metacognitive_history",
}


@dataclass(frozen=True)
class MetacognitiveTrace:
    sequence: int
    revision: int
    selection_source: str
    selected_id: str
    candidate_ids: list[str]
    candidate_scores: dict[str, float]
    selected_score: float
    selected_signal_contributions: dict[str, float]
    self_observation: dict[str, float]
    experience_dynamics: dict[str, float]
    metacognitive_prediction: dict[str, float]
    valuation_weights: dict[str, float]
    predicted_outcome: dict[str, Any] | None = None
    predicted_state_delta: dict[str, Any] | None = None
    prediction_error: float | None = None
    prediction_accuracy: float | None = None
    prediction_diagnostics: dict[str, Any] | None = None
    action: dict[str, Any] | None = None
    outcome: dict[str, Any] | None = None
    state_delta: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _numeric_mapping(value: Mapping[str, Any] | None) -> dict[str, float]:
    if not isinstance(value, Mapping):
        return {}
    return {
        str(key): float(raw)
        for key, raw in value.items()
        if isinstance(raw, (int, float)) and not isinstance(raw, bool)
    }


def state_delta(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    keys: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    selected_keys = keys or (
        "self_state",
        "self_model",
        "workspace",
        "intention",
        "selected_trajectory",
        "valuation",
        "valence",
        "coherence",
        "self_dissonance",
        "interoceptive_state",
        "affective_state",
        "temporal_state",
        "regime",
    )
    result: dict[str, Any] = {}
    for key in selected_keys:
        left = before.get(key)
        right = after.get(key)
        if left != right:
            result[str(key)] = {
                "before": left,
                "after": right,
            }
    return result


def build_metacognitive_trace(
    *,
    revision: int,
    sequence: int,
    candidates: list[Mapping[str, Any]],
    selected: Mapping[str, Any],
    selection_source: str,
    valuation_weights: Mapping[str, Any],
) -> MetacognitiveTrace:
    selected_id = str(selected.get("id", ""))
    candidate_ids = [str(item.get("id", "")) for item in candidates]
    candidate_scores = {
        str(item.get("id", "")): round(float(item.get("score", 0.0)), 6)
        for item in candidates
        if str(item.get("id", ""))
    }

    raw_breakdown = selected.get("_metacognitive_breakdown", {})
    if not isinstance(raw_breakdown, Mapping):
        raw_breakdown = {}

    raw_signals = raw_breakdown.get("signal_contributions", {})
    selected_signal_contributions = _numeric_mapping(raw_signals)

    raw_self = raw_breakdown.get("self_observation", {})
    raw_dynamic = raw_breakdown.get("experience_dynamics", {})
    raw_metacognitive_prediction = raw_breakdown.get("metacognitive_prediction", {})
    raw_predicted_outcome = selected.get("predicted_outcome")
    raw_predicted_state_delta = selected.get("predicted_state_delta")

    self_observation = {
        str(key): float(value)
        for key, value in raw_self.items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    } if isinstance(raw_self, Mapping) else {}

    experience_dynamics = {
        str(key): float(value)
        for key, value in raw_dynamic.items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    } if isinstance(raw_dynamic, Mapping) else {}

    metacognitive_prediction = {
        str(key): float(value)
        for key, value in raw_metacognitive_prediction.items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    } if isinstance(raw_metacognitive_prediction, Mapping) else {}

    return MetacognitiveTrace(
        sequence=int(sequence),
        revision=int(revision),
        selection_source=str(selection_source),
        selected_id=selected_id,
        candidate_ids=candidate_ids,
        candidate_scores=candidate_scores,
        selected_score=round(float(selected.get("score", 0.0)), 6),
        selected_signal_contributions=selected_signal_contributions,
        self_observation=self_observation,
        experience_dynamics=experience_dynamics,
        metacognitive_prediction=metacognitive_prediction,
        valuation_weights=_numeric_mapping(valuation_weights),
        predicted_outcome=(
            dict(raw_predicted_outcome)
            if isinstance(raw_predicted_outcome, Mapping)
            else None
        ),
        predicted_state_delta=(
            dict(raw_predicted_state_delta)
            if isinstance(raw_predicted_state_delta, Mapping)
            else None
        ),
    )
