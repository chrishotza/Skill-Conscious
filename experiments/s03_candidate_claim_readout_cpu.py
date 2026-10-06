#!/usr/bin/env python3
"""
S03.7 — Candidate claim readout.

Reads the S03.6 candidate queue and produces a complete human-readable audit
of the 31 priority candidates, plus all 67 multifamily candidates grouped by
seed-family combination.

No embeddings, no GPU, no automatic adjudication.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
S36 = ROOT / "results/s03/S03_CANDIDATE_ADJUDICATION_CPU_V1"
OUT = ROOT / "results/s03/S03_CANDIDATE_CLAIM_READOUT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

QUEUE = S36 / "priority_review_queue.csv"
ALL = S36 / "all_adjudication_candidates.csv"
PAIRS = S36 / "candidate_family_pairs.csv"
PAIR_SUMMARY = S36 / "candidate_family_pair_summary.csv"

def main():
    for p in [QUEUE, ALL, PAIRS, PAIR_SUMMARY]:
        if not p.exists():
            raise FileNotFoundError(p)

    queue = pd.read_csv(QUEUE)
    all_candidates = pd.read_csv(ALL)
    pairs = pd.read_csv(PAIRS)
    pair_summary = pd.read_csv(PAIR_SUMMARY)

    queue = queue.sort_values(
        ["seed_family_coverage", "best_seed_similarity", "seed_connection_count"],
        ascending=[False, False, False],
    )

    all_multi = all_candidates[
        all_candidates["seed_family_coverage"] >= 2
    ].copy()

    queue_out = queue.copy()
    queue_out.to_csv(OUT / "priority_31_claims.csv", index=False)
    all_multi.to_csv(OUT / "all_67_multifamily_candidates.csv", index=False)
    pair_summary.to_csv(OUT / "family_pair_summary.csv", index=False)

    lines = []
    lines.append("=" * 90)
    lines.append("S03.7 — PRIORITY CANDIDATE CLAIM READOUT")
    lines.append("=" * 90)
    lines.append("")
    lines.append(
        "Purpose: inspect the actual claim text before any phenomenological adjudication."
    )
    lines.append("No automatic classification is performed.")
    lines.append("")
    lines.append(f"Priority queue: {len(queue)}")
    lines.append(f"All multifamily candidates: {len(all_multi)}")
    lines.append("")

    lines.append("TOP SEED-FAMILY PAIRS")
    lines.append("-" * 90)
    for _, r in pair_summary.iterrows():
        lines.append(
            f"{r['family_a']} <-> {r['family_b']} | "
            f"claims={int(r['candidate_claims'])} | "
            f"mean_similarity={float(r['mean_similarity']):.6f}"
        )
    lines.append("")

    lines.append("PRIORITY CANDIDATES")
    lines.append("-" * 90)

    for _, r in queue.iterrows():
        lines.append("")
        lines.append(
            f"#{int(r['review_batch_order'])} | "
            f"{r['global_claim_id']} | "
            f"{r['corpus_id']} | "
            f"candidate_family={r['candidate_family']}"
        )
        lines.append(
            f"seed_family_coverage={int(r['seed_family_coverage'])} | "
            f"seed_families={r['seed_families']}"
        )
        lines.append(
            f"best_seed={r['best_seed_global_claim_id']} | "
            f"best_seed_family={r['best_seed_family']} | "
            f"best_similarity={float(r['best_seed_similarity']):.6f}"
        )
        lines.append(
            f"seed_connections={int(r['seed_connection_count'])} | "
            f"candidate_cluster={int(r['candidate_cluster'])}"
        )
        lines.append("CLAIM:")
        lines.append(str(r["candidate_claim"]))
        lines.append("BEST SEED CLAIM:")
        lines.append(str(r["best_seed_claim"]))
        lines.append("-" * 90)

    (OUT / "S03.7_PRIORITY_CANDIDATE_READOUT_V1.txt").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    # Family-pair grouped candidate readout.
    pair_lines = []
    pair_lines.append("=" * 90)
    pair_lines.append("S03.7 — MULTIFAMILY CANDIDATES BY SEED-FAMILY PAIR")
    pair_lines.append("=" * 90)

    for _, p in pair_summary.iterrows():
        a = p["family_a"]
        b = p["family_b"]
        subset = pairs[
            (pairs["family_a"] == a) &
            (pairs["family_b"] == b)
        ].sort_values(
            ["best_seed_similarity", "seed_connection_count"],
            ascending=[False, False],
        )

        pair_lines.append("")
        pair_lines.append("#" * 90)
        pair_lines.append(
            f"{a} <-> {b} | claims={len(subset)} | "
            f"mean_similarity={float(p['mean_similarity']):.6f}"
        )
        pair_lines.append("#" * 90)

        # Deduplicate because one candidate can occur in multiple pair rows.
        seen = set()
        for _, r in subset.iterrows():
            cid = int(r["claim_index"])
            if cid in seen:
                continue
            seen.add(cid)
            pair_lines.append("")
            pair_lines.append(
                f"{r['global_claim_id']} | {r['corpus_id']} | "
                f"candidate_family={r['candidate_family']}"
            )
            pair_lines.append(f"claim: {r['claim']}")
            pair_lines.append(
                f"similarity={float(r['best_seed_similarity']):.6f} | "
                f"seed_connections={int(r['seed_connection_count'])}"
            )

    (OUT / "S03.7_FAMILY_PAIR_READOUT_V1.txt").write_text(
        "\n".join(pair_lines),
        encoding="utf-8",
    )

    manifest = {
        "study": "S03.7_CANDIDATE_CLAIM_READOUT_CPU_V1",
        "priority_claims": int(len(queue)),
        "multifamily_claims": int(len(all_multi)),
        "gpu_used": False,
        "new_embeddings": False,
        "automatic_adjudication": False,
    }

    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 90)
    print("S03.7 COMPLETE")
    print("=" * 90)
    print("Priority claims:", len(queue))
    print("Multifamily candidates:", len(all_multi))
    print("Output:", OUT)
    print()
    print("Top family pairs:")
    print(pair_summary.to_string(index=False))
    print("=" * 90)

if __name__ == "__main__":
    main()
