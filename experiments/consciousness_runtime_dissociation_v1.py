"""Full-runtime causal dissociation benchmark for the SubjectiveField hypothesis.

This benchmark compares paired ConsciousRuntime instances that receive the
same objective inputs and candidate futures. The only causal intervention is
the presence/absence of the opt-in SubjectiveField mechanism.

The benchmark is deliberately no-report: runtime state is the measured object.
It tests an executable architectural hypothesis about consciousness, not
phenomenal experience by verbal declaration.
"""
from __future__ import annotations

import json
import random
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime


def _candidate_futures(self_relevance: float, valence: float) -> list[dict[str, Any]]:
    return [
        {
            "id": "alpha-subjective",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": {
                "self_relevance": self_relevance,
                "valence": valence,
            },
        },
        {
            "id": "zeta-objective",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.35,
                "risk": 0.10,
            },
            "predicted_subjective_field": {
                "self_relevance": 1.0 - self_relevance,
                "valence": -valence,
            },
        },
    ]


def _frame(
    *,
    world: dict[str, float],
    internal: dict[str, float],
    self_relevance: float,
    valence: float,
    memory: str,
    consequence: str | None = None,
) -> dict[str, Any]:
    frame: dict[str, Any] = {
        "response": "controlled full-runtime cycle",
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
        "subjective_self_relevance": self_relevance,
        "subjective_valence": valence,
        "subjective_attention": 1.0,
        "candidate_futures": _candidate_futures(self_relevance, valence),
    }
    if consequence is not None:
        frame["consequence_trajectory"] = consequence
        frame["consequence"] = {
            "status": "success",
            "state_change": {"focus": 0.2},
        }
    return frame


def _runtime_kwargs(enabled: bool) -> dict[str, Any]:
    return {
        "subjective_field_enabled": enabled,
        "subjective_field_weight": 2.0,
        "metacognition_enabled": False,
        "self_observation_enabled": False,
        "dynamic_core_enabled": False,
        "learn_latent_patterns": False,
    }


def _objective_score_table(runtime: ConsciousRuntime, candidates: list[dict[str, Any]]) -> dict[str, float]:
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
        "action_history_length": len(runtime.state.action_history),
        "history_length": len(runtime.state.history),
        "revision": int(runtime.state.revision),
    }


