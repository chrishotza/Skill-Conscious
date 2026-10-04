"""Minimal recurrent subjective substrate for pre-cognitive consciousness experiments.

This module is intentionally lower-level than language, memory, reasoning and
metacognition. It models a persistent internal dynamical substrate with:

- PI-like maintenance/oscillation;
- PHI-like coupling/propagation;
- REL-like closure/curvature;
- a normalized regime gain inspired by TCF's Phi(rho).

The implementation is an experimental architectural hypothesis. It does not
claim that the substrate is phenomenally conscious.
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass, field
from typing import Any, Mapping


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))


def _sigmoid(value: float) -> float:
    if value >= 0.0:
        z = math.exp(-min(value, 60.0))
        return 1.0 / (1.0 + z)
    z = math.exp(max(value, -60.0))
    return z / (1.0 + z)


@dataclass
class PrimarySubjectiveSubstrate:
    """Persistent lower-layer dynamics used before reflective cognition."""

    phase: float = 0.0
    previous_coupling: float = 0.0
    previous_gain: float = 0.0
    previous_subjective_drive: float = 0.0
    revision: int = 0
    last_snapshot: dict[str, Any] = field(default_factory=dict)

    def step(
        self,
        present: Mapping[str, Any],
        internal: Mapping[str, Any],
        *,
        tuning: float = 1.0,
        maintenance: bool = True,
        coupling: bool = True,
        closure: bool = True,
        recurrence: bool = True,
        persistence: bool = True,
    ) -> dict[str, Any]:
        """Advance the substrate by one causal step."""

        signal = _clamp(float(present.get("signal", 0.0)))
        reward = _clamp(float(present.get("reward", 0.0)))
        threat = _clamp(float(present.get("threat", 0.0)))
        energy = _clamp(float(internal.get("energy", 0.0)))
        safety = _clamp(float(internal.get("safety", 0.0)))
        goal = _clamp(float(internal.get("goal", 0.0)))

        world_drive = _clamp(
            0.50 * signal + 0.30 * reward - 0.20 * threat
        )
        internal_drive = _clamp(
            0.45 * energy + 0.30 * safety + 0.25 * goal
        )

        base_coupling = math.sqrt(
            max(0.0, world_drive * internal_drive)
        )
        effective_coupling = (
            base_coupling
            if coupling
            else 0.0
        )

        if closure:
            closure_score = _clamp(
                1.0 - abs(world_drive - internal_drive)
            )
        else:
            closure_score = 0.0

        if maintenance:
            # PI-like persistent oscillation. The phase survives between calls.
            self.phase = (
                self.phase
                + 0.35
                + 0.20 * effective_coupling
            ) % (2.0 * math.pi)
            oscillator = 0.5 + 0.5 * math.sin(self.phase)
        else:
            oscillator = 0.0

        effective_density = _clamp(
            float(tuning)
            * (
                0.55 * effective_coupling
                + 0.25 * closure_score
                + 0.20 * oscillator
            )
        )

        # TCF-inspired normalized regime variable. The absolute numerical
        # scale is deliberately local to the runtime, not a claim that the
        # cosmological rho_c from TCF transfers to biology.
        phi = _sigmoid(12.0 * (effective_density - 0.50))
        resonant_gain = _clamp(0.50 + 0.50 * phi)

        temporal_reentry = (
            _clamp(
                0.50 * self.previous_subjective_drive
                + 0.50 * resonant_gain
            )
            if recurrence and self.revision > 0
            else resonant_gain
        )

        subjective_drive = _clamp(
            effective_coupling
            * closure_score
            * resonant_gain
        )

        if persistence:
            self.previous_coupling = effective_coupling
            self.previous_gain = resonant_gain
            self.previous_subjective_drive = subjective_drive
            self.revision += 1

        snapshot = {
            "world_drive": round(world_drive, 6),
            "internal_drive": round(internal_drive, 6),
            "coupling": round(effective_coupling, 6),
            "closure": round(closure_score, 6),
            "oscillator": round(oscillator, 6),
            "effective_density": round(effective_density, 6),
            "phi": round(phi, 6),
            "resonant_gain": round(resonant_gain, 6),
            "temporal_reentry": round(temporal_reentry, 6),
            "subjective_drive": round(subjective_drive, 6),
            "maintenance": bool(maintenance),
            "coupling_enabled": bool(coupling),
            "closure_enabled": bool(closure),
            "recurrence_enabled": bool(recurrence),
            "tuning": round(float(tuning), 6),
            "revision": self.revision,
        }
        self.last_snapshot = copy.deepcopy(snapshot)
        return copy.deepcopy(snapshot)

    def snapshot(self) -> dict[str, Any]:
        return copy.deepcopy(self.last_snapshot)

    def restore(self, snapshot: Mapping[str, Any]) -> None:
        """Restore causal substrate state without adding evidence."""
        if not isinstance(snapshot, Mapping):
            raise ValueError("substrate snapshot must be a mapping")
        self.phase = float(snapshot.get("phase", self.phase))
        self.previous_coupling = float(
            snapshot.get("coupling", self.previous_coupling)
        )
        self.previous_gain = float(
            snapshot.get("resonant_gain", self.previous_gain)
        )
        self.previous_subjective_drive = float(
            snapshot.get("subjective_drive", self.previous_subjective_drive)
        )
        self.revision = max(
            0,
            int(snapshot.get("revision", self.revision)),
        )
        self.last_snapshot = {
            str(key): value
            for key, value in snapshot.items()
        }
