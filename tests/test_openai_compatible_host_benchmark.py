from __future__ import annotations

import json

import experiments.openai_compatible_host_benchmark as benchmark


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


def test_openai_compatible_benchmark_runs_with_fake_endpoint(monkeypatch):
    monkeypatch.setattr(
        benchmark.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: _FakeResponse(),
    )

    result = benchmark.run(
        endpoint="http://fake/v1",
        model_name="fake-model",
        api_key=None,
    )
    metrics = result["metrics"]

    assert metrics["same_initial_selection"] is True
    assert metrics["intact_changes_next_selection"] is True
    assert metrics["ablation_preserves_initial_selection"] is True
    assert metrics["causal_divergence"] is True
    assert metrics["authoritative_consequence_present"] is True
