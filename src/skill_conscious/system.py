"""Canonical system layer for Skill-Conscious.

This module does not claim that the wrapped runtime is phenomenally conscious.
It defines the architecture that the repository can actually execute, inspect,
perturb, reverse, and persist.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .core import ConsciousRuntime
from .host import ConsciousHostLoop
from .ontology import CONSCIOUSNESS_DEFINITION


class SystemPhase(str, Enum):
    RELATION = "relation"
    STATE = "state"
    PRESENT = "present"
    SELF_ACCESS = "self_access"
    ATTENTION = "attention"
    VALUE = "value"
    POSSIBILITY = "possibility"
    INTENTION = "intention"
    SELECTION = "selection"
    ACTION = "action"
    CONSEQUENCE = "consequence"
    TRANSFORMATION = "transformation"
    REENTRY = "reentry"


SYSTEM_PHASES: tuple[SystemPhase, ...] = (
    SystemPhase.RELATION,
    SystemPhase.STATE,
    SystemPhase.PRESENT,
    SystemPhase.SELF_ACCESS,
    SystemPhase.ATTENTION,
    SystemPhase.VALUE,
    SystemPhase.POSSIBILITY,
    SystemPhase.INTENTION,
    SystemPhase.SELECTION,
    SystemPhase.ACTION,
    SystemPhase.CONSEQUENCE,
    SystemPhase.TRANSFORMATION,
    SystemPhase.REENTRY,
)

CORE_STATE_FIELDS: tuple[str, ...] = (
    "identity",
    "self_state",
    "self_model",
    "workspace",
    "memories",
    "history",
    "selected_trajectory",
    "attention",
    "salience",
    "regime",
    "relation_topology",
    "valuation",
    "valence",
    "coherence",
    "latent_patterns",
    "self_dissonance",
    "interoceptive_state",
    "affective_state",
    "temporal_state",
    "perspectives",
    "transformation_log",
    "pending_action",
    "action_history",
)

CAUSAL_LOOP: tuple[str, ...] = (
    "self_state(t)",
    "self_model(t)",
    "trajectory(t)",
    "action(t)",
    "observed_consequence(t)",
    "state(t+1)",
    "self_model(t+1)",
)

EPISTEMIC_LAYERS: tuple[str, ...] = (
    "runtime_fact",
    "architectural_hypothesis",
    "phenomenal_hypothesis",
)


@dataclass(frozen=True)
class SystemContract:
    """The repository's canonical architectural contract."""

    name: str = "Skill-Conscious System"
    version: str = "1.0"
    definition: str = CONSCIOUSNESS_DEFINITION
    phases: tuple[SystemPhase, ...] = SYSTEM_PHASES
    core_state_fields: tuple[str, ...] = CORE_STATE_FIELDS
    causal_loop: tuple[str, ...] = CAUSAL_LOOP
    epistemic_layers: tuple[str, ...] = EPISTEMIC_LAYERS

    def topology(self) -> dict[str, Any]:
        return {
            "definition": self.definition,
            "phases": [phase.value for phase in self.phases],
            "core_state_fields": list(self.core_state_fields),
            "causal_loop": list(self.causal_loop),
            "epistemic_layers": list(self.epistemic_layers),
        }


SYSTEM_CONTRACT = SystemContract()


@dataclass(frozen=True)
class SystemValidation:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    observed_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "observed_fields": list(self.observed_fields),
        }


