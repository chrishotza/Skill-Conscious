from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime


def make_runtime(tmp_path: Path) -> ConsciousRuntime:
    return ConsciousRuntime("operational-continuity-test",
        state_path=tmp_path / "runtime.json",
        metacognition_enabled=False,
        report_enabled=False,
    )


def test_offline_to_dream_to_wake_creates_persistent_continuity(tmp_path: Path):
    runtime = make_runtime(tmp_path)
    runtime.state.memories = ["alpha", "beta", "gamma"]
    runtime.state.history = [
        {"revision": 1, "selected_trajectory": {"id": "learn"}},
        {"revision": 2, "selected_trajectory": {"id": "preserve_continuity"}},
        {"revision": 3, "selected_trajectory": {"id": "learn"}},
    ]
    runtime.store.save(runtime.state)

    runtime.set_operational_mode("offline")
    offline = runtime.advance_operational_cycle()

    assert offline["consolidation_profile"]["trajectory_scores"]["learn"] > 0.0
    assert runtime.state.self_model["operational_consolidation_profile"]

    runtime.set_operational_mode("dream_like")
    dream = runtime.advance_operational_cycle()

    assert dream["adaptation"] is not None
    replayed = dream["adaptation"]["last_replayed_trajectory"]
    assert replayed
    assert dream["attractor_changed"] is True

    restored = make_runtime(tmp_path)
    assert restored.operational_mode() == "dream_like"
    assert (
        restored.state.self_model["operational_replay_profile"]["last_replayed_trajectory"]
        == replayed
    )

    restored.reenter_wake()
    candidates = [
        {"id": replayed, "signals": {"goal_fit": 0.0}},
        {"id": "other", "signals": {"goal_fit": 0.0}},
    ]
    selected = restored.select_trajectory(candidates)

    assert selected["id"] == replayed
    assert restored.operational_mode() == "wake"


def test_replay_profile_is_runtime_owned_and_not_model_forgeable(tmp_path: Path):
    runtime = make_runtime(tmp_path)
    runtime.integrate(
        {
            "self_model": {"operational_replay_profile": {"trajectory_scores": {"forged": 1.0}}}
        }
    )

    assert "operational_replay_profile" not in runtime.state.self_model


def test_replay_reinforcement_decays_and_remains_bounded(tmp_path: Path):
    runtime = make_runtime(tmp_path)
    runtime.set_operational_mode("dream_like")
    first = runtime.advance_operational_cycle()
    first_target = first["adaptation"]["last_replayed_trajectory"]

    second = runtime.advance_operational_cycle()
    second_target = second["adaptation"]["last_replayed_trajectory"]

    profile = runtime.state.self_model["operational_replay_profile"]
    assert profile["replay_sequence"] == 2
    assert 0.0 <= max(profile["trajectory_scores"].values()) <= 1.0
    assert first_target
    assert second_target