"""Executable Subjective Field primitive for the consciousness hypothesis.

The field binds present-world content to persistent self-state through
self-relevance, valence, temporal continuity, attention and reentry.
This is a proposed architecture for studying consciousness, not a proof of
phenomenal experience.
"""
from __future__ import annotations
import copy, math
from dataclasses import dataclass, field
from typing import Any, Mapping

def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))

def _distance(left: Mapping[str,float], right: Mapping[str,float]) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    return sum(abs(float(left.get(k,0.0))-float(right.get(k,0.0))) for k in keys) / len(keys)

@dataclass
class SubjectiveField:
    # The previous field is causal state, not presentation history: continuity
    # and reentry both read it when constructing the next subjective present.
    # Temporal-order experiments therefore must compare fresh runtimes with
    # identical probes and distinct causal predecessors.
    previous: dict[str,float] = field(default_factory=dict)
    revision: int = 0

    def compute(
        self,
        present: Mapping[str,float],
        internal: Mapping[str,float],
        *,
        attention: float = 1.0,
        self_relevance: float = 0.0,
        valence: float = 0.0,
        integration: bool = True,
        temporal_continuity: bool = True,
        reentry: bool = True,
    ) -> dict[str,Any]:
        world={str(k):float(v) for k,v in present.items()
               if isinstance(v,(int,float))}
        self_state={str(k):float(v) for k,v in internal.items()
                    if isinstance(v,(int,float))}
        att=_clamp(attention)
        rel=_clamp(self_relevance)
        val=max(-1.0,min(1.0,float(valence)))
        world_signal=_clamp(
            0.50*world.get("signal",0.0)
            +0.30*world.get("reward",0.0)
            -0.20*world.get("threat",0.0)
        )
        internal_signal=_clamp(
            0.40*self_state.get("energy",0.0)
            +0.30*self_state.get("safety",0.0)
            +0.30*self_state.get("goal",0.0)
        )
        binding=(
            _clamp(math.sqrt(max(0.0,world_signal*internal_signal)))
            if integration else 0.0
        )
        current={
            "world_signal":world_signal,
            "internal_signal":internal_signal,
            "self_relevance":rel,
            "valence":val,
        }
        continuity=(
            _clamp(math.exp(-2.5*_distance(current,self.previous)))
            if temporal_continuity and self.previous else 0.0
        )
        reentry_signal=(
            _clamp(0.50*self.previous.get("strength",0.0)+0.50*continuity)
            if reentry and self.previous else 0.0
        )
        unity=(
            att*float(integration)*_clamp(
                0.45*binding+0.35*rel+0.20*continuity
            )
        )
        strength=(
            att*float(integration)*(
                0.25*binding+0.20*rel+0.15*abs(val)
                +0.20*continuity+0.20*reentry_signal
            )
        )
        snapshot={
            "world_signal":round(world_signal,6),
            "internal_signal":round(internal_signal,6),
            "binding":round(binding,6),
            "self_relevance":round(rel,6),
            "valence":round(val,6),
            "continuity":round(continuity,6),
            "reentry":round(reentry_signal,6),
            "attention":round(att,6),
            "integration":1.0 if integration else 0.0,
            "unity":round(_clamp(unity),6),
            "strength":round(_clamp(strength),6),
            "revision":self.revision+1,
        }
        self.previous=copy.deepcopy(snapshot)
        self.revision+=1
        return snapshot

    def snapshot(self) -> dict[str,Any]:
        return copy.deepcopy(self.previous)
