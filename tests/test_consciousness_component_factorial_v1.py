from experiments.consciousness_component_factorial_v1 import run_benchmark


def test_component_factorial_sufficiency_gate():
    summary = run_benchmark(seeds=3)
    assert summary["all_pass"] is True
    for result in summary["results"]:
        assert result["objective_score_match"] is True
        assert result["objective_state_match"] is True
        assert result["empty_field_collapsed"] is True
        assert result["full_field_nonzero"] is True
        assert result["full_dominates_subsets"] is True
