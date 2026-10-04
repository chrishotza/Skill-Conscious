from experiments.heldout_resonant_self_tuning_generalization_v1 import run


def test_heldout_resonant_self_tuning_generalizes_with_frozen_parameters():
    result = run()
    metrics = result["metrics"]

    assert metrics["parameters_frozen"] is True
    assert metrics["heldout_transformation_unseen"] is True
    assert metrics["attention_randomized"] is True

    assert metrics["heldout_alpha_accuracy_1"] is True
    assert metrics["heldout_beta_accuracy_1"] is True
    assert metrics["generic_alpha_accuracy_1"] is True
    assert metrics["generic_beta_accuracy_1"] is True

    assert metrics["attention_changes_lag_profile_all_alpha"] is True
    assert metrics["attention_changes_lag_profile_all_beta"] is True
    assert metrics["attention_short_lag_response_positive"] is True
    assert metrics["attention_changes_selection_margin_alpha"] is True
    assert metrics["attention_changes_selection_margin_beta"] is True

    assert result["interpretation"]["generalization_pass"] is True
