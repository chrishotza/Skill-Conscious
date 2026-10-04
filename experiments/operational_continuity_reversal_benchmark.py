"""Reversible longitudinal benchmark for history-dependent operational continuity."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime

REPLAY_CYCLES = 4
COUNTER_REPLAY_CYCLES = 2
CONTROL_OFFLINE_CYCLES = REPLAY_CYCLES + COUNTER_REPLAY_CYCLES

BASE_CANDIDATES = [
    {
        "id": "alpha_path",
        "signals": {"goal_fit": 1.1, "learning": 0.0, "continuity": 1.0},
    },
    {
        "id": "beta_path",
        "signals": {"goal_fit": 0.7, "learning": 1.0, "continuity": 0.8},
    },
]

COUNTER_REPLAY_CANDIDATES = [
    {
        "id": "alpha_path",
        "signals": {"goal_fit": 1.1, "learning": 1.0, "continuity": 1.0},
    },
    {
        "id": "beta_path",
        "signals": {"goal_fit": 0.7, "learning": 0.0, "continuity": 0.8},
    },
]


def _make_runtime(path: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=path,
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.state.self_model = {
        "trajectory_weights": {
            "goal_fit": 1.0,
            "learning": 0.5,
            "continuity": 1.0,
        }
    }
    runtime.state.memories = ["seed-alpha", "seed-beta", "seed-alpha"]
    runtime.state.history = [
        {"revision": 1, "selected_trajectory": {"id": "alpha_path"}},
        {"revision": 2, "selected_trajectory": {"id": "alpha_path"}},
    ]
    runtime.store.save(runtime.state)
    return runtime


def _select_wake(runtime: ConsciousRuntime) -> dict[str, Any]:
    runtime.reenter_wake()
    runtime.integrate(
        {
            "self_state": {"focus": 0.5},
            "candidate_futures": [dict(item) for item in BASE_CANDIDATES],
        }
    )
    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict):
        raise AssertionError("wake cycle produced no selected trajectory")
    return {
        "trajectory": str(selected["id"]),
        "replay_profile": dict(
            runtime.state.self_model.get("operational_replay_profile", {})
        ),
        "operational_state": runtime.snapshot_operational_state(),
    }


def _replay(
    runtime: ConsciousRuntime,
    candidates: list[dict[str, Any]],
    cycles: int,
) -> list[dict[str, Any]]:
    runtime.set_operational_mode("dream_like")
    results: list[dict[str, Any]] = []
    for _ in range(cycles):
        result = runtime.advance_operational_cycle(
            candidate_futures=[dict(item) for item in candidates]
        )
        results.append(result)
    return results


def _run_reversible(runtime: ConsciousRuntime) -> dict[str, Any]:
    baseline = _select_wake(runtime)

    runtime.set_operational_mode("offline")
    warmup = [runtime.advance_operational_cycle() for _ in range(2)]

    beta_replay = _replay(runtime, BASE_CANDIDATES, REPLAY_CYCLES)
    beta_profile = dict(runtime.state.self_model["operational_replay_profile"])

    first_restart = ConsciousRuntime(
        runtime.identity,
        state_path=Path(runtime.store.path),
        report_enabled=False,
        metacognition_enabled=False,
    )
    first_reentry = _select_wake(first_restart)

    alpha_counter_replay = _replay(
        first_restart,
        COUNTER_REPLAY_CANDIDATES,
        COUNTER_REPLAY_CYCLES,
    )
    alpha_profile = dict(
        first_restart.state.self_model["operational_replay_profile"]
    )

    second_restart = ConsciousRuntime(
        first_restart.identity,
        state_path=Path(first_restart.store.path),
        report_enabled=False,
        metacognition_enabled=False,
    )
    final_reentry = _select_wake(second_restart)

    return {
        "condition": "reversible_continuity",
        "baseline": baseline,
        "offline_warmup": len(warmup),
        "beta_replay_trajectories": [
            item.get("selected_trajectory", {}).get("id")
            for item in beta_replay
        ],
        "first_reentry": first_reentry,
        "alpha_counter_replay_trajectories": [
            item.get("selected_trajectory", {}).get("id")
            for item in alpha_counter_replay
        ],
        "beta_profile": beta_profile,
        "alpha_counter_profile": alpha_profile,
        "final_reentry": final_reentry,
        "restarts": 2,
    }


def _run_control(runtime: ConsciousRuntime) -> dict[str, Any]:
    baseline = _select_wake(runtime)

    runtime.set_operational_mode("offline")
    offline = [
        runtime.advance_operational_cycle()
        for _ in range(CONTROL_OFFLINE_CYCLES)
    ]

    final = _select_wake(runtime)
    return {
        "condition": "consolidation_only",
        "baseline": baseline,
        "offline_cycles": len(offline),
        "final_reentry": final,
        "replay_profile": dict(
            runtime.state.self_model.get("operational_replay_profile", {})
        ),
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        reversible = _run_reversible(
            _make_runtime(root / "reversible.json", "reversible")
        )
        control = _run_control(
            _make_runtime(root / "control.json", "control")
        )

        beta_phase = reversible["beta_replay_trajectories"]
        counter_phase = reversible["alpha_counter_replay_trajectories"]
        first_reentry = reversible["first_reentry"]["trajectory"]
        final_reentry = reversible["final_reentry"]["trajectory"]
        control_reentry = control["final_reentry"]["trajectory"]

        assert reversible["baseline"]["trajectory"] == "alpha_path"
        assert beta_phase and all(item == "beta_path" for item in beta_phase)
        assert first_reentry == "beta_path"
        assert counter_phase and all(item == "alpha_path" for item in counter_phase)
        assert final_reentry == "alpha_path"
        assert control["baseline"]["trajectory"] == "alpha_path"
        assert control_reentry == "alpha_path"
        assert not control["replay_profile"]
        assert reversible["final_reentry"]["operational_state"]["reentry_count"] >= 2

        result = {
            "conditions": [reversible, control],
            "metrics": {
                "baseline_wake": reversible["baseline"]["trajectory"],
                "first_reentry_after_beta_history": first_reentry,
                "counter_replay": counter_phase[-1],
                "final_reentry_after_alpha_history": final_reentry,
                "matched_control": control_reentry,
                "history_dependent_reversal": (
                    first_reentry == "beta_path"
                    and final_reentry == "alpha_path"
                ),
                "replay_state_survives_two_restarts": bool(
                    reversible["final_reentry"]["replay_profile"]
                ),
                "counter_history_changes_internal_trace": (
                    reversible["beta_profile"]["last_replayed_trajectory"]
                    != reversible["alpha_counter_profile"]["last_replayed_trajectory"]
                ),
                "control_preserves_baseline": (
                    control["baseline"]["trajectory"] == control_reentry == "alpha_path"
                ),
                "external_outcome_evidence_used": False,
            },
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        print("OPERATIONAL CONTINUITY REVERSIBILITY BENCHMARK v1: PASS")
        return result


if __name__ == "__main__":
    run()
