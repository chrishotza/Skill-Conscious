"""Controlled relational-coupling assay.

Uses independent deterministic disturbances and a fixed permutation replay control.
"""
import json
import numpy as np

N = 1200
DECAY = 0.78
COMMON_GAIN = 0.20
PRIVATE_GAIN = 0.15
COUPLING = 0.18
SEED = 7

def drive(t):
    return 0.6*np.sin(t/19.0) + 0.25*np.sin(t/7.0)

def simulate(coupling, replay=False):
    rng = np.random.default_rng(SEED)
    common = np.array([drive(t) for t in range(N)])
    da, db = rng.normal(size=N), rng.normal(size=N)
    perm = rng.permutation(N)
    a = np.zeros(N); b = np.zeros(N)
    ra = np.zeros(N); rb = np.zeros(N)
    for t in range(N-1):
        ra[t+1] = DECAY*ra[t] + COMMON_GAIN*common[t] + PRIVATE_GAIN*da[t]
        rb[t+1] = DECAY*rb[t] + COMMON_GAIN*common[t] + PRIVATE_GAIN*db[t]
    for t in range(N-1):
        pa = rb[perm[t]] if replay else b[t]
        pb = ra[perm[t]] if replay else a[t]
        a[t+1] = DECAY*a[t] + COMMON_GAIN*common[t] + PRIVATE_GAIN*da[t] + coupling*pa
        b[t+1] = DECAY*b[t] + COMMON_GAIN*common[t] + PRIVATE_GAIN*db[t] + coupling*pb
    return a, b, common

def r2(y, pred):
    den = np.sum((y-y.mean())**2)
    return 1.0 - np.sum((y-pred)**2)/den if den else 0.0

def fit(y, X):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return r2(y, X@beta)

def metrics(a, b, common):
    xa = np.c_[np.ones(N-1), a[:-1], common[:-1]]
    xb = np.c_[np.ones(N-1), b[:-1], common[:-1]]
    return {
        "a_partner_incremental_r2": fit(a[1:], np.c_[xa, b[:-1]]) - fit(a[1:], xa),
        "b_partner_incremental_r2": fit(b[1:], np.c_[xb, a[:-1]]) - fit(b[1:], xb),
    }

def run():
    return {
        "assay": "relational-coupling-probe-v3",
        "isolated": metrics(*simulate(0.0)),
        "coupled": metrics(*simulate(COUPLING)),
        "permuted_replay_control": metrics(*simulate(COUPLING, replay=True)),
        "note": "Relational predictive structure test; not a phenomenal-consciousness test.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
