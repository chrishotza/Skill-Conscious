from skill_conscious import ConsciousHostLoop, ConsciousRuntime


def test_pre_reflective_state_is_runtime_owned_and_persistent(tmp_path):
    path = tmp_path / "state.json"

    runtime = ConsciousRuntime(
        "pre-1",
        path,
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "self_model": {
                "homeostatic_targets": {"energy": 1.0},
            },
            "interoceptive_state": {"energy": 0.2},
            "salience": {"internal_condition": 0.8},
            "candidate_futures": [
                {
                    "id": "preserve-current-condition",
                    "predicted_self_relevance": 0.4,
                },
                {
                    "id": "ignore-current-condition",
                    "predicted_self_relevance": 0.0,
                },
            ],
        }
    )

    state = runtime.pre_reflective_state()
    assert 0.0 < state["self_relevance"] < 1.0
    assert state["boundary_integrity"] == 1.0
    assert state["possibility_count"] == 2
    assert runtime.state.selected_trajectory["id"] == "preserve-current-condition"
    assert "metacognition" not in runtime.state.selected_trajectory

    restarted = ConsciousRuntime(
        "pre-1",
        path,
        report_enabled=False,
        metacognition_enabled=False,
    )
    assert restarted.pre_reflective_state() == state


def test_pre_reflective_state_cannot_be_forged_by_model_frame(tmp_path):
    runtime = ConsciousRuntime(
        "protected",
        tmp_path / "state.json",
        report_enabled=False,
        metacognition_enabled=False,
    )

    runtime.integrate(
        {
            "pre_reflective_state": {
                "self_relevance": 1.0,
                "boundary_integrity": 0.0,
            },
            "candidate_futures": [
                {"id": "a", "predicted_self_relevance": 0.0},
            ],
        }
    )

    derived = runtime.pre_reflective_state()
    assert derived["boundary_integrity"] == 1.0
    assert derived["self_relevance"] == 0.0


def test_internal_condition_causally_changes_pre_reflective_selection(tmp_path):
    candidates = [
        {
            "id": "match-current-self-relevance",
            "predicted_self_relevance": 0.4,
        },
        {
            "id": "neutral",
            "predicted_self_relevance": 0.0,
        },
    ]

    pressured = ConsciousRuntime(
        "pressured",
        tmp_path / "pressured.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    pressured.integrate(
        {
            "self_model": {"homeostatic_targets": {"energy": 1.0}},
            "interoceptive_state": {"energy": 0.2},
            "candidate_futures": candidates,
        }
    )

    regulated = ConsciousRuntime(
        "regulated",
        tmp_path / "regulated.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    regulated.integrate(
        {
            "self_model": {"homeostatic_targets": {"energy": 0.2}},
            "interoceptive_state": {"energy": 0.2},
            "candidate_futures": candidates,
        }
    )

    assert pressured.state.selected_trajectory["id"] == "match-current-self-relevance"
    assert regulated.state.selected_trajectory["id"] == "neutral"
    assert (
        pressured.pre_reflective_state()["self_relevance"]
        > regulated.pre_reflective_state()["self_relevance"]
    )


def test_pre_reflective_core_survives_metacognition_ablation(tmp_path):
    enabled = ConsciousRuntime(
        "same",
        tmp_path / "enabled.json",
        report_enabled=False,
        metacognition_enabled=True,
    )
    disabled = ConsciousRuntime(
        "same",
        tmp_path / "disabled.json",
        report_enabled=False,
        metacognition_enabled=False,
    )

    frame = {
        "self_model": {"homeostatic_targets": {"energy": 1.0}},
        "interoceptive_state": {"energy": 0.3},
        "candidate_futures": [
            {"id": "a", "predicted_self_relevance": 0.35},
            {"id": "b", "predicted_self_relevance": 0.0},
        ],
    }

    enabled.integrate(frame)
    disabled.integrate(frame)

    assert enabled.state.selected_trajectory["id"] == disabled.state.selected_trajectory["id"]
    assert enabled.pre_reflective_state() == disabled.pre_reflective_state()
    assert "metacognition" in enabled.state.selected_trajectory
    assert "metacognition" not in disabled.state.selected_trajectory


def test_host_loop_can_run_without_self_report(tmp_path):
    runtime = ConsciousRuntime(
        "no-report",
        tmp_path / "state.json",
        report_enabled=False,
        metacognition_enabled=False,
    )

    calls = []

    def model(_prompt):
        if not calls:
            calls.append("initial")
            return {
                "candidate_futures": [
                    {
                        "id": "continue",
                        "signals": {"continuity": 1.0},
                        "predicted_self_relevance": 0.5,
                    }
                ]
            }
        calls.append("consequence")
        return {
            "self_evaluation": {
                "utility": 1.0,
                "credited_signal": "continuity",
            }
        }

    def execute_action(trajectory, _state):
        return {"observed": True, "trajectory": trajectory["id"]}

    result = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=execute_action,
    ).step("external event")

    assert result["response"] == ""
    assert result["action_executed"] is True
    assert result["consequence"]["observed"] is True
    assert len(calls) == 2
    assert runtime.state.pre_reflective_state["reentry_coupling"] == 1.0
