from experiments.consciousness_component_ablation_v1 import run_benchmark


def test_subjective_field_component_ablation_gate():
    summary = run_benchmark(trials_per_component=6)

    assert summary["all_pass"] is True
    for component in summary["components"]:
        metrics = summary["summary"][component]
        assert metrics["collapse_rate"] == 1.0
        assert metrics["restore_rate"] == 1.0
        assert metrics["selection_dissociation_rate"] == 1.0
        assert metrics["objective_score_match_rate"] == 1.0
        assert metrics["objective_processing_match_rate"] == 1.0
