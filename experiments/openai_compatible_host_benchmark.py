"""Real-host causal benchmark for OpenAI-compatible model endpoints.

The external model is used as a host-facing language/action planner, but the
benchmark keeps candidate futures and authoritative consequences controlled.
This prevents model prose from becoming the causal measurement.

Works with OpenAI-compatible endpoints such as a local Ollama-compatible
server. Credentials/configuration are supplied through environment variables.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping
from urllib.error import HTTPError, URLError

from skill_conscious import ConsciousHostLoop, ConsciousRuntime


CANDIDATES = [
    {
        "id": "stabilize",
        "signals": {"goal_fit": 1.0},
    },
    {
        "id": "explore",
        "signals": {"goal_fit": 0.95},
        "predicted_interoceptive_state": {"energy": 1.0},
    },
]


class OpenAICompatibleModel:
    def __init__(
        self,
        *,
        endpoint: str,
        model: str,
        api_key: str | None = None,
        timeout: int = 120,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    def __call__(self, prompt: str) -> Mapping[str, Any]:
        system = (
            "You are the host model for a causal architecture benchmark. "
            "Do not claim or assess phenomenal consciousness. "
            "Return a JSON object only. Your response is auxiliary metadata; "
            "the runtime owns trajectory selection and authoritative state."
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "stream": False,
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.endpoint}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                **(
                    {"Authorization": f"Bearer {self.api_key}"}
                    if self.api_key
                    else {}
                ),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except (HTTPError, URLError) as exc:
            raise RuntimeError(f"model endpoint request failed: {exc}") from exc

        data = json.loads(raw)
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("model response contained no choices")
        message = choices[0].get("message", {})
        text = str(message.get("content", "")).strip()
        fence = chr(96) * 3
        if text.startswith(fence):
            text = text.strip(chr(96)).strip()
            if text.lower().startswith("json"):
                text = text[4:].strip()
        parsed = json.loads(text)
        if not isinstance(parsed, Mapping):
            raise RuntimeError("model frame must be a JSON object")
        return dict(parsed)


def _controlled_model(raw_model):
    def model(prompt: str) -> Mapping[str, Any]:
        raw = dict(raw_model(prompt))
        frame: dict[str, Any] = {
            "candidate_futures": [dict(item) for item in CANDIDATES],
        }
        if "response" in raw:
            frame["response"] = str(raw["response"])
        return frame

    return model


def _runtime(root: Path, label: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        label,
        state_path=root / f"{label}.json",
        report_enabled=False,
        metacognition_enabled=False,
    )
    runtime.state.self_model = {
        "homeostatic_targets": {"energy": 1.0},
        "trajectory_weights": {
            "goal_fit": 1.0,
            "homeostatic_fit": 1.0,
        },
    }
    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)
    return runtime


def _run_intact(root: Path, model) -> dict[str, Any]:
    runtime = _runtime(root, "external-intact")
    loop = ConsciousHostLoop(
        runtime,
        model=_controlled_model(model),
        execute_action=lambda _trajectory, _snapshot: {
            "status": "success",
            "interoceptive_state": {"energy": 0.0},
            "self_state": {"focus": 0.2},
        },
    )
    result = loop.step("Choose the next trajectory.")
    selected = result.get("selected_trajectory") or {}
    next_selected = result.get("next_trajectory") or {}
    return {
        "condition": "intact",
        "selected": str(selected.get("id", "")),
        "next_selected": str(next_selected.get("id", "")),
        "action_history_length": len(runtime.state.action_history),
        "consequence": dict(result["consequence"] or {}),
    }


def _run_ablated(root: Path, model) -> dict[str, Any]:
    runtime = _runtime(root, "external-ablated")
    controlled = _controlled_model(model)

    first_frame = dict(controlled(runtime.prepare("Choose the next trajectory.")))
    runtime.integrate(first_frame)
    selected = dict(runtime.state.selected_trajectory or {})
    action_receipt = runtime.begin_action(selected)
    outcome = {
        "status": "success",
        "interoceptive_state": {"energy": 0.0},
        "self_state": {"focus": 0.2},
    }
    runtime.complete_action(outcome)

    runtime.state.interoceptive_state = {"energy": 1.0}
    runtime.refresh_affective_state()
    runtime.store.save(runtime.state)

    second = dict(
        controlled(
            runtime.prepare_consequence(str(selected["id"]), outcome)
        )
    )
    runtime.integrate(second)
    next_selected = dict(runtime.state.selected_trajectory or {})

    return {
        "condition": "consequence_ablation",
        "selected": str(selected.get("id", "")),
        "next_selected": str(next_selected.get("id", "")),
        "action_history_length": len(runtime.state.action_history),
        "consequence": outcome,
        "action_id": action_receipt["action_id"],
        "evidence_added": False,
    }


def run(*, endpoint: str, model_name: str, api_key: str | None) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        model = OpenAICompatibleModel(
            endpoint=endpoint,
            model=model_name,
            api_key=api_key,
        )

        intact = _run_intact(root, model)
        ablated = _run_ablated(root, model)

        result = {
            "provider": {
                "endpoint": endpoint,
                "model": model_name,
            },
            "conditions": [ablated, intact],
            "metrics": {
                "same_initial_selection": intact["selected"] == ablated["selected"],
                "intact_changes_next_selection": (
                    intact["next_selected"] != intact["selected"]
                ),
                "ablation_preserves_initial_selection": (
                    ablated["next_selected"] == ablated["selected"]
                ),
                "causal_divergence": (
                    intact["next_selected"] != ablated["next_selected"]
                ),
                "authoritative_consequence_present": (
                    intact["consequence"].get("status") == "success"
                ),
            },
        }

        print(json.dumps(result, indent=2, sort_keys=True))
        if not all(
            [
                result["metrics"]["same_initial_selection"],
                result["metrics"]["intact_changes_next_selection"],
                result["metrics"]["ablation_preserves_initial_selection"],
                result["metrics"]["causal_divergence"],
                result["metrics"]["authoritative_consequence_present"],
            ]
        ):
            raise AssertionError("external host causal benchmark did not pass")

        print("OPENAI-COMPATIBLE HOST CAUSAL BENCHMARK v1: PASS")
        return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        default=os.getenv(
            "SKILL_CONSCIOUS_ENDPOINT",
            "http://127.0.0.1:11434/v1",
        ),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("SKILL_CONSCIOUS_MODEL", "llama3.1"),
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("SKILL_CONSCIOUS_API_KEY"),
    )
    args = parser.parse_args()
    run(
        endpoint=args.endpoint,
        model_name=args.model,
        api_key=args.api_key,
    )


if __name__ == "__main__":
    main()
