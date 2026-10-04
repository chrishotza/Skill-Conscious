from __future__ import annotations

from experiments.host_loop_causal_benchmark import run


def test_host_consequence_reentry_changes_next_trajectory():
    result = run()
    metrics = result["metrics"]

    assert metrics["same_initial_selection"] is True
    assert metrics["reentry_changes_next_selection"] is True
    assert metrics["ablation_preserves_initial_selection"] is True
    assert metrics["reentry_switches_trajectory"] is True
    assert metrics["intervention_added_evidence"] is False
    assert metrics["causal_state_diverged"] is True
    assert metrics["authoritative_outcome_present"] is True
