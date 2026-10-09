import json
from pathlib import Path

import pytest

from experiments.p008_self_model_causal_runtime import (
    CONDITION_NAMES,
    DEFAULT_CONTINUITY_WEIGHT,
    INTERVENTION,
    run,
)


@pytest.fixture(scope="module")
def assay_result(tmp_path_factory: pytest.TempPathFactory) -> dict:
    output = tmp_path_factory.mktemp("p008-result") / "result.json"
    return run(output, git_commit="test-commit-sha")


def _conditions(result: dict) -> dict[str, dict]:
    return {item["condition"]: item for item in result["conditions"]}


def test_assay_conditions_match_cf01_registry(assay_result: dict) -> None:
    assert tuple(item["condition"] for item in assay_result["conditions"]) == CONDITION_NAMES
    assert set(CONDITION_NAMES) == {
        "A_no_self_model",
        "B_disconnected_self_model",
        "C_causal_self_model",
        "D_matched_generic_state",
    }


def test_single_factor_intervention_changes_only_continuity(assay_result: dict) -> None:
    assert INTERVENTION == {"continuity": 0.0}
    assert DEFAULT_CONTINUITY_WEIGHT == 1.0
    metadata = assay_result["metadata"]
    assert metadata["intervention_delta_from_default"] == -1.0
    assert metadata["intervention"] == {"continuity": 0.0}


def test_causal_condition_diverges_from_both_controls(assay_result: dict) -> None:
    conditions = _conditions(assay_result)
    primary = assay_result["primary_outcome"]

    assert [cycle["selected_trajectory"] for cycle in conditions["A_no_self_model"]["cycles"]] == [
        "preserve",
        "preserve",
    ]
    assert [cycle["selected_trajectory"] for cycle in conditions["B_disconnected_self_model"]["cycles"]] == [
        "preserve",
        "preserve",
    ]
    assert [cycle["selected_trajectory"] for cycle in conditions["D_matched_generic_state"]["cycles"]] == [
        "preserve",
        "preserve",
    ]
    assert [cycle["selected_trajectory"] for cycle in conditions["C_causal_self_model"]["cycles"]] == [
        "explore",
        "explore",
    ]
    assert primary["C_vs_B_disconnected_self_model"] == 1.0
    assert primary["C_vs_D_matched_generic_state"] == 1.0
    assert primary["B_vs_D_control_agreement_error_rate"] == 0.0
    assert primary["noncausal_controls_agree"] is True
    assert primary["predeclared_mechanism_criterion_met"] is True


def test_self_model_or_generic_intervention_survives_restart(assay_result: dict) -> None:
    conditions = _conditions(assay_result)
    assert assay_result["primary_outcome"]["all_interventions_persist_after_restart"] is True

    assert conditions["B_disconnected_self_model"]["persisted_model_weights_after_restart"] == {
        "continuity": 0.0
    }
    assert conditions["C_causal_self_model"]["persisted_model_weights_after_restart"] == {
        "continuity": 0.0
    }
    assert conditions["D_matched_generic_state"]["persisted_generic_state_after_restart"] == {
        "continuity": 0.0
    }
    for result in conditions.values():
        assert result["cycles"][1]["revision"] > result["cycles"][0]["revision"]
        assert len(result["state_sha256_after_restart"]) == 64


def test_result_artifact_is_valid_json_with_provenance(assay_result: dict) -> None:
    artifact = Path(assay_result["artifact_path"])
    assert artifact.is_file()
    stored = json.loads(artifact.read_text(encoding="utf-8"))
    assert stored == assay_result
    assert stored["schema_version"] == "1.1"
    assert stored["metadata"]["git_commit"] == "test-commit-sha"
    assert stored["metadata"]["runtime_version"]
    assert len(stored["metadata"]["candidate_set_sha256"]) == 64
    assert len(stored["metadata"]["input_sha256"]) == 64
    assert stored["metadata"]["seed"] == 0
    assert stored["primary_outcome"]["name"] == "trajectory_selection_divergence"
    assert stored["limitations"]
