from experiments.consciousness_action_relevance_v1 import run_benchmark


def test_action_relevance_causal_gate():
    result = run_benchmark(seeds=6)
    summary = result["summary"]
    assert result["all_pass"] is True
    assert summary["seed_count"] == 6
    assert summary["action_divergence_rate"] == 1.0
    assert summary["same_probe_rate"] == 1.0
    assert summary["ablation_restoration_rate"] == 1.0
    assert summary["restart_persistence_rate"] == 1.0
    assert summary["objective_control_rate"] == 1.0
    assert summary["field_difference_rate"] == 1.0
