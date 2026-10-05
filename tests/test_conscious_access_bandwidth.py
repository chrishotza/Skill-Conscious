from skill_conscious import ConsciousHostLoop, ConsciousRuntime


def test_access_state_is_runtime_owned_persistent_and_no_report_compatible(tmp_path):
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime(
        "access-1",
        path,
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.integrate(
        {
            "self_model": {"homeostatic_targets": {"energy": 1.0}},
            "interoceptive_state": {"energy": 0.2},
            "salience": {"internal_condition": 0.9},
            "candidate_futures": [
                {"id": "a", "predicted_self_relevance": 0.4},
                {"id": "b", "predicted_self_relevance": 0.0},
            ],
        }
    )

    access = runtime.snapshot_access()
    assert access["capacity"] == 12
    assert access["candidate_count"] > 1
    assert access["compression_load"] > 0.0
    assert access["selected_keys"]
    assert access["revision"] == runtime.state.revision

    restarted = ConsciousRuntime(
        "access-1",
        path,
        report_enabled=False,
        metacognition_enabled=False,
    )
    assert restarted.snapshot_access() == access


def test_access_capacity_causally_changes_trajectory_and_restores(tmp_path):
    runtime = ConsciousRuntime(
        "bandwidth-causal",
        tmp_path / "state.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    frame = {
        "self_model": {"memory_hint": "persistent"},
        "interoceptive_state": {"energy": 0.4},
        "candidate_futures": [
            {
                "id": "self-model-path",
                "signals": {"goal_fit": 1.0},
                "access_keys": ["self_model"],
            },
            {
                "id": "interoceptive-path",
                "signals": {"goal_fit": 0.8},
                "access_keys": ["interoceptive_state"],
            },
        ],
    }

    runtime.set_access_capacity(2)
    runtime.integrate(frame)
    a = runtime.state.selected_trajectory["id"]
    access_a = runtime.snapshot_access()

    runtime.set_access_capacity(6)
    runtime.integrate(frame)
    b = runtime.state.selected_trajectory["id"]

    runtime.set_access_capacity(2)
    runtime.integrate(frame)
    c = runtime.state.selected_trajectory["id"]
    access_c = runtime.snapshot_access()

    assert a == "interoceptive-path"
    assert b == "self-model-path"
    assert c == a
    assert access_c["capacity"] == access_a["capacity"] == 2


def test_omitted_state_remains_persistent_but_is_absent_from_limited_present(tmp_path):
    runtime = ConsciousRuntime(
        "omission",
        tmp_path / "state.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.state.self_model = {"persistent_fact": "still here"}
    runtime.state.interoceptive_state = {"energy": 0.3}
    runtime.set_access_capacity(2)

    present = runtime.present_field("external event")
    selected = set(present["access_state"]["selected_keys"])
    limited = present["limited_present"]

    assert runtime.state.self_model["persistent_fact"] == "still here"
    assert "self_model" in present["access_state"]["omitted_keys"]
    assert "self_model" not in limited
    assert selected


def test_model_cannot_forge_runtime_access_state(tmp_path):
    runtime = ConsciousRuntime(
        "protected-access",
        tmp_path / "state.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.set_access_capacity(2)
    before = runtime.snapshot_access()

    runtime.integrate(
        {
            "access_state": {
                "capacity": 999,
                "selected_keys": ["self_model"],
                "omitted_keys": [],
            },
            "access_capacity": 999,
            "self_model": {"x": 1},
            "interoceptive_state": {"energy": 0.2},
            "candidate_futures": [
                {
                    "id": "self-model-path",
                    "signals": {"goal_fit": 1.0},
                    "access_keys": ["self_model"],
                },
                {
                    "id": "interoceptive-path",
                    "signals": {"goal_fit": 0.8},
                    "access_keys": ["interoceptive_state"],
                },
            ],
        }
    )

    after = runtime.snapshot_access()
    assert after["capacity"] == before["capacity"] == 2
    assert after["selected_keys"] == before["selected_keys"]
    assert "access_state" not in runtime.state.self_model


def test_access_intervention_adds_no_learning_evidence(tmp_path):
    runtime = ConsciousRuntime(
        "access-intervention",
        tmp_path / "state.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    history_before = list(runtime.state.history)
    log_before = list(runtime.state.transformation_log)

    receipt = runtime.set_access_capacity(3)

    assert receipt["evidence_added"] is False
    assert runtime.state.history == history_before
    assert runtime.state.transformation_log == log_before
    assert runtime.snapshot_access()["capacity"] == 3
