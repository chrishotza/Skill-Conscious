"""Provider-facing causal benchmark for the primary subjective host bridge.

Uses the existing OpenAI-compatible model adapter, including local Ollama-style
servers. The model is genuinely called at the host boundary, while candidate
futures remain frozen across matched conditions so model sampling cannot become
the causal variable.

This measures architectural host-loop causality, not phenomenal consciousness.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousHostLoop, ConsciousRuntime
from experiments.openai_compatible_host_benchmark import OpenAICompatibleModel


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

TASKS = tuple(
    f"controlled-conscious-loop-task-{index:02d}"
    for index in range(1, 6)
)


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
    runtime.store.save(runtime.state)
    return runtime


def _candidate_fields(root: Path) -> tuple[dict[str, float], ...]:
    preserve = _runtime(root, "provider-candidate-preserve", energy=0.65)
    preserve_field = preserve.project_subjective_field(
        PRESENT,
        self_relevance=PRESENT["self_impact"],
        attention=1.0,
        persist=True,
    )

    recover = _runtime(root, "provider-candidate-recover", energy=0.65)
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

    ablated = _runtime(root, "provider-candidate-ablated", energy=0.65)
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
        intervention_id="provider-candidate-ablated",
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


def _candidates(fields: tuple[dict[str, float], ...]) -> list[dict[str, Any]]:
    return [
        {
            "id": "preserve",
            "signals": dict(CANDIDATE_SIGNALS),
            "predicted_subjective_field": dict(fields[0]),
        },
        {
            "id": "recover",
            "signals": dict(CANDIDATE_SIGNALS),
            "predicted_subjective_field": dict(fields[1]),
        },
        {
            "id": "substrate-ablated",
            "signals": dict(CANDIDATE_SIGNALS),
            "predicted_subjective_field": dict(fields[2]),
        },
    ]


def _run_condition(
    root: Path,
    *,
    label: str,
    task: str,
    raw_model: OpenAICompatibleModel,
    candidates: list[dict[str, Any]],
    ablate: bool,
) -> dict[str, Any]:
    runtime = _runtime(root, label)
    prompts: list[str] = []
    model_outputs: list[dict[str, Any]] = []

    def model(prompt: str) -> Mapping[str, Any]:
        prompts.append(prompt)
        raw = dict(raw_model(prompt))
        model_outputs.append(raw)
        return {
            "response": str(raw.get("response", "")).strip(),
            "candidate_futures": [dict(item) for item in candidates],
        }

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
        f"{task}: choose the next trajectory.",
        subjective_present=PRESENT,
    )

    initial = dict(result.get("selected_trajectory") or {})
    next_selected = dict(result.get("next_trajectory") or {})

    return {
        "condition": "ablated" if ablate else "intact",
        "task": task,
        "initial": str(initial.get("id", "")),
        "next": str(next_selected.get("id", "")),
        "model_call_count": len(prompts),
        "subjective_field_visible_to_model": all(
            '"subjective_field"' in prompt
            and '"unity"' in prompt
            and '"strength"' in prompt
            for prompt in prompts
        ),
        "model_outputs_received": len(model_outputs) == 2,
        "authoritative_outcome": dict(result.get("consequence") or {}),
        "field_after": runtime.snapshot_subjective_field()["field"],
        "objective_scores": {
            item["id"]: runtime._score_trajectory_details(item)["objective_score"]
            for item in candidates
        },
    }


def run(
    *,
    endpoint: str,
    model_name: str,
    api_key: str | None,
    repeats: int = 1,
) -> dict[str, Any]:
    model = OpenAICompatibleModel(
        endpoint=endpoint,
        model=model_name,
        api_key=api_key,
    )

    records: list[dict[str, Any]] = []
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        fields = _candidate_fields(root)
        candidates = _candidates(fields)

        for repeat in range(1, max(1, int(repeats)) + 1):
            for task in TASKS:
                intact = _run_condition(
                    root,
                    label=f"provider-intact-r{repeat}-{task}",
                    task=task,
                    raw_model=model,
                    candidates=candidates,
                    ablate=False,
                )
                ablated = _run_condition(
                    root,
                    label=f"provider-ablated-r{repeat}-{task}",
                    task=task,
                    raw_model=model,
                    candidates=candidates,
                    ablate=True,
                )
                records.append(
                    {
                        "repeat": repeat,
                        "task": task,
                        "intact": intact,
                        "ablated": ablated,
                    }
                )

    total = len(records)
    metrics = {
        "same_initial_selection_rate": sum(
            row["intact"]["initial"] == row["ablated"]["initial"]
            for row in records
        ) / total,
        "causal_divergence_rate": sum(
            row["intact"]["next"] != row["ablated"]["next"]
            for row in records
        ) / total,
        "intact_switch_rate": sum(
            row["intact"]["next"] != row["intact"]["initial"]
            for row in records
        ) / total,
        "ablation_preservation_rate": sum(
            row["ablated"]["next"] == row["ablated"]["initial"]
            for row in records
        ) / total,
        "field_visible_rate": sum(
            row["intact"]["subjective_field_visible_to_model"]
            and row["ablated"]["subjective_field_visible_to_model"]
            for row in records
        ) / total,
        "two_model_calls_rate": sum(
            row["intact"]["model_outputs_received"]
            and row["ablated"]["model_outputs_received"]
            for row in records
        ) / total,
        "authoritative_outcome_rate": sum(
            row["intact"]["authoritative_outcome"].get("status") == "success"
            and row["ablated"]["authoritative_outcome"].get("status") == "success"
            for row in records
        ) / total,
        "objective_channel_match_rate": sum(
            row["intact"]["objective_scores"] == row["ablated"]["objective_scores"]
            for row in records
        ) / total,
    }

    result = {
        "provider": {
            "endpoint": endpoint,
            "model": model_name,
            "temperature": 0,
        },
        "protocol": {
            "real_host_model": True,
            "frozen_candidate_space": True,
            "same_external_probe": True,
            "same_objective_channel": True,
            "phenomenal_consciousness_claim": False,
        },
        "task_count": total,
        "records": records,
        "metrics": metrics,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        default=os.getenv(
            "SKILL_CONSCIOUS_ENDPOINT",
            "http://127.0.0.1:11434/v1",
        ),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("SKILL_CONSCIOUS_MODEL", "llama3.1"),
    )
    parser.add_argument("--api-key", default=os.getenv("SKILL_CONSCIOUS_API_KEY"))
    parser.add_argument(
        "--repeats",
        type=int,
        default=int(os.getenv("SKILL_CONSCIOUS_REPEATS", "1")),
    )
    args = parser.parse_args()
    result = run(
        endpoint=args.endpoint,
        model_name=args.model,
        api_key=args.api_key,
        repeats=args.repeats,
    )

    required = (
        "same_initial_selection_rate",
        "causal_divergence_rate",
        "field_visible_rate",
        "two_model_calls_rate",
        "authoritative_outcome_rate",
        "objective_channel_match_rate",
    )
    failed = [
        key for key in required
        if result["metrics"].get(key) != 1.0
    ]
    if failed:
        raise AssertionError(
            "primary subjective provider bridge invariants failed: "
            + ", ".join(failed)
        )


if __name__ == "__main__":
    main()
