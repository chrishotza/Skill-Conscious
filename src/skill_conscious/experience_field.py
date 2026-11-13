from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite, sqrt
from typing import Mapping, Sequence

from .dynamics import DynamicProfile, measure_dynamics
from .sensor_affect import SensoryAffectiveSnapshot, appraise_sensory_field, score_action_with_affect


@dataclass(frozen=True)
class ExperienceFieldProfile:
    """Coupled sensory-affective-dynamic state vector.

    This is an engineering representation of the current integrated field.
    It is not a consciousness score and does not establish subjective experience.
    """

    prediction_error: float
    sensory_coherence: float
    valence: float
    self_relevance: float
    dynamic_persistence: float
    dynamic_synchrony: float
    dynamic_metastability: float
    dynamic_complexity: float
    avalanche_activity: float
    field_coherence: float
    dynamic_repertoire: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def build_experience_field(
    observation: Mapping[str, float],
    expected: Mapping[str, float],
    channels: Sequence[Sequence[float]],
    *,
    scales: Mapping[str, float] | None = None,
    affective_weights: Mapping[str, float] | None = None,
    self_relevance_weights: Mapping[str, float] | None = None,
    avalanche_threshold_sigma: float = 2.0,
    coupling_weights: Mapping[str, float] | None = None,
) -> tuple[ExperienceFieldProfile, SensoryAffectiveSnapshot, DynamicProfile]:
    sensory = appraise_sensory_field(
        observation,
        expected,
        scales=scales,
        affective_weights=affective_weights,
        self_relevance_weights=self_relevance_weights,
    )
    dynamic = measure_dynamics(channels, avalanche_threshold_sigma=avalanche_threshold_sigma)

    weights = {"sensory_coherence": 1.0, "dynamic_synchrony": 1.0}
    if coupling_weights is not None:
        for name, raw in coupling_weights.items():
            if name not in weights:
                raise ValueError(f"unknown coupling weight: {name}")
            if isinstance(raw, bool):
                raise ValueError(f"coupling weight {name} must be finite and nonnegative")
            try:
                value = float(raw)
            except (ValueError, TypeError, OverflowError) as exc:
                raise ValueError(f"coupling weight {name} must be finite and nonnegative") from exc
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"coupling weight {name} must be finite and nonnegative")
            weights[name] = value
    if not isfinite(sum(weights.values())):
        raise ValueError("coupling weights must have a finite total")

    field_coherence = (
        weights["sensory_coherence"] * sensory.coherence
        + weights["dynamic_synchrony"] * dynamic.pairwise_correlation
    ) / max(1e-12, weights["sensory_coherence"] + weights["dynamic_synchrony"])

    dynamic_repertoire = 0.5 * dynamic.metastability + 0.5 * dynamic.lz_complexity
    avalanche_activity = min(1.0, dynamic.avalanche_mean_size / max(1.0, float(dynamic.samples)))

    profile = ExperienceFieldProfile(
        prediction_error=sensory.prediction_error,
        sensory_coherence=sensory.coherence,
        valence=sensory.valence,
        self_relevance=sensory.self_relevance,
        dynamic_persistence=abs(dynamic.lag1_autocorrelation),
        dynamic_synchrony=dynamic.pairwise_correlation,
        dynamic_metastability=dynamic.metastability,
        dynamic_complexity=dynamic.lz_complexity,
        avalanche_activity=round(avalanche_activity, 6),
        field_coherence=round(max(0.0, min(1.0, field_coherence)), 6),
        dynamic_repertoire=round(max(0.0, min(1.0, dynamic_repertoire)), 6),
    )
    return profile, sensory, dynamic


def profile_distance(previous: ExperienceFieldProfile, current: ExperienceFieldProfile) -> float:
    left = previous.to_dict()
    right = current.to_dict()
    values = [right[key] - left[key] for key in sorted(left)]
    return round(min(1.0, sqrt(sum(delta * delta for delta in values) / max(1, len(values)))), 6)


def sensory_counterfactual_action_delta(
    external_utility: float,
    actual_observation: Mapping[str, float],
    expected: Mapping[str, float],
    *,
    scales: Mapping[str, float] | None = None,
    affective_weights: Mapping[str, float] | None = None,
    self_relevance_weights: Mapping[str, float] | None = None,
    affect_weight: float = 1.0,
) -> float:
    actual_score, _ = score_action_with_affect(
        external_utility,
        actual_observation,
        expected,
        scales=scales,
        affective_weights=affective_weights,
        self_relevance_weights=self_relevance_weights,
        affect_weight=affect_weight,
    )
    neutral_score, _ = score_action_with_affect(
        external_utility,
        expected,
        expected,
        scales=scales,
        affective_weights=affective_weights,
        self_relevance_weights=self_relevance_weights,
        affect_weight=affect_weight,
    )
    return round(actual_score - neutral_score, 6)
