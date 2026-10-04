from experiments.double_dissociation_sequence_controller_v1 import run


def test_resonant_vs_generic_double_dissociation():
    result = run()
    metrics = result["metrics"]

    assert metrics["baseline_agreement"] is True
    assert metrics["resonant_perturbation_changes_resonant"] is True
    assert metrics["resonant_perturbation_spares_generic"] is True
    assert metrics["generic_perturbation_changes_generic"] is True
    assert metrics["generic_perturbation_spares_resonant"] is True
    assert metrics["resonant_restoration_recovers"] is True
    assert metrics["generic_restoration_recovers"] is True
    assert result["interpretation"]["double_dissociation"] is True
