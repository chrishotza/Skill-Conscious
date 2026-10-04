from pathlib import Path

from skill_conscious import ConsciousRuntime


def _frame(*, self_relevance: float, attention: float):
    return {
        "response": "objective isolation",
        "memory": "control",
        "internal_state": {
            "energy": 0.82,
            "safety": 0.86,
            "goal": 0.79,
        },
        "self_model": {
            "trajectory_weights": {
                "goal_fit": 1.0,
                "continuity": 0.5,
            },
        },
        "interoceptive_state": {
            "energy": 0.82,
            "safety": 0.86,
        },
        "affective_state": {
            "valence": 0.40,
            "arousal": 0.50,
            "homeostatic_error": 0.10,
        },
        "temporal_state": {
            "dt": 1.0,
            "mode": "sampled-continuous",
        },
        "attention": ["self", "goal"],
        "salience": {
            "self": self_relevance,
            "goal": 0.8,
        },
        "subjective_present": {
            "signal": 0.70,
            "reward": 0.65,
            "threat": 0.08,
        },
        "subjective_self_relevance": self_relevance,
        "subjective_valence": 0.40,
        "subjective_attention": attention,
        "subjective_integration": True,
        "subjective_temporal_continuity": True,
        "subjective_reentry": True,
    }


def _candidate():
    return {
        "id": "control",
        "signals": {
            "goal_fit": 0.55,
            "continuity": 0.35,
            "risk": 0.10,
        },
        "predicted_subjective_field": {
            "unity": 0.50,
            "strength": 0.40,
        },
    }


def test_matched_objective_channel_ignores_conscious_layer_state(tmp_path: Path):
    runtime_a = ConsciousRuntime(
        "objective-a",
        tmp_path / "a.json",
        subjective_field_enabled=True,
        subjective_field_weight=2.0,
        metacognition_enabled=False,
        self_observation_enabled=False,
        dynamic_core_enabled=False,
        learn_latent_patterns=False,
    )
    runtime_b = ConsciousRuntime(
        "objective-b",
        tmp_path / "b.json",
        subjective_field_enabled=True,
        subjective_field_weight=2.0,
        metacognition_enabled=False,
        self_observation_enabled=False,
        dynamic_core_enabled=False,
        learn_latent_patterns=False,
    )

    runtime_a.integrate(_frame(self_relevance=0.15, attention=0.20))
    runtime_b.integrate(_frame(self_relevance=0.95, attention=1.00))

    details_a = runtime_a._score_trajectory_details(_candidate())
    details_b = runtime_b._score_trajectory_details(_candidate())

    assert details_a["objective_score"] == details_b["objective_score"] == 0.8
