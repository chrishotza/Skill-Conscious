"""Persistent bridge between ConsciousRuntime and the SubjectiveField."""
from __future__ import annotations
import copy
from typing import Any, Mapping
from .core import ConsciousRuntime
from .subjective_field import SubjectiveField

class ConsciousFieldRuntime:
    WORKSPACE_KEY = "subjective_field"

    def __init__(self, runtime: ConsciousRuntime, *, enabled: bool = True) -> None:
        self.runtime = runtime
        self.enabled = bool(enabled)
        self.field = SubjectiveField()
        self._restore()

    def _restore(self) -> None:
        payload = self.runtime.state.workspace.get(self.WORKSPACE_KEY, {})
        if not isinstance(payload, Mapping):
            return
        previous = payload.get("previous")
        if isinstance(previous, Mapping):
            self.field.previous = {
                str(k): float(v) for k, v in previous.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }
        revision = payload.get("revision")
        if isinstance(revision, int) and not isinstance(revision, bool):
            self.field.revision = max(0, revision)

    def snapshot(self) -> dict[str, Any]:
        payload = self.runtime.state.workspace.get(self.WORKSPACE_KEY, {})
        return copy.deepcopy(dict(payload)) if isinstance(payload, Mapping) else {}

    @staticmethod
    def _world_signals(present: Mapping[str, Any]) -> dict[str, float]:
        def n(v: Any) -> float:
            return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0
        return {
            "signal": n(present.get("signal", 0.0)),
            "reward": n(present.get("reward", 0.0)),
            "threat": n(present.get("threat", 0.0)),
            "self_impact": n(present.get("self_impact", 0.0)),
        }

    def _self_state_signals(self) -> dict[str, float]:
        intero = self.runtime.state.interoceptive_state
        state = self.runtime.state.self_state
        energy = intero.get("energy", state.get("energy", 0.0))
        safety = state.get("safety", 0.0)
        goal = state.get("goal", 0.0)
        return {
            "energy": float(energy) if isinstance(energy, (int, float)) else 0.0,
            "safety": float(safety) if isinstance(safety, (int, float)) else 0.0,
            "goal": float(goal) if isinstance(goal, (int, float)) else 0.0,
        }

    def _attention_value(self) -> float:
        if not self.runtime.state.attention or not self.runtime.state.salience:
            return 1.0
        values = [float(v) for v in self.runtime.state.salience.values() if isinstance(v, (int, float))]
        return max(0.0, min(1.0, sum(values) / max(1, len(values))))

    def project(
        self,
        present: Mapping[str, Any],
        *,
        self_relevance: float | None = None,
        valence: float | None = None,
        attention: float | None = None,
        integration: bool = True,
        temporal_continuity: bool = True,
        reentry: bool = True,
        persist: bool = True,
    ) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False, "unity": 0.0, "strength": 0.0}
        world = self._world_signals(present)
        internal = self._self_state_signals()
        relevance = world["self_impact"] if self_relevance is None else float(self_relevance)
        current_valence = float(self.runtime.state.valence) if valence is None else float(valence)
        current_attention = self._attention_value() if attention is None else float(attention)
        snapshot = self.field.compute(
            world,
            internal,
            attention=current_attention,
            self_relevance=relevance,
            valence=current_valence,
            integration=integration,
            temporal_continuity=temporal_continuity,
            reentry=reentry,
        )
        payload = {
            **snapshot,
            "enabled": True,
            "previous": {
                k: v for k, v in snapshot.items()
                if k in {"world_signal", "internal_signal", "self_relevance", "valence"}
            },
            "revision": self.field.revision,
        }
        if persist:
            self.runtime.state.workspace = {
                **self.runtime.state.workspace,
                self.WORKSPACE_KEY: payload,
            }
        return copy.deepcopy(payload)

    def integrate(
        self,
        frame: Mapping[str, Any],
        present: Mapping[str, Any],
        *,
        persist: bool = True,
    ) -> dict[str, Any]:
        before = self.project(present, persist=False)
        response = self.runtime.integrate(frame)
        after = self.project(present, persist=False)
        record = {
            "before": before,
            "after": after,
            "response": response,
            "causal_reentry_delta": round(
                float(after.get("reentry", 0.0)) - float(before.get("reentry", 0.0)), 6
            ),
        }
        if persist:
            self.runtime.state.workspace = {
                **self.runtime.state.workspace,
                self.WORKSPACE_KEY: after,
                "subjective_field_cycle": record,
            }
            self.runtime.store.save(self.runtime.state)
        return record
