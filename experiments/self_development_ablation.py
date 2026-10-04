"""Deterministic A/B/C/D ablation for self-development layers."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime


CONDITIONS = (
    ("A", {"homeostasis": False, "adaptive_targets": False, "priority_adaptation": False}),
    ("B", {"homeostasis": True, "adaptive_targets": False, "priority_adaptation": False}),
    ("C", {"homeostasis": True, "adaptive_targets": True, "priority_adaptation": False}),
    ("D", {"homeostasis": True, "adaptive_targets": True, "priority_adaptation": True}),
)

TRIALS = 18


def candidate_futures() -> list[dict[str, Any]]:
    return [
        {
            "id": "external_goal",
            "signals": {
                "goal_fit": 1.5,
                "self_alignment": 0.2,
                "continuity": 0.35,
                "risk": 0.15,
            },
            "predicted_interoceptive_state": {"energy": 0.4},
        },
        {
            "id": "self_maintenance",
            "signals": {
                "goal_fit": 0.2,
                "self_alignment": 0.8,
                "continuity": 0.8,
                "risk": 0.1,
            },
            "predicted_interoceptive_state": {"energy": 0.8},
        },
    ]


def make_runtime(
    name: str,
    path: Path,
    config: dict[str, bool],
) -> ConsciousRuntime:
    self_model: dict[str, Any] = {
        "trajectory_weights": {"goal_fit": 1.0},
    }

    if config["homeostasis"]:
        self_model["homeostatic_targets"] = {"energy": 0.8}

    if config["adaptive_targets"]:
        self_model["homeostatic_target_adaptation"] = {
            "enabled": True,
            "min_samples": 3,
            "error_threshold": 0.25,
            "confidence_threshold": 0.75,
            "required_high_error": 3,
            "learning_rate": 0.5,
            "max_step": 0.05,
            "cooldown": 2,
            "bounds": {"energy": [0.0, 1.0]},
        }

    if config["priority_adaptation"]:
        self_model["trajectory_priority_adaptation"] = {
            "enabled": True,
            "min_samples": 3,
            "utility_threshold": 0.5,
            "confidence_threshold": 0.75,
            "learning_rate": 0.5,
            "max_step": 0.25,
            "cooldown": 2,
            "bounds": {"goal_fit": [-3.0, 3.0]},
        }

    # Self-development A/B/C/D isolates homeostasis and adaptive learning.
    # Metacognition/self-report are orthogonal layers and would otherwise add
    # large persistent traces without changing the mechanism under test.
    runtime = ConsciousRuntime(
        name,
        path,
        metacognition_enabled=False,
        report_enabled=False,
    )
    runtime.integrate(
        {
            "response": "initialize controlled ablation",
            "self_model": self_model,
            "interoceptive_state": {"energy": 0.4}
            if config["homeostasis"]
            else {},
            "candidate_futures": candidate_futures(),
        }
    )
    return runtime


def count_oscillations(selections: list[str]) -> int:
    return sum(
        1
        for index in range(2, len(selections))
        if selections[index] == selections[index - 2]
        and selections[index] != selections[index - 1]
    )


def run_condition(
    label: str,
    config: dict[str, bool],
    root: Path,
) -> dict[str, Any]:
    runtime = make_runtime(label, root / f"{label}.json", config)
    selections: list[str] = []
    initial_error = runtime.calculate_homeostatic_error()

    for trial in range(1, TRIALS + 1):
        runtime.integrate(
            {
                "response": f"trial {trial}",
                "interoceptive_state": {"energy": 0.4}
                if config["homeostasis"]
                else {},
                "candidate_futures": candidate_futures(),
            }
        )
        selected = runtime.state.selected_trajectory
        if not isinstance(selected, dict):
            raise AssertionError(f"{label}: no trajectory selected on trial {trial}")
        trajectory_id = str(selected["id"])
        selections.append(trajectory_id)

        runtime.begin_action(selected)
        outcome = {
            "status": "success",
            "interoceptive_state": {"energy": 0.4}
            if config["homeostasis"]
            else {},
            "external_progress": 1.0 if trajectory_id == "external_goal" else 0.2,
        }
        runtime.complete_action(outcome)

        utility = 1.0 if trajectory_id == "external_goal" else 0.4
        runtime.integrate(
            {
                "response": f"evaluate trial {trial}",
                "candidate_futures": candidate_futures(),
                "consequence_trajectory": trajectory_id,
                "consequence": outcome,
                "self_evaluation": {
                    "utility": utility,
                    "credited_signal": "goal_fit",
                    "weight_delta": 99.0,
                },
            }
        )

    switches = sum(
        1
        for index in range(1, len(selections))
        if selections[index] != selections[index - 1]
    )
    continuity = 1.0 - switches / max(1, len(selections) - 1)
    oscillations = count_oscillations(selections)
    final_error = runtime.calculate_homeostatic_error()

    target_history = runtime.state.self_model.get(
        "homeostatic_adaptation_history",
        [],
    )
    target_history = [
        dict(item) for item in target_history if isinstance(item, dict)
    ]
    priority_history = runtime.state.self_model.get(
        "trajectory_priority_adaptation_history",
        [],
    )
    priority_history = [
        dict(item) for item in priority_history if isinstance(item, dict)
    ]

    learning_magnitude = sum(
        abs(float(item.get("delta", 0.0))) for item in target_history
    ) + sum(
        abs(float(item.get("delta", 0.0))) for item in priority_history
    )

    initial_target = 0.8 if config["homeostasis"] else None
    final_target = (
        runtime.state.self_model.get("homeostatic_targets", {}).get("energy")
        if config["homeostasis"]
        else None
    )

    return {
        "condition": label,
        "config": dict(config),
        "trajectory_selection": selections,
        "trajectory_switches": switches,
        "oscillation_count": oscillations,
        "continuity": round(continuity, 6),
        "initial_homeostatic_error": round(initial_error, 6),
        "final_homeostatic_error": round(final_error, 6),
        "convergence": round(max(0.0, initial_error - final_error), 6),
        "divergence": round(max(0.0, final_error - initial_error), 6),
        "self_model_change_events": len(target_history) + len(priority_history),
        "target_updates": target_history,
        "priority_updates": priority_history,
        "initial_target": initial_target,
        "final_target": final_target,
        "final_goal_fit_weight": runtime.state.self_model.get(
            "trajectory_weights",
            {},
        ).get("goal_fit"),
        "accumulated_learning": round(learning_magnitude, 6),
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        results = [run_condition(label, config, root) for label, config in CONDITIONS]

        assert [item["condition"] for item in results] == ["A", "B", "C", "D"]
        assert results[0]["trajectory_switches"] == 0
        assert results[0]["self_model_change_events"] == 0
        assert results[1]["final_target"] == 0.8
        assert results[2]["final_target"] < 0.8
        assert results[2]["self_model_change_events"] > 0
        assert results[3]["final_target"] < 0.8
        assert results[3]["priority_updates"]
        assert results[3]["final_goal_fit_weight"] > 1.0

        report = {
            "trials": TRIALS,
            "conditions": results,
            "metric_definitions": {
                "continuity": "1 - trajectory switch rate",
                "oscillation_count": "A-B-A transitions",
                "convergence": "initial homeostatic error minus final error, clipped at zero",
                "divergence": "final homeostatic error minus initial error, clipped at zero",
                "accumulated_learning": "sum of absolute target and priority update deltas",
            },
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        print("SELF-DEVELOPMENT A/B/C/D ABLATION: PASS")
        return report


if __name__ == "__main__":
    run()
