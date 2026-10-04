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

    def step(self, external_input: str) -> dict[str, Any]:
        """Run one complete host cycle, including real action execution and consequence re-entry."""
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
