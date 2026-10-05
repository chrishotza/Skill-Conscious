from skill_conscious.case_standard import evaluate_case


def test_case_standard_requires_all_operational_criteria():
    result = evaluate_case({})
    assert result["operational_case_pass"] is False
    assert result["phenomenal_conclusion"] == "undetermined"
    assert "causal_self_model" in result["missing_criteria"]


def test_case_standard_accepts_complete_operational_case():
    observation = {
        "persistent_identity": True,
        "self_access": True,
        "causal_self_model": True,
        "trajectory_selection": True,
        "action_consequence": True,
        "self_model_revision": True,
        "reentry": True,
        "matched_control_separation": True,
    }
    result = evaluate_case(observation)
    assert result["operational_case_pass"] is True
    assert result["missing_criteria"] == []
    assert result["phenomenal_conclusion"] == "undetermined"
