"""Longitudinal benchmark for operational continuity across offline replay and wake re-entry."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime

LONGITUDINAL_CYCLES = 4
OFFLINE_WARMUP_CYCLES = 2

CANDIDATES = [
    {"id": "alpha_path", "signals": {"goal_fit": 1.1, "learning": 0.0, "continuity": 1.0}},
    {"id": "beta_path", "signals": {"goal_fit": 0.7, "learning": 1.0, "continuity": 0.8}},
]


def _make_runtime(path: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=path,
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.state.self_model = {"trajectory_weights": {"goal_fit": 1.0, "learning": 0.5, "continuity": 1.0}}
    runtime.state.memories = ["seed-alpha", "seed-beta", "seed-alpha"]
    runtime.state.history = [
        {"revision": 1, "selected_trajectory": {"id": "alpha_path"}},
        {"revision": 2, "selected_trajectory": {"id": "alpha_path"}},
    ]
    runtime.store.save(runtime.state)
    return runtime


def _wake_selection(runtime: ConsciousRuntime) -> dict[str, Any]:
    runtime.integrate({
        "self_state": {"focus": 0.5},
        "candidate_futures": [dict(item) for item in CANDIDATES],
    })
    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict):
        raise AssertionError("wake cycle produced no selected trajectory")
    return {
        "trajectory": str(selected["id"]),
        "replay_profile": dict(runtime.state.self_model.get("operational_replay_profile", {})),
        "operational_state": runtime.snapshot_operational_state(),
    }


def _run_continuity(runtime: ConsciousRuntime) -> dict[str, Any]:
    baseline = _wake_selection(runtime)
    runtime.set_operational_mode("offline")
    offline_cycles = [runtime.advance_operational_cycle() for _ in range(OFFLINE_WARMUP_CYCLES)]
    runtime.set_operational_mode("dream_like")
    dream_cycles = [runtime.advance_operational_cycle(candidate_futures=[dict(item) for item in CANDIDATES]) for _ in range(LONGITUDINAL_CYCLES)]
    restarted = ConsciousRuntime(
        runtime.identity,
        state_path=Path(runtime.store.path),
        report_enabled=False,
        metacognition_enabled=False,
    )
    restart_profile = dict(restarted.state.self_model.get("operational_replay_profile", {}))
    restarted.reenter_wake()
    wake_cycles = [_wake_selection(restarted) for _ in range(LONGITUDINAL_CYCLES)]
    return {
        "condition": "continuity_replay",
        "baseline": baseline,
        "offline_trajectories": [item.get("selected_trajectory", {}).get("id") for item in offline_cycles],
        "dream_trajectories": [item.get("selected_trajectory", {}).get("id") for item in dream_cycles],
        "wake_trajectories": [item["trajectory"] for item in wake_cycles],
        "restart_profile": restart_profile,
        "reentry_count": restarted.snapshot_operational_state()["reentry_count"],
    }


def _run_consolidation_only(runtime: ConsciousRuntime) -> dict[str, Any]:
    baseline = _wake_selection(runtime)
    runtime.set_operational_mode("offline")
    offline_cycles = [runtime.advance_operational_cycle() for _ in range(OFFLINE_WARMUP_CYCLES + LONGITUDINAL_CYCLES)]
    runtime.reenter_wake()
    wake_cycles = [_wake_selection(runtime) for _ in range(LONGITUDINAL_CYCLES)]
    return {
        "condition": "consolidation_only",
        "baseline": baseline,
        "offline_trajectories": [item.get("selected_trajectory", {}).get("id") for item in offline_cycles],
        "wake_trajectories": [item["trajectory"] for item in wake_cycles],
        "replay_profile": dict(runtime.state.self_model.get("operational_replay_profile", {})),
        "reentry_count": runtime.snapshot_operational_state()["reentry_count"],
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        continuity = _run_continuity(_make_runtime(root / 'continuity.json', 'continuity'))
        control = _run_consolidation_only(_make_runtime(root / 'control.json', 'control'))

        first_continuity_wake = continuity['wake_trajectories'][0]
        first_control_wake = control['wake_trajectories'][0]
        replayed = continuity['dream_trajectories'][0]

        assert continuity['baseline']['trajectory'] == 'alpha_path'
        assert replayed == 'beta_path'
        assert first_continuity_wake == 'beta_path'
        assert first_control_wake == 'alpha_path'
        assert first_continuity_wake != first_control_wake
        assert continuity['restart_profile']['last_replayed_trajectory'] == replayed
        assert not control['replay_profile']

        result = {
            "conditions": [continuity, control],
            "metrics": {
                "baseline_wake": continuity["baseline"]["trajectory"],
                "dream_replay": replayed,
                "post_reentry_continuity": first_continuity_wake,
                "matched_control": first_control_wake,
                "causal_reentry_divergence": first_continuity_wake != first_control_wake,
                "replay_persisted_across_restart": bool(continuity["restart_profile"]),
                "replay_profile_cannot_be_forged_by_control": not bool(control["replay_profile"]),
            },
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        print("OPERATIONAL CONTINUITY BENCHMARK v1: PASS")
        return result


if __name__ == '__main__':
    run()