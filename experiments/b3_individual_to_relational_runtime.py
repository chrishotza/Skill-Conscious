"""B3 bridge assay: individual self-model intervention -> relational dynamics.

Question:
Does intervening on one agent's persistent self-model alter the trajectory
of the coupled system beyond a matched generic-state intervention?

This is a bridge assay, not a test of phenomenal consciousness.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime


def build_agent(identity: str, root: Path) -> ConsciousRuntime:
    return ConsciousRuntime(
        identity=identity,
        state_path=root / f"{identity}.json",
        learn_latent_patterns=False,
        learn_self_model_from_latent_patterns=False,
    )


def select(runtime: ConsciousRuntime, partner_state: float):
    candidates = [
        {
            "id": "stabilize",
            "signals": {
                "goal_fit": 0.45,
                "continuity": 0.80,
                "partner_alignment": 1.0 - abs(partner_state - 0.8),
            },
        },
        {
            "id": "explore",
            "signals": {
                "goal_fit": 0.55,
                "continuity": 0.25,
                "partner_alignment": 1.0 - abs(partner_state - 0.2),
            },
        },
    ]
    return runtime.select_trajectory(candidates)


def run_trial(condition: str, root: Path) -> dict:
    a = build_agent(f"a-{condition}", root)
    b = build_agent(f"b-{condition}", root)

    a.state.self_model["trajectory_weights"] = {
        "goal_fit": 1.0,
        "continuity": 1.0,
        "partner_alignment": 0.8,
    }

    if condition == "self_model_intervention":
        a.state.self_model["trajectory_weights"]["continuity"] = 2.5
    elif condition == "generic_state_control":
        a.state.self_state["control_parameter"] = 2.5

    partner_state = 0.6
    a_choice = select(a, partner_state)
    # B receives only A's executed trajectory ID as the relational signal.
    encoded = 0.85 if a_choice["id"] == "stabilize" else 0.15
    b_choice = select(b, encoded)

    return {
        "condition": condition,
        "a_selected": a_choice["id"],
        "a_score": float(a_choice["score"]),
        "b_selected": b_choice["id"],
        "b_score": float(b_choice["score"]),
        "relational_signal_from_A": encoded,
        "a_self_model": dict(a.state.self_model),
        "a_self_state": dict(a.state.self_state),
    }


def run():
    with tempfile.TemporaryDirectory(prefix="b3-individual-relational-") as tmp:
        root = Path(tmp)
        return {
            "experiment": "B3-individual-to-relational-runtime",
            "conditions": [
                run_trial("baseline", root),
                run_trial("self_model_intervention", root),
                run_trial("generic_state_control", root),
            ],
            "primary_question": (
                "Does an intervention on agent A's self-model alter the "
                "coupled relational trajectory through A's selected action, "
                "beyond a matched generic-state intervention?"
            ),
            "interpretation_boundary": (
                "A positive result establishes cross-level causal propagation "
                "from an individual intervention into relational dynamics. "
                "It does not establish shared phenomenal consciousness."
            ),
        }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
