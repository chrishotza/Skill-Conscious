"""P008 runtime assay: causal intervention on the persistent self-model.

This experiment uses the actual ConsciousRuntime trajectory scorer.
It compares a default condition, a self-model condition, a targeted
self-model intervention, and a matched non-self-state control.

This tests functional causal self-reference. It does not test phenomenal
consciousness directly.
"""
from __future__ import annotations

import json
import tempfile
from dataclasses import asdict
from pathlib import Path

from skill_conscious import ConsciousRuntime


CANDIDATES = [
    {
        "id": "preserve",
        "signals": {
            "goal_fit": 0.50,
            "continuity": 1.00,
            "learning": 0.20,
        },
    },
    {
        "id": "explore",
        "signals": {
            "goal_fit": 0.60,
            "continuity": 0.20,
            "learning": 1.00,
        },
    },
]


def run_condition(name: str, tmp: Path) -> dict:
    runtime = ConsciousRuntime(
        identity=f"p008-{name}",
        state_path=tmp / f"{name}.json",
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
    )

    if name == "self_model_neutral":
        runtime.state.self_model["trajectory_weights"] = {
            "goal_fit": 1.0,
            "continuity": 1.0,
            "learning": 0.5,
        }
    elif name == "self_model_preserve":
        runtime.state.self_model["trajectory_weights"] = {
            "goal_fit": 1.0,
            "continuity": 2.0,
            "learning": 0.2,
        }
    elif name == "self_model_explore":
        runtime.state.self_model["trajectory_weights"] = {
            "goal_fit": 1.0,
            "continuity": 0.0,
            "learning": 2.0,
        }
    elif name == "generic_state_control":
        # Change persistent state that is not consumed by trajectory_weights().
        runtime.state.self_state["control_parameter"] = 1.0

    selected = runtime.select_trajectory(CANDIDATES)
    scores = {
        item["id"]: runtime.score_trajectory(item)
        for item in CANDIDATES
    }

    return {
        "condition": name,
        "selected": selected["id"],
        "scores": scores,
        "trajectory_weights": runtime.trajectory_weights(),
        "self_state": dict(runtime.state.self_state),
        "self_model": dict(runtime.state.self_model),
    }


def run() -> dict:
    with tempfile.TemporaryDirectory(prefix="p008-self-model-") as directory:
        root = Path(directory)
        conditions = [
            "baseline",
            "self_model_neutral",
            "self_model_preserve",
            "self_model_explore",
            "generic_state_control",
        ]
        results = [run_condition(name, root) for name in conditions]

    return {
        "experiment": "P008-runtime-self-model-causal-intervention",
        "candidate_set": CANDIDATES,
        "results": results,
        "interpretation_boundary": (
            "A condition-specific trajectory effect establishes functional "
            "dependence of the runtime on the manipulated self-model variable. "
            "It does not establish phenomenal consciousness."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
