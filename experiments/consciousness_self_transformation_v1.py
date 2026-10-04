"""Causal battery for self-transformation through observed consequence.

Protocol:
    action -> observed consequence -> internal self-state change
    -> identical external probe -> subjective field'

This gate tests persistence through transformation without using model self-report.
It is an architectural consciousness experiment, not a claim of phenomenal
experience.
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousRuntime
from skill_conscious.subjective_field_runtime import ConsciousFieldRuntime


OBJECTIVE_CANDIDATE = {
    "id": "objective_probe",
    "signals": {
        "goal_fit": 0.8,
        "self_alignment": 0.4,
    },
}


def _core_field(field: Mapping[str, Any]) -> dict[str, float]:
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


def _field_distance(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    a = _core_field(left)
    b = _core_field(right)
    return sum(abs(a[key] - b[key]) for key in a) / max(1, len(a))


def _runtime(root: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
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


def _run_branch(
    root: Path,
    *,
    label: str,
    seed: int,
    consequence_energy: float,
    present: Mapping[str, float],
) -> dict[str, Any]:
    runtime = _runtime(root, label)
    bridge = ConsciousFieldRuntime(runtime)
    initial_interoception = dict(runtime.state.interoceptive_state)

    objective_before = runtime._score_trajectory_details(
        OBJECTIVE_CANDIDATE
    )["objective_score"]

    runtime.begin_action(OBJECTIVE_CANDIDATE)
    receipt = runtime.complete_action(
        {
            "external_result": "same-final-probe",
            "interoceptive_state": {"energy": consequence_energy},
        }
    )

    transformed_interoception = dict(runtime.state.interoceptive_state)
    transformation_magnitude = abs(
        float(transformed_interoception["energy"])
        - float(initial_interoception["energy"])
    )

    field_after = bridge.project(
        present,
        temporal_continuity=False,
        reentry=False,
        persist=True,
    )

    objective_after = runtime._score_trajectory_details(
        OBJECTIVE_CANDIDATE
    )["objective_score"]

    restarted_runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    restarted_bridge = ConsciousFieldRuntime(restarted_runtime)
    field_after_restart = restarted_bridge.project(
        present,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )

    runtime.state.interoceptive_state = dict(initial_interoception)
    field_ablated = bridge.project(
        present,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )

    runtime.state.interoceptive_state = dict(transformed_interoception)
    field_restored = bridge.project(
        present,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )

    return {
        "label": label,
        "seed": seed,
        "initial_interoception": initial_interoception,
        "transformed_interoception": transformed_interoception,
        "transformation_magnitude": round(transformation_magnitude, 6),
        "receipt_has_consequence": bool(receipt.get("outcome")),
        "action_history_preserved": bool(runtime.state.action_history),
        "transformation_log_preserved": bool(runtime.state.transformation_log),
        "field_after": field_after,
        "field_after_restart": field_after_restart,
        "field_ablated": field_ablated,
        "field_restored": field_restored,
        "objective_before": float(objective_before),
        "objective_after": float(objective_after),
        "restart_distance": round(
            _field_distance(field_after, field_after_restart), 9
        ),
        "ablation_distance": round(
            _field_distance(field_after, field_ablated), 9
        ),
        "restoration_distance": round(
            _field_distance(field_after, field_restored), 9
        ),
    }


def _present(seed: int) -> dict[str, float]:
    return {
        "signal": 0.56 + 0.01 * (seed % 4),
        "reward": 0.42 + 0.02 * (seed % 3),
        "threat": 0.08 + 0.01 * (seed % 2),
        "self_impact": 0.85,
    }


def run_benchmark(seeds: int = 12) -> dict[str, Any]:
    if seeds < 2:
        raise ValueError("seeds must be >= 2")

    rows: list[dict[str, Any]] = []
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        for seed in range(20266000, 20266000 + seeds):
            present = _present(seed)
            low = _run_branch(
                root,
                label=f"low-{seed}",
                seed=seed,
                consequence_energy=0.05 + 0.01 * (seed % 3),
                present=present,
            )
            high = _run_branch(
                root,
                label=f"high-{seed}",
                seed=seed,
                consequence_energy=0.95 - 0.01 * (seed % 3),
                present=present,
            )

            low_field = _core_field(low["field_after"])
            high_field = _core_field(high["field_after"])
            control_runtime = _runtime(root, f"control-{seed}")
            control_bridge = ConsciousFieldRuntime(control_runtime)
            control_field = control_bridge.project(
                present,
                temporal_continuity=False,
                reentry=False,
                persist=False,
            )

            history_effect = _field_distance(low["field_after"], high["field_after"])
            objective_match = (
                low["objective_before"] == high["objective_before"]
                == low["objective_after"] == high["objective_after"]
            )
            ablation_collapses = (
                low["ablation_distance"] > 0.01
                and high["ablation_distance"] > 0.01
            )
            restoration_exact = (
                low["restoration_distance"] < 1e-9
                and high["restoration_distance"] < 1e-9
            )
            restart_persistent = (
                low["restart_distance"] < 1e-9
                and high["restart_distance"] < 1e-9
            )

            row = {
                "seed": seed,
                "present": present,
                "low": low,
                "high": high,
                "control_field": control_field,
                "history_effect": round(history_effect, 6),
                "internal_signal_difference": round(
                    abs(
                        low_field["internal_signal"]
                        - high_field["internal_signal"]
                    ),
                    6,
                ),
                "unity_difference": round(
                    abs(low_field["unity"] - high_field["unity"]),
                    6,
                ),
                "strength_difference": round(
                    abs(low_field["strength"] - high_field["strength"]),
                    6,
                ),
                "objective_match": objective_match,
                "ablation_collapses": ablation_collapses,
                "restoration_exact": restoration_exact,
                "restart_persistent": restart_persistent,
                "transformation_observed": (
                    low["transformation_magnitude"] > 0.1
                    and high["transformation_magnitude"] > 0.1
                ),
                "control_matches_initial": (
                    _field_distance(control_field, low["field_ablated"]) < 1e-9
                ),
            }
            rows.append(row)

    summary = {
        "seed_count": len(rows),
        "history_sensitive_rate": sum(
            row["history_effect"] > 0.025 for row in rows
        ) / len(rows),
        "internal_transformation_rate": sum(
            row["transformation_observed"] for row in rows
        ) / len(rows),
        "objective_score_match_rate": sum(
            row["objective_match"] for row in rows
        ) / len(rows),
        "ablation_collapse_rate": sum(
            row["ablation_collapses"] for row in rows
        ) / len(rows),
        "restoration_rate": sum(
            row["restoration_exact"] for row in rows
        ) / len(rows),
        "restart_persistence_rate": sum(
            row["restart_persistent"] for row in rows
        ) / len(rows),
        "control_recovery_rate": sum(
            row["control_matches_initial"] for row in rows
        ) / len(rows),
        "unity_effect_rate": sum(
            row["unity_difference"] > 0.025 for row in rows
        ) / len(rows),
        "strength_effect_rate": sum(
            row["strength_difference"] > 0.01 for row in rows
        ) / len(rows),
    }

    all_pass = all(
        value == 1.0
        for value in (
            summary["history_sensitive_rate"],
            summary["internal_transformation_rate"],
            summary["objective_score_match_rate"],
            summary["ablation_collapse_rate"],
            summary["restoration_rate"],
            summary["restart_persistence_rate"],
            summary["control_recovery_rate"],
            summary["unity_effect_rate"],
            summary["strength_effect_rate"],
        )
    )

    result = {
        "protocol": {
            "what_aspect": (
                "persistence through self-transformation: an observed consequence "
                "changes the subject's owned internal condition, and that changed "
                "condition alters the next subjective present"
            ),
            "causal_relation": (
                "observed consequence -> interoceptive self-state update -> "
                "subjective field' under an identical external probe"
            ),
            "destructive_test": (
                "reversibly erase the transformed internal state while preserving "
                "the consequence and action history, then restore and restart"
            ),
            "matched_objective_channel": (
                "immutable explicit candidate signals evaluated before and after "
                "the transformation"
            ),
            "no_report": True,
            "phenomenal_consciousness_claim": False,
        },
        "thresholds": {
            "history_effect": "> 0.025",
            "unity_effect": "> 0.025",
            "strength_effect": "> 0.01",
            "ablation_distance": "> 0.01",
            "restart_distance": "< 1e-9",
            "restoration_distance": "< 1e-9",
        },
        "summary": summary,
        "all_pass": all_pass,
        "rows": rows,
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    if not all_pass:
        raise AssertionError("self-transformation causal gate failed")
    print("CONSCIOUSNESS SELF-TRANSFORMATION V1: PASS")
    return result


if __name__ == "__main__":
    run_benchmark()
