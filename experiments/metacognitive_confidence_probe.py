from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from skill_conscious import (
    ConsciousRuntime,
    run_reversible_metacognitive_confidence_intervention,
)


def main() -> None:
    with TemporaryDirectory() as tmp:
        runtime = ConsciousRuntime(
            "metacognitive-confidence-probe",
            state_path=Path(tmp) / "runtime.json",
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
        print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
