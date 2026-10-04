from experiments.process_level_resonant_self_tuning_generalization_v1 import run


def test_process_level_generalization():
    result = run()
    metrics = result["metrics"]
    assert all(metrics.values())
    assert result["marginals"]["gap"] < 0.005
    assert result["stats"]["alpha"][2] > 0.99
    assert result["stats"]["beta"][2] > 0.99
