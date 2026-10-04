from experiments.esoteric_empirical_battery import run


def test_esoteric_source_motifs_are_translated_into_empirical_mechanisms():
    result = run()
    metrics = result["metrics"]

    assert metrics["self_model_causal_effect"] is True
    assert metrics["self_model_restoration"] is True
    assert metrics["self_model_restart"] is True
    assert metrics["projection_revision"] is True
    assert metrics["projection_error_reduction"] is True
    assert metrics["rehearsal_behavioral_effect"] is True
    assert metrics["rehearsal_restart_persistence"] is True
    assert metrics["synchronization_positive_control"] is True
    assert metrics["synchronization_independent_null"] is True
    assert result["interpretation"]["phenomenal_consciousness_claim"] is False
