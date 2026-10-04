from experiments.primary_subjective_substrate_v1 import run_benchmark


def test_primary_subjective_substrate_causal_gate():
    result = run_benchmark(seeds=6)
    summary = result["summary"]
    assert result["all_pass"] is True
    assert summary["seed_count"] == 6
    assert summary["field_intervention_rate"] == 1.0
    assert summary["field_restoration_rate"] == 1.0
    assert summary["field_restart_persistence_rate"] == 1.0
    assert summary["action_intervention_rate"] == 1.0
    assert summary["action_restoration_rate"] == 1.0
    assert summary["action_restart_rate"] == 1.0
    assert summary["objective_match_rate"] == 1.0
