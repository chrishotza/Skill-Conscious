from experiments.resonant_self_tuning_causal_benchmark import run


def test_resonant_self_tuning_is_causally_reversible():
    result = run()
    metrics = result["metrics"]

    assert metrics["matched_information_multiset"] is True
    assert metrics["matched_final_state"] is True
    assert metrics["matched_candidate_field"] is True
    assert metrics["matched_temporal_order_only"] is True
    assert metrics["matched_experimental_selects_alpha"] is True
    assert metrics["matched_control_selects_beta"] is True
    assert metrics["temporal_order_changes_selection"] is True

    assert metrics["endogenous_lag_profile_changes"] is True
    assert metrics["endogenous_selection_changes"] is True

    assert metrics["independent_alpha_accuracy_1"] is True
    assert metrics["independent_beta_accuracy_1"] is True
    assert metrics["independent_marginals_match"] is True

    assert metrics["hysteresis_entry_pass"] is True
    assert metrics["hysteresis_exit_pass"] is True

    assert metrics["causal_ablation_changes_selection"] is True
    assert metrics["causal_restore_recovers"] is True
    assert metrics["causal_restart_persists"] is True
    assert metrics["causal_interventions_non_evidential"] is True

