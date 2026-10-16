from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt
from typing import Any, Mapping


SELF_OBSERVATION_RUNTIME_KEYS = {
    "self_observation_state",
    "self_observation_expected",
    "self_observation_error",
    "self_observation_sequence",
    "self_observation_history",
}


def _clamp01(value: Any, default: float = 0.0) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return default
    return max(0.0, min(1.0, float(value)))


@dataclass(frozen=True)
class SelfObservationProfile:
    coherence: float = 0.0
    self_state_level: float = 0.0
    homeostatic_fit: float = 0.0
    self_model_prediction_error: float = 0.0
    trajectory_presence: float = 0.0
    action_reentry: float = 0.0
    pending_action_presence: float = 0.0
    valuation_presence: float = 0.0
    dissonance_fit: float = 1.0
    metacognitive_trace_presence: float = 0.0
    decision_attribution_coverage: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {key: round(float(value), 6) for key, value in asdict(self).items()}

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "SelfObservationProfile":
        if not isinstance(value, Mapping):
            raise ValueError("self_observation must be a mapping")
        payload = {}
        for key in cls.__dataclass_fields__:
            payload[key] = _clamp01(value.get(key), getattr(cls(), key))
        return cls(**payload)


def _self_model_prediction_error(
    self_state: Mapping[str, Any],
    self_model: Mapping[str, Any],
) -> float:
    expected = self_model.get("expected_self_state", {})
    if not isinstance(expected, Mapping):
        return 0.0

    differences: list[float] = []
    for key, expected_value in expected.items():
        actual_value = self_state.get(str(key))
        if (
            isinstance(expected_value, (int, float))
            and not isinstance(expected_value, bool)
            and isinstance(actual_value, (int, float))
            and not isinstance(actual_value, bool)
        ):
            differences.append(abs(float(actual_value) - float(expected_value)))

    if not differences:
        return 0.0
    return _clamp01(sum(differences) / len(differences))


def build_self_observation(
    snapshot: Mapping[str, Any],
) -> SelfObservationProfile:
    """Derive a bounded observation of the runtime's own operational state."""
    self_state = snapshot.get("self_state", {})
    self_model = snapshot.get("self_model", {})
    selected = snapshot.get("selected_trajectory")
    pending = snapshot.get("pending_action")
    history = snapshot.get("action_history", [])
    affective = snapshot.get("affective_state", {})
    valuation = snapshot.get("valuation", {})

    if not isinstance(self_state, Mapping):
        self_state = {}
    if not isinstance(self_model, Mapping):
        self_model = {}
    metacognitive = self_model.get("metacognitive_trace", {})
    if not isinstance(affective, Mapping):
        affective = {}
    if not isinstance(history, list):
        history = []
    if not isinstance(valuation, Mapping):
        valuation = {}
    if not isinstance(metacognitive, Mapping):
        metacognitive = {}

    last_action = history[-1] if history and isinstance(history[-1], Mapping) else {}
    action_reentry = 1.0 if (
        isinstance(last_action, Mapping)
        and last_action.get("status") in {"completed", "failed"}
        and isinstance(last_action.get("outcome"), Mapping)
    ) else 0.0

    # Include a bounded measurement of numeric internal state, otherwise a
    # change in focus/energy could remain invisible to self-observation.
    state_values = [
        _clamp01(value)
        for value in self_state.values()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    ]
    self_state_level = (
        sum(state_values) / len(state_values) if state_values else 0.0
    )

    homeostatic_fit = affective.get("homeostatic_fit", 0.0)
    attribution_keys = (
        "candidate_ids",
        "candidate_scores",
        "selected_signal_contributions",
        "valuation_weights",
    )
    attribution_coverage = (
        sum(1.0 for key in attribution_keys if key in metacognitive)
        / float(len(attribution_keys))
        if metacognitive
        else 0.0
    )

    return SelfObservationProfile(
        coherence=_clamp01(snapshot.get("coherence"), 0.0),
        self_state_level=round(self_state_level, 6),
        homeostatic_fit=_clamp01(homeostatic_fit, 0.0),
        self_model_prediction_error=_self_model_prediction_error(
            self_state,
            self_model,
        ),
        trajectory_presence=1.0 if isinstance(selected, Mapping) and selected else 0.0,
        action_reentry=action_reentry,
        pending_action_presence=1.0 if isinstance(pending, Mapping) and pending else 0.0,
        valuation_presence=1.0 if valuation else 0.0,
        dissonance_fit=1.0 - _clamp01(snapshot.get("self_dissonance"), 0.0),
        metacognitive_trace_presence=1.0 if metacognitive else 0.0,
        decision_attribution_coverage=round(attribution_coverage, 6),
    )


def profile_distance(
    left: SelfObservationProfile | Mapping[str, Any],
    right: SelfObservationProfile | Mapping[str, Any],
) -> float:
    left_profile = (
        left if isinstance(left, SelfObservationProfile)
        else SelfObservationProfile.from_mapping(left)
    )
    right_profile = (
        right if isinstance(right, SelfObservationProfile)
        else SelfObservationProfile.from_mapping(right)
    )
    deltas = [
        float(getattr(left_profile, key)) - float(getattr(right_profile, key))
        for key in SelfObservationProfile.__dataclass_fields__
    ]
    return round(_clamp01(sqrt(sum(delta * delta for delta in deltas) / len(deltas))), 6)


def blend_profiles(
    previous: SelfObservationProfile,
    current: SelfObservationProfile,
    rate: float,
) -> SelfObservationProfile:
    alpha = _clamp01(rate, 0.25)
    return SelfObservationProfile(
        **{
            key: round(
                (1.0 - alpha) * float(getattr(previous, key))
                + alpha * float(getattr(current, key)),
                6,
            )
            for key in SelfObservationProfile.__dataclass_fields__
        }
    )
