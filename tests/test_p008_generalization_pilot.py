"""Pilot-only P008 generalization harness regression tests."""
import json
from pathlib import Path

import pytest

from experiments.p008_generalization_pilot import (
    CONDITION_NAMES, audit, generate_scenario, run_pilot,
)


def test_generator_determinism_and_holdout_guard():
    assert generate_scenario(9) == generate_scenario(9)
    assert generate_scenario(9) != generate_scenario(10)
    assert [item["id"] for item in generate_scenario(9)["candidates"]] == ["candidate_0", "candidate_1"]
    assert all(0 <= x <= 1 for row in generate_scenario(9)["candidates"] for x in row["signals"].values())
    for scenario_id in (-1, 32, 1000, 1127, True, "0"):
        with pytest.raises(ValueError, match="holdout|Pilot"):
            generate_scenario(scenario_id)


def test_pilot_all_four_arms_two_cycles_and_replay(tmp_path: Path):
    directory = tmp_path / "pilot"
    result = run_pilot(directory, count=3)
    assert result["holdout_accessed"] is False
    assert result["status"] == "EXPLORATORY_PILOT_NOT_CONFIRMATORY"
    assert result["scenarios"] == [0, 1, 2]
    assert len(result["files"]) == 15
    assert result == audit(directory)
    assert result["metrics"]["A_vs_B"]["mean"] == 0
    assert result["metrics"]["B_vs_D"]["mean"] == 0
    assert len(result["protocol_sha256"]) == 64
    assert len(result["generator_sha256"]) == 64
    rows = [
        json.loads((directory / "scenario-000" / (arm + ".json")).read_text())
        for arm in CONDITION_NAMES
    ]
    assert [row["condition"] for row in rows] == list(CONDITION_NAMES)
    assert all(row["restart_integrity"] for row in rows)
    assert all(len(row["selected_trajectory_each_cycle"]) == 2 for row in rows)
    with pytest.raises(FileExistsError):
        run_pilot(directory, count=3)


def test_raw_artifacts_detect_tampering(tmp_path: Path):
    directory = tmp_path / "pilot"
    run_pilot(directory, count=1)
    path = directory / "scenario-000" / (CONDITION_NAMES[0] + ".json")
    path.write_text(path.read_text() + " ", encoding="utf-8")
    with pytest.raises(ValueError, match="SHA-256"):
        audit(directory)


@pytest.mark.parametrize("count", [-1, 0, 33, True])
def test_no_invalid_pilot_counts(tmp_path, count):
    with pytest.raises(ValueError):
        run_pilot(tmp_path / "pilot", count=count)
