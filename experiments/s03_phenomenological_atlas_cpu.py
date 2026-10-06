#!/usr/bin/env python3
"""
S03 — PHENOMENOLOGICAL ATLAS + LEAVE-ONE-FAMILY-OUT TRANSFER
Exploratory CPU-only discovery layer.

Purpose
-------
Move from "there is cross-corpus structure" to "what semantic/phenomenological
components are actually recurring?"

This run is explicitly exploratory. It does NOT test a preregistered
hypothesis and it must not be reported as confirmatory evidence.

Inputs
------
- Frozen S01 semantic_neighbors.npz from:
  results/s01/S01_CONFIRMATORY_T4_V1/
- Frozen claim ledgers from GitHub branch corpus-v1, verified by Git blob SHA.

No embeddings are regenerated. No T4/GPU is used.

Main outputs
------------
- cluster_assignments.csv
- cluster_summary.csv
- cluster_motifs.csv
- cluster_representatives.csv
- bridge_claims.csv
- lofo_transfer.csv
- lofo_fold_summary.csv
- schema_audit.json
- S03_PHENOMENOLOGICAL_ATLAS_RESULTS_V1.json
- run_manifest.json

Method
------
1. Reconstruct the exact 4,315-claim semantic graph from S01's frozen top-10
   semantic neighbors.
2. Build a weighted undirected kNN graph.
3. Discover graph communities with deterministic Louvain (resolution=1.0).
4. Rank communities by family coverage / entropy and surface representative
   claim text + motifs.
5. Repeat the community discovery 19 times, each time removing one family.
6. For the held-out family, map each claim into communities learned from the
   remaining 18 families using only its frozen semantic-neighbor edges.
7. Report transfer strength and whether the receiving community contains
   multiple families.

Interpretation guardrails
------------------------
- A community is not automatically a "consciousness phenomenon".
- Cross-family presence is not proof of independent discovery.
- LOFO transfer is a structural transfer metric, not causal evidence.
- If no explicit phenomenological metadata field is found, the atlas is run
  on all claims and clearly marked as an all-claim semantic atlas.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import math
import os
import platform
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

REPO = "chrishotza/Skill-Conscious"
BRANCH = "corpus-v1"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

EXPECTED_CLAIMS = {
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

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
MODEL_REVISION = "ef15aed8b328d308d7237b9bf15269f2cd19e268"
SOURCE_REGISTER_PATH = "corpus/SOURCE_REGISTER_V1.md"
SOURCE_REGISTER_SHA = "a4184dc5c40dd9d3580ebf9cfd4302ac64686a8d"

SEED = 20261006
LOUVAIN_RESOLUTION = 1.0
TOP_REPRESENTATIVES = 7
TOP_MOTIFS = 12


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ensure_package(name: str, import_name: str | None = None, min_version: str | None = None):
    module = import_name or name
    try:
        return importlib.import_module(module)
    except ImportError:
        spec = f"{name}>={min_version}" if min_version else name
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", spec])
        return importlib.import_module(module)


def locate_semantic_neighbors() -> Path:
    root = Path("/content/drive/MyDrive/Skill-Conscious")
    exact = root / "results/s01/S01_CONFIRMATORY_T4_V1/semantic_neighbors.npz"
    if exact.exists():
        return exact

    matches = sorted(root.glob("results/s01/**/semantic_neighbors.npz"))
    if not matches:
        raise FileNotFoundError(
            "semantic_neighbors.npz not found under /content/drive/MyDrive/Skill-Conscious/results/s01"
        )
    if len(matches) > 1:
        preferred = [p for p in matches if "S01_CONFIRMATORY_T4_V1" in str(p)]
        if len(preferred) == 1:
            return preferred[0]
    return matches[0]


def fetch_verified(relpath: str, expected_sha: str, cache_dir: Path) -> bytes:
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / Path(relpath).name

    if target.exists():
        data = target.read_bytes()
        actual = git_blob_sha(data)
        if actual == expected_sha:
            return data

    url = f"{RAW_BASE}/{relpath}"
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    data = response.content
    actual = git_blob_sha(data)
    if actual != expected_sha:
        raise RuntimeError(
            f"Git blob mismatch for {relpath}: expected {expected_sha}, got {actual}"
        )
    target.write_bytes(data)
    return data


def load_claims(output_dir: Path) -> tuple[list[dict[str, Any]], dict[str, str]]:
    cache = output_dir / "data_cache"
    records: list[dict[str, Any]] = []
    sha_map: dict[str, str] = {}

    for relpath, expected_sha in EXPECTED_CLAIMS.items():
        data = fetch_verified(relpath, expected_sha, cache)
        sha_map[relpath] = expected_sha
        parsed = json.loads(data.decode("utf-8"))
        if "records" not in parsed or not isinstance(parsed["records"], list):
            raise RuntimeError(f"Missing records list in {relpath}")
        records.extend(parsed["records"])

    if len(records) != 4315:
        raise RuntimeError(f"Expected 4315 claims, got {len(records)}")
    ids = [r.get("global_claim_id") for r in records]
    if len(set(ids)) != 4315:
        raise RuntimeError("global_claim_id is not unique")

    return records, sha_map


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


def detect_phenomenological_metadata(records: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Detect explicit metadata fields without using claim text itself.
    This prevents accidentally selecting claims merely because they contain
    the word 'phenomenological'.
    """
    candidates: Counter[str] = Counter()
    hits_by_key: defaultdict[str, int] = defaultdict(int)

    excluded_text_keys = {
        "claim",
        "text",
        "source_text",
        "excerpt",
        "quote",
        "description",
        "notes",
        "comment",
    }

    for r in records:
        for k, v in r.items():
            lk = k.lower()
            if lk in excluded_text_keys:
                continue
            if isinstance(v, str):
                if "phenomen" in v.lower():
                    candidates[k] += 1
                    hits_by_key[k] += 1
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, str) and "phenomen" in item.lower():
                        candidates[k] += 1
                        hits_by_key[k] += 1
            elif isinstance(v, dict):
                for sk, sv in v.items():
                    if isinstance(sv, str) and "phenomen" in sv.lower():
                        key = f"{k}.{sk}"
                        candidates[key] += 1
                        hits_by_key[key] += 1

    if not candidates:
        return {
            "mode": "ALL_CLAIMS",
            "explicit_metadata_field": None,
            "matched_records": 0,
            "note": (
                "No explicit phenomenological metadata field was detected. "
                "The discovery atlas therefore runs on all 4315 claims."
            ),
        }

    chosen = candidates.most_common(1)[0][0]
    return {
        "mode": "EXPLICIT_PHENOMENOLOGICAL_METADATA_AVAILABLE",
        "explicit_metadata_field": chosen,
        "matched_records": int(candidates[chosen]),
        "all_candidates": dict(candidates),
        "note": (
            "The runtime will still retain all claims in the graph for the "
            "main atlas; the explicit phenomenological subset is reported separately."
        ),
    }


