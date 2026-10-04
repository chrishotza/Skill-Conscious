from experiments.consciousness_runtime_dissociation_v1 import run_benchmark


def test_full_runtime_consciousness_dissociation():
    summary = run_benchmark(trials=12)

    assert summary["all_pass"] is True
    assert summary["dissociation_rate"] == 1.0
    assert summary["objective_score_match_rate"] == 1.0
    assert summary["objective_processing_match_rate"] == 1.0
    assert summary["temporal_reentry_rate"] == 1.0
    assert summary["restart_persistence_rate"] == 1.0
    assert summary["restoration_rate"] == 1.0
