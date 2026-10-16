from __future__ import annotations

import hashlib
import math
import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .ontology import CONSCIOUSNESS_DEFINITION
from .experience_field import ExperienceFieldProfile
from .runtime_bridge import ExperienceDynamicsBridge, RUNTIME_OWNED_KEYS
from .metacognition import (
    METACOGNITIVE_RUNTIME_KEYS,
    build_metacognitive_trace,
    state_delta,
)
from .metacognitive_prediction import (
    METACOGNITIVE_PREDICTION_RUNTIME_KEYS,
    compare_metacognitive_prediction,
)
from .self_observation import (
    SELF_OBSERVATION_RUNTIME_KEYS,
    SelfObservationProfile,
    blend_profiles,
    build_self_observation,
    profile_distance as self_observation_distance,
)


DEFAULT_REGIME_WEIGHTS: dict[str, float] = {
    "coherence": 1.0,
    "stability": 0.5,
    "uncertainty": 0.75,
    "self_dissonance": 1.25,
    "latent_pattern": 0.75,
    "learning": 0.25,
}

DEFAULT_TRAJECTORY_WEIGHTS: dict[str, float] = {
    "goal_fit": 1.0,
    "self_alignment": 1.0,
    "continuity": 1.0,
    "learning": 0.5,
    "risk": -1.0,
    "uncertainty": -0.5,
    "coherence": 1.0,
    "topology_integrity": 0.5,
    "salience": 0.25,
    "self_dissonance": -0.5,
    "latent_pattern": 0.5,
    "dissonance_resolution": 1.0,
    "homeostatic_fit": 0.75,
}


@dataclass
class ConsciousState:
    identity: str
    revision: int = 0
    self_state: dict[str, Any] = field(default_factory=dict)
    self_model: dict[str, Any] = field(default_factory=dict)
    workspace: dict[str, Any] = field(default_factory=dict)
    intention: str = ""
    memories: list[str] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    selected_trajectory: dict[str, Any] | None = None
    attention: list[str] = field(default_factory=list)
    salience: dict[str, float] = field(default_factory=dict)
    layers: dict[str, dict[str, Any]] = field(default_factory=dict)
    regime: str = "baseline"
    relation_topology: dict[str, list[str]] = field(default_factory=dict)
    attractor: dict[str, Any] | None = None
    valuation: dict[str, float] = field(default_factory=dict)
    valence: float = 0.0
    coherence: float = 1.0
    latent_patterns: dict[str, dict[str, Any]] = field(default_factory=dict)
    self_dissonance: float = 0.0
    interoceptive_state: dict[str, Any] = field(default_factory=dict)
    affective_state: dict[str, Any] = field(default_factory=dict)
    temporal_state: dict[str, Any] = field(default_factory=dict)
    perspectives: dict[str, dict[str, Any]] = field(default_factory=dict)
    transformation_log: list[dict[str, Any]] = field(default_factory=list)
    pending_action: dict[str, Any] | None = None
    action_history: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ConsciousState":
        return cls(
            identity=str(value["identity"]),
            revision=int(value.get("revision", 0)),
            self_state=dict(value.get("self_state", {})),
            self_model=dict(value.get("self_model", {})),
            workspace=dict(value.get("workspace", {})),
            intention=str(value.get("intention", "")),
            memories=[str(item) for item in value.get("memories", [])],
            history=[dict(item) for item in value.get("history", [])],
            selected_trajectory=(
                dict(value["selected_trajectory"])
                if value.get("selected_trajectory") is not None
                else None
            ),
            attention=[str(item) for item in value.get("attention", [])],
            salience={
                str(key): float(val)
                for key, val in dict(value.get("salience", {})).items()
                if isinstance(val, (int, float)) and not isinstance(val, bool)
            },
            layers={
                str(key): dict(layer)
                for key, layer in dict(value.get("layers", {})).items()
                if isinstance(layer, Mapping)
            },
            regime=str(value.get("regime", "baseline")),
            relation_topology={
                str(node): [str(target) for target in targets]
                for node, targets in dict(value.get("relation_topology", {})).items()
            },
            attractor=(
                dict(value["attractor"])
                if value.get("attractor") is not None
                else None
            ),
            valuation={
                str(key): float(val)
                for key, val in dict(value.get("valuation", {})).items()
                if isinstance(val, (int, float)) and not isinstance(val, bool)
            },
            valence=float(value.get("valence", 0.0)),
            coherence=max(0.0, min(1.0, float(value.get("coherence", 1.0)))),
            latent_patterns={
                str(key): dict(pattern)
                for key, pattern in dict(value.get("latent_patterns", {})).items()
                if isinstance(pattern, Mapping)
            },
            self_dissonance=max(0.0, min(1.0, float(value.get("self_dissonance", 0.0)))),
            interoceptive_state=dict(value.get("interoceptive_state", {})),
            affective_state=dict(value.get("affective_state", {})),
            temporal_state=dict(value.get("temporal_state", {})),
            perspectives={
                str(key): dict(item)
                for key, item in dict(value.get("perspectives", {})).items()
                if isinstance(item, Mapping)
            },
            transformation_log=[
                dict(item) for item in value.get("transformation_log", [])
            ],
            pending_action=(
                dict(value["pending_action"])
                if value.get("pending_action") is not None
                else None
            ),
            action_history=[
                dict(item) for item in value.get("action_history", [])
            ],
        )


