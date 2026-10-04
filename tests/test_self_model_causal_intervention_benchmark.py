from experiments.self_model_causal_intervention_benchmark import run


def test_self_model_is_reversible_causal_variable():
    result = run()
    metrics = result["metrics"]

    assert metrics["task_count"] == 5
    assert metrics["intervention_divergence_rate"] == 1.0
    assert metrics["restoration_rate"] == 1.0
    assert metrics["restart_persistence_rate"] == 1.0
    assert metrics["runtime_restore_consistency_rate"] == 1.0
    assert metrics["intervention_changed_rate"] == 1.0
    assert metrics["evidence_unchanged_rate"] == 1.0
    assert metrics["intervention_non_evidential"] is True
    assert metrics["restore_non_evidential"] is True
