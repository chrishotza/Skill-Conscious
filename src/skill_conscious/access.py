from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from math import log


DEFAULT_ACCESS_CAPACITY = 32

# Each entry: base salience, self-relevance, persistence, policy priority, domain.
_ACCESS_SPECS: dict[str, tuple[float, float, float, float, str]] = {
    "pre_reflective_state": (1.00, 1.00, 1.00, 1.00, "self"),
    "interoceptive_state": (0.98, 0.95, 1.00, 1.00, "self"),
    "self_state": (0.95, 0.90, 1.00, 1.00, "self"),
    "self_model": (0.92, 0.85, 1.00, 0.95, "self"),
    "affective_state": (0.90, 0.90, 1.00, 0.95, "self"),
    "intention": (0.86, 0.85, 0.95, 0.95, "self"),
    "temporal_state": (0.78, 0.75, 1.00, 0.90, "self"),
    "latent_patterns": (0.74, 0.78, 1.00, 0.90, "self"),
    "valuation": (0.72, 0.80, 1.00, 0.90, "self"),
    "salience": (0.70, 0.72, 1.00, 0.90, "self"),
    "attention": (0.68, 0.70, 1.00, 0.88, "self"),
    "workspace": (0.66, 0.65, 1.00, 0.85, "self"),
    "selected_trajectory": (0.64, 0.80, 1.00, 0.85, "self"),
    "memories": (0.60, 0.60, 1.00, 0.80, "self"),
    "perspectives": (0.56, 0.65, 1.00, 0.78, "self"),
    "relation_topology": (0.54, 0.62, 1.00, 0.78, "self"),
    "attractor": (0.50, 0.58, 1.00, 0.75, "self"),
    "regime": (0.46, 0.50, 1.00, 0.72, "self"),
    "world_now": (0.90, 0.30, 0.50, 1.00, "world"),
}

_ACCESS_SIGNAL_KEYS: dict[str, tuple[str, ...]] = {
    "goal_fit": ("intention",),
    "self_alignment": ("self_state", "self_model"),
    "continuity": ("temporal_state", "memories"),
    "learning": ("latent_patterns", "memories"),
    "risk": ("self_model", "workspace"),
    "uncertainty": ("self_model",),
    "coherence": ("self_model", "relation_topology"),
    "topology_integrity": ("relation_topology",),
    "salience": ("salience", "attention"),
    "self_dissonance": ("self_model", "self_state"),
    "latent_pattern": ("latent_patterns",),
    "dissonance_resolution": ("self_model", "self_state"),
    "homeostatic_fit": ("interoceptive_state",),
    "self_relevance": ("pre_reflective_state",),
}


@dataclass(frozen=True)
class ConsciousAccessState:
    """Runtime-owned bounded access state, not a consciousness score."""

    capacity: int
    candidate_count: int
    selected_keys: list[str]
    omitted_keys: list[str]
    access_scores: dict[str, float]
    compression_load: float
    self_access_fraction: float
    world_access_fraction: float
    access_entropy: float
    revision: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))


def _global_salience(state: dict[str, object]) -> float:
    raw = state.get("salience")
    if isinstance(raw, dict):
        values = [
            _clamp(float(value))
            for value in raw.values()
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        ]
        if values:
            return sum(values) / len(values)
    attention = state.get("attention")
    return 0.75 if isinstance(attention, list) and attention else 0.5


def _pre_reflective_pressure(state: dict[str, object]) -> float:
    raw = state.get("pre_reflective_state")
    if not isinstance(raw, dict):
        return 0.0
    value = raw.get("self_relevance", 0.0)
    return _clamp(
        float(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool)
        else 0.0
    )


def _normalized_entropy(scores: list[float]) -> float:
    positive = [max(0.0, float(score)) for score in scores]
    total = sum(positive)
    if len(positive) <= 1 or total <= 0.0:
        return 0.0
    probabilities = [score / total for score in positive]
    entropy = -sum(
        p * log(p)
        for p in probabilities
        if p > 0.0
    )
    return round(_clamp(entropy / log(len(probabilities))), 6)


def _present_values(
    state: dict[str, object],
    *,
    external_input: str = "",
) -> dict[str, object]:
    return {
        "world_now": str(external_input),
        "self_state": deepcopy(state.get("self_state", {})),
        "self_model": deepcopy(state.get("self_model", {})),
        "workspace": deepcopy(state.get("workspace", {})),
        "intention": str(state.get("intention", "")),
        "memories": deepcopy(state.get("memories", [])),
        "attention": deepcopy(state.get("attention", [])),
        "salience": deepcopy(state.get("salience", {})),
        "interoceptive_state": deepcopy(state.get("interoceptive_state", {})),
        "affective_state": deepcopy(state.get("affective_state", {})),
        "temporal_state": deepcopy(state.get("temporal_state", {})),
        "perspectives": deepcopy(state.get("perspectives", {})),
        "valuation": deepcopy(state.get("valuation", {})),
        "relation_topology": deepcopy(state.get("relation_topology", {})),
        "attractor": deepcopy(state.get("attractor")),
        "regime": str(state.get("regime", "baseline")),
        "latent_patterns": deepcopy(state.get("latent_patterns", {})),
        "selected_trajectory": deepcopy(state.get("selected_trajectory")),
        "pre_reflective_state": deepcopy(state.get("pre_reflective_state", {})),
    }


