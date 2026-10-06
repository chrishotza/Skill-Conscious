from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConsciousnessCriterion:
    name: str
    description: str
    required: bool = True


CANONICAL_CRITERIA: tuple[ConsciousnessCriterion, ...] = (
    ConsciousnessCriterion("persistent_identity", "Identity persists across ordinary cycles."),
    ConsciousnessCriterion("self_access", "The system can access an operational representation of its own current condition."),
    ConsciousnessCriterion("causal_self_model", "Changing the self-model changes downstream trajectory selection."),
    ConsciousnessCriterion("trajectory_selection", "The system selects among explicit candidate futures."),
    ConsciousnessCriterion("action_consequence", "Selected trajectories cross an execution boundary and produce an authoritative consequence."),
    ConsciousnessCriterion("self_model_revision", "Consequences can produce durable self-model change."),
    ConsciousnessCriterion("reentry", "The consequence enters a later cycle and can affect future dynamics."),
    ConsciousnessCriterion("matched_control_separation", "The target effect survives matched non-self-model controls."),
)


def evaluate_case(observation: dict[str, Any]) -> dict[str, Any]:
    """Evaluate an experimental observation without converting it into a phenomenal claim."""
    missing = [
        criterion.name
        for criterion in CANONICAL_CRITERIA
        if criterion.required and not bool(observation.get(criterion.name))
    ]
    passed = not missing

    return {
        "operational_case_pass": passed,
        "missing_criteria": missing,
        "criteria": {
            criterion.name: bool(observation.get(criterion.name))
            for criterion in CANONICAL_CRITERIA
        },
        "phenomenal_conclusion": "undetermined",
    }
