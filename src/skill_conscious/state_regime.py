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



OPERATIONAL_RUNTIME_KEYS = (
    "operational_consolidation_profile",
    "operational_replay_profile",
)


def build_consolidation_profile(
    consolidation: Mapping[str, Any],
) -> dict[str, Any]:
    """Convert deterministic consolidation into a bounded replay prior."""
    raw_ids = consolidation.get("trajectory_ids", [])
    counts: dict[str, int] = {}
    if isinstance(raw_ids, list):
        for raw_id in raw_ids:
            identifier = str(raw_id).strip()
            if identifier:
                counts[identifier] = counts.get(identifier, 0) + 1

    total = sum(counts.values())
    scores = {
        key: round(value / total, 6)
        for key, value in counts.items()
    } if total else {}

    return {
        "source_signature": str(consolidation.get("signature", "")),
        "trajectory_counts": counts,
        "trajectory_scores": scores,
        "sample_count": total,
        "dominant_trajectory": (
            max(counts, key=lambda key: (counts[key], key))
            if counts
            else None
        ),
    }


def reinforce_replay_profile(
    profile: Mapping[str, Any] | None,
    trajectory_id: str,
    *,
    decay: float = 0.9,
    increment: float = 1.0,
    max_entries: int = 16,
) -> dict[str, Any]:
    """Apply explicit endogenous replay reinforcement without external outcome evidence."""
    decay = max(0.0, min(1.0, float(decay)))
    increment = max(0.0, float(increment))
    limit = max(1, int(max_entries))
    current = dict(profile) if isinstance(profile, Mapping) else {}

    raw_scores = current.get("trajectory_scores", {})
    scores = {
        str(key): max(0.0, float(value))
        for key, value in dict(raw_scores).items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    }

    scores = {
        key: value * decay
        for key, value in scores.items()
    }

    identifier = str(trajectory_id).strip()
    if identifier:
        scores[identifier] = scores.get(identifier, 0.0) + increment

    ranked = sorted(
        scores.items(),
        key=lambda item: (float(item[1]), str(item[0])),
        reverse=True,
    )[:limit]

    maximum = max((value for _, value in ranked), default=0.0)
    normalized = {
        key: round(value / maximum, 6)
        for key, value in ranked
    } if maximum else {}

    counts = dict(current.get("trajectory_replay_count", {}))
    if identifier:
        counts[identifier] = int(counts.get(identifier, 0)) + 1

    return {
        "trajectory_scores": normalized,
        "trajectory_replay_count": counts,
        "replay_sequence": int(current.get("replay_sequence", 0)) + 1,
        "last_replayed_trajectory": identifier or None,
        "decay": decay,
        "increment": increment,
        "max_entries": limit,
    }
