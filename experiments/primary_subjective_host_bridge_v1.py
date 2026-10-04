"""Host-loop closure benchmark for the primary subjective substrate.

This benchmark keeps the external probe and candidate objective channel fixed
while a consequence changes the internal bodily state. The primary substrate
must then alter the next subjectively organized field and the next selected
trajectory.

The model callback is deterministic in this harness. Its purpose is to verify
the host boundary, not to simulate an LLM. A later provider-facing benchmark
can replace the callback with an actual OpenAI-compatible model without
changing the causal protocol.
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousHostLoop, ConsciousRuntime


PRESENT = {
    "signal": 0.76,
    "reward": 0.38,
    "threat": 0.08,
    "self_impact": 0.90,
}

CANDIDATE_SIGNALS = {
    "goal_fit": 0.80,
    "self_alignment": 0.40,
}


def _field_core(field: Mapping[str, Any]) -> dict[str, float]:
    return {
        key: float(field.get(key, 0.0))
        for key in (
            "world_signal",
            "internal_signal",
            "binding",
            "self_relevance",
            "valence",
            "unity",
            "strength",
        )
    }


def _runtime(root: Path, label: str, *, energy: float = 0.65) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        memory_limit=1,
        history_limit=8,
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
        subjective_field_enabled=True,
        subjective_field_weight=1.0,
        primary_subjective_substrate_enabled=True,
        primary_subjective_substrate_weight=1.0,
    )
    runtime.state.self_state = {
        "energy": energy,
        "safety": 0.80,
        "goal": 0.70,
    }
    runtime.state.interoceptive_state = {"energy": energy}
    runtime.state.salience = {"present": 1.0}
    runtime.state.attention = []
    runtime.state.memories = []
    runtime.state.intention = ""
    runtime.state.latent_patterns = {}
    runtime.store.save(runtime.state)
    return runtime


def _build_candidate_field(
    root: Path,
) -> tuple[
    dict[str, float],
    dict[str, float],
    dict[str, float],
]:
    preserve = _runtime(root, "candidate-preserve", energy=0.65)
    preserve_field = preserve.project_subjective_field(
        PRESENT,
        self_relevance=PRESENT["self_impact"],
        attention=1.0,
        persist=True,
    )

    recover = _runtime(root, "candidate-recover", energy=0.65)
    recover.project_subjective_field(
        PRESENT,
        self_relevance=PRESENT["self_impact"],
        attention=1.0,
        persist=True,
    )
    recover.state.interoceptive_state = {"energy": 0.05}
    recover.state.self_state["energy"] = 0.05
    recover_field = recover.project_subjective_field(
        PRESENT,
        self_relevance=PRESENT["self_impact"],
        attention=1.0,
        persist=True,
    )

    ablated = _runtime(root, "candidate-ablated", energy=0.65)
    ablated.project_subjective_field(
        PRESENT,
        self_relevance=PRESENT["self_impact"],
        attention=1.0,
        persist=True,
    )
    ablated.intervene_primary_subjective_substrate(
        {
            "tuning": 0.50,
            "maintenance": False,
            "coupling": False,
            "closure": False,
            "recurrence": False,
        },
        intervention_id="candidate-ablated-state",
    )
    ablated.state.interoceptive_state = {"energy": 0.05}
    ablated.state.self_state["energy"] = 0.05
    ablated_field = ablated.project_subjective_field(
        PRESENT,
        self_relevance=PRESENT["self_impact"],
        attention=1.0,
        persist=True,
    )

    return (
        _field_core(preserve_field),
        _field_core(recover_field),
        _field_core(ablated_field),
    )


def _candidates(
    preserve_field: Mapping[str, float],
    recover_field: Mapping[str, float],
    ablated_field: Mapping[str, float],
) -> list[dict[str, Any]]:
    return [
        {
            "id": "preserve",
            "signals": dict(CANDIDATE_SIGNALS),
            "predicted_subjective_field": dict(preserve_field),
        },
        {
            "id": "recover",
            "signals": dict(CANDIDATE_SIGNALS),
            "predicted_subjective_field": dict(recover_field),
        },
        {
            "id": "substrate-ablated",
            "signals": dict(CANDIDATE_SIGNALS),
            "predicted_subjective_field": dict(ablated_field),
        },
    ]


def _run_condition(
    root: Path,
    *,
    label: str,
    candidates: list[dict[str, Any]],
    ablate: bool,
) -> dict[str, Any]:
    runtime = _runtime(root, label)
    prompts: list[str] = []

    def model(prompt: str) -> Mapping[str, Any]:
        prompts.append(prompt)
        return {"candidate_futures": [dict(item) for item in candidates]}

    def execute_action(
        _trajectory: Mapping[str, Any],
        _snapshot: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        if ablate:
            runtime.intervene_primary_subjective_substrate(
                {
                    "tuning": 0.50,
                    "maintenance": False,
                    "coupling": False,
                    "closure": False,
                    "recurrence": False,
                },
                persist=False,
                intervention_id=f"{label}-substrate-ablation",
            )
        return {
            "status": "success",
            "interoceptive_state": {"energy": 0.05},
            "subjective_present": dict(PRESENT),
        }

    loop = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=execute_action,
        require_report=False,
    )

    result = loop.step(
        "Choose what the system should do next.",
        subjective_present=PRESENT,
    )

    initial = dict(result.get("selected_trajectory") or {})
    next_selected = dict(result.get("next_trajectory") or {})
    field_after = runtime.snapshot_subjective_field()["field"]

    consequence_prompt_visible = (
        len(prompts) >= 2
        and '"subjective_field"' in prompts[1]
        and '"unity"' in prompts[1]
        and '"strength"' in prompts[1]
    )

    restarted = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        memory_limit=1,
        history_limit=8,
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
        subjective_field_enabled=True,
        subjective_field_weight=1.0,
        primary_subjective_substrate_enabled=True,
        primary_subjective_substrate_weight=1.0,
    )
    restart_field = restarted.snapshot_subjective_field()["field"]
    restart_selected = restarted.select_trajectory(candidates)

    return {
        "condition": "ablated" if ablate else "intact",
        "initial": str(initial.get("id", "")),
        "next": str(next_selected.get("id", "")),
        "after_restart": str(restart_selected.get("id", "")),
        "field_after": field_after,
        "restart_field": restart_field,
        "field_after_restart_distance": round(
            sum(
                abs(float(field_after.get(key, 0.0)) - float(restart_field.get(key, 0.0)))
                for key in _field_core(field_after)
            ) / len(_field_core(field_after)),
            6,
        ),
        "prompt_count": len(prompts),
        "consequence_prompt_visible": consequence_prompt_visible,
        "authoritative_outcome": dict(result.get("consequence") or {}),
        "objective_scores": {
            item["id"]: runtime._score_trajectory_details(item)["objective_score"]
            for item in candidates
        },
    }


def run_benchmark() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        preserve_field, recover_field, ablated_field = _build_candidate_field(root)
        candidates = _candidates(
            preserve_field,
            recover_field,
            ablated_field,
        )

        intact = _run_condition(
            root,
            label="primary-host-intact",
            candidates=candidates,
            ablate=False,
        )
        ablated = _run_condition(
            root,
            label="primary-host-ablated",
            candidates=candidates,
            ablate=True,
        )

        summary = {
            "same_initial_selection": intact["initial"] == ablated["initial"],
            "intact_changes_next_selection": intact["next"] != intact["initial"],
            "ablation_selects_explicit_control": (
                ablated["next"] == "substrate-ablated"
            ),
            "causal_divergence": intact["next"] != ablated["next"],
            "intact_restart_persistence": (
                intact["after_restart"] == intact["next"]
            ),
            "ablation_restart_persistence": (
                ablated["after_restart"] == ablated["next"]
            ),
            "intact_field_restart_persistence": (
                intact["field_after_restart_distance"] < 0.002
            ),
            "ablation_field_restart_persistence": (
                ablated["field_after_restart_distance"] < 0.002
            ),
            "consequence_prompt_visible": (
                intact["consequence_prompt_visible"]
                and ablated["consequence_prompt_visible"]
            ),
            "authoritative_outcome_present": (
                intact["authoritative_outcome"].get("status") == "success"
                and ablated["authoritative_outcome"].get("status") == "success"
            ),
            "objective_channel_equal": (
                intact["objective_scores"] == ablated["objective_scores"]
            ),
        }

        result = {
            "protocol": {
                "path": (
                    "subjective substrate -> SubjectiveField -> host model "
                    "boundary -> action -> authoritative consequence -> "
                    "post-action subjective re-entry"
                ),
                "same_external_probe": True,
                "matched_objective_channel": True,
                "phenomenal_consciousness_claim": False,
            },
            "thresholds": {
                "causal_divergence": True,
                "restart_field_distance": "< 0.002",
            },
            "intact": intact,
            "ablated": ablated,
            "summary": summary,
            "all_pass": all(summary.values()),
        }

        print(json.dumps(result, indent=2, sort_keys=True))
        if not result["all_pass"]:
            raise AssertionError(
                "primary subjective host bridge causal gate failed"
            )
        print("PRIMARY SUBJECTIVE HOST BRIDGE V1: PASS")
        return result


if __name__ == "__main__":
    run_benchmark()
