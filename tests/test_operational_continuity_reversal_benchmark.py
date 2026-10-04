
from __future__ import annotations

from pathlib import Path

import runpy


def test_operational_continuity_is_history_dependent_and_reversible(tmp_path: Path):
    module = runpy.run_path(
        str(
            Path(__file__).parents[1]
            / "experiments"
            / "operational_continuity_reversal_benchmark.py"
        )
    )
    result = module["run"]()
    metrics = result["metrics"]

    assert metrics["baseline_wake"] == "alpha_path"
    assert metrics["first_reentry_after_beta_history"] == "beta_path"
    assert metrics["counter_replay"] == "alpha_path"
    assert metrics["final_reentry_after_alpha_history"] == "alpha_path"
    assert metrics["matched_control"] == "alpha_path"
    assert metrics["history_dependent_reversal"] is True
    assert metrics["replay_state_survives_two_restarts"] is True
    assert metrics["counter_history_changes_internal_trace"] is True
    assert metrics["external_outcome_evidence_used"] is False
