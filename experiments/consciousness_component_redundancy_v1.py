"""Phenotypic substitution and redundancy kill test for the SubjectiveField hypothesis.

This benchmark asks a hard question that single-component ablation cannot answer:

    Can another proposed field component compensate for a removed component
    and restore the same downstream subjective-field function?

The target component remains disabled in every substitution condition. The
candidate substitute is kept within its native semantic range. Continuous
components may be boosted to their allowed maximum; boolean components remain
enabled in their native ON state. Objective processing is held constant.

A successful substitution therefore weakens a claim of unique causal necessity
at the functional level. A failed substitution strengthens causal separation,
but it does not by itself establish phenomenal consciousness.
"""
from __future__ import annotations

import itertools
import json
import random
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime

COMPONENTS = ("binding", "self_relevance", "continuity", "reentry", "attention")
CONTINUOUS = {"self_relevance", "attention"}

def runtime_kwargs() -> dict[str, Any]:
    return {
        "subjective_field_enabled": True,
        "subjective_field_weight": 2.0,
        "metacognition_enabled": False,
        "self_observation_enabled": False,
        "dynamic_core_enabled": False,
        "learn_latent_patterns": False,
    }

def _subjective_flags(
    *,
    target: str | None = None,
    substitute: str | None = None,
) -> dict[str, Any]:
    flags: dict[str, Any] = {
        "subjective_integration": True,
        "subjective_temporal_continuity": True,
        "subjective_reentry": True,
        "subjective_self_relevance": 0.65,
        "subjective_attention": 0.60,
    }

    if target == "binding":
        flags["subjective_integration"] = False
    elif target == "self_relevance":
        flags["subjective_self_relevance"] = 0.0
    elif target == "continuity":
        flags["subjective_temporal_continuity"] = False
    elif target == "reentry":
        flags["subjective_reentry"] = False
    elif target == "attention":
        flags["subjective_attention"] = 0.0

    if substitute is not None:
        if substitute == "self_relevance":
            flags["subjective_self_relevance"] = 1.0
        elif substitute == "attention":
            flags["subjective_attention"] = 1.0

    return flags

def frame(
    world: dict[str, float],
    internal: dict[str, float],
    memory: str,
    *,
    target: str | None = None,
    substitute: str | None = None,
) -> dict[str, Any]:
    flags = _subjective_flags(target=target, substitute=substitute)
    return {
        "response": "redundancy substitution cycle",
        "memory": memory,
        "internal_state": dict(internal),
        "self_model": {
            "trajectory_weights": {
                "goal_fit": 1.0,
                "continuity": 0.5,
            }
        },
        "interoceptive_state": {
            "energy": internal["energy"],
            "safety": internal["safety"],
        },
        "affective_state": {
            "valence": 0.40,
            "arousal": 0.50,
            "homeostatic_error": 0.10,
        },
        "temporal_state": {
            "dt": 1.0,
            "mode": "sampled-continuous",
        },
        "attention": ["self", "goal"],
        "salience": {
            "self": flags["subjective_self_relevance"],
            "goal": 0.8,
        },
        "subjective_present": dict(world),
        "subjective_self_relevance": flags["subjective_self_relevance"],
        "subjective_valence": 0.40,
        "subjective_attention": flags["subjective_attention"],
        "subjective_integration": flags["subjective_integration"],
        "subjective_temporal_continuity": flags["subjective_temporal_continuity"],
        "subjective_reentry": flags["subjective_reentry"],
    }

def objective_state(runtime: ConsciousRuntime) -> dict[str, Any]:
    return {
        "self_state": dict(runtime.state.self_state),
        "memories": list(runtime.state.memories),
        "coherence": float(runtime.state.coherence),
        "valence": float(runtime.state.valence),
        "interoceptive_state": dict(runtime.state.interoceptive_state),
        "affective_state": dict(runtime.state.affective_state),
        "temporal_state": dict(runtime.state.temporal_state),
        "trajectory_weights": dict(
            runtime.state.self_model.get("trajectory_weights", {})
        ),
        "history_length": len(runtime.state.history),
    }

def _cycle_runtime(
    name: str,
    path: Path,
    world: dict[str, float],
    internal: dict[str, float],
    *,
    target: str | None = None,
    substitute: str | None = None,
) -> ConsciousRuntime:
    runtime = ConsciousRuntime(name, path, **runtime_kwargs())
    runtime.integrate(
        frame(world, internal, "cycle-one", target=target, substitute=substitute)
    )
    runtime.integrate(
        frame(world, internal, "cycle-two", target=target, substitute=substitute)
    )
    return runtime

def _candidate_table(
    baseline_field: dict[str, Any],
    target_field: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "id": "canonical",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": dict(baseline_field),
        },
        {
            "id": "target-ablated",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": dict(target_field),
        },
    ]

def _field_distance(left: dict[str, Any], right: dict[str, Any]) -> float:
    keys = set(left) | set(right)
    numeric = []
    for key in keys:
        lv = left.get(key)
        rv = right.get(key)
        if isinstance(lv, (int, float)) and isinstance(rv, (int, float)):
            numeric.append(abs(float(lv) - float(rv)))
    return sum(numeric) / max(1, len(numeric))

def _selected(runtime: ConsciousRuntime, candidates: list[dict[str, Any]]) -> str:
    return str(runtime.select_trajectory(candidates)["id"])

