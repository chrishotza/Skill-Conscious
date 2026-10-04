from __future__ import annotations

from pathlib import Path

import pytest

from skill_conscious.core import ConsciousRuntime
from skill_conscious.state_regime import OPERATIONAL_MODES


def make_runtime(tmp_path: Path) -> ConsciousRuntime:
    return ConsciousRuntime(
        "operational-regime-test",
        state_path=tmp_path / "state.json",
        metacognition_enabled=False,
        report_enabled=False,
    )


def test_operational_modes_change_computation_and_persist(tmp_path: Path):
    runtime = make_runtime(tmp_path)
    runtime.state.memories = ["alpha", "beta"]
    runtime.state.history = [
        {"revision": 1, "selected_trajectory": {"id": "preserve_continuity"}},
        {"revision": 2, "selected_trajectory": {"id": "learn"}},
    ]
    runtime.store.save(runtime.state)

    assert runtime.operational_mode() == "wake"
    assert runtime.operational_snapshot()["dynamics"]["accepts_external_input"] is True

    runtime.set_operational_mode("offline")
    assert runtime.operational_mode() == "offline"
    assert runtime.operational_snapshot()["dynamics"]["accepts_external_input"] is False
    with pytest.raises(RuntimeError):
        runtime.present_field("external input")

    offline = runtime.advance_operational_cycle()
    assert offline["mode"] == "offline"
    assert offline["consolidation"]["memory_count"] == 2
    assert offline["operational_state"]["consolidation_count"] == 1

    restored = make_runtime(tmp_path)
    assert restored.operational_mode() == "offline"
    assert restored.snapshot_operational_state()["consolidation_count"] == 1
    assert restored.snapshot_operational_state()["last_replay_signature"]


def test_dream_like_mode_replays_without_crossing_action_boundary(tmp_path: Path):
    runtime = make_runtime(tmp_path)
    runtime.state.memories = ["one", "two", "three"]
    runtime.state.history = [
        {"revision": 1, "selected_trajectory": {"id": "learn"}},
        {"revision": 2, "selected_trajectory": {"id": "integrate_latent_pattern"}},
    ]
    runtime.store.save(runtime.state)

    runtime.set_operational_mode("dream_like")
    result = runtime.advance_operational_cycle()

    assert result["mode"] == "dream_like"
    assert result["replay"].startswith("Internal replay for dream-like computation:")
    assert result["selected_trajectory"]["id"]
    assert runtime.snapshot_operational_state()["replay_count"] == 1
    assert runtime.state.action_history == []
    assert runtime.state.pending_action is None
    with pytest.raises(RuntimeError):
        runtime.begin_action(result["selected_trajectory"])


def test_wake_reentry_restores_world_access(tmp_path: Path):
    runtime = make_runtime(tmp_path)
    runtime.set_operational_mode("offline")
    runtime.advance_operational_cycle()

    reentry = runtime.reenter_wake()
    assert reentry["mode"] == "wake"
    assert reentry["reentry_count"] == 1
    assert runtime.operational_mode() == "wake"
    assert runtime.prepare_frame("new external event")["present"]["world_now"] == "new external event"


def test_supported_modes_are_explicit():
    assert OPERATIONAL_MODES == ("wake", "offline", "dream_like")
