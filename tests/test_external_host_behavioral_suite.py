from __future__ import annotations

import json

import experiments.openai_compatible_host_benchmark as provider
from experiments.external_host_behavioral_suite import run


class _FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(
            {
                "choices": [
                    {
                        "message": {
                            "content": '{"response": "controlled host response"}'
                        }
                    }
                ]
            }
        ).encode("utf-8")


def test_external_host_behavioral_suite_is_quantitatively_causal(monkeypatch):
    monkeypatch.setattr(
        provider.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: _FakeResponse(),
    )

    result = run(
        endpoint="http://fake/v1",
        model_name="fake-model",
        api_key=None,
    )
    metrics = result["metrics"]

    assert result["task_count"] == 5
    assert metrics["initial_match_rate"] == 1.0
    assert metrics["causal_divergence_rate"] == 1.0
    assert metrics["intact_switch_rate"] == 1.0
    assert metrics["ablation_preservation_rate"] == 1.0
    assert metrics["intact_restart_persistence_rate"] == 1.0
    assert metrics["ablated_restart_persistence_rate"] == 1.0
    assert metrics["all_authoritative_outcomes_present"] is True
    assert metrics["all_interventions_non_evidential"] is True
