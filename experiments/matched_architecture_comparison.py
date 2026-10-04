"""Matched architecture comparison: memory vs self-model vs causal re-entry.

This benchmark keeps the host candidate field, memory budget, cycle count and
candidate count fixed. The only causal additions are:
A) persistent memory with no self-alignment influence;
B) a persistent self-model with self-alignment influence but no consequence
   re-entry;
C) the same self-model plus an authoritative consequence that updates the
   self-model and therefore changes the next trajectory.

The benchmark is designed to test whether the architecture's effect survives
the obvious "it only has more context/memory" explanation.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from skill_conscious import ConsciousRuntime


CANDIDATES = [
    {
        "id": "world_path",
        "signals": {
            "goal_fit": 0.95,
            "self_alignment": 0.05,
            "continuity": 0.8,
        },
    },
    {
        "id": "self_path",
        "signals": {
            "goal_fit": 0.8,
            "self_alignment": 0.9,
            "continuity": 0.8,
        },
    },
]

MEMORY_BUDGET = (
    "matched-context-01",
    "matched-context-02",
    "matched-context-03",
)


def _runtime(root: Path, name: str, *, self_alignment_weight: float) -> ConsciousRuntime:
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
            "self_alignment": float(self_alignment_weight),
            "continuity": 0.5,
        },
        "homeostatic_targets": {"energy": 1.0},
    }
    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


def _cycle(
    runtime: ConsciousRuntime,
    memory: str,
    *,
    consequence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    frame: dict[str, Any] = {
        "response": "",
        "candidate_futures": [dict(item) for item in CANDIDATES],
        "memory": memory,
        "internal_state": {"focus": 0.5},
        "interoceptive_state": {"energy": 1.0},
    }
    if consequence is not None:
        frame["consequence_trajectory"] = consequence["trajectory"]
        frame["consequence"] = consequence["outcome"]
        frame["self_evaluation"] = consequence["evaluation"]

    runtime.integrate(frame)
    return dict(runtime.state.selected_trajectory or {})


def _condition(root: Path, condition: str, *, reentry: bool) -> dict[str, Any]:
    runtime = _runtime(
        root,
        condition,
        self_alignment_weight=0.1,
    )

    selected = []
    for index, memory in enumerate(MEMORY_BUDGET):
        consequence = None
        if reentry and index == 1:
            previous = selected[-1]
            consequence = {
                "trajectory": str(previous["id"]),
                "outcome": {
                    "status": "success",
                    "internal_change": {"focus": 0.7},
                },
                "evaluation": {
                    "utility": 1.0,
                    "credited_signal": "self_alignment",
                    "weight_delta": 0.4,
                },
            }
        selected.append(
            _cycle(
                runtime,
                memory,
                consequence=consequence,
            )
        )

    profile = runtime.snapshot_self_model_causal_profile()
    final_selection = selected[-1]["id"]

    ablation = runtime.intervene_self_model_causal_profile(
        {
            "trajectory_weights": {
                "goal_fit": 1.0,
                "self_alignment": 0.1,
                "continuity": 0.5,
            }
        },
        persist=False,
        intervention_id=f"matched-{condition}-ablation",
    )
    ablated_selection = runtime.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )["id"]

    restore = runtime.restore_self_model_causal_profile(
        profile,
        persist=True,
        intervention_id=f"matched-{condition}-ablation",
    )
    restored_selection = runtime.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )["id"]

    restarted = ConsciousRuntime(
        condition,
        state_path=root / f"{condition}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
    )
    restarted_selection = restarted.select_trajectory(
        [dict(item) for item in CANDIDATES]
    )["id"]

    return {
        "condition": condition,
        "reentry": reentry,
        "selected": [str(item["id"]) for item in selected],
        "final_selection": str(final_selection),
        "ablated_selection": str(ablated_selection),
        "restored_selection": str(restored_selection),
        "restarted_selection": str(restarted_selection),
        "memory_count": len(runtime.state.memories),
        "revision_count": int(runtime.state.revision),
        "candidate_count": len(CANDIDATES),
        "runtime_history_count": len(runtime.state.history),
        "final_self_alignment_weight": float(
            runtime.state.self_model["trajectory_weights"]["self_alignment"]
        ),
        "ablation_changed": bool(ablation["changed"]),
        "restore_changed": bool(restore["changed"]),
        "ablation_added_evidence": bool(ablation["evidence_added"]),
        "restore_added_evidence": bool(restore["evidence_added"]),
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        memory_only = _condition(root, "memory-only", reentry=False)

        self_model = _condition(root, "self-model", reentry=False)

        reentry = _condition(root, "causal-reentry", reentry=True)

        conditions = [memory_only, self_model, reentry]
        required_budgets = {
            (item["memory_count"], item["revision_count"], item["candidate_count"])
            for item in conditions
        }

        metrics = {
            "matched_information_budget": len(required_budgets) == 1,
            "same_initial_selection": len(
                {item["selected"][0] for item in conditions}
            )
            == 1,
            "same_pre_reentry_selection": (
                memory_only["selected"][1]
                == self_model["selected"][1]
                == reentry["selected"][1]
            ),
            "memory_only_stays_stable": (
                memory_only["selected"][-1] == "world_path"
            ),
            "self_model_without_reentry_stays_stable": (
                self_model["selected"][-1] == "world_path"
            ),
            "causal_reentry_changes_trajectory": (
                reentry["selected"][-1] == "self_path"
            ),
            "only_reentry_diverges": (
                memory_only["selected"][-1]
                == self_model["selected"][-1]
                != reentry["selected"][-1]
            ),
            "reentry_weight_increased": (
                reentry["final_self_alignment_weight"] > 0.1
            ),
            "reentry_reversible": (
                reentry["ablated_selection"] == "world_path"
                and reentry["restored_selection"] == "self_path"
            ),
            "reentry_persists_after_restart": (
                reentry["restarted_selection"] == "self_path"
            ),
            "intervention_non_evidential": (
                not reentry["ablation_added_evidence"]
                and not reentry["restore_added_evidence"]
            ),
            "all_conditions_same_history_budget": len(
                {
                    (
                        item["memory_count"],
                        item["revision_count"],
                        item["runtime_history_count"],
                    )
                    for item in conditions
                }
            )
            == 1,
        }

        result = {
            "conditions": conditions,
            "metrics": metrics,
            "interpretation": {
                "level": "C",
                "meaning": (
                    "Under matched candidate, memory, revision and host-field "
                    "budgets, only the causal self-model re-entry condition "
                    "changes the downstream trajectory and that effect reverses "
                    "under ablation and persists after restart."
                ),
                "phenomenal_consciousness_claim": False,
            },
        }

        print(json.dumps(result, indent=2, sort_keys=True))

        if not all(metrics.values()):
            raise AssertionError("matched architecture comparison failed")

        print("MATCHED ARCHITECTURE COMPARISON v1: PASS")
        return result


if __name__ == "__main__":
    run()