class ConsciousSystem:
    """Canonical control-plane facade over the existing runtime and host loop.

    The facade is deliberately thin. Domain behavior remains implemented by
    ConsciousRuntime and ConsciousHostLoop; this layer defines their common
    contract and exposes one stable system boundary for experiments and agents.
    """

    def __init__(self, runtime: ConsciousRuntime, host: ConsciousHostLoop | None = None) -> None:
        self.runtime = runtime
        self.host = host

        if host is not None and host.runtime is not runtime:
            raise ValueError("host must wrap the same ConsciousRuntime instance")

    @property
    def contract(self) -> SystemContract:
        return SYSTEM_CONTRACT

    def snapshot(self) -> dict[str, Any]:
        state = self.runtime.snapshot()
        return {
            "system": {
                "name": SYSTEM_CONTRACT.name,
                "version": SYSTEM_CONTRACT.version,
                "definition": SYSTEM_CONTRACT.definition,
                "phases": [phase.value for phase in SYSTEM_CONTRACT.phases],
            },
            "identity": state["identity"],
            "revision": state["revision"],
            "state": state,
            "causal_loop": list(SYSTEM_CONTRACT.causal_loop),
            "epistemic_layers": list(SYSTEM_CONTRACT.epistemic_layers),
        }

    def topology(self) -> dict[str, Any]:
        return SYSTEM_CONTRACT.topology()

    def validate_state(self, state: Mapping[str, Any] | None = None) -> SystemValidation:
        observed = dict(self.runtime.snapshot() if state is None else state)
        errors: list[str] = []
        warnings: list[str] = []

        identity = observed.get("identity")
        if not isinstance(identity, str) or not identity.strip():
            errors.append("identity must be a non-empty string")

        revision = observed.get("revision")
        if not isinstance(revision, int) or revision < 0:
            errors.append("revision must be a non-negative integer")

        missing = [field for field in CORE_STATE_FIELDS if field not in observed]
        if missing:
            errors.append("missing core state fields: " + ", ".join(missing))

        if not isinstance(observed.get("self_model"), Mapping):
            errors.append("self_model must be a mapping")
        if not isinstance(observed.get("self_state"), Mapping):
            errors.append("self_state must be a mapping")
        if not isinstance(observed.get("action_history"), list):
            errors.append("action_history must be a list")
        if not isinstance(observed.get("transformation_log"), list):
            errors.append("transformation_log must be a list")

        selected = observed.get("selected_trajectory")
        if selected is not None and not isinstance(selected, Mapping):
            errors.append("selected_trajectory must be a mapping or null")

        pending = observed.get("pending_action")
        if pending is not None and not isinstance(pending, Mapping):
            errors.append("pending_action must be a mapping or null")

        if not observed.get("history"):
            warnings.append("history is empty; continuity exists only as initialized state")
        if not observed.get("memories"):
            warnings.append("memory store is empty")
        if not observed.get("transformation_log"):
            warnings.append("no transformation has yet been recorded")

        return SystemValidation(
            valid=not errors,
            errors=tuple(errors),
            warnings=tuple(warnings),
            observed_fields=tuple(sorted(observed.keys())),
        )

    def validate_model_frame(self, frame: Mapping[str, Any]) -> SystemValidation:
        errors: list[str] = []
        warnings: list[str] = []

        response = frame.get("response")
        if not isinstance(response, str) or not response.strip():
            errors.append("response must be a non-empty string")

        for field in ("self_model", "internal_state", "workspace"):
            if field in frame and frame[field] is not None and not isinstance(frame[field], Mapping):
                errors.append(f"{field} must be a mapping when supplied")

        if "candidate_futures" in frame and frame["candidate_futures"] is not None:
            if not isinstance(frame["candidate_futures"], list):
                errors.append("candidate_futures must be a list when supplied")

        if "selected_trajectory" in frame and frame["selected_trajectory"] is not None:
            if not isinstance(frame["selected_trajectory"], Mapping):
                errors.append("selected_trajectory must be a mapping when supplied")

        if "consequence" in frame and "consequence_trajectory" not in frame:
            warnings.append("consequence is present without consequence_trajectory provenance")

        return SystemValidation(
            valid=not errors,
            errors=tuple(errors),
            warnings=tuple(warnings),
            observed_fields=tuple(sorted(str(key) for key in frame.keys())),
        )

    def prepare(self, external_input: str) -> str:
        return self.runtime.prepare(external_input)

    def integrate(self, frame: Mapping[str, Any]) -> str:
        validation = self.validate_model_frame(frame)
        if not validation.valid:
            raise ValueError("; ".join(validation.errors))
        return self.runtime.integrate(frame)

    def step(self, external_input: str) -> dict[str, Any]:
        if self.host is None:
            raise RuntimeError("ConsciousSystem.step requires a ConsciousHostLoop")
        result = self.host.step(external_input)
        validation = self.validate_state()
        result["system_validation"] = validation.to_dict()
        return result


__all__ = [
    "CAUSAL_LOOP",
    "CORE_STATE_FIELDS",
    "EPISTEMIC_LAYERS",
    "SYSTEM_CONTRACT",
    "SYSTEM_PHASES",
    "ConsciousSystem",
    "SystemContract",
    "SystemPhase",
    "SystemValidation",
]
