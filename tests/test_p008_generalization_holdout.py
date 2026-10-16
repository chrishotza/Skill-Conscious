"""No holdout access from unit tests: only sealed release guard and pilot exercise."""
from pathlib import Path
import pytest
from experiments import p008_generalization_holdout as holdout
from experiments.p008_generalization_pilot import generate_scenario, run_arm
from experiments.p008_self_model_causal_runtime import CONDITION_NAMES


def test_holdout_not_released_before_separate_main_commit():
    with pytest.raises((FileNotFoundError, RuntimeError, ValueError)):
        holdout.verify_release()


def test_holdout_id_guard_rejects_invalid_ids():
    for bad in (-1, 31, 32, 999, 1128, 5000, "1000", True):
        with pytest.raises(ValueError):
            holdout.generate_holdout_scenario(bad)


def test_shared_arm_engine_tags_split_without_executing_holdout(tmp_path: Path):
    scenario = generate_scenario(0)
    arms = {
        name: run_arm(name, scenario, tmp_path, {})
        for name in CONDITION_NAMES
    }
    assert all(item["split"] == "pilot" for item in arms.values())
    assert all(item["restart_integrity"] for item in arms.values())
    assert arms["B_disconnected_self_model"]["selected_trajectory_each_cycle"] == (
        arms["D_matched_generic_state"]["selected_trajectory_each_cycle"]
    )


def test_holdout_executor_has_no_pr_or_dispatch_trigger():
    source = (Path(__file__).resolve().parents[1] /
              ".github/workflows/p008-generalization-holdout.yml").read_text()
    assert "branches: [main]" in source
    assert "research/p008_holdout_release.json" in source
    assert "pull_request:" not in source
    assert "workflow_dispatch:" not in source
    assert "--verify-release" in source
