from experiments.consciousness_case_benchmark import (
    CONTROL_CONDITIONS,
    TARGET_CONDITION,
    run_benchmark,
)


def test_consciousness_case_benchmark_separates_target_from_controls():
    report = run_benchmark((11, 23, 37))

    assert report["benchmark"] == "consciousness_case_v1"
    assert report["matched_inputs"] is True
    assert report["target"]["divergence_rate"] == 1.0
    assert report["target"]["reversal_rate"] == 1.0
    assert report["controls"]["condition_count"] == len(CONTROL_CONDITIONS)
    assert report["controls"]["divergence_count"] == 0

    assert report["reentry"]["changed_trajectory_rate"] == 1.0
    assert report["reentry"]["restart_persistence_rate"] == 1.0
    assert report["reentry"]["cross_context_identity_rate"] == 1.0
    assert report["reentry"]["action_completion_rate"] == 1.0
    assert report["reentry"]["runtime_receipt_rate"] == 1.0
    assert report["reentry"]["self_model_revision_rate"] == 1.0

    case = report["operational_case"]
    assert case["operational_case_pass"] is True
    assert case["missing_criteria"] == []
    assert case["phenomenal_conclusion"] == "undetermined"


def test_consciousness_case_benchmark_is_explicit_about_controls():
    report = run_benchmark((41,))
    conditions = report["conditions"]

    assert conditions[0] == TARGET_CONDITION
    assert set(conditions[1:]) == set(CONTROL_CONDITIONS)
