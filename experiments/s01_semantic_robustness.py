#!/usr/bin/env python3
"""S01 pre-specified semantic robustness analyses.

Implements the semantic sensitivity analyses frozen in:
research/S01_PREREGISTRATION_V1.md

This script must be frozen before confirmatory results are inspected.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from s01_cross_cultural_recurrence import (
    EXPECTED,
    MODEL_NAME,
    MODEL_REVISION,
    RAW_BASE,
    SOURCE_REGISTER_PATH,
    SOURCE_REGISTER_SHA,
    collapse_units,
    fetch_verified,
    load_claims,
    parse_source_families,
)


def condition_specs(families: list[str]) -> list[dict]:
    specs = [
        {"id": "SEM_K5", "kind": "semantic", "k": 5},
        {
            "id": "EXCLUDE_HETERODOXO_EXTENDIDO",
            "kind": "exclude_family",
            "exclude_families": ["Heterodoxo/extendido"],
        },
        {
            "id": "EXCLUDE_CIENCIA_IA_SUPLEMENTARIO",
            "kind": "exclude_family",
            "exclude_families": ["Ciencia/IA", "Suplementario"],
        },
        {
            "id": "P1_P2_S1_ONLY",
            "kind": "provenance",
            "provenance_prefixes": ["P1", "P2", "S1"],
        },
    ]
    specs.extend(
        {
            "id": f"LEAVE_OUT_{family.replace('/', '_').replace(' ', '_')}",
            "kind": "exclude_family",
            "exclude_families": [family],
        }
        for family in families
    )
    return specs


def build_units(records: list[dict], families: dict[str, str]) -> dict[str, dict]:
    units = collapse_units(records, families)
    return units


def filter_condition(
    records: list[dict],
    units: dict[str, dict],
    spec: dict,
) -> tuple[list[dict], dict[str, dict]]:
    keep_ids = set(units)

    if spec["kind"] == "exclude_family":
        excluded = set(spec["exclude_families"])
        keep_ids = {
            cid for cid in keep_ids if units[cid]["family"] not in excluded
        }
        filtered_records = [r for r in records if r["corpus_id"] in keep_ids]
    elif spec["kind"] == "provenance":
        prefixes = tuple(spec["provenance_prefixes"])
        filtered_records = [
            r
            for r in records
            if r["corpus_id"] in keep_ids
            and str(r.get("provenance", "")).startswith(prefixes)
        ]
    else:
        filtered_records = [r for r in records if r["corpus_id"] in keep_ids]

    filtered_units = {}
    for r in filtered_records:
        cid = r["corpus_id"]
        if cid not in filtered_units:
            filtered_units[cid] = {
                "family": units[cid]["family"],
                "motifs": set(),
            }
        filtered_units[cid]["motifs"].update(r.get("motifs") or [])

    return filtered_records, filtered_units


def semantic_condition(
    records: list[dict],
    units: dict[str, dict],
    embeddings: np.ndarray,
    k: int,
    null_reps: int,
    candidate_pool: int,
    seed: int,
) -> dict:
    from sklearn.neighbors import NearestNeighbors

    if not records:
        raise RuntimeError("No records remain after filtering.")

    unit_ids = sorted(units)
    if len(unit_ids) < 2:
        raise RuntimeError("At least two corpus units are required.")

    unit_index = {cid: i for i, cid in enumerate(unit_ids)}
    labels = np.array([units[cid]["family"] for cid in unit_ids], dtype=object)

    record_ids = [r["global_claim_id"] for r in records]
    original_index = {gid: i for i, gid in enumerate(record_ids)}

    candidate_pool = min(candidate_pool, len(records))
    nn = NearestNeighbors(
        n_neighbors=candidate_pool,
        metric="cosine",
        algorithm="brute",
    )
    nn.fit(embeddings)

    distances, indices = nn.kneighbors(embeddings)

    neighbor_similarities: list[list[float]] = []
    neighbor_units: list[list[int]] = []

    claim_units = np.array([r["corpus_id"] for r in records], dtype=object)

    for q in range(len(records)):
        chosen: list[int] = []
        sims: list[float] = []
        for dist, idx in zip(distances[q], indices[q]):
            if idx == q:
                continue
            if claim_units[idx] == claim_units[q]:
                continue
            chosen.append(int(idx))
            sims.append(1.0 - float(dist))
            if len(chosen) == k:
                break
        if len(chosen) != k:
            raise RuntimeError(
                f"Could not find {k} eligible neighbors for claim index {q}."
            )
        neighbor_units.append(
            [unit_index[str(claim_units[idx])] for idx in chosen]
        )
        neighbor_similarities.append(sims)

    claim_unit_index = np.array(
        [unit_index[str(cid)] for cid in claim_units],
        dtype=np.int32,
    )

    observed_cross_fraction = []
    observed_cross_cosine = []

    for q in range(len(records)):
        q_label = labels[claim_unit_index[q]]
        neighbor_label = labels[np.array(neighbor_units[q])]
        sims = np.array(neighbor_similarities[q], dtype=np.float32)
        cross = neighbor_label != q_label
        observed_cross_fraction.append(float(cross.mean()))
        if cross.any():
            observed_cross_cosine.append(float(sims[cross].mean()))

    observed_fraction = float(np.mean(observed_cross_fraction))
    observed_cosine = float(np.mean(observed_cross_cosine))

    rng = np.random.default_rng(seed)
    null_fraction = np.empty(null_reps, dtype=np.float64)
    null_cosine = np.empty(null_reps, dtype=np.float64)

    for rep in range(null_reps):
        permuted = rng.permutation(labels)

        per_claim_fraction = []
        per_claim_cosine = []

        for q in range(len(records)):
            q_label = permuted[claim_unit_index[q]]
            nlabels = permuted[np.array(neighbor_units[q])]
            sims = np.array(neighbor_similarities[q], dtype=np.float32)
            cross = nlabels != q_label

            per_claim_fraction.append(float(cross.mean()))
            if cross.any():
                per_claim_cosine.append(float(sims[cross].mean()))

        null_fraction[rep] = float(np.mean(per_claim_fraction))
        null_cosine[rep] = float(np.mean(per_claim_cosine))

    return {
        "claims": len(records),
        "corpus_units": len(units),
        "source_families": len(set(labels.tolist())),
        "k": k,
        "candidate_pool": candidate_pool,
        "observed_cross_neighbor_fraction": observed_fraction,
        "null_cross_neighbor_fraction_mean": float(null_fraction.mean()),
        "null_cross_neighbor_fraction_ci": [
            float(np.quantile(null_fraction, 0.025)),
            float(np.quantile(null_fraction, 0.975)),
        ],
        "p_fraction_ge_observed": float(
            (np.sum(null_fraction >= observed_fraction) + 1)
            / (len(null_fraction) + 1)
        ),
        "observed_cross_neighbor_mean_cosine": observed_cosine,
        "null_cross_neighbor_mean_cosine_mean": float(null_cosine.mean()),
        "null_cross_neighbor_mean_cosine_ci": [
            float(np.quantile(null_cosine, 0.025)),
            float(np.quantile(null_cosine, 0.975)),
        ],
        "delta_s": float(observed_cosine - null_cosine.mean()),
        "p_cosine_ge_observed": float(
            (np.sum(null_cosine >= observed_cosine) + 1)
            / (len(null_cosine) + 1)
        ),
    }


def load_model(device: str):
    import torch
    from sentence_transformers import SentenceTransformer

    return torch, SentenceTransformer(
        MODEL_NAME,
        revision=MODEL_REVISION,
        device=device,
    )


def encode_claims(model, records: list[dict], batch_size: int) -> np.ndarray:
    texts = [r["claim"] for r in records]
    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).astype(np.float32)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", required=True)
    parser.add_argument("--output_root", default="results/s01")
    parser.add_argument("--seed", type=int, default=20261006)
    parser.add_argument("--semantic_null_reps", type=int, default=5000)
    parser.add_argument("--semantic_k", type=int, default=10)
    parser.add_argument("--semantic_candidate_pool", type=int, default=100)
    parser.add_argument("--embedding_batch_size", type=int, default=64)
    parser.add_argument("--device", choices=["cuda", "cpu"], default="cuda")
    parser.add_argument(
        "--cpu_gpu_repro",
        action="store_true",
        help="Run the primary semantic analysis once on CPU after the requested device.",
    )
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)

    output_dir = Path(args.output_root) / args.run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    cache = output_dir / "data_cache"
    cache.mkdir()

    source_register = fetch_verified(
        SOURCE_REGISTER_PATH,
        SOURCE_REGISTER_SHA,
        cache,
    ).decode("utf-8")

    families = parse_source_families(source_register)
    records = load_claims(cache)
    units = build_units(records, families)

    import torch

    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but not available.")

    model = None
    embeddings = None

    def ensure_embeddings(device: str):
        nonlocal model, embeddings
        model = None
        model = load_model(device)[1]
        embeddings = encode_claims(
            model,
            records,
            args.embedding_batch_size,
        )
        return model, embeddings

    ensure_embeddings(args.device)

    specs = condition_specs(sorted(set(families.values())))
    results = {}

    for index, spec in enumerate(specs, start=1):
        filtered_records, filtered_units = filter_condition(
            records,
            units,
            spec,
        )
        source_indices = np.array(
            [next(i for i, r in enumerate(records) if r["global_claim_id"] == fr["global_claim_id"])
             for fr in filtered_records],
            dtype=np.int32,
        )
        condition_embeddings = embeddings[source_indices]

        k = int(spec.get("k", args.semantic_k))
        condition_seed = args.seed + 1000 + index

        results[spec["id"]] = {
            "spec": spec,
            "result": semantic_condition(
                filtered_records,
                filtered_units,
                condition_embeddings,
                k=k,
                null_reps=args.semantic_null_reps,
                candidate_pool=args.semantic_candidate_pool,
                seed=condition_seed,
            ),
            "seed": condition_seed,
        }

    cpu_gpu = None
    if args.cpu_gpu_repro:
        gpu_result = semantic_condition(
            records,
            units,
            embeddings,
            k=args.semantic_k,
            null_reps=args.semantic_null_reps,
            candidate_pool=args.semantic_candidate_pool,
            seed=args.seed + 9000,
        )

        cpu_torch, cpu_model = load_model("cpu")
        cpu_embeddings = encode_claims(
            cpu_model,
            records,
            args.embedding_batch_size,
        )
        cpu_result = semantic_condition(
            records,
            units,
            cpu_embeddings,
            k=args.semantic_k,
            null_reps=args.semantic_null_reps,
            candidate_pool=args.semantic_candidate_pool,
            seed=args.seed + 9000,
        )

        cpu_gpu = {
            "gpu": gpu_result,
            "cpu": cpu_result,
            "absolute_difference_observed_cross_neighbor_mean_cosine": abs(
                gpu_result["observed_cross_neighbor_mean_cosine"]
                - cpu_result["observed_cross_neighbor_mean_cosine"]
            ),
            "absolute_difference_delta_s": abs(
                gpu_result["delta_s"] - cpu_result["delta_s"]
            ),
            "cpu_python": sys.version,
            "cpu_torch_cuda_version": cpu_torch.version.cuda,
        }

    run_manifest = {
        "study_id": "S01",
        "analysis": "pre-specified semantic robustness",
        "run_id": args.run_id,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": MODEL_NAME,
        "model_revision": MODEL_REVISION,
        "requested_device": args.device,
        "gpu": (
            torch.cuda.get_device_name(0)
            if torch.cuda.is_available()
            else None
        ),
        "cuda": torch.version.cuda,
        "python": sys.version,
        "seed": args.seed,
        "semantic_null_reps": args.semantic_null_reps,
        "semantic_k": args.semantic_k,
        "semantic_candidate_pool": args.semantic_candidate_pool,
        "embedding_batch_size": args.embedding_batch_size,
        "corpus_units": len(units),
        "claims": len(records),
        "source_ids": len({r["source_id"] for r in records}),
        "source_families": len(set(families.values())),
    }

    (output_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2),
        encoding="utf-8",
    )
    (output_dir / "semantic_robustness.json").write_text(
        json.dumps(results, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    if cpu_gpu is not None:
        (output_dir / "cpu_gpu_reproducibility.json").write_text(
            json.dumps(cpu_gpu, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    final = {
        "study_id": "S01",
        "status": "complete",
        "analysis": "pre-specified semantic robustness",
        "conditions": results,
        "cpu_gpu_reproducibility": cpu_gpu,
    }
    (output_dir / "final_summary.json").write_text(
        json.dumps(final, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(json.dumps(final, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
