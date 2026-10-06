"""Deterministic coupled-agent dynamics assay.

Tests whether reciprocal coupling adds predictive information beyond each
agent's own state and a shared external input.

This is a relational-dynamics assay, not a shared-consciousness test.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Config:
    steps: int = 1200
    a: float = 0.78
    input_gain: float = 0.20
    coupling: float = 0.18


def shared_input(t: int) -> float:
    return 0.6 * np.sin(t / 19.0) + 0.25 * np.sin(t / 7.0)


def simulate(cfg: Config, *, coupling: float, replay: bool = False) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u = np.array([shared_input(t) for t in range(cfg.steps)], dtype=float)
    a = np.zeros(cfg.steps, dtype=float)
    b = np.zeros(cfg.steps, dtype=float)

    # Replay uses the isolated partner trajectory, preserving a time-varying
    # signal without allowing reciprocal causal influence.
    replay_a, replay_b = np.zeros_like(a), np.zeros_like(b)
    for t in range(cfg.steps - 1):
        replay_a[t + 1] = cfg.a * replay_a[t] + cfg.input_gain * u[t]
        replay_b[t + 1] = cfg.a * replay_b[t] + cfg.input_gain * u[t]

    for t in range(cfg.steps - 1):
        partner_a = replay_b[t] if replay else b[t]
        partner_b = replay_a[t] if replay else a[t]
        a[t + 1] = cfg.a * a[t] + cfg.input_gain * u[t] + coupling * partner_a
        b[t + 1] = cfg.a * b[t] + cfg.input_gain * u[t] + coupling * partner_b

    return a, b, u


def r2(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot else 0.0


def fit_r2(y: np.ndarray, X: np.ndarray) -> float:
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return r2(y, X @ beta)


def metrics(a: np.ndarray, b: np.ndarray, u: np.ndarray) -> dict:
    sl = slice(1, None)
    base_a = np.column_stack([np.ones(len(a[sl])), a[:-1], u[:-1]])
    partner_a = np.column_stack([base_a, b[:-1]])

    base_b = np.column_stack([np.ones(len(b[sl])), b[:-1], u[:-1]])
    partner_b = np.column_stack([base_b, a[:-1]])

    r2_a_base = fit_r2(a[sl], base_a)
    r2_a_partner = fit_r2(a[sl], partner_a)
    r2_b_base = fit_r2(b[sl], base_b)
    r2_b_partner = fit_r2(b[sl], partner_b)

    return {
        "a_partner_incremental_r2": r2_a_partner - r2_a_base,
        "b_partner_incremental_r2": r2_b_partner - r2_b_base,
        "a_base_r2": r2_a_base,
        "b_base_r2": r2_b_base,
        "coupling_correlation": float(np.corrcoef(a[1:], b[1:])[0, 1]),
    }


def run() -> dict:
    cfg = Config()

    isolated = simulate(cfg, coupling=0.0)
    coupled = simulate(cfg, coupling=cfg.coupling)
    sham = simulate(cfg, coupling=cfg.coupling, replay=True)

    return {
        "assay": "relational-coupling-probe",
        "configuration": cfg.__dict__,
        "isolated": metrics(*isolated),
        "coupled": metrics(*coupled),
        "sham_replay": metrics(*sham),
        "interpretation": (
            "Positive incremental partner R2 in the coupled condition, relative "
            "to isolated and sham-replay controls, is evidence of relational "
            "predictive structure. It is not evidence of shared phenomenal consciousness."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