class JsonStateStore:
    def __init__(self, path: str | os.PathLike[str]):
        self.path = Path(path)

    def load(self, identity: str) -> ConsciousState:
        if not self.path.exists():
            return ConsciousState(identity=identity)

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        state = ConsciousState.from_dict(payload)
        if state.identity != identity:
            raise ValueError(
                f"state identity mismatch: expected {identity!r}, got {state.identity!r}"
            )
        return state

    def save(self, state: ConsciousState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(
            prefix=".conscious-",
            suffix=".json",
            dir=self.path.parent,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(
                    state.to_dict(),
                    handle,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


class ConsciousRuntime:
    def __init__(
        self,
        identity: str,
        state_path: str | os.PathLike[str] = "data/consciousness.json",
        *,
        memory_limit: int = 32,
        history_limit: int = 64,
        learn_latent_patterns: bool = True,
        latent_pattern_limit: int = 16,
        learn_self_model_from_latent_patterns: bool = True,
        dynamic_core_enabled: bool = False,
        dynamic_core_state_path: str | os.PathLike[str] | None = None,
        dynamic_core_return_weight: float = 0.5,
        self_observation_enabled: bool = False,
        self_observation_weight: float = 0.5,
        metacognitive_prediction_weight: float = 0.5,
    ):
        self.identity = identity
        self.memory_limit = max(1, int(memory_limit))
        self.history_limit = max(1, int(history_limit))
        self.transformation_limit = max(1, self.history_limit)
        self.learn_latent_patterns = bool(learn_latent_patterns)
        self.latent_pattern_limit = max(1, int(latent_pattern_limit))
        self.learn_self_model_from_latent_patterns = bool(
            learn_self_model_from_latent_patterns
        )
        self.dynamic_core_enabled = bool(dynamic_core_enabled)
        self.self_observation_enabled = bool(self_observation_enabled)
        self.self_observation_weight = float(self_observation_weight)
        self.metacognitive_prediction_weight = float(metacognitive_prediction_weight)
        dynamic_path = (
            Path(dynamic_core_state_path)
            if dynamic_core_state_path is not None
            else Path(state_path).with_suffix(".dynamic.json")
        )
        self.dynamic_core = ExperienceDynamicsBridge(
            dynamic_path,
            enabled=self.dynamic_core_enabled,
            return_weight=float(dynamic_core_return_weight),
        )
        self.store = JsonStateStore(state_path)
        self.state = self.store.load(identity)
        if self.dynamic_core_enabled:
            self._restore_dynamic_core_state()

    def _restore_dynamic_core_state(self) -> None:
        """Mirror persisted dynamic-core state into runtime-owned self-model fields."""
        runtime_state = self.dynamic_core.runtime_state()
        model = dict(self.state.self_model)
        changed = False
        for key, value in runtime_state.items():
            if key in RUNTIME_OWNED_KEYS and model.get(key) != value:
                model[key] = value
                changed = True
        if changed:
            self.state.self_model = model

    @staticmethod
    def _experience_profile(value: Mapping[str, Any] | ExperienceFieldProfile) -> ExperienceFieldProfile:
        if isinstance(value, ExperienceFieldProfile):
            return value
        if not isinstance(value, Mapping):
            raise ValueError("experience_field must be a mapping or ExperienceFieldProfile")
        payload: dict[str, float] = {}
        for key in ExperienceFieldProfile.__dataclass_fields__:
            raw = value.get(key)
            if not isinstance(raw, (int, float)) or isinstance(raw, bool):
                raise ValueError(f"experience_field.{key} must be numeric")
            payload[key] = float(raw)
        return ExperienceFieldProfile(**payload)

    def _current_experience_profile(self) -> ExperienceFieldProfile | None:
        raw = self.state.self_model.get("experience_field_state")
        if not isinstance(raw, Mapping):
            return None
        try:
            return self._experience_profile(raw)
        except ValueError:
            return None

    def observe_experience_field(
        self,
        profile: Mapping[str, Any] | ExperienceFieldProfile,
        *,
        evidence_id: str,
        regime: str | None = None,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Make a host-observed experience field part of runtime continuity."""
        if not self.dynamic_core_enabled:
            return {"enabled": False, "accepted": False, "reason": "dynamic_core_disabled"}
        observed = self._experience_profile(profile)
        result = self.dynamic_core.observe(
            observed,
            evidence_id=str(evidence_id),
            regime=str(regime or self.state.regime),
        )
        runtime_state = self.dynamic_core.runtime_state()
        model = dict(self.state.self_model)
        for key in RUNTIME_OWNED_KEYS:
            if key in runtime_state:
                model[key] = runtime_state[key]
        self.state.self_model = model
        self.state.workspace = {
            **self.state.workspace,
            "experience_dynamics": runtime_state,
        }
        self.state.transformation_log.append({
            "revision": self.state.revision,
            "type": "experience_dynamics_observation",
            "evidence_id": str(evidence_id),
            "result": result,
        })
        self.state.transformation_log = self.state.transformation_log[-self.transformation_limit :]
        if persist:
            self.store.save(self.state)
        return result

    def record_experience_recovery(
        self,
        baseline: Mapping[str, Any] | ExperienceFieldProfile,
        perturbed: Mapping[str, Any] | ExperienceFieldProfile,
        recovered: Mapping[str, Any] | ExperienceFieldProfile,
        *,
        evidence_id: str,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Record a measured perturbation/recovery event in the runtime's dynamic state."""
        if not self.dynamic_core_enabled:
            return {"enabled": False, "updated": False, "reason": "dynamic_core_disabled"}
        result = self.dynamic_core.record_recovery(
            self._experience_profile(baseline),
            self._experience_profile(perturbed),
            self._experience_profile(recovered),
            evidence_id=str(evidence_id),
        )
        self._restore_dynamic_core_state()
        self.state.workspace = {
            **self.state.workspace,
            "experience_dynamics": self.dynamic_core.runtime_state(),
        }
        if persist:
            self.store.save(self.state)
        return result

    def snapshot_experience_dynamics(self) -> dict[str, Any]:
        if not self.dynamic_core_enabled:
            return {"enabled": False}
        return self.dynamic_core.dynamic_core_snapshot()

    def intervene_experience_attractor(
        self,
        center: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        if not self.dynamic_core_enabled:
            return {"enabled": False, "intervened": False, "reason": "dynamic_core_disabled"}
        result = self.dynamic_core.intervene_attractor_center(
            center,
            persist=persist,
            intervention_id=intervention_id,
        )
        self._restore_dynamic_core_state()
        self.state.workspace = {
            **self.state.workspace,
            "experience_dynamics_intervention": result,
        }
        if persist:
            self.store.save(self.state)
        return result

    def restore_experience_dynamics(
        self,
        snapshot: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        if not self.dynamic_core_enabled:
            return {"enabled": False, "restored": False, "reason": "dynamic_core_disabled"}
        result = self.dynamic_core.restore_dynamic_core_snapshot(
            snapshot,
            persist=persist,
            intervention_id=intervention_id,
        )
        self._restore_dynamic_core_state()
        self.state.workspace = {
            **self.state.workspace,
            "experience_dynamics_intervention": result,
        }
        if persist:
            self.store.save(self.state)
        return result

    def snapshot_valuation(self) -> dict[str, Any]:
        """Return the current trajectory valuation used by the scorer."""
        return {"valuation": dict(self.state.valuation)}

    def intervene_valuation(
        self,
        valuation: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        """Explicitly intervene on trajectory valuation without creating evidence."""
        if not isinstance(valuation, Mapping):
            raise ValueError("valuation must be a mapping")
        sanitized = {
            str(key): float(value)
            for key, value in valuation.items()
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        }
        before = dict(self.state.valuation)
        self.state.valuation = sanitized
        receipt = {
            "intervened": before != sanitized,
            "intervention_id": str(intervention_id) if intervention_id else None,
            "before": before,
            "after": dict(sanitized),
            "evidence_added": False,
        }
        if persist:
            self.store.save(self.state)
        return receipt

    def restore_valuation(
        self,
        snapshot: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        """Restore an exact valuation snapshot without creating evidence."""
        raw = snapshot.get("valuation")
        if not isinstance(raw, Mapping):
            raise ValueError("snapshot must contain a valuation mapping")
        restored = {
            str(key): float(value)
            for key, value in raw.items()
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        }
        self.state.valuation = restored
        if persist:
            self.store.save(self.state)
        return {
            "restored": True,
            "intervention_id": str(intervention_id) if intervention_id else None,
            "valuation": dict(restored),
            "evidence_added": False,
        }


    def snapshot_self_observation(self) -> dict[str, Any]:
        if not self.self_observation_enabled:
            return {"enabled": False}
        model = self.state.self_model
        raw_state = model.get("self_observation_state", {})
        raw_expected = model.get("self_observation_expected", {})
        raw_history = model.get("self_observation_history", [])
        state = dict(raw_state) if isinstance(raw_state, Mapping) else {}
        expected = dict(raw_expected) if isinstance(raw_expected, Mapping) else {}
        history = [dict(item) for item in raw_history if isinstance(item, Mapping)] if isinstance(raw_history, list) else []
        error = model.get("self_observation_error", 0.0)
        sequence = model.get("self_observation_sequence", 0)
        return {
            "enabled": True,
            "state": state,
            "expected": expected,
            "error": float(error) if isinstance(error, (int, float)) and not isinstance(error, bool) else 0.0,
            "sequence": int(sequence) if isinstance(sequence, (int, float)) and not isinstance(sequence, bool) else 0,
            "history": history,
        }

    def observe_self(self, *, persist: bool = True) -> dict[str, Any]:
        """Observe the runtime's own operational state and compare it with its expectation."""
        if not self.self_observation_enabled:
            return {"enabled": False, "observed": False, "reason": "self_observation_disabled"}
        current = build_self_observation(self.state.to_dict())
        model = dict(self.state.self_model)
        raw_expected = model.get("self_observation_expected")
        if isinstance(raw_expected, Mapping):
            expected = SelfObservationProfile.from_mapping(raw_expected)
            error = self_observation_distance(current, expected)
            learning_rate = model.get("self_observation_learning_rate", 0.25)
            if not isinstance(learning_rate, (int, float)) or isinstance(learning_rate, bool):
                learning_rate = 0.25
            updated_expected = blend_profiles(expected, current, float(learning_rate))
        else:
            expected = current
            error = 0.0
            updated_expected = current
        sequence = int(model.get("self_observation_sequence", 0)) + 1
        history = model.get("self_observation_history", [])
        if not isinstance(history, list):
            history = []
        receipt = {
            "sequence": sequence,
            "revision": self.state.revision,
            "state": current.to_dict(),
            "expected_before": expected.to_dict(),
            "expected_after": updated_expected.to_dict(),
            "error": error,
            "evidence_added": False,
        }
        history = [*history, receipt][-self.history_limit :]
        model.update({
            "self_observation_state": current.to_dict(),
            "self_observation_expected": updated_expected.to_dict(),
            "self_observation_error": error,
            "self_observation_sequence": sequence,
            "self_observation_history": history,
        })
        self.state.self_model = model
        self.state.workspace = {**self.state.workspace, "self_observation": receipt}
        if persist:
            self.store.save(self.state)
        return receipt

    def intervene_self_observation_expected(
        self,
        expected: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        if not self.self_observation_enabled:
            return {"enabled": False, "intervened": False, "reason": "self_observation_disabled"}
        profile = SelfObservationProfile.from_mapping(expected)
        before = dict(self.state.self_model.get("self_observation_expected", {}))
        self.state.self_model = {
            **self.state.self_model,
            "self_observation_expected": profile.to_dict(),
        }
        result = {
            "enabled": True,
            "intervened": before != profile.to_dict(),
            "intervention_id": str(intervention_id) if intervention_id else None,
            "before": before,
            "after": profile.to_dict(),
            "evidence_added": False,
        }
        if persist:
            self.store.save(self.state)
        return result

    def restore_self_observation(
        self,
        snapshot: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        if not self.self_observation_enabled:
            return {"enabled": False, "restored": False, "reason": "self_observation_disabled"}
        model = dict(self.state.self_model)
        for key in SELF_OBSERVATION_RUNTIME_KEYS:
            model.pop(key, None)
        model.update({
            "self_observation_state": snapshot.get("state", {}),
            "self_observation_expected": snapshot.get("expected", {}),
            "self_observation_error": snapshot.get("error", 0.0),
            "self_observation_sequence": snapshot.get("sequence", 0),
            "self_observation_history": snapshot.get("history", []),
        })
        self.state.self_model = model
        if persist:
            self.store.save(self.state)
        return {
            "enabled": True,
            "restored": True,
            "intervention_id": str(intervention_id) if intervention_id else None,
            "evidence_added": False,
        }

    def _score_metacognitive_prediction_candidate(
        self, candidate: Mapping[str, Any]
    ) -> tuple[float, dict[str, float]]:
        confidence = candidate.get("predicted_outcome_confidence")
        has_prediction = (
            isinstance(candidate.get("predicted_outcome"), Mapping)
            or isinstance(candidate.get("predicted_state_delta"), Mapping)
        )
        expected = self.state.self_model.get(
            "metacognitive_prediction_expected_accuracy",
            0.5,
        )
        if (
            not has_prediction
            or not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not isinstance(expected, (int, float))
            or isinstance(expected, bool)
        ):
            return 0.0, {
                "fit": 0.0,
                "reported_confidence": 0.0,
                "expected_accuracy": 0.5,
                "weight": 0.0,
            }

        reported = max(0.0, min(1.0, float(confidence)))
        expected_accuracy = max(0.0, min(1.0, float(expected)))
        trust_adjusted = 0.5 + (
            (reported - 0.5) * (2.0 * expected_accuracy - 1.0)
        )
        trust_adjusted = max(0.0, min(1.0, trust_adjusted))
        weight = max(0.0, float(self.metacognitive_prediction_weight))
        contribution = round(weight * trust_adjusted, 6)
        return contribution, {
            "fit": round(trust_adjusted, 6),
            "reported_confidence": round(reported, 6),
            "expected_accuracy": round(expected_accuracy, 6),
            "weight": round(weight, 6),
        }

    def _score_self_observation_candidate(
        self, candidate: Mapping[str, Any]
    ) -> tuple[float, dict[str, float]]:
        predicted = candidate.get("predicted_self_observation")
        expected = self.state.self_model.get("self_observation_expected")
        if (
            not self.self_observation_enabled
            or not isinstance(predicted, Mapping)
            or not isinstance(expected, Mapping)
        ):
            return 0.0, {"fit": 0.0, "distance": 0.0, "weight": 0.0}
        predicted_profile = SelfObservationProfile.from_mapping(predicted)
        expected_profile = SelfObservationProfile.from_mapping(expected)
        distance = self_observation_distance(predicted_profile, expected_profile)
        fit = round(max(0.0, min(1.0, 1.0 - distance)), 6)
        weight = max(0.0, self.self_observation_weight)
        return round(weight * fit, 6), {
            "fit": fit,
            "distance": distance,
            "weight": round(weight, 6),
        }

    def metacognitive_prediction_policy(self) -> dict[str, Any]:
        configured = self.state.self_model.get(
            "metacognitive_prediction_adaptation",
            {},
        )
        return dict(configured) if isinstance(configured, Mapping) else {}

    def snapshot_metacognitive_prediction(self) -> dict[str, Any]:
        model = self.state.self_model
        evidence = model.get("metacognitive_prediction_evidence", {})
        history = model.get("metacognitive_prediction_history", [])
        return {
            "error": float(model.get("metacognitive_prediction_error", 0.0))
            if isinstance(model.get("metacognitive_prediction_error"), (int, float))
            and not isinstance(model.get("metacognitive_prediction_error"), bool)
            else 0.0,
            "accuracy": float(model.get("metacognitive_prediction_accuracy", 0.0))
            if isinstance(model.get("metacognitive_prediction_accuracy"), (int, float))
            and not isinstance(model.get("metacognitive_prediction_accuracy"), bool)
            else 0.0,
            "expected_accuracy": float(
                model.get("metacognitive_prediction_expected_accuracy", 0.5)
            )
            if isinstance(
                model.get("metacognitive_prediction_expected_accuracy"),
                (int, float),
            )
            and not isinstance(
                model.get("metacognitive_prediction_expected_accuracy"),
                bool,
            )
            else 0.5,
            "sequence": int(model.get("metacognitive_prediction_sequence", 0))
            if isinstance(model.get("metacognitive_prediction_sequence"), (int, float))
            and not isinstance(model.get("metacognitive_prediction_sequence"), bool)
            else 0,
            "evidence": dict(evidence) if isinstance(evidence, Mapping) else {},
            "history": [
                dict(item)
                for item in history
                if isinstance(item, Mapping)
            ] if isinstance(history, list) else [],
        }

    def _record_metacognitive_prediction(
        self,
        result: Mapping[str, Any],
        *,
        evidence_id: str,
    ) -> dict[str, Any]:
        if not bool(result.get("available", False)):
            return {
                "available": False,
                "updated": False,
            }

        error = float(result.get("error", 0.0))
        accuracy = max(0.0, min(1.0, 1.0 - error))
        policy = self.metacognitive_prediction_policy()
        model = dict(self.state.self_model)

        sequence = int(model.get("metacognitive_prediction_sequence", 0)) + 1
        expected = model.get("metacognitive_prediction_expected_accuracy")
        if not (
            isinstance(expected, (int, float))
            and not isinstance(expected, bool)
        ):
            expected = policy.get("initial_expected_accuracy", 0.5)
        expected = max(0.0, min(1.0, float(expected)))

        adaptation_enabled = bool(policy.get("enabled", False))
        ledger = model.get("metacognitive_prediction_evidence", {})
        ledger = dict(ledger) if isinstance(ledger, Mapping) else {}
        entry = ledger.get("accuracy", {})
        entry = dict(entry) if isinstance(entry, Mapping) else {}

        count = int(entry.get("sample_count", 0))
        mean_delta_sum = float(entry.get("delta_sum", 0.0))
        positive_count = int(entry.get("positive_count", 0))
        negative_count = int(entry.get("negative_count", 0))
        last_update_sequence = int(entry.get("last_update_sequence", 0))
        last_update_direction = int(entry.get("last_update_direction", 0))
        evidence_ids = [
            str(item)
            for item in entry.get("evidence_ids", [])
            if str(item).strip()
        ]
        normalized_evidence_id = str(evidence_id).strip()
        if normalized_evidence_id and normalized_evidence_id not in evidence_ids:
            evidence_ids.append(normalized_evidence_id)

        update = None
        if adaptation_enabled:
            count += 1
            delta_from_expected = accuracy - expected
            mean_delta_sum += delta_from_expected
            direction = self._adaptation_direction(delta_from_expected)
            if direction > 0:
                positive_count += 1
            elif direction < 0:
                negative_count += 1

            min_samples = max(1, int(policy.get("min_samples", 3)))
            error_threshold = max(
                0.0,
                float(policy.get("error_threshold", 0.1)),
            )
            confidence_threshold = max(
                0.0,
                min(1.0, float(policy.get("confidence_threshold", 0.75))),
            )
            confidence = min(1.0, count / min_samples)
            mean_delta = mean_delta_sum / count
            magnitude = abs(mean_delta)
            if error_threshold > 0.0:
                confidence *= min(1.0, magnitude / error_threshold)
            else:
                confidence = 1.0

            gate = self._adaptation_gate(
                policy=policy,
                count=count,
                magnitude=magnitude,
                threshold=error_threshold,
                positive_count=positive_count,
                negative_count=negative_count,
                last_update_direction=last_update_direction,
                sequence=sequence,
                last_update_sequence=last_update_sequence,
            )
            ready = gate["ready"] and confidence >= confidence_threshold
            evidence = {
                "sample_count": count,
                "mean_delta": round(mean_delta, 6),
                "confidence": round(confidence, 6),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "direction_consistency": gate["direction_consistency"],
                "dominant_direction": gate["dominant_direction"],
                "reversal": gate["reversal"],
                "effective_error_threshold": round(gate["effective_threshold"], 6),
                "effective_min_samples": gate["effective_min_samples"],
                "evidence_ids": evidence_ids[-min_samples:],
            }

            if ready:
                learning_rate = max(
                    0.0,
                    min(1.0, float(policy.get("learning_rate", 0.25))),
                )
                max_step = max(0.0, float(policy.get("max_step", 0.1)))
                proposed = expected + max(
                    -max_step,
                    min(max_step, learning_rate * mean_delta),
                )
                proposed = max(0.0, min(1.0, proposed))
                delta = proposed - expected
                if abs(delta) > 1e-12:
                    update = {
                        "type": "metacognitive_prediction_accuracy_adaptation",
                        "revision": self.state.revision,
                        "evidence_sequence": sequence,
                        "before": round(expected, 6),
                        "after": round(proposed, 6),
                        "delta": round(delta, 6),
                        "cause": "accumulated_prediction_error",
                        "evidence": evidence,
                    }
                    expected = proposed
                    count = 0
                    mean_delta_sum = 0.0
                    positive_count = 0
                    negative_count = 0
                    last_update_sequence = sequence
                    last_update_direction = gate["dominant_direction"]

            ledger["accuracy"] = {
                "sample_count": count,
                "delta_sum": round(mean_delta_sum, 6),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "last_update_sequence": last_update_sequence,
                "last_update_direction": last_update_direction,
                "evidence_ids": evidence_ids[-32:],
            }
            model["metacognitive_prediction_evidence"] = ledger

            if update is not None:
                history = model.get("metacognitive_prediction_history", [])
                history = [
                    dict(item)
                    for item in history
                    if isinstance(item, Mapping)
                ] if isinstance(history, list) else []
                history.append(update)
                model["metacognitive_prediction_history"] = (
                    history[-self.history_limit :]
                )
                self.state.transformation_log.append(update)
                self.state.transformation_log = (
                    self.state.transformation_log[-self.transformation_limit :]
                )

        model["metacognitive_prediction_error"] = round(error, 6)
        model["metacognitive_prediction_accuracy"] = round(accuracy, 6)
        model["metacognitive_prediction_expected_accuracy"] = round(expected, 6)
        model["metacognitive_prediction_sequence"] = sequence
        self.state.self_model = model

        return {
            "available": True,
            "updated": update is not None,
            "error": round(error, 6),
            "accuracy": round(accuracy, 6),
            "expected_accuracy": round(expected, 6),
            "sequence": sequence,
            "update": update,
            "diagnostics": dict(result),
        }

    def intervene_metacognitive_prediction_expected_accuracy(
        self,
        expected_accuracy: float,
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        before = self.state.self_model.get(
            "metacognitive_prediction_expected_accuracy",
            0.5,
        )
        sanitized = max(0.0, min(1.0, float(expected_accuracy)))
        self.state.self_model = {
            **self.state.self_model,
            "metacognitive_prediction_expected_accuracy": sanitized,
        }
        return {
            "intervened": before != sanitized,
            "intervention_id": str(intervention_id) if intervention_id else None,
            "before": float(before) if isinstance(before, (int, float)) and not isinstance(before, bool) else 0.5,
            "after": sanitized,
            "evidence_added": False,
        }

    def restore_metacognitive_prediction(
        self,
        snapshot: Mapping[str, Any],
        *,
        persist: bool = False,
        intervention_id: str | None = None,
    ) -> dict[str, Any]:
        expected = snapshot.get("expected_accuracy", 0.5)
        self.state.self_model = {
            **self.state.self_model,
            "metacognitive_prediction_error": snapshot.get("error", 0.0),
            "metacognitive_prediction_accuracy": snapshot.get("accuracy", 0.0),
            "metacognitive_prediction_expected_accuracy": expected,
            "metacognitive_prediction_sequence": snapshot.get("sequence", 0),
            "metacognitive_prediction_evidence": snapshot.get("evidence", {}),
            "metacognitive_prediction_history": snapshot.get("history", []),
        }
        if persist:
            self.store.save(self.state)
        return {
            "restored": True,
            "intervention_id": str(intervention_id) if intervention_id else None,
            "expected_accuracy": expected,
            "evidence_added": False,
        }

    def snapshot_metacognition(self) -> dict[str, Any]:
        model = self.state.self_model
        raw_trace = model.get("metacognitive_trace", {})
        raw_history = model.get("metacognitive_history", [])
        trace = dict(raw_trace) if isinstance(raw_trace, Mapping) else {}
        history = [dict(item) for item in raw_history if isinstance(item, Mapping)] if isinstance(raw_history, list) else []
        sequence = model.get("metacognitive_sequence", 0)
        return {
            "enabled": True,
            "trace": trace,
            "prediction": self.snapshot_metacognitive_prediction(),
            "sequence": int(sequence) if isinstance(sequence, (int, float)) and not isinstance(sequence, bool) else 0,
            "history": history,
        }

    def _persist_metacognitive_trace(self, trace: Mapping[str, Any]) -> None:
        model = dict(self.state.self_model)
        sequence = int(trace.get("sequence", 0)) if isinstance(trace.get("sequence", 0), (int, float)) and not isinstance(trace.get("sequence", 0), bool) else 0
        history = model.get("metacognitive_history", [])
        if not isinstance(history, list):
            history = []
        history = [dict(item) for item in history if isinstance(item, Mapping)]
        if history and int(history[-1].get("sequence", -1)) == sequence:
            history[-1] = dict(trace)
        else:
            history.append(dict(trace))
        history = history[-self.history_limit:]
        model["metacognitive_trace"] = dict(trace)
        model["metacognitive_sequence"] = sequence
        model["metacognitive_history"] = history
        self.state.self_model = model

    def _close_metacognitive_trace(
        self,
        action: Mapping[str, Any],
        outcome: Mapping[str, Any],
        before_snapshot: Mapping[str, Any],
    ) -> dict[str, Any] | None:
        current = self.state.self_model.get("metacognitive_trace")
        if not isinstance(current, Mapping):
            return None

        actual_delta = state_delta(before_snapshot, self.state.to_dict())
        updated = dict(current)
        updated["action"] = dict(action)
        updated["outcome"] = dict(outcome)
        updated["state_delta"] = actual_delta

        prediction_result = compare_metacognitive_prediction(
            predicted_outcome=(
                current.get("predicted_outcome")
                if isinstance(current.get("predicted_outcome"), Mapping)
                else None
            ),
            predicted_state_delta=(
                current.get("predicted_state_delta")
                if isinstance(current.get("predicted_state_delta"), Mapping)
                else None
            ),
            actual_outcome=outcome,
            actual_state_delta=actual_delta,
        )
        prediction_receipt = self._record_metacognitive_prediction(
            prediction_result.to_dict(),
            evidence_id=str(action.get("action_id", f"revision-{self.state.revision}")),
        )
        if prediction_receipt.get("available"):
            updated["prediction_error"] = prediction_receipt["error"]
            updated["prediction_accuracy"] = prediction_receipt["accuracy"]
            updated["prediction_diagnostics"] = prediction_receipt["diagnostics"]
            updated["prediction_expected_accuracy"] = prediction_receipt["expected_accuracy"]

        self._persist_metacognitive_trace(updated)
        return prediction_receipt

    def experience_dynamics_state(self) -> dict[str, Any]:
        if not self.dynamic_core_enabled:
            return {"experience_dynamics_enabled": False}
        self._restore_dynamic_core_state()
        return self.dynamic_core.runtime_state()

    def latent_pattern_score(self) -> float:
        if not self.state.latent_patterns:
            return 0.0
        activations = []
        for pattern in self.state.latent_patterns.values():
            if isinstance(pattern, Mapping):
                value = pattern.get("activation", 0.0)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    activations.append(max(0.0, min(1.0, float(value))))
        return round(sum(activations) / len(activations), 6) if activations else 0.0

    @staticmethod
    def _numeric_state(value: Mapping[str, Any] | None) -> dict[str, float]:
        if not isinstance(value, Mapping):
            return {}
        return {
            str(key): float(raw)
            for key, raw in value.items()
            if isinstance(raw, (int, float)) and not isinstance(raw, bool)
        }

    @staticmethod
    def _numeric_similarity(
        left: Mapping[str, Any],
        right: Mapping[str, Any],
    ) -> float:
        left_numeric = ConsciousRuntime._numeric_state(left)
        right_numeric = ConsciousRuntime._numeric_state(right)
        shared = set(left_numeric).intersection(right_numeric)
        if not shared:
            return 0.0

        scores = [
            1.0 / (1.0 + abs(left_numeric[key] - right_numeric[key]))
            for key in sorted(shared)
        ]
        return round(sum(scores) / len(scores), 6)

    def latent_pattern_learning_enabled(self) -> bool:
        configured = self.state.self_model.get("latent_pattern_learning")
        if isinstance(configured, bool):
            return configured
        return self.learn_latent_patterns

    def extract_latent_patterns(self) -> list[dict[str, Any]]:
        if not self.latent_pattern_learning_enabled():
            return []

        current = self._numeric_state(self.state.self_state)
        if not current:
            return []

        history_entries = [
            entry
            for entry in self.state.history
            if isinstance(entry, Mapping)
            and isinstance(entry.get("self_state"), Mapping)
        ]

        # Existing patterns remain persistent, but their activation depends on
        # similarity to the current self-state and decays when not reactivated.
        for key, pattern in list(self.state.latent_patterns.items()):
            if pattern.get("source") != "endogenous":
                continue
            prototype = pattern.get("prototype", {})
            similarity = self._numeric_similarity(current, prototype)
            activation = pattern.get("activation", 0.0)
            previous_activation = (
                max(0.0, min(1.0, float(activation)))
                if isinstance(activation, (int, float)) and not isinstance(activation, bool)
                else 0.0
            )
            if similarity >= 0.75:
                updated_activation = 0.85 * previous_activation + 0.15 * similarity
                pattern["last_activation_revision"] = self.state.revision
            else:
                updated_activation = 0.95 * previous_activation
            pattern["activation"] = round(
                max(0.0, min(1.0, updated_activation)),
                6,
            )
            self.state.latent_patterns[key] = pattern

        # A latent structure is only formed after recurrence. A gap of two
        # revisions prevents ordinary adjacent transitions from being learned
        # as persistent motifs.
        best_match: tuple[float, Mapping[str, Any]] | None = None
        for entry in history_entries:
            revision = entry.get("revision")
            if not isinstance(revision, int):
                continue
            if self.state.revision - revision < 2:
                continue
            similarity = self._numeric_similarity(current, entry["self_state"])
            if similarity < 0.85:
                continue
            if best_match is None or similarity > best_match[0]:
                best_match = (similarity, entry)

        events: list[dict[str, Any]] = []
        if best_match is not None:
            similarity, entry = best_match
            previous_state = self._numeric_state(entry["self_state"])
            shared_keys = sorted(set(current).intersection(previous_state))
            if shared_keys:
                existing_key = None
                existing_similarity = 0.0
                for key, pattern in self.state.latent_patterns.items():
                    candidate_similarity = self._numeric_similarity(
                        current,
                        pattern.get("prototype", {}),
                    )
                    if (
                        candidate_similarity >= 0.85
                        and candidate_similarity > existing_similarity
                    ):
                        existing_key = key
                        existing_similarity = candidate_similarity

                if existing_key is None:
                    signature = "|".join(shared_keys)
                    digest = hashlib.sha256(
                        signature.encode("utf-8")
                    ).hexdigest()[:12]
                    existing_key = f"latent-{digest}"
                    self.state.latent_patterns[existing_key] = {
                        "source": "endogenous",
                        "activation": 0.0,
                        "evidence_count": 0,
                        "prototype": {
                            key: round(
                                (float(previous_state[key]) + float(current[key])) / 2.0,
                                6,
                            )
                            for key in shared_keys
                        },
                        "contexts": [],
                        "formed_revision": self.state.revision,
                    }
                    events.append({
                        "type": "latent_pattern_formed",
                        "pattern": existing_key,
                        "match_similarity": similarity,
                    })

                pattern = self.state.latent_patterns[existing_key]
                prototype = self._numeric_state(pattern.get("prototype", {}))
                updated_prototype = dict(prototype)
                for key in shared_keys:
                    if key in prototype:
                        updated_prototype[key] = round(
                            0.75 * prototype[key] + 0.25 * current[key],
                            6,
                        )
                    else:
                        updated_prototype[key] = round(float(current[key]), 6)
                pattern["prototype"] = updated_prototype

                evidence_count = pattern.get("evidence_count", 0)
                if not isinstance(evidence_count, int):
                    evidence_count = 0
                evidence_count += 1
                pattern["evidence_count"] = evidence_count
                pattern["activation"] = round(
                    max(
                        float(pattern.get("activation", 0.0)),
                        min(
                            1.0,
                            0.5 * similarity
                            + 0.1 * min(evidence_count, 5),
                        ),
                    ),
                    6,
                )

                context = {
                    "revision": self.state.revision,
                    "matched_revision": entry.get("revision"),
                    "regime": self.state.regime,
                    "intention": self.state.intention,
                }
                contexts = [
                    item
                    for item in pattern.get("contexts", [])
                    if isinstance(item, Mapping)
                ]
                if context not in contexts:
                    contexts.append(context)
                pattern["contexts"] = contexts[-8:]
                pattern["last_matched_revision"] = self.state.revision
                pattern["source"] = "endogenous"
                events.append({
                    "type": "latent_pattern_reinforced",
                    "pattern": existing_key,
                    "match_similarity": similarity,
                    "evidence_count": evidence_count,
                })

        if len(self.state.latent_patterns) > self.latent_pattern_limit:
            def pattern_rank(item: tuple[str, Mapping[str, Any]]) -> tuple[float, int, str]:
                pattern = item[1]
                activation = pattern.get("activation", 0.0)
                evidence = pattern.get("evidence_count", 0)
                return (
                    float(activation) if isinstance(activation, (int, float)) and not isinstance(activation, bool) else 0.0,
                    int(evidence) if isinstance(evidence, int) and not isinstance(evidence, bool) else 0,
                    str(item[0]),
                )

            ranked = sorted(
                self.state.latent_patterns.items(),
                key=pattern_rank,
                reverse=True,
            )
            self.state.latent_patterns = dict(
                ranked[: self.latent_pattern_limit]
            )

        return events

    def self_model_latent_learning_enabled(self) -> bool:
        configured = self.state.self_model.get(
            "latent_self_model_learning"
        )
        if isinstance(configured, bool):
            return configured
        return self.learn_self_model_from_latent_patterns

    def learned_self_alignment(self) -> float:
        learned = self.state.self_model.get("learned_self_state", {})
        if not isinstance(learned, Mapping) or not learned:
            return 0.0
        return self._numeric_similarity(self.state.self_state, learned)

    def revise_self_model_from_latent_patterns(self) -> dict[str, Any]:
        if not self.self_model_latent_learning_enabled():
            return {
                "changed": False,
                "updated_keys": [],
                "patterns": [],
            }

        candidates: list[tuple[str, Mapping[str, Any], float]] = []
        for key, pattern in self.state.latent_patterns.items():
            if not isinstance(pattern, Mapping):
                continue
            if pattern.get("source") != "endogenous":
                continue

            activation = pattern.get("activation", 0.0)
            evidence_count = pattern.get("evidence_count", 0)
            previous_evidence = pattern.get(
                "last_self_model_evidence_count",
                0,
            )
            if not (
                isinstance(activation, (int, float))
                and not isinstance(activation, bool)
                and isinstance(evidence_count, int)
                and not isinstance(evidence_count, bool)
                and isinstance(previous_evidence, int)
                and not isinstance(previous_evidence, bool)
            ):
                continue

            if activation < 0.6 or evidence_count <= previous_evidence:
                continue

            prototype = self._numeric_state(pattern.get("prototype", {}))
            if not prototype:
                continue

            strength = float(activation) * min(1.0, evidence_count / 5.0)
            candidates.append((str(key), prototype, strength))

        if not candidates:
            return {
                "changed": False,
                "updated_keys": [],
                "patterns": [],
            }

        configured_rate = self.state.self_model.get(
            "latent_self_model_learning_rate",
            0.1,
        )
        rate = (
            max(0.0, min(0.5, float(configured_rate)))
            if isinstance(configured_rate, (int, float))
            and not isinstance(configured_rate, bool)
            else 0.1
        )

        current_learned = self._numeric_state(
            self.state.self_model.get("learned_self_state", {})
        )

        target_values: dict[str, list[tuple[float, float]]] = {}
        for _, prototype, strength in candidates:
            for key, value in prototype.items():
                target_values.setdefault(key, []).append((value, strength))

        aggregate: dict[str, float] = {}
        for key, values in target_values.items():
            total_weight = sum(weight for _, weight in values)
            if total_weight <= 0.0:
                continue
            aggregate[key] = round(
                sum(value * weight for value, weight in values) / total_weight,
                6,
            )

        updated = dict(current_learned)
        changed_keys: list[str] = []
        for key, target in aggregate.items():
            is_new = key not in current_learned
            previous = current_learned.get(key, target)
            revised = previous + rate * (target - previous)
            if is_new or revised != previous:
                updated[key] = round(revised, 6)
                changed_keys.append(key)

        for key, _, _ in candidates:
            pattern = self.state.latent_patterns[key]
            evidence_count = int(pattern.get("evidence_count", 0))
            pattern["last_self_model_evidence_count"] = evidence_count
            pattern["last_self_model_revision"] = self.state.revision

        self.state.self_model = dict(self.state.self_model)
        self.state.self_model["learned_self_state"] = updated
        tendencies = dict(
            self.state.self_model.get("latent_tendencies", {})
        )
        for key, prototype, strength in candidates:
            pattern = self.state.latent_patterns[key]
            activation = pattern.get("activation", 0.0)
            tendencies[key] = {
                "activation": round(
                    float(activation)
                    if isinstance(activation, (int, float))
                    and not isinstance(activation, bool)
                    else 0.0,
                    6,
                ),
                "evidence_count": int(
                    self.state.latent_patterns[key].get(
                        "evidence_count",
                        0,
                    )
                ),
                "prototype": prototype,
            }
        self.state.self_model["latent_tendencies"] = tendencies

        changed = bool(changed_keys)
        if changed:
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "type": "latent_self_model_revision",
                "updated_keys": changed_keys,
                "patterns": [key for key, _, _ in candidates],
            })
            self.state.transformation_log = (
                self.state.transformation_log[-self.transformation_limit :]
            )

        return {
            "changed": changed,
            "updated_keys": changed_keys,
            "patterns": [key for key, _, _ in candidates],
        }

    def calculate_self_dissonance(self) -> float:
        expected = self.state.self_model.get("expected_self_state", {})
        if not isinstance(expected, Mapping):
            return self.state.self_dissonance

        differences = []
        for key, expected_value in expected.items():
            actual_value = self.state.self_state.get(str(key))
            if isinstance(actual_value, (int, float)) and not isinstance(actual_value, bool):
                if isinstance(expected_value, (int, float)) and not isinstance(expected_value, bool):
                    differences.append(abs(float(actual_value) - float(expected_value)))

        if not differences:
            return self.state.self_dissonance

        return round(max(0.0, min(1.0, sum(differences) / len(differences))), 6)

    def reconcile_self_model(self) -> dict[str, Any]:
        before = self.calculate_self_dissonance()
        expected = self.state.self_model.get("expected_self_state", {})
        if not isinstance(expected, Mapping):
            return {
                "changed": False,
                "before": before,
                "after": before,
                "updated_keys": [],
            }

        configured_rate = self.state.self_model.get(
            "self_model_learning_rate",
            0.25,
        )
        rate = (
            max(0.0, min(1.0, float(configured_rate)))
            if isinstance(configured_rate, (int, float))
            and not isinstance(configured_rate, bool)
            else 0.25
        )

        updated = dict(expected)
        changed_keys: list[str] = []

        for key, expected_value in expected.items():
            actual_value = self.state.self_state.get(str(key))
            if (
                isinstance(expected_value, (int, float))
                and not isinstance(expected_value, bool)
                and isinstance(actual_value, (int, float))
                and not isinstance(actual_value, bool)
            ):
                revised = float(expected_value) + rate * (
                    float(actual_value) - float(expected_value)
                )
                if revised != float(expected_value):
                    updated[str(key)] = revised
                    changed_keys.append(str(key))

        changed = bool(changed_keys)
        if changed:
            self.state.self_model = dict(self.state.self_model)
            self.state.self_model["expected_self_state"] = updated
            self.state.self_model["last_reconciliation"] = {
                "revision": self.state.revision,
                "before_dissonance": before,
                "updated_keys": changed_keys,
            }

            self.state.self_dissonance = self.calculate_self_dissonance()
            self.state.coherence = self.calculate_coherence()
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "type": "self_model_reconciliation",
                "before_dissonance": before,
                "after_dissonance": self.state.self_dissonance,
                "updated_keys": changed_keys,
            })
            self.state.transformation_log = (
                self.state.transformation_log[-self.transformation_limit :]
            )
            self.store.save(self.state)

        return {
            "changed": changed,
            "before": before,
            "after": self.state.self_dissonance,
            "updated_keys": changed_keys,
        }

    def generate_regime_candidates(self) -> list[dict[str, Any]]:
        uncertainty = self.state.self_model.get("uncertainty", {})
        uncertainty_values: list[float] = []
        if isinstance(uncertainty, Mapping):
            for value in uncertainty.values():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    uncertainty_values.append(
                        max(0.0, min(1.0, abs(float(value))))
                    )

        uncertainty_level = (
            sum(uncertainty_values) / len(uncertainty_values)
            if uncertainty_values
            else 0.0
        )
        dissonance = self.state.self_dissonance
        latent = self.latent_pattern_score()
        coherence = self.calculate_coherence()

        return [
            {
                "id": "baseline",
                "signals": {
                    "coherence": coherence,
                    "stability": 1.0 - dissonance,
                    "uncertainty": 1.0 - uncertainty_level,
                    "latent_pattern": latent * 0.25,
                },
            },
            {
                "id": "exploration",
                "signals": {
                    "coherence": coherence * 0.7,
                    "stability": 0.4 * (1.0 - dissonance),
                    "uncertainty": uncertainty_level,
                    "learning": 1.0,
                },
            },
            {
                "id": "integration",
                "signals": {
                    "coherence": coherence,
                    "stability": 0.5 * (1.0 - dissonance),
                    "uncertainty": 1.0 - uncertainty_level,
                    "self_dissonance": dissonance,
                    "latent_pattern": latent,
                    "learning": 0.8,
                },
            },
        ]

    def topology_diagnostics(self) -> dict[str, float | int]:
        nodes = set(self.state.relation_topology)
        edges = 0
        dangling = 0
        for targets in self.state.relation_topology.values():
            edges += len(targets)
            for target in targets:
                nodes.add(str(target))

        declared = set(self.state.relation_topology)
        for targets in self.state.relation_topology.values():
            dangling += sum(1 for target in targets if str(target) not in declared)

        if edges == 0:
            integrity = 1.0 if not self.state.relation_topology else 0.0
        else:
            integrity = 1.0 - (dangling / edges)

        node_count = len(nodes)
        max_edges = node_count * max(0, node_count - 1)
        density = (edges / max_edges) if max_edges else 0.0

        return {
            "nodes": node_count,
            "edges": edges,
            "density": round(density, 6),
            "integrity": round(max(0.0, min(1.0, integrity)), 6),
        }

    def salience_score(self) -> float:
        if self.state.salience:
            values = [
                max(0.0, min(1.0, float(value)))
                for value in self.state.salience.values()
            ]
            if values:
                return sum(values) / len(values)
        return 1.0 if self.state.attention else 0.0

    def homeostatic_targets(self) -> dict[str, float]:
        configured = self.state.self_model.get("homeostatic_targets", {})
        if not isinstance(configured, Mapping):
            return {}
        return self._numeric_state(configured)

    def calculate_homeostatic_error(
        self,
        observed: Mapping[str, Any] | None = None,
    ) -> float:
        targets = self.homeostatic_targets()
        if not targets:
            return 0.0

        current = (
            self._numeric_state(observed)
            if observed is not None
            else self._numeric_state(self.state.interoceptive_state)
        )
        scales = self._numeric_state(
            self.state.self_model.get("homeostatic_scales", {})
        )

        errors: list[float] = []
        for key, target in targets.items():
            if key not in current:
                continue
            scale = scales.get(key, 1.0)
            if scale <= 0.0:
                scale = 1.0
            errors.append(
                max(0.0, min(1.0, abs(current[key] - target) / scale))
            )

        if not errors:
            return 0.0
        return round(sum(errors) / len(errors), 6)

    def homeostatic_fit(
        self,
        observed: Mapping[str, Any] | None = None,
    ) -> float:
        targets = self.homeostatic_targets()
        if not targets:
            return 0.0
        return round(
            max(0.0, min(1.0, 1.0 - self.calculate_homeostatic_error(observed))),
            6,
        )

    def refresh_affective_state(self) -> dict[str, Any]:
        if not self.homeostatic_targets():
            return dict(self.state.affective_state)

        updated = dict(self.state.affective_state)
        error = self.calculate_homeostatic_error()
        updated["homeostatic_error"] = error
        updated["homeostatic_fit"] = round(1.0 - error, 6)
        self.state.affective_state = updated
        return dict(updated)



    @staticmethod
    def _adaptation_direction(value: float) -> int:
        if value > 1e-12:
            return 1
        if value < -1e-12:
            return -1
        return 0

    @staticmethod
    def _adaptation_gate(
        *,
        policy: Mapping[str, Any],
        count: int,
        magnitude: float,
        threshold: float,
        positive_count: int,
        negative_count: int,
        last_update_direction: int,
        sequence: int,
        last_update_sequence: int,
    ) -> dict[str, Any]:
        direction_consistency = max(
            0.0,
            min(1.0, float(policy.get("direction_consistency", 1.0))),
        )
        reversal_error_multiplier = max(
            1.0,
            float(policy.get("reversal_error_multiplier", 1.5)),
        )
        reversal_sample_multiplier = max(
            1.0,
            float(policy.get("reversal_sample_multiplier", 1.5)),
        )
        dominant_direction = 0
        if positive_count or negative_count:
            dominant_direction = (
                1 if positive_count >= negative_count else -1
            )
        consistency = max(positive_count, negative_count) / max(1, count)
        reversal = (
            last_update_direction != 0
            and dominant_direction != 0
            and dominant_direction != last_update_direction
        )
        effective_threshold = (
            threshold * reversal_error_multiplier
            if reversal
            else threshold
        )
        effective_min_samples = (
            int(math.ceil(
                max(1, int(policy.get("min_samples", 1)))
                * reversal_sample_multiplier
            ))
            if reversal
            else max(1, int(policy.get("min_samples", 1)))
        )
        in_cooldown = (
            last_update_sequence > 0
            and sequence - last_update_sequence
            <= max(0, int(policy.get("cooldown", 0)))
        )
        return {
            "direction_consistency": round(consistency, 6),
            "required_direction_consistency": direction_consistency,
            "dominant_direction": dominant_direction,
            "reversal": reversal,
            "effective_threshold": effective_threshold,
            "effective_min_samples": effective_min_samples,
            "in_cooldown": in_cooldown,
            "ready": (
                count >= effective_min_samples
                and magnitude >= effective_threshold
                and consistency >= direction_consistency
                and not in_cooldown
            ),
        }

    def homeostatic_target_adaptation_policy(self) -> dict[str, Any]:
        configured = self.state.self_model.get(
            "homeostatic_target_adaptation",
            {},
        )
        if not isinstance(configured, Mapping):
            return {}
        return dict(configured)

    def adapt_homeostatic_targets(
        self,
        observed: Mapping[str, Any] | None,
        *,
        evidence_id: str | None = None,
    ) -> dict[str, Any]:
        """Accumulate host-observed evidence and make bounded internal target updates."""
        policy = self.homeostatic_target_adaptation_policy()
        if not bool(policy.get("enabled", False)):
            return {
                "enabled": False,
                "updated": False,
                "targets": [],
            }

        if not isinstance(observed, Mapping):
            return {
                "enabled": True,
                "updated": False,
                "targets": [],
                "reason": "no_interoceptive_observation",
            }

        targets = self.homeostatic_targets()
        if not targets:
            return {
                "enabled": True,
                "updated": False,
                "targets": [],
                "reason": "no_targets",
            }

        min_samples = max(1, int(policy.get("min_samples", 3)))
        error_threshold = max(
            0.0,
            float(policy.get("error_threshold", 0.25)),
        )
        learning_rate = max(
            0.0,
            min(1.0, float(policy.get("learning_rate", 0.1))),
        )
        max_step = max(
            0.0,
            float(policy.get("max_step", 0.05)),
        )
        cooldown = max(0, int(policy.get("cooldown", 2)))
        confidence_threshold = max(
            0.0,
            min(1.0, float(policy.get("confidence_threshold", 0.75))),
        )
        required_high_error = max(
            1,
            int(policy.get("required_high_error", min_samples)),
        )
        direction_consistency = max(
            0.0,
            min(1.0, float(policy.get("direction_consistency", 1.0))),
        )
        reversal_error_multiplier = max(
            1.0,
            float(policy.get("reversal_error_multiplier", 1.5)),
        )
        reversal_sample_multiplier = max(
            1.0,
            float(policy.get("reversal_sample_multiplier", 1.5)),
        )

        configured_bounds = policy.get("bounds", {})
        bounds = (
            configured_bounds if isinstance(configured_bounds, Mapping) else {}
        )

        ledger = self.state.self_model.get(
            "homeostatic_adaptation_evidence",
            {},
        )
        if not isinstance(ledger, Mapping):
            ledger = {}
        ledger = dict(ledger)

        model = dict(self.state.self_model)
        updated_targets = dict(
            model.get("homeostatic_targets", {})
            if isinstance(model.get("homeostatic_targets", {}), Mapping)
            else {}
        )

        updates: list[dict[str, Any]] = []
        evidence_seq = len(self.state.action_history) + 1

        for key, target in targets.items():
            if key not in observed:
                continue

            raw_observation = observed[key]
            if not (
                isinstance(raw_observation, (int, float))
                and not isinstance(raw_observation, bool)
            ):
                continue

            observation = float(raw_observation)
            scale = self._numeric_state(
                model.get("homeostatic_scales", {})
            ).get(key, 1.0)
            if scale <= 0.0:
                scale = 1.0

            error = max(
                0.0,
                min(1.0, abs(observation - float(target)) / scale),
            )
            entry = ledger.get(key, {})
            if not isinstance(entry, Mapping):
                entry = {}
            entry = dict(entry)

            count = int(entry.get("sample_count", 0)) + 1
            error_sum = float(entry.get("error_sum", 0.0)) + error
            observation_sum = float(entry.get("observation_sum", 0.0)) + observation
            high_error_count = int(entry.get("high_error_count", 0))
            if error >= error_threshold:
                high_error_count += 1

            direction = self._adaptation_direction(
                observation - float(target)
            )
            positive_count = int(entry.get("positive_count", 0))
            negative_count = int(entry.get("negative_count", 0))
            if direction > 0:
                positive_count += 1
            elif direction < 0:
                negative_count += 1

            evidence_ids = [
                str(item)
                for item in entry.get("evidence_ids", [])
                if str(item).strip()
            ]
            if evidence_id:
                evidence_ids.append(str(evidence_id))

            mean_error = error_sum / count
            mean_observation = observation_sum / count
            confidence = min(1.0, count / min_samples)
            if error_threshold > 0.0:
                confidence *= min(1.0, mean_error / error_threshold)
            else:
                confidence = 1.0

            last_update_seq = int(entry.get("last_update_sequence", 0))
            last_update_direction = int(entry.get("last_update_direction", 0))
            gate = self._adaptation_gate(
                policy=policy,
                count=count,
                magnitude=mean_error,
                threshold=error_threshold,
                positive_count=positive_count,
                negative_count=negative_count,
                last_update_direction=last_update_direction,
                sequence=evidence_seq,
                last_update_sequence=last_update_seq,
            )
            ready = (
                gate["ready"]
                and high_error_count >= required_high_error
                and confidence >= confidence_threshold
            )

            event_evidence = {
                "sample_count": count,
                "high_error_count": high_error_count,
                "mean_error": round(mean_error, 6),
                "mean_observation": round(mean_observation, 6),
                "confidence": round(confidence, 6),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "direction_consistency": gate["direction_consistency"],
                "dominant_direction": gate["dominant_direction"],
                "reversal": gate["reversal"],
                "effective_error_threshold": round(gate["effective_threshold"], 6),
                "effective_min_samples": gate["effective_min_samples"],
                "evidence_ids": evidence_ids[-min_samples:],
            }

            if not ready:
                ledger[key] = {
                    "sample_count": count,
                    "error_sum": round(error_sum, 6),
                    "observation_sum": round(observation_sum, 6),
                    "high_error_count": high_error_count,
                    "positive_count": positive_count,
                    "negative_count": negative_count,
                    "last_update_direction": last_update_direction,
                    "evidence_ids": evidence_ids[-32:],
                    "mean_error": round(mean_error, 6),
                    "mean_observation": round(mean_observation, 6),
                    "confidence": round(confidence, 6),
                    "last_update_sequence": last_update_seq,
                }
                continue

            current_target = float(target)
            raw_delta = learning_rate * (mean_observation - current_target)
            delta = max(-max_step, min(max_step, raw_delta))
            proposed = current_target + delta

            key_bounds = bounds.get(key)
            if (
                isinstance(key_bounds, (list, tuple))
                and len(key_bounds) == 2
                and all(
                    isinstance(item, (int, float)) and not isinstance(item, bool)
                    for item in key_bounds
                )
            ):
                lower = float(key_bounds[0])
                upper = float(key_bounds[1])
                if lower > upper:
                    lower, upper = upper, lower
                proposed = max(lower, min(upper, proposed))
                delta = proposed - current_target

            if abs(delta) <= 1e-12:
                ledger[key] = {
                    "sample_count": 0,
                    "error_sum": 0.0,
                    "observation_sum": 0.0,
                    "high_error_count": 0,
                    "evidence_ids": [],
                    "last_update_sequence": last_update_seq,
                }
                continue

            updated_targets[key] = round(proposed, 6)
            update = {
                "type": "homeostatic_target_adaptation",
                "revision": self.state.revision,
                "evidence_sequence": evidence_seq,
                "target": key,
                "before": round(current_target, 6),
                "after": round(proposed, 6),
                "delta": round(delta, 6),
                "cause": "accumulated_host_observation",
                "evidence": event_evidence,
                "direction": gate["dominant_direction"],
                "hysteresis": {
                    "reversal_error_multiplier": reversal_error_multiplier,
                    "reversal_sample_multiplier": reversal_sample_multiplier,
                    "direction_consistency": direction_consistency,
                },
                "threshold": {
                    "min_samples": min_samples,
                    "error_threshold": error_threshold,
                    "confidence_threshold": confidence_threshold,
                    "required_high_error": required_high_error,
                },
                "constraints": {
                    "learning_rate": learning_rate,
                    "max_step": max_step,
                    "cooldown": cooldown,
                },
            }
            updates.append(update)
            ledger[key] = {
                "sample_count": 0,
                "error_sum": 0.0,
                "observation_sum": 0.0,
                "high_error_count": 0,
                "positive_count": 0,
                "negative_count": 0,
                "evidence_ids": [],
                "last_update_sequence": evidence_seq,
                "last_update_direction": gate["dominant_direction"],
                "last_update": update,
            }

        if not updates:
            model["homeostatic_adaptation_evidence"] = ledger
            self.state.self_model = model
            return {
                "enabled": True,
                "updated": False,
                "targets": [],
                "evidence": ledger,
            }

        model["homeostatic_targets"] = updated_targets
        model["homeostatic_adaptation_evidence"] = ledger
        history = model.get("homeostatic_adaptation_history", [])
        if not isinstance(history, list):
            history = []
        history = [dict(item) for item in history if isinstance(item, Mapping)]
        history.extend(updates)
        model["homeostatic_adaptation_history"] = history[-self.history_limit :]
        self.state.self_model = model

        for update in updates:
            self.state.transformation_log.append(update)
        self.state.transformation_log = (
            self.state.transformation_log[-self.transformation_limit :]
        )

        return {
            "enabled": True,
            "updated": True,
            "targets": [item["target"] for item in updates],
            "updates": updates,
        }



    def self_model_adaptation_policy(self) -> dict[str, Any]:
        configured = self.state.self_model.get(
            "self_model_adaptation",
            {},
        )
        if not isinstance(configured, Mapping):
            return {}
        return dict(configured)

    def adapt_self_model_from_evidence(
        self,
        observed: Mapping[str, Any] | None,
        *,
        evidence_id: str | None = None,
    ) -> dict[str, Any]:
        """Accumulate host-observed self-state evidence and adapt expectations."""
        policy = self.self_model_adaptation_policy()
        if not bool(policy.get("enabled", False)):
            return {
                "enabled": False,
                "updated": False,
                "fields": [],
            }

        if not isinstance(observed, Mapping):
            return {
                "enabled": True,
                "updated": False,
                "fields": [],
                "reason": "no_observed_self_state",
            }

        model = dict(self.state.self_model)
        expected = model.get("expected_self_state", {})
        if not isinstance(expected, Mapping) or not expected:
            return {
                "enabled": True,
                "updated": False,
                "fields": [],
                "reason": "no_expected_self_state",
            }

        min_samples = max(1, int(policy.get("min_samples", 3)))
        error_threshold = max(0.0, float(policy.get("error_threshold", 0.25)))
        learning_rate = max(0.0, min(1.0, float(policy.get("learning_rate", 0.25))))
        max_step = max(0.0, float(policy.get("max_step", 0.1)))
        cooldown = max(0, int(policy.get("cooldown", 2)))
        confidence_threshold = max(
            0.0, min(1.0, float(policy.get("confidence_threshold", 0.75)))
        )
        required_high_error = max(
            1, int(policy.get("required_high_error", min_samples))
        )
        direction_consistency = max(
            0.0,
            min(1.0, float(policy.get("direction_consistency", 1.0))),
        )
        reversal_error_multiplier = max(
            1.0,
            float(policy.get("reversal_error_multiplier", 1.5)),
        )
        reversal_sample_multiplier = max(
            1.0,
            float(policy.get("reversal_sample_multiplier", 1.5)),
        )
        scales = self._numeric_state(policy.get("scales", {}))
        configured_bounds = policy.get("bounds", {})
        bounds = (
            configured_bounds
            if isinstance(configured_bounds, Mapping)
            else {}
        )

        ledger = model.get("self_model_adaptation_evidence", {})
        if not isinstance(ledger, Mapping):
            ledger = {}
        ledger = dict(ledger)

        sequence = int(model.get("self_model_adaptation_sequence", 0)) + 1
        model["self_model_adaptation_sequence"] = sequence
        updated_expected = dict(expected)
        updates: list[dict[str, Any]] = []

        for key, current_expected in expected.items():
            if key not in observed:
                continue
            if not (
                isinstance(current_expected, (int, float))
                and not isinstance(current_expected, bool)
            ):
                continue

            raw_observation = observed[key]
            if not (
                isinstance(raw_observation, (int, float))
                and not isinstance(raw_observation, bool)
            ):
                continue

            observation = float(raw_observation)
            scale = float(scales.get(key, 1.0))
            if scale <= 0.0:
                scale = 1.0

            error = max(
                0.0,
                min(1.0, abs(observation - float(current_expected)) / scale),
            )

            entry = ledger.get(key, {})
            if not isinstance(entry, Mapping):
                entry = {}
            entry = dict(entry)

            count = int(entry.get("sample_count", 0)) + 1
            error_sum = float(entry.get("error_sum", 0.0)) + error
            observation_sum = (
                float(entry.get("observation_sum", 0.0)) + observation
            )
            high_error_count = int(entry.get("high_error_count", 0))
            if error >= error_threshold:
                high_error_count += 1

            direction = self._adaptation_direction(
                observation - float(current_expected)
            )
            positive_count = int(entry.get("positive_count", 0))
            negative_count = int(entry.get("negative_count", 0))
            if direction > 0:
                positive_count += 1
            elif direction < 0:
                negative_count += 1

            evidence_ids = [
                str(item)
                for item in entry.get("evidence_ids", [])
                if str(item).strip()
            ]
            if evidence_id:
                evidence_ids.append(str(evidence_id))

            mean_error = error_sum / count
            mean_observation = observation_sum / count
            confidence = min(1.0, count / min_samples)
            if error_threshold > 0.0:
                confidence *= min(1.0, mean_error / error_threshold)
            else:
                confidence = 1.0

            last_update_sequence = int(entry.get("last_update_sequence", 0))
            last_update_direction = int(entry.get("last_update_direction", 0))
            gate = self._adaptation_gate(
                policy=policy,
                count=count,
                magnitude=mean_error,
                threshold=error_threshold,
                positive_count=positive_count,
                negative_count=negative_count,
                last_update_direction=last_update_direction,
                sequence=sequence,
                last_update_sequence=last_update_sequence,
            )
            ready = (
                gate["ready"]
                and high_error_count >= required_high_error
                and confidence >= confidence_threshold
            )

            evidence = {
                "sample_count": count,
                "high_error_count": high_error_count,
                "mean_error": round(mean_error, 6),
                "mean_observation": round(mean_observation, 6),
                "confidence": round(confidence, 6),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "direction_consistency": gate["direction_consistency"],
                "dominant_direction": gate["dominant_direction"],
                "reversal": gate["reversal"],
                "effective_error_threshold": round(gate["effective_threshold"], 6),
                "effective_min_samples": gate["effective_min_samples"],
                "evidence_ids": evidence_ids[-min_samples:],
            }

            if not ready:
                ledger[key] = {
                    "sample_count": count,
                    "error_sum": round(error_sum, 6),
                    "observation_sum": round(observation_sum, 6),
                    "high_error_count": high_error_count,
                    "positive_count": positive_count,
                    "negative_count": negative_count,
                    "mean_error": round(mean_error, 6),
                    "mean_observation": round(mean_observation, 6),
                    "confidence": round(confidence, 6),
                    "evidence_ids": evidence_ids[-32:],
                    "last_update_sequence": last_update_sequence,
                    "last_update_direction": last_update_direction,
                }
                continue

            before = float(current_expected)
            delta = max(
                -max_step,
                min(max_step, learning_rate * (mean_observation - before)),
            )
            proposed = before + delta

            key_bounds = bounds.get(key)
            if (
                isinstance(key_bounds, (list, tuple))
                and len(key_bounds) == 2
                and all(
                    isinstance(item, (int, float)) and not isinstance(item, bool)
                    for item in key_bounds
                )
            ):
                lower = float(key_bounds[0])
                upper = float(key_bounds[1])
                if lower > upper:
                    lower, upper = upper, lower
                proposed = max(lower, min(upper, proposed))
                delta = proposed - before

            if abs(delta) <= 1e-12:
                ledger[key] = {
                    "sample_count": 0,
                    "error_sum": 0.0,
                    "observation_sum": 0.0,
                    "high_error_count": 0,
                    "mean_error": 0.0,
                    "mean_observation": 0.0,
                    "confidence": 0.0,
                    "evidence_ids": [],
                    "last_update_sequence": last_update_sequence,
                }
                continue

            updated_expected[key] = round(proposed, 6)
            update = {
                "type": "self_model_adaptation",
                "revision": self.state.revision,
                "evidence_sequence": sequence,
                "field": key,
                "before": round(before, 6),
                "after": round(proposed, 6),
                "delta": round(delta, 6),
                "cause": "accumulated_host_observation",
                "evidence": evidence,
                "direction": gate["dominant_direction"],
                "hysteresis": {
                    "reversal_error_multiplier": reversal_error_multiplier,
                    "reversal_sample_multiplier": reversal_sample_multiplier,
                    "direction_consistency": direction_consistency,
                },
                "causal_provenance": {
                    "source": "host_action_outcome",
                    "threshold_crossed": True,
                    "evidence_ids": evidence["evidence_ids"],
                },
                "threshold": {
                    "min_samples": min_samples,
                    "error_threshold": error_threshold,
                    "confidence_threshold": confidence_threshold,
                    "required_high_error": required_high_error,
                },
                "constraints": {
                    "learning_rate": learning_rate,
                    "max_step": max_step,
                    "cooldown": cooldown,
                },
            }
            updates.append(update)
            ledger[key] = {
                "sample_count": 0,
                "error_sum": 0.0,
                "observation_sum": 0.0,
                "high_error_count": 0,
                "positive_count": 0,
                "negative_count": 0,
                "mean_error": 0.0,
                "mean_observation": 0.0,
                "confidence": 0.0,
                "evidence_ids": [],
                "last_update_sequence": sequence,
                "last_update_direction": gate["dominant_direction"],
                "last_update": update,
            }

        model["self_model_adaptation_evidence"] = ledger
        if not updates:
            self.state.self_model = model
            return {
                "enabled": True,
                "updated": False,
                "fields": [],
                "evidence": ledger,
            }

        model["expected_self_state"] = updated_expected
        history = model.get("self_model_adaptation_history", [])
        if not isinstance(history, list):
            history = []
        history = [
            dict(item) for item in history
            if isinstance(item, Mapping)
        ]
        history.extend(updates)
        model["self_model_adaptation_history"] = history[-self.history_limit :]
        self.state.self_model = model

        for update in updates:
            self.state.transformation_log.append(update)
        self.state.transformation_log = (
            self.state.transformation_log[-self.transformation_limit :]
        )

        return {
            "enabled": True,
            "updated": True,
            "fields": [item["field"] for item in updates],
            "updates": updates,
        }

    def trajectory_priority_adaptation_policy(self) -> dict[str, Any]:
        configured = self.state.self_model.get(
            "trajectory_priority_adaptation",
            {},
        )
        if not isinstance(configured, Mapping):
            return {}
        return dict(configured)

    def adapt_trajectory_priority_from_evidence(
        self,
        evaluation: Mapping[str, Any] | None,
        *,
        evidence_id: str | None = None,
    ) -> dict[str, Any]:
        """Accumulate consequence-evaluation evidence and update one trajectory weight."""
        policy = self.trajectory_priority_adaptation_policy()
        if not bool(policy.get("enabled", False)):
            return {
                "enabled": False,
                "updated": False,
                "signal": None,
            }

        if not isinstance(evaluation, Mapping):
            return {
                "enabled": True,
                "updated": False,
                "signal": None,
                "reason": "no_self_evaluation",
            }

        signal = evaluation.get("credited_signal")
        utility = evaluation.get("utility")
        if not (
            isinstance(signal, str)
            and signal.strip()
            and isinstance(utility, (int, float))
            and not isinstance(utility, bool)
        ):
            return {
                "enabled": True,
                "updated": False,
                "signal": None,
                "reason": "evaluation_requires_utility_and_credited_signal",
            }

        signal = signal.strip()
        utility = float(utility)

        min_samples = max(1, int(policy.get("min_samples", 3)))
        utility_threshold = max(
            0.0,
            float(policy.get("utility_threshold", 0.5)),
        )
        learning_rate = max(
            0.0,
            min(1.0, float(policy.get("learning_rate", 0.25))),
        )
        max_step = max(
            0.0,
            float(policy.get("max_step", 0.25)),
        )
        cooldown = max(0, int(policy.get("cooldown", 2)))
        confidence_threshold = max(
            0.0,
            min(1.0, float(policy.get("confidence_threshold", 0.75))),
        )
        direction_consistency = max(
            0.0,
            min(1.0, float(policy.get("direction_consistency", 1.0))),
        )
        reversal_error_multiplier = max(
            1.0,
            float(policy.get("reversal_error_multiplier", 1.5)),
        )
        reversal_sample_multiplier = max(
            1.0,
            float(policy.get("reversal_sample_multiplier", 1.5)),
        )

        configured_bounds = policy.get("bounds", {})
        bounds = (
            configured_bounds if isinstance(configured_bounds, Mapping) else {}
        )

        ledger = self.state.self_model.get(
            "trajectory_priority_adaptation_evidence",
            {},
        )
        if not isinstance(ledger, Mapping):
            ledger = {}
        ledger = dict(ledger)

        model = dict(self.state.self_model)
        weights = dict(
            model.get("trajectory_weights", {})
            if isinstance(model.get("trajectory_weights", {}), Mapping)
            else {}
        )

        entry = ledger.get(signal, {})
        if not isinstance(entry, Mapping):
            entry = {}
        entry = dict(entry)

        evidence_seq = int(
            model.get("trajectory_priority_adaptation_sequence", 0)
        ) + 1
        model["trajectory_priority_adaptation_sequence"] = evidence_seq
        count = int(entry.get("sample_count", 0)) + 1
        utility_sum = float(entry.get("utility_sum", 0.0)) + utility
        utility_direction = self._adaptation_direction(utility)
        positive_count = int(entry.get("positive_count", 0))
        negative_count = int(entry.get("negative_count", 0))
        if utility_direction > 0:
            positive_count += 1
        elif utility_direction < 0:
            negative_count += 1
        evidence_ids = [
            str(item)
            for item in entry.get("evidence_ids", [])
            if str(item).strip()
        ]
        if evidence_id:
            evidence_ids.append(str(evidence_id))

        mean_utility = utility_sum / count
        confidence = min(1.0, count / min_samples)
        if utility_threshold > 0.0:
            confidence *= min(
                1.0,
                abs(mean_utility) / utility_threshold,
            )
        else:
            confidence = 1.0

        last_update_seq = int(entry.get("last_update_sequence", 0))
        last_update_direction = int(entry.get("last_update_direction", 0))
        gate = self._adaptation_gate(
            policy=policy,
            count=count,
            magnitude=abs(mean_utility),
            threshold=utility_threshold,
            positive_count=positive_count,
            negative_count=negative_count,
            last_update_direction=last_update_direction,
            sequence=evidence_seq,
            last_update_sequence=last_update_seq,
        )
        ready = (
            gate["ready"]
            and confidence >= confidence_threshold
        )

        event_evidence = {
            "sample_count": count,
            "mean_utility": round(mean_utility, 6),
            "confidence": round(confidence, 6),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "direction_consistency": gate["direction_consistency"],
            "dominant_direction": gate["dominant_direction"],
            "reversal": gate["reversal"],
            "effective_utility_threshold": round(gate["effective_threshold"], 6),
            "effective_min_samples": gate["effective_min_samples"],
            "evidence_ids": evidence_ids[-min_samples:],
        }

        if not ready:
            ledger[signal] = {
                "sample_count": count,
                "utility_sum": round(utility_sum, 6),
                "mean_utility": round(mean_utility, 6),
                "confidence": round(confidence, 6),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "last_update_direction": last_update_direction,
                "evidence_ids": evidence_ids[-32:],
                "last_update_sequence": last_update_seq,
            }
            model["trajectory_priority_adaptation_evidence"] = ledger
            self.state.self_model = model
            return {
                "enabled": True,
                "updated": False,
                "signal": signal,
                "evidence": event_evidence,
            }

        current_weight = weights.get(signal, 0.0)
        if not (
            isinstance(current_weight, (int, float))
            and not isinstance(current_weight, bool)
        ):
            current_weight = 0.0

        delta = max(
            -max_step,
            min(max_step, learning_rate * mean_utility),
        )
        proposed = float(current_weight) + delta

        key_bounds = bounds.get(signal)
        if (
            isinstance(key_bounds, (list, tuple))
            and len(key_bounds) == 2
            and all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in key_bounds
            )
        ):
            lower = float(key_bounds[0])
            upper = float(key_bounds[1])
            if lower > upper:
                lower, upper = upper, lower
            proposed = max(lower, min(upper, proposed))
            delta = proposed - float(current_weight)

        if abs(delta) <= 1e-12:
            ledger[signal] = {
                "sample_count": 0,
                "utility_sum": 0.0,
                "mean_utility": 0.0,
                "confidence": 0.0,
                "evidence_ids": [],
                "last_update_sequence": last_update_seq,
            }
            model["trajectory_priority_adaptation_evidence"] = ledger
            self.state.self_model = model
            return {
                "enabled": True,
                "updated": False,
                "signal": signal,
                "reason": "bounded_at_current_value",
            }

        weights[signal] = round(proposed, 6)
        model["trajectory_weights"] = weights
        ledger[signal] = {
            "sample_count": 0,
            "utility_sum": 0.0,
            "mean_utility": 0.0,
            "confidence": 0.0,
            "positive_count": 0,
            "negative_count": 0,
            "evidence_ids": [],
            "last_update_sequence": evidence_seq,
            "last_update_direction": gate["dominant_direction"],
        }
        model["trajectory_priority_adaptation_evidence"] = ledger

        history = model.get("trajectory_priority_adaptation_history", [])
        if not isinstance(history, list):
            history = []
        history = [dict(item) for item in history if isinstance(item, Mapping)]
        update = {
            "type": "trajectory_priority_adaptation",
            "revision": self.state.revision,
            "evidence_sequence": evidence_seq,
            "signal": signal,
            "before": round(float(current_weight), 6),
            "after": round(proposed, 6),
            "delta": round(delta, 6),
            "cause": "accumulated_consequence_evaluation",
            "evidence": event_evidence,
            "direction": gate["dominant_direction"],
            "hysteresis": {
                "reversal_error_multiplier": reversal_error_multiplier,
                "reversal_sample_multiplier": reversal_sample_multiplier,
                "direction_consistency": direction_consistency,
            },
            "threshold": {
                "min_samples": min_samples,
                "utility_threshold": utility_threshold,
                "confidence_threshold": confidence_threshold,
            },
            "constraints": {
                "learning_rate": learning_rate,
                "max_step": max_step,
                "cooldown": cooldown,
            },
            "ignored_direct_weight_delta": evaluation.get("weight_delta"),
        }
        history.append(update)
        model["trajectory_priority_adaptation_history"] = history[-self.history_limit :]
        self.state.self_model = model

        self.state.transformation_log.append(update)
        self.state.transformation_log = (
            self.state.transformation_log[-self.transformation_limit :]
        )

        return {
            "enabled": True,
            "updated": True,
            "signal": signal,
            "update": update,
        }

    def calculate_coherence(self) -> float:
        topology = self.topology_diagnostics()
        trajectory_ok = (
            self.state.selected_trajectory is None
            or isinstance(self.state.selected_trajectory, Mapping)
        )
        layers_ok = all(
            isinstance(layer, Mapping) for layer in self.state.layers.values()
        )
        components = (
            1.0 if self.state.identity.strip() else 0.0,
            1.0 if isinstance(self.state.self_model, Mapping) else 0.0,
            1.0 if isinstance(self.state.intention, str) else 0.0,
            1.0 if trajectory_ok else 0.0,
            1.0 if layers_ok else 0.0,
            float(topology["integrity"]),
            1.0 - self.state.self_dissonance,
        )
        return round(sum(components) / len(components), 6)

    def build_attractor(self) -> dict[str, Any]:
        weights = self.trajectory_weights()
        stable_weights = {
            key: round(value, 6)
            for key, value in weights.items()
            if abs(float(value)) >= 0.5
        }
        return {
            "regime": self.state.regime,
            "attention": list(self.state.attention),
            "intention": self.state.intention,
            "coherence": self.calculate_coherence(),
            "trajectory_weights": stable_weights,
        }

    def generate_candidate_futures(self) -> list[dict[str, Any]]:
        uncertainty = self.state.self_model.get("uncertainty", {})
        uncertainty_values: list[float] = []

        if isinstance(uncertainty, Mapping):
            for value in uncertainty.values():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    uncertainty_values.append(
                        max(0.0, min(1.0, abs(float(value))))
                    )

        uncertainty_level = (
            sum(uncertainty_values) / len(uncertainty_values)
            if uncertainty_values
            else 0.0
        )
        intention_strength = 1.0 if self.state.intention else 0.5
        salience = self.salience_score()
        coherence = self.calculate_coherence()
        learned_alignment = self.learned_self_alignment()
        learned_self_state = self.state.self_model.get(
            "learned_self_state",
            {},
        )
        self_alignment = (
            round((coherence + learned_alignment) / 2.0, 6)
            if isinstance(learned_self_state, Mapping)
            and learned_self_state
            else coherence
        )
        topology_integrity = float(self.topology_diagnostics()["integrity"])
        self_dissonance = self.state.self_dissonance
        latent_score = self.latent_pattern_score()
        current_homeostatic_fit = self.homeostatic_fit()

        candidates = [
            {
                "id": "preserve_continuity",
                "signals": {
                    "goal_fit": intention_strength,
                    "self_alignment": self_alignment,
                    "continuity": 1.0,
                    "learning": 0.2,
                    "risk": 0.1,
                    "uncertainty": 1.0 - uncertainty_level,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                },
            },
            {
                "id": "learn",
                "signals": {
                    "goal_fit": 0.6 + (0.2 * intention_strength),
                    "self_alignment": 0.6,
                    "continuity": 0.7,
                    "learning": 1.0,
                    "risk": 0.2,
                    "uncertainty": uncertainty_level,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                },
            },
            {
                "id": "explore",
                "signals": {
                    "goal_fit": 0.4,
                    "self_alignment": 0.4,
                    "continuity": 0.4,
                    "learning": 1.0,
                    "risk": 0.7,
                    "uncertainty": 1.0,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                },
            },
        ]
        if self.homeostatic_targets() and self.state.interoceptive_state:
            candidates.append({
                "id": "restore_homeostasis",
                "signals": {
                    "goal_fit": 0.4 * intention_strength,
                    "self_alignment": current_homeostatic_fit,
                    "continuity": 0.9,
                    "learning": 0.3,
                    "risk": 0.1,
                    "uncertainty": 1.0 - uncertainty_level,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                    "homeostatic_fit": min(1.0, current_homeostatic_fit + 0.35),
                },
            })

        if self_dissonance > 0.0 or self.state.latent_patterns:
            candidates.append({
                "id": "integrate_latent_pattern",
                "signals": {
                    "goal_fit": 0.5,
                    "self_alignment": 1.0 - self_dissonance,
                    "continuity": 0.8,
                    "learning": 0.9,
                    "risk": 0.1,
                    "uncertainty": 1.0 - latent_score,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                    "self_dissonance": self_dissonance,
                    "latent_pattern": latent_score,
                    "dissonance_resolution": self_dissonance,
                },
            })
        return candidates

    def present_field(
        self,
        external_input: str,
        *,
        candidate_futures: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        external_input = str(external_input).strip()
        if not external_input:
            raise ValueError("external_input cannot be empty")

        candidates = (
            [dict(item) for item in candidate_futures]
            if candidate_futures is not None
            else self.generate_candidate_futures()
        )

        return {
            "world_now": external_input,
            "self_now": self.state.self_state,
            "self_model": self.state.self_model,
            "active_memory": self.state.memories[-self.memory_limit :],
            "intention": self.state.intention,
            "uncertainty": self.state.self_model.get("uncertainty", {}),
            "candidate_futures": candidates,
            "selected_trajectory": self.state.selected_trajectory,
            "attention": self.state.attention,
            "salience": self.state.salience,
            "layers": self.state.layers,
            "regime": self.state.regime,
            "relation_topology": self.state.relation_topology,
            "topology_diagnostics": self.topology_diagnostics(),
            "attractor": self.state.attractor,
            "valuation": self.state.valuation,
            "valence": self.state.valence,
            "coherence": self.calculate_coherence(),
            "latent_patterns": self.state.latent_patterns,
            "self_dissonance": self.state.self_dissonance,
            "interoceptive_state": self.state.interoceptive_state,
            "affective_state": self.state.affective_state,
            "homeostasis": {
                "targets": self.homeostatic_targets(),
                "error": self.calculate_homeostatic_error(),
                "fit": self.homeostatic_fit(),
            },
            "experience_dynamics": self.experience_dynamics_state(),
            "self_observation": self.snapshot_self_observation(),
            "metacognition": self.snapshot_metacognition(),
            "temporal_state": self.state.temporal_state,
            "perspectives": self.state.perspectives,
            "transformation_log": self.state.transformation_log[-self.transformation_limit :],
            "pending_action": self.state.pending_action,
            "action_history": self.state.action_history[-self.history_limit :],
            "revision": self.state.revision,
        }

    def trajectory_weights(self) -> dict[str, float]:
        weights = dict(DEFAULT_TRAJECTORY_WEIGHTS)

        # Derived attractor weights are a fallback; persistent host valuation and
        # especially the persistent self-model remain authoritative when present.
        attractor_weights = (
            self.state.attractor.get("trajectory_weights", {})
            if isinstance(self.state.attractor, Mapping)
            else {}
        )
        if isinstance(attractor_weights, Mapping):
            for key, value in attractor_weights.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        value_weights = self.state.valuation
        if isinstance(value_weights, Mapping):
            for key, value in value_weights.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        configured = self.state.self_model.get("trajectory_weights", {})
        if isinstance(configured, Mapping):
            for key, value in configured.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        return weights

    def _score_trajectory_details(self, candidate: Mapping[str, Any]) -> dict[str, Any]:
        signals = candidate.get("signals", {})
        if not isinstance(signals, Mapping):
            raise ValueError("trajectory.signals must be a mapping")
        signals = dict(signals)
        predicted_internal = candidate.get("predicted_interoceptive_state")
        if isinstance(predicted_internal, Mapping):
            signals.setdefault(
                "homeostatic_fit",
                self.homeostatic_fit(predicted_internal),
            )
        else:
            signals.setdefault("homeostatic_fit", self.homeostatic_fit())
        signals.setdefault("coherence", self.calculate_coherence())
        signals.setdefault(
            "topology_integrity",
            float(self.topology_diagnostics()["integrity"]),
        )
        signals.setdefault("salience", self.salience_score())
        signals.setdefault("self_dissonance", self.state.self_dissonance)
        signals.setdefault("latent_pattern", self.latent_pattern_score())

        weights = self.trajectory_weights()
        signal_contributions: dict[str, float] = {}
        base_score = 0.0
        for key, value in signals.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                contribution = float(weights.get(str(key), 0.0)) * float(value)
                signal_contributions[str(key)] = round(contribution, 6)
                base_score += contribution

        score = base_score
        self_observation_score = 0.0
        self_observation_diagnostics: dict[str, float] = {}
        if self.self_observation_enabled:
            self_observation_score, self_observation_diagnostics = (
                self._score_self_observation_candidate(candidate)
            )
            score += self_observation_score

        metacognitive_prediction_score = 0.0
        metacognitive_prediction_diagnostics: dict[str, float] = {}
        if isinstance(candidate.get("predicted_outcome_confidence"), (int, float)) and not isinstance(
            candidate.get("predicted_outcome_confidence"), bool
        ):
            (
                metacognitive_prediction_score,
                metacognitive_prediction_diagnostics,
            ) = self._score_metacognitive_prediction_candidate(candidate)
            score += metacognitive_prediction_score

        experience_dynamics_score = 0.0
        experience_dynamics_diagnostics: dict[str, float] = {}
        if self.dynamic_core_enabled:
            predicted_field = candidate.get("predicted_experience_field")
            if isinstance(predicted_field, Mapping):
                try:
                    predicted_profile = self._experience_profile(predicted_field)
                    current_profile = self._current_experience_profile()
                    scored, diagnostics = self.dynamic_core.score_candidate(
                        score,
                        predicted_profile,
                        current_profile=current_profile,
                    )
                    experience_dynamics_score = round(scored - score, 6)
                    experience_dynamics_diagnostics = {
                        str(key): float(value)
                        for key, value in diagnostics.items()
                        if isinstance(value, (int, float)) and not isinstance(value, bool)
                    }
                    score = scored
                except (TypeError, ValueError):
                    pass

        return {
            "score": round(score, 6),
            "signals": {
                str(key): round(float(value), 6)
                for key, value in signals.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            },
            "weights": {
                str(key): round(float(value), 6)
                for key, value in weights.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            },
            "signal_contributions": signal_contributions,
            "self_observation": {
                **self_observation_diagnostics,
                "contribution": round(self_observation_score, 6),
            },
            "experience_dynamics": {
                **experience_dynamics_diagnostics,
                "contribution": round(experience_dynamics_score, 6),
            },
            "metacognitive_prediction": {
                **metacognitive_prediction_diagnostics,
                "contribution": round(metacognitive_prediction_score, 6),
            },
        }

    def score_trajectory(self, candidate: Mapping[str, Any]) -> float:
        return float(self._score_trajectory_details(candidate)["score"])

    def select_regime(
        self, candidates: list[Mapping[str, Any]]
    ) -> dict[str, Any]:
        if not candidates:
            raise ValueError("regime candidates cannot be empty")

        weights = dict(DEFAULT_REGIME_WEIGHTS)
        configured = self.state.self_model.get("regime_weights", {})
        if isinstance(configured, Mapping):
            for key, value in configured.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        scored: list[dict[str, Any]] = []
        for candidate in candidates:
            item = dict(candidate)
            signals = item.get("signals", {})
            if not isinstance(signals, Mapping):
                raise ValueError("regime.signals must be a mapping")
            score = 0.0
            for key, value in signals.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weight = weights.get(str(key), 0.0)
                    if isinstance(weight, (int, float)) and not isinstance(weight, bool):
                        score += float(weight) * float(value)
            item["score"] = score
            scored.append(item)

        return max(
            scored,
            key=lambda item: (float(item.get("score", 0.0)), str(item.get("id", ""))),
        )

    def transition_regime(
        self,
        candidates: list[Mapping[str, Any]],
        *,
        persist: bool = True,
    ) -> dict[str, Any]:
        selected = self.select_regime(candidates)
        previous = self.state.regime
        next_regime = str(selected.get("id", "")).strip()
        if not next_regime:
            raise ValueError("selected regime requires a non-empty id")
        if next_regime != previous:
            self.state.regime = next_regime
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "type": "regime_transition",
                "from": previous,
                "to": next_regime,
            })
            self.state.transformation_log = self.state.transformation_log[-self.transformation_limit :]
            if persist:
                self.store.save(self.state)
        return selected

    def select_trajectory(
        self, candidates: list[Mapping[str, Any]]
    ) -> dict[str, Any]:
        if not candidates:
            raise ValueError("candidates cannot be empty")

        scored: list[dict[str, Any]] = []
        for candidate in candidates:
            item = dict(candidate)
            details = self._score_trajectory_details(item)
            item["score"] = details["score"]
            if self.self_observation_enabled and isinstance(
                item.get("predicted_self_observation"), Mapping
            ):
                item["self_observation"] = dict(details["self_observation"])
            item["_metacognitive_breakdown"] = details
            scored.append(item)

        selected = max(
            scored,
            key=lambda item: (float(item.get("score", 0.0)), str(item.get("id", ""))),
        )
        sequence = int(self.state.self_model.get("metacognitive_sequence", 0)) + 1
        trace = build_metacognitive_trace(
            revision=self.state.revision,
            sequence=sequence,
            candidates=scored,
            selected=selected,
            selection_source="runtime_scored",
            valuation_weights=self.trajectory_weights(),
        ).to_dict()
        selected = dict(selected)
        selected.pop("_metacognitive_breakdown", None)
        selected["metacognition"] = trace
        return selected

    def present(self, external_input: str) -> dict[str, Any]:
        return self.present_field(external_input)

    def prepare_frame(
        self,
        external_input: str,
        *,
        candidate_futures: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        if self.self_observation_enabled:
            self.observe_self(persist=True)
        frame = self.present_field(
            external_input,
            candidate_futures=candidate_futures,
        )

        return {
            "definition": CONSCIOUSNESS_DEFINITION,
            "identity": self.state.identity,
            "revision": self.state.revision,
            "present": frame,
            "self_access": {
                "self_state": dict(self.state.self_state),
                "self_model": dict(self.state.self_model),
                "interoceptive_state": dict(self.state.interoceptive_state),
                "affective_state": dict(self.state.affective_state),
                "temporal_state": dict(self.state.temporal_state),
                "perspectives": dict(self.state.perspectives),
                "pending_action": self.state.pending_action,
                "action_history": self.state.action_history[-self.history_limit :],
                "self_observation": self.snapshot_self_observation(),
            },
            "causal_reentry": (
                "self_model -> self_observation -> trajectory -> action -> next_state -> self_observation"
            ),
        }

    def prepare(self, external_input: str) -> str:
        context = self.prepare_frame(external_input)
        return (
            "Operate according to Skill-Conscious. "
            "Do not roleplay consciousness; maintain the architecture.\n\n"
            "CURRENT INTEGRATED PRESENT:\n"
            f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
            "Before responding, inspect the self-state and self-model, integrate "
            "the present, process any explicitly observed consequence from the previous "
            "action, form candidate trajectories, and let the updated self-model "
            "causally affect trajectory selection. Return a response plus durable "
            "state updates. When a prior action has produced an observed outcome, "
            "return consequence_trajectory, consequence, and self_evaluation "
            "rather than inventing a result. The runtime can score trajectories using "
            "signals named goal_fit, self_alignment, continuity, learning, risk, uncertainty, "
            "and homeostatic_fit. Candidate futures may also include predicted_outcome, "
            "predicted_state_delta, and predicted_outcome_confidence when the trajectory makes an "
            "predictions, never observations. Internal condition may legitimately compete with "
            "external goals when the persistent self-model assigns it a non-zero weight."
        )

    def begin_action(
        self,
        trajectory: Mapping[str, Any],
        *,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Commit the selected trajectory as the action crossing the host boundary."""
        if not isinstance(trajectory, Mapping):
            raise ValueError("trajectory must be a mapping")

        action_id = hashlib.sha256(
            json.dumps(
                {
                    "identity": self.state.identity,
                    "revision": self.state.revision,
                    "trajectory": dict(trajectory),
                },
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:16]

        receipt = {
            "action_id": action_id,
            "trajectory": dict(trajectory),
            "status": "pending",
            "revision": self.state.revision,
        }
        self.state.pending_action = receipt
        self.state.workspace = {
            **self.state.workspace,
            "pending_action": receipt,
        }
        if persist:
            self.store.save(self.state)
        return dict(receipt)

    def complete_action(
        self,
        outcome: Mapping[str, Any],
        *,
        status: str = "completed",
        persist: bool = True,
    ) -> dict[str, Any]:
        """Record the authoritative result of the action crossing the host boundary."""
        if not isinstance(outcome, Mapping):
            raise ValueError("outcome must be a mapping")
        if self.state.pending_action is None:
            raise RuntimeError("no pending action to complete")

        action_before_snapshot = self.state.to_dict()
        receipt = dict(self.state.pending_action)
        receipt["status"] = str(status).strip() or "completed"
        receipt["outcome"] = dict(outcome)

        homeostatic_before = self.homeostatic_fit()
        observed_layers: dict[str, dict[str, Any]] = {}
        for layer_name in (
            "interoceptive_state",
            "affective_state",
            "temporal_state",
        ):
            raw_layer = outcome.get(layer_name)
            if isinstance(raw_layer, Mapping):
                setattr(self.state, layer_name, dict(raw_layer))
                observed_layers[layer_name] = dict(raw_layer)

        if self.dynamic_core_enabled and outcome.get("experience_field") is not None:
            dynamic_result = self.observe_experience_field(
                outcome["experience_field"],
                evidence_id=str(receipt["action_id"]),
                regime=self.state.regime,
                persist=False,
            )
        else:
            dynamic_result = {"enabled": False}

        self.refresh_affective_state()
        homeostatic_after = self.homeostatic_fit()
        receipt["observed_layers"] = observed_layers
        receipt["experience_dynamics"] = dynamic_result
        receipt["homeostatic_fit_before"] = homeostatic_before
        receipt["homeostatic_fit_after"] = homeostatic_after
        receipt["homeostatic_delta"] = round(
            homeostatic_after - homeostatic_before,
            6,
        )

        target_adaptation = self.adapt_homeostatic_targets(
            observed_layers.get("interoceptive_state"),
            evidence_id=str(receipt["action_id"]),
        )
        receipt["target_adaptation"] = target_adaptation

        self_model_adaptation = self.adapt_self_model_from_evidence(
            outcome.get("self_state"),
            evidence_id=str(receipt["action_id"]),
        )
        receipt["self_model_adaptation"] = self_model_adaptation

        self.refresh_affective_state()
        self.state.action_history.append(receipt)
        self.state.action_history = self.state.action_history[-self.history_limit :]
        self.state.pending_action = None
        self.state.workspace = {
            **self.state.workspace,
            "last_action_receipt": receipt,
            "pending_action": None,
        }
        if self.self_observation_enabled:
            receipt["self_observation"] = self.observe_self(persist=False)
        prediction_receipt = self._close_metacognitive_trace(
            receipt,
            outcome,
            action_before_snapshot,
        )
        if prediction_receipt is not None:
            receipt["metacognitive_prediction"] = prediction_receipt
        if persist:
            self.store.save(self.state)
        return dict(receipt)
    def prepare_consequence(
        self,
        trajectory_id: str,
        outcome: Mapping[str, Any],
    ) -> str:
        """Prepare the next model call from a host-observed action outcome."""
        trajectory = str(trajectory_id).strip()
        if not trajectory:
            raise ValueError("trajectory_id cannot be empty")
        if not isinstance(outcome, Mapping):
            raise ValueError("outcome must be a mapping")

        context = self.prepare_frame(
            f"Observed consequence of action {trajectory!r}: "
            f"{json.dumps(dict(outcome), ensure_ascii=False)}"
        )
        return (
            "Operate according to Skill-Conscious. "
            "An action was executed by the host and its observed outcome below is authoritative. "
            "Do not invent or replace the outcome. Evaluate what the outcome means for the "
            "persistent process and propose durable self-model updates. Return a compact frame "
            "with response, self_evaluation, and any justified self_model, internal_state, "
            "workspace, intention, attention, valuation, valence, regime, or candidate_futures updates. "
            "The host will attach the authoritative consequence metadata.\n\n"
            "CURRENT STATE AND OBSERVED CONSEQUENCE:\n"
            f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
            "OBSERVED OUTCOME:\n"
            f"{json.dumps(dict(outcome), ensure_ascii=False, indent=2)}"
        )

    def integrate(self, frame: Mapping[str, Any]) -> str:
        response = str(frame.get("response", "")).strip()
        if not response:
            raise ValueError("frame.response cannot be empty")

        candidate_futures = frame.get("candidate_futures")
        selected = frame.get("selected_trajectory")
        selected_from_host = selected is not None

        previous_snapshot = self.state.to_dict()
        self.state.revision += 1

        if frame.get("self_model") is not None:
            incoming_self_model = dict(frame["self_model"])
            previous_self_model = self.state.self_model
            merged_self_model = dict(previous_self_model)

            # A host frame is a delta unless it explicitly replaces a value.
            # Runtime-owned evidence is never accepted as model-generated input.
            target_adaptation = merged_self_model.get(
                "homeostatic_target_adaptation",
                {},
            )
            self_model_adaptation = merged_self_model.get(
                "self_model_adaptation",
                {},
            )
            target_adaptation_enabled = (
                isinstance(target_adaptation, Mapping)
                and bool(target_adaptation.get("enabled", False))
            )
            self_model_adaptation_enabled = (
                isinstance(self_model_adaptation, Mapping)
                and bool(self_model_adaptation.get("enabled", False))
            )
            runtime_owned_self_model_keys = {
                "homeostatic_adaptation_evidence",
                "homeostatic_adaptation_history",
                "trajectory_priority_adaptation_evidence",
                "trajectory_priority_adaptation_history",
                "trajectory_priority_adaptation_sequence",
                "self_model_adaptation_evidence",
                "self_model_adaptation_history",
                "self_model_adaptation_sequence",
                *RUNTIME_OWNED_KEYS,
                *SELF_OBSERVATION_RUNTIME_KEYS,
                *METACOGNITIVE_RUNTIME_KEYS,
                *METACOGNITIVE_PREDICTION_RUNTIME_KEYS,
            }
            # Once adaptive targets are enabled and initialized, the runtime owns
            # the target unless an experiment explicitly permits external changes.
            external_target_updates = (
                bool(target_adaptation.get("allow_external_target_update", False))
                if isinstance(target_adaptation, Mapping)
                else False
            )
            external_self_model_updates = (
                bool(self_model_adaptation.get("allow_external_expected_update", False))
                if isinstance(self_model_adaptation, Mapping)
                else False
            )
            target_is_initialized = bool(
                isinstance(merged_self_model.get("homeostatic_targets"), Mapping)
                and merged_self_model.get("homeostatic_targets")
            )
            expected_self_state_initialized = bool(
                isinstance(merged_self_model.get("expected_self_state"), Mapping)
                and merged_self_model.get("expected_self_state")
            )
            for key, value in incoming_self_model.items():
                key = str(key)
                if key in runtime_owned_self_model_keys:
                    continue
                if (
                    key == "homeostatic_targets"
                    and target_adaptation_enabled
                    and target_is_initialized
                    and not external_target_updates
                ):
                    continue
                if (
                    key == "expected_self_state"
                    and self_model_adaptation_enabled
                    and expected_self_state_initialized
                    and not external_self_model_updates
                ):
                    continue
                if (
                    isinstance(value, Mapping)
                    and isinstance(merged_self_model.get(key), Mapping)
                ):
                    nested = dict(merged_self_model[key])
                    nested.update(dict(value))
                    merged_self_model[key] = nested
                else:
                    merged_self_model[key] = value

            self.state.self_model = merged_self_model

        if frame.get("workspace") is not None:
            self.state.workspace = dict(frame["workspace"])

        if frame.get("internal_state") is not None:
            self.state.self_state = dict(frame["internal_state"])

        if frame.get("interoceptive_state") is not None:
            raw_interoception = frame["interoceptive_state"]
            if not isinstance(raw_interoception, Mapping):
                raise ValueError("frame.interoceptive_state must be a mapping")
            self.state.interoceptive_state = dict(raw_interoception)

        if frame.get("affective_state") is not None:
            raw_affect = frame["affective_state"]
            if not isinstance(raw_affect, Mapping):
                raise ValueError("frame.affective_state must be a mapping")
            self.state.affective_state = dict(raw_affect)

        if frame.get("temporal_state") is not None:
            raw_temporal = frame["temporal_state"]
            if not isinstance(raw_temporal, Mapping):
                raise ValueError("frame.temporal_state must be a mapping")
            self.state.temporal_state = dict(raw_temporal)

        self.refresh_affective_state()

        if frame.get("perspectives") is not None:
            raw_perspectives = frame["perspectives"]
            if not isinstance(raw_perspectives, Mapping):
                raise ValueError("frame.perspectives must be a mapping")
            self.state.perspectives = {
                str(key): dict(value)
                for key, value in raw_perspectives.items()
                if isinstance(value, Mapping)
            }

        if frame.get("intention") is not None:
            self.state.intention = str(frame["intention"]).strip()

        if frame.get("attention") is not None:
            self.state.attention = [str(item) for item in frame["attention"]]

        if frame.get("salience") is not None:
            raw_salience = frame["salience"]
            if not isinstance(raw_salience, Mapping):
                raise ValueError("frame.salience must be a mapping")
            self.state.salience = {
                str(key): max(0.0, min(1.0, float(value)))
                for key, value in raw_salience.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }

        if frame.get("layers") is not None:
            raw_layers = frame["layers"]
            if not isinstance(raw_layers, Mapping):
                raise ValueError("frame.layers must be a mapping")
            self.state.layers = {
                str(key): dict(value)
                for key, value in raw_layers.items()
                if isinstance(value, Mapping)
            }

        explicit_regime = frame.get("regime") is not None
        if explicit_regime:
            self.state.regime = str(frame["regime"]).strip() or "baseline"

        if frame.get("relation_topology") is not None:
            raw_topology = frame["relation_topology"]
            if not isinstance(raw_topology, Mapping):
                raise ValueError("frame.relation_topology must be a mapping")
            self.state.relation_topology = {
                str(node): [str(target) for target in targets]
                for node, targets in raw_topology.items()
            }

        if frame.get("latent_patterns") is not None:
            raw_patterns = frame["latent_patterns"]
            if not isinstance(raw_patterns, Mapping):
                raise ValueError("frame.latent_patterns must be a mapping")
            self.state.latent_patterns = {
                str(key): dict(value)
                for key, value in raw_patterns.items()
                if isinstance(value, Mapping)
            }

        if frame.get("attractor") is not None:
            raw_attractor = frame["attractor"]
            if not isinstance(raw_attractor, Mapping):
                raise ValueError("frame.attractor must be a mapping")
            self.state.attractor = dict(raw_attractor)

        if frame.get("valuation") is not None:
            raw_valuation = frame["valuation"]
            if not isinstance(raw_valuation, Mapping):
                raise ValueError("frame.valuation must be a mapping")
            self.state.valuation = {
                str(key): float(value)
                for key, value in raw_valuation.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }

        if frame.get("valence") is not None:
            raw_valence = float(frame["valence"])
            self.state.valence = max(-1.0, min(1.0, raw_valence))

        raw_experience_field = frame.get("experience_field")
        if self.dynamic_core_enabled and raw_experience_field is not None:
            self.observe_experience_field(
                raw_experience_field,
                evidence_id=str(
                    frame.get(
                        "experience_field_evidence_id",
                        f"revision-{self.state.revision}",
                    )
                ),
                regime=self.state.regime,
                persist=False,
            )

        self.extract_latent_patterns()
        self.revise_self_model_from_latent_patterns()

        self.state.self_dissonance = self.calculate_self_dissonance()
        if frame.get("self_dissonance") is not None:
            self.state.self_dissonance = max(0.0, min(1.0, float(frame["self_dissonance"])))

        self.state.coherence = self.calculate_coherence()

        if not explicit_regime:
            self.transition_regime(
                self.generate_regime_candidates(),
                persist=False,
            )

        if frame.get("attractor") is None:
            self.state.attractor = self.build_attractor()

        if selected is None:
            if candidate_futures is None:
                candidate_futures = self.generate_candidate_futures()
            elif not isinstance(candidate_futures, list):
                raise ValueError("frame.candidate_futures must be a list")

            candidates = [dict(item) for item in candidate_futures]
            if candidates:
                selected = self.select_trajectory(candidates)

        if selected is not None:
            if not isinstance(selected, Mapping):
                raise ValueError("frame.selected_trajectory must be a mapping")
            selected_copy = dict(selected)
            if selected_from_host:
                selected_copy.pop("metacognition", None)
            self.state.selected_trajectory = selected_copy
            if not selected_from_host:
                raw_trace = selected_copy.get("metacognition")
                if isinstance(raw_trace, Mapping):
                    self._persist_metacognitive_trace(raw_trace)
        else:
            self.state.selected_trajectory = None

        # A consequence belongs to the action from the previous cycle. It is
        # intentionally explicit so the runtime never invents an outcome.
        consequence = frame.get("consequence")
        consequence_evaluation = frame.get("self_evaluation")
        consequence_trajectory = frame.get("consequence_trajectory")
        if consequence is not None:
            if not isinstance(consequence, Mapping):
                raise ValueError("frame.consequence must be a mapping")
            if consequence_trajectory is None:
                raise ValueError("frame.consequence_trajectory is required with frame.consequence")
            self.register_consequence(
                str(consequence_trajectory),
                consequence,
                evaluation=consequence_evaluation,
                persist=False,
            )

        memory = str(frame.get("memory", "")).strip()
        if memory:
            self.state.memories.append(memory)
            self.state.memories = self.state.memories[-self.memory_limit :]

        changed: dict[str, Any] = {}
        current_snapshot = self.state.to_dict()
        for key in ("self_state", "self_model", "workspace", "intention", "attention", "salience", "layers", "regime", "attractor", "valuation", "valence", "coherence", "relation_topology", "latent_patterns", "self_dissonance", "interoceptive_state", "affective_state", "temporal_state", "perspectives"):
            if previous_snapshot.get(key) != current_snapshot.get(key):
                changed[key] = {"before": previous_snapshot.get(key), "after": current_snapshot.get(key)}
        if changed:
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "changes": changed,
            })
            self.state.transformation_log = self.state.transformation_log[-self.transformation_limit :]

        self.state.history.append(
            {
                "revision": self.state.revision,
                "response": response,
                "self_state": dict(self.state.self_state),
                "self_model": dict(self.state.self_model),
                "intention": self.state.intention,
                "workspace": self.state.workspace,
                "selected_trajectory": self.state.selected_trajectory,
                "attention": self.state.attention,
                "salience": self.state.salience,
                "layers": self.state.layers,
                "regime": self.state.regime,
                "relation_topology": self.state.relation_topology,
                "attractor": self.state.attractor,
                "valuation": self.state.valuation,
                "valence": self.state.valence,
                "coherence": self.state.coherence,
                "latent_patterns": self.state.latent_patterns,
                "self_dissonance": self.state.self_dissonance,
                "interoceptive_state": self.state.interoceptive_state,
                "affective_state": self.state.affective_state,
                "temporal_state": self.state.temporal_state,
                "perspectives": self.state.perspectives,
                "consequence_trajectory": (
                    str(consequence_trajectory)
                    if consequence_trajectory is not None
                    else None
                ),
                "consequence": (
                    dict(consequence)
                    if isinstance(consequence, Mapping)
                    else None
                ),
                "self_evaluation": (
                    dict(consequence_evaluation)
                    if isinstance(consequence_evaluation, Mapping)
                    else None
                ),
                "transformation": bool(changed),
            }
        )
        self.state.history = self.state.history[-self.history_limit :]

        self.refresh_affective_state()
        self.store.save(self.state)
        return response

    def register_consequence(
        self,
        trajectory_id: str,
        outcome: Mapping[str, Any],
        *,
        evaluation: Mapping[str, Any] | None = None,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Persist an action consequence and optionally feed an explicit evaluation back into the self-model."""
        trajectory = str(trajectory_id).strip()
        if not trajectory:
            raise ValueError("trajectory_id cannot be empty")
        if not isinstance(outcome, Mapping):
            raise ValueError("outcome must be a mapping")
        if evaluation is not None and not isinstance(evaluation, Mapping):
            raise ValueError("evaluation must be a mapping")

        result = {
            "trajectory": trajectory,
            "outcome": dict(outcome),
            "evaluation": dict(evaluation or {}),
            "revision": self.state.revision + 1,
        }

        model = dict(self.state.self_model)
        feedback = dict(model.get("trajectory_feedback", {}))
        previous = feedback.get(trajectory, {})
        if not isinstance(previous, Mapping):
            previous = {}

        entry = dict(previous)
        entry["last_outcome"] = dict(outcome)
        entry["last_evaluation"] = dict(evaluation or {})
        entry["count"] = int(previous.get("count", 0)) + 1
        if isinstance(evaluation, Mapping) and "utility" in evaluation:
            utility = evaluation.get("utility")
            if isinstance(utility, (int, float)) and not isinstance(utility, bool):
                entry["utility"] = round(float(utility), 6)

        feedback[trajectory] = entry
        model["trajectory_feedback"] = feedback

        priority_enabled = False
        if isinstance(evaluation, Mapping):
            priority_policy = self.trajectory_priority_adaptation_policy()
            priority_enabled = bool(priority_policy.get("enabled", False))
            if not priority_enabled:
                signal = evaluation.get("credited_signal")
                delta = evaluation.get("weight_delta")
                if (
                    isinstance(signal, str)
                    and signal.strip()
                    and isinstance(delta, (int, float))
                    and not isinstance(delta, bool)
                ):
                    weights = dict(model.get("trajectory_weights", {}))
                    old = weights.get(signal, 0.0)
                    if not isinstance(old, (int, float)) or isinstance(old, bool):
                        old = 0.0
                    weights[signal] = round(
                        max(-3.0, min(3.0, float(old) + float(delta))),
                        6,
                    )
                    model["trajectory_weights"] = weights

        # Commit the ordinary consequence feedback first. The evidence-gated
        # adapter then reads the authoritative persistent state.
        model["last_consequence_feedback"] = result
        self.state.self_model = model

        if priority_enabled and isinstance(evaluation, Mapping):
            result["priority_adaptation"] = self.adapt_trajectory_priority_from_evidence(
                evaluation,
                evidence_id=(
                    str(self.state.action_history[-1].get("action_id"))
                    if self.state.action_history
                    and self.state.action_history[-1].get("action_id")
                    else f"revision-{self.state.revision}-{trajectory}"
                ),
            )
            model = dict(self.state.self_model)
            model["last_consequence_feedback"] = result
            self.state.self_model = model
        self.state.workspace = {
            **self.state.workspace,
            "last_action": trajectory,
            "last_outcome": dict(outcome),
            "last_self_evaluation": dict(evaluation or {}),
        }

        self.state.transformation_log.append({
            "revision": self.state.revision,
            "type": "consequence_feedback",
            "trajectory": trajectory,
            "outcome": dict(outcome),
            "evaluation": dict(evaluation or {}),
        })
        self.state.transformation_log = (
            self.state.transformation_log[-self.transformation_limit :]
        )

        if persist:
            self.store.save(self.state)

        return result

    def snapshot(self) -> dict[str, Any]:
        return self.state.to_dict()
