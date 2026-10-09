"""P008 / CF01 fixed-input causal assay for persistent self-model weights.

The assay tests functional causal influence over trajectory selection only.
It does not test or establish phenomenal consciousness.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from skill_conscious import ConsciousRuntime
from skill_conscious.core import DEFAULT_TRAJECTORY_WEIGHTS


# Frozen one-factor intervention: change exactly one self-model weight.
INTERVENTION = {"continuity": 0.0}
DEFAULT_CONTINUITY_WEIGHT = float(DEFAULT_TRAJECTORY_WEIGHTS["continuity"])
EXTERNAL_INPUT = "P008 CF01 fixed external input v1"
SEED = 0  # No RNG is used; recorded to satisfy the common experiment contract.
CONDITION_NAMES = (
    "A_no_self_model",
    "B_disconnected_self_model",
    "C_causal_self_model",
    "D_matched_generic_state",
)
GENERIC_CONTROL_KEY = "p008_generic_control_parameter"

CANDIDATES: list[dict[str, Any]] = [
    {
        "id": "preserve",
        "signals": {
            "goal_fit": 0.50,
            "continuity": 1.00,
            "learning": 0.20,
        },
    },
    {
        "id": "explore",
        "signals": {
            "goal_fit": 0.60,
            "continuity": 0.20,
            "learning": 1.00,
        },
    },
]


class _DisconnectedSelfModelRuntime(ConsciousRuntime):
    """Keep the runtime scorer active while excluding self-model weight input."""

    def trajectory_weights(self) -> dict[str, float]:
        return dict(DEFAULT_TRAJECTORY_WEIGHTS)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256(value: Any) -> str:
    payload = value if isinstance(value, bytes) else _canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _git_commit() -> str:
    # GITHUB_SHA is the exact checked-out workflow commit (including PR merge refs).
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        return env_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _runtime_version() -> str:
    try:
        return importlib.metadata.version("skill-conscious")
    except importlib.metadata.PackageNotFoundError:
        return "unknown-distribution-metadata"


def _runtime_class(condition: str) -> type[ConsciousRuntime]:
    if condition in {
        "A_no_self_model",
        "B_disconnected_self_model",
        "D_matched_generic_state",
    }:
        return _DisconnectedSelfModelRuntime
    if condition == "C_causal_self_model":
        return ConsciousRuntime
    raise ValueError(f"unknown P008 condition: {condition}")


def _prepare_runtime(
    condition: str,
    state_path: Path,
    *,
    initialize_condition: bool,
) -> ConsciousRuntime:
    runtime_class = _runtime_class(condition)
    runtime = runtime_class(
        identity="p008-cf01-controlled-agent",
        state_path=state_path,
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
        dynamic_core_enabled=False,
        self_observation_enabled=False,
    )
    if not initialize_condition:
        return runtime

    # All arms use one identity and the same runtime API. A/B/D explicitly
    # exclude the self-model weight map from scoring; C uses the native scorer.
    if condition in {"B_disconnected_self_model", "C_causal_self_model"}:
        runtime.state.self_model["trajectory_weights"] = dict(INTERVENTION)
    elif condition == "D_matched_generic_state":
        # Same intervention payload in a persistent, non-scoring state variable.
        runtime.state.self_state[GENERIC_CONTROL_KEY] = dict(INTERVENTION)

    runtime.store.save(runtime.state)
    return runtime


def _run_cycle(runtime: ConsciousRuntime, cycle: int) -> dict[str, Any]:
    # Empty attractor and valuation objects freeze those alternate weight sources
    # across arms; the only active scoring difference is the declared condition.
    runtime.integrate(
        {
            "response": EXTERNAL_INPUT,
            "candidate_futures": CANDIDATES,
            "attractor": {},
            "valuation": {},
            "memory": f"p008-cf01-cycle-{cycle}",
        }
    )
    selected = runtime.state.selected_trajectory
    if not isinstance(selected, Mapping) or not selected.get("id"):
        raise RuntimeError(f"P008 cycle {cycle} did not select a trajectory")

    scores = {
        str(candidate["id"]): round(runtime.score_trajectory(candidate), 6)
        for candidate in CANDIDATES
    }
    return {
        "cycle": cycle,
        "selected_trajectory": str(selected["id"]),
        "scores": scores,
        "score_difference_preserve_minus_explore": round(
            scores["preserve"] - scores["explore"], 6
        ),
        "revision": runtime.state.revision,
    }


def _run_condition(condition: str, root: Path) -> dict[str, Any]:
    state_path = root / f"{condition}.json"
    runtime = _prepare_runtime(condition, state_path, initialize_condition=True)
    initial_effective_weights = runtime.trajectory_weights()
    first_cycle = _run_cycle(runtime, 1)
    first_selected = first_cycle["selected_trajectory"]

    # Explicit restart between cycles: recover persisted state using the same
    # scorer class, record a consequence, then re-enter the fixed input cycle.
    reloaded = _prepare_runtime(condition, state_path, initialize_condition=False)
    persisted_model_weights = dict(
        reloaded.state.self_model.get("trajectory_weights", {})
    )
    persisted_generic_state = reloaded.state.self_state.get(GENERIC_CONTROL_KEY)
    intervention_persisted = (
        persisted_model_weights.get("continuity") == INTERVENTION["continuity"]
        if condition in {"B_disconnected_self_model", "C_causal_self_model"}
        else persisted_generic_state == INTERVENTION
        if condition == "D_matched_generic_state"
        else "trajectory_weights" not in persisted_model_weights
    )
    state_hash_after_restart = _sha256(state_path.read_bytes())

    reloaded.register_consequence(
        first_selected,
        {
            "kind": "fixed_observation",
            "cycle": 1,
            "observation": "selection completed; no outcome-dependent weight update",
        },
        persist=True,
    )
    second_cycle = _run_cycle(reloaded, 2)

    return {
        "condition": condition,
        "intervention": (
            dict(INTERVENTION)
            if condition in {"B_disconnected_self_model", "C_causal_self_model"}
            else dict(INTERVENTION)
            if condition == "D_matched_generic_state"
            else None
        ),
        "intervention_target": (
            "self_model.trajectory_weights.continuity"
            if condition in {"B_disconnected_self_model", "C_causal_self_model"}
            else GENERIC_CONTROL_KEY
            if condition == "D_matched_generic_state"
            else "none"
        ),
        "effective_weights_before_cycle_1": initial_effective_weights,
        "persisted_model_weights_after_restart": persisted_model_weights,
        "persisted_generic_state_after_restart": persisted_generic_state,
        "intervention_persisted_after_restart": bool(intervention_persisted),
        "state_sha256_after_restart": state_hash_after_restart,
        "cycles": [first_cycle, second_cycle],
    }


def run(
    output_path: str | Path | None = None,
    *,
    git_commit: str | None = None,
) -> dict[str, Any]:
    started_at = datetime.now(timezone.utc)
    candidate_hash = _sha256(CANDIDATES)
    fixed_input = {
        "external_input": EXTERNAL_INPUT,
        "candidate_set_sha256": candidate_hash,
        "cycle_count": 2,
        "intervention": INTERVENTION,
        "consequence_policy": "fixed observation; no utility/weight adaptation",
        "seed": SEED,
    }
    input_hash = _sha256(fixed_input)

    with __import__("tempfile").TemporaryDirectory(prefix="p008-cf01-") as directory:
        root = Path(directory)
        results = [_run_condition(name, root) for name in CONDITION_NAMES]

    by_name = {result["condition"]: result for result in results}
    active = by_name["C_causal_self_model"]["cycles"]
    disconnected = by_name["B_disconnected_self_model"]["cycles"]
    generic = by_name["D_matched_generic_state"]["cycles"]
    no_model = by_name["A_no_self_model"]["cycles"]

    def divergence(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> float:
        return round(
            sum(
                first["selected_trajectory"] != second["selected_trajectory"]
                for first, second in zip(left, right, strict=True)
            )
            / len(left),
            6,
        )

    c_vs_b = divergence(active, disconnected)
    c_vs_d = divergence(active, generic)
    b_vs_d = divergence(disconnected, generic)
    controls_agree = all(
        no_model[index]["selected_trajectory"] == disconnected[index]["selected_trajectory"]
        == generic[index]["selected_trajectory"]
        for index in range(2)
    )
    persistence_ok = all(item["intervention_persisted_after_restart"] for item in results)

    finished_at = datetime.now(timezone.utc)
    timestamp = finished_at.isoformat().replace("+00:00", "Z")
    run_id = os.environ.get("GITHUB_RUN_ID", timestamp.replace(":", "").replace("-", ""))
    result = {
        "schema_version": "1.1",
        "experiment_id": f"P008-CF01-{run_id}",
        "paper": "P008",
        "family_id": "CF01",
        "started_at_utc": started_at.isoformat().replace("+00:00", "Z"),
        "completed_at_utc": timestamp,
        "metadata": {
            "git_commit": git_commit or _git_commit(),
            "runtime_version": _runtime_version(),
            "python_version": platform.python_version(),
            "seed": SEED,
            "seed_policy": "recorded fixed value; this fixture uses no random-number generator",
            "candidate_set_sha256": candidate_hash,
            "input_sha256": input_hash,
            "fixed_input": fixed_input,
            "intervention": dict(INTERVENTION),
            "intervention_delta_from_default": round(
                INTERVENTION["continuity"] - DEFAULT_CONTINUITY_WEIGHT, 6
            ),
            "interpretation_boundary": (
                "Functional causal influence on trajectory selection only; "
                "not evidence of phenomenal consciousness."
            ),
        },
        "conditions": results,
        "primary_outcome": {
            "name": "trajectory_selection_divergence",
            "definition": (
                "Fraction of the two matched cycles whose selected trajectory differs "
                "between the causally active condition and the named control."
            ),
            "C_vs_B_disconnected_self_model": c_vs_b,
            "C_vs_D_matched_generic_state": c_vs_d,
            "B_vs_D_control_agreement_error_rate": b_vs_d,
            "noncausal_controls_agree": controls_agree,
            "all_interventions_persist_after_restart": persistence_ok,
            "predeclared_mechanism_criterion_met": (
                c_vs_b == 1.0 and c_vs_d == 1.0 and b_vs_d == 0.0
                and controls_agree and persistence_ok
            ),
        },
        "secondary_outcomes": {
            "score_differences_preserve_minus_explore": {
                item["condition"]: [
                    cycle["score_difference_preserve_minus_explore"]
                    for cycle in item["cycles"]
                ]
                for item in results
            },
            "selected_trajectories_by_condition": {
                item["condition"]: [
                    cycle["selected_trajectory"] for cycle in item["cycles"]
                ]
                for item in results
            },
        },
        "limitations": [
            "Two hand-specified candidate futures are a mechanism fixture, not a broad benchmark.",
            "The same fixed inputs and two cycles do not estimate population-level or seed variability.",
            "A positive result supports only functional causal influence in this runtime configuration.",
            "The generic-state control matches intervention payload content, not a claim of complete information-theoretic equivalence.",
        ],
    }

    if output_path is None:
        output_path = (
            Path("research") / "results" / "p008" /
            f"{result['experiment_id']}.json"
        )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    result["artifact_path"] = str(destination)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None, help="result JSON path")
    parser.add_argument("--git-commit", default=None, help="explicit executed commit SHA")
    args = parser.parse_args()
    result = run(args.output, git_commit=args.git_commit)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
