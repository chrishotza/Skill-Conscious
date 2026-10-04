from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime
from skill_conscious.metacognition import state_delta


def test_runtime_selection_returns_auditable_metacognitive_breakdown(tmp_path: Path):
    runtime = ConsciousRuntime("meta-trace", state_path=tmp_path / "runtime.json")
    runtime.state.valuation = {"goal_fit": 2.0}

    candidates = [
        {"id": "preserve", "signals": {"goal_fit": 0.80, "continuity": 0.20}},
        {"id": "explore", "signals": {"goal_fit": 0.40, "continuity": 0.30}},
    ]

    selected = runtime.select_trajectory(candidates)

    assert selected["id"] == "preserve"
    assert selected["metacognition"]["selected_signal_contributions"]["goal_fit"] == 1.6
    assert selected["metacognition"]["valuation_weights"]["goal_fit"] == 2.0


def test_integrate_persists_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime("meta-persist", state_path=tmp_path / "runtime.json")

    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )

    trace = runtime.state.self_model["metacognitive_trace"]
    assert trace["selected_id"] == "preserve"
    assert trace["selection_source"] == "runtime_scored"
    assert trace["sequence"] == 1
    assert trace["candidate_ids"] == ["preserve", "explore"]


def test_model_cannot_overwrite_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime("meta-owned", state_path=tmp_path / "runtime.json")

    runtime.integrate(
        {
            "response": "first",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )
    before = dict(runtime.state.self_model["metacognitive_trace"])

    runtime.integrate(
        {
            "response": "second",
            "self_model": {
                "metacognitive_trace": {"selected_id": "forged"},
                "metacognitive_sequence": 99999,
            },
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )

    after = runtime.state.self_model["metacognitive_trace"]
    assert after["selected_id"] == "preserve"
    assert after != before
    assert runtime.state.self_model["metacognitive_sequence"] == 2


def test_action_completion_closes_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime("meta-action", state_path=tmp_path / "runtime.json")
    runtime.integrate(
        {
            "response": "choose",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )
    selected = runtime.state.selected_trajectory
    assert selected is not None

    runtime.begin_action(selected)
    receipt = runtime.complete_action({"observed_change": "changed"})

    trace = runtime.state.self_model["metacognitive_trace"]
    assert receipt["action_id"] == trace["action"]["action_id"]
    assert trace["outcome"]["observed_change"] == "changed"
    assert "pending_action" in trace["state_delta"]


def test_self_observation_sees_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime(
        "meta-observed",
        state_path=tmp_path / "runtime.json",
        self_observation_enabled=True,
    )
    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )
    runtime.observe_self(persist=False)
    profile = runtime.snapshot_self_observation()["state"]
    assert profile["metacognitive_trace_presence"] == 1.0
    assert profile["decision_attribution_coverage"] == 1.0


def test_host_selected_trajectory_cannot_persist_forged_metacognition(tmp_path: Path):
    runtime = ConsciousRuntime("meta-forged-selection", state_path=tmp_path / "runtime.json")

    runtime.integrate(
        {
            "response": "host choice",
            "selected_trajectory": {
                "id": "host-choice",
                "score": 999.0,
                "metacognition": {
                    "selection_source": "runtime_scored",
                    "selected_id": "forged",
                },
            },
        }
    )

    assert runtime.state.selected_trajectory == {
        "id": "host-choice",
        "score": 999.0,
    }
    assert "metacognitive_trace" not in runtime.state.self_model


def test_metacognitive_trace_survives_restart(tmp_path: Path):
    state_path = tmp_path / "runtime.json"
    runtime = ConsciousRuntime("meta-restart", state_path=state_path)
    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )

    trace = dict(runtime.state.self_model["metacognitive_trace"])
    restarted = ConsciousRuntime("meta-restart", state_path=state_path)

    assert restarted.state.self_model["metacognitive_trace"] == trace


def test_metacognitive_action_history_delta_stays_compact(tmp_path: Path):
    runtime = ConsciousRuntime(
        "meta-compact-history",
        state_path=tmp_path / "runtime.json",
        report_enabled=False,
    )

    for index in range(10):
        runtime.integrate(
            {
                "response": f"cycle-{index}",
                "candidate_futures": [
                    {"id": "act", "signals": {"goal_fit": 0.8}},
                ],
            }
        )
        selected = runtime.state.selected_trajectory
        assert selected is not None
        runtime.begin_action(selected)
        runtime.complete_action(
            {
                "status": "success",
                "interoceptive_state": {"energy": 0.5},
            }
        )

    trace = runtime.state.self_model["metacognitive_trace"]
    history_delta = trace["state_delta"]["action_history"]

    assert history_delta["before"]["count"] == 9
    assert history_delta["after"]["count"] == 10
    assert history_delta["after"]["last_action_id"]
    assert "action" in trace


def test_metacognitive_state_delta_bounds_recursive_mappings():
    nested: dict[str, object] = {}
    nested["metacognitive_trace"] = {
        "state_delta": {
            "self_model": nested,
        }
    }
    before = {
        "self_model": nested,
        "workspace": {"last_action_receipt": nested},
        "action_history": [{"action_id": "a1"}],
    }
    after = {
        "self_model": nested,
        "workspace": {"last_action_receipt": nested, "new": 1},
        "action_history": [{"action_id": "a1"}, {"action_id": "a2"}],
    }

    delta = state_delta(before, after)

    assert delta["self_model"]["after"]["type"] == "mapping"
    assert delta["self_model"]["after"]["containers"]["metacognitive_trace"]["type"] == "mapping"
    assert delta["workspace"]["after"]["containers"]["last_action_receipt"]["type"] == "mapping"
    assert delta["action_history"]["before"]["count"] == 1
    assert delta["action_history"]["after"]["count"] == 2
