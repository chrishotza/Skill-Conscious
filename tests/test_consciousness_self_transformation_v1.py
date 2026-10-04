from experiments.consciousness_self_transformation_v1 import run_benchmark


def test_self_transformation_causal_gate():
    summary = run_benchmark(seeds=6)
    assert summary["all_pass"] is True
    assert summary["history_sensitive_rate"] == 1.0
    assert summary["internal_transformation_rate"] == 1.0
    assert summary["objective_score_match_rate"] == 1.0
    assert summary["ablation_collapse_rate"] == 1.0
    assert summary["restoration_rate"] == 1.0
    assert summary["restart_persistence_rate"] == 1.0
    assert summary["control_recovery_rate"] == 1.0
    assert summary["unity_effect_rate"] == 1.0
    assert summary["strength_effect_rate"] == 1.0
