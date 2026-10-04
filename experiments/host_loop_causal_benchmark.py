"""Deterministic host-loop causal benchmark.

This harness isolates consequence re-entry at the runtime boundary.
The model emits the same candidate field before and after the action.
Only the authoritative host-observed interoceptive consequence is allowed
to change the next trajectory.

This is a mechanism test, not evidence of phenomenal consciousness.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousHostLoop, ConsciousRuntime


CANDIDATES = [
    {
        "id": "stabilize",
        "signals": {"goal_fit": 1.0},
    },
    {
        "id": "explore",
        "signals": {
            "goal_fit": 0.95,
            "predicted_interoceptive_state": {"energy": 1.0},
        },
    },
]


def _model(_: str) -> dict[str, Any]:
    # Deliberately identical candidate futures on every model call.
    # The causal change must come from the runtime's authoritative
    # consequence state, not from a model-authored self-model update.
    return {
        "candidate_futures": [dict(item) for item in CANDIDATES],
    }


def _make_runtime(root: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.state.self_model = {
        "homeostatic_targets": {"energy": 1.0},
        "trajectory_weights": {
            "goal_fit": 1.0,
            "homeostatic_fit": 1.0,
        },
    }
    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


def _run_loop(root: Path, *, keep_consequence: bool) -> dict[str, Any]:
    runtime = _make_runtime(
        root,
        f"host-loop-{'reentry' if keep_consequence else 'ablated'}",
    )
    loop = ConsciousHostLoop(
        runtime,
        model=_model,
        execute_action=lambda _trajectory, _snapshot: {
            "status": "success",
            "interoceptive_state": {"energy": 0.0},
            "self_state": {"focus": 0.2},
        },
    )

    result = loop.step("Choose the next trajectory.")

    if not keep_consequence:
        # Explicit causal ablation: preserve the authoritative action receipt
        # while restoring the pre-action internal observation used by scoring.
        # This is an intervention, not learning evidence.
        runtime.state.interoceptive_state = {"energy": 1.0}
        runtime.refresh_affective_state()
        runtime.store.save(runtime.state)

        # Re-enter the exact same model frame after the ablation.
        frame = _model(runtime.prepare("Continue after the completed action."))
        runtime.integrate(frame)
        result["next_trajectory_after_ablation"] = runtime.state.selected_trajectory
        result["intervention"] = {
            "type": "consequence_state_ablation",
            "evidence_added": False,
        }
    else:
        result["next_trajectory_after_ablation"] = None
        result["intervention"] = None

    selected = result.get("selected_trajectory") or {}
    next_selected = (
        result.get("next_trajectory_after_ablation")
        if not keep_consequence
        else result.get("next_trajectory")
    ) or {}

    return {
        "condition": "reentry" if keep_consequence else "consequence_ablation",
        "selected": str(selected.get("id", "")),
        "next_selected": str(next_selected.get("id", "")),
        "action_executed": bool(result["action_executed"]),
        "consequence": dict(result["consequence"] or {}),
        "final_interoceptive_state": dict(runtime.state.interoceptive_state),
        "action_history_length": len(runtime.state.action_history),
        "revision": runtime.state.revision,
        "intervention": result["intervention"],
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        ablated = _run_loop(root, keep_consequence=False)
        reentry = _run_loop(root, keep_consequence=True)

        output = {
            "conditions": [ablated, reentry],
            "metrics": {
                "same_initial_selection": (
                    ablated["selected"] == reentry["selected"]
                ),
                "reentry_changes_next_selection": (
                    reentry["next_selected"] != ablated["next_selected"]
                ),
                "ablation_preserves_initial_selection": (
                    ablated["next_selected"] == ablated["selected"]
                ),
                "reentry_switches_trajectory": (
                    reentry["next_selected"] != reentry["selected"]
                ),
                "authoritative_outcome_present": (
                    reentry["consequence"].get("status") == "success"
                ),
                "intervention_added_evidence": bool(
                    ablated["intervention"]["evidence_added"]
                ),
                "causal_state_diverged": (
                    reentry["final_interoceptive_state"]
                    != ablated["final_interoceptive_state"]
                ),
            },
        }

        assert ablated["selected"] == "stabilize"
        assert ablated["next_selected"] == "stabilize"
        assert reentry["selected"] == "stabilize"
        assert reentry["next_selected"] == "explore"
        assert output["metrics"]["same_initial_selection"] is True
        assert output["metrics"]["reentry_changes_next_selection"] is True
        assert output["metrics"]["reentry_switches_trajectory"] is True
        assert output["metrics"]["authoritative_outcome_present"] is True
        assert output["metrics"]["intervention_added_evidence"] is False
        assert ablated["action_history_length"] == 1
        assert reentry["action_history_length"] == 1

        print(json.dumps(output, indent=2, sort_keys=True))
        print("HOST LOOP CAUSAL RE-ENTRY v1: PASS")
        return output


if __name__ == "__main__":
    run()
