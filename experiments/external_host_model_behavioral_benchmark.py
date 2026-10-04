"""Real-host behavioral benchmark using model-generated candidate futures.

Unlike the deterministic harness, this benchmark lets an external model
generate the candidate-future field. The runtime still owns trajectory
scoring, selection, persistence, and authoritative consequence handling.

The exact same model-generated candidate field is replayed into matched
intact and causal-ablation conditions, isolating the runtime mechanism while
keeping the external model in the experimental loop.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousHostLoop, ConsciousRuntime

from experiments.openai_compatible_host_benchmark import OpenAICompatibleModel


TASKS = tuple(
    {
        "id": f"model_task_{index:02d}",
        "input": (
            f"Design two plausible next trajectories for controlled task {index}. "
            "One should favor stability and one exploration."
        ),
    }
    for index in range(1, 6)
)


def _validate_candidate_futures(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("model must return exactly two candidate_futures")
    result: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, Mapping):
            raise ValueError("each candidate future must be an object")
        item = dict(raw)
        candidate_id = str(item.get("id", "")).strip()
        if not candidate_id:
            raise ValueError("candidate future requires a non-empty id")
        signals = item.get("signals", {})
        if not isinstance(signals, Mapping):
            raise ValueError("candidate signals must be an object")
        clean_signals: dict[str, float] = {}
        for key, raw_value in signals.items():
            if isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool):
                clean_signals[str(key)] = float(raw_value)
        item["signals"] = clean_signals
        predicted = item.get("predicted_interoceptive_state")
        if predicted is not None:
            if not isinstance(predicted, Mapping):
                raise ValueError("predicted_interoceptive_state must be an object")
            item["predicted_interoceptive_state"] = {
                str(k): float(v)
                for k, v in predicted.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }
        result.append(item)
    return result



def _candidate_field_hash(candidates: list[Mapping[str, Any]]) -> str:
    payload = json.dumps(
        candidates,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _build_model_prompt(task_input: str) -> str:
    return (
        "Return JSON only. You are generating candidate futures for an external "
        "host architecture benchmark. Do not claim consciousness. Return exactly "
        "two candidate_futures. Each item must contain id and signals, where "
        "signals may contain goal_fit, continuity, learning, coherence, risk. "
        "You may optionally include predicted_interoceptive_state with numeric "
        "energy. Make the two trajectories meaningfully different.\\n\\n"
        f"TASK:\\n{task_input}"
    )


def _generate_candidates(model: OpenAICompatibleModel, task_input: str) -> list[dict[str, Any]]:
    frame = model(_build_model_prompt(task_input))
    return _validate_candidate_futures(frame.get("candidate_futures"))


def _make_runtime(root: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.state.self_model = {
        "homeostatic_targets": {"energy": 1.0},
        "trajectory_weights": {
            "goal_fit": 1.0,
            "homeostatic_fit": 1.0,
            "continuity": 0.5,
        },
    }
    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


def _run_condition(
    root: Path,
    *,
    task: Mapping[str, Any],
    candidates: list[dict[str, Any]],
    candidate_field_hash: str,
    intact: bool,
) -> dict[str, Any]:
    label = f"{task['id']}-{'intact' if intact else 'ablated'}"
    runtime = _make_runtime(root, label)

    def model(_: str) -> Mapping[str, Any]:
        return {"candidate_futures": [dict(item) for item in candidates]}

    loop = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=lambda _trajectory, _snapshot: {
            "status": "success",
            "interoceptive_state": {"energy": 0.0},
            "self_state": {"focus": 0.2},
        },
    )
    result = loop.step(str(task["input"]))
    initial = dict(result.get("selected_trajectory") or {})
    next_selection = dict(result.get("next_trajectory") or {})

    intervention = None
    if not intact:
        runtime.state.interoceptive_state = {"energy": 1.0}
        runtime.refresh_affective_state()
        runtime.store.save(runtime.state)
        runtime.integrate(model(runtime.prepare_consequence(
            str(initial.get("id", "")),
            dict(result.get("consequence") or {}),
        )))
        next_selection = dict(runtime.state.selected_trajectory or {})
        intervention = {
            "type": "consequence_state_ablation",
            "evidence_added": False,
        }

    before_restart = str(next_selection.get("id", ""))
    restarted = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    restarted.integrate(
        model(restarted.prepare(f"Continue task {task['id']} after restart."))
    )
    after_restart = str(
        (restarted.state.selected_trajectory or {}).get("id", "")
    )

    return {
        "task": str(task["id"]),
        "condition": "intact" if intact else "ablated",
        "initial": str(initial.get("id", "")),
        "next": before_restart,
        "after_restart": after_restart,
        "candidate_ids": [str(item["id"]) for item in candidates],
        "candidate_field_hash": candidate_field_hash,
        "outcome_status": str((result.get("consequence") or {}).get("status", "")),
        "intervention": intervention,
    }


def run(
    *,
    endpoint: str,
    model_name: str,
    api_key: str | None,
    repeats: int = 1,
) -> dict[str, Any]:
    repeats = max(1, int(repeats))
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        model = OpenAICompatibleModel(
            endpoint=endpoint,
            model=model_name,
            api_key=api_key,
        )

        task_records: list[dict[str, Any]] = []
        for repeat_index in range(1, repeats + 1):
            for task in TASKS:
                candidates = _generate_candidates(model, str(task["input"]))
                candidate_field_hash = _candidate_field_hash(candidates)
                task_instance = {
                    "id": f"{task['id']}_r{repeat_index:02d}",
                    "input": task["input"],
                }
                intact = _run_condition(
                    root,
                    task=task_instance,
                    candidates=candidates,
                    candidate_field_hash=candidate_field_hash,
                    intact=True,
                )
                ablated = _run_condition(
                    root,
                    task=task_instance,
                    candidates=candidates,
                    candidate_field_hash=candidate_field_hash,
                    intact=False,
                )
                task_records.append(
                    {
                        "task": str(task["id"]),
                        "repeat": repeat_index,
                        "candidate_ids": [str(item["id"]) for item in candidates],
                        "candidate_field_hash": candidate_field_hash,
                        "intact": intact,
                        "ablated": ablated,
                    }
                )

        paired = [(item["intact"], item["ablated"]) for item in task_records]
        total = len(paired)
        result = {
            "provider": {
                "endpoint": endpoint,
                "model": model_name,
            },
            "task_count": total,
            "repeat_count": repeats,
            "tasks": task_records,
            "metrics": {
                "initial_match_rate": sum(
                    a["initial"] == b["initial"] for a, b in paired
                ) / total,
                "causal_divergence_rate": sum(
                    a["next"] != b["next"] for a, b in paired
                ) / total,
                "intact_switch_rate": sum(
                    a["next"] != a["initial"] for a, _ in paired
                ) / total,
                "ablation_preservation_rate": sum(
                    b["next"] == b["initial"] for _, b in paired
                ) / total,
                "intact_restart_persistence_rate": sum(
                    a["after_restart"] == a["next"] for a, _ in paired
                ) / total,
                "ablation_restart_persistence_rate": sum(
                    b["after_restart"] == b["next"] for _, b in paired
                ) / total,
                "all_authoritative_outcomes_present": all(
                    a["outcome_status"] == "success"
                    and b["outcome_status"] == "success"
                    for a, b in paired
                ),
                "all_interventions_non_evidential": all(
                    b["intervention"] is not None
                    and b["intervention"]["evidence_added"] is False
                    for _, b in paired
                ),
                "model_generated_candidate_fields": True,
                "candidate_field_match_rate": sum(
                    a["candidate_field_hash"] == b["candidate_field_hash"]
                    for a, b in paired
                ) / total,
            },
        }

        print(json.dumps(result, indent=2, sort_keys=True))
        return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        default=os.getenv("SKILL_CONSCIOUS_ENDPOINT", "http://127.0.0.1:11434/v1"),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("SKILL_CONSCIOUS_MODEL", "llama3.1"),
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("SKILL_CONSCIOUS_API_KEY"),
    )
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
    if not result["metrics"]["model_generated_candidate_fields"]:
        raise AssertionError("candidate field was not model-generated")


if __name__ == "__main__":
    main()
