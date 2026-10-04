from experiments.temporal_recurrence_causal_benchmark import run


def test_temporal_recurrence_is_causally_reversible():
    result = run()
    metrics = result["metrics"]

    assert metrics["same_information_multiset"] is True
    assert metrics["same_final_self_state"] is True
    assert metrics["same_runtime_budget"] is True
    assert metrics["same_candidate_field_hash"] is True
    assert metrics["structured_recurrence_detected"] is True
    assert metrics["control_recurrence_absent"] is True
    assert metrics["structured_selected_alpha"] is True
    assert metrics["control_selected_beta"] is True
    assert metrics["temporal_arrangement_changes_selection"] is True
    assert metrics["structured_alpha_score_exceeds_beta"] is True
    assert metrics["ablation_returns_to_control"] is True
    assert metrics["restoration_recovers_structured"] is True
    assert metrics["restart_persists_structured_selection"] is True
    assert metrics["restart_restores_profile_exactly"] is True
    assert metrics["intervention_non_evidential"] is True
    assert metrics["intervention_preserves_revision_history_memory"] is True
    assert metrics["profile_evidence_counts_restored"] is True
    assert result["interpretation"]["phenomenal_consciousness_claim"] is False
