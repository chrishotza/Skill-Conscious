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
    reentry: bool,
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
        "subjective_reentry": reentry,
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
    # Use two intentionally distinct regimes so order changes the causal
    # predecessor of the identical probe without changing the final probe.
    base_world = {
        "signal": rng.uniform(0.10, 0.25),
        "reward": rng.uniform(0.10, 0.25),
        "threat": rng.uniform(0.70, 0.90),
    }
    alt_world = {
        "signal": rng.uniform(0.85, 0.98),
        "reward": rng.uniform(0.85, 0.98),
        "threat": rng.uniform(0.02, 0.10),
    }
    probe_world = {
        "signal": rng.uniform(0.55, 0.80),
        "reward": rng.uniform(0.55, 0.80),
        "threat": rng.uniform(0.05, 0.12),
    }
    base_internal = {
        "energy": rng.uniform(0.10, 0.30),
        "safety": rng.uniform(0.15, 0.35),
        "goal": rng.uniform(0.10, 0.30),
    }
    alt_internal = {
        "energy": rng.uniform(0.85, 0.98),
        "safety": rng.uniform(0.85, 0.98),
        "goal": rng.uniform(0.85, 0.98),
    }
    probe_internal = {
        "energy": rng.uniform(0.66, 0.86),
        "safety": rng.uniform(0.68, 0.88),
        "goal": rng.uniform(0.64, 0.86),
    }

    histories = {
        "forward": (
            (base_world, base_internal, "A"),
            (alt_world, alt_internal, "B"),
        ),
        "reverse": (
            (alt_world, alt_internal, "B"),
            (base_world, base_internal, "A"),
        ),
    }
    flags = {
        "full": (True, True),
        "continuity_only": (True, False),
        "reentry_only": (False, True),
        "neither": (False, False),
    }

    with tempfile.TemporaryDirectory(
        prefix=f"conscious-temporal-order-{seed}-"
    ) as tmp:
        root = Path(tmp)
        fields: dict[str, dict[str, float]] = {}
        objective_scores: list[float] = []

        for condition, (continuity, reentry) in flags.items():
            for order, sequence in histories.items():
                runtime = _runtime(
                    root / f"{condition}-{order}.json",
                    f"{condition}-{order}",
                    continuity=continuity,
                )

                for world, internal, memory in sequence:
                    runtime.integrate(
                        _frame(
                            world,
                            internal,
                            memory,
                            continuity=continuity,
                            reentry=reentry,
                        )
                    )

                runtime.integrate(
                    _frame(
                        probe_world,
                        probe_internal,
                        "PROBE",
                        continuity=continuity,
                        reentry=reentry,
                    )
                )

                fields[f"{condition}_{order}"] = _field_vector(
                    runtime.snapshot_subjective_field()["field"]
                )
                objective_scores.append(_objective(runtime))

        effects = {
            condition: _distance(
                fields[f"{condition}_forward"],
                fields[f"{condition}_reverse"],
            )
            for condition in flags
        }

        return {
            "seed": seed,
            "full_order_effect": round(effects["full"], 6),
            "continuity_only_order_effect": round(
                effects["continuity_only"], 6
            ),
            "reentry_only_order_effect": round(
                effects["reentry_only"], 6
            ),
            "neither_order_effect": round(effects["neither"], 6),
            "objective_score_match": len(set(objective_scores)) == 1,
            "full_history_sensitive": effects["full"] > 0.02,
            "continuity_carries_history": effects["continuity_only"] > 0.02,
            "reentry_carries_history": effects["reentry_only"] > 0.02,
            "history_collapses_when_both_removed": effects["neither"] < 0.002,
        }


def run_benchmark(seeds: int = 12) -> dict[str, Any]:
    results = [run_trial(20265000 + i) for i in range(seeds)]
    return {
        "seeds": seeds,
        "all_pass": all(
            result["objective_score_match"]
            and result["full_history_sensitive"]
            and result["continuity_carries_history"]
            and result["reentry_carries_history"]
            and result["history_collapses_when_both_removed"]
            for result in results
        ),
        "full_history_sensitive_rate": sum(
            result["full_history_sensitive"] for result in results
        ) / len(results),
        "continuity_history_rate": sum(
            result["continuity_carries_history"] for result in results
        ) / len(results),
        "reentry_history_rate": sum(
            result["reentry_carries_history"] for result in results
        ) / len(results),
        "history_collapse_rate": sum(
            result["history_collapses_when_both_removed"] for result in results
        ) / len(results),
        "objective_score_match_rate": sum(
            result["objective_score_match"] for result in results
        ) / len(results),
        "results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))

