"""Temporal recurrence causal benchmark.

The experimental and control histories contain the same states, same multiplicity,
same final state, same cycle count and the same candidate field. Only temporal
arrangement differs.

The causal probe is opt-in predicted_self_state scoring through the
runtime-owned learned_self_fit signal. The benchmark then ablates, restores,
and restarts the latent-self profile without injecting learning evidence.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from skill_conscious import ConsciousRuntime


STATE_A = {"stability": 0.0, "focus": 0.0}
STATE_B = {"stability": 1.0, "focus": 0.0}
STATE_C = {"stability": 0.0, "focus": 1.0}
STATE_D = {"stability": 1.0, "focus": 1.0}

STRUCTURED_SEQUENCE = [STATE_A, STATE_B, STATE_C, STATE_D, STATE_A]
CONTROL_SEQUENCE = [STATE_B, STATE_C, STATE_D, STATE_A, STATE_A]

CANDIDATES: list[dict[str, Any]] = [
    {
        "id": "alpha_path",
        "signals": {
            "goal_fit": 0.5,
            "self_alignment": 0.5,
            "continuity": 0.5,
            "learning": 0.5,
            "risk": 0.5,
            "uncertainty": 0.5,
        },
        "predicted_self_state": dict(STATE_A),
    },
    {
        "id": "beta_path",
        "signals": {
            "goal_fit": 0.5,
            "self_alignment": 0.5,
            "continuity": 0.5,
            "learning": 0.5,
            "risk": 0.5,
            "uncertainty": 0.5,
        },
        "predicted_self_state": dict(STATE_B),
    },
]


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _runtime(root: Path, name: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        name,
        state_path=root / f"{name}.json",
        report_enabled=False,
        metacognition_enabled=False,
        self_observation_enabled=False,
        learn_latent_patterns=True,
        learn_self_model_from_latent_patterns=True,
    )
    runtime.state.self_model = {
        "trajectory_weights": {
            "learned_self_fit": 1.0,
        },
        "latent_self_model_learning_rate": 0.1,
    }
    runtime.state.interoceptive_state = {}
    runtime.state.self_state = {}
    runtime.store.save(runtime.state)
    return runtime


def _cycle(
    runtime: ConsciousRuntime,
    index: int,
    self_state: Mapping[str, float],
) -> dict[str, Any]:
    runtime.integrate(
        {
            "response": "",
            "internal_state": dict(self_state),
            "candidate_futures": [dict(item) for item in CANDIDATES],
            "memory": f"matched-memory-{index}",
        }
    )
    return dict(runtime.state.selected_trajectory or {})


def _profile_evidence_counts(profile: Mapping[str, Any]) -> dict[str, int]:
    raw = profile.get("latent_patterns", {})
    if not isinstance(raw, Mapping):
        return {}
    counts: dict[str, int] = {}
    for key, pattern in raw.items():
        if isinstance(pattern, Mapping):
            count = pattern.get("evidence_count", 0)
            if isinstance(count, int) and not isinstance(count, bool):
                counts[str(key)] = count
    return counts


def _run_condition(
    root: Path,
    name: str,
    sequence: list[Mapping[str, float]],
) -> dict[str, Any]:
    runtime = _runtime(root, name)
    selected: list[str] = []

    for index, state in enumerate(sequence):
        trajectory = _cycle(runtime, index, state)
        selected.append(str(trajectory.get("id", "")))

    profile = runtime.snapshot_latent_self_causal_profile()
    selected_before = str(runtime.state.selected_trajectory["id"])
    score_before = {
        item["id"]: runtime.score_trajectory(item)
        for item in CANDIDATES
    }

    history_count_before = len(runtime.state.history)
    memory_count_before = len(runtime.state.memories)
    revision_before = int(runtime.state.revision)
    candidate_hash = _canonical_hash(CANDIDATES)

    return {
        "runtime": runtime,
        "sequence": [dict(item) for item in sequence],
        "selected": selected,
        "selected_before": selected_before,
        "score_before": score_before,
        "profile": profile,
        "candidate_hash": candidate_hash,
        "history_count_before": history_count_before,
        "memory_count_before": memory_count_before,
        "revision_before": revision_before,
        "final_self_state": dict(runtime.state.self_state),
        "final_self_state_hash": _canonical_hash(runtime.state.self_state),
    }


def run() -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)

        structured = _run_condition(
            root,
            "structured",
            STRUCTURED_SEQUENCE,
        )
        control = _run_condition(
            root,
            "control",
            CONTROL_SEQUENCE,
        )

        structured_runtime: ConsciousRuntime = structured["runtime"]
        structured_profile = structured["profile"]

        ablation_profile = {
            "latent_patterns": {},
            "learned_self_state": {},
            "latent_tendencies": {},
            "pattern_markers": {},
        }
        revision_before_ablation = structured_runtime.state.revision
        history_before_ablation = len(structured_runtime.state.history)
        memories_before_ablation = len(structured_runtime.state.memories)

        ablation = structured_runtime.intervene_latent_self_causal_profile(
            ablation_profile,
            persist=False,
            intervention_id="temporal-recurrence-v1-ablation",
        )
        ablated_selection = structured_runtime.select_trajectory(
            [dict(item) for item in CANDIDATES]
        )["id"]

        ablation_preserved_runtime_counters = (
            structured_runtime.state.revision == revision_before_ablation
            and len(structured_runtime.state.history) == history_before_ablation
            and len(structured_runtime.state.memories) == memories_before_ablation
        )

        restore = structured_runtime.restore_latent_self_causal_profile(
            structured_profile,
            persist=True,
            intervention_id="temporal-recurrence-v1-ablation",
        )
        restored_selection = structured_runtime.select_trajectory(
            [dict(item) for item in CANDIDATES]
        )["id"]

        restarted = ConsciousRuntime(
            "structured",
            state_path=root / "structured.json",
            report_enabled=False,
            metacognition_enabled=False,
            self_observation_enabled=False,
        )
        restarted_selection = restarted.select_trajectory(
            [dict(item) for item in CANDIDATES]
        )["id"]
        restarted_profile = restarted.snapshot_latent_self_causal_profile()

        structured_pattern_keys = [
            key
            for key, pattern in structured_profile["latent_patterns"].items()
            if isinstance(pattern, Mapping)
            and pattern.get("source") == "endogenous"
        ]

        same_multiset = sorted(
            _canonical_hash(item)
            for item in STRUCTURED_SEQUENCE
        ) == sorted(
            _canonical_hash(item)
            for item in CONTROL_SEQUENCE
        )

        same_final_state = (
            structured["final_self_state"]
            == control["final_self_state"]
        )

        same_budget = (
            structured["revision_before"] == control["revision_before"]
            and structured["history_count_before"]
            == control["history_count_before"]
            and structured["memory_count_before"]
            == control["memory_count_before"]
        )

        same_candidate_field = (
            structured["candidate_hash"] == control["candidate_hash"]
        )

        recurrence_detected = bool(structured_pattern_keys)
        recurrence_absent_in_control = not any(
            isinstance(pattern, Mapping)
            and pattern.get("source") == "endogenous"
            for pattern in control["profile"]["latent_patterns"].values()
        )

        metrics = {
            "same_information_multiset": same_multiset,
            "same_final_self_state": same_final_state,
            "same_runtime_budget": same_budget,
            "same_candidate_field_hash": same_candidate_field,
            "structured_recurrence_detected": recurrence_detected,
            "control_recurrence_absent": recurrence_absent_in_control,
            "structured_selected_alpha": structured["selected_before"] == "alpha_path",
            "control_selected_beta": control["selected_before"] == "beta_path",
            "temporal_arrangement_changes_selection": (
                structured["selected_before"] != control["selected_before"]
            ),
            "structured_alpha_score_exceeds_beta": (
                structured["score_before"]["alpha_path"]
                > structured["score_before"]["beta_path"]
            ),
            "ablation_returns_to_control": ablated_selection == "beta_path",
            "restoration_recovers_structured": restored_selection == "alpha_path",
            "restart_persists_structured_selection": (
                restarted_selection == "alpha_path"
            ),
            "restart_restores_profile_exactly": (
                restarted_profile == structured_profile
            ),
            "intervention_non_evidential": (
                ablation["evidence_added"] is False
                and restore["evidence_added"] is False
            ),
            "intervention_preserves_revision_history_memory": (
                ablation_preserved_runtime_counters
            ),
            "profile_evidence_counts_restored": (
                _profile_evidence_counts(restarted_profile)
                == _profile_evidence_counts(structured_profile)
            ),
        }

        result = {
            "protocol": {
                "experimental": "A,B,C,D,A",
                "control": "B,C,D,A,A",
                "constraint": (
                    "same multiset + same final self-state + same cycle/revision "
                    "budget + same candidate field; only temporal order differs"
                ),
            },
            "candidate_field": {
                "hash": structured["candidate_hash"],
                "algorithm": "sha256-canonical-json-v1",
                "count": len(CANDIDATES),
            },
            "structured": {
                "selected": structured["selected"],
                "selected_before_ablation": structured["selected_before"],
                "scores_before_ablation": structured["score_before"],
                "latent_pattern_keys": structured_pattern_keys,
                "latent_profile": structured_profile,
                "final_self_state": structured["final_self_state"],
            },
            "control": {
                "selected": control["selected"],
                "selected_before_ablation": control["selected_before"],
                "scores": control["score_before"],
                "latent_profile": control["profile"],
                "final_self_state": control["final_self_state"],
            },
            "causal_probe": {
                "ablated_selection": str(ablated_selection),
                "restored_selection": str(restored_selection),
                "restarted_selection": str(restarted_selection),
                "ablation": ablation,
                "restore": restore,
            },
            "metrics": metrics,
            "interpretation": {
                "level": "C",
                "meaning": (
                    "Under matched information and candidate-field constraints, "
                    "temporal organization alone changes endogenous latent-self "
                    "state and downstream trajectory selection. Causal ablation "
                    "returns the matched control selection, restoration recovers "
                    "the experimental selection, and restart preserves it."
                ),
                "phenomenal_consciousness_claim": False,
            },
        }

        print(json.dumps(result, indent=2, sort_keys=True))

        if not all(metrics.values()):
            raise AssertionError(
                "temporal recurrence causal benchmark failed: "
                + json.dumps(metrics, sort_keys=True)
            )

        print("TEMPORAL RECURRENCE CAUSAL BENCHMARK v1: PASS")
        return result


if __name__ == "__main__":
    run()
