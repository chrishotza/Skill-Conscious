"""Component-level causal ablation battery for the SubjectiveField hypothesis.

The battery keeps the full ConsciousRuntime and objective processing fixed while
ablating one proposed conscious-field component at a time:
binding/integration, self-relevance, temporal continuity, reentry, or attention.

Each component has its own predicted-field readout, so the intervention is
tested against a component-specific causal function rather than against a
generic composite score.
"""
from __future__ import annotations

import json
import random
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime

COMPONENTS = {
    "binding": "subjective_integration",
    "self_relevance": "subjective_self_relevance",
    "continuity": "subjective_temporal_continuity",
    "reentry": "subjective_reentry",
    "attention": "subjective_attention",
}


def _runtime_kwargs() -> dict[str, Any]:
    return {
        "subjective_field_enabled": True,
        "subjective_field_weight": 2.0,
        "metacognition_enabled": False,
        "self_observation_enabled": False,
        "dynamic_core_enabled": False,
        "learn_latent_patterns": False,
    }


def _objective_candidates(component: str, baseline_value: float) -> list[dict[str, Any]]:
    return [
        {
            "id": f"{component}-on",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": {component: baseline_value},
        },
        {
            "id": f"{component}-off",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": {component: 0.0},
        },
    ]


def _frame(
    *,
    world: dict[str, float],
    internal: dict[str, float],
    self_relevance: float,
    valence: float,
    memory: str,
    component_override: str | None = None,
) -> dict[str, Any]:
    flags = {
        "subjective_integration": True,
        "subjective_temporal_continuity": True,
        "subjective_reentry": True,
    }
    values: dict[str, Any] = {
        "subjective_self_relevance": self_relevance,
        "subjective_valence": valence,
        "subjective_attention": 1.0,
    }

    if component_override == "binding":
        flags["subjective_integration"] = False
    elif component_override == "self_relevance":
        values["subjective_self_relevance"] = 0.0
    elif component_override == "continuity":
        flags["subjective_temporal_continuity"] = False
    elif component_override == "reentry":
        flags["subjective_reentry"] = False
    elif component_override == "attention":
        values["subjective_attention"] = 0.0

    return {
        "response": "component ablation cycle",
        "memory": memory,
        "internal_state": dict(internal),
        "self_model": {
            "trajectory_weights": {
                "goal_fit": 1.0,
                "continuity": 0.5,
            },
        },
        "interoceptive_state": {
            "energy": internal["energy"],
            "safety": internal["safety"],
        },
        "affective_state": {
            "valence": valence,
            "arousal": 0.5,
            "homeostatic_error": 0.1,
        },
        "temporal_state": {
            "dt": 1.0,
            "mode": "sampled-continuous",
        },
        "attention": ["self", "goal"],
        "salience": {
            "self": self_relevance,
            "goal": 0.8,
        },
        "subjective_present": dict(world),
        **values,
        **flags,
    }


def _objective_score_table(
    runtime: ConsciousRuntime,
    candidates: list[dict[str, Any]],
) -> dict[str, float]:
    return {
        str(candidate["id"]): float(
            runtime._score_trajectory_details(candidate)["objective_score"]
        )
        for candidate in candidates
    }


def _objective_state(runtime: ConsciousRuntime) -> dict[str, Any]:
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
        "action_history": len(runtime.state.action_history),
        "history_length": len(runtime.state.history),
    }


