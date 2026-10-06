#!/usr/bin/env python3
"""S01 reproducible computational study."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import requests

REPO = "chrishotza/Skill-Conscious"
BRANCH = "corpus-v1"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

EXPECTED = {
    "corpus/CLAIMS/claim_ledger_v1.json": "86a9a310c30f2937a206f09bd8d65e7d3097d90b",
    "corpus/CLAIMS/claim_ledger_v1_append_v24.json": "95af02d2af246a97d29dcc1b1266d28dbbaa6551",
    "corpus/CLAIMS/claim_ledger_v1_append_v25.json": "334dd00f724da4c8249e25895326e6892072f37c",
    "corpus/CLAIMS/claim_ledger_v1_append_v26.json": "7b1ac7528eb421a52d18a9fd615711381d624745",
    "corpus/CLAIMS/claim_ledger_v1_append_v27.json": "70b1f767c532acafaa761dda5a4e2d42df7e8228",
    "corpus/CLAIMS/claim_ledger_v1_append_v28.json": "6c96ac9c2aa041c7dcd8c6d76637d2e0730ae7ba",
    "corpus/CLAIMS/claim_ledger_v1_append_v29.json": "c5519ea542667dda6280e9c72116f7963ef6c20b",
    "corpus/CLAIMS/claim_ledger_v1_append_v30.json": "57fa05224c9e0c99157dd30a7ab98e222cc042c4",
    "corpus/CLAIMS/claim_ledger_v1_append_v31.json": "bda1909c0898713ae81497a63c84b0c753f5180a",
    "corpus/CLAIMS/claim_ledger_v1_append_v32.json": "06adec55d4ae1ea3c0b1b0d40ed06c4ff832af2c",
    "corpus/CLAIMS/claim_ledger_v1_append_v33.json": "7dca934f5ace9d0bbcc5c8e9ace7374c96bc4695",
    "corpus/CLAIMS/claim_ledger_v1_append_v34.json": "65ac747328c4e2345202190987cedb178ca4672c",
    "corpus/CLAIMS/claim_ledger_v1_append_v35.json": "3aa539f92efa7fb2526e4a2742105ad569281c9b",
    "corpus/CLAIMS/claim_ledger_v1_append_v36.json": "0e4805e1172afe2cc890209371ffadf822a25f5b",
    "corpus/CLAIMS/claim_ledger_v1_append_v37.json": "46acc9f2a0aaef9e86ffab3e519c330c4a7d7cf2",
}

SOURCE_REGISTER_PATH = "corpus/SOURCE_REGISTER_V1.md"
SOURCE_REGISTER_SHA = "a4184dc5c40dd9d3580ebf9cfd4302ac64686a8d"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
MODEL_REVISION = "ef15aed8b328d308d7237b9bf15269f2cd19e268"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def fetch_verified(relpath: str, expected_sha: str, cache: Path) -> bytes:
    url = f"{RAW_BASE}/{relpath}"
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    data = response.content
    actual = git_blob_sha(data)
    if actual != expected_sha:
        raise RuntimeError(
            f"Git blob mismatch for {relpath}: expected {expected_sha}, got {actual}"
        )
    target = cache / Path(relpath).name
    target.write_bytes(data)
    return data


def parse_source_families(text: str) -> dict[str, str]:
    families: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("| C"):
            continue
        parts = line.split("|")
        if len(parts) < 4:
            continue
        cid = parts[1].strip()
        descriptor = parts[2].strip()
        if cid.startswith("C") and "—" in descriptor and ";" in descriptor:
            families[cid] = descriptor.split("—", 1)[1].split(";", 1)[0].strip()
    if len(families) != 325:
        raise RuntimeError(f"Expected 325 source families, got {len(families)}")
    return families


def load_claims(cache: Path) -> list[dict]:
    records: list[dict] = []
    for relpath, sha in EXPECTED.items():
        data = fetch_verified(relpath, sha, cache)
        records.extend(json.loads(data.decode("utf-8"))["records"])
    if len(records) != 4315:
        raise RuntimeError(f"Expected 4315 claims, got {len(records)}")
    if len({r["global_claim_id"] for r in records}) != 4315:
        raise RuntimeError("Global claim IDs are not unique")
    return records


def collapse_units(records: list[dict], families: dict[str, str]) -> dict[str, dict]:
    units: dict[str, dict] = {}
    for r in records:
        cid = r["corpus_id"]
        units.setdefault(
            cid,
            {
                "family": families[cid],
                "motifs": set(),
            },
        )
        units[cid]["motifs"].update(r.get("motifs") or [])
    if len(units) != 325:
        raise RuntimeError(f"Expected 325 corpus units, got {len(units)}")
    return units


def jaccard(a: set[str], b: set[str]) -> float:
    union = len(a | b)
    return 0.0 if union == 0 else len(a & b) / union


def pair_jaccard_matrix(units: dict[str, dict], ids: list[str]) -> np.ndarray:
    n = len(ids)
    out = np.zeros((n, n), dtype=np.float32)
    sets = [units[c]["motifs"] for c in ids]
    for i in range(n):
        for j in range(i + 1, n):
            v = jaccard(sets[i], sets[j])
            out[i, j] = v
            out[j, i] = v
    return out


def observed_delta(sim: np.ndarray, ids: list[str], labels: np.ndarray) -> dict:
    ii, jj = np.triu_indices(len(ids), 1)
    vals = sim[ii, jj]
    same = labels[ii] == labels[jj]
    cross = vals[~same]
    within = vals[same]
    delta = float(cross.mean() - within.mean())
    return {
        "cross_mean": float(cross.mean()),
        "within_mean": float(within.mean()),
        "delta_cross_minus_within": delta,
        "cross_pairs": int(cross.size),
        "within_pairs": int(within.size),
    }


def label_permutation_null(sim: np.ndarray, labels: np.ndarray, reps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    ii, jj = np.triu_indices(len(labels), 1)
    vals = sim[ii, jj]
    out = np.empty(reps, dtype=np.float64)
    for r in range(reps):
        p = rng.permutation(labels)
        same = p[ii] == p[jj]
        out[r] = vals[~same].mean() - vals[same].mean()
    return out


def normalized_entropy(counts: np.ndarray) -> float:
    total = counts.sum()
    if total == 0:
        return 0.0
    p = counts[counts > 0] / total
    return float(-(p * np.log(p)).sum() / np.log(len(counts)))


def motif_profile(
    units: dict[str, dict],
    ids: list[str],
    labels: np.ndarray,
    reps: int,
    seed: int,
) -> list[dict]:
    rng = np.random.default_rng(seed)
    families = sorted(set(labels.tolist()))
    label_masks = {f: labels == f for f in families}
    motifs = sorted({m for cid in ids for m in units[cid]["motifs"]})
    rows = []
    for motif in motifs:
        incidence = np.array([motif in units[cid]["motifs"] for cid in ids], dtype=np.int8)
        counts = np.array([incidence[mask].sum() for mask in label_masks.values()], dtype=np.float64)
        ent = normalized_entropy(counts)
        null = np.empty(reps, dtype=np.float64)
        for r in range(reps):
            perm = rng.permutation(incidence)
            pc = np.array([perm[mask].sum() for mask in label_masks.values()], dtype=np.float64)
            null[r] = normalized_entropy(pc)
        rows.append(
            {
                "motif": motif,
                "support_units": int(incidence.sum()),
                "families_present": int((counts > 0).sum()),
                "normalized_entropy": ent,
                "null_entropy_mean": float(null.mean()),
                "null_entropy_ci_low": float(np.quantile(null, 0.025)),
                "null_entropy_ci_high": float(np.quantile(null, 0.975)),
                "p_null_entropy_ge": float((np.sum(null >= ent) + 1) / (len(null) + 1)),
            }
        )
    return rows


def degree_preserving_null(
    units: dict[str, dict],
    ids: list[str],
    labels: np.ndarray,
    reps: int,
    swaps_factor: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    motifs = sorted({m for cid in ids for m in units[cid]["motifs"]})
    mindex = {m: i for i, m in enumerate(motifs)}
    base = np.zeros((len(ids), len(motifs)), dtype=np.int8)
    for i, cid in enumerate(ids):
        for m in units[cid]["motifs"]:
            base[i, mindex[m]] = 1

    edges0 = [tuple(x) for x in np.argwhere(base == 1)]
    if not edges0:
        return np.zeros(reps, dtype=float)

    ii, jj = np.triu_indices(len(ids), 1)
    same = labels[ii] == labels[jj]
    deltas = np.empty(reps, dtype=float)

    for r in range(reps):
        mat = base.copy()
        edges = list(edges0)
        edge_set = set(edges)
        swaps = swaps_factor * len(edges)

        for _ in range(swaps):
            p = int(rng.integers(len(edges)))
            q = int(rng.integers(len(edges)))
            if p == q:
                continue

            i, a = edges[p]
            j, b = edges[q]
            if i == j or a == b:
                continue

            e_new_1 = (i, b)
            e_new_2 = (j, a)
            if e_new_1 in edge_set or e_new_2 in edge_set:
                continue

            e_old_1 = edges[p]
            e_old_2 = edges[q]
            edge_set.remove(e_old_1)
            edge_set.remove(e_old_2)
            edge_set.add(e_new_1)
            edge_set.add(e_new_2)

            edges[p] = e_new_1
            edges[q] = e_new_2

            mat[i, a] = 0
            mat[j, b] = 0
            mat[i, b] = 1
            mat[j, a] = 1

        sim = np.zeros(ii.size, dtype=np.float32)
        for k, (i, j) in enumerate(zip(ii, jj)):
            a = mat[i].astype(bool)
            b = mat[j].astype(bool)
            u = np.logical_or(a, b).sum()
            sim[k] = 0.0 if u == 0 else np.logical_and(a, b).sum() / u

        deltas[r] = sim[~same].mean() - sim[same].mean()

    return deltas


def semantic_analysis(records, units, args, output_dir: Path) -> dict:
    import torch
    from sentence_transformers import SentenceTransformer
    from sklearn.neighbors import NearestNeighbors

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if args.require_gpu and device != "cuda":
        raise RuntimeError("Confirmatory run requires CUDA/GPU.")

    model = SentenceTransformer(
        MODEL_NAME,
        revision=MODEL_REVISION,
        device=device,
    )
    texts = [r["claim"] for r in records]
    embeddings = model.encode(
        texts,
        batch_size=args.embedding_batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype(np.float32)

    unit_ids = sorted(units)
    unit_index = {cid: i for i, cid in enumerate(unit_ids)}
    unit_family = {cid: units[cid]["family"] for cid in unit_ids}
    claim_units = [r["corpus_id"] for r in records]

    candidate_pool = min(args.semantic_candidate_pool, len(records))
    nn = NearestNeighbors(n_neighbors=candidate_pool, metric="cosine", algorithm="brute")
    nn.fit(embeddings)
    distances, indices = nn.kneighbors(embeddings)

    neighbors = np.empty((len(records), args.semantic_k), dtype=np.int32)
    similarities = np.empty((len(records), args.semantic_k), dtype=np.float32)

    for q in range(len(records)):
        chosen = []
        sims = []
        for dist, idx in zip(distances[q], indices[q]):
            if idx == q:
                continue
            if claim_units[idx] == claim_units[q]:
                continue
            chosen.append(idx)
            sims.append(1.0 - float(dist))
            if len(chosen) == args.semantic_k:
                break
        if len(chosen) != args.semantic_k:
            raise RuntimeError(f"Could not find {args.semantic_k} eligible neighbors for claim {q}")
        neighbors[q] = np.array(chosen, dtype=np.int32)
        similarities[q] = np.array(sims, dtype=np.float32)

    claim_unit_index = np.array([unit_index[cid] for cid in claim_units], dtype=np.int32)
    unit_labels = np.array([unit_family[cid] for cid in unit_ids], dtype=object)

    observed_fraction = []
    observed_cross_cos = []
    for q in range(len(records)):
        qfam = unit_labels[claim_unit_index[q]]
        nlabels = unit_labels[claim_unit_index[neighbors[q]]]
        mask = nlabels != qfam
        observed_fraction.append(float(mask.mean()))
        if mask.any():
            observed_cross_cos.append(float(similarities[q, mask].mean()))

    observed_fraction_mean = float(np.mean(observed_fraction))
    observed_cross_cos_mean = float(np.mean(observed_cross_cos))

    rng = np.random.default_rng(args.seed + 100)
    null_fraction = np.empty(args.semantic_null_reps, dtype=np.float64)
    null_cross_cos = np.empty(args.semantic_null_reps, dtype=np.float64)

    for r in range(args.semantic_null_reps):
        perm_labels = rng.permutation(unit_labels)
        qlabels = perm_labels[claim_unit_index]
        nlabels = perm_labels[claim_unit_index[neighbors]]
        mask = nlabels != qlabels[:, None]
        null_fraction[r] = float(mask.mean(axis=1).mean())
        valid = mask.any(axis=1)
        per_claim = np.sum(similarities * mask, axis=1) / np.maximum(mask.sum(axis=1), 1)
        null_cross_cos[r] = float(per_claim[valid].mean())

    summary = {
        "device": device,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "k": args.semantic_k,
        "candidate_pool": candidate_pool,
        "observed_cross_neighbor_fraction": observed_fraction_mean,
        "null_cross_neighbor_fraction_mean": float(null_fraction.mean()),
        "null_cross_neighbor_fraction_ci": [
            float(np.quantile(null_fraction, 0.025)),
            float(np.quantile(null_fraction, 0.975)),
        ],
        "p_fraction_ge_observed": float(
            (np.sum(null_fraction >= observed_fraction_mean) + 1)
            / (len(null_fraction) + 1)
        ),
        "observed_cross_neighbor_mean_cosine": observed_cross_cos_mean,
        "null_cross_neighbor_mean_cosine_mean": float(null_cross_cos.mean()),
        "null_cross_neighbor_mean_cosine_ci": [
            float(np.quantile(null_cross_cos, 0.025)),
            float(np.quantile(null_cross_cos, 0.975)),
        ],
        "p_cosine_ge_observed": float(
            (np.sum(null_cross_cos >= observed_cross_cos_mean) + 1)
            / (len(null_cross_cos) + 1)
        ),
    }

    (output_dir / "semantic_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    np.savez_compressed(
        output_dir / "semantic_neighbors.npz",
        indices=neighbors,
        similarities=similarities,
    )
    return summary


def runtime_manifest(args) -> dict:
    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        git_sha = os.environ.get("GIT_COMMIT", "unknown")

    try:
        import importlib.metadata as metadata

        package_names = [
            "numpy",
            "requests",
            "scikit-learn",
            "sentence-transformers",
            "torch",
            "transformers",
        ]
        packages = {}
        for name in package_names:
            try:
                packages[name] = metadata.version(name)
            except metadata.PackageNotFoundError:
                packages[name] = None
    except Exception:
        packages = {}

    gpu = None
    cuda = None
    try:
        import torch

        cuda = torch.version.cuda
        if torch.cuda.is_available():
            gpu = torch.cuda.get_device_name(0)
    except Exception:
        pass

    return {
        "git_commit": git_sha,
        "python": sys.version,
        "platform": platform.platform(),
        "cuda": cuda,
        "gpu": gpu,
        "packages": packages,
        "seed": args.seed,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "config": vars(args),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", required=True)
    parser.add_argument("--output_root", default="results/s01")
    parser.add_argument("--seed", type=int, default=20261006)
    parser.add_argument("--coded_null_reps", type=int, default=5000)
    parser.add_argument("--rewire_null_reps", type=int, default=1000)
    parser.add_argument("--semantic_null_reps", type=int, default=5000)
    parser.add_argument("--rewire_factor", type=int, default=5)
    parser.add_argument("--motif_entropy_reps", type=int, default=2000)
    parser.add_argument("--semantic_k", type=int, default=10)
    parser.add_argument("--semantic_candidate_pool", type=int, default=100)
    parser.add_argument("--embedding_batch_size", type=int, default=64)
    parser.add_argument("--require_gpu", action="store_true")
    parser.add_argument("--skip_semantic", action="store_true")
    parser.add_argument("--skip_rewire", action="store_true")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    output_dir = Path(args.output_root) / args.run_id
    output_dir.mkdir(parents=True, exist_ok=False)
    cache = output_dir / "data_cache"
    cache.mkdir()

    source_register = fetch_verified(
        SOURCE_REGISTER_PATH, SOURCE_REGISTER_SHA, cache
    ).decode("utf-8")
    families = parse_source_families(source_register)
    records = load_claims(cache)
    units = collapse_units(records, families)
    ids = sorted(units)

    (output_dir / "run_manifest.json").write_text(
        json.dumps(runtime_manifest(args), indent=2), encoding="utf-8"
    )

    matrix = pair_jaccard_matrix(units, ids)
    labels = np.array([units[c]["family"] for c in ids], dtype=object)

    observed = observed_delta(matrix, ids, labels)
    null = label_permutation_null(
        matrix, labels, args.coded_null_reps, args.seed + 1
    )
    coded_summary = {
        **observed,
        "label_null_mean": float(null.mean()),
        "label_null_ci": [
            float(np.quantile(null, 0.025)),
            float(np.quantile(null, 0.975)),
        ],
        "p_delta_ge_observed": float(
            (np.sum(null >= observed["delta_cross_minus_within"]) + 1)
            / (len(null) + 1)
        ),
    }
    (output_dir / "coded_summary.json").write_text(
        json.dumps(coded_summary, indent=2), encoding="utf-8"
    )

    profile = motif_profile(
        units,
        ids,
        labels,
        args.motif_entropy_reps,
        args.seed + 2,
    )
    (output_dir / "motif_profile.json").write_text(
        json.dumps(profile, indent=2), encoding="utf-8"
    )

    if not args.skip_rewire:
        rewire = degree_preserving_null(
            units,
            ids,
            labels,
            args.rewire_null_reps,
            args.rewire_factor,
            args.seed + 3,
        )
        rewire_summary = {
            "mean": float(rewire.mean()),
            "ci": [
                float(np.quantile(rewire, 0.025)),
                float(np.quantile(rewire, 0.975)),
            ],
            "p_delta_ge_observed": float(
                (np.sum(rewire >= observed["delta_cross_minus_within"]) + 1)
                / (len(rewire) + 1)
            ),
        }
        (output_dir / "rewire_null_summary.json").write_text(
            json.dumps(rewire_summary, indent=2), encoding="utf-8"
        )

    semantic = None
    if not args.skip_semantic:
        semantic = semantic_analysis(records, units, args, output_dir)

    final = {
        "study_id": "S01",
        "run_id": args.run_id,
        "status": "complete",
        "claims": len(records),
        "corpus_units": len(units),
        "source_ids": len({r["source_id"] for r in records}),
        "source_families": len(set(families.values())),
        "coded": coded_summary,
        "semantic": semantic,
    }
    (output_dir / "final_summary.json").write_text(
        json.dumps(final, indent=2), encoding="utf-8"
    )
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
