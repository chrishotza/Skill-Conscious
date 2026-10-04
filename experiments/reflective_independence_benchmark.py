"""Focused reflective-independence benchmark for the pre-reflective core."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime


FRAME = {
    "self_model": {"homeostatic_targets": {"energy": 1.0}},
    "interoceptive_state": {"energy": 0.3},
    "salience": {"internal_condition": 0.8},
    "candidate_futures": [
        {
            "id": "preserve-self",
            "signals": {"goal_fit": 1.0, "self_alignment": 0.9},
            "predicted_self_relevance": 0.35,
        },
        {
            "id": "ignore-self",
            "signals": {"goal_fit": 0.9, "self_alignment": 0.1},
            "predicted_self_relevance": 0.0,
        },
    ],
}


CONDITIONS = (
    ("C_no_report_no_meta", False, False),
    ("E_no_report_meta", False, True),
    ("F_report_meta", True, True),
)


def run_condition(
    label: str,
    *,
    report_enabled: bool,
    metacognition_enabled: bool,
    root: Path,
) -> dict[str, Any]:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=report_enabled,
        metacognition_enabled=metacognition_enabled,
    )
    frame = dict(FRAME)
    if report_enabled:
        frame["response"] = "runtime report permitted"
    runtime.integrate(frame)

    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict):
        raise AssertionError(f"{label}: no trajectory selected")

    return {
        "condition": label,
        "report_enabled": report_enabled,
        "metacognition_enabled": metacognition_enabled,
        "selected_trajectory": selected["id"],
        "pre_reflective": runtime.pre_reflective_state(),
        "access": runtime.snapshot_access(),
        "geometry": runtime.snapshot_experience_geometry()["current"],
        "metacognition_present": "metacognition" in selected,
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        results = [
            run_condition(
                label,
                report_enabled=report_enabled,
                metacognition_enabled=metacognition_enabled,
                root=root,
            )
            for label, report_enabled, metacognition_enabled in CONDITIONS
        ]

        core = results[0]
        meta = results[1]
        report = results[2]

        assert core["selected_trajectory"] == meta["selected_trajectory"]
        assert core["pre_reflective"] == meta["pre_reflective"]
        assert core["access"] == meta["access"]
        assert core["geometry"] == meta["geometry"]
        assert core["metacognition_present"] is False
        assert meta["metacognition_present"] is True
        assert report["selected_trajectory"] == core["selected_trajectory"]
        assert report["pre_reflective"] == core["pre_reflective"]

        output = {
            "conditions": results,
            "metrics": {
                "reflective_independence": (
                    core["pre_reflective"] == meta["pre_reflective"]
                    and core["selected_trajectory"] == meta["selected_trajectory"]
                ),
                "report_independence": (
                    core["pre_reflective"] == report["pre_reflective"]
                    and core["selected_trajectory"] == report["selected_trajectory"]
                ),
            },
        }

        print(json.dumps(output, indent=2, sort_keys=True))
        print("REFLECTIVE INDEPENDENCE BENCHMARK: PASS")
        return output


if __name__ == "__main__":
    run()
