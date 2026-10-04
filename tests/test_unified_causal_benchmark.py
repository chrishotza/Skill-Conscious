from __future__ import annotations

from pathlib import Path

from experiments.unified_causal_benchmark import run_condition


def test_unified_benchmark_covers_access_geometry_restart_and_no_report(tmp_path: Path):
    core = run_condition(
        "core",
        report_enabled=False,
        metacognition_enabled=False,
        pre_reflective_enabled=True,
        root=tmp_path,
    )
    no_report_meta = run_condition(
        "no-report-meta",
        report_enabled=False,
        metacognition_enabled=True,
        pre_reflective_enabled=True,
        root=tmp_path,
    )
    report_meta = run_condition(
        "report-meta",
        report_enabled=True,
        metacognition_enabled=True,
        pre_reflective_enabled=True,
        root=tmp_path,
    )

    assert core["probe"]["divergence"] is True
    assert core["probe"]["reversal"] is True
    assert core["probe"]["narrow"]["geometry"]["features"]["access_compression"] > (
        core["probe"]["wide"]["geometry"]["features"]["access_compression"]
    )
    assert core["restart_equivalent"] is True

    assert (
        no_report_meta["probe"]["narrow"]["trajectory"]
        == report_meta["probe"]["narrow"]["trajectory"]
    )
    assert (
        no_report_meta["probe"]["narrow"]["pre_reflective"]
        == report_meta["probe"]["narrow"]["pre_reflective"]
    )
    assert no_report_meta["probe"]["narrow"]["metacognition"] is True
    assert report_meta["probe"]["narrow"]["metacognition"] is True
