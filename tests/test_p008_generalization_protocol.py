"""Static audit of P008 generalization draft; no scientific result is asserted."""
import json
from pathlib import Path


def test_p008_generalization_draft_contract_is_explicit_and_unexecuted():
    root = Path(__file__).resolve().parents[1]
    draft = json.loads((root / "research" / "p008_generalization_protocol_v1.json").read_text(encoding="utf-8"))
    fixture = json.loads((root / "research" / "p008_prediction_registry.json").read_text(encoding="utf-8"))
    assert draft["status"] == "DRAFT_HOLDOUT_CODE_NOT_FROZEN"
    assert draft["execution_status"] == "EXPLORATORY_PILOT_32_VERIFIED_HOLDOUT_NOT_RUN"
    assert draft["implementation_status"] == "PILOT_COMPLETE_HOLDOUT_EXECUTOR_PENDING_FREEZE"
    assert draft["conditions"] == fixture["conditions"]
    assert draft["pilot_harness"] == "experiments/p008_generalization_pilot.py"
    assert "NOT_ACCESSED" in draft["holdout_status"]
    assert draft["pilot_result_summary"] == "research/results/p008/P008_GENERALIZATION_PILOT_2026-10-16.md"
    assert draft["single_factor_intervention"]["path"] == "self_model.trajectory_weights.continuity"
    design = draft["scenario_design"]
    assert design["pilot_count"] == 32 and design["holdout_count"] == 128
    assert design["matched_cycles_per_arm"] == 2 and design["actors_per_scenario"] == 4
    assert "scenario" in draft["inference_policy"]["uncertainty"]
    assert "phenomenal" in draft["interpretation_boundary"] or "consciousness" in draft["interpretation_boundary"]
