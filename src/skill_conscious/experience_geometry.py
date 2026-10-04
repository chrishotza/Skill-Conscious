from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt
from typing import Any, Mapping


FEATURE_ORDER = (
    "valence",
    "coherence",
    "self_dissonance",
    "salience",
    "self_relevance",
    "present_integrity",
    "temporal_continuity",
    "possibility_entropy",
    "reentry_coupling",
    "prediction_error",
    "metacognitive_uncertainty",
    "self_observation_error",
    "access_entropy",
    "access_compression",
    "self_access_fraction",
    "world_access_fraction",
    "field_coherence",
    "dynamic_synchrony",
    "dynamic_metastability",
    "dynamic_complexity",
    "dynamic_repertoire",
)


def _clamp01(value: Any, default: float = 0.0) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return float(default)
    return max(0.0, min(1.0, float(value)))


def _signed01(value: Any, default: float = 0.0) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return float(default)
    return max(0.0, min(1.0, (float(value) + 1.0) / 2.0))


def _numeric(mapping: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = mapping.get(key)
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else float(default)


@dataclass(frozen=True)
class ExperienceState:
    """A normalized point in operational experience state-space.

    This is a geometry for comparing runtime states and their transitions.
    It is not a consciousness meter and does not establish subjective
    experience.
    """

    features: dict[str, float]

    def __post_init__(self) -> None:
        normalized = {
            str(key): round(_clamp01(value), 6)
            for key, value in self.features.items()
            if str(key) in FEATURE_ORDER
        }
        normalized.update(
            {
                key: 0.0
                for key in FEATURE_ORDER
                if key not in normalized
            }
        )
        object.__setattr__(
            self,
            "features",
            {key: normalized[key] for key in FEATURE_ORDER},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_experience_state(snapshot: Mapping[str, Any]) -> ExperienceState:
    """Project a persistent runtime snapshot into a bounded multidimensional state."""
    self_model = snapshot.get("self_model", {})
    if not isinstance(self_model, Mapping):
        self_model = {}

    pre_reflective = snapshot.get("pre_reflective_state", {})
    if not isinstance(pre_reflective, Mapping):
        pre_reflective = {}

    experience_field = self_model.get("experience_field_state", {})
    if not isinstance(experience_field, Mapping):
        experience_field = {}

    access_state = snapshot.get("access_state", {})
    if not isinstance(access_state, Mapping):
        access_state = {}

    salience = snapshot.get("salience", {})
    salience_value = 0.0
    if isinstance(salience, Mapping):
        numeric = [
            _clamp01(value)
            for value in salience.values()
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        ]
        if numeric:
            salience_value = sum(numeric) / len(numeric)

    expected_accuracy = _clamp01(
        self_model.get("metacognitive_prediction_expected_accuracy", 0.5),
        default=0.5,
    )

    raw_self_relevance = pre_reflective.get("self_relevance")
    if not isinstance(raw_self_relevance, (int, float)) or isinstance(raw_self_relevance, bool):
        raw_self_relevance = experience_field.get("self_relevance", 0.0)

    features = {
        "valence": _signed01(snapshot.get("valence", 0.0)),
        "coherence": _clamp01(snapshot.get("coherence", 1.0), default=1.0),
        "self_dissonance": _clamp01(snapshot.get("self_dissonance", 0.0)),
        "salience": salience_value,
        "self_relevance": _clamp01(raw_self_relevance),
        "present_integrity": _clamp01(pre_reflective.get("present_integrity", 0.0)),
        "temporal_continuity": _clamp01(pre_reflective.get("temporal_continuity", 0.0)),
        "possibility_entropy": _clamp01(pre_reflective.get("possibility_entropy", 0.0)),
        "reentry_coupling": _clamp01(pre_reflective.get("reentry_coupling", 0.0)),
        "prediction_error": _clamp01(
            self_model.get("metacognitive_prediction_error", 0.0)
        ),
        "metacognitive_uncertainty": round(1.0 - expected_accuracy, 6),
        "self_observation_error": _clamp01(
            self_model.get("self_observation_error", 0.0)
        ),
        "access_entropy": _clamp01(access_state.get("access_entropy", 0.0)),
        "access_compression": _clamp01(
            access_state.get("compression_load", 0.0)
        ),
        "self_access_fraction": _clamp01(
            access_state.get("self_access_fraction", 0.0)
        ),
        "world_access_fraction": _clamp01(
            access_state.get("world_access_fraction", 0.0)
        ),
        "field_coherence": _clamp01(
            _numeric(experience_field, "field_coherence")
        ),
        "dynamic_synchrony": _clamp01(
            _numeric(experience_field, "dynamic_synchrony")
        ),
        "dynamic_metastability": _clamp01(
            _numeric(experience_field, "dynamic_metastability")
        ),
        "dynamic_complexity": _clamp01(
            _numeric(experience_field, "dynamic_complexity")
        ),
        "dynamic_repertoire": _clamp01(
            _numeric(experience_field, "dynamic_repertoire")
        ),
    }
    return ExperienceState(features=features)


def experience_distance(
    previous: ExperienceState,
    current: ExperienceState,
) -> float:
    """Return a bounded root-mean-square distance between two states."""
    deltas = [
        current.features[key] - previous.features[key]
        for key in FEATURE_ORDER
    ]
    return round(
        min(1.0, sqrt(sum(delta * delta for delta in deltas) / len(deltas))),
        6,
    )


def changed_dimensions(
    previous: ExperienceState,
    current: ExperienceState,
    *,
    threshold: float = 0.05,
) -> dict[str, float]:
    """Return dimensions whose normalized value changed by at least threshold."""
    threshold = max(0.0, float(threshold))
    result: dict[str, float] = {}
    for key in FEATURE_ORDER:
        delta = current.features[key] - previous.features[key]
        if abs(delta) >= threshold:
            result[key] = round(delta, 6)
    return result


def transition_record(
    previous: ExperienceState,
    current: ExperienceState,
    *,
    revision: int,
    threshold: float = 0.05,
) -> dict[str, Any]:
    """Represent one measurable transition in operational experience geometry."""
    return {
        "revision": int(revision),
        "distance": experience_distance(previous, current),
        "changed_dimensions": changed_dimensions(
            previous,
            current,
            threshold=threshold,
        ),
        "previous": previous.to_dict(),
        "current": current.to_dict(),
    }
