from skill_conscious.experience_field import build_experience_field, profile_distance, sensory_counterfactual_action_delta


def _channels(scale=1.0):
    return [
        [scale * (0.2 * i + 0.03 * ((i % 2) - 0.5)) for i in range(64)],
        [scale * (0.2 * i + 0.02 * ((i % 3) - 1.0)) for i in range(64)],
        [scale * (0.2 * i - 0.02 * ((i % 4) - 1.5)) for i in range(64)],
    ]


def test_coupled_field_is_deterministic():
    args = dict(
        observation={"vision": 1.0, "audio": 0.2},
        expected={"vision": 0.0, "audio": 0.0},
        channels=_channels(),
        affective_weights={"vision": 1.0, "audio": 0.5},
        self_relevance_weights={"vision": 1.0, "audio": 1.0},
    )
    assert build_experience_field(**args)[0] == build_experience_field(**args)[0]


def test_field_couples_sensory_and_dynamic_features():
    profile, sensory, dynamic = build_experience_field(
        {"vision": 1.0}, {"vision": 0.0}, _channels(),
        affective_weights={"vision": 1.0}, self_relevance_weights={"vision": 1.0},
    )
    assert profile.prediction_error == sensory.prediction_error
    assert profile.dynamic_synchrony == dynamic.pairwise_correlation
    assert 0.0 <= profile.field_coherence <= 1.0
    assert 0.0 <= profile.dynamic_repertoire <= 1.0


def test_large_field_change_is_measurable():
    stable, *_ = build_experience_field({"vision": 0.0}, {"vision": 0.0}, _channels())
    perturbed, *_ = build_experience_field(
        {"vision": 1.0}, {"vision": 0.0},
        [[v * (-1 if i % 2 else 1) for i, v in enumerate(ch)] for ch in _channels()],
    )
    assert profile_distance(stable, perturbed) > 0.0


def test_sensory_counterfactual_is_zero_when_observation_matches_expectation():
    assert sensory_counterfactual_action_delta(0.4, {"vision": 0.2}, {"vision": 0.2}, affective_weights={"vision": 1.0}) == 0.0


def test_sensory_counterfactual_can_reverse_action_preference():
    delta = sensory_counterfactual_action_delta(
        0.1, {"vision": 1.0}, {"vision": 0.0},
        affective_weights={"vision": -1.0}, affect_weight=1.0,
    )
    assert delta < 0.0


def test_coupling_weights_reject_nonfinite_negative_boolean_and_misspelled_keys():
    import pytest

    invalid = [
        {"sensory_coherence": float("nan")},
        {"dynamic_synchrony": float("inf")},
        {"sensory_coherence": float("-inf")},
        {"sensory_coherence": -1.0},
        {"sensory_coherence": True},
        {"sensory_coherence": "not-a-number"},
        {"sensory_coherance": 1.0},
        {"sensory_coherence": 1e308, "dynamic_synchrony": 1e308},
    ]
    for weights in invalid:
        with pytest.raises(ValueError, match="coupling weight"):
            build_experience_field(
                {"vision": 0.5}, {"vision": 0.0}, _channels(), coupling_weights=weights
            )


def test_nonnegative_finite_coupling_weights_keep_explicit_control():
    sensor_only, *_ = build_experience_field(
        {"vision": 1.0}, {"vision": 0.0}, _channels(),
        coupling_weights={"sensory_coherence": 1.0, "dynamic_synchrony": 0.0},
    )
    dynamic_only, *_ = build_experience_field(
        {"vision": 1.0}, {"vision": 0.0}, _channels(),
        coupling_weights={"sensory_coherence": 0.0, "dynamic_synchrony": 1.0},
    )
    assert sensor_only.field_coherence == sensor_only.sensory_coherence
    assert 0.0 <= dynamic_only.field_coherence <= 1.0
    assert sensor_only.field_coherence != dynamic_only.field_coherence
