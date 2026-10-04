"""Causal ablation benchmark for the runtime-owned replay trace."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime

CANDIDATES = [
    {
        "id": "alpha_path",
        "signals": {"goal_fit": 1.1, "learning": 0.0, "continuity": 1.0},
    },
    {
        "id": "beta_path",
        "signals": {"goal_fit": 0.7, "learning": 1.0, "continuity": 0.8},
    },
]


def _make_runtime(path: Path) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        "replay-ablation",
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


def _wake(runtime: ConsciousRuntime) -> str:
    runtime.reenter_wake()
    runtime.integrate(
        {
            "self_state": {"focus": 0.5},
            "candidate_futures": [dict(item) for item in CANDIDATES],
        }
    )
    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict):
        raise AssertionError("wake cycle produced no selection")
    return str(selected["id"])


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        runtime = _make_runtime(Path(tmp) / "state.json")
        runtime.set_operational_mode("dream_like")

        replay = [
            runtime.advance_operational_cycle(
                candidate_futures=[dict(item) for item in CANDIDATES]
            )
            for _ in range(4)
        ]
        profile = runtime.snapshot_operational_replay_profile()

        restarted = ConsciousRuntime(
            runtime.identity,
            state_path=Path(runtime.store.path),
            report_enabled=False,
            metacognition_enabled=False,
        )
        intact = _wake(restarted)

        before = restarted.snapshot_operational_replay_profile()
        intervention = restarted.intervene_operational_replay_profile(
            {},
            intervention_id="replay-ablation-v1",
        )
        ablated = _wake(restarted)

        restore = restarted.restore_operational_replay_profile(
            before,
            intervention_id="replay-ablation-v1-restore",
        )
        restored = _wake(restarted)

        persisted_profile = bool(restarted.snapshot_operational_replay_profile())

        result = {
            "metrics": {
                "replay_phase": [
                    item.get("selected_trajectory", {}).get("id")
                    for item in replay
                ],
                "intact_reentry": intact,
                "ablated_reentry": ablated,
                "restored_reentry": restored,
                "replay_profile_persisted": persisted_profile,
                "intervention_changed_selection": intact != ablated,
                "restoration_recovered_selection": restored == intact,
                "intervention_added_evidence": intervention["evidence_added"],
                "restore_added_evidence": restore["evidence_added"],
                "runtime_trace_was_present_before_ablation": bool(profile),
            },
            "profile_after_restore": restarted.snapshot_operational_replay_profile(),
        }

        assert result["metrics"]["replay_phase"] and all(
            item == "beta_path" for item in result["metrics"]["replay_phase"]
        )
        assert intact == "beta_path"
        assert ablated == "alpha_path"
        assert restored == "beta_path"
        assert persisted_profile is True
        assert intervention["evidence_added"] is False
        assert restore["evidence_added"] is False

        print(json.dumps(result, indent=2, sort_keys=True))
        print("OPERATIONAL REPLAY TRACE CAUSAL ABLATION v1: PASS")
        return result


if __name__ == "__main__":
    run()