def is_phenomenological_record(record: dict[str, Any], key: str | None) -> bool:
    if not key:
        return False
    if "." in key:
        a, b = key.split(".", 1)
        value = record.get(a)
        if isinstance(value, dict):
            value = value.get(b)
    else:
        value = record.get(key)

    values: list[str] = []
    if isinstance(value, str):
        values.append(value)
    elif isinstance(value, list):
        values.extend([x for x in value if isinstance(x, str)])

    return any("phenomen" in x.lower() for x in values)


def load_semantic_graph(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = np.load(path)
    if "indices" in data:
        indices = data["indices"]
    elif "neighbors" in data:
        indices = data["neighbors"]
    else:
        raise KeyError(f"No neighbor index array in {path}; keys={list(data.keys())}")

    if "similarities" in data:
        similarities = data["similarities"]
    elif "sims" in data:
        similarities = data["sims"]
    else:
        raise KeyError(f"No similarity array in {path}; keys={list(data.keys())}")

    indices = np.asarray(indices)
    similarities = np.asarray(similarities)

    if indices.shape != (4315, 10):
        raise RuntimeError(f"Expected indices shape (4315,10), got {indices.shape}")
    if similarities.shape != (4315, 10):
        raise RuntimeError(f"Expected similarities shape (4315,10), got {similarities.shape}")
    if indices.dtype.kind not in "iu":
        raise RuntimeError(f"Neighbor indices dtype must be integer, got {indices.dtype}")
    if not np.isfinite(similarities).all():
        raise RuntimeError("Semantic similarities contain non-finite values.")
    if not ((similarities >= -1.0001) & (similarities <= 1.0001)).all():
        raise RuntimeError("Semantic similarities are outside cosine range.")
    return indices.astype(np.int32), similarities.astype(np.float32)


def build_graph(indices: np.ndarray, similarities: np.ndarray, nx):
    g = nx.Graph()
    g.add_nodes_from(range(indices.shape[0]))

    edge_values: defaultdict[tuple[int, int], list[float]] = defaultdict(list)

    for i in range(indices.shape[0]):
        for k in range(indices.shape[1]):
            j = int(indices[i, k])
            if i == j:
                continue
            a, b = sorted((i, j))
            edge_values[(a, b)].append(float(similarities[i, k]))

    for (a, b), vals in edge_values.items():
        w = float(np.mean(vals))
        if not math.isfinite(w):
            continue
        g.add_edge(a, b, weight=w)

    return g


def shannon_normalized(counts: list[int]) -> float:
    vals = np.asarray([x for x in counts if x > 0], dtype=float)
    if len(vals) <= 1:
        return 0.0
    p = vals / vals.sum()
    return float(-(p * np.log(p)).sum() / np.log(len(p)))


def weighted_mean(values: list[float], weights: list[float]) -> float:
    if not values:
        return float("nan")
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    s = w.sum()
    return float((v * w).sum() / s) if s > 0 else float(v.mean())


def run_louvain(g, seed: int):
    from networkx.algorithms.community import louvain_communities
    communities = louvain_communities(
        g,
        weight="weight",
        resolution=LOUVAIN_RESOLUTION,
        seed=seed,
    )
    communities = sorted(
        [sorted(list(c)) for c in communities],
        key=lambda c: (-len(c), c[0] if c else -1),
    )
    assignment = {}
    for cid, members in enumerate(communities):
        for node in members:
            assignment[node] = cid
    return communities, assignment


def cluster_rows(
    communities,
    assignment,
    records,
    family_by_claim,
    graph,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = []
    reps = []
    motif_rows = []

    for cid, members in enumerate(communities):
        fam_counts = Counter(family_by_claim[i] for i in members)
        fam_values = list(fam_counts.values())
        fam_cov = len(fam_counts)
        fam_entropy = shannon_normalized(fam_values)
        max_share = max(fam_values) / len(members)

        # Internal edge similarity
        internal_weights = []
        for u, v, d in graph.subgraph(members).edges(data=True):
            internal_weights.append(float(d["weight"]))
        mean_internal = float(np.mean(internal_weights)) if internal_weights else float("nan")

        corpus_ids = {records[i]["corpus_id"] for i in members}
        summary.append(
            {
                "cluster": cid,
                "size": len(members),
                "family_coverage": fam_cov,
                "family_entropy": fam_entropy,
                "max_family_share": max_share,
                "corpus_coverage": len(corpus_ids),
                "mean_internal_similarity": mean_internal,
                "weighted_degree_total": float(sum(graph.degree(n, weight="weight") for n in members)),
            }
        )

        sg = graph.subgraph(members)
        ranked = sorted(
            members,
            key=lambda n: (
                -float(sg.degree(n, weight="weight")),
                -float(graph.degree(n, weight="weight")),
                n,
            ),
        )
        for rank, n in enumerate(ranked[:TOP_REPRESENTATIVES], start=1):
            rec = records[n]
            reps.append(
                {
                    "cluster": cid,
                    "rank": rank,
                    "claim_index": n,
                    "global_claim_id": rec.get("global_claim_id"),
                    "corpus_id": rec.get("corpus_id"),
                    "family": rec.get("family") or family_by_claim[n],
                    "claim": rec.get("claim", ""),
                    "node_weighted_degree": float(graph.degree(n, weight="weight")),
                    "cluster_weighted_degree": float(sg.degree(n, weight="weight")),
                }
            )

        motif_counts: Counter[str] = Counter()
        motif_family_units: defaultdict[str, set[str]] = defaultdict(set)
        for n in members:
            for motif in (records[n].get("motifs") or []):
                motif_counts[str(motif)] += 1
                motif_family_units[str(motif)].add(family_by_claim[n])

        for motif, count in motif_counts.most_common(TOP_MOTIFS):
            motif_rows.append(
                {
                    "cluster": cid,
                    "motif": motif,
                    "claim_support": int(count),
                    "family_support": int(len(motif_family_units[motif])),
                }
            )

    return (
        pd.DataFrame(summary).sort_values(["family_coverage", "size"], ascending=False),
        pd.DataFrame(reps),
        pd.DataFrame(motif_rows),
    )


def make_bridge_claims(indices, similarities, records, family_by_claim, assignment, graph):
    rows = []
    for i in range(len(records)):
        fam = family_by_claim[i]
        nbrs = indices[i]
        sims = similarities[i]

        eligible = [(int(n), float(s)) for n, s in zip(nbrs, sims) if family_by_claim[int(n)] != fam]
        if not eligible:
            cross_frac = 0.0
            mean_cross = float("nan")
            family_entropy = 0.0
        else:
            cross_frac = len(eligible) / len(nbrs)
            mean_cross = float(np.mean([s for _, s in eligible]))
            counts = Counter(family_by_claim[n] for n, _ in eligible)
            family_entropy = shannon_normalized(list(counts.values()))

        c = assignment[i]
        rows.append(
            {
                "claim_index": i,
                "global_claim_id": records[i].get("global_claim_id"),
                "corpus_id": records[i].get("corpus_id"),
                "family": fam,
                "cluster": c,
                "cluster_family_coverage": int(
                    len({family_by_claim[n] for n in graph.nodes if assignment[n] == c})
                ),
                "cross_family_neighbor_fraction": cross_frac,
                "cross_family_mean_cosine": mean_cross,
                "cross_family_neighbor_family_entropy": family_entropy,
                "claim": records[i].get("claim", ""),
            }
        )
    df = pd.DataFrame(rows)
    # Exploratory ranking only; not an inferential score.
    df["bridge_rank_score"] = (
        df["cross_family_neighbor_fraction"].fillna(0.0)
        * df["cross_family_neighbor_family_entropy"].fillna(0.0)
        * np.log1p(df["cluster_family_coverage"].clip(lower=1))
    )
    return df.sort_values("bridge_rank_score", ascending=False)


def lofo_transfer(indices, similarities, records, family_by_claim, base_graph, graph_module):
    import networkx as nx

    families = sorted(set(family_by_claim))
    rows = []
    fold_summaries = []

    for fold_i, heldout in enumerate(families):
        test_nodes = [i for i, f in enumerate(family_by_claim) if f == heldout]
        train_nodes = [i for i, f in enumerate(family_by_claim) if f != heldout]

        train_set = set(train_nodes)
        # Exact induced subgraph: same weighted graph as the atlas,
        # with the held-out family removed and nothing else changed.
        g_train = base_graph.subgraph(train_nodes).copy()

        communities, assignment = run_louvain(g_train, SEED + 1000 + fold_i)

        comm_family_sets = {}
        comm_sizes = {}
        for cid in set(assignment.values()):
            members = [n for n, c in assignment.items() if c == cid]
            comm_sizes[cid] = len(members)
            comm_family_sets[cid] = {family_by_claim[n] for n in members}

        strengths = []
        multi_family_receivers = 0
        with_training_neighbors = 0

        for i in test_nodes:
            masses: defaultdict[int, float] = defaultdict(float)
            n_train = 0
            for k, j0 in enumerate(indices[i]):
                j = int(j0)
                if j not in train_set:
                    continue
                n_train += 1
                c = assignment.get(j)
                if c is not None:
                    masses[c] += max(float(similarities[i, k]), 0.0)

            if not masses:
                rows.append(
                    {
                        "heldout_family": heldout,
                        "claim_index": i,
                        "global_claim_id": records[i].get("global_claim_id"),
                        "corpus_id": records[i].get("corpus_id"),
                        "n_training_neighbors": 0,
                        "top_community": None,
                        "top_community_strength": float("nan"),
                        "top_community_family_coverage": 0,
                        "top_community_size": 0,
                        "claim": records[i].get("claim", ""),
                    }
                )
                continue

            with_training_neighbors += 1
            total_mass = sum(masses.values())
            top_community, top_mass = max(masses.items(), key=lambda kv: (kv[1], -kv[0]))
            strength = float(top_mass / total_mass) if total_mass > 0 else float("nan")
            fam_cov = len(comm_family_sets.get(top_community, set()))

            strengths.append(strength)
            if fam_cov >= 2:
                multi_family_receivers += 1

            rows.append(
                {
                    "heldout_family": heldout,
                    "claim_index": i,
                    "global_claim_id": records[i].get("global_claim_id"),
                    "corpus_id": records[i].get("corpus_id"),
                    "n_training_neighbors": n_train,
                    "top_community": int(top_community),
                    "top_community_strength": strength,
                    "top_community_family_coverage": int(fam_cov),
                    "top_community_size": int(comm_sizes.get(top_community, 0)),
                    "claim": records[i].get("claim", ""),
                }
            )

        fold_summaries.append(
            {
                "heldout_family": heldout,
                "test_claims": len(test_nodes),
                "train_claims": len(train_nodes),
                "training_community_count": len(communities),
                "claims_with_training_neighbors": with_training_neighbors,
                "coverage_with_training_neighbors": (
                    with_training_neighbors / len(test_nodes) if test_nodes else float("nan")
                ),
                "mean_top_community_strength": (
                    float(np.mean(strengths)) if strengths else float("nan")
                ),
                "median_top_community_strength": (
                    float(np.median(strengths)) if strengths else float("nan")
                ),
                "fraction_receiving_multifamily_community": (
                    multi_family_receivers / with_training_neighbors
                    if with_training_neighbors
                    else float("nan")
                ),
            }
        )

    return pd.DataFrame(rows), pd.DataFrame(fold_summaries)


def main():
    ensure_package("networkx", "networkx", "3.2")
    import networkx as nx

    root = Path("/content/drive/MyDrive/Skill-Conscious")
    output_dir = root / "results/s03/S03_PHENOMENOLOGICAL_ATLAS_CPU_V1"
    output_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    semantic_path = locate_semantic_neighbors()
    semantic_bytes = semantic_path.read_bytes()

    print("=" * 70)
    print("S03 — PHENOMENOLOGICAL ATLAS + LOFO TRANSFER")
    print("=" * 70)
    print("CPU-only discovery run")
    print("No new embeddings")
    print("No T4/GPU")
    print(f"Semantic graph: {semantic_path}")

    records, ledger_shas = load_claims(output_dir)
    register_bytes = fetch_verified(SOURCE_REGISTER_PATH, SOURCE_REGISTER_SHA, output_dir / "data_cache")
    families = parse_source_families(register_bytes.decode("utf-8"))
    phenom_meta = detect_phenomenological_metadata(records)

    indices, similarities = load_semantic_graph(semantic_path)
    print(f"Claims: {len(records)}")
    print(f"Semantic edges: {indices.shape[0] * indices.shape[1]}")
    print(f"Phenomenological metadata mode: {phenom_meta['mode']}")

    family_by_claim = [families[r["corpus_id"]] for r in records]

    if len(set(family_by_claim)) != 19:
        raise RuntimeError(
            f"Expected 19 families in claim metadata, got {len(set(family_by_claim))}"
        )

    g = build_graph(indices, similarities, nx)
    print(f"Graph nodes: {g.number_of_nodes()}")
    print(f"Graph unique undirected edges: {g.number_of_edges()}")

    isolated = [n for n, d in g.degree() if d == 0]
    if isolated:
        raise RuntimeError(f"Unexpected isolated claim nodes: {len(isolated)}")

    communities, assignment = run_louvain(g, SEED)
    print(f"Louvain clusters: {len(communities)}")

    cluster_summary, representatives, cluster_motifs = cluster_rows(
        communities,
        assignment,
        records,
        family_by_claim,
        g,
    )

    cluster_assignments = pd.DataFrame(
        [
            {
                "claim_index": i,
                "global_claim_id": records[i].get("global_claim_id"),
                "corpus_id": records[i].get("corpus_id"),
                "family": family_by_claim[i],
                "cluster": assignment[i],
                "claim": records[i].get("claim", ""),
            }
            for i in range(len(records))
        ]
    )

    bridge_claims = make_bridge_claims(
        indices,
        similarities,
        records,
        family_by_claim,
        assignment,
        g,
    )

    lofo_df, lofo_summary = lofo_transfer(
        indices,
        similarities,
        records,
        family_by_claim,
        g,
        nx,
    )

    # Explicit phenomenological subset, only when metadata actually supports it.
    phenom_subset = []
    if phenom_meta["explicit_metadata_field"]:
        key = phenom_meta["explicit_metadata_field"]
        for i, r in enumerate(records):
            if is_phenomenological_record(r, key):
                phenom_subset.append(
                    {
                        "claim_index": i,
                        "global_claim_id": r.get("global_claim_id"),
                        "corpus_id": r.get("corpus_id"),
                        "family": family_by_claim[i],
                        "cluster": assignment[i],
                        "claim": r.get("claim", ""),
                    }
                )
    phenom_subset_df = pd.DataFrame(phenom_subset)

    cluster_assignments.to_csv(output_dir / "cluster_assignments.csv", index=False)
    cluster_summary.to_csv(output_dir / "cluster_summary.csv", index=False)
    cluster_representatives = representatives
    cluster_representatives.to_csv(output_dir / "cluster_representatives.csv", index=False)
    cluster_motifs.to_csv(output_dir / "cluster_motifs.csv", index=False)
    bridge_claims.to_csv(output_dir / "bridge_claims.csv", index=False)
    lofo_df.to_csv(output_dir / "lofo_transfer.csv", index=False)
    lofo_summary.to_csv(output_dir / "lofo_fold_summary.csv", index=False)
    if not phenom_subset_df.empty:
        phenom_subset_df.to_csv(output_dir / "phenomenological_subset.csv", index=False)

    modularity = float(nx.algorithms.community.quality.modularity(
        g,
        [set(c) for c in communities],
        weight="weight",
    ))

    cross_family_edges = 0
    same_family_edges = 0
    for u, v in g.edges():
        if family_by_claim[u] == family_by_claim[v]:
            same_family_edges += 1
        else:
            cross_family_edges += 1

    top_bridge = bridge_claims.head(25)[
        [
            "global_claim_id",
            "corpus_id",
            "family",
            "cluster",
            "bridge_rank_score",
            "cross_family_neighbor_fraction",
            "cross_family_mean_cosine",
            "cluster_family_coverage",
            "claim",
        ]
    ].to_dict(orient="records")

    results = {
        "study": "S03_PHENOMENOLOGICAL_ATLAS_CPU_V1",
        "status": "COMPLETE",
        "exploratory": True,
        "interpretation_limit": (
            "This is an exploratory semantic atlas. Communities are not "
            "automatically phenomenological invariants or evidence of fundamental consciousness."
        ),
        "inputs": {
            "claims": 4315,
            "families": 19,
            "semantic_edges_directed": 43150,
            "semantic_neighbors_path": str(semantic_path),
            "semantic_neighbors_sha256": sha256_bytes(semantic_bytes),
            "ledger_branch": BRANCH,
            "ledger_shas": ledger_shas,
            "source_register_sha": SOURCE_REGISTER_SHA,
            "model_name_reference": MODEL_NAME,
            "model_revision_reference": MODEL_REVISION,
            "new_embeddings": False,
        },
        "phenomenological_metadata": phenom_meta,
        "graph": {
            "nodes": g.number_of_nodes(),
            "unique_undirected_edges": g.number_of_edges(),
            "same_family_edges": same_family_edges,
            "cross_family_edges": cross_family_edges,
            "cross_family_edge_fraction": (
                cross_family_edges / g.number_of_edges()
                if g.number_of_edges() else float("nan")
            ),
        },
        "louvain": {
            "seed": SEED,
            "resolution": LOUVAIN_RESOLUTION,
            "cluster_count": len(communities),
            "modularity": modularity,
        },
        "atlas": {
            "largest_cluster": int(max(len(c) for c in communities)),
            "smallest_cluster": int(min(len(c) for c in communities)),
            "clusters_with_3plus_families": int(
                (cluster_summary["family_coverage"] >= 3).sum()
            ),
            "clusters_with_5plus_families": int(
                (cluster_summary["family_coverage"] >= 5).sum()
            ),
            "top_bridge_claims": top_bridge,
        },
        "lofo": {
            "folds": int(len(lofo_summary)),
            "mean_coverage_with_training_neighbors": float(
                lofo_summary["coverage_with_training_neighbors"].mean()
            ),
            "mean_top_community_strength": float(
                lofo_summary["mean_top_community_strength"].mean()
            ),
            "mean_fraction_multifamily_receiver": float(
                lofo_summary["fraction_receiving_multifamily_community"].mean()
            ),
        },
        "phenomenological_subset": {
            "available": bool(not phenom_subset_df.empty),
            "claims": int(len(phenom_subset_df)),
        },
        "elapsed_min": (time.time() - t0) / 60.0,
    }

    (output_dir / "schema_audit.json").write_text(
        json.dumps(
            {
                "record_count": len(records),
                "record_keys_union": sorted(
                    {k for r in records for k in r.keys()}
                ),
                "phenomenological_metadata": phenom_meta,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    (output_dir / "run_manifest.json").write_text(
        json.dumps(
            {
                "study": "S03_PHENOMENOLOGICAL_ATLAS_CPU_V1",
                "seed": SEED,
                "louvain_resolution": LOUVAIN_RESOLUTION,
                "top_representatives": TOP_REPRESENTATIVES,
                "top_motifs": TOP_MOTIFS,
                "semantic_neighbors": str(semantic_path),
                "semantic_neighbors_sha256": sha256_bytes(semantic_bytes),
                "ledger_branch": BRANCH,
                "ledger_blob_sha": ledger_shas,
                "source_register_sha": SOURCE_REGISTER_SHA,
                "new_embeddings": False,
                "gpu_used": False,
                "python": platform.python_version(),
                "platform": platform.platform(),
                "networkx": nx.__version__,
                "numpy": np.__version__,
                "pandas": pd.__version__,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    (output_dir / "S03_PHENOMENOLOGICAL_ATLAS_RESULTS_V1.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 70)
    print("S03 COMPLETE")
    print("=" * 70)
    print(f"Clusters: {len(communities)}")
    print(f"Modularity: {modularity:.6f}")
    print(
        "Clusters with >=3 families:",
        int((cluster_summary["family_coverage"] >= 3).sum()),
    )
    print(
        "Clusters with >=5 families:",
        int((cluster_summary["family_coverage"] >= 5).sum()),
    )
    print(
        "LOFO mean training-neighbor coverage:",
        float(lofo_summary["coverage_with_training_neighbors"].mean()),
    )
    print(
        "LOFO mean top-community strength:",
        float(lofo_summary["mean_top_community_strength"].mean()),
    )
    print(
        "LOFO mean multi-family receiver fraction:",
        float(lofo_summary["fraction_receiving_multifamily_community"].mean()),
    )
    print(f"Phenomenological subset available: {not phenom_subset_df.empty}")
    print(f"Output: {output_dir / 'S03_PHENOMENOLOGICAL_ATLAS_RESULTS_V1.json'}")
    print(f"Elapsed min: {(time.time() - t0) / 60.0:.2f}")
    print()
    print("Guardrail: this is discovery, not confirmatory evidence.")


if __name__ == "__main__":
    main()
