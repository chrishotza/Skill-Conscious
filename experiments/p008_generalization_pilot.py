"""P008 generalization development PILOT. Never executes reserved holdout IDs."""
from __future__ import annotations
import argparse
import hashlib
import inspect
import json
import math
import platform
import random
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from experiments.p008_self_model_causal_runtime import (
    CONDITION_NAMES, GENERIC_CONTROL_KEY, INTERVENTION,
    _runtime_class, _git_commit, _runtime_version, _sha256,
)
from skill_conscious.core import DEFAULT_TRAJECTORY_WEIGHTS

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research/p008_generalization_protocol_v1.json"
PILOT_IDS = range(32)
FIXED_OUTCOME = {"kind": "fixed_observation", "observation": "selection complete"}
BOOTSTRAP_SEED = 20261016


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    path.write_text(content, encoding="utf-8")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def generate_scenario(scenario_id):
    """The ID guard is intentional: no research holdout access here."""
    if type(scenario_id) is not int or scenario_id not in PILOT_IDS:
        raise ValueError("Pilot scenarios 0..31 only; holdout is locked")
    rng = random.Random(scenario_id)
    candidates = [
        {"id": f"candidate_{i}", "signals": {
            signal: round(rng.random(), 8)
            for signal in ("goal_fit", "continuity", "learning", "risk")
        }}
        for i in range(2)
    ]
    return {"scenario_id": scenario_id, "seed": scenario_id,
            "split": "pilot", "external_input": f"P008 PILOT scenario {scenario_id}",
            "candidates": candidates}


def _runtime(condition, path, *, initialize):
    runtime = _runtime_class(condition)(
        identity="p008-generalization-agent", state_path=path,
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
        self_observation_enabled=False, dynamic_core_enabled=False,
    )
    if initialize:
        if condition in ("B_disconnected_self_model", "C_causal_self_model"):
            runtime.state.self_model["trajectory_weights"] = dict(INTERVENTION)
        elif condition == "D_matched_generic_state":
            runtime.state.self_state[GENERIC_CONTROL_KEY] = dict(INTERVENTION)
        runtime.store.save(runtime.state)
    return runtime


def _verify_weights(runtime, condition):
    expected = dict(DEFAULT_TRAJECTORY_WEIGHTS)
    if condition == "C_causal_self_model":
        expected["continuity"] = 0.0
    if runtime.trajectory_weights() != expected:
        raise ValueError(f"Invalid weight isolation in {condition}")
    stored = runtime.state.self_model.get("trajectory_weights", {})
    generic = runtime.state.self_state.get(GENERIC_CONTROL_KEY)
    if condition in ("B_disconnected_self_model", "C_causal_self_model"):
        valid = stored == INTERVENTION and generic is None
    elif condition == "D_matched_generic_state":
        valid = not stored and generic == INTERVENTION
    else:
        valid = not stored and generic is None
    if not valid:
        raise ValueError(f"Invalid persistent state in {condition}")


def _cycle(runtime, scenario, cycle):
    runtime.integrate({
        "response": scenario["external_input"],
        "candidate_futures": scenario["candidates"],
        "valuation": {}, "attractor": {},
        "memory": f"p008-pilot-cycle-{cycle}",
    })
    selected = runtime.state.selected_trajectory
    if not isinstance(selected, dict) or selected.get("id") not in ("candidate_0", "candidate_1"):
        raise ValueError("No valid trajectory selection")
    scores = [runtime.score_trajectory(item) for item in scenario["candidates"]]
    if not all(math.isfinite(score) for score in scores):
        raise ValueError("Nonfinite score")
    return {"selected": selected["id"], "scores": scores,
            "score_margin": round(scores[0] - scores[1], 6),
            "revision": runtime.state.revision}


