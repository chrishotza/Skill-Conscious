from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .core import ConsciousRuntime


@dataclass(frozen=True)
class ReversibleMetacognitiveConfidenceInterventionResult:
    baseline_selection: str
    intervention_selection: str
    restored_selection: str
    baseline_contribution: float
    intervention_contribution: float
    restored_contribution: float
    downstream_divergence: bool
    reversible: bool
    expected_accuracy_restored: bool
    evidence_unchanged: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_selection": self.baseline_selection,
            "intervention_selection": self.intervention_selection,
            "restored_selection": self.restored_selection,
            "baseline_contribution": self.baseline_contribution,
            "intervention_contribution": self.intervention_contribution,
            "restored_contribution": self.restored_contribution,
            "downstream_divergence": self.downstream_divergence,
            "reversible": self.reversible,
            "expected_accuracy_restored": self.expected_accuracy_restored,
            "evidence_unchanged": self.evidence_unchanged,
        }


def run_reversible_metacognitive_confidence_intervention(
    runtime: ConsciousRuntime,
    candidates: list[Mapping[str, Any]],
    *,
    intervention_expected_accuracy: float,
) -> ReversibleMetacognitiveConfidenceInterventionResult:
    snapshot = runtime.snapshot_metacognitive_prediction()
    before_evidence = deepcopy(snapshot.get("evidence", {}))

    baseline = runtime.select_trajectory(candidates)
    runtime.intervene_metacognitive_prediction_expected_accuracy(
        intervention_expected_accuracy,
        persist=False,
        intervention_id="metacognitive-confidence",
    )
    intervention = runtime.select_trajectory(candidates)
    runtime.restore_metacognitive_prediction(
        snapshot,
        persist=False,
        intervention_id="metacognitive-confidence",
    )
    restored = runtime.select_trajectory(candidates)

    baseline_meta = dict(baseline.get("metacognition", {}))
    intervention_meta = dict(intervention.get("metacognition", {}))
    restored_meta = dict(restored.get("metacognition", {}))

    baseline_contribution = float(
        dict(baseline_meta.get("metacognitive_prediction", {})).get(
            "contribution",
            0.0,
        )
    )
    intervention_contribution = float(
        dict(intervention_meta.get("metacognitive_prediction", {})).get(
            "contribution",
            0.0,
        )
    )
    restored_contribution = float(
        dict(restored_meta.get("metacognitive_prediction", {})).get(
            "contribution",
            0.0,
        )
    )

    after = runtime.snapshot_metacognitive_prediction()
    return ReversibleMetacognitiveConfidenceInterventionResult(
        baseline_selection=str(baseline.get("id", "")),
        intervention_selection=str(intervention.get("id", "")),
        restored_selection=str(restored.get("id", "")),
        baseline_contribution=baseline_contribution,
        intervention_contribution=intervention_contribution,
        restored_contribution=restored_contribution,
        downstream_divergence=(
            str(baseline.get("id", "")) != str(intervention.get("id", ""))
        ),
        reversible=(
            str(baseline.get("id", "")) == str(restored.get("id", ""))
            and baseline_meta.get("selected_signal_contributions", {})
            == restored_meta.get("selected_signal_contributions", {})
        ),
        expected_accuracy_restored=(
            after.get("expected_accuracy") == snapshot.get("expected_accuracy")
        ),
        evidence_unchanged=(
            after.get("evidence", {}) == before_evidence
            and after.get("sequence") == snapshot.get("sequence")
        ),
    )
