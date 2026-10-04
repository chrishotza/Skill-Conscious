from __future__ import annotations

from pathlib import Path

import runpy


def test_operational_continuity_benchmark_demonstrates_reentry_causality(tmp_path: Path):
    module = runpy.run_path(str(Path(__file__).parents[1] / 'experiments' / 'operational_continuity_benchmark.py'))
    result = module['run']()
    metrics = result["metrics"]

    assert metrics["baseline_wake"] == "alpha_path"
    assert metrics["dream_replay"] == "beta_path"
    assert metrics["post_reentry_continuity"] == "beta_path"
    assert metrics["matched_control"] == "alpha_path"
    assert metrics["causal_reentry_divergence"] is True
    assert metrics["replay_persisted_across_restart"] is True
    assert metrics["replay_profile_cannot_be_forged_by_control"] is True