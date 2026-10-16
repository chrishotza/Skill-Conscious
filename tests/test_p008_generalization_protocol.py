"""Static audit of P008 generalization draft; no scientific result is asserted."""
import json
from pathlib import Path


def test_p008_generalization_draft_contract_is_explicit_and_unexecuted():
    root = Path(__file__).resolve().parents[1]
    draft = json.loads((root / "research" / "p008_generalization_protocol_v1.json").read_text(encoding="utf-8"))
    fixture = json.loads((root / "research" / "p008_prediction_registry.json").read_text(encoding="utf-8"))
    assert draft["status"] == "DRAFT_NOT_FROZEN_NOT_EXECUTED"
    assert draft["execution_status"] == "NOT_RUN"
    assert draft["implementation_status"] == "NOT_IMPLEMENTED"
    assert draft["conditions"] == fixture["conditions"]
    assert draft["single_factor_intervention"]["path"] == "self_model.trajectory_weights.continuity"
    design = draft["scenario_design"]
    assert design["pilot_count"] == 32 and design["holdout_count"] == 128
    assert design["matched_cycles_per_arm"] == 2 and design["actors_per_scenario"] == 4
    assert "scenario" in draft["inference_policy"]["uncertainty"]
    assert "phenomenal" in draft["interpretation_boundary"] or "consciousness" in draft["interpretation_boundary"]
