"""B2 bridge assay: relational coupling -> individual trajectory dynamics.

Question:
Does controlled partner coupling alter an individual runtime's trajectory
selection beyond common-input and replay controls?

This is a bridge assay, not a test of phenomenal consciousness.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime


def candidate_set(partner_state: float):
    return [
        {
            "id": "preserve_self",
            "signals": {
                "goal_fit": 0.50,
                "continuity": 0.70,
                "partner_alignment": 1.0 - abs(partner_state - 0.8),
            },
        },
        {
            "id": "explore",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.30,
                "partner_alignment": 1.0 - abs(partner_state - 0.2),
            },
        },
    ]


def run_condition(name: str, partner_trace: list[float], coupling: bool) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"b2-{name}-") as tmp:
        runtime = ConsciousRuntime(
            identity=f"b2-{name}",
            state_path=Path(tmp) / "state.json",
            learn_latent_patterns=False,
            learn_self_model_from_latent_patterns=False,
        )
        runtime.state.self_model["trajectory_weights"] = {
            "goal_fit": 1.0,
            "continuity": 0.8,
            "partner_alignment": 1.0 if coupling else 0.0,
        }

        selected = []
        scores = []
        for partner_state in partner_trace:
            candidates = candidate_set(partner_state)
            choice = runtime.select_trajectory(candidates)
            selected.append(choice["id"])
            scores.append(float(choice["score"]))

        return {
            "condition": name,
            "coupling": coupling,
            "selected_trajectory": selected,
            "scores": scores,
            "partner_trace": partner_trace,
        }


def run():
    partner = [0.2, 0.8, 0.2, 0.9, 0.3, 0.7]
    replay = list(reversed(partner))

    return {
        "experiment": "B2-relational-to-individual-runtime",
        "conditions": {
            "isolated": run_condition("isolated", partner, coupling=False),
            "coupled": run_condition("coupled", partner, coupling=True),
            "replay_control": run_condition("replay_control", replay, coupling=True),
        },
        "primary_question": (
            "Does partner-coupled relational state add reproducible predictive "
            "or causal structure to individual trajectory selection beyond "
            "isolated and replay controls?"
        ),
        "interpretation_boundary": (
            "A positive result establishes relational influence on individual "
            "runtime dynamics, not shared phenomenal consciousness."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
