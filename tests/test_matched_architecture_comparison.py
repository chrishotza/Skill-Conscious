from experiments.matched_architecture_comparison import run


def test_matched_architecture_comparison_is_not_explained_by_memory_alone():
    result = run()
    metrics = result["metrics"]

    assert metrics["matched_information_budget"] is True
    assert metrics["same_initial_selection"] is True
    assert metrics["same_pre_reentry_selection"] is True
    assert metrics["memory_only_stays_stable"] is True
    assert metrics["self_model_without_reentry_stays_stable"] is True
    assert metrics["causal_reentry_changes_trajectory"] is True
    assert metrics["only_reentry_diverges"] is True
    assert metrics["reentry_weight_increased"] is True
    assert metrics["reentry_reversible"] is True
    assert metrics["reentry_persists_after_restart"] is True
    assert metrics["intervention_non_evidential"] is True
    assert metrics["all_conditions_same_history_budget"] is True
    assert result["interpretation"]["phenomenal_consciousness_claim"] is False
