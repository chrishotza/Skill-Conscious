from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime, build_embodiment_state


def test_embodiment_state_is_runtime_owned_and_persistent(tmp_path: Path):
    runtime = ConsciousRuntime(
        "embodied",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "self_model": {
                "resource_budget": {"energy": 0.8},
            },
            "interoceptive_state": {"energy": 0.4},
            "candidate_futures": [
                {"id": "observe", "signals": {"goal_fit": 1.0}},
            ],
        }
    )

    state = runtime.snapshot_embodiment()
    assert state["boundary_integrity"] == 1.0
    assert state["interoceptive_coupling"] == 1.0
    assert state["resource_fit"] < 1.0

    restarted = ConsciousRuntime(
        "embodied",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    assert restarted.snapshot_embodiment() == state


def test_action_outcome_causally_changes_ownership_and_action_cost(tmp_path: Path):
    runtime = ConsciousRuntime(
        "ownership",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "candidate_futures": [
                {"id": "act", "signals": {"goal_fit": 1.0}},
            ],
        }
    )

    before = runtime.snapshot_embodiment()
    selected = runtime.state.selected_trajectory
    runtime.begin_action(selected)
    runtime.complete_action({"resource_cost": 0.6, "interoceptive_state": {"energy": 0.7}})
    after = runtime.snapshot_embodiment()

    assert after["ownership_coupling"] == 1.0
    assert after["action_cost"] == 0.6
    assert after["interoceptive_coupling"] == 1.0
    assert after["ownership_coupling"] >= before["ownership_coupling"]


def test_model_cannot_forge_embodiment_state(tmp_path: Path):
    runtime = ConsciousRuntime(
        "protected-embodiment",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "embodiment_state": {
                "boundary_integrity": 0.0,
                "action_cost": 1.0,
            },
            "candidate_futures": [
                {"id": "observe", "signals": {"goal_fit": 1.0}},
            ],
        }
    )
    state = runtime.snapshot_embodiment()
    assert state["boundary_integrity"] == 1.0
    assert state["action_cost"] == 0.0


def test_geometry_includes_operational_embodiment_dimensions(tmp_path: Path):
    runtime = ConsciousRuntime(
        "geometry-embodied",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "self_model": {"resource_budget": {"energy": 0.8}},
            "interoceptive_state": {"energy": 0.4},
            "candidate_futures": [
                {"id": "observe", "signals": {"goal_fit": 1.0}},
            ],
        }
    )
    features = runtime.snapshot_experience_geometry()["current"]["features"]
    assert "resource_fit" in features
    assert "ownership_coupling" in features
    assert "action_cost" in features
