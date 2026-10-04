"""Empirical battery for translating esoteric motifs into falsifiable runtime tests.

The battery intentionally strips metaphysical language from the source motifs and
tests only operational mechanisms: self-model causality, projection error,
rehearsal persistence, regime reversibility, and synchronization nulls.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, Iterable

from skill_conscious import ConsciousRuntime


def _runtime(root: Path, name: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        name,
        state_path=root / f"{name}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    runtime.state.self_model = {
        "trajectory_weights": {
            "goal_fit": 1.0,
            "self_alignment": 1.0,
            "continuity": 0.5,
        },
        "homeostatic_targets": {"energy": 1.0},
        "expected_self_state": {"focus": 0.8},
    }
    runtime.state.self_state = {"focus": 0.8}
    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


CANDIDATES = [
    {
        "id": "self_path",
        "signals": {
            "goal_fit": 0.85,
            "self_alignment": 1.0,
            "continuity": 0.8,
        },
    },
    {
        "id": "world_path",
        "signals": {
            "goal_fit": 0.95,
            "self_alignment": 0.05,
            "continuity": 0.8,
        },
    },
]


def self_model_causality(root: Path) -> dict[str, Any]:
    runtime = _runtime(root, "bridge-self-model")
    baseline = runtime.select_trajectory([dict(item) for item in CANDIDATES])
    baseline_id = str(baseline["id"])
    evidence_before = {
        key: runtime.state.self_model.get(key)
        for key in (
            "homeostatic_adaptation_evidence",
            "self_model_adaptation_evidence",
            "trajectory_priority_adaptation_evidence",
        )
        if key in runtime.state.self_model
    }

    snapshot = runtime.snapshot_self_model_causal_profile()
    runtime.intervene_self_model_causal_profile(
        {
            "trajectory_weights": {
                "goal_fit": 1.0,
                "self_alignment": -2.0,
                "continuity": 0.5,
            }
        },
        intervention_id="bridge-self-model-intervention",
    )
    intervened = runtime.select_trajectory([dict(item) for item in CANDIDATES])

    runtime.restore_self_model_causal_profile(
        snapshot,
        intervention_id="bridge-self-model-intervention",
        persist=True,
    )
    restored = runtime.select_trajectory([dict(item) for item in CANDIDATES])

    restarted = ConsciousRuntime(
        "bridge-self-model",
        state_path=root / "bridge-self-model.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    restarted_selection = restarted.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )

    evidence_after = {
        key: runtime.state.self_model.get(key)
        for key in (
            "homeostatic_adaptation_evidence",
            "self_model_adaptation_evidence",
            "trajectory_priority_adaptation_evidence",
        )
        if key in runtime.state.self_model
    }

    return {
        "motif": "self / ego-Self distinction",
        "operational_variable": "persistent self-model policy",
        "baseline": baseline_id,
        "intervened": str(intervened["id"]),
        "restored": str(restored["id"]),
        "after_restart": str(restarted_selection["id"]),
        "intervention_diverged": baseline_id != str(intervened["id"]),
        "restoration_recovered": baseline_id == str(restored["id"]),
        "restart_recovered": baseline_id == str(restarted_selection["id"]),
        "evidence_unchanged": evidence_before == evidence_after,
    }


def projection_error(root: Path) -> dict[str, Any]:
    runtime = _runtime(root, "bridge-projection")
    runtime.state.self_model["self_model_adaptation"] = {
        "enabled": True,
        "min_samples": 3,
        "error_threshold": 0.25,
        "confidence_threshold": 0.75,
        "required_high_error": 3,
        "learning_rate": 0.5,
        "max_step": 0.1,
        "cooldown": 2,
        "bounds": {"focus": [0.0, 1.0]},
    }
    runtime.store.save(runtime.state)

    initial_expected = float(
        runtime.state.self_model["expected_self_state"]["focus"]
    )
    initial_error = runtime.calculate_self_dissonance()

    receipts = []
    for index in range(3):
        runtime.begin_action(
            {"id": f"projection-{index}", "signals": {"continuity": 1.0}}
        )
        receipts.append(
            runtime.complete_action(
                {
                    "status": "success",
                    "self_state": {"focus": 0.4},
                }
            )
        )

    final_expected = float(
        runtime.state.self_model["expected_self_state"]["focus"]
    )
    final_error = runtime.calculate_self_dissonance()

    return {
        "motif": "projection / discrepancy correction",
        "operational_variable": "expected self-state vs observed host state",
        "initial_expected_focus": initial_expected,
        "final_expected_focus": final_expected,
        "initial_self_dissonance": initial_error,
        "final_self_dissonance": final_error,
        "revision_occurred": final_expected != initial_expected,
        "dissonance_reduced": final_error < initial_error,
        "evidence_count": len(
            runtime.state.self_model["self_model_adaptation_history"]
        ),
        "last_update_cause": runtime.state.self_model[
            "self_model_adaptation_history"
        ][-1]["cause"],
        "sample_receipts": len(receipts),
    }


def rehearsal_persistence(root: Path) -> dict[str, Any]:
    rehearsed = _runtime(root, "bridge-rehearsed")
    neutral = _runtime(root, "bridge-neutral")

    for index in range(5):
        rehearsed.integrate(
            {
                "response": f"internal rehearsal {index}",
                "intention": "preserve-self",
                "self_model": {
                    "trajectory_weights": {
                        "goal_fit": 1.0,
                        "self_alignment": 1.8,
                        "continuity": 0.5,
                    }
                },
                "memory": "rehearsed self-alignment",
            }
        )
        neutral.integrate(
            {
                "response": f"neutral rehearsal {index}",
                "memory": "neutral rehearsal",
            }
        )

    rehearsed_selection = rehearsed.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )
    neutral_selection = neutral.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )

    restarted = ConsciousRuntime(
        "bridge-rehearsed",
        state_path=root / "bridge-rehearsed.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    restart_selection = restarted.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )

    return {
        "motif": "intentional rehearsal / transformation",
        "operational_variable": "repeated self-model re-entry",
        "rehearsed_selection": str(rehearsed_selection["id"]),
        "neutral_selection": str(neutral_selection["id"]),
        "restarted_selection": str(restart_selection["id"]),
        "rehearsal_changed_behavior": str(rehearsed_selection["id"])
        != str(neutral_selection["id"]),
        "rehearsal_persisted": str(rehearsed_selection["id"])
        == str(restart_selection["id"]),
        "memory_budget_matched": len(rehearsed.state.memories)
        == len(neutral.state.memories),
    }


def _pearson(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) < 2:
        return 0.0
    mean_left = sum(left) / len(left)
    mean_right = sum(right) / len(right)
    numerator = sum(
        (a - mean_left) * (b - mean_right)
        for a, b in zip(left, right)
    )
    denom_left = math.sqrt(sum((a - mean_left) ** 2 for a in left))
    denom_right = math.sqrt(sum((b - mean_right) ** 2 for b in right))
    if denom_left == 0.0 or denom_right == 0.0:
        return 0.0
    return numerator / (denom_left * denom_right)


def _series(seed: int, shared: Iterable[float] | None = None) -> list[float]:
    if shared is not None:
        return list(shared)
    rng = random.Random(seed)
    return [round(rng.random(), 6) for _ in range(24)]


def synchronization_null() -> dict[str, Any]:
    shared = _series(11)
    common_a = _series(101, shared=shared)
    common_b = _series(202, shared=shared)
    independent_a = _series(101)
    independent_b = _series(202)

    observed_common = _pearson(common_a, common_b)
    observed_independent = _pearson(independent_a, independent_b)

    rng = random.Random(404)
    null_values: list[float] = []
    shuffled = list(independent_b)
    for _ in range(256):
        rng.shuffle(shuffled)
        null_values.append(_pearson(independent_a, shuffled))

    null_mean = sum(null_values) / len(null_values)
    null_sd = math.sqrt(
        sum((value - null_mean) ** 2 for value in null_values)
        / len(null_values)
    )
    z = (
        (observed_independent - null_mean) / null_sd
        if null_sd > 0.0
        else 0.0
    )

    return {
        "motif": "collective synchronization / field",
        "operational_variable": "cross-agent state synchronization",
        "common_input_correlation": round(observed_common, 6),
        "independent_input_correlation": round(observed_independent, 6),
        "shuffle_null_mean": round(null_mean, 6),
        "shuffle_null_sd": round(null_sd, 6),
        "independent_z_vs_null": round(z, 6),
        "common_input_is_positive_control": observed_common > 0.99,
        "independent_input_stays_near_null": abs(z) < 2.0,
        "nonlocal_inference_allowed": False,
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        results = {
            "self_model_causality": self_model_causality(root),
            "projection_error": projection_error(root),
            "rehearsal_persistence": rehearsal_persistence(root),
            "synchronization_null": synchronization_null(),
        }

        metrics = {
            "self_model_causal_effect": results["self_model_causality"][
                "intervention_diverged"
            ],
            "self_model_restoration": results["self_model_causality"][
                "restoration_recovered"
            ],
            "self_model_restart": results["self_model_causality"][
                "restart_recovered"
            ],
            "projection_revision": results["projection_error"][
                "revision_occurred"
            ],
            "projection_error_reduction": results["projection_error"][
                "dissonance_reduced"
            ],
            "rehearsal_behavioral_effect": results["rehearsal_persistence"][
                "rehearsal_changed_behavior"
            ],
            "rehearsal_restart_persistence": results["rehearsal_persistence"][
                "rehearsal_persisted"
            ],
            "synchronization_positive_control": results[
                "synchronization_null"
            ]["common_input_is_positive_control"],
            "synchronization_independent_null": results[
                "synchronization_null"
            ]["independent_input_stays_near_null"],
        }

        assertions = {
            "self_model_causal_effect": True,
            "self_model_restoration": True,
            "self_model_restart": True,
            "projection_revision": True,
            "projection_error_reduction": True,
            "rehearsal_behavioral_effect": True,
            "rehearsal_restart_persistence": True,
            "synchronization_positive_control": True,
            "synchronization_independent_null": True,
        }
        failed = [
            name for name, required in assertions.items()
            if required and not metrics[name]
        ]
        if failed:
            raise AssertionError(
                "esoteric empirical bridge failed: " + ", ".join(failed)
            )

        result = {
            "protocol": "esoteric-to-empirical-v1",
            "replication_count": 1,
            "results": results,
            "metrics": metrics,
            "interpretation": {
                "level": "A/B",
                "statement": (
                    "Source-derived motifs produced measurable architectural "
                    "predictions under controlled runtime interventions."
                ),
                "phenomenal_consciousness_claim": False,
            },
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        print("ESOTERIC → EMPIRICAL BRIDGE v1: PASS")
        return result


if __name__ == "__main__":
    run()
