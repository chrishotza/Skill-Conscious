from experiments.subjective_field_causal_battery import run


def test_subjective_field_causal_battery():
    result = run()
    assert result["protocol"]["no_report_measurement"] is True
    assert result["interpretation"]["pass"] is True
    assert all(result["metrics"].values())
