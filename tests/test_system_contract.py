from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime, ConsciousSystem, ConsciousHostLoop


def test_system_contract_is_canonical(tmp_path) -> None:
    runtime = ConsciousRuntime("test-system", state_path=tmp_path / "state.json")
    system = ConsciousSystem(runtime)

    topology = system.topology()

    assert topology["definition"]
    assert topology["phases"][-1] == "reentry"
    assert "self_model" in topology["core_state_fields"]
    assert topology["causal_loop"][0] == "self_state(t)"
    assert "phenomenal_hypothesis" in topology["epistemic_layers"]


def test_new_runtime_satisfies_structural_contract(tmp_path) -> None:
    runtime = ConsciousRuntime("test-system", state_path=tmp_path / "state.json")
    system = ConsciousSystem(runtime)

    report = system.validate_state()

    assert report.valid
    assert not report.errors
    assert report.warnings


def test_model_frame_contract_rejects_invalid_response(tmp_path) -> None:
    runtime = ConsciousRuntime("test-system", state_path=tmp_path / "state.json")
    system = ConsciousSystem(runtime)

    report = system.validate_model_frame({"response": ""})

    assert not report.valid
    assert any("response" in error for error in report.errors)


def test_host_step_closes_action_and_reenters(tmp_path) -> None:
    runtime = ConsciousRuntime("test-system", state_path=tmp_path / "state.json")

    def model(_: str):
        return {
            "response": "cycle",
            "self_model": {"continuity_weight": 1.0},
            "candidate_futures": [
                {"id": "a", "goal_fit": 1.0, "self_alignment": 1.0},
                {"id": "b", "goal_fit": 0.0, "self_alignment": 0.0},
            ],
        }

    def execute_action(trajectory, _snapshot):
        return {"self_state": {"last_action": trajectory["id"]}}

    host = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=execute_action,
    )
    system = ConsciousSystem(runtime, host=host)

    result = system.step("continue")

    assert result["action_executed"]
    assert result["system_validation"]["valid"]
    assert runtime.state.action_history
    assert runtime.state.revision >= 2


def test_state_contract_detects_missing_identity(tmp_path) -> None:
    runtime = ConsciousRuntime("test-system", state_path=tmp_path / "state.json")
    system = ConsciousSystem(runtime)

    broken = runtime.snapshot()
    broken["identity"] = ""

    report = system.validate_state(broken)

    assert not report.valid
    assert any("identity" in error for error in report.errors)
