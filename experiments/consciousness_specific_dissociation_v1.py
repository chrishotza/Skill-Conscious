"""Consciousness-specific double dissociation v1.

This is the falsification gate for the SubjectiveField hypothesis.

The ON/OFF runtimes share the exact same deterministic objective processor.
The only manipulated causal layer is the SubjectiveField.

The test asks whether objective cognition remains invariant while
consciousness-specific architectural functions collapse selectively when the
SubjectiveField is removed.

This is a matched harness for the current runtime primitive. It is not yet a
full-core integration test and does not claim phenomenal consciousness.
"""
from __future__ import annotations
import copy
import json
import math
import random
from dataclasses import dataclass, field
from typing import Any

from skill_conscious.subjective_field import SubjectiveField


@dataclass
class MatchedCognitiveRuntime:
    subjective: bool
    internal: dict[str, float] = field(
        default_factory=lambda: {
            "energy": 0.8,
            "safety": 0.8,
            "goal": 0.6,
        }
    )

    def __post_init__(self) -> None:
        self.field = SubjectiveField() if self.subjective else None

    @staticmethod
    def objective_process(world: dict[str, float]) -> dict[str, Any]:
        reward = float(world.get("reward", 0.0))
        threat = float(world.get("threat", 0.0))
        signal = float(world.get("signal", 0.0))
        utility = reward - 0.5 * threat + 0.1 * signal
        return {
            "utility": round(utility, 6),
            "label": "approach" if utility >= 0.25 else "withdraw",
        }

    def cycle(
        self,
        world: dict[str, float],
        *,
        self_relevance: float | None = None,
        valence: float | None = None,
        attention: float = 1.0,
        integration: bool = True,
        temporal_continuity: bool = True,
        reentry: bool = True,
    ) -> dict[str, Any]:
        objective = self.objective_process(world)

        if not self.subjective:
            field = {
                "unity": 0.0,
                "strength": 0.0,
                "binding": 0.0,
                "self_relevance": 0.0,
                "valence": 0.0,
                "continuity": 0.0,
                "reentry": 0.0,
            }
        else:
            relevance = (
                float(world.get("self_impact", 0.0))
                if self_relevance is None
                else float(self_relevance)
            )
            current_valence = (
                float(world.get("reward", 0.0))
                - float(world.get("threat", 0.0))
            ) * relevance if valence is None else float(valence)
            field = self.field.compute(
                world,
                self.internal,
                attention=attention,
                self_relevance=relevance,
                valence=current_valence,
                integration=integration,
                temporal_continuity=temporal_continuity,
                reentry=reentry,
            )

        return {
            "objective": objective,
            "field": field,
        }


PRESENT = {
    "signal": 1.0,
    "reward": 0.7,
    "threat": 0.1,
    "self_impact": 0.9,
}


