"""Deterministic probe connecting bounded access to experience geometry."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime


CANDIDATES = [
    {
        "id": "self_model_path",
        "signals": {"goal_fit": 1.5},
        "access_keys": ["self_model"],
    },
    {
        "id": "interoceptive_path",
        "signals": {"goal_fit": 1.0},
        "access_keys": ["interoceptive_state"],
    },
]


def run_condition(
    label: str,
    *,
    capacity: int,
    report_enabled: bool,
    metacognition_enabled: bool,
    root: Path,
) -> dict[str, Any]:
    runtime = ConsciousRuntime(
        identity=label,
        state_path=root / f"{label}.json",
        report_enabled=report_enabled,
        metacognition_enabled=metacognition_enabled,
    )
    runtime.set_access_capacity(capacity)
    runtime.integrate(
        {
            "response": "controlled geometry probe" if report_enabled else "",
            "self_model": {"persistent_goal": "preserve-process"},
            "interoceptive_state": {"energy": 0.3},
            "candidate_futures": CANDIDATES,
        }
    )

    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict):
        raise AssertionError(f"{label}: no trajectory selected")

    geometry = runtime.snapshot_experience_geometry()
    access = runtime.snapshot_access()

    return {
        "condition": label,
        "capacity": capacity,
        "report_enabled": report_enabled,
        "metacognition_enabled": metacognition_enabled,
        "selected_trajectory": selected["id"],
        "access": access,
        "geometry": geometry["current"],
        "geometry_history_length": len(geometry["history"]),
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)

        narrow_a = run_condition(
            "narrow_a",
            capacity=2,
            report_enabled=False,
            metacognition_enabled=False,
            root=root,
        )
        wide_b = run_condition(
            "wide_b",
            capacity=6,
            report_enabled=False,
            metacognition_enabled=False,
            root=root,
        )
        narrow_c = run_condition(
            "narrow_c",
            capacity=2,
            report_enabled=False,
            metacognition_enabled=False,
            root=root,
        )
        report_d = run_condition(
            "report_d",
            capacity=2,
            report_enabled=True,
            metacognition_enabled=True,
            root=root,
        )

        assert narrow_a["selected_trajectory"] == "interoceptive_path"
        assert wide_b["selected_trajectory"] == "self_model_path"
        assert narrow_c["selected_trajectory"] == narrow_a["selected_trajectory"]
        assert narrow_a["access"]["capacity"] == narrow_c["access"]["capacity"] == 2
        assert (
            narrow_a["geometry"]["features"]["access_compression"]
            == narrow_c["geometry"]["features"]["access_compression"]
        )
        assert (
            narrow_a["geometry"]["features"]["access_compression"]
            != wide_b["geometry"]["features"]["access_compression"]
        )
        assert report_d["selected_trajectory"] == narrow_a["selected_trajectory"]

        report = {
            "conditions": [narrow_a, wide_b, narrow_c, report_d],
            "metrics": {
                "trajectory_restoration": (
                    narrow_a["selected_trajectory"]
                    == narrow_c["selected_trajectory"]
                ),
                "bandwidth_changed_selection": (
                    narrow_a["selected_trajectory"]
                    != wide_b["selected_trajectory"]
                ),
                "report_independent_selection": (
                    narrow_a["selected_trajectory"]
                    == report_d["selected_trajectory"]
                ),
            },
        }

        print(json.dumps(report, indent=2, sort_keys=True))
        print("EXPERIENCE GEOMETRY / BANDWIDTH PROBE: PASS")
        return report


if __name__ == "__main__":
    run()
