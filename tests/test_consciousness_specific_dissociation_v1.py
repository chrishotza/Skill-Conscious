from experiments.consciousness_specific_dissociation_v1 import run


def test_consciousness_specific_double_dissociation():
    result = run()
    assert result["protocol"]["no_report"] is True
    assert result["interpretation"]["pass"] is True
    assert result["aggregate"]["objective_processing_complete"] is True
    assert result["aggregate"]["subjective_specific_double_dissociation"] is True
