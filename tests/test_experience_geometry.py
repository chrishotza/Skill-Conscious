from __future__ import annotations

from pathlib import Path

from skill_conscious import (
    FEATURE_ORDER,
    ConsciousRuntime,
    ExperienceState,
    build_experience_state,
    changed_dimensions,
    experience_distance,
)


def _snapshot(**overrides):
    state = {
        "valence": 0.0,
        "coherence": 1.0,
        "self_dissonance": 0.0,
        "salience": {"focus": 0.5},
        "pre_reflective_state": {
            "self_relevance": 0.2,
            "present_integrity": 1.0,
            "temporal_continuity": 1.0,
            "possibility_entropy": 0.5,
            "reentry_coupling": 0.0,
        },
        "access_state": {
            "access_entropy": 0.5,
            "compression_load": 0.25,
            "self_access_fraction": 0.8,
            "world_access_fraction": 0.2,
        },
        "self_model": {
            "metacognitive_prediction_expected_accuracy": 0.9,
            "metacognitive_prediction_error": 0.1,
            "self_observation_error": 0.0,
            "experience_field_state": {
                "field_coherence": 0.8,
                "dynamic_synchrony": 0.7,
                "dynamic_metastability": 0.3,
                "dynamic_complexity": 0.4,
                "dynamic_repertoire": 0.35,
            },
        },
    }
    state.update(overrides)
    return state


def test_experience_state_is_bounded_deterministic_and_dimensional():
    state = build_experience_state(_snapshot())
    assert state == build_experience_state(_snapshot())
    assert tuple(state.features) == FEATURE_ORDER
    assert len(state.features) >= 20
    assert all(0.0 <= value <= 1.0 for value in state.features.values())


def test_experience_distance_is_zero_and_symmetric():
    state = build_experience_state(_snapshot())
    other = build_experience_state(
        _snapshot(
            valence=1.0,
            pre_reflective_state={
                **_snapshot()["pre_reflective_state"],
                "self_relevance": 0.9,
            },
        )
    )
    assert experience_distance(state, state) == 0.0
    assert experience_distance(state, other) == experience_distance(other, state)


def test_geometry_localizes_present_access_and_self_change():
    before = build_experience_state(_snapshot())
    after = build_experience_state(
        _snapshot(
            access_state={
                "access_entropy": 0.2,
                "compression_load": 0.9,
                "self_access_fraction": 0.2,
                "world_access_fraction": 0.8,
            },
            pre_reflective_state={
                **_snapshot()["pre_reflective_state"],
                "self_relevance": 0.9,
            },
        )
    )
    changed = changed_dimensions(before, after, threshold=0.1)
    assert "access_compression" in changed
    assert "self_access_fraction" in changed
    assert "self_relevance" in changed


def test_access_intervention_changes_geometry_without_deleting_state(tmp_path: Path):
    runtime = ConsciousRuntime(
        "geometry-access",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.set_access_capacity(2)
    low = runtime.snapshot_experience_geometry()["current"]["features"]

    runtime.set_access_capacity(6)
    high = runtime.snapshot_experience_geometry()["current"]["features"]

    assert low["access_compression"] > high["access_compression"]
    assert runtime.state.self_model == {}


def test_runtime_persists_experience_geometry_transition(tmp_path: Path):
    runtime = ConsciousRuntime(
        "experience-geometry",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )

    runtime.integrate(
        {
            "valence": 0.75,
            "self_state": {"focus": 1.0},
            "candidate_futures": [
                {
                    "id": "observe",
                    "signals": {"goal_fit": 1.0},
                }
            ],
        }
    )

    snapshot = runtime.snapshot_experience_geometry()
    assert len(snapshot["history"]) == 1
    transition = snapshot["history"][0]
    assert 0.0 <= transition["distance"] <= 1.0
    assert transition["current"]["features"]["valence"] > 0.5
    assert "access_compression" in transition["current"]["features"]

    restarted = ConsciousRuntime(
        "experience-geometry",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    restarted_snapshot = restarted.snapshot_experience_geometry()
    assert restarted_snapshot["current"] == snapshot["current"]
    assert restarted_snapshot["history"] == snapshot["history"]


def test_llm_cannot_directly_write_experience_geometry(tmp_path: Path):
    runtime = ConsciousRuntime(
        "experience-geometry-owned",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "candidate_futures": [
                {"id": "observe", "signals": {"goal_fit": 1.0}},
            ],
        }
    )
    before = runtime.snapshot_experience_geometry()

    runtime.integrate(
        {
            "self_model": {
                "experience_geometry_current": {"features": {"valence": 1.0}},
                "experience_geometry_history": [{"forged": True}],
            },
            "candidate_futures": [
                {"id": "observe", "signals": {"goal_fit": 1.0}},
            ],
        }
    )

    after = runtime.snapshot_experience_geometry()
    assert after["current"] != {"features": {"valence": 1.0}}
    assert not any(
        item.get("forged") is True
        for item in after["history"]
        if isinstance(item, dict)
    )
    assert after["current"]["features"] == build_experience_state(
        runtime.snapshot()
    ).features
    assert len(after["history"]) == len(before["history"]) + 1
