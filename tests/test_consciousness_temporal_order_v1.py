from experiments.consciousness_temporal_order_v1 import run_benchmark


def test_temporal_order_causal_gate():
    summary = run_benchmark(seeds=6)
    assert summary["all_pass"] is True
    assert summary["history_sensitive_rate"] == 1.0
    assert summary["ablation_collapse_rate"] == 1.0
    assert summary["objective_score_match_rate"] == 1.0
