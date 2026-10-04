"""Unified causal benchmark for pre-reflective, access, geometry and no-report layers."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime


CANDIDATES = [
    {
        "id": "self_model_path",
        "signals": {
            "goal_fit": 1.5,
            "self_alignment": 0.8,
            "continuity": 0.7,
        },
        "access_keys": ["self_model"],
        "predicted_self_relevance": 0.35,
    },
    {
        "id": "interoceptive_path",
        "signals": {
            "goal_fit": 1.0,
            "self_alignment": 0.6,
            "continuity": 0.8,
        },
        "access_keys": ["interoceptive_state"],
        "predicted_self_relevance": 0.0,
    },
]


CONDITIONS = (
    ("B_persistent", False, False, False),
    ("C_pre_reflective", False, False, True),
    ("D_self_model", False, False, True),
    ("E_no_report_meta", False, True, True),
    ("F_report_meta", True, True, True),
)


def _make_runtime(
    label: str,
    *,
    report_enabled: bool,
    metacognition_enabled: bool,
    pre_reflective_enabled: bool,
    path: Path,
) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=path,
        report_enabled=report_enabled,
        metacognition_enabled=metacognition_enabled,
    )
    if pre_reflective_enabled:
        runtime.state.self_model = {
            "homeostatic_targets": {"energy": 1.0},
        }
        runtime.state.interoceptive_state = {"energy": 0.3}
    return runtime


def _frame(runtime: ConsciousRuntime, *, response: bool) -> dict[str, Any]:
    frame: dict[str, Any] = {
        "self_state": {"stability": 0.5, "focus": 0.5},
        "candidate_futures": [dict(item) for item in CANDIDATES],
    }
    if runtime.state.self_model:
        frame["self_model"] = dict(runtime.state.self_model)
        frame["interoceptive_state"] = dict(runtime.state.interoceptive_state)
        frame["salience"] = {"internal_condition": 0.9}
    if response:
        frame["response"] = "controlled benchmark frame"
    return frame


def _cycle(
    runtime: ConsciousRuntime,
    *,
    response: bool,
) -> dict[str, Any]:
    runtime.integrate(_frame(runtime, response=response))
    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict):
        raise AssertionError("benchmark cycle produced no selected trajectory")

    trajectory_id = str(selected["id"])
    runtime.begin_action(selected, persist=False)
    outcome = {
        "status": "success",
        "interoceptive_state": {
            "energy": 0.8 if trajectory_id == "self_model_path" else 0.6,
        },
        "self_state": {
            "focus": 0.8 if trajectory_id == "self_model_path" else 0.6,
        },
        "trajectory": trajectory_id,
    }
    runtime.complete_action(outcome, persist=False)

    return {
        "trajectory": trajectory_id,
        "pre_reflective": runtime.pre_reflective_state(),
        "access": runtime.snapshot_access(),
        "geometry": runtime.snapshot_experience_geometry()["current"],
        "geometry_history_length": len(runtime.snapshot_experience_geometry()["history"]),
        "action_history_length": len(runtime.state.action_history),
        "outcome": outcome,
        "metacognition": "metacognition" in selected,
    }


def _causal_probe(runtime: ConsciousRuntime, *, response: bool) -> dict[str, Any]:
    runtime.set_access_capacity(2)
    narrow = _cycle(runtime, response=response)

    runtime.set_access_capacity(6)
    wide = _cycle(runtime, response=response)

    runtime.set_access_capacity(2)
    restored = _cycle(runtime, response=response)

    return {
        "narrow": narrow,
        "wide": wide,
        "restored": restored,
        "divergence": narrow["trajectory"] != wide["trajectory"],
        "reversal": narrow["trajectory"] == restored["trajectory"],
    }


def run_condition(
    label: str,
    *,
    report_enabled: bool,
    metacognition_enabled: bool,
    pre_reflective_enabled: bool,
    root: Path,
) -> dict[str, Any]:
    runtime = _make_runtime(
        label,
        report_enabled=report_enabled,
        metacognition_enabled=metacognition_enabled,
        pre_reflective_enabled=pre_reflective_enabled,
        path=root / f"{label}.json",
    )

    baseline = _cycle(runtime, response=report_enabled)
    probe = _causal_probe(runtime, response=report_enabled)

    runtime_before_restart = runtime.snapshot()
    restarted = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=report_enabled,
        metacognition_enabled=metacognition_enabled,
    )
    restart_equivalent = restarted.snapshot_access() == runtime.snapshot_access()

    return {
        "condition": label,
        "report_enabled": report_enabled,
        "metacognition_enabled": metacognition_enabled,
        "pre_reflective_enabled": pre_reflective_enabled,
        "baseline": baseline,
        "probe": probe,
        "restart_equivalent": restart_equivalent,
        "revision_before_restart": runtime_before_restart["revision"],
        "revision_after_restart": restarted.state.revision,
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        results = []
        for label, report_enabled, metacognition_enabled, pre_reflective_enabled in CONDITIONS:
            results.append(
                run_condition(
                    label,
                    report_enabled=report_enabled,
                    metacognition_enabled=metacognition_enabled,
                    pre_reflective_enabled=pre_reflective_enabled,
                    root=root,
                )
            )

        no_report = next(
            item for item in results if item["condition"] == "E_no_report_meta"
        )
        report = next(
            item for item in results if item["condition"] == "F_report_meta"
        )
        core = next(
            item for item in results if item["condition"] == "C_pre_reflective"
        )

        assert core["probe"]["divergence"] is True
        assert core["probe"]["reversal"] is True
        assert no_report["probe"]["narrow"]["metacognition"] is True
        assert no_report["probe"]["narrow"]["trajectory"] == report["probe"]["narrow"]["trajectory"]
        assert no_report["probe"]["narrow"]["pre_reflective"] == report["probe"]["narrow"]["pre_reflective"]
        assert all(item["restart_equivalent"] for item in results)
        assert all(
            item["probe"]["restored"]["action_history_length"]
            >= item["probe"]["narrow"]["action_history_length"]
            for item in results
        )

        output = {
            "conditions": results,
            "metrics": {
                "bandwidth_causal_divergence": core["probe"]["divergence"],
                "bandwidth_reversal": core["probe"]["reversal"],
                "report_independence": (
                    no_report["probe"]["narrow"]["trajectory"]
                    == report["probe"]["narrow"]["trajectory"]
                ),
                "geometry_present": all(
                    "features" in item["baseline"]["geometry"]
                    for item in results
                ),
                "restart_persistence": all(
                    item["restart_equivalent"] for item in results
                ),
            },
        }

        print(json.dumps(output, indent=2, sort_keys=True))
        print("UNIFIED CAUSAL BENCHMARK v1: PASS")
        return output


if __name__ == "__main__":
    run()
