#!/usr/bin/env python3
"""
S03.10 — Full 67 multifamily candidate export.

Reads the frozen S03.6/S03.7 outputs and exports all 67 multifamily
phenomenology candidates, while marking the 31 already reviewed priority claims.

No GPU, embeddings, inference, or classification.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
IN = ROOT / "results/s03/S03_CANDIDATE_ADJUDICATION_CPU_V1/all_adjudication_candidates.csv"
OUT = ROOT / "results/s03/S03_MULTIFAMILY_FULL_EXPORT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    if not IN.exists():
        raise FileNotFoundError(IN)

    df = pd.read_csv(IN)
    required = {
        "claim_index",
        "global_claim_id",
        "corpus_id",
        "candidate_family",
        "candidate_cluster",
        "seed_family_coverage",
        "seed_families",
        "best_seed_global_claim_id",
        "best_seed_family",
        "best_seed_similarity",
        "seed_connection_count",
        "candidate_claim",
        "best_seed_claim",
    }
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns: {sorted(missing)}")

    multi = df[df["seed_family_coverage"] >= 2].copy()
    priority = (
        multi.sort_values(
            ["seed_family_coverage", "best_seed_similarity", "seed_connection_count"],
            ascending=[False, False, False],
        )
        .head(31)
    )

    reviewed_ids = set(priority["global_claim_id"].astype(str))

    multi["priority_31_reviewed"] = (
        multi["global_claim_id"].astype(str).isin(reviewed_ids)
    )

    multi["review_order_full67"] = range(1, len(multi) + 1)

    multi = multi.sort_values(
        ["priority_31_reviewed", "seed_family_coverage", "best_seed_similarity", "seed_connection_count"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)

    multi["review_batch"] = multi["priority_31_reviewed"].map(
        {True: "already_reviewed_priority31", False: "remaining36"}
    )

    cols = [
        "review_order_full67",
        "review_batch",
        "global_claim_id",
        "corpus_id",
        "candidate_family",
        "candidate_cluster",
        "seed_family_coverage",
        "seed_families",
        "best_seed_global_claim_id",
        "best_seed_family",
        "best_seed_similarity",
        "seed_connection_count",
        "candidate_claim",
        "best_seed_claim",
    ]

    multi[cols].to_csv(
        OUT / "all_67_multifamily_candidates_complete.csv",
        index=False,
    )

    remaining = multi[~multi["priority_31_reviewed"]].copy()
    remaining[cols].to_csv(
        OUT / "remaining_36_candidates.csv",
        index=False,
    )

    lines = []
    lines.append("=" * 100)
    lines.append("S03.10 — REMAINING 36 MULTIFAMILY CANDIDATES")
    lines.append("=" * 100)
    lines.append(
        "These are the 36 candidates not included in the original priority-31 readout."
    )
    lines.append("")

    for i, (_, r) in enumerate(remaining.iterrows(), start=1):
        lines.append(
            f"#{i} | {r['global_claim_id']} | {r['corpus_id']} | FAMILY={r['candidate_family']}"
        )
        lines.append(
            f"SEED-FAMILIES ({int(r['seed_family_coverage'])}): {r['seed_families']}"
        )
        lines.append(
            f"BEST-SEED: {r['best_seed_global_claim_id']} | "
            f"{r['best_seed_family']} | sim={float(r['best_seed_similarity']):.6f} | "
            f"connections={int(r['seed_connection_count'])}"
        )
        lines.append("CLAIM:")
        lines.append(str(r["candidate_claim"]))
        lines.append("SEED CLAIM:")
        lines.append(str(r["best_seed_claim"]))
        lines.append("-" * 100)

    (OUT / "S03.10_REMAINING_36_CLAIMS.txt").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    manifest = {
        "study": "S03.10_MULTIFAMILY_FULL_EXPORT_CPU_V1",
        "all_multifamily_candidates": int(len(multi)),
        "priority_reviewed": int(multi["priority_31_reviewed"].sum()),
        "remaining_unreviewed": int((~multi["priority_31_reviewed"]).sum()),
        "gpu_used": False,
        "new_embeddings": False,
        "purpose": "Complete the human adjudication pool before any convergence claim.",
    }

    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 100)
    print("S03.10 COMPLETE")
    print("=" * 100)
    print("All multifamily candidates:", len(multi))
    print("Priority 31:", int(multi["priority_31_reviewed"].sum()))
    print("Remaining 36:", int((~multi["priority_31_reviewed"]).sum()))
    print("Output:", OUT)
    print("=" * 100)

if __name__ == "__main__":
    main()
