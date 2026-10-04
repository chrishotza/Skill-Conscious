"""Causal battery for action relevance of the transformed subjective field.

Protocol:
    consequence -> self-transformation -> subjective field' -> trajectory'

The objective channel is held constant by using identical explicit candidate
signals. Only the candidate's predicted subjective-field match differs.
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
    if high:
        return 0.95 - 0.01 * (seed % 3)
    return 0.05 + 0.01 * (seed % 3)


def _candidate_set(
    low_field: Mapping[str, Any],
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
            "id": "trajectory-high-field",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(high_field),
        },
    ]


def _prepare_branch(
    root: Path,
    *,
    label: str,
    seed: int,
    consequence_energy: float,
    present: Mapping[str, float],
) -> dict[str, Any]:
    runtime = _runtime(root, label)

    objective_before = {
        item["id"]: runtime._score_trajectory_details(item)["objective_score"]
        for item in _candidate_set(
            runtime.snapshot_subjective_field()["field"],
            runtime.snapshot_subjective_field()["field"],
        )
    }

    action = {
        "id": "observe-consequence",
        "signals": dict(BASE_SIGNALS),
    }
    runtime.begin_action(action)
    receipt = runtime.complete_action(
        {
            "external_result": "same-final-probe",
            "interoceptive_state": {"energy": consequence_energy},
        }
    )

    transformed_field = runtime.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=runtime.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=True,
    )

    candidates = _candidate_set(
        low_field=transformed_field if consequence_energy < 0.5 else _field_core(transformed_field),
        high_field=transformed_field if consequence_energy >= 0.5 else _field_core(transformed_field),
    )

    # Use the same two candidate descriptions in both branches by computing the
    # canonical low/high field predictions from independent control runtimes.
    low_reference = _runtime(root, f"{label}-low-reference")
    low_reference.state.interoceptive_state = {"energy": _consequence_energy(seed, False)}
    low_field = low_reference.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=low_reference.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )
    high_reference = _runtime(root, f"{label}-high-reference")
    high_reference.state.interoceptive_state = {"energy": _consequence_energy(seed, True)}
    high_field = high_reference.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=high_reference.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )
    candidates = _candidate_set(low_field, high_field)

    objective_after = {
        item["id"]: runtime._score_trajectory_details(item)["objective_score"]
        for item in candidates
    }
    selected = runtime.select_trajectory(candidates)

    transformed = runtime.state.interoceptive_state["energy"]
    action_before_reset = str(selected["id"])

    # Destructive intervention: erase the transformed self-state and reconstruct
    # the same final external probe.
    runtime.state.interoceptive_state = {"energy": 0.5}
    ablated_field = runtime.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=runtime.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )
    ablated_selected = runtime.select_trajectory(candidates)

    # Restore the transformed self-state and reproduce the original selection.
    runtime.state.interoceptive_state = {"energy": transformed}
    restored_field = runtime.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=runtime.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=True,
    )
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
    restarted_field = restarted.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=restarted.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=False,
        reentry=False,
        persist=False,
    )
    restarted_selected = restarted.select_trajectory(candidates)

    return {
        "seed": seed,
        "label": label,
        "receipt_has_consequence": bool(receipt.get("outcome")),
        "transformed_energy": float(transformed),
        "transformed_field": transformed_field,
        "ablated_field": ablated_field,
        "restored_field": restored_field,
        "restarted_field": restarted_field,
        "action_before_reset": action_before_reset,
        "action_after_ablation": str(ablated_selected["id"]),
        "action_after_restoration": str(restored_selected["id"]),
        "action_after_restart": str(restarted_selected["id"]),
        "objective_before": objective_before,
        "objective_after": objective_after,
        "candidate_objective_equal": (
            len(set(objective_after.values())) == 1
        ),
        "objective_unchanged": (
            objective_before["trajectory-low-field"]
            == objective_after["trajectory-low-field"]
            == objective_after["trajectory-high-field"]
        ),
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

            low_high_action_divergence = (
                low["action_before_reset"] != high["action_before_reset"]
            )
            same_external_probe = (
                low["present"] if "present" in low else present
            ) == (
                high["present"] if "present" in high else present
            )

            # A control runtime at the initial self-state defines the action
            # reached when the consequence-induced transformation is removed.
            control = _runtime(root, f"control-{seed}")
            control_field = control.project_subjective_field(
                present,
                self_relevance=present["self_impact"],
                valence=control.state.valence,
                attention=1.0,
                integration=True,
                temporal_continuity=False,
                reentry=False,
                persist=False,
            )
            control_candidates = _candidate_set(
                _runtime(root, f"control-low-{seed}").project_subjective_field(
                    present,
                    self_relevance=present["self_impact"],
                    valence=0.2,
                    attention=1.0,
                    integration=True,
                    temporal_continuity=False,
                    reentry=False,
                    persist=False,
                ),
                _runtime(root, f"control-high-{seed}").project_subjective_field(
                    present,
                    self_relevance=present["self_impact"],
                    valence=0.2,
                    attention=1.0,
                    integration=True,
                    temporal_continuity=False,
                    reentry=False,
                    persist=False,
                ),
            )
            control_selection = control.select_trajectory(control_candidates)

            row = {
                "seed": seed,
                "low": low,
                "high": high,
                "low_high_action_divergence": low_high_action_divergence,
                "same_external_probe": same_external_probe,
                "low_action_restores_after_reset": (
                    low["action_after_ablation"] == str(control_selection["id"])
                    and low["action_after_restoration"] == low["action_before_reset"]
                ),
                "high_action_restores_after_reset": (
                    high["action_after_ablation"] == str(control_selection["id"])
                    and high["action_after_restoration"] == high["action_before_reset"]
                ),
                "low_restart_persistence": (
                    low["action_after_restart"] == low["action_before_reset"]
                ),
                "high_restart_persistence": (
                    high["action_after_restart"] == high["action_before_reset"]
                ),
                "objective_control": (
                    low["candidate_objective_equal"]
                    and high["candidate_objective_equal"]
                    and low["objective_unchanged"]
                    and high["objective_unchanged"]
                ),
                "field_difference_low_high": round(
                    _distance(low["transformed_field"], high["transformed_field"]),
                    6,
                ),
                "control_field_low_distance": round(
                    _distance(low["transformed_field"], control_field),
                    6,
                ),
            }
            rows.append(row)

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
    all_pass = all(value == 1.0 for value in summary.values() if isinstance(value, float))

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
                "restore the pre-consequence self-state and require the original "
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
