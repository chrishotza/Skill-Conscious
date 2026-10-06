"""Deterministic minimal assay for causal self-model influence.

This is a functional causal test, not a phenomenal-consciousness test.
The same candidate future set and external context are scored under controlled
interventions to a self-model parameter.
"""
from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    goal_fit: float
    continuity: float
    exploration: float


CANDIDATES = (
    Candidate("preserve", goal_fit=0.50, continuity=1.00, exploration=0.10),
    Candidate("explore", goal_fit=0.56, continuity=0.35, exploration=1.00),
)


def select(candidates: tuple[Candidate, ...], continuity_weight: float, exploration_weight: float) -> dict:
    scored = {}
    for item in candidates:
        scored[item.name] = (
            item.goal_fit
            + continuity_weight * item.continuity
            + exploration_weight * item.exploration
        )
    selected = max(scored, key=scored.get)
    return {"selected": selected, "scores": scored}


def run() -> dict:
    conditions = {
        "baseline_no_self_model": {"continuity_weight": 0.0, "exploration_weight": 0.0},
        "self_model_preserve": {"continuity_weight": 0.40, "exploration_weight": 0.00},
        "self_model_explore": {"continuity_weight": 0.00, "exploration_weight": 0.40},
        "intervention_flip": {"continuity_weight": -0.20, "exploration_weight": 0.60},
    }

    results = {
        name: {
            "intervention": params,
            **select(CANDIDATES, **params),
        }
        for name, params in conditions.items()
    }

    return {
        "assay": "self-model-causal-intervention",
        "candidate_futures": [item.__dict__ for item in CANDIDATES],
        "results": results,
        "interpretation": (
            "A condition-specific trajectory change establishes causal dependence "
            "of this toy selector on the intervened self-model variable. "
            "It does not establish phenomenal consciousness."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
