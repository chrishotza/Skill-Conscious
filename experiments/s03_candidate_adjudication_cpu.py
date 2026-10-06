#!/usr/bin/env python3
"""
S03.6 — Candidate phenomenology adjudication queue.

Reads the frozen S03.5 seed-expansion output and creates a transparent
manual-adjudication queue.

Important:
- 802 claims have at least one connection to the 53 explicit seeds.
- 67 connect to seeds from >=2 families.
- This script does NOT classify them automatically.
- It creates ranked batches for review and stratified sampling.
- No GPU, embeddings, or external inference.

Adjudication classes:
P1 direct phenomenological structure
P2 theoretical phenomenology
M1 meta/epistemic
O1 ontological/metaphysical
H1 historical/bibliographic
N1 comparative/methodological
U1 ambiguous/mixed
X1 irrelevant semantic proximity / non-phenomenological
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
S35 = ROOT / "results/s03/S03_PHENOMENOLOGY_SEED_EXPANSION_CPU_V1"
OUT = ROOT / "results/s03/S03_CANDIDATE_ADJUDICATION_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

INPUT = S35 / "phenomenology_expansion_candidates.csv"

CLASSES = [
    "P1",
    "P2",
    "M1",
    "O1",
    "H1",
    "N1",
    "U1",
    "X1",
]

def main():
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    df = pd.read_csv(INPUT)

    required = {
        "claim_index",
        "global_claim_id",
        "corpus_id",
        "candidate_family",
        "candidate_cluster",
        "candidate_claim",
        "best_seed_global_claim_id",
        "best_seed_family",
        "best_seed_similarity",
        "mean_seed_similarity",
        "seed_connection_count",
        "seed_family_coverage",
        "seed_families",
        "best_seed_claim",
    }
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns: {sorted(missing)}")

    # Stable ranking: prioritize multi-family seed convergence, then similarity,
    # then number of independent seed links.
    df = df.sort_values(
        ["seed_family_coverage", "best_seed_similarity", "seed_connection_count"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    df["review_order"] = range(1, len(df) + 1)

    # Manual annotation fields intentionally blank.
    df["adjudication"] = ""
    df["reviewer_note"] = ""
    df["retain_for_strict_atlas"] = ""
    df["possible_phenomenological_dimensions"] = ""

    df.to_csv(OUT / "all_adjudication_candidates.csv", index=False)

    multi = df[df["seed_family_coverage"] >= 2].copy()

    # Diverse review queue:
    # top 10 for each seed-family coverage level, plus top similarity rows.
    queues = []

    for coverage in sorted(multi["seed_family_coverage"].unique(), reverse=True):
        sub = multi[multi["seed_family_coverage"] == coverage].head(15).copy()
        sub["queue"] = f"coverage_{coverage}"
        queues.append(sub)

    sim = multi.sort_values(
        ["best_seed_similarity", "seed_connection_count"],
        ascending=[False, False],
    ).head(30).copy()
    sim["queue"] = "top_similarity"
    queues.append(sim)

    queue = pd.concat(queues, ignore_index=True).drop_duplicates("claim_index")
    queue = queue.sort_values(
        ["seed_family_coverage", "best_seed_similarity", "seed_connection_count"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    queue["review_batch_order"] = range(1, len(queue) + 1)
    queue.to_csv(OUT / "priority_review_queue.csv", index=False)

    # Family-pair table for candidate connectivity.
    pair_rows = []
    for _, row in multi.iterrows():
        fams = [x for x in str(row["seed_families"]).split(";") if x]
        for i, a in enumerate(fams):
            for b in fams[i + 1:]:
                pair_rows.append({
                    "claim_index": int(row["claim_index"]),
                    "candidate_family": row["candidate_family"],
                    "family_a": a,
                    "family_b": b,
                    "best_seed_similarity": float(row["best_seed_similarity"]),
                    "seed_connection_count": int(row["seed_connection_count"]),
                    "claim": row["candidate_claim"],
                })

    pair_df = pd.DataFrame(pair_rows)
    if not pair_df.empty:
        pair_summary = (
            pair_df.groupby(["family_a", "family_b"])
            .agg(
                candidate_claims=("claim_index", "nunique"),
                mean_similarity=("best_seed_similarity", "mean"),
            )
            .reset_index()
            .sort_values("candidate_claims", ascending=False)
        )
    else:
        pair_summary = pd.DataFrame()

    pair_df.to_csv(OUT / "candidate_family_pairs.csv", index=False)
    pair_summary.to_csv(OUT / "candidate_family_pair_summary.csv", index=False)

    # Blank adjudication template with explicit rules.
    rules = OUT / "ADJUDICATION_RULES_V1.md"
    rules.write_text(
        """# S03.6 Candidate Adjudication Rules

## P1 — Direct phenomenological structure
Use only when the claim describes organization of experience itself:
perception, lived experience, attention, self-awareness, subjectivity,
embodiment, first-person structure, experienced relation to world/other,
or state-transition structure.

## P2 — Theoretical phenomenology
Use when the claim is a theory/model about phenomenological organization,
but not a direct description of experience.

## M1 — Meta/epistemic
Use for claims about evidence, explanatory gaps, scientific status,
interpretation, methodology, or limitations of language.

## O1 — Ontological/metaphysical
Use for claims about what consciousness/reality fundamentally is.

## H1 — Historical/bibliographic
Use for provenance, publication, historical context, or attribution.

## N1 — Comparative/methodological
Use for instructions or methods for comparing traditions.

## U1 — Ambiguous/mixed
Use when the claim genuinely combines categories and cannot be assigned
without forcing an interpretation.

## X1 — Irrelevant semantic proximity
Use when semantic similarity to a seed does not correspond to phenomenological
content.

### Strict rule
Only P1 enters a future strict phenomenological-invariant atlas.
P2 is retained as theoretical context.
M1/O1/H1/N1/U1/X1 are excluded from the strict P1 set.
""",
        encoding="utf-8",
    )

    manifest = {
        "study": "S03.6_CANDIDATE_ADJUDICATION_CPU_V1",
        "input": str(INPUT),
        "all_candidates": int(len(df)),
        "multifamily_candidates": int(len(multi)),
        "priority_review_queue": int(len(queue)),
        "classes": CLASSES,
        "gpu_used": False,
        "new_embeddings": False,
        "purpose": "Manual adjudication queue, not automatic classification.",
    }

    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("S03.6 — CANDIDATE PHENOMENOLOGY ADJUDICATION QUEUE")
    print("=" * 80)
    print("All seed-connected candidates:", len(df))
    print("Candidates with >=2 seed families:", len(multi))
    print("Priority review queue:", len(queue))
    print("Output:", OUT)
    print()
    print("Top family pairs:")
    if pair_summary.empty:
        print("  none")
    else:
        print(pair_summary.head(15).to_string(index=False))
    print("=" * 80)

if __name__ == "__main__":
    main()