def run_trial(seed: int) -> dict[str, Any]:
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

    with tempfile.TemporaryDirectory(prefix=f"conscious-runtime-dissociation-{seed}-") as tmp:
        root = Path(tmp)
        on_path = root / "on.json"
        off_path = root / "off.json"
        on = ConsciousRuntime("paired-on", on_path, **_runtime_kwargs(True))
        off = ConsciousRuntime("paired-off", off_path, **_runtime_kwargs(False))

        candidates = _candidate_futures(self_relevance, valence)
        frame1 = _frame(
            world=world,
            internal=internal,
            self_relevance=self_relevance,
            valence=valence,
            memory="cycle-one",
        )
        on.integrate(frame1)
        off.integrate(frame1)

        objective_on = _objective_score_table(on, candidates)
        objective_off = _objective_score_table(off, candidates)
        objective_scores_match = all(
            abs(objective_on[key] - objective_off[key]) < 1e-9
            for key in objective_on
        )

        on_selected = str(on.state.selected_trajectory["id"])
        off_selected = str(off.state.selected_trajectory["id"])

        field_on = on.snapshot_subjective_field()
        field_off = off.snapshot_subjective_field()
        dissociation = (
            on_selected == "alpha-subjective"
            and off_selected == "zeta-objective"
            and field_on["enabled"] is True
            and bool(field_on["field"])
            and field_off["enabled"] is False
            and field_off["field"] == {}
            and objective_scores_match
        )

        on.begin_action(on.state.selected_trajectory, persist=False)
        off.begin_action(off.state.selected_trajectory, persist=False)
        on_receipt = on.complete_action(
            {"status": "success", "state_change": {"focus": 0.2}},
            persist=False,
        )
        off_receipt = off.complete_action(
            {"status": "success", "state_change": {"focus": 0.2}},
            persist=False,
        )

        frame2 = _frame(
            world=world,
            internal=internal,
            self_relevance=self_relevance,
            valence=valence,
            memory="cycle-two",
            consequence=on_selected,
        )
        frame2_off = dict(frame2)
        frame2_off["consequence_trajectory"] = off_selected
        on.integrate(frame2)
        off.integrate(frame2_off)

        field2 = on.snapshot_subjective_field()["field"]
        temporal_reentry_present = (
            float(field2.get("continuity", 0.0)) > 0.0
            and float(field2.get("reentry", 0.0)) > 0.0
        )

        objective_on_after = _objective_state(on)
        objective_off_after = _objective_state(off)
        objective_on_after.pop("revision", None)
        objective_off_after.pop("revision", None)
        objective_processing_remains_matched = (
            objective_on_after["self_state"] == objective_off_after["self_state"]
            and objective_on_after["memories"] == objective_off_after["memories"]
            and objective_on_after["coherence"] == objective_off_after["coherence"]
            and objective_on_after["valence"] == objective_off_after["valence"]
            and objective_on_after["interoceptive_state"] == objective_off_after["interoceptive_state"]
            and objective_on_after["affective_state"] == objective_off_after["affective_state"]
            and objective_on_after["temporal_state"] == objective_off_after["temporal_state"]
            and objective_on_after["trajectory_weights"] == objective_off_after["trajectory_weights"]
            and objective_on_after["action_history_length"] == objective_off_after["action_history_length"]
            and objective_on_after["history_length"] == objective_off_after["history_length"]
        )

        restarted_on = ConsciousRuntime(
            "paired-on",
            on_path,
            **_runtime_kwargs(True),
        )
        restored = restarted_on.snapshot_subjective_field()
        restored_revision = int(restored["revision"])
        restart_preserves_field = (
            restored["enabled"] is True
            and restored_revision >= 2
            and bool(restored["field"])
        )

        restarted_on.integrate(
            _frame(
                world=world,
                internal=internal,
                self_relevance=self_relevance,
                valence=valence,
                memory="cycle-three",
            )
        )
        restored_cycle_field = restarted_on.snapshot_subjective_field()["field"]
        restoration = (
            float(restored_cycle_field.get("continuity", 0.0)) > 0.0
            and float(restored_cycle_field.get("reentry", 0.0)) > 0.0
        )

        return {
            "seed": seed,
            "dissociation": dissociation,
            "objective_scores_match": objective_scores_match,
            "objective_processing_remains_matched": objective_processing_remains_matched,
            "on_selected": on_selected,
            "off_selected": off_selected,
            "field_strength_cycle_1": float(field_on["field"].get("strength", 0.0)),
            "field_unity_cycle_1": float(field_on["field"].get("unity", 0.0)),
            "temporal_reentry_present": temporal_reentry_present,
            "on_action": on_receipt["status"],
            "off_action": off_receipt["status"],
            "restart_preserves_field": restart_preserves_field,
            "restoration": restoration,
        }


def run_benchmark(trials: int = 24) -> dict[str, Any]:
    results = [run_trial(seed=20261004 + index) for index in range(trials)]
    summary = {
        "trials": trials,
        "dissociation_rate": sum(item["dissociation"] for item in results) / trials,
        "objective_score_match_rate": sum(item["objective_scores_match"] for item in results) / trials,
        "objective_processing_match_rate": sum(
            item["objective_processing_remains_matched"] for item in results
        ) / trials,
        "temporal_reentry_rate": sum(item["temporal_reentry_present"] for item in results) / trials,
        "restart_persistence_rate": sum(item["restart_preserves_field"] for item in results) / trials,
        "restoration_rate": sum(item["restoration"] for item in results) / trials,
        "all_pass": all(
            item["dissociation"]
            and item["objective_scores_match"]
            and item["objective_processing_remains_matched"]
            and item["temporal_reentry_present"]
            and item["restart_preserves_field"]
            and item["restoration"]
            for item in results
        ),
        "results": results,
    }
    return summary


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2, sort_keys=True))