def run_trial(*, target: str, substitute: str, seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    world = {
        "signal": rng.uniform(0.50, 0.85),
        "reward": rng.uniform(0.50, 0.85),
        "threat": rng.uniform(0.04, 0.16),
    }
    internal = {
        "energy": rng.uniform(0.70, 0.90),
        "safety": rng.uniform(0.72, 0.92),
        "goal": rng.uniform(0.68, 0.92),
    }

    with tempfile.TemporaryDirectory(
        prefix=f"conscious-redundancy-{target}-{substitute}-{seed}-"
    ) as tmp:
        root = Path(tmp)
        baseline = _cycle_runtime(
            "baseline",
            root / "baseline.json",
            world,
            internal,
        )
        ablated = _cycle_runtime(
            "ablated",
            root / "ablated.json",
            world,
            internal,
            target=target,
        )
        substituted = _cycle_runtime(
            "substituted",
            root / "substituted.json",
            world,
            internal,
            target=target,
            substitute=substitute,
        )

        baseline_field = baseline.snapshot_subjective_field()["field"]
        ablated_field = ablated.snapshot_subjective_field()["field"]
        substituted_field = substituted.snapshot_subjective_field()["field"]

        candidates = _candidate_table(baseline_field, ablated_field)
        objective_scores = [
            float(baseline._score_trajectory_details(candidate)["objective_score"])
            for candidate in candidates
        ]
        ablated_scores = [
            float(ablated._score_trajectory_details(candidate)["objective_score"])
            for candidate in candidates
        ]
        substituted_scores = [
            float(
                substituted._score_trajectory_details(candidate)["objective_score"]
            )
            for candidate in candidates
        ]

        baseline_selected = _selected(baseline, candidates)
        ablated_selected = _selected(ablated, candidates)
        substituted_selected = _selected(substituted, candidates)

        baseline_state = objective_state(baseline)
        substituted_state = objective_state(substituted)

        baseline_unity = float(baseline_field.get("unity", 0.0))
        baseline_strength = float(baseline_field.get("strength", 0.0))
        substituted_unity = float(substituted_field.get("unity", 0.0))
        substituted_strength = float(substituted_field.get("strength", 0.0))
        target_value = float(substituted_field.get(target, 0.0))

        unity_error = abs(substituted_unity - baseline_unity)
        strength_error = abs(substituted_strength - baseline_strength)
        full_field_error = _field_distance(
            dict(baseline_field),
            dict(substituted_field),
        )

        target_remains_absent = target_value < 1e-9
        baseline_function = (
            baseline_selected == "canonical"
            and ablated_selected == "target-ablated"
        )
        substitution_recovers_function = (
            baseline_function
            and target_remains_absent
            and unity_error <= 0.01
            and strength_error <= 0.01
            and substituted_selected == "canonical"
        )
        objective_scores_match = (
            objective_scores == ablated_scores == substituted_scores
        )
        objective_processing_match = baseline_state == substituted_state

        return {
            "target": target,
            "substitute": substitute,
            "seed": seed,
            "continuous_substitute": substitute in CONTINUOUS,
            "baseline_unity": round(baseline_unity, 6),
            "substituted_unity": round(substituted_unity, 6),
            "baseline_strength": round(baseline_strength, 6),
            "substituted_strength": round(substituted_strength, 6),
            "unity_error": round(unity_error, 6),
            "strength_error": round(strength_error, 6),
            "full_field_error": round(full_field_error, 6),
            "target_value_after_substitution": round(target_value, 6),
            "target_remains_absent": target_remains_absent,
            "baseline_selected": baseline_selected,
            "ablated_selected": ablated_selected,
            "substituted_selected": substituted_selected,
            "baseline_function": baseline_function,
            "substitution_recovers_function": substitution_recovers_function,
            "objective_scores_match": objective_scores_match,
            "objective_processing_match": objective_processing_match,
        }

def run_benchmark(seeds: int = 5) -> dict[str, Any]:
    pairs = list(itertools.permutations(COMPONENTS, 2))
    results = [
        run_trial(
            target=target,
            substitute=substitute,
            seed=20264000 + pair_index * 100 + seed_index,
        )
        for pair_index, (target, substitute) in enumerate(pairs)
        for seed_index in range(seeds)
    ]

    pair_summary: dict[str, Any] = {}
    for target, substitute in pairs:
        key = f"{target}->{substitute}"
        subset = [
            item
            for item in results
            if item["target"] == target and item["substitute"] == substitute
        ]
        pair_summary[key] = {
            "trials": len(subset),
            "substitution_success_rate": sum(
                item["substitution_recovers_function"] for item in subset
            ) / len(subset),
            "target_remains_absent_rate": sum(
                item["target_remains_absent"] for item in subset
            ) / len(subset),
            "objective_score_match_rate": sum(
                item["objective_scores_match"] for item in subset
            ) / len(subset),
            "objective_processing_match_rate": sum(
                item["objective_processing_match"] for item in subset
            ) / len(subset),
        }

    successful_pairs = [
        pair for pair, metrics in pair_summary.items()
        if metrics["substitution_success_rate"] == 1.0
    ]
    nontrivial_kill = all(
        metrics["objective_score_match_rate"] == 1.0
        and metrics["objective_processing_match_rate"] == 1.0
        and metrics["target_remains_absent_rate"] == 1.0
        for metrics in pair_summary.values()
    )

    return {
        "components": list(COMPONENTS),
        "seeds": seeds,
        "pairs": len(pairs),
        "trials": len(results),
        "nontrivial_kill_control_pass": nontrivial_kill,
        "successful_substitution_pairs": successful_pairs,
        "successful_substitution_count": len(successful_pairs),
        "no_substitution_pairs": len(successful_pairs) == 0,
        "all_pass": nontrivial_kill and len(successful_pairs) == 0,
        "pair_summary": pair_summary,
        "results": results,
    }

if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))
