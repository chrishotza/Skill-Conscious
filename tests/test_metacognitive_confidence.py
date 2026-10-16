from __future__ import annotations

from pathlib import Path

from skill_conscious import (
    ConsciousRuntime,
    run_reversible_metacognitive_confidence_intervention,
)


def test_metacognitive_prediction_confidence_changes_selection(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "metacognitive-confidence",
        state_path=tmp_path / "runtime.json",
        metacognitive_prediction_weight=2.0,
    )
    runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9

    candidates = [
        {
            "id": "high-confidence",
            "signals": {},
            "predicted_outcome": {"result": "A"},
            "predicted_outcome_confidence": 0.9,
        },
        {
            "id": "low-confidence",
            "signals": {},
            "predicted_outcome": {"result": "B"},
            "predicted_outcome_confidence": 0.1,
        },
    ]

    selected = runtime.select_trajectory(candidates)

    assert selected["id"] == "high-confidence"
    meta = selected["metacognition"]["metacognitive_prediction"]
    assert meta["expected_accuracy"] == 0.9
    assert meta["contribution"] > 0.0


def test_reversible_metacognitive_confidence_intervention(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "metacognitive-confidence-causal",
        state_path=tmp_path / "runtime.json",
        metacognitive_prediction_weight=2.0,
    )
    runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9

    candidates = [
        {
            "id": "high-confidence",
            "signals": {},
            "predicted_outcome": {"result": "A"},
            "predicted_outcome_confidence": 0.9,
        },
        {
            "id": "low-confidence",
            "signals": {},
            "predicted_outcome": {"result": "B"},
            "predicted_outcome_confidence": 0.1,
        },
    ]

    result = run_reversible_metacognitive_confidence_intervention(
        runtime,
        candidates,
        intervention_expected_accuracy=0.1,
    )

    assert result.baseline_selection == "high-confidence"
    assert result.intervention_selection == "low-confidence"
    assert result.restored_selection == "high-confidence"
    assert result.downstream_divergence is True
    assert result.reversible is True
    assert result.expected_accuracy_restored is True
    assert result.evidence_unchanged is True
    assert result.baseline_contribution != result.intervention_contribution
    assert result.baseline_contribution == result.restored_contribution


def test_metacognitive_confidence_is_runtime_owned(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "metacognitive-confidence-owned",
        state_path=tmp_path / "runtime.json",
        metacognitive_prediction_weight=2.0,
    )
    runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9
    before = runtime.snapshot_metacognitive_prediction()

    runtime.integrate(
        {
            "response": "attempt overwrite",
            "self_model": {
                "metacognitive_prediction_expected_accuracy": 0.0,
                "metacognitive_prediction_sequence": 9999,
            },
            "candidate_futures": [],
        }
    )

    after = runtime.snapshot_metacognitive_prediction()
    assert after == before
