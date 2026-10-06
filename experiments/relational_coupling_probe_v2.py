"""Relational coupling probe v2.

The two agents receive the same common drive plus independent private drives.
The coupled condition adds reciprocal state coupling; the sham condition
replays an isolated partner trajectory without reciprocal feedback.

This tests relational predictive structure, not phenomenal consciousness.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Config:
    steps: int = 1200
    decay: float = 0.78
    common_gain: float = 0.20
    private_gain: float = 0.15
    coupling: float = 0.18


def common_drive(t: int) -> float:
    return 0.6 * np.sin(t / 19.0) + 0.25 * np.sin(t / 7.0)


def private_a(t: int) -> float:
    return 0.15 * np.sin(t / 11.0) + 0.05 * np.cos(t / 17.0)


def private_b(t: int) -> float:
    return 0.15 * np.sin(t / 13.0) + 0.05 * np.cos(t / 23.0)


def simulate(cfg: Config, coupling: float, replay: bool = False):
    common = np.array([common_drive(t) for t in range(cfg.steps)])
    drive_a = np.array([private_a(t) for t in range(cfg.steps)])
    drive_b = np.array([private_b(t) for t in range(cfg.steps)])

    a = np.zeros(cfg.steps)
    b = np.zeros(cfg.steps)
    replay_a = np.zeros(cfg.steps)
    replay_b = np.zeros(cfg.steps)

    for t in range(cfg.steps - 1):
        replay_a[t + 1] = (
            cfg.decay * replay_a[t]
            + cfg.common_gain * common[t]
            + cfg.private_gain * drive_a[t]
        )
        replay_b[t + 1] = (
            cfg.decay * replay_b[t]
            + cfg.common_gain * common[t]
            + cfg.private_gain * drive_b[t]
        )

    for t in range(cfg.steps - 1):
        partner_a = replay_b[t] if replay else b[t]
        partner_b = replay_a[t] if replay else a[t]
        a[t + 1] = (
            cfg.decay * a[t]
            + cfg.common_gain * common[t]
            + cfg.private_gain * drive_a[t]
            + coupling * partner_a
        )
        b[t + 1] = (
            cfg.decay * b[t]
            + cfg.common_gain * common[t]
            + cfg.private_gain * drive_b[t]
            + coupling * partner_b
        )
    return a, b, common


def r2(y, pred):
    residual = float(np.sum((y - pred) ** 2))
    total = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - residual / total if total else 0.0


def fit_r2(y, X):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return r2(y, X @ beta)


def metrics(a, b, common):
    base_a = np.column_stack([np.ones(len(a) - 1), a[:-1], common[:-1]])
    with_a_partner = np.column_stack([base_a, b[:-1]])
    base_b = np.column_stack([np.ones(len(b) - 1), b[:-1], common[:-1]])
    with_b_partner = np.column_stack([base_b, a[:-1]])

    a_base = fit_r2(a[1:], base_a)
    a_partner = fit_r2(a[1:], with_a_partner)
    b_base = fit_r2(b[1:], base_b)
    b_partner = fit_r2(b[1:], with_b_partner)

    return {
        "a_partner_incremental_r2": a_partner - a_base,
        "b_partner_incremental_r2": b_partner - b_base,
        "a_base_r2": a_base,
        "b_base_r2": b_base,
    }


def run():
    cfg = Config()
    conditions = {
        "isolated": simulate(cfg, coupling=0.0),
        "coupled": simulate(cfg, coupling=cfg.coupling),
        "sham_replay": simulate(cfg, coupling=cfg.coupling, replay=True),
    }
    return {
        "assay": "relational-coupling-probe-v2",
        "configuration": cfg.__dict__,
        "metrics": {name: metrics(*series) for name, series in conditions.items()},
        "interpretation": (
            "The target effect is positive partner incremental R2 in the coupled "
            "condition relative to isolated and sham-replay controls. This is "
            "evidence about relational dynamics, not shared phenomenal experience."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
