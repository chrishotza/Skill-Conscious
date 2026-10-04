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


def _compact_action_history(value: Any) -> dict[str, Any]:
    """Summarize action history so metacognitive traces cannot recursively embed it."""
    if not isinstance(value, list):
        return {"count": 0, "last_action_id": None, "last_trajectory": None, "last_status": None}

    entries = [item for item in value if isinstance(item, Mapping)]
    last = entries[-1] if entries else {}
    trajectory = last.get("trajectory", {})
    trajectory_id = (
        str(trajectory.get("id", ""))
        if isinstance(trajectory, Mapping) and trajectory.get("id") is not None
        else None
    )
    return {
        "count": len(value),
        "last_action_id": (
            str(last.get("action_id", ""))
            if last.get("action_id") is not None
            else None
        ),
        "last_trajectory": trajectory_id or None,
        "last_status": (
            str(last.get("status", ""))
            if last.get("status") is not None
            else None
        ),
        "last_revision": (
            int(last.get("revision"))
            if isinstance(last.get("revision"), int)
            else None
        ),
    }


def _compact_mapping_state(value: Any) -> dict[str, Any]:
    """Summarize nested runtime mappings without copying recursive log structures."""
    if not isinstance(value, Mapping):
        return {"type": type(value).__name__}

    scalar_values: dict[str, Any] = {}
    containers: dict[str, dict[str, Any]] = {}

    for raw_key, raw_value in value.items():
        key = str(raw_key)
        if isinstance(raw_value, (str, int, float, bool)) or raw_value is None:
            if isinstance(raw_value, str) and len(raw_value) > 128:
                scalar_values[key] = raw_value[:128]
            else:
                scalar_values[key] = raw_value
        elif isinstance(raw_value, Mapping):
            containers[key] = {
                "type": "mapping",
                "size": len(raw_value),
                "keys": sorted(str(item) for item in raw_value.keys())[:64],
            }
        elif isinstance(raw_value, list):
            containers[key] = {
                "type": "list",
                "length": len(raw_value),
            }
        else:
            containers[key] = {"type": type(raw_value).__name__}

    return {
        "type": "mapping",
        "size": len(value),
        "scalar_values": scalar_values,
        "containers": containers,
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
        "pending_action",
        "action_history",
    )
    result: dict[str, Any] = {}
    compact_keys = {"self_model", "workspace", "action_history"}

    for key in selected_keys:
        left = before.get(key)
        right = after.get(key)

        if key == "action_history":
            left = _compact_action_history(left)
            right = _compact_action_history(right)
        elif key in compact_keys:
            left = _compact_mapping_state(left)
            right = _compact_mapping_state(right)

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
