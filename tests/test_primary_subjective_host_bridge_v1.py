from experiments.primary_subjective_host_bridge_v1 import run_benchmark


def test_primary_subjective_host_bridge_causal_gate():
    result = run_benchmark()
    assert result["all_pass"] is True
    assert result["summary"]["same_initial_selection"] is True
    assert result["summary"]["intact_changes_next_selection"] is True
    assert result["summary"]["ablation_selects_explicit_control"] is True
    assert result["summary"]["causal_divergence"] is True
    assert result["summary"]["intact_restart_persistence"] is True
    assert result["summary"]["ablation_restart_persistence"] is True
    assert result["summary"]["consequence_prompt_visible"] is True
    assert result["summary"]["authoritative_outcome_present"] is True
    assert result["summary"]["objective_channel_equal"] is True
