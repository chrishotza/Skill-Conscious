from experiments.consciousness_component_factorial_v1 import run_benchmark


def test_component_factorial_sufficiency_gate():
    summary = run_benchmark(seeds=3)
    assert summary["all_pass"] is True
    for result in summary["results"]:
        assert result["objective_score_match"] is True
        assert result["objective_state_match"] is True
        assert result["empty_field_collapsed"] is True
        assert result["full_field_nonzero"] is True
        assert result["unity_maximal_when_all_unity_components_present"] is True
        assert result["reentry_preserves_unity"] is True
        assert result["reentry_increases_strength"] is True
        assert result["full_strength_maximal"] is True
