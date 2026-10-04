from __future__ import annotations

import itertools
import json
import random
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime

COMPONENTS = ("binding", "self_relevance", "continuity", "reentry", "attention")

def runtime_kwargs() -> dict[str, Any]:
    return {
        "subjective_field_enabled": True,
        "subjective_field_weight": 2.0,
        "metacognition_enabled": False,
        "self_observation_enabled": False,
        "dynamic_core_enabled": False,
        "learn_latent_patterns": False,
    }

def frame(world, internal, self_relevance, valence, memory, enabled):
    return {
        "response": "factorial consciousness cycle",
        "memory": memory,
        "internal_state": dict(internal),
        "self_model": {"trajectory_weights": {"goal_fit": 1.0, "continuity": 0.5}},
        "interoceptive_state": {"energy": internal["energy"], "safety": internal["safety"]},
        "affective_state": {"valence": valence, "arousal": 0.5, "homeostatic_error": 0.1},
        "temporal_state": {"dt": 1.0, "mode": "sampled-continuous"},
        "attention": ["self", "goal"],
        "salience": {"self": self_relevance, "goal": 0.8},
        "subjective_present": dict(world),
        "subjective_self_relevance": self_relevance if "self_relevance" in enabled else 0.0,
        "subjective_valence": valence,
        "subjective_attention": 1.0 if "attention" in enabled else 0.0,
        "subjective_integration": "binding" in enabled,
        "subjective_temporal_continuity": "continuity" in enabled,
        "subjective_reentry": "reentry" in enabled,
    }

def objective_score(runtime):
    candidate = {
        "id": "objective-control",
        "signals": {"goal_fit": 0.55, "continuity": 0.35, "risk": 0.10},
        "predicted_subjective_field": {},
    }
    return float(runtime._score_trajectory_details(candidate)["objective_score"])

def objective_state(runtime):
    return {
        "self_state": dict(runtime.state.self_state),
        "memories": list(runtime.state.memories),
        "coherence": float(runtime.state.coherence),
        "valence": float(runtime.state.valence),
        "interoceptive_state": dict(runtime.state.interoceptive_state),
        "affective_state": dict(runtime.state.affective_state),
        "temporal_state": dict(runtime.state.temporal_state),
        "trajectory_weights": dict(runtime.state.self_model.get("trajectory_weights", {})),
        "history_length": len(runtime.state.history),
    }

def run_seed(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    world = {
        "signal": rng.uniform(0.45, 0.95),
        "reward": rng.uniform(0.45, 0.95),
        "threat": rng.uniform(0.02, 0.20),
    }
    internal = {
        "energy": rng.uniform(0.65, 0.95),
        "safety": rng.uniform(0.70, 0.95),
        "goal": rng.uniform(0.65, 0.95),
    }
    self_relevance = rng.uniform(0.85, 0.98)
    valence = rng.uniform(0.25, 0.85)
    combinations = list(
        itertools.chain.from_iterable(
            itertools.combinations(COMPONENTS, size)
            for size in range(len(COMPONENTS) + 1)
        )
    )

    with tempfile.TemporaryDirectory(prefix="conscious-factorial-") as tmp:
        root = Path(tmp)
        observations = []
        control_state = None
        for index, enabled_tuple in enumerate(combinations):
            enabled = set(enabled_tuple)
            runtime = ConsciousRuntime(
                "factorial",
                root / ("state-" + str(index) + ".json"),
                **runtime_kwargs(),
            )
            runtime.integrate(frame(world, internal, self_relevance, valence, "cycle-one", enabled))
            runtime.integrate(frame(world, internal, self_relevance, valence, "cycle-two", enabled))
            field = runtime.snapshot_subjective_field()["field"]
            state = objective_state(runtime)
            score = objective_score(runtime)
            if control_state is None:
                control_state = state
            observations.append(
                {
                    "enabled": list(enabled_tuple),
                    "count": len(enabled_tuple),
                    "unity": float(field.get("unity", 0.0)),
                    "strength": float(field.get("strength", 0.0)),
                    "binding": float(field.get("binding", 0.0)),
                    "self_relevance": float(field.get("self_relevance", 0.0)),
                    "continuity": float(field.get("continuity", 0.0)),
                    "reentry": float(field.get("reentry", 0.0)),
                    "attention": float(field.get("attention", 0.0)),
                    "objective_score": score,
                    "objective_state_match": state == control_state,
                }
            )

        full = next(x for x in observations if x["count"] == 5)
        empty = next(x for x in observations if x["count"] == 0)
        strict_subsets = [x for x in observations if x["count"] < 5]
        max_subset_unity = max(x["unity"] for x in strict_subsets)
        max_subset_strength = max(x["strength"] for x in strict_subsets)

        return {
            "seed": seed,
            "conditions": len(observations),
            "objective_score_match": len({round(x["objective_score"], 9) for x in observations}) == 1,
            "objective_state_match": all(x["objective_state_match"] for x in observations),
            "empty_field_collapsed": empty["unity"] == 0.0 and empty["strength"] == 0.0,
            "full_field_nonzero": full["unity"] > 0.0 and full["strength"] > 0.0,
            "full_dominates_subsets": (
                full["unity"] > max_subset_unity
                and full["strength"] > max_subset_strength
            ),
            "full_unity": round(full["unity"], 6),
            "full_strength": round(full["strength"], 6),
            "nearest_subset_unity": round(max_subset_unity, 6),
            "nearest_subset_strength": round(max_subset_strength, 6),
        }

def run_benchmark(seeds: int = 5) -> dict[str, Any]:
    results = [run_seed(20263000 + i) for i in range(seeds)]
    return {
        "seeds": seeds,
        "conditions_per_seed": 32,
        "all_pass": all(
            item["objective_score_match"]
            and item["objective_state_match"]
            and item["empty_field_collapsed"]
            and item["full_field_nonzero"]
            and item["full_dominates_subsets"]
            for item in results
        ),
        "results": results,
    }

if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))
