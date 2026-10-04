from experiments.conscious_field_runtime_causal_attack_v1 import run


def test_conscious_field_runtime_causal_attack():
    result = run()
    assert result["protocol"]["no_report"] is True
    assert result["interpretation"]["pass"] is True
    assert all(result["metrics"].values())
