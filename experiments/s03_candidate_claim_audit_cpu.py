#!/usr/bin/env python3
"""
S03.2 — Candidate claim audit.

Reads existing S03/S03.1 outputs only.
No embeddings, no GPU, no inference.

Purpose:
- identify the two (or any) candidate cross-family phenomenological clusters;
- print every phenomenological claim in those clusters;
- show family/corpus/source identifiers;
- show motifs if available;
- show cluster-level family composition;
- produce a compact human-readable report for manual scientific interpretation.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
S03 = ROOT / "results/s03/S03_PHENOMENOLOGICAL_ATLAS_CPU_V1"
S031 = ROOT / "results/s03/S03_ATLAS_INTERPRETATION_CPU_V1"
OUT = ROOT / "results/s03/S03_CANDIDATE_CLAIM_AUDIT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

REQ_S03 = [
    "cluster_assignments.csv",
    "cluster_representatives.csv",
    "cluster_motifs.csv",
]
REQ_S031 = [
    "candidate_cross_family_phenomenological_clusters.csv",
    "cluster_content_atlas.csv",
]
PHEN = S03 / "phenomenological_subset.csv"

def check():
    miss = [f for f in REQ_S03 if not (S03 / f).exists()]
    miss += [f for f in REQ_S031 if not (S031 / f).exists()]
    if not PHEN.exists():
        miss.append(str(PHEN))
    if miss:
        raise FileNotFoundError("Missing artifacts: " + repr(miss))

def main():
    check()

    assignments = pd.read_csv(S03 / "cluster_assignments.csv")
    reps = pd.read_csv(S03 / "cluster_representatives.csv")
    motifs = pd.read_csv(S03 / "cluster_motifs.csv")
    phen = pd.read_csv(PHEN)
    candidates = pd.read_csv(S031 / "candidate_cross_family_phenomenological_clusters.csv")
    atlas = pd.read_csv(S031 / "cluster_content_atlas.csv")

    candidate_ids = [int(x) for x in candidates["cluster"].tolist()]

    # Exact family composition from all claims.
    family_matrix = pd.crosstab(assignments["cluster"], assignments["family"])

    # Phenomenological claims in candidates.
    selected = phen[phen["cluster"].isin(candidate_ids)].copy()

    # Add motifs for each claim by joining back to original claim ledger is
    # intentionally avoided here: the S03 output does not carry per-claim motifs.
    # We therefore report cluster-level motifs separately, preserving source fidelity.

    selected = selected.sort_values(
        ["cluster", "family", "corpus_id", "global_claim_id"]
    )
    selected.to_csv(OUT / "candidate_phenomenological_claims.csv", index=False)

    lines = []
    lines.append("=" * 80)
    lines.append("S03.2 — CANDIDATE PHENOMENOLOGICAL CLAIM AUDIT")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Candidate clusters: {len(candidate_ids)}")
    lines.append(f"Phenomenological claims in candidates: {len(selected)}")
    lines.append("")

    for cid in candidate_ids:
        c_all = assignments[assignments["cluster"] == cid]
        c_ph = selected[selected["cluster"] == cid]
        c_reps = reps[reps["cluster"] == cid]
        c_m = motifs[motifs["cluster"] == cid]
        c_atlas = atlas[atlas["cluster"] == cid]

        lines.append("#" * 80)
        lines.append(f"CLUSTER {cid}")
        lines.append("#" * 80)

        if not c_atlas.empty:
            a = c_atlas.iloc[0]
            lines.append(f"All claims: {int(a['claims'])}")
            lines.append(f"Family coverage: {int(a['family_coverage'])}")
            lines.append(f"Phenomenological claims: {int(a['phenomenological_claims'])}")
            lines.append(f"Phenomenological family coverage: {int(a['phenomenological_family_coverage'])}")

        fam_all = Counter(c_all["family"])
        fam_ph = Counter(c_ph["family"])
        lines.append("")
        lines.append("ALL-CLAIM FAMILY COMPOSITION:")
        for f, n in fam_all.most_common():
            lines.append(f"  {f}: {n}")

        lines.append("")
        lines.append("PHENOMENOLOGICAL FAMILY COMPOSITION:")
        for f, n in fam_ph.most_common():
            lines.append(f"  {f}: {n}")

        lines.append("")
        lines.append("TOP CLUSTER MOTIFS:")
        if c_m.empty:
            lines.append("  [none]")
        else:
            for _, r in c_m.head(15).iterrows():
                lines.append(
                    f"  {r['motif']} | claim_support={int(r['claim_support'])} | family_support={int(r['family_support'])}"
                )

        lines.append("")
        lines.append("REPRESENTATIVE CLAIMS:")
        for _, r in c_reps.head(7).iterrows():
            lines.append(f"  [{r['family']}] {r['claim']}")

        lines.append("")
        lines.append("PHENOMENOLOGICAL CLAIMS — FULL:")
        for i, (_, r) in enumerate(c_ph.iterrows(), start=1):
            lines.append(
                f"  {i:03d}. [{r['family']}] "
                f"{r['global_claim_id']} | {r['corpus_id']}"
            )
            lines.append(f"       {r['claim']}")

        lines.append("")

    report = "\n".join(lines)
    (OUT / "S03_CANDIDATE_CLAIM_AUDIT_REPORT_V1.txt").write_text(
        report, encoding="utf-8"
    )

    summary = {
        "candidate_clusters": candidate_ids,
        "phenomenological_claims_in_candidates": int(len(selected)),
        "output_dir": str(OUT),
        "files": {
            "report": str(OUT / "S03_CANDIDATE_CLAIM_AUDIT_REPORT_V1.txt"),
            "claims_csv": str(OUT / "candidate_phenomenological_claims.csv"),
        },
    }
    (OUT / "run_manifest.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(report)
    print("")
    print("=" * 80)
    print("✅ S03.2 COMPLETE")
    print("=" * 80)
    print(f"Report: {OUT / 'S03_CANDIDATE_CLAIM_AUDIT_REPORT_V1.txt'}")
    print(f"CSV:    {OUT / 'candidate_phenomenological_claims.csv'}")

if __name__ == "__main__":
    main()
