from experiments.unlabeled_temporal_ontology_benchmark_v1 import run


def test_unlabeled_temporal_ontology_discovers_hidden_regimes():
    result = run()
    metrics = result["metrics"]

    assert metrics["unlabeled_runtime_input"] is True
    assert metrics["no_process_labels_provided_to_ontology"] is True
    assert metrics["hidden_process_changes"] is True
    assert metrics["matched_stationary_marginal_family"] is True

    assert metrics["all_changes_detected"] is True
    assert metrics["no_false_switches"] is True
    assert metrics["max_detection_delay_below_12"] is True
    assert metrics["mean_regime_accuracy_above_0_90"] is True
    assert metrics["attention_broadens_during_transition"] is True
    assert metrics["empirical_marginal_gap_below_0_10"] is True

    assert result["interpretation"]["pass"] is True