def run_arm(condition, scenario, folder, metadata):
    path = folder / (condition + ".json")
    runtime = _runtime(condition, path, initialize=True)
    _verify_weights(runtime, condition)
    weights = runtime.trajectory_weights()
    first = _cycle(runtime, scenario, 1)
    restarted = _runtime(condition, path, initialize=False)
    _verify_weights(restarted, condition)
    restart_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    restarted.register_consequence(first["selected"], FIXED_OUTCOME, persist=True)
    second = _cycle(restarted, scenario, 2)
    _verify_weights(restarted, condition)
    return {
        **metadata, "scenario_id": scenario["scenario_id"],
        "split": scenario["split"], "seed": scenario["seed"],
        "condition": condition,
        "external_input_sha256": _sha256(scenario["external_input"]),
        "candidate_set_sha256": _sha256(scenario["candidates"]),
        "intervention_payload": None if condition == "A_no_self_model" else dict(INTERVENTION),
        "effective_weights": weights,
        "selected_trajectory_each_cycle": [first["selected"], second["selected"]],
        "score_margin_each_cycle": [first["score_margin"], second["score_margin"]],
        "cycle_details": [first, second],
        "restart_integrity": True, "state_sha256_after_restart": restart_sha,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def _pair_rate(arms, a, b):
    left = arms[a]["selected_trajectory_each_cycle"]
    right = arms[b]["selected_trajectory_each_cycle"]
    return sum(x != y for x, y in zip(left, right, strict=True)) / 2


def _bootstrap(values):
    rng = random.Random(BOOTSTRAP_SEED)
    size = len(values)
    estimates = sorted(
        sum(values[rng.randrange(size)] for _ in range(size)) / size
        for _ in range(2000)
    )
    return {"mean": round(sum(values) / size, 6),
            "ci_95": [round(estimates[49], 6), round(estimates[1949], 6)],
            "unit": "scenario", "bootstrap_seed": BOOTSTRAP_SEED,
            "replicates": 2000}


def audit(folder):
    folder = Path(folder)
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if not manifest["files"] or len(manifest["scenarios"]) != manifest["pilot_count"]:
        raise ValueError("Incomplete pilot manifest")
    for rel, expected in manifest["files"].items():
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise ValueError("Invalid manifest path")
        data = (folder / rel).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"SHA-256 mismatch: {rel}")
    for scenario_id in manifest["scenarios"]:
        sub = folder / f"scenario-{scenario_id:03d}"
        scenario = json.loads((sub / "input.json").read_text(encoding="utf-8"))
        selections = {}
        for arm in CONDITION_NAMES:
            row = json.loads((sub / f"{arm}.json").read_text(encoding="utf-8"))
            if (row["scenario_id"] != scenario_id or row["condition"] != arm
                or row["external_input_sha256"] != _sha256(scenario["external_input"])
                or row["candidate_set_sha256"] != _sha256(scenario["candidates"])
                or not row["restart_integrity"]
                or len(row["selected_trajectory_each_cycle"]) != 2):
                raise ValueError("Control/persistence integrity violation")
            weights = dict(DEFAULT_TRAJECTORY_WEIGHTS)
            if arm == "C_causal_self_model":
                weights["continuity"] = 0.0
            if row["effective_weights"] != weights:
                raise ValueError("Effective weights differ from protocol")
            selections[arm] = row["selected_trajectory_each_cycle"]
        if not (selections["A_no_self_model"]
                == selections["B_disconnected_self_model"]
                == selections["D_matched_generic_state"]):
            raise ValueError("Disconnected control mismatch")
    return manifest


def run_pilot(folder, *, count=32):
    if type(count) is not int or not 1 <= count <= 32:
        raise ValueError("pilot count must be 1..32")
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if protocol["status"] not in ("DRAFT_NOT_FROZEN_NOT_EXECUTED", "DRAFT_PILOT_HARNESS_UNFROZEN"):
        raise RuntimeError("Protocol status changed: pilot must be reviewed")
    if tuple(protocol["conditions"]) != CONDITION_NAMES:
        raise RuntimeError("Arm registration differs")
    folder = Path(folder)
    if folder.exists() and any(folder.iterdir()):
        raise FileExistsError("Pilot evidence directory is not empty")
    folder.mkdir(parents=True, exist_ok=True)
    metadata = {
        "git_commit": _git_commit(), "runtime_version": _runtime_version(),
        "python_version": platform.python_version(),
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "generator_sha256": hashlib.sha256(
            inspect.getsource(generate_scenario).encode("utf-8")
        ).hexdigest(),
    }
    samples = {"C_vs_B": [], "C_vs_D": [], "B_vs_D": [], "A_vs_B": []}
    hashes = {}
    for scenario_id in range(count):
        scenario = generate_scenario(scenario_id)
        sub = f"scenario-{scenario_id:03d}"
        hashes[f"{sub}/input.json"] = _write_json(folder / sub / "input.json", scenario)
        arms = {}
        with tempfile.TemporaryDirectory(prefix="p008-pilot-") as temp:
            for arm in CONDITION_NAMES:
                row = run_arm(arm, scenario, Path(temp), metadata)
                arms[arm] = row
                hashes[f"{sub}/{arm}.json"] = _write_json(
                    folder / sub / f"{arm}.json", row
                )
        samples["C_vs_B"].append(_pair_rate(arms, "C_causal_self_model", "B_disconnected_self_model"))
        samples["C_vs_D"].append(_pair_rate(arms, "C_causal_self_model", "D_matched_generic_state"))
        samples["B_vs_D"].append(_pair_rate(arms, "B_disconnected_self_model", "D_matched_generic_state"))
        samples["A_vs_B"].append(_pair_rate(arms, "A_no_self_model", "B_disconnected_self_model"))
    manifest = {
        **metadata, "study_id": protocol["study_id"],
        "status": "EXPLORATORY_PILOT_NOT_CONFIRMATORY", "split": "pilot",
        "pilot_count": count, "scenarios": list(range(count)),
        "conditions": list(CONDITION_NAMES), "cycles_per_arm": 2,
        "metrics": {name: _bootstrap(values) for name, values in samples.items()},
        "files": hashes, "holdout_accessed": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "interpretation_boundary": "Synthetic software mechanism only; not consciousness",
    }
    _write_json(folder / "manifest.json", manifest)
    audit(folder)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--pilot-output", type=Path)
    modes.add_argument("--audit", type=Path)
    parser.add_argument("--pilot-count", type=int, default=32)
    args = parser.parse_args()
    result = audit(args.audit) if args.audit else run_pilot(args.pilot_output, count=args.pilot_count)
    print(json.dumps({"status": result["status"], "pilot_count": result["pilot_count"],
                      "metrics": result["metrics"], "holdout_accessed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
