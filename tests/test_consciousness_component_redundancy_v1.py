from experiments.consciousness_component_redundancy_v1 import run_benchmark


def test_component_redundancy_kill_gate():
    summary = run_benchmark(seeds=3)
    assert summary["all_pass"] is True
    assert summary["no_substitution_pairs"] is True
    assert summary["nontrivial_kill_control_pass"] is True
    for result in summary["results"]:
        assert result["objective_scores_match"] is True
        assert result["objective_processing_match"] is True
        assert result["target_remains_absent"] is True
        assert result["baseline_function"] is True
        assert result["substitution_recovers_function"] is False
