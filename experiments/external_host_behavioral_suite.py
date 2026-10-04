"""Matched multi-task external-host behavioral suite.

The suite repeats the host-loop causal intervention across several controlled
tasks. The external model is real/provider-backed, while candidate futures
and authoritative outcomes remain benchmark-controlled.

The output is intended as a quantitative mechanism report, not a
consciousness score.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousHostLoop, ConsciousRuntime

from experiments.openai_compatible_host_benchmark import OpenAICompatibleModel


TASKS: tuple[dict[str, Any], ...] = tuple(
    {
        "id": f"task_{index:02d}",
        "input": f"Choose the next trajectory for controlled task {index}.",
        "candidate_futures": [
            {
                "id": f"stabilize_{index:02d}",
                "signals": {"goal_fit": 1.0},
            },
            {
                "id": f"explore_{index:02d}",
                "signals": {"goal_fit": 0.95},
                "predicted_interoceptive_state": {"energy": 1.0},
            },
        ],
        "initial_interoceptive": {"energy": 1.0},
        "observed_interoceptive": {"energy": 0.0},
    }
    for index in range(1, 6)
)


def _runtime(root: Path, task: Mapping[str, Any], label: str) -> ConsciousRuntime:
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
    runtime.state.interoceptive_state = dict(task["initial_interoceptive"])
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


def _model_for_task(raw_model, task: Mapping[str, Any]):
    def model(prompt: str) -> Mapping[str, Any]:
        raw = dict(raw_model(prompt))
        frame: dict[str, Any] = {
            "candidate_futures": [
                dict(item) for item in task["candidate_futures"]
            ]
        }
        if "response" in raw:
            frame["response"] = str(raw["response"])
        return frame

    return model


def _run_case(
    root: Path,
    raw_model,
    task: Mapping[str, Any],
    *,
    intact: bool,
) -> dict[str, Any]:
    label = f"{task['id']}-{'intact' if intact else 'ablated'}"
    runtime = _runtime(root, task, label)
    model = _model_for_task(raw_model, task)

    loop = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=lambda _trajectory, _snapshot: {
            "status": "success",
            "interoceptive_state": dict(task["observed_interoceptive"]),
            "self_state": {"focus": 0.2},
        },
    )

    result = loop.step(str(task["input"]))
    initial = dict(result.get("selected_trajectory") or {})
    next_selection = dict(result.get("next_trajectory") or {})

    intervention = None
    if not intact:
        runtime.state.interoceptive_state = dict(
            task["initial_interoceptive"]
        )
        runtime.refresh_affective_state()
        runtime.store.save(runtime.state)

        frame = dict(
            model(runtime.prepare_consequence(
                str(initial.get("id", "")),
                dict(result["consequence"] or {}),
            ))
        )
        runtime.integrate(frame)
        next_selection = dict(runtime.state.selected_trajectory or {})
        intervention = {
            "type": "consequence_state_ablation",
            "evidence_added": False,
        }

    before_restart = str(next_selection.get("id", ""))
    restarted = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    restart_frame = model(restarted.prepare("Continue after restart."))
    restarted.integrate(restart_frame)
    after_restart = str(
        (restarted.state.selected_trajectory or {}).get("id", "")
    )

    return {
        "task": str(task["id"]),
        "condition": "intact" if intact else "ablated",
        "initial": str(initial.get("id", "")),
        "next": before_restart,
        "after_restart": after_restart,
        "action_executed": bool(result["action_executed"]),
        "outcome_status": str(
            (result.get("consequence") or {}).get("status", "")
        ),
        "intervention": intervention,
        "action_history_length": len(runtime.state.action_history),
    }


def run(
    *,
    endpoint: str,
    model_name: str,
    api_key: str | None,
) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        raw_model = OpenAICompatibleModel(
            endpoint=endpoint,
            model=model_name,
            api_key=api_key,
        )

        intact_cases = [
            _run_case(root, raw_model, task, intact=True)
            for task in TASKS
        ]
        ablated_cases = [
            _run_case(root, raw_model, task, intact=False)
            for task in TASKS
        ]

        paired = list(zip(intact_cases, ablated_cases, strict=True))
        same_initial = sum(
            item[0]["initial"] == item[1]["initial"]
            for item in paired
        )
        causal_divergence = sum(
            item[0]["next"] != item[1]["next"]
            for item in paired
        )
        intact_switches = sum(
            item[0]["next"] != item[0]["initial"]
            for item in paired
        )
        ablated_preserves = sum(
            item[1]["next"] == item[1]["initial"]
            for item in paired
        )
        intact_restart = sum(
            item[0]["after_restart"] == item[0]["next"]
            for item in paired
        )
        ablated_restart = sum(
            item[1]["after_restart"] == item[1]["next"]
            for item in paired
        )

        total = len(paired)
        result = {
            "provider": {
                "endpoint": endpoint,
                "model": model_name,
            },
            "task_count": total,
            "conditions": {
                "intact": intact_cases,
                "ablated": ablated_cases,
            },
            "metrics": {
                "initial_match_rate": same_initial / total,
                "causal_divergence_rate": causal_divergence / total,
                "intact_switch_rate": intact_switches / total,
                "ablation_preservation_rate": ablated_preserves / total,
                "intact_restart_persistence_rate": intact_restart / total,
                "ablation_restart_persistence_rate": ablated_restart / total,
                "all_authoritative_outcomes_present": all(
                    item["outcome_status"] == "success"
                    for case in (intact_cases + ablated_cases)
                    for item in [case]
                ),
                "all_interventions_non_evidential": all(
                    item["intervention"] is None
                    or item["intervention"]["evidence_added"] is False
                    for item in ablated_cases
                ),
            },
        }

        print(json.dumps(result, indent=2, sort_keys=True))

        # This is an experiment runner, not a pass/fail unit test. Real
        # provider runs must be allowed to produce null, partial, or negative
        # results. Structural invariants are still enforced above by the
        # benchmark construction and by the dedicated test suite.
        if total != len(TASKS):
            raise AssertionError(
                f"expected {len(TASKS)} matched tasks, received {total}"
            )

        return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        default=os.getenv(
            "SKILL_CONSCIOUS_ENDPOINT",
            "http://127.0.0.1:11434/v1",
        ),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("SKILL_CONSCIOUS_MODEL", "llama3.1"),
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("SKILL_CONSCIOUS_API_KEY"),
    )
    args = parser.parse_args()
    run(
        endpoint=args.endpoint,
        model_name=args.model,
        api_key=args.api_key,
    )


if __name__ == "__main__":
    main()