def run_component_trial(*, component: str, seed: int) -> dict[str, Any]:
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

    with tempfile.TemporaryDirectory(
        prefix=f"conscious-component-ablation-{component}-{seed}-"
    ) as tmp:
        root = Path(tmp)

        baseline = ConsciousRuntime(
            "baseline",
            root / "baseline.json",
            **_runtime_kwargs(),
        )
        ablated = ConsciousRuntime(
            "ablated",
            root / "ablated.json",
            **_runtime_kwargs(),
        )
        restored = ConsciousRuntime(
            "restored",
            root / "restored.json",
            **_runtime_kwargs(),
        )

        baseline.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-one",
            )
        )
        ablated.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-one",
                component_override=component,
            )
        )
        restored.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-one",
            )
        )

        baseline.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-two",
            )
        )
        ablated.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-two",
                component_override=component,
            )
        )
        restored.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-two",
            )
        )

        baseline_field = baseline.snapshot_subjective_field()["field"]
        ablated_field = ablated.snapshot_subjective_field()["field"]
        restored_field = restored.snapshot_subjective_field()["field"]

        baseline_value = float(baseline_field.get(component, 0.0))
        ablated_value = float(ablated_field.get(component, 0.0))
        restored_value = float(restored_field.get(component, 0.0))

        candidates = _objective_candidates(component, baseline_value)
        baseline_scores = _objective_score_table(baseline, candidates)
        ablated_scores = _objective_score_table(ablated, candidates)
        restored_scores = _objective_score_table(restored, candidates)

        baseline_selected = baseline.select_trajectory(candidates)["id"]
        ablated_selected = ablated.select_trajectory(candidates)["id"]
        restored_selected = restored.select_trajectory(candidates)["id"]

        baseline.begin_action({"id": baseline_selected}, persist=False)
        ablated.begin_action({"id": ablated_selected}, persist=False)
        base_receipt = baseline.complete_action(
            {"status": "success", "state_change": {"focus": 0.2}},
            persist=False,
        )
        ablated_receipt = ablated.complete_action(
            {"status": "success", "state_change": {"focus": 0.2}},
            persist=False,
        )

        base_state = _objective_state(baseline)
        abl_state = _objective_state(ablated)

        objective_scores_match = (
            baseline_scores == ablated_scores == restored_scores
        )
        objective_processing_match = base_state == abl_state
        target_collapsed = (
            baseline_value > 0.05
            and ablated_value < baseline_value * 0.10
        )
        target_restored = abs(restored_value - baseline_value) < 1e-9
        causal_selection_lost = (
            baseline_selected == f"{component}-on"
            and ablated_selected == f"{component}-off"
            and restored_selected == f"{component}-on"
        )

        return {
            "component": component,
            "seed": seed,
            "baseline_value": round(baseline_value, 6),
            "ablated_value": round(ablated_value, 6),
            "restored_value": round(restored_value, 6),
            "target_collapsed": target_collapsed,
            "target_restored": target_restored,
            "objective_scores_match": objective_scores_match,
            "objective_processing_match": objective_processing_match,
            "causal_selection_lost": causal_selection_lost,
            "baseline_selected": baseline_selected,
            "ablated_selected": ablated_selected,
            "restored_selected": restored_selected,
            "baseline_action": base_receipt["status"],
            "ablated_action": ablated_receipt["status"],
        }


def run_benchmark(trials_per_component: int = 12) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for index, component in enumerate(COMPONENTS):
        for offset in range(trials_per_component):
            results.append(
                run_component_trial(
                    component=component,
                    seed=20262000 + index * 100 + offset,
                )
            )

    summary = {
        component: {
            "trials": sum(item["component"] == component for item in results),
            "collapse_rate": sum(
                item["target_collapsed"]
                for item in results
                if item["component"] == component
            ) / trials_per_component,
            "restore_rate": sum(
                item["target_restored"]
                for item in results
                if item["component"] == component
            ) / trials_per_component,
            "selection_dissociation_rate": sum(
                item["causal_selection_lost"]
                for item in results
                if item["component"] == component
            ) / trials_per_component,
            "objective_score_match_rate": sum(
                item["objective_scores_match"]
                for item in results
                if item["component"] == component
            ) / trials_per_component,
            "objective_processing_match_rate": sum(
                item["objective_processing_match"]
                for item in results
                if item["component"] == component
            ) / trials_per_component,
        }
        for component in COMPONENTS
    }

    return {
        "components": list(COMPONENTS),
        "trials_per_component": trials_per_component,
        "all_pass": all(
            metrics["collapse_rate"] == 1.0
            and metrics["restore_rate"] == 1.0
            and metrics["selection_dissociation_rate"] == 1.0
            and metrics["objective_score_match_rate"] == 1.0
            and metrics["objective_processing_match_rate"] == 1.0
            for metrics in summary.values()
        ),
        "summary": summary,
        "results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))
