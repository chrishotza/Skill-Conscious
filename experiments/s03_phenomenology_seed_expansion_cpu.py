#!/usr/bin/env python3
"""
S03.5 — Phenomenology seed expansion from the frozen semantic graph.

Purpose
-------
The explicit phenomenological metadata inventory contains only 53 claims across
4 families / 5 corpus units. Before concluding that the corpus lacks direct
phenomenology, use those 53 metadata-tagged claims as transparent seeds and
retrieve nearby untagged claims from the already-frozen S01 semantic graph.

This is NOT classification. It is candidate generation for manual adjudication.

No new embeddings. No GPU. No external model inference.

For every untagged claim, compute:
- max cosine to an explicit phenomenology seed over the frozen graph
- mean cosine to connected phenomenology seeds
- number of seed connections
- seed-family coverage
- whether any seed connection is cross-family
- best seed claim identity

Outputs are ranked candidate queues for S03.6.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
S03 = ROOT / "results/s03/S03_EXHAUSTIVE_PHENOMENOLOGY_INVENTORY_CPU_V1"
S01 = ROOT / "results/s01/S01_CONFIRMATORY_T4_V1"
OUT = ROOT / "results/s03/S03_PHENOMENOLOGY_SEED_EXPANSION_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

TAGGED = S03 / "all_tagged_phenomenological_claims.csv"
ALL_CLAIMS = ROOT / "results/s03/S03_PHENOMENOLOGICAL_ATLAS_CPU_V1/cluster_assignments.csv"
NEIGHBORS = S01 / "semantic_neighbors.npz"

def main():
    if not TAGGED.exists():
        raise FileNotFoundError(TAGGED)
    if not NEIGHBORS.exists():
        raise FileNotFoundError(NEIGHBORS)
    if not ALL_CLAIMS.exists():
        raise FileNotFoundError(ALL_CLAIMS)

    tagged = pd.read_csv(TAGGED)
    all_claims = pd.read_csv(ALL_CLAIMS).set_index("claim_index")
    data = np.load(NEIGHBORS)
    indices = data["indices"].astype(np.int32)
    sims = data["similarities"].astype(np.float32)

    n = indices.shape[0]
    if indices.shape != (4315, 10):
        raise RuntimeError(f"Unexpected neighbor shape: {indices.shape}")

    seed_indices = set(tagged["claim_index"].astype(int).tolist())
    if not seed_indices:
        raise RuntimeError("No phenomenological seeds found.")

    seed_family = {
        int(r.claim_index): str(r.family)
        for _, r in tagged.iterrows()
    }
    seed_id = {
        int(r.claim_index): str(r.global_claim_id)
        for _, r in tagged.iterrows()
    }
    seed_claim = {
        int(r.claim_index): str(r.claim)
        for _, r in tagged.iterrows()
    }

    # Gather directed and reverse graph connections involving a seed.
    connections = defaultdict(list)

    for q in range(n):
        for k in range(indices.shape[1]):
            j = int(indices[q, k])
            s = float(sims[q, k])

            if q in seed_indices and j not in seed_indices:
                connections[j].append((q, s, "seed_to_candidate"))
            elif j in seed_indices and q not in seed_indices:
                connections[q].append((j, s, "candidate_to_seed"))

    rows = []

    for candidate, edges in connections.items():
        if candidate in seed_indices:
            continue

        weights = np.asarray([x[1] for x in edges], dtype=float)
        best_pos = int(np.argmax(weights))
        best_seed, best_sim, direction = edges[best_pos]

        families = sorted({seed_family[s] for s, _, _ in edges})
        candidate_row = all_claims.loc[int(candidate)]

        rows.append({
            "claim_index": int(candidate),
            "global_claim_id": str(candidate_row["global_claim_id"]),
            "corpus_id": str(candidate_row["corpus_id"]),
            "candidate_family": str(candidate_row["family"]),
            "candidate_cluster": int(candidate_row["cluster"]),
            "candidate_claim": str(candidate_row["claim"]),
            "best_seed_index": int(best_seed),
            "best_seed_global_claim_id": seed_id[best_seed],
            "best_seed_family": seed_family[best_seed],
            "best_seed_similarity": float(best_sim),
            "mean_seed_similarity": float(weights.mean()),
            "seed_connection_count": int(len(edges)),
            "seed_family_coverage": int(len(families)),
            "seed_families": ";".join(families),
            "connection_direction_best": direction,
            "best_seed_claim": seed_claim[best_seed],
        })

    ranked = pd.DataFrame(rows)

    if ranked.empty:
        raise RuntimeError("No untagged one-hop phenomenology candidates found.")

    ranked = ranked.sort_values(
        ["seed_family_coverage", "best_seed_similarity", "seed_connection_count"],
        ascending=[False, False, False],
    )

    ranked.to_csv(OUT / "phenomenology_expansion_candidates.csv", index=False)

    top_by_coverage = ranked[ranked["seed_family_coverage"] >= 2].copy()
    top_by_coverage.head(300).to_csv(
        OUT / "top_300_multifamily_seed_candidates.csv",
        index=False,
    )

    top_by_similarity = ranked.sort_values(
        ["best_seed_similarity", "seed_connection_count"],
        ascending=[False, False],
    )
    top_by_similarity.head(300).to_csv(
        OUT / "top_300_similarity_candidates.csv",
        index=False,
    )

    manifest = {
        "study": "S03.5_PHENOMENOLOGY_SEED_EXPANSION_CPU_V1",
        "claims": 4315,
        "seed_claims": int(len(seed_indices)),
        "all_claim_source": str(ALL_CLAIMS),
        "seed_families": int(tagged["family"].nunique()),
        "candidate_claims_with_seed_connection": int(len(ranked)),
        "multifamily_seed_candidate_claims": int((ranked["seed_family_coverage"] >= 2).sum()),
        "gpu_used": False,
        "new_embeddings": False,
        "important_limit": (
            "Candidate generation only. Semantic proximity to metadata-tagged "
            "claims does not establish phenomenological content."
        ),
    }

    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("S03.5 — PHENOMENOLOGY SEED EXPANSION")
    print("=" * 80)
    print("Seed claims:", len(seed_indices))
    print("Seed families:", tagged["family"].nunique())
    print("Candidate claims with a seed connection:", len(ranked))
    print(
        "Candidates connected to >=2 seed families:",
        int((ranked["seed_family_coverage"] >= 2).sum()),
    )
    print("Output:", OUT)
    print("No embeddings generated; frozen S01 neighbor graph reused.")
    print("=" * 80)

if __name__ == "__main__":
    main()
