"""Causal battery for action relevance of the transformed subjective field.

Protocol:
    consequence -> self-transformation -> subjective field' -> trajectory'

The objective channel is held constant by using identical explicit candidate
signals. Only the predicted subjective-field profile differs.
No model self-report or metacognition is used.
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousRuntime


BASE_SIGNALS = {
    "goal_fit": 0.8,
    "self_alignment": 0.4,
}


def _field_core(field: Mapping[str, Any]) -> dict[str, float]:
    return {
        key: float(field.get(key, 0.0))
        for key in (
            "world_signal",
            "internal_signal",
            "binding",
            "self_relevance",
            "valence",
            "unity",
            "strength",
        )
    }


def _distance(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    a = _field_core(left)
    b = _field_core(right)
    return sum(abs(a[key] - b[key]) for key in a) / len(a)


def _runtime(root: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
        subjective_field_enabled=True,
        subjective_field_weight=1.0,
    )
    runtime.state.self_state = {
        "energy": 0.5,
        "safety": 0.8,
        "goal": 0.7,
    }
    runtime.state.interoceptive_state = {"energy": 0.5}
    runtime.state.valence = 0.2
    runtime.state.salience = {"present": 1.0}
    runtime.state.attention = ["present"]
    runtime.store.save(runtime.state)
    return runtime


def _present(seed: int) -> dict[str, float]:
    return {
        "signal": 0.56 + 0.01 * (seed % 4),
        "reward": 0.42 + 0.02 * (seed % 3),
        "threat": 0.08 + 0.01 * (seed % 2),
        "self_impact": 0.85,
    }


def _consequence_energy(seed: int, high: bool) -> float:
    return (
        0.95 - 0.01 * (seed % 3)
        if high
        else 0.05 + 0.01 * (seed % 3)
    )


def _candidate_set(
    low_field: Mapping[str, Any],
    neutral_field: Mapping[str, Any],
    high_field: Mapping[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "id": "trajectory-low-field",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(low_field),
        },
        {
            "id": "trajectory-neutral-field",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(neutral_field),
        },
        {
            "id": "trajectory-high-field",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(high_field),
        },
    ]


def _project(runtime: ConsciousRuntime, present: Mapping[str, float]) -> dict[str, Any]:
    return runtime.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=runtime.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=True,
    )


def _reference_field(
    root: Path,
    *,
    label: str,
    present: Mapping[str, float],
    energy: float,
) -> dict[str, Any]:
    reference = _runtime(root, label)
    reference.state.interoceptive_state = {"energy": energy}
    reference.state.store = reference.store
    return _project(reference, present)


def _prepare_branch(
    root: Path,
    *,
    label: str,
    seed: int,
    consequence_energy: float,
    present: Mapping[str, float],
) -> dict[str, Any]:
    runtime = _runtime(root, label)

    runtime.begin_action(
        {
            "id": "observe-consequence",
            "signals": dict(BASE_SIGNALS),
        }
    )
    receipt = runtime.complete_action(
        {
            "external_result": "same-final-probe",
            "interoceptive_state": {"energy": consequence_energy},
        }
    )

    transformed_field = _project(runtime, present)

    low_reference = _runtime(root, f"{label}-low-reference")
    low_reference.state.interoceptive_state = {
        "energy": _consequence_energy(seed, False)
    }
    low_field = _project(low_reference, present)

    neutral_reference = _runtime(root, f"{label}-neutral-reference")
    neutral_field = _project(neutral_reference, present)

    high_reference = _runtime(root, f"{label}-high-reference")
    high_reference.state.interoceptive_state = {
        "energy": _consequence_energy(seed, True)
    }
    high_field = _project(high_reference, present)

    candidates = _candidate_set(low_field, neutral_field, high_field)

    objective_before = {
        item["id"]: runtime._score_trajectory_details(item)["objective_score"]
        for item in candidates
    }
    selected = runtime.select_trajectory(candidates)
    action_before_reset = str(selected["id"])

    transformed = float(runtime.state.interoceptive_state["energy"])

    runtime.state.interoceptive_state = {"energy": 0.5}
    ablated_field = _project(runtime, present)
    objective_after_ablation = {
        item["id"]: runtime._score_trajectory_details(item)["objective_score"]
        for item in candidates
    }
    ablated_selected = runtime.select_trajectory(candidates)

    runtime.state.interoceptive_state = {"energy": transformed}
    restored_field = _project(runtime, present)
    objective_after_restoration = {
        item["id"]: runtime._score_trajectory_details(item)["objective_score"]
        for item in candidates
    }
    restored_selected = runtime.select_trajectory(candidates)

    restarted = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
        subjective_field_enabled=True,
        subjective_field_weight=1.0,
    )
    restarted_field = _project(restarted, present)
    restarted_selected = restarted.select_trajectory(candidates)

    objective_unchanged = all(
        objective_before[item_id]
        == objective_after_ablation[item_id]
        == objective_after_restoration[item_id]
        for item_id in objective_before
    )

    return {
        "seed": seed,
        "label": label,
        "receipt_has_consequence": bool(receipt.get("outcome")),
        "transformed_energy": transformed,
        "transformed_field": transformed_field,
        "ablated_field": ablated_field,
        "restored_field": restored_field,
        "restarted_field": restarted_field,
        "action_before_reset": action_before_reset,
        "action_after_ablation": str(ablated_selected["id"]),
        "action_after_restoration": str(restored_selected["id"]),
        "action_after_restart": str(restarted_selected["id"]),
        "objective_before": objective_before,
        "objective_after_ablation": objective_after_ablation,
        "objective_after_restoration": objective_after_restoration,
        "candidate_objective_equal": (
            len(set(objective_before.values())) == 1
        ),
        "objective_unchanged": objective_unchanged,
    }


def run_benchmark(seeds: int = 12) -> dict[str, Any]:
    if seeds < 2:
        raise ValueError("seeds must be >= 2")

    rows: list[dict[str, Any]] = []
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        for seed in range(20267000, 20267000 + seeds):
            present = _present(seed)
            low = _prepare_branch(
                root,
                label=f"low-{seed}",
                seed=seed,
                consequence_energy=_consequence_energy(seed, False),
                present=present,
            )
            high = _prepare_branch(
                root,
                label=f"high-{seed}",
                seed=seed,
                consequence_energy=_consequence_energy(seed, True),
                present=present,
            )

            rows.append(
                {
                    "seed": seed,
                    "low": low,
                    "high": high,
                    "low_high_action_divergence": (
                        low["action_before_reset"]
                        != high["action_before_reset"]
                    ),
                    "same_external_probe": True,
                    "low_action_restores_after_reset": (
                        low["action_before_reset"] == "trajectory-low-field"
                        and low["action_after_ablation"]
                        == "trajectory-neutral-field"
                        and low["action_after_restoration"]
                        == low["action_before_reset"]
                    ),
                    "high_action_restores_after_reset": (
                        high["action_before_reset"] == "trajectory-high-field"
                        and high["action_after_ablation"]
                        == "trajectory-neutral-field"
                        and high["action_after_restoration"]
                        == high["action_before_reset"]
                    ),
                    "low_restart_persistence": (
                        low["action_after_restart"]
                        == low["action_before_reset"]
                    ),
                    "high_restart_persistence": (
                        high["action_after_restart"]
                        == high["action_before_reset"]
                    ),
                    "objective_control": (
                        low["candidate_objective_equal"]
                        and high["candidate_objective_equal"]
                        and low["objective_unchanged"]
                        and high["objective_unchanged"]
                    ),
                    "field_difference_low_high": round(
                        _distance(
                            low["transformed_field"],
                            high["transformed_field"],
                        ),
                        6,
                    ),
                }
            )

    summary = {
        "seed_count": len(rows),
        "action_divergence_rate": sum(
            row["low_high_action_divergence"] for row in rows
        ) / len(rows),
        "same_probe_rate": sum(
            row["same_external_probe"] for row in rows
        ) / len(rows),
        "ablation_restoration_rate": sum(
            row["low_action_restores_after_reset"]
            and row["high_action_restores_after_reset"]
            for row in rows
        ) / len(rows),
        "restart_persistence_rate": sum(
            row["low_restart_persistence"]
            and row["high_restart_persistence"]
            for row in rows
        ) / len(rows),
        "objective_control_rate": sum(
            row["objective_control"] for row in rows
        ) / len(rows),
        "field_difference_rate": sum(
            row["field_difference_low_high"] > 0.025 for row in rows
        ) / len(rows),
    }

    all_pass = all(
        value == 1.0
        for value in summary.values()
        if isinstance(value, float)
    )

    result = {
        "protocol": {
            "what_aspect": (
                "action relevance: the transformed subjective field constrains "
                "which trajectory is selected next"
            ),
            "causal_relation": (
                "observed consequence -> self-transformation -> subjective field' "
                "-> trajectory selection under matched explicit objective signals"
            ),
            "destructive_test": (
                "restore the pre-consequence self-state and require the neutral "
                "control trajectory; restore and restart must reproduce the transformed action"
            ),
            "no_report": True,
            "phenomenal_consciousness_claim": False,
        },
        "thresholds": {
            "field_difference": "> 0.025",
            "action_divergence": "1.0 across tested seeds",
            "objective_control": "1.0 across tested seeds",
            "reset_restoration": "1.0 across tested seeds",
            "restart_persistence": "1.0 across tested seeds",
        },
        "summary": summary,
        "all_pass": all_pass,
        "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all_pass:
        raise AssertionError("consciousness action-relevance gate failed")
    print("CONSCIOUSNESS ACTION RELEVANCE V1: PASS")
    return result


if __name__ == "__main__":
    run_benchmark()
