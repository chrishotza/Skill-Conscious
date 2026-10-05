from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class EmbodimentState:
    """Runtime-owned operational embodiment/ownership state.

    This is an engineering boundary model, not a claim of biological
    embodiment or phenomenal ownership.
    """

    boundary_integrity: float
    interoceptive_coupling: float
    resource_fit: float
    ownership_coupling: float
    action_cost: float
    revision: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _clamp(value: Any, default: float = 0.0) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return float(default)
    return max(0.0, min(1.0, float(value)))


def _numeric(mapping: Mapping[str, Any] | None) -> dict[str, float]:
    if not isinstance(mapping, Mapping):
        return {}
    return {
        str(key): float(value)
        for key, value in mapping.items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    }


def _resource_fit(
    state: Mapping[str, Any],
) -> float:
    model = state.get("self_model", {})
    model = model if isinstance(model, Mapping) else {}
    budget = _numeric(model.get("resource_budget"))
    current = _numeric(state.get("interoceptive_state"))
    if not budget or not current:
        return 1.0

    fits = []
    for key, target in budget.items():
        if key not in current:
            continue
        scale = max(1.0, abs(target))
        fits.append(max(0.0, min(1.0, 1.0 - abs(current[key] - target) / scale)))
    return sum(fits) / len(fits) if fits else 1.0


def _last_action_cost(state: Mapping[str, Any]) -> float:
    history = state.get("action_history", [])
    if not isinstance(history, list) or not history:
        return 0.0
    last = history[-1]
    if not isinstance(last, Mapping):
        return 0.0
    outcome = last.get("outcome", {})
    if not isinstance(outcome, Mapping):
        return 0.0
    return _clamp(outcome.get("resource_cost", 0.0))


def build_embodiment_state(
    state: Mapping[str, Any],
) -> EmbodimentState:
    identity = str(state.get("identity", "")).strip()
    interoception = state.get("interoceptive_state")
    interoceptive_coupling = (
        1.0 if isinstance(interoception, Mapping) and bool(interoception) else 0.0
    )

    pending = state.get("pending_action")
    action_history = state.get("action_history", [])
    has_history = isinstance(action_history, list) and bool(action_history)
    has_pending = isinstance(pending, Mapping)
    ownership_coupling = 1.0 if (has_pending or has_history) else (
        0.5 if state.get("selected_trajectory") is not None else 0.0
    )

    return EmbodimentState(
        boundary_integrity=1.0 if identity else 0.0,
        interoceptive_coupling=round(interoceptive_coupling, 6),
        resource_fit=round(_resource_fit(state), 6),
        ownership_coupling=round(_clamp(ownership_coupling), 6),
        action_cost=round(_last_action_cost(state), 6),
        revision=int(state.get("revision", 0))
        if isinstance(state.get("revision", 0), int)
        and not isinstance(state.get("revision", 0), bool)
        else 0,
    )


def predicted_resource_fit(
    state: EmbodimentState,
    candidate: Mapping[str, Any],
    *,
    current: Mapping[str, Any] | None = None,
) -> float:
    predicted = candidate.get("predicted_resource_load")
    if not isinstance(predicted, Mapping):
        return state.resource_fit

    predicted_values = _numeric(predicted)
    current_values = _numeric(current)
    if not predicted_values or not current_values:
        return state.resource_fit

    errors = []
    for key, value in predicted_values.items():
        if key not in current_values:
            continue
        scale = max(1.0, abs(current_values[key]))
        errors.append(max(0.0, min(1.0, 1.0 - abs(value - current_values[key]) / scale)))

    return round(sum(errors) / len(errors), 6) if errors else state.resource_fit
