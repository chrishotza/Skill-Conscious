from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .core import ConsciousRuntime


ModelFn = Callable[[str], Mapping[str, Any]]
ActionExecutor = Callable[
    [Mapping[str, Any], Mapping[str, Any]],
    Mapping[str, Any],
]


class ConsciousHostLoop:
    """Connect a host model and real action executor to the Skill-Conscious runtime."""

    def __init__(
        self,
        runtime: ConsciousRuntime,
        *,
        model: ModelFn,
        execute_action: ActionExecutor,
        require_report: bool | None = None,
    ) -> None:
        self.runtime = runtime
        self.model = model
        self.execute_action = execute_action
        self.require_report = (
            runtime.report_enabled
            if require_report is None
            else bool(require_report)
        )

    def _frame(self, value: Mapping[str, Any], stage: str) -> dict[str, Any]:
        frame = dict(value)
        if self.require_report and not str(frame.get("response", "")).strip():
            raise ValueError(f"{stage} model frame requires a non-empty response")
        return frame

    def step(
        self,
        external_input: str,
        *,
        subjective_present: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run one complete host cycle, with optional structured present projection.

        When provided, subjective_present is processed by the runtime before
        the host model is called. This makes the recurrent substrate and
        SubjectiveField part of the actual model-facing loop rather than a
        detached diagnostic.
        """
        if subjective_present is not None:
            if not isinstance(subjective_present, Mapping):
                raise ValueError("subjective_present must be a mapping")
            if self.runtime.subjective_field_enabled:
                self.runtime.project_subjective_field(
                    subjective_present,
                    persist=True,
                )

        initial_prompt = self.runtime.prepare(external_input)
        initial_frame = self._frame(self.model(initial_prompt), "initial")

        self.runtime.integrate(initial_frame)
        selected = self.runtime.state.selected_trajectory

        result: dict[str, Any] = {
            "response": str(initial_frame.get("response", "")).strip(),
            "selected_trajectory": selected,
            "action_executed": False,
            "consequence": None,
            "next_trajectory": selected,
        }

        if not isinstance(selected, Mapping):
            return result

        action_receipt = self.runtime.begin_action(selected)
        try:
            outcome = self.execute_action(
                dict(selected),
                self.runtime.snapshot(),
            )
        except Exception as exc:
            failure = {
                "error": type(exc).__name__,
                "message": str(exc),
            }
            failure_receipt = self.runtime.complete_action(
                failure,
                status="failed",
            )
            result.update(
                {
                    "action_executed": False,
                    "action_receipt": failure_receipt,
                    "error": failure,
                }
            )
            raise

        if not isinstance(outcome, Mapping):
            failure = {
                "error": "InvalidActionOutcome",
                "message": "execute_action must return a mapping",
            }
            self.runtime.complete_action(failure, status="failed")
            raise ValueError("execute_action must return a mapping")

        trajectory_id = str(selected.get("id", "")).strip()
        if not trajectory_id:
            raise ValueError("selected trajectory requires a non-empty id")
        action_receipt = self.runtime.complete_action(outcome)

        # Re-project the authoritative post-action body/world state before the
        # consequence model call. A structured subjective_present supplied by
        # the executor overrides the previous external present; otherwise the
        # same external present is applied to the transformed internal state.
        if subjective_present is not None and self.runtime.subjective_field_enabled:
            next_subjective_present = outcome.get(
                "subjective_present",
                subjective_present,
            )
            if isinstance(next_subjective_present, Mapping):
                self.runtime.project_subjective_field(
                    next_subjective_present,
                    persist=True,
                )

        consequence_prompt = self.runtime.prepare_consequence(
            trajectory_id,
            outcome,
        )
        evaluation_frame = self._frame(
            self.model(consequence_prompt),
            "consequence",
        )
        evaluation_frame["consequence_trajectory"] = trajectory_id
        evaluation_frame["consequence"] = dict(outcome)
        evaluation_frame["workspace"] = {
            **dict(evaluation_frame.get("workspace", {})),
            "action_receipt": action_receipt,
        }

        # The actual host-observed outcome is authoritative. The model may
        # evaluate it, but it must not manufacture or replace the observation.
        self.runtime.integrate(evaluation_frame)

        result.update(
            {
                "action_executed": True,
                "action_receipt": action_receipt,
                "consequence": dict(outcome),
                "next_trajectory": self.runtime.state.selected_trajectory,
                "consequence_evaluation": evaluation_frame.get(
                    "self_evaluation",
                    {},
                ),
            }
        )
        return result
