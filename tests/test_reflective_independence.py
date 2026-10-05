from __future__ import annotations

from pathlib import Path

from experiments.reflective_independence_benchmark import run_condition


def test_reflective_layers_do_not_change_pre_reflective_core(tmp_path: Path):
    core = run_condition(
        "core",
        report_enabled=False,
        metacognition_enabled=False,
        root=tmp_path,
    )
    meta = run_condition(
        "meta",
        report_enabled=False,
        metacognition_enabled=True,
        root=tmp_path,
    )
    report = run_condition(
        "report",
        report_enabled=True,
        metacognition_enabled=True,
        root=tmp_path,
    )

    assert core["selected_trajectory"] == meta["selected_trajectory"]
    assert core["pre_reflective"] == meta["pre_reflective"]
    assert core["access"] == meta["access"]
    assert core["geometry"] == meta["geometry"]
    assert core["metacognition_present"] is False
    assert meta["metacognition_present"] is True
    assert report["selected_trajectory"] == core["selected_trajectory"]
    assert report["pre_reflective"] == core["pre_reflective"]
