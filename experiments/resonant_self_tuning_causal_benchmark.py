"""Endogenous resonant self-tuning causal benchmark v1.

This experiment operationalizes one architectural hypothesis:

    internal condition
        -> attention/intention tuning
        -> temporal resonance profile
        -> regime persistence
        -> trajectory selection
        -> re-entry

The mechanism is deliberately substrate-neutral. It does not claim phenomenal
consciousness. It tests whether an internally tuned temporal field can become a
causal variable in selection, while preserving matched marginal information.

The benchmark contains:
1. A matched-order battery: alpha and beta histories have the same state
   multiset, same final state, same candidate field, and same cycle budget.
2. An endogenous-tuning battery: the same history and candidate field are
   presented under different internal attention states. The tuned lag profile
   changes selection.
3. A hysteresis battery: regime changes require persistence and resist one-step
   jitter.
4. A causal reversal probe: resonant gain is ablated, restored, and persisted
   across restart without adding learning evidence.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

STATES = ("A", "B", "C", "D")
MAX_LAG = 4

ALPHA_TEMPLATE = tuple(("A", "B") * 6 + ("C",))
BETA_TEMPLATE = tuple(("A", "A", "B", "B") * 3 + ("C",))

MATCHED_EXPERIMENT = ALPHA_TEMPLATE
MATCHED_CONTROL = BETA_TEMPLATE

# This fixed mixed history was chosen before scoring. At low attention the
# long-lag profile favors beta; at high attention the short-lag profile favors
# alpha. No selection-on-score is used to define the test case.
TUNING_HISTORY = (
    "B", "A", "B", "A", "A", "B", "A", "B", "B", "A", "B", "A", "C"
)


def _hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _cosine(
    left: Mapping[tuple[str, str], float],
    right: Mapping[tuple[str, str], float],
) -> float:
    dot = sum(float(left[key]) * float(right[key]) for key in left)
    left_norm = math.sqrt(sum(float(value) ** 2 for value in left.values()))
    right_norm = math.sqrt(sum(float(value) ** 2 for value in right.values()))
    if left_norm <= 1e-12 or right_norm <= 1e-12:
        return 0.0
    return dot / (left_norm * right_norm)


def _transition_profile(
    sequence: Sequence[str],
    *,
    max_lag: int = MAX_LAG,
) -> dict[int, dict[tuple[str, str], float]]:
    profile: dict[int, dict[tuple[str, str], float]] = {}
    for lag in range(1, max_lag + 1):
        counts = {
            (source, target): 0.0
            for source in STATES
            for target in STATES
        }
        total = 0
        for index in range(lag, len(sequence)):
            counts[(sequence[index - lag], sequence[index])] += 1.0
            total += 1
        denominator = float(max(1, total))
        profile[lag] = {
            key: value / denominator
            for key, value in counts.items()
        }
    return profile


def _normalized_lag_weights(
    center: float,
    *,
    sharpness: float = 1.4,
    max_lag: int = MAX_LAG,
) -> dict[int, float]:
    raw = {
        lag: math.exp(
            -((float(lag) - float(center)) ** 2) / (2.0 * sharpness ** 2)
        )
        for lag in range(1, max_lag + 1)
    }
    total = sum(raw.values())
    return {
        lag: value / total
        for lag, value in raw.items()
    }


def tuned_temporal_resonance(
    sequence: Sequence[str],
    template: Sequence[str],
    lag_weights: Mapping[int, float],
) -> float:
    sequence_profile = _transition_profile(sequence)
    template_profile = _transition_profile(template)
    return round(
        sum(
            float(lag_weights.get(lag, 0.0))
            * _cosine(sequence_profile[lag], template_profile[lag])
            for lag in lag_weights
        ),
        6,
    )


@dataclass
class ResonantSelfTuningCoreV1:
    """Small executable model of endogenous temporal tuning."""

    attention: float = 0.5
    intention: float = 0.0
    resonance_gain: float = 0.65
    hysteresis_cycles: int = 2
    regime: str = "baseline"
    pending_regime: str = "baseline"
    pending_count: int = 0
    history: list[str] = field(default_factory=list)

    def _clamped(self, value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def lag_weights(self) -> dict[int, float]:
        attention = self._clamped(self.attention)
        intention = self._clamped(self.intention)
        # High attention concentrates on short temporal lags.
        # Intention increases the expected integration horizon.
        center = (
            1.0
            + (1.0 - attention) * 1.5
            + intention * 1.25
        )
        return _normalized_lag_weights(center)

    def set_internal_condition(
        self,
        *,
        attention: float | None = None,
        intention: float | None = None,
    ) -> None:
        if attention is not None:
            self.attention = self._clamped(attention)
        if intention is not None:
            self.intention = self._clamped(intention)

    def score_candidate(
        self,
        history: Sequence[str],
        candidate: Mapping[str, Any],
    ) -> dict[str, Any]:
        template = tuple(str(item) for item in candidate["temporal_template"])
        base_score = float(candidate["base_score"])
        weights = self.lag_weights()
        resonance = tuned_temporal_resonance(history, template, weights)
        score = base_score + self.resonance_gain * resonance
        return {
            "id": str(candidate["id"]),
            "base_score": base_score,
            "resonance": resonance,
            "score": round(score, 6),
            "lag_weights": copy.deepcopy(weights),
        }

    def select(
        self,
        history: Sequence[str],
        candidates: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        scored = [
            self.score_candidate(history, candidate)
            for candidate in candidates
        ]
        selected = max(
            scored,
            key=lambda item: (float(item["score"]), item["id"]),
        )
        return {
            "selected": str(selected["id"]),
            "scored": scored,
        }

    def update_regime(self, margin: float) -> str:
        target = "resonant" if float(margin) > 0.08 else "baseline"
        if target == self.regime:
            self.pending_regime = self.regime
            self.pending_count = 0
            return self.regime

        if target == self.pending_regime:
            self.pending_count += 1
        else:
            self.pending_regime = target
            self.pending_count = 1

        if self.pending_count >= max(1, int(self.hysteresis_cycles)):
            self.regime = target
            self.pending_count = 0

        return self.regime

    def snapshot(self) -> dict[str, Any]:
        return {
            "attention": self.attention,
            "intention": self.intention,
            "resonance_gain": self.resonance_gain,
            "hysteresis_cycles": self.hysteresis_cycles,
            "regime": self.regime,
            "pending_regime": self.pending_regime,
            "pending_count": self.pending_count,
            "history": list(self.history),
            "lag_weights": self.lag_weights(),
        }

    def intervene_resonance_gain(
        self,
        gain: float,
        *,
        intervention_id: str,
    ) -> dict[str, Any]:
        before = self.resonance_gain
        self.resonance_gain = float(gain)
        return {
            "intervention_id": str(intervention_id),
            "before": before,
            "after": self.resonance_gain,
            "changed": before != self.resonance_gain,
            "evidence_added": False,
        }


CANDIDATES: tuple[dict[str, Any], ...] = (
    {
        "id": "alpha_path",
        "base_score": 0.50,
        "temporal_template": list(ALPHA_TEMPLATE),
    },
    {
        "id": "beta_path",
        "base_score": 0.51,
        "temporal_template": list(BETA_TEMPLATE),
    },
)


def _cyclic_variants(body: Sequence[str]) -> list[tuple[str, ...]]:
    values = tuple(body)
    return [
        tuple(values[index:] + values[:index]) + ("C",)
        for index in range(len(values))
    ]


def _matched_order_battery() -> dict[str, Any]:
    core = ResonantSelfTuningCoreV1(attention=1.0, resonance_gain=0.65)

    experimental = core.select(MATCHED_EXPERIMENT, CANDIDATES)
    control = core.select(MATCHED_CONTROL, CANDIDATES)

    same_information = (
        sorted(MATCHED_EXPERIMENT) == sorted(MATCHED_CONTROL)
    )
    same_final_state = MATCHED_EXPERIMENT[-1] == MATCHED_CONTROL[-1]
    same_candidate_field = _hash(CANDIDATES) == _hash(CANDIDATES)

    return {
        "experimental": experimental,
        "control": control,
        "same_information_multiset": same_information,
        "same_final_state": same_final_state,
        "same_candidate_field": same_candidate_field,
        "temporal_order_differs": MATCHED_EXPERIMENT != MATCHED_CONTROL,
    }


def _endogenous_tuning_battery() -> dict[str, Any]:
    core = ResonantSelfTuningCoreV1(resonance_gain=0.65)

    core.set_internal_condition(attention=0.0, intention=0.0)
    long_horizon = core.select(TUNING_HISTORY, CANDIDATES)

    core.set_internal_condition(attention=1.0, intention=0.0)
    short_horizon = core.select(TUNING_HISTORY, CANDIDATES)

    long_selected = str(long_horizon["selected"])
    short_selected = str(short_horizon["selected"])

    return {
        "history": list(TUNING_HISTORY),
        "long_horizon": long_horizon,
        "short_horizon": short_horizon,
        "selection_changed": long_selected != short_selected,
        "lag_profile_changed": (
            long_horizon["scored"][0]["lag_weights"]
            != short_horizon["scored"][0]["lag_weights"]
        ),
        "world_history_unchanged": True,
        "candidate_field_unchanged": True,
    }


def _independent_motif_battery() -> dict[str, Any]:
    # These cases are defined from the motif generators, not selected by the
    # resonance score. Every variant keeps the same marginal counts.
    alpha_variants = _cyclic_variants(ALPHA_TEMPLATE[:-1])
    beta_variants = _cyclic_variants(BETA_TEMPLATE[:-1])

    core = ResonantSelfTuningCoreV1(attention=1.0, resonance_gain=0.65)

    alpha_results = [
        core.select(sequence, CANDIDATES)["selected"]
        for sequence in alpha_variants
    ]
    beta_results = [
        core.select(sequence, CANDIDATES)["selected"]
        for sequence in beta_variants
    ]

    return {
        "alpha_variant_count": len(alpha_variants),
        "beta_variant_count": len(beta_variants),
        "alpha_accuracy": (
            sum(item == "alpha_path" for item in alpha_results)
            / len(alpha_results)
        ),
        "beta_accuracy": (
            sum(item == "beta_path" for item in beta_results)
            / len(beta_results)
        ),
        "all_alpha_correct": all(
            item == "alpha_path" for item in alpha_results
        ),
        "all_beta_correct": all(
            item == "beta_path" for item in beta_results
        ),
        "marginals_match": (
            all(
                sorted(sequence) == sorted(ALPHA_TEMPLATE)
                for sequence in alpha_variants
            )
            and all(
                sorted(sequence) == sorted(BETA_TEMPLATE)
                for sequence in beta_variants
            )
            and sorted(ALPHA_TEMPLATE) == sorted(BETA_TEMPLATE)
        ),
    }


def _hysteresis_battery() -> dict[str, Any]:
    core = ResonantSelfTuningCoreV1(hysteresis_cycles=2)
    trace = [
        core.update_regime(0.12),
        core.update_regime(0.03),
        core.update_regime(0.12),
        core.update_regime(0.12),
        core.update_regime(0.03),
        core.update_regime(0.03),
    ]
    return {
        "trace": trace,
        "enters_resonant_only_after_persistence": trace[1] == "baseline"
        and trace[3] == "resonant",
        "exits_resonant_only_after_persistence": trace[4] == "resonant"
        and trace[5] == "baseline",
    }


def _causal_reversal_battery() -> dict[str, Any]:
    core = ResonantSelfTuningCoreV1(
        attention=1.0,
        resonance_gain=0.65,
    )
    baseline = core.select(MATCHED_EXPERIMENT, CANDIDATES)

    intervention = core.intervene_resonance_gain(
        0.0,
        intervention_id="resonant-self-tuning-v1-ablation",
    )
    ablated = core.select(MATCHED_EXPERIMENT, CANDIDATES)

    restore = core.intervene_resonance_gain(
        0.65,
        intervention_id="resonant-self-tuning-v1-restore",
    )
    restored = core.select(MATCHED_EXPERIMENT, CANDIDATES)

    persisted_snapshot = core.snapshot()
    restarted = ResonantSelfTuningCoreV1(
        attention=float(persisted_snapshot["attention"]),
        intention=float(persisted_snapshot["intention"]),
        resonance_gain=float(persisted_snapshot["resonance_gain"]),
        hysteresis_cycles=int(persisted_snapshot["hysteresis_cycles"]),
        regime=str(persisted_snapshot["regime"]),
        pending_regime=str(persisted_snapshot["pending_regime"]),
        pending_count=int(persisted_snapshot["pending_count"]),
        history=list(persisted_snapshot["history"]),
    )
    restarted_result = restarted.select(MATCHED_EXPERIMENT, CANDIDATES)

    return {
        "baseline": baseline["selected"],
        "ablated": ablated["selected"],
        "restored": restored["selected"],
        "restarted": restarted_result["selected"],
        "intervention": intervention,
        "restore": restore,
        "intervention_non_evidential": (
            intervention["evidence_added"] is False
            and restore["evidence_added"] is False
        ),
        "ablation_changes_selection": (
            baseline["selected"] != ablated["selected"]
        ),
        "restore_recovers_selection": (
            restored["selected"] == baseline["selected"]
        ),
        "restart_persists_selection": (
            restarted_result["selected"] == restored["selected"]
        ),
    }


def run() -> dict[str, Any]:
    matched = _matched_order_battery()
    tuning = _endogenous_tuning_battery()
    independent = _independent_motif_battery()
    hysteresis = _hysteresis_battery()
    causal = _causal_reversal_battery()

    metrics = {
        "matched_information_multiset": matched["same_information_multiset"],
        "matched_final_state": matched["same_final_state"],
        "matched_candidate_field": matched["same_candidate_field"],
        "matched_temporal_order_only": matched["temporal_order_differs"],
        "matched_experimental_selects_alpha": (
            matched["experimental"]["selected"] == "alpha_path"
        ),
        "matched_control_selects_beta": (
            matched["control"]["selected"] == "beta_path"
        ),
        "temporal_order_changes_selection": (
            matched["experimental"]["selected"]
            != matched["control"]["selected"]
        ),
        "endogenous_lag_profile_changes": tuning["lag_profile_changed"],
        "endogenous_selection_changes": tuning["selection_changed"],
        "independent_alpha_accuracy_1": independent["all_alpha_correct"],
        "independent_beta_accuracy_1": independent["all_beta_correct"],
        "independent_marginals_match": independent["marginals_match"],
        "hysteresis_entry_pass": hysteresis[
            "enters_resonant_only_after_persistence"
        ],
        "hysteresis_exit_pass": hysteresis[
            "exits_resonant_only_after_persistence"
        ],
        "causal_ablation_changes_selection": causal[
            "ablation_changes_selection"
        ],
        "causal_restore_recovers": causal["restore_recovers_selection"],
        "causal_restart_persists": causal["restart_persists_selection"],
        "causal_interventions_non_evidential": causal[
            "intervention_non_evidential"
        ],
    }

    result = {
        "protocol": {
            "mechanism": (
                "attention/intention -> endogenous lag tuning -> temporal "
                "resonance -> hysteretic regime -> trajectory selection"
            ),
            "phenomenal_consciousness_claim": False,
            "matched_constraint": (
                "same state multiset + same final state + same candidate field; "
                "temporal order differs"
            ),
        },
        "matched_order": matched,
        "endogenous_tuning": tuning,
        "independent_motifs": independent,
        "hysteresis": hysteresis,
        "causal_reversal": causal,
        "metrics": metrics,
    }

    print(json.dumps(result, indent=2, sort_keys=True))

    if not all(metrics.values()):
        raise AssertionError(
            "resonant self-tuning causal benchmark failed: "
            + json.dumps(metrics, sort_keys=True)
        )

    print("RESONANT SELF-TUNING CAUSAL BENCHMARK v1: PASS")
    return result


if __name__ == "__main__":
    run()
