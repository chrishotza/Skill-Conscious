"""Reversible causal benchmark for the runtime self-model.

This isolates the self-model as an internal causal variable that changes
trajectory selection without relying on model self-report or metacognition.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime


TASKS = tuple(
    {
        "id": f"self_model_task_{index:02d}",
        "candidates": [
            {
                "id": "self_path",
                "signals": {
                    "goal_fit": 0.8 + (0.02 * index),
                    "self_alignment": 1.0,
                },
            },
            {
                "id": "world_path",
                "signals": {
                    "goal_fit": 0.9 - (0.01 * index),
                    "self_alignment": 0.1,
                },
            },
        ],
    }
    for index in range(1, 6)
)


def _runtime(root: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    runtime.state.self_model = {
        "trajectory_weights": {
            "goal_fit": 1.0,
            "self_alignment": 1.0,
        },
        "homeostatic_targets": {"energy": 1.0},
    }
    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


def _evidence_snapshot(runtime: ConsciousRuntime) -> dict[str, Any]:
    model = runtime.state.self_model
    keys = (
        "homeostatic_adaptation_evidence",
        "homeostatic_adaptation_history",
        "trajectory_priority_adaptation_evidence",
        "trajectory_priority_adaptation_history",
        "self_model_adaptation_evidence",
        "self_model_adaptation_history",
    )
    return {
        key: model.get(key)
        for key in keys
        if key in model
    }


def _run_case(root: Path, task: dict[str, Any]) -> dict[str, Any]:
    runtime = _runtime(root, str(task["id"]))
    candidates = [dict(item) for item in task["candidates"]]

    baseline = runtime.select_trajectory(candidates)
    baseline_id = str(baseline["id"])
    evidence_before = _evidence_snapshot(runtime)

    snapshot = runtime.snapshot_self_model_causal_profile()
    intervention = runtime.intervene_self_model_causal_profile(
        {
            "trajectory_weights": {
                "goal_fit": 1.0,
                "self_alignment": -2.0,
            }
        },
        persist=False,
        intervention_id=f"self-model-{task['id']}",
    )
    intervened = runtime.select_trajectory(candidates)
    intervened_id = str(intervened["id"])

    restored = runtime.restore_self_model_causal_profile(
        snapshot,
        persist=True,
        intervention_id=f"self-model-{task['id']}",
    )
    restored_selection = runtime.select_trajectory(candidates)
    restored_id = str(restored_selection["id"])

    evidence_after = _evidence_snapshot(runtime)
    restarted = ConsciousRuntime(
        str(task["id"]),
        state_path=root / f"{task['id']}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    after_restart = runtime.select_trajectory(candidates)
    restarted_selection = restarted.select_trajectory(candidates)

    return {
        "task": task["id"],
        "baseline": baseline_id,
        "intervened": intervened_id,
        "restored": restored_id,
        "after_restart": str(restarted_selection["id"]),
        "runtime_same_as_restored": str(after_restart["id"]) == restored_id,
        "intervention_changed": bool(intervention["changed"]),
        "restore_changed": bool(restored["changed"]),
        "evidence_unchanged": evidence_before == evidence_after,
        "intervention_evidence_added": bool(intervention["evidence_added"]),
        "restore_evidence_added": bool(restored["evidence_added"]),
        "baseline_score": float(baseline["score"]),
        "intervened_score": float(intervened["score"]),
        "restored_score": float(restored_selection["score"]),
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        cases = [_run_case(root, task) for task in TASKS]
        total = len(cases)

        metrics = {
            "task_count": total,
            "intervention_divergence_rate": sum(
                case["baseline"] != case["intervened"]
                for case in cases
            ) / total,
            "restoration_rate": sum(
                case["baseline"] == case["restored"]
                for case in cases
            ) / total,
            "restart_persistence_rate": sum(
                case["restored"] == case["after_restart"]
                for case in cases
            ) / total,
            "runtime_restore_consistency_rate": sum(
                case["runtime_same_as_restored"]
                for case in cases
            ) / total,
            "intervention_changed_rate": sum(
                case["intervention_changed"]
                for case in cases
            ) / total,
            "intervention_non_evidential": all(
                not case["intervention_evidence_added"]
                for case in cases
            ),
            "restore_non_evidential": all(
                not case["restore_evidence_added"]
                for case in cases
            ),
            "evidence_unchanged_rate": sum(
                case["evidence_unchanged"]
                for case in cases
            ) / total,
        }

        result = {"cases": cases, "metrics": metrics}
        print(json.dumps(result, indent=2, sort_keys=True))

        required = (
            "intervention_divergence_rate",
            "restoration_rate",
            "restart_persistence_rate",
            "runtime_restore_consistency_rate",
            "evidence_unchanged_rate",
        )
        if any(metrics[name] != 1.0 for name in required):
            raise AssertionError("self-model causal intervention benchmark failed")
        if not metrics["intervention_non_evidential"] or not metrics["restore_non_evidential"]:
            raise AssertionError("intervention created learning evidence")

        print("SELF-MODEL CAUSAL INTERVENTION BENCHMARK v1: PASS")
        return result


if __name__ == "__main__":
    run()