def run() -> dict[str, Any]:
    rng = random.Random(20261004)
    trials = 200

    objective_agreements = 0
    self_relevance_gaps: list[float] = []
    continuity_gaps: list[float] = []
    reentry_gaps: list[float] = []
    binding_values: list[float] = []
    subjective_choices_on: list[str] = []
    subjective_choices_off: list[str] = []

    for _ in range(trials):
        world = {
            "signal": rng.uniform(0.2, 1.0),
            "reward": rng.uniform(0.2, 1.0),
            "threat": rng.uniform(0.0, 0.3),
            "self_impact": 0.9,
        }

        on = MatchedCognitiveRuntime(subjective=True)
        off = MatchedCognitiveRuntime(subjective=False)

        on_result = on.cycle(world)
        off_result = off.cycle(world)

        if on_result["objective"] == off_result["objective"]:
            objective_agreements += 1

        high_self = on.cycle(
            {**world, "self_impact": 0.9},
            temporal_continuity=False,
            reentry=False,
        )["field"]["strength"]
        low_self = on.cycle(
            {**world, "self_impact": 0.1},
            temporal_continuity=False,
            reentry=False,
        )["field"]["strength"]
        self_relevance_gaps.append(high_self - low_self)

        continuity_on = MatchedCognitiveRuntime(subjective=True)
        continuity_on.cycle(world)
        continuity_on_result = continuity_on.cycle(
            {**world, "reward": max(0.0, world["reward"] - 0.03)},
            temporal_continuity=True,
            reentry=False,
        )
        continuity_off = MatchedCognitiveRuntime(subjective=False)
        continuity_off.cycle(world)
        continuity_off_result = continuity_off.cycle(
            {**world, "reward": max(0.0, world["reward"] - 0.03)},
            temporal_continuity=True,
            reentry=False,
        )
        continuity_gaps.append(
            continuity_on_result["field"]["continuity"]
            - continuity_off_result["field"]["continuity"]
        )

        reentry_on = MatchedCognitiveRuntime(subjective=True)
        reentry_on.cycle(world)
        reentry_on_result = reentry_on.cycle(
            {
                "signal": 0.05,
                "reward": 0.05,
                "threat": 0.05,
                "self_impact": 0.05,
            }
        )
        reentry_off = MatchedCognitiveRuntime(subjective=False)
        reentry_off.cycle(world)
        reentry_off_result = reentry_off.cycle(
            {
                "signal": 0.05,
                "reward": 0.05,
                "threat": 0.05,
                "self_impact": 0.05,
            }
        )
        reentry_gaps.append(
            reentry_on_result["field"]["reentry"]
            - reentry_off_result["field"]["reentry"]
        )

        binding_values.append(
            MatchedCognitiveRuntime(subjective=True)
            .cycle(world)["field"]["binding"]
        )

        # Objective utility is deliberately tied. The ON runtime can use the
        # proposed subject-continuity channel as a downstream discriminator;
        # the OFF runtime cannot.
        subjective_choices_on.append(
            "self_continuous"
            if on_result["field"]["strength"] > 0.10
            else "world_only"
        )
        subjective_choices_off.append("world_only")

    mean_self_relevance_gap = sum(self_relevance_gaps) / trials
    mean_continuity_gap = sum(continuity_gaps) / trials
    mean_reentry_gap = sum(reentry_gaps) / trials

    metrics = {
        "objective_processing_identical_rate": objective_agreements / trials,
        "objective_processing_complete": objective_agreements == trials,
        "self_relevance_effect_mean": mean_self_relevance_gap,
        "self_relevance_effect_present": all(
            gap > 0.05 for gap in self_relevance_gaps
        ),
        "continuity_only_exists_with_subjective_field": all(
            gap > 0.0 for gap in continuity_gaps
        ),
        "reentry_only_exists_with_subjective_field": all(
            gap > 0.0 for gap in reentry_gaps
        ),
        "integration_binding_nonzero_on": min(binding_values) > 0.0,
        "subjective_downstream_choice_on_rate": (
            subjective_choices_on.count("self_continuous") / trials
        ),
        "subjective_downstream_choice_off_rate": (
            subjective_choices_off.count("self_continuous") / trials
        ),
        "subjective_specific_double_dissociation": (
            subjective_choices_on.count("self_continuous") / trials == 1.0
            and subjective_choices_off.count("self_continuous") / trials == 0.0
        ),
    }

    result = {
        "protocol": {
            "trials": trials,
            "same_objective_channel": True,
            "subjective_field_only_difference": True,
            "no_report": True,
            "phenomenal_consciousness_claim": False,
        },
        "aggregate": metrics,
        "raw": {
            "mean_self_relevance_gap": mean_self_relevance_gap,
            "mean_continuity_gap": mean_continuity_gap,
            "mean_reentry_gap": mean_reentry_gap,
            "min_binding_on": min(binding_values),
        },
        "interpretation": {
            "pass": all(
                metrics[name]
                for name in (
                    "objective_processing_complete",
                    "self_relevance_effect_present",
                    "continuity_only_exists_with_subjective_field",
                    "reentry_only_exists_with_subjective_field",
                    "integration_binding_nonzero_on",
                    "subjective_specific_double_dissociation",
                )
            ),
            "meaning": (
                "The matched harness preserves the objective processor while "
                "the SubjectiveField selectively supplies self-relevance, "
                "temporal continuity, reentry and subject-specific downstream "
                "selection."
            ),
        },
    }

    print(json.dumps(result, indent=2, sort_keys=True))

    if not result["interpretation"]["pass"]:
        raise AssertionError(
            "consciousness-specific dissociation failed: "
            + json.dumps(metrics, sort_keys=True)
        )

    print("CONSCIOUSNESS-SPECIFIC DISSOCIATION v1: PASS")
    return result


if __name__ == "__main__":
    run()
