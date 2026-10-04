"""Deterministic host-loop causal benchmark.

This validates the host-boundary harness before external LLM integration.
It tests whether an authoritative host consequence can re-enter the runtime
and change the next trajectory through a persistent self-model update.

This is a mechanism test, not evidence of phenomenal consciousness.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousHostLoop, ConsciousRuntime


CANDIDATES = [
    {
        "id": "stabilize",
        "signals": {"goal_fit": 1.0},
    },
    {
        "id": "explore",
        "signals": {"goal_fit": 0.9},
    },
]


def _model_factory(*, reentry_enabled: bool):
    calls = {"count": 0}

    def model(_: str) -> dict[str, Any]:
        calls["count"] += 1
        if calls["count"] == 1:
            return {
                "candidate_futures": [dict(item) for item in CANDIDATES],
                "self_model": {
                    "trajectory_weights": {"goal_fit": 1.0},
                },
            }

        if not reentry_enabled:
            return {
                "candidate_futures": [dict(item) for item in CANDIDATES],
            }

        # The model is allowed to interpret the authoritative consequence.
        # The runtime still owns persistence and subsequent selection.
        return {
            "candidate_futures": [dict(item) for item in CANDIDATES],
            "self_model": {
                "trajectory_weights": {"goal_fit": -1.0},
            },
            "self_evaluation": {
                "consequence_effect": "the observed result changed trajectory preference"
            },
        }

    return model


def _run_condition(root: Path, *, reentry_enabled: bool) -> dict[str, Any]:
    runtime = ConsciousRuntime(
        f"host-loop-{'reentry' if reentry_enabled else 'control'}",
        state_path=root / f"{'reentry' if reentry_enabled else 'control'}.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    loop = ConsciousHostLoop(
        runtime,
        model=_model_factory(reentry_enabled=reentry_enabled),
        execute_action=lambda trajectory, _snapshot: {
            "status": "success",
            "self_state": {"focus": 0.2},
            "trajectory_executed": str(trajectory["id"]),
        },
    )

    result = loop.step("Choose the next trajectory.")
    selected = result.get("selected_trajectory") or {}
    next_selected = result.get("next_trajectory") or {}

    return {
        "condition": "reentry" if reentry_enabled else "control",
        "selected": str(selected.get("id", "")),
        "next_selected": str(next_selected.get("id", "")),
        "action_executed": bool(result["action_executed"]),
        "consequence": dict(result["consequence"] or {}),
        "action_history_length": len(runtime.state.action_history),
        "revision": runtime.state.revision,
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        control = _run_condition(root, reentry_enabled=False)
        reentry = _run_condition(root, reentry_enabled=True)

        output = {
            "conditions": [control, reentry],
            "metrics": {
                "same_initial_selection": control["selected"] == reentry["selected"],
                "reentry_changes_next_selection": (
                    control["next_selected"] != reentry["next_selected"]
                ),
                "control_preserves_initial_preference": (
                    control["next_selected"] == control["selected"]
                ),
                "reentry_switches_trajectory": (
                    reentry["selected"] != reentry["next_selected"]
                ),
                "authoritative_outcome_present": (
                    reentry["consequence"].get("status") == "success"
                ),
            },
        }

        assert control["selected"] == "stabilize"
        assert control["next_selected"] == "stabilize"
        assert reentry["selected"] == "stabilize"
        assert reentry["next_selected"] == "explore"
        assert output["metrics"]["reentry_changes_next_selection"] is True
        assert output["metrics"]["authoritative_outcome_present"] is True
        assert control["action_history_length"] == 1
        assert reentry["action_history_length"] == 1

        print(json.dumps(output, indent=2, sort_keys=True))
        print("EXTERNAL HOST BEHAVIORAL HARNESS v1: PASS")
        return output


if __name__ == "__main__":
    run()
