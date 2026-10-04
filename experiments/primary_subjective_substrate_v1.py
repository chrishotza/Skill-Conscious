"""Causal gate for a minimal pre-cognitive subjective substrate.

The substrate is tested below memory, language, metacognition and self-report.
The matched objective channel remains candidate-side only.

Protocol:
    substrate -> subjective field -> trajectory -> action
    intervention -> divergence -> restoration -> restart

This is an architectural causal experiment, not a test that proves phenomenal
consciousness.
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousRuntime
from skill_conscious.primary_subjective_substrate import PrimarySubjectiveSubstrate


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
        memory_limit=1,
        history_limit=8,
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
        subjective_field_enabled=True,
        subjective_field_weight=1.0,
        primary_subjective_substrate_enabled=True,
        primary_subjective_substrate_weight=1.0,
    )
    runtime.state.self_state = {
        "energy": 0.65,
        "safety": 0.80,
        "goal": 0.70,
    }
    runtime.state.interoceptive_state = {"energy": 0.65}
    runtime.state.valence = 0.10
    runtime.state.salience = {"present": 1.0}
    runtime.state.attention = []
    runtime.state.memories = []
    runtime.state.intention = ""
    runtime.state.latent_patterns = {}
    runtime.state.self_observation = {}
    runtime.store.save(runtime.state)
    return runtime


def _present(seed: int) -> dict[str, float]:
    return {
        "signal": 0.72 + 0.01 * (seed % 3),
        "reward": 0.38 + 0.01 * (seed % 4),
        "threat": 0.07 + 0.01 * (seed % 2),
        "self_impact": 0.90,
    }


def _candidates(low: Mapping[str, Any], neutral: Mapping[str, Any], high: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": "substrate-low",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(low),
        },
        {
            "id": "substrate-neutral",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(neutral),
        },
        {
            "id": "substrate-high",
            "signals": dict(BASE_SIGNALS),
            "predicted_self_relevance": 0.85,
            "predicted_subjective_field": _field_core(high),
        },
    ]


def _project(runtime: ConsciousRuntime, present: Mapping[str, float]) -> dict[str, Any]:
    return runtime.project_subjective_field(
        present,
        self_relevance=present["self_impact"],
        valence=runtime.state.valence,
        attention=1.0,
        integration=True,
        temporal_continuity=True,
        reentry=True,
        persist=True,
    )


def run_benchmark(seeds: int = 12) -> dict[str, Any]:
    if seeds < 2:
        raise ValueError("seeds must be >= 2")

    rows: list[dict[str, Any]] = []

    with TemporaryDirectory() as tmp:
        root = Path(tmp)

        for seed in range(20268000, 20268000 + seeds):
            present = _present(seed)

            baseline = _runtime(root, f"baseline-{seed}")
            baseline_field = _project(baseline, present)
            baseline_substrate = baseline.snapshot_primary_subjective_substrate()

            # Matched reference fields are used only to give the selector a
            # substrate-sensitive possibility space. Explicit candidate signals
            # remain identical.
            low_ref = _runtime(root, f"low-ref-{seed}")
            low_ref.primary_subjective_substrate.step(
                present,
                low_ref._numeric_state(low_ref.state.self_state),
                tuning=0.55,
            )
            low_field = _project(low_ref, present)

            neutral_ref = _runtime(root, f"neutral-ref-{seed}")
            neutral_ref.primary_subjective_substrate.step(
                present,
                neutral_ref._numeric_state(neutral_ref.state.self_state),
                tuning=1.00,
            )
            neutral_field = _project(neutral_ref, present)

            high_ref = _runtime(root, f"high-ref-{seed}")
            high_ref.primary_subjective_substrate.step(
                present,
                high_ref._numeric_state(high_ref.state.self_state),
                tuning=1.45,
            )
            high_field = _project(high_ref, present)

            candidates = _candidates(low_field, neutral_field, high_field)

            objective_before = {
                item["id"]: baseline._score_trajectory_details(item)["objective_score"]
                for item in candidates
            }
            selected_baseline = baseline.select_trajectory(candidates)

            intervention = baseline.intervene_primary_subjective_substrate(
                {"tuning": 0.55, "maintenance": True, "coupling": True, "closure": True, "recurrence": True},
                persist=False,
                intervention_id=f"abl-{seed}",
            )
            ablated_field = _project(baseline, present)
            ablated_selected = baseline.select_trajectory(candidates)

            restore = baseline.restore_primary_subjective_substrate(
                baseline_substrate,
                persist=False,
                intervention_id=f"restore-{seed}",
            )
            restored_field = _project(baseline, present)
            restored_selected = baseline.select_trajectory(candidates)

            restarted = ConsciousRuntime(
                f"baseline-{seed}",
                state_path=root / f"baseline-{seed}.json",
                memory_limit=1,
                history_limit=8,
                learn_latent_patterns=False,
                learn_self_model_from_latent_patterns=False,
                report_enabled=False,
                metacognition_enabled=False,
                self_observation_enabled=False,
                subjective_field_enabled=True,
                subjective_field_weight=1.0,
                primary_subjective_substrate_enabled=True,
                primary_subjective_substrate_weight=1.0,
            )
            restarted_field = _project(restarted, present)
            restarted_selected = restarted.select_trajectory(candidates)

            objective_after = {
                item["id"]: restarted._score_trajectory_details(item)["objective_score"]
                for item in candidates
            }

            rows.append(
                {
                    "seed": seed,
                    "baseline_substrate": baseline_substrate,
                    "intervention": intervention,
                    "restore": restore,
                    "baseline_field": baseline_field,
                    "ablated_field": ablated_field,
                    "restored_field": restored_field,
                    "restarted_field": restarted_field,
                    "baseline_action": str(selected_baseline["id"]),
                    "ablated_action": str(ablated_selected["id"]),
                    "restored_action": str(restored_selected["id"]),
                    "restarted_action": str(restarted_selected["id"]),
                    "field_intervention_distance": round(
                        _distance(baseline_field, ablated_field), 6
                    ),
                    "field_restore_distance": round(
                        _distance(baseline_field, restored_field), 6
                    ),
                    "field_restart_distance": round(
                        _distance(baseline_field, restarted_field), 6
                    ),
                    "objective_before": objective_before,
                    "objective_after": objective_after,
                }
            )

    summary = {
        "seed_count": len(rows),
        "field_intervention_rate": sum(
            row["field_intervention_distance"] > 0.02 for row in rows
        ) / len(rows),
        "field_restoration_rate": sum(
            row["field_restore_distance"] < 0.002 for row in rows
        ) / len(rows),
        "field_restart_persistence_rate": sum(
            row["field_restart_distance"] < 0.002 for row in rows
        ) / len(rows),
        "action_intervention_rate": sum(
            row["baseline_action"] != row["ablated_action"] for row in rows
        ) / len(rows),
        "action_restoration_rate": sum(
            row["baseline_action"] == row["restored_action"] for row in rows
        ) / len(rows),
        "action_restart_rate": sum(
            row["baseline_action"] == row["restarted_action"] for row in rows
        ) / len(rows),
        "objective_match_rate": sum(
            row["objective_before"] == row["objective_after"] for row in rows
        ) / len(rows),
    }

    result = {
        "protocol": {
            "what_aspect": (
                "pre-cognitive subjective organization: persistent internal "
                "state, coupling, oscillation, closure and recurrent tuning"
            ),
            "causal_relation": (
                "substrate regime -> subjective field -> next trajectory "
                "under a matched explicit objective channel"
            ),
            "destructive_test": (
                "alter substrate tuning, require field/action divergence, "
                "then restore the exact substrate state and restart"
            ),
            "pre_cognitive_constraints": {
                "memory": False,
                "language": False,
                "metacognition": False,
                "self_report": False,
                "self_observation": False,
            },
            "phenomenal_consciousness_claim": False,
        },
        "thresholds": {
            "field_intervention": "> 0.02",
            "field_restoration": "< 0.002",
            "field_restart": "< 0.002",
            "action_intervention": "1.0",
            "action_restoration": "1.0",
            "action_restart": "1.0",
            "objective_match": "1.0",
        },
        "summary": summary,
        "all_pass": all(
            value == 1.0
            for value in summary.values()
            if isinstance(value, float)
        ),
        "rows": rows,
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise AssertionError("primary subjective substrate causal gate failed")
    print("PRIMARY SUBJECTIVE SUBSTRATE V1: PASS")
    return result


if __name__ == "__main__":
    run_benchmark()