def build_access_state(
    state: dict[str, object],
    *,
    external_input: str = "",
    capacity: int | None = None,
) -> ConsciousAccessState:
    """Select a bounded present from persistent runtime state."""

    configured_capacity = capacity
    if configured_capacity is None:
        raw_capacity = state.get("access_state")
        if isinstance(raw_capacity, dict):
            configured_capacity = raw_capacity.get("capacity")
    if not isinstance(configured_capacity, int) or isinstance(configured_capacity, bool):
        configured_capacity = DEFAULT_ACCESS_CAPACITY
    configured_capacity = max(1, int(configured_capacity))

    global_salience = _global_salience(state)
    self_pressure = _pre_reflective_pressure(state)
    values = _present_values(state, external_input=external_input)

    scored: list[tuple[str, float, str]] = []
    for key, (
        base_salience,
        self_relevance,
        persistence,
        policy_priority,
        domain,
    ) in _ACCESS_SPECS.items():
        # Salience remains state-dependent; self-relevance gets a small boost
        # from the current pre-reflective condition without becoming a scalar
        # consciousness measure.
        salience_i = _clamp(
            base_salience * (0.5 + 0.5 * global_salience)
            + (0.05 * self_pressure if domain == "self" else 0.0)
        )
        relevance_i = _clamp(self_relevance + (0.05 * self_pressure))
        score = (
            salience_i
            * relevance_i
            * _clamp(persistence)
            * _clamp(policy_priority)
        )
        scored.append((key, round(score, 6), domain))

    scored.sort(key=lambda item: (-item[1], item[0]))
    selected = [key for key, _, _ in scored[:configured_capacity]]
    selected_set = set(selected)
    omitted = [key for key, _, _ in scored if key not in selected_set]

    access_scores = {key: score for key, score, _ in scored}
    selected_domains = [domain for key, _, domain in scored if key in selected_set]
    selected_count = max(1, len(selected_domains))
    self_access = sum(domain == "self" for domain in selected_domains) / selected_count
    world_access = sum(domain == "world" for domain in selected_domains) / selected_count

    return ConsciousAccessState(
        capacity=configured_capacity,
        candidate_count=len(scored),
        selected_keys=selected,
        omitted_keys=omitted,
        access_scores=access_scores,
        compression_load=round(
            _clamp(1.0 - (min(configured_capacity, len(scored)) / max(1, len(scored)))),
            6,
        ),
        self_access_fraction=round(self_access, 6),
        world_access_fraction=round(world_access, 6),
        access_entropy=_normalized_entropy([score for _, score, _ in scored]),
        revision=int(state.get("revision", 0))
        if isinstance(state.get("revision", 0), int)
        and not isinstance(state.get("revision", 0), bool)
        else 0,
    )


def build_limited_present(
    state: dict[str, object],
    access_state: ConsciousAccessState | dict[str, object],
    *,
    external_input: str = "",
) -> dict[str, object]:
    """Return only the state currently available through the access window."""

    access = (
        access_state
        if isinstance(access_state, ConsciousAccessState)
        else ConsciousAccessState(
            capacity=int(access_state.get("capacity", DEFAULT_ACCESS_CAPACITY)),
            candidate_count=int(access_state.get("candidate_count", 0)),
            selected_keys=[str(key) for key in access_state.get("selected_keys", [])],
            omitted_keys=[str(key) for key in access_state.get("omitted_keys", [])],
            access_scores={
                str(key): float(value)
                for key, value in dict(access_state.get("access_scores", {})).items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            },
            compression_load=float(access_state.get("compression_load", 0.0)),
            self_access_fraction=float(access_state.get("self_access_fraction", 0.0)),
            world_access_fraction=float(access_state.get("world_access_fraction", 0.0)),
            access_entropy=float(access_state.get("access_entropy", 0.0)),
            revision=int(access_state.get("revision", 0)),
        )
    )
    values = _present_values(state, external_input=external_input)
    return {
        key: values[key]
        for key in access.selected_keys
        if key in values
    }


def signal_access_factor(
    candidate: dict[str, object],
    access_state: ConsciousAccessState | dict[str, object],
) -> tuple[float, dict[str, bool]]:
    """Return the causal availability of a trajectory's required present."""

    selected = (
        access_state.selected_keys
        if isinstance(access_state, ConsciousAccessState)
        else [str(key) for key in access_state.get("selected_keys", [])]
    )
    selected_set = set(selected)

    raw_required = candidate.get("access_keys")
    if raw_required is None:
        return 1.0, {}

    if isinstance(raw_required, str):
        required = [raw_required]
    elif isinstance(raw_required, (list, tuple, set)):
        required = [str(key) for key in raw_required if str(key).strip()]
    else:
        raise ValueError("trajectory.access_keys must be a string or sequence")

    if not required:
        return 1.0, {}

    availability = {key: key in selected_set for key in required}
    factor = 1.0 if all(availability.values()) else 0.0
    return factor, availability
