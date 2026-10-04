from __future__ import annotations

from pathlib import Path

import runpy


def test_replay_trace_ablation_changes_and_restores_wake_selection(tmp_path: Path):
    module = runpy.run_path(
        str(
            Path(__file__).parents[1]
            / "experiments"
            / "operational_replay_trace_causal_ablation.py"
        )
    )
    result = module["run"]()
    metrics = result["metrics"]

    assert metrics["replay_phase"] == ["beta_path"] * 4
    assert metrics["intact_reentry"] == "beta_path"
    assert metrics["ablated_reentry"] == "alpha_path"
    assert metrics["restored_reentry"] == "beta_path"
    assert metrics["replay_profile_persisted"] is True
    assert metrics["intervention_changed_selection"] is True
    assert metrics["restoration_recovered_selection"] is True
    assert metrics["intervention_added_evidence"] is False
    assert metrics["restore_added_evidence"] is False
