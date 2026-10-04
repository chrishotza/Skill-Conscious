from experiments.self_organizing_temporal_ontology_benchmark_v1 import run


def test_self_organizing_temporal_ontology():
    result = run()
    metrics = result["metrics"]

    assert metrics["starts_without_process_labels"] is True
    assert metrics["starts_without_process_specific_prototypes"] is True
    assert metrics["prototypes_are_experience_formed"] is True
    assert metrics["all_changes_detected"] is True
    assert metrics["mean_accuracy_above_0_90"] is True
    assert metrics["mean_false_remaps_below_0_10"] is True
    assert metrics["mean_attention_broadening_above_0_20"] is True
    assert metrics["prototype_count_remains_compact"] is True
    assert metrics["mean_max_delay_below_13"] is True
    assert result["interpretation"]["pass"] is True
