"""Temporal-order causal test for the SubjectiveField consciousness hypothesis.

The same three world/internal states are presented in two different temporal
orders. The final probe is identical. With temporal continuity enabled, the
architecture predicts that the resulting subjective present will retain a
history-dependent difference. With temporal continuity disabled, the order
effect should collapse.

This tests temporal continuity as a causal property of the proposed conscious
subject rather than merely checking that a continuity scalar exists.
"""
from __future__ import annotations

import json
import random
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime


def _runtime(path: Path, identity: str, *, continuity: bool) -> ConsciousRuntime:
    return ConsciousRuntime(
        identity,
        path,
        subjective_field_enabled=True,
        subjective_field_weight=2.0,
        metacognition_enabled=False,
        self_observation_enabled=False,
        dynamic_core_enabled=False,
        learn_latent_patterns=False,
    )


def _frame(
    world: dict[str, float],
    internal: dict[str, float],
    memory: str,
    *,
    continuity: bool,
) -> dict[str, Any]:
    return {
        "response": "temporal order probe",
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
            "self": 0.90,
            "goal": 0.80,
        },
        "subjective_present": dict(world),
        "subjective_self_relevance": 0.90,
        "subjective_valence": 0.40,
        "subjective_attention": 1.0,
        "subjective_integration": True,
        "subjective_temporal_continuity": continuity,
        "subjective_reentry": True,
    }


def _candidate() -> list[dict[str, Any]]:
    return [
        {
            "id": "canonical",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": {
                "unity": 0.55,
                "strength": 0.40,
            },
        },
        {
            "id": "alternative",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": {
                "unity": 0.20,
                "strength": 0.15,
            },
        },
    ]


def _field_vector(field: dict[str, Any]) -> dict[str, float]:
    keys = (
        "world_signal",
        "internal_signal",
        "binding",
        "self_relevance",
        "valence",
        "continuity",
        "reentry",
        "attention",
        "unity",
        "strength",
    )
    return {
        key: float(field.get(key, 0.0))
        for key in keys
        if isinstance(field.get(key, 0.0), (int, float))
    }


def _distance(left: dict[str, float], right: dict[str, float]) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    return sum(abs(left.get(key, 0.0) - right.get(key, 0.0)) for key in keys) / len(keys)


def _objective(runtime: ConsciousRuntime) -> float:
    return float(
        runtime._score_trajectory_details(_candidate()[0])["objective_score"]
    )


def run_trial(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    base_world = {
        "signal": rng.uniform(0.50, 0.85),
        "reward": rng.uniform(0.50, 0.85),
        "threat": rng.uniform(0.04, 0.16),
    }
    alt_world = {
        "signal": rng.uniform(0.50, 0.85),
        "reward": rng.uniform(0.50, 0.85),
        "threat": rng.uniform(0.04, 0.16),
    }
    probe_world = {
        "signal": rng.uniform(0.55, 0.80),
        "reward": rng.uniform(0.55, 0.80),
        "threat": rng.uniform(0.05, 0.12),
    }
    base_internal = {
        "energy": rng.uniform(0.70, 0.90),
        "safety": rng.uniform(0.72, 0.92),
        "goal": rng.uniform(0.68, 0.92),
    }
    alt_internal = {
        "energy": rng.uniform(0.55, 0.75),
        "safety": rng.uniform(0.60, 0.80),
        "goal": rng.uniform(0.58, 0.78),
    }
    probe_internal = {
        "energy": rng.uniform(0.66, 0.86),
        "safety": rng.uniform(0.68, 0.88),
        "goal": rng.uniform(0.64, 0.86),
    }

    with tempfile.TemporaryDirectory(prefix=f"conscious-temporal-order-{seed}-") as tmp:
        root = Path(tmp)

        forward = _runtime(root / "forward.json", "forward", continuity=True)
        reverse = _runtime(root / "reverse.json", "reverse", continuity=True)
        forward_off = _runtime(root / "forward-off.json", "forward-off", continuity=False)
        reverse_off = _runtime(root / "reverse-off.json", "reverse-off", continuity=False)

        sequences = (
            (forward, ((base_world, base_internal, "A"), (alt_world, alt_internal, "B"))),
            (reverse, ((alt_world, alt_internal, "B"), (base_world, base_internal, "A"))),
            (forward_off, ((base_world, base_internal, "A"), (alt_world, alt_internal, "B"))),
            (reverse_off, ((alt_world, alt_internal, "B"), (base_world, base_internal, "A"))),
        )

        for runtime, sequence in sequences:
            for world, internal, memory in sequence:
                runtime.integrate(
                    _frame(world, internal, memory, continuity=runtime is forward or runtime is reverse)
                )

        # Identical final probe for every runtime.
        for runtime in (forward, reverse, forward_off, reverse_off):
            continuity = runtime is forward or runtime is reverse
            runtime.integrate(
                _frame(probe_world, probe_internal, "PROBE", continuity=continuity)
            )

        forward_field = _field_vector(forward.snapshot_subjective_field()["field"])
        reverse_field = _field_vector(reverse.snapshot_subjective_field()["field"])
        forward_off_field = _field_vector(
            forward_off.snapshot_subjective_field()["field"]
        )
        reverse_off_field = _field_vector(
            reverse_off.snapshot_subjective_field()["field"]
        )

        ordered_effect = _distance(forward_field, reverse_field)
        ablated_effect = _distance(forward_off_field, reverse_off_field)

        objective_scores = [
            _objective(runtime)
            for runtime in (forward, reverse, forward_off, reverse_off)
        ]

        return {
            "seed": seed,
            "ordered_effect": round(ordered_effect, 6),
            "continuity_ablated_effect": round(ablated_effect, 6),
            "objective_scores": [round(value, 6) for value in objective_scores],
            "objective_score_match": len(set(objective_scores)) == 1,
            "history_sensitive": ordered_effect > 0.02,
            "order_effect_collapses_under_ablation": ablated_effect < 0.002,
        }


def run_benchmark(seeds: int = 12) -> dict[str, Any]:
    results = [run_trial(20265000 + i) for i in range(seeds)]
    return {
        "seeds": seeds,
        "all_pass": all(
            result["objective_score_match"]
            and result["history_sensitive"]
            and result["order_effect_collapses_under_ablation"]
            for result in results
        ),
        "history_sensitive_rate": sum(
            result["history_sensitive"] for result in results
        ) / len(results),
        "ablation_collapse_rate": sum(
            result["order_effect_collapses_under_ablation"] for result in results
        ) / len(results),
        "objective_score_match_rate": sum(
            result["objective_score_match"] for result in results
        ) / len(results),
        "results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))
