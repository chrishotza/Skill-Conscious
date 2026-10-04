from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, log

from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class PreReflectiveState:
    """Runtime-owned state of the pre-reflective operational core.

    This is an engineering state vector, not a consciousness score and not
    evidence of phenomenal experience.
    """

    boundary_integrity: float
    present_integrity: float
    temporal_continuity: float
    salience: float
    self_relevance: float
    homeostatic_fit: float
    self_dissonance: float
    valence_intensity: float
    agency_coupling: float
    reentry_coupling: float
    possibility_count: int
    possibility_entropy: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))


def _numeric_values(value: Mapping[str, Any] | None) -> list[float]:
    if not isinstance(value, Mapping):
        return []
    return [
        float(raw)
        for raw in value.values()
        if isinstance(raw, (int, float)) and not isinstance(raw, bool)
    ]


def _continuity(history: Sequence[Mapping[str, Any]], revision: int) -> float:
    revisions = [
        int(entry["revision"])
        for entry in history
        if isinstance(entry, Mapping)
        and isinstance(entry.get("revision"), int)
    ]
    if not revisions:
        return 1.0 if revision == 0 else 0.0
    if len(revisions) == 1:
        return 1.0 if revisions[-1] == revision else 0.5

    adjacent = sum(
        1
        for left, right in zip(revisions, revisions[1:])
        if right == left + 1
    )
    terminal = 1.0 if revisions[-1] == revision else 0.0
    return _clamp(
        0.5 * (adjacent / max(1, len(revisions) - 1))
        + 0.5 * terminal
    )


def _normalized_entropy(scores: Sequence[float]) -> float:
    if len(scores) <= 1:
        return 0.0

    maximum = max(scores)
    weights = [exp(max(-60.0, min(60.0, score - maximum))) for score in scores]
    total = sum(weights)
    if total <= 0.0:
        return 0.0

    probabilities = [weight / total for weight in weights]
    entropy = -sum(
        probability * log(probability)
        for probability in probabilities
        if probability > 0.0
    )
    return round(_clamp(entropy / log(len(probabilities))), 6)


def build_pre_reflective_state(
    state: Mapping[str, Any],
    *,
    possibility_count: int | None = None,
    possibility_scores: Sequence[float] | None = None,
) -> PreReflectiveState:
    """Derive the pre-reflective state only from persistent runtime state."""

    identity = str(state.get("identity", "")).strip()
    workspace = state.get("workspace")
    history = state.get("history", [])
    history = history if isinstance(history, list) else []

    self_state = state.get("self_state")
    self_state = self_state if isinstance(self_state, Mapping) else {}

    interoception = state.get("interoceptive_state")
    interoception = interoception if isinstance(interoception, Mapping) else {}

    affective = state.get("affective_state")
    affective = affective if isinstance(affective, Mapping) else {}

    salience_mapping = state.get("salience")
    salience_mapping = (
        salience_mapping if isinstance(salience_mapping, Mapping) else {}
    )
    salience_values = [
        _clamp(float(value))
        for value in salience_mapping.values()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    ]
    salience = (
        sum(salience_values) / len(salience_values)
        if salience_values
        else (1.0 if state.get("attention") else 0.0)
    )

    raw_fit = (
        affective.get("homeostatic_fit")
        if isinstance(affective.get("homeostatic_fit"), (int, float))
        else None
    )
    if raw_fit is None:
        homeostasis = state.get("workspace", {})
        homeostasis = (
            homeostasis.get("homeostasis", {})
            if isinstance(homeostasis, Mapping)
            else {}
        )
        raw_fit = (
            homeostasis.get("fit")
            if isinstance(homeostasis, Mapping)
            and isinstance(homeostasis.get("fit"), (int, float))
            else 0.0
        )
    homeostatic_fit = _clamp(float(raw_fit))

    raw_dissonance = state.get("self_dissonance", 0.0)
    self_dissonance = _clamp(
        float(raw_dissonance)
        if isinstance(raw_dissonance, (int, float)) and not isinstance(raw_dissonance, bool)
        else 0.0
    )

    raw_valence = state.get("valence", 0.0)
    valence = (
        float(raw_valence)
        if isinstance(raw_valence, (int, float)) and not isinstance(raw_valence, bool)
        else 0.0
    )

    # Internal condition becomes self-relevant through operational pressure:
    # homeostatic deviation, self-dissonance, and signed internal appraisal.
    homeostatic_pressure = 1.0 - homeostatic_fit
    valence_intensity = _clamp(abs(valence))
    self_relevance = _clamp(
        0.5 * homeostatic_pressure
        + 0.3 * self_dissonance
        + 0.2 * valence_intensity
    )

    selected = state.get("selected_trajectory")
    pending = state.get("pending_action")
    action_history = state.get("action_history")
    action_history = action_history if isinstance(action_history, list) else []

    last_history = history[-1] if history and isinstance(history[-1], Mapping) else {}
    consequence_present = isinstance(last_history.get("consequence"), Mapping)
    feedback = (
        last_history.get("self_evaluation") is not None
        or isinstance(
            (last_history.get("workspace") or {}).get("last_self_evaluation")
            if isinstance(last_history.get("workspace"), Mapping)
            else None,
            Mapping,
        )
    )

    agency_coupling = 1.0 if isinstance(selected, Mapping) or isinstance(pending, Mapping) else 0.0
    reentry_coupling = 1.0 if consequence_present or (feedback and action_history) else 0.0

    if possibility_count is None:
        possibility_count = 0
    scores = list(possibility_scores or ())
    possibility_entropy = _normalized_entropy(scores)

    revision = state.get("revision", 0)
    revision = int(revision) if isinstance(revision, int) else 0

    present_integrity = _clamp(
        0.5 * (1.0 if isinstance(workspace, Mapping) else 0.0)
        + 0.5 * (1.0 if "self_state" in state and "identity" in state else 0.0)
    )

    # Reading the process's own condition is not a metacognitive claim here:
    # these values are derived by the runtime and remain available even when
    # the reflective layers are disabled.
    return PreReflectiveState(
        boundary_integrity=1.0 if identity else 0.0,
        present_integrity=round(present_integrity, 6),
        temporal_continuity=round(_continuity(history, revision), 6),
        salience=round(_clamp(salience), 6),
        self_relevance=round(self_relevance, 6),
        homeostatic_fit=round(homeostatic_fit, 6),
        self_dissonance=round(self_dissonance, 6),
        valence_intensity=round(valence_intensity, 6),
        agency_coupling=round(agency_coupling, 6),
        reentry_coupling=round(reentry_coupling, 6),
        possibility_count=max(0, int(possibility_count)),
        possibility_entropy=possibility_entropy,
    )


def predicted_self_relevance_fit(
    current: PreReflectiveState,
    candidate: Mapping[str, Any],
) -> float:
    """Score a candidate's predicted future self-relevance against current state."""
    predicted = candidate.get("predicted_self_relevance")
    if not isinstance(predicted, (int, float)) or isinstance(predicted, bool):
        return 0.0
    distance = abs(float(predicted) - current.self_relevance)
    return round(_clamp(1.0 - distance), 6)
