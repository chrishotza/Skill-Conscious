from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping

OPERATIONAL_MODES = ("wake", "offline", "dream_like")
DEFAULT_OPERATIONAL_MODE = "wake"


def normalize_operational_mode(value: Any) -> str:
    mode = str(value or DEFAULT_OPERATIONAL_MODE).strip().lower()
    if mode not in OPERATIONAL_MODES:
        raise ValueError(
            f"operational mode must be one of {OPERATIONAL_MODES}, got {mode!r}"
        )
    return mode


def operational_dynamics(mode: Any) -> dict[str, Any]:
    normalized = normalize_operational_mode(mode)
    return {
        "mode": normalized,
        "accepts_external_input": normalized == "wake",
        "generates_candidate_futures": normalized != "offline",
        "selects_trajectories": normalized != "offline",
        "executes_actions": normalized == "wake",
        "memory_consolidation": normalized in {"offline", "dream_like"},
        "internal_replay": normalized == "dream_like",
        "wake_reentry": normalized == "wake",
    }


@dataclass(frozen=True)
class OperationalState:
    """Persistent computational mode separate from the cognitive regime label.

    The mode describes whether the runtime is interacting with the external
    world, consolidating without external input, or replaying internally.
    It is an operational mechanism, not a claim about phenomenal states.
    """

    mode: str = DEFAULT_OPERATIONAL_MODE
    entered_revision: int = 0
    cycles: int = 0
    consolidation_count: int = 0
    replay_count: int = 0
    reentry_count: int = 0
    last_cycle_revision: int = 0
    last_reentry_revision: int = 0
    last_replay_signature: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "mode", normalize_operational_mode(self.mode))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "OperationalState":
        if not isinstance(value, Mapping):
            return cls()
        return cls(
            mode=normalize_operational_mode(
                value.get("mode", DEFAULT_OPERATIONAL_MODE)
            ),
            entered_revision=int(value.get("entered_revision", 0)),
            cycles=int(value.get("cycles", 0)),
            consolidation_count=int(value.get("consolidation_count", 0)),
            replay_count=int(value.get("replay_count", 0)),
            reentry_count=int(value.get("reentry_count", 0)),
            last_cycle_revision=int(value.get("last_cycle_revision", 0)),
            last_reentry_revision=int(value.get("last_reentry_revision", 0)),
            last_replay_signature=str(value.get("last_replay_signature", "")),
        )


def build_memory_consolidation(
    snapshot: Mapping[str, Any],
    *,
    replay_limit: int = 8,
) -> dict[str, Any]:
    """Build a deterministic consolidation event from persistent state."""
    limit = max(1, int(replay_limit))
    memories = [
        str(item)
        for item in snapshot.get("memories", [])
        if str(item).strip()
    ][-limit:]
    history = [
        dict(item)
        for item in snapshot.get("history", [])
        if isinstance(item, Mapping)
    ][-limit:]
    latent_patterns = snapshot.get("latent_patterns", {})
    latent_keys = (
        sorted(str(key) for key in latent_patterns)
        if isinstance(latent_patterns, Mapping)
        else []
    )

    replay_revisions = [
        int(item.get("revision", 0))
        for item in history
        if isinstance(item.get("revision", 0), int)
        and not isinstance(item.get("revision", 0), bool)
    ]
    trajectory_ids = []
    for item in history:
        selected = item.get("selected_trajectory")
        if isinstance(selected, Mapping):
            trajectory_id = selected.get("id")
            if trajectory_id is not None:
                trajectory_ids.append(str(trajectory_id))

    canonical = {
        "memories": memories,
        "replay_revisions": replay_revisions,
        "trajectory_ids": trajectory_ids,
        "latent_keys": latent_keys[-limit:],
    }
    signature = hashlib.sha256(
        json.dumps(
            canonical,
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "type": "memory_consolidation",
        "memory_count": len(memories),
        "history_count": len(history),
        "latent_pattern_count": len(latent_keys),
        "replay_revisions": replay_revisions,
        "trajectory_ids": trajectory_ids,
        "latent_keys": latent_keys[-limit:],
        "signature": signature,
        "replay_limit": limit,
    }


def build_dream_replay(
    snapshot: Mapping[str, Any],
    *,
    replay_limit: int = 6,
) -> str:
    """Create a compact internal replay payload without new world input."""
    limit = max(1, int(replay_limit))
    memories = [
        str(item)
        for item in snapshot.get("memories", [])
        if str(item).strip()
    ][-limit:]
    history = [
        dict(item)
        for item in snapshot.get("history", [])
        if isinstance(item, Mapping)
    ][-limit:]
    latent_patterns = snapshot.get("latent_patterns", {})
    latent_keys = (
        sorted(str(key) for key in latent_patterns)[-limit:]
        if isinstance(latent_patterns, Mapping)
        else []
    )

    selected = []
    for item in history:
        trajectory = item.get("selected_trajectory")
        if isinstance(trajectory, Mapping):
            identifier = trajectory.get("id")
            if identifier is not None:
                selected.append(str(identifier))

    payload = {
        "source": "internal_replay",
        "memories": memories,
        "recent_trajectories": selected,
        "latent_patterns": latent_keys,
    }
    return "Internal replay for dream-like computation: " + json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
    )
